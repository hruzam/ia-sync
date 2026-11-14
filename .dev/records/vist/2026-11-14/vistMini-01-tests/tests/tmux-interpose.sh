#!/usr/bin/env bash
# External deterministic interposition for race cases. Not sourced by adapter.
set -u
[[ -z ${VIST_CALL_LOG:-} ]] || printf '%s\n' "$*" >> "$VIST_CALL_LOG"
case ${VIST_INTERPOSE_MODE:-none} in
    metadata-once|metadata-always)
        if [[ " $* " == *' display-message '* && $* == *'#{pane_width}'* ]]; then
            count=0
            [[ ! -f $VIST_CONTROL/meta-count ]] || read -r count < "$VIST_CONTROL/meta-count"
            count=$((count+1)); printf '%s\n' "$count" > "$VIST_CONTROL/meta-count"
            value=$("$VIST_REAL_TMUX" "$@") || exit $?
            if ((count % 2 == 0)) && { [[ $VIST_INTERPOSE_MODE == metadata-always ]] || ((count == 2)); }; then
                printf '%s|fixture-metadata-change\n' "$value"
            else
                printf '%s\n' "$value"
            fi
            exit 0
        fi;;
    busy-after-text)
        if [[ " $* " == *' send-keys '* && " $* " == *' -l '* ]]; then
            "$VIST_REAL_TMUX" "$@" || exit $?
            : > "$VIST_CONTROL/busy-now"
            for ((i=0; i<100; i++)); do
                screen=$("$VIST_REAL_TMUX" -L vist-test capture-pane -p -t "$VIST_PANE")
                [[ $screen == *'esc to interrupt'* ]] && exit 0
                sleep 0.025
            done
            exit 1
        fi;;
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
