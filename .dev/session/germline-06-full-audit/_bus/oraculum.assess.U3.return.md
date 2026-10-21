---
from: oraculum · unit U3 · date 2026-10-21
---

Audit-only assessment of the personal programs (`~/reposoma/.majkee/.germline/programs/`, 7 files, 17,254 B measured; `~/.germline/programs` absent — checked). Everything below is legibility, not behaviour: the two recorded invocations (journal 2026-10-16 :1544 audit-beds, :1620 saddle-project) are briefs with no captured response; fold-entry, list-pending, carry-unfinished have no recorded invocation at all. Tags: `said:` = quoted text · `inferred:` = my reading. Field's line numbers drift; mine were re-located today.

**Governing insight.** The personal programs and Houston are complementary halves of the D1 target, each missing exactly what the other has: the programs have a stamped public procedure index but no native entry (no deployed launcher, no canary, no proof, no invoker); Houston has a native entry (wrapper, bindings, cards, proof) but no public procedure. The CONTROLLER functions table is *not* G5's binding table — it is the public index that G4/G5 presuppose (GAVELS :162 "the controller table remains the sole index"), while G5's table is the vendor-native adapter Houston's `binding.<vendor>.md` already is. Read this way, D1 coexistence has no collision to resolve; it has a seam to name.

## (1) What each shape gives the agent that the other does not

**CONTROLLER+fn gives, identity+card lacks:**
- An *expected-value* integrity check at load. `said:` journal-continuity CONTROLLER :54 "Load only the selected table binding; require matching program/stamp before its procedure runs." The agent knows the stamp before it reads the fn. Houston's entry proof echoes the token "copied from that file's frontmatter" (wrapper :41–42) — an *observed* value reported to a human; only the wrapper canary is pinned. `inferred:` the table detects index↔file drift agent-side; Houston detects source↔deployed drift operator-side. Different drift, different detector.
- Shared role vocabulary defined once (`journal-source` · `owner-state` · `destination`, CONTROLLER :34–37) and horizon semantics once (:39–43), reused by all fns. Field's friction 3 (fns do not redefine horizon) is the designed load order, not a defect: engine README :12 orders AGENTS → controller → fn, and CONTROLLER :21 says "Point rather than restate".
- An explicit single-line guarantee: `said:` "Controller plus selected function and named inputs suffice; no other function is a prerequisite" (:56). Houston has no such sentence; the load order is the guarantee.
- A uniform hold rule for unknown id / missing file / mismatch (:55; project-saddle :54–55).

**identity+card gives, CONTROLLER+fn lacks:**
- A deployed native entry: wrapper file, route line, canary, first-reply proof (wrapper :22–42). `said:` engine README :3–4 — the `ctrl` grammar "is prompt guidance, not a shell command, parser, skill, or auto-discovery." `inferred:` consequence: the CONTROLLER's "require matching stamp before its procedure runs" is unobservable — no proof line is prescribed, so a human cannot tell whether the check ran. This is the sharpest single gap on the program side.
- Invoker roster per card (identity :53–55 "the session head, or the operator" / "the operator, ad hoc"). Programs name no invoker; G6 says they should not ("private cards retain invokers/grants", GAVELS :129).
- Vendor mechanics (bindings), route child/main, card-selection defaults, delegation rules, `out of card:` refusal, evidence tags `said/inferred/locked`, no-standing-presence clause. None in the programs.

**Field's H1 breaks, re-graded:**
- *Per-card authority vs flat invariants* — overstated. The pen *is* differentiated, at the fn level: `said:` audit-beds :10 "never write or tick"; list-pending :10 "No writes."; fold-entry :11 "writes only `destination`"; carry-unfinished :11 "write only authorized source/destination journal scopes"; saddle-project :11 "this function writes nothing". `inferred:` an fn file is card+procedure fused; the controller invariants are flat because the differentiation moved down one level. Both programs state they grant nothing (CONTROLLER :32 "This procedure grants no tool capability or authority"; project-saddle :23–24) — these pens are ceilings/requirements, which is exactly G6's "public programs require capabilities but grant none".
- *Verdict taxonomy* — partly wrong. saddle-project has a two-value verdict (`READY`/`HELD`, :28–31). list-pending :20–21 and carry-unfinished :17–18 each carry a five-way finding classification — and they differ ("checked-current / journal-only / stale-conflicting / parked / unknown" vs "still actionable / parked-unanswered / resolved / stale-conflicting / unknown"). `inferred:` the true break is *uniformity*: Houston's taxonomy is identity-level and one; the programs' are per-fn and two, inside one program. Small, real, mech.
- *Deployed canary/proof vs textual `ctrl`* — correct, and the consequential one (above).
- *Walk-up vs alias* — see (4); the H1 leg "addendum ≈ project-local function" is itself the weak mapping: D4 calls the addendum "an agent-specific local layer carrying its project context, paths and applicable locks" — context, not a procedure.

## (2) Is the functions table G5's "small explicit binding table"?

No — it resembles it and is a different object. `said:` G5 (GAVELS :115–121): "A **vendor-native surface** may maintain a small explicit binding table from named public program capabilities/functions **to its harness or CLI mechanism** … native translation, qualification and evidence adaptation only. It is not discovery, a task router, a function census or an alternate procedure home." `said:` G4 acceptance (:162): "the controller table remains the sole index." `inferred:` the CONTROLLER table is the *public index* (a function census, legitimately — it is the one place G5 says the native table must not be); the G5 table maps *from* that index *to* a vendor mechanism. The programs have no G5 table at all — `ctrl` is prose, not a native route. Houston's `binding.<vendor>.md` is G5-shaped (U2 §5 stands) but has no public index to bind from. So my U2 hypothesis "the functions table plays G5's role" is withdrawn; the corrected statement is: *programs hold the index half, Houston holds the adapter half.*

**What the table binds** (`said:` CONTROLLER :47–52): function id → occasion → relative file path → expected stamp → result type. **Unbound:**
- Stamp regeneration. `said:` no sentence in any of the ten files names who re-rolls the table stamp when an fn is edited; AGENTS.md :37–38 only requires "an explicit authoring request". `inferred:` because the table is inside the controller, an fn edit must cascade: fn stamp → table row → controller stamp (96a5974b / 0d7f2a36). Unstated.
- The controller's own stamp is pinned nowhere. engine README :17–20 maps program → controller path without a stamp; AGENTS.md :21, :28 point by path only. `inferred:` controller drift is undetectable agent-side; only fn drift is.
- AGENTS.md and engine/README.md carry no stamp (Field, confirmed). They are the first two reads in the prescribed order (README :12) and the only home of the grammar and program table.
- Vendor mechanism, invoker, date/timezone source: all left to the caller, by design.
- Name collision (legibility): "binding" now means three things — the table column `file binding`, G5's "binding table", and Houston's `binding.<vendor>.md`. For the GUIDE layer (U6), not a file repair here.

## (3) Boundary between an agent's own cards and shared programs — proposal with alternatives

D1 requires coexistence; G6 already draws the line in gavel text (`said:` :128–131): "public programs require capabilities but grant none; private cards retain invokers/grants/agent authority and may explicitly call public programs; public programs never depend on private cards."

**Proposal (G6 applied as a sorting test, no file merge/split presumed):**
- Text answering *who may ask, under which route, with which pen, in which return shape* → card (or binding, for route). Text answering *which files, in what order, what counts as evidence, how to classify, what to return, when to hold* → program (controller invariants + fn). Text answering *what to read first and how to prove it* → wrapper/bootstrap (U2 §6 rule).
- Direction of reference is one-way: a card may name `program&function`; a program never names a card, agent or invoker. Both personal programs already satisfy the program side (:32; project-saddle :23–27 "Preserve the runtime/seat identity").
- The fn-level pen sentences ("writes nothing", "writes only `destination`") stay in the fn as *ceilings*; the card supplies the grant up to that ceiling. Nothing to move.

**Alternative A — fn stays fused (status quo):** each fn remains card+procedure, consumed by hand (AGENTS.md :20 "performs the procedure by hand — no dedicated agent"). Cheapest; it is the trial. Cost: when a second consumer appears, authority prose is re-authored per consumer.
**Alternative B — programs stay personal, Houston keeps cards-only:** satisfies today's reality, contradicts D1 as a *requirement* for the audited target. Rejected unless D1 is re-worded.
**Alternative C — Houston cards cite a program today:** premature; the RUNBOOK :38 says "Journal-continuity is a provisional specimen, not a template for all programs." No program has an observed response. Named for U5/U7, not for now.

## (4) Explicit alias vs cwd walk-up — real tension or two shapes?

Two legitimate shapes for two consumers, with one category error cleared.

- `said:` project-saddle :16 "never infer attachment from cwd, remembered work, a journal mention, or a similarly named folder"; saddle-project :13 "Match the explicit alias exactly to the controller's shortlist." `said:` Houston wrapper :28–33: resolve cwd, walk ancestors for `.germline/agents/houston/<ancestor-basename>.md`, "Ambiguous cwd or selection → I report it before card work and do not guess a project. None found → I am neutral Houston."
- `said:` G4 (:98–107) forbids *global-controller + project-local-function composition* "inferred from files being present". `inferred:` G4 governs composition of a *program line*; the addendum is context (D4), not a function. The walk-up does not compose a program line, so G4 does not literally bind it. U2 §5 raised this as a test; the test result is: no G4 violation, by category.
- `inferred:` why the shapes differ: myShell's cwd is always `.majkee/` inside reposoma — a walk-up would resolve *every* task to reposoma, so an alias is the only mechanism that can reach ia-sync, nablarva or freya. Houston is spawned *into* a project cwd by a head that chose that cwd — the cwd is a supplied input, and the hold on ambiguity (wrapper :33) is the saddle's "report the exact gap" in another dress. D4's "explicitly attach" is satisfied by authoring the addendum file; cwd only *selects among* explicitly attached layers.
- The tension becomes real only when one consumer needs both: Houston asked about a project other than its cwd, or a program run as a spawned child. `inferred:` then one sentence resolves it — an explicit project declaration in the assignment overrides the walk-up and is echoed in the entry proof. Belongs to U5 (project layer), mech; no decision now.

## (5) GUIDE/reference vs agent-consumable

- **Agent-consumable:** both CONTROLLERs in full (invariants, roles, horizon, table, hold rule); the five fn files; AGENTS.md :5–10 (seat precedence), :20–24 (function names fold/pending/audit → fn ids), :35–38 (write fence).
- **Reference / human:** engine README :29–40 expanded prompt template, :42–62 examples, :64–79 saddle examples, :81–93 "myShell routine and human relays" (relay tags are for Majkee; :93 "does not send messages, spawn agents, or grant writes"); CONTROLLER :58–60 optional snapshot shape; journal 2026-10-16 §"worked shapes" (`said:` :1535–1537 "explanatory only: no packet below is active").
- **Mixed, and that is the friction:** engine README :9 (grammar) and :17–20 (program → controller table) are the *only* home of the entry mechanism, embedded in a document that declares itself "prompt guidance". `inferred:` the agent must read a reference document to find its index. Two clean placements, see (7).

## (6) Recommended boundaries / inputs / returns / failure / verification

- **Inputs:** every fn requires "current local date/timezone" from the caller; none says what to do when omitted (Houston's wrapper names `pwd -P` for cwd; no analogue for date). Proposal: CONTROLLER :30 adds "if omitted, hold the horizon default and say so" — or keep as caller discipline. Minor.
- **Return:** prescribe a one-line program entry proof mirroring Houston's: `<controller path> · stamp · <fn path> · stamp`. It makes the :54 stamp check observable at zero procedure cost and gives the first behavioural evidence a future invocation can carry.
- **Failure:** hold rules are consistent across both controllers (Field F3 asymmetry is harmless). One gap: nothing holds on *controller* stamp drift (see 2). Second gap: the two five-way classifications (list-pending vs carry-unfinished) should be one list, owned by the controller next to horizon semantics.
- **Verification:** there is no observed response for any fn (`said:` journal windows hold briefs only). The only verification that counts is a fresh-session invocation per fn with the response captured in the journal under the TEST-INSTALL §3 three-part rule. Audit-only G06 cannot do this; it is later work and Majkee's call because the files are his corner.
- **Stamp regeneration rule (proposal):** "Editing an fn re-rolls its `stamp:`, the controller's table row, and the controller's `stamp:`; the author re-rolls all three in one authoring request." Alternative: drop table stamps and rely on the proof line only — weaker, loses the expected-value check that is the programs' one structural advantage over Houston. Not recommended.

## (7) Fold / repair destinations (nothing applied; all are Majkee's personal files — AGENTS.md :37–38 requires an explicit authoring request, so each is Majkee-authored or Majkee-GO'd)

| finding | primary destination | alternative |
|---|---|---|
| stamp regeneration rule | `.majkee/AGENTS.md` :37–38 (one sentence, covers both programs) | one sentence at each CONTROLLER :54–55 / :54–55 |
| controller stamp unpinned | `engine/README.md` :17–20 — add `expected stamp` column | `.majkee/AGENTS.md` :21, :28 carry the stamp beside the path |
| grammar + program table live in a reference doc | move :9 and :17–20 into `.majkee/AGENTS.md` (stamped seat doc); README keeps examples | stamp `engine/README.md` and treat its §Entry as agent-consumable |
| two differing five-way classifications | journal-continuity CONTROLLER, new line under Horizon (:39–43); fns cite | leave; harmless until a second consumer |
| program entry-proof line | journal-continuity CONTROLLER :54 and project-saddle :54 | engine README expanded prompt :39 only (weaker: reference, not law) |
| "binding" name collision | U6 GUIDE glossary | none |
| explicit-declaration-overrides-walk-up | U5 (Houston wrapper/binding; re-rolls canary) | none now |
| Field friction 3 (horizon in fns), F2 ("destination" wording in a historical brief), friction 4 (home shortlist) | **no repair** — designed load order / historical text / already "rechecked on the actual host" (:44) | — |

## (8) Decisions needed

- **Consequential (Majkee), named but not ripe for U3:** whether the personal programs are *candidates* for D1's shared program layer or remain a specimen while the shared layer is authored fresh. RUNBOOK :38 already leans specimen; no gavel is needed to finish U3. Carry to U5/U7 and the germline-planning owner.
- **Mech, Majkee as author (his corner):** stamp-regeneration sentence; controller stamp column; grammar/table relocation or stamping; one classification list; proof line. Five small edits, all re-roll stamps.
- **Mech, later unit:** explicit-declaration-overrides-walk-up (U5); "binding" glossary (U6).
- **Reading to confirm, Flight:** that G5's table is the vendor adapter and the CONTROLLER table is the public index (my (2)). If Flight reads GAVELS :115–121 and :162 differently, (2) and the governing insight fall together and should be re-argued, not patched.

Otherwise: **none.** Nothing in U3 is ready for `/gavel-loop`.

**Not read / limits:** Houston `cards/*.md` bodies, nablarva addendum, journal 2026-10-16 outside the two windows, any `.jsonl`; no fn behaviour observed; sizes measured by `wc -c` today.
