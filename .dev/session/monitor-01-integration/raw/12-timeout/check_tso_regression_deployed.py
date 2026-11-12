#!/usr/bin/env python3
"""Run cycle 07 checks plus isolated invalid-map regressions; all network calls mocked."""

import json
import runpy
import tempfile
from pathlib import Path


BED = Path("/home/hruzam/ia-sync/.dev/session/monitor-01-integration/raw")
SOURCE = Path("/home/hruzam/.config/zsh/system/tailscale.zsh")
suite = runpy.run_path(str(BED / "12-timeout/check_tso_deployed.py"))
run = suite["run"]
globals_for_run = run.__globals__
original_body = globals_for_run["BODY"]


def case(name, map_value, *, args=(), choice=None, success=False, expected_calls=(), message=None):
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        fixture = root / "machines.json"
        if map_value is not None:
            fixture.write_text(map_value if isinstance(map_value, str) else json.dumps(map_value))
        source_copy = root / "tailscale.zsh"
        source_copy.write_text(SOURCE.read_text().replace('"$HOME/ia-sync/machines.json"', f'"{fixture}"'))
        globals_for_run["BODY"] = original_body.replace(str(SOURCE), str(source_copy))
        try:
            code, output, calls = run(name, "monitor", args=args, choice=choice)
        finally:
            globals_for_run["BODY"] = original_body
    assert (code == 0) == success, (name, code, output, calls)
    assert calls == list(expected_calls), (name, calls, output)
    assert "Traceback" not in output, (name, output)
    if message:
        assert message in output, (name, output)
    if name == "empty eligible chooser":
        assert "Choice (empty to cancel):" not in output, (name, output)
    print(f"PASS {name}: exit={code}; calls={calls}")


for label, record in (
    ("null", {"logical": "home", "tailscale_ip": None}),
    ("missing", {"logical": "home"}),
    ("empty", {"logical": "home", "tailscale_ip": ""}),
    ("non-string", {"logical": "home", "tailscale_ip": 168296123}),
):
    case(f"registered {label} address", {"machines": {"pending": record}}, args=("home",), message="no usable address")

case("new registered alias null", {"machines": {"pending": {"logical": "lab", "tailscale_ip": None}}}, args=("lab",), message="no usable address")
case("missing map logical", None, args=("home",), message="machine map unavailable")
case("missing map raw address", None, args=("203.0.113.7",), success=True, expected_calls=("ping:ping --c 1 203.0.113.7", "ssh:-o ConnectTimeout=8 -o ConnectionAttempts=1 203.0.113.7"))
case("missing map raw hostname", None, args=("hruzam",), success=True, expected_calls=("ping:ping --c 1 hruzam", "ssh:-o ConnectTimeout=8 -o ConnectionAttempts=1 hruzam"))
case("malformed map logical", "{", args=("home",), message="machine map unavailable")
case("malformed map raw address", "{", args=("203.0.113.7",), success=True, expected_calls=("ping:ping --c 1 203.0.113.7", "ssh:-o ConnectTimeout=8 -o ConnectionAttempts=1 203.0.113.7"))
case("missing map chooser", None, choice=b"1\n", message="machine map unavailable")
case("malformed map chooser", "{", choice=b"1\n", message="machine map unavailable")
case("empty eligible chooser", {"machines": {"self": {"logical": "monitor", "tailscale_ip": "100.80.107.66"}}}, choice=b"1\n", message="no registered peers available")
