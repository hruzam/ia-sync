#!/usr/bin/env bash
# =============================================================================
# ZENITH-ZSH.SH — zsh config RAG assistant launcher
# =============================================================================
# Location: ~/.config/zsh/ai/zenith-zsh.sh
# Agent:    ~/.claude/agents/zenith-zsh.md  (Haiku · read-only · broken-wiring log)
# Alias:    zenith-zsh  (keyboard.zsh PARTITION 16)
#
# Usage:
#   zenith-zsh              interactive session (chatbot mode)
#   zenith-zsh "question"   headless one-shot — prints answer and exits
#
# The agent builds its own context on startup by reading the anchor files.
# This script's job is:
#   1. Ensure ~/.config/zsh/blessings/ exists (log target)
#   2. Route to interactive or headless mode
#   3. In headless mode: build a compact preamble so the agent doesn't need
#      to run its full startup sequence for a single question.
# =============================================================================

ZSH_CONF="${HOME}/.config/zsh"
BLESSINGS="${ZSH_CONF}/blessings"

# Ensure blessings dir exists before the agent tries to write broken-wiring.json
mkdir -p "${BLESSINGS}"

# ── headless mode: one-shot question ─────────────────────────────────────────
if [[ -n "${1:-}" ]]; then
  # Build a compact context preamble from the four anchor files.
  # Keeps the Haiku context window lean: summaries only, not full files.
  PREAMBLE=""

  for f in \
    "${ZSH_CONF}/AGENTS.md" \
    "${ZSH_CONF}/ai/README.md" \
    "${ZSH_CONF}/guides/keyboard.md"; do
    if [[ -f "${f}" ]]; then
      PREAMBLE+="=== ${f} ===\n"
      PREAMBLE+="$(cat "${f}")\n\n"
    fi
  done

  claude --agent zenith-zsh -p "$(printf '%b' "${PREAMBLE}")

---
Question: ${*}"
  exit $?
fi

# ── interactive mode ─────────────────────────────────────────────────────────
# The agent's system prompt instructs it to load context on startup.
# No preamble needed here — the agent reads its anchors autonomously.
exec claude --agent zenith-zsh
