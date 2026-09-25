#!/usr/bin/env zsh
# =============================================================================
# OVITMUGEN.ZSH — ovitmugen engine (tmux manager: frame + agents, layout C)
# =============================================================================
# Location: ~/.config/zsh/session/ovitmugen.zsh (table-authored in ~/ia-sync/zsh/;
#           `bash deploy.sh` spreads — never edit the live copy)
# Sourced by: session/base.zsh PARTITION 5 · aliases: session/keyboard.zsh ov-*
# Body: ovitmugen.py (stdlib; `ov-selftest` = isolated servers, zero side effects)
# Design: ~/unikuklatrix/nablarva/.dev/session/ovitmugen-00-console/raw/
#         draft.trajectory.ovitmugen-architecture.2026-09-23.md
# Laws (full list in ovitmugen.py header): views only — never send-keys; closing a
#   viewer never kills an agent; every tmux call names its server (-L).
# Contract of this file: definitions only on source.
# =============================================================================

_ov_py() {
    local py="$HOME/.config/zsh/session/ovitmugen.py"
    if [[ ! -f "$py" ]]; then
        echo "[ov] ovitmugen.py not found at $py — was deploy.sh run?" >&2
        return 1
    fi
    python3 "$py" "$@"
}

_ov_up()       { _ov_py up "$@"; }        # ov-up <slug> [@preset | tab...] [--dry-run]
_ov_tab()      { _ov_py tab "$@"; }       # ov-tab <slug> <tab|index|@id>
_ov_ls()       { _ov_py ls "$@"; }        # ov-ls [slug] [--json]
_ov_down()     { _ov_py down "$@"; }      # ov-down <slug> [--frame|--views|--idle] [--dry-run]
_ov_console()  { _ov_py console "$@"; }   # ov-console [slug] (slug optional inside the frame)
_ov_selftest() { _ov_py selftest; }
