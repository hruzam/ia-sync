#!/usr/bin/env zsh
# =============================================================================
# GIT LIFECYCLE TOOLKIT - UTF-8 Status Mapping
# =============================================================================

# Add this to ~/.config/zsh/git-lifecycle.zsh

# Phase Symbols
export G_ALPHA="🧪"
export G_BETA="🔨"
export G_RC="🚥"
export G_PROD="🚀"
export G_WIP="🏗️"
export G_FIX="🐛"
export G_REF="♻️"

# The "Smart Commit" Engine
# Usage: smart_commit "alpha" "Initial refactor"
smart_commit() {
    local phase="$1"
    local msg="$2"
    local symbol=""

    case "$phase" in
        alpha) symbol="$G_ALPHA [ALPHA]" ;;
        beta)  symbol="$G_BETA [BETA]" ;;
        rc)    symbol="$G_RC [RC]" ;;
        prod)  symbol="$G_PROD [PROD]" ;;
        wip)   symbol="$G_WIP [WIP]" ;;
        ref)   symbol="$G_REF [REF]" ;;
        *)     symbol="✨" ;; 
    esac
    
    git commit -m "$symbol $msg"
}

# The Help Menu to be shared across toolkits
_git_lifecycle_help() {
    cat << 'EOF'
+------------------------------------------------------------------+
|            GIT LIFECYCLE SYMBOLS (for -gc)                      |
+------------------------------------------------------------------+
|  alpha     🧪 [ALPHA] Experimental / Internal testing            |
|  beta      🔨 [BETA]  Hardening / Polish / Bugs                  |
|  rc        🚥 [RC]    Release Candidate / Final Tests            |
|  prod      🚀 [PROD]  Production Deployment                      |
|  ref       ♻️ [REF]   @codingStandards Refactoring               |
|  wip       🏗️ [WIP]   Work in Progress                           |
+------------------------------------------------------------------+
EOF
}

# Lifecycle Tables for terminal reference
git_phases() {
    echo "--- Project Lifecycle Symbols ---"
    echo "$G_ALPHA  alpha : Initial Testing"
    echo "$G_BETA  beta  : Hardening/Polish"
    echo "$G_RC  rc    : Release Candidate"
    echo "$G_PROD  prod  : Production Launch"
    echo "$G_REF  ref   : @codingStandards Refactor"
    echo "---------------------------------"
    echo "Usage: gcm <phase> \"your message\""
}