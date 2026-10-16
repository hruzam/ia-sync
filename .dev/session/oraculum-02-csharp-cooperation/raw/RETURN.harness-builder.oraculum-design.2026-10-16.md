# RETURN — harness-builder Oraculum design

```yaml
recorded: "2026-10-16 19:18 CEST"
recorded_by: "cartan · Codex · cSharp status_owner"
consulted_role: "harness_builder · no-write design consultation"
verdict: "REVISED PROPOSE — explicit $csharp control skill plus bounded Oraculum agent; creation requires a further Majkee gavel"
```

## Verified substrate

- Installed client: `codex-cli 0.162.1`.
- No candidate exists in either portable source or live target:
  `codex/agents/oraculum.toml` and `~/.codex/agents/oraculum.toml` are absent.
- `git diff -- codex` is empty. No deployed or portable Codex source was changed.
- Current official custom-agent documentation requires `name`, `description`, and
  `developer_instructions`; it permits model and reasoning settings, but says custom-agent
  files cannot override parent sandbox, approval, provider, or MCP configuration.
  [Subagents — ChatGPT Learn](https://learn.chatgpt.com/docs/agent-configuration/subagents)

## Revised native rendering

The recurring controller behavior belongs in an explicit `$csharp` skill; the strategic persona
belongs in `oraculum.toml`. A custom-agent file is the wrong home for parent-owned lifecycle
control, because it governs the child only. The skill instead instructs **Cartan's main thread**
to keep the named child target and deliberately continue it for as many authorized cycles as the
runtime retains that target. It never makes the child a second head or lets it choose its own
wake.

This implements the requested shape: `$csharp` is the operator's explicit request to Cartan,
and Cartan is the caller/holder. The skill is an authority and recovery protocol, not a daemon:
it cannot promise an immortal subprocess, manufacture persistence, or override Codex's own
thread-closing/retention behavior.

## Proposed later source scope

If Majkee gives a separate source-creation gavel, create only:

1. `codex/skills/csharp/SKILL.md` — explicit-only Cartan controller protocol. It directs Cartan
   to retain a running/idle Oraculum target, send each follow-up to that same target while it is
   actually available, record the current handle/cycle and recovery probe in the existing STATUS,
   and stop/recreate only at an explicit authorized edge or observed runtime loss.
2. `codex/agents/oraculum.toml` — a read-heavy, strategic custom agent with
   `model = "gpt-6-astra"` and explicit no-edit/no-canon/no-status/no-delegation instructions.
3. `codex/AGENTS.md` — roster and authority boundary.
4. `codex/README.md` — inventory and use boundary.

Do not change `deploy.sh`, profiles, hooks, skills, Claude source, zsh, live `~/.codex`, or
global permissions. The TOML should use feature/skill capability reductions only where the
installed schema supports them; it must not use `sandbox_mode` as a child isolation claim.

The future `$csharp` skill must be explicit-only, so normal Cartan work does not accidentally
acquire a retained adviser. It must not itself spawn by hidden automation: when invoked, Cartan
checks the RUNBOOK gate, requests/uses the named Oraculum only under the authorized cycle, and
keeps the sole STATUS pen.

## Cooperation contract

Cartan remains the cSharp navigator and sole STATUS writer. A future Oraculum is a named,
analysis-only child: Cartan opens the child once for the approved arc, holds its currently
available target through successive explicit cycles, and sends each continuation to that same
target while the runtime still exposes it. Cartan verifies/records each return and either
continues the same child, asks Majkee for a gavel, or wakes Medusa for a separately authorized
fixed implementation edge. Oraculum never becomes a co-head, direct-user entry point, status
writer, canonical authority, autonomous dispatcher, or Medusa trigger.

Retain from Claude Oraculum only the useful intellectual shape: substrate → architecture →
directive, long-arc/candid reasoning, and Buffering-aware release. Exclude its Claude-specific
tool list, Bash-hook control, direct invocation topology, hard-coded temple map, and any
assumption of write or spawn authority.

## Lifecycle truth and proof boundary

The official documentation supports parent orchestration, follow-up/steering of running
subagents, inspection of active/done threads, and parent-collected results. It does **not**
establish an indefinite held child, durable stable-ID reuse after a session closes, a retention
period, or machine-readable transcript retrieval merely from a TOML role. These remain distinct
claims and must be empirically proved in the installed runtime before promotion.

Required later proof (with disposable/non-sensitive prompts):

1. Start an Oraculum child with nonce A; steer or follow it with nonce B while it is live, and
   preserve the matching thread evidence.
2. Leave it idle after a completed body, then test whether the same runtime can actually
   re-address that exact child with nonce C; record its documented identifier and observed
   retention boundary.
3. Resume the parent session, if supported; separately test whether its child remains visible and
   whether prior results are inspectable.
4. Test transcript or saved-turn retrieval independently. If unavailable, use a concise Cartan
   evidence receipt such as this file and start a new child with that capsule; never represent it
   as a restored child.
5. Fresh-session proof after dry-run deployment, before calling the primitive live.

No lifecycle test, source creation, deploy, or activation is authorized by this return.

## Open hold

`DOPLU discipline` was not found in the readable repository or shared guide search and remains
undefined; it must be supplied by Majkee rather than invented by the agent.
