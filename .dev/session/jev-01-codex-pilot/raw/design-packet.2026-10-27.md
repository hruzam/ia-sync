---
title: Jev 01 engagement, channel and USD decision packet
author: cartan
date: 2026-10-27
status: proposal; no human answers or construction release
---

to-majkee(jev-01) from-cartan ---

1. This packet proposes a small settings boundary for the Codex/shell pilot. It preserves
   the predecessor's evidence without treating its unanswered choices as accepted.
2. Decide one item at a time. The first editable question is
   `decision-01.engagement.md` beside this file. Later choices below are an inventory,
   not a request to answer them together. Your October 12 sheet remains untouched.

---

## Proposed ownership and identities

| Term | Proposed pilot meaning | Consequence |
|---|---|---|
| Project | Canonical project root, recorded in full alongside its hash | Equal directory names cannot select each other's records. |
| Engagement | One explicitly selected runbook bed within that project | Owns the cumulative USD allowance and channel binding. |
| Jev session | The one durable pilot ledger attached to that engagement | Restart reopens it; a second funded session for the same bed refuses. |
| Channel | A named consultation profile: purpose, protocol/rubric version and provider/model policy | Selected explicitly; it is not a terminal, consumer identity, transport or new wallet. |
| Consumer | Codex or the operator shell | Both can read the same retained reply; their dispositions remain distinct. |

These meanings are proposals, especially **channel**. If you mean a delivery destination
or terminal by channel, the contract needs revising before construction. The pilot proposes
one channel per engagement, not a general multiplexing or configuration service.
No implicit current session, inherited ambient target or automatic bed attachment.
An unbound session is unfunded. Changing bed, channel binding or protocol requires an explicit
new binding design; it does not silently create another budget. In this pilot such rebinds refuse.

## Settings that can change, records that cannot

Proposed local operations are inspect/default-edit/open-bound-session, not a new daemon.
Defaults may be edited for future session openings. `settings show` exposes project, bed,
session, channel, protocol/rubric, model policy, token/time/question bounds, authorized total,
known spend, outstanding reservations, unknown liabilities and available allowance or unknown.
It labels the local admission limit separately from any verified provider backstop.

The opening event freezes the binding and policy. Each preparation freezes complete request
bytes, source-buffer hash, endpoint/method/non-auth headers, model allow-list, validator and
protocol versions, effective limits, channel and funding identity. A changed default cannot
rewrite it. A changed/missing buffer is visible freshness information, never replacement input.
No silent allowance refill, rolling reset, top-up, key rotation or grant replacement.
For this pilot, existing-session settings edits refuse; changing future defaults remains useful
without inventing live policy migration. Any future grant mutation needs a separately approved
design and durable reconciliation, not merely a config edit.

## USD admission proposal

The amount is **UNSET**. No $0.05 default is accepted by this packet. Unset or invalid caps
refuse paid sends. Use exact decimal USD arithmetic with conservative rounding, never floats.
Offline fixtures can use explicit synthetic amounts, labelled as test data, after build release.

For a candidate request, let B be its engagement's authorized cumulative allowance, S its
settled spend, R outstanding reserved upper bounds, and U the candidate's conservative cost
upper bound. Admission requires all quantities to be known and `S + R + U <= B`.
Reject negative/nonfinite values and any unknown or unreconciled cost/liability. The source,
unit, rounding and validity of U must be reviewable and frozen with the preparation. An estimate
without a defensible upper-bound method cannot support a claim of a strict USD cap.

Serialize admission through one stable engagement lock. Because pilot engagement and session
are one-to-one, this is also the full-send/session writer lock. Session creation must check the
same engagement identity under lock so two concurrent opens cannot mint two allowances.
The durable attempt records its reservation before any network operation; keep the lock from
state validation through confirmation, durable attempt, one send and result settlement.
No transport occurs before the attempt and reservation are fsynced.

Cancellation or wrong confirmation touches neither credentials nor transport and creates no
attempt liability. A persisted attempt whose remote outcome is uncertain retains its reservation
and halts subsequent sends. Reconciliation of local records alone cannot free possible charges.
A receipt with trustworthy settled cost replaces that attempt's reservation with actual spend,
even if its judgment is invalid. Missing/untrusted cost halts. An overrun is recorded as an
overrun and halts; it is never clamped to the cap. Restart reconstructs all liabilities before
admission. A retry is a new occurrence with fresh approval and possible additional cost.

This is a local admission policy, not proof of a hard remote ceiling. Live use additionally
requires current primary provider evidence, actual credential capability, a selected backstop,
and an explicit assessment of out-of-band usage, delayed billing, expiry/revocation and unknown
outcomes. No account, key or limit was inspected or changed to prepare this packet.

## Inherited contract and Flight corrections

The October 5 design remains proposed technical input. These are the proposed dispositions
for Jev 01, not amendments to Flight's files or a substitute Flight VERDICT.

| Source | Disposition in this proposal |
|---|---|
| D1: send boundary | Operator terminal sends after complete frozen-scope review and fresh hash-prefix confirmation. Known agent-tool and noninteractive contexts refuse before credentials. Same-user checks are cooperative; do not claim agents can never spend. Codex and shell remain local consumers. |
| D2–D3: wallet and funding | Offline first is recommended; wallet sequencing, amount and live credential/backstop remain explicit choices. Engagement/one-session ownership above elaborates the proposed bed funding scope. |
| D4: recovery and bytes | Preserve canonical request/approval bytes, no hidden retries/redirects/fallback, complete-send lock and request-driven validation. Proposed forensic malformed-tail recovery retains the bad bytes and is explicitly not strict JSONL; complete event without LF is distinct. Independent technical acceptance is still owed before coding. |
| D5: evidence vocabulary | Carry `actor.source: record` and receipt-scoped `data.certainty` with confirmed/observed/correlated/inferred/unknown. Receipt certainty never certifies advice. No Nablarva delivery or acceptance is claimed. |
| D6: names | Recommend jev runtime and belnap versioned protocol, with no personality. Invalid or self-inconsistent output gives no admissible vote, not BOTH. |
| D7: storage | Recommend private host-local project-scoped event ledger and separate editable buffer/stable lock. Full identity and immutable opening govern selection. Runtime is not portable source. |
| D8: promotion | Pilot code stays in this bed; later `zsh/jev/` placement needs separate authorization and fresh shell activation proof. No deployment here. |
| D9: lifecycle | Preserve independent occurrence IDs, content hashes and retry/reconsider/parent lineage. Extend the attempt/result data to carry budget reservation/settlement; no wallet mutation commands implicitly follow. Exact event schema needs technical review before construction. |
| D10: live workload | Recommend one synthetic brief with Choice + Noul + Score as minimum plumbing proof. Five briefs/15 questions remain an optional candidate, not a mandate. Actual workload is a later human choice and every send requires fresh confirmation. |

Dependent cascade success cannot be obtained by multiplying marginal probabilities without
independence. Historical model choices are not cheapest-model ground truth. GPG unlock,
request approval and spend limits are separate boundaries. Two consumers do not prove shell
activation. The prior tunnel seats-table mismatch stays historical: this RUNBOOK gives Cartan
the sole STATUS pen and uses no Claude carrier. Flight's wallet witness was a proposal;
the new independent Codex verifier does not claim to complete Flight's old gate.

## Program, controller, functions map and guide

Propose a session-local functional map first. Cartan controls this pilot, Astrobley owns released
implementation, a separate verifier checks it, and majkee supplies design gavels and send approval.
The CLI's deterministic controller dispatches operations; it neither decides scope nor executes
advice. This distinction avoids turning a software dispatcher into a second session head.

| Function boundary | Input/output and invariant |
|---|---|
| Resolve/open | Explicit project/bed/channel → one durable session; prevent duplicate funding. |
| Settings | Defaults for future openings; inspect frozen effective settings without mutation. |
| Prepare/check | Frozen typed questions and policy → canonical bytes and validation report. |
| Admit/confirm/send | Frozen occurrence + current liabilities + fresh human approval → one durable attempt and one transport call. |
| Receive/settle | Raw receipt → validation plus cost evidence; invalid advice still may cost money. |
| Show/ref/dispose | Retained reply → display/path and distinct append-only use/skip/reconsider. No command execution. |
| Reconcile | Damaged tail or unknown attempt → explicit local recovery; no automatic resend or charge erasure. |

A germline maintenance program is a candidate after the workflow is stable and earns reuse;
it is not required to prove this CLI. No new global agent, hook, skill or program is proposed
for installation now. A short session-local operator guide and live PAD can accompany the
accepted build; a shared canonical guide is a later separately authorized promotion.
Current germline program practice must ground any later placement, controller and function-file
proposal. The code's later proposed `zsh/jev/` home and a procedural program are different objects.
The inspected G07 specimen (`../germline-07-make-program/raw/experiment_1/program/CONTROLLER.md`
and `fn/audit-tunnel-opening.md` below that program) is an uncanonical bounded procedure
consumed by an existing child. Its qualified STATUS supports using a small functions map,
not claiming general promotion. Oraculum's actual returned summary and parent disposition
are retained in `oraculum-consult.2026-10-27.md`.

## Human decisions and release edges

Only decision 1 is presented now: engagement scope and its relationship to funding. Then clarify
the proposed channel meaning. The remaining queue preserves all eight unanswered old items:
send workflow; wallet order; actual USD amount; bed funding scope (now decision 1); names;
storage; later source placement; live workload revised to Codex/shell consumers.

Before construction: resolve engagement/channel semantics, inherited choices, USD amount and
enforcement policy as required by current STATUS; complete exact technical schema/recovery
review and obtain an independent Codex design review plus explicit bounded construction release.
An offline-first choice alone does not bypass those holds. Before live use: current provider
contract/pricing/bound evidence, approved credential/backstop handling, exact payload and fresh
per-send confirmation. Design acceptance never authorizes credential access or sending.
Oraculum noted that STATUS's amount/enforcement-before-construction hold is stricter than
RUNBOOK's live-use minimum and recommended allowing synthetic offline amounts sooner.
This packet retains the stricter hold; relaxing it requires an explicit majkee disposition.

## Bounded native assignments

- Oraculum `/root/jev_design_consult`: read-only analysis of the identities, costs and
  program/functions/guide disposition. Parent captures its actual reply with provenance.
- Independent verifier: inspect this packet, editable decision 1 and cited sources; assess
  readiness to present one decision, not build acceptance. Own only the assigned RETURN.
- Astrobley, after release only: own this bed's `impl/`, `tests/` and a named RETURN;
  implement the accepted contract with temporary roots and offline transport/credential spies.
  Not spawned now. Never overwrite another owner's implementation.
- Later fresh build verifier: read actual implementation and evidence, run proportionate checks,
  never fix the body it verifies. Houston consult remains optional, not invoked.

Handles are actual process references only while the native tool reports them available.
Cold recovery checks the matching task and its returned evidence before reusing a handle;
if absent, rebrief explicitly. STATUS alone states what to do next.

## Sources

- This bed: `RUNBOOK.md`, `raw/READ-FIRST.2026-10-26.md` and `raw/resume-before.2026-10-27.json`.
- Predecessor `../jev-implementation-00-build/`: `PLAN.md`,
  `raw/design.2026-10-05.md` D1–D10, `_bus/01.cartan.return.md`,
  `raw/flight-carry.2026-10-13.md`, `raw/majkee-gavels.2026-10-12.md`,
  `raw/HANDOFF.cartan.codex-only.2026-10-26.md`.
- Provider statements in predecessor sources are dated evidence, not a current capability claim.
