#!/usr/bin/env python3
"""Terminal command palette backed by a TSV map.

Invoke as ``python3 command-palette.py --map PALETTE_MAP``.  The map contains
``scope<TAB>command<TAB>help<TAB>engine``; its first line is a comment header.

Selecting a command writes only that command to the process's original stdout
and exits 0.  Cancelling writes nothing and exits 1.  A missing or zero-byte map
writes an error to stderr and exits 2.

Python's curses wrapper does not expose newterm(3).  To give curses the same
/dev/tty-bound terminal while keeping the ``sys.stdout`` object untouched, this
program saves descriptors 0 and 1, temporarily dup2s /dev/tty onto both before
calling curses.initscr(), restores them in a finally block, and only afterward
uses the single final ``print(command)``.  Thus redirected real stdout never
receives screen control sequences.
"""

import argparse
import curses
import os
import sys
import textwrap


def parse_args():
    parser = argparse.ArgumentParser(description="select a command from a palette map")
    parser.add_argument("--map", required=True, dest="map_file", help="palette TSV file")
    return parser.parse_args()


def load_map(map_file):
    try:
        if os.stat(map_file).st_size == 0:
            raise ValueError("map file is empty")
        with open(map_file, "r", encoding="utf-8") as source:
            lines = source.readlines()
    except (OSError, ValueError) as error:
        print(f"command-palette: {error}", file=sys.stderr)
        raise SystemExit(2)

    commands = []
    malformed = 0
    for line in lines[1:]:
        fields = line.rstrip("\r\n").split("\t")
        if len(fields) != 4:
            malformed += 1
            continue
        scope, command, help_text, engine = fields
        commands.append(
            {"scope": scope, "command": command, "help": help_text, "engine": engine}
        )
    if not commands:
        print("command-palette: map file contains no commands", file=sys.stderr)
        raise SystemExit(2)
    commands.sort(key=lambda item: (item["scope"].casefold(), item["command"].casefold()))
    return commands, malformed


def grouped_commands(commands):
    groups = {}
    for item in commands:
        groups.setdefault(item["scope"], []).append(item)
    for items in groups.values():
        items.sort(key=lambda item: item["command"].casefold())
    return groups


def tree_rows(groups, expanded):
    rows = []
    for scope in sorted(groups, key=str.casefold):
        rows.append({"kind": "scope", "scope": scope, "count": len(groups[scope])})
        if scope in expanded:
            for item in groups[scope]:
                rows.append({"kind": "command", "item": item, "scope": scope})
    return rows


def filtered_rows(commands, filter_text):
    needle = filter_text.casefold()
    return [
        {"kind": "command", "item": item, "scope": item["scope"]}
        for item in commands
        if needle in item["command"].casefold() or needle in item["help"].casefold()
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


def detail_lines(row, width):
    if row is None:
        return ["No matching commands"]
    if row["kind"] == "scope":
        return [f"Scope: {row['scope']}", f"Commands: {row['count']}"]

    item = row["item"]
    label_width = 9
    wrap_width = max(1, width - label_width)
    help_lines = textwrap.wrap(item["help"], width=wrap_width) or [""]
    result = [f"Command: {item['command']}", f"Help:    {help_lines[0]}"]
    result.extend(" " * label_width + line for line in help_lines[1:])
    result.extend([f"Engine:  {item['engine']}", f"Scope:   {item['scope']}"])
    return result


def visible_slice(rows, cursor, height):
    if height <= 0:
        return 0, []
    start = max(0, cursor - height + 1)
    if cursor < start:
        start = cursor
    return start, rows[start : start + height]


def draw(screen, rows, cursor, filter_text, expanded):
    screen.erase()
    height, width = screen.getmaxyx()
    selected = rows[cursor] if rows else None

    # Under 60 columns the detail pane is hidden so list and status stay usable.
    side_by_side = width >= 60
    left_width = max(1, int(width * 0.4)) if side_by_side else width
    detail_column = left_width + 1
    list_width = max(1, left_width - (1 if side_by_side else 0))

    # Build status/help string
    hints = "↑↓ move · →← fold · enter select · type to filter · esc quit"
    prefix = f"{len(rows)} items"
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

    start, visible = visible_slice(rows, cursor, body_height)
    for offset, row in enumerate(visible):
        absolute = start + offset
        attr = curses.A_REVERSE if absolute == cursor else 0
        if row["kind"] == "scope":
            marker = "▾" if row["scope"] in expanded else "▸"
            label = f"{marker} {row['scope']} ({row['count']})"
            attr |= curses.A_BOLD
        else:
            prefix = "" if filter_text else "  "
            label = prefix + row["item"]["command"]
        safe_add(screen, offset, 0, clipped(label, list_width), attr, list_width)

    if side_by_side:
        for row_number in range(body_height):
            safe_add(screen, row_number, left_width, "│")
        for row_number, line in enumerate(detail_lines(selected, width - detail_column)):
            if row_number >= body_height:
                break
            safe_add(screen, row_number, detail_column, line, 0, width - detail_column)

    # Draw wrapped help lines at the bottom
    for line_offset, help_line in enumerate(help_lines):
        help_row = body_height + line_offset
        safe_add(screen, help_row, 0, clipped(help_line, width), curses.A_REVERSE, width)

    screen.refresh()


def scope_index(rows, scope):
    for index, row in enumerate(rows):
        if row["kind"] == "scope" and row["scope"] == scope:
            return index
    return 0


def palette(screen, commands):
    groups = grouped_commands(commands)
    expanded = set()
    filter_text = ""
    cursor = 0
    try:
        curses.curs_set(0)
    except curses.error:
        pass
    screen.keypad(True)

    while True:
        rows = filtered_rows(commands, filter_text) if filter_text else tree_rows(groups, expanded)
        cursor = max(0, min(cursor, len(rows) - 1)) if rows else 0
        draw(screen, rows, cursor, filter_text, expanded)
        key = screen.get_wch()

        if key == curses.KEY_RESIZE:
            continue
        if key == curses.KEY_UP:
            cursor = max(0, cursor - 1)
        elif key == curses.KEY_DOWN:
            cursor = min(max(0, len(rows) - 1), cursor + 1)
        elif key == curses.KEY_RIGHT and not filter_text and rows:
            row = rows[cursor]
            if row["kind"] == "scope":
                expanded.add(row["scope"])
        elif key == curses.KEY_LEFT and not filter_text and rows:
            row = rows[cursor]
            scope = row["scope"]
            if row["kind"] == "command" or scope in expanded:
                expanded.discard(scope)
                cursor = scope_index(tree_rows(groups, expanded), scope)
        elif key in ("\n", "\r", curses.KEY_ENTER):
            if not rows:
                continue
            row = rows[cursor]
            if row["kind"] == "command":
                return row["item"]["command"], 0
            expanded.add(row["scope"])
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


def run_on_tty(commands):
    try:
        tty_fd = os.open("/dev/tty", os.O_RDWR)
    except OSError as error:
        print(f"command-palette: cannot open /dev/tty: {error}", file=sys.stderr)
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
        result = palette(screen, commands)
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
    commands, _malformed = load_map(arguments.map_file)
    command, status = run_on_tty(commands)
    if status == 0:
        print(command)
    return status


if __name__ == "__main__":
    raise SystemExit(main())
