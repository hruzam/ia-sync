#!/usr/bin/env python3
"""Exec one isolated private Codex TUI case; outer script(1) records the PTY."""

import json
import os
import sys
from pathlib import Path


ROOT = Path("/tmp/muticula-b0-codex-ki5dIN")
FIXTURE = ROOT / "fixture"
LOGS = ROOT / "logs"
CODEX = Path("/home/hruzam/.codex/packages/standalone/releases/0.156.1-x86_64-unknown-linux-musl/bin/codex")
HOOK = ROOT / "hook.py"
MODEL = "gpt-5.6-terra"
GLOBAL_HOOK_IDS = [
    "/home/hruzam/.codex/hooks.json:session_start:0:0",
    "/home/hruzam/.codex/hooks.json:user_prompt_submit:0:0",
    "/home/hruzam/.codex/hooks.json:stop:0:0",
]

case = sys.argv[1]
prompt = (ROOT / f"{case}.prompt.txt").read_text(encoding="utf-8").strip()
event_log = LOGS / f"{case}.hook-events.jsonl"
matcher = "^(apply_patch|Agent)$" if case == "02-child" else "^apply_patch$"
pre_tool = (
    "hooks.PreToolUse=[{matcher=\"" + matcher + "\",hooks=[{type=\"command\","
    "command=\"/usr/bin/python3 " + str(HOOK) + "\",timeout=2}]}]"
)
args = [
    str(CODEX),
    "--no-alt-screen",
    "--no-daemon",
    "--dangerously-bypass-hook-trust",
    "-C", str(FIXTURE),
    "-m", MODEL,
    "--sandbox", "workspace-write",
    "--ask-for-approval", "never",
    "-c", 'model_reasoning_effort="high"',
    "-c", "allow_login_shell=false",
    "-c", 'web_search="disabled"',
    "-c", f'projects={{\"{FIXTURE}\"={{trust_level=\"trusted\"}}}}',
    "-c", pre_tool,
]
if case == "02-child":
    args.extend([
        "-c",
        "hooks.SubagentStart=[{matcher=\"*\",hooks=[{type=\"command\","
        "command=\"/usr/bin/python3 " + str(HOOK) + "\",timeout=2}]}]",
    ])
disabled_global_hooks = ",".join(
    f'\"{hook_id}\"={{enabled=false}}' for hook_id in GLOBAL_HOOK_IDS
)
args.extend(["-c", f"hooks.state={{{disabled_global_hooks}}}"])
args.append(prompt)

env = os.environ.copy()
env.update({
    "MUTICULA_CASE": case,
    "MUTICULA_HOOK_MODE": "healthy",
    "MUTICULA_EVENT_LOG": str(event_log),
})
metadata = {
    "argv": args,
    "case": case,
    "cwd": str(FIXTURE),
    "fixture_event_log": str(event_log),
    "global_hook_ids_disabled_for_invocation": GLOBAL_HOOK_IDS,
    "home_unchanged": env.get("HOME"),
    "codex_home_unchanged": env.get("CODEX_HOME"),
}
(LOGS / f"{case}.invocation.json").write_text(
    json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
os.execvpe(str(CODEX), args, env)
