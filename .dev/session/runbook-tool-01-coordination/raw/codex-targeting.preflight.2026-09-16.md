---
title: Codex targeting and Vara preflight for the coordination pilot
scope: runbook-tool-01-coordination
audience: operator + agent + builder
machine: office
verified: 2026-09-16
state: documentation and configuration evidence; no child/profile/entry test run
recheck:
  - https://learn.chatgpt.com/docs/agent-configuration/subagents
  - https://learn.chatgpt.com/docs/agent-configuration/agents-md
---

# Distinguish four coordinates

**Role** is the delegated contract (`implementer`, `astrobley`, `worker`). **Model**
is the runtime carrying it. **Topology** is root versus spawned child. **Session seat**
is the RUNBOOK/POINT assignment and authority. None substitutes for another.

## Direct answer: Astra parent, different child model?

Yes, the native mechanism supports mixed models. Official documentation permits an
explicit child model/effort or configured defaults; absent those, parent settings are
inherited. A custom-agent file's model/effort takes precedence over the spawn selection.
The docs list Luna for narrow work and Terra for lighter supporting work. That establishes
mechanism, not this account's live model availability or successful execution.
Source, fetched September 16: [OpenAI Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents).

### Local configuration checked

`codex/agents/*.toml` is source; `~/.codex/agents/*.toml` is deployed configuration.
The `name` value identifies the exact role. `implementer` and `astrobley` source/live
files compare equal in this preflight. Other rows below are inspected configured values,
not fresh invocation results.

| Target | Configured model / effort | Consequence |
|---|---|---|
| `implementer` | `gpt-5.6-terra` / high | Routine implementation, distinct from an Astra parent |
| `researcher` | `gpt-5.6-terra` / high | Read-heavy evidence work |
| `astrobley` | `gpt-5.6-sol` / high | Senior implementation; a spawned child, not a sovereign window |
| `architect`, `challenger`, `harness_builder` | `gpt-5.6-sol` / xhigh | Bounded consequential judgment |
| `verifier` | `gpt-5.6-sol` / high | Independent check of a child writer's artifact, not a full-session substitute |
| Built-in `worker` plus explicit model selection | Candidate `gpt-5.6-luna` / medium | No portable `luna` role file found; do not invent that agent_type |

For this currently exposed collaboration tool, fixed custom-role model/effort values
cannot be overridden. Explicit selection on a built-in role requires a non-full-history
fork (`fork_turns: "none"` or a bounded turn count). Re-read the actual tool schema in
the receiving session; this is not a universal CLI command or a promise about another client.

### Operator prompt patterns — candidates, not executed

For the default Terra implementation role:

> Spawn exactly `agent_type=implementer` for this bounded task. Give it the allowed paths,
> constraints and done-when. It is a child; you remain the root and STATUS owner. Report
> the actual spawn result and observed configuration, not the role's self-description.

For a Luna capability probe after the pilot scope is approved:

> Use the native spawn tool for exactly one `agent_type=worker`, request
> `model=gpt-5.6-luna`, `reasoning_effort=medium`, `fork_turns=none`, and a unique task name.
> Give it only the approved fixture path and a read-only classification task with no writes,
> dispatch or gate acceptance. Return observed findings to the parent. If the requested
> role/model cannot be selected, report the limitation; do not silently use the parent model.

For senior Sol execution, target `agent_type=astrobley`; do not ask `implementer` to
pretend to be Astrobley or expect a contradictory model override to change its pinned role.
These are instructions to a controller, not text to paste as a shell command. Pasting
`agent_type=astrobley` into a root chat does not convert that root into a sovereign Astrobley.

## Existing identity bed — earlier dependency, not duplicated here

Inspected on September 16:

- `codex --version`: `codex-cli 0.154.0`; `codex --help` and `codex resume --help` list
  `--model`, `--profile` and `--cd`. Help still describes flat profile layers at
  `$CODEX_HOME/<name>.config.toml`. No top-level `--agent-type` is listed.
- All three commands exited 0 but warned that PATH aliases could not be created in
  the read-only frame. This is help evidence, not launch/resume proof.
- `codex/postures/`, `codex/profiles/`, `~/.codex/postures/` and
  `~/.codex/astrobley.config.toml` are absent. No profile activation was attempted.
- Identity STATUS says Stage A awaits gavel on decisions 1–5 and the exact AGENTS override
  paragraph. Its old worktree/version snapshot is historical; refresh only relevant deltas.
- The existing launcher contains an unquoted `@majkee` YAML item. Its owner should verify
  and repair that bounded syntax defect under its own authority before relying on parsing;
  this planning cut does not modify it or reinterpret its gate.
- A new presence record names that identity bed. Attachment is not proof of an active
  process. Majkee should use its existing window if alive, not create a competing owner.

The profile proposal addresses **sovereign top-level identity**; the existing native
subagent mechanism already addresses **bounded children**. Do not build profiles for
every helper model to answer the latter question. Keep the original five decisions and
P2–P6 gate in their own bed. This successor neither gavels old wording nor modifies its state.

## Vara: useful narrow candidate, not drop-in BUS controller

Read `/home/hruzam/ia-sync/claude/agents/vara.md` and
`/home/hruzam/ia-sync/claude/skills/track-run/SKILL.md` before any trial. Current source
declares Haiku/high, an edit-only sequential walker: the head pre-routes every task;
Vara dispatches only the named worker and stops at the human gate. Classification is
explicitly retired. Its proposed runbook-check capability is explicitly inactive.

**Candidate yes:** walk a bounded pre-routed track or PAD, capture evidence in an
already-created report surface, flag a missing/ambiguous instruction. **No as-is:**
choose the team, resolve semantic conflicts, author fresh BUS receipts, replace STATUS,
own a fanout join or certify completeness across arbitrary prose. Its append-only
checkpoint/program-pulse conventions need reconciliation before use with this bed's
single replacement STATUS. Absence of a Write tool is a declared boundary, not proof
that Bash cannot write; permission enforcement and behavior need their own checks.

Prefer a task-scoped qualified use or no change over turning Vara into a universal
router again. Atlas should recommend Y/N with reasons; never enable a deferred feature
merely because its name matches this request. No Vara or track-run edits here.

## Entry-card Y/N is a test, not a naming decision

For Codex, startup discovery follows the project-root-to-working-directory chain;
merely referencing a deeper RUNBOOK does not guarantee its AGENTS.md entered that chain.
[OpenAI AGENTS.md documentation](https://learn.chatgpt.com/docs/agent-configuration/agents-md),
checked September 16. Parent context inheritance and fresh child configuration are also
separate observations. Claude loading behavior was not established here.

Compare the minimal existing explicit read prompt against a thin local adapter. Test
the proposed same-folder parent/child case directly, without giving a reviewer the head
seat. No global `.dev/session/AGENTS.md` or `.dev/session/CLAUDE.md` is authorized.
