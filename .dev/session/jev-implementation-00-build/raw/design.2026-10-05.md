---
title: Jev pilot — Cartan revision for Flight cycle 01
date: 2026-10-05
author: cartan
status: proposed revision; operator ratification and Flight VERDICT outstanding
supersedes_on_acceptance: raw/design.2026-10-01.md
---

# Cycle 01 design revision

This is Cartan's disposition of Flight's ten decisions, not a record of majkee's gavel.
The POINT explicitly calls the October 2–4 smoothing ungaveled. The existing RUNBOOK gate
remains verbatim. Its implementation hold remains until the open choices below are resolved
and Flight verifies the RETURN. The October 1 design and fixture remain provenance.

## D1 — MODIFY: operator send; local consumer commands

Claude and Codex may prepare, check, show, reference and record dispositions locally.
The only proposed P1 send path is majkee's interactive terminal command:

```text
jev send --session <session-id> <request-id>
  display frozen request + endpoint + model + headers without auth + full hashes
  operator types hash8 at the controlling terminal
  persist attempt → send frozen bytes once → persist result
```

Keep session selection explicit. A shell function may carry an explicitly attached session,
but there is no ambient global current session. Prefer the confirmation prompt above to
accepting `<hash8>` as a command argument: it puts review immediately before transmission.
Hash8 is a human comparison aid, never a capability or signature. Full hashes identify records.

Before credential access, refuse known agent-tool contexts and noninteractive invocation.
These checks prevent accidental use; a same-user process can imitate their inputs. UI `!`
and phone paths are candidates, not enabled send paths until witnessed. A blanket check for
an agent environment could reject a human-typed `!` command too. Do not promise both behaviors
without testing the actual runtime. No native permission rules or hooks are added here.

Freeze the request body using Python's `json.dumps(..., sort_keys=True, separators=(",", ":"),
ensure_ascii=False, allow_nan=False).encode("utf-8")`. Hash and transmit exactly those bytes.
Keep `request_sha256` as the body hash. Also freeze the method, HTTPS endpoint and allowed
non-auth headers; `approval_scope_sha256` hashes that canonical object plus the body hash.
Type the scope hash prefix. A changed endpoint, body or header invalidates prior confirmation.
No redirects, hidden retries, automatic provider fallback or reserialization after approval.

Freeze the accepted resolved-model list in `request_prepared`; a new provider snapshot needs
a new preparation, not a wildcard match. Expose the full frozen state/questions for review;
a list of question names alone is insufficient.

Cancellation/wrong input must call neither the credential loader nor transport. Test these
with spies, including two rejected agent sends from each CLI. An absent ledger attempt is
not proof of absent network traffic. Exercise two distinct operator confirmations with a
mock transport; keep those fixtures separate from the individually approved live request.
Ask Flight to verify this reading of the RUNBOOK acceptance clause: two local consumers,
one enabled operator send workflow. No gate-text amendment is proposed.

## D2 — MODIFY: keep the wallet design; separate its activation

Recommend gpg/pinentry for the management credential under `~/.secrets/jev/`, a $0.05
operator-selected default, an expiring borrowed inference key, and no automatic re-mint.
However, constructing a management-key lifecycle is a separate bounded step before wallet
mode, not an implicit addition to this pilot. Decide this sequencing with majkee. P1 can
first prove its transport and ledger offline; its eventual live credential handoff must be
explicitly selected and approved before use. Do not quietly fall back to an exported key.

The public management API supports key creation with USD `limit`, UTC `expires_at` and
`limit_reset: null`, and updates including `disabled` and `limit` [S1–S3]. Set no recurring
reset. A $0.05 limit is proposed, not an observed accepted denomination. Newly minted key
access to `/api/alpha/decisions`, exact exhaustion behavior and revocation latency are untested.
Do not state that maximum loss is *exactly* the nominal limit without those measurements.

The lifecycle needs more than an adapter field:

- Creation can succeed remotely before the response is lost. Never retry creation silently;
  reconcile the named operation, and disable unidentified/orphaned grants before proceeding.
- The plaintext borrowed key is returned only on creation [S1]. Separate CLI invocations
  therefore need an explicit protected host-local storage/retrieval decision. The ledger
  keeps its provider hash ID and nonsecret grant metadata only. This decision is still open.
- A GPG prompt is an unlock, not an attestation to the exact HTTP request. Test the selected
  decryption mode, agent cache and external pinentry cache independently [S4]. Never claim
  a same-user security boundary merely because a TTL is set to zero. No shared GPG settings
  are changed by this proposal.
- Grant/top-up records follow confirmed provider mutations. A crash or lost response leaves
  an unknown operation that blocks further mutation until reconciled; it does not create a
  local success. Log no keys, passphrases, auth headers or raw management responses.
- Local spend is *recorded spend*. A lost reply or out-of-band use can make it incomplete.
  Unknown cost is not zero, and `remaining` must be labelled estimated/unknown accordingly.
- A local stop refuses future sends; it cannot cancel a request already accepted remotely.
  Drain/revoke needs provider acknowledgement before claiming the borrowed key is disabled.
  Disabling must not depend on successfully paying for another request.

These are review requirements for the wallet step, not additional P1 commands to implement.
If majkee requires the wallet before the first live request, keep that request held and scope
the wallet work explicitly. Do not infer authorization to read or alter existing credentials.

## D3 — MODIFY: one bed, one pilot session, one funding scope

Recommend one wallet per bound runbook bed. For P1 the mapping is deliberately one-to-one:
one bed, one Jev session, one grant lineage. A second Jev session must not silently mint a
second allowance for the same bed. Sharing a bed across several funded sessions later needs
a bed-level spending authority and lock; summing independent session ledgers is insufficient.

The proposed wallet ID derives from canonical project root plus canonical bed path, not a
human slug alone. For an unbound session there is no funded wallet until majkee chooses a
scope. No new global registry. A replacement grant must account for already spent credit;
rotation cannot replenish the authorized total implicitly.

A small OpenRouter balance is an operational backstop only under verified account conditions
(including recharge and other usage). It is not a hard global Jev ceiling established by
our code or this review. No account configuration has been inspected or changed. Majkee
still decides bed scope, default amount and whether this mechanism precedes P1 live use.

## D4 — MODIFY: exact bytes, explicit recovery and request-driven validation

Hold an OS `flock` on a stable session lock file from ledger validation through attempt,
HTTP completion and durable result append. Keep it through confirmation too; use bounded
timeouts and a clear busy response. Never unlink a lock file to release it. Flush/fsync an
attempt before transport. Check the entire small pilot ledger, not merely its last line.

`show` and `ref` can inspect a snapshot of the valid prefix without the writer lock. They
must label an unfinished tail or unresolved attempt, and cannot call it a complete session.
Send always uses the frozen prepared request. `buffer_sha256` measures preparation input;
missing/changed current input is disclosed as freshness information, never substituted.

Operator-only `jev reconcile` is local and never resends. Two recovery cases are distinct:

1. **Complete JSON event without its final LF:** validate its identity, sequence and
   correlation, append LF under lock, then append `ledger_reconciled`. Do not discard an
   otherwise complete reply or attempt.
2. **Malformed trailing fragment:** preserve its exact bytes. Append a separator LF when
   needed and a `ledger_reconciled` event naming byte offset, byte length, SHA-256 and the
   last valid sequence/prefix hash. Ordinary writers remain blocked until the recovery
   record is durable. A reader may quarantine only that exact verified fragment; arbitrary
   middle-file corruption, duplicate IDs or conflicting correlations still stop recovery.
   If recovery itself is interrupted, inspect that boundary again; never auto-skip damage.

Case 2 necessarily leaves a damaged physical line in the forensic file. It is **not strict
JSONL throughout** after recovery. State that exception explicitly; a derived export may
emit only verified JSON events, retaining the reconciliation reference. This is the cost
of Flight's append-only repair; silently promising both byte preservation and an ordinary
all-lines JSONL parser would be false. Flight should challenge this choice before coding.

Separately, an attempt with no terminal receipt blocks sends. Reconciliation appends a
`request_failed` with `remote_completion: unknown`; it does not assert provider failure or
erase possible charges. A deliberate retry gets a new request ID, `retry_of`, a reason and
fresh confirmation. Reconciliation of bookkeeping is never approval of that retry.

Validation is against the frozen request and adapter version:

- Reject missing/extra answer names, wrong types, nonfinite numbers and booleans posing as
  numbers. Probability keys must exactly match choice candidates or score levels.
- Require probabilities in [0,1] and sum near 1. Choice must be one of the maximizers,
  permitting ties. Score must agree with the weighted level and exact legend. Initial
  proposed numeric tolerance is 1e-6 for sums/choice differences and
  `1e-6 * max(1, highest_level)` for weighted score; freeze these with the validator version.
  If provider precision differs, preserve the invalid receipt and review, never relax silently.
- Noul is a probability and has no provider confidence field. Do not manufacture one.
- Preserve the original parsed provider JSON even when semantic validation fails; do not
  normalize it into a valid-looking answer. Handle non-JSON/oversized failures as bounded
  diagnostics, not fabricated provider responses. Actual cost, when validly supplied, still
  counts even for an invalid judgment.

## D5 — ACCEPT: shared envelope vocabulary, scoped certainty

Retain `schema, event_id, sequence, at, session_id, request_id, kind, actor, data`.
Add `actor.source: record` and `data.certainty` with the proposed vocabulary:
`confirmed | observed | correlated | inferred | unknown`. `actor` can retain runtime/seat
provenance separately; source is how the evidence is obtained, not its author or authority.

Certainty describes the event claim. A received reply can be confirmed as a receipt while
`validation.status` is invalid. Neither field says the judgment is true. An unresolved
remote completion uses `unknown`; its local failure observation can still be documented.
Unknown kinds or schema versions must never be silently treated as permission to send.

This adopts Oraculum's two fields for Jev only. The other EVENTS map is still a draft and
has not changed on our behalf. The separate nablarva RETURN is outside this cycle's write
scope; this design and STATUS record our disposition, not delivery or acceptance there.

## D6 — ACCEPT: belnap names a protocol; jev names the runtime

Adopt the recorded direction as Cartan's recommendation: `jev`, `~/.jev/`, `jev.event/v1`
stay; **belnap** is the first protocol, not an agent card, personality or germline identity.
The protocol identifies purpose, typed rubric/version, admissible inputs and interpretation.
Freeze rubric content/hash, not just its name. Epoch F3's Claude Bash agent is superseded
by the later operator direction; no Janus or native harness primitive is created here.

The later [JUD] machinery remains out of cycle. One correction matters now: malformed or
self-inconsistent model output is an invalid observation. It contributes no admissible vote
about proposition P; retain a separate validation error. It does **not** prove both P and
not-P. BOTH should represent opposing admissible claims about the same proposition/context.
Transport validity, probability, confidence, disposition and truth stay separate.

## D7 — MODIFY: project-scoped ledger, stable identity

```text
~/.jev/projects/<readable-name>-<root-hash>/
  <UTC-time>-<session-id>.jsonl   first event: session_opened
  <session-id>.buffer.md         editable authoring input
  <session-id>.lock              stable OS-lock target
~/.jev/config.json              optional defaults for new sessions only
```

Use canonical absolute project root, with a hash suffix to prevent equal basenames colliding.
Verify the full recorded root on opening; a shortened path-hash collision must refuse.
An explicit project root remains supported; cwd can supply a displayed project default at
creation, but never implicitly attach a bed or bus. Validate bed/bus containment and any
existing registry key against the actual resolved root. No new registry or ambient session.
Directories/files remain 0700/0600; portable defaults never overwrite runtime contents.

`session_opened` has sequence 1 and null request ID. It freezes host, project, optional bed
and bus, protocol, provider defaults and limits. Remove `session.json` as an authority.
For P1 rebinding creates a new session; no in-place edit or general binding-update mechanism.
Each preparation references the opening event and freezes its effective request policy.
Changing config cannot alter a prepared request or increase an existing allowance.

Keep independent random session/request IDs. Interpret “hash IDs” as content-addressed event
IDs and full request hashes, not “same body means same request.” A deliberate repeat must
have a new request ID. Proposed event ID: SHA-256 of canonical full event with `event_id`
omitted, including sequence/session/request IDs. This checks content, not authenticity;
same-user rewriting can recompute hashes. No blockchain or second index is needed.

A portable bus extract embeds the relevant opening/preparation, attempt, reply and disposition
events with hashes, validator/protocol versions and host label. Publish only approved payload
content under the owning bus's rules. Host-local file paths alone cannot prove a cross-host
claim. A verified hash establishes consistency, never human authorization or model correctness.

## D8 — ACCEPT: later source in zsh/jev; runtime stays private

After pilot acceptance and a separately authorized promotion, put Python engine, thin shell
face, protocols, rubrics, defaults and help in `ia-sync/zsh/jev/`. The existing deploy leg
copies `zsh/` to `~/.config/zsh/` (`deploy.sh:249–252`, read on October 5). No new deploy leg
is needed; shell activation and bash access still require deliberate wiring and fresh-session
proof. `~/.jev/` receives no deployed source. The pilot remains in its bed's `impl/` and
`tests/` with temporary roots. This cycle creates neither.

## D9 — MODIFY: explicit lifecycle kinds and lineage

Keep the original five kinds and add `session_opened` and `ledger_reconciled` for P1.
Reserve `budget_granted` and `budget_locked` as distinct kinds for the separately scoped
wallet step. Do not disguise funding or session creation as dispositions of a model reply.
Reserving names does not ship wallet commands. Their mutation/reconciliation contract must
be completed before activation. Session/budget/recovery events may have null request IDs.

Inside preparation data, use nullable, explicit lineage fields:

| field | meaning |
|---|---|
| `parent_request_id` | A prior consultation supplied input; no automatic cascade in P1. |
| `reconsider_of` | Revision of an earlier question/context; include a change reason. |
| `retry_of` | Fresh approved attempt after failed/unknown transport; possible duplicate cost. |

References must resolve to earlier requests in the same session for P1; never silently join
another session's IDs. Request ID identifies an occurrence; body hash identifies content.
Multiple append-only dispositions are allowed. A new disposition does not overwrite earlier
ones or automatically establish a final opinion. Label consumer interpretation separately
inside its disposition, with the exact raw-reply reference beside it.

## D10 — MODIFY: five-brief shadow batch, measured claims

Use **five briefs × three questions = 15 questions**, within the pilot's 20-question cap.
Flight's upper suggestion of eight briefs would require 24 questions. Prefer synthetic,
sanitized reconstructions of finished own-project briefs to preserve the RUNBOOK's synthetic
mixed-type acceptance example. Freeze the five items and human comparison labels before
the call; keep eventual outcomes and expected labels out of the provider's input.

Ask tier Choice, clarification Noul and brief-quality Score for each. Keep each brief's
questions explicitly scoped to its ID. Record shared-state interference as a limitation.
Actual historical model selection is not ground truth for the cheapest adequate model;
counterfactual performance is unobserved. Compare stated rubric judgments and record where
historical evidence is missing. Five examples prove plumbing, not calibration or savings.

Both consumers then show/reference the reply and record use/skip/reconsider independently,
without routing a paid model. A reconsideration may be prepared without being sent. The
batch itself still needs its own approval. Flight's mock checks and live witness remain.

## What the pictures add to this revision

Cartan directly viewed all 13 upload images. Byte-identical named copies are present in
`raw/majkee-photos.2026-10-03/`; their p0–p5 pages and t1–t3 diagrams are the primary operator
sketches. Flight's INDEX.md checksums were independently verified as well. Keep images
host-local and out of git per that INDEX; include them in the eventual promotion manifest.
The s1–s4 study screenshots are inspiration, not capability or benchmark receipts.

The p0/p3 emphasis is durable: build session processes with stable files and commands; put
model judgment at a bounded point. The proposed later shape is:

```text
session events → deterministic detection/delivery → scheduled head/consumer read
                                └→ optional Jev consultation → extra advisory signal
```

Thus a missed/invalid judgment cannot suppress delivery. P2 watchers, [JUD], cascades and
rubric scoring stay parked. Sixteen candidate situations answered the original “~10–20”
inventory request; there are no missing four required events, and no promise of 20 triggers.

Do not promote the map's stronger inferences unchanged: different vendors do not establish
independent errors; two equal responses do not prove determinism; multiplying marginal
accuracies is not a general bound for a dependent cascade. Opposite judgments establish
inconsistency only when they address the same proposition under the same assumptions.
These are corrections to future interpretation, not additional implementation tasks.

## Public source recheck — October 5, unauthenticated

- **S1:** [Create key](https://openrouter.ai/docs/api/api-reference/api-keys/create-a-new-api-key):
  creation fields, one-time plaintext return. No key was created.
- **S2:** [Update key](https://openrouter.ai/docs/api/api-reference/api-keys/update-an-api-key):
  disable/limit updates; unknown fields can be ignored, so verify returned state. Expiry is
  not among the accepted update fields. Old `update-keys` URL returned 404; used the docs index.
- **S3:** [Management keys](https://openrouter.ai/docs/guides/overview/auth/management-api-keys):
  administrative capability is separate from completion inference.
- **S4:** [GnuPG agent options](https://www.gnupg.org/documentation/manuals/gnupg/Agent-Options.html):
  agent and external caches exist; signing-cache controls are not a generic decryption proof.
- **S5:** [Decisions API](https://openrouter.ai/docs/api/api-reference/alphadecisions/submit-a-decisions-request):
  requested route, mixed types and dated model example still documented. The page also contains
  a management-key-only 403 example; do not interpret that isolated example as proof of which
  key classes the Decisions endpoint accepts. Authenticated behavior remains untested.
- **S6:** [JEV-as-a-Judge, v3](https://arxiv.org/abs/2609.26550v3), dated September 29:
  the primary abstract supports a task-dependent boundary and local threshold validation.
  The screenshot shows v1. Neither version validates our briefs or the screenshot's broad
  speed/cost claims. No benchmark replication or full-paper audit was performed in this cycle.

## Operator decision packet

Recommended package: D1 operator sends; D6 belnap protocol; D7 project-scoped event-led storage;
D8 later promotion under zsh/jev; D10 five-brief shadow pilot. D4/D5/D9 are Cartan's technical
dispositions, subject to Flight verification. Ratify or amend the package without restating
the whole design.

Separately choose D2/D3 sequencing: **recommended — prove the pilot offline first, then give
the GPG/borrowed-key wallet its own bounded assignment before wallet mode**; or require that
wallet before the first live pilot send. In either case, confirm the proposed $0.05 default
and one-bed/one-pilot-session scope. This is a design choice, not permission for a paid call,
credential access, implementation or deployment in cycle 01.
