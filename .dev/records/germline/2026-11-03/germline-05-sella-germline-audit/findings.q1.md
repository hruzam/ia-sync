---
session: germline-05-sella-germline-audit
pen: flight · integration · first question
date: 2026-10-20
question: >-
  What do Sella and Germline Forge prescribe about an agent loading and performing a selected
  procedure, and where do the current germline sources or recorded sessions support, extend
  or contradict those prescriptions?
sources_read:
  - /home/hruzam/reposoma/raw.guides/sella/GUIDE.md (full — flight-verified via field_sella)
  - /home/hruzam/reposoma/raw.guides/germline-forge/GUIDE.md (full — field_germline; :13 verified)
  - /home/hruzam/ia-sync/germline/README.md (full — field_germline; :8-12 verified)
  - /home/hruzam/reposoma/.majkee/.germline/programs/journal-continuity/CONTROLLER.md (full — verified :54-55)
  - /home/hruzam/reposoma/.majkee/.germline/programs/journal-continuity/fn/fold-entry.md (full — verified)
  - /home/hruzam/reposoma/.majkee/.germline/programs/project-saddle/CONTROLLER.md (full — field_germline)
  - /home/hruzam/unikuklatrix/nablarva/.dev/session/composer-01-parse/evidence/brief.sella-germline-audit.2026-10-19.md (:99, :105-107 verified)
  - /home/hruzam/reposoma/.majkee/journal/2026-10-16.md (bounded — field_germline :162-164, :514-516, :769-770)
  - /home/hruzam/reposoma/.majkee/journal/2026-10-17.md (bounded — field_germline :75-92)
  - /home/hruzam/reposoma/.majkee/journal/2026-10-19.md §2 (bounded — field_germline)
sources_not_read:
  - journal-continuity/fn/list-pending.md, audit-beds.md, carry-unfinished.md (three functions; noted below)
  - /home/hruzam/raw.research/harness/reports/2026-07-20-harness-lifecycle-skill-injection-safe-protocol.md (FILE NOT FOUND — dead reference; noted below)
---

# Findings — Q1: agent loading and performing a selected procedure

## F1 · Selective loading

**Source passages:**

Sella §1 (OS-cognate table):
> "dlopen | skill body loads at trigger via literal `cat SKILL.md` — text injection into the current window, not a process"
> "skill METADATA (~100 tokens each, resident from startup)"

Sella L9:
> "Agents get anchors … humans get full reads. Point, never copy. WHY: AX token economy — every full read an agent did not need is orientation budget burned"

germline README :8-12:
> "Runtime-load variant (Houston, final fold 2026-10-10): the wrappers carry only a loader; at entry the agent reads `identity.md` → `binding.<vendor>.md` → the nearest project addendum → `cards/<card>.md` and quotes each file's `stamp:`. Stamp rule: every loaded germline file carries `stamp: <8-hex random token>`, unique per file, regenerated on every edit — a matching token proves the current file was read."

journal-continuity CONTROLLER :54-55:
> "Load only the selected table binding; require matching program/stamp before its procedure runs.
> Missing file, stamp mismatch, or unknown id: report expected/observed path and token; hold, no fallback."

germline-forge GUIDE :13 (stale warning):
> "§0–§3 describe the pre-2026-10-10 model (build-time render files, body-equality checks) … Superseded by the Houston runtime-load fold (2026-10-10) … Current truth: `~/ia-sync/germline/README.md`."

**Observed evidence:** Journal 2026-10-17 :75-92 records Houston loading germline files at invocation, quoting stamps (identity 99ae988e, Codex binding 0c812f6c, Nablarva addendum a6498a47, consult card 5435b1c7). This is the runtime-load sequence in live practice.

**Relationship — Sella vs germline (C2):**
- **Observed:** The two-phase architecture maps conceptually — germline runtime-load has metadata resident (the wrapper's minimal loader) and body at trigger (identity.md → binding → addendum → card reads at entry). The implementation mechanism: germline uses tool reads to load identity files. Tool-read content enters the conversation as turn-level artifacts — not any named slot in Sella's three-layer stack (five named slots: Anthropic built-in, agent .md, --append-system-prompt, skill metadata in kernel; CLAUDE.md, auto memory, skill body in userland). Neither Sella nor [S3] addresses tool-read content in the compaction/survival model. Compaction rules cover kernel (resident), CLAUDE.md (disk re-injection), skill bodies (budget — confidence L per [S3] refresh). Tool-read content has no named survival path in either source; compaction behaviour is untested.
- **TENSION WITH SELLA L7 (Janus REVISE, 2026-10-20 — excerpt; full return: `_bus/janus.c2.return.2026-10-20.md`):** *"Sella L7 says outright: 'identity, hard limits, the one safety rule — must live in the kernel.' §1 puts 'the program's identity' in the agent .md kernel slot. The runtime-load wrappers 'carry only a loader'. By F3's own source ('the runtime does not fence a child; the card must'), the binding and card are the agent's only authority fence. So the thing being deferred is more than a gap in the documentation. It is a contradiction with L7, and it has a safety consequence: whether a germline agent's only fence is still resident after compaction."* The stamp proves a read at load time; it does not prove the content is still in context later.
- **EXTENDS:** Germline adds stamps (freshness proof Sella lacks); CONTROLLER's hold-no-fallback is stricter at the program layer than Sella's hook-layer exit 1.

**Verdict (final, Janus-checked):** F1 is reclassified to **TENSION WITH SELLA L7 — the germline runtime-load pattern places agent identity and its authority fence (binding/card) below the kernel boundary. Sella L7 requires identity and hard limits to be kernel-resident. The conceptual two-phase architecture maps; the specific implementation mechanism creates a named tension. Compaction behaviour is untested.**

**Later-work handoff (C2 — germline-planning Cartan):** Janus proposed a dated compaction pilot under Sella L8 as one approach to test the tension: load a germline agent, force compaction, check whether it can still quote the current binding and card stamps and still honour the card's forbidden-spawn and no-grant limits without re-reading. Majkee's direction: record C2 as a later-work handoff to the germline-planning Cartan. Janus's experiment is not automatically a universal production gate.

---

## F2 · Invocation

**Source passages:**

Sella §2:
> "description = the exported symbol — the one string by which the linker resolves you. Everything else in the file is invisible until after resolution."

Sella Walk B step 1:
> "Reference content that should stay in the caller's window → plain skill. Self-contained task needing isolation → `context: fork`. Reference content + fork = Rube Goldberg — the subagent gets rules but no task."

germline-forge GUIDE §4 :87-94 (four declared fields):
> entry · permissions · delegation authority · return destination — identical on both vendors.
> Claude child: Agent spawn from `<project>/.claude/agents/<slug>.md`; Codex child: `spawn_agent` with TOML; Claude main: `claude --agent <slug>` in project root; Codex main: `codex --profile <slug> -C <root>`.

journal-continuity CONTROLLER :30-31:
> "Caller supplies task, selected function, actor, current local date/timezone, and relevant anchor, horizon, paths, or carry destination."

brief :99-104:
> "Cartan's proposal: a readable assignment carrying request identity/revision, exact procedure/input references, task, limits, unresolved inputs and the selected native return contract. … Merely printing a harness tag does not load a procedure or invoke a role."

Journal 2026-10-16 :514-516 (Oraculum invocation):
> "skill: read `/home/hruzam/.agents/skills/buffering/SKILL.md` before beginning the cycle. This is a temporary controller procedure, not a request for a durable artifact." Skills load inside invocation when named.

**Relationship — Sella vs germline:**
- **SUPPORTS:** Germline's four declared fields (entry · permissions · delegation authority · return destination) are a concrete implementation of Sella's description-as-exported-symbol model. The binding file is the mechanism by which the description and its resolution contract are declared.
- **EXTENDS:** Germline specifies what the caller must supply (function id, actor, date, anchor/paths) — Sella describes the router/symbol side; germline adds the caller-side requirements.
- **EXTENDS:** Brief Q1 adds that skills load inside invocation when named in the controller; this is not a Sella-prescribed mechanism but is consistent with Sella's skill-metadata-resident / body-at-trigger pattern.

**Consequence:** A call that does not supply function id, actor, and named anchor is not a complete invocation. A tag or name in context is not invocation.

**Uncertainty:** Sella's `context: fork` for isolation is not directly mapped to a germline mechanism in these sources. The germline-forge §4 entry mechanisms (spawn, profile) may be the analog, but the correspondence is not stated.

---

## F3 · Authority

**Source passages:**

Sella §1 L1, L6, L7:
> "Three layers. Contracts placed in the wrong layer silently lose authority."
> "Skills: higher scope wins (Enterprise > Personal > Project). Subagents: more local wins. These are opposite; never design assuming one rule."
> "Only the kernel layer survives inattention."

germline-forge GUIDE :92-94:
> "on claude 2.1.292 a child can spawn and inherits the parent's effective permissions — the runtime does not fence a child; the card must."
> Forbidden spawn sets live in the binding; capability claims carry the client version they were observed on.

journal-continuity CONTROLLER :32:
> "This procedure grants no tool capability or authority."

project-saddle CONTROLLER :24:
> "This function grants no write, commit, deploy, session change, transport, agent/skill activation, or promotion."

Journal 2026-10-16 :162-164:
> "LOADED confirms only that the addressed packet/reply was read. It grants no project write, launch, receipt destination, STATUS/RUNBOOK authority, or gate change."

**Relationship — Sella vs germline:**
- **SUPPORTS:** Both agree authority is positional/declared, not ambient. Sella: layer determines authority. Germline: card/binding holds the operative limits; the runtime enforces nothing.
- **EXTENDS AND MAKES CONCRETE:** Sella's authority stack is conceptual. Germline shows the mechanism: forbidden spawn list in the binding + explicit no-capability declarations per function. The "runtime does not fence a child" is a direct operational consequence of Sella's layer model — the concept made operational.
- **EXTENDS:** The explicit per-function no-grant declarations (CONTROLLER :32, project-saddle :24) formalize what Sella implies: contracts must be in the right layer, and for programs that means explicit per-function authority lines, with no defaults assumed.

**Consequence:** A program without explicit per-function authority declarations relies on ambient runtime limits that do not exist. Authority must be stated; absence of a declaration is not absence of capability.

**Open question preserved from brief Q3:** "Phase 0 keeps `from` as a declared string and never resolves references or grants scope." Runtime bindings must disclose actual controls without claiming parity. This is not answered by either guide; preserved as open for Majkee's review.

**Uncertainty:** Sella's scope-collision inversion (skills: higher scope wins; agents: more local wins) — whether the germline program/controller model has an analog scope-collision rule is not addressed in the sources read.

---

## F4 · Useful return

**Source passages:**

Sella Walk A step 5; L4:
> "State in the body what the agent returns: shape, length, failure form ('if scope is unclear, return the question, do not guess')."
> "Every primitive declares what it returns and how it fails. Gate: a caller can parse success from failure without reading prose."

fold-entry :31:
> "Return exact file/chapter, appended event, evidence checked, and any unverified claim."

germline-forge GUIDE §7 :118:
> "Files carry the work; the wire carries one line + a path."

Journal 2026-10-16 :151-157 (standard BUS return shape):
```
from-<seat> to-myShell ---
packet: <id>
evidence: <absolute receipt path, or none>
observed: <short result>
uncertain: <remaining question, or none>
gate: <waiting for whom / what, or complete>
---
```

brief :105-107:
> "A stamp, digest, receipt or 'understood' response cannot guarantee reading or understanding. Identify what the loader proves, what the recipient reports, and what an independent check must observe. Keep Q1/Q2 open."

**Relationship — Sella vs germline:**
- **SUPPORTS:** Germline's BUS return shape and fold-entry return step are direct implementations of Sella's parseable-success-failure principle. The BUS shape gives evidence path + observed result + uncertainty + gate — each field parseable without prose.
- **EXTENDS:** Germline's "files carry the work; wire carries one line + a path" operationalizes Sella's token-economy principle (agents get anchors, not full bodies) at the return level. Heavy evidence goes in a file; the return wire is lean.
- **EXTENDS (preserved open):** Brief Q2 — a stamp proves the file was addressed, not that it was correctly interpreted. What the loader proves vs. what an independent check must observe remains open per brief's instruction.

**Consequence:** A return that quotes only "LOADED" or "understood" is not a useful return by either model. Evidence paths are structural, not optional.

---

## F5 · Recovery

**Source passages:**

Sella Walk B step 4; L4:
> "`!`-lines for live data, each with a fallback so a missing file degrades loudly, not silently: `` !`cat $file 2>/dev/null || echo "[FILE NOT FOUND]"` ``"
> "exit 2 is the ONLY blocking code; exit 1 does NOT block."

journal-continuity CONTROLLER :54-55:
> "Missing file, stamp mismatch, or unknown id: report expected/observed path and token; hold, no fallback."

fold-entry (last line):
> "Missing text, ambiguous scope/ownership, or missing write authority: return a draft and the exact missing input; no write."

Journal 2026-10-16 :769-770:
> "Before the first write, set STATUS `in_flight` with a recovery probe. After creating the draft, clear `in_flight`, set exactly one method-review next/expected pair."

**Relationship — Sella vs germline:**
- **SUPPORTS:** Both model recovery as explicit surfacing — not silent, not inferred. Loud degradation (Sella) and hold-with-report (germline programs) share the same principle: the agent must not proceed past a gap.
- **NUANCED DIFFERENCE (not a contradiction):** Sella's hook layer continues execution via exit 1 (non-blocking noise). The germline program layer holds unconditionally on stamp mismatch. Different execution contexts — a hook failure is recoverable by the shell-level runner; a program stamp failure means the procedure hasn't started. Both are consistent with the no-silent-failure principle, applied at different layers.
- **EXTENDS:** The STATUS `in_flight` + recovery probe pattern (journal :769-770) is a germline practice not prescribed by Sella. It provides operator-observable recovery state that Sella's hook model doesn't address.

**Consequence:** A germline program that falls back to a best-effort version on stamp mismatch violates the CONTROLLER's stated model. Recovery is hold + surface, not degrade + continue.

---

## [S3] reference — corrected

Sella GUIDE.md §1 and §2 cite `raw.research/harness/reports/2026-07-20-harness-lifecycle-skill-injection-safe-protocol.md`
as [S3·§3] (progressive-disclosure table), [S3·§5b] (live-data fallback), and [S3·§7] (layer-rule mechanism).
Sella uses a **relative path** that resolves under `/home/hruzam/reposoma/`.

**CORRECTED: the file exists.** My earlier `ls` check used the wrong absolute prefix (`/home/hruzam/raw.research/...` instead of `/home/hruzam/reposoma/raw.research/...`). That was Flight's error, not a Sella defect.

**Two versions present:**
- `/home/hruzam/reposoma/raw.research/harness/reports/2026-07-20-harness-lifecycle-skill-injection-safe-protocol.md`  
  sha256: `89b0054da53350a267f993f86c364655034dd37a09b7d7161820340086fbd041`
- `/home/hruzam/reposoma/raw.research/harness/reports/2026-09-17-harness-lifecycle-skill-injection-safe-protocol-refresh.md`  
  sha256: `2780cb6243a419487ff77277204e9b39f9911c7bb95b045935291e3e7c2cc190`

The refresh (September 2026) postdates Sella's July citation; whether it supersedes the §5d caveat or the progressive-disclosure table is not yet checked. Both files are in scope for the next-read proposal from field_sella.

---

## Program-layer pilot evidence

Source: `/home/hruzam/reposoma/.majkee/journal/2026-10-16.md` — bounded grep (ctrl, journal-continuity, project-saddle, fold-entry, audit-beds, carry-unfinished, CONTROLLER, stamp, program&).

**Two `ctrl` invocations confirmed in practice:**

1. **`ctrl journal-continuity&audit-beds`** (:1544, inside "Monthly audit delegation snapshot — 2026-10-16"):
   > `ctrl journal-continuity&audit-beds : horizon month (2026-09-17 through 2026-10-16 inclusive); actor: one-shot Astra reviewer; authority: read-only; destination: report to myShell only.`
   
   Completion record (:2047-2048, §4.4):
   > `- [x] One Astra reviewer completed a read-only, journal-first audit under ctrl journal-continuity&audit-beds. It read 21 dated Markdown sources …`

2. **`ctrl project-saddle&saddle-project`** (:1620, inside "Original myShell saddle and empty exchange container"):
   > `ctrl project-saddle&saddle-project : project ia-sync; scope: .dev/session/germline-03-foundation-audit/; authority: read-only; task: prepare the current instruction chain for this relay.`
   No separate completion record found in scanned sources.

**No CONTROLLER stamp-table entries found** in any of the three journals. Execution evidence for `audit-beds` is a prose checkbox. `project-saddle` invocation has no completion evidence. 2026-10-17 and 2026-10-19 returned zero matches.

**Consequence:** The program-layer mechanism was used in practice. Stamp-table verification was not found in the inspected records (2026-10-16, 2026-10-17, 2026-10-19 bounded scans); absence in these records does not establish it never happened. Practice evidence exists; stamp-verification evidence was not observed in the sources inspected.

---

## [S3] supplement — four sections read

Sources: `reposoma/raw.research/harness/reports/2026-07-20-harness-lifecycle-skill-injection-safe-protocol.md` (§3, §5b, §5d, §7 only) and the September 2026 refresh (full). Cross-checked against Sella GUIDE.md §2 (L200-244). All citations spot-verified by Flight.

### §3 — Progressive-disclosure / selective-loading table

Three-phase load (confirmed, backs Sella §1 OS-cognate table):
> Metadata (YAML frontmatter description) — Always, at startup — ~100 tokens  
> SKILL.md body — When triggered — <5k tokens  
> Supporting files / scripts — On demand — 0 until accessed

Two trigger modes: explicit `/skill-name` or description auto-match (gateable via `disable-model-invocation: true`).

**Refresh note:** The `<5k tokens` and `25k combined` figures are downgraded to CONFIDENCE L by the refresh — live docs now surface a line-count guideline (under 500 lines) instead. Architecture stands; specific token numbers should not be cited as settled.

**Relationship to F1:** Confirms and backs the three-phase model stated in findings F1. Metadata residency and body-at-trigger are not vendor folklore — they are documented progressive-disclosure architecture.

### §5b — Live-data fallback model

Explicit pattern (confirmed, backs Sella Walk B step 4):
> `` !`cat $file 2>/dev/null || echo "[FILE NOT FOUND]"` ``

The model receives assembled data before its first reasoning token; it never sees fetch instructions, only rendered output. Fallback is declared inline; silent failure requires active suppression of `||`.

**Refresh additions:** `disableSkillShellExecution` config setting provides a global kill switch for the entire `!` pipeline. Skills synced from claude.ai never run shell execution since v2.1.228. Neither changes the fallback model — they add administrative control over whether the pipeline runs at all.

**Relationship to F5:** Confirms the F5 "loud degradation" recovery model with the original pattern text.

### §5d — exec()/fork mechanics ⚡ STALE (confirmed by Sella §2)

The exec()/fork behavioral claim is confirmed accurate:
> "`context: fork` + `agent:` — spawn a specific specialist with a clean, pre-hydrated briefing assembled by the `!` pipeline. The specialist sees nothing from the parent conversation — only what the skill body provides."

**What is stale:** The original §5d presents `allowed-tools`, `disallowed-tools`, `context: fork`, `agent:` as a unified, universal "permission and resource tuning" table applicable to any harness frontmatter. Sella §2 (L201-242, verified) splits this into two distinct surfaces:

| §5d claim | Sella §2 correction (line) | Consequence |
|---|---|---|
| `allowed-tools` as universal | Skill frontmatter only (L232) | Agents use `tools` (L207) — different key |
| `disallowed-tools` as universal | Skill frontmatter only (L232) | Agents use `disallowedTools` (L207) — different key, camelCase |
| `context: fork` as universal | Skill frontmatter only (L234) | Agent `.md` files do not carry `context:` |
| `agent:` as universal | Skill frontmatter only (L235) | Agent `.md` files do not carry `agent:` |
| `model`/`effort` as one-turn override | Correct for skills (L233) but also present as session-level agent keys (L208, L215) | §5d does not distinguish one-turn vs session scope |

**Authoring trap:** A germline program wrapper (agent `.md`) built from §5d alone will use `allowed-tools` when the correct key is `tools`. The exec()/fork behavior (specialist sees nothing of parent) is accurate; the key-assignment table is stale. **The September refresh does not fix this** — it adds `omitClaudeMd` (v2.1.267) extending the fork mechanic but does not re-do the frontmatter split.

**Relationship to F1–F3:** Extends F2 (invocation: agent `.md` key names matter) and F3 (authority: wrong key in wrong layer silently loses authority). The practical consequence is a named silent-failure vector.

### §7 — Authority-stack / layer-rule mechanism

Core confirmed verbatim (backs Sella §1 L148, L248-252):
> "Place behavioral contracts at the layer that gives them the right weight. Identity and ground-truth declarations belong in system-prompt layer. Workflow conventions belong in CLAUDE.md. Procedural playbooks belong in skill bodies. Live data belongs in `!` preprocessing."

Refresh adds one material change: `omitClaudeMd` (v2.1.267) allows a subagent to skip CLAUDE.md loading entirely. The original §7 implicitly assumes CLAUDE.md always loads — that assumption is now false for opted-out subagents. The refresh flags this as a §7 addendum, not a contradiction.

Additional: Refresh Finding 6.1 corrects §5e (adjacent to §7) — workspace trust does NOT gate `allowed-tools` in `-p` runs. This affects how authority grants work in automated harness runs; noted but not §7 itself.

**Relationship to F3:** §7 is the strongest confirmed claim in [S3]. The `omitClaudeMd` exception is new and matters for germline programs running as subagents with agent `.md` wrappers.

---

## Open questions / preserved disagreements

**Q-A (preserved from brief Q1/Q2):** Stamp proves the file was addressed; it does not prove correct interpretation. What the loader proves, what the recipient reports, and what an independent check must observe are three distinct things. Brief instructs this stays open; preserved here.

**Q-B (preserved from brief Q3):** Phase 0 keeps `from` as a declared string, never resolving references or granting scope. Future delivery derives and compares sender. Runtime bindings must disclose actual controls without claiming parity. Not answered by Sella or germline-forge; preserved.

**Q-C (new, this audit):** Is the CONTROLLER stamp-table pattern prescribed for all germline programs, or specific to personal/uncanonical trials? journal-continuity CONTROLLER :5 reads "uncanonical; no deploy." The stamp rule in README applies globally but the table pattern's canonical status is unclear.

**Q-D (new, this audit):** Three journal-continuity functions (list-pending, audit-beds, carry-unfinished) not read in this pass. Their load model and return shape are unknown; they may extend or specialize the fold-entry pattern. Noted, not yet investigated.

**Q-E (new, this audit):** No per-procedure runtime staleness gate is prescribed by either Sella or germline-forge for the loaded procedure body's fitness for the task (stamps prove currency of the file; they don't gate whether the procedure is still appropriate). Whether this gap matters for programs is not addressed.

**Q-F1 classification — settled by Janus (2026-10-20):** F1 SUPPORTS verdict reclassified to TENSION WITH SELLA L7. Janus confirmed the flag: germline runtime-load places agent identity below the kernel boundary; Sella L7 requires identity and hard limits in the kernel; the wrapper holds only the loader. Full Janus return: `_bus/janus.c2.return.2026-10-20.md`. Compaction behaviour remains untested. C2 recorded as later-work handoff to germline-planning Cartan; Janus's proposed compaction pilot is not automatically a universal production gate (Majkee direction 2026-10-20).

**Q-G (Oraculum N2–N4):** Three new questions from umbrella assessment — preserved:
- N2: compaction survival of runtime-loaded identity (blocks F1 verdict)
- N3: if a germline function sits outside Sella's primitive set (agent/skill/hook), Sella has no law for it — reconcile or extend?
- N4: under body composition, does the CONTROLLER table become the registry the brief forbids ("no new registry")?

**Q-H (Brief Q4/Q5 — dropped from Q-A/Q-B/Q-C list, now restored):**
- Q4: Editor body-tags vs declared block grammar (Sublime IDE §Changed vs v3 opaque body rule — mismatch flagged in brief :113-117 but not carried into Q1's open list)
- Q5: Publication home/duties — exact code home, stack, verifier, and distinct duty separation for parser/renderer/exchange/STATUS/delivery owners (brief :118-122; Majkee decisions)

---

## Decisions needed from Majkee

**D1 — WITHDRAWN.** [S3] cross-reference was a path-prefix error by Flight (missing `reposoma/`); the file exists at `reposoma/raw.research/harness/reports/`. See corrected [S3] reference section above. Both versions present and verified. No Sella defect. Original D1 retired.

**D2 — Brief open questions (Q-A, Q-B):** Brief Q1/Q2/Q3 are preserved as open per the brief's own instruction. Are they in scope for further investigation in this audit, or does Majkee consider them adequately noted and parked for a later session?

**D3 — Remaining journal-continuity functions (Q-D):** Read list-pending, audit-beds, carry-unfinished to complete the program picture, or out of scope for this audit's first question?

**D4 — Next-read candidate:** The germline README references a "no index by design (discovery bus = parked)" with a pointer to `~/ia-sync/.dev/session/invariance-autonomy/raw/master-brief.2026-09-23.md` for design and open decisions. Is this in scope for this audit?

---

## Summary: prescriptions and their observed status

| Prescription | Sella says | Germline/practice says | Status |
|---|---|---|---|
| Selective loading | Metadata resident; body at trigger | Runtime-load sequence (4 files); stamp-gated by CONTROLLER | **TENSION WITH SELLA L7** (Janus REVISE) — wrapper holds only a loader; identity/fence below kernel. Compaction untested. Handoff: germline-planning Cartan. |
| Staleness gate | Not prescribed at runtime | Stamps prove file currency (not task fitness) | Sella gap; germline partially fills |
| Invocation completeness | Description match; caller phrases natural order | Caller must supply function id, actor, date, anchor | Supported + made concrete |
| Invocation via tag alone | Not addressed | Explicit: tag ≠ invocation | Germline adds constraint |
| Authority (layer model) | Positional, not stated; silent failure on wrong layer | Runtime does not fence; card/binding must declare | Supported + mechanized |
| Per-function authority default | Implied: no default | Explicit: every function must state grants; no-capability is stated | Germline tightens Sella's implication |
| Useful return | Parseable success/failure; no prose | BUS shape: evidence path + observed + uncertain + gate; stamps insufficient alone | Supported + operationalized |
| Recovery | Loud degradation; named fallback; no retry | Hold, no fallback; report expected/observed; STATUS in_flight for writes | Supported + stricter at program layer |
| CONTROLLER recovery probe | Not addressed | STATUS in_flight + recovery probe before any write | Germline extends |
