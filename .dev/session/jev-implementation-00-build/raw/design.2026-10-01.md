---
title: Jev pilot — operator choices and reviewable design
date: 2026-10-01
author: cartan
status: operator-approved direction; implementation contract for Flight review
---

# Jev consultation with local session records

## Operator choices

- OpenRouter is the pilot provider; Vercel Gateway stays parked.
- Store resumable runtime records under `~/.jev/`, inspired by useful CLI session-storage
  properties but using a vendor-neutral Jev schema. Do not copy native vendor transcript state.
- Attachment to `<project>/.dev/session/<slug>/_bus/` is an explicit session setting.
  Cartan, Claude or another attached consumer can use the adapter; no permanent relay seat.
- On request, the consumer shows a compact advisory block in the CLI conversation **or points
  to its file**. The arriving structured JSON should be retainable as one JSONL record.
- The consumer may use, skip or reconsider the judgment. Experience from previous streams
  and gavels is useful later; automatic learning/promotion is not part of this pilot.
- `(?)` in this conversation asks for Cartan's independent position or alternative.
- Majkee opened the authoring gate after these additions; Flight is the second voice and
  majkee wakes it after the first part. Do not confuse that with approval of a paid request.

## Smallest proposed implementation

A shared Python command callable from zsh or bash prepares an explicit consultation, sends
it only through the confirmed human gate, records the reply, and stops. No background event
listener. The initial workload is **advisory model-tier selection**, a Cartan recommendation
for Flight to challenge; transport acceptance still covers all three question primitives.

```text
~/.jev/sessions/<neutral-session-id>/
  session.json       explicit binding/settings; no credentials
  buffer.md          editable human/CLI input
  events.jsonl       authoritative request/reply/disposition receipts
  .lock             OS-held writer lock; existence alone is not ownership
```

Use a stable random ID for the decision session, separate from vendor thread IDs. Explicitly
attached consumers can share it; sharing a project or a seat name does not attach a session.
The selected session is required for every operation; no ambient global "current session".
Keep the root private to the user (new directories 0700, files 0600). Tests use a temporary root.

`session.json` is the single adapter binding surface: schema version, session ID, provider,
requested model, optional existing project key, resolved project root, optional bed/bus path,
and pilot limits. Validate the selected bed/bus belongs to the selected project; refuse a
registry/path mismatch instead of silently rebinding. Reuse
`/home/hruzam/ia-sync/zsh/registries/projects.json` when the project is registered. ia-sync is
not currently in that registry; an explicit project root works without adding a registry row.
No new global project registry is required. Integration with any external session-setting API
must use its inspected interface; no such interface is assumed to exist by this proposal.

The Markdown authoring surface remains. For the first parser, prefer a plain `## State`
section plus a `## Questions` fenced JSON object using native `type`, `instructions`, and
`criteria` fields. This is an implementation proposal replacing the draft's YAML shorthand;
it avoids a new YAML dependency and a second vocabulary. Flight may revise it before coding.
Freeze only parsed state/questions and the selected provider/model, not incidental commentary.

## JSONL contract — retain the provider reply, add correlation

Serialize a complete object as compact UTF-8 JSON plus one LF; never append pretty-printed
multi-line JSON with `cat`. Newlines inside string values are escaped by the JSON serializer.
The example file `jev-events.example.jsonl` demonstrates the proposed shape with synthetic data.
Its records carry `fixture: true`; they cannot serve as live approval, billing or provider
evidence and must never be imported into a live session as actual send receipts.

Every record carries `schema`, `event_id`, `sequence`, `at`, `session_id`, `request_id`, `kind`,
`actor`, and `data`. The sequence is session-local under one writer lock. Actor/runtime is
provenance, not storage ownership or authorization. Five lifecycle kinds suffice:

| kind | data and meaning |
|---|---|
| `request_prepared` | Frozen endpoint/request, request SHA-256, question version; no send yet. |
| `send_attempted` | Same request hash and a reference to actual approval evidence; persist before HTTP. |
| `reply_received` | Original parsed provider response nested unchanged, validation outcome, latency, input freshness, advisory marker. |
| `request_failed` | Bounded reason code, known HTTP status if any, and whether remote completion is unknown; no fabricated answer. |
| `disposition_recorded` | Reference to reply event, `use`/`skip`/`reconsider`, optional correction and separately observed outcome. |

The SHA-256 is over canonical request-body JSON (sorted keys, compact separators, UTF-8,
nonfinite numbers forbidden); endpoint is frozen alongside it and included in the approval
scope. JSONL preserves the provider's JSON structure, not its original whitespace. Credentials
and authorization headers are excluded. A receipt saying "approved" is not itself proof of
human approval; the actual enabled interaction must be tested independently.

Only `events.jsonl` is authoritative for receipts. Display blocks and optional exported JSON
are derived views. A file reference names host, session, request, event and absolute ledger path;
do not depend on a mutable "latest reply" pointer. A raw reply includes `answers`, `model`,
`provider`, `id`, and `usage` as supplied. Prefer actual `usage.cost` to a hardcoded estimate.

Serialize session writers and persist the attempt before dispatch. Flush durable records at
the recovery boundaries. A partial final line, duplicate sequence/ID or inconsistent correlation
must be surfaced; preserve evidence and refuse further sending until explicitly reconciled.
Do not silently truncate, mark the request successful or resend. A send without a conclusive
reply/failure receipt is indeterminate; a later retry can duplicate cost and needs fresh approval.
Counters come from recorded attempts, not an independently drifting `.count` file. Suggested
pilot caps remain 10 attempts per session and 20 questions per request; neither enforces authority.

## Consumer protocol

1. Prepare and validate a bounded batch. Review/approve its exact frozen contents and endpoint.
2. Send once. Preserve and validate the structured reply. Keep invalid replies out of the
   advisory display while retaining bounded diagnostic evidence without credentials.
3. On request, show the compact block **or provide the file reference**. These are local reads.
4. Record use, skip or reconsider against the exact reply. Use means adopting advice, not
   authorizing a command; the consumer's normal action permissions still apply.
5. Reconsider names changed state, criteria, candidates or model and creates a new request.
   A manual retry after a transport failure can retain input, but records its reason and prior
   request ID and obtains fresh send approval. No reroll-until-agreement behavior.

A display block contains the question, typed answer, supplied probabilities/confidence where
applicable, input revision/hash, request ID and receipt location. Noul has no confidence field.
Consumer interpretation must be labelled separately; no invented Jev rationale. Preserve the
raw judgment when local policy marks `needs_review`; no universal 0.7 threshold is settled.

Exact admission and approval remain code/runtime responsibilities. The old statement "set
both CLIs to ask every time" is not an implementation. Flight must challenge the concrete path;
unsupported agent-initiated sends stay disabled. Operator-run prepared sends are the smallest
candidate fallback. A TTY prompt, cap, file flag or cooperative shell convention is not a
security boundary against a same-user process which can obtain the credential.

## Sixteen candidate situations; no automatic subscriptions

| situation | useful judgment or deterministic handling | consumer response |
|---|---|---|
| New task | Is the brief sufficiently specified? | proceed or clarify |
| Several next steps | Compare an admissible shortlist | consider the suggested step |
| Model-tier choice | cheap / middle / frontier / human | confirm routing separately |
| Excess candidate evidence | Rank relevance | retain mandatory rules/evidence |
| Conflicting sources | Identify a likely contradiction | inspect the cited sources |
| Tool failure | Classify plausible causes | choose a diagnostic |
| Repeated ineffective attempts | Recognize lack of progress | change approach; exact counts stay in code |
| Scope expansion | Assess material change | bring scope to the operator |
| Unclear consequences | Flag concerns/missing context | retain existing action gates |
| Completion claim | Assess supplied evidence | perform real verification |
| Uncertain reply | Preserve uncertainty | ask, skip or gather evidence |
| Conflict with gavel | Retain disagreement | gavel remains authoritative |
| Input changed in flight | Code detects stale input | retain old receipt; optionally prepare anew |
| Failed/invalid response | Code records failure | continue without advice or approve a retry |
| Human accepts/rejects/corrects | Record disposition and outcome separately | retain feedback |
| Pattern recurs across streams | Assemble experience examples | propose rubric/protocol for gavel |

These are a design inventory. V1 uses model-tier advice plus uncertainty, disagreement,
staleness, failure and disposition handling. Do not build sixteen triggers.

## Bus, RUNBOOK and learning

The local ledger contains every consultation. Publish to an attached bus only when the result
matters to shared work and the session authorizes the write. Keep useful result/evidence in
the exchange; a host-local `~/.jev` path alone is not portable evidence. Follow the owning
bus's schema and writer rules, rather than appending arbitrary files or creating a watcher.
The RUNBOOK carries this fixed protocol; STATUS owns the resulting next action; a bus record
carries a particular exchange. Neither vendor identity nor mere file presence grants authority.

Later learning starts with an experience ledger: advice, human disposition, correction,
observed outcome, model/question versions, and gavel provenance. Acceptance is not correctness.
Past replies are examples, not fresh evidence or instructions. Do not automatically replay
prior streams, update thresholds, assign an experience score or promote lessons into canon.

## Fold disposition

- Keep the memory draft's readable batch, separate send/action gates and advisory semantics.
  Replace bus-owned storage, per-vendor session isolation, blanket confidence rewriting and
  the claim that a permission-setting label proves enforcement.
- Keep the older handoff's separation of evidence/model/policy, failure handling and shadow
  evaluation. Replace direct-TypeSafe credentials/endpoint with the selected OpenRouter route.
- Reuse the smoke script's numeric checks, bounded HTTPS and no-retry behavior; replace its
  fixed payload/model validation with request-driven, provider-aware checks. Strengthen answer
  correlation and choice/score consistency tests. Do not modify the original research script.
- Preserve original raw inputs through closure; the cSharp promotion manifest must account
  for each one, the new design/research evidence and the synthetic schema example.
