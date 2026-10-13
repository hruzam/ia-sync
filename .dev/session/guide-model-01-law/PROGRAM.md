# Program — cross-runbook backlog background

## Purpose

This is Majkee and myShell's small coordination surface for work turns that span or
touch several active runbooks. It helps recover context and prepare the next bounded
question or reader assignment. It is not a fourth source of execution state.

## Operating contract

1. Majkee may describe a work turn in plain language.
2. myShell records only: the scope, an authoritative source pointer, durable evidence
   (or an explicit unknown), and a concise unresolved question if one remains.
3. The owning bed's `STATUS.md` always wins for its actual position and `next:`.
   This file never copies or changes it.
4. A tentacle is released only for a named, bounded question. Its report supplies
   evidence; myShell checks cited artifacts before an index entry relies on it.
5. This file stays short. Detailed substrate belongs in the owning bed or the correct
   durable home, not here.

## Index format

```markdown
### <scope> — <short present-purpose label>
- Source: `<absolute path>`
- Evidence: <commit, receipt, observed file, or `unknown`>
- Open question: <none, or one bounded question>
```

## Current index

### guide-model-01-law — Symmetry design intake

- Source: `/home/hruzam/ia-sync/.dev/session/guide-model-01-law/raw/SYMMETRY-CATALOG.2026-10-13.md`
- Evidence: `guide-model.zip` SHA-256 `b0a0fae9d036bfd758b3c4c9aaa33b90414bb61b8ec14b4d11155a7d586fc3aa`; `unzip -t` PASS; unchanged 12-file extraction; no scripts executed; required-head assignment preserved at `raw/POINT.myShell-to-Astrobley.2026-10-13.md`.
- Open question: What, if anything, requires one human-mediated Opus Oraculum relay after Astrobley's cited plan returns?
