#!/usr/bin/env zsh
# =============================================================================
# KEYBOARD.ZSH — session/ control panel (aliases + comments ONLY)
# =============================================================================
# Location: ~/.config/zsh/session/keyboard.zsh (table-authored; deploy.sh spreads)
# Sourced by: session/base.zsh P1
# LAW (guide-for-builder.md §Architecture rules): aliases and comments only —
# every function body lives in an engine, never here.
#
# Scope: session — the session-layer instruments umbrella (majkee gavel 2026-09-06).
# One animal, several organs: runbook browser (P1, live) · cold-start cards
# (P2, reserved — cs-palette fold-in needs a temple gate on ai/base.zsh) ·
# presence dashboard (P3, reserved — pending @Epoch research + majkee design).
# =============================================================================

# --- P1: runbook browser -----------------------------------------------------
alias rb-open='_rb_open'     # launch TUI (rb-open [root])
alias rb-pick='_rb_pick'     # fzf bed picker → prints path
alias rb-help='_rb_help'     # help panel

# --- P2 (reserved): cold-start cards — cs-* land here post temple gate --------

# --- P3: presence board (advisory — informs, never authorizes) ----------------
alias rb-mark='_rb_mark'       # attach:  rb-mark [bed] [note...]
alias rb-unmark='_rb_unmark'   # detach:  rb-unmark [bed|id] (no arg = all own)
alias rb-board='_rb_board'     # render board; * = own attachments

# --- P4: maintenance ---------------------------------------------------------
alias rb-selftest='python3 ~/.config/zsh/session/runbook.py selftest'  # sandboxed, zero side effects

# --- P5: keys panel ----------------------------------------------------------
alias rb-keys='grep -E "^alias (rb|cs)-" ~/.config/zsh/session/keyboard.zsh | sed "s/alias //"'

# --- P6: ovitmugen — tmux manager (frame + agents; views only, never send-keys) ---
# Frame: C-a prefix · C-a h/l focus · C-a </> move split · C-a t console popup
alias ov-up='_ov_up'             # build/attach: ov-up <slug> [@preset | tab...] [--dry-run]
alias ov-tab='_ov_tab'           # switch left pane: ov-tab <slug> <tab|index|@id>
alias ov-ls='_ov_ls'             # beds · tabs (● agent / ○ idle) · views · frame [--json]
alias ov-down='_ov_down'         # peel: ov-down <slug> [--frame|--views|--idle] [--dry-run]
alias ov-console='_ov_console'   # console: ov-console <slug> — Enter switches the left pane
alias ov-selftest='_ov_selftest' # isolated tmux servers, PASS/FAIL, zero side effects
