<!-- Origin: .dev/session/germline-07-make-program/raw/experiment_1/RESULT.md; preserved: .dev/records/germline/2026-11-03/germline-07-make-program/raw/experiment_1/RESULT.md; sha256: 55f6baa00955fdfc9f60ea0d9c5440e97cb6451efc0ee7018ea5fb12269959b8; preservation commit: pending (local-only); promoter: myShell. Original body follows verbatim. Relative links in that body use its original directory; use the preserved source/legacy alias for navigation. -->

# experiment_1 — Codex-only caretaker trial

2026-10-23 · Cartan · office · disposition: operational pass with reporting correction and
explicit limits; ready for Majkee's acceptance, not production qualification.

## What ran

One main used the SAME native caretaker `/root/experiment_1_caretaker` across two assignments.
The caretaker consumed the deploy-inert controller/function specimen and operated two distinct
named Codex threads through the existing source shim. Each peer completed one bounded source
task: the tunnel GUIDE's opening/recovery claims, and the Python implementation's birth/save
behavior. Cartan then repeated those tasks directly on the same threads. Four target-model
turns total were used. The same caretaker resumed/read both threads without another target
turn; Cartan independently repeated the protocol reads and checked selected reply hashes.

Majkee's exclusion of `claude -p` is a trial requirement. No Claude process, SDK, new API key,
authentication mechanism, global agent, daemon, or transport-source change is introduced.
The existing Codex account's observed target model/effort was `gpt-6.1-sol` / `xhigh`, with
effective readOnly sandbox and networkAccess false. The caretaker role was configured as
`gpt-5.6-terra` / high; independent native-child usage telemetry is not exposed here.

## Verified outcomes

| check | outcome |
|---|---|
| Two recipients remain isolated | PASS — distinct IDs, matching initial/direct markers, separate source findings |
| Task results are durable | PASS — ask exits 0; stream/read-back verification; prompt/output hashes match |
| Stored threads survive separate shim invocations | PASS — resume/read retrieves the same IDs and latest direct turns |
| One caretaker can be re-addressed | PASS within the current root — same native handle returned the follow-up |
| Unknown report does not cause duplicate work | PASS with correction — parent reconciled actual completion before continuing |
| Main-context or total token savings | UNVERIFIED — no complete main/caretaker usage telemetry or controlled comparison |
| Permanent child memory after root/runtime restart | UNVERIFIED |
| First-turn failure/persistence, compaction and collision handling | NOT EXERCISED |

The source task found the GUIDE's preflight/thread-birth distinction consistent with the
implementation. It also preserved the source-inspected first-turn uncertainty: a new ID is
saved only after successful completion/reconciliation. No live transport failure demonstrated
that gap, and no fix was made. There was no justification to invent or apply a guide defect.

## The reporting failure that mattered

The caretaker initially reported peer B lacked a receipt/result/identity after a tool-return
interruption/clarification boundary. On verification, all completion artifacts existed and
matched. Its old RETURN and uncertainty note remain unchanged; the next cycle explicitly
corrects that report from durable evidence. No task was resent to resolve it.

This is a practical requirement for the next caretaker iteration: consult the operation's
durable receipt/state before concluding that an empty tool response means unfinished work.
Use pending-operation identity to distinguish still-running, completed, and genuinely unknown
outcomes. This finding does not justify automatic retries or a new transport framework.

## Timing and target usage

| route | peer | ask seconds | reported input delta | cached-input delta | output delta |
|---|---|---:|---:|---:|---:|
| caretaker initial | A | 30.370 | 44,326 | 20,352 | 904 |
| caretaker initial | B | 62.881 | 159,964 | 118,144 | 1,646 |
| main direct | A | 20.212 | 64,642 | 55,040 | 606 |
| main direct | B | 25.732 | 100,965 | 91,136 | 784 |

Open preflight took 1.766s and 1.262s. Follow-up resume/read took approximately 0.9–1.6s per
operation. A one-minute task-completion guarantee is not supported by the 62.881s observation.

Target totals across the four turns: **369,897 input**, of which **284,672 were reported cached**,
and **3,940 output**. Deltas are computed from each thread's cumulative totals; `last.input`
is context occupancy, not total consumption for the logical task. The small prompts did not
imply small runtime input. No dollar cost or subscription-quota conversion is inferred.

These are target-thread observations only. The root/caretaker's own model use is additional
and unmeasured. Ordering, accumulated history, concurrent versus sequential operation, and a
prompt clarification confound the route comparison. Direct results being faster in this run
does not establish that direct operation is generally faster or cheaper.

## Retained working arrangement

- Caretaker: `/root/experiment_1_caretaker`, reusable while this runtime retains the handle.
- Peer A: `01a1694a-7bdd-7d70-913d-d3dcef66c8ac`.
- Peer B: `01a1694b-0c61-76f0-897c-fc3c66f665c0`.
- Their explicit local vaults remain under `caretaker/tunnel.peer-*.state.json`, gitignored.
- No additional target turn or automatic follow-up is authorized by this result.

## Evidence and next recommendation

`contract.json` pins the source/programme revision. Initial exact prompts and command receipts
are in `caretaker/`; comparison operations and clarified prompts are in `direct/`; filtered
resume/read summaries are in `caretaker/followup/`. `measurements.json` preserves usage and
comparison limits; `verification.json` preserves independent parent protocol checks.
The two numbered bus cycles retain the original stale report and its verified correction.

Keep the existing transport. Before a next trial, improve the caretaker's receipt-first
completion check and deliberately select the target model/effort/read budget. Measure the
whole route before claiming savings. A fault-injection test of first-turn persistence is a
separate possible follow-up. No shared GUIDE/programme promotion follows from this one run.
