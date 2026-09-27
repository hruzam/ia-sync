#!/usr/bin/env python3
"""muticula B0 fixture guard — Claude lane (cycle 03).

TEST INSTRUMENT ONLY. Never a product dependency (RUNBOOK constraint, majkee 2026-09-25).
PreToolUse hook for write tools. argv[1] selects a fault mode:
  healthy   — deny a write whose target is listed in <fixture>/held.txt, allow others
  sleep     — log, then sleep 5 s (hook timeout is 2 s), then act as healthy
  exit1     — log, then exit 1 with no JSON (intended deny never emitted)
  malformed — log, then print invalid JSON with exit 0
Env: B0_ROOT (fixture root), B0_CASE (case id). Logs one line per call to
$B0_ROOT/logs/<case>.guard.jsonl — the guard's own view, independent of the runtime.
"""
import json
import os
import sys
import time

mode = sys.argv[1] if len(sys.argv) > 1 else "healthy"
root = os.environ["B0_ROOT"]
fx = os.path.join(root, "fx")
case = os.environ.get("B0_CASE", "unknown")

raw = sys.stdin.read()
try:
    ev = json.loads(raw)
except Exception:
    ev = {}

ti = ev.get("tool_input") or {}
target = ti.get("file_path") or ti.get("notebook_path") or ""
if target and not os.path.isabs(target):
    target = os.path.join(ev.get("cwd") or fx, target)
tpath = os.path.realpath(target) if target else ""

held = set()
with open(os.path.join(fx, "held.txt")) as f:
    for line in f:
        line = line.strip()
        if line:
            held.add(os.path.realpath(os.path.join(fx, line)))
is_held = tpath in held

with open(os.path.join(root, "logs", case + ".guard.jsonl"), "a") as f:
    f.write(json.dumps({
        "t": time.time(), "case": case, "mode": mode,
        "tool_name": ev.get("tool_name"), "target": tpath, "held": is_held,
        "intended": "deny" if is_held else "allow",
        "session_id": ev.get("session_id"), "agent_id": ev.get("agent_id"),
        "agent_type": ev.get("agent_type"), "permission_mode": ev.get("permission_mode"),
    }) + "\n")

if mode == "sleep":
    time.sleep(5)
if mode == "exit1":
    sys.exit(1)
if mode == "malformed":
    sys.stdout.write("{not-json deny")
    sys.exit(0)
if is_held:
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "B0 fixture guard: %s is held" % os.path.basename(tpath),
    }}))
sys.exit(0)
