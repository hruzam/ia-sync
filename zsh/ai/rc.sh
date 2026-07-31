#!/usr/bin/env bash

# rc.sh — Claude Code Remote Control launcher (Approach B: tmux on-demand)
# Reads project registry from ai.json; starts or attaches tmux sessions running
# `claude remote-control`. Does not require systemd — sessions are on-demand.
#
# Usage:
#   rc.sh                   list all projects and their tmux/RC status
#   rc.sh status            same as bare call
#   rc.sh <project>         start or attach RC session for project
#   rc.sh <project> stop    stop tmux RC session for project

REGISTRY="${HOME}/.config/zsh/registries/ai.json"

_check_jq() {
    if ! command -v jq &>/dev/null; then
        echo "Error: jq not found. Install jq to use rc.sh." >&2
        exit 1
    fi
}

_check_registry() {
    if [[ ! -f "${REGISTRY}" ]]; then
        echo "Error: registry not found at ${REGISTRY}" >&2
        exit 1
    fi
    if ! jq -e '.["remote-control"].projects' "${REGISTRY}" &>/dev/null; then
        echo "Error: no remote-control.projects key in ${REGISTRY}" >&2
        exit 1
    fi
}

_list_status() {
    _check_jq
    _check_registry

    printf "%-15s %-12s %-20s %-10s %-10s\n" "PROJECT" "NAME" "TMUX SESSION" "RUNNING" "AVAILABLE"
    printf "%-15s %-12s %-20s %-10s %-10s\n" "-------" "----" "------------" "-------" "---------"

    while IFS= read -r key; do
        local name session available running
        name=$(jq -r ".\"remote-control\".projects.\"${key}\".rc_name" "${REGISTRY}")
        session=$(jq -r ".\"remote-control\".projects.\"${key}\".tmux_session" "${REGISTRY}")
        available=$(jq -r ".\"remote-control\".projects.\"${key}\".available" "${REGISTRY}")

        if tmux has-session -t "${session}" 2>/dev/null; then
            running="yes"
        else
            running="no"
        fi

        printf "%-15s %-12s %-20s %-10s %-10s\n" "${key}" "${name}" "${session}" "${running}" "${available}"
    done < <(jq -r '.["remote-control"].projects | keys[]' "${REGISTRY}")
}

_start_or_attach() {
    local project="$1"
    _check_jq
    _check_registry

    local exists
    exists=$(jq -r ".\"remote-control\".projects.\"${project}\"" "${REGISTRY}")
    if [[ "${exists}" == "null" ]]; then
        echo "Error: project '${project}' not found in registry" >&2
        echo "Known projects: $(jq -r '.["remote-control"].projects | keys | join(", ")' "${REGISTRY}")" >&2
        exit 1
    fi

    local name path session available
    name=$(jq -r ".\"remote-control\".projects.\"${project}\".rc_name" "${REGISTRY}")
    path=$(jq -r ".\"remote-control\".projects.\"${project}\".path" "${REGISTRY}")
    session=$(jq -r ".\"remote-control\".projects.\"${project}\".tmux_session" "${REGISTRY}")
    available=$(jq -r ".\"remote-control\".projects.\"${project}\".available" "${REGISTRY}")

    if [[ "${available}" != "true" ]]; then
        echo "Project ${name} not available on this machine" >&2
        exit 1
    fi

    if tmux has-session -t "${session}" 2>/dev/null; then
        echo "Attaching to existing session: ${session}"
        tmux attach-session -t "${session}"
    else
        echo "Starting new RC session for ${name} in ${path}"
        tmux new-session -d -s "${session}" -c "${path}" "claude remote-control --name '${name}'"
        tmux attach-session -t "${session}"
    fi
}

_stop_session() {
    local project="$1"
    _check_jq
    _check_registry

    local exists
    exists=$(jq -r ".\"remote-control\".projects.\"${project}\"" "${REGISTRY}")
    if [[ "${exists}" == "null" ]]; then
        echo "Error: project '${project}' not found in registry" >&2
        exit 1
    fi

    local name session
    name=$(jq -r ".\"remote-control\".projects.\"${project}\".rc_name" "${REGISTRY}")
    session=$(jq -r ".\"remote-control\".projects.\"${project}\".tmux_session" "${REGISTRY}")

    if tmux has-session -t "${session}" 2>/dev/null; then
        tmux kill-session -t "${session}"
        echo "Stopped session: ${session} (${name})"
    else
        echo "Session not running: ${session} (${name})"
    fi
}

# ---- main ----

case "${1:-}" in
    ""|"status")
        _list_status
        ;;
    *)
        project="$1"
        action="${2:-}"
        case "${action}" in
            "stop")
                _stop_session "${project}"
                ;;
            "")
                _start_or_attach "${project}"
                ;;
            *)
                echo "Error: unknown action '${action}'. Usage: rc.sh <project> [stop]" >&2
                exit 1
                ;;
        esac
        ;;
esac
