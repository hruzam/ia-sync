# Jev 01 — current build design

Cartan · 2026-11-03 · working engineering decisions under majkee's delegated judgment.
STATUS owns progress. RUNBOOK owns the unchanged final gate. This document supersedes
the October 27 proposal and subsequent channel notes as the current design; those remain
historical evidence. A working choice here is not a claim that majkee ticked an old sheet.

## Authority and immediate scope

Majkee's November 3 instruction:

> I left oraculum(nabla-lab) to make research about jev usage as additional help, maybe you can find there something usefull. If this will lead to another gavel looping and bureocratic exchange, than I rather go by picking any solution to move, by your own judgement, I will only check little.

Cartan interprets this as authority to settle reversible engineering choices and advance
offline construction after the independent technical review required by prompt-0. It
supersedes our stricter STATUS hold that demanded a real USD amount before any construction.
It does not grant spending, credential access, deployment, promotion, or final pilot GO.
No historical operator answer is rewritten. No additional human design questionnaire is needed.

The first construction slice is a local, offline judgment kernel with a CLI, synthetic
fixtures and tests. It freezes a case/question/memory packet, validates imported synthetic
receipts, and reports a typed interpretation. It has no network, credentials, runtime store,
budget mutation or action execution. The durable session ledger and provider adapter follow
as separate implementation slices against the boundaries below, without routine re-gavelling.

## Selected shape

```text
engagement: one project + one work bed + one cumulative allowance
  Jev session: one durable record for that engagement
    channel main: local continuity stream, usable from several CLIs
      iteration: frozen input → attempt → raw receipt → validation
                                          → interpretation → disposition/outcome
```

`channel` is the operator's stream meaning. It is neither the provider model nor the CLI
conversation. Start with one named stream `main`; retain its ID in every request. Require
explicit session/channel selection. A future second stream shares the same allowance.
Use `jev` for the executable and `belnap` only for a versioned question protocol, no persona.
The first practical protocols are `brief-check/v1` (U01) and `claim-support/v1` (U02).
Keep Python standard-library code in this bed's `impl/` with `tests/`. Later source promotion
to `ia-sync/zsh/jev/` remains separate from installing or using the pilot.

## What the research changes

Source: Oraculum's [implementer brief](/home/hruzam/nabla-lab/publications/inner-circle/jev-usage/implementer-brief.md),
[usage atlas](/home/hruzam/nabla-lab/publications/inner-circle/jev-usage/usage-atlas.md),
[study §2–3](/home/hruzam/nabla-lab/publications/inner-circle/jev-usage/study.md) and
[E2 experiment](/home/hruzam/nabla-lab/publications/inner-circle/jev-usage/experiments.md).
The [source directory](/home/hruzam/nabla-lab/session/research-jev-usage/sources.md) records
its checks and limits. Research file hashes are in `raw/research-intake-before.2026-11-03.json`.
This intake checks the local publications; it does not reproduce their public-source audit.

| Adopt now | Concrete consequence |
|---|---|
| Brief omissions and bounded claim support first | Synthetic examples cover a missing constraint, supported claim, contradiction, and missing source. No model-tier recommendation as ground truth. |
| Frozen evidence and versioned semantics | Keep case ID, evidence text/reference/hash, missingness, question wording/options/rubric and protocol version. |
| Observation separate from interpretation | Preserve provider output before validating; record interpretation policy/version separately. Never turn an invalid receipt into an uncertainty probability. |
| Outcome separate from disposition | `use` records a consumer choice; later independently assessed correctness is a separate, superseding observation. |
| Batch only questions already defined over the same evidence | A follow-up that depends on an answer is a new preparation with lineage. Shared state does not imply independent errors. |
| Measure added usefulness | Compare against a deterministic checklist/quote check and a second review; count material defects, false alarms and review effort. Passing plumbing is not evidence of usefulness. |

Coin/rotation, coalition acquisition, experimental images/Box, semantic caches, vector stores,
automatic memory rewriting and generic workflow engines are outside this first build. They
remain possible consumers of the small interface, not prerequisites. E0 coalition fixtures
are required if that separate interpreter is built, not for a plain U01/U02 judgment kernel.

## Memory and IF

History is the immutable source. A small human/head-authored stream note is an explicit
reading aid with version, author, text and source references. Preparation freezes the selected
note in full with its hash; later edits do not alter the packet. No automatic history ingestion
or summarization, no automatic trust upgrade for previous advice. Saved reply inspection is
enough reuse initially; do not claim fresh inference when showing old output.

Code owns the conditional. The model supplies a typed observation. For Noul, a supplied
versioned rule with `0 <= low < high <= 1` yields NO at `p <= low`, YES at `p >= high`,
otherwise UNCERTAIN. Without a rule, no Boolean decision is produced. Example thresholds in
tests are synthetic only; no operationally calibrated threshold is selected. Invalid input
is ERROR, distinct from a valid uncertain judgment. For Choice retain the selected category
and distribution; `insufficient` is a semantic option, not a transport failure. Score retains
its ordered rubric/distribution and weighted value. Confidence is never action permission.
No interpreter runs commands, loops, chooses another paid call or grants authority.

## First slice: exact offline contract

Use a clearly labelled internal format, **not an OpenRouter wire-schema claim**. The later
provider adapter must map current provider evidence to it and preserve the original bytes.

- Input packet `jev.case/v1`: `case_id`, `target` (what is being assessed),
  `related_case_group` (shared underlying case, including paraphrases; an isolated case uses
  its own case ID), `session_id`, `channel` (only `main` in this slice),
  `protocol` (`id`, `version`), `state` (JSON object), `evidence` (list of `id`, `ref`, `text`),
  `missing_evidence` (list of strings), `questions` (nonempty list), and optional `memory`
  (`version`, `author`, `text`, `refs`). All identifiers/text metadata are nonempty strings;
  evidence text and state may be empty to model missing context explicitly. Duplicate evidence
  and question IDs refuse. Keep expected labels in separate test files, never in the input.
- Question: `id`, `type` (`choice`, `noul`, `score`), `text`, `rubric_version`,
  `predicate_meaning` (stable statement of what the observation is intended to measure).
  Target, group and predicate meaning are required nonempty strings, frozen in the packet;
  no missingness default or assumption of statistical independence is inferred from a group ID.
  Choice additionally has `options` (at least two unique nonempty strings). Score has `levels`
  (at least two unique nonempty descriptions, indexed 0..n-1). Noul has neither. Reject
  unknown schema fields, wrong types, nonfinite values, booleans posing as numbers, and
  duplicate JSON object keys. Arbitrary JSON inside `state` remains allowed, subject to
  finite numbers and bounded input. No flattening of conflict into missingness.
- `prepare`: validate, canonicalize with Python JSON (`sort_keys=True`, compact separators,
  UTF-8, `ensure_ascii=False`, `allow_nan=False`); return `jev.prepared/v1` containing the
  complete packet, SHA-256 of those exact canonical packet bytes, per-evidence text hashes,
  optional memory hash, and an independent random occurrence ID. Equal packets give equal
  content hashes and different occurrence IDs. Retain no hidden ambient/default session.
- Internal receipt `jev.receipt/v1`: `request_id`, `packet_sha256`, `model`, `answers` list.
  Both correlation fields must match the prepared object. Every requested question has exactly
  one answer; no extra/missing names. Answer fields: `id`, `type`, plus Noul `probability`,
  Choice `value` and `probabilities` (keys exactly options), or Score `value` and
  `probabilities` (keys exactly stringified indices). Optional `confidence` is allowed only
  on Choice/Score, finite within [0,1]; it is retained as a supplied statistic, not recomputed
  or advertised as calibrated. No probability normalization or repair. Choice value must be
  a maximizer within 1e-6; Score value agrees with weighted index within
  `1e-6 * max(1, n-1)`; probability sums within 1e-6 of 1 and every value in [0,1].
- `check`: revalidate the entire prepared object and its derived hashes before use; validate
  imported receipt against it. Output structured VALID/INVALID plus precise errors and the
  original imported receipt for valid JSON, including semantically invalid content. Bad JSON
  yields a parse error; it never becomes a fake observation. All commands are read-only with
  respect to input files and output JSON to stdout. Bound each input file to 1 MiB and each
  packet to 20 questions; reject oversized input before parsing. No `~/.jev` defaults.
- `interpret`: validate first; for a selected Noul question apply an explicitly supplied
  threshold policy (`id`, `version`, `low`, `high`). Emit YES/NO/UNCERTAIN or ERROR with policy,
  question and request references. Invalid receipt/policy refuses interpretation; no action.
  Threshold equality follows the inclusive boundaries above.
- Commands: `python3 impl/jev.py prepare PACKET`, `check PREPARED RECEIPT`,
  `interpret PREPARED RECEIPT QUESTION POLICY`. Invalid data exits nonzero with JSON error;
  UNCERTAIN is a valid result and exits zero. These names only become working interfaces
  when implementation and tests exist. Examples use temporary files, not a live runtime root.

Tests must cover malformed/duplicate/nonfinite JSON, wrong/missing/extra answer IDs/types,
probability sums/ranges, score consistency, ties, correlation mismatch, tampered prepared
objects, missing/invalid target/group/predicate meaning, repeated occurrence identity,
memory/input/semantic-field freezing, maximum input bounds, explicit
threshold boundaries and uncertainty/error separation. Use malicious-looking state text to
show it stays data. All test receipts must be labelled synthetic; no provider success claim.

## Following slices: durable lifecycle and real adapter

These boundaries are selected, but their exact schemas need a bounded technical review at
implementation, not another user questionnaire. No unfinished slice is described as shipped.

Runtime home: private `~/.jev/projects/<name>-<root-hash>/`, with one session JSONL ledger,
editable buffer and stable lock. Verify full canonical root/bed identities; under an
engagement creation lock, refuse a second session that would mint another allowance.
0700 directories, 0600 files; temporary roots only during offline development. Append-only
events carry schema/event ID/sequence/time/session/request/channel/actor/data; event hashes
check consistency, not authenticity. Retain `actor.source: record` and scoped certainty.
Opening freezes identity/policy. Request IDs are occurrences; content hashes do not deduplicate
intentional repeats. Parent/reconsider/retry links resolve within the same session.

Adopt complete-send lock and fsync before transport. A complete valid event lacking LF can
be completed under explicit recovery. Malformed trailing bytes are preserved and may be
quarantined only by a verified recovery record; forensic storage is then not ordinary strict
JSONL. Mid-file corruption blocks. Readers label partial/unknown state; recovery never sends.
Persist raw receipts, validation, interpretation, consumer dispositions and later outcomes
separately. `show/ref/use/skip/reconsider` are local operations with no automatic actions.

Majkee's follow-up requires continuity suitable for later stair/cascade/wandering experiments.
The durable layer must record operations automatically through the common CLI/library path;
manual stdout redirection is only the current kernel's interface, not the persistence design.
Keep chronological source events unchanged. Sorting/layering belongs in rebuildable derived
views with explicit selection/ranking policy versions. A prepared next-loop packet freezes
the exact selected event references, ordering, excerpts and memory version, so later reranking
cannot rewrite what an earlier iteration saw. Preserve branch/step and dependency references
in the lifecycle schema; do not implement a generic loop scheduler merely to retain lineage.
Historical observations remain observations, including conflicting or rejected results.
Automatic response reuse is separate and still deferred: a future cache hit must identify
the reused occurrence, and experiments requesting a fresh sample must bypass reuse. Neither
recording nor ranking authorizes another paid call. No optimal selection policy is established.

USD total remains UNSET and all paid sends refuse. Offline ledger tests use explicit synthetic
amounts. Use Decimal, `settled + outstanding + candidate_upper_bound <= authorized_total`,
with no unknown liabilities, under the engagement lock. Freeze the upper-bound evidence.
Unknown outcome/cost halts; invalid advice may still cost money; record overrun without
clamping. No top-up, reset or new channel can replenish the total. Local accounting alone
cannot establish a hard provider ceiling. Real budget/backstop/credential handling belongs
immediately before live readiness, when evidence and a concrete payload are available.

Provider adapter: OpenRouter Decisions, text Choice/Noul/Score. Verify its current schema,
resolved model policy, pricing and cost evidence before building the network slice. Preserve
frozen method/endpoint/non-auth headers/body bytes and full approval hash. No fallback,
redirect or hidden retry. Only an individually confirmed human-terminal send is proposed;
reject known agent contexts/noninteractive calls before touching credentials. Same-user
checks are cooperative, not an authentication boundary. No exported-key fallback.

## Documentation and completion

This file is the single current build design. First-slice usage/reference belongs beside
`impl/`; later exact engine docs stay beside source. An enduring machine-workflow guide can
eventually live at `~/reposoma/raw.guides/jev/GUIDE.md` with one editable authority, after
actual reusable behavior exists. No global guide, germline program, agent or hook is needed
to build this pilot. Preserve Houston's consult and correction as evidence, not duplicate law.

Full completion still requires the RUNBOOK's recovered durable records, tested USD admission,
explicit settings/channel binding, distinct Codex/shell dispositions, current live preparation,
one individually approved mixed-type request, independent verification and majkee's final GO.
The U01/U02 usefulness comparison is a separate measured follow-up; its sample size and live
budget are not invented here. Readiness of the offline kernel proves neither endpoint access
nor usefulness. Cartan owns integration and STATUS throughout.
