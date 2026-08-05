# PARKED · palette v2 — frontmatter projection (single-source help/alias metadata)

> Locked for a later phase by @majkee, 2026-08-05, session flight.office.zsh-monitor.forked.
> Status: PARKED — design direction gaveled, build NOT scheduled. Recorded by Flight (MANNED).

## The idea (operator's words, distilled)

Help snippets should be naturally parked for load: one structured source per
scope/engine — loadable markdown/zsh with frontmatter, or a structured part of
the script itself (pin-style) — so help text and keyboard alias references are
never written twice. The composer recognizes the structured block and projects
everything else from it. Model precedents: Claude harness skills/agents
(.md + YAML frontmatter) · elements-factory pin-core (open schema, tolerant).

## What it replaces

v1 (shipped): truth scattered across three projections — `_<scope>_help()`
heredocs + keyboard.zsh aliases + palette.map derived by PARSING both
(heuristics: box-drawn tables, sub-flag docs, trailing comments). Every new
help-format quirk = new parser heuristic. v2 kills the heuristics.

## The design fork to decide at un-park time

- **A · metadata-in-script (pin variant):** comment-fenced structured block
  inside each engine/keyboard file. Composer reads it exactly (no heuristics).
  Shell files stay plain + sourceable, no build step. Residual duplication:
  aliases still hand-written.
- **B · full inversion:** frontmatter file is THE source; keyboard.zsh, help
  panels, palette.map ALL generated projections. Zero duplication — but shell
  config becomes build-dependent (culture change; compose-first deploy.sh
  would gain a generate step).

## Constraints already known

- Frontmatter in .zsh must be comment-fenced (zsh can't host raw YAML) —
  or sidecar .md as the ONLY source (else drift returns).
- Migration = a real phase: 145 commands' help moves into structured blocks;
  heredoc panels become generated output.
- Whatever the shape, `palette-map-gen.py --check` evolves from lint-by-parse
  to schema validation — strictly simpler.

## Pointers

- v1 composer + registry: zsh/ai/palette-map-gen.py · zsh/registries/palette.json
- Precedents: ~/.claude/skills/*/SKILL.md (frontmatter) ·
  elements-factory bricks/python/pin-core (open-schema JSONL)
