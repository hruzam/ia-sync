#!/usr/bin/env python3
"""Exact G09 receipt-linked process observation; no process enumeration or signalling."""
import json
import os
from pathlib import Path
import time

BED = Path("/home/hruzam/ia-sync/.dev/session/germline-09-source-reader")
RES = BED / "raw/closeout/resources"
OUT = BED / "raw/closeout/sanitation/09.processes-elevated.json"
KNOWN = [
    ("R1-runner", 1319728, "296276499", None),
    ("old-verification-checker", 1923120, "299269158", "python3"),
    ("old-verification-app-server", 1923121, "299269177", "codex"),
]


def identity(pid):
    proc = Path("/proc") / str(pid)
    try:
        raw = (proc / "stat").read_text()
        fields = raw[raw.rfind(")") + 2:].split()
        return {"present": True, "pid": pid, "uid": proc.stat().st_uid,
                "start_ticks": fields[19], "comm": (proc / "comm").read_text().strip(),
                "pid_namespace": os.readlink(proc / "ns/pid")}
    except (FileNotFoundError, PermissionError, OSError, IndexError, ValueError):
        return {"present": False, "pid": pid}


def historical_receipts():
    rows = []
    for name in ("01.inventory.json", "02.read-before-archive.json", "03.archive-R1.json",
                 "05.snapshot-vault.json", "06.close-vault.json"):
        data = json.loads((RES / name).read_text())
        rows.append({"receipt": name, "pid": data.get("pid"),
                     "pid_namespace": data.get("pid_namespace"), "status": data.get("status")})
    report = json.loads((RES / "07.archival-and-process-verification.json").read_text())
    rows.extend([
        {"receipt": "07.archival-and-process-verification.json/checker",
         "pid": report["checker"]["pid"], "pid_namespace": report["checker"]["pid_namespace"],
         "start_ticks": report["checker"]["start_ticks"], "status": report["status"]},
        {"receipt": "07.archival-and-process-verification.json/owned_app_server",
         "pid": report["owned_app_server"]["pid"],
         "pid_namespace": report["owned_app_server"]["pid_namespace"],
         "start_ticks": report["owned_app_server"]["start_ticks"], "status": report["status"]},
    ])
    return rows


def main():
    if OUT.exists():
        raise RuntimeError(f"refusing to overwrite receipt: {OUT}")
    current_ns = os.readlink("/proc/self/ns/pid")
    observations = []
    for role, pid, start, comm in KNOWN:
        observed = identity(pid)
        observed.update({
            "role": role, "expected_start_ticks": start, "expected_comm": comm,
            "identity_matches_historical": observed.get("present") and observed.get("start_ticks") == start and
                (comm is None or observed.get("comm") == comm),
        })
        observations.append(observed)
    result = {
        "schema": "g09-sanitation-cycle07-processes/v1",
        "recorded_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "current_pid_namespace": current_ns,
        "current_uid": os.getuid(),
        "historical_receipt_processes": historical_receipts(),
        "exact_observations": observations,
        "signals_sent": [],
        "outcome": "No currently visible exact PID matched its recorded ownership identity; no leftover leaf was proven and no signal was sent.",
        "residual_limit": "Operator-reported old native root termination is not independently addressable from this root; no /proc/1 namespace gate or broad process scan was used.",
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"receipt": str(OUT), "present_pids": [x["pid"] for x in observations if x["present"]],
                      "signals_sent": result["signals_sent"]}))


if __name__ == "__main__":
    main()
