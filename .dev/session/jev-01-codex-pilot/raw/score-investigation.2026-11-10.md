# Saved Score replay — successor investigation

Cartan, office, 2026-11-10. Controller `01a1c4af-1fbe-7301-9f52-654e1a0b8cd3`.
Bounded offline investigation selected by STATUS; no production change or paid call.

## Result

Native replay reproduces INVALID at `receipt.answers[5]` (S2). The retained HTTP and
reply bytes equal the private exported response byte-for-byte. Mapping to the local
receipt preserves the provider values. Exact decimal arithmetic confirms:

| Question | Returned scalar | Weighted returned probabilities | Scalar minus weighted |
|---|---:|---:|---:|
| S1 | 1.16 | 1.16 | 0 |
| S2 | 2 | 2.01 | -0.01 |
| S3 | 2.02 | 2.02 | 0 |
| S4 | 2.95 | 2.96 | -0.01 |
| S6 | 1.78 | 1.77 | +0.01 |

All five returned distributions sum to exactly one. This discrepancy exists in the
wire decimals; replacing Python float parsing with Decimal alone would not remove it.
The native four-level tolerance is 0.000003. The adapter preserves the mismatching values
and independently extracts cost USD0.000420126; accounting settlement is not typed validity.

## Rounding is possible, not established

Under the **hypothetical** rule that probabilities and their unrounded weighted mean
are independently rounded to nearest 0.01, these normalized underlying distributions
would produce the observed scalar/distribution pairs:

| Question | Hypothetical probabilities at levels 0,1,2,3 | Unrounded mean |
|---|---|---:|
| S2 | .013, 0, .957, .030 | 2.004 |
| S4 | .003, 0, .040, .957 | 2.951 |
| S6 | .107, .010, .883, 0 | 1.776 |

The probe checks normalization, bounds, every rounded probability and the rounded mean
using exact Decimal arithmetic. These examples avoid half-way ties. They establish
mathematical feasibility only, not hidden provider values or the cause of the discrepancy.
They address scalar/distribution consistency, not the separate confidence field.

Current official [Score documentation](https://docs.typesafe.ai/primitives/score) and
[SDK response reference](https://docs.typesafe.ai/sdk/python/api/types/responses), checked
November 10, describe the scalar as the probability-weighted level average. Neither inspected
page specifies decimal precision, rounding order or a permitted scalar discrepancy.
The SDK's Choice probability description allows approximate normalization without a numerical
bound; that is not a Score serialization contract. The inspected
[System One API page](https://docs.typesafe.ai/api/system-one) adds no such guarantee.
[OpenRouter's Jev example](https://openrouter.ai/blog/insights/what-is-jev/) explains variation
between calls; that does not explain within-response serialization or authorize a tolerance.
This is a bounded documentation search, not proof that no guarantee exists anywhere.

Keep the original INVALID receipt and fail-closed validator. A change needs provider evidence
for precision, rounding stage, normalization and endpoint/model applicability, followed by
a bounded design and independent tests. Per-question acceptance remains a separate design.
No provider contact was made and no further call is queued.

## Re-entry and research intake

All 11 source/live hashes match the predecessor receipt. Native settings replay confirms
32 events, three replies/settlements, two memory notes; spent USD0.001999830, available
USD0.018000170, no reservation/liability. Ledger and exported response hashes remain unchanged.
Fresh fetch confirms local/upstream 0/0 at 19f36bd. Foreign work is preserved.

Read both Oraculum proposals; canonical calibration protocol hash matches the handoff.
The companion substrate hash is in the probe receipt. Calibration work requires independently
adjudicated atoms, explicit coverage/UNKNOWN semantics, family-level splits, and distinct
coherence/calibration/utility measurements. Proposed fixture counts are not constructed data
or permission to run a study. E1/E2 observer/cache experiments and local model training are
separate proposals; none is added to Jev production scope by this intake. T09/T10 retain their
existing design boundary, with these record requirements available as research input.

## Reproduction and limits

Run `python3 -B .dev/session/jev-01-codex-pilot/raw/score-replay.2026-11-10.py` from this
office checkout. Output: `score-replay.2026-11-10.json`. Private input bodies remain in
their existing host-local homes; the source probe contains paths and derived numbers only.
Native settings needs access to the vault lock; the initial sandbox run refused that open,
then the approved run passed. No ledger write occurred. This focused probe does not claim
a fresh full-suite run, home qualification, general calibration or final pilot GO.

Independent verifier `/root/score_replay_check` returned PASS after direct ledger-byte,
Decimal, provider-parse and all-11-hash checks. Main checked the same cited artifacts.
No failures; provider precision remains the residual uncertainty. Verified probe SHA256
`c3eb3ca9606f8e02695ba7daf1cfdb095b9e5a773fc8ed57cc58587b4fa43598`;
result SHA256 `0fa3cd092efd65783eaccfc5c2b6e770a11b6942aaac5bce0294153ccd803844`.
