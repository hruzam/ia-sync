# RESULT.U9 — retention vs rehydration vs recovery (C2 question sheet; no live test)
Flight · 2026-10-21 · inputs: _bus/field.U9.return.md (Field, verbatim), _bus/oraculum.assess.U9.return.md (Oraculum, verbatim; no experiment performed). Flight checks at the bottom. Audit-only: nothing run, no compaction, no model probe. The question sheet is copied, attributed, to `units/QUESTIONS.C2.compaction.md` for handoff to the germline-planning owner.

## 1. Intended job and consumer needs
Houston's meaning enters as tool reads (runtime load). After a compaction the agent must either still hold its identity, binding, addendum and card (retention), get them back (rehydration — by the harness or by its own re-read), or notice the loss and act (recovery). D2 (gaveled) says this is unverified and is later work for the germline-planning owner; no universal production gate follows.

## 2. Current knowledge (verified; three columns kept apart)
- **Retention — Claude, documented (E4, official docs 2026-10-21, re-confirmed):** ≤5 most-recently read/edited files ≤5k tokens each are re-injected after compaction; larger → path reference; CLAUDE.md + unscoped rules re-read from disk; skill bodies 5k/25k; "system prompt … still applies" (subagent `.md` body survival inferred, not documented). All seven germline files are under the cap (identity ≈2.5k, addendum ≈2.8k, bindings ≈1.4–1.8k, cards <1k). **Codex:** nothing documented. **Chatbots:** nothing.
- **Rehydration — design intent:** none written. The only "compact" string in `germline/`, the Houston wrappers or bindings is `tunnel/tunnel.preamble.md:4` ("read only STATUS.md and the files this message names; never the full read order") — Codex-only, operator-driven (ctx ~70 % → `tun compact` → one `ask`, feedback §3.9), and it restores the *bed*, not the *agent* (it does not name the germline load order). The "per-reply stamps make loss visible" reading (RESULT.U6 §3) is an inference and weak as written: a model can re-emit a stamp from its own earlier replies or from the compaction summary.
- **Recovery — rule gap:** wrapper :44 "a file missing or unreadable is my first finding" is a *disk* predicate; after compaction the file is readable and the rule never fires. No Claude-side recovery routine exists.
- **Slot competition is arithmetic, not observation:** nobody has watched a transcript. Correction to Field: CLAUDE.md is harness-injected, not a tool read, so it does not occupy a slot (inferred from E4 listing it as a separate path — flagged for Q1); the real displacers are the bed files a Houston child reads for its card, so 4 germline files + card inputs ≥ 5 within the first turn of any real consult.
- **No contradiction** across Janus C2 (:20 proposed pilot shape; :27 Majkee: not a universal gate), G04 HANDOFF (silent), D2 (broader wording). Drift: the concrete pilot shape lives only in G05 evidence.
- Field's F-caveat (Sella 5k/25k CONFIDENCE-L) is superseded by E4.

## 3. The lever (Oraculum; Flight concurs)
A quoted stamp after compaction is **three-way ambiguous** — retained · re-read · echoed. The states are separable only by what the child transcript shows between the compaction boundary and the answer, never by the agent's self-report. The sheet therefore uses a controlled disk change (re-roll a *throwaway* project addendum's stamp between load and compaction) plus the transcript's Reads-after-boundary.

## 4. GUIDE/reference vs agent-consumable
Reference: E4 facts → Sella R01 paging row + the L7 dated note (D11); the outcome key and results → the germline-planning bed. Agent-consumable *only if adopted*: one re-read-trigger sentence.

## 5. Program/controller/skill/agent appropriateness
No mechanism. One candidate design sentence (not a test): "If my window contains a compaction summary, or I cannot quote a stamp from file content now in my window (not from my own earlier replies), I re-read the load order before any further card work and say so in one line." Destination proposal: **binding.claude §Entry proof** (compaction is a vendor mechanism; no canary re-roll, no wrapper re-witness), Codex twin in binding.codex pointing at the preamble; at most one principle line in identity ("my authority is what is in my window now, not what I once read"). Not wrapper step 5 (bootstrap law; re-rolls canaries; re-witness per route for one sentence). Alternatives: no sentence until the pilot; identity-only principle. **Must not land before the pilot's baseline arm** — else Q9 measures the rule, not the mechanism.

## 6. The question sheet (summary; full text in `units/QUESTIONS.C2.compaction.md`)
Nine questions, one common procedure (fresh head, throwaway bed with its own addendum, entry proof, controlled read sequence, canary edit on the throwaway addendum, forced compaction — `/compact` on main, fed reads on child — probe, child-transcript read), one universal outcome key (RETENTION · REHYDRATION-harness · REHYDRATION-agent · ECHO · RECOVERY), PASS rule = TEST-INSTALL §3 three-part. Q1 empty-bed survival of the four entry files · Q2 displacement by ≥5 / 3 later reads · Q3 the consult fence after compaction (Janus's shape, credited) · Q4 wrapper body, child vs main · Q5 Codex `tun compact` + preamble intent · Q6 stamps: current tokens or echoes · Q7 main vs child · Q8 priority under scarcity (addendum vs identity — prediction: recency wins, the inversion of L7) · Q9 recovery trigger, arms A (baseline) / B (candidate sentence). Pre-conditions: office; current revisions; land the pending mech bundle first; no re-read rule before arm A. Record shape: `raw/PILOT.compaction.<route>.<date>.md` in the germline-planning bed, TEST-INSTALL §3 form. Authorization: Majkee's word only; G06 dispatches nothing. Each Q states what the owner may and may NOT conclude — never a production gate (Majkee :27; D2).

## 7. Fold destinations (nothing applied)
| what | primary | alternative |
|---|---|---|
| the sheet | germline-planning bed (does not exist yet — E5) or by mail to Cartan per HANDSHAKE | findings.g06 P1 inline |
| re-read trigger sentence (if adopted) | binding.claude §Entry proof + binding.codex twin | identity principle line |
| preamble: name germline files? | tunnel.preamble.md :4 second clause (Codex) — after Q5; owner tunnel guide + Cartan | rule in the `ask` template |
| E4 facts | Sella R01:185 + L7/D11 note (P2) | findings.g06 only |

## 8. Decisions
**Not G06's (Majkee / germline-planning owner):** run the pilot, which arms and routes; adopt the re-read sentence and where; change the tunnel preamble; load-order priority under scarcity; treating any outcome as a gate — **already answered no**. **Mech (recorded here):** Field's F-caveat superseded; CLAUDE.md-not-a-slot flagged as inference for Q1; sheet handed via the handoff; Sella L7/D11 note (P2 bundle). No DEC file: nothing here is ripe for a gavel; the sheet is a design handed to its owner.

## Flight verification log
Verified today: `grep -ri compact` over germline/ + Houston wrappers → only tunnel.preamble.md:4; janus.c2.return :16/:20/:27 text; G05 `_bus/` listing; tunnel GUIDE has no "compact" string (Field cited preamble delivery lines, not compaction). Accepted on Field/Oraculum quotes: E4 wording (my own earlier return); findings.q1 :39–57, :246, :305–306; umbrella N2 :77; tunnel GUIDE :50–52, :79, :120–122; feedback §3.9; RUNBOOK :60–61; D2 :46. Inferences flagged: CLAUDE.md not a slot; a visible compaction summary message in the window (Oraculum, high confidence; consistent with this session's own compaction); subagent body = system prompt layer. Not read: tunnel/res/preamble.md; any `.jsonl`.
