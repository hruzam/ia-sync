#!/usr/bin/env python3
"""
palette-map-gen.py — rerunnable generator for palette.map

Scans a zsh config tree (keyboard.zsh control panels + scope engines) and
emits a TSV manifest consumed by the command-palette TUI.

STDLIB ONLY. Read-only except for writing <root>/palette.map. No network,
no subprocess calls into the shell configs — pure text parsing.

Usage:
    python3 palette-map-gen.py [--root <path>]

Default root: two directories up from this script's own location
(script lives at <root>/ai/palette-map-gen.py).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# --------------------------------------------------------------------------
# Config
# --------------------------------------------------------------------------

# Registry: operator-maintainable folder list, resolved relative to --root.
# registries/palette.json — see that file's "comment" field for the contract.
REGISTRY_REL_PATH = "registries/palette.json"

# Built-in fallback, used only when the registry is missing/unparseable
# (matches the pre-registry behavior of this generator).
DEFAULT_SCAN_DIRS = ["ai", "system", "projects", "piql", "sync", "archx", "nablarva"]
DEFAULT_ROOT_FILES = [
    "config.home.zsh",
    "config.office.zsh",
    "project-switcher.zsh",
    "git-lifecycle.zsh",
    "krfb.zsh",
    "session-meassure.zsh",
    "shared-toolkit.zsh",
]
DEFAULT_EXCLUDED: list[str] = []

# Top-level folders that are never command sources (retired, data-only, or
# fixtures) — excluded from both scanning and the "unregistered folder"
# check, regardless of registry contents.
NEVER_SCAN_DIRS = {
    "archive", "blessings", "guides", "registries", ".git", ".codex", ".env",
}

# Files whose top-level content is pure control-panel (aliases + comments,
# bodies live elsewhere) — the "keyboard.zsh" convention.
KEYBOARD_FILENAME = "keyboard.zsh"


def load_registry(root: Path) -> tuple[list[str], list[str], list[str]]:
    """
    Returns (scan_dirs, root_files, excluded). Reads registries/palette.json
    relative to root; falls back to the built-in defaults (with a stderr
    warning) if the registry is missing or unparseable. Never raises.
    """
    reg_path = root / REGISTRY_REL_PATH
    if not reg_path.is_file():
        print(f"warning: registry not found at {reg_path} — using built-in defaults",
              file=sys.stderr)
        return list(DEFAULT_SCAN_DIRS), list(DEFAULT_ROOT_FILES), list(DEFAULT_EXCLUDED)

    try:
        data = json.loads(reg_path.read_text(encoding="utf-8"))
        scopes = data["scopes"]
        root_files = data.get("root_files", [])
        excluded = data.get("excluded", [])
        if not isinstance(scopes, list) or not all(isinstance(s, str) for s in scopes):
            raise ValueError("'scopes' must be a list of strings")
        if not isinstance(root_files, list) or not all(isinstance(s, str) for s in root_files):
            raise ValueError("'root_files' must be a list of strings")
        if not isinstance(excluded, list) or not all(isinstance(s, str) for s in excluded):
            raise ValueError("'excluded' must be a list of strings")
        return list(scopes), list(root_files), list(excluded)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"warning: registry at {reg_path} is unparseable ({exc}) — "
              f"using built-in defaults", file=sys.stderr)
        return list(DEFAULT_SCAN_DIRS), list(DEFAULT_ROOT_FILES), list(DEFAULT_EXCLUDED)

ALIAS_RE = re.compile(
    r"""^\s*alias\s+
        (?P<name>[A-Za-z0-9_-]+)
        =
        (?:
            '(?P<sq>[^']*)'
          | "(?P<dq>[^"]*)"
          | (?P<bare>\S+)
        )
        \s*(?:\#\s*(?P<comment>.*))?\s*$
    """,
    re.VERBOSE,
)

# Matches both multi-line ("name() {" then body on following lines) and
# one-liner ("name()  { body }") function definitions.
# Leading char allows a digit (2026-09-22, one-char widen): zsh itself places
# no such restriction on function names (unlike shell variable/identifier
# rules) — "4x1() { ... }" is a valid zsh function def. Widening only ADDS
# matches, never removes one, so this cannot regress any currently-passing
# scope; verified via a full-tree regen (see palette-map-gen.py --check).
FUNC_DEF_RE = re.compile(r"^(?P<name>[A-Za-z0-9_][A-Za-z0-9_-]*)\s*\(\)\s*\{")

HEREDOC_START_RE = re.compile(r"cat\s*<<-?\s*'?\"?(?P<tag>[A-Za-z_][A-Za-z0-9_]*)'?\"?\s*$")

PRINTF_LINE_RE = re.compile(r'^\s*printf\s+"(?P<body>.*)"\s*$')

# A help-table content line: "  command args...   description text"
# We take the first whitespace-delimited token as the candidate command name,
# and the text after the LAST run of 2+ spaces as the description.
HELP_LINE_TOKEN_RE = re.compile(r"^\s*(?P<cmd>[A-Za-z0-9_.-]+)\b")
HELP_LINE_SPLIT_RE = re.compile(r"\s{2,}")


def sanitize(text: str) -> str:
    """Collapse whitespace/newlines/tabs so a field is safe for one TSV line."""
    if text is None:
        return ""
    text = text.replace("\t", " ").replace("\n", " ").replace("\r", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def repo_relative(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def scope_for_file(path: Path, root: Path) -> str:
    rel = path.relative_to(root)
    parts = rel.parts
    if len(parts) == 1:
        return "root"
    return parts[0]  # scope = top-level directory name (as registered)


def iter_source_files(root: Path, scan_dirs, root_files):
    for d in scan_dirs:
        dpath = root / d
        if not dpath.is_dir():
            continue
        for p in sorted(dpath.rglob("*.zsh")):
            # skip nested fixture/test directories
            if any(part.endswith(".fixtures") for part in p.relative_to(root).parts):
                continue
            yield p
    for fname in root_files:
        fpath = root / fname
        if fpath.is_file():
            yield fpath


# --------------------------------------------------------------------------
# Pass 1: index every function definition (name -> file), and collect
# help-block text keyed by function name that looks like a help emitter.
# --------------------------------------------------------------------------

def extract_functions_and_help(files):
    """
    Returns:
      func_files: dict[funcname] -> Path (first definition wins; ambiguities
                  are reported by the caller)
      func_dupes: dict[funcname] -> list[Path] (all definitions, for report)
      help_text:  dict[cmd_token] -> help string (parsed out of *_help()
                  bodies, both heredoc and printf styles)
      help_ambiguous: list of (cmd_token, [values]) for tokens redefined
                      with conflicting text
      preceding_comment: dict[(file, lineno)] -> comment text immediately
                      above a function/alias definition
    """
    func_files: dict[str, Path] = {}
    func_dupes: dict[str, list[Path]] = {}
    help_text: dict[str, str] = {}
    help_conflicts: dict[str, set[str]] = {}
    preceding_comment: dict[tuple[str, int], str] = {}

    for path in files:
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue

        # -- function defs + preceding comment capture --
        for i, line in enumerate(lines):
            m = FUNC_DEF_RE.match(line)
            if m:
                name = m.group("name")
                func_dupes.setdefault(name, []).append(path)
                if name not in func_files:
                    func_files[name] = path
                # preceding non-blank comment line (if immediately above)
                j = i - 1
                if j >= 0:
                    prev = lines[j].strip()
                    if prev.startswith("#") and not prev.startswith("#!") and not re.match(r"^#\s*={5,}", prev):
                        preceding_comment[(str(path), i)] = prev.lstrip("#").strip()

        # -- help blocks: heredoc style --
        i = 0
        n = len(lines)
        while i < n:
            hd = HEREDOC_START_RE.search(lines[i])
            if hd and i > 0:
                # find the enclosing function name (nearest FUNC_DEF_RE above)
                func_name = None
                for k in range(i, -1, -1):
                    fm = FUNC_DEF_RE.match(lines[k])
                    if fm:
                        func_name = fm.group("name")
                        break
                tag = hd.group("tag")
                body_lines = []
                j = i + 1
                while j < n and lines[j].strip() != tag:
                    body_lines.append(lines[j])
                    j += 1
                _harvest_help_lines(body_lines, help_text, help_conflicts)
                i = j
            i += 1

        # -- help blocks: printf style (consecutive printf "..." lines under
        #    a *_help() function) --
        i = 0
        while i < n:
            fm = FUNC_DEF_RE.match(lines[i])
            if fm and fm.group("name").endswith("_help"):
                j = i + 1
                body_lines = []
                depth = 1
                while j < n and depth > 0:
                    if lines[j].strip() == "}":
                        depth -= 1
                        if depth == 0:
                            break
                    pm = PRINTF_LINE_RE.match(lines[j])
                    if pm:
                        body = pm.group("body")
                        body = body.replace("\\n", "\n")
                        body_lines.extend(body.split("\n"))
                    j += 1
                _harvest_help_lines(body_lines, help_text, help_conflicts)
            i += 1

    return func_files, func_dupes, help_text, help_conflicts, preceding_comment


def _harvest_help_lines(body_lines, help_text, help_conflicts):
    for raw in body_lines:
        line = raw.rstrip()
        if not line.strip():
            continue
        # strip box-drawing table borders (fo/nab/psd/im/ltp "+---+ | ... |" style)
        stripped = line.strip()
        stripped = re.sub(r"^\|\s*", "", stripped)
        stripped = re.sub(r"\s*\|$", "", stripped)
        if not stripped or set(stripped) <= set("+-="):
            continue

        tm = HELP_LINE_TOKEN_RE.match(stripped)
        if not tm:
            continue
        cmd = tm.group("cmd")
        # reject decorative box-drawing / non-command tokens
        if not re.match(r"^[A-Za-z0-9_.-]+$", cmd):
            continue
        if cmd in ("Guide:", "Registry:", "Script:", "Agent:", "Log:", "Config:", "Engine:"):
            continue

        # description = text after the FIRST run of 2+ spaces following the
        # command token (so internal double-spaces inside the description
        # itself don't truncate it). The text between the command token and
        # that split point is either nothing, or a bracketed/plain arg hint
        # ("[--project <x>]", "<msg>") — both fine for the command's OWN
        # entry. But if that in-between text starts with a bare flag
        # ("-gs", "-f", "--plain") it's documenting a sub-flag of a
        # case-dispatch command (fo -gs, nab -f, project-paths --plain …),
        # not the command's own bare invocation — skip so it doesn't
        # collapse into (or clobber) the parent command's real entry.
        sm = HELP_LINE_SPLIT_RE.search(stripped)
        if not sm:
            continue
        between = stripped[tm.end():sm.start()].strip()
        if between.startswith("-"):
            continue
        desc = stripped[sm.end():].strip()
        if not desc or desc == cmd:
            continue
        prev = help_text.get(cmd)
        if prev is not None and prev != desc:
            help_conflicts.setdefault(cmd, set()).add(prev)
            help_conflicts.setdefault(cmd, set()).add(desc)
            continue  # keep first-seen, flag conflict
        help_text.setdefault(cmd, desc)


# --------------------------------------------------------------------------
# Pass 2: collect user-facing commands (aliases from keyboard.zsh files +
# top-level functions from scope engines / root files).
# --------------------------------------------------------------------------

def collect_commands(root: Path, files, func_files, func_dupes, help_text, preceding_comment):
    rows = []  # (scope, command, help, engine)
    ambiguities = []
    seen_commands = set()

    # Aliases live primarily in keyboard.zsh control panels, but the spec
    # also calls for user-facing aliases defined directly in scope engines
    # / root files (e.g. archx/commands.zsh, project-switcher.zsh) — so we
    # scan every file for `alias` lines, not just keyboard.zsh.
    other_files = [p for p in files if p.name != KEYBOARD_FILENAME]

    # -- aliases (keyboard.zsh control panels + scope engines / root files) --
    for path in files:
        scope = scope_for_file(path, root)
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for line in lines:
            m = ALIAS_RE.match(line)
            if not m:
                continue
            name = m.group("name")
            body = m.group("sq") or m.group("dq") or m.group("bare") or ""
            comment = m.group("comment")

            engine = repo_relative(path, root)
            body_stripped = body.strip()
            target_ident = None
            ident_m = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*)$", body_stripped)
            if ident_m:
                target_ident = ident_m.group(1)
            if target_ident and target_ident in func_files:
                engine = repo_relative(func_files[target_ident], root)
                if len(func_dupes.get(target_ident, [])) > 1:
                    ambiguities.append(
                        f"alias {name}: target function '{target_ident}' defined in "
                        f"{len(func_dupes[target_ident])} files "
                        f"({', '.join(repo_relative(p, root) for p in func_dupes[target_ident])}); "
                        f"used first-seen ({engine})"
                    )

            help_str = None
            if target_ident and target_ident in help_text:
                help_str = help_text[target_ident]
            elif name in help_text:
                help_str = help_text[name]
            elif comment:
                help_str = comment
            if not help_str:
                help_str = "(no help line)"

            rows.append((scope, name, sanitize(help_str), engine))
            seen_commands.add(name)

    # -- top-level functions in scope engines / root files (skip _private) --
    for path in other_files:
        scope = scope_for_file(path, root)
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for i, line in enumerate(lines):
            m = FUNC_DEF_RE.match(line)
            if not m:
                continue
            name = m.group("name")
            if name.startswith("_"):
                continue
            if name in seen_commands:
                continue  # already captured via alias resolution
            # only record this function under the FIRST file it's defined in
            # (matches func_files index) to avoid duplicate rows for
            # launcher-stub / toolkit-real double-definitions.
            if func_files.get(name) != path:
                continue

            help_str = help_text.get(name)
            if help_str is None:
                pc = preceding_comment.get((str(path), i))
                help_str = pc if pc else "(no help line)"

            rows.append((scope, name, sanitize(help_str), repo_relative(path, root)))
            seen_commands.add(name)

    # report any function name defined in >1 file (informational)
    for name, defs in func_dupes.items():
        if len(defs) > 1 and name in seen_commands:
            paths = ", ".join(repo_relative(p, root) for p in defs)
            note = f"function '{name}' defined in {len(defs)} files ({paths})"
            if note not in ambiguities:
                ambiguities.append(note)

    return rows, ambiguities


# --------------------------------------------------------------------------
# --check mode: convention-discipline lint over the same parse.
# --------------------------------------------------------------------------

EXTERNAL_BINARY_ALLOWLIST = {
    "gemini", "tailscale", "agy", "bash", "zsh", "php", "git", "grep",
    "tail", "ls", "code", "subl", "vi", "docker", "systemctl", "mariadb",
    "echo", "cat", "source", "python3", "jq", "uniqid", "openssl", "cut",
}


def discover_all_command_folders(root: Path) -> list[str]:
    """
    Lightweight scan of EVERY top-level directory under root (ignoring
    NEVER_SCAN_DIRS and *.fixtures dirs) for evidence of user-facing
    commands (an alias or a top-level function def anywhere under it) —
    used by --check to spot folders the registry doesn't know about yet,
    independent of which folders the generator was actually told to scan.
    """
    found = []
    for child in sorted(root.iterdir()):
        if not child.is_dir():
            continue
        name = child.name
        if name in NEVER_SCAN_DIRS or name.startswith(".") or name.endswith(".fixtures"):
            continue
        has_commands = False
        for p in child.rglob("*.zsh"):
            if any(part.endswith(".fixtures") for part in p.relative_to(root).parts):
                continue
            try:
                lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
            except OSError:
                continue
            if any(ALIAS_RE.match(line) or FUNC_DEF_RE.match(line) for line in lines):
                has_commands = True
                break
        if has_commands:
            found.append(name)
    return found


def run_check(root: Path, files, func_files, func_dupes, help_text,
               preceding_comment, rows, scan_dirs, excluded) -> int:
    violations = 0

    # 1. function bodies inside any keyboard.zsh (aliases-only law)
    kb_func_violations = []
    for path in files:
        if path.name != KEYBOARD_FILENAME:
            continue
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for i, line in enumerate(lines, start=1):
            if FUNC_DEF_RE.match(line):
                kb_func_violations.append((repo_relative(path, root), i, line.strip()))

    # 2. commands with no help line, grouped by scope
    no_help_by_scope: dict[str, list[str]] = {}
    for scope, command, help_str, engine in rows:
        if help_str == "(no help line)":
            no_help_by_scope.setdefault(scope, []).append(command)

    # 3. scopes with user-facing commands but no keyboard.zsh at all
    scopes_with_commands = {scope for scope, *_ in rows}
    scopes_with_keyboard = {
        scope_for_file(p, root) for p in files if p.name == KEYBOARD_FILENAME
    }
    retrofit_candidates = sorted(
        s for s in scopes_with_commands
        if s not in scopes_with_keyboard and s != "root"
    )

    # 4. dangling wiring: aliases in keyboard.zsh whose bare-identifier
    #    target cannot be resolved to any known local function, and doesn't
    #    look like an external binary call.
    dangling = []
    for path in files:
        if path.name != KEYBOARD_FILENAME:
            continue
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for i, line in enumerate(lines, start=1):
            m = ALIAS_RE.match(line)
            if not m:
                continue
            body = (m.group("sq") or m.group("dq") or m.group("bare") or "").strip()
            ident_m = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*)$", body)
            if not ident_m:
                continue
            ident = ident_m.group(1)
            looks_local = ident.startswith("_") or "-" in ident
            if not looks_local:
                continue
            if ident in EXTERNAL_BINARY_ALLOWLIST:
                continue
            if ident not in func_files:
                dangling.append((repo_relative(path, root), i, m.group("name"), ident))

    print("=== palette-map-gen --check ===")

    print(f"\n[1] function bodies inside keyboard.zsh: {len(kb_func_violations)}")
    for f, ln, text in kb_func_violations:
        print(f"  {f}:{ln}: {text}")
        violations += 1

    total_no_help = sum(len(v) for v in no_help_by_scope.values())
    print(f"\n[2] commands with no help line: {total_no_help}")
    for scope in sorted(no_help_by_scope):
        cmds = sorted(no_help_by_scope[scope])
        print(f"  {scope} ({len(cmds)}): {', '.join(cmds)}")
        violations += len(cmds)

    print(f"\n[3] scopes with commands but no keyboard.zsh: {len(retrofit_candidates)}")
    for s in retrofit_candidates:
        print(f"  {s}")
        violations += 1

    print(f"\n[4] dangling alias wiring (target function not found): {len(dangling)}")
    for f, ln, name, ident in dangling:
        print(f"  {f}:{ln}: alias {name} -> {ident} (unresolved)")
        violations += 1

    # 5/6. registry folder classification (informational — not violations).
    # Any top-level folder with real commands must be either registered
    # ("scopes"), or explicitly parked ("excluded") — anything else is
    # "unregistered" and worth an operator decision (registries/palette.json).
    all_command_folders = discover_all_command_folders(root)
    registered = set(scan_dirs)
    excluded_set = set(excluded)
    excluded_found = sorted(f for f in all_command_folders if f in excluded_set)
    unregistered = sorted(
        f for f in all_command_folders
        if f not in registered and f not in excluded_set
    )

    print(f"\n[5] excluded folders (per registries/palette.json, info only): {len(excluded_found)}")
    for f in excluded_found:
        print(f"  {f}  (parked — add to \"scopes\" in registries/palette.json to enable)")

    print(f"\n[6] unregistered folders (has commands, not in scopes or excluded, info only): {len(unregistered)}")
    for f in unregistered:
        print(f"  {f}  (add to \"scopes\" or \"excluded\" in registries/palette.json)")

    print(f"\n=== check {'FAILED' if violations else 'CLEAN'} — {violations} violation(s) ===")
    return 1 if violations else 0


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Generate palette.map from a zsh config tree.")
    default_root = Path(__file__).resolve().parent.parent
    parser.add_argument("--root", type=Path, default=default_root,
                         help="zsh root directory (default: two levels up from this script)")
    parser.add_argument("--check", action="store_true",
                         help="audit convention discipline instead of writing palette.map")
    args = parser.parse_args()

    root = args.root.resolve()
    if not root.is_dir():
        print(f"error: root not found: {root}", file=sys.stderr)
        return 1

    scan_dirs, root_files, excluded = load_registry(root)
    # registry "excluded" wins over "scopes" if an operator ever lists a
    # folder in both — belt and suspenders, keeps the parked decision sticky.
    scan_dirs = [d for d in scan_dirs if d not in excluded]

    files = list(iter_source_files(root, scan_dirs, root_files))

    func_files, func_dupes, help_text, help_conflicts, preceding_comment = \
        extract_functions_and_help(files)

    rows, ambiguities = collect_commands(root, files, func_files, func_dupes,
                                          help_text, preceding_comment)

    rows.sort(key=lambda r: (r[0], r[1]))

    if args.check:
        return run_check(root, files, func_files, func_dupes, help_text,
                          preceding_comment, rows, scan_dirs, excluded)

    out_path = root / "palette.map"
    with out_path.open("w", encoding="utf-8") as f:
        f.write("# palette.map — generated by ai/palette-map-gen.py — do not hand-edit\n")
        for scope, command, help_str, engine in rows:
            f.write(f"{scope}\t{command}\t{help_str}\t{engine}\n")

    # -------- coverage report (stdout) --------
    total = len(rows)
    with_help = sum(1 for r in rows if r[2] != "(no help line)")
    without_help = total - with_help
    scope_counts: dict[str, int] = {}
    for scope, *_ in rows:
        scope_counts[scope] = scope_counts.get(scope, 0) + 1

    print(f"palette.map written: {out_path}")
    print(f"total commands: {total}")
    print(f"with real help: {with_help}")
    print(f"(no help line): {without_help}")
    print("per-scope counts:")
    for scope in sorted(scope_counts):
        print(f"  {scope}: {scope_counts[scope]}")
    if help_conflicts:
        print(f"help-token conflicts ({len(help_conflicts)}):")
        for cmd, vals in sorted(help_conflicts.items()):
            print(f"  {cmd}: {sorted(vals)}")
    if ambiguities:
        print(f"ambiguities ({len(ambiguities)}):")
        for a in ambiguities:
            print(f"  - {a}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
