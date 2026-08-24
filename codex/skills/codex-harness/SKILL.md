---
name: codex-harness
description: Design, audit, or update Codex harness primitives and their cross-runtime role contracts. Use for Codex agents, skills, AGENTS routing, config, hooks, rules, plugins, MCP/control-plane seams, or Claude-to-Codex semantic adaptation; not for ordinary application implementation.
---

# Codex Harness

Build the smallest Codex-native primitive that preserves the intended behavior and authority
boundary. File parity with Claude is not a goal; semantic drift is the failure to prevent.

## Resolve sources

1. Resolve the active host, Codex version, repository, worktree, sandbox, and instruction
   chain. Read local project truth before shared pattern libraries.
2. For current Codex capability, syntax, models, or behavior, use the `openai-docs` skill and
   fetch current official documentation. Historical local reports are evidence, not current
   product authority.
3. Read [source-map.md](references/source-map.md) for the smallest relevant local source set.
4. When creating, collapsing, or comparing roles across runtimes, also read
   [cross-runtime-roles.md](references/cross-runtime-roles.md).

Do not full-read every corpus on every task. Search by the requested primitive, role,
mechanism, and failure mode; open only the load-bearing files.

## Select the primitive

| Need | Codex surface |
|---|---|
| Always-relevant behavior or routing | global/project `AGENTS.md` |
| Reusable procedure or knowledge bundle | skill |
| Delegated role with its own context and capability posture | custom agent |
| Project MCP, model, profile, or runtime defaults | config |
| Deterministic command authorization | rule |
| Reaction or validation at a lifecycle event | hook |
| Installable bundle of related primitives | plugin |
| Cross-run orchestration, observation, or recovery | exec/SDK/app-server supervisor |

Prefer the smallest sufficient primitive for the need. Do not create an agent for an on-demand
procedure, a hook for advisory policy, or an external supervisor for a single-session task.

## Creator loop

1. State the requested outcome, trigger, authority boundary, expected output, and proof of
   success. Name uncertainty rather than filling it with a familiar Claude mechanism.
2. Run an existence sweep by name and purpose across `~/ia-sync/codex/` and the applicable
   project `.codex/` or skills. If cross-runtime semantics matter, inspect the corresponding
   source under `~/ia-sync/claude/`. Prefer extend, collapse, or reuse over another role.
3. State the invariant being preserved and the Codex-native rendering chosen. Explain one
   material difference from the Claude rendering when there is one.
4. Propose exact source files, activation, write scope, deployment target, and verification.
   Wait for @majkee's confirmation before writing.
5. After confirmation, author on `~/ia-sync/codex/` or the explicitly authorized project
   source. Never author in live `~/.codex/`. Do not reorganize reposoma while consuming it.
6. Validate syntax and content, run the applicable deploy dry-run, and hand actual deployment
   plus fresh-session behavior verification to Cartan or the operator. A file existing on disk
   is not proof that the model uses it correctly.

## Promotion boundary

Keep observation, evidence, and deployable behavior distinct. Promote a recurring correction
to the smallest inspectable home: documentation or `AGENTS.md` for guidance, a skill for
procedure, a test/rule/hook for deterministic enforcement, or nowhere when it did not repeat.
Never auto-promote memories, session reflections, or one successful prompt into global policy.
