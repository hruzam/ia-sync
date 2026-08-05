#!/usr/bin/env zsh
# =============================================================================
# DASHBOARD.ZSH — the system/ startup dashboard engine
# =============================================================================
# Location: ~/.config/zsh/system/dashboard.zsh (authored on the surgical table
# ~/ia-sync/zsh/ — deploy.sh spreads to both machines; never edit live copy)
# Sourced by: system/base.zsh (interactive shells), guarded
# Contract: idempotent + side-effect-free on source — defines only, never prints
# Scope: system — startup dashboard: prints @majkee's editable notes on shell open
# =============================================================================

_dash_header() {
    local f="${1:-$HOME/.config/zsh/system/dashboard.md}"
    local line

    [[ -f "$f" ]] || return 0

    while IFS= read -r line || [[ -n "$line" ]]; do
        if [[ "$line" == '## '* ]]; then
            print -P -- "%B%F{cyan}${line#\#\# }%f%b"
        elif [[ -n "$line" ]]; then
            print -r -- "  $line"
        else
            print
        fi
    done < "$f"
}
