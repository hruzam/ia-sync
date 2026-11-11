# Jev offline kernel

This first slice freezes an explicit evidence/question/memory packet and validates an
imported reply. It uses a versioned internal JSON schema from [DESIGN](../DESIGN.md).
All example judgments are synthetic fixtures; this code makes no model call.

Run from `.dev/session/jev-01-codex-pilot/`:

```bash
python3 -B impl/jev.py prepare tests/fixtures/brief-missing.json
python3 -B -m unittest discover -s tests -v
```

`prepare` prints a complete `jev.prepared/v1` JSON object. Save stdout to your chosen
temporary file. `request_id` identifies this occurrence; `packet_sha256` identifies the
canonical packet bytes. Repeating identical input creates another occurrence with the same
content hash. The object contains a frozen copy of evidence and optional explicit memory.

To check a receipt with that occurrence's exact `request_id` and `packet_sha256`:

```text
python3 -B impl/jev.py check PREPARED.json RECEIPT.json
python3 -B impl/jev.py interpret PREPARED.json RECEIPT.json missing tests/fixtures/policy.json
```

`tests/fixtures/expected.json` contains synthetic answers, kept outside input packets. A
receipt has `schema: jev.receipt/v1`, the two correlation fields, `model`, and `answers`.
The four case fixtures cover a brief missing constraints and a claim supported, refuted,
or unsupported by the supplied evidence. Labels describe these synthetic examples only.

`check` returns VALID or INVALID and retains the imported JSON receipt, including semantic
errors. Parsing errors return ERROR. `interpret` requires a valid Noul answer and an explicit
policy (`id`, `version`, `low`, `high`): `p <= low` gives NO, `p >= high` gives YES, and
the interval between gives UNCERTAIN. The example thresholds are test values, with no
calibration claim. Interpretation preserves the request/question/policy references. On ERROR,
it also records input-file pointers and validation labels. Request references are populated
only after prepared-object schema/hash checks pass; missing, unparseable or schema/hash-invalid prepared
inputs leave them null. A parsed policy on an error is explicitly UNVALIDATED. These local
checks establish consistency, not authenticity or authority.

Every data refusal exits 2 with JSON errors on stdout; VALID, YES, NO and UNCERTAIN exit 0.
`--help` prints ordinary CLI help. Inputs are read-only; each input file is limited to 1 MiB
and a packet to 20 questions. The prepared object must also fit 1 MiB including metadata.
Unknown fields, duplicate JSON keys, invalid numbers, correlation/hash mismatches and
inconsistent probability distributions refuse. Confidence is only a supplied statistic.

No send command, provider adapter, credentials, persistent session ledger, USD admission,
automatic memory or action executor exists in this slice. The internal receipt format is
not an OpenRouter response-schema assertion. Later slices must preserve original provider
bytes, add the durable lifecycle, and prove the unchanged RUNBOOK gate separately.
