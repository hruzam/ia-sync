#!/usr/bin/env zsh
# temple-transport-selftest.zsh — end-to-end self-test of the temple transport family
# host: office  (MACHINE_NAME=office)
# tests: temple-project-map.zsh · temple-mail.zsh · temple-doorbell.zsh
#        temple-mail-inbox.zsh
# (temple-recalibration leg removed — superseded by ai/harness-check, 0009 step 5)
#
# ISOLATION RULE: zero writes to any real project tree.
# Checks 2-4 run inside subshells with a fully-overridden TEMPLE_PROJECT_MAP
# that points exclusively at mktemp sandbox dirs. Traps clean up on subshell exit.
#
# Usage: zsh ~/.config/zsh/ai/temple-transport-selftest.zsh
# Exit: 0 if all checks pass, 1 if any fail.

# ---------------------------------------------------------------------------
# Config — no sudo, no third-party tools, no ~/
# ---------------------------------------------------------------------------
_ZSH_CFG="/home/hruzam/.config/zsh"
_AI_DIR="${_ZSH_CFG}/ai"
_MAP_FILE="${_AI_DIR}/temple-project-map.zsh"
_MAIL_FILE="${_AI_DIR}/temple-mail.zsh"
_DOORBELL_FILE="${_AI_DIR}/temple-doorbell.zsh"
_INBOX_FILE="${_AI_DIR}/temple-mail-inbox.zsh"

# ---------------------------------------------------------------------------
# Color / result tracking — no set -e; checks return 0/1 manually
# ---------------------------------------------------------------------------
_GREEN='\033[0;32m'
_RED='\033[0;31m'
_NC='\033[0m'

typeset -a _RESULTS _LABELS
_RESULTS=()
_LABELS=()

_record() {
  local label="$1" result="$2"   # result: 0=pass, nonzero=fail
  _LABELS+=("$label")
  _RESULTS+=("$result")
}

# ---------------------------------------------------------------------------
# CHECK 1 — P0 resolves every registry project (read-only; real map)
# ---------------------------------------------------------------------------
_check_p0() {
  source "$_MAP_FILE" || { print "[check1] cannot source $_MAP_FILE"; return 1; }

  local all_ok=1
  for project in "${(@k)TEMPLE_PROJECT_MAP}"; do
    local root
    root="$(temple-project-root "$project" 2>&1)"
    local rc=$?
    if (( rc != 0 )) || [[ -z "$root" ]]; then
      print "[check1] FAIL: temple-project-root '$project' → rc=$rc output='$root'"
      all_ok=0
    else
      print "[check1] OK: $project → $root"
    fi
  done

  return $(( all_ok == 0 ? 1 : 0 ))
}

# ---------------------------------------------------------------------------
# CHECK 2 — A: mail round-trip, sandbox only
# ---------------------------------------------------------------------------
_check_mail_roundtrip() {
  (
    local sandbox
    sandbox="$(mktemp -d /tmp/selftest-mail.XXXXXX)"
    trap 'rm -rf "$sandbox"' EXIT

    # Build minimal sandbox dirs — all projects map to non-existent stubs except
    # the destination we actually send to. We need piql.dev dir so temple-project-root
    # returns success.
    local sb_piql="${sandbox}/piql"
    local sb_reposoma="${sandbox}/reposoma"
    mkdir -p "$sb_piql" "$sb_reposoma"

    # Source map first, then override the full array
    source "$_MAP_FILE"
    typeset -gA TEMPLE_PROJECT_MAP
    TEMPLE_PROJECT_MAP=(
      [reposoma]="$sb_reposoma"
      [subai.devenv]="${sandbox}/subai"
      [reposoma.devenv]="${sandbox}/reposoma.devenv"
      [freya.devstudio]="${sandbox}/freya"
      [piql.dev]="$sb_piql"
      [vacuole]="${sandbox}/vacuole"
    )
    # Create stub dirs so temple-project-root passes the -d check
    mkdir -p "${sandbox}/subai" "${sandbox}/reposoma.devenv" "${sandbox}/freya" "${sandbox}/vacuole"

    # Source mail (guard sees temple-project-root exists; skips map re-source)
    source "$_MAIL_FILE"

    # Send a test mail to piql.dev:houston from temple:houston
    echo "selftest round-trip body" | temple-mail "piql.dev:houston" "selftest-roundtrip" - --from "temple:houston"
    local send_rc=$?
    if (( send_rc != 0 )); then
      print "[check2] FAIL: temple-mail returned rc=$send_rc"
      exit 1
    fi

    # Expected inbox path
    local today
    today="$(date +%Y-%m-%d)"
    local expected="${sb_piql}/_mail/houston/inbox/houston.selftest-roundtrip.${today}.md"

    if [[ ! -f "$expected" ]]; then
      print "[check2] FAIL: expected inbox file not found: $expected"
      exit 1
    fi

    # No sent-copy should exist anywhere in sender's (reposoma) tree
    local sent_count
    sent_count="$(find "$sb_reposoma" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')"
    if (( sent_count > 0 )); then
      print "[check2] FAIL: unexpected files found in sender tree: $sent_count"
      exit 1
    fi

    print "[check2] OK: delivered to $expected; no sent-copy in sender tree"
    exit 0
  )
}

# ---------------------------------------------------------------------------
# CHECK 3 — B: doorbell staleness discriminator (sandbox only)
# ---------------------------------------------------------------------------
_check_doorbell_discriminator() {
  (
    local sandbox
    sandbox="$(mktemp -d /tmp/selftest-doorbell.XXXXXX)"
    trap 'rm -rf "$sandbox"' EXIT

    local sb_reposoma="${sandbox}/reposoma"
    local sb_stale="${sandbox}/stale_project"
    local sb_fresh="${sandbox}/fresh_project"
    mkdir -p "$sb_reposoma" "$sb_stale" "$sb_fresh"

    # Synthetic decisions/index.md with a fixed LOCKED date
    local canon_date="2026-06-25"
    mkdir -p "${sb_reposoma}/temple/decisions"
    cat > "${sb_reposoma}/temple/decisions/index.md" <<EOF
# Decisions

| # | Lock | Status |
|---|------|--------|
| 0001 | Test lock alpha | LOCKED 2026-06-10 |
| 0002 | Test lock beta  | LOCKED ${canon_date} |
EOF

    # fresh_project has a stamp matching canon_date — should NOT be rung
    cat > "${sb_fresh}/.projection-stamp" <<EOF
projected-from: decisions@${canon_date}
updated: ${canon_date}
host: office
EOF

    # stale_project has NO stamp — maximally stale, should be rung

    # Source map and override fully
    source "$_MAP_FILE"
    typeset -gA TEMPLE_PROJECT_MAP
    TEMPLE_PROJECT_MAP=(
      [reposoma]="$sb_reposoma"
      [stale_project]="$sb_stale"
      [fresh_project]="$sb_fresh"
    )

    # Source dependencies in order (guards check for temple-project-root; already loaded)
    source "$_MAIL_FILE"
    source "$_DOORBELL_FILE"

    # Run the doorbell; capture output
    local doorbell_out
    doorbell_out="$(temple-doorbell-run 2>&1)"
    local db_rc=$?
    print "[check3] doorbell output:\n$doorbell_out"

    if (( db_rc != 0 )); then
      print "[check3] FAIL: temple-doorbell-run returned rc=$db_rc"
      exit 1
    fi

    # stale_project should have received a mail
    local today
    today="$(date +%Y-%m-%d)"
    local stale_inbox="${sb_stale}/_mail/houston/inbox"
    local stale_mail_count
    stale_mail_count="$(find "$stale_inbox" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')"

    if (( stale_mail_count == 0 )); then
      print "[check3] FAIL: stale_project should have received a doorbell mail but got none"
      exit 1
    fi

    # fresh_project should NOT have received a mail
    local fresh_inbox="${sb_fresh}/_mail/houston/inbox"
    local fresh_mail_count
    fresh_mail_count="$(find "$fresh_inbox" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')"

    if (( fresh_mail_count > 0 )); then
      print "[check3] FAIL: fresh_project should NOT have received a doorbell mail but got $fresh_mail_count"
      exit 1
    fi

    # Confirm no doorbell mail appeared in any REAL project _mail tree (not sandbox)
    # Strategy: verify no sandbox path escaped into real trees by checking that every
    # delivered file is under $sandbox (not under /home/hruzam/reposoma or other real dirs).
    # We grep the doorbell output for "delivered →" lines and check each path.
    local delivered_path isolation_ok=1
    while IFS= read -r line; do
      if [[ "$line" == *"delivered →"* ]]; then
        delivered_path="${line##*delivered → }"
        if [[ "$delivered_path" != "${sandbox}"/* ]]; then
          print "[check3] FAIL: delivered path is outside sandbox: $delivered_path"
          isolation_ok=0
        fi
      fi
    done <<< "$doorbell_out"
    if (( isolation_ok == 0 )); then
      exit 1
    fi

    print "[check3] OK: stale_project rung ($stale_mail_count mail), fresh_project skipped"
    exit 0
  )
}

# ---------------------------------------------------------------------------
# CHECK 4 — read-side: inbox + toAll surface (sandbox only)
# ---------------------------------------------------------------------------
_check_inbox_readside() {
  (
    local sandbox
    sandbox="$(mktemp -d /tmp/selftest-inbox.XXXXXX)"
    trap 'rm -rf "$sandbox"' EXIT

    local sb_reposoma="${sandbox}/reposoma"
    local sb_piql="${sandbox}/piql"
    mkdir -p "$sb_reposoma" "$sb_piql"

    # Plant a direct inbox item for piql.dev:houston
    local today
    today="$(date +%Y-%m-%d)"
    local inbox_dir="${sb_piql}/_mail/houston/inbox"
    mkdir -p "$inbox_dir"
    cat > "${inbox_dir}/houston.test-scope.${today}.md" <<EOF
---
from: temple:houston
to: piql.dev:houston
scope: test-scope
date: ${today}
---
inbox test item
EOF

    # Plant a toAll item in reposoma (the global broadcast location)
    local toall_dir="${sb_reposoma}/_mail/toAll/inbox"
    mkdir -p "$toall_dir"
    cat > "${toall_dir}/recalibration-${today}.md" <<EOF
---
scope: recalibration-reminder
date: ${today}
---
toAll test broadcast
EOF

    # Source map and override
    source "$_MAP_FILE"
    typeset -gA TEMPLE_PROJECT_MAP
    TEMPLE_PROJECT_MAP=(
      [reposoma]="$sb_reposoma"
      [subai.devenv]="${sandbox}/subai"
      [reposoma.devenv]="${sandbox}/reposoma.devenv"
      [freya.devstudio]="${sandbox}/freya"
      [piql.dev]="$sb_piql"
      [vacuole]="${sandbox}/vacuole"
    )
    mkdir -p "${sandbox}/subai" "${sandbox}/reposoma.devenv" "${sandbox}/freya" "${sandbox}/vacuole"

    source "$_INBOX_FILE"

    local inbox_out
    inbox_out="$(temple-mail-inbox "piql.dev:houston" 2>&1)"
    local inbox_rc=$?

    print "[check4] inbox output:\n$inbox_out"

    if (( inbox_rc != 0 )); then
      print "[check4] FAIL: temple-mail-inbox returned rc=$inbox_rc"
      exit 1
    fi

    if [[ -z "$inbox_out" ]]; then
      print "[check4] FAIL: temple-mail-inbox produced no output (expected inbox + toAll items)"
      exit 1
    fi

    # Check inbox item appears
    if ! print -- "$inbox_out" | grep -q "houston.test-scope.${today}.md"; then
      print "[check4] FAIL: inbox item not found in output"
      exit 1
    fi

    # Check toAll item appears
    if ! print -- "$inbox_out" | grep -q "recalibration-${today}.md"; then
      print "[check4] FAIL: toAll broadcast not found in output"
      exit 1
    fi

    print "[check4] OK: inbox item and toAll broadcast both surface"
    exit 0
  )
}

# ---------------------------------------------------------------------------
# Run all checks
# ---------------------------------------------------------------------------
# Create a marker file at script start so we can detect any writes to real
# project trees that happened DURING this run (vs pre-existing files).
_selftest_marker="$(mktemp /tmp/selftest-marker.XXXXXX)"
trap 'rm -f "$_selftest_marker"' EXIT

print "temple-transport-selftest: starting"
print "-----------------------------------------------"

print "\n--- CHECK 1: P0 resolves every registry project ---"
_check_p0
_record "P0: all 6 projects resolve" $?

print "\n--- CHECK 2: A — mail round-trip ---"
_check_mail_roundtrip
_record "A: message round-trip clean" $?

print "\n--- CHECK 3: B — staleness discriminator ---"
_check_doorbell_discriminator
_record "B: staleness discriminator" $?

print "\n--- CHECK 4: read-side — inbox + toAll surface ---"
_check_inbox_readside
_record "read-side: inbox + toAll surface" $?

# ---------------------------------------------------------------------------
# Print result matrix
# ---------------------------------------------------------------------------
print "\n==============================================="
print "temple-transport-selftest: results"
print "==============================================="

local overall=0
for i in {1..${#_LABELS[@]}}; do
  local label="${_LABELS[$i]}"
  local result="${_RESULTS[$i]}"
  if (( result == 0 )); then
    print "${_GREEN}[PASS]${_NC} ${label}"
  else
    print "${_RED}[FAIL]${_NC} ${label}"
    overall=1
  fi
done

print "==============================================="

# Confirm real project trees are clean
print "\n--- Isolation verification ---"
local real_dirty
real_dirty="$(git -C /home/hruzam/reposoma status --porcelain 2>/dev/null)"
if [[ -z "$real_dirty" ]]; then
  print "git status: clean (no writes to reposoma)"
else
  print "WARNING: reposoma has uncommitted changes (pre-existing or isolation breach):"
  print "$real_dirty"
fi

# Check for any .md written in real _mail dirs DURING THIS RUN
# We use the marker file created at script start to detect post-start writes.
local real_mail_new
real_mail_new="$(find /home/hruzam/reposoma/_mail -newer "$_selftest_marker" -name "*.md" 2>/dev/null | grep -v '^$')"
if [[ -z "$real_mail_new" ]]; then
  print "real _mail scan: no new files written in real reposoma _mail during this run"
else
  print "WARNING: files written in real _mail during this run:"
  print "$real_mail_new"
fi

print "==============================================="

exit $overall
