#!/usr/bin/env bash
# Cycle 01 only: a contracted stand-in receiver on the isolated vist-test server.
# This is a notification attempt, not a consumption stamp or live-TUI adapter.
set -uo pipefail
export LC_ALL=C

fail() { printf '%s refused code=%s %s\n' "$(date -u +%FT%TZ)" "$1" "$2" >&2; exit "$1"; }
mode= server= pane= pointer= state_dir=
while (($#)); do
    case $1 in
        --check|--send) [[ -z $mode ]] || fail 2 'choose one mode'; mode=$1; shift ;;
        --server|--pane|--pointer|--state-dir)
            (($# >= 2)) || fail 2 "missing value for $1"
            case $1 in
                --server) server=$2;; --pane) pane=$2;;
                --pointer) pointer=$2;; --state-dir) state_dir=$2;;
            esac
            shift 2 ;;
        *) fail 2 'usage: --check|--send --server vist-test --pane %N --pointer LINE --state-dir ABS';;
    esac
done
[[ -n $mode && -n $pointer && $server == vist-test && $pane =~ ^%[0-9]+$ && $state_dir == /* ]] || fail 2 'explicit isolated server, pane id, mode, pointer and absolute state path required'
# Deliberately bounded grammar; it cannot express a shell-expansion payload.
pattern='^\[bus ([A-Za-z0-9][A-Za-z0-9._:-]*)\] from [A-Za-z0-9._-]+:[A-Za-z0-9._/-]+ -> (git pull, )?read [A-Za-z0-9_./~-]+ ; ack: (none|stamp|reply)$'
[[ ${#pointer} -le 200 && $pointer =~ $pattern ]] || fail 30 'invalid pointer: one ASCII line, <=200 chars, bounded bus/read grammar'
msg=${BASH_REMATCH[1]}
key=$(printf '%s\n%s\n%s\n' "$server" "$pane" "$msg" | sha256sum) || fail 28 'cannot hash attempt key'
claim=$state_dir/${key%% *}
[[ ! -e $claim ]] || fail 25 'duplicate or uncertain prior attempt; inspect receipt before recovery'

identity= last_line= cursor_x= cursor_y=
snapshot() {
    local info id pid dead command argv0 stat rest screen line
    local -a fields
    info=$(tmux -L "$server" display-message -p -t "$pane" '#{pane_id}|#{pane_pid}|#{pane_dead}|#{pane_current_command}|#{cursor_x}|#{cursor_y}' 2>/dev/null) || return 20
    IFS='|' read -r id pid dead command cursor_x cursor_y <<< "$info"
    [[ $id == "$pane" && $pid =~ ^[0-9]+$ ]] || return 20
    [[ $dead == 0 ]] || return 21
    [[ $command == codex || $command == claude ]] || return 22
    IFS= read -r -d '' argv0 < "/proc/$pid/cmdline" 2>/dev/null || return 26
    argv0=${argv0##*/}
    [[ $argv0 == "$command" ]] || return 26
    # PID plus Linux process start time prevents a stale PID snapshot from matching.
    stat=$(cat "/proc/$pid/stat" 2>/dev/null) || return 26
    rest=${stat##*) }
    read -r -a fields <<< "$rest"
    [[ ${fields[19]:-} =~ ^[0-9]+$ ]] || return 26
    identity=$pid:${fields[19]}
    screen=$(tmux -L "$server" capture-pane -p -t "$pane" 2>/dev/null) || return 20
    [[ $screen != *'esc to interrupt'* ]] || return 24
    last_line=
    while IFS= read -r line; do
        # tmux can retain spaces to the pane width. Strip only trailing ASCII spaces.
        while [[ $line == *' ' ]]; do line=${line% }; done
        [[ -z $line ]] || last_line=$line
    done <<< "$screen"
    return 0
}
snapshot; rc=$?
((rc == 0)) || fail "$rc" 'unknown/dead/non-agent/unsafe/busy receiver'
initial_identity=$identity
if [[ $last_line != '❯' || $cursor_x != 2 || $cursor_y != 0 ]]; then
    [[ $last_line == '❯' ]] && fail 23 'nonempty/unknown cursor position in composer'
    [[ $last_line == '❯ '* ]] && fail 23 'occupied composer'
    fail 29 'unrecognized composer state'
fi
if [[ $mode == --check ]]; then
    printf '%s check=ready server=%s pane=%s attempt=none\n' "$(date -u +%FT%TZ)" "$server" "$pane"
    exit 0
fi
mkdir -p -- "$state_dir" 2>/dev/null || fail 28 'cannot create attempt state directory'
mkdir -- "$claim" 2>/dev/null || {
    [[ -e $claim ]] && fail 25 'concurrent or previous attempt'
    fail 28 'cannot reserve attempt'
}
printf 'phase=reserved msg=%s server=%s pane=%s utc=%s\n' "$msg" "$server" "$pane" "$(date -u +%FT%TZ)" > "$claim/state" || fail 28 'cannot persist reservation'
# Reservations deliberately survive failure/signals: uncertain does not mean retryable.
trap 'exit 28' INT TERM
tmux -L "$server" send-keys -t "$pane" -l "$pointer" || fail 28 'text injection failed; attempt uncertain'
printf 'phase=text-attempted msg=%s utc=%s\n' "$msg" "$(date -u +%FT%TZ)" > "$claim/state" || fail 28 'cannot persist text attempt'
# Bounded redraw wait; every iteration rechecks identity and composer. No claim of
# atomicity: an untrusted agent can still change its input semantics after this check.
for ((i=0; i<40; i++)); do
    snapshot; rc=$?
    ((rc == 0)) || fail 27 "receiver changed before Enter (observation=$rc); attempt uncertain"
    [[ $identity == "$initial_identity" ]] || fail 27 'receiver identity changed; attempt uncertain'
    [[ $last_line == "❯ $pointer" && $cursor_y == 0 && $cursor_x == $((${#pointer} + 2)) ]] && break
    [[ $last_line == '❯' || $last_line == '❯ '* ]] || fail 27 'composer changed; attempt uncertain'
    sleep 0.025
done
[[ $last_line == "❯ $pointer" && $cursor_y == 0 && $cursor_x == $((${#pointer} + 2)) ]] || fail 27 'injected text not exactly visible; no Enter sent'
tmux -L "$server" send-keys -t "$pane" Enter || fail 28 'Enter injection failed; attempt uncertain'
printf 'phase=enter-attempted msg=%s utc=%s\n' "$msg" "$(date -u +%FT%TZ)" > "$claim/state" || fail 28 'cannot persist Enter attempt'
printf '%s notification-attempted server=%s pane=%s msg=%s receipt=unproven\n' "$(date -u +%FT%TZ)" "$server" "$pane" "$msg"
