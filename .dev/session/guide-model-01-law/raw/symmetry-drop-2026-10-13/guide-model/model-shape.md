---
title: model-shape — when a guide becomes a controller with functions; how to write, convert and prove one
chapter-of: guide-writing
state: DRAFT — gavel text for guide-model-01-law · staged in guide-writing/src/ · lands inside guide-writing (the fold distributes it into controller + functions)
verified: 2026-10-12
by: claude.ai seat (Symmetry project thread) from majkee's brief, 2026-10-12
---

# Model shape — guides as controllers

`what: the second guide shape. A flat guide is read to understand. A model guide is consulted to do`
`one of several jobs — its GUIDE.md is a controller that sends each reader to the one function that job needs.`
`not: a mandate. Shape is earned by occasions of use — never by length, age or importance.`
`extends: guide-writing/GUIDE.md + res/slug-directories.md — every rule there stays law; the changes are listed at the end.`

## Two shapes

| | flat (default — no key) | model (`shape: model`) |
|---|---|---|
| the reader arrives to… | understand one thing | do one of several jobs |
| `GUIDE.md` is… | the text, read whole | a controller: invariants · functions table · shared core |
| `res/` chapters are… | depth — sliced by topic | functions — one per occasion (plus optional reference) |

Both keep every existing law: one topic = one slug, fixed `GUIDE.md`, manifest, side-directory slots,
frontmatter, point-never-copy, trust disk over doc, commit the same session.

## The split law — one function per occasion of use

- An **occasion** is a distinct job a reader arrives with, in their words: "open a session",
  "recover a broken fan-out". List the occasions before anything else is decided.
- One occasion → flat, however long. Several occasions, reached at different times → model.
- **Size is a symptom, never a trigger.** A long guide prompts the occasion question; it never
  answers it.
- **The split test:** a reader holding the controller plus one function finishes that occasion's
  job. If not, the function is not self-sufficient or the controller lacks an invariant — fix that;
  never make a second function a required preload.
- A function no reader ever reaches alone is not a function — fold it back.
- **One hop:** controller → function. A function may point to the *next* occasion's row; it never
  requires another function first.
- **Order of values:** finishing the job → clean context → tokens. A split that makes the job
  harder to finish is wrong even when it saves tokens.

## The controller — `GUIDE.md` of a model guide

In this order (copy `ast/GUIDE.template.txt`):

1. **Frontmatter** — the five required keys + `shape: model` (+ knowledge-card extras if volatile).
2. **Reader banner** — fixed text: this file is a controller; find your job in *Functions*, read
   only that function, finish there; *Invariants* bind every function; the why is in `BACKGROUND.md`.
3. **`what:` / `not:`** — what the guide governs; what it never owns, and where that lives.
4. **Invariants** — rules every function obeys. A rule whose breach is costly or irreversible
   lives here, never only in a function: **safety lines load eagerly, procedure loads lazily.**
   (Receipt: the tunnel's "no seat runs `open --enable`" must reach a seat before any verb does.)
   Keep it short — if this section outgrows a screen, the guide is probably two guides.
5. **Functions** — the dispatch table `| when you need to … | read | you get |`, one row per
   occasion, phrased as the reader's job, not the topic. **This table registers the functions** —
   they are not repeated in the Manifest (one list per thing).
6. **Core** — optional branch-free steps every function assumes.
7. **Manifest** — everything else: `BACKGROUND.md`, reference chapters, attachments,
   side-directories (one line each), the journal.

Writer rule 3 ("open with the process, not the inventory") is met by 2 + 5: the reader meets
"where do I go for my job" before any inventory.

## A function — `res/<fn>.md`

Copy `ast/FUNCTION.template.txt`.

- Header: `title:` + `chapter-of: <slug>` (existing law) + **`occasion:`** — the exact text of its
  Functions row, so table and function can be checked against each other both ways.
- Self-sufficient for its occasion under the controller's invariants (the split test).
- **Commands, not prose:** every step that runs something gives the exact command and what success
  looks like. "Adjust as needed" is a defect.
- **Failure paths are specific** ("exit 61 → wait or `tun read`, never a second turn"), never a
  generic retry.
- Reference longer than the procedure it serves moves to its own `res/` chapter (no `occasion:`,
  class `reference` in the Manifest) and is pointed to.
- Optional **Next**: the row of the occasion that usually follows — a pointer, never a preload.

## `BACKGROUND.md` — the narrative door (name gaveled by majkee 2026-10-12)

Copy `ast/BACKGROUND.template.txt`.

- One per slug, beside `GUIDE.md`, fixed filename. **Human first** — agents grep it for *why* and
  never act from it.
- Holds what a conversion removes from procedure: why the guide exists, decisions with reasons,
  options rejected, the arc, the incident behind a rule.
- **Tells and links, never copies.** Its own prose for the arc; pointers into `raw/` (briefs,
  evidence, session stories), `src/` (staging in progress), `dev-journal.<slug>.md` (maintenance).
  That material already exists in those slots — BACKGROUND is the one door a human can open.
- **No authority.** `GUIDE.md` wins any conflict; a rule stated only in BACKGROUND is not a rule.
  Two files are allowed, two authorities are not.
- **Earned:** a guide with no story worth keeping has none — flat or model.
- **Not a GLOSS.** A GLOSS explains a *run*, step by step, for the human sitting it
  (`raw.guides/gloss/`). BACKGROUND explains a *design*, once, for the human who wants to
  understand it. Same family — uncanonical, human-facing — different animals.
- Served only on explicit ask: `/guide <slug> background`.
- How to write and keep one — the sort test, the three sections, append-only decisions, the
  review checks: `res/write-background.md` (staged as `src/write-background.md`).

## Converting a guide — the collapse

1. **Occasions first.** Read `GUIDE.md` and every chapter; list the jobs readers come for, with
   evidence (headings, `→ chapter` pointers, journal entries showing use). One occasion → stop: flat.
2. **Sort every paragraph** to one home: invariant → controller · shared core → controller ·
   occasion procedure → function · lookup → reference chapter · why and story → BACKGROUND ·
   field observation → `raw/` or the journal · dead → retired with a dated line in BACKGROUND or
   the journal. Nothing leaves silently.
3. **Write in this order:** Functions table → functions → controller → BACKGROUND. Workpieces stage
   in the slug's `src/` (outbound — slug-directories law) and leave it when they land.
4. **Collapse map:** `old location → new home | retired (why)`, one line per source paragraph. It is
   the reviewer's checklist during review and rides in the commit body afterwards (history lives
   in git).
5. **Prove.** Mechanically: the census shows the slug clean — frontmatter ok, every file registered,
   no dangling pointer, table and `occasion:` agree. Behaviourally: a witness that authored none of
   it gets one prompt per Functions row from a fresh session, with only `/guide <slug>` to start
   from, and must finish each job (`/guide germline-forge witness`). Check that the steps were
   done, not only that the output looks right — a loaded procedure is not a followed one.
6. **Promote.** majkee gavels; one guide per commit (one concern, reversible); commit reposoma the
   same session.

## Creating a new guide

1. Write the occasions first. One → flat. Several → model.
2. Copy the shelves from `guide-writing/ast/`. **Templates scaffold empty shelves; they never carry
   generated content.** Text emitted without a human or a witnessed seat owning it is a rewrite
   candidate, whatever its shape.
3. Fill by hand or by a witnessed seat. BACKGROUND only if there is a story.
4. Prove and promote as in steps 5–6 above.

## Defects — what an audit or a reviewer looks for

Grouped by the temple audit loop's three bins (`raw.guides/audit-loop.card.draft.md`). The census
reports the ones marked ✓; the rest are judgment.

*lapsus — meaning*
- **L1 two authorities** — BACKGROUND, a function, a chapter or a sibling guide states a rule the
  controller contradicts or lacks.
- **L2 lazy safety line** — a costly or irreversible rule lives only in a function or chapter.
- **L3 weather** — version-bound facts undated or past half-life (Sella L8). ✓ for half-life
- **L4 generated** — comprehensive, generic, unowned text.

*chain — integrity*
- **C1 unregistered** — a file or directory neither the Manifest nor the Functions table names. ✓
- **C2 dangling** — a `res/` pointer to a file that does not exist. ✓
- **C3 table drift** — a function whose `occasion:` matches no row, or a row whose function lacks one. ✓
- **C4 frontmatter** — no YAML block, or required keys missing. ✓

*compression — context economy*
- **K1 over-split** — functions never reached alone; a guide small enough to grep, split anyway.
- **K2 under-split** — several occasions in one body; every reader wades through jobs that are not
  theirs.
- **K3 teaching bloat** — story, rationale and incident narrative inside procedure (→ BACKGROUND).
- **K4 embedded reference** — lookup material longer than the procedure it serves, inline.
- **K5 prose for command** — "adjust as needed" where an exact command and its expected output
  belong.

## Reader behaviour — what `/guide` does

- The listing shows `shape` beside title · machine · verified (model only; absent = flat).
- `/guide <slug>` presents `GUIDE.md` verbatim — for a model guide, the controller. The reader then
  reads only the function whose row matches the job.
- `/guide <slug> <fn>` reads one function — the resolver is unchanged.
- `/guide <slug> background` reads `BACKGROUND.md`; never served unasked. `background` is therefore
  a reserved word: no `res/` chapter is named `background*` — the keyword would shadow it.
- `raw/`, `src/`, `ast/`, `cod/` stay unserved. The orphan flag reads Manifest + Functions as the
  register.

## What this changes in guide-writing — the gavel list

| # | guide-writing today | with this law |
|---|---|---|
| 1 | four sibling classes (GUIDE · chapter · attachment · legacy) | + `BACKGROUND.md` (fixed name, no authority); chapters subdivide into function (has `occasion:`) and reference |
| 2 | every sibling named in `## Manifest` | in a model guide the Functions table registers the functions; the Manifest names everything else |
| 3 | chapter header: `title` + `chapter-of` | functions add `occasion:` |
| 4 | five required frontmatter keys | + `shape: model` when a guide has several occasions; absent = flat — no bulk edit of flat guides |
| 5 | the resolver serves `GUIDE.md` + `res/` | + `BACKGROUND.md` on explicit `background` |
| 6 | "chapters are the sip unit" — by topic | by occasion in model guides; topic slices stay legal in flat ones |
| 7 | writer rule 3: open with the process | met by banner + Functions table; Invariants sit between them and stay short |
| 8 | `ast/` is a reserved slot | `guide-writing/ast/` holds the three templates — its first tenant here |

Self-application: guide-writing has several occasions (write a guide, convert one, write a
background, place a side file, treat guides as a project agent). By this law it is the first model guide — converting it is
session `guide-model-01-law`.

## Provenance — evidence, not authority

- The split law and the order of values: majkee, 2026-10-12 — split a guide so an agent reads only
  the parts its job needs; finishing the job outranks token thrift; the reason to split is clean
  context.
- The narrative door: majkee, 2026-10-12 — one file per guide gathering what a conversion removes;
  human the main reader; greppable by agents; a different animal from GLOSS. Named BACKGROUND the
  same day — README and context rejected (reasons: guide-writing's BACKGROUND.md, Decisions).
- The guide system this extends, read 2026-10-12: the `/guide` skill
  (`~/ia-sync/claude/skills/guide/SKILL.md`), guide-writing + slug-directories, gloss, runbook,
  status, tunnel, germline-forge, the audit-loop card.
- The defect list: practitioner write-ups on progressive disclosure and agent instruction files
  (ardalis.com, mindstudio.ai, synthesiscoding.org, agentpatterns.ai, aihero.dev, wordman.dev,
  blakecrosley.com; arXiv 2607.17598), read 2026-10-12 and folded into house vocabulary.
