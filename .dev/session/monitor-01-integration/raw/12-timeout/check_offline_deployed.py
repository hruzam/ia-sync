#!/usr/bin/env python3
"""Source regressions plus unsuccessful ping/SSH behavior; all peer calls mocked."""

import os
import runpy
from pathlib import Path


BASE = Path(__file__).resolve().parent
suite = runpy.run_path(str(BASE / "check_tso_regression_deployed.py"))
run = suite["run"]
os.environ["TS_TEST_PING_EXIT"] = "1"
os.environ["TS_TEST_SSH_EXIT"] = "255"


def check(name, *, args=(), choice=None, code, calls):
    actual_code, output, actual_calls = run(name, "monitor", args=args, choice=choice)
    assert actual_code == code, (name, actual_code, output)
    assert actual_calls == calls, (name, actual_calls, calls)
    if calls:
        assert "no response (proceeding anyway)" in output, (name, output)
    print(f"PASS {name}: exit={actual_code}; calls={actual_calls}")


prefix = "ssh:-o ConnectTimeout=8 -o ConnectionAttempts=1 "
check(
    "offline plain connection failure", args=("home",), code=255,
    calls=["ping:ping --c 1 100.110.27.60", prefix + "100.110.27.60"],
)
check(
    "offline bed connection failure", args=("-t", "office"), code=255,
    calls=["ping:ping --c 1 100.126.182.111", prefix + "-t 100.126.182.111 exec sh /home/hruzam/ia-sync/devices/_shared/termux/bin/agentive-door"],
)
check("offline chooser cancellation", choice=b"\n", code=1, calls=[])
check("offline chooser invalid choice", choice=b"9\n", code=1, calls=[])
