#!/usr/bin/env bash

# ⚠ GEMINI LINE PARKED 2026-07-24 — vendor seat re-bound to Codex/GPT (reposoma: temple/decisions/0005 A1).
# Tokens refunded; API line off. Override for archaeology only: GEMINI_LINE_FORCE=1

if [[ -z "$GEMINI_LINE_FORCE" ]]; then
	# Warn once per shell. Two legitimate source paths reach this engine —
	# ai/base.zsh:70 directly, and ai/keyboard.zsh:22 via ai/base.zsh:17 — so
	# without this guard the park notice prints twice at every startup. Both
	# paths are kept on purpose: base.zsh is the loader (ai/README.md:49 —
	# engines hold bodies), and keyboard.zsh needs _gai_* if sourced standalone.
	# The return below still fires on EVERY source, so park semantics are unchanged.
	if [[ -z "$_GEMINI_LINE_WARNED" ]]; then
		print -u2 "gemini-line PARKED 2026-07-24 — see reposoma maintenance/codex-line/ (override: GEMINI_LINE_FORCE=1)"
		_GEMINI_LINE_WARNED=1
	fi
	return 2 2>/dev/null || exit 2
fi

# gemini-processor.sh — Gemini scope: subprocess core + interactive surface
# bash/zsh compatible — no bash 4.3+ exclusive features
#
# Dual-sourced:
#   bash subprocess  — sourced by vega.sh / orby.sh / astrobley.sh / bluebottle.sh
#   zsh interactive  — sourced by base.zsh PARTITION 8 (was: gemini.zsh)
#
# P2 (2026-07-03): _gai_rest_call gets --connect-timeout 10 --max-time 120,
#   model param (URL-built), HTTP code capture, single 503/429 retry (sleep 4).
# 2026-07-11: gemini.zsh merged in — one file per scope (gaveled).

# ── subprocess core (sourced by per-agent launchers, bash) ───────────────────

_gai_api_key() {
    if [[ -z "${GOOGLE_API_KEY:-}" ]]; then
        echo "[gemini-processor.sh] GOOGLE_API_KEY not set" >&2
        return 1
    fi
    echo "$GOOGLE_API_KEY"
}

_gai_payload() {
    # $1 = model (passed for caller compat; model goes in the URL, not the body)
    # $2 = temperature
    # $3 = input text
    # $4 = persona / system instruction (optional)
    local model="$1"
    local temp="$2"
    local input="$3"
    local persona="$4"

    if [[ -n "$persona" ]]; then
        jq -n \
            --arg system_instruction "$persona" \
            --arg contents "$input" \
            '{systemInstruction: {parts: [{text: $system_instruction}]}, contents: [{parts: [{text: $contents}]}]}'
    else
        jq -n \
            --arg contents "$input" \
            '{contents: [{parts: [{text: $contents}]}]}'
    fi
}

_gai_rest_call() {
    # $1 = JSON payload
    # $2 = model string (defaults to gemini-2.5-flash)
    # Returns: JSON response body on stdout; exit 1 on non-200 after retry.
    # Timeout: --connect-timeout 10 --max-time 120 per P2 (Q13 numbers).
    # Retry: single bounded retry on HTTP 503 or 429 (sleep 4, one re-attempt).
    local payload="$1"
    local model="${2:-gemini-2.5-flash}"
    local api_key
    api_key=$(_gai_api_key) || return 1

    local url="https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent"
    local tmp_resp
    tmp_resp=$(mktemp)

    local http_code
    http_code=$(curl -s -o "${tmp_resp}" -w "%{http_code}" \
        --connect-timeout 10 --max-time 120 \
        -X POST "${url}" \
        -H "Content-Type: application/json" \
        -H "x-goog-api-key: ${api_key}" \
        -d "${payload}")

    if [[ "${http_code}" == "200" ]]; then
        cat "${tmp_resp}"
        rm -f "${tmp_resp}"
        return 0
    elif [[ "${http_code}" == "503" || "${http_code}" == "429" ]]; then
        # Single bounded retry — no loop (P2)
        sleep 4
        http_code=$(curl -s -o "${tmp_resp}" -w "%{http_code}" \
            --connect-timeout 10 --max-time 120 \
            -X POST "${url}" \
            -H "Content-Type: application/json" \
            -H "x-goog-api-key: ${api_key}" \
            -d "${payload}")
        if [[ "${http_code}" == "200" ]]; then
            cat "${tmp_resp}"
            rm -f "${tmp_resp}"
            return 0
        fi
    fi

    echo "[_gai_rest_call] HTTP ${http_code} from ${model} — giving up" >&2
    rm -f "${tmp_resp}"
    return 1
}

_gai_strip_noise() {
    # Removes common CLI noise lines from stderr
    grep -vE '^(INFO|DEBUG|WARNING)'
}

_gai_extract() {
    # Extracts the text from the JSON response.
    # Accepts JSON via $1 argument OR stdin (pipe-friendly).
    if [[ $# -gt 0 ]]; then
        echo "$1" | jq -r '.candidates[0].content.parts[0].text'
    else
        jq -r '.candidates[0].content.parts[0].text'
    fi
}

# ── interactive surface (sourced into zsh via base.zsh P8) ───────────────────
# Bodies for keyboard.zsh PARTITION 4 (agy wrappers), PARTITION 6 (hygiene),
# PARTITION 7 (gemini-agents-help). All bodies are bash/zsh compatible.

# PARTITION 4 bodies: agy wrappers
# Model must be set in-session via /model — no pre-lock confirmed on agy.

agy-orby() {
  echo "[agy-orby] ⚠ Set model in-session: /model → 2.5 Flash | Researcher seat"
  agy "$@"
}

# PARTITION 6 bodies: hygiene

gemini-fresh() {
  echo "[hygiene] Spinning fresh Gemini CLI session with clean-slate context..."
  /bin/zsh -c "gemini"
}

agy-fresh() {
  echo "[hygiene] Spinning fresh Antigravity CLI session with clean-slate context..."
  /bin/zsh -c "agy"
}

# PARTITION 7 body: Gemini agent help

gemini-agents-help() {
  cat <<'EOF'
keyboard.zsh — Gemini agent surface (rebuilt 2026-07-03)

  Per-agent scripts — no arg = interactive, arg = headless
    g-orby [task]        Researcher          — gemini-2.5-flash  | web-fetch     | no yolo
    g-bluebottle [blob]  Synthesizer         — gemini-2.5-flash  | headless REST | single-pass
                         OR: echo "blob" | g-bluebottle
                         OR: cat file | g-bluebottle

  Kebab shims (backward-compat):
    gemini-orby          → ~/.config/zsh/ai/orby.sh
    gemini-bluebottle    → ~/.config/zsh/ai/bluebottle.sh

  agy wrappers (model must be set in-session via /model — no pre-lock confirmed):
    agy-orby             → reminder + agy  (set: /model → 2.5 Flash)

  Agent definition files (model: in frontmatter):
    ~/.gemini/agents/orby.md         gemini-2.5-flash (researcher)
    ~/.gemini/agents/bluebottle.md   gemini-2.5-flash (synthesizer — headless REST only)

  Processor (one file per scope — dual-sourced):
    ~/.config/zsh/ai/gemini-processor.sh    _gai_api_key  _gai_payload
                                            _gai_rest_call  _gai_extract
                                            _gai_strip_noise
    # LEGACY? — majkee audit 2026-07-11: _gai_model and _gai_graceful_fail are listed
    # in AGENTS.md and the prior gemini.zsh help text but do not exist in the file.
    # They were either removed in an earlier cleanup or never implemented.

  See: ~/.config/zsh/guides/guide-for-user.md
  For Claude RC surface: ai-help
EOF
}
