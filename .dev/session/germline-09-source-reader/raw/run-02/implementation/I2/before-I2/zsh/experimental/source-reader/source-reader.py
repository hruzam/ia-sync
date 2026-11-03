#!/usr/bin/env python3
"""Read-only, bounded source discovery. File contents are data, never commands."""

import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys


NOTICE = "Found on disk; runtime visibility/activation unknown."
LAYOUTS = {"skills", "synced-skills", "guides", "germline"}


def diagnostic(message):
    print(f"source-reader: {message}", file=sys.stderr)


def default_roots():
    """Same boundaries as D1; derive user paths on the current host."""
    home = Path.home()
    repo = home / "ia-sync"
    here = Path(__file__).resolve()
    if (here.parents[3] / "machines.json").is_file():
        repo = here.parents[3]
    specs = [
        ("germline-authored", "germline", None, "authored", repo / "germline", "germline"),
        ("germline-deployed", "germline", None, "deployed", home / ".germline", "germline"),
        ("temple-guides", "guide", None, "temple", home / "reposoma/raw.guides", "guides"),
        ("codex-authored", "skill", "codex", "authored", repo / "codex/skills", "skills"),
        ("claude-authored", "skill", "claude", "authored", repo / "claude/skills", "skills"),
        ("codex-personal", "skill", "codex", "installed-personal", home / ".agents/skills", "skills"),
        ("claude-personal", "skill", "claude", "installed-personal", home / ".claude/skills", "skills"),
        ("codex-project", "skill", "codex", "project", repo / ".agents/skills", "skills"),
        ("claude-project", "skill", "claude", "project", repo / ".claude/skills", "skills"),
        ("codex-system", "skill", "codex", "runtime-identified-system", home / ".codex/skills/.system", "skills"),
        ("claude-account-sync", "skill", "claude", "account-sync; individual publisher unknown", home / ".claude/skills/synced", "synced-skills"),
        ("codex-admin", "skill", "codex", "admin candidate", Path("/etc/codex/skills"), "skills"),
        ("claude-admin", "skill", "claude", "admin candidate", Path("/etc/claude-code/.claude/skills"), "skills"),
    ]
    keys = ("id", "kind", "vendor_if_any", "origin", "absolute_path", "layout")
    return [dict(zip(keys, (a, b, c, d, str(e), f))) for a, b, c, d, e, f in specs]


def load_roots(filename):
    roots = json.loads(Path(filename).read_text())["roots"] if filename else default_roots()
    if not isinstance(roots, list):
        raise ValueError("roots must be an array")
    seen = set()
    for root in roots:
        for key in ("id", "kind", "origin", "absolute_path", "layout"):
            if not isinstance(root.get(key), str) or not root[key]:
                raise ValueError(f"root requires nonempty {key}")
        if "vendor_if_any" not in root or root["vendor_if_any"] is not None and not isinstance(root["vendor_if_any"], str):
            raise ValueError("root requires vendor_if_any string or null")
        if root["id"] in seen:
            raise ValueError(f"duplicate root ID: {root['id']}")
        seen.add(root["id"])
        if not Path(root["absolute_path"]).is_absolute() or root["layout"] not in LAYOUTS:
            raise ValueError(f"invalid absolute path/layout for {root['id']}")
    return roots


def frontmatter(path):
    """Read only a bounded leading frontmatter block, without YAML evaluation."""
    values = {}
    with path.open("rb", buffering=0) as stream:
        if stream.readline(8193).strip() != b"---":
            return values
        total = 0
        for _ in range(128):
            line = stream.readline(8193)
            total += len(line)
            if not line or total > 32768 or len(line) > 8192:
                values["_warning"] = "frontmatter incomplete or exceeds metadata limit"
                break
            if line.strip() in (b"---", b"..."):
                break
            match = re.match(r"^([A-Za-z_][\w-]*):\s*(.*?)\s*$", line.decode("utf-8", "replace"))
            if match:
                values[match[1]] = match[2].strip("\"'")
        else:
            values["_warning"] = "frontmatter exceeds 128 lines"
    return values


def children(path):
    return sorted(path.iterdir(), key=lambda child: child.name)


def candidates(root, gaps):
    base = Path(root["absolute_path"])
    layout = root["layout"]
    if layout in ("skills", "synced-skills", "guides"):
        folders = children(base)
        if layout == "synced-skills":
            buckets = [p for p in folders if p.is_dir()]
            if len(buckets) != 1:
                gaps.append({"root_id": root["id"], "reason": "expected one account bucket; publisher unknown", "buckets": [p.name for p in buckets]})
                return
            folders = children(buckets[0])
        for folder in folders:
            if not folder.is_dir():
                continue
            if layout == "guides":
                guide = folder / "GUIDE.md"
                if guide.is_file():
                    yield guide, "GUIDE", folder.name
                    res = folder / "res"
                    if res.is_dir():
                        for chapter in children(res):
                            if chapter.suffix == ".md" and chapter.is_file():
                                yield chapter, "guide chapter", folder.name
            else:
                yield folder / "SKILL.md", "native SKILL.md", None
    else:
        agents = base / "agents"
        if agents.is_dir():
            for agent in children(agents):
                if not agent.is_dir():
                    continue
                for file in children(agent):
                    if file.name == "identity.md":
                        yield file, "germline identity", None
                    elif re.fullmatch(r"binding\.[^.]+\.md", file.name):
                        yield file, "germline binding", None
                    elif re.fullmatch(r"method\..+\.md", file.name):
                        yield file, "germline method", None
                    elif file.name in ("cards", "methods") and file.is_dir():
                        for item in children(file):
                            if item.suffix == ".md":
                                yield item, "germline card" if file.name == "cards" else "germline method", None
        skills = base / "skills"
        if skills.is_dir():
            for file in children(skills):
                if re.fullmatch(r"skill\..+\.md", file.name):
                    yield file, "germline skill", None


def catalog(roots):
    entries, statuses, gaps = [], [], []
    for root in roots:
        status = dict(root)
        start = len(entries)
        try:
            base = Path(root["absolute_path"])
            if not base.exists():
                status["availability"] = "missing"
            elif not base.is_dir():
                status["availability"] = "not-directory"
            else:
                for path, kind, slug in candidates(root, gaps):
                    if not path.is_file():
                        continue
                    lexical = str(path.absolute())
                    entry = {key: root[key] for key in ("kind", "vendor_if_any", "origin")}
                    entry.update(id=hashlib.sha256(f"{root['id']}\0{root['origin']}\0{lexical}".encode()).hexdigest(),
                                 root_id=root["id"], family=root["kind"], source_file_kind=kind,
                                 absolute_path=lexical, resolved_path=str(path.resolve()),
                                 symlink_target=str(path.resolve()) if path.is_symlink() or path.absolute() != path.resolve() else None,
                                 name=path.parent.name if path.name in ("GUIDE.md", "SKILL.md", "identity.md") else path.stem,
                                 guide_slug=slug, availability="found on disk", activation="unknown",
                                 provenance_evidence=f"bounded {root['layout']} discovery under {base}")
                    try:
                        entry["frontmatter"] = {} if kind == "guide chapter" else frontmatter(path)
                    except OSError as error:
                        entry.update(frontmatter={}, availability="unreadable", metadata_error=str(error))
                        gaps.append({"root_id": root["id"], "path": lexical, "reason": str(error)})
                    entries.append(entry)
                status["availability"] = "present" if len(entries) > start else "empty"
        except OSError as error:
            status.update(availability="unreadable", error=str(error))
        status["entries"] = len(entries) - start
        status["provenance_evidence"] = "bounded filesystem observation; no runtime activation check"
        statuses.append(status)
        if status["availability"] != "present":
            gaps.append({"root_id": root["id"], "reason": status["availability"]})
    return {"notice": NOTICE, "roots": statuses, "entries": entries, "gaps": gaps,
            "inventory_limits": ["Plugin/bundled roots not declared here are unknown.", "Account-sync publisher unknown."]}


def label(entry):
    return f"{entry['id']}\t{entry['family']}/{entry['source_file_kind']}\t{entry['vendor_if_any'] or '-'}\t{entry['origin']}\t{entry['absolute_path']}"


def plain(data, entries=None, stream=None):
    stream = stream or sys.stdout
    print(NOTICE, file=stream)
    for gap in data["gaps"]:
        print(f"GAP {gap['root_id']}: {gap['reason']}", file=stream)
    for limit in data["inventory_limits"]:
        print(limit, file=stream)
    for entry in data["entries"] if entries is None else entries:
        print(label(entry), file=stream)


def show(entries, selection):
    matches = [entry for entry in entries if selection in (entry["id"], entry["absolute_path"])]
    paths = {entry["absolute_path"] for entry in matches}
    if len(paths) != 1:
        diagnostic("select an exact catalog ID or exact catalog lexical path")
        return 2
    # No decoration, decoding, rendering, shell, eval or instruction execution.
    sys.stdout.buffer.write(Path(matches[0]["absolute_path"]).read_bytes())
    return 0


def manifest_section(body):
    lines = body.splitlines(keepends=True)
    start = next((i for i, line in enumerate(lines) if re.fullmatch(rb"## Manifest\s*", line.rstrip(b"\r\n"))), None)
    if start is None:
        return b""
    end = next((i for i in range(start + 1, len(lines)) if re.match(rb"#{1,2} ", lines[i])), len(lines))
    return b"".join(lines[start:end])


def guide_warnings(guide, body):
    metadata = guide["frontmatter"]
    try:
        verified = datetime.date.fromisoformat(metadata["verified"])
        if datetime.date.today() > verified + datetime.timedelta(days=int(metadata["half_life_days"])):
            diagnostic(f"guide verified {verified} is stale")
    except (KeyError, ValueError, OverflowError):
        pass
    if b"PUBLISHED MIRROR" in body:
        diagnostic("PUBLISHED MIRROR: the owning project is the truth")
    manifest = manifest_section(body).decode("utf-8", "replace")
    folder = Path(guide["absolute_path"]).parent
    for item in children(folder):
        if item.name in ("GUIDE.md", "res"):
            continue
        name = item.name + "/" if item.is_dir() else item.name
        if name not in manifest:
            diagnostic(f"manifest drift: undeclared {name}")
    res = folder / "res"
    if res.is_dir():
        for chapter in children(res):
            if chapter.suffix == ".md" and chapter.is_file() and chapter.name not in manifest:
                diagnostic(f"manifest drift: unlisted res/{chapter.name}")


def guide_command(data, slug, chapter):
    guides = [e for e in data["entries"] if e["source_file_kind"] == "GUIDE"]
    matches = [e for e in guides if e["guide_slug"] == slug] if slug else []
    if not matches:
        plain(data, guides)
        for guide in guides:
            chapters = [Path(e["absolute_path"]).name for e in data["entries"] if e["source_file_kind"] == "guide chapter" and e["root_id"] == guide["root_id"] and e["guide_slug"] == guide["guide_slug"]]
            print(json.dumps({"slug": guide["guide_slug"], "root_id": guide["root_id"], "frontmatter": guide["frontmatter"], "chapters": chapters}, ensure_ascii=False))
        return 2 if slug else 0
    if len(matches) > 1:
        diagnostic("ambiguous guide slug; select an exact catalog path with show")
        plain(data, matches)
        return 2
    guide = matches[0]
    body = Path(guide["absolute_path"]).read_bytes()
    guide_warnings(guide, body)
    if chapter is None:
        sys.stdout.buffer.write(body)
        return 0
    choices = [e for e in data["entries"] if e["source_file_kind"] == "guide chapter" and e["root_id"] == guide["root_id"] and e["guide_slug"] == slug and chapter.casefold() in Path(e["absolute_path"]).name.casefold()]
    if len(choices) == 1:
        return show(choices, choices[0]["id"])
    if choices:
        diagnostic("ambiguous chapter; choose one of these basenames; no file resolved")
        print("\n".join(Path(e["absolute_path"]).name for e in choices))
    else:
        diagnostic("no chapter match; showing only GUIDE ## Manifest; no file resolved")
        sys.stdout.buffer.write(manifest_section(body))
    return 2


def browse(data, force_plain):
    if not sys.stdin.isatty():
        plain(data)
        return 0
    plain(data, [], sys.stderr)
    entries = data["entries"]
    if not entries:
        return 0
    if not force_plain and shutil.which("fzf"):
        # Fixed argv; source text is never a command, preview or shell expression.
        picker_env = {key: value for key, value in os.environ.items() if key not in ("FZF_DEFAULT_OPTS", "FZF_DEFAULT_OPTS_FILE")}
        result = subprocess.run(["fzf", "--delimiter=\t", "--with-nth=2..", "--no-multi", "--prompt=source> "],
                                input="\n".join(label(e) for e in entries), text=True, stdout=subprocess.PIPE, env=picker_env)
        if result.returncode:
            return 1
        selection = result.stdout.split("\t", 1)[0]
    else:
        for i, entry in enumerate(entries, 1):
            print(f"{i}\t{label(entry)}", file=sys.stderr)
        print("Read number (blank cancels): ", end="", file=sys.stderr, flush=True)
        answer = sys.stdin.readline().strip()
        if not answer:
            return 1
        if not answer.isdecimal() or not 1 <= int(answer) <= len(entries):
            diagnostic("invalid selection")
            return 2
        selection = entries[int(answer) - 1]["id"]
    return show(entries, selection)


def main():
    parser = argparse.ArgumentParser(description="Lazy read-only source browser. " + NOTICE,
                                     epilog="No install, model, network, index or source execution. --roots may precede or follow the command.")
    parser.add_argument("--roots", metavar="JSON", help="declared bounded roots override")
    subs = parser.add_subparsers(dest="command", required=True)
    for name, help_text in (("catalog", "metadata only; no source bodies"), ("show", "exact selected file bytes"), ("guide", "GUIDE.md or immediate res chapter"), ("browse", "terminal selection; nonTTY lists metadata")):
        sub = subs.add_parser(name, help=help_text)
        sub.add_argument("--roots", metavar="JSON", default=argparse.SUPPRESS)
        if name == "catalog":
            sub.add_argument("--json", action="store_true")
        elif name == "show":
            sub.add_argument("selection")
        elif name == "guide":
            sub.add_argument("slug", nargs="?")
            sub.add_argument("chapter", nargs="?")
        else:
            sub.add_argument("--plain", action="store_true", help="use numbered terminal list instead of optional fzf")
    args = parser.parse_args()
    try:
        data = catalog(load_roots(args.roots))
        if args.command == "catalog":
            if args.json:
                print(json.dumps(data, indent=2, ensure_ascii=False))
            else:
                plain(data)
            return 0
        if args.command == "show":
            return show(data["entries"], args.selection)
        if args.command == "guide":
            return guide_command(data, args.slug, args.chapter)
        return browse(data, args.plain)
    except (OSError, ValueError, KeyError, TypeError, RuntimeError) as error:
        diagnostic(str(error))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
