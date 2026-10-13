---
title: guide-census receipt — raw.guides on 2026-10-12, with stress and template proofs
by: claude.ai seat · Symmetry project thread
source: hruzam/reposoma@core e80c398 (shallow clone, 2026-10-12)
what: proof that the census runs on the real tree, catches planted defects, and passes a guide filled from the templates. Stale with the next commit — the auditor re-runs it (RUNBOOK 02, step 2).
---

## Proofs (final script version)

- **Stress — deliberate red, sandbox copy:** 5/5 planted defects caught — a dead `res/` pointer, an
  unregistered `res/` file, an undeclared directory, a stale clock, a mirror banner. The real tree
  stayed untouched (`git status` clean).
- **Templates:** a toy guide filled from `GUIDE` / `FUNCTION` / `BACKGROUND.template.txt` reads clean
  (`fm ok · shape model · bg y`, nothing unregistered, nothing dangling). Editing one function's
  `occasion:` without its row → `table-drift` caught.

## Flagged rows checked by hand (a census is not truth until checked)

- **meeting** — dangling `participants.md` is real: the file is `res/participant.md`.
- **cold-start-card** — dangling `HANDOFF.md`, `STATUS.md` are real: the Manifest names tombstones
  whose files were deleted.
- **sella** — `manifest-heading≠law` is real: the section is "Wired surfaces (vault manifest …)"; the
  registrations themselves are complete.
- **tunnel** — `−machine` is real.
- **sella** — fresh 41/42 days: STALE from 2026-10-13.

## Reading the columns

`fm` ok · no-yaml · −missing keys — `clock` verified date, fresh/STALE age/half-life, or no-clock —
`res` chapter count (✗ = missing `chapter-of:`) — `side` raw/src/ast/cod present — `jnl` dev-journal —
`bg` BACKGROUND.md — `unregistered` siblings named in neither Manifest nor Functions — `dangling`
`res/` pointers to missing files — `flags` mirror · non-kebab · undeclared dirs · manifest heading ·
table drift.

## guide-census · ~/reposoma/raw.guides · 2026-10-12

Facts only — verdicts belong to the auditor.

## Folders

| slug | lines | fm | shape | clock | res | side | jnl | bg | unregistered | dangling | flags |
|---|---|---|---|---|---|---|---|---|---|---|---|
| PAD | 134 | no-yaml | — | — | 0 | raw | — | — | (no manifest section: 1 siblings) | — | non-kebab |
| browser-egress | 115 | ok | — | 2026-08-24 no-clock | 0 | — | — | — | — | — | — |
| bus | 207 | ok | — | 2026-09-05 no-clock | 0 | — | — | — | — | — | — |
| codex-builder-user | — | no-GUIDE | | | | | | | | | 3 md, 0 mirror-bannered |
| cold-start-card | 188 | ok | — | 2026-08-27 no-clock | 3 | — | — | — | — | HANDOFF.md, STATUS.md | — |
| gemini-seats | 190 | ok | — | 2026-07-27 no-clock | 0 | — | — | — | — | — | — |
| geminicli@com | — | no-GUIDE | | | | | | | | | 1 md, 0 mirror-bannered |
| germline-forge | 148 | ok | — | 2026-10-07 fresh 5/30d | 3 | raw | — | — | — | — | — |
| gloss | 94 | no-yaml | — | — | 0 | — | — | — | — | — | — |
| guide-writing | 126 | ok | — | 2026-09-04 no-clock | 1 | — | — | — | — | — | — |
| handoff | 3 | no-yaml | — | — | 0 | — | — | — | — | — | — |
| harness-check | 100 | ok | — | 2026-07-11 no-clock | 0 | — | — | — | — | — | — |
| intake | — | no-GUIDE | | | | | | | | | 6 md, 0 mirror-bannered |
| laravel-daily-epistemics | 66 | ok | — | 2026-08-20 no-clock | 0 | — | — | — | — | — | — |
| machine-home | 511 | ok | — | 2026-06-28 no-clock | 0 | — | — | — | — | — | — |
| machine-office | 242 | ok | — | 2026-07-15 no-clock | 0 | — | — | — | — | — | — |
| meeting | 192 | ok | — | 2026-09-16 no-clock | 3 (✗chapter-of 1) | raw src | — | — | src/, res/README.md | participants.md | — |
| piql | — | mirror-dir | | | | | | | | | 3 md, 3 mirror-bannered |
| project-base-pattern | 54 | no-yaml | — | — | 0 | — | — | — | — | — | — |
| project-topology | 76 | ok | — | 2026-09-02 no-clock | 0 | — | — | — | — | — | — |
| reach | — | mirror-dir | | | | | | | | | 2 md, 1 mirror-bannered |
| regime-session | 167 | ok | — | 2026-07-20 no-clock | 0 | — | — | — | — | — | — |
| remote-cli | 170 | ok | — | 2026-09-11 fresh 31/60d | 0 | — | — | — | — | — | — |
| remote-control | 165 | ok | — | 2026-10-08 fresh 4/42d | 0 | — | — | — | — | — | — |
| research.web | — | no-GUIDE | | | | | | | | | 1 md, 0 mirror-bannered |
| runbook | 231 | ok | — | 2026-09-17 no-clock | 7 | raw ast | — | — | — | — | — |
| sella | 483 | ok | — | 2026-09-01 fresh 41/42d | 1 | raw src | y | — | — | — | manifest-heading≠law |
| session-browser | 103 | ok | — | 2026-09-09 no-clock | 0 | — | — | — | — | — | — |
| status | 178 | ok | — | 2026-09-05 no-clock | 0 | — | — | — | — | — | — |
| temple-mail | 117 | ok | — | 2026-07-11 no-clock | 0 | — | — | — | — | — | — |
| tree-snapshot | 62 | ok | — | 2026-07-11 no-clock | 0 | — | — | — | — | — | — |
| tunnel | 142 | −machine | — | 2026-10-03 no-clock | 4 | src | y | — | — | — | — |

## Loose top-level files (legacy zone)

| file | lines | fm | clock | flags |
|---|---|---|---|---|
| audit-loop.card.draft.md | 59 | no-yaml | — | — |
| bootstrap-new-project.md | 72 | −title,scope,audience,machine | 2026-10-08 fresh 4/90d | — |
| guide-publishing.md | 60 | no-yaml | — | — |
| onboarding-kit.md | 79 | −title,scope,audience,machine | 2026-10-08 fresh 4/90d | — |
| project-intake.md | 45 | no-yaml | — | name-overlap:intake/ |
| recover-broken-loop.md | 60 | no-yaml | — | — |
| research-program-brief.md | 106 | no-yaml | — | — |

## Counts

- entries 39 · slug folders 26 · other folders 6 · loose files 7
- frontmatter: no-yaml 4 · missing keys 1
- STALE 0 · no half-life clock 18
- unregistered siblings in 2 slugs · dangling res/ refs in 2 slugs
- shape declared 0 · BACKGROUND.md 0 · journals 2
