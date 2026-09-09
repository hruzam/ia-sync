#!/usr/bin/env python3
"""runbook.py — session-scope runbook browser. v0.2 (rescoped from nablarva/ 2026-09-06)

Browse .dev/session/ beds: D1 list with gate-state, D2 sectioned view
(STATUS / _bus/ / RUNBOOK / bed-root files / raw/) with foldable groups,
internal reader, print-buffer pane, and base colors.

Invoke via:  python3 runbook.py [--root <.dev/session path>]
Root resolution: --root > $RB_ROOT (config default bench) > walk-up.

Keybinds:
  ↑ ↓           navigate D1 / free-scroll D2
  Tab           switch focus D1 ↔ D2
  j / k         move node cursor in D2 (headers + files)
  J / K         jump node cursor between section headers (groups)
  Enter / Space header → fold/unfold group · file → open internal reader
  1–5           jump to section (R2 STATUS / R5 _bus / R1 RUNBOOK / R3 files / R4 raw)
  F             fold/unfold R1 RUNBOOK
  e             open cursor file in $EDITOR (curses escape)
  B             presence board modal (advisory display; ● in D1 = bed attached locally)
  m / u         attach / detach own board record for the selected bed (D1 focus)
  p             collect selected path into print buffer (printed at quit)
  b             toggle buffer pane
  r             manual reload
  q / Esc       quit (buffer prints to scroll-back)

Reader keybinds: ↑↓ PgUp/PgDn g/G scroll · e editor · q/Esc/← back

Board CLI (same grammar core as the TUI):
  runbook.py board list
  runbook.py board mark --bed <path> [--workspace <path>] [--seat S] [--note N]
  runbook.py board unmark [--id ID | --bed <path>]
Contract: ~/reposoma/raw.guides/runbook/res/presence-board.md — advisory only.
"""

import argparse
import curses
import os
import re
import subprocess
import sys
import textwrap
from pathlib import Path

# ESCDELAY must be set before curses.initscr()
os.environ.setdefault("ESCDELAY", "25")


# ── Small helpers (cs-palette pattern, stdlib only) ──────────────────────────

def clipped(value, width):
    if width <= 0:
        return ""
    if len(value) <= width:
        return value
    if width == 1:
        return "…"
    return value[: width - 1] + "…"


def safe_add(screen, row, col, value, attr=0, width=None):
    h, w = screen.getmaxyx()
    if row < 0 or row >= h or col < 0 or col >= w:
        return
    avail = w - col
    if width is not None:
        avail = min(avail, max(0, width))
    if avail <= 0:
        return
    try:
        screen.addnstr(row, col, value, avail, attr)
    except curses.error:
        pass


def wrap_line(raw, width):
    """WRITELN law: wrap, never clip body text. No hyphen breaks; long words wrap."""
    if not raw.strip():
        return [""]
    return textwrap.wrap(
        raw,
        width=max(1, width),
        break_on_hyphens=False,
        break_long_words=True,
    ) or [""]


# ── Colors ───────────────────────────────────────────────────────────────────

CP = {}  # name -> curses attr (color_pair); stays {} when colors unavailable


def init_colors():
    if not curses.has_colors():
        return
    try:
        curses.start_color()
        curses.use_default_colors()
    except curses.error:
        return
    palette_pairs = [
        ("header", curses.COLOR_CYAN),     # section headers, md headings
        ("accent", curses.COLOR_YELLOW),   # next: strip, json, buffer
        ("good", curses.COLOR_GREEN),      # → state, done boxes, sh/py/zsh
        ("warn", curses.COLOR_RED),        # ! state
        ("meta", curses.COLOR_MAGENTA),    # yaml, keys
    ]
    for i, (name, fg) in enumerate(palette_pairs, start=1):
        try:
            curses.init_pair(i, fg, -1)
            CP[name] = curses.color_pair(i)
        except curses.error:
            CP[name] = 0


def c(name, extra=0):
    return CP.get(name, 0) | extra


STATE_STYLE = {  # gate state char -> (color name, extra attr)
    "!": ("warn", curses.A_BOLD),
    "→": ("good", 0),
    "·": ("accent", 0),
    "?": (None, curses.A_DIM),
}

EXT_STYLE = {  # file suffix -> (color name, extra attr)
    ".json": ("accent", 0),
    ".yaml": ("meta", 0),
    ".yml": ("meta", 0),
    ".zsh": ("good", 0),
    ".sh": ("good", 0),
    ".py": ("good", 0),
    ".kdl": ("meta", 0),
}


def attr_for_file(path):
    name, extra = EXT_STYLE.get(path.suffix.lower(), (None, 0))
    return c(name, extra) if name else extra


YAML_KEY_RE = re.compile(r"^\s*[\w@`][\w@`_.-]*:(\s|$)")


def md_line_attr(raw, in_fence):
    """Attr for one source line of a document body (markdown-biased)."""
    s = raw.lstrip()
    if s.startswith("```"):
        return curses.A_DIM
    if in_fence:
        if YAML_KEY_RE.match(s):
            return c("meta")
        return 0
    if s.startswith("#"):
        return c("header", curses.A_BOLD)
    if s.startswith("- [x]"):
        return c("good")
    if s.startswith(">"):
        return curses.A_DIM
    if s.startswith("---") and s.strip("- ") == "":
        return curses.A_DIM
    return 0


# ── Frontmatter reader (fenced ```yaml + --- fallback) ───────────────────────

def read_fenced_block(path):
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    m = re.search(r"^```ya?ml\s*\n(.*?)^```", text, re.M | re.S)
    if m:
        return m.group(1)
    m = re.search(r"^---\s*\n(.*?)^---", text, re.M | re.S)
    if m:
        return m.group(1)
    return None


BLOCK_SCALAR = re.compile(r"^[>|][+-]?\s*$")


def _collect_block_scalar(lines, key_idx, key_indent, limit=20):
    """Collect a YAML block scalar's continuation lines (>-, >, |, |-, …).
    Returns the folded one-line text (strip display collapses newlines anyway)."""
    parts = []
    for line in lines[key_idx + 1: key_idx + 1 + limit]:
        if not line.strip():
            continue  # paragraph break inside the block — keep folding
        indent = len(line) - len(line.lstrip())
        if indent <= key_indent:
            break  # dedent ends the block
        parts.append(line.strip())
    return " ".join(parts)


def flat_keys(block):
    result = {}
    if not block:
        return result
    lines = block.splitlines()
    for i, line in enumerate(lines):
        m = re.match(r"^(\s*)`?(\w[\w_-]*):`?\s*(.*)", line)
        if not m:
            continue
        indent, key, val = len(m.group(1)), m.group(2), m.group(3).strip()
        if BLOCK_SCALAR.match(val):
            val = _collect_block_scalar(lines, i, indent)
        result[key] = val.strip().strip('"').strip("'")
    return result


def extract_next(path):
    """Extract next: from STATUS. Flat key → regex fallback → —."""
    if path is None or not path.is_file():
        return "—"
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return "—"
    block = read_fenced_block(path)
    if block:
        val = flat_keys(block).get("next", "")
        if val:
            return val
    lines = text.splitlines()
    for i, line in enumerate(lines):
        m = re.match(r"^(\s*)`?next:`?\s*(.*)", line)
        if m:
            val = m.group(2).strip()
            if BLOCK_SCALAR.match(val):
                val = _collect_block_scalar(lines, i, len(m.group(1)))
            val = val.strip().strip('"').strip("'")
            if val:
                return val
    return "—"


def _inflight_idle(raw):
    return raw is None or raw.lower() in ("none", "", "false", "no")


def extract_in_flight_raw(path):
    """Raw in_flight: value, or None. Reader stays strict: only canonical
    `none` (or empty/false/no) is idle — never guesses at prefixes. The raw
    value is displayed so a human sees WHY a bed is flagged."""
    if path is None or not path.is_file():
        return None
    block = read_fenced_block(path)
    if not block:
        return None
    return flat_keys(block).get("in_flight") or None


# ── Bed discovery ─────────────────────────────────────────────────────────────

def find_root(explicit):
    if explicit:
        p = Path(explicit).expanduser()
        return p if p.is_dir() else None
    env = os.environ.get("RB_ROOT")
    if env:
        p = Path(env).expanduser()
        if p.is_dir():
            return p
    cwd = Path.cwd()
    for parent in [cwd, *cwd.parents]:
        candidate = parent / ".dev" / "session"
        if candidate.is_dir() and candidate.parent.name == ".dev":
            return candidate
    return None


def find_status(bed):
    for name in ("STATUS.md", "status.md", "Status.md"):
        p = bed / name
        if p.is_file():
            return p
    return None


def find_runbook(bed):
    for name in ("RUNBOOK.md", "runbook.md"):
        p = bed / name
        if p.is_file():
            return p
    return None


def bed_state(rb_path, st_path):
    if rb_path is None:
        return "?"
    if st_path is None:
        return "·"
    if not _inflight_idle(extract_in_flight_raw(st_path)):
        return "!"
    return "→"


def load_beds(root):
    beds = []
    try:
        children = sorted(root.iterdir())
    except OSError:
        return beds
    for child in children:
        if not child.is_dir() or child.name.startswith("."):
            continue
        rb = find_runbook(child)
        st = find_status(child)
        drift = "~" if (st and st.name != "STATUS.md") else ""
        beds.append({
            "path": child,
            "slug": child.name + drift,
            "state": bed_state(rb, st),
            "status_path": st,
            "runbook_path": rb,
            "next_line": extract_next(st),
            "in_flight_raw": extract_in_flight_raw(st),
        })
    return beds


# ── Document rendering (wrapped lines with per-line attrs) ───────────────────

def render_file_lines(path, width):
    """Wrapped (text, attr) tuples for a document body. Fence-state aware."""
    if path is None or not path.is_file():
        return [("—", curses.A_DIM)]
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return [("(read error)", c("warn"))]
    out = []
    in_fence = False
    for raw in text.splitlines():
        attr = md_line_attr(raw, in_fence)
        if raw.lstrip().startswith("```"):
            in_fence = not in_fence
        for piece in wrap_line(raw, width):
            out.append((piece, attr))
    return out or [("", 0)]


def list_dir(path):
    if path is None or not path.is_dir():
        return []
    try:
        return sorted([p for p in path.iterdir() if p.is_file()], key=lambda p: p.name)
    except OSError:
        return []


def bed_root_items(bed):
    exclude = {"RUNBOOK.md", "runbook.md", "STATUS.md", "status.md", "Status.md"}
    try:
        return sorted(
            [p for p in bed.iterdir()
             if p.is_file() and p.name not in exclude and not p.name.startswith(".")],
            key=lambda p: p.name,
        )
    except OSError:
        return []


# ── D2 builder — lines + cursor nodes ────────────────────────────────────────
#
# Line dict:  {"text", "attr", "kind": "header"|"item"|"text", "path", "section"}
# Node dict:  {"line": int, "kind": "header"|"file", "section": int, "path": Path|None}
# Sections (fixed order, keyed 1–5): 0=R2 STATUS · 1=R5 _bus/ · 2=R1 RUNBOOK ·
#                                    3=R3 bed files · 4=R4 raw/

SECTION_LABELS = ["R2 · STATUS", "R5 · _bus/", "R1 · RUNBOOK", "R3 · bed files", "R4 · raw/"]


def build_d2(bed_info, width, collapsed):
    bed = bed_info["path"]
    lines = []
    nodes = []

    def header(section):
        mark = "▸" if section in collapsed else "▾"
        label = f"{mark} {SECTION_LABELS[section]} "
        bar = "─" * max(0, width - len(label) - 1)
        nodes.append({"line": len(lines), "kind": "header", "section": section, "path": None})
        lines.append({"text": label + bar, "attr": c("header", curses.A_BOLD),
                      "kind": "header", "path": None, "section": section})

    def item(section, path, label=None):
        nodes.append({"line": len(lines), "kind": "file", "section": section, "path": path})
        lines.append({"text": f"  {label or path.name}", "attr": attr_for_file(path),
                      "kind": "item", "path": path, "section": section})

    def body(pairs):
        for text, attr in pairs:
            lines.append({"text": text, "attr": attr, "kind": "text",
                          "path": None, "section": None})

    def empty():
        lines.append({"text": "  —", "attr": curses.A_DIM, "kind": "text",
                      "path": None, "section": None})

    # 0 — R2 STATUS (doc inline)
    header(0)
    if 0 not in collapsed:
        st = bed_info["status_path"]
        if st:
            item(0, st)
            body(render_file_lines(st, width))
        else:
            empty()

    # 1 — R5 _bus/ (most critical — sits high)
    header(1)
    if 1 not in collapsed:
        bus_files = list_dir(bed / "_bus")
        if bus_files:
            for p in bus_files:
                item(1, p)
        else:
            empty()

    # 2 — R1 RUNBOOK (doc inline; F folds)
    header(2)
    if 2 not in collapsed:
        rb = bed_info["runbook_path"]
        if rb:
            item(2, rb)
            body(render_file_lines(rb, width))
        else:
            empty()

    # 3 — R3 bed-root files
    header(3)
    if 3 not in collapsed:
        root_items = bed_root_items(bed)
        if root_items:
            for p in root_items:
                item(3, p)
        else:
            empty()

    # 4 — R4 raw/
    header(4)
    if 4 not in collapsed:
        raw_files = list_dir(bed / "raw")
        if raw_files:
            for p in raw_files:
                item(4, p)
        else:
            empty()

    return lines, nodes


# ── Mtime tracking ────────────────────────────────────────────────────────────

def mtime_ns(path):
    if path and path.is_file():
        try:
            return path.stat().st_mtime_ns
        except OSError:
            pass
    return 0


def bus_key(bed_path):
    bus = bed_path / "_bus"
    if not bus.is_dir():
        return ()
    try:
        return tuple(sorted(p.name for p in bus.iterdir() if p.is_file()))
    except OSError:
        return ()


# ── Presence board — presence-board/v1 client ────────────────────────────────
# Contract: ~/reposoma/raw.guides/runbook/res/presence-board.md (gaveled 2026-09-09,
# reposoma 0f48dce). Advisory only: records inform, never command or authorize.
# This client renders and writes records; it never auto-deletes, repairs, or
# infers liveness. Own-attachment memory is machine-local state, never synced.

BOARD_KEYS = ["schema", "attachment_id", "seat", "host", "workspace", "bed", "attached_at"]
BOARD_ROW = re.compile(r'^([a-z_]+): "([^"\\\x00-\x1f\x7f]*)"$')
BOARD_TS = re.compile(
    r"^(\d{4})-(\d{2})-(\d{2})T([01]\d|2[0-3]):([0-5]\d):([0-5]\d)"
    r"(Z|[+-](?:0\d|1[0-4]):[0-5]\d)$")
BOARD_FILENAME = re.compile(r"^presence\.[0-9a-f]{32}\.md$")


def board_dir():
    return Path(os.environ.get("RB_BOARD", "~/reposoma/_active")).expanduser()


def local_host():
    return os.environ.get("MACHINE_NAME", "") or "unknown"


def own_state_path():
    base = os.environ.get("RB_STATE", "~/.local/state/session-board")
    return Path(base).expanduser() / "own.tsv"


def load_own_ids():
    p = own_state_path()
    out = {}
    if p.is_file():
        for line in p.read_text(encoding="utf-8").splitlines():
            parts = line.split("\t")
            if len(parts) >= 2:
                out[parts[0]] = parts[1]  # id -> bed pointer
    return out


def save_own_ids(ids):
    p = own_state_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("".join(f"{i}\t{b}\n" for i, b in ids.items()), encoding="utf-8")


def to_tilde(path):
    s = str(Path(path).expanduser().resolve())
    home = str(Path.home())
    return "~" + s[len(home):] if s.startswith(home) else s


def board_now_stamp():
    import datetime
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


def sanitize_note(note):
    return re.sub(r'[\x00-\x1f\x7f"\\]', "", note or "").strip()


def compose_record(seat, host, workspace, bed, note=""):
    """Compose a byte-valid presence-board/v1 record + its attachment id."""
    import secrets
    aid = secrets.token_hex(16)
    lines = [
        "---",
        'schema: "presence-board/v1"',
        f'attachment_id: "{aid}"',
        f'seat: "{seat}"',
        f'host: "{host}"',
        f'workspace: "{workspace}"',
        f'bed: "{bed}"',
        f'attached_at: "{board_now_stamp()}"',
    ]
    note = sanitize_note(note)
    if note:
        lines.append(f'note: "{note}"')
    lines.append("---")
    return aid, "\n".join(lines) + "\n"


def parse_record(text, fname):
    """Strict presence-board/v1 parse. Returns (state, reason, fields|None).
    state: 'valid' | 'malformed'. Never guesses; reports reason."""
    import datetime
    try:
        if "\r" in text or text.startswith("﻿"):
            return "malformed", "CRLF or BOM framing", None
        if not (text.startswith("---\n") and text.endswith("\n---\n")):
            return "malformed", "frontmatter framing", None
        if "<<<<<<<" in text or ">>>>>>>" in text:
            return "malformed", "conflict markers", None
        rows = [BOARD_ROW.match(l) for l in text[4:-5].split("\n")]
        if not all(rows) or len(rows) not in (7, 8):
            return "malformed", "row grammar or count", None
        names = [r.group(1) for r in rows]
        want = BOARD_KEYS + ["note"] if len(rows) == 8 else BOARD_KEYS
        if names != want:
            return "malformed", "key order or unknown key", None
        v = {r.group(1): r.group(2) for r in rows}
        if v["schema"] != "presence-board/v1":
            return "malformed", "schema", None
        if not re.fullmatch(r"[0-9a-f]{32}", v["attachment_id"]) \
                or fname != f"presence.{v['attachment_id']}.md":
            return "malformed", "filename/ID mismatch", None
        for k in ("seat", "host"):
            if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}", v[k]):
                return "malformed", f"{k} grammar", None
        for k in ("workspace", "bed"):
            if not v[k].startswith("~/"):
                return "malformed", f"{k} pointer", None
        t = BOARD_TS.match(v["attached_at"])
        if not t:
            return "malformed", "timestamp grammar", None
        if t.group(7) not in ("Z",) and t.group(7).startswith(("+14", "-14")) \
                and not t.group(7).endswith(":00"):
            return "malformed", "offset range", None
        try:
            datetime.date(int(t.group(1)), int(t.group(2)), int(t.group(3)))
        except ValueError:
            return "malformed", "calendar date", None
        return "valid", "", v
    except Exception as e:  # never crash a reader on hostile bytes
        return "malformed", f"parse error: {e}", None


def record_age_seconds(fields):
    """Seconds since attached_at, or None for unparseable/future (renders unknown)."""
    import datetime
    try:
        dt = datetime.datetime.fromisoformat(fields["attached_at"])
        delta = (datetime.datetime.now(datetime.timezone.utc) - dt).total_seconds()
        return None if delta < 0 else delta
    except (ValueError, KeyError):
        return None


def age_label(secs):
    if secs is None:
        return "?"
    if secs < 3600:
        return f"{int(secs // 60)}m"
    if secs < 86400:
        return f"{int(secs // 3600)}h"
    return f"{int(secs // 86400)}d"


def load_board():
    """All records on the board, parsed strictly. Sorted newest-first by name-set."""
    d = board_dir()
    out = []
    if not d.is_dir():
        return out
    own = load_own_ids()
    try:
        files = sorted(p for p in d.iterdir() if p.is_file())
    except OSError:
        return out
    for p in files:
        if not BOARD_FILENAME.match(p.name):
            continue  # foreign files are not records; ignore silently
        try:
            text = p.read_text(encoding="utf-8", errors="strict")
        except (OSError, UnicodeError):
            out.append({"state": "malformed", "reason": "unreadable bytes",
                        "path": p, "fields": None, "own": False})
            continue
        state, reason, fields = parse_record(text, p.name)
        aid = fields["attachment_id"] if fields else p.name[len("presence."):-3]
        out.append({"state": state, "reason": reason, "path": p,
                    "fields": fields, "own": aid in own})
    return out


def board_key():
    d = board_dir()
    if not d.is_dir():
        return ()
    try:
        return tuple(sorted(p.name for p in d.iterdir() if p.is_file()))
    except OSError:
        return ()


def board_mark(bed, workspace=None, seat=None, note=""):
    """Attach: exclusive-create one record. Returns (id, path). Raises on failure."""
    bed_p = Path(bed).expanduser()
    if not bed_p.is_dir():
        raise SystemExit(f"rb-mark: bed is not a directory: {bed}")
    if workspace is None:
        # git toplevel of the bed, else the bed's own tree root guess
        import subprocess as sp
        r = sp.run(["git", "-C", str(bed_p), "rev-parse", "--show-toplevel"],
                   capture_output=True, text=True)
        workspace = r.stdout.strip() if r.returncode == 0 else str(bed_p)
    seat = seat or os.environ.get("RB_SEAT", "") or "majkee"
    d = board_dir()
    d.mkdir(parents=True, exist_ok=True)
    for _ in range(3):  # fresh-ID retry per contract
        aid, record = compose_record(seat, local_host(), to_tilde(workspace),
                                     to_tilde(bed_p), note)
        # self-check: never write a contract-invalid record (e.g. a bed outside ~
        # cannot be ~-anchored; bad seat/host grammar; etc.)
        state, reason, _ = parse_record(record, f"presence.{aid}.md")
        if state != "valid":
            raise SystemExit(f"rb-mark: refusing to write invalid record ({reason})")
        target = d / f"presence.{aid}.md"
        try:
            fd = os.open(str(target), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
        except FileExistsError:
            continue  # collision: fresh ID, new filename — never touch the existing
        try:
            os.write(fd, record.encode("utf-8"))  # single write
        finally:
            os.close(fd)
        own = load_own_ids()
        own[aid] = to_tilde(bed_p)
        save_own_ids(own)
        return aid, target
    raise SystemExit("rb-mark: exclusive creation failed 3 times")


def board_unmark(aid=None, bed=None):
    """Detach own record(s). Explicit id, or all own records for a bed pointer.
    Only removes files whose id is in own state — never another owner's record."""
    own = load_own_ids()
    if aid:
        targets = [aid] if aid in own else []
        if not targets:
            raise SystemExit(f"rb-unmark: {aid} is not an own attachment (ownership law)")
    elif bed:
        want = to_tilde(Path(bed).expanduser())
        targets = [i for i, b in own.items() if b == want]
        if not targets:
            raise SystemExit(f"rb-unmark: no own attachment for bed {want}")
    else:
        targets = list(own.keys())
        if not targets:
            raise SystemExit("rb-unmark: no own attachments recorded")
    removed = []
    for i in targets:
        p = board_dir() / f"presence.{i}.md"
        try:
            p.unlink()
        except FileNotFoundError:
            pass  # already swept; still drop from own state
        own.pop(i, None)
        removed.append(i)
    save_own_ids(own)
    return removed


def board_list_plain():
    recs = load_board()
    if not recs:
        print(f"board empty — {board_dir()}")
        return 0
    for r in recs:
        if r["state"] == "valid":
            f = r["fields"]
            mark = "*" if r["own"] else " "
            note = f' · {f.get("note")}' if f.get("note") else ""
            print(f"[{age_label(record_age_seconds(f)):>3}]{mark}{f['seat']}@{f['host']} "
                  f"· {f['bed']}{note}")
        else:
            print(f"[ ! ] malformed: {r['path'].name} — {r['reason']}")
    return 0


# ── Curses escapes ───────────────────────────────────────────────────────────

GUI_EDITORS = {"subl", "code", "kate", "gedit"}  # detach — no curses escape needed


def open_editor(screen, path):
    editor = os.environ.get("EDITOR") or os.environ.get("PREFERRED_EDITOR") or "vi"
    name = os.path.basename(editor.split()[0])
    try:
        if name in GUI_EDITORS:
            subprocess.Popen([editor, str(path)], start_new_session=True,
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return f"→ {name}: {Path(path).name}"  # informational, TUI stays live
        curses.def_prog_mode()
        curses.endwin()
        try:
            rc = subprocess.call([editor, str(path)])
        finally:
            curses.reset_prog_mode()
            screen.refresh()
        return None if rc == 0 else f"{name} exited {rc}"
    except OSError as e:
        return f"editor error ({name}): {e}"


# ── Internal reader (feature: read any document without $EDITOR) ─────────────

def reader(screen, path):
    """Modal WRITELN reader. Recomputes each draw → live reload for free (1s tick)."""
    offset = 0
    while True:
        h, w = screen.getmaxyx()
        body_w = max(1, w - 2)
        doc = render_file_lines(path, body_w)
        body_h = max(1, h - 2)
        max_off = max(0, len(doc) - body_h)
        offset = max(0, min(offset, max_off))

        screen.erase()
        title = clipped(f" {path} ", w)
        safe_add(screen, 0, 0, title + " " * max(0, w - len(title)),
                 curses.A_REVERSE | curses.A_BOLD, w)
        for i, (text, attr) in enumerate(doc[offset: offset + body_h]):
            safe_add(screen, 1 + i, 1, text, attr, body_w)
        pos = f" {offset + 1}-{min(offset + body_h, len(doc))}/{len(doc)} · ↑↓ PgUp/PgDn g/G · e edit · q back "
        safe_add(screen, h - 1, 0, clipped(pos, w), curses.A_REVERSE, w)
        screen.refresh()

        try:
            key = screen.get_wch()
        except curses.error:
            continue  # tick — redraw picks up file changes
        except KeyboardInterrupt:
            return

        if key == curses.KEY_UP:
            offset -= 1
        elif key == curses.KEY_DOWN:
            offset += 1
        elif key == curses.KEY_PPAGE:
            offset -= body_h
        elif key == curses.KEY_NPAGE:
            offset += body_h
        elif key == "g":
            offset = 0
        elif key == "G":
            offset = max_off
        elif key in ("e", "E"):
            open_editor(screen, path)
        elif key in ("q", "Q", "\x1b", curses.KEY_LEFT):
            return
        elif key == curses.KEY_RESIZE:
            pass  # sizes recomputed at loop top


# ── Board modal (advisory display only — no action derives from what it shows) ─

def board_view(screen):
    offset = 0
    while True:
        h, w = screen.getmaxyx()
        recs = load_board()  # recomputed per draw → live on the 1s tick
        body_w = max(1, w - 2)

        # WRITELN: every record renders fully — wrapped lines, never clipped
        lines = []  # (text, attr)
        for r in recs:
            if r["state"] == "valid":
                f = r["fields"]
                secs = record_age_seconds(f)
                attr = c("accent", curses.A_BOLD) if r["own"] else 0
                if secs is not None and secs > 86400:
                    attr |= curses.A_DIM  # display-only staleness, client policy
                own_mark = "*" if r["own"] else " "
                head = f"[{age_label(secs):>3}]{own_mark}{f['seat']}@{f['host']}"
                for piece in wrap_line(head, body_w):
                    lines.append((piece, attr | curses.A_BOLD))
                for piece in wrap_line(f"      bed: {f['bed']}", body_w):
                    lines.append((piece, attr))
                for piece in wrap_line(f"      ws:  {f['workspace']}", body_w):
                    lines.append((piece, attr | curses.A_DIM))
                if f.get("note"):
                    for piece in wrap_line(f"      {f['note']}", body_w):
                        lines.append((piece, attr))
            else:
                for piece in wrap_line(
                        f"[ ! ] malformed: {r['path'].name} — {r['reason']}", body_w):
                    lines.append((piece, c("warn")))
            lines.append(("", 0))  # record separator
        if not lines:
            lines = [("— board empty —", curses.A_DIM)]

        body_h = max(1, h - 2)
        max_off = max(0, len(lines) - body_h)
        offset = max(0, min(offset, max_off))

        screen.erase()
        title = clipped(f" presence board · {board_dir()} · {len(recs)} records ", w)
        safe_add(screen, 0, 0, title + " " * max(0, w - len(title)),
                 curses.A_REVERSE | curses.A_BOLD, w)
        for i, (text, attr) in enumerate(lines[offset: offset + body_h]):
            safe_add(screen, 1 + i, 1, text, attr, body_w)
        hint = " ↑↓ scroll · * = own attachment · advisory only — informs, never authorizes · q back "
        safe_add(screen, h - 1, 0, clipped(hint, w), curses.A_REVERSE, w)
        screen.refresh()

        try:
            key = screen.get_wch()
        except curses.error:
            continue
        except KeyboardInterrupt:
            return
        if key == curses.KEY_UP:
            offset -= 1
        elif key == curses.KEY_DOWN:
            offset += 1
        elif key == curses.KEY_PPAGE:
            offset -= body_h
        elif key == curses.KEY_NPAGE:
            offset += body_h
        elif key in ("q", "Q", "\x1b", curses.KEY_LEFT, "B", "b"):
            return
        elif key == curses.KEY_RESIZE:
            pass


def refresh_bed_marks(beds):
    """Set bed['marked'] from valid local-host board records. Display-only."""
    pointers = set()
    for r in load_board():
        if r["state"] == "valid" and r["fields"]["host"] == local_host():
            try:
                pointers.add(str(Path(os.path.expanduser(r["fields"]["bed"])).resolve()))
            except OSError:
                pass
    for b in beds:
        try:
            b["marked"] = str(b["path"].resolve()) in pointers
        except OSError:
            b["marked"] = False


# ── Draw ──────────────────────────────────────────────────────────────────────

def draw(screen, beds, d1_cursor, d1_offset, focus,
         d2_lines, d2_offset, nodes, cursor, active_bed,
         buffer_lines, show_buffer, message):
    screen.erase()
    h, w = screen.getmaxyx()

    hints = ("↑↓ scroll · Tab focus · j/k item · J/K group · Enter read/fold · "
             "e edit · 1-5 sect · F fold-R1 · B board · m/u mark/unmark · "
             "b buffer · p collect · r reload · q quit")
    full_status = message if message else f"{len(beds)} beds · focus:{focus} · {hints}"
    hint_lines = []
    for seg in full_status.split(" · "):
        if not hint_lines or len(hint_lines[-1]) + 3 + len(seg) > w:
            hint_lines.append(seg)
        else:
            hint_lines[-1] += " · " + seg
    hint_h = min(len(hint_lines), 2)

    buf_h = 0
    if show_buffer and buffer_lines:
        buf_h = 1 + min(len(buffer_lines), 4)

    body_h = max(0, h - hint_h - buf_h)

    side = w >= 60
    left_w = max(1, int(w * 0.35)) if side else w
    right_col = left_w + 1
    right_w = max(1, w - right_col) if side else 0

    # ── D1 ──
    for offset, bed in enumerate(beds[d1_offset: d1_offset + body_h]):
        abs_i = d1_offset + offset
        is_cur = (abs_i == d1_cursor)
        sel = curses.A_REVERSE if is_cur else 0
        if focus == "d1" and is_cur:
            sel |= curses.A_BOLD
        cname, extra = STATE_STYLE.get(bed["state"], (None, 0))
        state_attr = (c(cname, extra) if cname else extra) | sel
        safe_add(screen, offset, 0, f"[{bed['state']}]", state_attr, min(3, left_w))
        label = bed["slug"] + (" ●" if bed.get("marked") else "")
        safe_add(screen, offset, 4, clipped(label, left_w - 4), sel, left_w - 4)

    if side:
        for row in range(body_h):
            safe_add(screen, row, left_w, "│", curses.A_DIM)

        # fixed strip: next: (+ raw in_flight when flagged — truth, not guess)
        d2_body_row = 1
        if active_bed:
            safe_add(screen, 0, right_col,
                     clipped(f"next: {active_bed['next_line']}", right_w),
                     c("accent", curses.A_BOLD), right_w)
            raw = active_bed.get("in_flight_raw")
            if raw is not None and raw.lower() not in ("none", "", "false", "no"):
                safe_add(screen, 1, right_col,
                         clipped(f"in_flight: {raw}", right_w),
                         c("warn", curses.A_BOLD), right_w)
                d2_body_row = 2
        d2_body_h = max(0, body_h - d2_body_row)
        max_offset = max(0, len(d2_lines) - d2_body_h)
        d2_off = max(0, min(d2_offset, max_offset))

        sel_line = nodes[cursor]["line"] if (focus == "d2" and nodes and cursor < len(nodes)) else -1

        for offset, li in enumerate(d2_lines[d2_off: d2_off + d2_body_h]):
            row = d2_body_row + offset
            if row >= body_h:
                break
            abs_line = d2_off + offset
            attr = li["attr"]
            if abs_line == sel_line:
                attr |= curses.A_REVERSE
            safe_add(screen, row, right_col, clipped(li["text"], right_w), attr, right_w)

    # ── buffer pane ──
    if buf_h:
        brow = body_h
        label = f"─ buffer ({len(buffer_lines)}) — printed at quit "
        safe_add(screen, brow, 0, clipped(label + "─" * max(0, w - len(label)), w),
                 c("accent", curses.A_BOLD), w)
        tail = buffer_lines[-(buf_h - 1):]
        for i, bl in enumerate(tail):
            safe_add(screen, brow + 1 + i, 0, clipped("  " + bl, w), c("accent"), w)

    # ── hints ──
    for li, hl in enumerate(hint_lines[:hint_h]):
        row = body_h + buf_h + li
        if row < h:
            safe_add(screen, row, 0, clipped(hl, w), curses.A_REVERSE, w)

    screen.refresh()


# ── TUI loop ──────────────────────────────────────────────────────────────────

def palette(screen, beds):
    """Returns the print buffer (list of str) for scroll-back print at quit."""
    try:
        curses.curs_set(0)
    except curses.error:
        pass
    init_colors()
    screen.keypad(True)
    screen.timeout(1000)  # 1s tick; mtime-gated reload

    d1_cursor = 0
    d1_offset = 0
    d2_offset = 0
    cursor = 0                 # index into nodes
    collapsed = set()          # folded section indices (persists across beds)
    focus = "d1"
    message = ""
    buffer_lines = []
    show_buffer = False

    d2_lines = []
    nodes = []
    last_st_mtime = 0
    last_bus_key = ()
    last_board_key = None

    def cur_bed():
        return beds[d1_cursor] if beds else None

    def right_width():
        _, w = screen.getmaxyx()
        return max(1, w - int(w * 0.35) - 1)

    def layout_heights():
        h, _ = screen.getmaxyx()
        buf_h = (1 + min(len(buffer_lines), 4)) if (show_buffer and buffer_lines) else 0
        body_h = max(0, h - 2 - buf_h)
        return body_h, max(0, body_h - 1)  # (body_h, d2_body_h)

    def rebuild():
        nonlocal d2_lines, nodes, last_st_mtime, last_bus_key
        bed = cur_bed()
        if bed is None:
            d2_lines, nodes = [], []
            return
        d2_lines, nodes = build_d2(bed, right_width(), collapsed)
        last_st_mtime = mtime_ns(bed["status_path"])
        last_bus_key = bus_key(bed["path"])

    def clamp():
        nonlocal d2_offset, cursor, d1_offset
        body_h, d2_body_h = layout_heights()
        d2_offset = max(0, min(d2_offset, max(0, len(d2_lines) - d2_body_h)))
        cursor = max(0, min(cursor, len(nodes) - 1)) if nodes else 0
        if d1_cursor < d1_offset:
            d1_offset = d1_cursor
        elif d1_cursor >= d1_offset + max(1, body_h):
            d1_offset = d1_cursor - max(1, body_h) + 1

    def scroll_to_cursor():
        nonlocal d2_offset
        if not nodes:
            return
        line_i = nodes[cursor]["line"]
        _, d2_body_h = layout_heights()
        if line_i < d2_offset:
            d2_offset = line_i
        elif line_i >= d2_offset + max(1, d2_body_h):
            d2_offset = line_i - max(1, d2_body_h) + 1

    def cursor_to_section(section):
        nonlocal cursor
        for i, n in enumerate(nodes):
            if n["kind"] == "header" and n["section"] == section:
                cursor = i
                return

    def jump_header(direction):
        nonlocal cursor
        if not nodes:
            return
        i = cursor + direction
        while 0 <= i < len(nodes):
            if nodes[i]["kind"] == "header":
                cursor = i
                return
            i += direction

    def toggle_fold(section):
        if section in collapsed:
            collapsed.discard(section)
        else:
            collapsed.add(section)
        rebuild()
        cursor_to_section(section)
        clamp()
        scroll_to_cursor()

    rebuild()

    while True:
        bed = cur_bed()

        # mtime-gated reload (1s tick)
        if bed:
            if mtime_ns(bed["status_path"]) != last_st_mtime or bus_key(bed["path"]) != last_bus_key:
                bed["next_line"] = extract_next(bed["status_path"])
                bed["in_flight_raw"] = extract_in_flight_raw(bed["status_path"])
                bed["state"] = bed_state(bed["runbook_path"], bed["status_path"])
                rebuild()
                clamp()
        bkey = board_key()
        if bkey != last_board_key:
            refresh_bed_marks(beds)
            last_board_key = bkey

        draw(screen, beds, d1_cursor, d1_offset, focus,
             d2_lines, d2_offset, nodes, cursor, bed,
             buffer_lines, show_buffer, message)
        message = ""

        try:
            key = screen.get_wch()
        except curses.error:
            continue  # timeout tick
        except KeyboardInterrupt:
            return buffer_lines

        cur_node = nodes[cursor] if (nodes and cursor < len(nodes)) else None
        cur_path = cur_node["path"] if cur_node else None

        if key == curses.KEY_RESIZE:
            rebuild()
            clamp()

        elif key == "\t":
            focus = "d2" if focus == "d1" else "d1"

        elif key in ("F", "f"):
            toggle_fold(2)  # R1 RUNBOOK

        elif key in ("r", "R"):
            if bed:
                bed["next_line"] = extract_next(bed["status_path"])
                bed["in_flight_raw"] = extract_in_flight_raw(bed["status_path"])
                bed["state"] = bed_state(bed["runbook_path"], bed["status_path"])
                rebuild()
                clamp()
                message = "reloaded"

        elif key == "b":
            show_buffer = not show_buffer
            clamp()

        elif key == "B":
            board_view(screen)
            refresh_bed_marks(beds)

        elif key in ("q", "Q", "\x1b"):
            return buffer_lines

        # --- D1 focus ---
        elif focus == "d1":
            if key == curses.KEY_UP:
                d1_cursor = max(0, d1_cursor - 1)
                d2_offset, cursor = 0, 0
                rebuild()
                clamp()
            elif key == curses.KEY_DOWN:
                d1_cursor = min(max(0, len(beds) - 1), d1_cursor + 1)
                d2_offset, cursor = 0, 0
                rebuild()
                clamp()
            elif key in ("\n", "\r", curses.KEY_ENTER):
                focus = "d2"
            elif key == "m" and bed:
                try:
                    aid, _ = board_mark(str(bed["path"]))
                    refresh_bed_marks(beds)
                    message = f"attached {aid[:8]}… to board"
                except SystemExit as e:
                    message = str(e)
            elif key == "u" and bed:
                try:
                    removed = board_unmark(bed=str(bed["path"]))
                    refresh_bed_marks(beds)
                    message = f"detached {len(removed)} own record(s)"
                except SystemExit as e:
                    message = str(e)
            elif key == "p" and bed:
                buffer_lines.append(str(bed["path"]))
                show_buffer = True
                message = f"buffered ({len(buffer_lines)})"
            elif key in ("e", "E") and bed:
                target = bed["runbook_path"] or bed["status_path"]
                if target:
                    err = open_editor(screen, target)
                    if err:
                        message = err
                else:
                    message = "no RUNBOOK or STATUS in this bed"

        # --- D2 focus ---
        elif focus == "d2":
            if key == curses.KEY_UP:
                d2_offset = max(0, d2_offset - 1)
            elif key == curses.KEY_DOWN:
                d2_offset += 1
                clamp()
            elif key == "j" and nodes:
                cursor = min(len(nodes) - 1, cursor + 1)
                scroll_to_cursor()
                clamp()
            elif key == "k" and nodes:
                cursor = max(0, cursor - 1)
                scroll_to_cursor()
            elif key == "J":
                jump_header(+1)
                scroll_to_cursor()
                clamp()
            elif key == "K":
                jump_header(-1)
                scroll_to_cursor()
            elif isinstance(key, str) and key in "12345":
                cursor_to_section(int(key) - 1)
                scroll_to_cursor()
                clamp()
            elif key in ("\n", "\r", " ", curses.KEY_ENTER):
                if cur_node and cur_node["kind"] == "header":
                    toggle_fold(cur_node["section"])
                elif cur_path and cur_path.is_file():
                    reader(screen, cur_path)
                    rebuild()  # reader may have edited via e
                    clamp()
                else:
                    message = "nothing under cursor (j/k, J/K to move)"
            elif key in ("e", "E"):
                if cur_path and cur_path.is_file():
                    err = open_editor(screen, cur_path)
                    if err:
                        message = err
                    rebuild()
                    clamp()
                else:
                    message = "cursor is not on a file"
            elif key == "p":
                target = str(cur_path) if cur_path else (str(bed["path"]) if bed else "")
                if target:
                    buffer_lines.append(target)
                    show_buffer = True
                    message = f"buffered ({len(buffer_lines)})"


# ── Entry ─────────────────────────────────────────────────────────────────────

def run_on_tty(root):
    beds = load_beds(root)
    try:
        tty_fd = os.open("/dev/tty", os.O_RDWR)
    except OSError as e:
        print(f"rb-open: cannot open /dev/tty: {e}", file=sys.stderr)
        return 2
    saved_in = os.dup(0)
    saved_out = os.dup(1)
    screen = None
    buffer_lines = []
    try:
        os.dup2(tty_fd, 0)
        os.dup2(tty_fd, 1)
        screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        buffer_lines = palette(screen, beds) or []
    finally:
        if screen:
            try:
                screen.keypad(False)
                curses.nocbreak()
                curses.echo()
                curses.endwin()
            except curses.error:
                pass
        os.dup2(saved_in, 0)
        os.dup2(saved_out, 1)
        os.close(saved_in)
        os.close(saved_out)
        os.close(tty_fd)
    if buffer_lines:
        print("── rb buffer ──")
        for line in buffer_lines:
            print(line)
    return 0


def board_cli(argv):
    parser = argparse.ArgumentParser(prog="runbook.py board",
                                     description="presence-board/v1 client (advisory)")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list", help="render all records; * marks own attachments")
    pm = sub.add_parser("mark", help="attach: exclusive-create one record")
    pm.add_argument("--bed", required=True)
    pm.add_argument("--workspace", default=None)
    pm.add_argument("--seat", default=None)
    pm.add_argument("--note", default="")
    pu = sub.add_parser("unmark", help="detach own record(s) — never another owner's")
    pu.add_argument("--id", default=None)
    pu.add_argument("--bed", default=None)
    args = parser.parse_args(argv)
    if args.cmd == "list":
        return board_list_plain()
    if args.cmd == "mark":
        aid, path = board_mark(args.bed, args.workspace, args.seat, args.note)
        print(f"attached: {aid}\n{path}")
        return 0
    if args.cmd == "unmark":
        removed = board_unmark(aid=args.id, bed=args.bed)
        for i in removed:
            print(f"detached: {i}")
        return 0
    return 1


def selftest():
    """Sandboxed selftest — temp tree + temp board, zero touches outside it.
    Covers the truth-display regression class (next: block scalars, in_flight
    raw flag), gate states, D2 build/fold, and the full board contract cycle."""
    import tempfile
    failures = []

    def check(label, cond):
        print(("PASS  " if cond else "FAIL  ") + label)
        if not cond:
            failures.append(label)

    with tempfile.TemporaryDirectory(prefix="rb-selftest.") as td:
        root = Path(td) / ".dev" / "session"
        # bed-a: canonical — fenced yaml, flat quoted next, in_flight none
        a = root / "bed-a"; (a / "_bus").mkdir(parents=True)
        (a / "RUNBOOK.md").write_text("# RUNBOOK\n```yaml\ngoal: test\n```\n")
        (a / "STATUS.md").write_text(
            '# S\n```yaml\nnext: "do the thing"\nin_flight: none\n```\n')
        (a / "_bus" / "01.seat.point.md").write_text("x\n")
        # bed-b: RUNBOOK only → ·
        b = root / "bed-b"; b.mkdir()
        (b / "RUNBOOK.md").write_text("# R\n")
        # bed-c: empty → ?
        (root / "bed-c").mkdir()
        # bed-d: lowercase status (drift), folded next: >-, non-canon in_flight → ! + ~
        d = root / "bed-d"; d.mkdir()
        (d / "RUNBOOK.md").write_text("# R\n")
        (d / "status.md").write_text(
            "# S\n```yaml\nnext: >-\n  first folded line\n  second folded line\n"
            "in_flight: none — but with a trailing comment\n```\n")

        beds = {x["path"].name: x for x in load_beds(root)}
        check("gate states → · ? !", [beds[k]["state"] for k in
              ("bed-a", "bed-b", "bed-c", "bed-d")] == ["→", "·", "?", "!"])
        check("lowercase drift marker ~", beds["bed-d"]["slug"] == "bed-d~")
        check("flat quoted next", beds["bed-a"]["next_line"] == "do the thing")
        check("folded >- next resolved",
              beds["bed-d"]["next_line"] == "first folded line second folded line")
        check("in_flight raw carried",
              beds["bed-d"]["in_flight_raw"] == "none — but with a trailing comment")
        check("canonical none idle", _inflight_idle(beds["bed-a"]["in_flight_raw"]))
        check("non-canon flags active", not _inflight_idle(beds["bed-d"]["in_flight_raw"]))

        lines, nodes = build_d2(beds["bed-a"], 60, set())
        check("D2 five headers", sum(1 for n in nodes if n["kind"] == "header") == 5)
        check("D2 bus item present",
              any(n["path"] and n["path"].name == "01.seat.point.md" for n in nodes))
        folded, _ = build_d2(beds["bed-a"], 60, {0, 1, 2, 3, 4})
        check("full fold collapses", len(folded) < len(lines))

        # board contract cycle in sandbox (HOME retargeted so ~-anchoring works)
        os.environ["RB_BOARD"] = str(Path(td) / "_active")
        os.environ["RB_STATE"] = str(Path(td) / "state")
        os.environ.setdefault("MACHINE_NAME", "selftest")
        saved_home = os.environ["HOME"]
        os.environ["HOME"] = td
        try:
            try:
                board_mark("/etc", seat="selftest")
                check("outside-~ bed refused", False)
            except SystemExit:
                check("outside-~ bed refused", True)
            aid, rpath = board_mark(str(a), seat="selftest", note='q"uo\\te stripped')
            rec_text, rec_name = rpath.read_text(), rpath.name
            state, reason, fields = parse_record(rec_text, rec_name)
            check("board record valid", state == "valid")
            check("note sanitized", '"' not in fields.get("note", '"'))
            check("own flagged", load_board()[0]["own"])
            try:
                board_unmark(aid="f" * 32); check("foreign unmark rejected", False)
            except SystemExit:
                check("foreign unmark rejected", True)
            board_unmark(aid=aid)
            check("detach empties board", load_board() == [])
            bad = Path(os.environ["RB_BOARD"]) / ("presence." + "a" * 32 + ".md")
            bad.write_text("---\nschema: \"presence-board/v1\"\n---\n")
            check("malformed reported not hidden",
                  [r["state"] for r in load_board()] == ["malformed"])
            check("calendar 02-30 rejected", parse_record(rec_text.replace(
                fields["attached_at"][:10], "2026-02-30"), rec_name)[0] == "malformed")
        finally:
            os.environ["HOME"] = saved_home

    print(("SELFTEST PASS" if not failures else
           f"SELFTEST FAIL — {len(failures)}: {failures}"))
    return 0 if not failures else 1


def main():
    if sys.argv[1:2] == ["board"]:
        return board_cli(sys.argv[2:])
    if sys.argv[1:2] == ["selftest"]:
        return selftest()
    parser = argparse.ArgumentParser(description="session browser (rb-open)")
    parser.add_argument("--root", default=None, help="explicit .dev/session/ path")
    args = parser.parse_args()
    root = find_root(args.root)
    if root is None:
        print("rb-open: could not locate .dev/session/ — pass --root or set $RB_ROOT",
              file=sys.stderr)
        return 1
    return run_on_tty(root)


if __name__ == "__main__":
    raise SystemExit(main())
