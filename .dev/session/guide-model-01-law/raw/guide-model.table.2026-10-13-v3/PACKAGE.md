---
title: guide-model — the table batch that starts the program
by: claude.ai seat · Symmetry project thread · from majkee's brief
what: every file the executors need, laid out by destination, and how to place and verify it
verified: 2026-10-13
batch: guide-model.table.2026-10-13-v3 — supersedes every earlier batch (v1, v2)
---

# guide-model — table batch (2026-10-13, v3)

Program **guide-model**: a guide consulted for several jobs becomes a controller with functions; a
guide read to understand stays flat; the story behind a guide gets one door (`BACKGROUND.md`).
Sessions, one gate each: **01-law** (the builder instruction first) → **02-audit** (one read-only
pass over the whole tree) → **03-…** conversions, guide by guide, authored by the head from 02's
frozen worklist.

## Place it

Unzip into a temporary folder, `cd` into it, then:

```text
B=$PWD
# 1 · anything already installed that differs from this batch? (an earlier batch, or a local edit)
find reposoma ia-sync -type f | while read -r f; do
  [ -e "$HOME/$f" ] && ! cmp -s "$f" "$HOME/$f" && echo "DIFFERS  ~/$f"
done
# 2 · copy what is new — never overwrites
cp -rn reposoma/. ~/reposoma/ && cp -rn ia-sync/. ~/ia-sync/
# 3 · prove the installed files are the reviewed ones
(cd ~ && sha256sum -c "$B/SHA256SUMS")
```

Step 1 prints nothing on a clean install. A `DIFFERS` line stops you: look at that file, and only if
the batch version is the one you approved, replace it on purpose — `cp "$B/<path>" ~/<path>` — then
rerun 1–3. Step 3 must print `OK` on every line. Newer `cp` may warn that `-n` is non-portable —
harmless. The sealed hypotheses file is **not** in this batch — it stays on your shelf until 02 step 6.

## What lands where

| file | lands in | role |
|---|---|---|
| `model-shape.md` · `write-background.md` | `~/reposoma/raw.guides/guide-writing/src/` | the law to gavel in 01 |
| `BACKGROUND.guide-writing.seed.md` | the same `src/` | the first BACKGROUND — confirm its rows; lands as `guide-writing/BACKGROUND.md` |
| `GUIDE.template.txt` · `FUNCTION.template.txt` · `BACKGROUND.template.txt` | the same `src/` | land in `ast/` in 01 |
| `WAVE-to-Symmetry_guide-model_addendum_2026-10-13.md` · `Symmetry-to-WAVE_guide-model_countersign_2026-10-13.md` | `~/reposoma/raw.guides/guide-writing/raw/` | review round 1 — registered in 01 |
| `WAVE-to-Symmetry_guide-model_batch-verification_2026-10-13.md` · `Symmetry-to-WAVE_guide-model_verification-return_2026-10-13.md` | the same `raw/` | review round 2 |
| `guide-census.py` | `~/ia-sync/_staging/` | the census (v3); promoted only if it earns reuse |
| `RUNBOOK.guide-model-01-law.md` · `RUNBOOK.guide-model-02-audit.md` | `~/ia-sync/_staging/guide-model/` | inert drafts until a session opens |
| `census.2026-10-12.md` | `~/ia-sync/_staging/guide-model/` | receipt — goes into the 02 bed's `raw/` |
| `PACKAGE.md` (this file) · `SHA256SUMS` | `~/ia-sync/_staging/guide-model/` | the program's door, and the install check the 01 head re-runs |

Until 01 lands, the census shows guide-writing's `src/` and `raw/` as unregistered — expected.

## Open a session

- **01:** `mkdir -p ~/ia-sync/.dev/session/guide-model-01-law && cp ~/ia-sync/_staging/guide-model/RUNBOOK.guide-model-01-law.md ~/ia-sync/.dev/session/guide-model-01-law/RUNBOOK.md` — then wake the head with its prompt-0.
- **02**, after 01's gate: the same for `guide-model-02-audit`, with `census.2026-10-12.md` into the bed's `raw/`.

Your read order: `model-shape.md` + `write-background.md` (to gavel) → `BACKGROUND.guide-writing.seed.md`
(confirm its rows) → `RUNBOOK.guide-model-02-audit.md` → `RUNBOOK.guide-model-01-law.md`.

## Rulings so far (majkee)

- The narrative door is named `BACKGROUND`; `background` is a reserved chapter word (2026-10-12).
- R2: one read-only whole-tree pass before the per-guide line (2026-10-13).

## Receipts

- census v3 on `hruzam/reposoma@core e80c398`: real-tree output identical to v2 and v1; the
  suffix-named orphan v1 missed is caught; stress 5/5; five of Wave's seven boundary probes now
  handled, the other two stated as limits in the script header. Details: `census.2026-10-12.md`.
- Placement dry-run on copies of both repos: a clean install adds files only and verifies `OK`; over
  a stale earlier batch, step 1 names every differing file and step 3 fails them.
- Nothing was written to either repo from this thread.

## Side flag — outside raw.guides, not this program's scope

- `~/ia-sync/HANDSHAKE.md`'s mounting table names `session/rellays-calude-codex/`; on disk the room
  is `.dev/session/rellays-claude-codex/`.
