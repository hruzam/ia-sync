#!/usr/bin/env bash
# C01-C18 and registered T01-T16 mirrors; calls only isolated vist-test.
set -uo pipefail
HERE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
ADAPTER=$HERE/../scripts/bus-poke.sh
REAL_TMUX=$(command -v tmux) || exit 2
scratch=$(mktemp -d /tmp/vist-cycle01.XXXXXX) || exit 2
session=vist-cycle01-$$-$RANDOM
owned=0 failures=0 pane= log= control=
cleanup() { ((owned == 0)) || "$REAL_TMUX" -L vist-test kill-session -t "$session" 2>/dev/null || :; }
trap cleanup EXIT
printf 'UTC=%s bash=%s tmux=%s artifacts=%s\n' "$(date -u +%FT%TZ)" "$BASH_VERSION" "$("$REAL_TMUX" -V)" "$scratch"
if "$REAL_TMUX" -L vist-test list-sessions > "$scratch/preexisting" 2>&1; then
    printf 'REFUSE: vist-test already has sessions; no cleanup/reset attempted\n' >&2
    exit 2
fi
"$REAL_TMUX" -L vist-test -f /dev/null new-session -d -s "$session" -x 240 -y 30 sleep 600 || exit 2
owned=1
"$REAL_TMUX" -L vist-test set-window-option -g remain-on-exit on || exit 2
mkdir "$scratch/bin"
cp "$HERE/tmux-interpose.sh" "$scratch/bin/tmux"
chmod +x "$scratch/bin/tmux"
export VIST_REAL_TMUX=$REAL_TMUX
export VIST_CALL_LOG=$scratch/tmux.calls
export PATH=$scratch/bin:$PATH
VIST_INTERPOSE_MODE=none
export VIST_INTERPOSE_MODE

result() {
    local id=$1 ok=$2 detail=$3
    if ((ok)); then printf '%s PASS %s\n' "$id" "$detail"; else
        printf '%s FAIL %s\n' "$id" "$detail"; failures=$((failures+1))
    fi
}
capture() { "$REAL_TMUX" -L vist-test capture-pane -p -t "$pane"; }
composer_snapshot() {
    capture
    "$REAL_TMUX" -L vist-test display-message -p -t "$pane" 'CURSOR #{cursor_x}:#{cursor_y}'
}
make_shell() {
    local tag=$1
    pane=$("$REAL_TMUX" -L vist-test new-window -d -t "$session" -n "$tag" -P -F '#{pane_id}' \
        /usr/bin/env 'PS1=VIST_SHELL> ' /usr/bin/bash --noprofile --norc -i) || exit 2
    for ((j=0; j<100; j++)); do
        screen=$(capture)
        [[ $screen == *'VIST_SHELL>'* ]] && return 0
        sleep 0.025
    done
    printf 'shell fixture failed readiness: %s\n' "$tag" >&2
    exit 2
}
make_agent() {
    local tag=$1 agent=$2 mode=$3
    control=$scratch/$tag.control; log=$scratch/$tag.received
    mkdir "$control"
    pane=$("$REAL_TMUX" -L vist-test new-window -d -t "$session" -n "$tag" -P -F '#{pane_id}' \
        /usr/bin/bash -c 'exec -a "$1" /usr/bin/bash "$2" "$3" "$4" "$5"' \
        fixture "$agent" "$HERE/fake-agent.sh" "$mode" "$log" "$control") || exit 2
    for ((j=0; j<100; j++)); do
        command=$("$REAL_TMUX" -L vist-test display-message -p -t "$pane" '#{pane_current_command}')
        screen=$(capture)
        if [[ $command == "$agent" && -e $control/ready ]]; then return 0; fi
        sleep 0.025
    done
    printf 'fixture failed to become ready: %s command=%s\n' "$tag" "$command" >&2
    exit 2
}
pointer_for() { pointer="[bus $1] from home:cartan -> read /tmp/request.md ; ack: none"; }
run_adapter() {
    local testmode=$1
    shift
    bash "$ADAPTER" "$testmode" --server vist-test --pane "$pane" --pointer "$pointer" --state-dir "$scratch/state" "$@" > "$scratch/last.out" 2>&1
    rc=$?
}
received() {
    local wanted=$1 text=
    for ((j=0; j<100; j++)); do
        [[ ! -f $log ]] || text=$(cat "$log")
        [[ $text == "$wanted" ]] && return 0
        sleep 0.025
    done
    return 1
}

make_agent c01 codex ready; pointer_for c01
before=$(composer_snapshot); run_adapter --check
after=$(composer_snapshot)
ok=0; [[ $rc == 0 && ! -e $scratch/state && ! -e $log ]] && ok=1
result C01 "$ok" "rc=$rc read-only state/log absent; composer-equal=$([[ $before == "$after" ]] && printf yes || printf no)"
[[ $before == "$after" ]] || { printf 'C01 FAIL composer changed\n'; failures=$((failures+1)); }

pointer_for c02; run_adapter --send
ok=0; if ((rc == 0)) && received "$pointer"; then ok=1; fi
text_calls=0; enter_calls=0
while IFS= read -r call; do
    [[ $call != "-L vist-test send-keys -t $pane -l $pointer" ]] || text_calls=$((text_calls+1))
    [[ $call != "-L vist-test send-keys -t $pane Enter" ]] || enter_calls=$((enter_calls+1))
done < "$VIST_CALL_LOG"
((text_calls == 1 && enter_calls == 1)) || ok=0
result C02 "$ok" "rc=$rc literal receiver line text-calls=$text_calls separate-Enter-calls=$enter_calls; $(cat "$scratch/last.out")"

pointer_for c03
bash "$ADAPTER" --check --server vist-test --pane bad --pointer "$pointer" --state-dir "$scratch/state" > "$scratch/last.out" 2>&1; rc=$?
result C03 "$((rc == 2))" "malformed pane rc=$rc expected=2"
bash "$ADAPTER" --check > "$scratch/last.out" 2>&1; rc=$?
result C03 "$((rc == 2))" "missing args rc=$rc expected=2"

saved=$pane; pane=%999999999; pointer_for c04; run_adapter --send
result C04 "$((rc == 20))" "unknown pane rc=$rc expected=20"; pane=$saved

make_agent c05 codex ready; pointer_for c05; : > "$control/exit-now"
for ((j=0; j<100; j++)); do
    dead=$("$REAL_TMUX" -L vist-test display-message -p -t "$pane" '#{pane_dead}')
    [[ $dead == 1 ]] && break; sleep 0.025
done
run_adapter --send
result C05 "$((rc == 21))" "retained dead pane=$dead rc=$rc expected=21 log-absent=$([[ ! -e $log ]] && printf yes || printf no)"

make_shell c06
pointer_for c06; before=$(composer_snapshot); run_adapter --send; after=$(composer_snapshot)
result C06 "$((rc == 22))" "non-agent shell rc=$rc expected=22"
[[ $before == "$after" ]] || { printf 'C06 FAIL shell content changed\n'; failures=$((failures+1)); }

for variant in occupied whitespace; do
    make_agent "c07-$variant" codex "$variant"; pointer_for "c07-$variant"
    before=$(composer_snapshot); run_adapter --send; after=$(composer_snapshot)
    ok=0; [[ $rc == 23 && $before == "$after" && ! -e $log ]] && ok=1
    result C07 "$ok" "$variant draft unchanged rc=$rc expected=23"
done

make_agent c08 codex busy; pointer_for c08; before=$(composer_snapshot); run_adapter --send; after=$(composer_snapshot)
ok=0; [[ $rc == 24 && $before == "$after" && ! -e $log ]] && ok=1
result C08 "$ok" "busy unchanged rc=$rc expected=24"

make_agent c09 codex ready; pointer_for c09; run_adapter --send
first=$rc; received "$pointer"; read_first=$?; run_adapter --send
ok=0; [[ $first == 0 && $read_first == 0 && $rc == 25 && $(wc -l < "$log") == 1 ]] && ok=1
result C09 "$ok" "first=$first duplicate=$rc received-lines=$(wc -l < "$log")"

make_agent c10 codex ready; pointer_for c10
export VIST_CONTROL=$control VIST_PANE=$pane VIST_INTERPOSE_MODE=exit-before-enter
run_adapter --send
VIST_INTERPOSE_MODE=none
dead=$("$REAL_TMUX" -L vist-test display-message -p -t "$pane" '#{pane_dead}')
ok=0; [[ $rc == 27 && $dead == 1 && ! -e $log ]] && ok=1
result C10 "$ok" "exit after text before Enter rc=$rc expected=27 pane-dead=$dead no shell parent/no receipt"
capture > "$scratch/c10.pane"

control=$scratch/c11.control; log=$scratch/c11.received; mkdir "$control"
sentinel=$scratch/c11.shell-fallback
make_shell c11
printf -v launch '%q ' /usr/bin/bash -c 'exec -a codex /usr/bin/bash "$1" ready "$2" "$3"' fixture "$HERE/fake-agent.sh" "$log" "$control"
printf -v after_child 'printf fallback > %q' "$sentinel"
"$REAL_TMUX" -L vist-test send-keys -t "$pane" -l "$launch; $after_child"
"$REAL_TMUX" -L vist-test send-keys -t "$pane" Enter
for ((j=0; j<100; j++)); do
    command=$("$REAL_TMUX" -L vist-test display-message -p -t "$pane" '#{pane_current_command}')
    [[ $command == codex ]] && break; sleep 0.025
done
pointer_for c11; run_adapter --send
ok=0; [[ $rc == 26 && ! -e $sentinel && ! -e $log ]] && ok=1
result C11 "$ok" "foreground=$command enclosing shell refused rc=$rc expected=26 fallback sentinel absent"

make_agent c12 codex ready
before=$(composer_snapshot)
expansion_bad='[bus x] from home:cartan -> read $(touch '"$scratch"'/expansion-sentinel) ; ack: none'
bad_pointers=('not a bus pointer' "$(printf '%0201d' 0)" '[bus x] from home:cartan -> read /tmp/é.md ; ack: none' $'[bus x]\nfrom home:cartan' $'[bus x]\tfrom home:cartan' "$expansion_bad" '[bus x] from home:cartan -> read /tmp/a; echo nope ; ack: none')
variant=0
for pointer in "${bad_pointers[@]}"; do
    variant=$((variant+1)); run_adapter --send
    after=$(composer_snapshot); ok=0
    [[ $rc == 30 && $before == "$after" && ! -e $log ]] && ok=1
    result C12 "$ok" "validation variant=$variant rc=$rc expected=30 composer unchanged"
done
ok=0; [[ ! -e $scratch/expansion-sentinel ]] && ok=1
result C12 "$ok" 'literal expansion payload never executed (unique scratch sentinel absent)'

make_agent c13 codex ready; pointer_for c13; : > "$scratch/state-is-file"
run_adapter --send --state-dir "$scratch/state-is-file"
ok=0; [[ $rc == 28 && ! -e $log ]] && ok=1
result C13 "$ok" "state path is file rc=$rc expected=28 no submission"

make_agent c14 codex ready; pointer_for c14
export VIST_CONTROL=$control VIST_PANE=$pane VIST_INTERPOSE_MODE=crash-after-reserve
run_adapter --send
crash_rc=$rc; VIST_INTERPOSE_MODE=none
run_adapter --send
ok=0; [[ $crash_rc == 137 && $rc == 25 && -e $control/crash-observed && ! -e $log ]] && ok=1
result C14 "$ok" "killed-after-reservation=$crash_rc restart=$rc expected=25 no receipt; uncertain claim retained"

make_agent c15 codex unknown; pointer_for c15; before=$(composer_snapshot); run_adapter --send; after=$(composer_snapshot)
ok=0; [[ $rc == 29 && $before == "$after" && ! -e $log ]] && ok=1
result C15 "$ok" "unknown composer unchanged rc=$rc expected=29"

make_agent c16 codex ready; pointer_for c16
bash "$ADAPTER" --send --server vist-test --pane "$pane" --pointer "$pointer" --state-dir "$scratch/state" > "$scratch/c16a.out" 2>&1 & a=$!
bash "$ADAPTER" --send --server vist-test --pane "$pane" --pointer "$pointer" --state-dir "$scratch/state" > "$scratch/c16b.out" 2>&1 & b=$!
wait "$a"; ra=$?; wait "$b"; rb=$?
received "$pointer"; got=$?
ok=0; [[ $got == 0 && $(wc -l < "$log") == 1 ]] && { [[ $ra == 0 && $rb != 0 || $rb == 0 && $ra != 0 ]] && ok=1; }
result C16 "$ok" "competing exits=$ra,$rb exactly-one-line=$([[ $got == 0 ]] && wc -l < "$log" || printf no)"

pointer_for c17
for endpoint in 'vist-unregistered:%0' 'default:%999999999'; do
    before_calls=$(cat "$VIST_CALL_LOG")
    bash "$ADAPTER" --check --server "${endpoint%%:*}" --pane "${endpoint#*:}" --pointer "$pointer" --state-dir "$scratch/state" > "$scratch/last.out" 2>&1; rc=$?
    after_calls=$(cat "$VIST_CALL_LOG"); ok=0
    [[ $rc == 2 && $before_calls == "$after_calls" ]] && ok=1
    result C17 "$ok" "registered amendment: forbidden $endpoint rc=$rc expected=2 zero tmux calls"
done

for agent in codex claude; do
    make_agent "c18-$agent" "$agent" ready; pointer_for "c18-$agent"; run_adapter --send
    ok=0; if ((rc == 0)) && received "$pointer"; then ok=1; fi
    result C18 "$ok" "$agent stand-in rc=$rc literal submission"
done

# Registered cycle-02 mirrors; all remain on vist-test and use synthetic text.
mirror_count=0
mirror() {
    local id=$1 agent=$2 fixture=$3 expected_rc=$4 send=${5:-0} state before after check_rc ok
    mirror_count=$((mirror_count+1))
    make_agent "$id-$mirror_count" "$agent" "$fixture"
    pointer_for "$id-$mirror_count"
    state=$scratch/$id-$mirror_count.attempts
    before=$(composer_snapshot)
    run_adapter --check --state-dir "$state"; check_rc=$rc
    after=$(composer_snapshot); ok=0
    [[ $check_rc == "$expected_rc" && $before == "$after" && ! -e $state && ! -e $log ]] && ok=1
    if ((send && check_rc == 0)); then
        run_adapter --send --state-dir "$state"
        if ((rc != 0)) || ! received "$pointer"; then ok=0; fi
    elif ((expected_rc != 0)); then
        run_adapter --send --state-dir "$state"
        after=$(composer_snapshot)
        [[ $rc == "$expected_rc" && $before == "$after" && ! -e $state && ! -e $log ]] || ok=0
    fi
    result "$id" "$ok" "$agent mirror=$fixture check=$check_rc expected=$expected_rc final=$rc no live calls"
    ((ok)) || cat "$scratch/last.out"
}
mirror T01 claude claude-empty 0 1
mirror T02 claude claude-suggestion 0 1
mirror T02 claude claude-reset-dim 0 1
mirror T03 claude claude-typed 23
mirror T03 claude claude-typed-start 23
mirror T04 claude claude-whitespace 23
mirror T05 claude claude-multiline 23
mirror T05 claude claude-continuation-start 23
mirror T05 claude claude-dim-continuation-start 23
mirror T06 claude claude-busy 24
mirror T07 codex codex-busy 24
mirror T08 codex codex-placeholder 0 1
mirror T09 codex codex-typed 23
mirror T09 codex codex-typed-start 23
for fixture in claude-rgb claude-bg-rgb claude-indexed claude-bg-indexed claude-mixed; do mirror T10 claude "$fixture" 23; done
mirror T11 claude claude-missing-footer 29
mirror T11 codex codex-missing-footer 29
mirror T11 codex codex-alternative 29
mirror T12 claude claude-historical 0
mirror T12 codex codex-historical 0

make_agent t13 claude claude-empty
window=$("$REAL_TMUX" -L vist-test display-message -p -t "$pane" '#{window_id}')
"$REAL_TMUX" -L vist-test resize-window -t "$window" -x 130 -y 30
printf -v wide_path '%0125d' 0
pointer="[bus t13] from home:cartan -> read /$wide_path ; ack: none"
before=$(composer_snapshot); run_adapter --send --state-dir "$scratch/t13.attempts"; after=$(composer_snapshot)
ok=0; [[ $rc == 30 && $before == "$after" && ! -e $scratch/t13.attempts && ! -e $log ]] && ok=1
result T13 "$ok" "pointer-bytes=${#pointer} width=130 wrap validation rc=$rc expected=30 unchanged/no reservation"

pointer_for t14
for endpoint in 'vist-unregistered:%0' 'default:%999999999'; do
    before_calls=$(cat "$VIST_CALL_LOG")
    bash "$ADAPTER" --check --server "${endpoint%%:*}" --pane "${endpoint#*:}" --pointer "$pointer" --state-dir "$scratch/state" > "$scratch/last.out" 2>&1; rc=$?
    after_calls=$(cat "$VIST_CALL_LOG"); ok=0
    [[ $rc == 2 && $before_calls == "$after_calls" ]] && ok=1
    result T14 "$ok" "forbidden $endpoint rc=$rc no tmux call"
done

make_agent t15 claude claude-empty; pointer_for t15
export VIST_CONTROL=$control VIST_PANE=$pane VIST_INTERPOSE_MODE=busy-after-text
run_adapter --send --state-dir "$scratch/t15.attempts"; changed_rc=$rc
VIST_INTERPOSE_MODE=none
run_adapter --send --state-dir "$scratch/t15.attempts"
ok=0; [[ $changed_rc == 27 && $rc == 25 && -d $scratch/t15.attempts && ! -e $log ]] && ok=1
result T15 "$ok" "mirrored state changed after text=$changed_rc restart=$rc expected=27,25 no Enter/receipt"
mirror T16 claude claude-suggestion 0
mirror T16 codex codex-placeholder 0
printf 'SUMMARY failures=%s artifacts=%s UTC=%s\n' "$failures" "$scratch" "$(date -u +%FT%TZ)"
((failures == 0))
