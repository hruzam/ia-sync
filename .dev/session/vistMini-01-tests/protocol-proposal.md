# vistMini-01-tests — Cartan's trial proposal

2026-11-12 · author: home:cartan · experimental proposal, no canon promotion.

## Gate proposed to the head

The Cartan–Trajectory cooperation trial has an independently checked report of bidirectional delivery, receipt, duplicate/refusal/recovery behavior and permission boundaries, with explicit limits on applicability to VIST.

This gate is written before opening the requested bed. Trajectory settles its exact wording in RUNBOOK before implementation. These preparation files do not substitute for RUNBOOK or STATUS, and do not declare the gate met.

## Authority and ownership

Majkee explicitly authorized this trial, Bash helpers, peer messages, researcher subagents and reports, named the bed `/home/hruzam/ia-sync/.dev/session/vistMini-01-tests/`, and assigned Trajectory the cSharp posture. He wants to intervene for permissions when needed while we resolve routine coordination together.

Trajectory owns RUNBOOK, STATUS, pulse routing, cycle assignment and integration scheduling; Cartan is the implementation partner and independent witness. Each seat owns its reports and BUS files. Neither edits the other's artifact while verifying it. Both may use bounded researchers, with source checks before integration. Serialize stage/commit/pull/push windows in our shared checkout; explicit filenames alone cannot prevent a shared-index race. No agent-authored canon locks.

Read before authoring:

- `/home/hruzam/reposoma/raw.guides/runbook/GUIDE.md` — one gate, fixed launcher, observations_read, session-owned artifacts.
- `/home/hruzam/reposoma/raw.guides/runbook/res/csharp-head-protocol.md` — head stays and owns navigation; crossed witnesses.
- `/home/hruzam/reposoma/raw.guides/status/GUIDE.md` — sole current state and recovery probe.
- `/home/hruzam/reposoma/raw.guides/bus/GUIDE.md` — POINT/RETURN/VERDICT, six-field RETURN, independent verification.
- `/home/hruzam/ia-sync/HANDSHAKE.md` — delivery versus consumption.
- `/home/hruzam/ia-sync/.dev/_backlog/cross-host-session-bus.md` — candidate wire contract to test, not adopted canon.

The cSharp chapter's historical operator-only transport paragraph conflicts with this trial's live peer messaging. Majkee explicitly authorizes the peer exchange here. Record that scoped exception; do not silently rewrite the guide.

## Common protocol to test

Keep one vendor-neutral envelope and receipt meaning. Runtime adapters may differ. Mail carries a bounded request or points to a session artifact; the short notification carries its location. Scope comes from the request and receiver's standing rules. Codex queue is only an optional adapter experiment, not the governing protocol.

Retain the existing envelope fields. Use UTC timestamps with `Z`, unique `msg`, stable bus `thread`, `re`, unambiguous sender/recipient, and the sender's own `reply-to`. A bus thread is not a runtime thread UUID. Use unicast first; assess recipient-specific deduplication by `(msg, recipient)` without inventing a second task-state registry. Decide multi-recipient archive semantics before testing fan-out.

Distinguish these observations in test evidence:

| Observation | Sufficient evidence | What it cannot establish |
|---|---|---|
| Available | exact file content at recorded commit | recipient read it |
| Notification attempted | endpoint, UTC, adapter result | input submission or consumption |
| Consumed | existing worked reply with `re`, or explicit consumer stamp | work independently correct |
| Verified | checked artifacts and the cycle VERDICT | universal delivery guarantees |

Do not add unread/cursor/stamp files to `_bus/`: its existing POINT/RETURN/VERDICT contract remains intact. A transport stamp is not an extra BUS kind. Archives are local/ignored; archive presence cannot establish cross-host receipt. Prefer a worked reply when owed. An `ack: none` reply ends that obligation. Preserve the draft's hop/open-thread/retry limits; do not silently renew a capped thread to continue the same task. The head schedules a genuinely new bounded cycle when appropriate.

## Smallest helper candidate

After a POINT assigns it, Cartan can own a Bash helper under this bed's `scripts/` and isolated tests under `tests/`. It should validate an already-written request/pointer, offer a read-only check mode, and notify only an explicitly selected endpoint. Keep mail composition and Git commits explicit. No daemon, watcher, generic remote-shell endpoint or global settings change.

For tmux, name the server and pane ID explicitly; preserve literal text and separate Enter. Refuse unknown/busy/dirty-input/dead panes. Checking `pane_current_command` is insufficient to eliminate the race before Enter. A dedicated launch whose agent exit cannot expose a shell is a hypothesis to test, not a guarantee already obtained. Never replace an existing composer draft. Test these cases on an isolated server before touching live peers. A failed/uncertain submission is not automatically retried; receipt and the documented retry budget govern recovery.

Inspect reuse findings in `reports/cartan.preflight.2026-11-12.md`. Do not repurpose ovitmugen: its viewer-only law forbids send-keys/paste-buffer. New helpers remain session-local until evidence supports a separately authorized promotion. Native support that makes a helper redundant should retire the adapter, not the common wire contract.

## Scientific test plan proposed for registration

Hypothesis: the common file/notification/receipt contract supports bounded useful cooperation across the two runtimes without operator relay after initial permissions are set.

Pre-register criteria before helper tests: three ordinary messages each direction; controlled duplicate, expired request, wrong recipient/path, occupied composer, busy target, agent-exit-before-Enter, denied command, and crash-after-notify cases. Use isolated fixtures for disruptive cases. No duplicate work, overwritten draft, shell execution of a pointer or false receipt is acceptable. A detected refusal is a valid result, not a delivery success.

Record runtime/version, host/worktree/commit, endpoint, input case, expected versus observed behavior, UTC times, exit/result, receipt/artifact pointers, operator interventions and remaining uncertainty. Report latency as exploratory observations only. Distinguish byte injection, turn submission, reading and verified work; a successful tool exit proves only its own step. Three repetitions are a smoke trial, not statistical validation or evidence of vendor superiority.

Cartan authors the preflight and implementation report; Trajectory authors or delegates an independent review. Reports live in `reports/`, not only in chat or `_bus`. Their test receipts are cited by RETURNS; VERDICTS check them. Ask the existing Oraculum companion for VIST purpose, expected future collaboration flow and what this trial would need to demonstrate before claiming VIST relevance.

## Permission and third-seat questions

Trajectory: identify the exact denied Bash command, settings/deny/hook source, launch mode, and smallest session-only allowance you need. Supply a redacted diagnostic, never credentials. Do not infer an allowance from majkee's authorization or bypass a deny. Test one allowed and one deliberately unlisted command after the operator applies a necessary change.

Cartan's current sandbox initially denied ia-sync writes and the tmux socket; explicit escalation now succeeds for authorized Git/mail and read-only tmux checks. Operator permission and technical enforcement are separate. No broad permission config has been changed.

The third companion is the existing `GPT-6-Astra high · /home/hruzam/unikuklatrix/nablarva · oraculum|v:codex,cwd:nablarva` session, as supplied by majkee. Its host, live address and VIST task context are unverified. Do not spawn a substitute or claim contact. Resolve its route, obtain the bounded VIST brief, and assign its report scope before including it as a live participant. Nablarva retains its own instruction chain and state ownership.

Cartan can call `researcher` for read-only evidence, `astrobley` for implementation, `verifier` for independent checks, and `challenger` for an adversarial design review. They are bounded children, not extra peers or autonomous transport heads. This preparation used one researcher; no other role was spawned.
