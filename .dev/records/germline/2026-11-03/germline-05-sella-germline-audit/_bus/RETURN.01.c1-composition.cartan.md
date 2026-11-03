---
point: POINT.01
from: cartan · Composer-01 navigator and STATUS owner
to: flight · Germline-05 head and integration owner
date: 2026-10-20
authority: Majkee's explicit bounded C1 grammar revision/review instruction to Composer-01
position: C1 applied in checked v4; independent native PROCEED; final grammar GO pending
candidate: /home/hruzam/unikuklatrix/nablarva/.dev/session/composer-01-parse/evidence/grammar.builder.v4.md
candidate_sha256: a977682c65bcd6b3c66cc67cb7c2b40a926cf4d96a7f58eb50f1a1fb0839b2ec
---

# RETURN.01 — C1 composition correction

## 1. Files changed

Composer's native Astrobley authored a complete **v4 candidate** and a new literal
unmeasured v4 fixture in Composer-01. Cartan checked that body in cycle 14, then
commissioned a fresh native challenger in cycle 15 and checked its **PROCEED**.
The native reply is preserved verbatim and attributed. This is a grammar review;
no parser implementation or functional acceptance is claimed.

Majkee's direct decision selects **removal from allowed fields**. V4 permits no
optional/list-valued program/function aliases or primary header routing pair.
Agent/program/controller/function selections and their prepared references and
instructions belong in the body. Phase 0 preserves that body as opaque bytes,
apart from its existing active exact closer, without instruction discovery,
loading, resolution, dispatch or execution. Picker notation remains open.

| Affected v4 section | Checked result |
|---|---|
| §§1–2 | Record the operator decision and composed-body boundary; retained from/to/consult metadata grants no selection or dispatch semantics. |
| §5 | Remove program/function from allowed and required sets. Exactly five required fields remain: format, id, from, to, requested_scope. |
| §7 | Revise the valid/empty/insertion examples; add an opaque multiple-selection example. V3 and its old examples remain unchanged historical artifacts. |
| §8 | Well-shaped program/function header lines yield FIELD_INVALID/unknown_key before value/repetition handling. No required_absent for their omission. EOL and line-shape checks still precede key lookup; existing diagnostic code/reason set and sorting remain unchanged. |
| §9 | Add explicit pair-free, body-composition, removed-key and missing-required-field cases; use the new unmeasured fixture and retain all four frozen corpus bodies/extents. |
| §10 | Keep final GO and later decisions open; record the selected removal without designing a picker. |

V4 §§3/4/6, scalar rules, diagnostic code/reason table and four-corpus extent table
are unchanged from v3. Delimiter, nonce, UTF-8/BOM, byte/EOL preservation and the
first exact wrong-EOL closer rule remain intact.

In G05, Cartan wrote **only this RETURN**. Flight's RUNBOOK, STATUS, POINT, findings,
delegates and integration pen remain Flight's. No commit, deployment, installer,
delivery activation or later phase was performed. Composer retains its own STATUS.

## 2. Commands and outcomes

The head ran these checks from the exact composer bed:

```sh
cd /home/hruzam/unikuklatrix/nablarva/.dev/session/composer-01-parse
sha256sum -c SHA256SUMS
sha256sum -c evidence/grammar.builder.v3.sha256
sha256sum -c evidence/grammar.builder.v4.sha256
sha256sum -c evidence/review-packet.janus.2026-10-17.sha256
```

All exited 0: 19 raw entries, v3, v4, and the three frozen Janus packet entries
verified. A before/after file-digest comparison preserved all 83 pre-existing
non-STATUS files in Composer-01; only the authorized head STATUS changed among
the original 84 files. Source-section comparisons and the v3→v4 diff confirmed
the preservation and affected-section claims above.

From the same composer bed:

```sh
git diff --no-index --check /dev/null evidence/grammar.builder.v4.md
git diff --no-index --check /dev/null evidence/fixtures/packet.handwritten.v4.md
git diff --no-index --check /dev/null _bus/14.builder.return.md
```

Each exited 1 with no whitespace diagnostics. RETURN has the six BUS headings.
These are static document checks, not executable parser tests.

The following are **required future acceptance outcomes**, already written in v4:

| Case | Required outcome |
|---|---|
| Five required fields present; no program/function header | Success, with no missing-field finding for the removed keys. |
| Multiple selections, ctrl/&& and program:/function: strings in body | Byte-identical body, no lookup/loading/dispatch/execution; no picker syntax is adopted. |
| Either removed key in a well-shaped header, with scalar/list/empty/malformed value or repeated occurrences | Each occurrence yields FIELD_INVALID/unknown_key; never value-shape, empty-value or duplicate-key substitution. |
| Bad EOL or malformed header line containing a removed key | Existing EOL/line-shape precedence applies before key lookup. |
| Truly empty header between sound opening/body markers | Exactly five FIELD_MISSING/required_absent findings at body-marker start; final sort follows §8. No silent success. |
| Old v3 fixture used as v4 input | Its program/function header lines are rejected as unknown_key; do not rewrite the historical fixture. |
| First exact closer has wrong EOL, later closer has correct EOL | Immediate frame_eol; no scanning fallback. |

The reviewer highlighted the risk of retaining removed keys as optional known
fields. Its proposed future safeguard is one allowed-key classification path and
the conformance matrix above. Cartan checked the cited v4 passages; no material
drafting REVISE/STOP remains. The review grants no implementation authority.

## 3. Evidence paths

- [Controlling Majkee instruction](/home/hruzam/unikuklatrix/nablarva/.dev/session/composer-01-parse/evidence/decision.majkee.c1.2026-10-20.md)
- [Complete checked v4](/home/hruzam/unikuklatrix/nablarva/.dev/session/composer-01-parse/evidence/grammar.builder.v4.md)
- [V4 identity manifest](/home/hruzam/unikuklatrix/nablarva/.dev/session/composer-01-parse/evidence/grammar.builder.v4.sha256)
- [New literal fixture](/home/hruzam/unikuklatrix/nablarva/.dev/session/composer-01-parse/evidence/fixtures/packet.handwritten.v4.md)
- [Builder RETURN](/home/hruzam/unikuklatrix/nablarva/.dev/session/composer-01-parse/_bus/14.builder.return.md) and [Cartan verification](/home/hruzam/unikuklatrix/nablarva/.dev/session/composer-01-parse/_bus/14.cartan.verdict.md)
- [Verbatim independent review](/home/hruzam/unikuklatrix/nablarva/.dev/session/composer-01-parse/evidence/challenge.native-v4.2026-10-20.md) and [checked disposition](/home/hruzam/unikuklatrix/nablarva/.dev/session/composer-01-parse/_bus/15.cartan.verdict.md)
- [Preserved v3](/home/hruzam/unikuklatrix/nablarva/.dev/session/composer-01-parse/evidence/grammar.builder.v3.md), SHA256 `578f01f9f5f01e7121cdcdee224c5259f32c345079e3a0dfe09c9344f56bf91b`

## 4. Mismatches discovered

The POINT changed externally during this run. Both observed versions are preserved
in Composer evidence; Cartan did not edit the G05 POINT:

- [Initial observed POINT](/home/hruzam/unikuklatrix/nablarva/.dev/session/composer-01-parse/evidence/point.flight.c1.2026-10-20.md), SHA256 `a1da1c88505134be0c985779985ed31668593a18875fd7eaf6cd5a2d99c4cd03`.
- [Observed POINT carrying removal direction](/home/hruzam/unikuklatrix/nablarva/.dev/session/composer-01-parse/evidence/point.flight.c1.after-direction.2026-10-20.md), SHA256 `1e1c4355705e9732cf1b8bc3ce4555010afc2c310e1b9ee5f5256eb8043063c7`.

Majkee's direct instruction supersedes the A/B/C options, remaining “removed or
optional” wording, and the unchanged-v3-example condition. Existing examples may
change in the new candidate; their original v3 bytes stay preserved. This resolves
the written C1 constraint without changing the Phase 0 gate.

To answer the newer POINT's identity/diagnostic question: `format` still declares
the proposed wire format `request/0.1`; `id` still identifies the packet and must
be unique within the document. Neither selects a program/function or an operation
type. No new `type` key is introduced. The body carries the composed instructions;
the header still has structured metadata and five required fields. Diagnostics
continue to validate encoding, framing, header syntax, allowed fields and required
fields. “No program/function” therefore does not mean “empty header.”

## 5. Recommended next task

Flight checks this RETURN against the cited candidate/review and records its own
C1 disposition. The remaining Composer decision is **Majkee's final grammar GO or
concrete revision on written v4 at the recorded SHA256**. This recommendation does
not alter either session's STATUS by itself.

## 6. Remaining uncertainty

Final grammar GO has not been given. Code home, stack and independent functional
verifier remain separate Majkee decisions before any implementation assignment.
Picker notation, later composition preparation/rendering and delivery remain open
and unexecuted. No size-cap value is selected. Functional round-trip, diagnostic
and non-execution evidence remains future work. The new fixture is agent-authored
literal text, not a human artifact or independent functional witness.

This file's existence proves availability, not Flight's consumption or acceptance.
The C1 correction/review is complete; no broader execution is released.
