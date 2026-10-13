---
title: Jev implementation plan — pilot first, protocol trials afterward
date: 2026-10-12
author: cartan
status: proposed work sequence; cycle 01 and operator choices remain open
authority: RUNBOOK.md fixes the pilot gate; STATUS.md owns the current next action
---

# JEV implementation plan

Build a small consultation CLI, prove its records and human send path, then measure whether
its advice helps a real protocol. My preferred first useful application is **brief clarity
before delegation**. It has a direct consequence—improve the brief or ask a missing question—
and its feedback is easier to inspect than a claim about the cheapest adequate model.

Keep the proposed five-brief, mixed-type batch for the first transport proof. Model-tier
advice can be recorded there without controlling routing. The later usefulness trial should
concentrate on one question family; expanding the number of protocols before measuring one
would make failures harder to understand.

This plan does not record a gavel or authorize implementation. The eight answers in
[majkee's decision sheet](raw/majkee-gavels.2026-10-12.md) are blank, and Flight's cycle-01
VERDICT is absent at authoring. The detailed proposed contract is
[design.2026-10-05.md](raw/design.2026-10-05.md); the older design remains provenance.
The fixed [RUNBOOK](RUNBOOK.md) gate is unchanged. Later phases below need their own scope
and acceptance; they do not enlarge this bed's gate.

## What we are building

```text
consumer drafts state + typed questions
  → freeze and check request locally
  → majkee reviews and confirms this send in a terminal
  → one provider request → retained reply + validation
  → consumer shows the block or its file reference
  → use / skip / reconsider, with interpretation labelled separately
```

The engine is shared Python, callable from zsh or bash. Jev is the runtime; belnap names a
versioned protocol, not a native Claude/Codex agent. The runtime ledger stays host-local:

```text
~/.jev/projects/<readable-project>-<root-hash>/
  <UTC-time>-<session-id>.jsonl    opening, request, receipt and disposition events
  <session-id>.buffer.md          editable input
  <session-id>.lock               stable writer-lock target
```

Project/bed/bus attachment is explicit and frozen in `session_opened`. The bus receives a
reviewed extract when useful to shared work; it does not become a second memory store.
The extract carries actual evidence and correlation, not just a host-local pathname.
Code stays in this bed's future `impl/` during the pilot. Later portable placement is
`ia-sync/zsh/jev/`; nothing deploys into `~/.jev/`.

## Phases and evidence

| Phase | Work and owner | Evidence required to advance |
|---|---|---|
| **P0 — finish the contract** | Cartan reconciles D1–D10; Flight verifies; majkee resolves the eight choices. | Flight's verified cycle-01 disposition, explicit operator answers, accepted design references, and a bounded implementation POINT. No unresolved contract choice is silently handed to the builder. |
| **P1a — local records and consumer commands** | Astrobley owns `impl/` and `tests/`, using temporary roots only. Build creation, preparation, validation, show/ref, disposition and reconciliation. | Offline restart/correlation/recovery checks; both consumers can locate the same reply and record distinct dispositions. No credentials or HTTP needed. |
| **P1b — transport and confirmation** | Astrobley adds the frozen-request adapter and operator terminal send path. Flight independently checks the enabled workflows. | Mock transport proves exact bytes, cancellation before credential access, distinct confirmations, serialization and unknown-outcome handling. Unsupported agent paths refuse. |
| **P1c — one live pilot and gate decision** | Majkee chooses the credential handoff and confirms the frozen request; Flight witnesses; Cartan integrates evidence. | Five synthetic briefs × three questions, raw receipt and actual usage/cost, both consumer displays/dispositions, Flight verification, then explicit majkee GO or REVISE. |
| **P2 — one manual protocol trial** | A separately scoped successor trial, preferably brief clarification before delegation. | Predeclared comparison and observed outcomes from a small consecutive sample; evidence about useful corrections and total work, not just agreement with the model. |
| **P3 — portable promotion** | Separately authorized compose-first promotion to `zsh/jev/`, after pilot acceptance; usefulness evidence informs how broadly to adopt it. | Manifest for every keeper, dry-run, collision check, fresh zsh and bash sessions, rollback receipt, runtime memory untouched. |
| **P4 — optional automatic advice and learning** | Separate future beds for wallet-backed event consultation, [JUD], or rubric revision. | Each mechanism earns its own acceptance. Delivery remains deterministic; no judgment executes work or changes a gavel. |

**Wallet branch W:** if majkee chooses decision-sheet 2B, W becomes a prerequisite of P1c.
With 2A, P1a/P1b proceed first and the live pilot's credential is a separate explicit choice;
W must still precede any automatic spending mode. Its scope includes protected borrowed-key
retrieval, creation/response-loss reconciliation, expiry/revocation, one bed's total allowance,
and observed Jev access/limit granularity. The $0.05 proposal is not a verified provider
denomination or a proven maximum loss. Wallet mutations and their secrets are outside P1a/P1b.

The smallest execution sequence is two bounded offline builder assignments and one human
pilot sitting. Cartan integrates between assignments; Flight checks independently. Calendar
estimates wait until P0 settles recovery and credential sequencing.

## The two offline implementation assignments

**P1a — ledger and local face.** Freeze the v1 envelope and protocol/validator versions.
Use independent session/request occurrence IDs and full content hashes. The seven proposed
P1 kinds are `session_opened`, `request_prepared`, `send_attempted`, `reply_received`,
`request_failed`, `disposition_recorded`, and `ledger_reconciled`. Budget kinds are reserved
for W. The earlier sixteen-situation inventory is a use-case map, not sixteen event handlers.

Verify private file permissions, explicit attachment, equal-basename project separation,
immutable preparation, request-driven answer validation, and read-only show/ref after restart.
Exercise duplicate IDs, wrong correlation, concurrent writers, truncated tails and interrupted
reconciliation. Hashes detect inconsistency; they do not authenticate a human or the writer.

**A review choice before coding:** D4 preserves a malformed tail in the forensic ledger, so
that recovered physical file is not strict JSONL on every line. Flight must explicitly accept
that reader/export contract or request a revised design. Do not implement generic `jq`/line
parsing while claiming it handles that exception. A complete event missing only its LF is
a different case and must not be discarded.

**P1b — send and failure semantics.** Under one session `flock`, validate the ledger, display
the complete frozen request and approval-scope hash, obtain confirmation, persist/fsync the
attempt, send exactly once, and persist the result. Wrong input or cancellation calls neither
the credential loader nor HTTP. No redirects, hidden retry/fallback or post-approval rewrite.

Test two distinct confirmations through the supported human path, and rejected agent-tool
sends from both consumers using spies. Preserve invalid responses without presenting them as
advice. Lost replies leave remote completion and possible cost unknown. Reconciliation is
local; retry/reconsideration creates a new request and requires fresh approval. Adversarial
reply text and consumer `use` must never turn into command execution.

The human terminal checks are cooperative under one OS account. The wording “agents can
never spend” in decision-sheet §1 is too strong; its following same-user limitation and
design D1 are the actual proposed guarantee. Flight should reconcile that wording in its
own review. Human `!` commands and phone sends remain unsupported until separately witnessed.

## Live pilot sitting

Before requesting live approval, make the payload reviewable: five sanitized reconstructions
of finished own-project briefs, each with tier Choice, clarification Noul and quality Score.
Freeze human comparison labels before the call, keep them out of the provider input, and
state that historical model selection is not a cheapest-model ground truth.

At the sitting, recheck official endpoint/model/schema/pricing and the available account/key
capability. Record the actual resolved model and usage from the reply. Public documentation
alone does not establish credential access. A drifted model allow-list or invalid reply is
evidence to review, not a reason to relax validation silently.

The PAD should contain exact commands and expected observations for preparation, confirmation,
one send, restart, show/ref from both consumers, and separate use/skip/reconsider records.
Mocks carry cancellation, cap and repeated-confirmation checks; the live batch does not
need repeated paid attempts merely to prove those mechanics. Failure or unknown completion
stops the sitting for reconciliation. Flight writes `raw/flight-verification.md`; Cartan
checks its evidence; majkee alone supplies the RUNBOOK's final GO.

## Where Jev could help the protocols

The three tunnel sketches are retained in
[the photo index](raw/majkee-photos.2026-10-03/INDEX.md). These applications are proposals,
not additional requirements for the pilot.

| Protocol boundary | Candidate consultation | Owner and effect | Start |
|---|---|---|---|
| **cSharp / POINT before delegation** | Are required inputs missing? Is the brief specific enough? | Head improves the brief or asks majkee a concrete question. Reuse a frozen rubric. | Preferred P2 trial |
| **Protocol 1: Codex head + Flight carrier** | Does an arrived RETURN contain an issue the head should inspect sooner? | Carrier retains normal delivery/read cadence and may add an attention signal. | P2 manually; automatic only after W |
| **Protocol 1: before asking the human** | Does the gavel/PAD packet explain the choice and its consequences? | Flight improves the packet; the human still receives every required gavel. | P2 |
| **Protocol 2: Claude head + Codex workers** | Does the brief suggest clarification or a different admissible worker tier? | Head chooses assignment; advice never spawns or routes a paid worker itself. | Tier advice stays shadow until measured |
| **Protocol 2: RETURN against POINT** | Which declared requirement appears unanswered in the supplied evidence? | Head/witness inspects the cited artifact; required verification still runs. | P2 |
| **Protocol 3: human tester / PAD** | Is free-text observed behavior ambiguous relative to the expected line? | Tester clarifies or captures evidence. Deterministic comparisons happen in code; Jev cannot certify a test PASS. | P2 if ambiguity recurs |
| **Evidence selection** | Which optional excerpt is relevant to the current question? | Consumer chooses a reading order, with full evidence retained and mandatory sources always read. | Later P2 |
| **[JUD] / conflicting reports** | Compare admissible claims about the same proposition and context. | Code records told-values; a thinking seat or majkee resolves the disagreement. Invalid output contributes no admissible vote. | P4 |
| **Experience across sessions** | Which repeated corrections suggest a rubric revision? | Thinking seat drafts a revision from cited outcomes; majkee gavels it; version is frozen for new requests. | P4 |

File arrival, duplicate detection, timeout, stale input and invalid response detection belong
in code. Advice may increase attention; it must not suppress delivery, scheduled reads,
required review or a human question. No Jev component types into a terminal pane.

## How we learn whether it helps

For P2, start with 10–20 consecutive eligible briefs, not a selection of successful examples.
Before starting, record the rubric, comparison method, primary outcome and stop conditions.
A useful primary outcome is **material missing information discovered before delegation**,
with later rework recorded separately. Compare the existing head's review with the additional
Jev-assisted review; document order effects or use assigned comparison groups if feasible.

For every consultation retain formulation/version, raw answer, labelled interpretation,
use/skip/reconsider, correction, and separately observed outcome. Measure human/head effort,
formulation and interpretation calls, latency and total spend. An inexpensive Jev call can
still be an expensive workflow. Accepted advice is not necessarily correct; disagreement is
not necessarily an error; missing outcomes remain unknown.

Such a small trial supports a keep/revise/stop decision, not a calibrated accuracy claim.
An “experience level” should initially be evidence coverage by protocol/version, not a single
earned authority score. Retrospective records become examples for deliberate formulation;
they do not silently enter a new session or override current instructions.

## Flight as carrier, Cartan as head

The proposed [bed tunnel protocol](tunnel-using-protocole.md) makes Flight the operator-facing
carrier while Cartan remains this RUNBOOK's cSharp head and sole STATUS owner. Flight can
carry a gavel request, collect majkee's exact answer, and return it by file and a short tunnel
message. The tunnel is independent of Jev and can support P0 without a Jev implementation.

Flight can remain the implementation witness while carrying unchanged files and challenging
the design. If Flight authors an implementation body, it cannot independently witness that
body; choose another witness explicitly. Astrobley remains a bounded implementation delegate
with exclusive ownership of `impl/` and `tests/`, not a second STATUS writer.

## Sources and present evidence

- [Cycle-01 RETURN](_bus/01.cartan.return.md), [October 5 proposal](raw/design.2026-10-05.md),
  [Flight map](raw/flight-jev-map.md), and [operator decision sheet](raw/majkee-gavels.2026-10-12.md).
- [October 12 checks](raw/plan-check.2026-10-12.md): document verifier passes; no implementation,
  live Jev store or tunnel vault; tunnel fixture self-test 139/139, live round-trip unperformed.
- [OpenRouter decisions reference](https://openrouter.ai/docs/api/api-reference/alphadecisions/submit-a-decisions-request),
  checked 2026-10-12: the documented mixed-type endpoint remains available. This is a public
  contract check, not proof of account access, price stability or successful inference.

At closure, follow the cSharp transfer and promotion-manifest rules in RUNBOOK, including all
raw keepers and the host-local photo originals. No pruning is part of this planning step.
