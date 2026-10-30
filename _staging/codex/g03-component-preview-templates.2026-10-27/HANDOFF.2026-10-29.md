# Parked component-preview design — frozen handoff

2026-10-29 · Cartan(germline-03) · office · ia-sync.
This is a dated design/continuity record, not another live STATUS or a release to implement.
G03's formal audit position and authority remain in
`~/ia-sync/.dev/session/germline-03-foundation-audit/STATUS.md`.

## Purpose and recorded recommendation

The operator wants a loading helper to reveal a cheap, useful preview before an agent
consumes a card, controller, function or skill. Ordinary CLI file/glob/search reads must
remain useful across Claude, Codex and Gemini CLI use; AGY is excluded.

The working recommendation after Oraculum consultation is **thin B now, C as compatibility**:

- A small neutral source core: schema, stable id, kind, name, short description.
- One typed normalized reader record; existing files/native envelopes remain valid inputs
  through versioned adapters. Missing/computed values retain their provenance.
- Reader-owned cumulative collections, with source revision and per-field origins.
- Native wrappers retain runtime-specific syntax, permissions and entry mechanics.
- Ordinary first reads remain possible without a custom service or projector.
- Optional read hints and caller-owned tool preferences can improve discovery and reading.
- Metadata placement, extraction, physical caching and model intake are separate decisions.
  A derived host-local cache is possible; selected output saves context.
- Prefer one source with a bounded optional metadata extension initially. A sidecar requires
  deliberate linkage/composite provenance. A preview stamp cannot prove full-body intake.

These are proposals under operator review. No schema, migration, cache or native mechanism
was promoted or installed by this work.

## Read a small set first

| File | Role |
|---|---|
| `08.thin-B.shell-first.proposal.md` | Revised foundation and normalized record |
| `09.read-recommendations.proposal.2026-10-28.md` | Caller tool preferences and optional file hints |
| `10.metadata-placement-and-cache.proposal.2026-10-28.md` | Placement/cache tradeoffs and later Oraculum supplement |
| `07.oraculum-consultation.md` | Full initial consultation and ordinary-CLI supplement |
| `00.before-reading.md` | First ideas, preserved before further reading |
| `01`–`06` examples and `README.md` | Initial alternatives and projection examples, not the final recommendation |

The README's initial A/C-first lean was revised by 07/08. Its older rich B and legacy-map
examples also expose the verified scope-type mismatch and ambiguous dependency timing;
do not silently treat those draft-01 examples as the corrected contract.

Read deeper files only for the question being resumed. The complete transcript or the
entire packet is not required for initial orientation.

## Evidence and limits

Local checks parsed the example headers/YAML, exercised ordered field projection and missing
values, checked ordinary shell examples, and verified the protected sources at each write.
Oraculum's returns are analysis; its entry proof was late and is labelled accordingly.

No production reader/cache, native registration, full-body witness mechanism, performance,
token saving, cost saving or retained-understanding result was established. G09 execution
belongs to its own head; this packet does not grant a G09 turn or alter its frozen inputs.

## Custody and discoverability

The packet lives outside the session bed at
`~/ia-sync/_staging/codex/g03-component-preview-templates.2026-10-27/`.
Closing a CLI pane does not remove these ordinary files, and pruning G03's bed would not
itself remove this directory.

At this capture the packet was **untracked and local to office**. Repository HEAD
`5c26d80aa3c90de6cafc1c47a7d199fdbcc7466d` identifies the surrounding worktree, not a
commit preserving these drafts. The dated manifest records filenames, sizes and SHA256.
It is an integrity inventory, not a backup.

Central re-entry pointer:
`~/reposoma/_cold-start/card/CS.germline-03-preview-design.2026-10-29.md`.
The card points back here and to G03 STATUS; it does not replace either source.
Both repositories need an authorized preservation/publication step for cross-machine
visibility. No stage/commit/push is implied by creating this handoff.

Native child handles are historical observations, not portable resume identities.
A later session should reconstruct context from these files under its actual assignment.

## Unsettled design questions recorded at handoff

The exact core/types/extension contract and first concrete consumer still need the operator's
decision. Further proposed evidence includes typed projections over one unchanged card,
controller and function; explicit missing/invalid values; duplicate identities; source-change
handling; and separate preview versus complete-body delivery.

Physical cache adoption remains optional and would need actual invalidation/value evidence.
This dated record supplies no competing next-action order for G03's formal audit gate.

## Eventual disposition

Keep the packet intact while its design is under review. On adoption, move the accepted
meaning to the reviewed destination appropriate to its purpose and leave provenance/pointers.
Partial acceptance retains the unresolved drafts with an explicit disposition. Rejected
material can be retired only through the authorized preservation/cleanup process.

Before formal session pruning, account for this external packet as a keeper and confirm
preservation. Session-process observations inside the bed follow the shared RUNBOOK guide's
observations-before-prune rule; that rule does not automatically promote these templates
into canon or turn them into executable germline files.
