#!/usr/bin/env zsh
# =============================================================================
# adr-guard.zsh — Canon-integrity gate for temple/decisions/ ADRs
# =============================================================================
# 2026-07-07 · host: ${MACHINE_NAME:-home}
# Part of 0009 L5 verify-it-fires closure — the gate the 2026-07-03 audit required.
# Doctrine: "the remedy is a gate, not prose" (0008 §7 — governance enforced by the
# harness, not the model).
#
# Two FAIL conditions checked against the staged diff vs HEAD:
#   1. Locked-ADR in-place edit — a status:LOCKED decision record has lines removed
#      or changed (not purely appended) → FAIL. Doctrine §1b: append-only, never edited.
#   2. Evidence-rot cite — any staged decisions/*.md introduces a _mail/*/inbox/
#      reference → FAIL. Those paths are gitignored + drainable — not durable evidence.
#
# Wire:  pre-commit hook (template: adr-guard.pre-commit.hook)
#        on-demand alias `adr-guard` (base.zsh PARTITION 4)
# Bypass: git commit --no-verify — a rail, not a trap (decision-0009 standing)
# Fixtures: ~/.config/zsh/ai/adr-guard.fixtures/ (natural red captures 2026-07-07)
#
# Usage:
#   zsh ~/.config/zsh/ai/adr-guard.zsh               # gate check (default / on-demand)
#   zsh ~/.config/zsh/ai/adr-guard.zsh --deliberate-red  # sandbox smoke proof (0009 L5)
# =============================================================================

# ---- Top-level cleanup (sandbox for --deliberate-red) ----
typeset -a _ADRGUARD_SANDBOXES
_adrguard_cleanup() {
  for _s in "${_ADRGUARD_SANDBOXES[@]}"; do [[ -d "$_s" ]] && rm -rf "$_s"; done
}
trap _adrguard_cleanup EXIT INT TERM

# ---- Gate state ----
_ADRGUARD_FAIL=0
_adrguard_flag() {
  print -- "\n[ADR-GUARD FAIL] $1" >&2
  _ADRGUARD_FAIL=1
}

# =============================================================================
# Check 1 — Locked-ADR in-place edit
# Scans every staged temple/decisions/00NN-*.md. If the file's HEAD version
# declares `status: LOCKED` in its first 10 lines, any removed line in the staged
# diff (grep '^-[^-]') means existing content was changed — FAIL.
# Purely appended content (amendment blocks) produces only + lines → passes.
# New files have no prior locked content to violate → skipped.
# =============================================================================
_adrguard_check_inplace() {
  local staged f removed
  staged=$(git diff --cached --name-only 2>/dev/null \
    | grep '^temple/decisions/[0-9][0-9][0-9][0-9]-.*\.md$')
  [[ -z "$staged" ]] && return 0

  while IFS= read -r f; do
    [[ -z "$f" ]] && continue
    git show "HEAD:${f}" &>/dev/null || continue       # new file — no locked content
    git show "HEAD:${f}" 2>/dev/null | head -10 \
      | grep -qiE '`?status:[[:space:]]*LOCKED' || continue  # not locked — skip
    removed=$(git diff --cached -- "$f" 2>/dev/null | grep '^-[^-]')
    if [[ -n "$removed" ]]; then
      _adrguard_flag "Locked ADR modified in-place: ${f}"
      print -- "  Removed/changed lines (first 5):" >&2
      print -- "$removed" | head -5 | sed 's/^/    /' >&2
    fi
  done <<< "$staged"
}

# =============================================================================
# Check 2 — Evidence-rot cite
# Scans every staged temple/decisions/*.md. If the diff adds a line
# (grep '^+[^+]') containing a _mail/*/inbox/ path → FAIL.
# =============================================================================
_adrguard_check_evidence_rot() {
  local staged f refs
  staged=$(git diff --cached --name-only 2>/dev/null \
    | grep '^temple/decisions/.*\.md$')
  [[ -z "$staged" ]] && return 0

  while IFS= read -r f; do
    [[ -z "$f" ]] && continue
    refs=$(git diff --cached -- "$f" 2>/dev/null \
      | grep '^+[^+]' | grep '_mail/[^/]*/inbox/')
    if [[ -n "$refs" ]]; then
      _adrguard_flag "Evidence-rot cite introduced in: ${f}"
      print -- "  New _mail/*/inbox/ references (first 5):" >&2
      print -- "$refs" | head -5 | sed 's/^/    /' >&2
    fi
  done <<< "$staged"
}

# =============================================================================
# Gate run (default mode)
# =============================================================================
_adrguard_run_gate() {
  _ADRGUARD_FAIL=0
  _adrguard_check_inplace
  _adrguard_check_evidence_rot
  if (( _ADRGUARD_FAIL )); then
    print -- "" >&2
    print -- "[ADR-GUARD] Commit BLOCKED. Resolve the violations above." >&2
    print -- "  Bypass (emergency only): git commit --no-verify" >&2
    return 1
  fi
  return 0
}

# =============================================================================
# Deliberate-red smoke proof (--deliberate-red mode)
# 0009 L5: "verify-it-fires" — the real hook fires, the real adr-guard.zsh is
# called, FAIL output is produced. Two probes, one per fail condition.
# Safety: runs entirely in a disposable sandbox temp git repo — never touches
# the live ~/reposoma tree.
# =============================================================================
_adrguard_deliberate_red() {
  local SANDBOX r1=0 r2=0 out rc

  print -- "\n====== ADR-GUARD DELIBERATE-RED SMOKE PROBE ======"
  print -- "date: $(date +%Y-%m-%d) | host: ${MACHINE_NAME:-home}"
  print -- "gate script: ${HOME}/.config/zsh/ai/adr-guard.zsh"

  SANDBOX=$(mktemp -d) || { print -- "[SMOKE FAIL] mktemp -d failed"; return 1; }
  _ADRGUARD_SANDBOXES+=("$SANDBOX")
  print -- "sandbox: ${SANDBOX}"

  git -C "$SANDBOX" init -q
  git -C "$SANDBOX" config user.email "adr-guard-smoke@home"
  git -C "$SANDBOX" config user.name "ADR Guard Smoke"

  # Seed commit so later commits have a parent (needed for correct git diff behavior)
  printf 'adr-guard smoke seed\n' > "${SANDBOX}/seed.txt"
  git -C "$SANDBOX" add seed.txt
  git -C "$SANDBOX" commit -q -m "smoke: seed (parent)"

  # Install the REAL pre-commit hook — the actual trigger under test.
  # The hook calls the real adr-guard.zsh; this is 0009 L5: "the real trigger firing."
  cat > "${SANDBOX}/.git/hooks/pre-commit" << 'HOOK'
#!/usr/bin/env zsh
# adr-guard pre-commit hook — sandbox copy for deliberate-red smoke probe
# Calls the REAL adr-guard.zsh (the live gate) — this IS the trigger under test.
zsh "${HOME}/.config/zsh/ai/adr-guard.zsh" || exit 1
HOOK
  chmod +x "${SANDBOX}/.git/hooks/pre-commit"
  print -- "hook installed: calls real adr-guard.zsh"

  # ==========================================================================
  # RED PROBE 1 — Locked-ADR in-place edit
  # ==========================================================================
  print -- "\n------ RED PROBE 1: Locked-ADR in-place edit ------"
  mkdir -p "${SANDBOX}/temple/decisions"

  # Commit a clean locked ADR (the baseline)
  cat > "${SANDBOX}/temple/decisions/0001-probe-locked.md" << 'ADR'
# Probe Locked ADR — adr-guard deliberate-red

`status: LOCKED 2026-07-07 (smoke probe — adr-guard)`
`date: 2026-07-07`

## Locked content

Original line A — must not be modified after lock.
Original line B — append-only rule applies.

## End
ADR
  git -C "$SANDBOX" add "temple/decisions/0001-probe-locked.md"
  git -C "$SANDBOX" commit -q -m "smoke: add locked ADR (version 1 — clean)"
  print -- "locked ADR committed (version 1 — clean baseline)"

  # Now modify line A in-place (the breach) and stage it
  cat > "${SANDBOX}/temple/decisions/0001-probe-locked.md" << 'ADR'
# Probe Locked ADR — adr-guard deliberate-red

`status: LOCKED 2026-07-07 (smoke probe — adr-guard)`
`date: 2026-07-07`

## Locked content

MODIFIED line A — this is the deliberate in-place edit breach.
Original line B — append-only rule applies.

## End
ADR
  git -C "$SANDBOX" add "temple/decisions/0001-probe-locked.md"
  print -- "in-place modification staged — attempting commit (FAIL expected)..."

  out=$(git -C "$SANDBOX" commit -m "smoke: attempt in-place edit of LOCKED ADR" 2>&1)
  rc=$?

  print -- "\n  [verbatim hook output]:"
  print -- "$out" | sed 's/^/    /'
  print -- "  [exit code]: ${rc}"

  if (( rc != 0 )) && print -- "$out" | grep -q 'ADR-GUARD FAIL'; then
    print -- "\n[SMOKE PASS] RED PROBE 1 — hook fired → adr-guard FAILed on in-place edit of LOCKED ADR"
    r1=1
  else
    print -- "\n[SMOKE FAIL] RED PROBE 1 — expected FAIL not produced"
    print -- "  exit=${rc}; 'ADR-GUARD FAIL' matches: $(print -- "$out" | grep -c 'ADR-GUARD FAIL')"
  fi

  # ==========================================================================
  # RED PROBE 2 — Evidence-rot cite
  # ==========================================================================
  print -- "\n------ RED PROBE 2: Evidence-rot _mail/*/inbox/ cite ------"

  # Stage a new decisions file that introduces an inbox reference
  cat > "${SANDBOX}/temple/decisions/0002-probe-evidence-rot.md" << 'ADR'
# Probe Evidence-Rot ADR — adr-guard deliberate-red

`status: DRAFT`
`date: 2026-07-07`

## Context

Evidence: _mail/houston/inbox/atlas.probe-evidence-rot.2026-07-07.md
ADR
  git -C "$SANDBOX" add "temple/decisions/0002-probe-evidence-rot.md"
  print -- "decisions file with _mail/*/inbox/ cite staged — attempting commit (FAIL expected)..."

  out=$(git -C "$SANDBOX" commit -m "smoke: attempt evidence-rot cite breach" 2>&1)
  rc=$?

  print -- "\n  [verbatim hook output]:"
  print -- "$out" | sed 's/^/    /'
  print -- "  [exit code]: ${rc}"

  if (( rc != 0 )) && print -- "$out" | grep -q 'ADR-GUARD FAIL'; then
    print -- "\n[SMOKE PASS] RED PROBE 2 — hook fired → adr-guard FAILed on evidence-rot cite"
    r2=1
  else
    print -- "\n[SMOKE FAIL] RED PROBE 2 — expected FAIL not produced"
    print -- "  exit=${rc}; 'ADR-GUARD FAIL' matches: $(print -- "$out" | grep -c 'ADR-GUARD FAIL')"
  fi

  # ==========================================================================
  # Summary
  # ==========================================================================
  print -- "\n====== DELIBERATE-RED COMPLETE ======"
  print -- "RED PROBE 1 (locked-ADR in-place edit):  $( (( r1 )) && print PASS || print FAIL )"
  print -- "RED PROBE 2 (evidence-rot cite):          $( (( r2 )) && print PASS || print FAIL )"
  print -- "sandbox: ${SANDBOX} (removed by EXIT trap)"

  (( r1 && r2 ))
  return $?
}

# =============================================================================
# Main dispatch
# =============================================================================
case "${1:-}" in
  --deliberate-red)
    _adrguard_deliberate_red
    exit $?
    ;;
  *)
    # Gate mode (default / on-demand): check staged diff vs HEAD.
    # Quick-exit if no decisions files are staged — zero overhead on every other commit.
    if ! git diff --cached --name-only 2>/dev/null | grep -q '^temple/decisions/'; then
      exit 0
    fi
    _adrguard_run_gate
    exit $?
    ;;
esac
