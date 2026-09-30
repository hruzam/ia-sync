#!/usr/bin/env python3
"""Promote/rotate the registered Galaxy key; preview unless --apply.

Run on each host as hruzam. Never reads a private key or changes authentication.
Authorized by majkee's 2026-09-29 request for Galaxy/Redmi capability parity.
"""

import argparse
import base64
import datetime
import os
from pathlib import Path
import tempfile


KEY = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIPYmFekrHdN888EhGbUTPHoI2wkHyIHaiL30z/ds9d9Q tab"
GUARDS = 'no-port-forwarding,no-agent-forwarding,no-X11-forwarding,from="100.127.230.71"'
OLD = f'command="tmux attach -rt agentive",{GUARDS} {KEY}'
NEW = f'command="tmux new-session -A -s agentive",{GUARDS} {KEY}'


def promote(original, replacement=None, utf8=False):
    command = "tmux -u new-session -A -s agentive" if utf8 else "tmux new-session -A -s agentive"
    target = f'command="{command}",{GUARDS} {KEY}'
    accepted = {OLD, NEW}
    blobs = {KEY.split()[1]}
    if replacement is not None:
        parts = replacement.split()
        if len(parts) != 3 or parts[0] != "ssh-ed25519" or parts[2] != "galaxy":
            raise ValueError("Expected a single Ed25519 public key with comment galaxy")
        raw = base64.b64decode(parts[1], validate=True)
        if len(raw) != 51 or raw[:19] != b"\x00\x00\x00\x0bssh-ed25519\x00\x00\x00\x20":
            raise ValueError("Invalid Ed25519 public key encoding")
        replacement = " ".join(parts)
        blobs.add(parts[1])
        accepted.add(f'command="tmux new-session -A -s agentive",{GUARDS} {replacement}')
        target = f'command="{command}",{GUARDS} {replacement}'
    lines = original.splitlines(keepends=True)
    matches = [i for i, line in enumerate(lines) if any(blob in line for blob in blobs)]
    if len(matches) != 1:
        raise ValueError("Expected exactly one registered Galaxy key; no changes")
    index = matches[0]
    current = lines[index].rstrip("\r\n")
    if current == target:
        return original
    if current not in accepted:
        raise ValueError("Galaxy entry differs from reviewed before-state; no changes")
    lines[index] = target + lines[index][len(current):]
    return "".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--replacement-key", help="New Galaxy PUBLIC key; never a private key")
    parser.add_argument("--utf8", action="store_true", help="Force UTF-8 output for the Galaxy tmux client")
    args = parser.parse_args()
    path = Path.home() / ".ssh/authorized_keys"
    if path.is_symlink() or path.stat().st_uid != os.getuid():
        raise SystemExit("Expected an owned, regular authorized_keys file")
    before = path.read_text()
    after = promote(before, args.replacement_key, args.utf8)
    if after == before:
        print("Galaxy entry already matches the requested state; unchanged")
        return
    print("Galaxy: reviewed entry -> " + ("UTF-8 " if args.utf8 else "") + "writable tmux")
    print("Source-IP guard, forwarding restrictions and other keys unchanged")
    if not args.apply:
        print("DRY RUN; use --apply on this host to write")
        return
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    backup = path.with_name(f"authorized_keys.before-galaxy-write-{stamp}")
    fd = os.open(backup, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w") as stream:
        stream.write(before)
    fd, temporary = tempfile.mkstemp(prefix=".authorized_keys-galaxy-", dir=path.parent)
    try:
        with os.fdopen(fd, "w") as stream:
            stream.write(after)
        if path.read_text() != before:
            raise SystemExit("authorized_keys changed during preparation; no replacement")
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    assert path.read_text() == after
    print(f"APPLIED; backup: {backup}")


if __name__ == "__main__":
    main()
