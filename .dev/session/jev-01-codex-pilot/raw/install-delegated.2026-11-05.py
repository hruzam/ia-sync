#!/usr/bin/env python3
"""Scoped, hash-pinned Jev delegated-audit update; no inference or engagement creation."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import socket
import stat
import tempfile

REPO = Path('/home/hruzam/ia-sync')
BED = REPO / '.dev/session/jev-01-codex-pilot'
TARGET = Path('/home/hruzam/.config/zsh/jev')
BACKUP = Path('/home/hruzam/.config/zsh/.jev-delegated-backup-20261105')
CHANGED = ('store.py', 'jev.py', 'README.md')

def sha(data):
    return hashlib.sha256(data).hexdigest()

def plain(path):
    for part in (path, *path.parents):
        if part.is_symlink():
            raise RuntimeError('Symlink refused: ' + str(part))

def syncdir(path):
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    if socket.gethostname().split('.')[0] != 'hruzam-120922':
        raise RuntimeError('Office-only installation')
    manifest = json.loads((BED / 'raw/delegated-install-manifest.2026-11-05.json').read_text())
    previous = manifest['before']; expected = manifest['after']
    if set(expected) != set(previous) or set(expected) != {'store.py','jev.py','jev.zsh','README.md','kernel.py','provider.py','PROVIDER.md','base.zsh','keyboard.zsh'}:
        raise RuntimeError('Unexpected scope')
    plain(TARGET); plain(BACKUP)
    if BACKUP.exists() and (not BACKUP.is_dir() or BACKUP.stat().st_uid != os.getuid() or stat.S_IMODE(BACKUP.stat().st_mode) != 0o700):
        raise RuntimeError('Unexpected backup directory')
    sources = {}
    for name in expected:
        source = REPO / 'zsh/jev' / name; live = TARGET / name
        plain(source); plain(live)
        sources[name] = source.read_bytes()
        if sha(sources[name]) != expected[name] or sha(live.read_bytes()) not in {previous[name],expected[name]}:
            raise RuntimeError('Source or live bytes diverged: ' + name)
        if name not in CHANGED and previous[name] != expected[name]:
            raise RuntimeError('Unrelated change: ' + name)
        saved = BACKUP / name
        plain(saved)
        if saved.exists() and sha(saved.read_bytes()) != previous[name]:
            raise RuntimeError('Unexpected backup bytes: ' + name)
    print(json.dumps({'mode':'apply' if args.apply else 'dry-run','changed':list(CHANGED),'target':str(TARGET)}))
    if not args.apply:
        return
    if not BACKUP.exists():
        BACKUP.mkdir(mode=0o700); syncdir(BACKUP.parent)
    for name in CHANGED:
        live = TARGET / name; saved = BACKUP / name
        old = live.read_bytes()
        if sha(old) == expected[name]:
            continue
        if not saved.exists():
            with saved.open('xb') as stream:
                os.fchmod(stream.fileno(),0o600); stream.write(old); stream.flush(); os.fsync(stream.fileno())
            syncdir(BACKUP)
        fd, tmp = tempfile.mkstemp(prefix='.jev-update-',dir=TARGET)
        try:
            with os.fdopen(fd,'wb') as stream:
                os.fchmod(stream.fileno(),0o644); stream.write(sources[name]); stream.flush(); os.fsync(stream.fileno())
            os.replace(tmp,live); syncdir(TARGET)
        finally:
            if os.path.exists(tmp):
                os.unlink(tmp)
    observed = {name:sha((TARGET/name).read_bytes()) for name in expected}
    if observed != expected:
        raise RuntimeError('Post-install hash mismatch')
    receipt = {'at':datetime.datetime.now().astimezone().isoformat(),'host':socket.gethostname(),'files':observed,'backup':str(BACKUP),'provider_calls':0,'credential_access':False,'engagement_created':False}
    (BED/'raw/delegated-install-receipt.2026-11-05.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print('Scoped delegated-audit update installed; verified hashes; runtime history untouched.')

if __name__ == '__main__':
    main()
