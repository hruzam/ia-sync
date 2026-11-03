# Retired germline work and reusable evidence

2026-11-03 · operator-authorized local cleanup. This is discovery and custody information, not a second STATUS or acceptance ledger. Local relocation with historical aliases is distinct from a completed guide-defined preservation/closure: the preservation commit remains pending. No source bytes are discarded.

## Where to look

- Live work: [pulse](pulse.md) → each owning STATUS. Directory numbering is identity, not dependency or execution order.
- Retired readable packages: `.dev/records/germline/2026-11-03/<original-full-slug>/`.
- Compressed cold copies: `history/germline/2026-11-03/<original-full-slug>.tar.gz` (already gitignored).
- [Manifest](.dev/records/germline/2026-11-03/MANIFEST.json): full origin, each file hash, archive hash, disposition and custody. [Disposition records](.dev/records/germline/2026-11-03/dispositions/) distinguish retirement from acceptance.
- Old `.dev/session/<full-slug>` paths are compatibility symlinks to the exact historical package. They are not active sessions. Never repoint an old full slug to unrelated work. For relative links in historical bodies, read through these aliases; historical snapshots are not silently rewritten.

## Recovery and preservation limits

The readable packages and compressed copies were compared file-by-file after actual extraction. Original result bodies, frozen fixtures, scores, addenda, dispatches and returns remain unchanged. Four idle G07/G08 tunnel handles were closed through the supported local operation before archival; [close receipts](.dev/records/germline/2026-11-03/TUNNEL-CLOSE.json) preserve identifiers without live enable state. No model turns or thread deletion occurred.

Custodian: myShell for this move; original owners retain result disposition. Everything is currently local to office. No preservation commit, independent backup, transport or home receipt is claimed. Readable ordinary source files are eligible for normal authorized Git preservation; existing ignore rules still apply to JSONL/runtime material. Do not force-add runtime histories. The compressed copy is not shared custody by itself.

To recover: select the exact full slug in MANIFEST, verify the archive SHA-256, extract to a fresh temporary directory with `tar -xzf <archive> -C <empty-directory>`, and compare every member against the manifest before restoring anything. Never extract over living work. A missing local archive is unknown custody, not proof of deletion; the manifest alone cannot recover bytes. Retained scripts may embed original absolute paths; aliases preserve local reads, but executing an archived script needs a fresh scoped review and authorization. Restoration does not re-enable a tunnel.

## Retired packages

| Original identity | Disposition | Integrity |
|---|---|---|
| [germline-02-guide-model-law](.dev/session/germline-02-guide-model-law/STATUS.md) | accepted closed scope; proposals and unresolved exit distinctions retain their original status | [manifest](.dev/records/germline/2026-11-03/MANIFEST.json) |
| [germline-04-wiring-plan](.dev/session/germline-04-wiring-plan/STATUS.md) | accepted closed scope; proposals and unresolved exit distinctions retain their original status | [manifest](.dev/records/germline/2026-11-03/MANIFEST.json) |
| [germline-05-sella-germline-audit](.dev/session/germline-05-sella-germline-audit/STATUS.md) | accepted closed scope; proposals and unresolved exit distinctions retain their original status | [manifest](.dev/records/germline/2026-11-03/MANIFEST.json) |
| [germline-06-full-audit](.dev/session/germline-06-full-audit/STATUS.md) | accepted closed scope; proposals and unresolved exit distinctions retain their original status | [manifest](.dev/records/germline/2026-11-03/MANIFEST.json) |
| [germline-07-make-program](.dev/session/germline-07-make-program/STATUS.md) | retired from active use by Majkee; result acceptance remains pending; no further trial released | [manifest](.dev/records/germline/2026-11-03/MANIFEST.json) |
| [germline-08-caretaker-receipts](.dev/session/germline-08-caretaker-receipts/STATUS.md) | retired from active use by Majkee; result acceptance remains pending; no further trial released | [manifest](.dev/records/germline/2026-11-03/MANIFEST.json) |
| [germline-A4-reader-shapes](.dev/session/germline-A4-reader-shapes/STATUS.md) | retired from active use by Majkee; result acceptance remains pending; no further trial released | [manifest](.dev/records/germline/2026-11-03/MANIFEST.json) |
| [germline-A5-reader-navigation](.dev/session/germline-A5-reader-navigation/STATUS.md) | retired from active use by Majkee; result acceptance remains pending; no further trial released | [manifest](.dev/records/germline/2026-11-03/MANIFEST.json) |
| [germline-A9-reader-economy](.dev/session/germline-A9-reader-economy/STATUS.md) | retired from active use by Majkee; result acceptance remains pending; no further trial released | [manifest](.dev/records/germline/2026-11-03/MANIFEST.json) |
| [germline-A6-harness-builder](.dev/session/germline-A6-harness-builder/STATUS.md) | superseded preparation; unstarted builds belong to A1 groups 002–004, not completed | [manifest](.dev/records/germline/2026-11-03/MANIFEST.json) |
| [germline-A7-shuttle-execution](.dev/session/germline-A7-shuttle-execution/STATUS.md) | superseded preparation; unstarted builds belong to A1 groups 002–004, not completed | [manifest](.dev/records/germline/2026-11-03/MANIFEST.json) |
| [germline-A8-epoch-researcher](.dev/session/germline-A8-epoch-researcher/STATUS.md) | superseded preparation; unstarted builds belong to A1 groups 002–004, not completed | [manifest](.dev/records/germline/2026-11-03/MANIFEST.json) |
| [germline-A2-nabla-lab](.dev/session/germline-A2-nabla-lab/STATUS.md) | accepted closed lab setup, inherited as group 001 of A2-projects; Track 2 research remains separate | [manifest](.dev/records/germline/2026-11-03/MANIFEST.json) |

## Knowledge worth inheriting

- [G06 integrated audit](.dev/session/germline-06-full-audit/units/INTEGRATED.recommendations.md): findings, decision distinctions and later work; accepted audit is not blanket acceptance of proposals.
- [Scars and receipts](.dev/observations/README.md): verbatim process lessons and result qualifications for reincarnation and sequential work. Choose relevant lessons; verify currentness.
- [A1 CACHE](.dev/session/germline-A1-vi-agents/CACHE.md): reusable agent-production experience, separate from its task queue.
- [A2 projects](.dev/session/germline-A2-projects/RUNBOOK.md): the continuing project-preparation ladder, with original lab setup as group 001.
- [Whole-design understanding](_staging/codex/germline-whole-design.2026-10-29/CONTINUITY.md) and [CACHE](_staging/codex/germline-whole-design.2026-10-29/CACHE.md): coordinator's attributed synthesis; A3 owns design position.
- [A4/A5/A9 evaluation](_staging/codex/germline-reader-experiments.2026-11-03/EVALUATION.md): bounded findings and A9 adjudication; pending result acceptance travels with retirement.
- [Crawler feedback for G03](.dev/session/germline-03-foundation-audit/raw/REPORT.myShell.crawler-experience.2026-11-03.md): actual model/effort evidence, useful findings and limits; no measured economy claim.

G03 and G09 remain live. G00's outdated symlink-era gate requires an owner disposition; do not execute its old recovery instruction as current guidance. G01 remains a historical witness source and A0 broader intake. No GUIDE/canon promotion occurred. The named Agol harvest route is not exposed by this Codex runtime; any bounded native-reader harvest is labeled with its actual role/model, not passed off as a witnessed Agol invocation.
