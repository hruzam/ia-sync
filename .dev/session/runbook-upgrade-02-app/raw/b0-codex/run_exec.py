#!/usr/bin/env python3
"""Run one fresh noninteractive Codex fixture case and preserve JSONL evidence."""

import json
import hashlib
import os
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path("/tmp/muticula-b0-codex-ki5dIN")
FIXTURE = ROOT / "fixture"
LOGS = ROOT / "logs"
CODEX = Path("/home/hruzam/.codex/packages/standalone/releases/0.156.1-x86_64-unknown-linux-musl/bin/codex")
HOOK = ROOT / "hook.py"
MODEL = "gpt-5.6-terra"


def fixture_hashes():
    return {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(FIXTURE.glob("*.txt"))
    }

case, mode = sys.argv[1:3]
prompt = (ROOT / f"{case}.prompt.txt").read_text(encoding="utf-8").strip()
event_log = LOGS / f"{case}.hook-events.jsonl"
hook_command = str(ROOT / "does-not-exist.py") if mode == "missing" else f"/usr/bin/python3 {HOOK}"
pre_tool = (
    "hooks.PreToolUse=[{matcher=\"^apply_patch$\",hooks=[{type=\"command\","
    f"command=\"{hook_command}\",timeout=2}}]}}]"
)
args = [
    str(CODEX), "exec",
    "--json",
    "--ephemeral",
    "--ignore-user-config",
    "--ignore-rules",
    "--dangerously-bypass-hook-trust",
    "-C", str(FIXTURE),
    "-m", MODEL,
    "--sandbox", "workspace-write",
    "-c", 'approval_policy="never"',
    "-c", 'model_reasoning_effort="high"',
    "-c", "allow_login_shell=false",
    "-c", 'web_search="disabled"',
    "-c", pre_tool,
]
if mode == "disabled":
    args.extend(["--disable", "hooks"])
args.append(prompt)
env = os.environ.copy()
env.update({
    "MUTICULA_CASE": case,
    "MUTICULA_HOOK_MODE": mode,
    "MUTICULA_EVENT_LOG": str(event_log),
})
metadata = {
    "argv": args,
    "case": case,
    "cwd": str(FIXTURE),
    "fixture_event_log": str(event_log),
    "home_unchanged": env.get("HOME"),
    "codex_home_unchanged": env.get("CODEX_HOME"),
    "mode": mode,
    "sentinel_hashes_before": fixture_hashes(),
    "started_at_unix_ns": time.time_ns(),
}
(LOGS / f"{case}.invocation.json").write_text(
    json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
completed = subprocess.run(args, cwd=FIXTURE, env=env, text=True, capture_output=True)
(LOGS / f"{case}.stdout.jsonl").write_text(completed.stdout, encoding="utf-8")
(LOGS / f"{case}.stderr.txt").write_text(completed.stderr, encoding="utf-8")
metadata.update({
    "completed_at_unix_ns": time.time_ns(),
    "returncode": completed.returncode,
    "sentinel_hashes_after": fixture_hashes(),
})
(LOGS / f"{case}.invocation.json").write_text(
    json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
print(json.dumps({
    "case": case,
    "returncode": completed.returncode,
    "stdout_bytes": len(completed.stdout.encode()),
    "stderr_bytes": len(completed.stderr.encode()),
}))
raise SystemExit(completed.returncode)
