#!/usr/bin/env python3
"""Run one declared tunnel command with a literal argv and preserve a receipt."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

home = Path(__file__).resolve().parent
name, verb, state_name, prompt_name = sys.argv[1:5]
state = home / state_name
prompt = home / prompt_name if prompt_name != "-" else None
stdout = home / f"{name}.{verb}.stdout.txt"
stderr = home / f"{name}.{verb}.stderr.txt"
started = time.time()
argv = ["/home/hruzam/ia-sync/zsh/ai/tunnel-codex.zsh", verb,
       "--state", str(state)]
if verb == "open":
    argv += ["--enable", "--sandbox", "read-only", "--cwd",
            "/home/hruzam/ia-sync/.dev/session/germline-07-make-program", "--preamble", "none"]
else:
    argv.append(prompt.read_text())
env = dict(os.environ, TUNNEL_CODEX_USAGE="full")
run = subprocess.run(argv, cwd="/home/hruzam/ia-sync/.dev/session/germline-07-make-program",
                     env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
ended = time.time()
stdout.write_text(run.stdout)
stderr.write_text(run.stderr)
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
record = {
    "argv": argv,
    "started_unix": started,
    "ended_unix": ended,
    "elapsed_seconds": round(ended - started, 3),
    "exit": run.returncode,
    "stdout": {"path": str(stdout), "sha256": digest(stdout)},
    "stderr": {"path": str(stderr), "sha256": digest(stderr)},
    "prompt": None if prompt is None else {"path": str(prompt), "sha256": digest(prompt)},
    "state": None,
}
if state.exists():
    data = json.loads(state.read_text())
    record["state"] = {k: data.get(k) for k in ("enabled", "threadId", "lastTurnId", "model", "sandbox", "cwd", "runtime", "created")}
(home / f"{name}.{verb}.receipt.json").write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
sys.exit(run.returncode)
