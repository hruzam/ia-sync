# Jev source and vault build — 2026-11-04

Current implementation contract extending DESIGN. Majkee explicitly authorized building Jev
and its zsh vault on the surgical table, using Astrobley. This releases source construction
in `zsh/jev/` and shell wiring. The old kernel in `impl/` is a historical snapshot; the new
editable kernel is `zsh/jev/kernel.py`. Tests and evidence remain in this bed. No paid call,
credential inspection, full deploy, commit/push or global guide publication is implied.
After independent acceptance, the requested shell/vault setup includes scoped office
activation of Jev's files and its single ai/base signpost, plus an empty private runtime
directory. Filesystem approval is still required outside the workspace. Do not initialize
an engagement with an arbitrary permanent model/budget policy merely to demonstrate install.

## Runtime and command contract

Standard library Python, Linux flock; source `zsh/jev/{kernel,store,provider,jev}.py`.
One namespace `python3 zsh/jev/jev.py --root ROOT ...`. ROOT defaults to `~/.jev` only when
the operator actually invokes a command. Tests ALWAYS provide temporary roots. No root is
created on import, help, source, failed selection or reading an absent vault.

- `open --project PATH --bed PATH [--budget USD] [--model ID --allow-model ID ...]`:
  project/bed must be existing canonical directories, bed within project. Stable project
  hash directory and engagement lock prevent duplicate sessions. Reopen same binding
  idempotently; changed opening settings refuse. Budget omitted is UNSET. One channel main.
- Selected operations take `--session ID --channel main` explicitly. `settings` returns
  project/bed/session/channel, immutable policy, total/spent/reserved/available and blocking
  liabilities. No existing-session policy/budget mutation or refill command.
- `prepare PACKET [--lineage FILE] [--upper-bound USD --bound-evidence TEXT]` freezes the
  kernel packet with session/channel matched, an optional lineage object and provider body
  when a model policy is present. Source path/hash is diagnostic; send uses saved bytes.
- `import-reply REQUEST RECEIPT` records an explicitly SYNTHETIC/internal receipt, raw JSON
  and validation; a malformed/invalid reply still gets diagnostic history. It cannot settle
  a real attempt or become live-provider evidence. No duplicate terminal receipt per request.
- `interpret REQUEST QUESTION POLICY` appends result/error with policy, selected receipt
  and request references. `dispose REQUEST use|skip|reconsider --consumer NAME [--reason TEXT]`
  appends independent dispositions. `outcome REQUEST FILE` stores later labels/adjudication
  with references without rewriting observation or disposition.
- `show [--request ID]` JSON history; `ref REQUEST` returns exact ledger path, event ID and
  sequence, preferring the retained reply when present and otherwise the preparation,
  not merely a mutable line number. Both expose valid prefix and incomplete-tail
  diagnostics. `memory FILE` records a versioned explicit note; `prepare` can select it
  explicitly by event ID, never silently inject the latest note.
- `select FILE` freezes a next-loop selection manifest: policy id/version, ordered items
  `{event_id, excerpt}` and optional labels/layers. References must belong to this session;
  excerpts must occur in the canonical referenced event. `prepare --selection EVENT_ID`
  freezes that manifest and its source events into state. Lineage has branch/step strings,
  parent_request_ids list and optional reconsider_of/retry_of with reason. Same-session prior
  references only. No automatic ranking, cache hits, scheduler or inference.
- `reconcile` explicitly handles a valid final event missing LF or one malformed trailing
  fragment. For a fully valid event missing only LF, appending/fsyncing LF is itself the
  complete recovery; a later audit event is optional. A crash after that LF leaves a valid
  completed event, not an unknown recovery. This technical choice supersedes the older
  proposal's mandatory recovery-event requirement for this case. For malformed tails,
  keep exact original bytes. A recovery event identifies fragment offset/length/hash
  and verified prefix. A reader skips only a fragment matched by the adjacent valid recovery
  event; unknown/middle corruption blocks writes. Forensic ledger may then not be strict
  JSONL, as DESIGN already discloses. If recovery itself is interrupted and cannot be proven,
  fail closed with evidence; never erase unknown charges or resend.

## Ledger integrity and concurrency

Private root/project dirs 0700; ledger/stable locks 0600. Refuse symlink-managed roots/files
and insecure existing managed paths rather than chmod unrelated material. Full root/bed
identity checked from opening event. Session lookup is bounded to the explicit root; refuse
duplicate/colliding IDs. Reject path traversal in IDs.

All state mutations hold the stable engagement/session lock, validate/replay the entire small
ledger and append canonical LF-terminated events with flush/fsync before returning. Never
unlink the lock. Creation and opening share deterministic engagement locking. Event fields:
`schema,event_id,sequence,at,session_id,channel,request_id,kind,actor,data,previous_event_id`.
SHA-256 covers the canonical full event except event_id. Hash/sequence/previous link and
known schema/kinds checked; missing references and impossible transitions refuse. This is
local consistency, not authentication. Publish no mutable sidecar as another state authority.
Fsync new files/directories as needed. Failed persistence means no success response.

## Spend and send

Budget accounting is Decimal from decimal strings. Reject negative/nonfinite/bool input.
Admission requires known total and liabilities and `spent + reserved + upper_bound <= total`.
A bound is a declared conservative upper bound with evidence, not a price guess. Local
admission is not proof of the provider ceiling. No budget is configured by this build.

`send REQUEST --credential-file PATH` is operator-terminal only: reject known Codex/Claude
agent-tool environments and noninteractive invocation BEFORE credential access. Display full
saved payload, method, endpoint, nonsecret headers, model policy, budget/bound and approval hash;
freshly request the hash prefix on controlling terminal. Cancellation reads no credential and
calls no transport. Hold the lock through review, durable reservation/attempt, one call and
settlement. No CLI yes/approval flag, persisted approval reuse or automatic resend. Per-request
terminal/attempt uniqueness; an intentional retry is new preparation/ID with lineage.

The credential file is explicitly supplied, owned by current user, regular nonsymlink 0600,
bounded nonempty key read only after confirmation. Never read ambient exported API keys.
No key value, auth header or exception string containing it may reach output/history.
An encrypted key manager/wallet is separate future work. No actual credential file is created
or read during this build. Cooperative same-user guards are not an authentication boundary.

Raw HTTP bytes and status retained before interpretation. Known valid billed cost settles
even invalid advice; missing/untrusted cost or transport uncertainty retains liability and
blocks later sends. Record actual overrun and block, never clamp. Imported/synthetic results
cannot release a reservation. No automatic reconciliation of uncertain remote completion.
Test the send path through injected confirmation/credential/transport seams, never real HTTP.
OpenRouter endpoint fixed to https://openrouter.ai/api/alpha/decisions; no redirects, proxies
from environment, retries, model fallback or post-confirmation reserialization.

## Provider module interface (separate owner)

`provider.py` imports sibling kernel, has no store/CLI dependency:

- `ENDPOINT` string fixed above; `ADAPTER_VERSION` string.
- `build_request(packet, model) -> bytes`: validate packet, map typed questions, include full
  explicit evidence/memory/state; add `provider: {allow_fallbacks: false}`. Return canonical
  exact body bytes, <=1 MiB. Pin caller's model string, no implicit latest/default.
- `parse_response(prepared, raw_bytes, allowed_models) -> dict`: always return
  `{receipt: object|null, validation: {status,errors}, cost_usd: decimal-string|null,
  provider_id: string|null, model: string|null}`. Cost extracted independently from answer
  validity with Decimal parsing; do not manufacture zero. Raw bytes remain caller-owned.
  Check exact answer keys/types, model allow-list, Score legend and kernel typed validation.
  Provider wire Noul.noul -> probability, Choice.choice -> value, Score.score -> value.
- `post(body_bytes, key, *, timeout=30, max_bytes=1048576) -> (status:int, raw:bytes)`:
  one HTTPS POST, TLS verification, no redirect/retry/env proxy. Bounded errors contain no key.
  Over-limit or transport error raises `ProviderError`; caller records unknown liability.

Current primary docs checked Nov4: OpenRouter Decisions reference (request/provider/response
usage.cost), TypeSafe Choice/Noul/Score. Account access/pricing/backstop unverified. Provider
worker retains source URLs, date and exact fixture limits in adjacent reference docs.

## Shell surface (Cartan ownership)

`zsh/jev/base.zsh` sources only sibling engine and keyboard; silent/idempotent. `jev.zsh`
functions, `keyboard.zsh` aliases only. `jev` delegates to local sibling Python script.
`jev-use ROOT SESSION [main]` validates settings before exporting JEV_ROOT/JEV_SESSION/
JEV_CHANNEL for this shell; no global current file. `jev-off` detaches only this shell.
Wrapper supplies explicit selected arguments, rejects mixed overrides when attached, and
leaves help/open available without selection. Python direct entry never uses ambient session.
Wire shared ai/base.zsh to the sibling Jev signpost so both machine configs use the same
entry without changing the home-owned config. Fresh zsh and bash/direct Python smoke tests.

## Acceptance

Existing 26 kernel regressions against promoted kernel; real subprocess vault roundtrip;
two processes/restart/duplicate open, concurrent mutation, private modes/symlink refusal,
cross-session reference rejection, missing LF/malformed tail/middle corruption, immutable
packet/note/selection, dispositions/outcomes, budget reservation/unknown/overrun, distinct
confirmations with spies proving rejection-before-credentials, exact sent bytes, malformed
provider and no redirect/retry behavior. Fresh independent verification after integration.
Full live pilot GO and guide publication remain later, explicitly qualified work.
