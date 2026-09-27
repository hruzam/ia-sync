#!/usr/bin/env bash
# muticula B0 — run ONE headless (print-mode) case. TEST INSTRUMENT ONLY: `claude -p` is
# permitted solely as B0 instrumentation (RUNBOOK, majkee 2026-09-25); never a product path.
# Usage: run-print-case.sh <ROOT> <case> <prompt-file> [extra claude flags...]
# Records: before/after sha256 of both sentinels, the exact command, exit code, stream-json
# output and stderr, all under ROOT/logs/<case>.*. Exactly one claude invocation, no retry.
set -uo pipefail
ROOT="${1:?}"; CASE="${2:?}"; PROMPT_FILE="${3:?}"; shift 3
FX="$ROOT/fx"; L="$ROOT/logs"
cd "$FX" || exit 90

git checkout -q -- held.md unheld.md
git status --porcelain -- held.md unheld.md > "$L/$CASE.before-status.txt"
sha256sum held.md unheld.md > "$L/$CASE.before.sha256"

CMD=(claude -p "$(cat "$PROMPT_FILE")" --model haiku --permission-mode acceptEdits
     --setting-sources project,local --settings "$ROOT/settings/$CASE.json"
     --output-format stream-json --verbose "$@")
printf '%q ' "${CMD[@]:0:1}" "-p" "<prompt:$PROMPT_FILE>" "${CMD[@]:3}" > "$L/$CASE.command.txt"
echo >> "$L/$CASE.command.txt"

B0_ROOT="$ROOT" B0_CASE="$CASE" timeout 150 "${CMD[@]}" > "$L/$CASE.stream.jsonl" 2> "$L/$CASE.stderr"
echo "$?" > "$L/$CASE.exit"

sha256sum held.md unheld.md > "$L/$CASE.after.sha256"
git diff -- held.md unheld.md > "$L/$CASE.after.diff"
echo "case=$CASE exit=$(cat "$L/$CASE.exit")"
for f in held.md unheld.md; do
  b=$(grep " $f\$" "$L/$CASE.before.sha256" | cut -c1-12); a=$(grep " $f\$" "$L/$CASE.after.sha256" | cut -c1-12)
  [ "$b" = "$a" ] && echo "  $f: unchanged ($a)" || echo "  $f: CHANGED ($b -> $a): $(tail -n1 "$FX/$f")"
done
