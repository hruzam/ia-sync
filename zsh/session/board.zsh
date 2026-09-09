#!/usr/bin/env zsh
# =============================================================================
# BOARD.ZSH — presence-board engine (the session scope's dashboard organ)
# =============================================================================
# Location: ~/.config/zsh/session/board.zsh (table-authored; deploy.sh spreads)
# Sourced by: session/base.zsh PARTITION 3
# Contract (LAW): ~/reposoma/raw.guides/runbook/res/presence-board.md
#   (gaveled 2026-09-09, reposoma 0f48dce). Advisory only — a record informs,
#   it never commands, authorizes, locks, or closes anything.
# Grammar lives ONCE in runbook.py (presence-board/v1 composer + strict parser);
# these verbs are thin wrappers. Own-attachment memory: machine-local state at
# ~/.local/state/session-board/ — never synced.
# Vars: RB_BOARD (board dir override; default ~/reposoma/_active) · RB_SEAT
#   (declaring seat; default majkee) · MACHINE_NAME (host label)
# Contract of this file: definitions only on source.
# =============================================================================

_rb_board_py() {
    local py="$HOME/.config/zsh/session/runbook.py"
    if [[ ! -f "$py" ]]; then
        echo "[rb-board] runbook.py not found at $py — was deploy.sh run?" >&2
        return 1
    fi
    python3 "$py" board "$@"
}

# _rb_mark [bed] [note...] — attach. Bed defaults to $PWD if it is a bed-like dir.
_rb_mark() {
    local bed="${1:-$PWD}"
    (( $# )) && shift
    if (( $# )); then
        _rb_board_py mark --bed "$bed" --note "$*"
    else
        _rb_board_py mark --bed "$bed"
    fi
}

# _rb_unmark [bed|id] — detach own record(s); no arg = all own on this machine.
_rb_unmark() {
    local target="${1:-}"
    if [[ -z "$target" ]]; then
        _rb_board_py unmark
    elif [[ "$target" =~ '^[0-9a-f]{32}$' ]]; then
        _rb_board_py unmark --id "$target"
    else
        _rb_board_py unmark --bed "$target"
    fi
}

# _rb_board — render the board; * marks own attachments.
_rb_board() {
    _rb_board_py list
}
