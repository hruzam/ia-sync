#!/usr/bin/env zsh
# =============================================================================
# SESSION-SYNTAX - Active syntax layer loader
# =============================================================================
# Location: ~/.config/zsh/session-syntax.zsh
# Sourced by: ~/.config/zsh/session-helpers.zsh
# =============================================================================
# READS FROM: $SESSION_SHARED_SRC (source — hidden, authoritative)
# NEVER FROM: $SESSION_SHARED_DST (mirror — for outside-PC only)
# =============================================================================

# =============================================================================
# INTERNAL: resolve active layer paths
# Sets _SYNTAX_ACTIVE_FILE, _SYNTAX_LAYER_ID, _SYNTAX_LAYER_FILE, _SYNTAX_SUMMARY_FILE
# =============================================================================
_session_syntax_resolve() {
    local syntax_dir="$SESSION_SHARED_SRC/syntax"
    local active_file="$syntax_dir/active.md"

    if [[ ! -f "$active_file" ]]; then
        echo "[ERROR] active.md not found: $active_file"
        return 1
    fi

    _SYNTAX_ACTIVE_FILE="$active_file"
    _SYNTAX_LAYER_ID=$(grep -m1 'layer_id:' "$active_file" | awk '{print $2}')
    _SYNTAX_LAYER_FILE="$syntax_dir/layers/${_SYNTAX_LAYER_ID}.md"
    _SYNTAX_SUMMARY_FILE="$syntax_dir/layers/${_SYNTAX_LAYER_ID}.summary.md"
}

# =============================================================================
# _session_init_phase_syntax
# Called by session-init. Echoes compact summary.
# =============================================================================
_session_init_phase_syntax() {
    _session_syntax_resolve || return 1

    if [[ ! -f "$_SYNTAX_SUMMARY_FILE" ]]; then
        echo "[WARN] syntax summary not found: $_SYNTAX_SUMMARY_FILE"
        echo "[WARN] run: session-syntax active   to see full active.md"
        return 0
    fi

    cat "$_SYNTAX_SUMMARY_FILE"
}

# =============================================================================
# session-syntax - standalone subcommand
# =============================================================================
session-syntax() {
    local cmd="${1:-}"

    case "$cmd" in
        open)
            _session_syntax_resolve || return 1
            if [[ ! -f "$_SYNTAX_LAYER_FILE" ]]; then
                echo "[ERROR] layer file not found: $_SYNTAX_LAYER_FILE"
                return 1
            fi
            local vdesk
            vdesk=$(wmctrl -d 2>/dev/null | awk '/\*/{print $1}')
            [[ -n "$vdesk" ]] && wmctrl -s "$vdesk"
            subl -a "$_SYNTAX_LAYER_FILE"
            echo "[OK] opened: $_SYNTAX_LAYER_FILE"
            ;;
        active)
            _session_syntax_resolve || return 1
            cat "$_SYNTAX_ACTIVE_FILE"
            ;;
        which)
            _session_syntax_resolve || return 1
            echo "$_SYNTAX_LAYER_FILE"
            ;;
        summary|"")
            _session_init_phase_syntax
            ;;
        -h|help)
            cat << 'EOF'
session-syntax [subcommand]

  (none)    Print compact summary of active syntax layer
  open      Open full layer file in Sublime on current desktop
  active    Print active.md (pointer file)
  which     Print path to active layer file
  help      This help
EOF
            ;;
        *)
            echo "[ERROR] Unknown: $cmd  (session-syntax help)"
            return 1
            ;;
    esac
}

echo "[session] session-syntax loaded"
