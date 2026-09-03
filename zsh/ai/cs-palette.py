#!/usr/bin/env python3
"""Cold-start vault explorer + mover (merged tool, 2026-09-03).

The palette compresses reading speed AND move operations in one TUI:
D1 (left) shows cards with state prefix; D2 (right-top) shows frontmatter;
D3 (right-bottom) shows the first prompt block + runbook line.

Invoke as ``python3 cs-palette.py --vault VAULT_ROOT [--sort date|mtime|name]``.
VAULT_ROOT is the already-resolved absolute path to the vault (resolved by the
zsh wrappers via temple-project-map so this file never hardcodes a /home path).

Layout:
  D1 (left)         — card/ + routines/ (or archive/ when toggled), sorted
                       by filename-embedded date newest-first (default).
                       [c] prefix = card/, [r] prefix = routines/.
  D2 (right-top)    — the selected card's raw YAML frontmatter, verbatim.
  D3 (right-bottom) — the selected card's first ``###### prompt`` fenced
                       block + its ``runbook:`` line, if present.

Keybinds:
  ↑ ↓           navigate list
  Enter         print resume: to stdout and exit (session start)
  e             open card in $EDITOR
  r             open runbook: target in $EDITOR
  a             toggle archive view
  s             cycle sort: date → mtime → name → date
  c             move selected card → card/
  x             move selected card → archive/
  t             move selected card → routines/
  q / Esc       quit — print absolute path of selected card to stdout (exit 0);
                exit 1 silently only when the vault is empty

Sort default: date (filename YYYY-MM-DD newest-first; no-date cards sink last).
Override: TEMPLE_SORT=date|mtime|name env var, or --sort flag, or 's' in TUI.
"""

import argparse
import curses
import os
import re
import subprocess
import sys
import textwrap

import cs_vault


_MOVE_KEYS = {"c": "card", "x": "archive", "t": "routines"}
_SORT_CYCLE = ["date", "mtime", "name"]

# State prefix shown in D1 when in mixed card/routines view.
_STATE_PREFIX = {"card": "[c] ", "routines": "[r] "}


def parse_args():
    parser = argparse.ArgumentParser(description="explore and manage the cold-start vault")
    parser.add_argument("--vault", required=True, dest="vault_root", help="resolved _cold-start root")
    parser.add_argument(
        "--sort",
        choices=["date", "mtime", "name"],
        default=os.environ.get("TEMPLE_SORT", "date"),
        help="sort: date = filename date newest-first (default), mtime = modification time, name = alpha",
    )
    return parser.parse_args()


def extract_date(filename):
    """Return the last YYYY-MM-DD found in filename, or '' if absent (sorts last)."""
    matches = re.findall(r"\d{4}-\d{2}-\d{2}", filename)
    return matches[-1] if matches else ""


def load_rows(vault_root, archive_view, sort_mode):
    if archive_view:
        raw = [(n, f, m, "archive") for n, f, m in cs_vault.list_state(vault_root, "archive")]
    else:
        raw = (
            [(n, f, m, "card") for n, f, m in cs_vault.list_state(vault_root, "card")]
            + [(n, f, m, "routines") for n, f, m in cs_vault.list_state(vault_root, "routines")]
        )
    if sort_mode == "mtime":
        raw.sort(key=lambda r: (r[2], r[0]), reverse=True)
    elif sort_mode == "name":
        raw.sort(key=lambda r: r[0].casefold())
    else:  # date (default)
        raw.sort(key=lambda r: (extract_date(r[0]), r[0].casefold()), reverse=True)
    return [{"filename": n, "fullpath": f, "mtime": m, "state": s} for n, f, m, s in raw]


def clipped(value, width):
    if width <= 0:
        return ""
    if len(value) <= width:
        return value
    if width == 1:
        return "…"
    return value[: width - 1] + "…"


def safe_add(screen, row, column, value, attr=0, width=None):
    height, screen_width = screen.getmaxyx()
    if row < 0 or row >= height or column < 0 or column >= screen_width:
        return
    available = screen_width - column
    if width is not None:
        available = min(available, max(0, width))
    if available <= 0:
        return
    try:
        screen.addnstr(row, column, value, available, attr)
    except curses.error:
        pass


def visible_slice(rows, cursor, height):
    if height <= 0:
        return 0, []
    start = max(0, cursor - height + 1)
    if cursor < start:
        start = cursor
    return start, rows[start : start + height]


def wrap_block(text, width):
    if not text:
        return []
    lines = []
    for raw_line in text.splitlines():
        if not raw_line:
            lines.append("")
            continue
        wrapped = textwrap.wrap(raw_line, width=max(1, width), subsequent_indent="  ")
        lines.extend(wrapped or [""])
    return lines


def d2_lines(row, width):
    if row is None:
        return ["(no card selected)"]
    block = cs_vault.read_frontmatter_block(row["fullpath"])
    if block is None:
        return ["— no frontmatter (legacy) —"]
    return wrap_block(block.rstrip("\n"), width)


def d3_lines(row, width):
    if row is None:
        return ["—"]
    prompt = cs_vault.first_prompt_block(row["fullpath"])
    frontmatter = cs_vault.read_frontmatter_block(row["fullpath"])
    keys = cs_vault.parse_flat_keys(frontmatter)
    runbook = keys.get("runbook")

    lines = []
    if prompt:
        lines.append("###### prompt")
        lines.append("```text")
        lines.extend(wrap_block(prompt, width))
        lines.append("```")
    if runbook:
        if lines:
            lines.append("")
        lines.append(f"runbook: {runbook}")
    if not lines:
        return ["—"]
    return lines


def draw(screen, rows, cursor, archive_view, message, sort_mode):
    screen.erase()
    height, width = screen.getmaxyx()

    hints = "↑↓ move · enter resume · e edit · r runbook · a archive · s sort · c→card x→archive t→routines · q/esc→path+quit"
    view_label = "archive" if archive_view else "card/+routines"
    prefix = f"{len(rows)} cards · {view_label} · sort:{sort_mode}"
    status = message if message else f"{prefix} · {hints}"

    segments = status.split(" · ")
    help_lines = []
    current_line = []
    current_length = 0
    for segment in segments:
        needed_length = (current_length + len(" · ") + len(segment)) if current_line else len(segment)
        if current_line and needed_length > width:
            help_lines.append(" · ".join(current_line))
            current_line = [segment]
            current_length = len(segment)
        else:
            current_line.append(segment)
            current_length = needed_length
    if current_line:
        help_lines.append(" · ".join(current_line))
    help_height = min(len(help_lines), max(1, height // 2))
    help_lines = help_lines[:help_height]
    body_height = max(0, height - help_height)

    side_by_side = width >= 60
    left_width = max(1, int(width * 0.35)) if side_by_side else width
    right_column = left_width + 1
    right_width = max(1, width - right_column)

    selected = rows[cursor] if rows else None

    # D1 — left column: state prefix [c]/[r] shown in mixed card/routines view
    if not rows and body_height > 0:
        safe_add(screen, 0, 0, clipped("(vault empty in this view)", left_width), 0, left_width)
    elif rows:
        start, visible = visible_slice(rows, cursor, body_height)
        for offset, row in enumerate(visible):
            absolute = start + offset
            attr = curses.A_REVERSE if absolute == cursor else 0
            if not archive_view:
                prefix_str = _STATE_PREFIX.get(row["state"], "    ")
                label = f"{prefix_str}{row['filename']}"
            else:
                label = row["filename"]
            safe_add(screen, offset, 0, clipped(label, left_width), attr, left_width)

    if side_by_side:
        for row_number in range(body_height):
            safe_add(screen, row_number, left_width, "│")

        d2_height = max(1, body_height // 2) if body_height > 1 else body_height
        d3_start = d2_height + 1  # +1 for the divider row
        d3_height = max(0, body_height - d3_start)

        safe_add(screen, 0, right_column, clipped("D2 · frontmatter", right_width), curses.A_BOLD, right_width)
        for offset, line in enumerate(d2_lines(selected, right_width)):
            row_number = offset + 1
            if row_number >= d2_height:
                break
            safe_add(screen, row_number, right_column, clipped(line, right_width), 0, right_width)

        if d2_height < body_height:
            safe_add(screen, d2_height, right_column, clipped("─" * right_width, right_width))

        if d3_height > 0:
            safe_add(screen, d3_start, right_column, clipped("D3 · prompt-0 + runbook", right_width), curses.A_BOLD, right_width)
            for offset, line in enumerate(d3_lines(selected, right_width)):
                row_number = d3_start + offset + 1
                if row_number >= height - help_height:
                    break
                safe_add(screen, row_number, right_column, clipped(line, right_width), 0, right_width)

    for line_offset, help_line in enumerate(help_lines):
        help_row = body_height + line_offset
        safe_add(screen, help_row, 0, clipped(help_line, width), curses.A_REVERSE, width)

    screen.refresh()


def _open_in_editor(screen, path):
    editor = os.environ.get("EDITOR") or os.environ.get("PREFERRED_EDITOR") or "vi"
    try:
        curses.def_prog_mode()
        curses.endwin()
        try:
            subprocess.call([editor, path])
        finally:
            curses.reset_prog_mode()
            screen.refresh()
        return None
    except OSError as error:
        return f"cs-palette: could not launch '{editor}': {error}"


def palette(screen, sort_mode, vault_root):
    try:
        curses.curs_set(0)
    except curses.error:
        pass
    screen.keypad(True)

    archive_view = False
    cursor = 0
    message = ""

    while True:
        rows = load_rows(vault_root, archive_view, sort_mode)
        cursor = max(0, min(cursor, len(rows) - 1)) if rows else 0
        draw(screen, rows, cursor, archive_view, message, sort_mode)
        message = ""
        try:
            key = screen.get_wch()
        except KeyboardInterrupt:
            return None, 1

        if key == curses.KEY_RESIZE:
            continue
        if key == curses.KEY_UP:
            cursor = max(0, cursor - 1)
        elif key == curses.KEY_DOWN:
            cursor = min(max(0, len(rows) - 1), cursor + 1)
        elif key in ("s", "S"):
            idx = _SORT_CYCLE.index(sort_mode)
            sort_mode = _SORT_CYCLE[(idx + 1) % len(_SORT_CYCLE)]
            cursor = 0
        elif key in ("a", "A"):
            archive_view = not archive_view
            cursor = 0
        elif isinstance(key, str) and key.lower() in _MOVE_KEYS and rows:
            dest = _MOVE_KEYS[key.lower()]
            row = rows[cursor]
            if row["state"] == dest:
                message = f"'{row['filename']}' is already in {dest}/"
            else:
                _, err = cs_vault.move_card(vault_root, row["fullpath"], dest)
                if err:
                    message = f"move failed: {err}"
                else:
                    message = f"→ {dest}/ · '{row['filename']}'"
        elif key in ("\n", "\r", curses.KEY_ENTER):
            if not rows:
                continue
            row = rows[cursor]
            frontmatter = cs_vault.read_frontmatter_block(row["fullpath"])
            keys = cs_vault.parse_flat_keys(frontmatter)
            resume = keys.get("resume")
            if resume:
                return resume, 0
            message = f"'{row['filename']}' — no resume: key (legacy or incomplete card)"
        elif key in ("e", "E"):
            if not rows:
                continue
            row = rows[cursor]
            error = _open_in_editor(screen, row["fullpath"])
            if error:
                message = error
        elif key in ("r", "R"):
            if not rows:
                continue
            row = rows[cursor]
            frontmatter = cs_vault.read_frontmatter_block(row["fullpath"])
            keys = cs_vault.parse_flat_keys(frontmatter)
            runbook = keys.get("runbook")
            if not runbook:
                message = f"'{row['filename']}' — no runbook: key on this card"
                continue
            target = os.path.expanduser(runbook)
            error = _open_in_editor(screen, target)
            if error:
                message = error
        elif key in ("q", "Q", "\x1b"):
            # Flush the selected card's absolute path to stdout on quit.
            # Exit 1 only when the vault is empty (nothing to report).
            if rows:
                return rows[cursor]["fullpath"], 0
            return None, 1


def run_on_tty(sort_mode, vault_root):
    try:
        tty_fd = os.open("/dev/tty", os.O_RDWR)
    except OSError as error:
        print(f"cs-palette: cannot open /dev/tty: {error}", file=sys.stderr)
        return None, 2

    saved_input = os.dup(0)
    saved_output = os.dup(1)
    screen = None
    result = (None, 1)
    try:
        os.dup2(tty_fd, 0)
        os.dup2(tty_fd, 1)
        screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        result = palette(screen, sort_mode, vault_root)
    finally:
        if screen is not None:
            try:
                screen.keypad(False)
                curses.nocbreak()
                curses.echo()
                curses.endwin()
            except curses.error:
                pass
        os.dup2(saved_input, 0)
        os.dup2(saved_output, 1)
        os.close(saved_input)
        os.close(saved_output)
        os.close(tty_fd)
    return result


def main():
    arguments = parse_args()
    vault_root = os.path.expanduser(arguments.vault_root)
    output, status = run_on_tty(arguments.sort, vault_root)
    # output is either the resume: text (Enter) or the card's fullpath (q/Esc).
    if status == 0 and output:
        print(output)
    return status


if __name__ == "__main__":
    raise SystemExit(main())
