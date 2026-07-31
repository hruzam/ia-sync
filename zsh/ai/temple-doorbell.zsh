#!/usr/bin/env zsh
# temple-doorbell.zsh — the canon-doorbell (B)
# host: office  (MACHINE_NAME=office)
# implements: decision 0008 Stage 1 — L6 (projection-version stamp) + L7 (hook rings the doorbell)
# skeleton: the recalibration-trigger pattern (Vega's sector, gaveled 2026-06-19) re-parameterized:
#   - staleness-predicate delta: canon-version-lag (not card half-life)
#   - destination delta: stale project's own inbox (via temple-mail) not _mail/toAll/
#
# SIGNALS staleness; does NOT diff canon. Message is a pointer, never an enumeration.
# No-stamp = maximally stale = ring (bootstraps never-projected projects at zero cost).
#
# Canon version: derived from decisions/index.md (latest LOCKED date — no hand-maintained field).
# Stamp location per project: <repo-root>/.projection-stamp
#   Format: projected-from: decisions@<YYYY-MM-DD>
#   Lives at repo-root (NOT under _mail/ which is drainable — stamp must survive a mail drain).
#   Untracked by design (each host's stamp is local state, not canon).
#   Absence = stale by design — safe bootstrap.
#   The propagation pass (out of scope here) writes the real stamp after each projection run.
#
# Trigger options:
#   (1) manual: source temple-doorbell.zsh && temple-doorbell-run
#   (2) post-commit hook on temple decisions/: calls temple-doorbell-run in background
#   (3) cron: optional, not wired here
#
# Depends on: temple-project-map.zsh (P0) + temple-mail.zsh (A)

# --- Load dependencies ---
_DOORBELL_DIR="${0:h}"

if (( ${+functions[temple-project-root]} == 0 )); then
  source "${_DOORBELL_DIR}/temple-project-map.zsh" || {
    print -u2 "temple-doorbell: cannot load temple-project-map.zsh"
    return 1
  }
fi

if (( ${+functions[temple-mail]} == 0 )); then
  source "${_DOORBELL_DIR}/temple-mail.zsh" || {
    print -u2 "temple-doorbell: cannot load temple-mail.zsh"
    return 1
  }
fi

# --- Derive current canon version from decisions/index.md ---
# Parses "LOCKED YYYY-MM-DD" lines and returns the latest (lexicographic max = date max).
_doorbell_canon_version() {
  local index_file="${TEMPLE_PROJECT_MAP[reposoma]}/temple/decisions/index.md"
  if [[ ! -f "$index_file" ]]; then
    print -u2 "temple-doorbell: cannot find decisions/index.md at '$index_file'"
    return 1
  fi
  # Extract all "LOCKED YYYY-MM-DD" strings, take the lexicographically last date
  local canon_date
  canon_date="$(grep -oP 'LOCKED \K\d{4}-\d{2}-\d{2}' "$index_file" | sort | tail -1)"
  if [[ -z "$canon_date" ]]; then
    print -u2 "temple-doorbell: could not extract a LOCKED date from decisions/index.md"
    return 1
  fi
  print -- "$canon_date"
}

# --- Read a project's current stamp ---
# Returns the date portion of "projected-from: decisions@<date>" or empty string if absent/unparseable.
_doorbell_read_stamp() {
  local project="$1"
  local root="${TEMPLE_PROJECT_MAP[$project]}"
  if [[ -z "$root" ]]; then
    print -u2 "temple-doorbell: unknown project '$project'"
    return 1
  fi
  local stamp_file="${root}/.projection-stamp"
  if [[ ! -f "$stamp_file" ]]; then
    # No stamp = maximally stale
    print ""
    return 0
  fi
  local stamp_date
  stamp_date="$(grep -oP 'projected-from:\s+decisions@\K\d{4}-\d{2}-\d{2}' "$stamp_file" 2>/dev/null | head -1)"
  print -- "${stamp_date:-}"
}

# --- Update a project's stamp ---
# Writes "projected-from: decisions@<date>" to <repo>/.projection-stamp
_doorbell_write_stamp() {
  local project="$1" canon_date="$2"
  local root="${TEMPLE_PROJECT_MAP[$project]}"
  cat > "${root}/.projection-stamp" <<STAMP_EOF
projected-from: decisions@${canon_date}
updated: $(date +%Y-%m-%d)
host: ${MACHINE_NAME:-office}
STAMP_EOF
}

# --- Main doorbell run ---
temple-doorbell-run() {
  local canon_date
  canon_date="$(_doorbell_canon_version)" || return 1

  local date_stamp
  date_stamp="$(date +%Y-%m-%d)"

  print "temple-doorbell: canon version = decisions@${canon_date}"
  print "temple-doorbell: run date = ${date_stamp}"

  local rung=0 skipped=0
  local project stamp_date stamp_label body

  # Iterate projects — skip reposoma (it IS the canon source, does not project from itself)
  for project in "${(@k)TEMPLE_PROJECT_MAP}"; do
    [[ "$project" == "reposoma" ]] && continue

    stamp_date="$(_doorbell_read_stamp "$project")"

    if [[ -n "$stamp_date" && "$stamp_date" == "$canon_date" ]]; then
      print "  [$project] up-to-date (stamp=$stamp_date) — no ring"
      (( skipped++ ))
      continue
    fi

    [[ -z "$stamp_date" ]] && stamp_label="<none>" || stamp_label="decisions@${stamp_date}"

    print "  [$project] stale (stamp=${stamp_label}, canon=decisions@${canon_date}) — ringing"

    # Build notification body — pointer only, never a diff
    body="$(cat <<BODY_EOF
Temple canon has advanced to decisions@${canon_date}.

Project \`${project}\` was last projected from: ${stamp_label}

Action required: run the propagation pass to re-align this project's agent surfaces with current canon.
Pass prompt: \`temple/tools/propagation-pass.prompt.draft.md\` (relative to the temple repo)

This message is a SIGNAL only. The doorbell does not enumerate what changed.
Run the propagation pass to get the diff.

host: ${MACHINE_NAME:-office}
date: ${date_stamp}
BODY_EOF
)"

    if [[ "${DOORBELL_DRY_FIRE:-0}" == "1" ]]; then
      # Dry-fire mode: compute who would be rung but write nothing to any inbox.
      # Emit the would-deliver record to stdout (captured by hook → log, or by probe).
      print "  [$project] DRY-FIRE: would-ring (stamp=${stamp_label}, canon=decisions@${canon_date})"
      print "  [$project] DRY-FIRE: would-send to <${project}:houston> subject=canon-doorbell"
    else
      echo "$body" | temple-mail "${project}:houston" "canon-doorbell" - --from "temple:houston"
    fi
    (( rung++ ))
  done

  if [[ "${DOORBELL_DRY_FIRE:-0}" == "1" ]]; then
    print "temple-doorbell: DRY-FIRE complete — would-ring=$rung skipped=$skipped (no inboxes written)"
  else
    print "temple-doorbell: done — rung=$rung skipped=$skipped"
  fi
}
