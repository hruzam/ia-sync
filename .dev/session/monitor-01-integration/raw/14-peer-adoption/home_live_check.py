import errno
import fcntl
import json
import os
import pty
import select
import subprocess
import tempfile
import termios
from pathlib import Path

backup = Path('/home/hruzam/.local/state/ia-sync/backups/monitor-01-cycle14/20261112T163216Z')
body = r'''
print -r -- "IDENTITY:$MACHINE_NAME"
print -r -- "PEER:$TAILSCALE_PEER"
print -r -- "ALIAS:$(alias tso)"
print -r -- "REGISTRY:$(temple-project-root nabla-lab)"
timeout() { shift; "$@"; }
tailscale() { print -r -- "ping:$*" >> "$TS_TEST_LOG"; }
ssh() { print -r -- "ssh:$*" >> "$TS_TEST_LOG"; }
eval "$TS_TEST_CASE"
'''
cases = {
    'default': ('tso', ['ping:ping --c 1 hruzam-120922',
                        'ssh:-o ConnectTimeout=8 -o ConnectionAttempts=1 hruzam-120922']),
    'monitor': ('tso monitor', ['ping:ping --c 1 100.80.107.66',
                               'ssh:-o ConnectTimeout=8 -o ConnectionAttempts=1 100.80.107.66']),
    'monitor_bed': ('tso -t monitor', ['ping:ping --c 1 100.80.107.66',
                                     'ssh:-o ConnectTimeout=8 -o ConnectionAttempts=1 -t 100.80.107.66 exec sh /home/hruzam/ia-sync/devices/_shared/termux/bin/agentive-door']),
}
results = []
for name, (command, expected) in cases.items():
    with tempfile.TemporaryDirectory(dir=backup) as directory:
        log = Path(directory) / 'network.log'
        env = os.environ.copy()
        env['TS_TEST_LOG'] = str(log)
        env['TS_TEST_CASE'] = command
        master, slave = pty.openpty()
        try:
            def controlling_terminal():
                os.setsid()
                fcntl.ioctl(slave, termios.TIOCSCTTY, 0)

            proc = subprocess.Popen(['zsh', '-i', '-c', body], env=env,
                                    stdin=slave, stdout=slave, stderr=slave,
                                    preexec_fn=controlling_terminal)
            os.close(slave)
            output = bytearray()
            while proc.poll() is None:
                ready, _, _ = select.select([master], [], [], 12)
                if not ready:
                    proc.kill()
                    raise RuntimeError(f'{name}: shell timed out')
                try:
                    output.extend(os.read(master, 4096))
                except OSError as error:
                    if error.errno == errno.EIO:
                        break
                    raise
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
            code = proc.wait(timeout=5)
        finally:
            os.close(master)
        shell_text = output.decode(errors='replace')
        calls = log.read_text().splitlines() if log.exists() else []
        for marker in ('IDENTITY:home', 'PEER:hruzam-120922',
                       'ALIAS:tso=_ts_session', 'REGISTRY:/home/hruzam/nabla-lab'):
            if marker not in shell_text:
                raise AssertionError(f'{name}: missing {marker}; output={shell_text!r}')
        if code != 0 or calls != expected:
            raise AssertionError(f'{name}: exit={code}, calls={calls}, output={shell_text!r}')
        results.append({'case': name, 'identity': 'home', 'peer': 'hruzam-120922',
                        'alias': 'tso=_ts_session', 'registry': '/home/hruzam/nabla-lab',
                        'exit': code, 'calls': calls})
print(json.dumps(results, indent=2))
