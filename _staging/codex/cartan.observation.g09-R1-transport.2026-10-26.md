# G09 R1 — verified transport diagnosis and recovery recommendation

to-cartan(germline-09) from-cartan(germline-03) · 2026-10-26 · office

Scope: inspect the failed R1, propose correction and recover identity without another model
turn. No G09 STATUS, vault, receipt, adapter, source pin or canonical transport was edited.
All new diagnostic artifacts are under `g09-R1-diagnostic.2026-10-26/` beside this report.

## Verified result

**The missing identity was recovered through filtered protocol reads. R1 was accepted and
performed work, then was stored as interrupted. It has no completed final answer.**

| field | observed |
|---|---|
| Thread ID | `01a176f7-532b-7722-9324-0ecb92694073` |
| Turn ID | `01a176f7-53a6-7b83-b203-b86b08ec15ac` |
| User-message SHA256 | `3abfe0add260404ba9daae8e3204edd61975951bb06288a3eaad7f128f442d4d` — exact frozen R1 prompt match |
| Stored turn status | `interrupted` |
| Query-time thread status | `notLoaded` |
| Stored activity | 12 commandExecution, 4 webSearch, 3 agentMessage/commentary, 5 reasoning items |
| Final answer | None; the marker-bearing message is commentary, not completion |
| Created / updated | 1792997282 / 1792997402 — same seconds as the recorded attempt start/end |
| New model turns used by diagnosis | Zero |

One `thread/list` query matched exact G09 cwd, searchTerm `G09.R1`, a page limit of 10 and all
documented source kinds. `useStateDbOnly:true` avoided the default rollout scan/metadata-repair
path. The single candidate also matched the attempt's narrow creation window. `thread/read`
then verified the exact user text and interrupted turn. No thread/start, turn/start, resume,
resend, archive or delete was invoked. No direct history/rollout/auth file was read.

The supported filtered list and non-resuming read operations are documented in
[Codex App Server](https://learn.chatgpt.com/docs/app-server). Installed CLI 0.164.0's generated
schema confirmed those parameters before the probe. Selected evidence, not the full history,
is in `identity-recovery.json`; the probe is `recover_identity.py`.

## Why 120.811 seconds and 4.124 seconds agree

The wrapper's default `TUNNEL_CODEX_TIMEOUT` is 120 seconds. Each response wait and the
turn-completion wait creates a phase deadline, then calls the receive queue with **remaining**
time. The timeout string prints that final queue-wait argument, not elapsed command time.

For a 120-second phase, `120 - 4.124068260192871 = 115.87593173980713` seconds had already
elapsed when the final receive wait began. The receipt's total is 120.81116795539856 seconds.
The remaining 0.811 seconds cannot be allocated among startup, other phases and cleanup from
the retained evidence. The inherited timeout environment was not recorded, so the default is
source fact and the 120-second incident interpretation is supported by timing, not an env dump.

The exact failing wait is not recoverable from stderr: `turn/start` acknowledgement,
`turn/completed`, or reconciliation response use the same receive helper. Original protocol
phase/ACK timing was not retained. Source: `tunnel-codex.py:354`, `:394`, `:476`, `:485`, `:948`.

The stored work proves this was not a preflight-only rejection. The shim reached its deadline
without a validated final response and its cleanup terminated the owned app-server. The
interrupted stored turn and matching update time are consistent with that cleanup. There is
no captured evidence of a provider outage or a four-second whole-operation failure. A productive,
multi-step research task reaching a fixed deadline is the supported explanation; exact wire
phase and backend latency allocation remain unproved.

## How the identity disappeared

The override log is reached only after initialize and thread/start return a nonempty ID.
`_birth_or_resume` stores that ID in memory (`tunnel-codex.py:857`), but `cmd_ask` saves the vault
only after drive_turn and reconciliation (`:951–952`). A ProtocolError skips that save, while
finally closes the app-server and releases the shim lock. Thus the preflight vault remains
null even though a durable task exists. This previously source-inspected gap is now exercised.

`probe_timeout_and_checkpoint.py` ran the real Session/cmd_ask/cmd_send logic with a fake clock,
queue and transport. For all three failure phases, the original code reproduced the exact
4.124068260192871-second diagnostic at fake elapsed 120.0, retaining the ID in memory and
performing no vault save. Cleanup still ran. No app-server or model was used by those probes.

## Empty native output and the false-dead observation

The adapter blocks in subprocess.run with captured pipes and prints only when that call
finishes. The shim also waits for completion/read-back before printing a result. Empty output
while the native exec yields a running session is therefore expected; use that returned
session/cell handle and inspect the durable operation rather than treating the yield as exit.

Actual artifact times support an in-flight observation: the pending capsule was written
78.313s after start; RETURN was written at 119.383s; the failed receipt finalized at 120.812s.
These timestamps do not preserve the original native tool-session response or checker context.

The PID failure mode was reproduced directly with a harmless buffered 20-second process:

| observation | runner PID namespace | checker PID namespace | result |
|---|---:|---:|---|
| Escalated runner | 4026531836 | — | PID 1394569 alive/pending |
| Default sandbox checker | 4026531836 | 4026533211 | Runner PID absent |
| Escalated checker | 4026531836 | 4026531836 | Same PID and start identity match |
| Poll original native session | — | — | Completed normally, exit 0 |

The initial exec returned empty output plus a valid session ID. This proves that a cross-
namespace `/proc/<pid>` check can falsely look dead while the managed operation lives. It is
a strong explanation for R1's early dead/unverifiable claim, but the original checker's
namespace was not recorded, so that historical attribution remains inference.

Correction: record the runner's PID namespace along with PID/start, persist the native tool
session/cell handle at the caller boundary, and poll that handle. Namespace mismatch or
inaccessible process metadata means **unverified visibility**, not a proved dead runner.
Receipt completion takes precedence over old prose. Evidence: `session-visibility.json`.

## Proposed corrections — not applied

1. **Preserve thread identity before driving the first turn.** The small candidate patch
   `identity-checkpoint.candidate.patch` adds an atomic vault checkpoint after birth/resume
   in send/ask. It does not update lastTurnId or claim completion. Twelve offline cases
   (two verbs × three failure phases × original/candidate) confirm the candidate retains
   the known ID, leaves lastTurnId null and still runs cleanup. It cannot recover an ID
   whose thread/start response never reached the client, or guarantee server durability.
2. **Use an explicit substantive-work deadline and truthful diagnostics.** The 120-second
   default was inadequate for this run. For an authorized continuation, an explicit larger
   phase budget (for example 600s via the existing TUNNEL_CODEX_TIMEOUT) is a proposal, not a
   performance guarantee. That knob applies per phase, not as a whole-ask ceiling. Record
   phase, elapsed/configured budget, last-event time and known IDs, and prefer monotonic clocks.
   Keep native polling short; do not silently turn a longer model task into a blocking main wait.
3. **Repair the adapter's recovery guards before dispatch.** `probe_adapter_guards.py` confirms:
   - check_state rejects the structured readOnly sandbox value produced after thread birth;
   - read/resume require lastTurnId/completed-first-turn even though identity-only read is
     exactly the needed recovery path;
   - run/ask reaches a stub dispatch without rechecking current pins/release; those checks
     currently occur during compilation only. Recheck release, pins, exact frozen prompt and
     unresolved holds immediately before dispatch. Make A3 conditionality explicit there.
   Normalize sandbox intent versus effective runtime, and separate recovery-read validation
   from normal completed-bootstrap dispatch. Never invent a successful lastTurnId to pass a guard.
4. **Test the real integration guards.** The 11 recorded helper checks do not cover those
   dispatch/recovery paths; some check static tuple length or raw exclusive-file behavior.
   Add tests that exercise actual start/run boundaries, halted/revoked dispatch, frozen hash
   mismatch, identity-only read and structured sandbox state. Tag nonzero transport exits as
   command-failed with remote outcome unknown until reconciled, not remote rejection.

The candidate patch is limited to identity preservation; it does not purport to implement
all four corrections. Apply any canonical transport change only in a separately authorized
fix scope with journal/deploy discipline and updated pins. The original source remains intact.

## Explicit recovery recommendation

**Keep G09 stopped, but refine the hold from unknown acceptance to known interrupted R1.**
The recovered identity needs no repeat of the original request. G09's head can verify these
selected artifacts and update its own STATUS; this diagnostic seat does not take its pen.

Next, approve the narrow transport/adapter repair and offline verification. Preserve the
original vault and receipt as evidence. Before any identity adoption, snapshot them and make
the chosen binding change explicit; no fake completed turn or silent overwrite.

If Majkee then releases further work, prefer a **new, explicitly counted continuation on this
exact recovered thread**, asking only for the missing substantive result from its existing
research. The interrupted first attempt stays consumed and zero original completions remain.
The continuation is a new model turn, not read/resume and not an automatic retry. Recovery
orientation/preamble handling must be explicitly granted; the ordinary completed-bootstrap
rule cannot simply be claimed satisfied. If the added cycle/budget changes G09's fixed contract,
open a numbered recovery sibling rather than rewriting its RUNBOOK. A fresh replacement
thread is an operator-chosen alternative, not required for identity recovery.

Until that ruling: no resend, A1, preamble arming, D1/CONTRACT, product implementation, local
close, thread deletion or transport deployment. PRODUCT remains UNVERIFIED and DELEGATION
INDETERMINATE. Target usage is unmeasured; a failed local receipt did not mean no model work.

## Independent check and preserved evidence

`/root/g09_package_review` returned PASS after reading the helpers/artifacts, source, patch and
recomputed hashes, without launching runtime or rerunning probes. It confirmed the prompt/ID
binding, original receipt/vault/source preservation, namespace limitation and guard findings.
Its essential conditions are preserved in `diagnosis-review.md`.

Diagnostic files: `identity-recovery.json`, `session-visibility.json`,
`offline-checkpoint-probes.json`, `adapter-guard-probes.json`, candidate patch and their helpers.
There is no global primitive, daemon, model replay, auth change, deployment, commit or push.
