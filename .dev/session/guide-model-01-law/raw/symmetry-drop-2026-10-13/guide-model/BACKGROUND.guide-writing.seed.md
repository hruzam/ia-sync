---
title: guide-writing — background
scope: guide-writing
audience: human first — agents grep it for "why", never act from it
authority: none — explains, never legislates; GUIDE.md wins any conflict
verified: 2026-10-12
seed: DRAFT — staged in guide-writing/src/ · majkee confirms each Decisions row before it lands as guide-writing/BACKGROUND.md (guide-model-01-law) · the writer then adds what the collapse map retires into it
---

# guide-writing — background

`what: the story behind guide-writing — why guides live where they live, why they are shaped as they are, what was rejected on the way.`
`not: procedure (→ GUIDE.md, res/) · evidence (→ raw/) · staging (→ src/) · maintenance log (→ the journal)`
`how to treat: tell the arc in your own words and link the material — never copy it. Decisions are append-only,`
`newest last; a reversal is a new row. When a conversion removes a paragraph of "why" from the guide, it lands here, dated.`

## The arc

Guides used to sit beside the shell configuration, in `~/.config/zsh/guides/`, one machine at a
time. On 2026-08-20 majkee gaveled B′: knowledge lives in the temple, executables on the surgical
table. The temple already held the research that guides grow out of, so one repository now carries
the whole line from research to synthesis to guide; a guide kept anywhere else stays invisible to
the corpus; and a single home ended the mirror-staleness coupling a cross-vendor audit had flagged.
The old folder became a pointer stub, and the loose `guide-writing.md` moved into its own slug in
the same session.

That session also fixed the shape: one topic per slug folder, a fixed `GUIDE.md` that is both the
door and the manifest, and a listing derived from disk rather than kept by hand. Writer rule 4 —
trust disk over doc — carries a scar: the remote-control card went on teaching tmux for five days
after its engine had dropped it.

On 2026-09-04 a triple audit found `raw/` uncodified. The fold gave every slug five three-letter
side-directory slots and drew the seam between `raw/` (inbound) and `src/` (outbound), with a
recorded lean that `src/` may fold into `raw/` if sessions keep guessing between them.

On 2026-10-12 the guides were looked at as instruments rather than documents. Some are consulted for
several different jobs, and every reader paid for all of them. The model shape answers that with a
controller that sends each reader to one function. Collapsing a guide into a controller squeezes its
story out — this file is where the story goes.

## Decisions

| date | decision | why | instead of |
|---|---|---|---|
| 2026-08-20 | B′ — guides live in the temple, executables on the table | one research → guide line; visible to the corpus; no mirror-staleness coupling | guides beside the zsh configuration |
| 2026-08-20 | the guide listing is derived from disk + frontmatter on every call | registers rot, derivation doesn't | a hand-maintained index |
| 2026-08-20 | `GUIDE.md` is the door and the manifest; an unnamed file is drift | the cheapest audit check, and a cleanup pass's protect-list | — |
| 2026-09-04 | five side-directory slots; `raw/` inbound, `src/` outbound | `raw/` was uncodified (triple audit) | — |
| 2026-10-12 | two shapes — flat (read to understand) and model (controller + functions) | a reader who arrives for one job should load only that job | converting every guide to one shape |
| 2026-10-12 | split by occasion of use, never by size | clean context is the reason to split; finishing the job outranks token thrift | splitting long guides by size or token budget |
| 2026-10-12 | a guide's story gets one door — `BACKGROUND.md`, no authority | the collapse to a controller removes the *why*; a human needs one door into `raw/`, `src/` and the journal | story left inside procedure; repurposing GLOSS, which explains a run |
| 2026-10-12 | the door is named BACKGROUND | says context-for-understanding with no authority to act; collides with nothing in the tree | README — already used in the tree, and read as "start here, act from me"; context — collides with the live-window sense and is broad enough to become a junk drawer; story — undersells the job |

## Where the material lives

- `~/ia-sync/_staging/dev-journal.guides.md` — the trace of the 2026-08-20 gavel (session `REP.Offc.Atlas-fable.guides`)
- `res/slug-directories.md` — the 2026-09-04 fold and the recorded `raw/` ↔ `src/` lean
- `~/ia-sync/.dev/session/guide-model-01-law/` and `…/guide-model-02-audit/` — the model-shape sessions, while their beds exist
