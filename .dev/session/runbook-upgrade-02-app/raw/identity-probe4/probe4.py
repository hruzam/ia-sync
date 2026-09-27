#!/usr/bin/env python3
"""Probe this tool process's terminal access; never read terminal input or secrets."""
import datetime
import json
import os
from pathlib import Path
import subprocess
import sys

label, output_path = sys.argv[1:]
result = {
    "probe": "muticula-identity-probe-4",
    "mode": label,
    "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "pid": os.getpid(),
    "ppid": os.getppid(),
    "ps_tty": subprocess.check_output(
        ["ps", "-o", "tty=", "-p", str(os.getpid())], text=True
    ).strip(),
    "isatty": {str(fd): os.isatty(fd) for fd in (0, 1, 2)},
}
try:
    fd = os.open("/dev/tty", os.O_RDONLY | os.O_NOCTTY | os.O_NONBLOCK)
except OSError as error:
    result["dev_tty"] = {"opened": False, "errno": error.errno, "error": error.strerror}
else:
    result["dev_tty"] = {"opened": True, "isatty": os.isatty(fd)}
    os.close(fd)
result["terminal_input_read"] = False
result["secrets_accessed"] = False
rendered = json.dumps(result, indent=2) + "\n"
with Path(output_path).open("x") as stream:
    stream.write(rendered)
print(rendered, end="")
