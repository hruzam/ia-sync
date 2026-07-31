---
name: learn-repomix
description: >
  Invoke as /learn-repomix. Economic token approach for reading repomix files and
  packed repo bundles: grep first, small context, confirm before going deeper.
  Use for repomix analysis, code/logic traversal, structure mapping.
  Headless pipeline alias: rn lnrx
---

I am in `rn lnrx` regime. I navigate repomix files step by step with minimal token spend.

## Golden rules

1. Grep first — locate before reading
2. Read small context around the hit
3. Ask: "is this what we are searching for?" — confirm before going deeper
4. Follow the logical code/text vector
5. Show each step — @majkee confirms before I proceed

## Repomix structure

I read the standard repomix header **once**, then skip it. On subsequent encounters I jump
directly to `# Directory Structure` and `# Files` blocks.

Header I skip after first read:
```
# File Summary / ## Purpose / ## File Format / ## Usage Guidelines / ## Notes
```

## Context intake

Invoked as `cmd lrnrx -- <where> -- <file> -- <context>`:
- `<where>` — location scope
- `<file>` — target file to focus on
- `<context>` — freehand phrase: session goal, what to find, pivot info

Invoked as `rn lnrx` without cmd context:
- I ask @majkee for context before proceeding
- Regime stays active until `!rn lnrx` or until it would block other active work

## Navigator mode

When navigating step by step:
- I show small snippets only
- I state what I think the next logical move is
- I wait for @majkee to confirm before the next step

## Memory guard

If my context is saturating from consumption → I STOP and notify @majkee before continuing.
