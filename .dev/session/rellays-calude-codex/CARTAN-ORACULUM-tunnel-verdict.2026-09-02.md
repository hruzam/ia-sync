---
what: "RETURN — Cartan's live Codex-side mechanics verdict for termbrana tunnel v0"
state: "MEETING-ROOM INPUT — not STATUS, project canon, or an implementation start signal"
from: "@Cartan (codex/cartan)"
to: "@Oraculum + owner seat + @majkee"
date: 2026-09-02
runtime: "office hruzam-120922 · Manjaro 26.1.0 x86_64 · codex-cli 0.152.1 · gpt-5.6-sol session"
fold_into: "The toolbox-termbrana-03-tunnel owner creates its STATUS.md and folds this verdict there; that STATUS does not exist at return time."
authority: "Live runtime observations below outrank the 2026-09-01 research for volatile CLI facts; §4's app-server-first axis remains gaveled and was not reopened."
---

# Cartan → Oraculum — tunnel v0 verdict

## One-line verdict

**PROCEED with v0 as a local stdio App Server supervisor: preflight the inherited ChatGPT
account and entitled model, start or resume one stored headless thread, drive turns by ID,
stream completion, and reconcile the result with `thread/read(includeTurns: true)`.**
`turn/steer` is live and reliable on the tested path. Pane injection, MCP, visible-mode work,
and native subagent orchestration do not belong in v0.

## Evidence boundary

Observed directly on the installed runtime, 2026-09-02:

- `codex --version` → `codex-cli 0.152.1`.
- `codex login status` → logged in using ChatGPT.
- `codex app-server --help` → stdio (default), Unix socket, and WebSocket transports;
  non-loopback WebSocket listeners require capability-token or signed-bearer-token auth.
- App Server `initialize` → `termbrana_probe/0.152.1`, `codexHome` at the host-local
  `~/.codex`, Unix/Linux runtime.
- `account/read(refreshToken: false)` → account type `chatgpt`, plan type `prolite`,
  `requiresOpenaiAuth: true`; email was redacted from the probe record. This matches the
  documented ChatGPT-account response shape: `requiresOpenaiAuth` alone is not a failed
  login when a ChatGPT account object is present.
- `model/list` returned entitled Sol, Terra, Luna, and earlier models. Sol is the default;
  Sol and Terra advertise `multiAgentVersion: "v2"`, while Luna advertises v1.

Protocol proof used one stored disposable thread with `gpt-5.6-luna`, read-only sandbox,
and approval policy `never`:

1. `thread/start` returned an idle stored thread and the loaded instruction source.
2. `turn/start` returned an `inProgress` turn ID.
3. `turn/steer` accepted additional text with `expectedTurnId` and returned the same turn ID.
4. `turn/completed` reported `completed`, no error; the streamed agent result was `STEERED`.
5. `thread/read(includeTurns: true)` found that turn as completed and returned the persisted
   agent message `STEERED`.
6. `thread/resume` returned the same thread ID in idle state.
7. The disposable probe thread was deleted after the proof.

This behavior agrees with the current [official App Server lifecycle documentation](https://developers.openai.com/codex/app-server):
initialize once, `thread/start|resume`, `turn/start`, active-turn `turn/steer`, streamed
notifications, and final `turn/completed`.

## Mechanics verdict within the gaveled shape

The v0 client should own this sequence:

```text
spawn `codex app-server --stdio`
  → initialize / initialized
  → account/read + model/list preflight
  → thread/start, or thread/resume with the recorded threadId
  → turn/start; retain threadId + turnId
  → optional turn/steer(expectedTurnId = active turnId)
  → consume item deltas + turn/completed
  → thread/read(includeTurns = true) for durable reconciliation
```

Use a **stored** thread for v0. The live runtime rejects
`thread/read(includeTurns: true)` for ephemeral threads, so ephemeral mode cannot provide
the requested persisted read-back contract. Streaming is the low-latency channel;
`thread/read` is the reconciliation channel after completion or reconnect. Resume should
always use the recorded thread ID, never “last thread” inference.

For the same-host v0, stdio is the smallest transport and needs no second listener secret.
Upstream model authentication is inherited from Codex's host-local ChatGPT login. If a later
version crosses a host boundary over WebSocket, transport bearer authentication and TLS are
a separate security frame from the ChatGPT account entitlement; do not conflate them.

## Curvature found live

1. **Official example vs installed enum.** The current official page shows legacy
   `sandbox: "workspaceWrite"`; CLI 0.152.1 rejects `readOnly`/camelCase and accepts the
   CLI-form values `read-only`, `workspace-write`, or `danger-full-access`. Generate or pin
   the 0.152.1 protocol schema in the tunnel bed and contract-test the actual enum rather
   than copying the prose example.
2. **Ephemeral read-back boundary.** `thread/start(ephemeral: true)` works for streaming,
   but `thread/read(includeTurns: true)` fails closed. Stored-thread lifecycle plus explicit
   retention/cleanup policy is therefore part of v0, not an optional persistence detail.
3. **CLI maturity label.** `codex app-server --help` still labels the command experimental
   even though the official docs present the protocol as the rich-client integration
   surface. Pin CLI/protocol behavior for the pilot and treat upgrade as a tested migration.

## Multi-agent status for later v2

The 2026-09-01 research's blanket **UNSTABLE** verdict is stale on this runtime.

- `codex features list` and App Server `experimentalFeature/list` both report
  `multi_agent` **stable, enabled** and `multi_agent_v2` **stable, disabled**.
- The live entitled catalog routes Sol and Terra to multi-agent v2 and Luna to v1.
- Current [official subagent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents)
  says current Codex releases enable subagent workflows by default and expose them in the
  app, CLI, and IDE.

Therefore: **deny “still unstable”; confirm “not yet a v2 dependency.”** The capability and
model route are present, but this local profile has the explicit v2 flag disabled, and this
RETURN did not spawn subagents or canary custom-role/model-override behavior. Before the
termbrana architect-with-crew v2 is scheduled, the owner should enable v2 in an isolated
profile and prove spawn, message/steer, completion collection, custom role selection, model
override, and depth/concurrency limits from a fresh session. That is a focused behavior gate,
not a wait-for-GA gate.

## Ownership and gates

- **This file:** meeting-room evidence and Codex mechanics verdict, owned by Cartan's RETURN.
- **03-tunnel owner seat:** creates the missing STATUS, folds this verdict into the session
  gate, chooses retention policy, and authors the v0 client in the experimental bed.
- **@majkee:** gavels any durable protocol/config lock and any later HANDSHAKE r3/TABLE
  adoption.
- **Fresh-session proof:** remains required before any Codex primitive or tunnel behavior is
  called live.

## What I did NOT touch

- Did not create or edit the 03-tunnel STATUS, RUNBOOK, nablarva flag/pulse, termbrana code,
  ADRs, or the frozen M0 contract.
- Did not reopen app-server-first vs pane injection, and did not test visible-mode injection.
- Did not invoke `codex mcp-server`, alter auth, enable feature flags, or spawn subagents.
- Did not write or deploy anything under live `~/.codex/agents/`.
- Did not commit, push, or deploy.

`[2026-09-02 · codex/cartan · gpt-5.6-sol]`
