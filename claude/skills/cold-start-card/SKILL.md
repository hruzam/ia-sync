---
name: cold-start-card
description: >
  Invoke as /cold-start-card. Drops a session-glue card into the central vault
  ~/reposoma/_cold-start/ so any brand/host can fully re-enter — CS.<slug>.<date>.md
  for live process glue, RT.<slug>.md for routines. Sibling /issue-card for known
  defects in the same flat vault. Law: raw.guides/cold-start-card/GUIDE.md.
---

I drop a session-glue card into the central vault — enough for the next incarnation
(any brand, any host) to fully re-enter. Frontmatter carries the parseable truth; the
body carries the taste.

**Schema of record:** `~/reposoma/raw.guides/cold-start-card/res/cold-start-card.md`
(the field-by-field subchapter of `~/reposoma/raw.guides/cold-start-card/GUIDE.md` — read
the GUIDE signpost first for the shared vault / filename / frontmatter law). On conflict
between this skill and the guide, THE GUIDE WINS. The block below is the operational
minimum, not a second authority — cross-check the subchapter only if it looks stale, not
as a default read.

## Where it lands

- Vault root via cascade: `temple-project-map.zsh` → reposoma root → `_cold-start/`.
  Only the folder name is baked here; the map absorbs any future reposoma move.
- Process card → `<reposoma>/_cold-start/card/CS.<slug>.<YYYY-MM-DD>.md`
- Routine card → `<reposoma>/_cold-start/routines/RT.<slug>.md` (dateless — it recurs)
- Vault is git-tracked: the card exists cross-machine only after commit+push — say so
  at handoff if I can't commit from my seat.
- I only ADD files; never edit or move another seat's card (single-writer).

**One vault, flat categories.** This same vault also holds the issue category — a FLAT
`issues/` folder at the SAME level as `card/` · `routines/` · `archive/`, written by
`/issue-card`, never a nested subtree. I write the cold-start category (`card/` ·
`routines/` · `archive/`); the shared frontmatter contract, filename law, and the sort
rule below are family-wide. `routines/` also receives issue cards that graduate out of
`issues/` via the fold (three paths: known-recurring → straight to `routines/` · one-shot
→ `archive/` · archived-then-recurs → pulled into `routines/`) — a graduated card keeps
its `ISS.` name and catch-date; the fold mechanism itself lives in `res/issue-card.md`.

## The card

Frontmatter first — flat shared cross-brand contract, every path WHOLE and
`~`-anchored (`~/path/to/target`; never bare-relative, never literal /home/…). Skip empty
keys; never invent values. Field semantics live in the subchapter above:

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
    runbook: ~/<project>/<session-root>/<program>-<NN>-<phase>/RUNBOOK.md   # optional — the LIVE RUNBOOK in the owning project's session bed; omit when no live bed exists. reposoma is the card/canon home, never a session owner.
    pointers:
      - ~/<where depth lives>
    ---

`model`+`dedicated`+`recommend` = my routing assessment — the human reads it in the
palette before launching anything.

**Optional master prompt** — runbook grammar EXACTLY (blocks lift verbatim into
RUNBOOK.md; the palette reveals them without opening the card):

    ## prompt-0

    ###### prompt

    ```text
    <master prompt for the next session>
    ```

**One-authority law:** the card is a transfer POINTER, never a second doing-state. If a
live session bed exists (a `STATUS.md` for an open gate), I point to it and carry NO
competing next-action — STATUS owns the position. I keep my own next-action only when no
live bed exists.

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
