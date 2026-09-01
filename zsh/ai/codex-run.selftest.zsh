#!/usr/bin/env zsh
# Deterministic transport/parser test for codex-run.zsh (no network or Codex quota).

set -euo pipefail

selftest_dir="${0:A:h}"
wrapper="$selftest_dir/codex-run.zsh"
fixture_dir="$(mktemp -d)"
trap 'rm -rf -- "$fixture_dir"' EXIT

cat > "$fixture_dir/codex" <<'FIXTURE'
#!/usr/bin/env zsh
set -euo pipefail

prompt="${argv[-1]}"
python3 - "$prompt" <<'PY'
import json
import sys

prompt = sys.argv[1]
events = [
    {"type": "thread.started", "thread_id": "selftest"},
    {"type": "turn.started"},
    {
        "type": "item.completed",
        "item": {
            "id": "item_0",
            "type": "agent_message",
            "text": "not the final message",
            "status": "completed",
        },
    },
    {
        "type": "item.completed",
        "item": {
            "id": "item_1",
            "type": "agent_message",
            "text": prompt,
            "status": "completed",
        },
    },
    {
        "type": "turn.completed",
        "usage": {
            "input_tokens": 11,
            "cached_input_tokens": 7,
            "output_tokens": 5,
            "reasoning_output_tokens": 0,
        },
    },
]
for event in events:
    print(json.dumps(event, separators=(",", ":")))
PY
FIXTURE
chmod +x "$fixture_dir/codex"

for command_name in timeout grep tail python3 zsh; do
  ln -s "${commands[$command_name]}" "$fixture_dir/$command_name"
done

usage_line='[usage: {"input_tokens":11,"cached_input_tokens":7,"output_tokens":5,"reasoning_output_tokens":0}]'
hazard_prompt=$'`date`\n$(hostname)\n"double quote"\n\'apostrophe\''
escaped_prompt=$'escaped "quotes", backslash \\, tab\t, unicode λ'

assert_equal() {
  local label="$1"
  local expected="$2"
  local actual="$3"

  if [[ "$actual" != "$expected" ]]; then
    print -u2 -- "not ok - $label"
    print -u2 -- "expected: ${(qqq)expected}"
    print -u2 -- "actual:   ${(qqq)actual}"
    return 1
  fi
  print -- "ok - $label"
}

jq_output=$(print -rn -- "$hazard_prompt" \
  | PATH="$fixture_dir:/usr/bin" /usr/bin/zsh "$wrapper" -)
assert_equal "stdin quote hazards + jq extraction + usage" \
  "$hazard_prompt"$'\n'"$usage_line" "$jq_output"

python_output=$(PATH="$fixture_dir" /usr/bin/zsh "$wrapper" "$escaped_prompt")
assert_equal "positional back-compat + python fallback + JSON escapes" \
  "$escaped_prompt"$'\n'"$usage_line" "$python_output"

# --- adversarial retry lane -------------------------------------------------
# Forces the silent-exit path (GitHub #19945): the fake codex below emits
# nothing on its first invocation (the direct exec), then on the second
# invocation — reachable ONLY through codex-run's script(1) retry — echoes
# the received prompt/model back as JSON. This proves the hardened retry
# (zsh/ai/codex-run.zsh) carries untrusted prompt/model/timeout through the
# retry as environment data read by an explicitly-invoked inner zsh, never as
# interpolated shell source: `;`, `$( )`, backticks, whitespace, quotes, and
# newlines in BOTH values must round-trip as inert data, and no injected
# command may execute.
adversarial_dir="$(mktemp -d)"
trap 'rm -rf -- "$fixture_dir" "$adversarial_dir"' EXIT
retry_marker="$adversarial_dir/.retry_marker"

cat > "$adversarial_dir/codex" <<'FIXTURE'
#!/usr/bin/env zsh
set -euo pipefail

marker="${CODEX_RUN_SELFTEST_RETRY_MARKER:?marker env var required}"

if [[ ! -f "$marker" ]]; then
  # First invocation: simulate the silent-exit regression (GitHub #19945) —
  # emit nothing and exit 0, forcing codex-run's retry path.
  touch "$marker"
  exit 0
fi

# Second invocation happens only through the script(1) retry.
model=""
integer i=1
while (( i <= $#argv )); do
  if [[ "${argv[i]}" == "-m" ]]; then
    model="${argv[i+1]}"
  fi
  (( i++ ))
done
prompt="${argv[-1]}"

python3 - "$prompt" "$model" <<'PY'
import json
import sys

prompt, model = sys.argv[1], sys.argv[2]
payload = json.dumps({"prompt": prompt, "model": model}, ensure_ascii=False)
events = [
    {"type": "thread.started", "thread_id": "retry-selftest"},
    {"type": "turn.started"},
    {
        "type": "item.completed",
        "item": {
            "id": "item_0",
            "type": "agent_message",
            "text": payload,
            "status": "completed",
        },
    },
    {
        "type": "turn.completed",
        "usage": {
            "input_tokens": 3,
            "cached_input_tokens": 1,
            "output_tokens": 2,
            "reasoning_output_tokens": 0,
        },
    },
]
for event in events:
    print(json.dumps(event, separators=(",", ":")))
PY
FIXTURE
chmod +x "$adversarial_dir/codex"

for command_name in timeout grep tail python3 zsh script; do
  ln -s "${commands[$command_name]}" "$adversarial_dir/$command_name"
done

retry_pwn_marker="$adversarial_dir/PWNED_IF_EXECUTED"

retry_hazard_prompt="\`touch ${retry_pwn_marker}.prompt.backtick\`; \$(touch ${retry_pwn_marker}.prompt.subshell); \"double quote\"; 'single quote';"$'\nsecond line\twith tab'
retry_hazard_model="evil-model; touch ${retry_pwn_marker}.model.semicolon; \$(touch ${retry_pwn_marker}.model.subshell); \`touch ${retry_pwn_marker}.model.backtick\`; \"double\"; 'single';"$'\nmodel second line\twith tab'

usage_line_retry='[usage: {"input_tokens":3,"cached_input_tokens":1,"output_tokens":2,"reasoning_output_tokens":0}]'

retry_output=$(print -rn -- "$retry_hazard_prompt" \
  | CODEX_RUN_SELFTEST_RETRY_MARKER="$retry_marker" \
    PATH="$adversarial_dir:/usr/bin" /usr/bin/zsh "$wrapper" - "$retry_hazard_model")

retry_message="${retry_output%%$'\n'*}"
retry_usage_tail="${retry_output##*$'\n'}"

decoded_prompt=$(print -r -- "$retry_message" | python3 -c 'import json,sys; sys.stdout.write(json.load(sys.stdin)["prompt"])')
decoded_model=$(print -r -- "$retry_message" | python3 -c 'import json,sys; sys.stdout.write(json.load(sys.stdin)["model"])')

if [[ ! -f "$retry_marker" ]]; then
  print -u2 -- "not ok - adversarial retry: fake codex never called (test harness broken)"
  exit 1
fi
print -- "ok - adversarial retry: silent-exit path was actually exercised"

assert_equal "adversarial retry: prompt survives script(1) retry as inert data" \
  "$retry_hazard_prompt" "$decoded_prompt"
assert_equal "adversarial retry: model survives script(1) retry as inert data" \
  "$retry_hazard_model" "$decoded_model"
assert_equal "adversarial retry: usage present on stdout after retry" \
  "$usage_line_retry" "$retry_usage_tail"

if print -rl -- "$adversarial_dir"/PWNED_IF_EXECUTED*(N) | grep -q .; then
  print -u2 -- "not ok - adversarial retry: injected command executed (injection succeeded!)"
  exit 1
fi
print -- "ok - adversarial retry: no injected command executed (prompt/model stayed inert)"

print -- "7/7 codex-run self-tests passed"
