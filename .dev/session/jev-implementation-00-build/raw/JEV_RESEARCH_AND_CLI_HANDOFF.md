---
title: "Jev — research and CLI implementer handoff"
date: 2026-09-24
prepared_for: majkee
prepared_by: asymmetry
implementers: [Codex CLI, Claude Code]
status: "Research checked; offline smoke checks passed; not installed or live-tested"
recommended_scope: "Isolated, advisory-only experiment with a shared Unix adapter"
authority: "majkee; existing host and agent permissions remain authoritative"
companion: jev_smoke.py
---

# Jev: what to install, what to build, and how to operate it

## 1. The actual target

The screenshot says **Jev**, a TypeSafe model, rather than “GEV.” Three different things must remain separate:

| Component | What it supplies | What it does not supply |
|---|---|---|
| Jev hosted service | Typed decisions over supplied text/state | A conversational coding model or local coding agent |
| Official TypeSafe agent skill and SDKs | Integration knowledge and API clients | Automatic control of every Claude/Codex turn |
| A Jev-based harness | Application code that consumes decisions | A universally interchangeable plugin for every native runtime |

TypeSafe explicitly distinguishes Jev from a replacement for a coding LLM. A coding agent can build an application that calls it; changing the agent's model setting to Jev is not the integration. [S1]

The Google Drive link in the screenshot resolves to an **independently compiled study synthesis**, titled “Jev Engineering for Coding Agents.” Its front matter says it is not affiliated with or endorsed by TypeSafe. Treat its architecture as a proposal, not installation authority. The currently linked document is not necessarily the same edition pictured in the preview. [S15]

**Recommendation:** retain the existing coding agents and add one bounded decision service callable from either. Do not begin by replacing their runtime, adding MCP, or installing an unreviewed permission gate.

## 2. Verified availability and economics

Checked against first-party documentation on **2026-09-24**. Recheck on the target host before implementation.

| Item | Verified value |
|---|---|
| API | `POST https://api.typesafe.ai/v1/systemone` |
| Authentication | Bearer token; environment variable `TYPESAFE_API_KEY` |
| Account/key management | `https://console.typesafe.ai` |
| Current model | `jev-1.13.0` |
| Moving aliases | `jev-latest`, `jev-preview`; currently both resolve to that version |
| Published pricing | $0.042 per million input tokens; output tokens free |
| Request limits | 64k total tokens; also 32k for state plus the longest question |
| Input | Text, including structured JSON; not direct images/audio/video |
| Python SDK | `typesafe-sdk`, Python 3.10+ |
| JavaScript/TypeScript SDK | `@typesafe-ai/sdk` |

Sources: endpoint [S3], credentials [S4], model/pricing/limits [S5], SDKs [S6–S7]. I found a hosted API, **not a verified local-weights/Ollama installation**. A local adapter still sends its approved input to that service.

The launch article reports approximately **193.6× faster and 444.6× cheaper** on selected decision workflows. It also identifies these as high-end gains, describes vendor-designed evaluations, and notes that its LLM comparison asks for probability-producing outputs. These are not measured speedups for an entire coding session on this computer. [S8]

Our experiment must measure **cost and elapsed time per successful task**. Adding a cheap classifier without removing expensive work can make the workflow slower. Model handoffs must include context loading, cache effects, returned evidence, retries and orchestration overhead. Keep subscription consumption and separately billed API usage distinct; do not convert saved tokens into invented cash savings.

## 3. Installation plan

### Stage 0 — inspect the actual execution host

Run a read-only inventory before changing anything. Prefer the host where the CLI actually executes; a phone/tablet connected over SSH is only an interface.

```bash
pwd
hostname
uname -srmo
python3 --version
command -v git python3 uv node npm npx claude codex timeout
# Run only for tools that exist:
claude --version
codex --version
# Run only inside the intended repository:
git status --short --branch
```

Report the working directory, OS, tool versions, existing skill/hook locations, permission mode, proposed experiment directory, and whether approved outbound HTTPS is possible. Inspect only relevant configuration fields: never dump environment variables, auth files, session transcripts or complete settings containing credentials.

Do not repair an unrelated environment, upgrade the system or CLIs, reset/stash a dirty worktree, install globally, or widen a sandbox as a side effect of this investigation. Existing uncommitted work belongs to the user.

### Stage 1 — choose one skill-installation path

The official TypeSafe instructions provide the following paths. The skill helps the implementer use the API; it does not itself create the decision adapter. [S2]

**Shared/project-oriented route:**

```bash
npx skills add typesafe-ai/skills --skill typesafe-ai
```

Run from the selected project and choose the intended agent targets. The documented skills-installer default is project-local; do not add `-g` accidentally. Before running, inspect the official skill repository and the installer/package being executed. Record resolved versions and installed destinations. An official skill repository and a third-party installer are separate supply-chain dependencies.

**Alternative Claude Code plugin route:**

```bash
claude plugin marketplace add typesafe-ai/skills
claude plugin install typesafe@typesafe-ai
```

Inspect `claude plugin install --help` and the installed version's scope behavior first. Do not assume the plugin command shares the project-local default of the other installer. Do not run both methods for the same agent. Restart/reload only when required and agreed; do not terminate a valuable live session just to discover whether reload was needed.

**Manual alternative:** install the complete official `skills/typesafe-ai` directory, including its referenced files, in the installed agent's documented skill location. Do not copy only `SKILL.md` while leaving broken references. Keep the canonical shared content separate from thin vendor-specific loaders.

For a Claude plugin installation the documented invocation is `/typesafe:typesafe-ai`; otherwise ask the agent to use the TypeSafe skill. Its live documentation references must still be checked against the installed API/client version. [S2]

### Stage 2 — perform the isolated smoke test

The companion `jev_smoke.py` uses only Python's standard library. It requires **no pip package, daemon, MCP server, system service or agent hook**.

Place both handoff files in the chosen experiment directory. Run:

```bash
python3 jev_smoke.py --self-test
python3 jev_smoke.py --dry-run
```

These commands do not contact TypeSafe and need no key. The default, with no arguments, also only prints the synthetic request.

The user creates/provides the TypeSafe key on the execution host. Never ask them to paste it into chat or put it in a source file, command-line argument, recorded terminal output or shell history. A temporary **Bash** session can receive it without echoing the value:

```bash
read -r -s -p 'TypeSafe API key: ' TYPESAFE_API_KEY
printf '\n'
export TYPESAFE_API_KEY
# Only after approval for one synthetic, potentially billed API request:
timeout 15s python3 jev_smoke.py --live
unset TYPESAFE_API_KEY
```

The script sends fixed synthetic state, asks one Choice, one Noul and one Score, validates the response fields it consumes, and reports usage, elapsed time and the resolved model. It neither reads project files nor executes proposed actions. Exit 0 means the smoke response validated, **not that semantic quality or permission safety has been established**.

Missing key exits 2 without a request. HTTP, network or validation failures exit 3. The script performs no automatic retries and refuses redirects. It uses certificate-checked direct HTTPS with environment proxies disabled; a host that requires a proxy needs an explicit, reviewed networking adjustment. Do not disable TLS verification to make it work. The external `timeout` supplies a wall-clock bound in addition to the script's socket timeout.

### Optional SDK installation for the real implementation

Raw HTTPS is sufficient. Install an SDK only when it helps the chosen implementation. Use an isolated environment; choose the project's existing dependency manager rather than introducing two.

```bash
# Python alternative, inside the approved spike directory:
python3 -m venv .venv
.venv/bin/python -m pip install typesafe-sdk
```

For an existing uv-managed project, the documented package can instead be added with `uv add typesafe-sdk`. Record and lock the resolved package and dependency versions after review. Never use `sudo pip` or alter the system Python installation. The Python client is `typesafe_sdk.TypeSafeClient`. [S6]

For a JavaScript/TypeScript project, the documented package is installed with `npm install @typesafe-ai/sdk`; its client export is `TypeSafeClient`. Use the existing package manager and lockfile. [S7]

Neither SDK installation creates a general-purpose official `jev` command. The executable proposed below is **our own adapter**, not an existing TypeSafe CLI.

## 4. First useful implementation

### Shared body, thin agent integrations

Proposed flow:

```text
Codex or Claude / deterministic collector
    -> explicitly bounded, sanitized state
    -> shared jev-decide executable
    -> TypeSafe HTTPS request
    -> schema validation + local policy interpretation
    -> advisory JSON and a local evidence record
    -> existing agent workflow, with original permissions unchanged
```

Use JSON on stdin/stdout; diagnostics belong on stderr. The adapter should not read arbitrary files named by input, execute commands, modify repository content, choose an account, or silently send entire transcripts. Candidate collection is a separate, explicit operation.

Build only one initial use case: **rank a bounded set of candidate context snippets**, or **classify a small sanitized test failure and suggest a next investigative step**. Do not start with autonomous permission approval. A routing decision can select only among explicitly configured, authorized endpoints; it must never create a new model account or invoke an unknown command.

For context selection, keep paths and source ranges addressable. Preserve mandatory project rules and evidence even when a relevance classifier ranks them poorly. Do not claim native context-window control where the CLI only receives optional tool output. Real savings require a boundary where selection actually avoids later reading or processing.

### Proposed adapter contract

This is a project design, **not TypeSafe's native wire schema**:

```json
{
  "schema_version": 1,
  "request_id": "local-unique-id",
  "status": "ok",
  "mode": "observe",
  "requested_model": "jev-1.13.0",
  "resolved_model": "jev-1.13.0",
  "decision": {"kind": "next_step", "value": "inspect_test"},
  "permission_granted": false,
  "evidence": {"state_hash": "...", "question_version": "triage-v1"},
  "usage": {"input_tokens": 0, "output_tokens": 0},
  "latency_ms": 0
}
```

The zero usage/latency values above are placeholders, not measurements. For an error, return an explicit status such as `unavailable` or `invalid_response`, with no fabricated decision. Use fixed reason codes for policy branches; do not invent a natural-language reasoning trace on Jev's behalf.

Set local request-size, time, concurrency and spend budgets smaller than service maxima. Version the schema, questions and policy separately. Log the actual model returned; refuse or escalate an unexpected model version rather than silently treating old calibration as valid. Cache only with a complete key covering state, candidates, model and question/policy versions; invalidate stale evidence.

## 5. How the implementer and agent should behave

**Ask bounded questions.** Choice selects among supplied options. Score evaluates an ordered rubric. Noul gives a yes probability, not a separate confidence score. Independent questions can share one request; dependent judgments require code to compose the results or make another request. [S9]

**Keep exact work in code.** Exit-code checks, numeric comparisons, path constraints, budgets, authorization and deterministic lookups should not become model judgments. Jev's published limitations include literal interpretation, numerical weaknesses and susceptibility to adversarial instructions embedded in state. [S10]

**Keep observations distinct from recommendations.** Test output is evidence; a “done” classification is an interpretation. A passing completion judgment does not replace the actual test, requirements check or human sign-off. Never automatically install a package merely because a classified failure resembles a missing dependency.

**Make unknown explicit.** Include an abstain/no-match option where needed. Do not import a community confidence threshold as a universal safety guarantee. Evaluate thresholds on the actual task and its consequences. Typed output reduces parsing ambiguity; it does not prove the judgment is correct. [S16]

**Preserve authority.** In the initial observe mode, the classifier cannot grant, deny or rewrite native tool actions. On failure, record the failed observation and retain the exact pre-existing permission flow. That baseline may itself be permissive; this is not a promise of a new security boundary.

A future enforcement mode is a separate change requiring approval and tests. A failed mandatory check must block or escalate through a verified path, not become an implicit allow. Deterministic constraints must win even when a mocked model confidently recommends the prohibited action. Shell command names and regexes alone are not a complete execution-security model.

**Minimize cloud disclosure.** Start with synthetic fixtures. Obtain an explicit data scope before sending private source, filenames, logs or business content. Use field allowlists, not merely secret-pattern replacement. Keep local audit records access-restricted and omit credentials. Hashes and file pointers are preferable to uncontrolled raw-payload logging, but even metadata can be sensitive.

TypeSafe says inputs are not used for model training. Its privacy policy also describes retention and US hosting; that is not a blanket zero-retention guarantee. Enterprise zero-data-retention is a separate offering, not an assumed property of this account. [S11–S12]

## 6. Native adapters: a material Claude/Codex difference

Hooks are optional after the shared CLI experiment succeeds. A hook process is not the same as an agent voluntarily calling a tool. Verify behavior against **the installed CLI version**, not just this dated handoff.

**Claude Code:** its `PreToolUse` interface supports `allow`, `ask` and `deny`. An observational hook should emit no permission decision, rather than return `allow` and alter the approval flow. Check current settings locations and hook semantics before adding an entry. [S13]

**Codex:** current documentation includes `PreToolUse` and hook configuration. Critically, `permissionDecision: "ask"` at `PreToolUse` is presently unsupported: the documented behavior is a failed hook with an error **followed by continuation of the tool call**. Do not copy a Claude permission adapter into Codex. For a mandatory human review, block through a verified supported path and request approval separately. Hooks do not cover every execution path. [S14]

For either adapter, preserve existing entries, trust review and permission configuration. Back up and merge only the approved changes; never overwrite entire settings files. Test in a disposable repository/session before touching a live development session. Do not edit transcripts, bypass approvals, or depend on inherited tmux environments carrying a newly entered secret.

An observer should not accidentally become an authorizer, and a failed authorizer should not accidentally become an observer. Those are different contracts.

## 7. Existing implementations worth knowing about

| Project | What it offers | Disposition for this experiment |
|---|---|---|
| `typesafe-ai/skills` | Official integration skill | Preferred documentation aid; review before installation |
| `langchain-typesafe` | LangChain ecosystem integration and harness patterns | Reference only unless the project already uses LangChain |
| `eugeniughelbur/jev-engineering` | Independent gate, routing and context utilities | Audit reference, not a default security installation |
| `ismaelsoilet/jev-harness` | Independent wrapper package | Separate product; not the official model or the PDF |

The community gate's README currently uses `OPENROUTER_API_KEY`, defaults to observe mode, and describes fall-through on errors. Do not confuse that credential/provider path with the direct TypeSafe route used here. Its author also reports adversarial failures. Introducing that provider adds another data and billing boundary. [S17–S19]

No community package was installed or security-audited during this research. Similar names are not evidence of common ownership, official endorsement or interchangeable APIs.

## 8. Acceptance, evidence and rollback

Before connecting real work, demonstrate these properties with local fixtures and mocks:

- Valid responses are consumed; malformed JSON, wrong types, invalid ranges, unknown labels, stale evidence and unexpected model versions are rejected.
- Missing/invalid credentials, timeout, rate limits, server errors, oversized responses and audit-write failures do not silently produce a decision or grant new permission.
- Injected “ignore the rules” text remains untrusted state; secrets and unapproved fields cannot enter an outbound payload. Mock dangerous actions rather than executing them to test the gate.
- The disabled adapter reproduces the original workflow. Observe mode preserves permissions. Any later mandatory-check mode proves blocking on failure across the actual enabled tool paths.

Start with a small labeled fixture set, for example 30–50 varied cases, including failures and ambiguous examples. This is an engineering smoke evaluation, **not security certification or sufficient proof of calibration**. Reserve held-out examples and expand coverage before trusting consequential decisions.

Compare matched tasks with and without the adapter. Record task success, retries, human corrections, candidate misses, end-to-end latency, decision latency distribution, actual token usage and total billed work. A cheaper judgment that loses critical evidence is not a successful optimization. Reevaluate after changing the model, rubric, candidate collector, prompt or agent version.

Deliver `INSTALL_REPORT.md` with exact versions, installed paths, configuration diffs, tests and failures, actual live usage where approved, and remaining unknowns. Distinguish **installed**, **offline-tested**, **API-tested**, and **integrated into native workflow**.

Rollback removes only this experiment's hook/skill entries and files, restoring its backed-up settings without discarding unrelated changes. Preserve required audit evidence securely. Let the user decide whether to revoke the test key; do not delete accounts, logs or global configuration automatically.

## 9. Copy-paste instruction for the implementing agent

```text
Read JEV_RESEARCH_AND_CLI_HANDOFF.md and inspect jev_smoke.py.
Your target is a bounded TypeSafe/Jev experiment beside our existing CLI,
not a replacement coding agent and not an automatic permission authority.

Start with Stage 0: inspect this host, installed versions, project state,
existing skills/hooks and relevant official documentation. Report the
proposed directory, dependencies, configuration changes and data boundary.
Do not expose secrets, change global settings, upgrade CLIs or disturb
existing work. Confirm any unresolved target/scope before modifying it.

Within the agreed isolated scope, run the offline smoke checks, then install
only the selected official skill/SDK pieces that are actually needed.
Request the host-side key and approval for one synthetic API call separately;
do not ask for the key in chat or send project material yet.

Build one shared JSON-in/JSON-out advisory adapter for one bounded use case.
No MCP, background service, transcript editing, automatic dependency repair,
or weakened native sandbox. Separate evidence, model output and policy.
Do not wire a permission hook in the first phase. Codex PreToolUse "ask"
is not interchangeable with Claude "ask"; verify installed-version behavior.

Produce an installation report, tests, measured costs where authorized,
known gaps and an exact rollback. State a failure rather than claiming
installation or safety from an untested configuration.
```

## 10. Research sources

Primary documentation governs implementation; the independent synthesis and community repositories are identified separately. All entries were consulted during research dated 2026-09-24; a mutable page or default branch is not a pinned release.

| ID | Source and address |
|---|---|
| S1 | TypeSafe, use with coding agents — `https://docs.typesafe.ai/introduction/coding-agents` |
| S2 | Official agent skill setup — `https://docs.typesafe.ai/agent-skill`; source — `https://github.com/typesafe-ai/skills` |
| S3 | HTTP API contract — `https://docs.typesafe.ai/api` |
| S4 | Official quickstart — `https://docs.typesafe.ai/introduction/quickstart` |
| S5 | Models, aliases, pricing and limits — `https://docs.typesafe.ai/models` |
| S6 | Python SDK — `https://docs.typesafe.ai/sdk/python` |
| S7 | JavaScript SDK — `https://docs.typesafe.ai/sdk/javascript` |
| S8 | Vendor launch claims and evaluation caveats — `https://typesafe.ai/blog/introducing-system-one-models-and-jev` |
| S9 | Primitives and composition — `https://docs.typesafe.ai/introduction`; official skill source — `https://github.com/typesafe-ai/skills/blob/main/skills/typesafe-ai/SKILL.md` |
| S10 | Published model limitations — `https://docs.typesafe.ai/model-jaggedness/jev-1.13` |
| S11 | Privacy policy — `https://typesafe.ai/legal/privacy-policy` |
| S12 | Legal/data-retention overview — `https://docs.typesafe.ai/legal` |
| S13 | Claude Code hooks — `https://code.claude.com/docs/en/hooks` |
| S14 | Codex hooks — `https://developers.openai.com/codex/hooks` (currently redirects to `https://learn.chatgpt.com/docs/hooks`) |
| S15 | Independent PDF from the screenshot's link — `https://drive.google.com/file/d/17h982xvsL3E7b80iGmOCfKp9qTOW9ohv/view` |
| S16 | Confidence interpretation — `https://docs.typesafe.ai/confidence`; official skill source in S9 |
| S17 | LangChain-authored integration article — `https://www.langchain.com/blog/building-a-harness-with-jev` |
| S18 | Community gate README — `https://github.com/eugeniughelbur/jev-engineering` |
| S19 | Community wrapper package — `https://pypi.org/project/jev-harness/` |

For discovery, TypeSafe publishes `https://docs.typesafe.ai/llms.txt`. Prefer targeted current pages over loading every document into the agent context.

### Verification status of the supplied files

The companion script passed local response-validation fixtures, dry-run execution, compilation and missing-key handling in this research environment. **No authenticated TypeSafe request was made. No installation, hook activation or integration test was performed on majkee's computer.** The supplied script is a diagnostic starting point, not a production security gate.
