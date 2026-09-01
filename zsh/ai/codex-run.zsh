#!/usr/bin/env zsh
# codex-run.zsh — canonical wrapper for headless Codex CLI invocation
# Handles: stdin-hang bug (GitHub #20919), silent-exit regression (GitHub #19945)
# Usage: codex-run "<prompt>" [model] | codex-run - [model]
# Env:   CODEX_TIMEOUT (default 300s), CODEX_WORKDIR (cd before exec if set)
# deploy target: ~/.config/zsh/ai/ per decision 0009 — WS5 gavel

set -euo pipefail

# --- args ---
prompt_arg="${1:?codex-run: prompt required}"
if [[ "$prompt_arg" == "-" ]]; then
  prompt="$(cat)"
else
  prompt="$prompt_arg"
fi
codex_model="${2:-}"

# --- reserved zsh names: do NOT use 'path' or 'fpath' as variables ---
timeout_val="${CODEX_TIMEOUT:-300}"
workdir="${CODEX_WORKDIR:-}"

if [[ -n "$workdir" ]]; then
  cd "$workdir"
fi

# --- build model flag ---
model_flag=()
if [[ -n "$codex_model" ]]; then
  model_flag=(-m "$codex_model")
fi

# --- invoke codex, emit raw merged stream ---
# < /dev/null is MANDATORY — prevents stdin-hang (GitHub #20919)
# Raw stream keeps plain-text errors (auth failure, 429, CLI errors) that grep '^{' would swallow
_run_codex() {
  timeout "$timeout_val" codex exec --json --ephemeral --sandbox workspace-write \
    "${model_flag[@]}" "$prompt" < /dev/null 2>&1
}

raw="$(_run_codex)" || true
filtered="$(print -r -- "$raw" | grep '^{')" || true

# --- silent-exit regression guard (GitHub #19945) ---
if [[ -z "$raw" ]]; then
  # Retry once via script(1) to break pseudo-TTY silent-exit.
  #
  # SECURITY INVARIANT: the -c program text handed to the inner `zsh -c`
  # below is a FIXED string, written once, and is never built from
  # $prompt / $codex_model / $timeout_val. Untrusted values cross into the
  # retry only as environment variables (set on the command line just
  # below) that the explicitly-invoked inner zsh reads back for itself —
  # never by interpolating their content into shell source. Do NOT
  # reintroduce printf '%q'-style substitution of prompt/model/timeout into
  # this program text; that reopens the injection this block exists to
  # close, and also assumes script(1)'s default shell understands zsh's
  # %q output, which it may not.
  _codex_retry_prog='
model_flag_retry=()
if [[ -n "$CODEX_RUN_RETRY_MODEL" ]]; then
  model_flag_retry=(-m "$CODEX_RUN_RETRY_MODEL")
fi
timeout "$CODEX_RUN_RETRY_TIMEOUT" codex exec --json --ephemeral --sandbox workspace-write "${model_flag_retry[@]}" "$CODEX_RUN_RETRY_PROMPT" < /dev/null
'
  raw=$(CODEX_RUN_RETRY_PROMPT="$prompt" \
        CODEX_RUN_RETRY_MODEL="$codex_model" \
        CODEX_RUN_RETRY_TIMEOUT="$timeout_val" \
        script -qfc "zsh -c ${(qq)_codex_retry_prog}" /dev/null) || true
  unset _codex_retry_prog
  filtered="$(print -r -- "$raw" | grep '^{')" || true

  if [[ -z "$raw" ]]; then
    print -u2 "codex-run: filtered stream empty after retry — silent-exit regression; exit 4"
    exit 4
  fi
fi

# --- plain-text failure branch: raw present but no JSON ---
if [[ -n "$raw" && -z "$filtered" ]]; then
  print -u2 "codex-run: no JSON in output — raw tail:"
  print -r -- "$raw" | tail -20 | while IFS= read -r _l; do
    print -u2 "  $_l"
  done

  if print -r -- "$raw" | grep -qiE 'auth|unauthorized|invalid_api_key|rate.?limit|429|unknown model|model not found'; then
    exit 5
  else
    exit 3
  fi
fi

# --- success check: presence of turn.completed ---
# NEVER trust process exit code — inspect the stream
if ! echo "$filtered" | grep -q '"type":"turn.completed"'; then
  # Capture last ~20 raw lines for diagnostics
  print -u2 "codex-run: turn.completed not found in stream — raw tail:"
  print -r -- "$raw" | tail -20 | while IFS= read -r raw_line; do
    print -u2 "  $raw_line"
  done

  # Check for known error patterns: auth, 429, unknown model
  if print -r -- "$raw" | grep -qiE 'auth|unauthorized|invalid_api_key|rate.?limit|429|unknown model|model not found'; then
    print -r -- "$raw" | grep -iE 'error|message' | tail -5 | while IFS= read -r _l; do
      print -u2 "codex-run: upstream — $_l"
    done
    exit 5
  fi

  exit 3
fi

# --- extract final agent message + usage with a JSON parser ---
_emit_result_jq() {
  print -r -- "$filtered" | jq -j -s '
    ([.[]
      | select(.type == "item.completed" and .item.type == "agent_message")
      | .item.text] | last // "") as $agent_text
    | ([.[]
        | select(.type == "turn.completed")
        | .usage] | last // null) as $usage
    | $agent_text,
      (if ($agent_text | endswith("\n")) then "" else "\n" end),
      "[usage: ",
      (if $usage == null then "unavailable" else ($usage | tojson) end),
      "]\n"
  '
}

_emit_result_python() {
  print -r -- "$filtered" | python3 -c '
import json
import sys

events = [json.loads(line) for line in sys.stdin if line.strip()]
messages = [
    event["item"]["text"]
    for event in events
    if event.get("type") == "item.completed"
    and event.get("item", {}).get("type") == "agent_message"
]
usages = [
    event.get("usage")
    for event in events
    if event.get("type") == "turn.completed"
]

agent_text = messages[-1] if messages else ""
usage = usages[-1] if usages else None
sys.stdout.write(agent_text)
if not agent_text.endswith("\n"):
    sys.stdout.write("\n")
usage_text = "unavailable" if usage is None else json.dumps(
    usage, separators=(",", ":"), ensure_ascii=False
)
sys.stdout.write(f"[usage: {usage_text}]\n")
'
}

if (( $+commands[jq] )); then
  if ! _emit_result_jq; then
    print -u2 "codex-run: jq failed to parse JSON stream"
    exit 3
  fi
elif (( $+commands[python3] )); then
  if ! _emit_result_python; then
    print -u2 "codex-run: python3 failed to parse JSON stream"
    exit 3
  fi
else
  print -u2 "codex-run: jq or python3 is required to parse JSON output"
  exit 3
fi
