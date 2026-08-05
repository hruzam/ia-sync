#!/usr/bin/env zsh
# =============================================================================
# LARVA.ZSH — LARVA system shell plugin
# =============================================================================
# Location: ~/.config/zsh/larva.zsh
# Source:   one line in config.zsh or .zshrc:
#             source ~/.config/zsh/larva.zsh
#
# REQUIRES: config.zsh sourced BEFORE this file.
#   Uses: $HOME, $MACHINE_NAME
#   Uses: PROJECT_*_PATH variables (for OVUM root resolution)
#
# PORTABLE: This file is IDENTICAL across all NIDUS machines.
#   Machine-specific paths come from config.zsh.
#   Copy this file + larva/ scripts folder to any NIDUS.
#
# SETUP ON NEW NIDUS:
#   1. Copy ~/.config/zsh/larva.zsh (this file)
#   2. Copy ~/.config/zsh/larva/ folder (scripts)
#   3. Add `source ~/.config/zsh/larva.zsh` to config.zsh
#   4. Ensure config.zsh defines PROJECT_*_PATH variables
#   5. pip install pyyaml --break-system-packages
#
# =============================================================================

# --- Guard: don't load twice ---
[[ -n "$LARVA_LOADED" ]] && return
export LARVA_LOADED=1

# --- Script directory ---
export LARVA_SCRIPTS_DIR="$HOME/.config/zsh/larva"
export PATH="$HOME/.config/claude/bin:$HOME/.config/gemini/bin:$PATH"

# =============================================================================
# OVUM RESOLUTION
# =============================================================================
# Maps OVUM shortcode → filesystem root.
# Uses PROJECT_*_PATH from config.zsh (machine-specific).
# Add new OVUMs here when they join the system.
# =============================================================================

_larva_ovum_root() {
    local ovum="$1"
    case "$ovum" in
        fo)  echo "${PROJECT_FO_PATH:-$HOME/www/fantasyobchod}" ;;
        im)  echo "${PROJECT_IM_PATH:-$HOME/www/freya}" ;;
        psd) echo "${PROJECT_PSD_PATH:-$HOME/www/psdvs}" ;;
        pupa) echo "${PROJECT_PUPA_PATH:-$HOME/www/kukla}" ;;
        *)
            echo "[LARVA] Unknown OVUM: $ovum" >&2
            return 1
            ;;
    esac
}

# =============================================================================
# ALIASES — LARVA agent tools
# =============================================================================

# @Laika — one-shot scanner, fire and forget
alias laika="$LARVA_SCRIPTS_DIR/laika.sh"  # one-shot codebase scanner (fire and forget)

# NUCLEUS/TRACHEA — interactive consultation with one zone
alias consult="$LARVA_SCRIPTS_DIR/consult.sh"  # interactive consultation with one zone

# NUCLEUS/TRACHEA — broadcast question to all zones in parallel
alias broadcast="$LARVA_SCRIPTS_DIR/broadcast.sh"  # broadcast a question to all zones in parallel

# Slice management — regenerate all repomix slices for an OVUM
alias slices="$LARVA_SCRIPTS_DIR/slices.sh"  # regenerate all repomix slices for an OVUM

# =============================================================================
# ALIASES — Claude CLI agents
# =============================================================================

alias capcom="$HOME/.config/claude/bin/capcom"  # Claude CLI operational planner
alias trajectory="$HOME/.config/claude/bin/trajectory"  # Claude CLI executor

# =============================================================================
# ALIASES — Gemini CLI agents
# =============================================================================

alias athena="$HOME/.config/gemini/bin/athena"    # Gemini CLI operator
alias zenit="$HOME/.config/gemini/bin/zenit"      # Gemini CLI (deep research)
alias horizon="$HOME/.config/gemini/bin/horizon"  # Gemini CLI (fast research)

# =============================================================================
# COMMON ALIASES
# =============================================================================
alias nidus="echo $MACHINE_NAME"  # print this machine's NIDUS name (MACHINE_NAME)

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

# Quick cd to OVUM .larva/ folder
larva() {
    local ovum="${1:-fo}"
    local root
    root=$(_larva_ovum_root "$ovum") || return 1
    
    if [[ -d "$root/.larva" ]]; then
        cd "$root/.larva"
        echo "[LARVA] $root/.larva"
    else
        echo "[LARVA] .larva/ not found in $root"
        return 1
    fi
}

# Show active LARVAs (tasks) for an OVUM
larva-status() {
    local ovum="${1:-fo}"
    local root
    root=$(_larva_ovum_root "$ovum") || return 1
    local larva_dir="$root/.larva"

    if [[ ! -d "$larva_dir" ]]; then
        echo "[LARVA] No .larva/ in $root"
        return 1
    fi

    echo ""
    echo "=== LARVA STATUS [$ovum] ==="
    echo "Root: $root"
    echo ""

    local found=0
    for manifest in "$larva_dir"/*/LARVA_MANIFEST.ini; do
        [[ -f "$manifest" ]] || continue
        found=1
        local larva_name=$(basename "$(dirname "$manifest")")
        local status=$(grep -oP 'status\s*=\s*\K\w+' "$manifest" 2>/dev/null || echo "?")
        local active_agents=""

        # Collect active agents
        while IFS='=' read -r key value; do
            key=$(echo "$key" | tr -d ' ')
            value=$(echo "$value" | tr -d ' ' | cut -d';' -f1)
            if [[ "$value" == "active" && "$key" != "status" ]]; then
                active_agents="$active_agents @$key"
            fi
        done < <(grep -v '^\[' "$manifest" | grep -v '^;' | grep -v '^$')

        printf "  %-20s  %-10s  %s\n" "$larva_name" "[$status]" "$active_agents"
    done

    if [[ $found -eq 0 ]]; then
        echo "  (no LARVAs found)"
    fi
    echo ""
}

# Quick LARVA init — create folder structure for new LARVA
larva-init() {
    local ovum="${1}"
    local larva_name="${2}"

    if [[ -z "$ovum" || -z "$larva_name" ]]; then
        echo "Usage: larva-init <ovum> <larva_name>"
        echo "Example: larva-init fo order-tags"
        return 1
    fi

    local root
    root=$(_larva_ovum_root "$ovum") || return 1
    local larva_dir="$root/.larva/$larva_name"

    if [[ -d "$larva_dir" ]]; then
        echo "[LARVA] Already exists: $larva_dir"
        return 1
    fi

    mkdir -p "$larva_dir"

    # Copy manifest template
    local template="$root/.larva/_library/_larva_manifest.ini"
    if [[ -f "$template" ]]; then
        sed "s/^name     =.*/name     = $larva_name/" "$template" \
            | sed "s/^ovum     =.*/ovum     = $ovum/" \
            | sed "s/^status   =.*/status   = active/" \
            > "$larva_dir/LARVA_MANIFEST.ini"
    else
        # Inline fallback if template missing
        cat > "$larva_dir/LARVA_MANIFEST.ini" <<INI
[larva]
name     = $larva_name
alias    =
ovum     = $ovum
status   = active          ; active | parked | nympha

[agents]
; active | standby | inactive | done
houston    = standby
trajectory = inactive
eagle      = inactive
vega       = standby
laika      = inactive
voyager    = inactive

[knowledge]
laika_ran  = false
maps       =
INI
    fi

    # Create team_session.md header
    cat > "$larva_dir/team_session.md" <<SESSION
## IDENTITY
LARVA:    $larva_name
OVUM:     [$ovum]
STARTED:  $(date +%Y-%m-%d)

---

## CONTEXT
*What this LARVA is for. Fill in.*

---
SESSION

    echo "[LARVA] Created: $larva_dir"
    echo "  LARVA_MANIFEST.ini — edit agents and alias"
    echo "  team_session.md    — fill CONTEXT section"
    echo ""
    echo "Next: create first INSTAR folder:"
    echo "  mkdir $larva_dir/_first-instar-name"
}

# =============================================================================
# ZSH COMPLETION
# =============================================================================
_larva_completion() {
    local -a commands
    commands=(
        'larva:cd to .larva/ folder'
        'larva-status:show active LARVAs'
        'larva-init:create new LARVA'
        'laika:one-shot codebase scan'
        'consult:interactive zone consultation'
        'broadcast:group consultation (all zones)'
        'slices:regenerate repomix slices'
        'capcom:Claude CLI operational planner'
        'trajectory:Claude CLI executor'
        'athena:Gemini CLI operator'
        'zenit:Gemini CLI (deep research)'
        'horizon:Gemini CLI (fast research)'
    )
    _describe 'command' commands
}

# =============================================================================
# LOAD CONFIRMATION
# =============================================================================
echo "[larva] plugin loaded (@${MACHINE_NAME:-unknown})"
