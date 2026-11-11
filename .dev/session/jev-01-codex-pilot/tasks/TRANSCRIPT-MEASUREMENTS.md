# Transcript capture and measurements — intake and implementation line

Cartan · office · 2026-11-05. Working task contract; not a released event schema.
Authority: majkee asks to incorporate Oraculum's handoff in this Jev line. No successor
session is needed. Source: [research handoff](../raw/oraculum.transcript-measurements-handoff.2026-11-05.md).
The research reviewed ten other publication streams; this intake maps its requirements to
Jev, rather than claiming to have independently repeated that literature assessment.

## Current coverage

| Requirement | Present mechanism / audit-specific evidence | Missing general capability |
|---|---|---|
| C01 source identity | Event actor records caller CLI/requester; dogfeed packet separately names source session, roles and message IDs | Validated imported-speaker/occurrence contract across adapters |
| C02 recoverable content | Exact frozen packet/provider bytes and raw replies; selected transcript texts embedded in audit packet | Durable typed attachment/artifact custody with verified references |
| C03 snapshot and parser | Audit manifest has prefix digest, offsets, source record/text hashes | Reusable adapter/import versioning and stable occurrence/conflict policy |
| C04 time and ordering | Jev event sequence/time; original source timestamps in audit manifest | Source/import clock distinctions and uncertainty as a general contract |
| C05 relationships | Request lineage, retry/reconsideration, selections and event references | Typed source reply/tool/fork/revision relations with evidence and inference status |
| C06 coverage | Audit cutoff and exclusions are explicit; ledger exposes tail diagnostics | Adapter capability declarations, missing attachments, gaps and normalized recovery export |
| C07 lifecycle | Jev prepare/attempt/HTTP/reply/settlement correlate its own request | Imported source request lifecycle and explicitly unknown associations |
| C08 experimental context | Frozen questions, rubric, evidence, selected model and actual reply model; synthetic/live separation | A common import/evaluation manifest across cases |
| C09 exposure/cost | Raw provider usage; exact USD ledger; audit records tokens | Named units, windows, measurement provenance and unavailable/estimated distinctions across adapters |
| C10 later labels | Append-only outcomes/dispositions and explicit memory/selection references | Blinded adjudication, grouped holdout manifests and correction protocol |

Evidence anchors: `zsh/jev/{README.md,store.py,jev.py,kernel.py,provider.py}` and the private
dogfeed `bound-packet.json`, `extraction-manifest.json`, `comparison.json`, and saved ledger.
Application metadata inside this one packet is not proof of a general transcript importer.
Existing outcome JSON is not a substitute for a validated measurement schema.

## Ordered increments

**T09 — P0 capture/export.** Start with a versioned, read-only projection and manifest over
existing verified records plus an explicit source adapter. Keep private source bytes and
normalized content distinct. Pin the exact input snapshot, source occurrences, original
identities, coverage and unavailable fields. Specify schemas and fixtures before adding a
command; reuse ledger replay instead of a second permissive parser. The first slice can use
the existing dogfeed as a compatibility fixture; it must not advertise general multi-CLI
coverage from that single fixture. Preserve available C09/C10 evidence from the outset.

**T10 — P1 named measurement projection.** Export actual full distributions and criterion
values with ordered axis meanings, units, schema, producer/version, input references,
cutoff, masks and validation. Store derivations separately with source/version links.
Keep provider confidence distinct from chosen-category probability. Define resolvable
schemas; reject invalid values without silently clipping, filling or renormalizing.
Evaluate a declared lexical/checklist comparator before proposing embeddings.

**P2 — optional research derivatives.** Embeddings, graph coordinates, tensor factors and
geometry stay optional. Record model/frame/dataset/representation versions if later used.
Neither capture nor a readable view needs an embedding service.

T03/T04 spending visibility/settings remain the next engine implementation work. T09/T10
join this session's line; they do not block those tasks or reopen the fixed RUNBOOK gate.
The separately requested reader handoff may proceed on the existing record contract.
No automatic experiment loop, cache, provider call or general workflow engine is implied.

## Acceptance before claiming the new capability

- Legacy events and hashes unchanged; readers preserve unknown legacy caller fields.
- Recorder/requester/source speakers remain separate across a multi-CLI fixture; forks,
  tool pairs, retries and corrections carry typed, evidenced links.
- Unicode/multiline text survives exactly; unavailable attachments remain unavailable.
- Overlapping snapshots deduplicate by proven source occurrence, not equal text; conflicting
  bytes for one stable ID are surfaced. Span-only cross-snapshot identity stays unproven.
- Source-local order survives out-of-order import and uncertain clocks. Missing, zero,
  ineligible and invalid values stay distinguishable.
- Filtered/corrupt sources export truthful coverage and a verified prefix; forensic originals
  remain intact. Every normalized JSONL output line parses independently.
- Axis/model/representation mismatches prevent unsupported comparisons; later labels do not
  alter earlier cutoffs. Capture works with all enrichment disabled.

Implementation returns must name supported adapters, schema versions, observed fixture
results and custody limitations. A document or example alone does not close T09/T10.
