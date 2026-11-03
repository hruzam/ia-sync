---
from: field · unit U5 · date: 2026-10-21
---

## A. Project-layer inventory

Globs run: `unikuklatrix/*/.germline/**/*.md`, `ia-sync/.germline/**/*.md`, `reposoma/.germline/agents/**/*.md`, `reposoma/.majkee/.germline/**/*.md`, `projects/*/.germline/**/*.md`.

| path | lines (read) | stamp | role | status |
|---|---|---|---|---|
| `nablarva/.germline/agents/houston/nablarva.md` | 133 | d9ee9067 | project addendum — Houston specialisation for nablarva | live, CANDIDATE state |
| `nablarva/.germline/agents/convergence.md` | 82 | none | convergence wrapper-keeper role | retired (nablarva.md:60; no in-file marker) |
| `reposoma/.germline/agents/houston/identity.md` | not read | not read | full identity copy | historical/pre-migration (chatbot-targeted fork; RECONCILE.G01:34 "fork is chatbot target, not a ghost") |
| `reposoma/.germline/agents/houston/binding.claude.md` | not read | not read | full binding copy | historical/pre-migration |
| `reposoma/.germline/agents/houston/binding.codex.md` | not read | not read | full binding copy | historical/pre-migration |
| `reposoma/.germline/agents/houston/cards/consult.md` | not read | not read | full card copy | historical/pre-migration |
| `reposoma/.germline/agents/houston/cards/audit.md` | not read | not read | full card copy | historical/pre-migration |
| `reposoma/.germline/agents/houston/cards/sitting.md` | not read | not read | full card copy | historical/pre-migration |
| `reposoma/.majkee/.germline/programs/journal-continuity/CONTROLLER.md` | not read | not read | program controller | live, majkee-personal, not a Houston addendum |
| `reposoma/.majkee/.germline/programs/journal-continuity/fn/*.md` (4 files) | not read | not read | program fns | live, majkee-personal |
| `reposoma/.majkee/.germline/programs/project-saddle/CONTROLLER.md` | not read | not read | program controller | live, majkee-personal |
| `reposoma/.majkee/.germline/programs/project-saddle/fn/saddle-project.md` | not read | not read | program fn | live, majkee-personal |
| `ia-sync/.germline/` | 0 files | — | empty | absent |
| `projects/` depth ≤ 3 | 0 files | — | none found | absent |

Only nablarva carries a project-layer Houston addendum. reposoma/.germline/ is a full-copy fork (chatbot target), not an addendum layer. reposoma/.majkee/.germline/ is majkee-personal programs.

---

## B. nablarva.md section map

| section | what it carries | class |
|---|---|---|
| frontmatter (:1–12) | project, scope constraint, authority (flag commit-pin + full record path), state (CANDIDATE), home (LOADER walk-up note), dates, stamp d9ee9067, revision b57e199, authorship | context, provenance |
| preamble (:15–16) | base path declaration ("repo-relative to /home/hruzam/unikuklatrix/nablarva/") | paths |
| §1 The map (:18–30) | identity roles → nablarva disk homes table (PROJECT.yaml · PROJECT-DESIGN.md · docs/ARCHITECTURE.md · organ bodies · flag · pulse · session · saddle) | paths · locks (locked: L16.9) |
| §2 Card output landings (:32–39) | per-card (consult/audit/sitting) invocation party · output shape · landing path · write limits; one `inferred: atlas` tag | procedure · paths · authority |
| §3 Trigger + intrinsic classes (:41–52) | trigger class list (pointer to record §4) · intrinsic class list · earned mechanisms null | procedure pointer · locks (locked: L16.6–8) |
| §4 Keeper current state (:54–90) | audit card = keeper (since 31bd51e) · convergence retired · pre-31bd51e migration plan (labeled "*History*" at :67) | authority · history (locked: L16.14) |
| §5 Project procedures (:92–113) | session surfaces · bus method · archive rule · naming law · mail rule · entry commands · no-project-wrappers rule | procedure · paths · authority |
| §6 First-audit seed (:115–125) | historical stale items and repair record | history |
| §7 What this addendum does not do (:127–133) | scope negations (no write outside §2 paths; does not retire convergence; flag wins on contradiction) | authority |

---

## C. H1–H7 evidence tables

### H1 — D4 fit

D4 accepted wording (RECONCILE.G01:34): `"A project may explicitly attach an agent-specific local layer carrying its project context, paths and applicable locks."`

nablarva.md frontmatter scope (:4): `"may add paths, procedures and local method; may not override the identity or any lock in flag.md"`

The scope string widens D4's "context, paths and applicable locks" to include "procedures and local method." RECONCILE.G01:34 notes "authority limits remain (addendum 'specialises, never overrides a lock'; feedback §3.5: a project layer narrows, never widens, the route matrix)."

Sentences that are **procedure / authority / method** (not context):

| line | text (quoted) | class |
|---|---|---|
| :35 | "`majkee commits the diff`; I never apply it to the wrapper, and neither I nor a helper edits another head's STATUS" | authority |
| :36–37 | "`exact filenames assigned by the invocation (suffix if two audits share a date)`" | procedure |
| :37 | "`the sitting card never writes flag.md (L16.12/14)`" | authority (reinforces lock) |
| :43 | "Trigger classes (the head decides whether to invoke consult)" | procedure pointer |
| :50 | "Known at authoring → RUNBOOK constraints; found mid-session → STATUS `holds:`; a new permanent class → majkee GO → flag." | procedure |
| :95–98 | "flag.md owns locks; pulse.md routes… I never write a POINT or a VERDICT" | procedure + authority |
| :99–104 | archive rule · naming law · mail rule | procedure |
| :106–110 | entry commands (`claude --agent houston` · `codex --profile houston -C …`); delegated route on Codex when Cartan is head — "local policy, not a vendor requirement" | procedure, local method |
| :111–113 | "`.claude/agents/houston.md` and `.codex/agents/houston.toml` must not exist here" | authority (placement rule) |
| :129–133 | "grants no write outside §2's landing paths… If a line here contradicts flag.md, flag wins" | authority |

Sentences that could be read as **overriding** identity or binding: none found that contradict. nablarva.md:111–113 restates binding.claude:42–44 and binding.codex:54–56 in spirit. nablarva.md:107–108 names vendor-specific entry commands (`claude`, `codex`), which identity.md:130–132 deliberately excludes ("Nothing vendor-specific lives in this file"). The addendum places these under its "local method" claim; it does not contradict the identity's own scope.

Evidence **against** D4 fit: the frontmatter scope string was authored 2026-10-06 (:11); D4 was gaveled 2026-10-21 per RECONCILE.G01:31. Whether §5 procedures "narrow" or "extend" the route matrix is not tested in any file read today.

---

### H2 — Selection

Rule text (houston.md:29–34): `"resolve the session working directory (pwd -P when shell access exists) and walk its ancestors upward. At each ancestor, look for .germline/agents/houston/<ancestor-basename>.md; select the first unambiguous readable one, continuing past a directory with no matching addendum. Never select the global ~/.germline. Ambiguous cwd or selection → I report it before card work and do not guess a project. None found → I am neutral Houston; I say so in my first line."`

Rule text (identity.md:142–144): `"the nearest project addendum (walking up from the session's working directory to the first .germline/agents/houston/ that is not the global one) → cards/<card>.md; a later layer specialises, never overrides an earlier one or a project lock."`

Basename confirmed: `nablarva.md` basename = `nablarva` = repo dir `/home/hruzam/unikuklatrix/nablarva` ✓

**What the rule leaves unsaid:**

| gap | evidence |
|---|---|
| Dir name ≠ intended addendum name | No mechanism defined in any file. Walk-up is basename-only. |
| Definition of "ambiguous" | Not defined in houston.md:33 or identity.md:143 beyond the hold statement. |
| Explicit project declaration overrides walk-up | Identified as a gap by RESULT.U3.md:28: `"one sentence ('explicit project declaration in the assignment overrides the walk-up, echoed in the entry proof') → U5"`; fold/repair table RESULT.U3.md:47: `"explicit declaration overrides walk-up | U5 (Houston wrapper/binding; re-rolls canary) | —"`. No current authored file contains this rule. |
| Two ancestors each with an addendum | "Select the first unambiguous readable one" (houston.md:32) — nearest ancestor wins; ambiguity criteria undefined. |
| Session started outside any project | Covered: "None found → neutral Houston" (houston.md:34). |
| Subdirectory cwd | Walk-up through `nablarva/subdir → nablarva → unikuklatrix` reaches nablarva.md. Covered by rule without special handling. |

---

### H3 — Retired role

convergence.md frontmatter (:1–5):
```
name: convergence
description: Maintain nabLarva's project-design wrapper across runtimes
target: PROJECT-DESIGN.md
```
No `state:` field. No "retired," "tombstone," or similar text anywhere in the file.

Retirement record outside the file:
- nablarva.md:60–62: `"Convergence (.germline/agents/convergence.md) is retired as keeper; the file stays as history."`
- flag.md L16.14 (:177–179): `"Convergence (.germline/agents/convergence.md) is an ad hoc, uncanonical seat that may be retired without ceremony; when it retires, the audit card keeps PROJECT-DESIGN.md."`

No rule in any file read today defines how a retired germline file must be marked. "Without ceremony" (flag.md:178) explicitly confirms no required marker; it does not specify an optional one either.

---

### H4 — Flag pointers

**`locked: L16.9`** (nablarva.md:18, §1 heading):
- flag.md L16.9 (:151–154): `"Documentation homes. PROJECT.yaml = machine skeleton and pointers; PROJECT-DESIGN.md = thin animal wrapper and index; docs/ARCHITECTURE.md = whole-animal cross-organ architecture; organ body = local contract, detail, key files; flag.md = locks; pulse.md = live-session router; session = temporary work."`
- nablarva.md §1 table maps each of these homes. Match ✓

**`locked: L16.6–8`** (nablarva.md:41, §3 heading):
- flag.md L16.6 (:138–143): intrinsic classes (new/reopened locks, irreversible, trust-boundary, ownership, architect-authored consequential, `breaks` verdict). ← matches nablarva.md:48–50 ✓
- flag.md L16.7 (:144–146): earned ceremony. ← nablarva.md:51: `"Earned mechanisms (thresholds are proposals under L16.7...): none is in force."` ✓
- flag.md L16.8 (:147–148): no autonomous loops. ← nablarva.md does not re-state L16.8 text explicitly; the heading groups §3 under L16.6–8 as a range.
- Trigger classes (nablarva.md:43–46) are cited as `"Source: record architecture-process §4"` — not explicitly in any L16 clause. nablarva.md groups them under L16.6–8 but flag.md L16.6 covers intrinsic classes, not trigger classes. Minor grouping mismatch; nablarva.md:43 correctly attributes trigger classes to the record.

**`locked: L16.14`** (nablarva.md:54, §4 heading):
- flag.md L16.14 (:169–179): Houston pen and keeper; convergence may retire without ceremony; audit card keeps wrapper. ← nablarva.md §4 states exactly this ✓

**`inferred:` tags in nablarva.md:**
- nablarva.md:39 only: `"(inferred: atlas — the audit landing path follows the bed/raw convention; cartan may name a better one.)"` — audit landing path is inferred, not locked. No other `inferred:` tags found.

---

### H5 — Placement rule

binding.claude.md:42–44: `"Projects therefore carry no Houston wrapper; the project layer is the addendum <project>/.germline/agents/houston/<project>.md only."`
nablarva.md:111–112: `".claude/agents/houston.md and .codex/agents/houston.toml must not exist here — a project-scope wrapper would override the global one and skip the germline load."`
binding.codex.md:54–56: `"projects carry no Houston TOML or profile. A project .codex/agents/houston.toml would collide with the personal one (docs promise precedence only over built-ins): do not install a same-named project agent."`

Glob results today:
- `nablarva/.claude/agents/` contains `tester.md` only. No `houston.md`. ✓
- `nablarva/.codex/` — no files found. ✓

Placement rule is satisfied in the current tree.

---

### H6 — Stamp + provenance

nablarva.md frontmatter (:8–11):
```
updated: 2026-10-17
stamp: d9ee9067
revision: b57e199
authored: 2026-10-06 · atlas-ui(harness) · assignment _bus/15 + amendment _bus/16
```
Expected stamp d9ee9067 (from AGENTS.md context) matches (:9). ✓

No sentence in nablarva.md names who re-stamps the addendum or what event triggers a re-stamp. The `authority:` field (:5) names the flag lock and full record as provenance of the L16 clauses, not stamp regeneration. The `authored:` field (:11) names original authorship. No witness record path is cited in the file. RESULT.U3.md:35 proposes a stamp-regeneration rule for programs ("Editing an fn re-rolls its stamp"); no equivalent rule is authored for addenda in any file read today.

---

### H7 — Other projects

| project | .germline/ content | role of content |
|---|---|---|
| nablarva | nablarva.md (addendum) + convergence.md (retired role) | project-layer addendum (only real one found) |
| ia-sync | empty (no .md files) | absent |
| reposoma | 6 files: identity.md + 2 bindings + 3 cards (all houston) | full copies — chatbot-targeted fork (RECONCILE.G01:34); not project addenda |
| reposoma/.majkee | 7 files in programs/ (journal-continuity + project-saddle) | majkee-personal programs; not Houston addenda |
| projects/ depth ≤ 3 | none | absent |

reposoma/.germline/ expected to carry no project-scoped content per D3 disposition (RECONCILE.G01:34); that finding is confirmed — it carries full copies, not an addendum.

---

## D. Contradictions / stale

1. **convergence.md has no in-file retirement marker** (convergence.md:1–5). Retirement is recorded in nablarva.md:60 and flag.md:177, not in the file itself. A cold reader of `.germline/agents/` without first reading nablarva.md §4 sees an apparently active role definition. `flag.md:178` says retirement requires no ceremony — no marker is required — but none is present even optionally.

2. **nablarva.md:41 groups trigger classes under `locked: L16.6–8`**. flag.md L16.6 (:138) covers intrinsic classes; trigger classes come from `architecture-process §4` (full record), not from any L16 clause directly. nablarva.md:43 correctly names the source as the record, but the heading implies L16.6 covers trigger classes. Partial misalignment; does not affect the locked content.

3. **nablarva.md:4 scope string vs D4 wording.** nablarva.md:4: `"may add paths, procedures and local method"`. D4 (RECONCILE.G01:34): `"project context, paths and applicable locks"`. The scope string is wider and was authored before D4 was gaveled (authored 2026-10-06; D4 gaveled 2026-10-21). Whether "procedures and local method" needs re-alignment to D4 is not decided in the files read today.

---

## E. Friction for a cold Houston entering nablarva (ranked)

1. **convergence.md has no retirement marker** (convergence.md:1–5). Highest friction: a cold Houston reading `.germline/agents/` sees an active-looking role with no state field. Retirement notice is in nablarva.md:60 and flag.md:177, requiring prior reading of those files.

2. **No "explicit declaration overrides walk-up" mechanism authored** (RESULT.U3.md:28, :47). If a session starts with an explicit project directive that does not match the walk-up result, there is no current rule for resolution. The gap is proposed for this unit (U5) but is not yet in any file Houston loads at entry.

3. **`inferred: atlas` on audit landing path** (nablarva.md:39). The audit output landing path is marked inferred, not locked. A cold Houston running an audit cannot treat the path as settled; the tag flags it as requiring confirmation.

4. **CANDIDATE state** (nablarva.md:6: `"CANDIDATE — review stage"`). The addendum is not a finalized standard. A cold Houston sees a not-yet-approved specialisation and must treat procedure details as under review.

5. **History block length in §4** (nablarva.md:67–86, ~20 lines labeled "*History — the migration as planned before 31bd51e*"). The migration history is inline and verbose. The "*History*" label at :67 is explicit, but a cold reader must scan past it to reach current procedure. No summary line separates current state from historical record at a glance.

---

## F. Uncertainty / not-read

- Byte sizes for all files in inventory: not obtained (Glob returns paths only).
- reposoma/.germline/ files (6 files): content not read — stamps, revision dates, and divergence from ia-sync/germline/ source unverified in this unit.
- reposoma/.majkee/.germline/ program files (7 files): content not read — stamps and fn details unverified.
- germline/README.md (global source README): not read — possible additional rule on retired-file marking not checked at source.
- flag.md beyond line ~182 (L17 and later): lines 193–204 were returned by pagination but not cited; content beyond L16.15 is not part of this unit's findings.
- nablarva/.claude/agents/tester.md: not read — content not relevant to H5.
- "Explicit declaration overrides walk-up" rule assigned to U5 in RESULT.U3.md:47: not yet authored in any file; final wording unknown.
- unikuklatrix projects at depth > 1 level below unikuklatrix/ not probed (glob pattern was `unikuklatrix/*/.germline/` — one level only).
