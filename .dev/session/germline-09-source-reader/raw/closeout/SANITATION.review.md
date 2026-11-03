# Independent sanitation verification

2026-10-26 · `/root/g09_sanitation_verifier` · read-only verifier.

VERDICT: PASS

TASK: Verify bounded G09 run-01 sanitation: evidence preserved, exact owned resources
retired, R1 archived-only/notLoaded/interrupted, release false, no new work or signals,
honest reconstructed report, cycle07 closure, and unchanged unmet gate.

RAN: Read authority/final/report/preservation/bus/status/release/controller receipts and
helper source; recalculated all manifest SHA-256/byte counts; recalculated receipt,
snapshot and report hashes and word count; asserted JSON state; checked vault, lock and
cycle06-record absence; ran `git diff --check`.

EVIDENCE: 61/61 protected originals matched hash and bytes; sole allowed vault absent;
9/9 foreign hashes matched. Four snapshots and all receipt-linked hashes matched.
R1 receipt proves archived-only, notLoaded, sole turn interrupted. Controller receipt
records ENOENT/errno 2 for PIDs 1319728/1923120/1923121 in pid:[4026531836], no signals,
and exact stale-presence removal with no collateral removals. Report is explicitly
reconstructed and 684 words. STATUS has in_flight none, unchanged gate text, gate unmet;
release remains false. Cycle06 RETURN/VERDICT remain absent; cycle07 closes sanitation.

FAILURES: none.

RESIDUAL RISK: Old native-head termination remains operator-reported and its inaccessible
handle was not inspected; this is not whole-host quiescence certification.

Finalization note: the verifier observed independent_review pending and the cleanup
attachment still active, as expected while its verdict was pending. Cartan consumes this
PASS in SANITATION.final.json, then detaches only its exact cleanup attachment and records
that operation separately.
