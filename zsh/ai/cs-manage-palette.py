#!/usr/bin/env python3
"""Stable curses selector for cold-start vault state moves (card/routines/archive).

Curses backend for temple-cs-manage.zsh — mirrors mail-palette.py's selector
grammar (tree list, mark, act), adapted from a 2-state view toggle (mail's
inbox/archive) to 3 simultaneous state groups, since the cold-start vault has
no per-receiver split and a move can target any of the three folders.

This script never touches the filesystem — it only decides. It reads the TSV
map built by temple-cs-manage.zsh (columns: state<TAB>filename<TAB>fullpath)
and, once the operator marks files and presses a destination key, prints
"<filename>\tdest" lines to stdout and exits 0. The actual mv is
temple-cs-manage.zsh's job (folder = state; no frontmatter rewriting, ever).
"""

import argparse
import curses
import os
import sys
import textwrap


DEST_KEYS = {"c": "card", "x": "archive", "t": "routines"}
STATE_LABELS = {"card": "card", "routines": "routines", "archive": "archive"}


def parse_args():
    parser = argparse.ArgumentParser(description="select cold-start cards to move")
    parser.add_argument("--map", required=True, dest="map_file", help="cold-start TSV map")
    return parser.parse_args()


def load_map(map_file):
    try:
        if os.stat(map_file).st_size == 0:
            raise ValueError("map file is empty")
        with open(map_file, "r", encoding="utf-8") as source:
            lines = source.readlines()
    except (OSError, ValueError) as error:
        print(f"cs-manage-palette: {error}", file=sys.stderr)
        raise SystemExit(2)

    rows = []
    for line in lines[1:]:
        fields = line.rstrip("\r\n").split("\t")
        if len(fields) != 3 or fields[0] not in STATE_LABELS:
            continue
        state, filename, full_path = fields
        rows.append({"state": state, "filename": filename, "fullpath": full_path})
    return rows


def grouped(rows):
    groups = {}
    for item in rows:
        groups.setdefault(item["state"], []).append(item)
    for items in groups.values():
        items.sort(key=lambda item: item["filename"].casefold())
    return groups


def tree_rows(groups, expanded):
    rows = []
    for state in ("card", "routines", "archive"):
        items = groups.get(state, [])
        rows.append({"kind": "group", "state": state, "count": len(items)})
        if state in expanded:
            for item in items:
                rows.append({"kind": "file", "item": item, "state": state})
    return rows


def filtered_rows(all_rows, filter_text):
    needle = filter_text.casefold()
    return [
        {"kind": "file", "item": item, "state": item["state"]}
        for item in all_rows
        if needle in item["filename"].casefold()
    ]


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


def draw(screen, rows, cursor, filter_text, expanded, marks, message):
    screen.erase()
    height, width = screen.getmaxyx()

    hints = "↑↓ move · →← fold · space mark · c/x/t move to card|archive|routines · type filter · esc/q quit"
    prefix = f"{len(rows)} rows"
    if filter_text:
        prefix += f" · /{filter_text}"
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

    if not rows and body_height > 0:
        safe_add(screen, 0, 0, clipped("(empty)", width), 0, width)
    elif rows:
        start, visible = visible_slice(rows, cursor, body_height)
        for offset, row in enumerate(visible):
            absolute = start + offset
            attr = curses.A_REVERSE if absolute == cursor else 0
            if row["kind"] == "group":
                marker = "▾" if row["state"] in expanded else "▸"
                label = f"{marker} {STATE_LABELS[row['state']]} ({row['count']})"
                attr |= curses.A_BOLD
            else:
                mark = "[x]" if marks.get(row["item"]["fullpath"]) else "[ ]"
                lead = "" if filter_text else "  "
                label = f"{lead}{mark} {row['item']['filename']}"
            safe_add(screen, offset, 0, clipped(label, width), attr, width)

    for line_offset, help_line in enumerate(help_lines):
        help_row = body_height + line_offset
        safe_add(screen, help_row, 0, clipped(help_line, width), curses.A_REVERSE, width)

    screen.refresh()


def group_index(rows, state):
    for index, row in enumerate(rows):
        if row["kind"] == "group" and row["state"] == state:
            return index
    return 0


def palette(screen, all_rows):
    expanded = {"card", "routines", "archive"}
    marks = {}
    filter_text = ""
    cursor = 0
    message = ""
    try:
        curses.curs_set(0)
    except curses.error:
        pass
    screen.keypad(True)

    while True:
        groups = grouped(all_rows)
        rows = filtered_rows(all_rows, filter_text) if filter_text else tree_rows(groups, expanded)
        cursor = max(0, min(cursor, len(rows) - 1)) if rows else 0
        draw(screen, rows, cursor, filter_text, expanded, marks, message)
        message = ""
        key = screen.get_wch()

        if key == curses.KEY_RESIZE:
            continue
        if key == curses.KEY_UP:
            cursor = max(0, cursor - 1)
        elif key == curses.KEY_DOWN:
            cursor = min(max(0, len(rows) - 1), cursor + 1)
        elif key == curses.KEY_RIGHT and not filter_text and rows:
            row = rows[cursor]
            if row["kind"] == "group":
                expanded.add(row["state"])
        elif key == curses.KEY_LEFT and not filter_text and rows:
            row = rows[cursor]
            state = row["state"]
            if row["kind"] == "file" or state in expanded:
                expanded.discard(state)
                cursor = group_index(tree_rows(groups, expanded), state)
        elif key == " " and rows:
            row = rows[cursor]
            if row["kind"] == "file":
                full_path = row["item"]["fullpath"]
                marks[full_path] = not marks.get(full_path, False)
        elif isinstance(key, str) and key.lower() in DEST_KEYS and not filter_text:
            dest = DEST_KEYS[key.lower()]
            selected_items = [item for item in all_rows if marks.get(item["fullpath"])]
            if not selected_items and rows and rows[cursor]["kind"] == "file":
                selected_items = [rows[cursor]["item"]]
            moves = [item for item in selected_items if item["state"] != dest]
            if not moves:
                message = "nothing to move (mark a file, or it is already there)"
                continue
            return moves, dest, 0
        elif key == "\x1b":
            if filter_text:
                filter_text = ""
                cursor = 0
            else:
                return [], None, 1
        elif key in (curses.KEY_BACKSPACE, "\b", "\x7f"):
            if filter_text:
                filter_text = filter_text[:-1]
                cursor = 0
        elif isinstance(key, str) and key.isprintable():
            if key == "q" and not filter_text:
                return [], None, 1
            filter_text += key
            cursor = 0


def run_on_tty(all_rows):
    try:
        tty_fd = os.open("/dev/tty", os.O_RDWR)
    except OSError as error:
        print(f"cs-manage-palette: cannot open /dev/tty: {error}", file=sys.stderr)
        return [], None, 2

    saved_input = os.dup(0)
    saved_output = os.dup(1)
    screen = None
    result = ([], None, 1)
    try:
        os.dup2(tty_fd, 0)
        os.dup2(tty_fd, 1)
        screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        result = palette(screen, all_rows)
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
    all_rows = load_map(arguments.map_file)
    moves, dest, status = run_on_tty(all_rows)
    if status == 0:
        for item in moves:
            print(f"{item['filename']}\t{dest}")
    return status


if __name__ == "__main__":
    raise SystemExit(main())
