---
name: program-pulse
description: Invoke as /program-pulse. Drive the octopus task-line buffer (program.pulse.md) — add-to-line (deposit issued tasks), pull-from-line (claim a task to run), and reconcile (archive/park at close). The head's and Vara's procedure for the shared task buffer per decision 0012. Use when planning work into the buffer, dispatching from it, or closing a run.
---

I am the procedure for the **program-pulse buffer** (`program.pulse.md`) — the octopus
task-line. I give the head and @Vara one correct way to read and write it.

**Authority:** decision **0012** (`temple/decisions/0012-program-pulse-contract.md`) — the
full grammar, lifecycle, and guards live there. This card is the working procedure; if it
looks stale against 0012, 0012 wins.

## The line (one task = one line)

```
- [STATUS] <task-id> · <scope/slug> · owns: <file-globs> · gate: <assay|human|skip> · <one-line intent> · log: <pointer>
```

`STATUS` ∈ `issued → staged → review → done` · `parked` · `blocked`. Status is position-1,
bracketed → greppable.

**The pulse is a *phasing wrapper*.** It sequences tasks and points to them; it never
stores a task's full detail. A task's peripheries live in its own **task file** (the `log:`
pointer, e.g. `session/<slug>/tasks/<task-id>.md`) — one file, three layers: **spec** (head
writes it) → **log** (coder appends progress) → **handoff** (coder's how-to-use). The line
carries only the one-line intent + the pointer.

## add-to-line  (plan → deposit work)

For each task the head + brain have settled:

1. **Check owns-disjointness first (0012 L4).** No two non-`done` lines may share a
   file-glob. If a new task would overlap an open line's `owns:`, narrow its scope or
   serialize it — never add an overlapping `owns:`. This is the parallel-write race guard.
2. Write ONE `- [issued]` line under the active program header, using the grammar above.
3. Assign a **fresh `task-id`** (T1, T2…). Never reuse a retired id.
4. Set `gate:` by risk — `assay` (load-bearing, spawn @Assay), `human` (you review), `skip`
   (trivial, head's judgment).
5. Write the **full task spec** (all peripheries) into the task's file — the `log:` pointer
   (`session/<slug>/tasks/<task-id>.md`). The pulse **line** stays a thin one-liner; the
   substance lives in the file. The coder reads the spec, appends progress below it, leaves
   its handoff at the bottom.

## pull-from-line  (claim → dispatch)

1. Read `program.pulse.md`. Pick the next `issued` line (queue order, or the head's priority).
2. Flip its status `issued → staged`.
3. Route by the line's `scope/slug` — dispatch the coder (Trajectory / Vector / Delta) with
   exactly: the task intent · the `owns:` file scope · the `gate:` · the `log:` pointer.
4. **Batch rule (0012 L5):** 1 line → the head runs it directly. N lines → hand the set to
   @Vara to run the program. Vara only flips status in-flight; the head keeps buffer authority.
5. **Never pull two lines with overlapping `owns:` into parallel flight (L4).**

## reconcile  (last turn, or on a surfaced issue)

1. `done` lines (gate PASS + committed) → move to `program.pulse.archive.md`.
2. `parked` / `blocked` lines → keep living in `program.pulse.md`.
3. The head may re-read, correct status, re-issue a reconfigured line, or split/merge — the
   head owns the buffer's *shape* across the whole arc (0012 L6). Vara does not reconcile.

## Kickoff discipline (harvested from the retired /run-task, 2026-07-16)
- **Name the shape and hold it** — declare a program-pulse run at kickoff and don't switch
  shapes mid-run; a mid-run switch pays max context re-establishment for min savings.
- **Reserve a token floor** at kickoff (e.g. 0.30). When the run burns down to the reserve it
  STOPS and reports — the run-side name for the 0012-L8 program-level token ceiling.

## Guards I never cross (0012 L7–L8)

- `blocked` waits for brain/human — **it never auto-proceeds on a guess** (dead-man's-switch).
- Commit only to a program / throwaway branch; **never auto-commit to `core`**; load-bearing
  paths take a human gate.
- A `review` line's gate is @Assay (fresh-eyes) or human or skip — set per line, not by default.
