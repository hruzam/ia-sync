#!/usr/bin/env python3
"""One bounded controller wake for vistMini; activate only through an external timer."""
from __future__ import annotations

import argparse
import fcntl
import json
import os
import re
import subprocess
import sys
import time
import uuid
from pathlib import Path

THREAD = re.compile(r"^[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}$")
UNIT = re.compile(r"^vist-mini-[A-Za-z0-9_-]+\.timer$")


def load(path: Path) -> dict:
    try:
        value = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid lease: {exc}") from exc
    required = {
        "active", "controller_thread", "unit", "expires_epoch", "max_wakes", "wakes",
        "pending_id", "pending_since", "report_bed", "codex_binary",
    }
    if not isinstance(value, dict) or required - value.keys():
        raise ValueError("invalid lease: required fields missing")
    if not isinstance(value["active"], bool) or not THREAD.fullmatch(value["controller_thread"]):
        raise ValueError("invalid lease: active or controller_thread")
    if not isinstance(value["unit"], str) or not UNIT.fullmatch(value["unit"]):
        raise ValueError("invalid lease: unit")
    if not all(isinstance(value[k], int) and value[k] >= 0 for k in ("expires_epoch", "max_wakes", "wakes")):
        raise ValueError("invalid lease: numeric bounds")
    if value["pending_id"] is not None and not isinstance(value["pending_id"], str):
        raise ValueError("invalid lease: pending_id")
    if value["pending_since"] is not None and not isinstance(value["pending_since"], (int, float)):
        raise ValueError("invalid lease: pending_since")
    bed = Path(value["report_bed"])
    binary = Path(value["codex_binary"])
    if not bed.is_absolute() or not bed.is_dir() or not binary.is_absolute() or not os.access(binary, os.X_OK):
        raise ValueError("invalid lease: report_bed or codex_binary")
    return value


def save(path: Path, lease: dict) -> None:
    temp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temp.write_text(json.dumps(lease, sort_keys=True, indent=2) + "\n")
    os.chmod(temp, 0o600)
    os.replace(temp, path)


def log(path: Path, event: str, detail: str = "") -> None:
    with path.with_suffix(path.suffix + ".log").open("a", encoding="utf-8") as stream:
        stream.write(f"{int(time.time())} event={event} {detail}\n")


def stop_timer(lease: dict, systemctl: str) -> None:
    subprocess.run([systemctl, "--user", "--no-block", "stop", lease["unit"]],
                   stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                   timeout=10, check=False)


def deactivate(path: Path, lease: dict, systemctl: str, reason: str) -> int:
    lease["active"] = False
    lease["last_result"] = reason
    lease["last_at"] = int(time.time())
    save(path, lease)
    log(path, "stopped", f"reason={reason}")
    stop_timer(lease, systemctl)
    return 0


def run(path: Path, codex: str | None, systemctl: str, now: float) -> int:
    lock_path = path.with_suffix(path.suffix + ".lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        lease = load(path)
        codex = codex or lease["codex_binary"]
        if not lease["active"]:
            return deactivate(path, lease, systemctl, "inactive")
        if now >= lease["expires_epoch"]:
            return deactivate(path, lease, systemctl, "expired")
        if lease["wakes"] >= lease["max_wakes"]:
            return deactivate(path, lease, systemctl, "wake_budget_exhausted")
        if lease["pending_id"]:
            lease["last_result"] = "pending"
            lease["last_at"] = int(now)
            save(path, lease)
            log(path, "skipped", f"reason=pending id={lease['pending_id']}")
            return 0

        message_id = f"hb-{uuid.uuid4().hex[:16]}"
        lease["pending_id"] = message_id
        lease["pending_since"] = int(now)
        lease["wakes"] += 1
        lease["last_result"] = "queueing"
        lease["last_at"] = int(now)
        save(path, lease)
        message = (
            f"[vist heartbeat {message_id}] Read {lease['report_bed']}/STATUS.md and {path}; "
            "reconcile assigned RETURNs, acknowledge pending_id in lease, continue only useful in-scope work. "
            "No peer resend inferred."
        )
        try:
            result = subprocess.run([codex, "queue", "--thread", lease["controller_thread"], "--message", message],
                                    stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                    timeout=20, check=False)
        except subprocess.TimeoutExpired:
            return deactivate(path, lease, systemctl, "queue_timeout")
        if result.returncode:
            return deactivate(path, lease, systemctl, f"queue_exit_{result.returncode}")
        lease["last_result"] = "queued"
        lease["last_at"] = int(time.time())
        save(path, lease)
        log(path, "queued", f"id={message_id}")
        return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lease", required=True, type=Path)
    parser.add_argument("--codex", default=None, help=argparse.SUPPRESS)
    parser.add_argument("--systemctl", default="systemctl", help=argparse.SUPPRESS)
    parser.add_argument("--now", type=float, default=None, help=argparse.SUPPRESS)
    args = parser.parse_args()
    try:
        return run(args.lease, args.codex, args.systemctl, time.time() if args.now is None else args.now)
    except ValueError as exc:
        print(f"vist-heartbeat: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
