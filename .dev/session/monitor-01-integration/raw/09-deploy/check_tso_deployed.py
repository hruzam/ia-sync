#!/usr/bin/env python3
"""Isolated tso behavior checks: shell functions replace every network command."""

import errno
import fcntl
import os
import pty
import select
import subprocess
import tempfile
import termios
from pathlib import Path


SOURCE = "/home/hruzam/.config/zsh/system/tailscale.zsh"
BODY = rf'''
source {SOURCE}
timeout() {{ shift; "$@"; }}
tailscale() {{ print -r -- "ping:$*" >> "$TS_TEST_LOG"; }}
ssh() {{ print -r -- "ssh:$*" >> "$TS_TEST_LOG"; }}
_ts_session "$@"
'''


def run(name, machine, args=(), choice=None, peer=None):
    with tempfile.TemporaryDirectory() as directory:
        log = Path(directory) / "network.log"
        env = os.environ.copy()
        env.update(MACHINE_NAME=machine, TS_TEST_LOG=str(log))
        env.pop("TAILSCALE_PEER", None)
        if peer is not None:
            env["TAILSCALE_PEER"] = peer
        command = ["zsh", "-f", "-c", BODY, "tso-test", *args]
        if choice is None:
            result = subprocess.run(command, env=env, capture_output=True, text=True, timeout=5)
            output = result.stdout + result.stderr
            code = result.returncode
        else:
            master, slave = pty.openpty()
            try:
                def controlling_terminal():
                    os.setsid()
                    fcntl.ioctl(slave, termios.TIOCSCTTY, 0)

                process = subprocess.Popen(command, env=env, stdin=slave, stdout=slave, stderr=slave, preexec_fn=controlling_terminal)
                os.close(slave)
                output = bytearray()
                sent = False
                while process.poll() is None:
                    ready, _, _ = select.select([master], [], [], 5)
                    assert ready, f"{name}: prompt timed out"
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
                code = process.wait(timeout=5)
                output = output.decode(errors="replace")
            finally:
                os.close(master)
        calls = log.read_text().splitlines() if log.exists() else []
        return code, output, calls


def check(name, machine, args=(), choice=None, peer=None, expected=(), success=True):
    code, output, calls = run(name, machine, args, choice, peer)
    assert (code == 0) == success, (name, code, output, calls)
    assert calls == list(expected), (name, calls, expected, output)
    print(f"PASS {name}: exit={code}; calls={calls}")


check("monitor chooses home", "monitor", choice=b"1\n", expected=("ping:ping --c 1 100.110.27.60", "ssh:100.110.27.60"))
check("monitor chooses office bed", "monitor", args=("-t",), choice=b"2\n", expected=("ping:ping --c 1 100.126.182.111", "ssh:-t 100.126.182.111 exec sh /home/hruzam/ia-sync/devices/_shared/termux/bin/agentive-door"))
check("monitor cancellation", "monitor", choice=b"\n", success=False)
check("monitor invalid choice", "monitor", choice=b"9\n", success=False)
check("monitor EOF", "monitor", choice=b"\x04", success=False)
check("noninteractive no target", "monitor", success=False)
check("explicit logical noninteractive", "monitor", args=("office",), expected=("ping:ping --c 1 100.126.182.111", "ssh:100.126.182.111"))
check("explicit logical bed", "monitor", args=("-t", "home"), expected=("ping:ping --c 1 100.110.27.60", "ssh:-t 100.110.27.60 exec sh /home/hruzam/ia-sync/devices/_shared/termux/bin/agentive-door"))
check("explicit address noninteractive", "monitor", args=("203.0.113.7",), expected=("ping:ping --c 1 203.0.113.7", "ssh:203.0.113.7"))
check("home existing default", "home", peer="hruzam-120922", expected=("ping:ping --c 1 hruzam-120922", "ssh:hruzam-120922"))
check("office existing default bed", "office", args=("--bed",), peer="hruzam", expected=("ping:ping --c 1 hruzam", "ssh:-t hruzam exec sh /home/hruzam/ia-sync/devices/_shared/termux/bin/agentive-door"))
