# PAD builder — how to author an operator step-pad

`what: the general shape of a PAD (operator-facing step-pad) and its PAD→log breathing.`
`scope: STYLE only — vendor/project/driver agnostic. The PAD's LOCATION + naming belong to`
`the consuming project's own rules; this guide owns the SHAPE. Never name a specific driver`
`agent here — say "the driver".`
`companions: raw.guides/runbook/GUIDE.md (the session) · raw.guides/status/GUIDE.md (the`
`position) · raw.guides/bus/GUIDE.md (multi-seat exchange) · raw.guides/gloss/GUIDE.md (the why`
`beside the PAD). Destination law revised 2026-08-27 with the session file set (stream/journal`
`retired).`

## What a PAD is

A **PAD** is an operator-facing **sequential step surface**: one step → the operator runs it →
reports back → the next step. It is where an agent hands a human (or a driver seat helping a
human) a bounded run to execute by hand — a test sitting, a bring-up, a guided learning session.

The PAD's law is **one step at a time**. It never dumps the whole procedure. Each step is small,
copy-pasteable, and ends by waiting for a report before the next is revealed.

## When to reach for a PAD (vs. a task or a report)

- **Task** — an agent will execute autonomously. No PAD.
- **Report / log** — the durable record of what happened. Downstream of the PAD.
- **PAD** — a *human runs the steps* and the outcome is uncertain at each step (a test whose
  verdict branches, a bring-up that may block, a lesson that must land before the next builds
  on it). If a human hand is in the loop and the path forks on results → PAD.

## Anatomy

A PAD is a single markdown file. Its parts, in order:

**1 — Header.**
```
# pad.<order>-<scope> — <one-line purpose>

> Operator <test|learning|bring-up> surface. Sequential — one step, report back, next step.
> Driver: <the driver>.  [+ any per-run protocol line]
```
`<order>` = sitting order (1st, 2nd, …). `<scope>` = the brick/topic under the PAD.

**2 — Driver-rules block (optional — for teaching/guided PADs).** A short numbered list the
driver reads before step 0, every sitting. The general laws worth carrying:
- One step, one concept, then wait. Never run ahead. Never dump theory.
- Plain words before jargon (say the plain thing first, name it after).
- Every instruction is copy-pasteable: full paths, no `cd` assumptions, say WHICH line / WHAT
  to type / WHERE.
- Nothing the operator can do is stupid or broken-forever — step 0 makes that true.
- When an error appears, celebrate it: a traceback names the exact line. Read it bottom-up.
- Confirm before any edit that touches more than one thing.
- Off-pad questions → answer briefly, then return to the step; park big ones at the bottom.
- Offer a GLOSS (raw.guides/gloss/GUIDE.md) at least when asked; if not asked, ask once whether
  the operator wants one. Explanations never go into the PAD.

**3 — Shared constant.** Declare the path/file/session used verbatim in every command, ONCE,
at the top — so no step re-derives it and every command stays copy-pasteable.
```
Project path used in all commands:
/abs/path/used/everywhere
```

**4 — Precondition.** One line naming what must already be true before step 0 (a live session,
a running service). If it can't hold, step 0 catches it.

**5 — STEP 0 = state check / safety copy.** Always first, always non-destructive: verify the
precondition, OR make a restore point (a `.bak` copy). Worst case for the whole PAD = restore
step 0. It also proves the environment before any real move.

**6 — STEP N.** Each real step is:
```
### STEP N — <short title>

```bash
<copy-pasteable command — full paths, no cd assumptions>
*(```)*

<expected output, one or two lines>

<branch verdicts — what each outcome means and where it sends the operator:>
- `<SUPPORTED>` → proceed
- `<REFUTED|BLOCKED>` → STOP, flag <the head/driver>

>MAJKEE report N
```zsh

*(```)*
```

**7 — Trailing sinks (optional).** A verdict-mapping table (step → prediction → SUPPORTED-when /
REFUTED-when) for test PADs, and/or a `## parked` section where the driver appends off-pad
questions without chasing them.

## The PAD → log breathing (minimum bureaucracy)

The PAD **breathes into itself**. The empty ```` ```zsh ```` fence under each `>MAJKEE report N`
is where the operator pastes the real output — so the PAD becomes its own raw run-log as it runs.
**No separate file per step. No separate raw-run file at all** — the PAD IS the raw surface.

Then, and only then, distilled verdicts graduate to **at most ONE** downstream home:

- in a **multi-seat session**: the cycle's VERDICT file in `_bus/` (see the bus GUIDE), or
- in a **single-seat session**: the project's evidence home (e.g. `research/evidence/`), or a
  protocol/verdict file in the session directory.

`STATUS.md` is **not** that home — it is a bounded snapshot that may *point* at the distilled
verdict (`checkpoint:`) but never retells it. There is no session stream or journal in the
current file set; that destination is retired. The rule stands:

> **One raw surface (the PAD) + at most one distilled log. Never a file per step.**

Orphan-safety, built in:
- A PAD that never runs is just **deleted** — it wrote nothing elsewhere, so nothing dangles.
- A PAD that moved leaves a stub saying **"safe to delete."**
- The distilled log is written by the seat that owns verdicts (a report/protocol seat), not by
  the operator mid-run — keep the two roles separate so the raw PAD stays raw.

## Placement + naming (pointer, not law)

This guide owns the **shape**. WHERE a PAD lives and how it's named is the **consuming project's**
call — its own rules file governs that (typically flat in a session folder, e.g.
`session/<slug>/pad.<order>-<scope>.md`, split into sibling folders rather than nested when a
sitting grows). Read the project's session/PAD rules before dropping a PAD; if none exist, that
project needs one line of convention first.

## Style laws (carry these into every PAD)

- Copy-pasteable, absolute, no assumed shell state.
- One step revealed at a time; wait for the report.
- STEP 0 makes the run reversible.
- Branch every step's outcome explicitly — the operator never guesses what a result means.
- Errors are evidence, read bottom-up, never a dead end.
- Generic driver voice — the PAD serves whoever sits it.
- Artifact case in prose: RUNBOOK, STATUS, PAD, POINT, RETURN, VERDICT. Disk case exact:
  `pad.<order>-<scope>.md`.
