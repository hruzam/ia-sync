# Jev OpenRouter adapter

`provider.py` implements the provider interface in
`../../.dev/session/jev-01-codex-pilot/BUILD.md`. It imports sibling `kernel.py` and performs
no I/O at import. Store, confirmation, credential-file checks, durable attempt/reservation
and settlement belong to the calling vault implementation. Calling `post` directly bypasses
that caller policy; this helper is neither authentication nor spending authorization.

## Primary evidence checked 2026-11-04

[OpenRouter Decisions reference](https://openrouter.ai/docs/api/api-reference/alphadecisions/submit-a-decisions-request)
defines the fixed POST endpoint `https://openrouter.ai/api/alpha/decisions`, body fields
`model`, keyed `questions`, `state`, and optional `provider` routing preferences. The response
uses keyed `answers`, `model`, `usage`, and optional `id`/`provider`; its example reports
numeric `usage.cost`. This alpha interface may change. Direct TypeSafe response envelopes
are not the OpenRouter contract.

[TypeSafe Noul](https://docs.typesafe.ai/primitives/noul) documents an instructions question
and a `noul` probability, with no separate confidence. This adapter omits optional true/false
criteria because the packet does not supply them.

[TypeSafe Choice](https://docs.typesafe.ai/primitives/choice) documents named criteria,
`choice`, per-option `probabilities` and `confidence`, with up to 255 options. Packet options
are both keys and descriptions; the adapter invents no extra descriptions.

[TypeSafe Score](https://docs.typesafe.ai/primitives/score) documents ordered criteria,
`score`, `legend`, `probabilities` and `confidence`, with 2–10 levels. The adapter checks the
returned string-indexed legend against the complete frozen rubric.

## Exact local choices

`ADAPTER_VERSION` is `jev.openrouter-decisions/v1`. `build_request(packet, model)` validates
the kernel packet, pins the supplied model string, maps each exact question text to
`instructions`, and sets `provider.allow_fallbacks` false. The full packet is the provider
`state`: evidence, memory, missingness, user state, protocol, target, group, question semantics
and session metadata all travel. This is an explicit local mapping, not a claim that the
provider treats metadata as instructions. No ambient context is added. Provider size/count
limits can reject a packet that the broader offline kernel accepts.

The returned bytes use kernel canonical JSON and are bounded to 1 MiB. Save and review these
exact bytes; the transport never reserializes them. Nonsecret semantic headers are exported
as `HEADERS` (`Content-Type: application/json`, `Accept: application/json`). The HTTP library
supplies fixed-host framing, including Host, Content-Length and Accept-Encoding: identity.

`parse_response(prepared, raw_bytes, allowed_models)` leaves caller-owned raw bytes untouched.
It checks exact answer names/fields/types, explicit allowed response models, Score legend,
and the kernel's probability/range/weighted-score rules. Choice and Score require supplied
confidence. No normalization or confidence calibration is performed. A mapped receipt may
remain present with INVALID validation; failed wire mapping leaves it null. Local request ID
and packet hash are assigned from the validated preparation, not authenticated remote echoes.
`provider_id` means response `id` (generation ID); the provider label remains in raw bytes.

Cost is parsed independently with Decimal from the original JSON numeric token; integer zero
is valid. Missing, negative, boolean, string or nonfinite cost remains null. Advice may be
VALID with unknown cost, or INVALID with known cost. Duplicate keys, malformed/nonfinite JSON
constants and oversized bodies prevent trusting the body. No zero is invented. Decimal strings
may use exponent spelling. The caller must check HTTP status before trusting cost; this helper
cannot determine remote billing from an error body or recover an uncertain completion.

`post(body_bytes, key, timeout=30, max_bytes=1048576)` sends once using verified HTTPS directly
to the fixed host/path. It reads at most `max_bytes + 1`, closes the connection, returns the
status and unmodified response body, and follows no redirect. It reads no credential file or
environment key and uses no environment proxy, retry, fallback or alternate endpoint. Errors
are bounded generic `ProviderError` messages; transport exception text is discarded. Timeout
is the HTTP socket timeout, not a wall-clock deadline for an arbitrarily slow peer. The caller
must retain unknown liability on any oversized response or transport failure.

## Offline proof and limits

Run `python3 -B -m unittest discover -s .dev/session/jev-01-codex-pilot/tests -p test_provider.py -v`
from the repository. Fixtures are synthetic adaptations of the internal brief packet, not
captured successful provider calls. Tests mock HTTPSConnection and cover exact bytes, verified
TLS context, no proxy routing/redirect/retry, bounded responses, safe errors, mixed mappings,
strict schemas, immutable input, model policy and Decimal cost independent of advice validity.

No account access, endpoint availability, resolved model availability, pricing, server-side
spending ceiling, billing correctness, real credentials, real HTTP inference, calibration or
usefulness was tested. Network/live-pilot approval and independent integration verification
remain separate gates.
