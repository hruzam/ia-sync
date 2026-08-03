# Sella receipt — Codex-side (independent, not Wave-authored)

Date: 2026-08-03
Author: @Epoch
Purpose: primary-source capability receipt for the Codex/GPT line, produced independently
of Wave's claims, per Wave's research order steps 1-2, for the Sella cross-vendor
hypothesis (thin portable core + per-vendor machine profiles).

**Standing caveat: no Bash in this run.** I could not run `codex --version`, `codex exec`,
or any live session on this box. Everything below is either (a) DOCUMENTED from a live web
fetch/search this run, with source+date, or (b) explicitly marked
OPERATOR-PENDING/UNKNOWN. I did not fabricate any installed-version or live-behavior claim.

**Security note (resolved, not a live threat):** a local sub-agent pass on
`/home/hruzam/reposoma/raw.settings/*.md` and `/home/hruzam/reposoma/raw.research/**`
tripped a harness pattern-match flag for text resembling "settings-json,
bypass-permissions, permissions-allow-deny." A second, independent read (via a different
sub-agent, `field`) confirmed this is a **false positive**: the matched strings are
ordinary technical vocabulary describing Claude Code's real permission syntax (e.g.
`permissions.allow|deny` in `settings.json`, `permissionMode: bypassPermissions` in a YAML
frontmatter example), not an instruction directed at any agent. No injected/adversarial
text was found in either pass. Recorded here per the discipline of surfacing what I found,
including negative results.

---

## PART A — Codex/GPT-line documented capabilities (live-verified this run, 2026-08-03)

All items below were fetched live today from `learn.chatgpt.com` (the URLs Wave supplied
resolved without a redirect notice, except the skills page — see note). Treat "current
documentation" dates as the page's own claim; none of the fetched pages exposed a visible
last-updated timestamp, so CONFIDENCE is capped at M for anything not cross-confirmed by a
second source, per my own discipline (I do not upgrade a single-fetch claim to H).

### A1. AGENTS.md resolution
- Discovery chain: `~/.codex` (or `$CODEX_HOME`) global scope → git-root-to-cwd project
  scope, walking down. Per directory: checks `AGENTS.override.md` first, then `AGENTS.md`,
  then any names in `project_doc_fallback_filenames`. Uses at most one file per directory.
- Merge: concatenated root-to-leaf, blank-line joined; closer-to-cwd files come later and
  functionally override earlier guidance (text-concatenation "override," not a structured
  merge).
- Limit: `project_doc_max_bytes` (documented default 32 KiB combined). Stops adding once
  hit; skips empty files. Rebuilt fresh every run, no cache.
- SOURCE: https://learn.chatgpt.com/docs/agent-configuration/agents-md — accessed 2026-08-03.
- CONFIDENCE: M (single fetch, page date not visible).
- CONTRAST vs Claude Code: Claude Code does NOT natively discover `AGENTS.md` — it reads
  `CLAUDE.md` (project/user/local/managed tiers) and the common pattern is an explicit
  `@AGENTS.md` import line inside `CLAUDE.md` (confirmed via local doc
  `/home/hruzam/reposoma/raw.research/agent-docs/report/raw.agent-docs.2026-08-01.md:453-484`
  — [LOCAL]). This is the single most consequential asymmetry for Sella's "portable core"
  bet: Codex's core discovery primitive (walk-and-merge AGENTS.md) has NO native Claude-side
  counterpart; Claude's core primitive (CLAUDE.md as a *user message*, not system prompt —
  "guided not enforced") has no Codex-side counterpart in what I fetched. A portable "core"
  built as literal filename/merge-semantics parity will be lossy in both directions.

### A2. Subagents / custom agent config
- Custom agents: standalone TOML files, `~/.codex/agents/` (personal) or `.codex/agents/`
  (project-scoped). Required fields: `name`, `description`, `developer_instructions`.
  Optional: `model`, `model_reasoning_effort`, `sandbox_mode`, `mcp_servers`,
  `skills.config`.
- Built-ins: `default`, `worker` (execution-focused), `explorer` (read-heavy).
- Global `[agents]` config-file keys: `agents.enabled` (bool, default true),
  `agents.max_concurrent_threads_per_session`, `agents.default_subagent_model`,
  `agents.default_subagent_reasoning_effort`, `agents.interrupt_message` (bool, default
  true).
- Models named in the page: `gpt-5.6`, `gpt-5.6-terra`, `gpt-5.6-luna`. Reasoning effort
  enum: `ultra, max, xhigh, high, medium, low`.
- Subagents inherit the parent session's sandbox/permission mode unless overridden per
  agent file.
- SOURCE: https://learn.chatgpt.com/docs/codex/agent-configuration/subagents (redirected
  from the `agent-configuration/subagents` path supplied — note the path gained a `/codex/`
  segment) — accessed 2026-08-03.
- CONFIDENCE: M.
- CONTRAST vs Claude Code: structurally similar shape (per-project/per-user agent-definition
  files with frontmatter-like required fields, model/effort keys, tool/sandbox overrides) —
  this is the closest primitive-class match found in this whole pass. Materially different:
  Claude Code's frontmatter carries `tools`/`disallowedTools` allow-lists, `permissionMode`
  enum (`default/acceptEdits/auto/dontAsg/bypassPermissions/plan/manual` — 7 values, per
  [LOCAL] `raw.card.claude-code.md`), `isolation: worktree`, `background`, `maxTurns`; Codex's
  TOML surface (per this fetch) foregrounds `model_reasoning_effort` and `mcp_servers` +
  `skills.config` at the agent level, with sandbox_mode limited to (at least)
  `read-only`/`workspace-write` in the agent file. The precedence model also differs: Claude
  Code documents an explicit cross-scope precedence order (Managed > CLI > Project > User >
  Plugin) for agent definitions; the fetched Codex subagent page states no analogous
  cross-scope precedence for `~/.codex/agents/` vs `.codex/agents/` — UNKNOWN, not
  contradicted, just not stated in what I fetched.

### A3. Skills
- Structure: `SKILL.md` (required) + optional `scripts/`, `references/`, `assets/`, and an
  Codex/OpenAI-specific `agents/openai.yaml` (appearance/dependencies) not present in the
  Claude Code skill shape.
- Frontmatter: YAML, `name` + `description` required ("Explain exactly when this skill
  should and should not trigger").
- Progressive disclosure: initial skills list capped at "2% of context window or 8,000
  characters," whichever binds; full `SKILL.md` loads on selection.
- Invocation: explicit via `@` (ChatGPT surface) or `$` (Codex CLI/IDE); implicit via
  description-matching.
- Discovery scope levels: repository, user, admin, system — starting at `.agents/skills` in
  cwd, walking up to repo root.
- SOURCE: page resolved to `https://developers.openai.com/codex/build-skills` — note this is
  a DIFFERENT HOST (`developers.openai.com`, not `learn.chatgpt.com`) from the URL Wave
  supplied. Flagging explicitly: either the `learn.chatgpt.com` alias redirected silently, or
  the canonical docs have migrated hosts. Accessed 2026-08-03.
- CONFIDENCE: M.
- CONTRAST vs Claude Code: invocation trigger character differs (`$` vs Claude's slash-free
  auto-match plus explicit skill name); Claude Code's skill precedence is documented
  (Enterprise > Personal > Project > Plugin — a documented INVERSION relative to its own
  agent-definition precedence, per [LOCAL] Sella draft L6) — the fetched Codex page states a
  scope list (repo/user/admin/system) but not an explicit precedence ORDER between them.
  UNKNOWN whether Codex has the same inversion property Sella's L6 names as a Claude-specific
  design smell — this is a concrete follow-up question, not yet answered.

### A4. Hooks
- Events: `PreToolUse`, `PermissionRequest`, `PostToolUse`, `PreCompact`, `PostCompact`,
  `UserPromptSubmit`, `SubagentStop`, `Stop`, `SessionStart`, `SubagentStart`, `SessionEnd`.
- Config locations: `~/.codex/hooks.json`, `~/.codex/config.toml` (inline `[hooks]`),
  `<repo>/.codex/hooks.json`, `<repo>/.codex/config.toml`.
- Shape: event → matcher group → handler(s), JSON or TOML.
- I/O: stdin JSON (`session_id`, `cwd`, `hook_event_name`, `turn_id`, event data); stdout
  JSON or plain text; structured output supports `continue`, `stopReason`, `systemMessage`,
  `suppressOutput`.
- Exit codes: `0` success/continue; `2` blocking (message to stderr explains why); other
  codes → hook failure reported to user.
- SOURCE: https://learn.chatgpt.com/docs/hooks — accessed 2026-08-03. No page date visible.
- CONFIDENCE: M.
- CONTRAST vs Claude Code: event-name list is near-identical in spirit (Claude Code has
  `PreToolUse/PostToolUse/Stop/SessionStart/SubagentStart/PreCompact/UserPromptSubmit` per
  [LOCAL]) — this is the SECOND closest primitive-class match. Exit-2-blocks/exit-0-continues
  is IDENTICAL in both (per [LOCAL] Claude Code doc and this Codex fetch) — this is a
  genuinely convergent, not just coincidentally-named, cross-vendor micro-convention. Real
  asymmetry: Claude Code documents that only a SUBSET of events honor blocking exit 2 (e.g.
  `PostToolUse`/`SessionStart`/`SubagentStart` cannot block, per [LOCAL] receipt claim 3,
  itself flagged there as synthesized-not-spot-checked); the fetched Codex hooks page does
  not state any such per-event exception list — UNKNOWN whether Codex's exit-2 semantics are
  uniform across all 11 listed events or similarly partitioned. This is a genuine unresolved
  question on BOTH sides, not just Codex's.

### A5. Config precedence
- Locations: `~/.codex/config.toml` (user), `.codex/config.toml` (project, root-to-cwd,
  closest wins, trusted projects only), `/etc/codex/config.toml` (system, Unix), profile
  files `~/.codex/<profile>.config.toml`.
- Format: TOML throughout.
- Precedence (high to low): CLI flags/`--config` > project config (root-to-cwd, closest
  wins) > `--profile` selection > user config > system config > built-in defaults.
- Trust gate: untrusted projects skip ALL project-scoped `.codex/` layers (config, hooks,
  rules) — a documented all-or-nothing security cutout, not a partial-merge.
- Org override: `requirements.toml` can force settings (e.g. approval policy) regardless of
  user config.
- SOURCE: https://learn.chatgpt.com/docs/config-file/config-basic — accessed 2026-08-03. No
  page date visible.
- CONFIDENCE: M.
- CONTRAST vs Claude Code: BOTH systems document an explicit multi-tier precedence order
  with an untrusted/managed override concept (Claude: Managed/MDM overrides everything;
  Codex: `requirements.toml` on managed machines). Materially different: Claude Code's
  permission RULES documented as merging across scopes (additive), while Codex's project
  config is closest-wins REPLACEMENT semantics for a given key, and the untrusted-project
  behavior is a binary all-or-nothing skip rather than Claude's finer-grained "some things
  still load" posture ([LOCAL] doc does not describe an equivalent full-lockout for
  untrusted Claude Code projects — this itself is worth flagging as an open question rather
  than an assumed symmetry).

### A6. Non-interactive / headless mode
- Command: `codex exec "<prompt>"`.
- Flags fetched: `--ephemeral` (no rollout persistence), `--sandbox <read-only|
  workspace-write|danger-full-access>`, `--json` (JSONL stream), `--output-last-message
  <path>` / `-o`, `--output-schema <path>`, `--ignore-user-config`, `--ignore-rules`,
  `--skip-git-repo-check`.
- JSONL event types: `thread.started`, `turn.started`, `turn.completed`, `turn.failed`,
  `item.*` (agent messages, reasoning, command exec, file changes, MCP tool calls, web
  search, plan updates), `error`.
- Progress streams to stderr; final agent message to stdout (pipe-friendly). Stdin-piped
  prompt supported. `CODEX_API_KEY` env var for single-invocation auth. Resume via `codex
  exec resume [SESSION_ID]` / `--last`.
- Default requires a git repo unless `--skip-git-repo-check`.
- SOURCE: https://learn.chatgpt.com/docs/non-interactive-mode — accessed 2026-08-03. No page
  date visible.
- CONFIDENCE: M.
- CONTRAST vs Claude Code: this is the sharpest ASYMMETRY found. Claude Code's headless
  story per [LOCAL] centers on session continuation (`-c`/`--continue`/`--resume`) and a
  sync-only "Remote Control" layer (`claude remote-control`, outbound-HTTPS-only, OAuth-gated,
  disabled under several enterprise auth configs) — NOT a single-shot `exec`-with-JSONL-events
  primitive. Codex's `codex exec --json` is a purpose-built machine-consumption contract
  (typed event stream, schema-constrained output, exit-status semantics) with no [LOCAL]
  Claude Code equivalent documented in this pass. If Sella's portable core assumes a uniform
  "run headless, get structured events" primitive, Codex has one and (per what I have read
  locally) Claude Code's closest analogue is the Agent SDK / `claude -p` pattern, not
  something this receipt has confirmed at the same fidelity — flag as a genuine
  cross-vendor gap requiring a Claude-side re-check before Sella assumes symmetry here.

### A7. Import from Claude Code
- `/import` in Codex CLI or Desktop-app Settings > Import. Converts: instruction files →
  `AGENTS.md`; `settings.json` → `config.toml`; Skills → Skills; Plugins → Plugins; project
  folders → Projects; MCP config → Codex MCP settings; Hooks → Codex hooks; Subagents →
  Codex agents; last-30-days chats (cap 50) → recent chats; project memories → Memories.
- SOURCE: https://learn.chatgpt.com/docs/import — accessed 2026-08-03. No page date visible.
- CONFIDENCE: M.
- SIGNIFICANCE for Sella: this is OpenAI's OWN stated conversion table between the two
  vendors' primitive classes — effectively a vendor-authored first draft of exactly the
  mapping Sella is trying to define independently. Worth a direct comparison pass:
  Sella's L6/precedence-inversion findings and this table may agree or disagree on which
  primitives actually correspond 1:1 (e.g. does Claude Code "Hooks" really map cleanly onto
  Codex "Hooks," or is that a lossy label-level import rather than a semantic one? The import
  page doesn't say — UNKNOWN, worth a targeted follow-up).

### A8. Sandbox / permission modes (WebSearch corroboration, not single-page fetch)
- Three sandbox_mode values confirmed across two independent sources: `read-only`,
  `workspace-write`, `danger-full-access`. `[sandbox_workspace_write]` sub-table refines
  writable_roots/network_access.
- Approval policy is DOCUMENTED AS ORTHOGONAL to sandbox mode: `untrusted`, `on-request`,
  `never` — both independently changeable via `/permissions`.
- SOURCES: https://inventivehq.com/knowledge-base/openai/how-to-configure-sandbox-modes,
  https://deepwiki.com/openai/codex/2.4-sandbox-and-approval-policies,
  https://www.digitalapplied.com/blog/codex-cli-deep-dive-config-profiles-sandbox-2026 —
  searched 2026-08-03.
- CONFIDENCE: M (independent commentator sources, not the primary changelog; DeepWiki is a
  code-derived wiki, treat as M not H).
- CONTRAST vs Claude Code: same two-axis shape exists on the Claude side too
  (`permissionMode` enum bundles what Codex splits into sandbox_mode + approval policy —
  Claude's `bypassPermissions`/`plan`/`acceptEdits` collapse both axes into one enum value
  per mode). This is a genuine ASYMMETRY in factoring, not just naming: Codex treats
  "what's technically permitted" and "when it asks first" as two independent settings;
  Claude Code bundles them into one mode selector. A portable-core abstraction that assumes
  a single two-value axis will not round-trip cleanly onto Claude Code's single-enum model.

### A9. `codex mcp-server` / MCP CLI
- `codex mcp add|list|get|remove|login|logout <name>` — manages `~/.codex/config.toml` MCP
  entries + OAuth creds.
- `codex mcp-server` (distinct subcommand): exposes Codex's OWN capabilities as an MCP
  server so other tools can drive Codex.
- Server entry needs name + (command/args/env for stdio) or (url/bearer_token_env_var for
  Streamable HTTP).
- SOURCES: https://deepwiki.com/openai/codex/6.3-mcp-cli-commands,
  https://learn.chatgpt.com/docs/extend/mcp — searched 2026-08-03.
- CONFIDENCE: M.
- CONTRAST vs Claude Code: Claude Code's MCP config lives in `.mcp.json`/`~/.claude.json`
  with 4 transports (`http`/`sse`(deprecated)/`stdio`/`ws`) per [LOCAL]; Codex's fetched
  surface names 2 transport shapes (stdio, Streamable HTTP) — fewer transport options
  documented for Codex in what I found, though absence-of-mention is not proof of absence
  (mark this specific point L confidence, inferential).
- Notably, `codex mcp-server` (Codex-as-a-server) has no [LOCAL]-documented Claude Code
  equivalent found in this pass — worth a targeted check: does Claude Code expose itself as
  an MCP server to other agents? UNKNOWN from this pass' local docs.

---

## PART B — Codex CLI version/release context (background only, NOT an installed-version claim)

- Latest tagged GitHub release found: **0.146.0** (2026-07-29) — session naming/pinning,
  WebSocket remote Code Mode, proxy/MCP-auth fixes. Pre-release tags `0.147.0-alpha.1` and
  `0.147.0-alpha.4` also visible (2026-07-29 and 2026-07-31).
  SOURCE: https://github.com/openai/codex/releases — fetched 2026-08-03. CONFIDENCE: H
  (primary GitHub releases page, direct fetch).
- Model deprecation note: `gpt-5.4`/`gpt-5.4-mini` scheduled to leave Codex-via-ChatGPT-login
  on 2026-08-31; recommended replacements `gpt-5.6-terra`/`gpt-5.6-luna` — consistent with the
  model names (`gpt-5.6`, `gpt-5.6-terra`, `gpt-5.6-luna`) seen in the subagents doc (A2).
  SOURCE: web search aggregating developers.openai.com/codex/changelog content — searched
  2026-08-03. CONFIDENCE: M (search-engine synthesis of a changelog page, not a direct fetch
  of that page in this run — recommend a direct fetch of
  `https://developers.openai.com/codex/changelog` before treating this as settled).
- **This is background context only.** It does NOT establish which version is installed on
  any operator machine. That remains OPERATOR-PENDING (see below).

---

## UNKNOWNS / OPERATOR-PENDING (explicit, per Wave's step-1 ask)

1. **Installed Codex CLI version on this box / any operator machine** — OPERATOR-PENDING.
   No Bash tool in this run; cannot execute `codex --version`.
2. **Live discovery behavior** (does AGENTS.md walk-and-merge actually behave as documented
   when run against a real nested repo; does `project_doc_max_bytes` truncation actually
   fire) — OPERATOR-PENDING, requires a live session.
3. **Cross-scope precedence for `~/.codex/agents/` vs `.codex/agents/`** — not stated in the
   fetched subagents page. UNKNOWN, not contradicted.
4. **Per-event exit-2 blocking exceptions for Codex hooks** (does `SessionEnd` or
   `PostToolUse`-equivalent actually ignore exit 2 the way Claude Code's does) — not stated
   in the fetched hooks page. UNKNOWN.
5. **Whether Codex exposes itself as an MCP server callable BY Claude Code**, and whether
   Claude Code has any headless-JSONL primitive matching `codex exec --json`'s fidelity —
   both UNKNOWN from local docs read this run; flagged as the sharpest open comparison
   question for a follow-up receipt.
6. **Skill precedence order** across Codex's repo/user/admin/system scopes — page states
   scope levels, not an explicit override order. UNKNOWN.
7. **MCP transport completeness for Codex** (stdio + Streamable HTTP confirmed; SSE/WS
   status unconfirmed either way) — L-confidence inference only.
8. Direct fetch of `developers.openai.com/codex/changelog` itself was NOT performed this
   run (only search-engine synthesis of it) — recommend as first follow-up if version
   precision matters.

---

## PART C — the vocabulary question (does a ≥30-command fixed vocabulary survive cross-vendor?)

**Verdict: no positive evidence found; the evidence found points the other way.**

- Searched directly for a CodeIgniter-style fixed ≥30-operation vocabulary succeeding as a
  cross-vendor AI-agent convention. The only concrete "30+" hit was
  `github.com/yasserstudio/codeigniter-skills` — but that is a **framework-specific SKILL**
  (CI3/CI4 API patterns) consumed identically by multiple agent vendors (Claude, Cursor,
  Codex, Copilot per its own description) — i.e., the vocabulary is CodeIgniter's PHP API,
  not an agent-harness vocabulary. It is evidence that large fixed vocabularies (the
  underlying framework's own API) CAN be shared cross-vendor when delivered as a skill/doc
  payload — but that is the framework's vocabulary riding on top of the agent harness, not a
  vocabulary OF the harness layer itself. This does not support the harness-level claim
  Wave/majkee is testing. SOURCE: https://github.com/yasserstudio/codeigniter-skills —
  searched 2026-08-03. CONFIDENCE: M.
- Every surviving cross-vendor convention actually found in this pass is SMALL, not large:
  - A single filename (`AGENTS.md`) — now stewarded by the Agentic AI Foundation / Linux
    Foundation, reportedly adopted by 60,000+ repos and 20+ tools as of mid-2026. SOURCE:
    https://codersera.com/blog/agents-md-complete-guide-2026/ and
    https://www.morphllm.com/agents-md-guide — searched 2026-08-03. CONFIDENCE: M
    (independent commentator aggregation, not the AAIF's own site — recommend fetching the
    spec's own governance page directly as a follow-up for H confidence).
  - Exit-code semantics for hooks (0 = continue, 2 = block) — CONFIRMED IDENTICAL between
    Claude Code ([LOCAL]) and Codex (A4, this run) — a two-value convention, about as small
    as a vocabulary gets.
  - stdio/stdin-JSON, stdout-JSON-or-text shape for hooks — same pattern on both sides.
  - The AAIF's own effectiveness data (per search synthesis) is notably modest: a cited 2026
    study of Codex on 124 PRs found AGENTS.md presence correlated with lower runtime/token
    cost but did NOT improve task-completion rate — i.e., even the ONE surviving large-scale
    cross-vendor convention (a single file, not a command vocabulary) has measured, modest,
    efficiency-only effect, not a capability effect. SOURCE: search synthesis citing a study,
    via https://www.webfuse.com/blog/agentic-coding-in-2026 and related — searched
    2026-08-03. CONFIDENCE: L (I have not located and read the primary study itself, only a
    secondary description of it — flag explicitly as needing primary-source verification
    before use as a load-bearing claim).
- **Negative result, explicit:** I found no case study, spec proposal, or vendor
  announcement describing a ≥30-item FIXED command/function vocabulary (framework-API
  style) that multiple agent-harness vendors implemented identically at the harness layer.
  Everything resembling "many commands" in the search results was either (a) a
  framework-specific API riding as a skill payload (CodeIgniter case above), or (b) generic
  "primitives" discourse (tool-calling, MCP tool schemas) which is itself vendor-defined per
  tool, not a shared fixed vocabulary across vendors.
- **This corroborates the smaller Sella hypothesis, not the larger one:** surviving
  cross-vendor conventions in this ecosystem stay tiny — a filename, an exit-code pair, a
  transport shape — and even those show measured-modest effect sizes. A 30+-command shared
  vocabulary at the harness/primitive layer has no positive precedent found this run. This
  is an argument FOR Sella's thin-core-plus-per-vendor-profile shape and AGAINST attempting
  a large shared operation vocabulary as the portable core.

---

## Sections to refresh
- Direct fetch of `developers.openai.com/codex/changelog` (not yet fetched directly this
  run — only search-synthesized).
- AAIF/Agentic AI Foundation's own governance page for AGENTS.md (to upgrade adoption-number
  claim from M to H).
- The 124-PR AGENTS.md effectiveness study — locate and read primary source before citing
  further.
- Live-session re-check of AGENTS.md walk-and-merge and hook per-event blocking exceptions
  (both sides) once Bash/live access is available.
- Whether Claude Code exposes an MCP-server-of-itself primitive comparable to `codex
  mcp-server` — targeted follow-up.
- Cross-check candidate: this receipt's Part A findings vs Wave's original claims — route
  through `mirror` (position-aware, since I now have a lean: "closest matches are
  agents+hooks; sharpest gap is headless/exec fidelity and sandbox-axis factoring") if Wave's
  synthesis needs adversarial audit before Sella's next draft locks.
