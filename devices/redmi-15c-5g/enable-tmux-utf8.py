#!/usr/bin/env python3
"""Force UTF-8 for Redmi's registered tmux entry; preview unless --apply.

Run on home as hruzam. Changes only the reviewed Redmi forced command.
"""

import argparse
import datetime
import os
from pathlib import Path
import tempfile


KEY = b"ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDSpTWXD6r8JpwtAbKScRHhMBletMLP0VraRADimRhA1 redmi"
GUARDS = b'no-port-forwarding,no-agent-forwarding,no-X11-forwarding,from="100.105.201.3"'
OLD = b'command="tmux new-session -A -s agentive",' + GUARDS + b" " + KEY
NEW = b'command="tmux -u new-session -A -s agentive",' + GUARDS + b" " + KEY


def transform(before):
    lines = before.splitlines(keepends=True)
    matches = [i for i, line in enumerate(lines) if KEY.split()[1] in line]
    if len(matches) != 1:
        raise ValueError("Expected exactly one registered Redmi key; no changes")
    index = matches[0]
    current = lines[index].rstrip(b"\r\n")
    if current == NEW:
        return before
    if current != OLD:
        raise ValueError("Redmi entry differs from reviewed before-state; no changes")
    lines[index] = NEW + lines[index][len(current):]
    return b"".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    path = Path.home() / ".ssh/authorized_keys"
    if path.is_symlink() or not path.is_file() or path.stat().st_uid != os.getuid():
        raise SystemExit("Expected an owned, regular authorized_keys file")
    before = path.read_bytes()
    after = transform(before)
    if after == before:
        print("Redmi entry already forces UTF-8; unchanged")
        return
    print("Redmi: tmux -> tmux -u; key, restrictions and other entries unchanged")
    if not args.apply:
        print("DRY RUN; use --apply on home to write")
        return
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    backup = path.with_name(f"authorized_keys.before-redmi-utf8-{stamp}")
    fd = os.open(backup, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as stream:
        stream.write(before)
    fd, temporary = tempfile.mkstemp(prefix=".authorized_keys-redmi-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(after)
        if path.read_bytes() != before:
            raise SystemExit("authorized_keys changed during preparation; no replacement")
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    assert path.read_bytes() == after
    print(f"APPLIED; backup: {backup}")


if __name__ == "__main__":
    main()
