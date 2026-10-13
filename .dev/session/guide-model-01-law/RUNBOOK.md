# RUNBOOK: guide-model-01-law

```yaml
goal: >
  Establish a small, durable collaboration program through which Majkee can describe
  work turns and myShell can keep the active cross-runbook backlog legible without
  duplicating any owning bed's state.
gate: >
  PROGRAM.md contains an operator-usable intake method and its first reconciled index
  points to every work turn supplied for this session, with each item's owning source
  explicit and no competing next action.
participant_1: [myShell, {brand: Codex, model: GPT-5, effort: adaptive}, host: office, role: status_owner and backlog steward]
participant_2: [majkee, {brand: human, model: none, effort: n/a}, host: office, role: operator and source of work-turn accounts]
participant_3: [Astrobley, {brand: Codex, model: gpt-6.1-sol, effort: high}, host: office, role: cSharp reasoning head and plan author]
status_owner: myShell
head_note: cSharp — Astrobley owns the bounded guide-model plan; myShell owns STATUS and integration.
observations_read: none exist
```

## Why this session exists

Majkee is simultaneously carrying JEV work, germline/Nablarva work, and this fourth
day-square chapter. This bed supplies a lightweight administrative background: it
receives concise accounts of completed or interrupted work turns, preserves their
authoritative pointers, and prepares narrow evidence requests or delegated reads.

## Fixed facts

- Each owning bed's `STATUS.md` remains the sole authority for its present state and
  next action. This program only indexes it.
- JEV and germline/Nablarva remain separate scopes. No change to either is implied by
  adding an item here.
- Delegated readers are bounded, read-only by default, and must return paths and
  observed evidence. myShell checks cited artifacts before using their conclusions.
- Astrobley is the required cSharp reasoning head. myShell remains status owner and
  steward; Astrobley returns a cited plan and does not gavel or edit canon.
- `PROGRAM.md` is stable process plus a cross-scope index; it must not restate a
  RUNBOOK, hold mutable bed state, or prescribe an owning bed's next action.

## prompt-0 — myShell

```text
Work only in /home/hruzam/ia-sync/.dev/session/guide-model-01-law/ unless an
explicitly named source needs read-only inspection. Receive Majkee's work-turn
accounts, update PROGRAM.md only with concise source pointers, evidence, ownership,
and open questions, and keep STATUS.md's single next action current. Do not alter
JEV or germline/Nablarva state, deploy, commit, push, or infer completion from a
delegated report without checking the named artifact. Do not claim the Astrobley head
role or start execution before the real Astrobley session is resumed and bound.
```

## prompt-1 — majkee

```text
Describe a recent work turn in plain language: scope/bed, what changed or was
learned, durable evidence or path, what remains uncertain, and any desired follow-up.
myShell will turn it into a concise cross-scope index entry without changing the
owning bed's STATUS.md.
```

## Known constraints + destructive holds

- Preserve the pre-existing dirty worktree; it belongs to active work outside this bed.
- Do not run deploy, commit, push, pull, tunnel binding, or external calls under this
  session unless Majkee explicitly extends its authority.
- Do not create a replacement journal or a second status surface for another bed.

## Acceptance evidence

- `PROGRAM.md` has a clear intake and indexing contract.
- Each supplied work turn has an owning source pointer and evidence or an explicit
  unknown; none claims to update another bed's `next:`.

## References

- `/home/hruzam/reposoma/raw.guides/runbook/GUIDE.md` — RUNBOOK/session boundary.
- `/home/hruzam/reposoma/raw.guides/status/GUIDE.md` — present-tense status law.
- `/home/hruzam/reposoma/raw.guides/guide-writing/GUIDE.md` — guide-model law.
- `/home/hruzam/reposoma/raw.guides/guide-writing/res/slug-directories.md` — substrate seam.
- `/home/hruzam/reposoma/.majkee/journal/2026-10-13.md` — day-square scope boundary.

## What this session deliberately does not do

- Implement, activate, or advance the JEV tunnel.
- Implement germline/Nablarva work or modify its session state.
- Author or change a temple guide without a separately scoped guide-writing task.
