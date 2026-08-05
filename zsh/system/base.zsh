#!/usr/bin/env zsh
# =============================================================================
# BASE.ZSH — the system/ signpost (scope folder, ai/-pattern)
# =============================================================================
# Location: ~/.config/zsh/system/base.zsh (authored on the surgical table
# ~/ia-sync/zsh/ — deploy.sh spreads to both machines; never edit live copy)
# Sourced by: config.zsh (interactive shells), guarded — same hook as ai/base.zsh
# Contract: idempotent + side-effect-free on source — defines only, never runs
#           work or prints (decision 0009 L2 discipline carried over). The
#           `_ts_header` status-line call stays in config.*.zsh, AFTER this
#           source line — that is genuine "work" (prints), not a definition,
#           so it does not belong in a signpost. Unchanged from pre-WP5.
#
# Scope: system — shell utilities + Tailscale + PHP version switching.
# Reach differs by machine (pre-existing, not introduced by this retrofit):
#   office: keyboard + tailscale + shell.zsh + office.php-switch.zsh
#   home:   keyboard + tailscale only (shell.zsh / office.php-switch.zsh were
#           never sourced on home — preserved exactly, not a WP5 decision)
# PARTITIONS 3-4 below are MACHINE_NAME-guarded to reproduce that split
# exactly, mirroring the guard idiom office.php-switch.zsh already uses
# internally (not a new mechanism).
#
# Pre-existing violation (config.*.zsh sourced keyboard.zsh directly,
# predates WP4) — fixed under WP5 per operator instruction, same pass as the
# WP4 archx/piql/sync/projects retrofit.
# Retrofit 2026-08-05 (WP5) — reference: nablarva/base.zsh.
# =============================================================================

# -----------------------------------------------------------------------------
# PARTITION 1: control panel (aliases only — bodies live in engines)
# -----------------------------------------------------------------------------
[[ -f ~/.config/zsh/system/keyboard.zsh ]] && source ~/.config/zsh/system/keyboard.zsh

# -----------------------------------------------------------------------------
# PARTITION 2: Tailscale engine (cross-machine — both home + office)
# -----------------------------------------------------------------------------
[[ -f ~/.config/zsh/system/tailscale.zsh ]] && source ~/.config/zsh/system/tailscale.zsh

# -----------------------------------------------------------------------------
# PARTITION 3: general shell utilities engine (office only — see header)
# -----------------------------------------------------------------------------
[[ "$MACHINE_NAME" == "office" && -f ~/.config/zsh/system/shell.zsh ]] && source ~/.config/zsh/system/shell.zsh

# -----------------------------------------------------------------------------
# PARTITION 4: office PHP version switching engine (office only — also
# self-guards internally via its own MACHINE_NAME check; guarded here too so
# the source attempt itself matches pre-WP5 reach on home)
# -----------------------------------------------------------------------------
[[ "$MACHINE_NAME" == "office" && -f ~/.config/zsh/system/office.php-switch.zsh ]] && source ~/.config/zsh/system/office.php-switch.zsh

# -----------------------------------------------------------------------------
# PARTITION 5: startup dashboard engine (cross-machine — both home + office)
# -----------------------------------------------------------------------------
[[ -f ~/.config/zsh/system/dashboard.zsh ]] && source ~/.config/zsh/system/dashboard.zsh
