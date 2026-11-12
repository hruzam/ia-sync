#!/usr/bin/env bash
# External deterministic interposition for race cases. Not sourced by adapter.
set -u
[[ -z ${VIST_CALL_LOG:-} ]] || printf '%s\n' "$*" >> "$VIST_CALL_LOG"
case ${VIST_INTERPOSE_MODE:-none} in
    exit-before-enter)
        if [[ " $* " == *' send-keys '* && " $* " == *' -l '* ]]; then
            "$VIST_REAL_TMUX" "$@" || exit $?
            : > "$VIST_CONTROL/exit-now"
            for ((i=0; i<100; i++)); do
                dead=$("$VIST_REAL_TMUX" -L vist-test display-message -p -t "$VIST_PANE" '#{pane_dead}')
                [[ $dead == 1 ]] && exit 0
                sleep 0.025
            done
            exit 1
        fi ;;
    crash-after-reserve)
        if [[ " $* " == *' send-keys '* && " $* " == *' -l '* ]]; then
            : > "$VIST_CONTROL/crash-observed"
            kill -KILL "$PPID"
            exit 1
        fi ;;
esac
exec "$VIST_REAL_TMUX" "$@"
