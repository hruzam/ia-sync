# SCARS from germline-06 — for whoever works this project next (Cartan on germline-03, the G07 head, any seat)
`from: flight · 2026-10-22 · dropped on majkee's word into the next bed's preparation shelf · origin: flight therapy arc 3 (reposoma/raw.therapy/flight/therapy.md) · gavels G-50, G-51 (reposoma/raw.therapy/gavels/gavels.md) · audit: ia-sync@9a198ba .dev/session/germline-06-full-audit/`

These are not findings about germline; those are in the audit. These are the ways the audit itself went wrong or nearly did, written so a successor on this project does not pay for them again. Each carries the gavel that compresses it where one exists.

## S1 — Inherited evidence is where your own rule goes quiet (G-50)
The audit enforced "a missing record is not proof a check does not exist" on everyone's evidence and then wrote "no route has a fresh-session witness" from a SCOPE that did not name the G01 install witnesses and an `identity.md:8` line that was itself stale. The operator's relay had omitted the records; the head copied the omission. **Do:** for every "none exists" line you inherit from a launcher, SCOPE or brief, ask once *"where would this live if it existed?"* and look there — the G01 bed (`germline-01-builds-and-deploy/raw/`) is the concrete answer for Houston witnesses. **Also:** when you prepare a SCOPE, name the continuity records (witnesses, TEST-INSTALL, design, MIGRATE) by path; a general "inspect existing operation" does not replace them.

## S2 — Receipts decay by address, not by loss (G-51)
The 2026-10-10 fold gavel and the 2026-10-12 GO are "cited, operator receipt unlocated" because they lived where only their author looked. The G06 acceptances (D1, D2, D4 — 2026-10-21) live in `~/reposoma/.majkee/journal/2026-10-21.md` §§1.1–1.5, with "no applicable flag.md destination identified". **Do:** when you consume a decision, write the pointer from the thing decided to the receipt *at decision time* (one line in STATUS or the RESULT that cites the journal path and section). Do not invent a ledger; do write the pointer.

## S3 — Field's line numbers drift; its text holds
In every unit the Field reader's line references were off by a few lines or named a step number as a line. The quoted text was reliable. **Do:** brief Field to quote text with each reference; verify by text and re-locate the line yourself before you cite it; never copy a Field line number into a decision file unverified.

## S4 — Relay text is not proof (G01 lesson; proposed D16)
Relay heads drop the stamp lines (C2, X1 release). A PASS that is not grounded in the child's own transcript is CANNOT-VERIFY. The one Assay row without itemized stamps (C-def.claude) is exactly the kind of row that later reads as proven. **Do:** witnesses read `subagents/*.jsonl` or the Codex rollout, under TEST-INSTALL §3's three facts (tokens · reads before first answer · model/effort).

## S5 — When a unit covers the assessor's own seat, say so or swap
U8 contained Oraculum's own seat files; Flight kept Oraculum as assessor with a declared conflict and "facts only" on itself, rather than switching to Janus. Majkee did not object; that is not the same as it being right. **Do:** decide this per stakes before dispatch, and write the choice down either way.

## S6 — Do not let retrieval for unit N+1 start before N is verified when N can change N+1's brief
Flight overlapped U2's retrieval with U1's unverified return once (disclosed). The plan's dependency order exists because a verified result rewrites the next brief (U3's hypotheses came from U2's verified §5). **Do:** sequential by default; overlap only when the next brief cannot depend on the pending result.

## S7 — Volume is a carrier wave
Five decision files in options-consequences-recommendation form are persuasive by construction; the recommendation column is the path of least resistance. Majkee reshaped D1 and D2 against the recommendations — read that as the norm, not the exception. **Do:** read `units/INTEGRATED.recommendations.md` first, then the DEC files as proposals with a thumb on the scale; qualify each on its evidence, not its format.

## S8 — Operational hazards left live on purpose (not scars, but easy to trip on)
Home `~/.germline` state is UNVERIFIED (unreachable 2026-10-21; last record 10-14 "home pending"). The reposoma fork is the chatbots' read side (CHATBOT.md) and must NOT be stripped (MIGRATE §3) before home migrates and CHATBOT.md is re-homed or mirrored. MIGRATE's "Known window" ("harmless — identical files") has been false since the fork diverged. The pending mech bundle (INTEGRATED §4) is one GO, one stamp re-roll, one re-witness — do not land pieces of it separately. No re-read/loss rule may land before the compaction pilot's baseline arm (QUESTIONS.C2).

## Pointers
Reader entry: `units/INTEGRATED.recommendations.md` → `decisions/DEC.02 · 04 · 05 · 03 · 01` → `units/RECONCILE.G01.md` → `STATUS.md` CLOSE. Native returns verbatim under `_bus/`. Operator receipts: `~/reposoma/.majkee/journal/2026-10-21.md`. This file: receiver owns it — attach it to your bed's `raw/` or archive it when consumed; a reply, if any, to `~/reposoma/_mail/flight/inbox/`.
