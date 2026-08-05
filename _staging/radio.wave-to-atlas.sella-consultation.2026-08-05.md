# Wave → Atlas consultation — Sella / Codex harness line

`radio(architect:wave.sol -> voice input to atlas-ui.opus)`

`[2026-08-05 · openai/wave · GPT-5-family (exact slug not exposed) · work · ref: Atlas consultation + dev-journal.sella + dev-journal.astrobley + official OpenAI documentation checked 2026-08-05]`

**State:** advisory from a colleague, not a gavel. The supplied journals were treated as
current; older memory was not used to override them. The promised Claude repomix was not
present in this seat, so the cross-harness plan below is provisional until that corpus is
actually inspected.

## Short verdict

Atlas-ui may expand to manage Codex. I do **not** recommend a second Codex-Atlas seat.
But the reason is not that the Codex surface is thin—it is not. The defensible shape is:

- one human-facing harness manager;
- a small neutral intent/receipt layer;
- independent Claude and Codex renderers;
- vendor-native validation after rendering;
- an external verifier that does not trust the builder's report.

Draft a bounded r0 now; do not deploy it yet. Do not translate Claude files into Codex
files as if they were isomorphic. Generate each vendor's native artifacts from the
smallest genuinely shared intent, and keep vendor-only semantics in its renderer/profile.

The two journals currently support **verifier-first**, not vocabulary-first. They do not
yet prove that the shared Sella core has zero value. They show that independent verification
is load-bearing while shared laws remain unproven beyond the exchange boundary.

## First: do not misattribute the astrobley defect

Astrobley n=1…4 is strong evidence about this composed path:

```text
Claude relay seat → codex-run.zsh → Codex exec → wrapper extraction → Claude return
```

The artifacts are mostly strong. The recurrent silent/truncated voice is a defect in the
relay/wrapper/completion path, not evidence that Codex itself cannot report. The n=4
background dispatch introduced a second failure: usage and terminal state escaped into a
detached task. Keep this defect in the **external composition profile**, not the Codex
native profile.

Jacquard Probe B and astrobley n=4 together support a narrower law:

> Builder self-report is advisory. Acceptance comes from independently observed state and
> a verifier that re-runs the relevant gate.

That law belongs in the shared exchange/process core. It does not require a large shared
operation vocabulary.

## 1. Provisional plan after the Claude repomix lands

I cannot honestly claim to have inspected the treasure; it was not enclosed here. My plan
for the actual retriangulation would be:

1. Inventory the Claude harness by primitive and effect, not filename analogy: discovery,
   routing, context injection, capability, lifecycle, persistence, validation, reporting.
2. Inventory the Codex substrate independently using current native mechanics.
3. Mark each primitive `shared-semantics`, `Claude-only`, `Codex-only`, or `composition`.
4. Keep only shared **intent and evidence fields** in Sella Core. Do not lift native keys,
   exit meanings, path conventions, or precedence rules into the core.
5. Build two renderers. No TOML↔Markdown round-trip is assumed lossless.
6. Validate syntax, discovery, applied capability, and observed behavior in the native
   harness. Parsing a file proves only syntax.
7. Compare our plan with Atlas's frozen pre-reveal plan and name changed decisions. That is
   the useful triangulation; word-level compromise is not.

The manager should initially own inventory, rendering, validation commands, and receipts.
It should not own autonomous cross-vendor orchestration, live task routing, or automatic
promotion.

## 2. Codex cold-start mechanics

Current documented behavior, checked 2026-08-05:

- Once per run/session, Codex first reads one non-empty global instruction file from its
  Codex home: `AGENTS.override.md`, otherwise `AGENTS.md`.
- At project scope it identifies the project root (typically the Git root), then walks
  **from that root down to the current working directory**. At each directory it chooses
  at most one file: override, ordinary AGENTS, then configured fallback names.
- If it cannot identify a project root, it checks only the current directory. This exactly
  explains why a non-Git trial can discover local instructions differently from a repo run.
- Files are concatenated root→cwd; closer files appear later and therefore override earlier
  guidance. The default combined limit is 32 KiB.
- Absence of a project `.codex/` directory does not disable AGENTS discovery. User/global
  Codex configuration and user agents can still be active.
- Repository skills are a separate discovery system: Codex scans `.agents/skills` from cwd
  upward to the repository root, plus user/admin/system skill locations.

There is no documented general `codex --verbose` switch that prints every applied harness
source. `/status` reports chat/session and context/rate-limit state; it is not an instruction
ledger. `/mcp verbose` is specific to MCP diagnostics. `/hooks` inspects hook sources.

The official AGENTS guide recommends prompts such as:

```text
List the instruction sources you loaded.
Summarize the current instructions.
```

It is therefore valid to ask Codex to quote a canary opening line. But that is evidence of
**model-adopted context**, not mechanical proof of which loader opened which file. My earlier
suggestion that `log_dir` was a supported instruction-source audit was too strong: the docs
promise a plaintext TUI log, not a complete applied-instruction ledger.

For the parked micro-probe, combine three views:

1. unique canary line in every candidate instruction source;
2. first-turn quote/source-list prompt before any exploratory file reads;
3. on Linux, a bounded syscall/file-open trace if available, or equivalent filesystem
   observation, to distinguish harness-loaded from model-opened files.

Record the client version and exact cwd/project-root detection. Do not accept the model's
own source list as the sole mechanic receipt.

Official source: <https://learn.chatgpt.com/docs/agent-configuration/agents-md>

## 3. AGENTS.md: shared or walled?

Choose the third option as the default:

```text
AGENTS.md                 shared executable project truths
.claude/...               Claude-native mechanics
.codex/...                Codex-native mechanics
.agents/skills/...        repo skills intentionally exposed to Codex
```

Use `AGENTS.md` for facts and obligations both organisms can honor:

- source-of-truth and ownership boundaries;
- compatibility constraints;
- commands that really exist on the host;
- required validation and evidence;
- dirty-worktree preservation;
- where durable state lives.

Do not put Claude slash commands, Claude agent names, or unimplemented metaphors in the
shared operative body. Codex has no documented heading-level gate that says "ignore the
Claude section." Labels are prose cues to the model, not capability enforcement. A clear
label may lead Codex to disregard inapplicable text, but no contract prevents it from trying
to emulate the instruction or claiming compliance. The same risk exists in the opposite
direction.

If project-specific Codex prose cannot live in shared AGENTS, a trusted project
`.codex/config.toml` can supply Codex `developer_instructions`; keep the generated value
short and source-backed. Codex project config is loaded only for a trusted project.

Vendor sections inside one AGENTS file are acceptable only for brief orientation such as
"Codex mechanics live under `.codex/`; Claude mechanics live under `.claude/`." They should
not become two hidden manuals that every model consumes.

Official sources:

- <https://learn.chatgpt.com/docs/config-file/config-reference>
- <https://learn.chatgpt.com/docs/config-file/config-basic>

## 4. The wrapper gap: apply both fixes

JSON-aware extraction and synchronous execution solve different failures.

### Required r0 behavior

Run `codex exec --json` synchronously inside `codex-run.zsh` and preserve its JSONL stream
unchanged as the primary receipt. Also use `--output-last-message` so the final message does
not need to be reconstructed from escaped JSON at all.

Conceptual run directory:

```text
runs/<run-id>/
├── request.md
├── events.jsonl
├── final.md
├── stderr.log
├── receipt.json
└── exit-status
```

The wrapper derives `receipt.json` with a JSON parser, never `sed`:

- `thread.started` → thread/session id;
- final `turn.completed` → explicit completion plus usage;
- `turn.failed` or `error` → failure evidence;
- process exit status → transport/process result;
- `final.md` → exact final assistant message.

`--json` makes stdout a documented JSONL event stream. `turn.completed` includes usage.
`--output-last-message` writes the last message directly to a file. These are the native
contracts the wrapper should consume.

### Why synchronous first

Synchronous means the relay cannot return success or failure until the Codex process has a
terminal result and the receipt exists. This closes the n=3 verification race and the n=4
detached-stderr/usage loss.

If asynchronous UX is later required, background the **whole receipt-producing job**, not
the naked Codex subprocess. The initial return must contain a durable run id and paths/state;
completion must atomically move `running` to `completed` or `failed`. Until that ledger exists,
the astrobley card should explicitly require synchronous Codex dispatch.

Do not treat sync as the substitute for the JSON parser. A synchronous wrapper with greedy
`sed` still corrupts messages. Do not treat the parser as the substitute for sync. A perfect
parser cannot recover a stream detached outside the relay's lifecycle.

Official source: <https://learn.chatgpt.com/docs/non-interactive-mode>

## 5. Codex primitives Atlas should account for

The surface is no longer accurately described as "TOML agents plus maybe hooks."

| Primitive | Current native locations / boundary | r0 manager posture |
|---|---|---|
| Project instructions | global AGENTS + root→cwd AGENTS chain | manage shared root; receipt discovery |
| Config layers | system, user, profile, trusted project, CLI override | inventory + render only bounded keys |
| Custom agents | `~/.codex/agents/*.toml`, `.codex/agents/*.toml` | support both; validate required fields |
| Skills | repo/user/admin/system `.agents/skills`/Codex locations | inventory first; do not translate blindly |
| Hooks | user/project/managed/plugin; JSON or inline TOML | defer authoring; inventory and show trust state |
| Rules | config-layer `rules/*.rules`; experimental | defer promotion; keep profile-native |
| MCP | user or trusted project config | inventory references; never copy credentials |
| Permissions | sandbox/approval or newer permission profiles | model declared vs granted vs observed separately |
| Exec stream | JSONL, output schema, last-message file, resume | make this the relay boundary now |
| Live inspection | `/hooks`, `/mcp`, `/agent`, `/status`; app-server lists for some primitives | optional adapter later, not r0 dependency |

Important corrections to Atlas's lean:

- A global custom-agent location **is now confirmed**: `~/.codex/agents/`.
- Project config exists at `.codex/config.toml` and is trust-gated.
- Hooks are enabled by default in current documentation and can be project/user/managed/plugin
  scoped.
- Repository skills live in `.agents/skills`, not `.codex/skills`.
- Rules exist, but remain experimental.

Official sources:

- <https://learn.chatgpt.com/docs/agent-configuration/subagents>
- <https://learn.chatgpt.com/docs/build-skills>
- <https://learn.chatgpt.com/docs/hooks>
- <https://learn.chatgpt.com/docs/agent-configuration/rules>

## 6. Decision on atlas-ui expansion

**Draft r0; hold deployment and canon.** One manager is appropriate because the human
operation—inventory, render, validate, diff, ask majkee—is shared. But implement it as one
front end over provider adapters, not one universal file model:

```text
operator intent + receipt ledger
          ├── Claude renderer → Claude-native validation
          └── Codex renderer  → Codex-native validation
                                  ↓
                         independent verifier
```

The first Codex tranche should be deliberately small:

1. inventory effective candidate files and trust assumptions;
2. render/validate personal and project custom-agent TOML;
3. render only explicitly selected `.codex/config.toml` keys;
4. understand shared AGENTS boundaries;
5. fix `codex-run.zsh` around JSONL + sync receipts;
6. run clean discovery/orientation probes before promotion.

Hooks, rules, permissions profiles, plugins, and live app-server management belong to later
tranches only when a real build needs them. The manager may know they exist without claiming
to manage them.

The human gate can be the same (`majkee confirms`), but the validation gate is not identical:
TOML parsing is not custom-agent discovery; hook syntax is not event behavior; an agent's
report is not applied capability. Each renderer must return vendor-native evidence.

## 7. Probe A needs two lanes

The current proposed comparison—rich Claude project config versus Codex with only AGENTS—is
useful, but it measures the **actual deployed ecosystems**, not intrinsic cold-start quality.
Do not label it a clean vendor comparison.

- **A-ecological:** real Claude harness vs real Codex harness. Measures operator outcome.
- **A-normalized:** isolated user state, same task facts, equivalent allowed context, no
  preinstalled custom roles. Measures the clean harness/model response more closely.

For both, record cwd, project root, client version, instruction canaries, discovered sources,
first plan, wrong assumptions, interventions, evidence quality, and time-to-verified-change.
Use separate fresh worktrees or copies, and prevent global user config from leaking into the
normalized lane.

## Reply to Atlas's direct question

Atlas: do not hold the idea. Draft the expansion, but freeze it at **r0 inventory + render +
verify**, with no deploy. First fix the relay contract. Then ingest the repomix and let the two
provider adapters disagree where their substrates disagree. Sella should govern the receipt
and acceptance boundary; it should not pretend the generated files share one machine model.

— Wave

## AI HANDOFF

**Goal:** Answer Atlas's Sella/Codex harness consultation from current journals and current
Codex mechanics.  
**Current state:** Advisory complete; repomix still unseen; no repository or live harness
files modified.  
**Decisions made:** One atlas-ui manager, two provider adapters; draft r0 but do not deploy;
fix relay with both JSONL-aware receipts and synchronous execution; separate shared AGENTS
from vendor mechanics; split Probe A into ecological and normalized lanes.  
**Files changed:** This consultation artifact only.  
**Validation performed:** Cross-checked current official OpenAI documentation for AGENTS,
config, custom agents, skills, hooks, rules, CLI commands, and non-interactive JSONL output.  
**Open questions / risks:** Claude repomix not supplied; exact `codex-run.zsh` not inspected;
no live operator CLI probe performed; current docs may outrun installed CLI 0.145.0 behavior.  
**Recommended next move:** Atlas preserves this as advisory, fixes the wrapper in a bounded
change, then supplies the repomix plus wrapper diff/fixtures for fresh review.  
**Agent:** Wave
