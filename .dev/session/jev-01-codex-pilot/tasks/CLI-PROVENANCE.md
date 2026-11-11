# CLI provenance increment — November 5

Operator request: saved Jev replies and their future cache references must retain which CLI
session produced the record: Codex, Claude, Gemini; reserve controller and leave it empty.

Implement this bounded increment after independent design check. Existing Jev session,
channel, request and reply event IDs remain distinct from calling CLI session IDs.

Operator clarification in the same turn: requests from majkee are `hlm`. Record independent
`requester` provenance (`hlm`, `agent`, or null unknown) under the actor, selectable through
explicit `--requester hlm|agent` before the subcommand. Do not infer human intent from TTY or
infer requester from a CLI brand. A human-origin request may be submitted through Codex;
requester and cli_sessions then record different facts. The calling agent may explicitly
declare hlm when carrying the operator's task; otherwise leave unknown unless supplied.
Origin of the prepared request remains available through its linked event even if the later
send/reply recorder has a different requester/context. Legacy records have unknown requester.

- New durable events record a four-slot `cli_sessions` map under actor provenance:
  `{codex: string|null, claude: string|null, gemini: string|null, controller: null}`.
  Describe these as caller-supplied/observed identifiers, not authentication or provider IDs.
- Explicit CLI origin arguments must support all three clients without invented runtime
  environment names. Required public flags: `--cli codex|claude|gemini --cli-session ID`,
  before subcommand. Pair required. IDs must match ASCII `[A-Za-z0-9][A-Za-z0-9._:-]{0,127}`
  exactly (1–128 ASCII characters/bytes); no trimming, case folding or other normalization.
  An explicit pair overrides ambient detection entirely, including invalid ambient values.
  Without explicit origin, read Codex's observed CODEX_THREAD_ID (fallback CODEX_SESSION_ID;
  present empty/malformed values refuse; two present unequal values refuse by exact string
  comparison). Both environment keys absent means all null. Never reuse a
  session's opening origin as the caller of later operations. No transcript file contents,
  credentials or unknown environment values are read for provenance.
- A direct callable store API without origin records unknown (all null); CLI resolves and
  passes provenance into the vault/ledger. Copy/freeze map values to prevent mutation leaks.
- Keep existing ledgers readable and original bytes/hashes untouched. Explicitly validate
  legacy actor shape and new extended shape (or version new events if compatibility requires).
  Invalid extra keys/types, populated controller and malformed IDs refuse.
- Every new reply/http/interpret/disposition records its actual caller context. The preparing
  agent and later operator can differ; their linked events retain both without pretending the
  operator's terminal is the originating agent. Unknown is null, not an invented identifier.
- `ref` identifies the existing saved response event and exposes that event's origin, even
  when queried by another CLI. Exact new public field: `actor`, a copy of the selected stored
  event's actor object. For legacy events return the exact legacy actor shape with no invented
  fields; consumers interpret absent requester/CLI map as unknown. Never rewrite old events
  to normalize them. `show` retains full events. Explicit selections already embed
  complete source events, so reused observations keep original IDs/provenance. New consumer
  events retain their own caller. No new automatic response cache in this increment.
- A future response-cache entry must point to original ledger/session/request/reply event ID
  and preserve original provenance; never relabel a cache hit as a new provider observation.
- Shell invocation must pass explicit origin arguments correctly for attached/unattached
  open/help/selected operations; do not weaken selector ambiguity checks or the send guard.

Acceptance: old ledger replay; new null and each explicit CLI origin; auto Codex and override;
invalid/conflicting origins; hlm through Codex, unknown requester, independent requester and
CLI origin; cross-client prepare/reply/ref without relabelling; selection
retains source provenance; mocked send records origin; shell paths; unchanged prior tests.
No paid/provider/account operation. Parent owns integration, STATUS and scoped activation.
