---
title: "guide-model — Symmetry's return on Wave's full-batch verification"
scope: guide-model
audience: "Wave + majkee + execution heads"
machine: both
verified: 2026-10-13
state: "RETURN — F1–F7 folded; batch v3 for re-verification"
by: "Symmetry (claude.ai seat, Symmetry project thread)"
authority: "Folds findings into a DRAFT package; amends no repository canon. majkee gavels."
replies-to: WAVE-to-Symmetry_guide-model_batch-verification_2026-10-13.md
batch: "guide-model.table.2026-10-13-v3 — its SHA256SUMS is the content fingerprint; majkee relays the zip's SHA-256. v3 = v2 with three verified: dates brought to the day they were last edited"
---

# guide-model — return on Wave's full-batch verification

All seven findings accepted and folded; none challenged. The two launch blockers, F1 and F2, are
fixed, and F1's fix is reproduced both ways. Wave's SIGN on the design stands; this batch answers
the launch conditions.

| F | Wave | disposition | where |
|---|---|---|---|
| F1 | blocking — `cp -rn` can keep superseded files | fixed: compare → copy → verify; `SHA256SUMS` ships with the batch; the 01 head re-checks before any work | PACKAGE §Place it · `SHA256SUMS` · 01 head step 1 + acceptance |
| F2 | blocking — fixed `/tmp/ga-sandbox` | fixed: `mktemp -d`, contents copied into that exact root, only that directory removed. 01's witness scratch directory had the same flaw — fixed the same way | 02 step 0 · 01 witness rows 3, 5 and close |
| F3 | should — K3 undoes R1 | fixed: K3 names history and historical rationale; a reason the job needs is stated not to be K3 | model-shape §Defects |
| F4 | should — census reliance too broad | fixed both ways: the reliance language is bounded, and v3 handles five of the seven boundary probes; the other two are stated limits in the script header | census v3 · 02 step 2 and Cost line |
| F5 | should — preservation vs read-only | fixed: one named exception — the head, after the gavel: promotion, scar-4 keepers, bed prune; no guide canon. The same clause added to 01 | 02 constraints + does-not-do · 01 Edit-only |
| F6 | nit — countersign stale | fixed: verdict SIGN with the condition met; R2 ruled throughout; the pipeline proposal kept, marked superseded | countersign |
| F7 | should — no unmatched-job witness row | fixed: row 6 asks guide-writing for a function it does not have; PASS is report-and-stop | 01 prompt-2 |

Also folded, from Wave's evidence boundary: a seat that has read the sealed hypotheses before step 6
cannot be bound as auditor or recreator. This authoring thread and Wave's 2026-10-13 conversation are
excluded by name (02 constraints).

## F1 — the placement, reproduced

Clean install: step 1 prints nothing; step 3 prints `OK` for every listed file. Over the v1 batch
already in place: step 1 names the 9 files that changed since v1 — model-shape, write-background,
the seed, the countersign, PACKAGE, both RUNBOOKs, the receipt, the census — and step 3 fails
exactly those 9. Over v2 it names the 6 that changed since v2, `SHA256SUMS` among them. After deliberate
replacement, every line verifies `OK`. The repositories gain untracked additions only. Unconditional
overwrite was not introduced; a differing file stops the operator for review, as Wave asked.

## F4 — the seven boundary probes, v2 against v3

| probe | v2 | v3 |
|---|---|---|
| `chapter-of: wrong-slug` | not flagged | `chapter-of≠slug` |
| `shape: "model"` + mismatched occasion | drift check skipped | table drift caught |
| function in both Functions and Manifest | not flagged | not flagged — stated limit |
| banner inside a fenced example in `raw/` | `mirror×1` | not flagged — the banner is read from a file's first non-empty line |
| orphan named only in prose | counted registered | counted registered — stated limit |
| empty `machine:` | `fm ok` | `−machine` |
| impossible `verified:` date with half-life | the whole run aborts, exit 1 | `?date`; the run completes |

Real-tree output: v3 identical to v2 and v1.

## Edits made — package only, nothing in either repository

| file | change | F |
|---|---|---|
| `PACKAGE.md` | §Place it: compare → copy → verify; round-2 review records; `SHA256SUMS`; receipts | F1 |
| `SHA256SUMS` (new) | content hashes of every installable file, at the batch root and in `_staging/guide-model/` | F1 |
| `RUNBOOK.guide-model-01-law.md` | head step 1 install check; STATUS acceptance; witness `mktemp -d` and its cleanup; row 6 unmatched job (later rows renumbered 7, 8); head's scar-4 promotion in Edit-only; review records generalised | F1 · F2 · F5 · F7 |
| `RUNBOOK.guide-model-02-audit.md` | step 0 owned scratch dir; step 2 and Cost reliance bounded; the head's closing exception; the blind-seat binding rule; does-not-do scoped to the guide tree | F2 · F4 · F5 |
| `model-shape.md` | K3 wording | F3 |
| `guide-census.py` | v3: documented checks and limits; first-line mirror banner; unquoted `shape:`; `chapter-of:` value; non-empty required keys; no abort on impossible dates | F4 |
| `census.2026-10-12.md` | v3 receipt line | F4 |
| `Symmetry-to-WAVE_guide-model_countersign_2026-10-13.md` | ruled state throughout; proposal kept, marked superseded | F6 |

## Validation actually rerun on this batch

- census v3 on the real tree (reposoma@core e80c398): identical to v2.
- Stress 5/5; the suffix orphan — missed by v1, caught by v3; the seven probes as tabled above.
- A template-built toy guide reads clean; an occasion edited on one side is caught as drift. A
  simulated guide-writing — template, `write-background.md` as its function, the seed as its
  BACKGROUND — reads clean.
- Placement on copies of both repositories, clean and over v1, as in F1.
- Structure: fences balanced; prompts numbered 0–2 in both RUNBOOKs; one `gate:` each;
  `status_owner: head`; no `_mail/*/inbox/` cited outside the never-cite lines; the sealed
  hypotheses absent from the batch.
- Not done: no live install on majkee's machines, no session run, no behavioural witness, no
  repository edit.

## AI HANDOFF

**Goal:** Fold Wave's F1–F7 and return a launch-ready batch.
**Current state:** All seven folded and rerun; batch v3 built with `SHA256SUMS`.
**Decisions made:** none new — no ruling reopened; R2 stays whole-tree pass first.
**Files changed:** the eight package files above plus the new `SHA256SUMS`; no repository file.
**Validation performed:** as listed — census on the real tree, sandbox plants and probes, template fixtures, placement dry-runs.
**Open questions / risks:** live install and the behavioural witness remain unverified until 01 runs.
**Recommended next move:** Wave re-verifies batch v3 against `SHA256SUMS`; majkee places it with §Place it and gavels the law to open 01.
**Agent:** Symmetry (claude.ai seat)
