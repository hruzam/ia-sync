---
name: issue-card
description: >
  Invoke as /issue-card. Drops a known-defect card into the SAME central card vault as
  cold-start (~/reposoma/_cold-start/), into a FLAT issues/ folder at the same level as
  card/, routines/, archive/ — no nested open/parked/archive/reactions subtree. Frontmatter
  is the source of truth (project, whole ~paths, the broken file, a one-sentence defect
  description, and >=7 association tags an agent can filter on WITHOUT opening the body);
  free-prose body carries the evidence AND, once known, the fix — the card is a fix manual.
  Filename ISS.<slug>.<YYYY-MM-DD>.md — the date is the durable sort radar; a card missing it
  lands UNSORTED, never silently mis-ordered. A card that turns out to recur FOLDS into
  routines/ (keeping its ISS. name + catch-date); a solved one-shot folds into archive/.
  Sibling of /cold-start-card, same mechanism, different category. Law:
  raw.guides/cold-start-card/GUIDE.md + raw.guides/cold-start-card/res/issue-card.md.
---

I drop a known-but-not-yet-fixed defect into the shared card vault so any later session
(any brand, any host) can find it, filter it, and pick it up without re-discovering it —
and, once a fix is known, the SAME card becomes the fix manual: look it up instead of
re-deriving it. Same mechanism as `cold-start-card` — frontmatter is the parseable truth,
the body carries the evidence, git-pull is the cross-machine transport — just a different
**category** and a different **lifecycle** (the fold, not a private state subtree).

**Schema of record:** `~/reposoma/raw.guides/cold-start-card/res/issue-card.md`
(subchapter of `~/reposoma/raw.guides/cold-start-card/GUIDE.md`, which is the thin signpost
— read it first for the shared vault/filename/frontmatter law) — one family, one law. On
conflict between this skill and the guide, the guide wins. (Pointer note: the schema below
is a working copy; cross-check the subchapter only if this looks stale.)

## Where it lands — the flat issues/ folder of the shared vault

The vault is `~/reposoma/_cold-start/` (resolved via cascade: `temple-project-map.zsh` →
reposoma root → `_cold-start/`). Issues are a category inside it, FLAT — at the same level
as `card/`, `routines/`, `archive/`, with no private state subtree underneath:

```
~/reposoma/_cold-start/
├── card/       # cold-start category (CS.*) — untouched
├── routines/   # RT.* (born routine) + ISS.* (graduated from an issue) — shared with cold-start
├── issues/     # ISS.<slug>.<YYYY-MM-DD>.md — flat, no subfolders
└── archive/    # CS.* (drained) + ISS.* (solved one-shot) — shared with cold-start
```

- **The top-level folder carries the state** — no `status:` field, no nested subfolders
  under `issues/`. An issue's lifecycle is **the fold**, not a private open→parked→resolved
  machine: known-recurring from the start → straight to `routines/`; assumed one-shot →
  `archive/` once solved; recurs after all → `archive/` → `routines/`. Full mechanism:
  `res/issue-card.md`.
- **Parked (deliberately deferred) is not a folder or a `status:` field** — it is a `parked`
  entry in the card's `assoc:` list plus a body note. The card stays in `issues/`.
- Vault is git-tracked: the card exists cross-machine only after commit+push — say so at
  handoff if I can't commit from my seat.
- I only ADD files; I never edit another seat's card (single-writer). Folding a card between
  top-level folders is majkee's per-card call, not something I do unattended.

## The card

Filename `ISS.<slug>.<YYYY-MM-DD>.md`. The `ISS.` prefix + date are for the human eye and
glob ergonomics (`ISS.*`) and — the date — the durable sort key. Machines never parse the
filename for meaning; `kind:` in frontmatter is the truth.

Frontmatter first — flat, `~`-anchored paths (whole, never bare-relative, never literal
/home/…):

    ---
    kind: issue-card               # the category — parser truth
    date: <YYYY-MM-DD>             # also the filename date — the durable sort radar
    brand: claude
    found_by: <seat/agent that found it>   # issue-domain author key
    project: <origin registry key>         # which repo/component owns the defect
    root: ~/<whole path to project root>
    where: ~/<whole path>:<line?> (<symbol?>)   # the broken surface
    defect: <ONE sentence — the description, tacit discriminators woven in>
    assoc: [<tag>, <tag>, <tag>, <tag>, <tag>, <tag>, <tag>]   # >=7 filterable discriminators
    severity: <low|med|high>       # optional
    pointers:
      - ~/<where the deeper trail lives — journal entry, related commit, sibling card>
    ---

- **`defect:` is the one-sentence description** — a reader filters on it without opening the
  body.
- **`assoc:` is >=7 association tags** — the "know, not said" discriminators (class · tech ·
  subsystem · host · symptom · area · severity). An agent narrows candidates by grepping this
  list alone. Put a couple of the strongest discriminators into the slug too (radar), the rest
  live here (manifest). Skip empty keys; never invent values. A deliberately-deferred
  (parked) card adds a `parked` entry to this list — there is no `parked/` folder and no
  `status:` field.
- **`origin:` / `from_issue:`** apply only once a card has graduated into `routines/` via the
  fold — not while it still lives in `issues/`. See `res/issue-card.md`.

**Body — the fix-manual layer** (free prose, point never copy): what was observed and when ·
the consequence confirmed vs suspected · **once known, the fix itself or the playbook to
apply it** — this is what makes the card a fix manual, not just a defect log · why it is
parked, if it is · where it was first flagged. The card + its pointers must be sufficient;
keep it small.

## Sort + drift — the durable radar

- **Sort by the filename `YYYY-MM-DD` date, primary.** A date in the name is repository data
  that survives clone / checkout / host-move; filesystem mtime is only one checkout's
  observational state and resets on any git op — different epistemic classes. The richer
  discriminators (`assoc:`) live in frontmatter; the body is the payload. Narrow by
  filename/tags first, read metadata second, open the body only after candidate reduction.
- **UNSORTED fallback.** An issue card whose filename lacks the `YYYY-MM-DD` marker is NOT
  silently mis-ordered — a sorter surfaces it in an UNSORTED bucket for a human to fix the
  name (the drift-detector pattern). (Routine cards are dateless by design and are exempt —
  that rule is theirs, not this one.)

## The fold — folder is state, no nested subtree

`issues/` is flat and is a waiting room, not a state machine. Every card's lifecycle runs
one of three paths (full mechanism: `res/issue-card.md`):

1. **Known-recurring from the start** (structural) → straight to `routines/`, no detour
   through `issues/` or `archive/`.
2. **Assumed one-shot, stays solved** → `mv` from `issues/` to `archive/` once fixed.
3. **Assumed one-shot, but recurs later** → pull back out of `archive/` and `mv` into
   `routines/`.

A card graduating to `routines/` keeps its `ISS.<slug>.<YYYY-MM-DD>.md` name (never renamed
to `RT.`) and its catch-date (now read as "first seen"), and gains `origin: issue` (+
optional `from_issue:`) in frontmatter. Plain `mv` until a `temple-cs-manage` equivalent
exists. No `status:` field ever — the top-level folder says it. Folding a card is majkee's
per-card call, not something this skill does unattended.

**NOTE — deleted from the design:** there is no `issues/reactions/` category and no
`IR.<slug>.md` reaction-card type. The recurring-fix role that reaction cards used to serve
is now handled entirely by the fold into `routines/` — a graduated issue card IS the
playbook, in its own body, not a separate card type.

## Run

1. Pull the facts from THIS session — the broken surface, when/how observed, the
   consequence, whether it looks structurally recurring or assumed one-shot. I hold the
   context; no subagent.
2. Compose: one-sentence `defect:`, >=7 `assoc:` tags, whole `~`-anchored paths, evidence
   body (+ the fix, once known). Point, don't copy — the card stays small.
3. Choose the destination by the fold call: known-recurring from the start → straight to
   `routines/`; otherwise → `issues/` (add `parked` to `assoc:` + a body note if this is a
   deliberate defer, not an active untriaged flag).
4. Draft, show majkee, confirm — then Write the file at
   `~/reposoma/_cold-start/issues/ISS.<slug>.<YYYY-MM-DD>.md` (or
   `~/reposoma/_cold-start/routines/ISS.<slug>.<YYYY-MM-DD>.md` for a known-recurring card).
5. Confirm: "issue card dropped at `~/reposoma/_cold-start/<issues|routines>/<name>` — commit
   reposoma to make it cross-machine." Fold decisions after the initial write are majkee's.
