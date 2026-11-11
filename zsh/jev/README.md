# Jev vault and shell

Jev freezes typed judgment packets and preserves observations, interpretations, consumer
choices and later outcomes in private append-only session records. Advice never executes
commands or authorizes another inference. Python uses the standard library; Linux `flock`
coordinates local processes. Control-panel convention: `zsh/AGENTS.md`, one keyboard of
aliases, bodies in the scope engine, `base.zsh` as the silent signpost.

Automated tests use synthetic amounts, keys and replies. They establish offline behavior;
live access, allowance, billing and usefulness require separate per-engagement evidence.
Provider mapping, checked documentation and transport limits: [PROVIDER.md](PROVIDER.md).

## Explicit session binding

Every selected operation needs global selectors **before** its subcommand. Python never
reads an ambient current session. Importing modules, help, absent-vault reads and invalid
opening bindings create no runtime directories. Opening is the first creation operation.
The root's parent must exist; managed roots/directories must be owned 0700, files 0600.
Existing insecure paths, symlinks and multiply linked files refuse without changing modes.

```sh
python3 zsh/jev/jev.py --root /private/test-vault open \
  --project /existing/project --bed /existing/project/work-bed
python3 zsh/jev/jev.py --root /private/test-vault \
  --session SESSION --channel main settings
```

`open` returns the session ID. One canonical project/bed binding has one stable ledger and
lock, including across simultaneous opens. Reopening requires the same immutable opening
settings. Budget omitted means UNSET; model omitted permits offline work only. An explicit
`--model ID` freezes that model and optional repeated `--allow-model ID` entries. There is
no policy edit, refill, budget reset or automatic second engagement for the same bed.

Source `base.zsh` for the `jev`, `jev-use ROOT SESSION [main]` and `jev-off` shell controls.
Attachment validates settings before changing shell variables. Failed attachment preserves
the prior binding. `jev-off` affects only this shell. Attached `jev` supplies explicit
selectors and refuses selector overrides; detach first to select explicitly. `jev open`
and help remain available without attachment. Sourcing is silent and creates no vault.

## Calling CLI and requester provenance

Each new event records this extended actor shape:

```json
{"source":"record","name":"jev","cli_sessions":{"codex":null,"claude":null,"gemini":null,"controller":null},"requester":null}
```

These are caller-supplied or observed CLI session identifiers, separate from Jev's session,
channel, request and provider IDs. They are not authentication. The controller slot is
reserved and must remain null. Use paired global flags before the subcommand:

```sh
jev --cli codex --cli-session Actual.CLI:Session-1 --requester hlm prepare packet.json
jev --cli claude --cli-session Actual.Claude.Session import-reply REQUEST reply.json
jev --cli gemini --cli-session Actual.Gemini.Session ref REQUEST
```

`--requester hlm|agent` independently describes who originated the operation; omitted means
unknown/null. A human task submitted through Codex can be `hlm` with a Codex CLI ID. Neither
a terminal nor a CLI brand implies requester. This declaration grants no paid-send authority.

CLI IDs must match ASCII `[A-Za-z0-9][A-Za-z0-9._:-]{0,127}` exactly: 1–128 characters,
without trimming or case folding. An explicit `--cli`/`--cli-session` pair overrides ambient
origin detection entirely, even malformed/conflicting ambient values. Without the pair,
the CLI uses observed `CODEX_THREAD_ID`, falling back to `CODEX_SESSION_ID`. Present empty
or malformed values refuse; if both keys are present they must be exactly equal. Both absent
means all slots null. No Claude/Gemini environment names are invented or transcript files
read. Some child runtimes have been observed supplying unequal Codex keys; they fail closed
and can supply the actual intended CLI ID explicitly. Do not silently choose one conflicting
value. Shell open/help and attached operations accept the same origin flags.

The callable `store.Vault(root, cli_sessions=MAP, requester=VALUE)` copies and validates the
map; omission always records unknown, regardless of environment. Every invocation uses its
actual supplied/detected caller, never the session opener's origin. Existing legacy actors
`{"source":"record","name":"jev"}` replay without rewriting bytes or hashes. `ref.actor`
is a copy of the selected saved event's exact actor, including that legacy shape; it never
substitutes the querying client's actor. Missing legacy fields mean unknown to readers.

### Reading views and Markdown support

The local `reader.py` and `jev-browse` render event strings in escaped HTML `<pre>`
blocks, with controls made visible. The source text remains data, including markup and
backticks; the output is a derived view. The checked Markdown configuration is
Python-Markdown 3.10.3 with default settings or the `fenced_code` extension, with raw
HTML enabled. Renderers that remove or alter HTML, and other Markdown engines, have not
been verified. Python-Markdown is needed only for the renderer regression tests; the
reader itself uses the Python standard library.
Explicit selections embed original source events with their IDs and provenance; subsequent
consumer events carry their own actor. A future response-cache entry must point to the
original ledger/session/request/reply event ID and preserve that actor, rather than present
reuse as a fresh provider observation. This increment adds no automatic response cache.

## Local operations

The following examples assume the shell is attached. Direct Python accepts the same verbs.
Input JSON is at most 1 MiB; packet/question semantics are defined in `kernel.py`.

```sh
jev prepare packet.json
jev import-reply REQUEST reply.json
jev interpret REQUEST QUESTION policy.json
jev dispose REQUEST use --consumer codex --reason 'checked independently'
jev dispose REQUEST reconsider --consumer operator --reason 'new evidence'
jev outcome REQUEST later-adjudication.json
jev show --request REQUEST
jev ref REQUEST
```

Preparation requires the packet's exact session/channel. It saves the canonical packet,
occurrence ID and hashes, source-file diagnostic, and exact provider body when a model was
configured. Later edits to source files cannot change it. Imported replies are always
labelled **synthetic**, including malformed UTF-8/JSON and invalid typed answers; original
bytes are retained in base64 with their hash. Import never settles a real attempt. A request
has one terminal receipt; deliberate repetition needs a new preparation, optionally lineage.

Interpretation preserves the selected receipt, question and explicit policy, including
ERROR events for unreadable/invalid policies or missing/invalid observations. Noul policies
are `{id,version,low,high}` and produce NO, UNCERTAIN or YES using inclusive thresholds.
An error is distinct from uncertainty. Dispositions append consumer choices independently;
outcome files are separate JSON objects, with optional same-session event IDs in `refs`.

`show` returns immutable events and tail diagnostics. `ref` identifies the retained reply
when present, otherwise the preparation: exact ledger path, hash event ID, sequence and
kind, plus the preparation ID and stored `actor`. Sequence is an aid, not an unverified mutable line reference.

`memory FILE` takes `{version,author,text,refs}`; `refs` are earlier same-session event IDs.
Select the note explicitly with `prepare --memory EVENT_ID`. Existing packet memory remains
explicit input; the latest saved note is never automatically injected.

`select FILE` freezes `{policy:{id,version},items:[{event_id,excerpt}],labels?,layers?}`.
Items may also carry labels/layers. Every excerpt must occur in the canonical source event.
`prepare --selection EVENT_ID` freezes the ordered manifest and complete source events in
`state.jev_selection`. That state key is reserved when selecting a manifest. Sorting and
layering are explicit derived choices, never changes to chronological evidence.

`prepare --lineage FILE` takes `{branch,step,parent_request_ids}` with optional `retry_of`
or `reconsider_of` and a required nonempty `reason` for either link. Links resolve only to
prior requests in this session. There is no scheduler, automatic ranking or response cache.

## Durability and recovery

The ledger is the only state authority. All writes hold a stable engagement lock, replay
and validate the entire bounded ledger, append canonical hashed events and fsync before
success. Locks are never unlinked. Contention waits at most two seconds and then returns a
controlled busy error. Lookup and full send both respect the same locks. Hashes establish
local consistency; a same-user process can forge data and these checks are not authentication.

Events use `jev.event/v1`, event hash ID, sequence, timestamp, session/channel/request,
kind, actor, data and previous ID. `actor.source` is `record`; `data.certainty` scopes the
recorded claim: local durable transitions confirmed, HTTP/reply content observed,
interpretations inferred, uncertain completion unknown. Observed content is not certified
truth. Frozen provider bytes and parsed receipts are checked against saved packet/raw data;
settlements must agree with the independently extracted supported billed amount.

Readers expose a valid prefix plus an incomplete-tail diagnostic. Writes refuse until
`reconcile`. A completely valid final event missing only LF is completed by append+fsync
of that LF; no subsequent audit event is required. Malformed trailing bytes are preserved
exactly, followed by a canonical recovery event with offset, length, SHA-256 and verified
prefix. That forensic file is consequently not always ordinary strict JSONL. Only the exact
fragment paired with its adjacent valid recovery is skipped during replay. Middle corruption,
unproven/interrupted recovery, unknown schemas and impossible transitions fail closed.
A malformed fragment's unknown meaning remains an `UNKNOWN_FRAGMENT` budget liability:
forensic recovery restores local history access but cannot establish remote completion or
permit another send. LF-only completion adds no such liability.

## Spend boundary

A preparation may freeze `--upper-bound USD --bound-evidence TEXT`. This declares a
conservative bound with its provenance; it is not a price estimate or evidence of a provider
ceiling. USD uses exact nonnegative decimal strings with at most 18 integer and 18 fractional
digits, no exponent notation, booleans or nonfinite values. Accounting uses sufficient
precision to preserve all supported digits. Unsupported provider cost precision/range is
unknown and blocks spending, with raw evidence retained.

Manual `send REQUEST --credential-file PATH` is operator-terminal only. Production entry rejects
known agent/tool environments and noninteractive callers before credential access. It shows
the complete saved payload, endpoint, method, nonsecret headers, policy, bound, budget and
approval hash, and requests the first twelve hash characters on `/dev/tty`. Every manual request
needs a fresh manual confirmation; there is no yes flag or reusable manual approval file. The lock covers
review, fsynced reservation/attempt, credential read, exactly one transport and settlement.
Cancellation reads no credential. A crash after attempt leaves a blocking liability.

The supplied credential file must be owned regular nonsymlink 0600, unlinked elsewhere,
nonempty and at most 4096 bytes. Manual mode uses no ambient API key. There is no credential manager
or encrypted wallet in this build. Transport exception strings are never retained or shown;
a response containing the literal credential or one exposed by JSON decoding is withheld
and marked unknown to prevent a secret leak. This checks the actual JSON decoding path;
it is not universal redaction of arbitrary encodings. Other raw HTTP bodies/status are persisted before interpretation. There are
no redirects, retries, environment proxies, model fallback or reserialization after approval.

Admission requires known allowance/liabilities and `spent + reserved + upper_bound <= total`.
A valid billed cost on 2xx settles even invalid advice or an unallowed model. Missing,
untrusted or unsupported cost and transport uncertainty keep liabilities and block subsequent
sends. Non-2xx cost is untrusted. Actual overruns are retained without clamping and block
future sends. Synthetic replies cannot release reservations; no command automatically
reconciles unknown remote completion.

### One-use delegated transcript audit

For the individually authorized November 5 transcript audit, a native alternative accepts
an explicit one-use grant instead of manual terminal confirmation:

```sh
jev send REQUEST --authorization-file /private/one-use-grant.json --credential-env JEV_ORAK_KEY
```

This is an operator-authorized mode, not a test override. Possessing the command grants no
standing permission for future calls. There is no automatic grant issuer or generic yes/
skip-guard flag. Future grants require new actual operator authorization. Manual mode keeps
its existing agent/tool and interactive-terminal guard. Mixed or incomplete modes refuse.

The controller supplies an owned, regular nonsymlink single-link 0600 grant file, at most
16 KiB. It must contain exactly the fields of `jev.send-grant/v1`: `schema`, `root`,
`session_id`, `request_id`, `approval_sha256`, `max_cost_usd`, `credential_env`, `authorized_by`,
`authorization_ref`, `expires_at`. Root/session/request and the recomputed current approval
must match the saved preparation. The positive grant amount must equal the frozen upper
bound and be at most 0.02 USD; the engagement allowance must also be at most 0.02 USD.
Amounts retain their supplied exact decimal representation; equality is monetary equality.
`credential_env` is exactly `JEV_ORAK_KEY`; `authorized_by` is exactly `hlm`.
`authorization_ref` identifies observed operator approval: 1–2048 ASCII bytes in 0x20..0x7e,
with at least one non-space character, retained without trimming or normalization.
`expires_at` is a timezone-aware ISO timestamp in the future at invocation.

Under the existing lock, valid grant consumption is an append/fsync of the attempt with
`authorization: {grant: FULL_GRANT, grant_sha256: CANONICAL_SHA256}`. The attempt is the
one-use record, never removed or reset. Invalid grants leave no attempt and read no
credential. Replay validates the proof and expiry against the attempt's event time, so a
legitimate old attempt remains readable after grant expiry. Old attempts without proof
remain valid. Grant identifiers are controller-recorded authority, not cryptographic human
authentication; same-user forgery remains outside this cooperative boundary.

Only after durable consumption does delegated mode read the explicitly named environment
value, in memory: exactly 1–4096 ASCII bytes, each 0x21..0x7e, no whitespace/newline stripping.
No other environment key, alias or fallback is accepted. No credential is placed in grant,
argv, ledger or output. A missing/invalid credential, transport failure or interrupted attempt
still consumes this request and retains its liability. A second invocation, reused grant
for another request, concurrent send or automatic retry cannot obtain another call from
that authorization. Both modes share the same exact saved-byte transport, receipt retention,
secret-echo protection, settlement, overrun and unknown-cost behavior described above.

Offline tests inject confirmation, dummy credential, transport and guard through the callable
`send` seam. The CLI exposes none of those test overrides; its delegated mode validates real grant evidence. Production guards are cooperative and
same-user, not an authentication boundary. Live pilot approval, an actual allowance/provider
backstop and one individually approved mixed-type request remain separate gates.

Run the offline suite from the repository root:

```sh
python3 -B -m unittest discover -s .dev/session/jev-01-codex-pilot/tests -p 'test_*.py' -v
```

If a test runner inherits conflicting Codex keys, isolate only those provenance inputs for
the offline suite (provenance-specific tests supply their own positive and negative inputs):

```sh
env -u CODEX_THREAD_ID -u CODEX_SESSION_ID python3 -B -m unittest discover \
  -s .dev/session/jev-01-codex-pilot/tests -p 'test_*.py' -v
```
