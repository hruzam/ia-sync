#!/usr/bin/env bash
# muticula B0 — Claude lane fixture generator (cycle 03). TEST INSTRUMENT ONLY.
# Usage: setup-fixture.sh <ROOT>   (ROOT = a fresh /tmp/muticula-b0-claude-XXXXXX)
# Creates: ROOT/fx (git fixture: held.md, unheld.md, held.txt, project+local marker layers),
#          ROOT/tools (guard.py, logger.py — copied from this evidence folder),
#          ROOT/settings/<case>.json (flag-layer settings per case). Writes nothing else.
set -euo pipefail
ROOT="${1:?ROOT required}"
EV="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
mkdir -p "$ROOT"/{fx/.claude,tools,settings,logs}

install -m 0755 "$EV/guard.py"  "$ROOT/tools/guard.py"
install -m 0755 "$EV/logger.py" "$ROOT/tools/logger.py"

cd "$ROOT/fx"
git init -q
git config user.email b0@fixture.invalid
git config user.name b0-fixture
printf 'status: original\n' > held.md
printf 'status: original\n' > unheld.md
printf 'held.md\n' > held.txt
# Layer markers: each settings layer only logs that it loaded (SessionStart).
cat > .claude/settings.json <<JSON
{"hooks":{"SessionStart":[{"hooks":[{"type":"command","command":"$ROOT/tools/logger.py layer-project"}]}]}}
JSON
cat > .claude/settings.local.json <<JSON
{"hooks":{"SessionStart":[{"hooks":[{"type":"command","command":"$ROOT/tools/logger.py layer-local"}]}]}}
JSON
git add -A && git commit -q -m "B0 fixture baseline"

# Flag-layer settings, one per case. Only the variable under test differs.
python3 - "$ROOT" <<'PY'
import json, sys
root = sys.argv[1]
T = root + "/tools/"
def settings(guard_cmd, disable=False):
    s = {
        "permissions": {"allow": ["Read", "Edit", "Write", "Agent", "Task", "Bash(echo:*)"]},
        "hooks": {
            "SessionStart": [{"hooks": [{"type": "command", "command": T + "logger.py layer-flag"}]}],
            "PreToolUse": [
                {"matcher": "*", "hooks": [{"type": "command", "command": T + "logger.py pre"}]},
                {"matcher": "Edit|Write|MultiEdit|NotebookEdit",
                 "hooks": [{"type": "command", "command": guard_cmd, "timeout": 2}]},
            ],
            "PostToolUse": [{"matcher": "*", "hooks": [{"type": "command", "command": T + "logger.py post"}]}],
        },
    }
    if disable:
        s["disableAllHooks"] = True
    return s
cases = {
    "c1-healthy":   settings(T + "guard.py healthy"),
    "c2-child":     settings(T + "guard.py healthy"),
    "c3-timeout":   settings(T + "guard.py sleep"),
    "c4-exit1":     settings(T + "guard.py exit1"),
    "c5-malformed": settings(T + "guard.py malformed"),
    "c6-missing":   settings(T + "missing-guard"),          # executable path that does not exist
    "c7-disabled":  settings(T + "guard.py healthy", disable=True),
    "c8-shell":     settings(T + "guard.py healthy"),
    "c9-bare":      settings(T + "guard.py healthy"),
    "i1-healthy":   settings(T + "guard.py healthy"),
    "i2-child":     settings(T + "guard.py healthy"),
}
for name, s in cases.items():
    with open(f"{root}/settings/{name}.json", "w") as f:
        json.dump(s, f, indent=1)
PY
echo "fixture ready: $ROOT"
