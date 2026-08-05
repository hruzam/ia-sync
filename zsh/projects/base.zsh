#!/usr/bin/env zsh
# =============================================================================
# BASE.ZSH — the projects/ signpost (scope folder, ai/-pattern)
# =============================================================================
# Location: ~/.config/zsh/projects/base.zsh (authored on the surgical table
# ~/ia-sync/zsh/ — deploy.sh spreads to both machines; never edit live copy)
# Sourced by: project-switcher.zsh (the scope's eager root engine — projects/
#             toolkits themselves are lazy-loaded on `fo`/`im`/`ltp`/`psd`,
#             see project-switcher.zsh's project_switch(); there is no
#             config.zsh → projects/base.zsh hook, unlike ai/ or nablarva/,
#             because this scope has no single eager entry point to hang
#             one off — project-switcher.zsh already fills that role)
# Contract: idempotent + side-effect-free on source — defines only, never
#           runs work or prints (decision 0009 L2 discipline carried over).
#
# Scope: projects — per-project toolkits (fo/im/ltp/psd/larva). Cross-machine
# (project-switcher.zsh is sourced on both).
#
# PARTITION 2+ intentionally empty by design (mirrors nablarva/base.zsh's
# "mostly-empty by design" shape): toolkit engines (im-toolkit.zsh,
# fo-toolkit.zsh, ltp-toolkit.zsh, psdvs-toolkit.zsh, larva.zsh) are lazy —
# sourced on demand by project_switch(), never eagerly here. Moving them to
# an eager base.zsh partition would change WHEN their aliases become
# available (a behavior change, not a rewiring) — see projects/keyboard.zsh's
# own header for the full rationale (WP4 flag, unchanged by this retrofit).
#
# Retrofit 2026-08-05 (WP5) — reference: nablarva/base.zsh. Replaces the
# direct project-switcher.zsh → projects/keyboard.zsh source line (WP4) with
# this signpost, for structural consistency with the other four scopes.
# =============================================================================

# -----------------------------------------------------------------------------
# PARTITION 1: control panel (aliases only — bodies live in engines)
# -----------------------------------------------------------------------------
[[ -f ~/.config/zsh/projects/keyboard.zsh ]] && source ~/.config/zsh/projects/keyboard.zsh

# -----------------------------------------------------------------------------
# PARTITION 2+ (reserved, deliberately empty): lazy per-project toolkits are
# NOT sourced here — see project_switch() in project-switcher.zsh.
# -----------------------------------------------------------------------------
