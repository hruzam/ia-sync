# Caretaker's tunnel establishment and maintenance loops

Read once with the program; on warm calls read only named changes or missing context.
This file belongs to IT support. Main delegates by role/question and consumes capsules.
Existing command law is `/home/hruzam/reposoma/raw.guides/tunnel/GUIDE.md`; existing source is
`/home/hruzam/ia-sync/zsh/ai/tunnel-codex.{zsh,py}`. Do not patch that transport in this gate.

## Inputs, outputs and fixed profile

Bed: `/home/hruzam/ia-sync/.dev/session/germline-09-source-reader`.
Inputs: head POINT; raw/control/RELEASE.json; raw/hold-line/{controller.md,task.json,sources.json};
selected function; raw/briefs/caretaker.md; the named round packet and source bindings.
Use native `implementer` capability, not a new global agent. Respect normal tool escalation
for the same authorized CLI operation; an approval rejection is a hold, never a bypass.

Own all artifacts under `raw/caretaker/`: adapter, fake checks, `operations/`, `results/`,
`packets/`, `capsules/`, `metrics/`, selected recovery evidence and the two ignored vaults:

- `tunnel.researcher.state.json`
- `tunnel.auditor.state.json`

The head owns RELEASE, STATUS, POINT and VERDICT. Targets write no files. Never persist auth,
full environment, raw thread/tool histories, rollouts or native state databases. Persist exact
task prompts, final task replies, selected protocol fields, command/output hashes and timings.

Pin `TUNNEL_CODEX_BIN=/home/hruzam/.local/bin/codex`, record version, set
`TUNNEL_CODEX_USAGE=full`. Both targets request `gpt-6.1-sol`, `effort=high`, read-only. A
zero-turn model/list check must confirm the account offers that model/effort; save only that
filtered capability. Unsupported profile stops, with no substitute or speculative ask.

## 1 — Offline preparation loop (C1 before any target turn)

1. Check an actual operator grant is recorded and matches the fixed scope/budget. Check source
   pins and canonical source/deployed preamble equality. Missing release permits offline
   validation only, never an enabled table.
2. Adapt G08's receipt-first pattern into `raw/caretaker/run_operations.py` (or an equivalently
   small trial-local driver). The old runner is a historical reference with hardcoded G08
   paths: DO NOT execute it or reuse old operation records/vaults.
3. Before any effect, exclusively create the operation record with argv, prompt/hash, role,
   cycle, expected identity, runner PID/start identity and time. Atomically finish with exit,
   output hashes, selected state and elapsed time. Every existing operation key refuses replay.
   Inspect valid completion, living pending, failed/unknown distinctly; a tool exit is not proof.
4. Local fake checks must show: ignored caller return recoverable from receipt; live pending;
   dead pending unknown; corrupt/malformed receipt/output unknown; duplicate refusal without
   a second invocation; total ask-attempt cap; original role-ID binding; cold/no-preamble and
   warm/pinned-preamble rules. Verify through pure helpers/fakes, no live fault injection.
5. Freeze the adapter hash, local-check evidence, and compiled R1/A1 prompt hashes in a C1
   execution plan under raw/caretaker. Proceed only after these local checks pass. Parent need
   not rebuild the adapter; cite its source/checks and report any defect as a precise hold.

## 2 — Establishment loop, separately for each role

1. Reconcile existing role records first. If a known vault/operation exists, inspect its content
   and use recovery below; never replace it to get a new ID. No `--last`, no bind to another
   trial, no two vaults addressing the same thread.
2. For a truly new role, invoke the unchanged shim once with literal argv equivalent to:

```text
/home/hruzam/ia-sync/zsh/ai/tunnel-codex.zsh open --state <exact declared role vault>
  --enable --sandbox read-only --cwd /home/hruzam/ia-sync/.dev/session/germline-09-source-reader
  --preamble none --model gpt-6.1-sol --override effort=high
```

   Build argv in Python (no shell interpolation of messages). This open is zero-model-turn
   preflight. Verify its receipt, enabled state, threadId/lastTurnId null, intended model,
   read-only sandbox and high override before the first ask.
3. A preflight has at most TWO attempts per role. A second attempt needs a proved zero-turn
   open-only failure before any ask, a known non-auth local cause fixed within owned scope,
   and a new operation key. Preserve the first failure. Existing successful/pending/unknown
   state is reconciled, not reopened. If those conditions are not proved, return HOLD.
   No automatic login, dependency installation, global source edit or third preflight attempt.
4. Ask R1/A1 exactly once with its compiled substantive cold packet. Creation, orientation
   and actual task are one target turn. Do not prepend “already oriented” before this occurs.
   A preflight success is not semantic readiness. Count the ask attempt BEFORE invocation;
   uncertain or failed submission remains consumed for this grant.
5. Inspect durable completion regardless of tool stdout. Verify marker `G09.R1` or `G09.A1`,
   expected role, source scope, stored thread/turn IDs and ask/read-back agreement. Record its
   bootstrap acknowledgement (role/scope and consumed source pointers); do not call a stamp
   proof of understanding. Require distinct researcher/auditor IDs.
6. Arm that EXISTING vault with the canonical deployed preamble using this zero-target-turn update:

```text
/home/hruzam/ia-sync/zsh/ai/tunnel-codex.zsh open --state <same exact role vault>
  --preamble /home/hruzam/.germline/tunnel/tunnel.preamble.md
```

   Verify unchanged ID and exact state preamble path/hash. Compare both authored
   `/home/hruzam/ia-sync/germline/tunnel/tunnel.preamble.md` and live file against sources.json.
   The older `/home/hruzam/reposoma/.germline/tunnel/tunnel.preamble.md` is not substituted.
   This policy update is distinct from an enable preflight and has its own operation key.
   Existing-vault `open` also resumes the born thread and stamps runtime (shim lines 735–752);
   it is not solely a filesystem update. It still starts no model turn.
7. Invoke zero-target-turn `resume`, then filtered `read` on the explicit vault. Record actual
   model/high/readOnly/networkAccess false, same thread ID and completed first turn. A birth-time
   runtime stamp predates the turn override; post-turn server observation is required. On mismatch
   hold without another model turn. Keep the table available through ordinary yields.

## 3 — Warm consultation loop (C2, optional C3)

1. Consume the new POINT and named deltas. Reuse retained controller/functions/GUIDE. Check
   current pins and remaining attempt budget mechanically; do not reread all orientation.
2. Compile R2/A2/A3 from the corresponding fixed packet plus explicit manifest-derived source
   files, current contract/decision and evidence pointers. Materialize all binding markers;
   freeze the exact compiled prompt/hash before dispatch. No wildcard “read anything helpful”.
3. Require the correct role ID and armed, matching preamble. Invoke ask once. `_apply_preamble`
   will read/prepend the small policy; repeated read-order discovery remains prohibited on
   warm calls unless explicitly named or required by higher-priority instructions.
4. Inspect receipt; if successful, read-back the named turn and retain selected fields only.
   Verify cycle/recipient marker, unchanged role identity, actual completed status and exact
   final answer text. An independently audited semantic failure is separate from transport success.
5. Preserve findings, dissent, unknowns and source pointers in the capsule. Do not smooth a
   REVISE into PASS. If 300 words cannot preserve a consequential fact, declare an overrun or
   request a focused follow-up rather than suppressing the fact.
6. Persist metrics and return through the assigned native RETURN/capsule. Never dispatch R3,
   A4 or a sixth attempt from a recommendation, tool error or inferred need.

## 4 — Waiting and uncertain completion loop

After an exec returns a running cell/session handle, poll THAT owned handle, normally at
10–30s intervals and never a single blocking wait over 60s. A still-running operation is not
a failed task. The driver records PID/start identity; inspect only those known process fields,
not broad process arguments/environment. Publish a compact progress/hold if required, not logs.

The shim has its existing timeout; record the observed value/version and do not promise a
one-minute completion or silently change the transport. On timeout/empty tool output:

- **Validated receipt/output:** reconcile stored identity/result; no resend.
- **Pending, same runner alive:** continue bounded polling of that owned operation.
- **Dead/unverifiable runner, nonzero exit, damaged evidence or absent identity:** unknown/failed;
  preserve evidence and stop new target dispatch. A null first-turn vault cannot prove absence
  of server-side work because the shim saves a new ID only after turn/reconciliation.
- **Known thread ID:** permitted zero-turn read/resume may narrow the uncertainty. Preserve
  latest turn/status/text hash and compare to the attempted cycle. Never infer safe replay.

At C1/C2 interruption, reconstruct from durable operations before interpreting the native
child's last prose. No task retry, fresh replacement thread, tmux kill, writer-lock deletion,
remote archival or destructive cleanup is permitted to manufacture a green result.

## 5 — Memory/context recovery loop

For a target or native caretaker that reports lost orientation/compaction, old load receipts
show past consumption only. Protocol read/resume first; they spend no target turn. Recover
STATUS and only the named minimum program/function/task deltas. Do not reload full GUIDE,
all roles, all canon or git state automatically. If a model recovery question is necessary,
it needs its own explicit remaining grant; there is no unbudgeted liveness call.

A lost native child can be replaced from the existing role plus pinned program, but record
that intervention and reconcile existing vaults before any target ask. Native replacement
does not establish permanent memory or remote absence. Missing authority/source remains HOLD.

## 6 — Receipt, cost and end-of-run checks

Operation keys distinguish zero-turn opens/preamble updates/resume/read from asks; use stable
cycle keys such as `R1.ask`, `A1.ask`, `R2.ask`, `A2.ask`, `A3.ask`. Persist the attempt marker
before invoking. The adapter must enforce fixed allowlisted cycles/role binding and max five.

Usage tails are per-thread cumulative totals. Initial turn delta equals its total; later
deltas subtract that SAME thread's prior measured total. Cached input is a subset. Reset,
missing or inconsistent counters remain unverified; do not manufacture deltas or native-main
usage. Record context occupancy separately from total input across internal model calls.

Before final acceptance reconcile both explicit IDs, expected latest cycle and idle/completed
status with zero-turn operations. Leave no running process hidden behind file presence. On
ordinary yield retain vaults; on explicit gate closure/relinquishment follow the existing local
close contract and preserve IDs/results. No remote deletion, lock tampering or daemon is added.
