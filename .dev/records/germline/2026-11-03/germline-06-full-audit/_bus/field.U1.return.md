---
from: field (subagent, Claude, spawned by Flight) · unit U1
date: 2026-10-21
status: native return preserved with light abridgement of repeated cross-references inside table cells (no claim changed); Flight citation checks in units/RESULT.U1.md (Field line numbers drift in places).
---

## U1 return — consumption contracts, dated intent ladder, gaps, conflicts, gavels

Corpus read in full: master-brief.2026-09-23.md, RECONCILIATION.germline-02-guide-model-law.2026-10-13.md, GAVELS.program-guide-law.md, germline-02-guide-model-law/RUNBOOK.md, CLOSE.g04-preparation.2026-10-20.md, germline/README.md, germline/CHATBOT.md, findings.g06.md (reused), coverage.matrix.md (reused), oraculum.unit-plan.return.md, PLAN.md. Bounded reads: majkee journal 2026-10-16 (grep hits, 120 lines), Forge GUIDE.md (grep hits, full header). Not read: program fn files, binding files, HANDOFF.g06-make-program.md interior, G03/Composer/Sella res/ (per scope exclusion).

### Table 1 — Five consumption contracts

| # | Contract | Who loads | Mechanism | Proof | Dated intent |
|---|---|---|---|---|---|
| 1 | Houston runtime-load (wrapper→identity→binding→addendum→card, stamps quoted) | Houston (the agent itself, both vendors, at entry) | Thin vendor wrapper carries no procedure; agent reads identity.md → binding.<vendor>.md → nearest project addendum → cards/<card>.md; quotes each file's `stamp:` in its reply | README.md:8-11 (rule); findings.g06 E1 (one witnessed run, 2026-10-17 :75-92, stamp-quoting confirmed) | Houston runtime-load fold, 2026-10-10 — Forge GUIDE.md:13 banner names it; README.md :8 encodes it |
| 2 | Personal programs (ctrl <program>&<function>, CONTROLLER table pins stamps) | myShell only ("only declared caller" — findings.g06, CONTROLLER.md) | `ctrl <program>&<function>` → CONTROLLER.md + selected fn/<verb-object>.md; CONTROLLER's functions table pins expected stamps; hold-no-fallback on mismatch; no automatic discovery | PLAN.md :7 (CORRECTION to friction (5): stamps are table-pinned, not caller-supplied); findings.g06 CORRECTION 2026-10-21; programs explicitly "uncanonical personal trials" (findings.g06 §Authority) | G02 accepted planning directions 2026-10-13/14 (RECONCILIATION); PG-r3 gaveled 2026-10-15 (GAVELS G1/G3/G4) — planning authority only, no implementation authority yet |
| 3 | Chatbot skill files read as-is (ChatGPT, Claude.ai) | Chatbot (ChatGPT, Claude.ai, or next) | Direct file read from reposoma/.germline/skills/ via GitHub connector or hand-drop; CHATBOT.md is the guide card; no stamp checking; body is the method in first person | CHATBOT.md (full, path: ia-sync/germline/CHATBOT.md); README.md:6 ("vendor-neutral methods; the chatbot skills … read these files as-is"); coverage.matrix R06 INSPECTED | README.md gaveled 2026-09-25; CHATBOT.md undated (no explicit gavel date found in sources read); germline-01 deploy 2026-10-12 set ia-sync as source |
| 4 | Tunnel preamble injected by shim | Tunnel shim (not the agent reading it; injected as prepend before context) | germline/tunnel/tunnel.preamble.md prepended by the shim; agent receives it without knowing the load path; file carries no stamp (findings.g06 S3) | README.md :6 (skill/tunnel listed); findings.g06 S3; coverage.matrix R15 INSPECTED | No explicit operator gavel date found for this design in sources read; file mtime 2026-10-10 (per PLAN.md :6, reposoma fork has `updated: 2026-10-10`) — predates germline-01 |
| 5 | Vendor-native wrappers loading no germline (Oraculum) | Nobody loads germline; wrappers are fully self-contained per vendor | claude/agents/oraculum.md and codex/agents/oraculum.toml are independently defined with different callers (Claude: hooks+Bash; Codex: bounded child, different model string); no germline oraculum identity file exists | findings.g06 System pass; coverage.matrix R19/R20 INSPECTED | No germline-binding criterion stated anywhere in sources read — UNDERSPECIFIED (findings.g06 §Underspecified: "Oraculum cross-vendor contract") |

### Table 2 — Dated intent ladder

| Date | Claim | Source file:line | Surfaces implementing it | Surfaces contradicting it |
|---|---|---|---|---|
| 2026-09-23 | Build-time render: identity.md composed INTO wrapper at build; provenance stamp in wrapper | master-brief.2026-09-23.md:43-47 ("physically the direction is reversed: the shared MD is rendered into the wrapper's instruction field at build time") | Forge GUIDE.md §0-§3 (now stale per banner) | Forge GUIDE.md:13 (STALE banner 2026-10-14); README.md :8-11 (runtime-load model) |
| 2026-09-23 | canonical tree: reposoma/.germline/agents/<slug>/identity.md | master-brief.2026-09-23.md:73-76 (§Tree) | Forge GUIDE.md §2 fold-scheme :59 | README.md :3-4 (ia-sync/germline/ as source); findings.g06 G-A; Forge GUIDE.md:13 banner |
| 2026-09-23 | "Print mode -p is NEVER used — operator law … destructive hold" (gaveled) | master-brief.2026-09-23.md:58-59 | All session prompts omit -p; RUNBOOK.md pattern | No contradiction found |
| 2026-09-25 | Source = ia-sync/germline/; deployed copy = ~/.germline/ (real, never symlink) | README.md:3-4 (gaveled 2026-09-25, majkee) | deploy.sh germline leg; germline/README.md; findings.g06 E2 | Forge GUIDE.md §2 :59 still names reposoma home + symlink (stale, per banner); Forge R04 :26 names old path with no chapter-level banner |
| 2026-10-07 | Forge GUIDE verified; binding homes gaveled; seven-file build-time model distilled from Houston forge | Forge GUIDE.md:6,11 | Forge GUIDE.md §1-§6; res/fold-scheme, res/checks, res/witness | STALE banner (2026-10-14) marks §0-§3 superseded; R03/R04/R05 carry no per-chapter banner |
| 2026-10-10 | Houston runtime-load fold: wrapper = thin loader only; agent reads identity→binding→addendum→card at entry, quotes stamps | Forge GUIDE.md:13 (banner mentions the fold by date); README.md:8-11 | README.md:8-11; binding.claude.md + binding.codex.md; houston.md wrapper | Forge §0-§3 still describe build-time model |
| 2026-10-12 | germline-01: ia-sync/germline/ = source; ~/.germline/ = real deploy target | README.md:3 note ("germline-01, majkee GO 2026-10-12"); Forge GUIDE.md:13 | deploy.sh germline leg; findings.g06 E2; README | reposoma/.germline fork: 6 files differ, not retired |
| 2026-10-13..14 | Nine planning directions: binding procedure in germline programs; GUIDE = book; programs public; vendor skills = thin loaders; one-home promotion | RECONCILIATION.germline-02-guide-model-law.2026-10-13.md:86-109 (accepted 2026-10-14) | G02 RUNBOOK §Fixed facts; GAVELS; CONTROLLER.md files (personal trial only) | Programs are "uncanonical personal trials"; C1(a-c) deferred to germline-03 (unresolved) |
| 2026-10-15 | G1-G7 gaveled (PG-r3 accepted, verbatim Majkee receipt) | GAVELS.program-guide-law.md:62-163 | G02 RUNBOOK; CONTROLLER.md (personal trial) | Planning authority only ("not installed law" — GAVELS :41); C1 deferred |
| 2026-10-16 | "germline extends its composition into controllers, selected functions, bindings and cooperating agents" | HANDOFF.g05-sella-germline-audit.md:16-17 | G06 RUNBOOK.md:34-35 (restated verbatim) | No cooperating-agent surface in germline/ or programs/ (grep: no matches) |
| 2026-10-16 | G04 wiring: bus topology elected; G05→G06 handoff chain | journal/2026-10-16.md:17,34-39 | G04 RUNBOOK/STATUS; G05/G06 beds | None |
| 2026-10-20 | G04 CLOSE: no remaining execution; G06 audit-only; make-program proposal superseded | CLOSE.g04-preparation.2026-10-20.md:10-12 | G06 RUNBOOK.md:30-33 | None |

### Gaps — intent without implementing surface

1. **"cooperating agents"** — stated in HANDOFF.g05-sella-germline-audit.md:17 and restated in G06 RUNBOOK.md:34-35. No file in germline/ or programs/ implements a cooperating-agent mechanism. Source: grep no-match in both trees.
2. **"agent is the primary consumer"** (G06 RUNBOOK.md:35) — declared as philosophy; chatbot readers and human readers consume the same file shapes without a distinguishing mechanism.
3. **Public programs serving "any seat, vendor, chatbot, or human"** (RECONCILIATION:90, direction #4) — programs are currently private personal trials. Acknowledged in GAVELS ("planning only").
4. **"thin vendor loader only — no procedure in vendor-specific files"** (RECONCILIATION:85, direction #6; GAVELS G1:73) — binding.claude.md and binding.codex.md carry substantial procedure (load order, addendum steps, return shape). Planning direction names a future state, not the current one.
5. **Explicit project/global/project-first resolution with confirmed local absence** (RECONCILIATION:83, direction #7; GAVELS G4:99) — CONTROLLER uses an alias shortlist; Houston uses cwd walk-up. Neither implements it. GAVELS G4 deferred C1(a-c) to germline-03 (unresolved per GAVELS:163).

### Contradictions between dated intents

**C1 — Build-time (09-23) vs Runtime-load (10-10):** Master-brief (09-23) establishes build-time render ("physically the direction is reversed: the shared MD is rendered into the wrapper's instruction field at build time" — master-brief:44). The Houston runtime-load fold (10-10) inverts this. Forge GUIDE.md:13 banner marks the old model stale; NOT on res/checks.md, res/fold-scheme.md, res/witness.md.

**C2 — Reposoma canonical home (09-23 tree / Forge §2) vs ia-sync home (09-25 rule / 10-12 deploy):** Master-brief:73-76 §Tree names reposoma/.germline/agents/<slug>/identity.md. README.md (gaveled 09-25) makes ia-sync/germline/ the source. Forge R04:26 still names the old path and the symlink with no chapter-level banner. A reader following Forge R04 reads the stale forked identity.

**C3 — Planning-accepted program law (10-15) vs personal-trial status (current):** GAVELS marks all decisions "accepted planning proposal, not installed law" (GAVELS:41). Intent says public programs; surface says personal trial. Not a defect — implementation gate not opened.

### Majkee-gaveled statements (exact text, file:line)

All from GAVELS.program-guide-law.md, operator-carried final acceptance 2026-10-15. Authority: verbatim receipt SHA `3a4783e8…` (GAVELS:21).

- G1 (GAVELS:73-75): "Accept the G1 candidate: public `programs/<slug>/CONTROLLER.md` with `fn/<verb-object>.md`; process is one invocation; `perform` is the thin public doorway; `guide read|write` remain working vocabulary."
- G2 (GAVELS:79-82): "Accept the G2 candidate: GUIDE remains the discretionary knowledge book; `res/` remains registered knowledge depth under current chapter law; no executable function table or second maintained operational recipe belongs in GUIDE."
- G3 (GAVELS:86-90): "Accept the G3 candidate: cross-occasion or costly/irreversible rules are controller invariants; other bounded rules belong in one sufficient selected function. A program is larger than an invocation skill and smaller than a topic book; an independently insufficient function folds into its caller."
- G4 (GAVELS:99-107): "The normal selection is one coherent line: controller plus selected function from one scope, loaded on the agent side through the shared germline path. Global-controller plus project-local-function composition is an exceptional, explicitly declared and composer-verified shape, never inferred from files being present and never the expected split-program form."
- G5 (GAVELS:113-122): "A vendor-native surface may maintain a small explicit binding table from named public program capabilities/functions to its harness or CLI mechanism. The table is entered through the vendor's native route and contains native translation, qualification and evidence adaptation only. It is not discovery, a task router, a function census or an alternate procedure home."
- G6 (GAVELS:127-131): "Accept the G6 candidate: public programs require capabilities but grant none; private cards retain invokers/grants/agent authority and may explicitly call public programs; public programs never depend on private cards."
- G7 (GAVELS:136-143): "Retire BACKGROUND as a prescribed slot. A GUIDE may carry an optional guide-local maintenance/history journal only in the shape `<guide-slug>/{GUIDE.md,src/journal-...}`."
- README.md:3 (gaveled 2026-09-25): "Rule (gaveled 2026-09-25, majkee): what lives here is the source (ia-sync `germline/`; deployed copy: `~/.germline/`); every vendor file derived from it is a one-way, stamped rendering (`derived from <path> @ <revision> — do not edit here`)."
- Majkee verbatim final acceptance (GAVELS:162): "I accept PG-r3 (ecc6566c…), reviewed by Atlas AR-r3 (802b5aa1…), with AS-r4 (6a1cc469…) and GV-r4 (0ec78c04…), as the planning proposal… I defer C1 to germline-03-foundation-audit as required inputs… Every exceptional line stays HELD until those are resolved."

Operator-gaveled vs agent-proposed: all GAVELS G1-G7 are operator-carried final acceptance. README :3 rule also operator-gaveled. Master-brief subject gavel (Atlas pilot) is operator-gaveled (master-brief:109). Planning directions in RECONCILIATION :86-109 were "accepted 2026-10-14" by Majkee as planning direction only. The "cooperating agents" / "agent is primary consumer" phrases in HANDOFF.g05:17 and G06 RUNBOOK.md:34-35 are agent-authored (myShell/planning head) — not gaveled.

### Uncertainty and what was not read

Not read: HANDOFF.g06-make-program.md interior, program fn files (audit-beds, carry-unfinished, list-pending, saddle-project), binding.claude.md and binding.codex.md in full, houston identity.md in full, G03 material, Composer grammar, Sella res/, Forge raw/observations.atlas-ui. The Forge 10-07 date is confirmed from GUIDE.md header and note.atlas-ui-to-carrier.2026-10-07.md:1; the 10-10 fold date is confirmed from Forge GUIDE.md:13 banner only. The tunnel preamble's gavel date is not confirmed. G4's C1(a-c) deferred (GAVELS :163) but germline-03 gate has not been opened.
