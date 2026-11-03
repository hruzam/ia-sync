#!/usr/bin/env python3
"""Zero-turn explicit-ID resume/read reconciliation for experiment_1 cycle 02."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path("/home/hruzam/ia-sync/.dev/session/germline-07-make-program")
CARETAKER = ROOT / "raw/experiment_1/caretaker"
DIRECT = ROOT / "raw/experiment_1/direct"
OUT = CARETAKER / "followup"
SHIM = "/home/hruzam/ia-sync/zsh/ai/tunnel-codex.zsh"

PEERS = {
    "peer-a": ("01a1694a-7bdd-7d70-913d-d3dcef66c8ac", "01a16951-2359-7a00-93f2-429f3a70fe15", "experiment_1.peer-a.direct"),
    "peer-b": ("01a1694b-0c61-76f0-897c-fc3c66f665c0", "01a16951-2359-7d72-9e70-b9262e9df2f8", "experiment_1.peer-b.direct"),
}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def selected_state(path):
    state = json.loads(path.read_text())
    return {key: state.get(key) for key in ("threadId", "lastTurnId", "model", "sandbox", "runtime")}

def call(peer, verb, state_path):
    argv = [SHIM, verb, "--state", str(state_path)]
    started = time.time()
    run = subprocess.run(argv, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ended = time.time()
    (OUT / f"{peer}.{verb}.stderr.txt").write_bytes(run.stderr)
    return run, {
        "argv": argv,
        "exit": run.returncode,
        "started_unix": started,
        "ended_unix": ended,
        "elapsed_seconds": round(ended - started, 3),
        "stdout_sha256": sha(run.stdout),
        "stdout_bytes": len(run.stdout),
        "stderr_path": str(OUT / f"{peer}.{verb}.stderr.txt"),
        "stderr_sha256": sha(run.stderr),
    }

def direct_text(peer):
    text = (DIRECT / f"{peer}.stdout.txt").read_text()
    return text.rsplit("\n[usage: ", 1)[0]

def reconcile(peer, expected_thread, expected_turn, marker):
    state_path = CARETAKER / f"tunnel.{peer}.state.json"
    before = selected_state(state_path)
    resume, resume_record = call(peer, "resume", state_path)
    after_resume = selected_state(state_path)
    read, read_record = call(peer, "read", state_path)
    after_read = selected_state(state_path)
    summary = {
        "peer": peer,
        "expected": {"threadId": expected_thread, "latestTurnId": expected_turn, "marker": marker},
        "state_before": before,
        "resume": resume_record,
        "state_after_resume": after_resume,
        "read": read_record,
        "state_after_read": after_read,
    }
    if read.returncode == 0:
        raw = json.loads(read.stdout)
        thread = raw.get("thread", {})
        turns = thread.get("turns", [])
        expected = next((turn for turn in turns if turn.get("id") == expected_turn), None)
        items = (expected or {}).get("items", [])
        replies = [item.get("text", "") for item in items if item.get("type") == "agentMessage"]
        reply = replies[-1] if replies else None
        expected_text = direct_text(peer)
        ids = [turn.get("id") for turn in turns]
        index = ids.index(expected_turn) if expected_turn in ids else None
        summary["read_selected"] = {
            "raw_response_sha256": sha(read.stdout),
            "threadId": thread.get("id"),
            "threadStatus": thread.get("status"),
            "turnCount": len(turns),
            "turnIds_sha256": sha(json.dumps(ids, separators=(",", ":")).encode()),
            "latestTurnId": ids[-1] if ids else None,
            "expectedTurnIndex": index,
            "turnsAfterExpected": len(ids) - index - 1 if index is not None else None,
            "turnStatus": None if expected is None else expected.get("status"),
            "agentReply": reply,
            "agentReply_sha256": None if reply is None else sha(reply.encode()),
            "markerPresent": bool(reply and reply.startswith(marker)),
            "storedDirectReply_sha256": sha(expected_text.encode()),
            "matchesStoredDirectReply": reply == expected_text,
        }
    (OUT / f"{peer}.summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    return summary

results = [reconcile(peer, *values) for peer, values in PEERS.items()]
ok = all(
    item["resume"]["exit"] == 0 and item["read"]["exit"] == 0
    and item.get("read_selected", {}).get("threadId") == item["expected"]["threadId"]
    and item.get("read_selected", {}).get("latestTurnId") == item["expected"]["latestTurnId"]
    and item.get("read_selected", {}).get("turnsAfterExpected") == 0
    and item.get("read_selected", {}).get("markerPresent")
    and item.get("read_selected", {}).get("matchesStoredDirectReply")
    and item["state_before"]["threadId"] == item["state_after_read"]["threadId"]
    and item["state_before"]["lastTurnId"] == item["state_after_read"]["lastTurnId"]
    for item in results
)
sys.exit(0 if ok else 1)
