#!/usr/bin/env bash
# Cycle 02: registered live endpoints plus isolated stand-ins. Screen inference is
# not an atomic/authenticated input API. Success is only a notification attempt.
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
        *) fail 2 'usage: --check|--send --server SERVER --pane %N --pointer LINE --state-dir ABS';;
    esac
done
[[ -n $mode && -n $pointer && $pane =~ ^%[0-9]+$ && $state_dir == /* ]] || fail 2 'explicit server, pane id, mode, pointer and absolute state path required'
expected=
case $server:$pane in
    default:%3) expected=claude;; default:%2) expected=codex;;
    vist-test:*) ;; *) fail 2 'unregistered endpoint';;
esac
# Deliberately bounded grammar; it cannot express a shell-expansion payload.
pattern='^\[bus ([A-Za-z0-9][A-Za-z0-9._:-]*)\] from [A-Za-z0-9._-]+:[A-Za-z0-9._/-]+ -> (git pull, )?read [A-Za-z0-9_./~-]+ ; ack: (none|stamp|reply)$'
[[ ${#pointer} -le 200 && $pointer =~ $pattern ]] || fail 30 'invalid pointer: one ASCII line, <=200 chars, bounded bus/read grammar'
msg=${BASH_REMATCH[1]}
key=$(printf '%s\n%s\n%s\n' "$server" "$pane" "$msg" | sha256sum) || fail 28 'cannot hash attempt key'
claim=$state_dir/${key%% *}
[[ ! -e $claim ]] || fail 25 'duplicate or uncertain prior attempt; inspect receipt before recovery'

identity= cursor_x= cursor_y= pane_width= composer_row= suffix= suffix_dim= layout= incoherent=0
sgr_re=$'\033''\[([0-9;]*)m'
strip_sgr() {
    plain=$1
    while [[ $plain =~ $sgr_re ]]; do plain=${plain/"${BASH_REMATCH[0]}"/}; done
}
# Per-byte dim mask: colors' indexed/RGB payloads are not standalone SGR codes.
composer_text() {
    local raw=$1 seq code dim=0 mask= rendered= c pos=0 prefix_len
    local -a params
    while [[ -n $raw ]]; do
        if [[ $raw == $'\033'* ]]; then
            [[ $raw =~ ^$sgr_re ]] || return 29
            seq=${BASH_REMATCH[1]}; raw=${raw:${#BASH_REMATCH[0]}}
            [[ -n $seq ]] || seq=0
            IFS=';' read -r -a params <<< "$seq"
            for ((pos=0; pos<${#params[@]}; pos++)); do
                code=${params[pos]:-0}
                case $code in
                    0|22) dim=0;; 2) dim=1;;
                    38|48|58)
                        case ${params[pos+1]:-} in
                            2) ((pos+=4));; 5) ((pos+=2));; *) return 29;;
                        esac;;
                esac
            done
        else
            c=${raw:0:1}; rendered+=$c; mask+=$dim; raw=${raw:1}
        fi
    done
    prefix_len=${#glyph}
    case ${rendered:prefix_len} in
        ' '*) ((prefix_len+=1));; $'\302\240'*) ((prefix_len+=2));;
        '') ;; *) return 29;;
    esac
    suffix=${rendered:prefix_len}
    mask=${mask:prefix_len}
    suffix_dim=0
    [[ -z $suffix || $mask == *0* ]] || suffix_dim=1
}
screen_contract() {
    local raw=$1 command=$2 row=0 line raw_line last=-1 footer=0 separator=0 model_footer=0 shortcuts=0 start continuation=0 known
    local -a raw_rows=() rows=()
    while IFS= read -r raw_line; do
        raw_rows+=("$raw_line"); strip_sgr "$raw_line"; rows+=("$plain")
    done <<< "$raw"
    glyph='❯'; [[ $command != codex ]] || glyph='›'
    for ((row=0; row<${#rows[@]}; row++)); do
        line=${rows[row]}
        if [[ $line == "$glyph" || $line == "$glyph "* || $line == "$glyph"$'\302\240'* ]]; then last=$row; fi
    done
    # Preserve C01's legacy contract only on the isolated server, never live.
    layout=$command
    if [[ $server == vist-test && $last == -1 || $server == vist-test && $last == 0 ]]; then
        strip_sgr "${raw_rows[0]}"
        if [[ $plain == '❯' || $plain == '❯ '* ]]; then glyph='❯'; last=0; layout=legacy; fi
    fi
    if ((last < 0)); then
        [[ $server != vist-test || $raw != *'esc to interrupt'* ]] || return 24
        return 29
    fi
    composer_row=$last
    for ((row=last+1; row<${#rows[@]}; row++)); do
        line=${rows[row]}
        [[ $line != *'esc to interrupt'* ]] || return 24
        known=0
        [[ $line != *'⏵⏵ auto mode on (shift+tab to cycle)'* ]] || { footer=1; known=1; }
        [[ -z $line || -n ${line//─/} ]] || { separator=1; known=1; }
        [[ $line != '  GPT-6.1-Sol high · ~/reposoma · cartan|astrobley · '* || $line != *' · Context '* ]] || { model_footer=1; known=1; }
        [[ $line != '  ← for agents · ? for shortcuts' ]] || { shortcuts=1; known=1; }
        [[ -z ${line// /} || $known == 1 ]] || continuation=1
    done
    if [[ $layout == legacy && $footer == 1 ]]; then layout=claude; fi
    case $layout in
        claude) ((footer && separator)) || return 29;;
        codex)
            ((model_footer && shortcuts)) || return 29
            start=$((last > 8 ? last-8 : 0))
            for ((row=start; row<last; row++)); do
                [[ ${rows[row]} != '• '* || ${rows[row]} != *'esc to interrupt'* ]] || return 24
            done;;
        legacy) ;;
    esac
    ((continuation == 0)) || return 23
    composer_text "${raw_rows[last]}" || return $?
    return 0
}
snapshot() {
    local info again id pid dead command argv0 stat rest screen
    local -a fields
    incoherent=0
    info=$(tmux -L "$server" display-message -p -t "$pane" '#{pane_id}|#{pane_pid}|#{pane_dead}|#{pane_current_command}|#{cursor_x}|#{cursor_y}|#{pane_width}' 2>/dev/null) || return 20
    IFS='|' read -r id pid dead command cursor_x cursor_y pane_width <<< "$info"
    [[ $id == "$pane" && $pid =~ ^[0-9]+$ ]] || return 20
    [[ $dead == 0 ]] || return 21
    [[ $command == codex || $command == claude ]] || return 22
    [[ -z $expected || $command == "$expected" ]] || return 22
    IFS= read -r -d '' argv0 < "/proc/$pid/cmdline" 2>/dev/null || return 26
    argv0=${argv0##*/}
    [[ $argv0 == "$command" ]] || return 26
    # PID plus Linux process start time prevents a stale PID snapshot from matching.
    stat=$(cat "/proc/$pid/stat" 2>/dev/null) || return 26
    rest=${stat##*) }
    read -r -a fields <<< "$rest"
    [[ ${fields[19]:-} =~ ^[0-9]+$ ]] || return 26
    identity=$pid:${fields[19]}
    screen=$(tmux -L "$server" capture-pane -p -e -t "$pane" 2>/dev/null) || return 20
    again=$(tmux -L "$server" display-message -p -t "$pane" '#{pane_id}|#{pane_pid}|#{pane_dead}|#{pane_current_command}|#{cursor_x}|#{cursor_y}|#{pane_width}' 2>/dev/null) || return 20
    [[ $again == "$info" ]] || { incoherent=1; return 29; }
    screen_contract "$screen" "$command"
}
# Observe a changing frame again before declaring a refusal. Coherent unknown
# layouts are never retried or accepted by this bounded metadata-coherence path.
for ((observation=0; observation<3; observation++)); do
    snapshot; rc=$?
    if ((rc == 29 && incoherent == 1 && observation < 2)); then sleep 0.025; continue; fi
    break
done
((rc == 0)) || fail "$rc" 'unknown/dead/non-agent/unsafe/busy receiver'
initial_identity=$identity
initial_row=$composer_row; initial_layout=$layout
(( ${#pointer} + 2 < pane_width )) || fail 30 'pointer would wrap; no attempt reserved'
[[ $cursor_x == 2 && $cursor_y == "$composer_row" ]] || fail 23 'occupied/multiline composer or non-start cursor'
if [[ -n $suffix ]]; then
    [[ $layout != legacy && $suffix_dim == 1 ]] || fail 23 'non-dim draft'
    [[ $layout != codex || $suffix == 'Ask Codex to do anything' ]] || fail 29 'unknown Codex suggestion'
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
confirmed=0
for ((i=0; i<40; i++)); do
    snapshot; rc=$?
    # A changing redraw is not a safe snapshot. Read again within the same
    # reservation; never re-inject text or send Enter until one exact coherent view.
    if ((rc == 29)); then
        [[ $identity == "$initial_identity" ]] || fail 27 'identity changed during redraw; attempt uncertain'
        sleep 0.025; continue
    fi
    ((rc == 0)) || fail 27 "receiver changed before Enter (observation=$rc); attempt uncertain"
    [[ $identity == "$initial_identity" ]] || fail 27 'receiver identity changed; attempt uncertain'
    [[ $composer_row == "$initial_row" && $layout == "$initial_layout" ]] || fail 27 'layout changed; attempt uncertain'
    if [[ $suffix == "$pointer" && $suffix_dim == 0 && $cursor_y == "$composer_row" && $cursor_x == $((${#pointer} + 2)) ]]; then confirmed=1; break; fi
    sleep 0.025
done
((confirmed)) || fail 27 'injected text not exactly visible; no Enter sent'
tmux -L "$server" send-keys -t "$pane" Enter || fail 28 'Enter injection failed; attempt uncertain'
printf 'phase=enter-attempted msg=%s utc=%s\n' "$msg" "$(date -u +%FT%TZ)" > "$claim/state" || fail 28 'cannot persist Enter attempt'
printf '%s notification-attempted server=%s pane=%s msg=%s receipt=unproven\n' "$(date -u +%FT%TZ)" "$server" "$pane" "$msg"
