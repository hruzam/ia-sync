#!/usr/bin/env zsh
# =============================================================================
# BASE.ZSH — the nablarva/ signpost (scope folder, ai/-pattern)
# =============================================================================
# Location: ~/.config/zsh/nablarva/base.zsh (authored on the surgical table
# ~/ia-sync/zsh/ — deploy.sh spreads to both machines; never edit live copy)
# Sourced by: config.zsh (interactive shells), guarded — same hook as ai/base.zsh
# Contract: idempotent + side-effect-free on source — defines only, never runs
#           work or prints (decision 0009 L2 discipline carried over).
#
# Scope: nabLarva — larva V3 (project flag L1-L10). Founded 2026-08-02.
# Mostly-empty by design: docs-only phase until gavel docket item 2 (v1 language)
# lands. Partitions grow as organs are born; add a partition per engine, never
# bodies here.
# =============================================================================

# -----------------------------------------------------------------------------
# PARTITION 1: control panel (aliases only — bodies live in engines)
# -----------------------------------------------------------------------------
[[ -f ~/.config/zsh/nablarva/keyboard.zsh ]] && source ~/.config/zsh/nablarva/keyboard.zsh

# -----------------------------------------------------------------------------
# PARTITION 2: nab engine (project verbs: cd, status, harness, devenv transport)
# -----------------------------------------------------------------------------
[[ -f ~/.config/zsh/nablarva/nablarva.zsh ]] && source ~/.config/zsh/nablarva/nablarva.zsh

# -----------------------------------------------------------------------------
# PARTITION 3+ (reserved): stridularium / broker / adapter engines — land here
# post-gavel, one file per organ, wired as new partitions.
# (runbook browser lived here 2026-09-04→06; rescoped to session/ — different animal.)
# -----------------------------------------------------------------------------
