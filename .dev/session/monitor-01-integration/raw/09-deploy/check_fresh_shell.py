#!/usr/bin/env python3
"""Fresh interactive login-loader checks with mocked tso network calls."""

import errno
import fcntl
import os
import pty
import select
import subprocess
import tempfile
import termios
from pathlib import Path


SCRIPT = r'''
print -r -- "IDENTITY:$MACHINE_NAME"
print -r -- "ALIAS:$(alias tso)"
print -r -- "REGISTRY:$(temple-project-root nabla-lab)"
timeout() { shift; "$@"; }
tailscale() { print -r -- "ping:$*" >> "$TS_TEST_LOG"; }
ssh() { print -r -- "ssh:$*" >> "$TS_TEST_LOG"; }
eval 'tso'
'''


def check(name, choice, expected_code, expected_calls):
    with tempfile.TemporaryDirectory() as directory:
        log = Path(directory) / "network.log"
        env = os.environ.copy()
        env["TS_TEST_LOG"] = str(log)
        master, slave = pty.openpty()
        try:
            def make_controlling_terminal():
                os.setsid()
                fcntl.ioctl(slave, termios.TIOCSCTTY, 0)

            process = subprocess.Popen(
                ["zsh", "-i", "-c", SCRIPT],
                env=env, stdin=slave, stdout=slave, stderr=slave,
                preexec_fn=make_controlling_terminal,
            )
            os.close(slave)
            output = bytearray()
            sent = False
            while process.poll() is None:
                ready, _, _ = select.select([master], [], [], 10)
                assert ready, (name, "timed out", output.decode(errors="replace"))
                try:
                    chunk = os.read(master, 4096)
                except OSError as error:
                    if error.errno == errno.EIO:
                        break
                    raise
                output.extend(chunk)
                if b"Choice (empty to cancel):" in output and not sent:
                    os.write(master, choice)
                    sent = True
            while True:
                try:
                    chunk = os.read(master, 4096)
                except OSError as error:
                    if error.errno == errno.EIO:
                        break
                    raise
                if not chunk:
                    break
                output.extend(chunk)
            code = process.wait(timeout=10)
        finally:
            os.close(master)
        text = output.decode(errors="replace")
        calls = log.read_text().splitlines() if log.exists() else []
        assert "IDENTITY:monitor" in text, (name, text)
        assert "ALIAS:tso=_ts_session" in text, (name, text)
        assert "REGISTRY:/home/hruzam/nabla-lab" in text, (name, text)
        assert "Choice (empty to cancel):" in text, (name, text)
        assert code == expected_code and calls == expected_calls, (name, code, calls, text)
        print(f"PASS {name}: identity=monitor; alias=tso=_ts_session; registry=/home/hruzam/nabla-lab; exit={code}; calls={calls}")


check("fresh shell chooser success", b"1\n", 0, ["ping:ping --c 1 100.110.27.60", "ssh:100.110.27.60"])
check("fresh shell chooser cancel", b"\n", 1, [])
