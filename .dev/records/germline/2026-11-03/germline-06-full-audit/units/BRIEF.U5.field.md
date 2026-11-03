# BRIEF U5 → field (Flight, 2026-10-21) — project layer: addenda, retired roles, resolution
Audit-only. Read in full; no edits outside your return file; no verdicts, no dispatch.

## Discover, then read in full
0. Inventory every project-layer file: Glob `/home/hruzam/unikuklatrix/*/.germline/**/*.md`, `/home/hruzam/ia-sync/.germline/**/*.md`, `/home/hruzam/reposoma/.germline/agents/**/*.md`, `/home/hruzam/reposoma/.majkee/.germline/**/*.md` (list only — programs were U3), and any other `<project>/.germline/` you can find under /home/hruzam/{unikuklatrix,ia-sync,reposoma,projects} (depth ≤ 3). Report the full list with sizes and `stamp:` presence. Exclude the global source `/home/hruzam/ia-sync/germline/` and the deployed `/home/hruzam/.germline/`.
1. /home/hruzam/unikuklatrix/nablarva/.germline/agents/houston/nablarva.md (the only known addendum; whole)
2. /home/hruzam/unikuklatrix/nablarva/.germline/agents/convergence.md (retired keeper; whole)
3. /home/hruzam/unikuklatrix/nablarva/AGENTS.md — the Houston paragraph(s) and any `.germline` mention (grep, ±8 lines)
4. /home/hruzam/unikuklatrix/nablarva/PROJECT.yaml — lines 1–30
5. /home/hruzam/unikuklatrix/nablarva/.dev/session/flag.md — ONLY the L16 clause block (grep `L16`, read the clause list; cite the lines the addendum points at: L16.6–8, L16.9, L16.14)
6. /home/hruzam/ia-sync/germline/agents/houston/identity.md :138–150 (§Saddle: "a later layer specialises, never overrides") and :110–116 (flag pointer)
7. /home/hruzam/ia-sync/claude/agents/houston.md :29–34 (walk-up) and /home/hruzam/ia-sync/germline/agents/houston/binding.claude.md :42–46 (placement + CWD), binding.codex.md :54–58
8. /home/hruzam/ia-sync/.dev/session/germline-06-full-audit/units/RESULT.U3.md §5 bullet "Alias vs walk-up" and RECONCILE.G01 §2 D4 wording (context only)

## One question
What does the project layer actually consist of today (files, per project), what does the one real addendum carry (context/paths/locks vs procedure/authority/method), how is it selected (walk-up rule, basename match, ambiguity, exclusion of global), how are retired roles marked (convergence.md), and where does the addendum point into project law (flag clauses) — as the files literally state it.

## Hypotheses to TEST (evidence for/against; no conclusion)
H1 D4 fit: the addendum carries only "project context, paths and applicable locks" (D4) and "may add paths, procedures and local method; may not override the identity or any lock" (nablarva.md:4) — list every sentence in nablarva.md that is procedure/authority/method rather than context, and any that could be read as overriding identity/binding text.
H2 Selection: walk-up matches `.germline/agents/houston/<ancestor-basename>.md`; nablarva.md's basename = `nablarva` = repo dir name. What happens for a project whose dir name ≠ intended addendum name, for a cwd in a subdirectory, for two ancestors each with an addendum, for a session started outside any project? Quote the rule text and note what it leaves unsaid. Does any file define "explicit project declaration overrides walk-up"?
H3 Retired role: convergence.md — does it carry any in-file marker (frontmatter `state:`, "retired", tombstone)? nablarva.md says it is retired as keeper (quote the line). Is there any rule anywhere for how a retired germline file is marked?
H4 Flag pointers: do nablarva.md's `locked: L16.x` cites match the clause texts in flag.md today (quote both)? Any `inferred:` tags in the addendum (e.g. :39 audit landing path) — list all with text.
H5 Placement rule: "projects carry no Houston wrapper" (binding.claude:42–44; nablarva.md ~:112–113) — verify `nablarva/.claude/agents/houston.md` and `nablarva/.codex/agents/houston.toml` are absent (Glob); list what nablarva/.claude/agents/ and .codex/ DO contain.
H6 Stamp + provenance: nablarva.md frontmatter (stamp d9ee9067 expected, `revision:`, `updated:`) — quote; does the addendum say who re-stamps it and where its witness record lives?
H7 Other projects: does any other project have an addendum, or a `.germline/` folder with other content (e.g. ia-sync's own)? What does the reposoma `.germline/` contain that is project-scoped (expected: nothing)?

## Return shape (write yourself, verbatim; then ≤15-line inline summary)
Return file: /home/hruzam/ia-sync/.dev/session/germline-06-full-audit/_bus/field.U5.return.md — header `from: field · unit U5 · date`, then:
A. Project-layer inventory table (path · size · stamp · role · live/retired/historical).
B. nablarva.md section map (section · what it carries · class: context | paths | locks | procedure | authority | history | inferred).
C. H1–H7 evidence tables (quote text with every line ref; line numbers from files as read today).
D. Contradictions / stale (file:line, quote, what is true today).
E. Friction for a cold Houston entering a project (ranked, cited).
F. Uncertainty / not-read.
Bounds: ≤ 3,500 words. Separate authored / deployed / historical / proposed. Do not read flag.md beyond the L16 block. Stop when A–F are filled.
