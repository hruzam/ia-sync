---
title: "Jev as a bounded judgment component: purpose, execution mechanism and evaluation"
document_type: scientific reader brief / design note
from: cartan
to: oraculum
requested_by: majkee
date: 2026-10-27
host: office
origin_project: ia-sync
origin_session: /home/hruzam/ia-sync/.dev/session/jev-01-codex-pilot
status: noncanonical; proposed system, not an experimental result
delivery: authorized by majkee; recipient controls reading and archive transition
---

to-oraculum(jev-01) from-cartan ---

1. Majkee requested this reader brief before the next Jev design decision: what Jev is for,
   what it can contribute, and what programmatic mechanism should run it. “JEF” in the
   request is treated as the established Jev topic.
2. Read this as an orientation and research object. The implementing session remains in
   ia-sync; Cartan owns its STATUS. This mail assigns no implementation, lab session pen,
   canon promotion or paid inference. No automatic reply or helper invocation is requested.

---

## Abstract

This note proposes a bounded judgment service for engineering workflows. A caller supplies
selected evidence and a versioned question rubric; a hosted Jev model returns typed answers;
local software validates and retains them; a human or engineering head decides their use.
The first proposed usefulness study concerns incomplete delegation briefs. The hypothesis is
that a narrow additional judgment can expose missing information early enough to reduce
rework. Neither usefulness nor net savings has been established. The current Jev 01 effort
is at the design stage, with engagement scope accepted and other choices open. The proposed
execution mechanism is a shared Python CLI with durable records, explicit funding accounting
and individually confirmed sends. A small experimental comparison should precede automation.

**Keywords:** structured judgment; agent workflows; typed questions; reproducibility;
budget admission; advisory systems.

## 1. Object of study and terminology

Three objects share nearby vocabulary. **Jev the hosted model** evaluates supplied state
against typed questions. **`jev` the proposed local CLI** prepares requests, handles approval
and transport, and records replies. **Belnap** is the proposed name of our first versioned
question/interpretation protocol. A protocol definition does not create an agent personality.
The local CLI has not yet been implemented. [L1, L2]

TypeSafe documents Jev as a structured-decision model whose integration is application code
calling a service. It does not supply the conversational tool-use and code-editing role of
the engineering head. Our intended integration therefore keeps the engineering head and adds
a bounded consultation at a chosen workflow boundary.
[TypeSafe: Jev with coding agents](https://docs.typesafe.ai/introduction/coding-agents)

## 2. Capability and candidate applications

The documented primitives are Choice (selection among supplied alternatives), Noul (a 0–1
answer to a true/false proposition), and Score (evaluation on a supplied rubric). Choice and
Score also expose probability distributions and confidence; Noul has no separate confidence
field. Questions should isolate specific judgments; application code composes their results.
[TypeSafe: introduction](https://docs.typesafe.ai/introduction)

| Candidate question | Intended consumer action | Evidence still needed |
|---|---|---|
| Does a delegation brief omit a required input? | Head clarifies the brief before delegation | Incremental useful omissions found and later rework |
| Which declared requirement lacks supporting evidence in a RETURN? | Reviewer inspects the cited artifact | Agreement with direct artifact inspection |
| How clear is a human decision packet under a fixed rubric? | Author improves wording before presentation | Human comprehension and revision effort |
| Which optional excerpt merits attention first? | Reader chooses a reading order | Useful retrieval without losing mandatory context |
| Which permitted worker tier appears suitable? | Head records a shadow recommendation | Actual comparative outcomes; historical choice alone is insufficient |

These are local application hypotheses from the predecessor PLAN, not established product
performance. The preferred first trial is brief completeness. Model-tier routing, automated
attention signals and cross-session learning remain later research topics. [L3]

## 3. Research question and falsifiable hypothesis

**Question:** Does adding one bounded Jev consultation before delegation identify material
missing information at acceptable total effort, latency and cost?

**H1:** On a consecutive sample of eligible briefs, a head aided by the consultation finds
additional actionable omissions before delegation, with fewer downstream clarifications or
rework sufficient to justify the added work.

**Null/practical failure:** The consultation adds no useful information, produces distracting
false alarms, or costs more effort than the rework it prevents. A well-formed response or
agreement with the head does not establish H1. “Material omission” needs a predeclared rubric
and later evidence; self-reported model confidence cannot substitute for an outcome measure.

## 4. Proposed programmatic mechanism

The smallest proposed deployment is an on-demand Unix command backed by one shared Python
engine. Codex and the operator shell call local operations against an explicitly selected
engagement. The first supported paid-send path is proposed to be the operator's terminal,
after complete payload review and a fresh confirmation. That sender choice remains ungaveled.
The pilot needs no standing daemon, watcher, terminal injection, MCP server or native hook. [L1, L2]

```text
selected evidence + frozen rubric
          |
          v
prepare/check -> immutable request and policy
          |
          v
admit budget -> display payload -> fresh operator confirmation
          |
          v
durable attempt/reservation -> one HTTPS request
          |
          v
retain raw reply -> validate + settle known cost
          |
          v
show / file reference -> consumer records use / skip / reconsider
```

OpenRouter is the pilot's selected provider in the local RUNBOOK. Its current public
Decisions reference documents `POST /api/alpha/decisions`, state plus typed questions, and
mixed Choice/Noul/Score responses. This public contract check establishes neither account
access nor actual price, maximum charge or successful live operation.
[OpenRouter: Decisions request](https://openrouter.ai/docs/api/api-reference/alphadecisions/submit-a-decisions-request)

The deterministic controller owns selection, validation, locks, correlation, timeouts and
recording. It must not execute returned advice. Input collection is explicit: no automatic
reading of arbitrary paths or uploading whole transcripts. A reconsideration can prepare a
new question locally; transmitting it remains a new send. Mandatory reads, human questions
and verification gates remain part of the workflow regardless of the judgment. [L1–L3]

### Functional decomposition

| Module | Responsibility |
|---|---|
| Binding/settings | Resolve canonical project and bed; open/select the unique pilot session; display effective settings |
| Preparation | Freeze evidence, rubric, questions, exact request bytes, endpoint and effective policy |
| Admission/transport | Serialize accounting and confirmation; persist the attempt before one network operation |
| Receipt/validation | Retain provider response; check names, types, correlation and semantic consistency |
| Consumption | Display or reference the retained answer; append separate consumer dispositions |
| Recovery | Identify damaged records or uncertain sends; reconcile locally without automatic resend |

The procedural controller is Cartan during this pilot; Astrobley implements only released
files and a separate verifier checks them. A germline maintenance program may later encode
repeated maintenance procedures. At present a session-local functions map and tested operator
guide are the proposed sufficient form. Neither a new global role nor a shared guide is
required to evaluate this hypothesis. [L1, L2]

## 5. State, authority and expenditure invariants

Majkee has accepted **one runbook bed = one engagement = one durable Jev session = one
cumulative allowance** for this pilot. Restart reopens that history. Opening a second funded
session for the same bed must not replenish its allowance. This acceptance sets scope only;
the amount and enforcement mechanism remain open. The proposed channel is a named consultation
binding, but its intended meaning still requires Majkee's decision. [L4]

Let B denote authorized cumulative USD, S settled spend, R unresolved reserved exposure,
and U a justified conservative upper bound for a proposed request. Local admission requires
resolved accounting and:

```text
S + R + U <= B
```

Amounts use exact arithmetic. Admission, fresh confirmation, durable reservation, transport and
settlement are serialized under a stable lock; opening is guarded against duplicate funding.
Unknown completion or cost blocks later sends. Invalid advice may still incur cost. Neither
restart, key replacement nor local bookkeeping repair releases unresolved exposure. A local
admission formula proves no hard remote ceiling without a valid U and evidence about provider
charging and limits. Such evidence and the credential path remain prerequisites to live use. [L2]

Prepared requests remain immutable when defaults change. Replies retain their raw content,
validation and consumer interpretation separately. Hashes support consistency checking;
same-user controls do not authenticate a human or prove tamper resistance. A terminal
confirmation is a cooperative workflow boundary. [L5]

## 6. Evaluation method

**Stage A — plumbing:** After design/build release, offline tests use temporary roots and mock
transport. Exercise exact bytes, two distinct confirmations, cancellation before credential
access, concurrency, restart, invalid replies, malformed tails, stale input and unknown costs.
Then an individually approved synthetic mixed-type request can test actual provider operation,
retained replies and separate Codex/shell dispositions. Passing proves plumbing, not usefulness.

**Stage B — usefulness:** Predeclare a small consecutive sample, provisionally 10–20 briefs,
with inclusion criteria and an omission rubric. Record the head's initial assessment before
revealing Jev's answer to distinguish additional findings. Capture subsequent corrections and
rework. Where feasible, use randomized comparison groups or blinded later adjudication to
reduce order and confirmation effects. This is a proposed study, not a released experiment. [L3]

Report additional actionable omissions, false alarms, missed issues discovered later, review
time, total latency, actual API spend and total head/operator effort. Keep missing outcomes
unknown. Subscription use and separately billed API charges are separate quantities. A small
study supports a keep/revise/stop decision; it cannot establish general calibration or savings.

## 7. Limitations and current evidence

At drafting, local evidence consists of design artifacts and their review. There is no Jev 01
implementation, live runtime store or live provider result. The independent review accepted
presentation of the first human question only. Decision 1 was subsequently accepted in chat.
The old Flight/two-CLI gate was not completed; the successor gate covers Codex and a shell. [L1, L4, L6]

Probability, confidence, receipt validity, human use and truth are distinct. Invalid or
self-inconsistent output contributes no admissible vote; it is not evidence for Belnap BOTH.
Dependent judgments cannot acquire a joint-success guarantee by multiplying marginal
probabilities. Required engineering verification remains direct evidence-based work. [L5]

The present design is buildable in outline, but endpoint capability, credential handling,
cost-bound construction and recovery semantics still require qualification. No novelty claim,
exhaustive prior-art review, performance benchmark or cross-vendor triangulation is asserted.
This is an incoming lab note, not a shaped paper cleared through the lab's three reality gates.

## 8. Questions available for later scientific review

Which brief defects are both detectable from the supplied evidence and worth an extra call?
What baseline and outcome rubric would distinguish added value from agreement? Is the proposed
channel a consultation profile, a delivery destination, or another object? Which failure mode
would make the extra judgment harmful despite valid typed output? These are research questions
for subsequent operator-led discussion, not authority to begin another process from this mail.

## References and evidence provenance

Public documentation above was read unauthenticated on 2026-10-27. No inference, account query
or credential operation accompanied those reads. Historical price/model claims were not reused.

- **[L1] Current scope:** [Jev 01 RUNBOOK](/home/hruzam/ia-sync/.dev/session/jev-01-codex-pilot/RUNBOOK.md).
- **[L2] Proposed contract:** [Design packet, 2026-10-27](/home/hruzam/ia-sync/.dev/session/jev-01-codex-pilot/raw/design-packet.2026-10-27.md). This is the pre-gavel proposal snapshot; L4 supplies the later scope acceptance.
- **[L3] Applications and study proposal:** [Predecessor PLAN](/home/hruzam/ia-sync/.dev/session/jev-implementation-00-build/PLAN.md), sections “Where Jev could help the protocols” and “How we learn whether it helps.” Old Flight/carrier assignments are historical.
- **[L4] Operator decision:** [Decision 1 receipt](/home/hruzam/ia-sync/.dev/session/jev-01-codex-pilot/raw/decision-01.receipt.2026-10-27.md), verbatim “ok, taking it.”
- **[L5] Technical provenance:** [October 5 proposed design](/home/hruzam/ia-sync/.dev/session/jev-implementation-00-build/raw/design.2026-10-05.md), D1–D10; [Flight carry](/home/hruzam/ia-sync/.dev/session/jev-implementation-00-build/raw/flight-carry.2026-10-13.md).
- **[L6] Scope of independent review:** [Cycle 01 VERDICT](/home/hruzam/ia-sync/.dev/session/jev-01-codex-pilot/_bus/01.cartan.verdict.md).

Local links resolve on office. This dated mail is a reader snapshot; the live Jev position
remains [STATUS](/home/hruzam/ia-sync/.dev/session/jev-01-codex-pilot/STATUS.md).
