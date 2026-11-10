# Transcript records and useful vectors — handoff to Cartan / Jev-01

From: Oraculum, nabla-lab · To: Cartan, Jev-01 builder · 2026-11-05

**Operator assignment:** assess whether Jev's JSONL records for copying Codex/general CLI transcripts should retain additional useful vectors, using the lab's publications beyond the Jev chapters; add requirements and deliver this dated handoff here. This is the requested research handoff, not an implementation change or a new STATUS owner.

**Recommendation:** preserve recoverable observations and their meaning first. Add typed measurements when actually available. Keep embeddings, graph coordinates, tensor factors and geometric transformations as versioned derived records linked to those observations. A single anonymous `vector: [...]` would lose the distinctions the research needs.

## 1. Current contract and the proposed increment

Read on November 5: this bed's [STATUS](../STATUS.md), [BUILD](../BUILD.md), [CLI provenance task](../tasks/CLI-PROVENANCE.md), [task list](../tasks/README.md), [stream/memory design note](design-notes.stream-memory-if.2026-11-03.md), and [source reference](../../../../zsh/jev/README.md). These documents report an accepted office installation and offline tests. This handoff did not inspect implementation code, rerun tests, read actual transcripts or access the runtime vault/provider.

Current events already have `schema,event_id,sequence,at,session_id,channel,request_id,kind,actor,data,previous_event_id`. Caller provenance separates `requester` from CLI session slots, with `controller` reserved null. Frozen requests, original receipts, selections, lineage and later outcomes already have defined roles. Reuse these meanings.

**New distinction:** a Jev caller session ID identifies who recorded an event; it does not identify every speaker or originating session inside a copied transcript. Preserve **recorder**, **requester**, **source session** and **source speaker** independently. Do not repurpose the actor's CLI slots to describe imported speakers. Copying or querying a record must not relabel its original author.

The inspected documents do not establish a general transcript importer or a measurement-extension namespace. Proposed names below are design vocabulary, not accepted fields or commands. Cartan chooses a versioned extension, dedicated event kind or export projection after compatibility review. Do not insert arbitrary fields into strict `jev.event/v1` records, change its hash recipe, bypass existing validators, expand same-session references implicitly, or rewrite legacy bytes.

## 2. Capture requirements — information that is hard to recover later

| ID | Requirement | Why it matters |
|---|---|---|
| C01 | Stable source namespace/session ID where observed, event/occurrence ID, record kind, role and speaker/agent identity; retain unknowns. Distinguish Jev engagement/channel/request from source conversation/turn/tool IDs. | Multiple CLIs may share one Jev stream; one imported transcript may contain several speakers. |
| C02 | Recoverable source content: exact selected bytes or a durable content-addressed artifact reference with digest, encoding, length and defined span/chunk boundaries. Record text, image, diagram, tool input/output and attachments by type. | A digest verifies bytes but cannot reconstruct them. A mutable file path alone is insufficient. |
| C03 | Source record ID or byte span plus source snapshot/generation identity, parser/adapter version and import occurrence. Preserve both exact source representation and normalized projection when needed. | Line numbers and paths can change; semantic extraction is a transformation. |
| C04 | Source event time and recorder observation/import time separately, with timezone/clock source/precision where known. Preserve source-local sequence, source turn and available monotonic intervals with units. | Import time is not event time. Separate machines' clocks or sequences do not establish a total causal order. |
| C05 | Explicit relation types: replies-to, tool-call/result, fork, retry, reconsideration, revision, supersession, selection-from and requested-by. Each link records observed/declared/inferred status and source evidence. | Chronological adjacency or a copied citation does not prove causal influence. |
| C06 | Observation boundary: captured interval/snapshot, cursor/span, complete/partial/unknown scope, gaps, truncation, filtering/redaction, parser failures and unavailable attachments. Distinguish a source omission from an importer omission. | Missing observations must not silently become observed zero or a clean session ending. |
| C07 | Request/response correlation and lifecycle evidence separately: source request ID, available nonce, start/stop/cancel/failure/timeout observations and terminal reason. Unknown correlation remains unknown. | Visible text or a stop marker alone does not prove completed, correctly associated work. |
| C08 | Known task/question/rubric/context identifiers, selected evidence and cutoff, exact prompt/packet or immutable reference, model/provider/runtime versions when actually supplied, settings provenance and synthetic/live designation. | Later comparisons need to identify what question was answered with which available information. |
| C09 | Observable exposure and cost: duration/window, token counts with tokenizer/source if known, calls, latency, cost currency and precision, budget/stop policy references. Separate observed, estimated and unavailable values. | Unequal exposure can imitate agent differences; counts, probabilities and money have different units. |
| C10 | Later adjudication, human correction, disposition and intervention as linked new observations, with author, time, rubric and source. Track holdout/group membership in evaluation manifests. | Future labels must not leak into earlier decision packets; an edit to interpretation must not rewrite evidence. |

These are a capture contract, not a requirement that every field be populated on every line. Put stable shared metadata in a versioned manifest and reference it. Capture an explicit capability/coverage declaration for each adapter: which fields are observed, supplied, derived or unavailable. A terminal-rendered capture may be useful but cannot be labelled a complete structured transcript by default. Preserve exported visible analysis/scratch only if actually present in the authorized source; it is not a record of hidden model computation or internal activation vectors.

Large objects may live beside the ledger in the private runtime store, with durable verified references; do not copy live transcripts into portable ia-sync source. An unavailable object must stay visibly unavailable rather than dangling behind a success claim. An export intended to be portable needs a bundle/manifest or an explicit external-reference limitation.

## 3. Which vectors are useful?

“Vector” here includes ordered, named measurements. It does not mean that unlike quantities should be concatenated and compared with one cosine metric.

| Measurement family | Save when available | Derive only when needed; interpretation boundary |
|---|---|---|
| **Categorical judgment** | Ordered option IDs and semantics, complete returned probability vector if provided, question/evidence/rubric version, raw response and validation result. | Entropy, margin, `sqrt(p)` or `2sqrt(p)`, Fisher–Rao distances. Compare the same category meanings/order; do not reconstruct a distribution from a chosen label or scalar score. Preserve any actually returned rubric-level distribution with its ordered level meanings. |
| **Predicate / Coin evidence** | Predicate IDs, yes/no/unresolved status, per-predicate observation references, rubric and rule versions; separate support/refutation evidence where genuinely measured. | Endpoint bounds, feasible completions, possible pivots, coalition evaluation. A near tie does not supply orientation. Separate binary marginal probabilities do not determine a joint distribution. |
| **Rubric score profile** | Criterion IDs, individual values, scale/units, ordering, weight/policy version, missingness and source. | Aggregates under an explicit rule. An ordinal score is not automatically a distance, probability or interval-scale measurement. |
| **Concept features** | Declared vocabulary/taxonomy version, named counts or scores, extractor/version, exposure denominator and eligibility/observation mask. | Agent × aligned-time × concept arrays and factors. A valid zero, missing cell and impossible cell are different. Sparse omission means zero only under an explicit schema convention. |
| **Session/process observations** | Named axes such as observed process existence, progress delta, expected waiting, ownership evidence, freshness, window and units. | State labels, history-dependent classifiers, suspicion and recovery statistics. These axes are not mutually exclusive modes or a universal health number. |
| **Participant evidence** | Who supplied each input, model/role where known, source evidence overlap, exposure and prompt condition. | Choquet/coalition scores, capacities and importance indices. Shared evidence and shared prompts must not be counted as independent witnesses. |
| **Dense embedding / stance measurement** | Optional artifact with producer/model revision, dimensions, preprocessing/chunking/pooling, normalization, coordinate/frame ID, input digest, task/question when relevant and generation settings. | Similarity, alignment or stance trajectories after validation. Unit length does not establish opposition or make vectors from different models comparable. Do not require an embedding service for ordinary capture. |
| **Graph features** | Explicit typed edges and their provenance; when queried, graph snapshot/construction version, seed method and retrieval parameters. | Spectral coordinates, diffusion ranks, clusters and graph-relative vectors. Appending records can change existing coordinates; they are not immutable identities. |
| **Dynamic/control features** | Actual time samples, observation windows, measured variables, intervention/action, delay and relevant outcome/loss. | Lags, spectra, derivatives or control scores under a specified model. One transcript trajectory does not identify curl, divergence, a causal field or an optimal recovery action. |
| **Selection/routing observations** | Candidate IDs/versions, capabilities, eligibility and reason, selected candidate, observable selection probability if actually randomized, cost and realized outcome. | Policy comparisons and calibrated utility estimates. Unchosen outcomes are unknown; normalized routing scores are not success probabilities. |
| **Scratch/representation condition** | Visible intermediate artifact type, instructed binding/nonbinding status, budget, parent task/final answer links and failures. | Compression/anchoring comparisons. Tokens are not information bits, and overlap is not automatically harmful copying. |

The most immediately useful vector is a **named per-question/per-criterion observation profile**, accompanied by its evidence and missingness. For Coin research, preserve primitive observations before collapsing them into FACE/TAIL/EDGE. Derived categorical geometry is cheap to reconstruct from valid `p`; storing both it and `p` is optional caching, not additional evidence. Binary Gini and absolute margin are similarly redundant when computed from the same `p`.

If a provider does not expose a quantity, mark it unavailable. Do not silently manufacture confidence, hidden embeddings, orientation, joint probabilities, calibration or zero cost. Two support/refutation scores need their semantics stated: they need not sum to one, and marginals alone do not identify four joint evidence states.

## 4. Common measurement metadata

Each measurement or referenced measurement bundle should declare:

```text
measurement_id, kind, measurement_schema_id/version
scope: event | span | turn | window | request | session | corpus
subject/source event IDs and exact input snapshot/digests
producer: method, version, model/revision when applicable, config digest
coordinate schema: ordered axis IDs, meanings, units, category set or frame ID
representation: dimensions, dtype, normalization, metric convention when used
value(s) or durable artifact reference; per-axis observation/eligibility status
generated_at, evidence_cutoff, calibration reference/status where applicable
derivation/source references; supersedes or recomputed_from when appropriate
```

The schema registry itself must be available or explicitly external, not just an opaque name. Validate finite numbers, vector length, unique/order-consistent axis IDs, masks, bounds and probability normalization where applicable. Preserve invalid raw input and validation errors separately; do not silently clip, renormalize, fill with zeros or reinterpret it. Unknown is not a numerical result. Record rounding/tolerance and any deliberate repair as a new transform.

For frame transformations, retain source/target frame and alignment-method/version/anchor references. Graph embeddings require graph snapshot and solver/basis conventions; tensor factors require dataset/mask/exposure definitions, fit and component alignment. Equal array shape is not enough for meaningful subtraction. An aggregate residual or norm cannot replace the measurements that produced it.

## 5. JSONL placement and compatibility

Use one independently parseable JSON object per exported line, with embedded newlines escaped. This describes the normalized export: BUILD explicitly allows a forensic ledger with preserved malformed fragments, which is not always strict JSONL. Do not copy that damaged byte stream and advertise every line as valid JSON. Preserve the forensic original separately; an export names its verified prefix, excluded fragment references and recovery state.

Recommended division:

1. **Capture observation** retains source content/references and recorder/source provenance.
2. **Measurement observation** links an extraction or derived vector to its exact inputs and method.
3. **Interpretation/outcome observation** records a policy result or later label with its own provenance.

This is a conceptual separation, not three compulsory files or a second ledger authority. A line may contain small measurements inline; expensive or subsequently computed measurements can arrive later as linked events/artifacts. The existing ledger remains authoritative under its released contract. Cartan must define cross-session/source references explicitly if added; current same-session validation must not be weakened by arbitrary paths.

Deduplication must distinguish the same occurrence imported twice from two real identical messages. Content hashes alone cannot do that. Prefer source namespace + source session + stable occurrence ID when available; keep snapshot identity separately as capture provenance so overlapping snapshots do not duplicate the same occurrence. If stable occurrence identity is unavailable, snapshot + byte span is a fallback whose deduplication across snapshots is unproven. An existing stable occurrence ID with conflicting bytes is a conflict to report, not permission to overwrite. Original occurrence and import occurrence remain separate. Do not let a schema change rewrite earlier hashes or confuse duplicate transport with independent samples.

### Synthetic projection example — not a current Jev event

The following is one proposed **export projection** combining two synthetic source references and a synthetic categorical observation. It is not valid input to the current CLI, not a new ledger schema, and not evidence of an exercised model. Real exports must resolve their references through the source/artifact manifests described above.

```json
{"schema":"jev.transcript-projection/proposal-1","synthetic":true,"source":{"namespace":"fixture","session_id":"conversation-A","event_id":"reply-7","role":"assistant","turn_id":"turn-3","sequence":7,"parent_ids":["request-6"],"captured_by":"transcript-adapter-fixture-v1","coverage":"fixture-complete"},"content":{"media_type":"text/plain","text":"The supplied passage supports the claim."},"measurement":{"id":"fixture-measurement-1","kind":"categorical_probability","scope":"request","source_event_ids":["request-6","reply-7"],"question_id":"support-q1","schema_id":"fixture-support/v1","axis_ids":["supports","refutes","insufficient"],"values":[0.6,0.1,0.3],"observed_mask":[true,true,true],"producer":{"method":"synthetic-fixture","version":"1"},"calibration_status":"not_established"}}
```

The three options in this fixture are stipulated exclusive/exhaustive outcomes of one question. They are not independent support/refutation probabilities. Schema and source manifests are omitted from this tiny illustration, so it is not a complete portable bundle.

## 6. Priority and acceptance for a bounded builder increment

**P0 — preserve evidence:** C01–C08, unknown/missing/error distinctions, exact source identity, durable payload references and explicit extension/export compatibility. Existing caller provenance should be reused, not rebuilt. Record C09/C10 when observations exist and preserve the ability to append them later.

**P1 — capture existing measurements:** full typed Jev outputs where supplied, predicate/rubric identities and measurement metadata. Start with named vocabulary and an ordinary exact/lexical retrieval baseline. No need to compute embeddings to save a transcript correctly.

**P2 — optional experiments:** embeddings, graph/tensor views, aligned stance trajectories, observer routing and dynamic estimates, each with a task and baseline. They should not block Jev-01's existing T03/T04 work or live-use gates. This handoff does not renumber T00–T07 or authorize paid extraction calls.

Suggested acceptance fixtures for a future agreed increment:

- Legacy Jev events replay byte-for-byte; caller slots and null controller remain valid; source speakers are not confused with the importer.
- One synthetic conversation crosses two CLI origins, forks, calls a tool, retries and receives a later correction; each occurrence and relation remains traceable.
- Multiline/Unicode text and an attachment survive export/import with verified bytes or explicit unavailability; a moved/mutated original path does not masquerade as the saved source.
- Duplicate ingestion deduplicates the same stable source occurrence across overlapping snapshots; two identical genuine messages remain two events. Snapshot-only fallback declares its cross-snapshot limitation, and conflicting bytes under one stable ID are surfaced.
- Source and import times differ; out-of-order arrivals, missing timestamps and concurrent branches preserve local order without inventing causality.
- Zero, missing, unobserved, ineligible, truncated, invalid and provider-error cases remain distinct. Invalid distributions/NaN/axis mismatches are refused as measurements while their raw evidence is preserved.
- Partial/filtered transcript and malformed-tail recovery export truthful coverage; neither is reported as a complete strict-JSONL transcript.
- Reordered options, changed vocabularies/models and graph updates invalidate incompatible derived comparisons; the old derived artifact remains attributable to its old snapshot.
- A later outcome can be attached without changing an earlier frozen evidence cutoff; evaluation keeps related incidents together.
- Disabled enrichment preserves capture operation; all basic checks use synthetic fixtures, with no paid calls or actual transcript copying in this research handoff.

## 7. Publication coverage and why these fields exist

The publications recover SHIFT_1 work and carry explicit SHIFT_2 corrections. This handoff uses that wider body, not just the Jev edition. Links are local research sources; original papers and their verification limits are recorded within each chapter. This is contract synthesis, not a fresh literature or runtime-API survey.

| Publication and section | Contribution to this handoff |
|---|---|
| [Stance geometry §§2,4,6](/home/hruzam/nabla-lab/publications/inner-circle/stance-geometry/study.md) | Question-conditioned measurements, category identity, representation/frame version; valid categorical geometry without assuming semantics. |
| [Spectral retrieval §§2,5–6](/home/hruzam/nabla-lab/publications/inner-circle/spectral-retrieval/study.md) | Typed edges and source snapshots; graph coordinates are rebuildable views. |
| [Coalition evidence §§2–5](/home/hruzam/nabla-lab/publications/inner-circle/coalition-evidence/study.md) | Participant identity, individual scores, shared-evidence provenance and rule version. |
| [Cascade diagnostics §§2,4–5](/home/hruzam/nabla-lab/publications/inner-circle/cascade-diagnostics/study.md) | Event order, parent/trigger evidence, external drive, coverage and binning. |
| [Tensor analytics §§2,4–6](/home/hruzam/nabla-lab/publications/inner-circle/tensor-analytics/study.md) | Aligned time, concept dictionary, exposure and explicit masks; factors are not causal roles. |
| [Flow/control/stopping §§2,4–6](/home/hruzam/nabla-lab/publications/inner-circle/flow-control-stopping/study.md) | Sampling, delays, actions, loss and information cutoff; a single path cannot identify a field. |
| [Coherence/composition §§2–4,6](/home/hruzam/nabla-lab/publications/inner-circle/coherence-composition/study.md) | Semantic units, comparison-map provenance and separate diagnostic types. |
| [Mental map: lineage, retrieval, reconstruction](/home/hruzam/nabla-lab/publications/inner-circle/mental-map/study.md) | Immutable source identities, explicit revision/view policy and retrieval provenance. |
| [Scratch instruments: mechanism and testing](/home/hruzam/nabla-lab/publications/inner-circle/scratch-instruments/study.md) | Observable representation, task links, commitment condition and measured cost. |
| [Interactive interposition: completion specification](/home/hruzam/nabla-lab/publications/inner-circle/interactive-interposition/study.md) | Distinguish rendered output, source event, correlation and turn completion. |
| [Jev practice study](/home/hruzam/nabla-lab/publications/inner-circle/jev-judgment/study.md) and [usage collection](/home/hruzam/nabla-lab/publications/inner-circle/jev-usage/README.md) | Bounded typed observations, evidence/interpretation/outcome separation and reusable experiment contracts. |
| [Later representation/history chapter](/home/hruzam/nabla-lab/publications/inner-circle/jev-usage/research-directions.md) and [coin dynamics](/home/hruzam/nabla-lab/publications/inner-circle/jev-usage/coin-dynamics.md) | History versus missing observations; separate physical geometry, confidence and operational state. |

Read-only helper `/root/jev_map` read the ten non-Jev studies in full and returned the coverage map. Main checked the decisive cited sections and current Jev design/provenance documents, then authored this synthesis. No new theorem, independent verification gate, or empirical benefit is claimed. The lab's briefing intake remains closed; this is a bounded downstream requirement handoff.

**Return requested from Cartan:** map P0/P1 onto the current contract, identify already-covered requirements and genuine gaps, and propose the smallest separately tested capture/measurement increment. Keep optional P2 derivations outside the initial logging path unless a concrete experiment calls for them.

Bounded read-only challenge by `/root/jev_challenge` found no publication blocker. Its two material corrections were incorporated: preserve genuine rubric-level distributions rather than reconstructing them from a scalar, and separate stable source-occurrence identity from snapshot provenance when deduplicating. This review is not an implementation acceptance gate.
