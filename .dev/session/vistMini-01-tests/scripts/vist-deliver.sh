#!/usr/bin/env bash
# vist-deliver.sh — deliver ONE bus pointer to the seat named in the bus file's `to:`.
# Resolver = tmux session "vist" window options (@seat @vendor @id @carrier). Data, not code.
# Usage: vist-deliver.sh <abs-path-to-bus-file> [from-label]
# Exit: 0 delivered(accepted) · 2 usage · 20 unknown seat · 21 dead pane · 22 not an agent · 25 duplicate msg
#       27 uncertain (keys typed, no turn start seen) · 28 carrier error · 31 wait exhausted (occupied/busy/needs_approval)
# Log (persistent, outside repos): ${VIST_STATE:-~/.local/state/vist}/deliver.log
# Env: VIST_SESSION (vist) · VIST_WAITS ("30 60 120 120") · VIST_QUIET (5 s) · VIST_DRY=1 (resolve + check, never send)
set -u
SES=${VIST_SESSION:-vist}
STATE=${VIST_STATE:-$HOME/.local/state/vist}
WAITS=${VIST_WAITS:-"30 60 120 120"}
QUIET=${VIST_QUIET:-5}
SIG=${VIST_SIGNATURES:-$(dirname "$(readlink -f "$0")")/vist-signatures.conf}
mkdir -p "$STATE/sent"; LOG=$STATE/deliver.log

log() { printf '%s %s msg=%s seat=%s %s\n' "$(date -u +%FT%TZ)" "$1" "${MSG:--}" "${TO:--}" "$2" >>"$LOG"; }
die() { log ERROR "exit=$1 $2"; echo "vist-deliver: $2 (exit $1)" >&2; exit "$1"; }

FILE=${1:-}; FROM=${2:-home:trajectory}
[[ -n $FILE && -f $FILE && $FILE = /* ]] || { echo "usage: $0 /abs/bus-file [from]" >&2; exit 2; }
field() { grep -m1 -E "^$1:" "$FILE" | sed -E "s/^$1:[[:space:]]*//; s/[[:space:]]+#.*$//"; }
TO=$(field to); MSG=$(field msg)
[[ -n $TO && -n $MSG ]] || die 2 "bus file lacks to:/msg:"
[[ $MSG =~ ^[A-Za-z0-9._-]+$ ]] || die 2 "msg id has unsafe characters"

# --- resolve: match `to:` against @seat, whole value or the part before '|'
row=""
while IFS=$'\t' read -r idx seat vendor id carrier pane dead cmd; do
  [[ -z $seat ]] && continue
  if [[ $TO == "$seat" || $TO == "${seat%%|*}" ]]; then row="$idx"$'\t'"$vendor"$'\t'"$id"$'\t'"$carrier"$'\t'"$pane"$'\t'"$dead"$'\t'"$cmd"; break; fi
done < <(tmux list-windows -t "$SES" -F $'#{window_index}\t#{@seat}\t#{@vendor}\t#{@id}\t#{@carrier}\t#{pane_id}\t#{pane_dead}\t#{pane_current_command}' 2>/dev/null)
[[ -n $row ]] || die 20 "no window in session $SES labels seat '$TO'"
IFS=$'\t' read -r IDX VENDOR ID CARRIER PANE DEAD CMD <<<"$row"
log INFO "resolved window=$SES:$IDX pane=$PANE vendor=$VENDOR carrier=$CARRIER"

[[ -e $STATE/sent/$MSG ]] && die 25 "duplicate: $MSG already reserved ($(cat "$STATE/sent/$MSG" 2>/dev/null))"

signal() { tmux set -w -t "$SES:$IDX" @state "$1" 2>/dev/null; [[ $1 == needs_approval || $1 == stuck ]] && \
  tmux display-message -d 8000 "vist: $SES:$IDX ($TO) is $1 — msg $MSG waiting" 2>/dev/null; }

# NB: Claude writes a NO-BREAK SPACE (U+00A0) after the prompt glyph; [[:space:]] does not match it (found 2026-11-13).
# --- one read-only observation → prints: ok | dead | not_agent | busy | occupied | needs_approval
observe() {
  local d c act quiet raw plain prompt st
  d=$(tmux display -p -t "$PANE" '#{pane_dead}' 2>/dev/null) || { echo dead; return; }
  [[ $d == 1 ]] && { echo dead; return; }
  c=$(tmux display -p -t "$PANE" '#{pane_current_command}')
  [[ $c == "$VENDOR" || ( $VENDOR == codex && $c == codex* ) ]] || { echo not_agent; return; }
  raw=$(tmux capture-pane -p -e -t "$PANE" | grep -v '^[[:space:]]*$' | tail -6)
  plain=$(printf '%s\n' "$raw" | sed -E 's/\x1b\[[0-9;]*[A-Za-z]//g')
  while IFS='|' read -r v st re; do
    [[ -z $v || $v == \#* || $v != "$VENDOR" ]] && continue
    printf '%s\n' "$plain" | grep -qE -- "$re" && { echo "$st"; return; }
  done <"$SIG"
  act=$(tmux display -p -t "$PANE" '#{window_activity}'); quiet=$(( $(date +%s) - act ))
  # busy blocks only the typed carrier; codex queue holds the message until the receiver's turn ends (receiver keeps working)
  [[ $CARRIER == tmux ]] && (( quiet < QUIET )) && { echo busy; return; }
  if [[ $CARRIER == tmux ]]; then   # typed carrier: composer must be empty once dim (suggestion) text is removed
    prompt=$(printf '%s\n' "$raw" | grep '❯' | tail -1 | sed -E 's/\xc2\xa0/ /g; s/\x1b\[2m[^\x1b]*\x1b\[(0|22)m//g; s/\x1b\[[0-9;]*[A-Za-z]//g; s/^.*❯[[:space:]]*//; s/[[:space:]]+$//')
    [[ -n $prompt ]] && { echo occupied; return; }
  fi
  echo ok
}

# --- wait loop: re-observe (read-only) with growing gaps; send at most once
st=$(observe); n=0
for w in $WAITS; do
  case $st in ok) break ;; dead) die 21 "pane $PANE dead" ;; not_agent) die 22 "pane $PANE runs '$CMD', not $VENDOR" ;; esac
  signal "$st"; log WARN "state=$st attempt=$((++n)) waiting=${w}s quiet_needed=${QUIET}s"
  sleep "$w"; st=$(observe)
done
case $st in ok) ;; dead) die 21 "pane $PANE dead" ;; not_agent) die 22 "pane $PANE not $VENDOR" ;;
  *) signal stuck; die 31 "wait exhausted: last state=$st after $n waits ($WAITS)" ;; esac

POINTER="[vist $MSG] from $FROM -> read $FILE ; ack: per file"
[[ ${VIST_DRY:-0} == 1 ]] && { log INFO "dry-run ok, would send via $CARRIER"; echo "dry-run ok: $SES:$IDX $CARRIER"; exit 0; }
mkdir "$STATE/sent/$MSG.lock" 2>/dev/null || die 25 "duplicate: concurrent reservation for $MSG"
printf '%s %s %s\n' "$(date -u +%FT%TZ)" "$CARRIER" "$PANE" >"$STATE/sent/$MSG"; rmdir "$STATE/sent/$MSG.lock"

case $CARRIER in
  codex-queue)
    out=$(codex queue --thread "$ID" --message "$POINTER" 2>&1); rc=$?
    log INFO "codex-queue rc=$rc out=$(printf '%s' "$out" | tr '\n' ' ')"
    (( rc == 0 )) || die 28 "codex queue failed rc=$rc"
    signal delivered; echo "delivered (queued): $out"; exit 0 ;;
  tmux)
    tmux send-keys -t "$PANE" -l "$POINTER"; sleep 1; tmux send-keys -t "$PANE" Enter
    log INFO "keys sent, waiting for the composer to clear (= submitted)"
    for _ in 1 2 3 4 5 6 7 8 9 10; do   # vendor-neutral: submitted text leaves the composer. Spinner words vary by version.
      sleep 1
      left=$(tmux capture-pane -p -e -t "$PANE" | grep '❯' | tail -1 | sed -E 's/\xc2\xa0/ /g; s/\x1b\[2m[^\x1b]*\x1b\[(0|22)m//g; s/\x1b\[[0-9;]*[A-Za-z]//g; s/^.*❯[[:space:]]*//; s/[[:space:]]+$//')
      if [[ -z $left ]]; then signal delivered; log INFO "submitted (composer clear)"; echo "delivered (submitted)"; exit 0; fi
    done
    signal uncertain; die 27 "keys typed, no turn start seen in 10 s; reservation kept, never retry" ;;
  *) die 28 "unknown carrier '$CARRIER'" ;;
esac
