#!/usr/bin/env zsh
# =============================================================================
# KEYBOARD.ZSH — experimental/ control panel (aliases only — no bodies)
# =============================================================================
# Sourced by: experimental/base.zsh PARTITION 1.
# Bodies live in the dispatcher engine (experimental/dispatcher.zsh).
# A per-brick convenience alias is allowed here, but it MUST delegate to
# _exp_run <id> — never re-implement the runner. Contract: experimental/README.md.
# =============================================================================

# -----------------------------------------------------------------------------
# PARTITION 1: dispatcher surface
# -----------------------------------------------------------------------------
alias exp-list='_exp_list'
alias exp-run='_exp_run'

# -----------------------------------------------------------------------------
# PARTITION 2: per-brick convenience shims (delegate to _exp_run <id>)
# -----------------------------------------------------------------------------
alias ox-alpha='_exp_run ox-alpha'
alias ox-alpha-help='_exp_run ox-alpha --help'  # show ox-alpha usage
