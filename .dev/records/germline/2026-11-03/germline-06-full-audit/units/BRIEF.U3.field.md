# BRIEF U3 → field (Flight, 2026-10-21) — personal programs: both CONTROLLERs and all five functions
Audit-only. Read in full; no edits outside your return file; no verdicts, no dispatch.

## Read in full (absolute paths)
1. /home/hruzam/reposoma/.majkee/.germline/programs/journal-continuity/CONTROLLER.md
2. /home/hruzam/reposoma/.majkee/.germline/programs/journal-continuity/fn/audit-beds.md
3. /home/hruzam/reposoma/.majkee/.germline/programs/journal-continuity/fn/carry-unfinished.md
4. /home/hruzam/reposoma/.majkee/.germline/programs/journal-continuity/fn/fold-entry.md
5. /home/hruzam/reposoma/.majkee/.germline/programs/journal-continuity/fn/list-pending.md
6. /home/hruzam/reposoma/.majkee/.germline/programs/project-saddle/CONTROLLER.md
7. /home/hruzam/reposoma/.majkee/.germline/programs/project-saddle/fn/saddle-project.md
8. /home/hruzam/reposoma/.majkee/AGENTS.md
9. /home/hruzam/reposoma/.majkee/engine/README.md
10. /home/hruzam/reposoma/.majkee/journal/2026-10-16.md — ONLY lines 1535–1560 and 1610–1630 (two recorded invocations; read with offset/limit, not the whole file)
Comparison references (already audited in U2 — read only the named sections): /home/hruzam/ia-sync/germline/agents/houston/identity.md §The three cards + §Card selection (≈ lines 50–65) and frontmatter (1–10); /home/hruzam/ia-sync/germline/agents/houston/binding.claude.md §Entry routes (25–53); /home/hruzam/ia-sync/claude/agents/houston.md (whole, 49 lines).

## One question
For each program and each function: what exactly does an agent consume, in what order, with what inputs, what it may/may not do (authority), what it returns, what happens on failure (hold / no fallback / stamp mismatch / missing file), and how continuity is carried — as the files literally state it. Then report where the two programs differ from each other and from Houston's identity/binding/card/wrapper shape, citing text.

## Hypotheses to TEST (report evidence for and against; do not conclude)
H1 Isomorphism: identity≈CONTROLLER invariants, card≈fn, wrapper≈launcher (invocation line `ctrl <program>&<fn>`), project addendum≈project-local function. Where does the mapping break?
H2 The CONTROLLER functions table (pinned stamps) plays the role of GAVELS G5's "small explicit binding table". Quote what the table actually binds (name → file → stamp → what else?).
H3 Table↔file stamp drift: who regenerates the table stamp when an fn file is edited? Is there a rule, a check, or nothing? Compare each table stamp against the `stamp:` in the fn file NOW (grep) and report matches/mismatches literally.
H4 project-saddle resolves the project by a shortlist/explicit argument, Houston by cwd walk-up: quote both mechanisms; state inputs each requires.
H5 Invocation grammar `ctrl X&Y` and `&&`: quote every place it is defined or used; note any divergence in form between the two CONTROLLERs and the journal invocations.
H6 Authority/return: do the functions name a destination and pen (who writes where), and what does "read-only" mean in each? Do the two journal invocations (:1544 audit-beds, :1620 saddle-project) match the function contracts in inputs/authority/destination?

## Return shape (write it yourself, verbatim, to the path below; then reply inline with ≤15 lines summary)
Return file: /home/hruzam/ia-sync/.dev/session/germline-06-full-audit/_bus/field.U3.return.md — header `from: field · unit U3 · date`, then:
A. Per-file table (10 rows): job for agent · inputs · authority · return · failure/hold · continuity · size (bytes) · stamp (if any) · line refs.
B. Program-vs-program differences (journal-continuity vs project-saddle), cited.
C. Program-vs-Houston mapping (H1), cited, with breaks.
D. H2–H6 evidence tables.
E. Friction list for an agent consumer (ranked, cited) — legibility only.
F. Contradictions (file vs file, file vs journal invocation).
G. Uncertainty / not-read.
Bounds: ≤ 4,000 words. Line numbers must come from the files as read today; quote text alongside each line ref. Separate authored/deployed/historical/proposed material (note: no `~/.germline/programs` exists — these are personal, undeployed files; say so). Stop when A–G are filled; do not extrapolate a personal trial into global law.
