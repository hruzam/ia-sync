---
title: guide-model — the package that starts the program
by: claude.ai seat · Symmetry project thread · 2026-10-12, from majkee's brief
what: the files that open program guide-model, where each goes, and in what order
---

# guide-model — package

Program **guide-model**: a guide consulted for several jobs becomes a controller with functions; a
guide read to understand stays flat; the story behind a guide gets one door (`BACKGROUND.md`).

Sessions, one gate each: **01-law** (the builder instruction first) → **02-audit** (every entry gets
a verdict) → **03-…** conversions, batch by batch, authored by the next head from the 02 return.

| file | goes to | when |
|---|---|---|
| `model-shape.md` | `~/reposoma/raw.guides/guide-writing/src/` | now — staging; lands in 01 |
| `write-background.md` | the same `src/` | now — the BACKGROUND standard; lands as `res/write-background.md` in 01 |
| `BACKGROUND.guide-writing.seed.md` | the same `src/` | now — confirm its Decisions rows; lands as `guide-writing/BACKGROUND.md` in 01 |
| `GUIDE.template.txt` · `FUNCTION.template.txt` · `BACKGROUND.template.txt` | the same `src/` | now — they land in `ast/` in 01 |
| `guide-census.py` | `~/ia-sync/_staging/` | now — the census; promoted only if it earns reuse |
| `RUNBOOK.guide-model-01-law.md` | `~/ia-sync/.dev/session/guide-model-01-law/RUNBOOK.md` | when you open 01 |
| `RUNBOOK.guide-model-02-audit.md` | `~/ia-sync/.dev/session/guide-model-02-audit/RUNBOOK.md` | when you open 02 |
| `hypotheses.reconcile-only.md` | your own shelf — never inside the 02 bed | to the auditor at 02 step 6 |
| `census.2026-10-12.md` | the 02 bed, or discard | receipt only — stale with the next commit |

Your read order: `model-shape.md` + `write-background.md` (to gavel) → `BACKGROUND.guide-writing.seed.md`
(confirm its rows) → `RUNBOOK.guide-model-02-audit.md` → `RUNBOOK.guide-model-01-law.md`.

## Receipts

- The census ran on `hruzam/reposoma@core e80c398`: 5/5 planted defects caught on a sandbox copy; a
  toy guide filled from the three templates reads clean; table drift caught. Details:
  `census.2026-10-12.md`.
- Nothing was written to either repo from this thread.

## Side flag — outside raw.guides, not this program's scope

- `~/ia-sync/HANDSHAKE.md`'s mounting table names `session/rellays-calude-codex/`; on disk the room
  is `.dev/session/rellays-claude-codex/`.
