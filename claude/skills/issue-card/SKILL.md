---
name: issue-card
description: >
  Invoke as /issue-card. Drops a known-defect card into the SAME central card vault as
  cold-start (~/reposoma/_cold-start/), under the issue category (its own state subtree
  issues/open · issues/parked · issues/archive). Frontmatter is the source of truth
  (project, whole ~paths, the broken file, a one-sentence defect description, and >=7
  association tags an agent can filter on WITHOUT opening the body); free-prose body carries
  the evidence. Filename ISS.<slug>.<YYYY-MM-DD>.md — the date is the durable sort radar; a
  card missing it lands UNSORTED, never silently mis-ordered. Sibling of /cold-start-card,
  same mechanism, different category. Law: raw.guides/cold-start-card/GUIDE.md.
---

I drop a known-but-not-yet-fixed defect into the shared card vault so any later session
(any brand, any host) can find it, filter it, and pick it up without re-discovering it.
Same mechanism as `cold-start-card` — frontmatter is the parseable truth, the body carries
the evidence, git-pull is the cross-machine transport — just a different **category** and a
different **state model**.

**Schema of record:** `~/reposoma/raw.guides/cold-start-card/GUIDE.md` — one family, one
law. On conflict between this skill and the guide, the guide wins. (Pointer note: the schema
below is a working copy; cross-check the guide only if this looks stale.)

## Where it lands — the issue subtree of the shared vault

The vault is `~/reposoma/_cold-start/` (resolved via cascade: `temple-project-map.zsh` →
reposoma root → `_cold-start/`). Issues are a category inside it, with **their own state
folders** — because an issue's lifecycle (open → parked → resolved) is a different state
machine than a cold-start card's (live → drained):

```
~/reposoma/_cold-start/
├── card/  routines/  archive/   # cold-start category (CS.* / RT.*) — untouched
└── issues/
    ├── open/      # flagged, not yet triaged into a keep-or-fix call
    ├── parked/    # triaged, deliberately deferred ("known, not fixed, operator call")
    ├── archive/   # resolved
    └── reactions/ # [ISSUE-DRAFT] playbook cards for recurrent defect patterns
```

- **Folder carries the state** — no `status:` field (a field would drift from the location).
  A triage or a fix is a `mv` between these folders, nothing else.
- Vault is git-tracked: the card exists cross-machine only after commit+push — say so at
  handoff if I can't commit from my seat.
- I only ADD files; I never edit another seat's card (single-writer).

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
  live here (manifest). Skip empty keys; never invent values.

**Body — the evidence layer** (free prose, point never copy): what was observed and when ·
the consequence confirmed vs suspected · why it is open/parked (the triage or operator call) ·
where it was first flagged. The card + its pointers must be sufficient; keep it small.

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

## State moves — folder is state

Triage moves `issues/open/` → `issues/parked/` (deferred) or straight to a fix. A resolved
issue moves to `issues/archive/`. Plain `mv` until a `temple-cs-manage` equivalent exists.
No `status:` field ever — the folder says it.

## Reaction cards — [ISSUE-DRAFT] playbook for recurrent patterns

A **reaction card** captures a known pattern of defect and its playbook response — "we've
seen this class of defect before, here's how to react." Unlike issue cards (which describe
a single dated instance in `open/parked/archive/`), reaction cards are dateless, never
archived, live in `issues/reactions/`, and recur: a frozen response to a known defect family.

Filename `IR.<slug>.md` (no date — mirrors `RT.<slug>.md` reasoning: "dateless — it recurs").

Frontmatter is minimal (no `date:` field — this is a class, not an instance):

    ---
    kind: issue-reaction           # category identifier
    brand: claude
    found_by: <seat/agent>
    project: <origin registry key>
    root: ~/<whole path to project root>
    pattern: <ONE sentence describing the defect pattern>
    assoc: [<tag>, <tag>, <tag>, <tag>, <tag>, <tag>, <tag>]   # >=7 discriminators
    playbook: <how to respond when you hit this pattern>
    pointers:
      - ~/<where related instance cards or deeper trail live>
    ---

- **`pattern:` and `playbook:` carry the contract** — a reader identifies the pattern without
  opening the body and reads the playbook response from frontmatter.
- **`assoc:` is >=7 association tags** — same discriminator discipline as issue cards (class ·
  tech · subsystem · host · symptom · area · severity). An agent greps these to surface
  candidate reactions without a body read.
- **No date, no archive** — reaction cards are stateless and permanent (like routines).

## Run

1. Pull the facts from THIS session — the broken surface, when/how observed, the
   consequence, the triage call. I hold the context; no subagent.
2. Compose: one-sentence `defect:`, >=7 `assoc:` tags, whole `~`-anchored paths, evidence
   body. Point, don't copy — the card stays small.
3. Choose the folder by state: untriaged → `open/`, deferred → `parked/`.
4. Draft, show majkee, confirm — then Write the file at
   `~/reposoma/_cold-start/issues/<state>/ISS.<slug>.<YYYY-MM-DD>.md`.
5. Confirm: "issue card dropped at `~/reposoma/_cold-start/issues/<state>/<name>` — commit
   reposoma to make it cross-machine."
