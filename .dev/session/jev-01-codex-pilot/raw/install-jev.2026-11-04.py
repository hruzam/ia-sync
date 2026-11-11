#!/usr/bin/env python3
"""Install only hash-pinned Jev source and its single shell signpost."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import socket
import stat
import tempfile

REPO = Path('/home/hruzam/ia-sync')
BED = REPO / '.dev/session/jev-01-codex-pilot'
TARGET = Path('/home/hruzam/.config/zsh')
RUNTIME = Path('/home/hruzam/.jev')
NAMES = {'base.zsh', 'keyboard.zsh', 'jev.zsh', 'kernel.py', 'provider.py', 'store.py', 'jev.py', 'README.md', 'PROVIDER.md'}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def plain(path):
    for candidate in (path, *path.parents):
        if candidate.is_symlink():
            raise RuntimeError('Refusing symlink: ' + str(candidate))


def sync_dir(path):
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def private_dir(path):
    plain(path)
    if path.exists():
        info = path.stat()
        if not path.is_dir() or info.st_uid != os.getuid() or stat.S_IMODE(info.st_mode) != 0o700:
            raise RuntimeError('Existing private directory has unexpected owner/mode: ' + str(path))


def write_file(path, data, mode):
    with path.open('xb') as stream:
        os.fchmod(stream.fileno(), mode)
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    manifest = json.loads((BED / 'raw/install-manifest.2026-11-04.json').read_text())
    if socket.gethostname().split('.')[0] != 'hruzam-120922':
        raise RuntimeError('This reviewed installation is office-only')
    if set(manifest['files']) != NAMES:
        raise RuntimeError('Unexpected installation manifest scope')
    files = {}
    for name, expected in manifest['files'].items():
        source = REPO / 'zsh/jev' / name
        plain(source)
        data = source.read_bytes()
        if digest(data) != expected:
            raise RuntimeError('Source changed since verification: ' + name)
        files[name] = data
    base = TARGET / 'ai/base.zsh'
    plain(base)
    if not base.is_file():
        raise RuntimeError('Existing ai signpost missing')
    old = base.read_bytes()
    new = (REPO / 'zsh/ai/base.zsh').read_bytes()
    if digest(new) != manifest['signpost_new'] or digest(old) not in {manifest['signpost_old'], manifest['signpost_new']}:
        raise RuntimeError('Signpost differs from reviewed before/after bytes')
    destination = TARGET / 'jev'
    plain(destination)
    if destination.exists():
        if not destination.is_dir() or {p.name for p in destination.iterdir()} != NAMES:
            raise RuntimeError('Existing Jev destination differs; review required')
        for name, data in files.items():
            plain(destination / name)
            if not (destination / name).is_file() or (destination / name).read_bytes() != data:
                raise RuntimeError('Existing deployed Jev file differs: ' + name)
    private_dir(RUNTIME)
    private_dir(RUNTIME / 'projects')
    backup = TARGET / '.jev-install-backup-20261104'
    plain(backup)
    if backup.exists() and not backup.is_dir():
        raise RuntimeError('Backup path is not a directory')
    print(json.dumps({'mode': 'apply' if args.apply else 'dry-run', 'files': len(files),
                      'destination': str(destination), 'signpost': str(base),
                      'runtime': str(RUNTIME), 'engagement_created': False}))
    if not args.apply:
        return
    if digest(old) != manifest['signpost_new']:
        if not backup.exists():
            backup.mkdir(mode=0o700)
            sync_dir(TARGET)
        saved = backup / 'ai-base.zsh'
        plain(saved)
        if saved.exists():
            if saved.read_bytes() != old:
                raise RuntimeError('Backup already contains different bytes')
        else:
            write_file(saved, old, 0o600)
            sync_dir(backup)
    if not destination.exists():
        stage = Path(tempfile.mkdtemp(prefix='.jev-install-stage-', dir=TARGET))
        try:
            for name, data in files.items():
                write_file(stage / name, data, 0o644)
            os.chmod(stage, 0o755)
            sync_dir(stage)
            os.replace(stage, destination)
            sync_dir(TARGET)
        finally:
            if stage.exists():
                shutil.rmtree(stage)
    if base.read_bytes() != new:
        fd, temporary = tempfile.mkstemp(prefix='.jev-signpost-', dir=base.parent)
        temporary = Path(temporary)
        try:
            with os.fdopen(fd, 'wb') as stream:
                os.fchmod(stream.fileno(), stat.S_IMODE(base.stat().st_mode))
                stream.write(new)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, base)
            sync_dir(base.parent)
        finally:
            if temporary.exists():
                temporary.unlink()
    for folder in (RUNTIME, RUNTIME / 'projects'):
        if not folder.exists():
            folder.mkdir(mode=0o700)
            sync_dir(folder.parent)
        private_dir(folder)
    observed = {name: digest((destination / name).read_bytes()) for name in NAMES}
    if observed != manifest['files'] or digest(base.read_bytes()) != manifest['signpost_new']:
        raise RuntimeError('Installed hash verification failed')
    receipt = {'at': datetime.datetime.now().astimezone().isoformat(), 'host': socket.gethostname(),
               'files': observed, 'destination': str(destination), 'signpost_sha256': digest(base.read_bytes()),
               'backup': str(backup / 'ai-base.zsh') if (backup / 'ai-base.zsh').exists() else None,
               'runtime': str(RUNTIME), 'engagement_created': False, 'credential_access': False,
               'inference_calls': 0}
    (BED / 'raw/install-receipt.2026-11-04.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print('Installed Jev only; source/target hashes match; private empty vault ready; no engagement or inference created.')


if __name__ == '__main__':
    main()
