#!/usr/bin/env zsh
# =============================================================================
# BASE.ZSH — the archx/ signpost (scope folder, ai/-pattern)
# =============================================================================
# Location: ~/.config/zsh/archx/base.zsh (authored on the surgical table
# ~/ia-sync/zsh/ — deploy.sh spreads to both machines; never edit live copy)
# Sourced by: config.zsh (interactive shells), guarded — same hook as ai/base.zsh
# Contract: idempotent + side-effect-free on source — defines only, never runs
#           work or prints (decision 0009 L2 discipline carried over).
#
# Scope: archx — Arch Linux monitoring suite. Cross-machine (home + office).
# Retrofit 2026-08-05 (WP5) — collapses the direct config.*.zsh → keyboard.zsh /
# commands.zsh double-source into the canonical config → base.zsh → partitions
# chain (reference: nablarva/base.zsh).
# =============================================================================

# -----------------------------------------------------------------------------
# PARTITION 1: control panel (aliases only — bodies live in engines)
# -----------------------------------------------------------------------------
[[ -f ~/.config/zsh/archx/keyboard.zsh ]] && source ~/.config/zsh/archx/keyboard.zsh

# -----------------------------------------------------------------------------
# PARTITION 2: archx engine (troubleshoot + substrate_* via bash.substrates.sh)
# -----------------------------------------------------------------------------
[[ -f ~/.config/zsh/archx/commands.zsh ]] && source ~/.config/zsh/archx/commands.zsh
