# BRIEF U6 → field (Flight, 2026-10-21) — GUIDE layering: Sella and Germline Forge vs the system as it is
Audit-only. Read in full; no edits outside your return file; no verdicts, no dispatch.

## Read in full (absolute paths)
1. /home/hruzam/reposoma/raw.guides/germline-forge/GUIDE.md (whole, incl. frontmatter/banner)
2. /home/hruzam/reposoma/raw.guides/germline-forge/res/checks.md · res/fold-scheme.md · res/witness.md (whole) — and Glob `raw.guides/germline-forge/**` for any other file (manifest, README, index) and list it
3. /home/hruzam/reposoma/raw.guides/sella/GUIDE.md — whole if ≤ 40 kB; otherwise frontmatter + every section whose heading or body mentions: layering, seams, kernel/userland, L1, L7, identity, tool-read, compaction, paging, germline, vendor facts, half_life, and the vendor-dated list (≈ :185, :208–217, :275). Report which sections you read.
4. /home/hruzam/reposoma/raw.guides/guide/GUIDE.md or the guide-writer law the `/guide` skill names ("3-line writer law", staleness/mirror warnings) — locate it under /home/hruzam/reposoma/raw.guides/ (Glob `*/GUIDE.md`, grep "writer law|half_life|stale|banner"); read the staleness/banner rule only.
5. /home/hruzam/ia-sync/.dev/session/germline-06-full-audit/findings.g06.md — "Guidance pass" and "E4 vendor facts" sections only (prior checked evidence; reuse, do not redo).

## Facts to compare against (Flight-verified, current system — treat as ground truth for staleness classification)
- Source `~/ia-sync/germline/` → `deploy.sh deploy_germline()` → real `~/.germline/` (never a symlink); office migrated 2026-10-14; `~/reposoma/.germline/` is a stale fork read by chatbots via CHATBOT.md.
- Houston = thin wrapper (runtime-load, canary) → identity → binding.<vendor> → addendum (cwd walk-up) → card; stamps 8-hex regenerated on edit; no render/ directory anywhere; zero "derived from" instances.
- Global bindings exist and are live (binding.claude cf14943f, binding.codex 0c812f6c); project bindings were deleted 2026-10-10; project layer = addendum only.
- Witnesses: Assay fresh-session rows C1–C4, X1, X2, P1, C-def(FAIL)/C-def.2/C-def.claude, COEX (2026-10-13..17), PASS rule = tokens + transcript reads + model/effort.
- Programs: personal `.majkee` CONTROLLER + fn table with pinned stamps; GAVELS G1–G7 planning-only; D1/D2/D4 accepted 2026-10-21 (shared agent definition + shared programs; runtime load is the working design, compaction unverified; project layer = explicitly attached local layer).
- Compaction (official docs 2026-10-21): ≤5 recently read files ≤5k tokens each re-read; larger → path reference; subagent .md body survival undocumented.

## One question
For every Forge chapter and every Sella section read: what does it teach (doctrine) vs assert as fact (dated vendor/system fact) vs prescribe as procedure (checks, fold steps, witness steps); which assertions are stale against the facts above (quote both); which procedures describe a model that no longer exists (render/derived-from/project bindings/symlink) vs still apply to runtime-load; and what layering the guides themselves claim (what is law, what is reference, what points where). Then: which guide text an *agent* would need at runtime (should it be in germline instead?) and which is human explanation that belongs in the GUIDE.

## Hypotheses to TEST
H1 Forge GUIDE.md carries a staleness banner (dated 2026-10-14) but res/* chapters do not — quote banner text and confirm absence in each chapter.
H2 Forge res/checks.md is written for the render model (build-time); list each check and mark: still meaningful for runtime-load / meaningless / needs a runtime-load twin (e.g. stamp quote check, canary check, witness rule).
H3 Forge res/witness.md vs the G01 PASS rule (tokens + transcript reads + model/effort; child transcript not relay): which witness steps match, which are missing, which are extra.
H4 Sella L1/L7 kernel/userland text: quote exactly; state what it predicts for tool-read identity; note whether Sella offers any mitigation or test. Does Sella anywhere discuss compaction re-read of tool results?
H5 Sella vendor-dated facts (claude 2.1.292, codex 0.160.0, 5k/25k paging, background default, omitClaudeMd, /agents wizard) — quote each with line; findings.g06 E4 already classified them (CONFIRMED/CONTRADICTED) — carry the classification, do not re-verify.
H6 Layering claims: does either guide say which of its statements are law vs reference vs pointer? Does the guide-writer law (item 4) require a banner/half-life/verified date, and do Forge/Sella comply (frontmatter fields present? dates?)?
H7 Agent-need vs human-explanation: list Forge/Sella passages that state an operating rule an agent needs at runtime (e.g. stamp rule, card selection, witness-before-proven) and whether germline already carries the same rule (cite germline file:line) — i.e. duplication across GUIDE↔germline.

## Return shape (write yourself, verbatim; then ≤15-line inline summary)
Return file: /home/hruzam/ia-sync/.dev/session/germline-06-full-audit/_bus/field.U6.return.md — header `from: field · unit U6 · date`, then:
A. File/section inventory (path · size · frontmatter fields: verified/half_life/banner · sections read).
B. Claim table per chapter/section: claim (quoted, line) · type (doctrine | dated fact | procedure | pointer) · status vs facts above (current | stale | superseded-model | unverifiable) · note.
C. H1–H7 evidence tables.
D. GUIDE↔germline duplication map (rule · GUIDE loc · germline loc · same/diverged).
E. Friction for a seat that reads the GUIDE first (ranked, cited).
F. Uncertainty / not-read.
Bounds: ≤ 4,000 words; quote text with each line ref; line numbers from files as read today. Stop when A–F are filled.
