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
alias rb-keys='grep -E "^alias (rb|cs|ov)-" ~/.config/zsh/session/keyboard.zsh | sed "s/alias //"'

# --- P6: ovitmugen — tmux manager (frame + agents; views only, never send-keys) ---
# Frame: C-a prefix · C-a h/l focus · C-a </> move split · C-a t console popup
alias ov-up='_ov_up'             # build/attach: ov-up <slug> [@preset | tab...] [--dry-run]
alias ov-tab='_ov_tab'           # switch left pane: ov-tab <slug> <tab|index|@id>
alias ov-ls='_ov_ls'             # beds · tabs (● agent / ○ idle) · views · frame [--json]
alias ov-down='_ov_down'         # peel: ov-down <slug> [--frame|--views|--idle] [--dry-run]
alias ov-console='_ov_console'   # console: ov-console <slug> — Enter switches the left pane
alias ov-selftest='_ov_selftest' # isolated tmux servers, PASS/FAIL, zero side effects

# --- P6: tunnel manager (vault per bed; the shim stays in ai/) — added 2026-10-04 ---
alias tn-ls='_tn_ls'             # list vaults under $RB_ROOT (* = this shell's current)
alias tn-use='_tn_use'           # point this shell at a vault: tn-use <bed> [name]
alias tn-on='_tn_on'             # open: tn-on <bed> [name] [-- --thread <id> --cwd <dir> …]
alias tn-off='_tn_off'           # close: tn-off [bed] [name]
alias tn-st='_tn_st'             # status, intent vs runtime: tn-st [bed] [name]
alias tn-check='_tn_check'       # read-only verdict: tn-check [bed] [name] · tn-check --id <thread> [--cwd <dir>]
alias tn-back='_tn_back'         # after a TUI visit: wait writer-lock holder → resume → check: tn-back [bed] [name] [--timeout S]
alias tn-rebind='_tn_rebind'     # successor: tn-rebind <bed> [name] --thread NEW [--reason TEXT] (carries intent, logs lineage)
alias tn-beds='_tn_beds'         # explorer: numbered beds of this repo's .dev/session → @N works as <bed>
alias tn-threads='_tn_threads'   # explorer: numbered codex threads of this repo → @N works as --thread/--id
alias tn-bed='_tn_bed_n'         # tn-bed N → full path of bed row N
alias tn-tid='_tn_tid_n'         # tn-tid N → full thread id of row N
alias tn-help='_tn_help'         # help panel
