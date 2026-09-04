#!/usr/bin/env zsh
# =============================================================================
# RUNBOOK.ZSH — rb engine (session browser verbs)
# =============================================================================
# Location: ~/.config/zsh/nablarva/runbook.zsh (table-authored; deploy.sh spreads)
# Sourced by: nablarva/base.zsh PARTITION 3
# Vars used: PROJECT_NAB_PATH (set by config.<machine>.zsh), RB_ROOT (override)
# Contract: definitions only on source; work happens when rb-* aliases are called.
# =============================================================================

# ---------------------------------------------------------------------------
# _rb_resolve_root: finds .dev/session/ root — caller passes explicit or ""
#   Order: explicit > $RB_ROOT env > $PROJECT_NAB_PATH/.dev/session > walk-up
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

    if [[ -n "${PROJECT_NAB_PATH:-}" ]]; then
        local candidate="$PROJECT_NAB_PATH/.dev/session"
        if [[ -d "$candidate" ]]; then
            echo "$candidate"
            return 0
        fi
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
# _rb_open: launch the runbook TUI
# ---------------------------------------------------------------------------
_rb_open() {
    local explicit="${1:-}"
    local root
    root="$(_rb_resolve_root "$explicit")"

    if [[ -z "$root" ]]; then
        echo "[rb-open] could not locate .dev/session/ — set \$RB_ROOT or \$PROJECT_NAB_PATH, or cd into the project" >&2
        return 1
    fi

    local py="$HOME/.config/zsh/nablarva/runbook.py"
    if [[ ! -f "$py" ]]; then
        echo "[rb-open] runbook.py not found at $py — was deploy.sh run?" >&2
        return 1
    fi

    python3 "$py" --root "$root"
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
|  rb-open [root]    Launch TUI browser (all beds in .dev/session) |
|  rb-pick [root]    fzf picker — prints selected bed path         |
|  rb-help           This help panel                               |
|                                                                  |
|  ROOT RESOLUTION (in order):                                     |
|  1. explicit argument  2. $RB_ROOT env  3. $PROJECT_NAB_PATH     |
|     /.dev/session      4. walk-up from $PWD                      |
|                                                                  |
|  TUI KEYBINDS:                                                   |
|  ↑ ↓        scroll D2 / navigate D1                             |
|  j / k      move item cursor in D2 (file entries)               |
|  1–5        jump to section  (R2 STATUS / R5 _bus / R1 RUNBOOK  |
|             / R3 bed-root / R4 raw)                              |
|  Tab        switch focus D1 ↔ D2                                 |
|  F          toggle R1 RUNBOOK section                            |
|  r          manual reload STATUS + _bus/                         |
|  e / Enter  open item-cursor file in $EDITOR                     |
|  p          print selected path to terminal scroll-back          |
|  q / Esc    quit                                                 |
+------------------------------------------------------------------+
EOF
}
