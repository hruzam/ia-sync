#!/usr/bin/env bash
# C01-C18 from reports/cartan.matrix.2026-11-12.md; only isolated vist-test.
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
        if [[ $command == "$agent" && -n $screen ]]; then return 0; fi
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
before_calls=$(cat "$VIST_CALL_LOG")
bash "$ADAPTER" --check --server default --pane %0 --pointer "$pointer" --state-dir "$scratch/state" > "$scratch/last.out" 2>&1; rc=$?
after_calls=$(cat "$VIST_CALL_LOG"); ok=0
[[ $rc == 2 && $before_calls == "$after_calls" ]] && ok=1
result C17 "$ok" "forbidden default server rc=$rc expected=2 no tmux call (local validation)"

for agent in codex claude; do
    make_agent "c18-$agent" "$agent" ready; pointer_for "c18-$agent"; run_adapter --send
    ok=0; if ((rc == 0)) && received "$pointer"; then ok=1; fi
    result C18 "$ok" "$agent stand-in rc=$rc literal submission"
done
printf 'SUMMARY failures=%s artifacts=%s UTC=%s\n' "$failures" "$scratch" "$(date -u +%FT%TZ)"
((failures == 0))
