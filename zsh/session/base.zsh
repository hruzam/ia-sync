#!/usr/bin/env zsh
# =============================================================================
# BASE.ZSH — the session/ signpost (scope folder, ai/-pattern)
# =============================================================================
# Location: ~/.config/zsh/session/base.zsh (authored on the surgical table
# ~/ia-sync/zsh/ — deploy.sh spreads to both machines; never edit live copy)
# Sourced by: config.<machine>.zsh (interactive shells), guarded
# Contract: idempotent + side-effect-free on source — defines only, never runs
#           work or prints (decision 0009 L2 discipline).
#
# Scope: session — session-layer instruments umbrella (founded 2026-09-06,
# majkee gavel; rescoped out of nablarva/, which is a different animal).
# Reads .dev/session/ trees anywhere; default bench via $RB_ROOT in config.
# Organs land as partitions: runbook browser (live) · cold-start cards
# (reserved) · presence dashboard (reserved).
# =============================================================================

# -----------------------------------------------------------------------------
# PARTITION 1: control panel (aliases only — bodies live in engines)
# -----------------------------------------------------------------------------
[[ -f ~/.config/zsh/session/keyboard.zsh ]] && source ~/.config/zsh/session/keyboard.zsh

# -----------------------------------------------------------------------------
# PARTITION 2: runbook browser engine (rb-* bodies + runbook.py TUI)
# -----------------------------------------------------------------------------
[[ -f ~/.config/zsh/session/runbook.zsh ]] && source ~/.config/zsh/session/runbook.zsh

# -----------------------------------------------------------------------------
# PARTITION 3: presence-board engine (rb-mark / rb-unmark / rb-board bodies)
# Contract: reposoma/raw.guides/runbook/res/presence-board.md (gaveled 2026-09-09)
# -----------------------------------------------------------------------------
[[ -f ~/.config/zsh/session/board.zsh ]] && source ~/.config/zsh/session/board.zsh

# -----------------------------------------------------------------------------
# PARTITION 4+ (reserved): cold-start cards engine (post temple gate)
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# PARTITION 5: ovitmugen engine — tmux manager (frame + agents; views only)
# Added 2026-09-25 (@Trajectory, majkee go). Design + notice:
#   ~/unikuklatrix/nablarva/.dev/session/ovitmugen-00-console/raw/
# -----------------------------------------------------------------------------
[[ -f ~/.config/zsh/session/ovitmugen.zsh ]] && source ~/.config/zsh/session/ovitmugen.zsh
