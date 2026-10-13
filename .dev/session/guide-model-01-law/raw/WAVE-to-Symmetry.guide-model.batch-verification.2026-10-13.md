---
title: "guide-model — Wave verification of the full table batch"
scope: guide-model
audience: "majkee + Symmetry + execution heads"
machine: both
verified: 2026-10-13
state: "REVIEW — SIGN on reconciled design; SIGN WITH CONDITIONS on launch material"
authority: "Findings and recommendations only. No repository canon amended. majkee gavels."
agent: Wave
source_batch: guide-model.table.2026-10-13.zip
---

# guide-model — full-batch verification

## Verdict and evidence boundary

**SIGN for the reconciled R1–R6 design. SIGN WITH CONDITIONS for launching from this batch.**

The ZIP contains the revised working files, not merely a countersign describing intended edits. The R4 suffix-matching fix reproduces. Two concrete launch hazards need correction: existing drafts can survive the advertised upgrade copy unnoticed, and the stress procedure uses an unowned fixed temporary directory. These do not require another architectural round.

**Weakest remaining assumption:** that the files executed on the operator's machine will actually be the reviewed versions. The package's non-overwriting copy does not establish that when an earlier batch is present.

This report distinguishes inspection, reproduced sandbox behavior, and recommendations. It does not certify a live session or the full repository tree. Symmetry remains the folding executor; nothing below is a claim that a proposed correction has already landed.

## Sources and scope

All local path:line references below are relative to the ZIP's `guide-model.table.2026-10-13/` directory. Short names resolve as follows:

| Short name | Actual archive path |
|---|---|
| PACKAGE | `PACKAGE.md` — identical to `ia-sync/_staging/guide-model/PACKAGE.md` |
| 01 | `ia-sync/_staging/guide-model/RUNBOOK.guide-model-01-law.md` |
| 02 | `ia-sync/_staging/guide-model/RUNBOOK.guide-model-02-audit.md` |
| census | `ia-sync/_staging/guide-census.py` |
| model-shape | `reposoma/raw.guides/guide-writing/src/model-shape.md` |
| write-background | `reposoma/raw.guides/guide-writing/src/write-background.md` |
| templates and seed | the same `guide-writing/src/` directory |
| countersign | `reposoma/raw.guides/guide-writing/raw/Symmetry-to-WAVE_guide-model_countersign_2026-10-13.md` |

The current `hruzam/reposoma:core/raw.guides/runbook/GUIDE.md` was read first through the GitHub connector. Returned content blob: `28479a2349853bc8c89b2b4dbd6e005f468770fb`. It defines the launcher/STATUS separation, numbered prompts, one gate, and promotion before pruning. This was a targeted governing-file check, not a repository-wide reread.

The ZIP has **14 regular files**, including the two identical PACKAGE copies. The separate sealed hypotheses are absent from it. Archive extraction rejected unsafe paths and symlink entries and used a separate local directory. Earlier attachments and all extracted source files were left unchanged.

The earlier hypothesis text has already appeared in this conversation. I did not use it for this review or give individual guides shape verdicts. **This conversation must not be treated as the fresh blind auditor for session 02.**

## Reconciliation against the actual files

| Item | What is physically present | Assessment |
|---|---|---|
| R1 | model-shape:89–91,109–112 preserve reasons the job needs on the operational path; write-background's sort test and review check match | Fold confirmed; qualify the old K3 shorthand as noted in F3 |
| R2 | PACKAGE:12–14,54–57 and 02:37–38 put the whole-tree audit before the later per-guide conversions; 02:167–173 describes fresh tasklines and the consultant stream | Ruling implemented; not reopened |
| R3 | model-shape:48–50,56–61,164–172 and GUIDE.template.txt:13–16 supply the two-section logical register and the no-matching-row stop | Fold confirmed; behavior still needs the actual witness |
| R4 | census:19–28,123–131 replace substring registration with token matching | Specific regression fixed and reproduced; helper remains a bounded detector |
| R5 | 01:12–18,50–64 and 02:13–20,87–99 bind a transferable head, give it STATUS, and use the existing transfer posture | Fold confirmed; not a permanent agent/vendor assignment |
| R6 | PACKAGE:40,46–49 retains the chosen session root and names | Confirmed; no objection |
| S1 | 02:8–12,96–98,137–141,191–193 preserve worklist/report and name their durable destination | Intention confirmed; clarify the write-scope exception in F5 |

The head/writer/witness prompts in 01 and head/auditor/recreator prompts in 02 are numbered consistently. Both RUNBOOKs have one `gate:`, `status_owner: head`, an `observations_read` line, and no `state:` field. Seat placeholders remain draft authoring fields; I did not treat their presence as proof that real seats have been bound.

## Findings — risk ordered

### F1 — A superseding batch can leave the superseded files active

**Severity: blocking before applying over an earlier batch.**

**Claim:** The placement instructions do not guarantee installation of this revision.

**Evidence:** PACKAGE:16 says this batch supersedes earlier ZIPs. PACKAGE:20–29 prescribes `cp -rn` into the existing repositories and says every file lands. In a disposable fake home, the commands returned exit 0 while retaining both an earlier `guide-census.py` and an earlier `model-shape.md`; new files were copied around them. The destination can therefore become a mixed-version package without an error.

**Consequence:** Review can correctly approve v2 while the executor still runs v1 or folds the old law. This is more material than the original substring defect because it can prevent the fix from arriving at all.

**Fix in one line:** Compare destinations first; skip only byte-identical files, stop on differing files for review, explicitly apply the approved updates, and verify installed contents against the batch.

Do not replace `-n` with unconditional overwrite across an active worktree. Preserve the maintainer stopping-point check and unrelated edits. A clean first installation is not the failing case.

### F2 — The stress test does not own its temporary directory

**Severity: blocking before running 02's stress step.**

**Claim:** A fixed `/tmp/ga-sandbox` is unsafe to reuse and can invalidate the test.

**Evidence:** 02:109–112 copies `raw.guides` to `/tmp/ga-sandbox`, then deletes that destination recursively. In an isolated reproduction with an already-existing destination, `cp -r` put the new tree inside a nested `raw.guides/` while leaving an unrelated sentinel beside it. Running the census at the original destination would no longer inspect the intended root, and the prescribed recursive deletion would include the unrelated sentinel.

**Consequence:** A repeat or parallel audit can inspect the wrong tree or remove another run's scratch material. The dangerous deletion against a real shared path was not executed in this review.

**Fix in one line:** Allocate a unique directory with `mktemp -d`, copy the contents into that exact root, use the returned path for every plant and census call, and clean up only that owned directory.

This needs a small shell correction, not a sandbox framework.

### F3 — The audit shorthand still contradicts R1's working-reason distinction

**Severity: should — before the law is used as session 02's yardstick.**

**Claim:** The R1 fold is present, but the defect list retains wording that can undo it.

**Evidence:** model-shape:89–91 and 109–112 keep a reason the job needs beside its rule. K3 at model-shape:157 still flags “story, rationale and incident narrative inside procedure” without distinguishing historical rationale from a working reason.

**Consequence:** A literal K3-driven cleanup could remove precisely the operational understanding R1 protects.

**Fix in one line:** Qualify K3 as historical or non-operational rationale, explicitly excluding reasons required to perform the job correctly.

This implements the settled R1 decision; it does not ask majkee to decide it again.

### F4 — Census output is narrower than a general claim of structural validity

**Severity: should — correct the reliance language; targeted hardening is optional where manual checks cover the boundary.**

**Claim:** Exact-token matching closes the reported suffix defect, but a clean row still does not prove all metadata and registration properties.

**Evidence:** 02:115–116 tells the auditor not to re-derive mechanical facts by reading. census:30–41 uses a line-oriented frontmatter extractor, 111–112 checks the presence rather than the value of `chapter-of`, 123 tokenizes all register-section text, and 138 checks the raw `shape` value against one literal string. The seven boundary probes below reproduce the limitations.

**Consequence:** An audit relying exclusively on the table can inherit false negatives, a misleading mirror flag, or an aborted run.

**Fix in one line:** Keep this helper, state its supported checks and formatting assumptions, and permit focused verification of anomalies and unsupported cases instead of forbidding rechecking.

I am not requesting a full YAML/Markdown parser or another tool. Small corrections—such as checking the parent slug, normalizing the shape scalar, or distinguishing a source mirror banner from a quoted evidence example—can be selected in proportion to actual use. Required-key presence and nonempty-value validation are different checks; I do not claim the original C4 definition promised the latter.

### F5 — Preservation and the read-only constraint need an explicit boundary

**Severity: should — before 02's closure/promotion instructions are executed.**

**Claim:** S1 gives the head a preservation task outside the bed while the blanket constraints still describe the whole session as read-only outside it.

**Evidence:** 02:96–98 directs promotion to `~/reposoma/raw.guides/guide-writing/raw/`; 02:177 allows writes only in the bed, and 02:209 says the session does not migrate or delete anything. The governing runbook's “On gate closure” requires promotion before pruning.

**Consequence:** A literal executor must either stop at the stated boundary or infer an unstated exception. The intended distinction is clear to a human but should be explicit for the agent.

**Fix in one line:** Keep the audit read-only and explicitly authorize only the head's named post-gavel evidence promotion and governed bed cleanup, without authorizing changes to guide canon.

This is a scope clarification, not an objection to durable evidence or to the chosen destination.

### F6 — The countersign's current-state summaries are still stale

**Severity: nit — record consistency.**

**Evidence:** The ZIP's countersign is byte-identical to the separately supplied one. Lines 16–17,22,57–62,131 and155 still leave R2 awaiting a ruling, while lines 8,147–150,156 and159 record that the ruling is made and no review questions remain. PACKAGE and 02 carry the correct ruling.

**Fix in one line:** Mark the earlier conditional verdict and pipeline alternative as superseded by the dated R2 ruling and make the current summary say no R2 decision remains open, while preserving the historical proposal.

Do not ask majkee the R2 question again.

### F7 — The new no-match instruction lacks a dedicated witness row

**Severity: should — behavioral acceptance coverage.**

**Evidence:** The controller and GUIDE template now say an unmatched job must be reported rather than causing an all-functions read. 01:106–128 tests named occasions, scaffolding, background, and listing behavior, but contains no explicit unmatched-job test. “One row per Functions row” cannot itself cover the absence of a matching row.

**Fix in one line:** Add one prompt for a genuinely unmatched job to the existing fresh-session witness and verify that the agent reports the gap and stops dispatching rather than inventing a route or loading every function.

This is a test recommendation, not a claim that the new behavior has failed in a real agent session.

## Validation actually performed

**15 baseline checks passed.** Those include syntax, two mechanical template fixtures, five individual planted defects, the v1/v2 suffix-orphan regression, occasion drift, missing occasion, a missing required key, CLI execution, and unchanged-input checks. They are not 15 agent-behavior trials.

| Check group | Observed result |
|---|---|
| Basic five plants | Missing res pointer, orphan res file, undeclared directory, expired clock, and mirror banner all detected |
| Suffix orphan | `res/run.md` beside registered `res/user-run.md`: earlier script misses it; ZIP's v2 reports it |
| Template fixtures | A two-job controller/function/background shelf fixture reads mechanically clean; a simulated guide-writing using supplied write-background and seed also reads clean |
| Drift/header checks | Changed occasion, absent occasion, and absent required key detected |
| Input integrity | CLI left fixture files unchanged; all extracted batch file hashes remained unchanged |
| Package structure | 13 Markdown/text files have balanced fences; PACKAGE copies match; sealed hypotheses absent; prompts/gates/STATUS ownership checks pass |
| Installation over old files | The no-clobber copy returned 0 but kept both deliberately stale destination files |
| Fixed scratch path reuse | Copy nested the source inside the pre-existing destination; cleanup target would include unrelated content |

### Extended boundary probes — not covered by the baseline success

These are additional tests, not a claim that Symmetry reported having passed them.

| Input | Result from the supplied census |
|---|---|
| Wrong `chapter-of: wrong-slug` | No parent-mismatch flag |
| `shape: "model"` plus a mismatched occasion | Quoted shape retained literally; drift check skipped |
| The same function registered in Functions and Manifest | No duplicate-registration flag |
| Mirror banner inside a fenced example in `raw/observation.md` | Owning guide receives `mirror×1` |
| An orphan named only in prose saying it is not registered | Orphan treated as registered |
| Present but empty `machine:` field | `fm ok` |
| Impossible verified date with half-life metadata | Uncaught ValueError; census process exits 1 |

The baseline and boundary results are reported separately because the first validates the promised change and the second bounds what may safely be inferred from it.

## What I did not check

- I did not execute the census over a complete current or pinned `reposoma` checkout. Symmetry's reported 39-entry real-tree comparison remains her evidence, not mine.
- I did not inspect the complete seven-chapter runbook resource set in this pass, re-audit every governing guide, inspect the Codex-side `/guide` implementation, or test installed skills on either user machine.
- I did not run session 01 or 02, bind real seats, invoke a fresh behavioral witness, deploy anything, commit, or modify either repository.
- I did not give individual guides shape verdicts or use the sealed hypothesis guesses as evidence.
- I did not turn this review's test harness into proposed program machinery.

## Smallest next move

Symmetry should fold F1 and F2 as launch corrections; bring K3 and the preservation scope into agreement with the settled instructions; bound the census reliance and add the unmatched-job witness row. Keep the chosen architecture, the living audit card, the transfer posture, and the agreed session order.

Return disposition by F1–F7 with the exact changed files and tests actually rerun. A disagreement is a CHALLENGE, not an implied instruction to implement every suggestion. majkee's gavel remains the promotion authority.

## AI HANDOFF

**Goal:** Verify the full revised batch against the reconciled review decisions, with actual source inspection and bounded local reproduction.

**Current state:** Design reconciled; actual folds confirmed; census suffix regression passes. Launch readiness remains conditional on F1 and F2. Other findings have explicit should/nit scopes.

**Decisions made:** No earlier ruling changed. R2 remains whole-tree audit first. No new canon approved.

**Files changed:** No supplied file or repository changed. Created this review, test harness/results, source excerpts, hashes, structural checks, and a comparison diff in the local review workspace.

**Validation performed:** The checks and limitations above; exact machine-readable results accompany this report.

**Open questions / risks:** F1–F7 await executor disposition; live installation and behavioral witness remain unverified.

**Recommended next move:** Symmetry folds the bounded corrections and returns an updated batch or focused diff with validation evidence.

**Agent:** Wave

## Batch fingerprint

SHA-256 of reviewed ZIP:

```text
a964837f8ab0ef8ce70f4087c07e8a0ff297d2d0f149c4f4e1a06c7db95ae684
```
