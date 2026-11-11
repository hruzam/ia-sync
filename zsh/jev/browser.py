#!/usr/bin/env python3
"""Browse verified Jev sessions, mark events and compose a private reading view."""
import argparse
import curses
import os
from pathlib import Path
import sys
import tempfile

import kernel
import reader
import store


def discover(root):
    """Discover sessions through the vault's normal locks and validated replay."""
    vault = store.Vault(root)
    store.directory(vault.root)
    projects = vault.root / 'projects'
    store.directory(projects)
    project_paths = list(projects.iterdir())
    store.require(len(project_paths) <= 10000, 'project lookup bound exceeded')
    sessions = []
    for project in sorted(project_paths):
        store.require(store.HASH.fullmatch(project.name), 'unknown managed project path')
        store.directory(project)
        paths = list(project.iterdir())
        store.require(len(paths) <= 20000, 'session lookup bound exceeded')
        for path in sorted(paths):
            store.require(path.suffix in {'.lock', '.jsonl'} and store.HASH.fullmatch(path.stem),
                          'unknown managed session path')
            store.private(path)
            if path.suffix != '.jsonl':
                continue
            with vault._locked(project.name, path.stem, shared=True) as ledger:
                store.require(bool(ledger.events), 'empty ledger: cannot identify session')
                opening = ledger.events[0]['data']
                sessions.append({'session': ledger.session_id, 'project': opening.get('project', 'unknown'),
                                 'bed': opening.get('bed', 'unknown'), 'count': len(ledger.events),
                                 'tail': ledger.tail is not None})
    ids = [entry['session'] for entry in sessions]
    store.require(len(ids) == len(set(ids)), 'duplicate session IDs')
    return vault, sessions


def runtime_dir():
    for name in (os.environ.get('XDG_RUNTIME_DIR'), f'/run/user/{os.getuid()}'):
        if not name:
            continue
        base = Path(name)
        try:
            info = base.lstat()
            if base.is_dir() and not base.is_symlink() and info.st_uid == os.getuid() and info.st_mode & 0o077 == 0:
                return Path(tempfile.mkdtemp(prefix='jev-view-', dir=base))
        except OSError:
            pass
    raise kernel.Invalid('private runtime directory unavailable')


def event_label(event):
    data = event['data']
    text = ''
    if event['kind'] == 'memory':
        note = data.get('note', {})
        text = str(note.get('text', '')) if isinstance(note, dict) else ''
    return f"{event['sequence']:>4}  {event['kind']:<12} {event.get('at', '')}  {' '.join(reader._text(text).split())[:100]}"


def browse(screen, vault, sessions):
    curses.curs_set(0)
    screen.keypad(True)
    events, selected, marked, memories = None, None, set(), False
    position, offset, message = 0, 0, ''
    while True:
        height, width = screen.getmaxyx()
        shown = sessions if events is None else [e for e in events if not memories or e['kind'] == 'memory']
        position = min(position, max(0, len(shown)-1))
        available = max(1, height-5)
        offset = max(0, min(offset, position))
        if position >= offset + available:
            offset = position - available + 1
        screen.erase()
        def line(row, text, attr=0):
            if 0 <= row < height and width > 1:
                try: screen.addnstr(row, 0, reader._text(str(text)).replace('\n',' ').replace('\t',' '), width-1, attr)
                except curses.error: pass
        line(0, 'Jev memory navigator — ' + ('sessions' if events is None else selected['bed']), curses.A_BOLD)
        line(1, 'Up/Down move  Enter open  q quit' if events is None else
             'Space mark  a mark visible  p compose  m memories/all  b sessions  q quit')
        for row, item in enumerate(shown[offset:offset+available], 3):
            if events is None:
                text = f"{item['bed']}  |  {item['session']}  |  {item['count']} events" + ('  |  INCOMPLETE TAIL' if item['tail'] else '')
            else:
                text = f"[{'x' if item['sequence'] in marked else ' '}] " + event_label(item)
            line(row, text, curses.A_REVERSE if row-3+offset == position else 0)
        line(height-1, message or ('No memory events; press m to show all events.' if events is not None and not shown else ''))
        screen.refresh()
        key = screen.getch()
        message = ''
        if key in (ord('q'), 27): return None
        if key in (curses.KEY_UP, ord('k')): position = max(0, position-1)
        elif key in (curses.KEY_DOWN, ord('j')): position = min(max(0, len(shown)-1), position+1)
        elif events is None and key in (10, 13, curses.KEY_ENTER) and shown:
            selected = shown[position]
            try:
                with vault.selected(selected['session']) as ledger:
                    events = list(ledger.events)
                marked, memories, position, offset = set(), False, 0, 0
            except (kernel.Invalid, OSError) as error: message = str(error)
        elif events is not None and key == ord('b'):
            events, selected, position, offset = None, None, 0, 0
        elif events is not None and key == ord('m'):
            memories, position, offset = not memories, 0, 0
        elif events is not None and key == ord(' ') and shown:
            marked.symmetric_difference_update({shown[position]['sequence']})
        elif events is not None and key == ord('a'):
            marked.update(e['sequence'] for e in shown)
        elif events is not None and key == ord('p'):
            if not marked:
                message = 'Mark events with Space before composing.'
                continue
            try:
                with vault.selected(selected['session']) as ledger:
                    current = {e['sequence']: e['event_id'] for e in ledger.events}
                    observed = {e['sequence']: e['event_id'] for e in events}
                    store.require(all(current.get(i) == observed.get(i) for i in marked), 'selected events changed; reopen session')
                    content = reader.render(ledger, sequences=marked)
                folder = runtime_dir()
                return reader.write_output(folder / 'view.md', content)
            except (kernel.Invalid, OSError) as error: message = str(error)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', default='~/.jev', help='private Jev vault')
    args = parser.parse_args()
    try:
        if not sys.stdin.isatty() or not sys.stdout.isatty():
            raise kernel.Invalid('interactive terminal required')
        vault, sessions = discover(args.root)
        if not sessions: raise kernel.Invalid('no Jev sessions found')
        view = curses.wrapper(browse, vault, sessions)
        if view: print(f'Jev reading view: {view}\nOpen: subl {view}\nPrivate and temporary; source ledger is unchanged.')
        return 0
    except (kernel.Invalid, OSError, curses.error) as error:
        print('jev-browse: ' + reader._text(str(error)), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
