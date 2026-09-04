#!/usr/bin/env python3
"""runbook.py — nablarva session browser.

Browse .dev/session/ beds: D1 list with gate-state, D2 sectioned view
(STATUS / _bus/ / RUNBOOK / bed-root files / raw/).

Invoke via:  python3 runbook.py [--root <.dev/session path>]
Root resolution: --root > $RB_ROOT env > $PROJECT_NAB_PATH/.dev/session > walk-up.

Keybinds:
  ↑ ↓           scroll D2 (text) / navigate D1
  j / k         move item cursor in D2 (file entries only)
  1–5           jump D2 to section (R2 STATUS / R5 _bus / R1 RUNBOOK / R3 files / R4 raw)
  Tab           switch focus D1 ↔ D2
  F             toggle R1 RUNBOOK section
  r             manual reload STATUS + _bus/
  e / Enter     open item-cursor file in $EDITOR (curses escape)
  p             print selected bed path (or item path in D2) to terminal scroll-back
  q / Esc       quit
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


# ── Helpers (cs-palette pattern, stdlib only) ─────────────────────────────────

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


def wrap_text(text, width):
    """WRITELN law: wrap, never clip body text. No hyphen breaks; long words wrap."""
    if not text:
        return []
    lines = []
    for raw in text.splitlines():
        if not raw.strip():
            lines.append("")
            continue
        wrapped = textwrap.wrap(
            raw,
            width=max(1, width),
            break_on_hyphens=False,
            break_long_words=True,
        )
        lines.extend(wrapped or [""])
    return lines


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


def flat_keys(block):
    result = {}
    if not block:
        return result
    for line in block.splitlines():
        m = re.match(r"^\s*`?(\w[\w_-]*):`?\s*(.*)", line)
        if m:
            result[m.group(1)] = m.group(2).strip().strip('"').strip("'")
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
        keys = flat_keys(block)
        val = keys.get("next", "")
        if val:
            return val
    m = re.search(r"^\s*`?next:`?\s*(.*)", text, re.M)
    if m:
        val = m.group(1).strip().strip('"').strip("'")
        if val:
            return val
    return "—"


def extract_in_flight(path):
    if path is None or not path.is_file():
        return False
    block = read_fenced_block(path)
    if not block:
        return False
    keys = flat_keys(block)
    val = keys.get("in_flight", "none")
    return val.lower() not in ("none", "", "false", "no")


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
    nab = os.environ.get("PROJECT_NAB_PATH")
    if nab:
        p = Path(nab).expanduser() / ".dev" / "session"
        if p.is_dir():
            return p
    # walk-up: stop at the right .dev/session level
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
    if extract_in_flight(st_path):
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
        state = bed_state(rb, st)
        slug = child.name
        drift = "~" if (st and st.name != "STATUS.md") else ""
        next_line = extract_next(st)
        beds.append({
            "path": child,
            "slug": slug + drift,
            "state": state,
            "status_path": st,
            "runbook_path": rb,
            "next_line": next_line,
        })
    return beds


# ── D2 section builder ────────────────────────────────────────────────────────

def read_file_text(path, width):
    if path is None or not path.is_file():
        return ["—"]
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ["(read error)"]
    return wrap_text(text, width)


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
            [p for p in bed.iterdir() if p.is_file() and p.name not in exclude and not p.name.startswith(".")],
            key=lambda p: p.name,
        )
    except OSError:
        return []


def build_d2(bed_info, width, r1_hidden):
    """Build D2 line list and section-start indices.

    Each line: {"text": str, "is_item": bool, "path": Path|None}
    section_starts: [idx for R2, R5, R1, R3, R4] (5 entries)
    item_paths: flat list of paths for item cursor
    """
    bed = bed_info["path"]
    lines = []
    section_starts = []
    item_paths = []

    def header(label):
        bar = "─" * max(0, width - len(label) - 4)
        lines.append({"text": f"── {label} {bar}", "is_item": False, "path": None})

    def item(path, label=None):
        lines.append({"text": f"  {label or path.name}", "is_item": True, "path": path})
        item_paths.append(path)

    def text_lines(tl):
        for t in tl:
            lines.append({"text": t, "is_item": False, "path": None})

    def empty():
        lines.append({"text": "  —", "is_item": False, "path": None})

    # R2 — STATUS (section 1)
    section_starts.append(len(lines))
    header("R2 · STATUS")
    st = bed_info["status_path"]
    if st:
        item(st, st.name)
        text_lines(read_file_text(st, width))
    else:
        empty()

    # R5 — _bus/ (section 2, most critical — sits high)
    section_starts.append(len(lines))
    header("R5 · _bus/")
    bus_files = list_dir(bed / "_bus")
    if bus_files:
        for p in bus_files:
            item(p)
    else:
        empty()

    # R1 — RUNBOOK (section 3, toggleable)
    section_starts.append(len(lines))
    rb = bed_info["runbook_path"]
    if r1_hidden:
        header("R1 · RUNBOOK  [F to show]")
    else:
        header("R1 · RUNBOOK  [F to hide]")
        if rb:
            item(rb, rb.name)
            text_lines(read_file_text(rb, width))
        else:
            empty()

    # R3 — bed-root files (section 4)
    section_starts.append(len(lines))
    header("R3 · bed files")
    root_items = bed_root_items(bed)
    if root_items:
        for p in root_items:
            item(p)
    else:
        empty()

    # R4 — raw/ (section 5)
    section_starts.append(len(lines))
    header("R4 · raw/")
    raw_files = list_dir(bed / "raw")
    if raw_files:
        for p in raw_files:
            item(p)
    else:
        empty()

    return lines, section_starts, item_paths


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


# ── Curses helpers ────────────────────────────────────────────────────────────

def open_editor(screen, path):
    editor = os.environ.get("EDITOR") or os.environ.get("PREFERRED_EDITOR") or "vi"
    try:
        curses.def_prog_mode()
        curses.endwin()
        try:
            subprocess.call([editor, str(path)])
        finally:
            curses.reset_prog_mode()
            screen.refresh()
    except OSError as e:
        return f"editor error: {e}"
    return None


def print_to_scrollback(screen, text):
    curses.def_prog_mode()
    curses.endwin()
    try:
        print(text)
    finally:
        curses.reset_prog_mode()
        screen.refresh()


# ── Draw ──────────────────────────────────────────────────────────────────────

def draw(screen, beds, d1_cursor, d1_offset, focus,
         d2_lines, d2_offset, d2_item_idx, d2_section_starts, d2_item_paths,
         active_bed, r1_hidden, message):
    screen.erase()
    h, w = screen.getmaxyx()

    # hint bar (bottom, max 2 rows)
    hints = ("↑↓ scroll · j/k item · 1-5 jump · Tab focus · "
             "F R1 · r reload · e edit · p path · q quit")
    state_str = f"focus:{focus}"
    full_status = message if message else f"{len(beds)} beds · {state_str} · {hints}"
    hint_lines = []
    for seg in full_status.split(" · "):
        if not hint_lines or len(hint_lines[-1]) + 3 + len(seg) > w:
            hint_lines.append(seg)
        else:
            hint_lines[-1] += " · " + seg
    hint_h = min(len(hint_lines), 2)
    body_h = max(0, h - hint_h)

    # layout
    side = w >= 60
    left_w = max(1, int(w * 0.35)) if side else w
    right_col = left_w + 1
    right_w = max(1, w - right_col) if side else 0

    # D1
    d1_vis = body_h
    for offset, bed in enumerate(beds[d1_offset: d1_offset + d1_vis]):
        abs_i = d1_offset + offset
        is_cur = (abs_i == d1_cursor)
        attr = curses.A_REVERSE if is_cur else 0
        if focus == "d1" and is_cur:
            attr |= curses.A_BOLD
        label = f"[{bed['state']}] {bed['slug']}"
        safe_add(screen, offset, 0, clipped(label, left_w), attr, left_w)

    if side:
        # vertical separator
        for row in range(body_h):
            safe_add(screen, row, left_w, "│")

        # D2 fixed strip: next:
        next_text = ""
        if active_bed:
            next_text = clipped(f"next: {active_bed['next_line']}", right_w)
            safe_add(screen, 0, right_col, next_text, curses.A_BOLD, right_w)
        d2_body_row = 1  # first scrollable row

        d2_body_h = max(0, body_h - d2_body_row)
        total = len(d2_lines)
        max_offset = max(0, total - d2_body_h)
        d2_off = max(0, min(d2_offset, max_offset))

        # selected item path
        sel_path = (d2_item_paths[d2_item_idx]
                    if focus == "d2" and d2_item_paths and d2_item_idx < len(d2_item_paths)
                    else None)

        for offset, line_info in enumerate(d2_lines[d2_off: d2_off + d2_body_h]):
            row = d2_body_row + offset
            if row >= body_h:
                break
            is_item = line_info["is_item"]
            lpath = line_info["path"]
            is_sel = (is_item and lpath is not None and lpath == sel_path)
            attr = curses.A_REVERSE if is_sel else 0
            safe_add(screen, row, right_col, clipped(line_info["text"], right_w), attr, right_w)

    # hints
    for li, hl in enumerate(hint_lines[:hint_h]):
        row = body_h + li
        if row < h:
            safe_add(screen, row, 0, clipped(hl, w), curses.A_REVERSE, w)

    screen.refresh()


# ── TUI loop ──────────────────────────────────────────────────────────────────

def palette(screen, beds, root):
    try:
        curses.curs_set(0)
    except curses.error:
        pass
    screen.keypad(True)
    screen.timeout(1000)  # 1 s tick; mtime-gated reload

    d1_cursor = 0
    d1_offset = 0
    d2_offset = 0
    d2_item_idx = 0
    r1_hidden = False
    focus = "d1"
    message = ""

    d2_lines = []
    d2_section_starts = []
    d2_item_paths = []
    last_st_mtime = 0
    last_bus_key = ()

    def cur_bed():
        return beds[d1_cursor] if beds else None

    def right_width():
        _, w = screen.getmaxyx()
        return max(1, w - int(w * 0.35) - 1)

    def rebuild():
        nonlocal d2_lines, d2_section_starts, d2_item_paths
        nonlocal last_st_mtime, last_bus_key
        bed = cur_bed()
        if bed is None:
            d2_lines, d2_section_starts, d2_item_paths = [], [], []
            return
        d2_lines, d2_section_starts, d2_item_paths = build_d2(bed, right_width(), r1_hidden)
        last_st_mtime = mtime_ns(bed["status_path"])
        last_bus_key = bus_key(bed["path"])

    def clamp():
        nonlocal d2_offset, d2_item_idx, d1_offset
        h, _ = screen.getmaxyx()
        body_h = max(0, h - 2)
        d2_body_h = max(0, body_h - 1)
        max_d2 = max(0, len(d2_lines) - d2_body_h)
        nonlocal d2_offset
        d2_offset = max(0, min(d2_offset, max_d2))
        nonlocal d2_item_idx
        d2_item_idx = max(0, min(d2_item_idx, len(d2_item_paths) - 1)) if d2_item_paths else 0
        d1_vis = body_h
        nonlocal d1_offset
        if d1_cursor < d1_offset:
            d1_offset = d1_cursor
        elif d1_cursor >= d1_offset + d1_vis:
            d1_offset = d1_cursor - d1_vis + 1

    def item_line_idx(item_idx):
        """Find the line index in d2_lines for a given item_idx."""
        count = 0
        for i, ln in enumerate(d2_lines):
            if ln["is_item"]:
                if count == item_idx:
                    return i
                count += 1
        return 0

    def scroll_to_item(item_idx):
        nonlocal d2_offset
        line_i = item_line_idx(item_idx)
        h, _ = screen.getmaxyx()
        body_h = max(0, h - 2)
        d2_body_h = max(0, body_h - 1)
        if line_i < d2_offset:
            d2_offset = line_i
        elif line_i >= d2_offset + d2_body_h:
            d2_offset = line_i - d2_body_h + 1

    rebuild()

    while True:
        bed = cur_bed()

        # mtime-gated reload
        if bed:
            cur_st = mtime_ns(bed["status_path"])
            cur_bk = bus_key(bed["path"])
            if cur_st != last_st_mtime or cur_bk != last_bus_key:
                bed["next_line"] = extract_next(bed["status_path"])
                rebuild()
                clamp()

        # item path for p in D2
        d2_item_path = (d2_item_paths[d2_item_idx]
                        if focus == "d2" and d2_item_paths and d2_item_idx < len(d2_item_paths)
                        else None)

        draw(screen, beds, d1_cursor, d1_offset, focus,
             d2_lines, d2_offset, d2_item_idx, d2_section_starts, d2_item_paths,
             bed, r1_hidden, message)
        message = ""

        try:
            key = screen.get_wch()
        except curses.error:
            continue  # timeout — tick only
        except KeyboardInterrupt:
            return

        if key == curses.KEY_RESIZE:
            rebuild()
            clamp()
            continue

        # --- Tab: switch focus ---
        if key == "\t":
            focus = "d2" if focus == "d1" else "d1"

        # --- F: toggle R1 ---
        elif key in ("F", "f"):
            r1_hidden = not r1_hidden
            rebuild()
            clamp()

        # --- r: manual reload ---
        elif key in ("r", "R"):
            if bed:
                bed["next_line"] = extract_next(bed["status_path"])
                rebuild()
                clamp()
                message = "reloaded"

        # --- q / Esc: quit ---
        elif key in ("q", "Q", "\x1b"):
            return

        # --- D1 focus ---
        elif focus == "d1":
            if key == curses.KEY_UP:
                d1_cursor = max(0, d1_cursor - 1)
                d2_offset = 0
                d2_item_idx = 0
                rebuild()
                clamp()
            elif key == curses.KEY_DOWN:
                d1_cursor = min(max(0, len(beds) - 1), d1_cursor + 1)
                d2_offset = 0
                d2_item_idx = 0
                rebuild()
                clamp()
            elif key in ("p", "P") and bed:
                print_to_scrollback(screen, str(bed["path"]))
                message = "↓ printed bed path"
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
            elif key in ("j", "J") and d2_item_paths:
                d2_item_idx = min(len(d2_item_paths) - 1, d2_item_idx + 1)
                scroll_to_item(d2_item_idx)
                clamp()
            elif key in ("k", "K") and d2_item_paths:
                d2_item_idx = max(0, d2_item_idx - 1)
                scroll_to_item(d2_item_idx)
            elif isinstance(key, str) and key in "12345" and d2_section_starts:
                sec = int(key) - 1
                if sec < len(d2_section_starts):
                    d2_offset = d2_section_starts[sec]
                    clamp()
            elif key in ("e", "E", "\n", "\r", curses.KEY_ENTER):
                if d2_item_path and d2_item_path.is_file():
                    err = open_editor(screen, d2_item_path)
                    if err:
                        message = err
                else:
                    message = "no file at item cursor (j/k to move)"
            elif key in ("p", "P"):
                target = str(d2_item_path) if d2_item_path else (str(bed["path"]) if bed else "")
                if target:
                    print_to_scrollback(screen, target)
                    message = "↓ printed path"


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
    try:
        os.dup2(tty_fd, 0)
        os.dup2(tty_fd, 1)
        screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        palette(screen, beds, root)
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
    return 0


def main():
    parser = argparse.ArgumentParser(description="nablarva session browser")
    parser.add_argument("--root", default=None, help="explicit .dev/session/ path")
    args = parser.parse_args()
    root = find_root(args.root)
    if root is None:
        print("rb-open: could not locate .dev/session/ — pass --root or set $RB_ROOT or $PROJECT_NAB_PATH",
              file=sys.stderr)
        return 1
    return run_on_tty(root)


if __name__ == "__main__":
    raise SystemExit(main())
