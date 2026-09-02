#!/usr/bin/env zsh
# tunnel-codex.selftest.zsh — fixture-only proof for tunnel-codex.zsh / tunnel-codex.py.
#
# NO live Codex call, NO quota spent — the fake `codex` executable below (a small
# python3 script) speaks canned JSON-RPC 2.0 over stdio, shaped from the same pinned
# 0.152.1 schema tunnel-codex.py itself was built against (see that file's header).
# This proves the shim's OWN request/response wiring and exit-code contract; it does
# NOT prove the real app-server accepts these calls — that is session t3's job
# (majkee-enabled, one scoped live round-trip), not this selftest's.
#
# Proves: initialize handshake, preflight parse (account/read + model/list), the full
# open->send->steer->read chain (start/steer/completed/read-back extraction), --sandbox
# enum validation, refuse-without-enable (Law 2.4), and the reconcile-mismatch path.

set -euo pipefail

selftest_dir="${0:A:h}"
wrapper="$selftest_dir/tunnel-codex.zsh"
work_dir="$(mktemp -d)"
trap 'rm -rf -- "$work_dir"' EXIT

fixture_dir="$work_dir/bin"
mkdir -p "$fixture_dir"
state_file="$work_dir/tunnel.state.json"

# --- the fake `codex app-server --stdio` -----------------------------------------
# Stateless per-invocation responder: echoes back whatever threadId/expectedTurnId the
# real client sent, so continuity across separate shim invocations comes from the
# shim's OWN state file (tunnel.state.json) — exactly as it would against the real
# server — never from memory inside this fixture.
cat > "$fixture_dir/codex" <<'FIXTURE'
#!/usr/bin/env python3
import json
import os
import sys


def send(obj):
    sys.stdout.write(json.dumps(obj) + "\n")
    sys.stdout.flush()


MISMATCH = os.environ.get("FIXTURE_RECONCILE_MISMATCH") == "1"
TURN_STATUS = os.environ.get("FIXTURE_TURN_STATUS", "completed")
# Regression fixture: reproduce the OLD t3 FAIL shape — a stored threadId whose
# thread/start took zero turns has no rollout on codex-cli 0.152.1, so every
# thread/resume against it dies with -32600 "no rollout found". Toggled on to prove
# the shim still surfaces this cleanly (exit 30) if it were ever hit again.
NO_ROLLOUT = os.environ.get("FIXTURE_NO_ROLLOUT") == "1"

argv = sys.argv[1:]
if not (len(argv) >= 2 and argv[0] == "app-server" and "--stdio" in argv):
    sys.stderr.write("fixture codex: expected 'app-server --stdio', got: %r\n" % (argv,))
    sys.exit(1)

for raw in sys.stdin:
    raw = raw.strip()
    if not raw:
        continue
    msg = json.loads(raw)
    method = msg.get("method")
    rid = msg.get("id")
    params = msg.get("params") or {}

    if method == "initialize":
        send({"jsonrpc": "2.0", "id": rid, "result": {
            "serverInfo": {"name": "fixture-app-server", "version": "0.152.1-fixture"},
        }})
    elif method == "initialized":
        pass  # client notification — no response
    elif method == "account/read":
        send({"jsonrpc": "2.0", "id": rid, "result": {
            "account": {"type": "chatgpt", "planType": "prolite"},
            "requiresOpenaiAuth": True,
        }})
    elif method == "model/list":
        send({"jsonrpc": "2.0", "id": rid, "result": {
            "data": [{"id": "gpt-5.6-fixture", "displayName": "Fixture Model"}],
        }})
    elif method == "thread/start":
        send({"jsonrpc": "2.0", "id": rid, "result": {
            "thread": {"id": "thread-fixture-1", "status": "idle"},
            "model": params.get("model") or "gpt-5.6-fixture",
            "sandbox": params.get("sandbox"),
            "approvalPolicy": params.get("approvalPolicy", "never"),
            "approvalsReviewer": "user",
            "cwd": os.getcwd(),
            "modelProvider": "openai",
        }})
    elif method == "thread/resume":
        thread_id = params.get("threadId")
        if NO_ROLLOUT:
            send({"jsonrpc": "2.0", "id": rid, "error": {
                "code": -32600,
                "message": f"no rollout found for thread id {thread_id}",
            }})
        else:
            send({"jsonrpc": "2.0", "id": rid, "result": {
                "thread": {"id": thread_id, "status": "idle"},
            }})
    elif method in ("turn/start", "turn/steer"):
        thread_id = params.get("threadId")
        turn_id = params.get("expectedTurnId") or "turn-fixture-1"
        send({"jsonrpc": "2.0", "id": rid, "result": {
            "turn": {"id": turn_id, "status": "inProgress", "items": []},
        }})
        agent_text = "STEERED" if method == "turn/steer" else "OPENED"
        send({"jsonrpc": "2.0", "method": "item/completed", "params": {
            "threadId": thread_id, "turnId": turn_id, "completedAtMs": 0,
            "item": {"id": "item-1", "type": "agentMessage", "text": agent_text},
        }})
        send({"jsonrpc": "2.0", "method": "turn/completed", "params": {
            "threadId": thread_id,
            "turn": {"id": turn_id, "status": TURN_STATUS, "items": []},
        }})
    elif method == "thread/read":
        thread_id = params.get("threadId")
        turns = [] if MISMATCH else [{"id": "turn-fixture-1", "status": "completed", "items": []}]
        send({"jsonrpc": "2.0", "id": rid, "result": {
            "thread": {"id": thread_id, "turns": turns},
        }})
    elif rid is not None:
        send({"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": f"fixture: unhandled method {method}"}})
FIXTURE
chmod +x "$fixture_dir/codex"

# Only `codex` is shadowed; everything else (python3, jq if present, rm, cat) resolves
# through the real PATH — no isolated PATH needed since there is no injection surface
# to sandbox against here (args reach python as argv elements, never shell text).
export PATH="$fixture_dir:$PATH"
export TUNNEL_CODEX_STATE="$state_file"
export TUNNEL_CODEX_TIMEOUT=5   # fixture replies instantly; keep any real hang short

integer ok_count=0
integer fail_count=0
LAST_OUTPUT=""
integer LAST_EXIT=0

# Runs "$@", capturing combined output into LAST_OUTPUT and its exit code into
# LAST_EXIT, WITHOUT tripping `set -e` and WITHOUT running in a subshell (a plain
# `var=$(cmd)` command-substitution assignment would do both of those wrong: -e would
# abort on the first nonzero exit, and any counter increments inside a substitution
# subshell would never reach the caller's variables).
run() {
  set +e
  LAST_OUTPUT="$("$@" 2>&1)"
  LAST_EXIT=$?
  set -e
}

check_exit() {
  local label="$1" expected="$2"
  if (( LAST_EXIT != expected )); then
    print -u2 -- "not ok - $label (expected exit $expected, got $LAST_EXIT)"
    print -u2 -- "  output: $LAST_OUTPUT"
    (( fail_count += 1 ))
  else
    print -- "ok - $label (exit $expected)"
    (( ok_count += 1 ))
  fi
}

assert_contains() {
  local label="$1" haystack="$2" needle="$3"
  if [[ "$haystack" == *"$needle"* ]]; then
    print -- "ok - $label"
    (( ok_count += 1 ))
  else
    print -u2 -- "not ok - $label (expected to contain: $needle)"
    print -u2 -- "  actual: $haystack"
    (( fail_count += 1 ))
  fi
}

assert_true() {
  local label="$1" condition="$2"
  if [[ "$condition" == true ]]; then
    print -- "ok - $label"
    (( ok_count += 1 ))
  else
    print -u2 -- "not ok - $label"
    (( fail_count += 1 ))
  fi
}

# --- 1. zsh -n / py_compile on both scripts --------------------------------------
if zsh -n "$wrapper"; then
  print -- "ok - zsh -n clean on tunnel-codex.zsh"
  (( ok_count += 1 ))
else
  print -u2 -- "not ok - zsh -n failed on tunnel-codex.zsh"
  (( fail_count += 1 ))
fi

if zsh -n "$selftest_dir/tunnel-codex.selftest.zsh"; then
  print -- "ok - zsh -n clean on tunnel-codex.selftest.zsh (self)"
  (( ok_count += 1 ))
else
  print -u2 -- "not ok - zsh -n failed on tunnel-codex.selftest.zsh"
  (( fail_count += 1 ))
fi

if python3 -m py_compile "$selftest_dir/tunnel-codex.py"; then
  print -- "ok - python3 -m py_compile clean on tunnel-codex.py"
  (( ok_count += 1 ))
else
  print -u2 -- "not ok - py_compile failed on tunnel-codex.py"
  (( fail_count += 1 ))
fi

# --- 2. refuse-without-enable (Law 2.4) -----------------------------------------
rm -f -- "$state_file"

run zsh "$wrapper" send "hello"
check_exit "refuse-without-enable: send with no state file" 10
assert_true "refuse-without-enable created no state file" "$([[ -f "$state_file" ]] && echo false || echo true)"

run zsh "$wrapper" status
check_exit "refuse-without-enable: status with no state file" 10

run zsh "$wrapper" open
check_exit "refuse-without-enable: open without --enable" 10

# --- 3. --sandbox enum validation -----------------------------------------------
rm -f -- "$state_file"

run zsh "$wrapper" open --enable --sandbox workspaceWrite
check_exit "sandbox enum: rejects camelCase/legacy value" 11
assert_true "invalid --sandbox created no state file" "$([[ -f "$state_file" ]] && echo false || echo true)"

# --- 4. initialize handshake + preflight parse ONLY — NO thread/start (open) ----
# Fix (2026-09-03, t3 FAIL): open no longer calls thread/start. It preflights and
# persists threadId: null; the thread is born on the first send.
rm -f -- "$state_file"

run zsh "$wrapper" open --enable --sandbox read-only
check_exit "open --enable: initialize + preflight, NO thread/start" 0
assert_contains "open output says no thread yet" "$LAST_OUTPUT" "no thread yet"

assert_true "open --enable created tunnel.state.json" "$([[ -f "$state_file" ]] && echo true || echo false)"
if [[ -f "$state_file" ]]; then
  assert_true "state file records threadId as null (not born yet)" \
    "$(grep -q '"threadId": null' "$state_file" && echo true || echo false)"
  assert_true "state file records sandbox from open args" \
    "$(grep -q '"sandbox": "read-only"' "$state_file" && echo true || echo false)"
fi

# idempotent reopen — threadId still null, no re-enable needed, no spawn required
run zsh "$wrapper" open
check_exit "open (reopen, threadId still null, no --enable needed)" 0
assert_contains "reopen output still says no thread yet" "$LAST_OUTPUT" "no thread yet"

# --- 4b. read/resume/steer on a null threadId refuse cleanly (exit 12) ----------
run zsh "$wrapper" read
check_exit "read before any send: no-thread (exit 12)" 12

run zsh "$wrapper" resume
check_exit "resume before any send: no-thread (exit 12)" 12

run zsh "$wrapper" steer "nothing to steer yet"
check_exit "steer before any send: no-thread (exit 12)" 12

# --- 5. first send = thread birth (thread/start + turn/start, same connection) --
run zsh "$wrapper" send "hello codex"
check_exit "send (birth): thread/start -> turn/start -> turn/completed -> reconcile" 0
assert_contains "send extracted the agent message text" "$LAST_OUTPUT" "OPENED"
assert_true "state file now records the born threadId" \
  "$(grep -q '"threadId": "thread-fixture-1"' "$state_file" && echo true || echo false)"

# --- 5b. second send = resume path (threadId already stored) --------------------
run zsh "$wrapper" send "hello again"
check_exit "send (resume): thread/resume -> turn/start -> turn/completed -> reconcile" 0
assert_contains "second send extracted the agent message text" "$LAST_OUTPUT" "OPENED"

run zsh "$wrapper" steer "more please"
check_exit "steer: turn/steer(expectedTurnId) -> turn/completed -> reconcile" 0
assert_contains "steer extracted the agent message text" "$LAST_OUTPUT" "STEERED"

run zsh "$wrapper" read
check_exit "read: thread/read(includeTurns=true) raw result" 0
assert_contains "read output contains the completed turn id" "$LAST_OUTPUT" "turn-fixture-1"
assert_contains "read output contains status completed" "$LAST_OUTPUT" "completed"

run zsh "$wrapper" resume
check_exit "resume: thread/resume liveness probe" 0
assert_contains "resume output names the resumed thread" "$LAST_OUTPUT" "thread-fixture-1"

# --- 6. reconcile-mismatch path --------------------------------------------------
export FIXTURE_RECONCILE_MISMATCH=1
run zsh "$wrapper" send "trigger mismatch"
unset FIXTURE_RECONCILE_MISMATCH
check_exit "reconcile-mismatch: thread/read omits the driven turn" 50

# --- 6b. regression: OLD zero-turn-thread failure shape still surfaces cleanly --
# Reproduces the exact t3 FAIL: a threadId that was allocated without a rollout
# (as the old open's zero-turn thread/start used to produce) must still fail
# thread/resume with a clean, documented exit 30 — never hang, never silently
# succeed. This is the regression guard for the bug this fix removes at the source.
regression_state="$work_dir/tunnel.state.regression.json"
cat > "$regression_state" <<JSON
{
  "enabled": true,
  "threadId": "dead-thread-no-rollout",
  "lastTurnId": null,
  "model": "gpt-5.6-fixture",
  "sandbox": "read-only",
  "created": "2026-09-02T22:45:16Z"
}
JSON

export FIXTURE_NO_ROLLOUT=1
run zsh "$wrapper" resume --state "$regression_state"
unset FIXTURE_NO_ROLLOUT
check_exit "regression: resume on dead-rollout threadId (exit 30, old FAIL shape)" 30
assert_contains "regression: server message surfaced verbatim" "$LAST_OUTPUT" "no rollout found"

# --- 7. status / close ------------------------------------------------------------
run zsh "$wrapper" status
check_exit "status: prints state file (local-only, no spawn)" 0
assert_contains "status output names the thread" "$LAST_OUTPUT" "thread-fixture-1"

run zsh "$wrapper" close
check_exit "close: removes state file, exit 0" 0
assert_true "close removed the state file (Law 2.4 re-armed)" \
  "$([[ -f "$state_file" ]] && echo false || echo true)"

run zsh "$wrapper" send "should be refused"
check_exit "post-close: send refuses again (Law 2.4 re-armed)" 10

print --
if (( fail_count == 0 )); then
  print -- "$ok_count/$ok_count tunnel-codex self-tests passed"
  exit 0
else
  print -u2 -- "$fail_count check(s) FAILED ($ok_count passed)"
  exit 1
fi
