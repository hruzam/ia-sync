#!/usr/bin/env zsh
# Explicit per-shell vault attachment. Python receives explicit selectors only.
# Law: zsh/AGENTS.md, Control-panel convention.

_jev() {
    local jev_arg jev_command
    local -i jev_index=1 jev_help=0
    local -a jev_selectors
    if (( $# == 0 )); then
        python3 -B "${_JEV_SOURCE_DIR}/jev.py" --help
        return $?
    fi
    for jev_arg in "$@"; do
        [[ "$jev_arg" == --help || "$jev_arg" == -h ]] && jev_help=1
        if [[ "$jev_arg" == --root || "$jev_arg" == --root=* ||
              "$jev_arg" == --session || "$jev_arg" == --session=* ||
              "$jev_arg" == --channel || "$jev_arg" == --channel=* ]]; then
            if [[ -n ${JEV_SESSION:-} || -n ${JEV_CHANNEL:-} ]]; then
                print -u2 -- 'jev: attached shell; use jev-off before explicit selector overrides'
                return 2
            fi
            python3 -B "${_JEV_SOURCE_DIR}/jev.py" "$@"
            return $?
        fi
    done
    # Origin options are globals too. Find the command without mistaking their values
    # for a selected operation; Python remains the authority for argument validation.
    while (( jev_index <= $# )); do
        jev_arg="${argv[jev_index]}"
        case "$jev_arg" in
            --cli|--cli-session|--requester) (( jev_index += 2 )) ;;
            --cli=*|--cli-session=*|--requester=*) (( jev_index += 1 )) ;;
            *) jev_command="$jev_arg"; break ;;
        esac
    done
    if [[ -n "$jev_command" && "$jev_command" != open ]] && (( ! jev_help )); then
        if [[ -z ${JEV_SESSION:-} || -z ${JEV_CHANNEL:-} ]]; then
            print -u2 -- 'jev: select a vault with jev-use ROOT SESSION [main], or pass explicit selectors'
            return 2
        fi
        jev_selectors=(--session "$JEV_SESSION" --channel "$JEV_CHANNEL")
    fi
    python3 -B "${_JEV_SOURCE_DIR}/jev.py" --root "${JEV_ROOT:-$HOME/.jev}" "${jev_selectors[@]}" "$@"
}

_jev_use() {
    if (( $# < 2 || $# > 3 )); then
        print -u2 -- 'usage: jev-use ROOT SESSION [main]'
        return 2
    fi
    local jev_root="${1:a}" jev_session="$2" jev_channel="${3:-main}"
    python3 -B "${_JEV_SOURCE_DIR}/jev.py" --root "$jev_root" \
        --session "$jev_session" --channel "$jev_channel" settings || return $?
    export JEV_ROOT="$jev_root" JEV_SESSION="$jev_session" JEV_CHANNEL="$jev_channel"
}

_jev_off() {
    if (( $# != 0 )); then
        print -u2 -- 'usage: jev-off'
        return 2
    fi
    unset JEV_ROOT JEV_SESSION JEV_CHANNEL
}
