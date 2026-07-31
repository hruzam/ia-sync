#!/usr/bin/env zsh
# =============================================================================
# SHARED TOOLKIT - Mirror manager for ~/www/session hidden folders
# =============================================================================
# Location: ~/.config/zsh/shared-toolkit.zsh
# Loaded by: ~/.zshrc
#   [[ -f ~/.config/zsh/shared-toolkit.zsh ]] && source ~/.config/zsh/shared-toolkit.zsh
# =============================================================================
# PAIRS:
#   shared  ->  .shared  (src)  /  shared  (dst)
#   majkee  ->  .majkee  (src)  /  majkee  (dst)
#
# USAGE:
#   shpub shared      publish .shared -> shared
#   shpub majkee      publish .majkee -> majkee
#   shdiff shared     dry run for shared pair
#   shstat            show state of all pairs
#   shsyntax          print active.md from shared mirror
# =============================================================================

# =============================================================================
# PAIR REGISTRY (from config.zsh — must be sourced before this file)
# =============================================================================
# Pairs are resolved at call time from these env vars:
#   SESSION_SHARED_SRC / SESSION_SHARED_DST
#   SESSION_MAJKEE_SRC / SESSION_MAJKEE_DST
# =============================================================================

# =============================================================================
# INTERNAL: resolve pair -> SRC DST
# Sets _SHPAIR_SRC and _SHPAIR_DST in caller scope
# =============================================================================
_sh_resolve_pair() {
    local pair="$1"

    case "$pair" in
        shared)
            _SHPAIR_SRC="$SESSION_SHARED_SRC"
            _SHPAIR_DST="$SESSION_SHARED_DST"
            ;;
        majkee)
            _SHPAIR_SRC="$SESSION_MAJKEE_SRC"
            _SHPAIR_DST="$SESSION_MAJKEE_DST"
            ;;
        *)
            echo "[ERROR] Unknown pair: '$pair'"
            echo "        Available: shared, majkee"
            return 1
            ;;
    esac
}

# =============================================================================
# shpub <pair> - publish .<pair>/ to <pair>/ (one-way rsync)
# =============================================================================
shpub() {
    local pair="${1:-}"

    if [[ -z "$pair" ]]; then
        echo "[ERROR] Usage: shpub <pair>   (shared | majkee)"
        return 1
    fi

    _sh_resolve_pair "$pair" || return 1

    if [[ ! -d "$_SHPAIR_SRC" ]]; then
        echo "[ERROR] source not found: $_SHPAIR_SRC"
        return 1
    fi

    mkdir -p "$_SHPAIR_DST"

    echo "[*] Publishing $_SHPAIR_SRC -> $_SHPAIR_DST"

    rsync -av --delete \
        --exclude='.git' \
        --exclude='.DS_Store' \
        "$_SHPAIR_SRC/" \
        "$_SHPAIR_DST/"

    # Sentinel — restored after rsync --delete
    cat > "$_SHPAIR_DST/.DO_NOT_EDIT_HERE" << EOF
This is a generated mirror of $_SHPAIR_SRC

DO NOT EDIT FILES HERE. They will be overwritten on the next \`shpub $pair\`.

To make changes, edit the source:
    $_SHPAIR_SRC/<file>

Then re-publish:
    shpub $pair
EOF

    echo "[OK] Mirror published. Sentinel restored."
}

# =============================================================================
# shdiff <pair> - dry run, show what shpub would change
# =============================================================================
shdiff() {
    local pair="${1:-}"

    if [[ -z "$pair" ]]; then
        echo "[ERROR] Usage: shdiff <pair>   (shared | majkee)"
        return 1
    fi

    _sh_resolve_pair "$pair" || return 1

    if [[ ! -d "$_SHPAIR_SRC" ]]; then
        echo "[ERROR] source not found: $_SHPAIR_SRC"
        return 1
    fi

    mkdir -p "$_SHPAIR_DST"

    echo "[*] Dry run: $_SHPAIR_SRC -> $_SHPAIR_DST"
    rsync -av --delete --dry-run \
        --exclude='.git' \
        --exclude='.DS_Store' \
        "$_SHPAIR_SRC/" \
        "$_SHPAIR_DST/"
}

# =============================================================================
# shstat - show source/mirror state for all pairs
# =============================================================================
shstat() {
    local pairs=(shared majkee)

    for pair in "${pairs[@]}"; do
        _sh_resolve_pair "$pair" || continue

        echo "=== pair: $pair ==="
        echo "[SRC] $_SHPAIR_SRC"
        if [[ -d "$_SHPAIR_SRC" ]]; then
            echo "      $(find "$_SHPAIR_SRC" -type f | wc -l) files"
            echo "      latest: $(find "$_SHPAIR_SRC" -type f -printf '%T@ %p\n' 2>/dev/null | sort -nr | head -n1 | cut -d' ' -f2-)"
        else
            echo "      [!] does not exist"
        fi
        echo "[DST] $_SHPAIR_DST"
        if [[ -d "$_SHPAIR_DST" ]]; then
            echo "      $(find "$_SHPAIR_DST" -type f | wc -l) files"
            echo "      latest: $(find "$_SHPAIR_DST" -type f -printf '%T@ %p\n' 2>/dev/null | sort -nr | head -n1 | cut -d' ' -f2-)"
        else
            echo "      [!] does not exist (run: shpub $pair)"
        fi
        echo ""
    done
}

# =============================================================================
# shsyntax - print active syntax pointer from shared mirror
# =============================================================================
shsyntax() {
    local active="$SESSION_SHARED_DST/syntax/active.md"
    if [[ -f "$active" ]]; then
        cat "$active"
    else
        echo "[!] $active not found. Did you run: shpub shared?"
    fi
}

# =============================================================================
# COMPLETION
# =============================================================================
_shared_completion() {
    local -a commands
    commands=(
        'shpub:Publish .<pair> -> <pair> (one-way rsync)'
        'shdiff:Dry run — show changes shpub would make'
        'shstat:Show source/mirror state for all pairs'
        'shsyntax:Print active syntax pointer (shared pair)'
    )
    _describe 'command' commands
}

echo "[toolkit] shared loaded — commands: shpub, shdiff, shstat, shsyntax"