#!/usr/bin/env bash
# One bounded handoff after the controller turn ends; never a poller or retry.
set -uo pipefail
[[ $# == 3 ]] || { printf 'usage: handoff-once.sh %%2|%%3 POINTER ABS_STATE_DIR\n' >&2; exit 2; }
target=$1 pointer=$2 state_dir=$3
[[ $target == %2 || $target == %3 ]] || exit 2
[[ $state_dir == /* && -n $pointer ]] || exit 2
adapter=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)/bus-poke.sh
printf '%s handoff-scheduled delay=8 target=%s\n' "$(date -u +%FT%TZ)" "$target"
sleep 8
call() {
    local mode=$1 pane=$2 rc
    printf '%s call mode=%s server=default pane=%s state=%s pointer=%s\n' "$(date -u +%FT%TZ)" "$mode" "$pane" "$state_dir" "$pointer"
    bash "$adapter" "$mode" --server default --pane "$pane" --pointer "$pointer" --state-dir "$state_dir"
    rc=$?
    printf '%s result mode=%s pane=%s exit=%s\n' "$(date -u +%FT%TZ)" "$mode" "$pane" "$rc"
    if ((rc == 29)); then
        printf '%s LOCAL-PRIVATE diagnostic pane=%s; original refusal retained\n' "$(date -u +%FT%TZ)" "$pane"
        tmux -L default display-message -p -t "$pane" '#{pane_id}|#{pane_current_command}|#{pane_dead}|#{cursor_x}|#{cursor_y}|#{pane_width}' || :
        tmux -L default capture-pane -e -p -t "$pane" || :
        printf 'END LOCAL-PRIVATE diagnostic; redact before promotion\n'
    fi
    return "$rc"
}
call --check %2 || exit $?
call --check %3 || exit $?
call --send "$target"
