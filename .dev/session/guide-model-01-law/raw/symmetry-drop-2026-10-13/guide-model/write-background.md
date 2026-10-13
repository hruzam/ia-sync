---
title: write-background — how to write and keep a guide's BACKGROUND.md (the standard)
chapter-of: guide-writing
occasion: "write or extend a guide's BACKGROUND.md"
state: DRAFT — addendum to model-shape.md · staged in guide-writing/src/ · lands as res/write-background.md in guide-model-01-law
verified: 2026-10-12
---

# write-background — the BACKGROUND.md standard

`gives: a BACKGROUND.md a human reads in one sitting and an agent can grep for "why" — that never becomes a second rulebook.`
`assumes: the BACKGROUND rules in the controller (model-shape §BACKGROUND.md) — one per slug, no authority, earned, not a GLOSS.`
`name: BACKGROUND — gaveled by majkee 2026-10-12. Why this name and not README, context or story: guide-writing's own BACKGROUND.md, Decisions.`

The standard in one line: **restraint plus a fixed shape** — one earned file, no authority, its own
words for the arc, pointers for the evidence, three sections and nothing else.

## The two ways it fails

| failure | looks like | guard |
|---|---|---|
| overfilled — the junk drawer | copied receipts, procedure, rules that live nowhere else, everything "vaguely relevant" | the sort test · the review checks |
| ceremonial — the empty shelf | a template filled with nothing, born because the template exists | earned: no story, no file |

A GLOSS tends to get skipped; a BACKGROUND tends to get overfilled. This standard holds that line.

## Born when

- a conversion removes a paragraph of *why* from `GUIDE.md` or a chapter — it lands here, dated;
- a decision about the guide is made that a later reader will ask about ("why not X?").

Never because a template exists, or because a guide feels incomplete without one.

## The sort test — what goes where

| the material | its home |
|---|---|
| why the guide exists; the problem it answers | BACKGROUND · arc |
| a decision about the guide, with its reason | BACKGROUND · a Decisions row |
| an option considered and rejected | BACKGROUND · that row's *instead of* |
| the incident behind a rule | BACKGROUND · arc — the **rule itself** stays in `GUIDE.md` or its function |
| verbatim evidence, receipts, session stories | `raw/` — BACKGROUND points |
| a change being prepared | `src/` — BACKGROUND points while it is open |
| maintenance entries — what changed, when | `dev-journal.<slug>.md` — BACKGROUND points |
| why a step of a run is done | GLOSS, at the project's session root — not here |
| any rule, any command | `GUIDE.md` or a function — never here |

A paragraph that holds both a rule and its story splits: the rule goes to `GUIDE.md`, the story
stays here and points at the rule.

## Anatomy — three sections, nothing else

Copy `ast/BACKGROUND.template.txt`.

- **Frontmatter** — `title` · `scope` · `audience` · **`authority: none — …`** · `verified`. The
  authority line is required: it is what keeps the file from becoming a second rulebook.
- **Header lines** — `what:` · `not:` · `how to treat:`, as the template has them.
1. **The arc** — prose, in its own words: the problem, what was tried, what held. A few paragraphs;
   an arc that outgrows a page is copying `raw/`, or the guide is two topics.
2. **Decisions** — `| date | decision | why | instead of |`, one row per decision, newest last.
3. **Where the material lives** — pointers only, one line each, with what a reader finds there.

A section that wants to exist is material for one of these three — or for another home in the sort
test.

## Keeping it

- **Decisions are append-only.** A reversal is a new dated row naming the row it reverses; the old
  row stays — that history is what a reader came for.
- **The arc may be rewritten** when understanding changes; git keeps the old telling.
- **Pointers are checked like any pointer.** A dead path in *Where the material lives* is drift: fix
  it, or drop the line with a dated note in the arc.
- **Nothing moves into `GUIDE.md` silently.** A *why* that turns out to carry a rule is promoted by
  the normal gavel; its row stays here as history.

## How it is read

- Humans read it whole, when they want to understand the guide.
- Agents read it only when asked (`/guide <slug> background`) or grep it for a *why*; they never act
  from it and never cite it as a rule.
- If BACKGROUND and `GUIDE.md` disagree, `GUIDE.md` wins and the disagreement is a finding
  (L1 two authorities).

## Review checks — the writer before commit, an auditor on a walk

1. The `authority:` line is present.
2. No rule or command lives only here.
3. Nothing is copied from `raw/`, `src/` or the journal — it is pointed to.
4. Exactly the three sections.
5. Every Decisions row has a date and a reason; rejected options are named wherever there were any.
6. Every pointer resolves.
7. It was earned — there is a story. Otherwise, delete the file.

## BACKGROUND and GLOSS — siblings, not twins

| | GLOSS | BACKGROUND |
|---|---|---|
| explains | a run — the steps a human is sitting | a design — the guide a human wants to understand |
| unit | one per project part; sections per session; notes per step | one per slug |
| written | before each step is run | when a decision is made, or a conversion removes a *why* |
| lives | the project's session root, `GLOSS.<slug>.md` | beside `GUIDE.md` |
| common ground | uncanonical · human-facing · never cited as truth | the same |

## First instance

`guide-writing/BACKGROUND.md` — seeded as `src/BACKGROUND.guide-writing.seed.md`; it lands in
guide-model-01-law once majkee has confirmed each Decisions row.
