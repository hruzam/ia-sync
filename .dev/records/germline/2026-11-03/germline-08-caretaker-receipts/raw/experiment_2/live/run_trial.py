#!/usr/bin/env python3
"""G08 cycle-02 receipt-first dispatch; exactly two fresh asks at most."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

LIVE = Path(__file__).resolve().parent
ROOT = LIVE.parent
BED = ROOT.parents[1]
RUNNER = ROOT / "receipt_runner.py"
CONTRACT = ROOT / "contract.json"
INSPECTION = LIVE / "inspection.json"
PEERS = ("peer-a", "peer-b")


def atomic(value):
    tmp = INSPECTION.with_name(INSPECTION.name + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    tmp.replace(INSPECTION)


def hash_contract():
    contract = json.loads(CONTRACT.read_text())
    mismatches = []
    for item in contract["files"]:
        actual = hashlib.sha256(Path(item["path"]).read_bytes()).hexdigest()
        if actual != item["sha256"]:
            mismatches.append(item["path"])
    return not mismatches, mismatches


def selected_state(peer):
    path = LIVE / f"tunnel.{peer}.state.json"
    if not path.exists():
        return None
    state = json.loads(path.read_text())
    runtime = state.get("runtime") or {}
    return {
        "threadId": state.get("threadId"), "lastTurnId": state.get("lastTurnId"),
        "model": state.get("model"), "sandbox": state.get("sandbox"),
        "requestedEffort": (state.get("turnOverrides") or {}).get("effort"),
        "runtime": {key: runtime.get(key) for key in ("model", "reasoningEffort", "sandbox", "cwd")},
    }


def invoke(peer, verb, discard_stdout=False):
    argv = [sys.executable, str(RUNNER), "run", peer, verb]
    started = time.time()
    result = subprocess.run(argv, cwd=BED, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ended = time.time()
    return {
        "argv": argv, "exit": result.returncode, "elapsed_seconds": round(ended - started, 3),
        "caller_stdout": "deliberately-discarded" if discard_stdout else "not-used; inspect is authoritative",
        "stderr_sha256": hashlib.sha256(result.stderr).hexdigest(),
    }


def inspect(peer, verb):
    argv = [sys.executable, str(RUNNER), "inspect", peer, verb]
    result = subprocess.run(argv, cwd=BED, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        value = json.loads(result.stdout)
    except json.JSONDecodeError:
        value = {"classification": "unknown", "reason": "inspect-output-malformed"}
    return {"argv": argv, "exit": result.returncode, "result": value,
            "stderr_sha256": hashlib.sha256(result.stderr).hexdigest()}


def operation(peer, verb):
    return LIVE / f"{peer}.{verb}.operation.json"


def receipt_summary(peer, verb):
    record = json.loads(operation(peer, verb).read_text())
    outputs = record.get("outputs") or {}
    return {
        "exit": record.get("exit"), "elapsed_seconds": record.get("elapsed_seconds"),
        "status": record.get("status"), "codex_version": record.get("codex_version"),
        "stdout": outputs.get("stdout"), "stderr": outputs.get("stderr"),
        "state_after": selected_state(peer),
    }


def stop(trial, reason):
    trial["stopped"] = reason
    atomic(trial)
    raise SystemExit(reason)


def is_completed(check):
    return check["exit"] == 0 and check["result"].get("classification") == "completed-and-validated"


def main():
    trial = {"contract_verified": None, "peers": {}, "asks_dispatched": [], "stopped": None}
    valid, mismatches = hash_contract()
    trial["contract_verified"] = {"valid": valid, "mismatches": mismatches}
    atomic(trial)
    if not valid:
        stop(trial, "contract-drift")
    for peer in PEERS:
        record = trial["peers"].setdefault(peer, {})
        state_path = LIVE / f"tunnel.{peer}.state.json"
        if any(operation(peer, verb).exists() for verb in ("open", "ask", "resume")) or state_path.exists():
            stop(trial, f"existing-operation-or-vault:{peer}")
        record["open_call"] = invoke(peer, "open")
        record["open_inspect"] = inspect(peer, "open")
        record["open_receipt"] = receipt_summary(peer, "open") if operation(peer, "open").exists() else None
        atomic(trial)
        state = selected_state(peer)
        open_ok = is_completed(record["open_inspect"]) and state and state["threadId"] is None and state["lastTurnId"] is None and state["model"] == "gpt-6.1-sol" and state["sandbox"] == "read-only" and state["requestedEffort"] == "low"
        if not open_ok:
            stop(trial, f"open-not-verified:{peer}")
        trial["asks_dispatched"].append({"peer": peer, "status": "about-to-invoke"})
        atomic(trial)
        record["ask_call"] = invoke(peer, "ask", discard_stdout=(peer == "peer-a"))
        trial["asks_dispatched"][-1]["status"] = "returned-to-caller"
        record["ask_inspect"] = inspect(peer, "ask")
        record["ask_receipt"] = receipt_summary(peer, "ask") if operation(peer, "ask").exists() else None
        atomic(trial)
        if not is_completed(record["ask_inspect"]):
            stop(trial, f"ask-not-validated:{peer}")
        record["resume_call"] = invoke(peer, "resume")
        record["resume_inspect"] = inspect(peer, "resume")
        record["resume_receipt"] = receipt_summary(peer, "resume") if operation(peer, "resume").exists() else None
        atomic(trial)
        runtime = (selected_state(peer) or {}).get("runtime") or {}
        runtime_ok = is_completed(record["resume_inspect"]) and runtime.get("model") == "gpt-6.1-sol" and runtime.get("reasoningEffort") == "low" and runtime.get("sandbox") == {"type": "readOnly", "networkAccess": False}
        if not runtime_ok:
            stop(trial, f"runtime-not-verified:{peer}")
    trial["completed"] = True
    atomic(trial)


if __name__ == "__main__":
    main()
