#!/usr/bin/env python3
"""Stable curses selector for mailbox archive and restore actions."""

import argparse
import curses
import os
import sys
import textwrap


def parse_args():
    parser = argparse.ArgumentParser(description="select mail to archive or restore")
    parser.add_argument("--map", required=True, dest="map_file", help="mail TSV file")
    return parser.parse_args()


def load_map(map_file):
    try:
        if os.stat(map_file).st_size == 0:
            raise ValueError("map file is empty")
        with open(map_file, "r", encoding="utf-8") as source:
            lines = source.readlines()
    except (OSError, ValueError) as error:
        print(f"mail-palette: {error}", file=sys.stderr)
        raise SystemExit(2)

    mail_rows = []
    malformed = 0
    for line in lines[1:]:
        fields = line.rstrip("\r\n").split("\t")
        if len(fields) != 4 or fields[0] not in ("inbox", "archive"):
            malformed += 1
            continue
        view, receiver, filename, full_path = fields
        mail_rows.append(
            {
                "view": view,
                "receiver": receiver,
                "filename": filename,
                "fullpath": full_path,
            }
        )
    return mail_rows, malformed


def grouped_mail(mail_rows, active_view):
    groups = {}
    for item in mail_rows:
        if item["view"] == active_view:
            groups.setdefault(item["receiver"], []).append(item)
    for items in groups.values():
        items.sort(key=lambda item: item["filename"].casefold())
    return groups


def tree_rows(groups, expanded):
    rows = []
    for receiver in sorted(groups, key=str.casefold):
        rows.append(
            {"kind": "receiver", "receiver": receiver, "count": len(groups[receiver])}
        )
        if receiver in expanded:
            for item in groups[receiver]:
                rows.append({"kind": "file", "item": item, "receiver": receiver})
    return rows


def filtered_rows(mail_rows, active_view, filter_text):
    needle = filter_text.casefold()
    return [
        {"kind": "file", "item": item, "receiver": item["receiver"]}
        for item in mail_rows
        if item["view"] == active_view
        and needle in item["filename"].casefold()
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


def draw(screen, rows, cursor, filter_text, expanded, active_view, marks):
    screen.erase()
    height, width = screen.getmaxyx()

    # Build status/help string
    hints = "↑↓ move · →← fold · space mark · tab view · a act · type filter · esc/q quit"
    prefix = f"{len(rows)} rows · {active_view}"
    if filter_text:
        prefix += f" · /{filter_text}"
    status = f"{prefix} · {hints}"

    # Wrap help onto multiple lines by packing segments on " · " boundaries
    segments = status.split(" · ")
    help_lines = []
    current_line = []
    current_length = 0

    for segment in segments:
        if current_line:
            # Need to add " · " before this segment
            needed_length = current_length + len(" · ") + len(segment)
        else:
            needed_length = len(segment)

        if current_line and needed_length > width:
            # Current line is full, start a new one
            help_lines.append(" · ".join(current_line))
            current_line = [segment]
            current_length = len(segment)
        else:
            current_line.append(segment)
            current_length = needed_length

    if current_line:
        help_lines.append(" · ".join(current_line))

    # Cap help height to at most half the screen
    help_height = min(len(help_lines), max(1, height // 2))
    help_lines = help_lines[:help_height]

    # Adjust body height for the list area
    body_height = max(0, height - help_height)

    # Draw list area
    if not rows and body_height > 0:
        safe_add(screen, 0, 0, clipped("(empty)", width), 0, width)
    elif rows:
        start, visible = visible_slice(rows, cursor, body_height)
        for offset, row in enumerate(visible):
            absolute = start + offset
            attr = curses.A_REVERSE if absolute == cursor else 0
            if row["kind"] == "receiver":
                marker = "▾" if row["receiver"] in expanded else "▸"
                label = f"{marker} {row['receiver']} ({row['count']})"
                attr |= curses.A_BOLD
            else:
                mark = "[x]" if marks.get(row["item"]["fullpath"]) else "[ ]"
                prefix = "" if filter_text else "  "
                label = f"{prefix}{mark} {row['item']['filename']}"
            safe_add(screen, offset, 0, clipped(label, width), attr, width)

    # Draw wrapped help lines at the bottom
    for line_offset, help_line in enumerate(help_lines):
        help_row = body_height + line_offset
        safe_add(screen, help_row, 0, clipped(help_line, width), curses.A_REVERSE, width)

    screen.refresh()


def receiver_index(rows, receiver):
    for index, row in enumerate(rows):
        if row["kind"] == "receiver" and row["receiver"] == receiver:
            return index
    return 0


def palette(screen, mail_rows):
    # Default to all receivers expanded on every launch — so the reloop reopens
    # into the open tree (← still collapses within a session).
    expanded = {item["receiver"] for item in mail_rows}
    marks = {}
    filter_text = ""
    active_view = "inbox"
    cursor = 0
    try:
        curses.curs_set(0)
    except curses.error:
        pass
    screen.keypad(True)

    while True:
        groups = grouped_mail(mail_rows, active_view)
        rows = (
            filtered_rows(mail_rows, active_view, filter_text)
            if filter_text
            else tree_rows(groups, expanded)
        )
        cursor = max(0, min(cursor, len(rows) - 1)) if rows else 0
        draw(screen, rows, cursor, filter_text, expanded, active_view, marks)
        key = screen.get_wch()

        if key == curses.KEY_RESIZE:
            continue
        if key == curses.KEY_UP:
            cursor = max(0, cursor - 1)
        elif key == curses.KEY_DOWN:
            cursor = min(max(0, len(rows) - 1), cursor + 1)
        elif key == curses.KEY_RIGHT and not filter_text and rows:
            row = rows[cursor]
            if row["kind"] == "receiver":
                expanded.add(row["receiver"])
        elif key == curses.KEY_LEFT and not filter_text and rows:
            row = rows[cursor]
            receiver = row["receiver"]
            if row["kind"] == "file" or receiver in expanded:
                expanded.discard(receiver)
                cursor = receiver_index(tree_rows(groups, expanded), receiver)
        elif key == "\t":
            active_view = "archive" if active_view == "inbox" else "inbox"
            cursor = 0
        elif key == " " and rows:
            row = rows[cursor]
            if row["kind"] == "file":
                full_path = row["item"]["fullpath"]
                marks[full_path] = not marks.get(full_path, False)
        elif key in ("a", "A"):
            selected = [item for item in mail_rows if marks.get(item["fullpath"])]
            return (selected, 0)
        elif key == "\x1b":
            if filter_text:
                filter_text = ""
                cursor = 0
            else:
                return None, 1
        elif key in (curses.KEY_BACKSPACE, "\b", "\x7f"):
            if filter_text:
                filter_text = filter_text[:-1]
                cursor = 0
        elif isinstance(key, str) and key.isprintable():
            if key == "q" and not filter_text:
                return None, 1
            filter_text += key
            cursor = 0


def run_on_tty(mail_rows):
    try:
        tty_fd = os.open("/dev/tty", os.O_RDWR)
    except OSError as error:
        print(f"mail-palette: cannot open /dev/tty: {error}", file=sys.stderr)
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
        result = palette(screen, mail_rows)
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
    mail_rows, _malformed = load_map(arguments.map_file)
    selected, status = run_on_tty(mail_rows)
    if status == 0:
        # Preserve source TSV order so multi-file actions are deterministic.
        for item in selected:
            verb = "archive" if item["view"] == "inbox" else "restore"
            print(f"{item['receiver']}/{item['filename']}\t{verb}")
    return status


if __name__ == "__main__":
    raise SystemExit(main())
