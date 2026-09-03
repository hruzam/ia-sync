# A′ mechanism proof — palette v2 frontmatter projection

Isolated, mechanism-only proof of the A′ design
(`design.parked.v2-frontmatter-projection.md`, "The design fork — DECIDED").
Nothing here is wired into the real config. Every real `keyboard.zsh` /
`_*_help()` / `palette-map-gen.py` / `command-palette.py` /
`command-palette.zsh` stays byte-for-byte untouched.

## What this proves

1. **The alias line's trailing doc-comment is already the single source.**
   `palette-map-gen.py` requires ZERO changes — its `ALIAS_RE` already
   captures `# comment` and falls through to it as `help_str` when no
   heredoc/printf help exists. Proof `[a]`/`[b]` run the REAL generator,
   unmodified, against the isolated scratch root and show the help column
   in `palette.map` == the trailing comments verbatim.
2. **Help panels can become one generic live renderer.** `ai/palette-help.py`
   is a new, standalone, stdlib-only script that parses `# ── Section ──`
   headers and `alias NAME=... # HELP` lines with a regex identical in shape
   to `palette-map-gen.py`'s `ALIAS_RE`, and prints an aligned two-column
   panel — the `just --list` model, read live, no persisted artifact. Proof
   `[c]` runs it against the scratch fixture; `[d]` runs it — read-only —
   against the real, already fully-annotated `system/keyboard.zsh`, which is
   the stronger proof since it's zero-mutation on live config.
3. **The discipline check needs no new logic to catch missing help.**
   `--check`'s existing "[2] commands with no help line" already flags the
   comment-less fixture alias (`ax`). `palette-help.py`'s render also
   surfaces it directly as `(no help)` in the panel — visible in both the
   audit and the live view, not silently skipped.

## What a future MIGRATION session must still do

This proof does NOT migrate anything. The migration phase is separate work:

1. **Annotate the remaining ~153 comment-less aliases** across the other
   6 real `keyboard.zsh` files (everything besides `system/keyboard.zsh`,
   which is already done) with trailing `# help text` comments.
2. **Delete the heredoc/printf help harvesting** in
   `palette-map-gen.py`: remove `extract_functions_and_help`'s heredoc-style
   and printf-style passes, and delete `_harvest_help_lines` entirely. Once
   every alias carries its own trailing comment, `help_text` lookup by
   function name is no longer needed — `comment` is always the source.
3. **Simplify `--check`** so "missing trailing comment on the alias line" is
   the whole schema rule for help coverage (drop the box-table / sub-flag
   heuristics that exist only to parse heredoc bodies).
4. **Point each real `_<scope>_help`** at
   `_palette_help <that scope's keyboard.zsh>` (sourcing `ai/palette-help.zsh`),
   passing `--section` where a scope's existing panel is section-filtered.
5. **Delete the old heredoc `_*_help()` bodies** once each scope's live
   renderer is verified to reproduce (or intentionally improve on) the old
   panel's content.

Do all of the above only after step 1 (annotation) is complete for a given
scope — the live renderer's "(no help)" markers make incomplete scopes
visually obvious, so migrate scope-by-scope and diff the rendered panel
against the retired heredoc before deleting it.

## Files

- `registries/palette.json` — scratch-only registry (`scopes: ["scratch"]`),
  same shape as `zsh/registries/palette.json`.
- `scratch/keyboard.zsh` — fixture: 2 sections, 5 aliases, one (`ax`)
  deliberately without a trailing comment.
- `prove.sh` — runs the real generator + the new renderer against both the
  scratch fixture and (read-only) the real `system/keyboard.zsh`.
- `palette.map` — generated output of `prove.sh` step `[a]` (artifact, safe
  to regenerate/ignore).
