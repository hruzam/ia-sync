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
# _rb_open: launch the runbook TUI
# ---------------------------------------------------------------------------
_rb_open() {
    local explicit="${1:-}"
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
|  TUI KEYBINDS (v0.2):                                            |
|  ↑ ↓        free-scroll D2 / navigate D1                        |
|  Tab        switch focus D1 ↔ D2                                 |
|  j / k      move node cursor (headers + files)                   |
|  J / K      jump between section groups                          |
|  Enter/Spc  header → fold/unfold group · file → internal reader  |
|  1–5        jump to section  (R2 STATUS / R5 _bus / R1 RUNBOOK  |
|             / R3 bed-root / R4 raw)                              |
|  F          fold/unfold R1 RUNBOOK                               |
|  B          presence-board modal · m/u attach/detach (D1)        |
|  e          open cursor file in $EDITOR                          |
|  p          collect path into buffer (printed at quit)           |
|  b          toggle buffer pane                                   |
|  r          manual reload                                        |
|  q / Esc    quit — buffer prints to scroll-back                  |
|                                                                  |
|  READER:    ↑↓ PgUp/PgDn g/G scroll · e edit · q/Esc/← back      |
+------------------------------------------------------------------+
EOF
}
