#!/usr/bin/env python3
"""muticula B0 event logger — Claude lane. TEST INSTRUMENT ONLY; never decides anything.
argv[1] = tag (layer-flag | layer-project | layer-local | pre | post).
Appends the runtime's hook input verbatim to $B0_ROOT/logs/<case>.events.jsonl and exits 0.
SessionStart layer markers show which settings layers actually loaded in each run."""
import json
import os
import sys
import time

tag = sys.argv[1] if len(sys.argv) > 1 else "untagged"
root = os.environ["B0_ROOT"]
case = os.environ.get("B0_CASE", "unknown")
raw = sys.stdin.read()
try:
    ev = json.loads(raw)
except Exception:
    ev = {"unparsed": raw[:2000]}
with open(os.path.join(root, "logs", case + ".events.jsonl"), "a") as f:
    f.write(json.dumps({"t": time.time(), "tag": tag, "ev": ev}) + "\n")
sys.exit(0)
