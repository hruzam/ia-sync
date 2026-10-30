# G09 run-01 closeout — independent review and reconstructed handoff

2026-10-26 · Cartan(germline-03) · office · requested by Majkee after the session failed.

**DATA INTEGRITY: PASS. CLOSEOUT COMPLETENESS: FAIL.**

This is an independent reconstruction from the files, not the missing G09 head's self-report.
The G09 STATUS pen was not taken over and no resource-retirement command was repeated.

## What is reliable

- The pre-retirement manifest lists 62 original G09 files. All **61 non-retired originals**
  still match exact hashes. The only absent original is the explicitly retirement-allowed
  researcher vault; its exact ignored snapshot exists with SHA256 `5789ba86…69e6e9`.
- All nine protected foreign dirty-file hashes match the preservation baseline.
- Original RUNBOOK is unchanged and its snapshot is byte-identical. The authority's
  pre-close RUNBOOK/release/STATUS snapshots match their declared hashes. The old dispatch
  release was preserved as true; the current release is correctly revoked, false.
- R1 thread `01a176f7-532b-7722-9324-0ecb92694073` was archived: the supported command exited
  zero with hashed output; independent selected protocol observations find that exact ID
  in archived results and absent from active results. Its sole turn remains interrupted.
- Local close exited zero. The researcher vault and its shim lock are absent. Both state
  snapshots remain gitignored. No auditor vault or product was created.
- The verification helper's own app-server exited zero and was waited for. That fact is
  available even though a later, separate process-verification step failed.

These are archival/closeout observations, not a new live qualification of the transport.

## Missing or incomplete requested outputs

1. `raw/closeout/SELFREPORT.run-01.2026-10-26.md` does not exist; no alternate self-report
   filename was found in G09.
2. `_bus/06.caretaker.return.md` does not exist, nor does a cycle-06 Cartan VERDICT.
3. `STATUS.md` still says caretaker cleanup is in flight and archive/close outcomes pending.
   Its checkpoint records preservation/revocation, but it never reaches the required handback.
4. Full owned-process/native-worker quiescence is unverified. Resource record 07 has status
   failed and never supplies final candidate-process, cleanup-hold or native-worker disposition.
   A native handle is not an OS PID; this review cannot claim it was stopped or remained active.

## Why the last verifier failed

`raw/closeout/resources/controller_verify.py:50` reads `/proc/1/ns/pid` to label the check
as host-qualified. In the same escalated host context, the focused reproduction gave:

```text
/proc/self/ns/pid -> pid:[4026531836]
/proc/1/ns/pid    -> PermissionError, errno 13
```

The helper's outer handler saves status failed after that exception. Earlier archive-list,
thread-read and owned-app-server-exit facts remain valid. The failed process observation
must be a specific cleanup hold. It does not justify omitting the self-report, and no evidence
establishes that it was the only reason the head stopped before delivering the handback.
Do not rerun archive/close operations: those effects already completed.

## Reconstructed run-01 facts

Goal: a read-only zsh browser for germline, guides and native skills, testing a fresh main
delegating whole consultation mechanics. Actual work stopped during C1. Native caretaker
`/root/caretaker` was used; Astrobley, A1 and product implementation never started.

One target attempt was consumed; zero completed consultations were validated. The first
R1 request reached the model, performed research, and was interrupted at the local deadline.
The initial null vault was not proof of remote absence. G03 recovered the exact prompt-bound
thread/turn by zero-turn filtered protocol reads. The original failed receipt/adapter remain
unchanged. The candidate checkpoint patch remains unapplied.

The final run-01 product/context disposition remains PRODUCT UNVERIFIED, DELEGATION
INDETERMINATE, gate unmet. Resource retirement subsequently archived the stored thread and
closed the local vault, without establishing all native-worker lifecycle facts.

## Main-context measurement problem

The **707-word value measures only the three specified starter files**. It is not actual
main-context consumption. `raw/control/main-events.json` reports nine additional task-document
reads, ordinary shared-law/harness reads, a truncated batch followed by rereads, and later
TUNNEL/selected operational-evidence intake. It also records zero routine main tunnel CLI
operations. Those are distinct observations; neither proves a clean main or total savings.

The next trial should measure all additional task material actually consumed by the main,
including exception intake. My starter-packet metric was too narrow to answer Majkee's real
question on its own. Native token/context occupancy measurements remain unavailable.

## What this permits for preparation

The preserved evidence is usable for rebuilding the same G09 bed with explicit run-01/run-02
continuity. Preserve the incomplete closeout and its cleanup hold; do not present this document
as a completed self-report or overwrite missing RETURN/VERDICT on behalf of their writers.
Final native-worker disposition still needs explicit evidence or an operator-confirmed reset.
Planning can use the recovered facts without treating the old run as successful or its spend
as erased. No new run is started by this review.

## Evidence

All G09 paths above are under `/home/hruzam/ia-sync/.dev/session/germline-09-source-reader/`.
Primary preservation: `raw/closeout/PRESERVATION.run-01.json`, authority and snapshots.
Primary effects: resource receipts 02/03/05/06 and their verified output hashes.
Partial verification: `raw/closeout/resources/07.archival-and-process-verification.json`.
Independent review: native `/root/g09_package_review` returned DATA INTEGRITY PASS /
CLOSEOUT COMPLETENESS FAIL after direct source/hash checks, without executing helpers.
Machine-readable review: `_staging/codex/g09-R1-diagnostic.2026-10-26/closeout-output-review.json`.
