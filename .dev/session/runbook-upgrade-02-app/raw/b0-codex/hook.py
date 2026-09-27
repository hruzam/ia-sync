#!/usr/bin/env python3
"""Fixture-only Codex hook used by cycle-04 B0 qualification."""

import json
import os
import re
import sys
import time
from pathlib import Path


case = os.environ.get("MUTICULA_CASE", "unknown")
mode = os.environ.get("MUTICULA_HOOK_MODE", "healthy")
log_path = Path(os.environ["MUTICULA_EVENT_LOG"])
raw = sys.stdin.read()
try:
    payload = json.loads(raw)
except json.JSONDecodeError:
    payload = {"_input_parse_error": True, "raw": raw}

serialized_input = json.dumps(payload.get("tool_input") or {}, sort_keys=True)
effective_mode = mode
if mode == "dispatch":
    if "held-timeout.txt" in serialized_input:
        effective_mode = "timeout"
    elif "held-exit1.txt" in serialized_input:
        effective_mode = "exit1"
    elif "held-malformed.txt" in serialized_input:
        effective_mode = "malformed"
record = {
    "case": case,
    "effective_mode": effective_mode,
    "hook_mode": mode,
    "observed_at_unix_ns": time.time_ns(),
    "pid": os.getpid(),
    "payload": payload,
}
log_path.parent.mkdir(parents=True, exist_ok=True)
with log_path.open("a", encoding="utf-8") as stream:
    stream.write(json.dumps(record, sort_keys=True) + "\n")

if effective_mode == "timeout":
    time.sleep(5)
    raise SystemExit(0)
if effective_mode == "exit1":
    raise SystemExit(1)
if effective_mode == "malformed":
    print("{this-is-not-json")
    raise SystemExit(0)

if mode == "healthy" and payload.get("hook_event_name") == "PreToolUse":
    tool_name = payload.get("tool_name")
    tool_input = payload.get("tool_input") or {}
    serialized = json.dumps(tool_input, sort_keys=True)
    held_path = re.search(r"(?<![A-Za-z0-9_.-])held\.txt(?![A-Za-z0-9_.-])", serialized)
    if tool_name == "apply_patch" and held_path:
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": "cycle04 fixture hold: held.txt",
            }
        }))
