# BRIEF U9 → field (Flight, 2026-10-21) — retention vs rehydration vs recovery: the evidence for a question sheet (NO test)
Audit-only. Read in full; no edits outside your return file; no verdicts, no dispatch, no web, **no compaction or model experiment of any kind**.

## Read in full (absolute paths)
1. /home/hruzam/ia-sync/.dev/session/germline-06-full-audit/findings.g06.md — "E4 vendor facts" section (checked platform facts, official docs 2026-10-21) and "E5 / C2" section
2. G05 preserved C2 material (read at the preservation commit's working-tree copies): /home/hruzam/ia-sync/.dev/session/germline-05-sella-germline-audit/_bus/janus.c2.return*.md (Glob; whole) · …/_bus/oraculum.assessment.umbrella*.md — the C2 / compaction / pilot section only (grep "C2|compaction|pilot|retention|rehydrat") · …/findings.q1.md — F1 and C2 passages only
3. /home/hruzam/ia-sync/.dev/session/germline-04-wiring-plan/raw/HANDOFF.g06-make-program.md — any pilot / P1 / compaction passage (grep)
4. /home/hruzam/reposoma/raw.guides/sella/GUIDE.md :180–190 (paging row) and :290–300 (L7) — already classified; quote only
5. /home/hruzam/reposoma/raw.guides/tunnel/GUIDE.md — the context/compaction routine (grep "compact|70 %|preamble|ctx", ±10 lines) and /home/hruzam/ia-sync/germline/tunnel/tunnel.preamble.md (whole, small) — the one *existing* recovery routine in the house
6. /home/hruzam/ia-sync/.dev/session/germline-06-full-audit/raw/feedback.houston-install.oraculum.2026-10-21.md §3.9 only (tunnel compaction routine as practised)
7. /home/hruzam/reposoma/.majkee/journal/2026-10-21.md :39–54 (D2 accepted wording — retention and rehydration unverified; validation = later work, germline-planning owner; no universal gate)
8. Load-set sizes (Flight-measured, reuse): wrapper 2,967 B · identity 10,179 · binding.claude 5,688 · binding.codex 7,054 · nablarva addendum 11,261 · consult 2,983 · audit 2,311 · sitting 1,291 → Claude child ≈ 33 kB ≈ 8.3k tokens; Houston quotes stamps on EVERY reply (binding.claude :65–67); the consult write fence is card prose only (G01).
9. Glob /home/hruzam/ia-sync/.dev/session/*/raw/*compaction* and /home/hruzam/reposoma/_cold-start/**/*compaction* — list any existing compaction observation/issue cards; read any ≤ 3 kB.

## One question
What does the corpus already know, claim or assume about (a) RETENTION — which loaded germline text stays in the model's context across a compaction (kernel vs tool-result layers; the ≤5 files / ≤5k-token re-read rule; what degrades to a path reference), (b) REHYDRATION — what the design *intends* to be re-read after compaction and by whom (the wrapper? the agent on its own? the operator via `tun compact` + one `ask`?), (c) RECOVERY — what the agent does when it notices loss (stamp lines missing → re-read? the "a file missing or unreadable is my first finding" rule?) — and which of these are documented mechanism, design intent, agent-authored assumption, or untested. Separate the three strictly; separate Claude from Codex from chatbot.

## Hypotheses to TEST (evidence; no conclusion; NO experiment)
H1 Retention: E4 says ≤5 recently read files ≤5k tokens each are re-read after compaction; identity ≈2.5k tok (under cap), addendum ≈2.8k tok, bindings ≈1.4–1.8k, cards <1k — so the five entry files fit the count but compete with later reads for the 5 slots; the wrapper body (system prompt) survival is "inferred, not documented". Quote E4; list which of the 5 loaded files would survive under which read sequence (no test — arithmetic from the documented rule only). Codex: does any read source state Codex's compaction behaviour? (feedback §3.9 `tun compact`; E4 silent?) Chatbots: anything?
H2 Rehydration intent: does the wrapper/binding/identity say "re-read after compaction"? (grep "compact" in germline/ and claude/agents/houston.md, codex/agents/houston.toml) — quote or report absence. Does the stamp-every-reply rule (binding.claude :65) function as a *detector* of loss by design (quote any text saying so) or is that an inference (RESULT.U6 §3)?
H3 Recovery rule: identity/wrapper "A file missing or unreadable is my first finding; I never reconstruct its content from memory" (wrapper :44) — does it cover *content lost from context* (file still readable on disk) or only unreadable files? Quote; note the gap if any.
H4 Existing routine: tunnel preamble routine (ctx ~70 % → `tun compact` → one targeted `ask` naming STATUS.md + the cited _bus file — never the full read order) — quote; is it Codex-only? operator-driven? Does any Claude-side analogue exist?
H5 G05 C2 state: what Janus's c2 return concluded (the "earlier experiment is not a universal production gate" line — quote), what the umbrella proposed as pilot, what G04 HANDOFF carried as P1, and what D2 now says. Any contradiction between them?
H6 Measurables already named anywhere: list every concrete, testable statement found (e.g. "ask for the Hard limits after forced compaction", "which is retained vs which must be re-read", "≤5 files", "5k tokens", "70 %") with its source line — these become the question sheet's rows.
H7 Ownership: who owns the pilot (germline-planning Cartan per RUNBOOK/E5; D2 "germline-planning owner") and what authorization a live test needs (RUNBOOK: "Force-compaction/live model tests are not authorized by this preparation") — quote.

## Return shape (write yourself, verbatim; then ≤15-line inline summary)
Return file: /home/hruzam/ia-sync/.dev/session/germline-06-full-audit/_bus/field.U9.return.md — header `from: field · unit U9 · date`, then:
A. Three-column knowledge table: RETENTION / REHYDRATION / RECOVERY × (documented mechanism · design intent · agent assumption · untested), per vendor (Claude · Codex · chatbot), each cell cited or "nothing found".
B. H1–H7 evidence tables (quote text with every line ref).
C. Measurables list (candidate question-sheet rows: statement · source · what would falsify it · which vendor).
D. Contradictions / drift between G05 C2 material, G04 HANDOFF, D2 and the feedback.
E. Friction for an agent that has just been compacted (ranked, cited) — legibility only.
F. Uncertainty / not-read.
Bounds: ≤ 3,500 words. Stop when A–F are filled. Repeat: no experiment, no compaction, no model probe.
