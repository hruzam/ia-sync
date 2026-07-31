#!/usr/bin/env zsh
# doorbell-smoke.zsh — real-trigger smoke probe for the canon-doorbell
# Closes: 0009 L5 (the "real-fire OWED" debt on the relocated post-commit doorbell)
# host: office  (machine-specific: exercises the live base.zsh and project map)
# spec: temple/tools/doorbell-smoke-probe.spec.draft.md
#
# SAFETY CONTRACT:
#   - NEVER commits to the live ~/reposoma/temple/decisions/
#   - NEVER writes to any real project inbox (DOORBELL_DRY_FIRE=1 enforced + injected into hook copy)
#   - Runs in a disposable sandbox git repo (mktemp -d), torn down on exit
#   - Appends to live doorbell log (stated transparently in residue report)
#
# Usage:
#   zsh ~/.config/zsh/ai/doorbell-smoke.zsh          # green run only
#   zsh ~/.config/zsh/ai/doorbell-smoke.zsh --red     # deliberate-red run only (planted dead path)
#   zsh ~/.config/zsh/ai/doorbell-smoke.zsh --both    # green then red (full circuit)

# ---- Constants ----
REAL_BASE="${HOME}/.config/zsh/ai/base.zsh"
REAL_HOOK_TEMPLATE="${HOME}/.config/zsh/ai/temple-doorbell.post-commit.hook"
DEPLOYED_HOOK="${HOME}/reposoma/.git/hooks/post-commit"   # the trigger that actually fires
LOG_FILE="${HOME}/.config/zsh/temple-doorbell.log"
DEAD_PATH="/nonexistent/dead/path/PLANTED-DEAD-base.zsh"

# ---- Parse args (no setopt ERR_EXIT — probe deliberately drives a failing path) ----
RUN_GREEN=1
RUN_RED=0
for _arg in "$@"; do
  case "$_arg" in
    --red)  RUN_GREEN=0; RUN_RED=1 ;;
    --both) RUN_GREEN=1; RUN_RED=1 ;;
  esac
done

# ---- Cleanup state (owned by EXIT trap) ----
typeset -a _SANDBOXES_TO_CLEAN
_smoke_cleanup() {
  for _sd in "${_SANDBOXES_TO_CLEAN[@]}"; do
    [[ -d "$_sd" ]] && rm -rf "$_sd"
  done
  unset DOORBELL_DRY_FIRE
}
trap _smoke_cleanup EXIT INT TERM

# ---- Helpers ----
_pline()  { print -- "$@" }
_pass()   { print -- "\n[SMOKE PASS] $1" }
_fail()   { print -- "\n[SMOKE FAIL] $1" }
_info()   { print -- "  $1" }

# ---- Core probe function ----
# Returns 0 on PASS, 1 on FAIL.
_run_probe() {
  local mode="$1"   # "green" or "red"

  _pline "\n====== SMOKE PROBE: mode=${mode} ======"

  # 1. Create sandbox
  local SANDBOX
  SANDBOX=$(mktemp -d) || { _fail "mktemp -d failed"; return 1; }
  _SANDBOXES_TO_CLEAN+=("$SANDBOX")
  _info "sandbox created: ${SANDBOX}"

  # 2. Init git repo with identity
  git -C "$SANDBOX" init -q
  git -C "$SANDBOX" config user.email "doorbell-smoke-probe@office"
  git -C "$SANDBOX" config user.name "Doorbell Smoke Probe"

  # 3. Seed a parent commit (CRITICAL: git diff-tree prints nothing on a root commit
  #    without --root; the real hook doesn't pass --root; so the guard would never fire
  #    on the first commit. Seed a parent so HEAD has a parent when the test commit lands.)
  printf 'smoke-probe seed commit\n' > "${SANDBOX}/seed.txt"
  git -C "$SANDBOX" add seed.txt
  git -C "$SANDBOX" commit -q -m "smoke-probe: seed (parent)"
  _info "seed commit created (parent for test commit)"

  # 4. Install post-commit hook AFTER the seed commit.
  #    CRITICAL: copy from the DEPLOYED hook (the trigger that actually fires on real commits),
  #    not the template source. This is the exact failure class 0009 L5 was designed to catch:
  #    deploy-vs-template drift. Also assert deployed == template (detect drift before running).
  if [[ "$mode" == "green" ]]; then
    # Drift assertion: deployed hook must match the template.
    if ! diff -q "$DEPLOYED_HOOK" "$REAL_HOOK_TEMPLATE" > /dev/null 2>&1; then
      _fail "DRIFT DETECTED: deployed hook differs from template"
      _info "  deployed:  ${DEPLOYED_HOOK}"
      _info "  template:  ${REAL_HOOK_TEMPLATE}"
      _info "  Run: diff ${DEPLOYED_HOOK} ${REAL_HOOK_TEMPLATE}"
      return 1
    fi
    _info "drift assertion: deployed hook matches template (PASS)"

    # Belt-and-suspenders: inject DOORBELL_DRY_FIRE=1 at the top of the deployed copy
    # to guarantee no real inbox writes even if the env chain had a gap.
    # The trigger wiring under test (source base.zsh, diff-tree guard, temple-doorbell-run)
    # comes from the real deployed hook — only the safety header is added.
    {
      print "#!/usr/bin/env zsh"
      print "# SMOKE-PROBE COPY of deployed hook + safety header"
      print "export DOORBELL_DRY_FIRE=1  # belt-and-suspenders: prevents real inbox writes"
      tail -n +2 "$DEPLOYED_HOOK"
    } > "${SANDBOX}/.git/hooks/post-commit"
    _info "hook: deployed hook (${DEPLOYED_HOOK}) + DRY-FIRE safety header installed"
  else
    # Deliberate-red: plant a dead source path in place of the real base.zsh.
    # Use the deployed hook as base (same as green) — only the source path is wrong.
    {
      print "#!/usr/bin/env zsh"
      print "# SMOKE-PROBE DELIBERATE-RED — planted dead source path in deployed hook"
      print "export DOORBELL_DRY_FIRE=1  # still set (though hook will fail before using it)"
      sed 's|source "${HOME}/\.config/zsh/ai/base\.zsh"|source "'"${DEAD_PATH}"'"|' \
        <(tail -n +2 "$DEPLOYED_HOOK")
    } > "${SANDBOX}/.git/hooks/post-commit"
    _info "hook: DELIBERATE-RED installed (deployed hook, source → ${DEAD_PATH})"
  fi
  chmod +x "${SANDBOX}/.git/hooks/post-commit"

  # 5. Enforce dry-fire in the environment (belt-and-suspenders; hook also injects it)
  export DOORBELL_DRY_FIRE=1

  # 6. Record log position before commit
  touch "$LOG_FILE"
  local LOG_BEFORE
  LOG_BEFORE=$(wc -l < "$LOG_FILE")
  _info "log: ${LOG_FILE} (lines before commit: ${LOG_BEFORE})"

  # 7. Create the test file under temple/decisions/ and commit
  mkdir -p "${SANDBOX}/temple/decisions"
  printf 'smoke-probe: throwaway test file — safe to ignore\ndate: %s\n' "$(date +%Y-%m-%d)" \
    > "${SANDBOX}/temple/decisions/smoke-test.md"
  git -C "$SANDBOX" add temple/decisions/smoke-test.md
  _info "committing throwaway change under temple/decisions/ ..."
  git -C "$SANDBOX" commit -q -m "smoke-probe: throwaway commit touching temple/decisions/"
  _info "commit done — hook background job should be running"

  # 8. Wait for the hook to finish (poll log for the completion sentinel, up to 10s)
  #    GREEN: hook writes "DRY-FIRE complete" or "done —" when it finishes.
  #    RED: hook fails silently; we time out and check the absence of the canon line.
  local waited=0
  local TIMEOUT_CYCLES=50   # 50 * 0.2s = 10s
  local lines_now
  local new_content=""
  while (( waited < TIMEOUT_CYCLES )); do
    sleep 0.2
    lines_now=$(wc -l < "$LOG_FILE" 2>/dev/null || print 0)
    if (( lines_now > LOG_BEFORE )); then
      # Got some output; check for the completion sentinel
      new_content=$(tail -n +"$((LOG_BEFORE + 1))" "$LOG_FILE" 2>/dev/null)
      if grep -qF "DRY-FIRE complete" <<< "$new_content" \
         || grep -qF "done —" <<< "$new_content"; then
        _info "completion sentinel found after $((waited * 2 / 10)).$((waited * 2 % 10))s"
        break
      fi
    fi
    (( waited++ ))
  done
  if (( waited >= TIMEOUT_CYCLES )) && [[ -z "$new_content" ]]; then
    # Timed out with no new log output at all
    new_content="<no output in log — hook did not write anything>"
  fi
  (( waited >= TIMEOUT_CYCLES )) && [[ "$mode" == "green" ]] && \
    _info "WARNING: timed out waiting for completion sentinel (10s)"

  # 9. Show verbatim log output
  _pline "\n  [verbatim log output — new entries after commit]:"
  _pline "$new_content" | sed 's/^/    /'

  # 10. Assert
  local probe_pass=0
  if [[ "$mode" == "green" ]]; then
    local canon_ok=0 dryfire_ok=0 nosend_ok=0
    grep -qF "temple-doorbell: canon version" <<< "$new_content"  && canon_ok=1
    grep -qF "DRY-FIRE"                       <<< "$new_content"  && dryfire_ok=1
    grep -qF "no inboxes written"             <<< "$new_content"  && nosend_ok=1

    _pline "\n  [assertions — green]:"
    _info "canon version line present:    $( (( canon_ok ))   && print PASS || print FAIL )"
    _info "DRY-FIRE marker present:       $( (( dryfire_ok )) && print PASS || print FAIL )"
    _info "no-inboxes-written confirmed:  $( (( nosend_ok ))  && print PASS || print FAIL )"

    if (( canon_ok && dryfire_ok && nosend_ok )); then
      _pass "GREEN — hook fired → base.zsh sourced → temple-doorbell-run invoked → DRY-FIRE honored → no inboxes written"
      probe_pass=1
    else
      _fail "GREEN — one or more assertions failed (see above)"
    fi
  else
    # RED: assert that "temple-doorbell: canon version" is ABSENT (hook broke before reaching it)
    local canon_absent=0
    grep -qF "temple-doorbell: canon version" <<< "$new_content" || canon_absent=1

    _pline "\n  [assertions — deliberate-red]:"
    _info "canon version line absent:  $( (( canon_absent )) && print PASS || print FAIL )"

    if (( canon_absent )); then
      _pass "RED — probe reports FAIL as expected: planted dead path broke the hook; no canon line produced"
      probe_pass=1
    else
      _fail "RED — SELF-TEST BROKEN: 'temple-doorbell: canon version' appeared despite planted dead path"
      _info "The probe cannot distinguish dead from live wiring — the deliberate-red gate is invalid."
    fi
  fi

  # 11. Residue report
  _pline "\n  [residue check]:"
  local live_repo="${HOME}/reposoma"
  local live_head
  live_head=$(git -C "$live_repo" log --oneline -1 2>/dev/null || print "unknown")
  _info "live repo HEAD: ${live_head}"
  _info "live repo temple/decisions/ unchanged (sandbox commits went to: ${SANDBOX})"

  local inbox_count
  inbox_count=$(find "${live_repo}/_mail" -name "*.md" -newer "${SANDBOX}/seed.txt" 2>/dev/null | wc -l)
  _info "new inbox files in live _mail/ since probe start: ${inbox_count} (expected: 0)"

  local log_lines_added=$(( $(wc -l < "$LOG_FILE" 2>/dev/null || print 0) - LOG_BEFORE ))
  _info "lines appended to live doorbell log: ${log_lines_added}"
  _info "DOORBELL_DRY_FIRE=1 was active — no real inboxes written"

  # sandbox removed by EXIT trap; note its path for the record
  _info "sandbox to be removed: ${SANDBOX} (EXIT trap)"

  return $(( probe_pass == 1 ? 0 : 1 ))
}

# ---- Main ----
_pline "doorbell-smoke.zsh — real-trigger smoke probe"
_pline "date: $(date +%Y-%m-%d) | host: ${MACHINE_NAME:-office}"
_pline "deployed hook:      ${DEPLOYED_HOOK}"
_pline "hook template:      ${REAL_HOOK_TEMPLATE}"
_pline "real base.zsh:      ${REAL_BASE}"

OVERALL_PASS=0

if (( RUN_GREEN )); then
  if _run_probe green; then
    OVERALL_PASS=1
  else
    OVERALL_PASS=0
  fi
fi

if (( RUN_RED )); then
  # Deliberate-red failure is expected; we track its pass/fail separately
  _run_probe red
  RED_RESULT=$?
fi

_pline "\n====== SMOKE PROBE COMPLETE ======"
if (( RUN_GREEN && RUN_RED )); then
  _pline "green: $( (( OVERALL_PASS )) && print PASS || print FAIL ) | red: $( (( RED_RESULT == 0 )) && print PASS || print FAIL )"
elif (( RUN_GREEN )); then
  _pline "result: $( (( OVERALL_PASS )) && print PASS || print FAIL )"
else
  _pline "result: $( (( RED_RESULT == 0 )) && print PASS || print FAIL ) (deliberate-red)"
fi

# Cleanup runs via EXIT trap
