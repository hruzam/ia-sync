#!/usr/bin/env zsh
# =============================================================================
# IMPLEMENTATION: Concurrency Guard for Multi-Agent Work
# =============================================================================
# Purpose: Prevent >2 concurrent Gemini agents from exhausting RAM
# Source: handoff.gemini-freeze-multiagent-2026-05-18.md
# Status: Ready to integrate into ~/.config/zsh/ai-lifecycle.zsh
# =============================================================================

# =============================================================================
# Configuration
# =============================================================================
# Aligned with earlyoom threshold (see ~/www/my-env-sync/guides/machine.resource-control.home.md)
AI_GUARD_RAM_PERCENT_MIN=${AI_GUARD_RAM_PERCENT_MIN:-7}   # Block if free RAM < 7% of total
AI_GUARD_MAX_AGENTS=${AI_GUARD_MAX_AGENTS:-3}             # Max concurrent agents

# Guarded session launcher - checks RAM and active agent count before spawn
ai-session-guarded() {
    # Count active Gemini CLI processes (exclude grep and this script)
    local active_agents=$(ps aux | grep -E "gemini.*-[mi]" | grep -v grep | wc -l)

    # Get RAM stats (use absolute path to avoid alias conflict)
    local total_kb=$(/usr/bin/free | awk '/^Mem:/ {print $2}')
    local avail_kb=$(/usr/bin/free | awk '/^Mem:/ {print $7}')
    local avail_percent=$((avail_kb * 100 / total_kb))
    local avail_gb=$((avail_kb / 1024 / 1024))

    # Guard 1: Max concurrent agents
    if [[ $active_agents -ge $AI_GUARD_MAX_AGENTS ]]; then
        echo "[Guard] ⛔ Max $AI_GUARD_MAX_AGENTS agents already running."
        echo "[Guard] Active: $(ps aux | grep -E 'gemini.*-[mi]' | grep -v grep | awk '{print $NF}' | head -$AI_GUARD_MAX_AGENTS)"
        echo "[Guard] Wait for one to finish or kill it."
        return 1
    fi

    # Guard 2: Minimum RAM threshold (percentage-based, aligned with earlyoom)
    if [[ $avail_percent -lt $AI_GUARD_RAM_PERCENT_MIN ]]; then
        echo "[Guard] ⛔ RAM below ${AI_GUARD_RAM_PERCENT_MIN}% threshold (current: ${avail_percent}% free, ${avail_gb}GB)."
        echo "[Guard] Clear memory first or close other applications."
        ramwatch --suspects 2>/dev/null || echo "[Guard] Tip: run 'ramwatch --suspects' to see memory hogs"
        return 1
    fi

    # All checks passed - proceed with normal ai-session
    echo "[Guard] ✅ Checks passed (agents: $active_agents/$AI_GUARD_MAX_AGENTS, RAM: ${avail_percent}% free ~${avail_gb}GB)"
    ai-session "$@"
}

# Nesting detection - prevents agent-in-agent loops
ai-session-nested-safe() {
    # Check if we're already inside an agent session
    local parent_comm=""
    parent_comm=$(ps -p "$PPID" -o comm= 2>/dev/null)
    local parent_is_agent=0
    if [[ "$parent_comm" == *gemini* ]] || [[ "$parent_comm" == *claude* ]]; then
        parent_is_agent=1
    fi

    if (( parent_is_agent )); then
        echo "[Lifecycle] ⚠️  Nested session detected."
        echo "[Lifecycle] Running direct (no tracking) to avoid I/O loop."

        # Resolve agent command from registry
        local agent_or_cmd="$1"
        shift
        local cmd="${_AI_AGENT_REGISTRY[$agent_or_cmd]:-$agent_or_cmd}"

        # Execute directly without wrapper (avoid replacing the shell)
        $cmd "$@"
        return $?
    fi

    # Not nested - set flag and proceed normally
    export AI_SESSION_ACTIVE=1
    ai-session-guarded "$@"
    local exit_code=$?
    unset AI_SESSION_ACTIVE
    return $exit_code
}

# =============================================================================
# INTEGRATION INSTRUCTIONS
# =============================================================================
# 1. Source this file from ~/.config/zsh/ai-lifecycle.zsh:
#    source "$HOME/.shared/implementation.concurrency-guard.zsh"
#
# 2. Update the 'track' alias:
#    alias track='ai-session-nested-safe'
#
# 3. Test the guard:
#    track athena "test 1" &
#    track zenit "test 2" &
#    track horizon "test 3"  # Should block with guard message
#
# 4. Test nesting detection:
#    # From inside Claude Code terminal:
#    track athena "nested test"  # Should run direct (no tracking)
# =============================================================================

# =============================================================================
# OPTIONAL: Status command to see active agents
# =============================================================================
ai-agents-status() {
    echo "=== Active AI Agents ==="
    local active=$(ps aux | grep -E "gemini.*-[mi]|claude.*--agent" | grep -v grep)
    if [[ -z "$active" ]]; then
        echo "No agents currently running."
    else
        echo "$active" | awk '{printf "%-10s %6s %5s  %s\n", $1, $2, $4"%", substr($0, index($0,$11))}'
    fi
    echo ""
    echo "=== RAM Status ==="
    free -h | grep "^Mem:"
    echo ""
    echo "Capacity: 2 agents max (measured: ~1.9GB per agent)"
}

alias agents-status='ai-agents-status'
