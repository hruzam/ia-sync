#!/usr/bin/env python3
"""Browse a project for JSONL files, select lines and make a local Markdown view."""
import argparse
import curses
import json
import os
from pathlib import Path
import sys

import jsonl_reader as reader


def entries(directory):
    """List immediate directories and JSONL files, without following symlinks."""
    return sorted((p for p in directory.iterdir()
                   if not p.is_symlink() and (p.is_dir() or p.is_file() and p.suffix.lower() == '.jsonl')),
                  key=lambda p: (not p.is_dir(), p.name.casefold()))


def summary(record):
    if 'error' in record:
        return 'INVALID: ' + record['error']
    value = record['value']
    if isinstance(value, dict):
        text = '; '.join(f'{k}: {str(v)[:85]}' for k, v in list(value.items())[:3])
    else:
        text = str(value)
    return ' '.join(reader.visible(text).split())


def browse(screen, root):
    curses.curs_set(0)
    screen.keypad(True)
    directory, position, offset = root, 0, 0
    state, marked, message = None, set(), ''
    while True:
        height, width = screen.getmaxyx()
        try:
            items = entries(directory) if state is None else state['records']
        except OSError as error:
            items, message = [], str(error)
        position = min(position, max(0, len(items) - 1))
        available = max(1, height - 5)
        offset = max(0, min(offset, position))
        if position >= offset + available:
            offset = position - available + 1
        screen.erase()
        def line(row, text, attr=0):
            if 0 <= row < height and width > 1:
                try:
                    screen.addnstr(row, 0, reader.visible(text).replace('\n', ' ').replace('\t', ' '), width - 1, attr)
                except curses.error:
                    pass
        line(0, 'JSONL browser  |  ' + (str(directory) if state is None else state['source']), curses.A_BOLD)
        line(1, 'Up/Down move  Enter open  Backspace parent  q quit' if state is None else
             'Up/Down move  Space mark  p print Markdown  b files  q quit')
        for row, item in enumerate(items[offset:offset + available], 3):
            if state is None:
                text = ('[dir]  ' if item.is_dir() else '[jsonl] ') + item.name
            else:
                text = f"[{'x' if item['line'] in marked else ' '}] {item['line']:>5}  {summary(item)}"
            line(row, text, curses.A_REVERSE if row - 3 + offset == position else 0)
        line(height - 1, message)
        screen.refresh()
        key = screen.getch()
        message = ''
        if key in (ord('q'), 27):
            return None
        if key in (curses.KEY_UP, ord('k')):
            position = max(0, position - 1)
        elif key in (curses.KEY_DOWN, ord('j')):
            position = min(max(0, len(items) - 1), position + 1)
        elif state is None and key in (curses.KEY_BACKSPACE, 127, 8):
            directory, position, offset = directory.parent, 0, 0
        elif state is not None and key == ord('b'):
            state, marked, position, offset = None, set(), 0, 0
        elif state is None and key in (10, 13, curses.KEY_ENTER) and items:
            choice = items[position]
            if choice.is_dir():
                directory, position, offset = choice, 0, 0
            else:
                try:
                    state = reader.load_source(choice)
                    marked, position, offset = set(), 0, 0
                except (OSError, ValueError, RecursionError) as error:
                    message = str(error)
        elif state is not None and key == ord(' ') and items:
            number = items[position]['line']
            marked.symmetric_difference_update({number})
        elif state is not None and key == ord('p'):
            if not marked:
                message = 'Mark at least one record with Space first.'
                continue
            try:
                cache = reader.cache_path()
                if Path(state['source']).is_relative_to(cache.resolve()):
                    raise ValueError('source cannot be inside the disposable cache')
                state['selected'] = sorted(marked)
                reader.private_write(cache / 'view.md', reader.render_snapshot(state))
                reader.private_write(cache / 'snapshot.json', json.dumps(state, ensure_ascii=False))
                return cache / 'view.md'
            except (OSError, ValueError, RecursionError) as error:
                message = str(error)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', nargs='?', default='.', help='project directory to start browsing')
    args = parser.parse_args()
    try:
        root = Path(args.root).expanduser().resolve(strict=True)
        if not root.is_dir():
            raise ValueError('starting path must be a directory')
        if not sys.stdin.isatty() or not sys.stdout.isatty():
            raise ValueError('interactive terminal required')
        view = curses.wrapper(browse, root)
        if view:
            print(f'Markdown: {view}\nOpen: tools-jsonl open\nKeep: tools-jsonl save /chosen/output.md')
        return 0
    except (OSError, ValueError, curses.error) as error:
        print('tools-browse: ' + reader.visible(error), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
