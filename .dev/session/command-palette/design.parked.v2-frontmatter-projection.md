# PARKED · palette v2 — frontmatter projection (single-source help/alias metadata)

> Locked for a later phase by @majkee, 2026-08-05, session flight.office.zsh-monitor.forked.
> Status: FORK DECIDED (2026-08-05, Flight MANNED — majkee delegated "pick your design").
>         BUILD still NOT scheduled — direction chosen, migration remains a parked phase.
> Decision: **Fork A, sharpened to A′ (just-informed)** — see "The design fork — DECIDED".
> Grounding: @Epoch date-calibrated survey 2026-08-05 (just v1.58.0, navi, pet, tldr,
>           fzf, PEP 723 / userscript metadata blocks). Returned inline (no research bed —
>           one-off design input, not a recurring radar scope).

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

## The design fork — DECIDED (Fork A, sharpened to A′)

Original fork:
- **A · metadata-in-script (pin variant):** comment-fenced structured block
  inside each engine/keyboard file. Composer reads it exactly (no heuristics).
  Shell files stay plain + sourceable, no build step. Residual duplication:
  aliases still hand-written.
- **B · full inversion:** frontmatter file is THE source; keyboard.zsh, help
  panels, palette.map ALL generated projections. Zero duplication — but shell
  config becomes build-dependent (culture change; compose-first deploy.sh
  would gain a generate step). **REJECTED** — the build-dependency is exactly the
  automation-layer-before-the-pain the global bias warns against.

**CHOSEN — A′ (Fork A, `just`-informed).** Epoch showed the field's lowest-friction
model is `just`'s doc-comment-on-the-definition, live-parsed, no sidecar, no build
step. Applied here that beats even the parked Fork A (which left the help heredocs
duplicated) and reaches Fork B's zero-duplication WITHOUT B's build-dependency cost:

1. **Single source = the alias line's trailing doc-comment** in each `keyboard.zsh`:
   `alias ts-ls='_ts_ls'   # formatted peer list`. Help text and invocation are the
   same statement in the same file — never written twice.
2. **Help panels become a generic LIVE renderer.** The hand-written `_<scope>_help()`
   heredocs are replaced by one function that greps the scope's `keyboard.zsh` for
   `alias NAME=... # HELP` and prints them — the `just --list` model. No persisted
   artifact, no heredoc duplication, read live at call time.
3. **palette.map stays composer-generated** (existing accepted step) but from those
   same alias-comment lines via ONE exact regex — killing the box-table/heuristic
   parsing. `palette-map-gen.py --check` becomes schema validation, strictly simpler.
4. **Scope = folder, engine = derivable from location.** No new fields needed: the
   palette filter already searches command + help, so tags are unnecessary. The
   PEP-723-style fenced structured block is held as the escalation path IF structured
   fields (e.g. tags, arg-schemas) ever become required — recognized precedent, not
   yet warranted.

**Risk ledger (what the pick buys / costs):**
- Buys: kills the parser heuristics AND the heredoc duplication; no sidecar; no new
  build-dependency; shell stays fully sourceable; `--check` gets simpler.
- Costs: help panels move from static heredocs to a live grep-render (tiny runtime
  cost per `*-help` call, negligible); migration is still a real phase — 145 commands'
  help must move onto the alias lines and the heredoc panels be deleted.
- Does not foreclose: PEP-723 fenced block remains a clean upgrade if tags ever land.

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
