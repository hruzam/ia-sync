---
from: field · unit U3 · date: 2026-10-21
---

## Scope note

All ten sources are personal, undeployed files under `.majkee/.germline/programs/` and `.majkee/`.
No `~/.germline/programs/` exists (AGENTS.md L37–38: "Program and engine documents are personal,
uncanonical, no-deploy guidance"; both CONTROLLERs L6 frontmatter: `scope: personal .majkee trial;
uncanonical; no deploy`). This corpus is a local trial using the PG-r3 package shape, not an
installation of global law (journal-continuity CONTROLLER.md L10).

---

## A. Per-file table

**File 1 — journal-continuity/CONTROLLER.md** · stamp: `96a5974b` L4  
Job: govern all journal-continuity invocations; define shared invariants, roles, horizon semantics, function table.  
Inputs: "Caller supplies task, selected function, actor, current local date/timezone, and relevant anchor, horizon, paths, or carry destination." L30–31.  
Authority: "Read named journal/source files; write the authorized journal scope only." L31. "No commit, push, deploy, source-program change, session-bed edit, or automatic promotion." L18.  
Return: delegates to selected fn; controller itself issues no direct output.  
Failure/hold: "Missing file, stamp mismatch, or unknown id: report expected/observed path and token; hold, no fallback." L55.  
Continuity: "Today's date is context, not a rollover instruction. Default fold destination is today; an explicit old anchor such as `journal/2026-10-13.md` §4 stays valid until Majkee changes it." L25–26.  
Size: not computed (no shell). Line refs: L4, L18, L25–26, L30–32, L54–55.

**File 2 — fn/audit-beds.md** · stamp: `e1c9e403` L5  
Job: compare journal claims against current owner-state files; surface discrepancies.  
Inputs: "current local date, explicit journal chapters or horizon (default today), optional bed filter." L9.  
Authority: "Read `journal-source` and each named `owner-state`; never write or tick." L10.  
Return: evidence-backed discrepancies; "the smallest suggested dated correction/carry pointer." L21–22.  
Failure/hold: "Unreadable, contradictory, or stale required owner input holds any conclusion depending on it; report the boundary and continue independent comparisons." L24–25.  
Continuity: none (read-only; correction pointer suggested, not appended).  
Size: not computed. Line refs: L5, L9–10, L21–25.

**File 3 — fn/carry-unfinished.md** · stamp: `10577337` L5  
Job: review horizon for unfinished matters; optionally append reciprocal carry receipts.  
Inputs: "current local date/timezone, source anchor or explicit horizon, optional topic/bed, proposed destination journal file/chapter, and explicit carry/fold authority." L9–10.  
Authority: "write only authorized source/destination journal scopes." L11. Explicit authority required before any mutation (L19–20).  
Return: report of candidate pointers and uncertainties; or if authorized, paired dated receipts: source: "CARRIED TO <destination file#heading> · <reference>"; destination: "CARRIED FROM <source file#heading> · <reference>" plus classification and current owner/evidence pointer. L26–27.  
Failure/hold: "Missing owner evidence holds active claims" L20; "If only one append succeeds, report the incomplete pair and exact missing half; do not claim completion." L31–32.  
Continuity: paired receipts in both source and destination; "Preserve the original entry." L28.  
Size: not computed. Line refs: L5, L9–11, L20, L26–28, L31–32.

**File 4 — fn/fold-entry.md** · stamp: `9456ec9a` L5  
Job: append authorized text/snapshot/relay to a dated journal chapter.  
Inputs: "supplied text/task, actor, current local date, explicit anchor if any, evidence paths, and authority to fold." L9. "If no explicit anchor, use `journal/<current-date>.md`." L11.  
Authority: "writes only `destination`." L10. Reads source/owner-state "only where claims require checking." L10.  
Return: "exact file/chapter, appended event, evidence checked, and any unverified claim." L32.  
Failure/hold: "Missing text, ambiguous scope/ownership, or missing write authority: return a draft and the exact missing input; no write." L34.  
Continuity: "Corrections, closure receipts, and carry pointers are new dated entries, never silent rewrites." (CONTROLLER.md L20).  
Size: not computed. Line refs: L5, L9–11, L32–34.

**File 5 — fn/list-pending.md** · stamp: `6fc4b914` L5  
Job: inspect a horizon for unfinished matters; no writes.  
Inputs: "current local date, horizon (`all | month | week | N days`, default today), optional topic/bed/anchor." L9–10.  
Authority: "Read `journal-source`; optionally inspect named `owner-state`. No writes." L10.  
Return: grouped candidates: source/date/chapter, brief matter, observed wording/state, current owner/source pointer, verification status. L19–21.  
Failure/hold: "If inputs/files are missing, return the available partial inventory and what was not inspected." L25.  
Continuity: none (read-only).  
Size: not computed. Line refs: L5, L9–10, L19–21, L24–25.

**File 6 — project-saddle/CONTROLLER.md** · stamp: `0d7f2a36` L4  
Job: govern project-saddle; define invariants, maintained shortlist of 4 projects, single function.  
Inputs: "caller's explicit alias, task, scope/path and authority." L29. "never infer attachment from cwd, remembered work, a journal mention, or a similarly named folder." L6.  
Authority: "Read-only capabilities suffice. This function grants no write, commit, deploy, session change, transport, agent/skill activation, or promotion." L22–25.  
Return: "verified instruction chain and scoped handoff" (via saddle-project fn). L52.  
Failure/hold: "Missing, ambiguous, unreadable, or conflicting required paths/instructions hold the affected handoff. Report the exact gap; do not invent instructions, fall back to another project, or create files." L18–19.  
Continuity: not a continuity function; "journal-continuity remains personal continuity support and cannot override project state or gates." L8.  
Size: not computed. Line refs: L4, L6, L8, L18–19, L22–25, L29, L54–55.

**File 7 — fn/saddle-project.md** · stamp: `a3ea5e32` L5  
Job: match alias to CONTROLLER shortlist, walk AGENTS chain, return READY or HELD.  
Inputs: "explicit shortlist alias, task (`myShell-says:` or `task:`), task path/scope, actor and authority (read-only if omitted)." L9–10.  
Authority: "this function writes nothing." L11. "READY is a checked context receipt, not task completion, write authorization, or permission to change session owners." L34.  
Return: READY with alias, verified absolute root, actual host, complete AGENTS chain, required-read evidence, task words, scoped paths, authority, next governing owner/read pointer (L29–31); or HELD with exact path and missing decision/material (L31–32).  
Failure/hold: "Missing/conflicting instructions or required state → HELD … do not handle the blocked task." L31–32.  
Continuity: N/A (handoff receipt, not journal write).  
Size: not computed. Line refs: L5, L9–11, L29–34, L36–37.

**File 8 — .majkee/AGENTS.md** · stamp: none (no frontmatter)  
Job: assign myShell as active seat within .majkee/; name programs and `ctrl` convention; govern continuity scope.  
Inputs: N/A (seat instruction document).  
Authority: "write only inside `journal/`." L35. "no commit, no push. Secrets never inline." L36.  
Return: N/A.  
Failure/hold: N/A.  
Continuity: "Use today's day square by default; an explicitly named older chapter remains a valid anchor (including `journal/2026-10-13.md` §4). A date change alone never carries work." L32–33.  
Size: not computed. Line refs: L5–6, L14–16, L21–27, L32–38.

**File 9 — engine/README.md** · stamp: none (no frontmatter)  
Job: define `ctrl <program>&<function> : <task>` prompt convention; provide expanded prompt template; table of programs to controllers; examples; human relay tags.  
Inputs: N/A (reference document).  
Authority: "prompt guidance, not a shell command, parser, skill, or auto-discovery." L3.  
Return: N/A.  
Failure/hold: "Unknown program/function: report the missing binding and request the intended material." L15.  
Continuity: "Review horizon alone grants no carry." L27.  
Size: not computed. Line refs: L9, L13–15, L25–27, L87–93.

**File 10 — journal/2026-10-16.md (L1535–1560, L1610–1630)**  
Two recorded invocations in the given windows:  
- L1544: `ctrl journal-continuity&audit-beds : horizon month (2026-09-17 through 2026-10-16 inclusive); actor: one-shot Astra reviewer; authority: read-only; destination: report to myShell only.`  
- L1620: `ctrl project-saddle&saddle-project : project ia-sync; scope: .dev/session/germline-03-foundation-audit/; authority: read-only; task: prepare the current instruction chain for this relay.`  
L1535–1537 context: "This sector preserves the worked shapes that led to the current relay. It is explanatory only: no packet below is active, no line number is a task address."  
Line refs: L1535–1537, L1544–1545, L1618–1620.

---

## B. Program-vs-program differences

| Axis | journal-continuity | project-saddle |
|---|---|---|
| Function count | 4 (fold-entry, list-pending, audit-beds, carry-unfinished) — CONTROLLER L47–52 | 1 (saddle-project) — CONTROLLER L50–52 |
| Write authority | fold-entry and carry-unfinished may write inside journal/ when explicitly authorized; audit-beds and list-pending never write | "this function writes nothing" — saddle-project.md L11 |
| Horizon concept | Defined: `all / month / week / N days` — CONTROLLER L39–43; used in list-pending and carry-unfinished inputs | Absent; works from explicit alias and path only |
| Project shortlist | None | Maintained table of 4 projects with absolute roots — CONTROLLER L37–45 |
| Independence clause | "no other function is a prerequisite" — CONTROLLER L56 | "no journal function is a prerequisite" — CONTROLLER L56 (explicitly names journal-continuity) |
| Hold language | "report expected/observed path and token; hold, no fallback" — CONTROLLER L55 | "report expected/observed path and token; hold without fallback" — CONTROLLER L55 (near-verbatim) |
| Continuity relationship | Primary; is the continuity layer | "journal-continuity remains personal continuity support and cannot override project state or gates" — CONTROLLER L8 |
| Return taxonomy | Varies by fn: findings, reports, or appended entries | Binary: READY or HELD — saddle-project.md L29–32 |

---

## C. Program-vs-Houston mapping (H1)

**Proposed mapping and breaks:**

identity ≈ CONTROLLER invariants: Both hold behavioral rules, authority ceilings, and role definitions before any task runs. BREAK: Houston identity.md has three cards with distinct authority per card (consult: none write; audit: wrapper-mechanics diff; sitting: drafts in own bed) — identity.md L53–55. CONTROLLERs have flat invariants applying uniformly across all functions; no card-level authority differentiation.

card ≈ fn: Both define inputs, authority, and return contract for one bounded task. BREAK: Houston's card returns a verdict taxonomy (`fits · stretches · breaks · unclear`) — identity.md L53. Fn files have numbered procedural steps with no verdict taxonomy. Houston cards are separate files in `cards/<card>.md`; fn files are sibling files in `fn/`.

wrapper ≈ launcher (`ctrl <program>&<function>`): Houston's wrapper (houston.md L22–43) is a deployed file in `~/.claude/agents/` that loads germline at runtime and carries a canary. The `ctrl X&Y` grammar (engine/README.md L9) is a textual prompt convention, never deployed (engine/README.md L3: "not a shell command"). BREAK: wrapper carries entry-proof mechanism (canary + stamp echoes on first reply — houston.md L40–42); `ctrl` has no canary, no stamp echo, no entry-proof requirement.

project addendum ≈ project-local function: Houston's addendum specializes neutral Houston for one project and is an authored germline file. Project-saddle shortlist is a table maintained inside one CONTROLLER, not per-project authored files. BREAK: addendum is loaded by CWD walk-up (houston.md L28–33); shortlist requires explicit alias (saddle-project.md L1).

Additional breaks not covered by the mapping:
- Houston has vendor delta separation (binding.claude.md); programs have no vendor layer.
- Houston has explicit evidence-discipline tags (`said:` / `inferred:` / `locked:`) — identity.md L66–69; programs have no tagging taxonomy.
- Houston has `no standing presence` — identity.md L45–47; programs have no equivalent clause.
- Houston wrapper is deployed; programs are explicitly undeployed — both CONTROLLER frontmatters L6.

---

## D. H2–H6 evidence tables

**H2 — CONTROLLER functions table as binding table**

The table binds 5 columns per row: `function id | occasion | file binding | expected stamp | result` — journal-continuity CONTROLLER.md L47–52; project-saddle CONTROLLER.md L50–52. It binds: name → relative file path → a specific stamp token → result type. The stamp is what the CONTROLLER calls the "binding check" — CONTROLLER.md L54: "Load only the selected table binding; require matching program/stamp before its procedure runs."

**H3 — Table stamp vs fn file stamp (literal comparison)**

Grep output (all five `.md` files under `.majkee/.germline/programs/`):

| fn | Table stamp (CONTROLLER) | fn file stamp (frontmatter) | Match |
|---|---|---|---|
| audit-beds | `e1c9e403` (journal-continuity CONTROLLER.md L51) | `e1c9e403` (audit-beds.md L5) | YES |
| fold-entry | `9456ec9a` (journal-continuity CONTROLLER.md L49) | `9456ec9a` (fold-entry.md L5) | YES |
| list-pending | `6fc4b914` (journal-continuity CONTROLLER.md L50) | `6fc4b914` (list-pending.md L5) | YES |
| carry-unfinished | `10577337` (journal-continuity CONTROLLER.md L52) | `10577337` (carry-unfinished.md L5) | YES |
| saddle-project | `a3ea5e32` (project-saddle CONTROLLER.md L52) | `a3ea5e32` (saddle-project.md L5) | YES |

All five stamps match today. Regeneration rule: neither CONTROLLER contains any text about who regenerates the table stamp when an fn file is edited. AGENTS.md L37–38 states "Changing them or these instructions needs an explicit authoring request" — implying manual update, but no regeneration procedure is described anywhere in the read corpus.

**H4 — Project resolution mechanism**

project-saddle: "Match the explicit alias exactly to the controller's shortlist." — saddle-project.md L1. Requires: explicit alias in caller's invocation, present in shortlist table. "never infer attachment from cwd, remembered work, a journal mention, or a similarly named folder." — CONTROLLER.md L6.

Houston: "Context is CWD-based: the session receives the CLAUDE.md/AGENTS.md stack of the directory it started in, and the LOADER's addendum walk starts there." — binding.claude.md L45–46. Walk: "walk its ancestors upward. At each ancestor, look for `.germline/agents/houston/<ancestor-basename>.md`; select the first unambiguous readable one." — houston.md L29–32. Requires: no explicit alias; uses `pwd -P` (when available).

Inputs compared: project-saddle requires explicit alias from caller; Houston requires CWD (automatic). The AGENTS.md notes this explicitly at L30–31: "The saddle is read-only and never attaches a project from the working directory alone."

**H5 — Invocation grammar `ctrl X&Y`**

Defined / used:
1. engine/README.md L9: `ctrl <program>&<function> : <task>` — canonical definition.
2. AGENTS.md L26–27: "`ctrl <program>&<function> : <task>` is a manual prompt convention, defined in `engine/README.md`."
3. engine/README.md L14: "`&` separates names in this prompt convention; never execute this text in a shell."
4. engine/README.md L13: "No global search/fallback, function guessing, or missing-file substitution."

Neither CONTROLLER.md repeats the grammar; both defer to engine/README.md. No `&&` (double ampersand) appears in any of the ten read sources. The BRIEF mentions `&&` — it is not found in this corpus.

Journal invocations:
- L1544: `ctrl journal-continuity&audit-beds :` — matches canonical grammar.
- L1620: `ctrl project-saddle&saddle-project :` — matches canonical grammar.

No divergence in form between the two CONTROLLERs and the journal invocations; all use single `&`.

**H6 — Authority/return: destination and pen**

| fn | Destination named? | Pen | "Read-only" meaning |
|---|---|---|---|
| fold-entry | Yes — "`destination` = caller-authorized journal file/chapter" CONTROLLER L35 | Writes to destination only | Reads source/owner-state only where claims require checking (fn L10) |
| list-pending | No (report only) | None | "No writes." L10 — explicit |
| audit-beds | Report "to myShell only" (journal invocation L1545) — not a write destination | None | "never write or tick" L10 — explicit |
| carry-unfinished | Yes — named source and destination chapters both | Writes own-scope receipts to both | Default is report only; mutation requires explicit authority (fn L19–20) |
| saddle-project | "Output is a handoff to the current seat/operator" L11 | None | "this function writes nothing" L11 |

Journal invocation vs function contracts:
- L1544 audit-beds: "authority: read-only; destination: report to myShell only" — matches audit-beds "never write or tick" (fn L10). "destination" here means output audience, not write target.
- L1620 saddle-project: "authority: read-only; task: prepare the current instruction chain for this relay" — matches saddle-project "writes nothing" (fn L11) and read-only default (fn L10).
Both invocations match their function contracts on inputs and authority.

---

## E. Friction list for agent consumer (legibility only, ranked)

1. **Stamp regeneration undefined** (both CONTROLLERs, no rule anywhere in corpus): When an fn file is edited, no procedure names who updates the table stamp. A consumer reading only the CONTROLLER cannot detect a silent stamp mismatch introduced by an edit.

2. **engine/README.md and AGENTS.md have no stamps**: Unlike fn files, these two documents carry no frontmatter `stamp:`. They cannot be binding-checked at invocation. An agent following the CONTROLLER's stamp-check discipline has no equivalent check for its two most frequently read instruction sources.

3. **Horizon semantics defined only in CONTROLLER** (CONTROLLER.md L39–43): list-pending.md and carry-unfinished.md reference `all | month | week | N days` in their Inputs lines but do not define them. A consumer reading only a fn file must cross-reference the CONTROLLER for horizon meaning.

4. **shortlist is office-authored; home validity stated as rechecked but not recorded**: project-saddle CONTROLLER.md L44–45: "These paths existed on office when authored; existence is rechecked on the actual host." No home-side verification is recorded in the shortlist or elsewhere in the read corpus.

5. **`myShell-says:` vs `task:` distinction undefined**: saddle-project.md L9 names both as valid task labels. engine/README.md examples show both forms (L67–68, L72) without defining when each is preferred.

6. **journal invocation window prefixed with "explanatory only" notice** (L1535–1537): Consumer must parse contextual prose before reaching the actual invocation at L1544.

---

## F. Contradictions

1. **No stamp mismatch exists today**: All five table stamps match their fn file stamps (see H3). Not a contradiction.

2. **audit-beds invocation uses "destination" for a read-only report** (L1545: "destination: report to myShell only"): carry-unfinished and fold-entry use "destination" to mean a write target. audit-beds never writes. Same word, different meaning across fns. Not a logical conflict but a terminology inconsistency within the corpus.

3. **Independence clause asymmetry**: journal-continuity CONTROLLER.md L56: "no other function is a prerequisite." project-saddle CONTROLLER.md L56: "no journal function is a prerequisite." The former is neutral about project-saddle; the latter explicitly names journal-continuity as non-prerequisite. Not a conflict; asymmetry may reflect authoring order.

4. **No conflict found between either journal invocation and its function contract**: Both L1544 and L1620 invocations supply inputs consistent with their function's stated requirements and authority.

---

## G. Uncertainty / not read

1. **Byte sizes**: not computed; no shell access available in this unit.
2. **Houston cards files** (`cards/consult.md`, `cards/audit.md`, `cards/sitting.md`): referenced by identity.md L49 and houston.md L35–36 but not in BRIEF read list; not read.
3. **Houston project addenda**: addendum walk described in houston.md L28–33 but no addendum file was in the BRIEF read list; not read.
4. **journal/2026-10-16.md outside named windows**: the bulk of the file (1630+ lines) was not read. Only L1535–1560 and L1610–1630 are in evidence. No invocation of fold-entry, list-pending, or carry-unfinished appears in these two windows.
5. **`~/.germline/programs/` existence**: confirmed absent by BRIEF context and AGENTS.md L37–38; not directly verified by a path check.
6. **journal-continuity CONTROLLER stamp `96a5974b`**: this is the CONTROLLER's own stamp, not a fn binding stamp; it is not checked against any table entry by the fn-binding mechanism.
