#!/usr/bin/env zsh
# codex-run.zsh — canonical wrapper for headless Codex CLI invocation
# Handles: stdin-hang bug (GitHub #20919), silent-exit regression (GitHub #19945)
# Usage: codex-run "<prompt>" [model]
# Env:   CODEX_TIMEOUT (default 300s), CODEX_WORKDIR (cd before exec if set)
# deploy target: ~/.config/zsh/ai/ per decision 0009 — WS5 gavel

set -euo pipefail

# --- args ---
prompt="${1:?codex-run: prompt required}"
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
  # Retry once via script(1) to break pseudo-TTY silent-exit; capture raw again
  raw=$(script -qfc \
    "timeout ${timeout_val} codex exec --json --ephemeral --sandbox workspace-write ${model_flag[*]-} $(printf '%q' "$prompt") < /dev/null" \
    /dev/null) || true
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

# --- extract agent_message text (last occurrence) ---
agent_text=$(echo "$filtered" \
  | grep '"type":"agent_message"' \
  | tail -1 \
  | sed 's/.*"text":"\(.*\)".*/\1/' \
  | sed 's/\\n/\n/g; s/\\"/"/g')

# --- extract usage object ---
usage_obj=$(echo "$filtered" \
  | grep '"type":"turn.completed"' \
  | tail -1 \
  | grep -o '"usage":{[^}]*}' \
  | head -1)

# --- output ---
print -- "$agent_text"
print -u2 "usage: ${usage_obj:-unavailable}"
