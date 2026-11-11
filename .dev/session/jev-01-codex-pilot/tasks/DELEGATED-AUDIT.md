# One-use delegated transcript audit — November 5

Authority: majkee explicitly selected “Add and verify a one-use delegated-send path for this
audit, with a $0.02 allowance.” This supersedes the operator-terminal-only requirement for
this single audit, not for arbitrary future calls. Existing manual send remains unchanged.

The reviewed input is private `~/.jev/dogfeed-20261105/packet.json`: all 31 eligible user/final
messages before the current audit, 16 questions, independent baseline excluded. Pin model
typesafe/jev-1.14, allow resolved typesafe/jev-1.14-20261014. Open this existing work bed once
with total allowance 0.02 USD; bind its generated session into the packet and prepare with
upper bound 0.02. Current public endpoint pricing: 0.000000042 USD/input token, zero output,
262144 context; this declared conservative allowance is not proof of remote per-call enforcement.
Key status was checked read-only. Its remote cap is a separate control, not a new granted budget.

## Narrow implementation contract

- Add native `send REQUEST --authorization-file FILE --credential-env JEV_ORAK_KEY`.
  Manual `send REQUEST --credential-file FILE` keeps its current guard and confirmation.
  Reject mixed/incomplete modes. No generic yes/skip-guard flag; no automatic grant issuer.
- Parent creates exactly one private grant after this explicit operator approval and exact
  preparation. Schema `jev.send-grant/v1`: root (canonical absolute), session_id, request_id,
  approval_sha256, max_cost_usd, credential_env (literal JEV_ORAK_KEY), authorized_by (hlm),
  authorization_ref (1–2048 ASCII bytes in 0x20..0x7e, at least one non-space character,
  identifying observed operator approval; no trimming/normalization), expires_at
  (timezone-aware ISO timestamp). Strict exact field set; canonical hash preserved with grant.
  max_cost_usd must equal frozen upper_bound, be positive and <=0.02; engagement total <=0.02.
  Expiry must be future at invocation. No aliases, general env-key lookup or ambient fallback.
- Read grant through owned0600 nonsymlink regular single-link file, bounded16KiB, race-checked
  open like credential file. Reject malformed fields/JSON, mismatched scope/approval/budget,
  expired grant and prior attempt/reply before reading the named credential or transport.
- Under the existing stable ledger lock, recompute exact current approval hash and validate
  the grant. Append/fsync one attempt with optional `authorization` proof containing full grant
  and its canonical SHA-256; this attempt is the durable consumption. Never unlink/reset it.
  All old attempts remain valid without the extension. New reader validates extended proof,
  scope/hash/budget and expiry against event time on replay, not against today's wall clock.
- Only then read the explicitly named environment value in memory: exactly 1–4096 ASCII bytes,
  every byte 0x21..0x7e, no newline/whitespace/trimming. Call the existing provider once.
  Keep raw receipt, cost/uncertainty,
  no-retry semantics and secret-echo protection. No key in argv, grant, ledger, stdout or logs.
- Both modes reuse one transaction/accounting implementation; do not duplicate paid transport
  or exercise the test-injection seams to bypass the normal production entry.
- A second invocation, reused grant for a different preparation, concurrent send, or interrupted
  attempt cannot trigger another call. Invalid grant leaves no attempt. Post-attempt credential
  or transport failure retains liability and consumes the request; no retry authorization.
- Grant is explicit operator authority recorded by this controller, not cryptographic user
  authentication. Same-user forgery remains outside this cooperative boundary. Future grants
  need new actual operator authorization; possession of this feature is not standing permission.

## Acceptance before actual call

Real CLI mode parsing, default agent guard unchanged; private file checks; valid grant mocked
send; exact bytes/recorded proof and caller; changed payload/current approval/budget/root/session/
request rejection; overlimit/zero/bad expiry; expiry replay; repeated/concurrent/crashed attempts;
env key read strictly after durable attempt; no secret output; old ledgers/tests preserved.
Independent design and source checks, scoped office installation, then exactly one authorized
live call. Parent owns actual grant, credentials, network call, STATUS and result comparison.
Implementer/verifier use synthetic grants/keys/transport and temporary roots only.
