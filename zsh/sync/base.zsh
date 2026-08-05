#!/usr/bin/env zsh
# =============================================================================
# BASE.ZSH — the sync/ signpost (scope folder, ai/-pattern)
# =============================================================================
# Location: ~/.config/zsh/sync/base.zsh (authored on the surgical table
# ~/ia-sync/zsh/ — deploy.sh spreads to both machines; never edit live copy)
# Sourced by: config.zsh (interactive shells), guarded — same hook as ai/base.zsh
# Contract: idempotent + side-effect-free on source — defines only, never runs
#           work or prints (decision 0009 L2 discipline carried over).
#
# Scope: sync — guide-publish synchronizer. Office-only (registry sources live
# on the project checkouts present there; see registries/config.sync.json).
# Retrofit 2026-08-05 (WP5) — collapses the direct config.office.zsh →
# keyboard.zsh / guides.zsh double-source into the canonical config → base.zsh
# → partitions chain (reference: nablarva/base.zsh).
# =============================================================================

# -----------------------------------------------------------------------------
# PARTITION 1: control panel (aliases only — bodies live in engines)
# -----------------------------------------------------------------------------
[[ -f ~/.config/zsh/sync/keyboard.zsh ]] && source ~/.config/zsh/sync/keyboard.zsh

# -----------------------------------------------------------------------------
# PARTITION 2: guide-publish synchronizer engine (sync-guides)
# -----------------------------------------------------------------------------
[[ -f ~/.config/zsh/sync/guides.zsh ]] && source ~/.config/zsh/sync/guides.zsh
