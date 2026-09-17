---
name: cold-start-card
description: >
  Invoke as /cold-start-card. Drops a session-glue card into the central vault
  ~/reposoma/_cold-start/ — frontmatter is the source of truth (project, whole ~paths,
  commit, resume command, routing assessment), free-prose continuity layer, optional
  prompt-0 master prompt in runbook grammar. CS.<slug>.<date>.md for process glue,
  RT.<slug>.md for routines. The glue to re-enter a session. Law:
  raw.guides/cold-start-card/GUIDE.md. Sibling of /drop-brief (terse agent take) and
  /issue-card (known-defect cards in the same vault under the issues/ subtree).
---

I drop a session-glue card into the central vault — enough for the next incarnation
(any brand, any host) to fully re-enter. Frontmatter carries the parseable truth; the
body carries the taste.

**Schema of record:** `~/reposoma/raw.guides/cold-start-card/GUIDE.md` — on conflict
between this skill and the guide, the guide wins. (Pointer note: the schema below is a
working copy; cross-check the guide only if this looks stale.)

## Where it lands

- Vault root via cascade: `temple-project-map.zsh` → reposoma root → `_cold-start/`.
- Process card → `<reposoma>/_cold-start/card/CS.<slug>.<YYYY-MM-DD>.md`
- Routine card → `<reposoma>/_cold-start/routines/RT.<slug>.md` (dateless — it recurs)
- Vault is git-tracked: the card exists cross-machine only after commit+push — say so
  at handoff if I can't commit from my seat.
- I only ADD files; never edit another seat's card (single-writer).

**One vault, categories inside it.** This same vault also holds the issue category
(`issues/open · issues/parked · issues/archive`, written by `/issue-card`) — same mechanism,
different lifecycle, so it gets its own state subtree. I write only the cold-start category
(`card/` · `routines/` · `archive/`); the shared frontmatter contract, filename law, and the
sort rule below are family-wide.

## The card

Frontmatter first — flat shared cross-brand contract, every path WHOLE and
`~`-anchored (`~/path/to/target`; never bare-relative, never literal /home/…):

    ---
    kind: cold-start-card            # cold-start-card | routine
    date: <YYYY-MM-DD>
    brand: claude
    seat: <my seat name>
    project: <origin registry key>
    projects: [<a>, <b>]             # optional — cross-project span
    root: ~/<whole path to project root>
    commit: <short-hash> (<branch>)  # via seat Bash if present, else leave for majkee
    task: <one line>
    resume: <command + flags>
    model: <fable|opus|sonnet|haiku> # thinking level the continuation deserves
    dedicated: <recommended seat/agent>
    recommend: <one-line steer for the next incarnation>
    runbook: ~/reposoma/_runbook/<project>/<slug>/RUNBOOK.md   # optional
    pointers:
      - ~/<where depth lives>
    ---

Skip empty keys; never invent values. `model`+`dedicated`+`recommend` = my routing
assessment — the human reads it in the palette before launching anything.

**Optional master prompt** — runbook grammar EXACTLY (blocks lift verbatim into
RUNBOOK.md; the palette reveals them without opening the card):

    ## prompt-0

    ###### prompt

    ```text
    <master prompt for the next session>
    ```

**One-authority law:** the card is a transfer POINTER, never a second doing-state. If a
live session bed exists (a `STATUS.md` for an open gate), I point to it and carry NO
competing next-action — STATUS owns the position. Own queue only when no live bed exists.

**Body — continuity layer** (free prose, point never copy): pending tasks in order ·
state pointers (dev-journals, pulse entries, staged files) · first-step instruction ·
session advice (one lesson) · cleanup/hygiene debts. The card alone may be tiny, but
card + its pointers must be sufficient.

## Read-state — drain by default

Folder = state. The reader who consumed a CS card moves it `card/` → `archive/`
(Cinderella; `temple-cs-manage` once built, plain `mv` until then). A multi-reader card
carries `leave: for more readers` and stays until all have drained it. RT cards never
move.

## Sort key — the durable radar (family-wide)

- **Dated categories (cold-start-card, issue-card) sort by the filename `YYYY-MM-DD` date,
  primary.** A date in the name is repository data that survives clone / checkout / host-move;
  mtime is only one checkout's observational state and resets on any git op. Richer
  discriminators live in frontmatter; narrow by name first, read metadata second, body last.
- **UNSORTED fallback.** A dated card whose filename lacks the `YYYY-MM-DD` marker is surfaced
  UNSORTED, never silently mis-ordered. **Routines are dateless by design and are exempt** —
  a missing date on an RT card is correct, not drift.

## Run

1. Pull the frontmatter facts from THIS session (I hold the context — no subagent).
2. Compose the continuity layer: open items, state artifacts, lessons, debts.
   Point, don't copy — the card stays small.
3. Draft, show majkee, confirm — then Write the file.
4. Confirm: "card dropped at `~/reposoma/_cold-start/<subdir>/<name>` — commit reposoma
   to make it cross-machine."
