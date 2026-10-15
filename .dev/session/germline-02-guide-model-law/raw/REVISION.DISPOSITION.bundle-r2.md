---
title: Cartan dispositions — Atlas AR-r1 proposal review
revision: DR-r1
date: 2026-10-14
by: Cartan · codex · Medusa
review: AR-r1
candidate: PG-r2 / AS-r2 / GV-r2
authority: proposal correction and evidence only; Atlas re-reviews, Majkee gavels
scope: germline-02-guide-model-law
---

# Review consumption and dispositions

Majkee returned Atlas's receipt path. Cartan read its actual content and verified its candidate
identity table against the still-current r1 manifest before changing candidates. AR-r1's
overall verdict is **FAIL — narrow/additive**, with PG-r1 PASS with findings, GV-r1 PASS and
AS-r1 failing completeness. Its receipt remains unchanged at its Atlas-owned path; exact
r1 bytes are also retained in REVISION.AR-r1.md.

AR-r1 SHA-256:
`797614f708ad5a125a6b1b693ad83573d072464f6bb4076c3d11e91b00532c5b`.
Reviewed r1 manifest SHA-256:
`43ac6b79d5da744094dd6b1e7dca35603a00b57b39c5ff602aa6e7f448165363`.

## Every finding — author disposition, not review approval

| Atlas id | disposition and actual change | evidence / focused re-review |
|---|---|---|
| A1 major | Accepted. AS-r2 adds B44–B50 for v3 ZIP, original fidelity POINT, four bed-raw reviews and sealed path. Six supplementary hashes; sealed file is name/metadata only. B49 distinguishes pre-ruling conditional countersign from adopted post-ruling S02. | All 14 regular old-raw files accounted; 13 unsealed identities + one sealed disposition; 16 staged rows unchanged. Atlas re-reviews seven rows, scope/identity explanation and provenance. |
| A2 low | Accepted. B7 count corrected from 13 to 14 non-directory members; v3 ZIP separately has 18. | Performed central-directory name counts only; no member payload read, extraction or integrity test. |
| A3 low | Accepted. Specific use cells replace generic descriptions for B6/B18/B19/B21/B24–B28/B36–B39/B41. Claude row B19 no longer claims Codex source/live equality. | deploy_germline and RSYNC_FLAGS source inspected, not run; native/session/presence comparisons stated by object. Re-review changed cells. |
| P1 medium | Accepted as candidate clarification. PG-r2 P2 requires table-expected versus observed function stamp comparison for project, global and project-first before procedure load; mismatch HELD even without caller pin, no operation/fallback. P4 rows agree. | Atlas re-walks P2/P4/T3; universal mismatch hold is explicit candidate detail still awaiting G4 acceptance. |
| P2 low | Accepted optional coverage. T11 omitted scope and T12 package-escaping function path added; both predict hold before function load. | Atlas paper-walks these two cases. No runtime resolver implemented or tested. |
| P3 low | Clarified candidate boundary. Explicit global requires no project root and performs no unrelated project probe. T4 collision is supplied input, not discovered knowledge. Optional probing remains an exposed G4 choice. | Re-review P4/T4 and G4; no hidden project-input requirement or scope scan. |
| P4 low | Retained as a proposal for G2/the later audit: an illustrative command may point to its public function for traceability. No automatic rule/hook adopted. | Re-review P6/G2 disclosure; final traceability rule and audit enforcement remain ungaveled. |
| P5 low | Accepted audit-subject omission. P8 tunnel candidate adds explicit state-path gate and never-unlink-Codex-writer-locks to its measured invariants. | HANDSHAKE already cited these; Atlas checks changed candidate row. No tunnel operation or skill implementation. |

## G4 concerns and limits carried forward

The specialisation pin choice is now explicit in P4 and G4: per-edit token/byte revision can
stale every dependent on a typo; a semantic compatibility revision requires a separately
governed compatibility/invariant review. Neither is selected. S1/S2 remain alternatives.
S2's invariant-drift risk, where no explicit global lock is supplied, remains part of that
decision. Cartan does not resolve it by dropping a lock or by importing another controller.

AR-r1's limits remain visible: paper reasoning only; focused source greps rather than full
live-law/native-body reads; older review claims not independently rechecked beyond countersign
diff; author interest in earlier INSIGHT S1/ghost/receipt proposals. These are limits, not
unreported PASS coverage. Atlas cannot attest the first wake's before-state beyond retained
baseline or its detached presence record. This reconciliation asserts no stronger witness.

PG-r2, AS-r2, GV-r2, AB-r2 and CP-r2 have new identities. AR-r1's whole-file hash table no
longer identifies them. Unchanged text may retain bounded coverage only after Atlas compares
it with exact r1 snapshots. P8's foundations, audit-only successor direction and all seven
OPEN gavel families remain intact; no final gavel has arrived.

## Retention and checks

Exact r1 candidate snapshots: REVISION.PG-r1.md, REVISION.AS-r1.md, REVISION.GV-r1.md,
REVISION.AB-r1.md and REVISION.CP-r1.md. Their hashes match AR-r1's identity table.
SHA256SUMS.review.r1 preserves the original manifest bytes; it still names the original
candidate addresses, so verify the snapshot mapping rather than running it on r2 files.
The refreshed current manifest pins these retained receipts and new candidate evidence.

Observed before r2 completion: 67 unsealed source hashes retained; all seven A1 dispositions;
14 old-raw top-level file names covered; 16 staged files / 15 v3 payloads / 18 v3-tree files;
B46–B48 directly equal S01/S03/S04 and B49 diverges from S02; ZIP metadata counts 18 and 14;
all r1 snapshots and Atlas receipt unchanged; r2 YAML/fences/case/gavel checks pass;
git diff --check passes and scoped tracked live surfaces have no diff.
CP-r2 carries the exact read-only recovery probe and final evidence boundary.

No old input, original review, sealed content, live law/skill/agent/card, deployment, git
transport or other bed was changed. Source completeness correction does not perform the
separate audit-only successor. STATUS alone carries the next action; AB-r2 supplies the
operator-transported re-review task.
