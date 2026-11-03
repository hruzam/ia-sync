# Unapplied pin transition required after an approved race correction

The staged patch changes the adapter hash; a matching frozen adapter-test correction would
also change a named A1 input hash. Regenerating `hold-line/sources.json` therefore changes
the manifest hash. Current adapter `compile_packets()` and `current_packet()` reject the
existing `plan.C1.json` once its stored `pins` no longer equal `verify_pins()` (source lines
353–428). The existing `RELEASE.json.source_manifest_sha256` would also no longer match.

Do not rewrite the historical C1 plan or R1/A1 packets. Preserve their current plan hash
`d60bc70f…4d1a3fba`, compiled packets, both completed ask receipts, outputs, bootstrap/
preamble/read receipts, identities, and the two consumed ask attempts exactly as evidence.

If Majkee approves applying the staged patch, Cartan should authorize one atomic correction
transition: preserve `plan.C1.json` as C1 history; rotate source pins; point a newly revised
CONTRACT at a new future-plan path (for R2/A2 compilation only); then update the release's
contract and source-manifest hashes under explicit operator authority. The new future plan
starts empty and must never recreate R1/A1 packets or reservations. Its plan is compiled only
after the named R2/A2 inputs exist. This leaves current C1 evidence self-consistent and keeps
the cumulative target cap at two consumed run-02 asks.

No transition is applied or authorized by this review. A fresh exact authority decision is
required because the recorded GO pins both CONTRACT and source manifest hashes.
