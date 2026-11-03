# BRIEF U8 → field (Flight, 2026-10-21) — the vendor seam: what is vendor-native, what is germline-bound, and the missing criterion
Audit-only. Read in full; no edits outside your return file; no verdicts, no dispatch, no web.

## Read in full (absolute paths)
1. /home/hruzam/ia-sync/germline/agents/houston/binding.claude.md and binding.codex.md (whole — the two existing vendor seams)
2. /home/hruzam/ia-sync/claude/agents/oraculum.md (whole) and /home/hruzam/ia-sync/codex/agents/oraculum.toml (whole) — the cross-vendor seat with NO germline identity (defined twice, independently)
3. /home/hruzam/ia-sync/codex/agents/{architect,challenger,researcher}.toml (whole — the three portable role TOMLs with the inert `sandbox_mode = "read-only"` key per G01)
4. /home/hruzam/ia-sync/codex/AGENTS.md (whole — deployed to ~/.codex/AGENTS.md; the Codex user-guidance channel)
5. /home/hruzam/reposoma/raw.settings/raw.card.model-effort.md (whole — `active_pins`; the model/effort mirror both bindings cite)
6. /home/hruzam/ia-sync/claude/agents/houston.md :1–21 (frontmatter: model/effort/tools) and codex/agents/houston.toml :1–9 + codex/profiles/houston.config.toml :1–9 (keys only)
7. /home/hruzam/ia-sync/germline/README.md :1–12 (what germline claims to hold per vendor) and CHATBOT.md :1–30 (the third "vendor": chatbots)
8. /home/hruzam/ia-sync/.dev/session/germline-06-full-audit/findings.g06.md — "E4 vendor facts" section only (checked platform facts; reuse)
9. git: run `git -C /home/hruzam/ia-sync show --stat 286085d` and `git -C /home/hruzam/ia-sync show 286085d -- codex/agents/oraculum.toml` (read-only) — the one authorized vendor-config change on record (2026-10-20)
10. Glob `/home/hruzam/ia-sync/claude/agents/*.md` and `/home/hruzam/ia-sync/codex/agents/*.toml` — list names only (which seats exist on each vendor; which exist on both; which on one).

## Facts to rely on (Flight-verified)
Houston is the only germline-bound seat (identity + binding.<vendor> + cards; thin wrappers on both vendors). Oraculum is vendor-native on both vendors with no germline identity (baseline S-finding: "independently defined with different callers"). `sandbox_mode` is inert for spawned Codex children (G01 C-def.2); model/effort keys apply. Codex `developer_instructions` outrank the AGENTS.md channel (feedback §3.3). The Claude API tool-name regex forbids dots; MCP allows them (Epoch). D1 accepted: each participating agent declares how its runtime consumes its sources (generated vendor files / runtime reading / a described combination); role names do not select the mechanism.

## One question
What exactly does each vendor seam carry today (keys, pins, tools, sandbox/approval, hooks, route/canary, entry proof extras, delegation bans, placement rules), what is duplicated or diverged between the two Houston bindings and between the two Oraculum definitions, where vendor facts live (binding vs card vs Sella vs TOML comments), and what written criterion — if any — says which seats get a germline identity and which stay vendor-native. As the files literally state it.

## Hypotheses to TEST
H1 Binding parity: list every rule present in binding.claude.md and check its twin in binding.codex.md (and vice versa) — same / vendor-delta / missing. Include: delegation ban roster (:39 claude only), "effective cwd", `sandbox_mode` note, placement, "one wrapper serves both routes" vs two wrappers, §Sources.
H2 Oraculum coherence: compare claude/agents/oraculum.md and codex/agents/oraculum.toml field by field — identity prose, callers/authorized spawners, model/effort pins, tools/sandbox, hooks (the Claude `PreToolUse[Bash]` hook per G01 §3.8 — is it in the .md? any Codex analogue?), description. List divergences; note which are vendor-necessary and which are drift. Does either file cite the other or any shared source?
H3 Criterion: does ANY file state why Houston has a germline identity and Oraculum does not (README :1–12, CHATBOT, bindings, the agents' own frontmatter)? Quote or report absence. Does D1's "each agent declares how its runtime consumes its sources" have ANY existing instance besides Houston's wrapper line "This file is a thin loader"? (grep "loader|germline|derived from|source:" across claude/agents/*.md and codex/agents/*.toml — list hits.)
H4 Pins: raw.card.model-effort.md `active_pins` vs the actual wrapper/TOML values for houston, oraculum, and the three role TOMLs — match / mismatch per seat (quote both). Who updates the card when a pin changes (any rule)?
H5 Inert keys: the three role TOMLs still carry `sandbox_mode = "read-only"` (G01 open item, Majkee "leave for now") — quote; does any comment in them say it is inert? Any other key in the TOMLs that G01/E4 showed to be ignored or required (`name`, `description`, `developer_instructions` required per E4)?
H6 Hooks as a vendor seam: the Claude Oraculum hook (`PreToolUse[Bash]`, agent_id exemption) — where is it configured (agent .md frontmatter? settings?) and is there any germline-level or binding-level statement about hooks for ANY seat? For Codex, what replaces it (sandbox/approval policy)? Report what the files say; do not infer behaviour.
H7 Third vendor (chatbots): CHATBOT.md :1–30 — what a chatbot is told to read (skills; identity when assigned) and whether any seam document exists for it (no binding.chatbot.md?). Report absence.
H8 Commit 286085d: what changed in codex/agents/oraculum.toml (authorized callers broadened) — does the Claude oraculum.md carry the same caller list? (cross-vendor drift test on a real, dated change.)

## Return shape (write yourself, verbatim; then ≤15-line inline summary)
Return file: /home/hruzam/ia-sync/.dev/session/germline-06-full-audit/_bus/field.U8.return.md — header `from: field · unit U8 · date`, then:
A. Seat inventory (name · claude file · codex file · germline identity? · pins · route/canary · hook/sandbox keys).
B. Binding parity table (H1).
C. Oraculum divergence table (H2, H8).
D. H3–H7 evidence tables (quote text with every line ref; line numbers as read today).
E. Where vendor facts live (fact · file:line · is it a vendor fact, a doctrine, or a pin).
F. Friction for (i) a seat author adding a vendor, (ii) an agent on the "other" vendor (ranked, cited).
G. Uncertainty / not-read.
Bounds: ≤ 4,000 words. Separate authored / deployed / historical / proposed. Stop when A–G are filled.
