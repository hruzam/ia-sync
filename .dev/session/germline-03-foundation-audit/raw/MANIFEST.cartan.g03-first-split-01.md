---
title: Draft source manifest — G03 first split
status: draft · not frozen · no research body authorized
writer: Cartan · cSharp
repository: /home/hruzam/ia-sync
branch: main
commit: a30acc41fb5f57334abe79d866124554a99bb4d9
---

# Scope boundary

This is a proposed absolute-path manifest for later review, not a source assessment. No body may
read a candidate source until Majkee accepts this manifest and the paired criterion. The candidate
labels came from the authorized Germline-03 substrate locator; their cited historical evidence was
not followed.

## Proposed entries

| candidate label | absolute source path | repository identity | content hash | draft disposition |
|---|---|---|---|---|
| tunnel | `/home/hruzam/ia-sync/germline/tunnel/tunnel.preamble.md` | tracked blob `fce63d75bdc0603a9ed80bf8ed23758a4289acef` at commit `a30acc41fb5f57334abe79d866124554a99bb4d9` | `c2153598ebd068ed49e54268c9566595633fae0bd2b50f419eddf79d59e4a611` | candidate path located; not read for this preparation |
| primitive-build | none | none | none | source path not supplied by authorized locators; requires Majkee-approved mapping |
| guide-author | none | none | none | source path not supplied by authorized locators; requires Majkee-approved mapping |
| session-position | none | none | none | source path not supplied by authorized locators; requires Majkee-approved mapping |

## Locator mapping attempt — proposed, unapproved

The authorized locator read identifies all three labels only in
`/home/hruzam/ia-sync/.dev/session/germline-03-foundation-audit/raw/SUBSTRATE.atlas.from-germline-02-close.2026-10-15.md:17-18`.
It does not associate any of them with an absolute candidate-source path. The separate paths it
names for Atlas-card and pulse-placement drift are not labelled as any of these candidates, so
they are not proposed here.

| candidate label | proposed mapping | identity | reason |
|---|---|---|---|
| primitive-build | none — unresolved locator boundary | none | no absolute candidate path appears in either authorized locator |
| guide-author | none — unresolved locator boundary | none | no absolute candidate path appears in either authorized locator |
| session-position | none — unresolved locator boundary | none | no absolute candidate path appears in either authorized locator |

## A2 locator proposal — unapproved

This identity-only pass read P8's candidate rows and the P8-linked AS-r4 inventory metadata,
not any candidate body. P8 supplies functions, inputs, and evidence boundaries; it does not bind
any of these three labels to an exhaustive, label-specific accounting set. Contextual accounting
rows therefore remain provenance, not selected candidate mappings.

| candidate label | proposed source set | recorded immutable identity | exact P8/accounting provenance | disposition |
|---|---|---|---|---|
| primitive-build | none — ambiguous P8 provenance | none | `REVISION.PG-r3.md:341` calls for measurement against generic “existing builders/skills” plus germline-forge. AS-r4 B3 records one builder-skill source (`/home/hruzam/.agents/skills/codex-harness/SKILL.md`, SHA-256 `9ffc84515873e5be202ad6f5ab3a06c50a0c265759a809dbddefe0fa0eb66e12`) and B33 records germline-forge (`/home/hruzam/reposoma/raw.guides/germline-forge/GUIDE.md`, SHA-256 `2a97c2935fd38d923d3401e8d245aca552cf6f47f68919433c6808f3598f696b`); neither row binds an exhaustive source set to this label. | non-unique/incomplete; no source set selected |
| guide-author | none — ambiguous P8 provenance | none | `REVISION.PG-r3.md:342` supplies only the role and required exact source/topic, owner rights, and destination; it names no source-accounting row or source path for the label. | missing label-to-accounting binding |
| session-position | none — ambiguous P8 provenance | none | `REVISION.PG-r3.md:313,343` names RUNBOOK/STATUS law and required gate/evidence/snapshot/write grant, but no absolute RUNBOOK/STATUS accounting row is bound to `session-position`. | missing label-to-accounting binding |

## Freeze and dirty-byte rule

Before the body starts, every candidate must have an absolute path and repository identity. Each
named dirty or untracked source must additionally carry a current `git status --short` entry and
SHA-256. This draft names no dirty or untracked candidate source. Any missing mapping, changed
identity, dirty-byte omission, or requested scope expansion stops the body and returns to Majkee.
