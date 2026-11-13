#!/usr/bin/env bash
# vist-deliver.sh v2 — deliver ONE bus pointer to the seat named in the bus file's `to:` (cycle 08, after cartan NOK d032fd1).
# Resolver: tmux session "vist" window options @seat @vendor @id @carrier (data, not code).
# Usage: vist-deliver.sh <abs-path-to-bus-file> [from-label]      (from-label default: the file's `from:`, else home:trajectory)
#
# Exit  0 carrier accepted (queue) / submitted (keys: composer positively cleared) — NOT consumption
#       2 usage · 20 unknown recipient · 21 dead target · 22 not an agent (root process) · 25 duplicate / retained key
#      27 uncertain: keys typed, submission not proven (key kept, never retry) · 28 carrier error before any input
#      29 unknown composer/signature or identity changed before input · 31 bounded wait exhausted (nothing typed)
# Window options: @state   = latest TARGET observation: ready|busy|occupied|dialog|needs_approval|dead|unknown|not_agent|identity_changed
#                 @attempt = "<msg> <outcome> <utc>"   (this sender's attempt outcome; never overwrites @state)
#                 @notice  = on the SENDER's window when an attempt fails: "<utc> <msg> exit=<n> <reason>"
# Files (host-local, outside repos): $VIST_STATE (~/.local/state/vist)/deliver.log · notices.log · sent/<msg>/phase
# Env: VIST_SESSION=vist · VIST_WAITS="30 60 120 120" · VIST_QUIET=5 · VIST_DRY=1 (resolve+observe, no send) · VIST_SIGNATURES
set -u
# G1 (r1): run tmux WITHOUT the caller's client context; a read-only viewer client must never become the command's client.
tmux() { env -u TMUX tmux "$@"; }
# G1b (r1, found by trajectory): tmux send-keys borrows the most recently active client on the server; when that is a
# read-only viewer (attach -r) it fails "client is read-only" for ANY pane. paste-buffer has no such check. So input goes
# through a named, per-message buffer: text first, then a lone CR as a separate paste (= the Enter key).
put() { tmux set-buffer -b "vist-$MSG" -- "$1" && tmux paste-buffer -b "vist-$MSG" -t "$PANE" -d; }
SES=${VIST_SESSION:-vist}
STATE=${VIST_STATE:-$HOME/.local/state/vist}
WAITS=${VIST_WAITS:-"30 60 120 120"}
QUIET=${VIST_QUIET:-5}
HERE=$(dirname "$(readlink -f "$0")")
SIG=${VIST_SIGNATURES:-$HERE/vist-signatures.conf}
mkdir -p "$STATE/sent" && chmod 700 "$STATE"; LOG=$STATE/deliver.log
MSG=- TO=- CARRIER=- ATTEMPT=0 RESERVED=0 TYPED=0 IDX="" SIDX="" SSEAT="" FILE=""

utc() { date -u +%FT%TZ; }
log() { printf '%s %s event=%s msg=%s seat=%s carrier=%s attempt=%s %s\n' "$(utc)" "$1" "$2" "$MSG" "$TO" "$CARRIER" "$ATTEMPT" "${3:-}" >>"$LOG"; }
phase() { [[ $RESERVED == 1 ]] && printf '%s %s\n' "$(utc)" "$1" >>"$STATE/sent/$MSG/phase"; }
release() { phase "$1"; rm -rf "${STATE:?}/sent/$MSG"; RESERVED=0; }
notify_sender() {   # $1 exit, $2 reason
  local line; line="$(utc) $MSG exit=$1 $2"
  printf '%s to=%s\n' "$line" "$TO" >>"$STATE/notices.log"
  if [[ -n $SIDX ]]; then
    tmux set -w -t "$SES:$SIDX" @notice "$line" 2>/dev/null
    tmux display-message -d 8000 "vist: delivery to $TO failed: $2 (msg $MSG)" 2>/dev/null
    # G4 (r1): wake the sender with ONE bounded notice delivery. Hop limit 1: a notice never produces a notice.
    if [[ -z ${VIST_NOTICE_HOP:-} && -n $SSEAT && $SSEAT != "$TO" ]]; then
      mkdir -p "$STATE/notices"; local nf="$STATE/notices/$MSG.n.md"
      printf '```yaml\nmsg: %s.n\nfrom: vist\nto: %s\nre: %s\n```\n\nDelivery of %s to %s FAILED: exit=%s %s.\nSee %s/deliver.log (msg=%s). Nothing was resent.\n' \
        "$MSG" "$SSEAT" "$FILE" "$MSG" "$TO" "$1" "$2" "$STATE" "$MSG" >"$nf"
      VIST_NOTICE_HOP=1 VIST_WAITS="${VIST_NOTICE_WAITS:-30 60 120}" nohup bash "$0" "$nf" vist >/dev/null 2>&1 &
      log INFO notice_spawned "notice=$nf to=$SSEAT"
    fi
  fi
}
finish() {          # $1 exit, $2 event, $3 reason   (non-zero exits only)
  local rc=$1
  log ERROR "$2" "reason=$3 exit=$rc"; notify_sender "$rc" "$3"; echo "vist-deliver: $3 (exit $rc)" >&2
  [[ -n $IDX ]] && tmux set -w -t "$SES:$IDX" @attempt "$MSG $2 $(utc)" 2>/dev/null
  if [[ $RESERVED == 1 && $TYPED == 0 ]]; then release "released-clean exit=$rc"; fi
  if [[ $RESERVED == 1 && $TYPED == 1 ]]; then phase "kept exit=$rc $3"; fi
  exit "$rc"
}

FILE=${1:-}
[[ -n $FILE && -f $FILE && $FILE = /* ]] || { echo "usage: $0 /abs/bus-file [from]" >&2; exit 2; }
field() { grep -m1 -E "^$1:" "$FILE" | sed -E "s/^$1:[[:space:]]*//; s/[[:space:]]+#.*$//"; }
TO=$(field to); MSG=$(field msg); FROM=${2:-$(field from)}; FROM=${FROM:-home:trajectory}
if [[ -z $TO || -z $MSG ]]; then MSG=${MSG:--}; TO=${TO:--}; finish 2 refused bad_bus_file; fi
[[ $MSG =~ ^[A-Za-z0-9._-]+$ ]] || { MSG=unsafe; finish 2 refused unsafe_msg_id; }

# --- resolve recipient (and sender, for notices): match @seat whole or the part before '|'
ROWS=$(tmux list-windows -t "$SES" -F $'#{window_index}\t#{@seat}\t#{@vendor}\t#{@id}\t#{@carrier}\t#{pane_id}' 2>/dev/null)
match() { local want=$1 i s rest
  while IFS=$'\t' read -r i s rest; do
    [[ -n $s && ( $want == "$s" || $want == "${s%%|*}" ) ]] && { printf '%s\t%s\t%s\n' "$i" "$s" "$rest"; return; }
  done <<<"$ROWS"; }
srow=$(match "${FROM##*:}"); SIDX=${srow%%$'\t'*}; SSEAT=$(printf '%s' "$srow" | cut -f2)
row=$(match "$TO"); [[ -n $row ]] || finish 20 refused unknown_recipient
IFS=$'\t' read -r IDX _ VENDOR ID CARRIER PANE <<<"$row"
log INFO resolved "window=$SES:$IDX pane=$PANE vendor=$VENDOR"
[[ $CARRIER == codex-queue || ( $CARRIER == tmux && $VENDOR == claude ) ]] || finish 28 refused unsupported_carrier

# --- durable reservation BEFORE waiting (atomic mkdir: a concurrent second caller gets 25 at once)
mkdir "$STATE/sent/$MSG" 2>/dev/null || finish 25 refused "duplicate_or_retained_key last_phase=$(tail -1 "$STATE/sent/$MSG/phase" 2>/dev/null | tr ' ' '_')"
RESERVED=1; phase "reserved by $FROM to $TO via $CARRIER"

ident() {  # root process identity "<pid> <start-ticks> <comm>", empty when dead
  local pid; pid=$(tmux display -p -t "$PANE" '#{pane_pid}' 2>/dev/null) || return
  [[ $(tmux display -p -t "$PANE" '#{pane_dead}' 2>/dev/null) == 1 ]] && return
  printf '%s %s %s' "$pid" "$(awk '{print $22}' "/proc/$pid/stat" 2>/dev/null)" "$(ps -o comm= -p "$pid" 2>/dev/null)"
}
composer() {  # Claude input box = rows between the last two border rows (blank rows dropped first: Claude draws inline, the
              # pane bottom can be empty); first row must hold the prompt glyph.
              # Prints NOBOX, or the box text with dim (suggestion) segments, NBSP, the glyph and all whitespace removed.
  tmux capture-pane -p -e -t "$PANE" | grep -v $'^[[:space:]]*$' | tail -25 | python3 -c '
import re,sys
rows=[re.sub(r"\x1b\[2m.*?\x1b\[(?:0|22)m","",r).replace(" "," ") for r in sys.stdin.read().split("\n")]
plain=[re.sub(r"\x1b\[[0-9;?]*[A-Za-z]","",r) for r in rows]
b=[i for i,r in enumerate(plain) if len(r.strip())>=20 and set(r.strip())<={"─"}]
if len(b)<2 or b[-1]-b[-2]<2 or "❯" not in plain[b[-2]+1]: print("NOBOX"); sys.exit()
print(re.sub(r"\s+","","".join(plain[b[-2]+1:b[-1]]).replace("❯","",1)))'
}
ID0=$(ident)
observe() {  # -> ready|busy|occupied|needs_approval|dead|not_agent|unknown|identity_changed
  local now v st re act c plain
  now=$(ident); [[ -z $now ]] && { echo dead; return; }
  [[ ${now##* } == "$VENDOR" && $(tmux display -p -t "$PANE" '#{pane_current_command}') == "$VENDOR"* ]] || { echo not_agent; return; }
  [[ $now == "$ID0" ]] || { echo identity_changed; return; }
  plain=$(tmux capture-pane -p -t "$PANE" | grep -v '^[[:space:]]*$' | tail -6)
  while IFS='|' read -r v st re; do
    [[ -z $v || $v == \#* || $v != "$VENDOR" ]] && continue
    printf '%s\n' "$plain" | grep -qE -- "$re" && { echo "$st"; return; }
  done <"$SIG"
  act=$(tmux display -p -t "$PANE" '#{window_activity}'); (( $(date +%s) - act < QUIET )) && { echo busy; return; }
  [[ $CARRIER == codex-queue ]] && { echo ready; return; }   # G3 (r1): report busy truly; deliverability is decided below
  c=$(composer); [[ $c == NOBOX ]] && { echo unknown; return; }; [[ -n $c ]] && { echo occupied; return; }
  echo ready
}
setstate() { tmux set -w -t "$SES:$IDX" @state "$1" 2>/dev/null; }
[[ -n $ID0 ]] || { setstate dead; finish 21 refused dead_target; }

# --- bounded wait (read-only observations only)
st=$(observe); setstate "$st"; n=0
deliverable() { [[ $1 == ready || ( $1 == busy && $CARRIER == codex-queue ) ]]; }  # queue holds until the turn ends
for w in $WAITS; do
  deliverable "$st" && break
  case $st in dead) finish 21 refused dead_target ;; not_agent) finish 22 refused not_agent_root ;;
    identity_changed) finish 29 refused identity_changed ;; esac
  ATTEMPT=$((++n)); log WARN wait "state=$st waiting=${w}s"; sleep "$w"; st=$(observe); setstate "$st"
done
deliverable "$st" && st=ready
case $st in ready) ;; dead) finish 21 refused dead_target ;; not_agent) finish 22 refused not_agent_root ;;
  identity_changed) finish 29 refused identity_changed ;; unknown) finish 29 refused unknown_composer ;;
  *) finish 31 refused "wait_exhausted last_state=$st waits=$n" ;; esac

POINTER="[vist $MSG] from $FROM -> read $FILE ; ack: per file"
if [[ ${VIST_DRY:-0} == 1 ]]; then log INFO dry_run "would_send=1"; release released-dry; echo "dry-run ok: $SES:$IDX $CARRIER"; exit 0; fi

case $CARRIER in
  codex-queue)
    [[ $(ident) == "$ID0" ]] || finish 29 refused identity_changed
    TYPED=1; phase carrier-called   # from here a submission may exist: key is kept whatever happens
    out=$(codex queue --thread "$ID" --message "$POINTER" 2>&1); rc=$?
    log INFO carrier_call "rc=$rc out=$(printf '%s' "$out" | tr '\n' ' ')"
    (( rc == 0 )) || finish 27 uncertain "codex_queue_rc=$rc"
    phase "queued $(printf '%s' "$out" | grep -oE '[0-9a-f]{8}-[0-9a-f-]{27}' | head -1)"
    tmux set -w -t "$SES:$IDX" @attempt "$MSG queued $(utc)"; log INFO queued "accepted=1"; echo "queued: $out"; exit 0 ;;
  tmux)
    [[ $(ident) == "$ID0" ]] || finish 29 refused identity_changed
    TYPED=1; phase text-attempted
    put "$POINTER" || finish 27 uncertain paste_text_failed
    sleep 1
    [[ $(ident) == "$ID0" ]] || finish 27 uncertain identity_changed_after_text
    want=$(printf '%s' "$POINTER" | tr -d '[:space:]'); have=$(composer)
    [[ $have == "$want" ]] || finish 27 uncertain "post_text_mismatch box_len=${#have} want_len=${#want}"
    phase enter-attempted
    put $'\r' || finish 27 uncertain paste_enter_failed
    for _ in 1 2 3 4 5 6 7 8 9 10; do
      sleep 1; c=$(composer)
      if [[ $c != NOBOX && -z $c ]]; then
        phase submitted; tmux set -w -t "$SES:$IDX" @attempt "$MSG submitted $(utc)"
        log INFO submitted "composer=positively_empty"; echo "submitted"; exit 0
      fi
    done
    finish 27 uncertain "no_positive_submission_evidence" ;;
esac
