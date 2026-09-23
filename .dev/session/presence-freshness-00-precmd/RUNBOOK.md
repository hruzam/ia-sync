# RUNBOOK: presence-freshness-00-precmd

```yaml
goal: >
  Close the concrete gap this session's own investigation found: the presence board
  (~/reposoma/_active/) is only ever checked once, at orientation — a seat that attaches to a
  workspace AFTER another session has already started goes unnoticed by the running session for
  the rest of its life. The fix stays native and advisory (no daemon, no git hook — an attach or
  detach is a plain file write that no hook sees until someone commits), matching the board's own
  gaveled "informs, never blocks" law.
gate: >
  A precmd-hooked presence-board freshness check is live and deployed on office: it silently
  detects a NEW attachment appearing at this workspace after the current shell started, without
  any manual re-check; prints exactly one quiet advisory line on the next prompt when (and only
  when) the board changed for this workspace; stays silent when it did not; is read-only against
  the board (never calls mark/unmark); adds no noticeable delay to prompt return; degrades to a
  silent no-op if its read path is unavailable; and the mechanism plus its home-parity gap are
  documented in SYNC_DISCIPLINE.md's "Presence" section.
participant_1: [trajectory, {brand: anthropic, model: claude-opus (operator's choice — record exact version at execution), effort: high}, host: office, role: sole executor — designs, writes, verifies, and reports the mechanism; single seat, no BUS needed]
status_owner: trajectory
schema_note: runbook/GUIDE.md verified 2026-09-17 · status/GUIDE.md gaveled 2026-08-27
```

## Why this session exists

Opened live, inside a `/runbook`-posture pause of an ia-sync maintenance session. Across that
session: (1) a `precmd`-style live re-check was proposed as the right-sized answer to a real,
separately-diagnosed gap in the presence board's usage pattern — "checked once at start, never
again" — after three observed same-session collisions on shared root files (`pulse.md`,
`journal.host-cleanup.md`, `AGENTS.md`); (2) while verifying the board's mechanics before
documenting them, a bare `rb-unmark` (no id argument) detached 5 unrelated legitimate
attachments in one shot — proof, not theory, that this mechanism has sharp edges worth a real
session rather than an inline patch. The operator asked for research and proposals rather than
immediate implementation, weighed a full automatic-worktree "agentive framework" against this
narrower fix, and leaned toward the narrower one. This session is that fix, done properly: a real
trigger test, not a read-through, matching this repo's own 0009 L5 verify-real-trigger culture.

## Fixed facts

- `~/reposoma/_active/` **IS git-tracked** in reposoma (verified 2026-09-23, `git ls-files
  _active/` lists the records; this line was first authored as "not tracked" — a misread of that
  same command's output, corrected before any execution). Consequences: records travel between
  hosts via reposoma commits, and a detach shows up as a git deletion (which is how the parent
  session's accidental bare-unmark was caught). Still no git-hook trigger: attach/detach is a
  plain file write, and a hook fires only on commit, not on the write. The mechanism must be a
  shell-native, check-on-prompt read of the files on disk.
- The board's law (`~/reposoma/raw.guides/runbook/res/presence-board.md`, gaveled 2026-09-09) is
  **advisory only** — "never commands or authorizes... resource lock... prune... workspace
  access." The new mechanism must only ever print; it must never block, wait, or refuse anything.
- `rb-mark` / `rb-unmark` / `rb-board` already exist and work
  (`~/ia-sync/zsh/session/board.zsh` → `~/ia-sync/zsh/session/runbook.py board`). Reuse this read
  path — do not hand-parse `~/reposoma/_active/*.md` again.
- **Safety fact, proven live 2026-09-22, not theoretical:** bare `rb-unmark` (no id) detaches
  EVERY attachment sharing the caller's default seat/host, not just the caller's own — this is
  documented behavior ("no arg = all own on this machine"), and every record on this board
  currently shares one default seat. The new mechanism is **read-only** against the board — it
  must never call `mark` or `unmark` itself, under any code path.
- `precmd_functions` (zsh's native per-prompt hook array) is **not used anywhere in this config
  today** (verified 2026-09-22, repo-wide grep, zero hits). This will be the first use of that
  mechanism here — there is no existing convention to extend, so register it idempotently
  (guard against double-registration if `config.zsh` is re-sourced).
- The existing startup headers (`_ts_header`, `_dash_header`,
  `/home/hruzam/ia-sync/zsh/config.office.zsh:197-198`) run **once, at shell open**, called
  directly at the end of `config.office.zsh` — not via `precmd_functions`. Contrast with this;
  do not copy that pattern, since this mechanism needs to fire on every prompt, not once.
- `session/base.zsh` already wires `session/board.zsh` (P3) as the presence-board engine home —
  the natural place to add this, unless the executor finds a concrete reason otherwise (state it
  in STATUS if so).
- This repo's own working-session steps (`SYNC_DISCIPLINE.md`) are: pull → edit → dry-run deploy
  → deploy → verify live → commit → push. This session follows them through "verify live"; commit
  and push are the operator's call, not automatic (matches how every prior change this parent
  session made was handled).

## prompt-0 — trajectory (sole executor · status_owner)

```text
You are @Trajectory, sole executor and status_owner of session presence-freshness-00-precmd.
Read /home/hruzam/ia-sync/.dev/session/presence-freshness-00-precmd/RUNBOOK.md in full, then
STATUS.md, before writing anything.

1. Design the check: reuse the existing read path
   (/home/hruzam/ia-sync/zsh/session/board.zsh's `_rb_board_py` → `runbook.py board`) rather than
   re-parsing ~/reposoma/_active/ by hand. Cache the set of attachment ids seen for the CURRENT
   workspace at last check (machine-local state only — never synced/committed, matching how
   session/base.zsh already treats own-attachment memory at ~/.local/state/session-board/). On
   each precmd: diff current ids for this workspace against the cache; print exactly one quiet
   line only when there are NEW ids since last check; update the cache; stay silent otherwise.
2. This is the FIRST use of `precmd_functions` in this config (RUNBOOK "Fixed facts") — register
   idempotently. Contrast with, do not copy, the startup-only `_ts_header`/`_dash_header` pattern
   (/home/hruzam/ia-sync/zsh/config.office.zsh:197-198).
3. Wire it from /home/hruzam/ia-sync/zsh/session/base.zsh, the existing presence-board scope —
   or state plainly in STATUS why a different home was chosen.
4. Verify with a REAL trigger, not a read-through (0009 L5 discipline — this parent session used
   it throughout, e.g. planting a syntax error to prove a `zsh -n` gate actually fires): open a
   fresh shell; from a SEPARATE shell or process, `rb-mark` a new attachment at this workspace;
   confirm the ORIGINAL shell's next prompt prints exactly one quiet line, unprompted, with no
   manual `rb-board` call; confirm a control run (nothing changed) prints nothing; confirm a
   broken/unavailable `runbook.py` degrades to a silent no-op, never a blocked or broken prompt.
   Clean up any test attachment with a TARGETED `rb-unmark <exact-id>` — never bare `rb-unmark`
   (RUNBOOK "Fixed facts" — this is not optional, it has already cost 5 real records once).
5. `bash /home/hruzam/ia-sync/deploy.sh --dry-run` then `deploy.sh` — verify live on office.
6. Add a short addendum to /home/hruzam/ia-sync/SYNC_DISCIPLINE.md's "Presence — even for
   non-session, direct-edit work" section pointing at the new mechanism (point, do not duplicate
   the design — that lives in the code + this RUNBOOK).
7. Flag the home-parity gap in /home/hruzam/ia-sync/journal.host-cleanup.md — office cannot
   execute home's side (config.home.zsh is home-owned, SYNC_DISCIPLINE.md ownership rules).
8. Do NOT `git commit` or `git push` without an explicit operator ask — deploying for verification
   is expected and normal (SYNC_DISCIPLINE.md); matches how this parent session handled every
   prior change.

Done-when: the gate (RUNBOOK.md, verbatim) is met and evidence for every "Acceptance evidence"
row below is on disk or in the report. Return path: rewrite STATUS.md to the closing snapshot;
report directly to the operator (no BUS — single seat).
```

## Known constraints + destructive holds

- Read-only against the presence board, unconditionally — no code path in this mechanism may
  call `mark` or `unmark`. Testing it still requires real `rb-mark`/targeted `rb-unmark` calls
  from the executor's own shell, per prompt-0 step 4 — that is the executor testing the board,
  not the mechanism touching it.
- The 5 presence records deleted by the parent session's bare `rb-unmark` sit as uncommitted
  deletions in reposoma's working tree — an open operator decision (`git restore` them, or commit
  the deletions deliberately). Not this session's to resolve: never stage or commit anything under
  `~/reposoma/_active/` from this session.
- **Concurrency guard — multiple local shells.** Several interactive shells on one host each run
  the precmd check. If the "last seen" cache is a shared file, concurrent read-modify-write can
  race; if it is shell-local, every new shell reports all existing attachments as new on its
  first prompt. The executor must pick one deliberately and prove it: no false-positive burst on
  shell open, and no lost or duplicated notice when two shells prompt at nearly the same time
  (write to a temp file, then atomic `mv`, is the minimum for a shared cache).
- No change to `~/reposoma/raw.guides/runbook/res/presence-board.md` (temple law) — this session
  builds a consumer of the existing law, not a revision to it.
- No home-host execution from this session — office builds and verifies; home-parity is a
  journal flag only, picked up by a home seat later (established pattern this parent session
  used for every prior change).
- No touch to `~/ia-sync/zsh/ai/base.zsh`'s already-tracked dead PARTITION 9 line — unrelated,
  separate, already-deferred item (needs its own temple gate; noted in `zsh/AGENTS.md`).
- No full automatic worktree / "agentive framework" work — explicitly parked by the operator as
  a separate, unopened concern (see "What this session deliberately does not do").
- `ai/base.zsh`, `ai/temple-*.zsh`, `ai/temple-*.hook`, `ai/adr-guard.*` remain temple-gated
  (`zsh/CLAUDE.md` dev rule 2) — this session's own deliverable lives in `session/`, not `ai/`,
  so this should not be reachable, but flag immediately if it turns out otherwise.

## Acceptance evidence

- A real fresh-shell trigger test on disk or in the report: shell A running, shell B marks a new
  attachment at this workspace, shell A's next prompt prints the advisory line unprompted.
- A control run: nothing changed → nothing printed, on disk or in the report.
- A degrade-gracefully check: read path unavailable → silent no-op, shell still boots and prompts
  normally, on disk or in the report.
- A multi-shell check: two shells open, a new attachment appears, each shell reports it once;
  opening a third shell produces no burst of stale "new" notices.
- `deploy.sh --dry-run` and `deploy.sh` output showing only the intended files, plus a `diff`
  confirming live matches repo (the verification shape this parent session used throughout).
- `SYNC_DISCIPLINE.md` "Presence" section carries a short, accurate addendum.
- `journal.host-cleanup.md` carries the home-parity flag.

## References

- `~/reposoma/raw.guides/runbook/res/presence-board.md` — the law this mechanism consumes
- `~/ia-sync/zsh/session/board.zsh` — existing presence-board engine; reuse its read path
- `~/ia-sync/zsh/session/runbook.py` (`board` subcommand) — the actual parser/renderer to call
- `~/ia-sync/zsh/session/base.zsh` — scope signpost; likely wiring point (PARTITION 3 is board.zsh)
- `~/ia-sync/SYNC_DISCIPLINE.md` "Presence — even for non-session, direct-edit work" — the doc
  this session's mechanism extends
- `~/ia-sync/zsh/config.office.zsh:197-198` — the startup-only header pattern to contrast against
- `~/ia-sync/journal.host-cleanup.md` — where to flag the home-parity gap
- `~/reposoma/raw.guides/runbook/GUIDE.md` · `status/GUIDE.md` — the law this RUNBOOK/STATUS pair follows

## What this session deliberately does not do

- Build any full automatic worktree orchestration ("agentive framework": auto-spin-per-task,
  measure, merge/select) — the operator was explicitly wary of this as new-canon-with-chaos-risk;
  it is parked, not refused, and would need its own session if ever pursued.
- Formalize a documented "reach for a manual worktree when work looks heavy/collision-prone"
  convention — a smaller, separate, optional addition the parent session floated; not this gate.
- Modify `res/presence-board.md` itself, or any other temple-owned canon.
- Decide or act on the 5 presence-board records deleted earlier in the parent session — that is
  the operator's call, outside this gate.
- Touch anything under `zsh/ai/` beyond reading it for reference (this deliverable lives in
  `zsh/session/`).
- Execute anything on home — journal flag only.
