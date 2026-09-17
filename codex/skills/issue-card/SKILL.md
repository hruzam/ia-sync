---
name: issue-card
description: Preserve a known defect as a searchable fix manual in the flat shared ~/reposoma/_cold-start/ vault. Use when recording an issue, a deliberate deferral, its verified fix, or a recurring defect that should fold into routines; not for session re-entry glue.
---

# Issue Card

Preserve a defect and, once known, its fix so a later session can act without rediscovering
either. This is the issue category of the same mechanism and vault used by
`cold-start-card`; it is not a parallel issue store.

Schema of record: `~/reposoma/raw.guides/cold-start-card/res/issue-card.md`. Shared vault,
filename, sort, and frontmatter law: `~/reposoma/raw.guides/cold-start-card/GUIDE.md`.
The issue schema is `[GAVELED · REVIEW-AFTER-USE]`: it is in force, not a draft, and its
first real card plus fold triggers a re-audit. On conflict, report the mismatch and follow
the current guide state. This skill does not gavel canon or perform that re-audit itself.

## Resolve the destination

Use the flat shared vault at `~/reposoma/_cold-start/`:

```text
issues/     ISS.<slug>.<YYYY-MM-DD>.md   caught issue awaiting its fold
routines/   RT.<slug>.md                 routine born as intended
            ISS.<slug>.<YYYY-MM-DD>.md   issue graduated to a routine
archive/    CS.* and ISS.*               drained cards and solved one-shot issues
```

`issues/` has no nested state folders. Folder is state at the top level, so never add a
`status:` field. The earlier `issues/{open,parked,archive,reactions}` shape and separate
`IR.<slug>.md` reaction-card type are deleted; recurring fixes now live in the issue card
that folds into `routines/`.

**Coupled-location invariant:** the issue category belongs to the cold-start vault. Any
future relocation of `~/reposoma/_cold-start/` and `issues/` within it must happen together
in the same commit. Never create another issue vault.

The vault is git-tracked. Do not write, move, stage, commit, or publish a card beyond the
current authority. Report that an uncommitted card is not visible cross-machine.

## Choose the fold path

Every issue follows one of three paths:

1. **Known-recurring from the start:** write the issue card directly to `routines/`; do not
   route it through `issues/` or `archive/`.
2. **Assumed one-shot and stays solved:** write it to `issues/`, record the fix in the same
   card, then move it to `archive/` once resolved.
3. **Assumed one-shot but recurs later:** retrieve the solved card from `archive/` and move
   it to `routines/`; recurrence proves the routine.

Folding is a per-card operator decision. Do not move a card unattended.

A card landing in `routines/` through path 1 or 3 keeps its
`ISS.<slug>.<YYYY-MM-DD>.md` filename and original catch date; the date now means “first
seen.” Never rename it to `RT.`. Add `origin: issue` to its frontmatter. A routine born as
a routine uses `RT.<slug>.md` with `origin: intended`. Use optional `from_issue:` only when
a fresh routine card splits from an issue instead of moving the issue card wholesale.

## Write the issue card

Put one or two strong discriminators in the slug. `kind:` remains the category truth.
Use flat YAML and whole `~`-anchored paths, never bare-relative paths or a literal
`/home/<user>` prefix.

```yaml
---
kind: issue-card
date: <YYYY-MM-DD>
brand: codex
found_by: <seat or agent that observed it>
project: <origin project registry key>
root: ~/<whole path to project root>
where: ~/<whole path to broken surface>:<line?> (<symbol?>)
defect: <one sentence identifying the defect>
assoc: [<tag>, <tag>, <tag>, <tag>, <tag>, <tag>, <tag>]
severity: <low | med | high> # optional
pointers:
  - ~/<durable evidence or deeper trail>
---
```

`assoc:` has a hard floor of **seven real, filterable associations**. Cover useful
dimensions such as defect class, technology, subsystem, host, symptom, area, and severity.
Do not invent tags to meet the floor; gather the missing facts or ask the user. Make
`defect:` specific enough to identify the issue without opening the body.

After the frontmatter, write compact evidence: what was observed and when, confirmed versus
suspected consequences, where it was first recorded, and **the fix or response playbook once
known**. The fix stays in this card; point to durable sources instead of copying them.
Distinguish observed, reported, and inferred claims.

For a deliberate deferral, add `parked` to `assoc:` and add a body note explaining why it
is deferred and what condition ends the deferral. Parked is neither a folder nor a
frontmatter status; the card remains an ordinary resident of `issues/` until it folds.

## Sort and detect drift

For dated `ISS.*` cards, extract the `YYYY-MM-DD` substring from the **filename** as the
primary sort key. Date extraction for ordering is distinct from inferring `kind:` from a
filename; machines must still use frontmatter for kind. Never use filesystem mtime as the
durable order.

Surface any dated card without a filename date marker in an `UNSORTED` bucket rather than
guessing or silently mis-ordering it. Born `RT.*` routines are intentionally dateless and
exempt. A graduated `ISS.*` routine deliberately keeps its date as “first seen.”

## Run

1. Gather the broken surface, observation time and method, consequence, current fix
   knowledge, and whether recurrence is known or only possible.
2. Choose `routines/` only for a known-recurring defect; otherwise choose `issues/`.
3. Draft the filename, shared frontmatter, and compact fix-manual body. If deliberately
   deferred, encode parked only through `assoc:` plus the body note.
4. Validate the destination, flat YAML, whole paths, one-sentence `defect:`, at least seven
   real `assoc:` entries, and filename date.
5. Write only within current authority. Confirm the exact path and state, and report any
   later fold as a separate operator-approved move.
