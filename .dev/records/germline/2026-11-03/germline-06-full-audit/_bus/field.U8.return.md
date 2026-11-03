---
from: field · unit U8 · date: 2026-10-21
sources-read: binding.claude.md, binding.codex.md, claude/agents/oraculum.md, codex/agents/oraculum.toml, architect/challenger/researcher.toml, codex/AGENTS.md, raw.card.model-effort.md, claude/agents/houston.md :1-21, codex/agents/houston.toml :1-9, codex/profiles/houston.config.toml :1-9, germline/README.md :1-12, germline/CHATBOT.md :1-30, findings.g06.md (E4 section); globs run; git show not available (see G)
---

## A. Seat inventory

| Seat | Claude file | Codex file | Germline identity | Pins (model · effort) | Canary / route | Hook / sandbox |
|---|---|---|---|---|---|---|
| houston | claude/agents/houston.md | codex/agents/houston.toml (child) + codex/profiles/houston.config.toml (main) | YES — identity.md + binding.claude.md + binding.codex.md | claude: opus·high; codex child: gpt-6.1-sol·high; codex main: gpt-6.1-sol·high (all match card active_pins) | cl-<8hex> (claude); hc-<8hex> child / hp-<8hex> main (codex) | Claude: "a Claude child has no sandbox key" (binding.claude.md:49); Codex: sandbox_mode ignored for children (binding.codex.md:48-50) |
| oraculum | claude/agents/oraculum.md | codex/agents/oraculum.toml | NO — each file self-contained | claude: fable·high (oraculum.md:12-13; not in card); codex: gpt-6-astra·high (oraculum.toml:4-5; not in card) | none in either file | Claude: PreToolUse[Bash] hook (oraculum.md:25-29); Codex: [features] apps/plugins/memories/request_permissions_tool = false (oraculum.toml:49-54) |
| astrobley | claude/agents/astrobley.md | codex/agents/astrobley.toml | NO (not stated) | not read (out of brief scope) | — | — |
| architect | none | codex/agents/architect.toml | NO | gpt-5.6-sol·xhigh (architect.toml:3-4); not in card; card:45 notes as unreconciled | none | sandbox_mode = "read-only" (architect.toml:7); no in-file comment stating it is inert |
| challenger | none | codex/agents/challenger.toml | NO | gpt-5.6-sol·xhigh (challenger.toml:3-4); not in card; same drift note | none | sandbox_mode = "read-only" (challenger.toml:7); no in-file comment |
| researcher | none | codex/agents/researcher.toml | NO | gpt-5.6-terra·high (researcher.toml:3-4); not in card; same drift note | none | NO sandbox_mode key |
| 31 Claude-only seats | advisor-*, agol, assay, atlas-*, capcom, color, delta, eagle, epoch, ferry, field, flight, hypatia, janus, maxwell, metaterminal, mirror, recorder, shannon, symmetry, trajectory, vara, vega, vector, zenith, zenith-zsh, zed-editor-expert | none | NO | not read | — | — |
| implementer, verifier, harness_builder | none | codex-only | NO | not read | — | — |

Seats on both vendors: houston, oraculum, astrobley. Only germline-bound seat: houston.


## B. Binding parity table (H1)

| Rule | binding.claude.md | binding.codex.md | Status |
|---|---|---|---|
| Wrapper body = LOADER only | "body the LOADER only" (:20) | "This file is a thin loader: it carries no identity, card or project prose" (codex/agents/houston.toml:1 + profile:9, echoed in binding :10) | Same |
| Model/effort = "weather" | "weather, set in the wrapper only" (:18) | "weather, set in the wrappers only" (:20) | Same |
| Mirror in active_pins | "mirrored in raw.card.model-effort.md active_pins" (:18) | "mirrored in raw.card.model-effort.md active_pins" (:21) | Same |
| One wrapper vs two | "one file serves both routes" (:21); path: claude/agents/houston.md | Two files: houston.toml (child) (:17) + houston.config.toml (main) (:18) | Vendor-delta (Claude single-file; Codex child/main split) |
| Consult writes nothing | "Consult writes no file on any route; a write request is out of card:" (:49) | "Consult writes no file on any route; a write request is out of card:" (:47) | Same |
| Delegation ban — child consult | "never an executor (delta, trajectory, vector), never atlas-*, never Houston → Houston" (:39) | "any helper is bounded to reading or verification, never Houston's judgment or a wider pen" (:44) | Vendor-delta: Claude names roles explicitly; Codex does not |
| sandbox_mode / sandbox note | "a Claude child has no sandbox key; one wrapper serves both routes" (:49-51) | "sandbox_mode in the agent TOML is ignored for children (witnessed 2026-10-17, C-def.2)" (:48-50) | Vendor-delta (different runtime facts; both note inertness; Codex adds witness) |
| Effective cwd | "Context is CWD-based...Start in the project root" (:45-46) | "Child cwd is not guaranteed...child's entry proof records its effective cwd" (:57-58) | Vendor-delta (Codex acknowledges docs gap; Claude does not) |
| Canary prefix | "cl-<8hex>" (:23) | "hc-<8hex>" child / "hp-<8hex>" main (:24) | Vendor-delta (expected; different prefixes per route) |
| Placement | "projects carry no Houston wrapper; project layer is the addendum" (:42-44) | "projects carry no Houston TOML or profile...project layer is the addendum only" (:53-55) | Same principle |
| Entry proof includes cwd | Route line + stamp lines (:57-58) | Route line + stamp lines + "plus the effective cwd" (:79-81) | Vendor-delta: Codex adds cwd to proof; Claude does not |
| Sources section | Absent | Present (:85-87) — Codex docs URLs | Missing from Claude binding |
| Spawn bounded by instruction | "Spawn is bounded by instruction, not by the runtime" (:47) | "A native delegation tool only when available and when the card and the invoker authorize" (:69) | Same intent; Codex more detailed |


## C. Oraculum divergence table (H2, H8)

| Field | claude/agents/oraculum.md (line) | codex/agents/oraculum.toml (line) | Type |
|---|---|---|---|
| Germline source | None — 144-line self-contained identity | None — 47-line developer_instructions block | Same (no germline for either) |
| Cross-reference to other vendor file | Absent | Absent | Same (neither cites the other or any shared source) |
| Model | fable (:12) | gpt-6-astra (:4) | Vendor-delta (card notes astra ≈ fable; both not pinned in card active_pins) |
| Effort | high (:13) | model_reasoning_effort = "high" (:5) | Same value; different key name |
| In card active_pins | NOT listed | NOT listed | Both absent from card |
| Authorized callers / spawn rule | "User invokes directly; not spawned by Houston" (:9) | description :3: "authorized Cartan, myShell, Astrobley, or Houston consultations"; developer_instructions :8-9: "authorized Cartan, myShell, Astrobley, or Houston consultation" | ⚡ CONFLICT — Claude .md says not spawned by Houston; Codex .toml explicitly authorizes Houston as caller |
| Hook (PreToolUse[Bash]) | Yes: matcher "Bash", command "bash ~/.claude/hooks/oraculum-bash-whitelist.sh" (:25-29) | Absent | Vendor-delta (Claude-only mechanism; no Codex analogue) |
| Sandbox / features | No sandbox key in frontmatter | [features] apps=false, plugins=false, memories=false, request_permissions_tool=false (:49-54) | Vendor-delta (Codex-only mechanism) |
| Return shape | Not prescribed in .md | ORACULUM RETURN / CYCLE / INSIGHT / RECOMMENDATION / EVIDENCE / CURVATURE / RETURN_TO_CALLER (:39-46) | Vendor-delta (Codex prescribes; Claude does not) |
| "Not spawned by Houston" | "User invokes directly; not spawned by Houston" (:9) | description and developer_instructions include Houston (:3, :8-9) | ⚡ CONFLICT (H8) |

**H8 cross-vendor drift:** Commit 286085d message "codex: broaden Oraculum authorized callers" (2026-10-20; from git log). Current oraculum.toml description and developer_instructions include Houston as authorized caller. Claude oraculum.md :9 still states "not spawned by Houston." The git diff was not directly read (no Bash tool; see G); inference from commit message + current TOML + findings.g06.md:58 ("Delta edited source on GO (patch :3), commit 286085d changed codex/agents/oraculum.toml under Majkee's authorization"). The Claude .md was not updated in 286085d.


## D. H3–H7 evidence tables

### H3 — Criterion for germline identity

| Question | Evidence | File:line |
|---|---|---|
| Any written rule stating when a seat gets a germline identity | None found in any of: README :1-12, CHATBOT.md :1-30, binding.claude.md, binding.codex.md, oraculum.md frontmatter, oraculum.toml, role TOMLs | — (absence) |
| README statement covering germline load | "Runtime-load variant (Houston, final fold 2026-10-10): the wrappers carry only a loader; at entry the agent reads identity.md → binding.<vendor>.md → the nearest project addendum → cards/<card>.md and quotes each file's stamp:" | germline/README.md:8-11 |
| "loader" / "germline" hits in claude/agents | houston.md:22 "This file is a thin loader: it carries no identity, card or project prose."; houston.md:23 "My meaning lives in the germline; I load it before I answer anything."; atlas-ui.md:96-97 uses "germline" to mean forging/authoring it (not loading) | claude/agents/houston.md:22-23 |
| "loader" / "germline" hits in codex/agents | houston.toml:1 "Meaning lives in ~/.germline/agents/houston/; this file only loads it."; houston.toml:10-11 mirror of the claude loader text | codex/agents/houston.toml:1, :10-11 |
| "derived from" or "source:" hits | None found in claude/agents/*.md or codex/agents/*.toml | — (absence) |
| D1 existing instances ("each agent declares how its runtime consumes its sources") | Only houston.md:22, houston.toml:1, houston.toml:10 use this pattern. No other agent in either directory carries a loader line or germline reference in its wrapper. | — |

No written criterion distinguishes Houston (germline) from Oraculum (vendor-native). The distinction is established only by what exists, not by any rule.

### H4 — Pins

| Route | card active_pins (raw.card.model-effort.md:line) | Wrapper value (file:line) | Status |
|---|---|---|---|
| claude/houston | model: opus, effort: high (:17-19) | model: opus, effort: high (houston.md:12-13) | MATCH |
| codex/houston-child | model: gpt-6.1-sol, effort: high (:24-27) | model = "gpt-6.1-sol", model_reasoning_effort = "high" (houston.toml:6-7) | MATCH |
| codex/houston-main | model: gpt-6.1-sol, effort: high (:29-33) | model = "gpt-6.1-sol", model_reasoning_effort = "high" (profile.toml:5-6) | MATCH |
| claude/oraculum | NOT in card | fable · high (oraculum.md:12-13) | NOT PINNED in card |
| codex/oraculum | NOT in card | gpt-6-astra · high (oraculum.toml:4-5) | NOT PINNED in card |
| codex/architect | NOT in card; card:45-46 "Codex roster in ~/ia-sync/codex/agents/ still pins gpt-5.6-sol / gpt-5.6-terra...Not reconciled by this card." | gpt-5.6-sol · xhigh (architect.toml:3-4) | NOT PINNED; noted as unreconciled in card |
| codex/challenger | NOT in card; same drift note | gpt-5.6-sol · xhigh (challenger.toml:3-4) | NOT PINNED; unreconciled |
| codex/researcher | NOT in card; same drift note | gpt-5.6-terra · high (researcher.toml:3-4) | NOT PINNED; unreconciled |

Change rule: card:15 (GAVEL-ONLY header): "the recalibration researcher refreshes verified/evidence/candidates and PROPOSES pin changes; active_pins changes only on majkee's gavel after a witnessed probe." Card:94-98 (Change rule section): researcher refreshes → probe → gavel → renderer regenerates. "The recalibration researcher" is unnamed — no rule identifies which agent or person fills this role.

### H5 — Inert keys

| File | Key present | In-file comment stating inert | Required keys (name, description, developer_instructions) |
|---|---|---|---|
| architect.toml | sandbox_mode = "read-only" (:7) | None | name (:2), description (:3-4), developer_instructions (:9) — all present |
| challenger.toml | sandbox_mode = "read-only" (:7) | None | name (:2), description (:3-4), developer_instructions (:9) — all present |
| researcher.toml | NO sandbox_mode key | N/A | name (:2), description (:3-4), developer_instructions (:9) — all present |

The only germline-layer file that states sandbox_mode is inert is binding.codex.md:48-50, where it addresses the houston agent TOML. Neither the three role TOMLs nor codex/AGENTS.md carries a comment noting the key is ignored. G01 brief (as given in BRIEF.U8) states it is inert for spawned Codex children; the evidence lives in the binding, not in the role files themselves.

### H6 — Hooks as a vendor seam

| Question | Evidence | File:line |
|---|---|---|
| Where Claude oraculum hook is configured | oraculum.md frontmatter, hooks section: PreToolUse, matcher "Bash", type: command, command: "bash ~/.claude/hooks/oraculum-bash-whitelist.sh" | oraculum.md:24-29 |
| Any germline-level or binding-level statement about hooks | None found in binding.claude.md (full), binding.codex.md (full), germline/README.md :1-12 | — (absence) |
| Codex analogue for the Bash hook | Absent from oraculum.toml. [features] block carries request_permissions_tool = false (:53); developer_instructions state "Do not edit files, run mutating commands..." (developer_instructions body) | oraculum.toml:49-54 |
| What replaces it on Codex side | request_permissions_tool = false (:53) and instruction-level constraint in developer_instructions body; no runtime enforcement hook | oraculum.toml |

### H7 — Third vendor (chatbots)

| Question | Evidence | File:line |
|---|---|---|
| What chatbot is told to read | Skills from .germline/skills/skill.<slug>.md; identity from .germline/agents/<slug>/identity.md when majkee assigns it | germline/CHATBOT.md:15-19 |
| Repo for chatbot skills | "GitHub: hruzam/reposoma (private)...The shared home inside it: .germline/" | germline/CHATBOT.md:9-11 |
| binding.chatbot.md or equivalent | Absent — no binding.chatbot.md in germline/agents/houston/ or germline/ root (glob confirmed) | — (absence) |
| Canary / stamp / entry-proof requirements | Not mentioned in CHATBOT.md :1-30 | — (absence) |
| Return shape prescribed | Not mentioned in CHATBOT.md :1-30 | — (absence) |
| README :1-12 chatbot mention | "vendor-neutral methods; the chatbot skills (ChatGPT · Claude.ai) read these files as-is" | germline/README.md:12 |

CHATBOT.md is the only seam document for the chatbot vendor. It is guidance (what to read, where to find it) — not a structured binding. No canary, no stamp rule, no entry proof, no return contract equivalent to those in binding.claude.md and binding.codex.md.


## E. Where vendor facts live

| Fact | File:line | Category |
|---|---|---|
| Houston model/effort pins | binding.claude.md:18; houston.md:12-13; binding.codex.md:20-21; houston.toml:6-7; profile.toml:5-6; card:17-34 | Pin (3 places per route — wrapper, binding, card) |
| "sandbox_mode ignored for Codex children" | binding.codex.md:48-50 — "sandbox_mode in the agent TOML is ignored for children (witnessed 2026-10-17, C-def.2)" | Vendor fact (runtime behavior; witnessed) |
| Delegation bans by role name (delta, trajectory, vector, atlas-*) | binding.claude.md:39 only | Doctrine (absent from Codex binding; vendor-delta in coverage, not a contradiction) |
| "one file serves both routes" | binding.claude.md:21 | Vendor fact (Claude single-file deploy) |
| "two wrappers" (child + main) | binding.codex.md:17-18 | Vendor fact (Codex child/main split) |
| Canary prefixes cl-/hc-/hp- | binding.claude.md:23; binding.codex.md:24 | Vendor fact |
| Oraculum PreToolUse[Bash] hook | oraculum.md:24-29 | Vendor fact (Claude-only; no germline-layer anchor) |
| Oraculum [features] block | oraculum.toml:49-54 | Vendor fact (Codex-only; no germline-layer anchor) |
| Oraculum authorized callers | oraculum.toml:3, :8-9 (Codex includes Houston); oraculum.md:9 (Claude excludes Houston) | ⚡ CONFLICT (vendor-specific, but cross-vendor drift since 286085d) |
| "Child cwd not guaranteed" | binding.codex.md:57-58 | Vendor fact (Codex docs gap; no Claude analogue) |
| Sources (Codex docs URLs) | binding.codex.md:85-87 | Doctrine (absent from Claude binding) |
| Role-TOML model drift noted | raw.card.model-effort.md:45-46 | Vendor fact documented in card only |
| "chatbot reads skills from reposoma" | germline/CHATBOT.md:9-11 | Vendor fact (chatbot channel; no binding) |


## F. Friction

### (i) A seat author adding a new vendor

1. **No criterion for germline identity** (ranked first because it gates everything): no file states when a seat requires a germline identity versus staying vendor-native. README :1-12, CHATBOT.md :1-30, both bindings, all agent frontmatter are silent. An author must infer from the single Houston precedent. (H3.)
2. **No binding template**: both Houston bindings were authored without a stated spec for what a binding must contain. An author constructing a new-vendor binding must reconstruct the required field set from examples.
3. **No scope boundary rule between wrapper, binding, and card**: wrapper = "vendor facts only" (binding.claude.md:5 scope line); binding = "mechanics only" (binding.codex.md:5). Where a new vendor fact lands (wrapper vs binding) is not written beyond those phrases.
4. **Active_pins requires witnessed probe + gavel** before a new pin can appear (card:15, :94-98). "The recalibration researcher" is unnamed. An author cannot add a pin unilaterally.
5. **Chatbot seam is guidance, not a binding spec**: CHATBOT.md carries no canary rule, no stamp rule, no entry proof, no return contract shape. A chatbot-vendor author cannot derive the same mechanics from CHATBOT.md that the other two bindings carry explicitly.

### (ii) An agent operating from the "other" vendor

1. **Oraculum Houston-caller CONFLICT** (ranked first): Claude oraculum.md:9 "not spawned by Houston"; Codex oraculum.toml:3 lists Houston. A Claude-side Oraculum would refuse a Houston-originated spawn that Codex allows. Changed in 286085d (Codex-only); Claude .md not updated. (H2, H8.)
2. **Delegation ban names absent from Codex binding**: delta, trajectory, vector, atlas-* are named only in binding.claude.md:39. A Codex-side Houston session operating from binding.codex.md:44 alone cannot derive the same named bans. (H1.)
3. **Oraculum hook exists on Claude only**: PreToolUse[Bash] whitelist (oraculum.md:25-29) has no equivalent in oraculum.toml. A Claude agent expecting whitelist enforcement on Bash calls finds no Codex analogue; Codex substitutes instruction-level constraints. (H6.)
4. **Entry proof completeness differs**: Codex proof includes effective cwd (binding.codex.md:79-81); Claude proof does not. A cross-vendor audit checking proof completeness sees different sets. (H1.)
5. **No cross-reference in either oraculum file**: neither oraculum.md nor oraculum.toml cites the other file or any shared source. A reader on one side has no discovery path to the other definition. (H2.)


## G. Uncertainty / not-read

1. **Git show commands not executed** — no Bash tool in this session. `git show --stat 286085d` and `git show 286085d -- codex/agents/oraculum.toml` were not run. H8's pre-commit diff is inferred from: commit message "broaden Oraculum authorized callers" (git log in session context), current oraculum.toml caller list, findings.g06.md:58 ("Delta edited source on GO (patch :3), commit 286085d changed codex/agents/oraculum.toml under Majkee's authorization"). The exact pre-commit caller list is not verified by direct diff.
2. **claude/agents/houston.md lines 22+** — brief limit was :1-21 (frontmatter only). The LOADER body in houston.md was not read. Inferred from codex/agents/houston.toml:1-9 which opens the same loader structure.
3. **codex/profiles/houston.config.toml lines 10+** — brief limit :1-9. Confirmed model/effort and loader-comment opening; full profile body not read.
4. **germline/CHATBOT.md lines 31+** — brief limit :1-30. Subsequent chatbot instructions (e.g., what to do with identity vs skill files, frontmatter handling) not read.
5. **astrobley.toml, implementer.toml, verifier.toml, harness_builder.toml** — not in brief scope; not read. Cross-vendor pattern for astrobley (present on both vendors) is unverified.
6. **germline/README.md lines 13+** — brief limit :1-12. Post-line-12 content (skills detail, deploy rules, etc.) not read.
7. **oraculum-bash-whitelist.sh** — referenced in oraculum.md:29; not in brief scope; content unknown.
8. **findings.g06.md sections other than "E4 vendor facts"** — read as supplementary context per note in §Guidance and §System passes; not formally in the E4-only scope but no finding from those sections was presented without attribution.
