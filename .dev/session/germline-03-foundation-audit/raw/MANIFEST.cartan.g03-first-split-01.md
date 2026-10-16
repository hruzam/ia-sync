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

## Freeze and dirty-byte rule

Before the body starts, every candidate must have an absolute path and repository identity. Each
named dirty or untracked source must additionally carry a current `git status --short` entry and
SHA-256. This draft names no dirty or untracked candidate source. Any missing mapping, changed
identity, dirty-byte omission, or requested scope expansion stops the body and returns to Majkee.
