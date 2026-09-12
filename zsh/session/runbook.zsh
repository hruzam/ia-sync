#!/usr/bin/env zsh
# =============================================================================
# RUNBOOK.ZSH — rb engine (runbook browser — the session scope's first organ)
# =============================================================================
# Location: ~/.config/zsh/session/runbook.zsh (table-authored; deploy.sh spreads)
# Sourced by: session/base.zsh PARTITION 2
# Vars used: RB_ROOT — operator's default .dev/session/ bench, exported by
#            config.<machine>.zsh. Tool is project-agnostic; the machine binding
#            lives in config, never here (rescoped out of nablarva/ 2026-09-06).
# Contract: definitions only on source; work happens when rb-* aliases are called.
# =============================================================================

# ---------------------------------------------------------------------------
# _rb_resolve_root: finds .dev/session/ root — caller passes explicit or ""
#   Order: explicit > $RB_ROOT (config default bench) > walk-up from $PWD
# ---------------------------------------------------------------------------
_rb_resolve_root() {
    local explicit="${1:-}"

    if [[ -n "$explicit" && -d "$explicit" ]]; then
        echo "$explicit"
        return 0
    fi

    if [[ -n "${RB_ROOT:-}" && -d "$RB_ROOT" ]]; then
        echo "$RB_ROOT"
        return 0
    fi

    # Walk-up: stop only at a directory named "session" whose parent is ".dev"
    local d="$PWD"
    while [[ "$d" != "/" ]]; do
        if [[ -d "$d/.dev/session" ]]; then
            echo "$d/.dev/session"
            return 0
        fi
        d="${d:h}"
    done

    return 1
}

# ---------------------------------------------------------------------------
# _rb_open: launch the runbook TUI.  rb-open [-R|--right] [root]
#   -R/--right: mirror view — tree column on the right (v toggles live too)
# ---------------------------------------------------------------------------
_rb_open() {
    local explicit="" side_flag=""
    local arg
    for arg in "$@"; do
        case "$arg" in
            -R|--right) side_flag="--right" ;;
            *) explicit="$arg" ;;
        esac
    done
    local root
    root="$(_rb_resolve_root "$explicit")"

    if [[ -z "$root" ]]; then
        echo "[rb-open] could not locate .dev/session/ — set \$RB_ROOT, pass a path, or cd into a project with .dev/session/" >&2
        return 1
    fi

    local py="$HOME/.config/zsh/session/runbook.py"
    if [[ ! -f "$py" ]]; then
        echo "[rb-open] runbook.py not found at $py — was deploy.sh run?" >&2
        return 1
    fi

    python3 "$py" --root "$root" ${side_flag:+$side_flag}
}

# ---------------------------------------------------------------------------
# _rb_pick: fzf bed picker (fallback: ls) — opens selected bed or prints path
# ---------------------------------------------------------------------------
_rb_pick() {
    local explicit="${1:-}"
    local root
    root="$(_rb_resolve_root "$explicit")"

    if [[ -z "$root" ]]; then
        echo "[rb-pick] could not locate .dev/session/" >&2
        return 1
    fi

    local selection
    if command -v fzf &>/dev/null; then
        selection=$(
            ls -1 "$root" 2>/dev/null \
            | fzf --prompt="bed> " --height=12 --reverse --no-info
        )
    else
        echo "[rb-pick] fzf not available — beds under $root:" >&2
        ls -1 "$root" 2>/dev/null
        return 0
    fi

    [[ -z "$selection" ]] && return 0
    echo "$root/$selection"
}

# ---------------------------------------------------------------------------
# _rb_help: help panel
# ---------------------------------------------------------------------------
_rb_help() {
    cat << 'EOF'
+------------------------------------------------------------------+
|               RB ENGINE - runbook session browser                |
+------------------------------------------------------------------+
|  rb-open [-R] [root]  Launch TUI (-R: tree column on the right)  |
|  rb-pick [root]    fzf picker — prints selected bed path         |
|  rb-board          Render presence board (* = own attachments)   |
|  rb-mark [bed] [note...]   Attach this session to the board      |
|  rb-unmark [bed|id]        Detach own record(s) (no arg = all)   |
|  rb-help           This help panel                               |
|                                                                  |
|  BOARD LAW: raw.guides/runbook/res/presence-board.md — advisory  |
|  only; informs, never authorizes. ● in D1 = bed attached here.   |
|                                                                  |
|  ROOT RESOLUTION (in order):                                     |
|  1. explicit argument (any .dev/session/ tree)                   |
|  2. $RB_ROOT — default bench, set in config.<machine>.zsh        |
|  3. walk-up from $PWD                                            |
|                                                                  |
|  TUI (v0.3): LEFT = tree (beds → STATUS/_bus/RUNBOOK/files/raw)  |
|  RIGHT = content (bed → overview · file → document · grp → list) |
|                                                                  |
|  ↑↓ PgUp/Dn  move tree / scroll content (by focus; g/G content)  |
|  → ←         expand / collapse (← also parent · content→tree)    |
|  Enter/Spc   toggle branch · file → focus content                |
|  Tab         switch pane · J/K jump between beds                 |
|  1–5         jump to part (STATUS/_bus/RUNBOOK/files/raw)        |
|  F           fold selected bed · e edit in $EDITOR               |
|  y / Y       copy path / file content to clipboard               |
|  ≋ vault     cs cards under project umbrellas, newest first;     |
|              Enter = land on card's bed · R = copy its resume:   |
|  B           board modal · m/u attach/detach selected bed        |
|  p           collect path · b buffer pane · r reload             |
|  P           buffer maintainer: x remove line · X clear · y copy |
|  q / Esc     quit — buffer prints to scroll-back                 |
|                                                                  |
|  v            flip tree column left ↔ right (remembered)         |
|  < / >        move the pane divider (5% steps, remembered)       |
|  A A          drain a consumed card → archive/ (two presses;     |
|               explicit Cinderella move — routines never archive) |
|  ● before bed name = attached on board (always visible prefix)   |
|  Narrow (<60 cols): focused pane fills screen, Tab flips.        |
|  Place memory: selection + expanded + side survive restarts.     |
+------------------------------------------------------------------+
EOF
}
