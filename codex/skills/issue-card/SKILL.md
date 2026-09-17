---
name: issue-card
description: Capture a known defect instance or reusable defect-reaction playbook in the shared ~/reposoma/_cold-start/ vault. Use when preserving an open, parked, or resolved issue with filterable evidence, or a recurring issue pattern and response; not for session re-entry glue.
---

# Issue Card

Preserve a defect so a later session can find and act on it without rediscovery. This is
the issue category of the same mechanism and vault used by `cold-start-card`; it is not a
parallel issue store.

Schema and lifecycle source: `~/reposoma/raw.guides/cold-start-card/GUIDE.md`. The issue
extension there is currently marked `[ISSUE-DRAFT]`; this skill does not gavel or promote
it. On conflict, report the mismatch and follow the operator-approved guide state.

## Choose the card type and destination

Use the shared vault at `~/reposoma/_cold-start/`:

```text
issues/
├── open/       ISS.<slug>.<YYYY-MM-DD>.md
├── parked/     ISS.<slug>.<YYYY-MM-DD>.md
├── archive/    ISS.<slug>.<YYYY-MM-DD>.md
└── reactions/  IR.<slug>.md
```

- `open/`: a dated defect instance not yet triaged into defer-or-fix.
- `parked/`: a dated defect instance deliberately deferred by the operator.
- `archive/`: a resolved dated defect instance.
- `reactions/`: a dateless, standing pattern-and-playbook card for a recurring defect
  class. Reaction cards never move to an archive.

Folder is state. Do not add a `status:` field. A state transition is a move between the
three dated-issue folders.

**Coupled-location invariant:** the issue subtree belongs to the cold-start vault. Any
future relocation of `~/reposoma/_cold-start/` and its issue location must happen together
in the same commit; never relocate either independently or create another issue vault.

The vault is git-tracked. Do not stage, commit, move, or publish a card unless the current
request authorizes it. Report that an uncommitted card is not visible cross-machine.

## Dated issue instance

Name the file `ISS.<slug>.<YYYY-MM-DD>.md`. Put one or two strong discriminators in the
slug; `kind:` remains the category truth.

Write flat frontmatter first. Use whole `~`-anchored paths, never bare-relative paths or a
literal `/home/<user>` prefix.

```yaml
---
kind: issue-card
date: <YYYY-MM-DD>
brand: codex
found_by: <seat or agent that observed it>
project: <origin project registry key>
root: ~/<whole path to project root>
where: ~/<whole path to broken surface>:<line?> (<symbol?>)
defect: <one sentence identifying this defect and its strongest discriminators>
assoc: [<tag>, <tag>, <tag>, <tag>, <tag>, <tag>, <tag>]
severity: <low | med | high> # optional
pointers:
  - ~/<durable evidence or deeper trail>
---
```

`assoc:` is a hard floor of **seven real, filterable associations**. Useful dimensions
include defect class, technology, subsystem, host, symptom, area, and severity. More are
allowed only when they naturally improve retrieval. Do not invent tags to meet the floor:
gather the missing facts or ask the user before writing. The one-sentence `defect:` is the
second cheap retrieval surface; it must identify the instance without a body read.

After the frontmatter, add compact evidence: what was observed and when, confirmed versus
suspected consequences, why it is open or parked, and where it was first recorded. Point
to durable sources instead of copying them. Distinguish observed, reported, and inferred
claims.

## Dateless reaction card

Use `issues/reactions/IR.<slug>.md` for a recurring defect class and its reusable response.
It has no filename date and no `date:` field because it recurs.

```yaml
---
kind: issue-reaction
brand: codex
found_by: <seat or agent>
project: <origin project registry key>
root: ~/<whole path to project root>
pattern: <one sentence identifying the recurring defect pattern>
playbook: <how to respond when this pattern appears>
assoc: [<tag>, <tag>, <tag>, <tag>, <tag>, <tag>, <tag>]
pointers:
  - ~/<related issue instance or deeper trail>
---
```

`pattern:` is the one-sentence recognition key; `playbook:` is the response. The same
hard `assoc:` floor of seven real discriminators applies. Reaction cards are permanent,
dateless knowledge like cold-start routines, not dated issue instances.

## Filename sorting and drift

For dated `ISS.*` cards, parse the `YYYY-MM-DD` substring from the **filename** as the
primary sort key. This is allowed even though `kind:` must never be inferred from a
filename: category parsing and date extraction are distinct operations. Do not use
filesystem mtime as the durable order.

If a card in a dated issue category lacks a filename date marker, surface it in an
`UNSORTED` bucket for correction; never silently guess or mis-order it. `IR.*` reaction
cards are intentionally dateless and exempt from `UNSORTED`.

## Write and verify

1. Resolve the vault through the repository's current reposoma mapping and confirm the
   requested state or reaction mode.
2. Draft the destination, frontmatter, and evidence within the current write authority.
3. Validate the filename/type contract, flat YAML, whole paths, one-sentence retrieval
   field, and `assoc:` count of at least seven.
4. Confirm the written path and state. Do not imply that draft creation gavels the guide,
   commits reposoma, or makes the card cross-machine.
