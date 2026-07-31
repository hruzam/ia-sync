#!/usr/bin/env zsh
# =============================================================================
# SESSION TOOLKIT — AI Lifecycle + Agent Registry
# =============================================================================

# =============================================================================
# Agent Registry (loaded from external JSON)
# =============================================================================
# Source: ~/.config/zsh/ai-agents.registry.json
# Edit the JSON to add/modify agents — this script reads it dynamically
typeset -A _AI_AGENT_REGISTRY

_ai_load_registry() {
    local registry="$HOME/.config/zsh/ai-agents.registry.json"
    [[ ! -f "$registry" ]] && return 1

    # Parse CLI agents from JSON using jq
    if command -v jq &>/dev/null; then
        local entries
        entries=$(jq -r '
            [.cli.gemini, .cli.claude, .cli.raw] | add | to_entries[] |
            "\(.key) \(.value.bin)"
        ' "$registry" 2>/dev/null)

        while IFS=' ' read -r name bin; do
            # Expand $HOME in bin path
            bin="${bin//\$HOME/$HOME}"
            _AI_AGENT_REGISTRY[$name]="$bin"
        done <<< "$entries"
    else
        # Fallback: hardcoded if jq unavailable
        _AI_AGENT_REGISTRY=(
            athena "$HOME/.config/gemini/bin/athena"
            horizon "$HOME/.config/gemini/bin/horizon"
            laika "$HOME/.config/gemini/bin/laika"
            orby "$HOME/.config/gemini/bin/orby"
            vega-cli "$HOME/.config/gemini/bin/vega"
            zenit "$HOME/.config/gemini/bin/zenit"
            42 "$HOME/.config/claude/bin/42"
            trajectory "$HOME/.config/claude/bin/trajectory"
            capcom "$HOME/.config/claude/bin/capcom"
            mlok "$HOME/.config/claude/bin/mlok"
            gemini "gemini"
            claude "claude"
        )
    fi
}

_ai_load_registry

# =============================================================================
# Autonomy mode registry (global)
# =============================================================================
_AUTONOMY_REGISTRY="$HOME/.config/zsh/registries/autonomy-mode.json"

_autonomy_mode_get() {
    local mode="safe"
    if [[ -f "$_AUTONOMY_REGISTRY" ]]; then
        if command -v jq &>/dev/null; then
            mode=$(jq -r '.mode // "safe"' "$_AUTONOMY_REGISTRY" 2>/dev/null)
        else
            mode=$(grep -m1 '"mode"' "$_AUTONOMY_REGISTRY" | sed -E 's/.*"mode"[[:space:]]*:[[:space:]]*"([^"]+)".*/\1/')
        fi
    fi
    [[ -z "$mode" ]] && mode="safe"
    echo "$mode"
}

autonomy-mode() {
    local mode="${1:-status}"
    local ts
    ts=$(/usr/bin/date -u +"%Y-%m-%dT%H:%M:%SZ")

    case "$mode" in
        status)
            echo "autonomy-mode: $(_autonomy_mode_get)"
            ;;
        safe|auto)
            cat > "$_AUTONOMY_REGISTRY" <<EOF
{
  "mode": "${mode}",
  "last_changed": "${ts}"
}
EOF
            echo "autonomy-mode set to: ${mode}"
            ;;
        *)
            echo "Usage: autonomy-mode [safe|auto|status]"
            return 1
            ;;
    esac
}

# =============================================================================
# AI Lifecycle Wrapper
# =============================================================================
# Usage: ai-session <agent|command> [args...]
# Example: ai-session athena
# Example: ai-session gemini -m gemini-2.5-pro
ai-session() {
    # Ensure standard PATH is available (including npm global bin)
    [[ ":$PATH:" != *":/usr/bin:"* ]] && export PATH="/usr/bin:$PATH"
    [[ ":$PATH:" != *":$HOME/.npm-global/bin:"* ]] && export PATH="$HOME/.npm-global/bin:$PATH"

    if [[ -z "$1" ]]; then
        echo "Usage: ai-session <agent|command> [args...]"
        echo "Registered agents: ${(k)_AI_AGENT_REGISTRY}"
        return 1
    fi

    local agent_or_cmd="$1"
    shift

    # Resolve agent from registry, or use raw command
    local cmd="${_AI_AGENT_REGISTRY[$agent_or_cmd]:-$agent_or_cmd}"
    local agent_name="$agent_or_cmd"

    # Variables
    # Use normalizer-provided PROJECT_SES_PATH if available, fallback to home default
    local journal_path="${PROJECT_SES_PATH:-$HOME/www/larva_dev/dev}/dev.journal.jsonl"
    local autonomy_mode=$(_autonomy_mode_get)
    local session_id=$(/usr/bin/uuidgen 2>/dev/null || cat /proc/sys/kernel/random/uuid 2>/dev/null | cut -c1-8 || echo "$$-$RANDOM")
    [[ ${#session_id} -gt 8 ]] && session_id=${session_id:0:8}
    local timestamp=$(/usr/bin/date -u +"%Y-%m-%dT%H:%M:%SZ")
    local host_name="${MACHINE_NAME:-unknown}"

    # Determine T1 path and model based on agent type
    local t1_path=""
    local model="default"
    if [[ "$cmd" == *"gemini"* ]] || [[ -n "${_AI_AGENT_REGISTRY[$agent_or_cmd]}" && "$cmd" == *".config/gemini"* ]]; then
        t1_path="$HOME/.gemini/tmp/hruzam/chats/session-${timestamp}-${session_id}.jsonl"
        model="gemini-2.5-flash"
    elif [[ "$cmd" == *"claude"* ]]; then
        t1_path="$HOME/.claude/projects/default/${session_id}.jsonl"
        model="claude-sonnet-4-5"
    else
        t1_path="/unknown/path/${session_id}.jsonl"
    fi

    # Optional: Create T2 session digest (opt-in via CREATE_T2_DIGEST=1)
    local t2_file=""
    local t2_folder=""
    if [[ -n "$CREATE_T2_DIGEST" ]]; then
        local session_base="${PROJECT_SES_PATH:-$HOME/www/larva_dev/dev}/session"
        local session_scope="${SESSION_SCOPE:-}"

        # If no scope and interactive, ask user
        if [[ -z "$session_scope" && -t 0 ]]; then
            echo -n "[Lifecycle] Session name (or ENTER for auto): "
            read session_scope
        fi

        # Build filename per naming convention (skill.naming-convention.md)
        if [[ -n "$session_scope" ]]; then
            t2_file="session.${session_scope}.${session_id}.md"
            t2_folder="${session_base}/${session_scope}"
        else
            t2_file="session.${session_id}.md"
            t2_folder="${session_base}/session-${session_id}"
        fi

        # Create T2 file with frontmatter
        /usr/bin/mkdir -p "$t2_folder"
        cat > "${t2_folder}/${t2_file}" <<EOF
---
session_id: ${session_id}
scope: ${session_scope:-auto}
agent: ${agent_name}
model: ${model}
host: ${host_name}
who: ${USER:-majkee}
started_at: ${timestamp}
t1_path: ${t1_path}
---

# Session: ${session_scope:-session-${session_id}}

## Work Log

EOF

        echo "[Lifecycle] T2 digest: ${t2_folder}/${t2_file}"
    fi

    # 1. Log Start Event (T3)
    /usr/bin/mkdir -p "${journal_path:h}"
    [[ ! -f "$journal_path" ]] && /usr/bin/touch "$journal_path"

    # Build T3 event (include T2 ref if digest was created)
    local t3_event="{\"ts\":\"${timestamp}\",\"evt\":\"auto:session_start\",\"who\":\"auto\",\"host\":\"${host_name}\",\"agent\":\"${agent_name}\",\"model\":\"${model}\",\"path\":\"${t1_path}\",\"autonomy_mode\":\"${autonomy_mode}\""
    if [[ -n "$t2_file" && -n "$t2_folder" ]]; then
        t3_event="${t3_event},\"ref\":\"${t2_folder}/${t2_file}\""
    fi
    t3_event="${t3_event}}"

    echo "$t3_event" >> "$journal_path"
    echo "[Lifecycle] Session started: ${agent_name} (${session_id})"

    # 2. Execute Command
    $cmd "$@"
    local exit_code=$?

    # 3. Log End Event
    local end_timestamp=$(/usr/bin/date -u +"%Y-%m-%dT%H:%M:%SZ")

    # Append to T2 digest if it was created
    if [[ -n "$t2_file" && -n "$t2_folder" && -f "${t2_folder}/${t2_file}" ]]; then
        cat >> "${t2_folder}/${t2_file}" <<EOF

---

## Session End

**Ended:** ${end_timestamp}
**Exit code:** ${exit_code}
**Duration:** Started ${timestamp}

EOF
        echo "[Lifecycle] T2 updated: ${t2_folder}/${t2_file}"
    fi

    # Log to T3
    local t3_end_event="{\"ts\":\"${end_timestamp}\",\"evt\":\"auto:session_end\",\"who\":\"auto\",\"host\":\"${host_name}\",\"agent\":\"${agent_name}\",\"model\":\"${model}\",\"path\":\"${t1_path}\",\"synthesis\":\"Process exited with code ${exit_code}\""
    if [[ -n "$t2_file" && -n "$t2_folder" ]]; then
        t3_end_event="${t3_end_event},\"ref\":\"${t2_folder}/${t2_file}\""
    fi
    t3_end_event="${t3_end_event}}"

    echo "$t3_end_event" >> "$journal_path"
    echo "[Lifecycle] Session ended: ${agent_name} (${session_id})"

    return $exit_code
}

# =============================================================================
# Agent Aliases (generated from registry)
# =============================================================================
# Default: direct invocation (no tracking)
# Tracked: use `track <agent>` prefix
#
# Examples:
#   athena "quick question"        → not tracked
#   track athena "review this"     → tracked to journal

_ai_create_aliases() {
    for agent bin in ${(kv)_AI_AGENT_REGISTRY}; do
        # Skip raw CLI entries and invalid names
        [[ "$agent" == "gemini" || "$agent" == "claude" ]] && continue
        alias "$agent"="$bin"
    done
}

_ai_create_aliases

# =============================================================================
# Concurrency Guard + Nesting Detection
# =============================================================================
# Source: ~/.shared/implementation.concurrency-guard.zsh
# Prevents >3 concurrent agents (freeze risk) and agent-in-agent loops
source "$HOME/.shared/implementation.concurrency-guard.zsh"

# Tracking wrapper with allowed-params validation
TRACK_PARAMS_REGISTRY="${TRACK_PARAMS_REGISTRY:-/home/hruzam/www/larva_dev/dev/.config/registries.track-params.json}"

_track_allowed_params() {
    if [[ -f "$TRACK_PARAMS_REGISTRY" ]]; then
        if command -v jq &>/dev/null; then
            jq -r '.allowed_params[]?' "$TRACK_PARAMS_REGISTRY" 2>/dev/null
            return 0
        fi
    fi
    return 1
}

unalias track 2>/dev/null
track() {
    local args=("$@")
    local allowed_params=()
    local extra_params=()
    local agent=""
    local prompt_parts=()
    local session_mode=""

    while IFS= read -r p; do
        [[ -n "$p" ]] && allowed_params+=("$p")
    done < <(_track_allowed_params || true)

    local i=1
    while [[ $i -le ${#args[@]} ]]; do
        local token="${args[$i]}"
        local next_index=$((i + 1))

        if [[ "$token" == --* ]]; then
            if (( ${#allowed_params[@]} > 0 )) && [[ ! " ${allowed_params[*]} " =~ " ${token} " ]]; then
                echo "[track] ⛔ Param not allowed: $token"
                echo "[track] Allowed: ${allowed_params[*]}"
                return 1
            fi
            local val="${args[$next_index]}"
            if [[ -z "$val" || "$val" == --* ]]; then
                echo "[track] ⛔ Missing value for $token"
                return 1
            fi
            if [[ "$token" == "--mode" ]]; then
                session_mode="$val"
            else
                extra_params+=("$token" "$val")
            fi
            i=$((i + 2))
            continue
        fi

        if [[ -z "$agent" ]]; then
            agent="$token"
        else
            prompt_parts+=("$token")
        fi
        i=$((i + 1))
    done

    if [[ -z "$agent" ]]; then
        echo "Usage: track [--param value...] <agent> \"prompt\""
        return 1
    fi

    local prompt="${(j: :)prompt_parts}"
    if [[ -z "$prompt" ]]; then
        AI_SESSION_MODE="$session_mode" ai-session-nested-safe "$agent" "${extra_params[@]}"
    else
        AI_SESSION_MODE="$session_mode" ai-session-nested-safe "$agent" "${extra_params[@]}" "$prompt"
    fi
}

# =============================================================================
# Helper: List registered agents
# =============================================================================
ai-agents() {
    echo "Registered AI agents (all route through ai-session lifecycle):"
    for agent path in ${(kv)_AI_AGENT_REGISTRY}; do
        echo "  $agent -> $path"
    done
}

# =============================================================================
# Task Registry
# =============================================================================
alias tasks='node ~/.config/zsh/registries/tasks.js'
