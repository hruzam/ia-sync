# STATUS: presence-freshness-00-precmd

```yaml
updated: 2026-09-23 (corrected before first wake)
writer: trajectory · anthropic
host: office
worktree: >
  /home/hruzam/ia-sync · main · 892e13e · dirty — SYNC_DISCIPLINE.md, pulse.md, and this bed
  (parent session's, being committed together); .dev/session/aur-php74-update/ belongs to a
  concurrent session — not ours, never stage it
gate: >
  A precmd-hooked presence-board freshness check is live and deployed on office: it silently
  detects a NEW attachment appearing at this workspace after the current shell started, without
  any manual re-check; prints exactly one quiet advisory line on the next prompt when (and only
  when) the board changed for this workspace; stays silent when it did not; is read-only against
  the board (never calls mark/unmark); adds no noticeable delay to prompt return; degrades to a
  silent no-op if its read path is unavailable; and the mechanism plus its home-parity gap are
  documented in SYNC_DISCIPLINE.md's "Presence" section.
checkpoint: >
  RUNBOOK.md authored and parked; execution has not started. No file under zsh/session/ or
  zsh/config.office.zsh has been touched by this session yet.
in_flight: none
recovery_probe: >
  Run grep -n "precmd_functions" /home/hruzam/ia-sync/zsh/session/*.zsh
  /home/hruzam/ia-sync/zsh/config.office.zsh 2>/dev/null —
  no output means execution has not begun, wake prompt-0 fresh, nothing to reconcile;
  output found means execution has begun, then run git status --short against
  zsh/session/, zsh/config.office.zsh, SYNC_DISCIPLINE.md, and journal.host-cleanup.md
  to see what is drafted but uncommitted, run zsh -n on any changed .zsh file to confirm
  it at least parses, then diff the changed repo files against their live ~/.config/zsh/
  counterparts — identical means deployed, different means drafted but not yet deployed.
  Then check journal.host-cleanup.md's newest entries and SYNC_DISCIPLINE.md's Presence
  section for whether steps 6 and 7 of prompt-0 already landed. Do not assume partial work
  is done work — reconcile against the Acceptance evidence list in RUNBOOK.md line by line.
holds: >
  Read-only against the presence board, unconditionally — the mechanism itself may never call
  mark or unmark under any code path. Never bare rb-unmark while testing, always by the exact
  id rb-mark returns — proven costly once already this parent session, five real records lost.
  Never stage anything under ~/reposoma/_active/ from this session (the five records a bare
  unmark deleted were restored by the operator via git restore, 2026-09-23). No execution on home from this session — office builds and
  verifies; home parity is a journal flag only.
next: Wake @Trajectory on prompt-0 (RUNBOOK.md) — the operator's deliberate action, on whichever
  carriage they choose.
expected: >
  A real fresh-shell trigger test, not a read-through, demonstrating the precmd hook firing
  exactly once on the next prompt after a separate-process rb-mark, staying silent when nothing
  changed, and degrading to a silent no-op when its read path is unavailable — plus
  deploy.sh --dry-run showing only the intended new or changed files, and both doc updates
  (SYNC_DISCIPLINE.md addendum, journal.host-cleanup.md home-parity flag) present on disk.
```
