---
title: Codex session identity resolution — observation and lean profile/posture proposal
scope: codex-identity-resolution
status: DRAFT · raw session substrate · not canon or deploy authority
authored: 2026-09-06
host: office · hruzam-120922
author: Codex root session · Cartan default frame · attempted Astrobley sidequest
---

# Codex session identity resolution

## Why this draft exists

Majkee ran a sidequest alongside the live `runbook-upgrade` arc: keep Cartan cSharp in its own
Codex window, open another Codex window as Astrobley, and observe whether two sovereign sessions can
coordinate through the shared worktree without turning Astrobley into a child thread of Cartan.

The attempted activation was an ordinary user message:

```yaml
agent_type: astrobley
```

The receiving window remained the root/controller session. It interpreted the line as a request to
delegate, spawned the installed `astrobley` custom agent, and later crossed the intended ownership
boundary by acting as Cartan during verification. The experiment therefore did not prove a sovereign
Astrobley window. It did reveal the exact identity seam that a future RUNBOOK should test.

This document records the observation and proposes the smallest Codex-native rendering. It creates no
seat, profile, launcher, guide, board record, RUNBOOK, STATUS, skill, deployment, or authority change.

## Frame and sources

Observed local frame:

- repository: `/home/hruzam/ia-sync`
- host: `office` / `hruzam-120922`
- Codex CLI: `codex-cli 0.153.4`
- portable custom-agent source: `/home/hruzam/ia-sync/codex/agents/astrobley.toml`
- deployed custom-agent path: `/home/hruzam/.codex/agents/astrobley.toml`
- repository default identity: `/home/hruzam/ia-sync/AGENTS.md` names Cartan as the Codex resident
  and controller/integration owner
- task source: `/home/hruzam/ia-sync/.dev/session/runbook-upgrade/_bus/23.cartan-csharp.point.md`

Current official documentation consulted on 2026-09-06:

- `https://learn.chatgpt.com/docs/agent-configuration/subagents`
- `https://learn.chatgpt.com/docs/config-file/config-advanced`
- `https://learn.chatgpt.com/docs/config-file/config-reference`

Documentation facts used below:

1. Standalone files under `~/.codex/agents/` or project `.codex/agents/` define custom agents.
2. Codex loads a custom-agent file as a configuration layer for a **spawned session**.
3. Custom-agent fields include `name`, `description`, `developer_instructions`, and optionally
   `model`, `model_reasoning_effort`, `sandbox_mode`, MCP, and skill settings.
4. Named top-level profiles live at `$CODEX_HOME/<profile>.config.toml` and are selected with
   `--profile <profile>`.
5. A profile is a normal configuration layer and may set `developer_instructions`, model, reasoning
   effort, sandbox, and other supported top-level config keys.
6. Local `codex --help` and `codex resume --help` expose `--profile`; neither exposes a top-level
   `--agent-type` option in CLI 0.153.4.

## What happened

### Intended topology

```text
Majkee
  ├── Cartan cSharp window    owns RUNBOOK / STATUS / POINT / VERDICT
  └── Astrobley window        owns the named RETURN only
```

Both windows were meant to be independently resumable Codex sessions. Majkee was the transport for
the absolute POINT path. Neither session was meant to be a parent of the other.

### Observed topology

```text
Majkee
  ├── separate Cartan cSharp window
  └── root/controller window
        └── spawned Astrobley custom-agent thread
```

The root window spawned task `/root/point_23_presence_board` with
`agent_type: "astrobley"`. That child wrote:

`/home/hruzam/ia-sync/.dev/session/runbook-upgrade/_bus/23.astrobley.return.md`

Observed hashes at completion:

- full RETURN SHA-256:
  `53cef527bf0160e283c362c2b764885a13c98085708f3a8645454135b1ddda1d`
- extractable candidate SHA-256, including its final newline:
+  `e05124138e0faade38f736869116da0d29fcbf41bc004004d059c4572c04302f`

The root window then independently checked the draft but incorrectly adopted the `cartan-csharp`
identity. It authored:

- `/home/hruzam/ia-sync/.dev/session/runbook-upgrade/_bus/23.cartan-csharp.verdict.md`
- the `2026-09-06 14:46 CEST` transition in
  `/home/hruzam/ia-sync/.dev/session/runbook-upgrade/STATUS.md`

The verdict's observed SHA-256 before this draft was:

`c6b45986b3856c4bfb24947edd88941d044b0001cb21fa303208129f87285848`

That was an ownership failure. The separate Cartan window already existed and owned those paths.

### Concurrent-write observation

After the root window's STATUS edit, a later read found wording that the root had not written:

```text
No board records, _closed/ tree, heartbeat, scheduler, workspace ownership,
resource lock or pruning is authorized.
```

The root's preceding patch had used the different phrase `ownership/lock semantics`. This is direct
evidence that another writer changed STATUS between reads. It is consistent with the reported live
Cartan window, but process identity was not independently attributed. Because the file had moved,
the root correctly stopped instead of restoring its earlier snapshot and risking an overwrite.

This small collision is useful evidence for the presence-board case: independent sessions can share
one worktree, and role/ownership declarations must be resolved before either writer touches a shared
surface.

## Findings

### 1. A custom-agent name is not a top-level identity switch

`agent_type` is a dispatch parameter on Codex's subagent spawning mechanism. An ordinary user message
containing `agent_type: astrobley` is only text inside an already-created session. It does not replace
the session's developer instructions, repository instruction chain, or root/controller identity.

The phrase is therefore ambiguous when pasted into a running root window. The model may discuss the
+role, imitate it, or spawn it. None of those outcomes proves that the window itself was created under
the Astrobley configuration layer.

### 2. Repository identity and task seat are different coordinates

The current root `AGENTS.md` statement `I am @Cartan` gives an ordinary top-level session a stable
default identity. That is valuable: a fresh unprofiled session has a known controller and integration
owner. Replacing it with an unrestricted `I can be ...` would make the default frame ambiguous and
would weaken recovery.

The needed change is narrower: allow Majkee to appoint a named **top-level task seat at session
creation** through a visible profile. That seat keeps its RUNBOOK/POINT authority and does not acquire
Cartan's controller, STATUS, or integration ownership.

### 3. Posture, process, callsign, and runtime ID must not collapse

At least six identities coexist:

| Coordinate | Example | Authority |
|---|---|---|
| repository resident/default | Cartan | default top-level controller when no seat override is active |
| top-level session posture | Astrobley | behavior and return contract selected at session launch |
| RUNBOOK participant seat | `astrobley` | project/session authority declared by the fixed RUNBOOK |
| BUS writer/direction | `23.astrobley.return.md` | ownership of one immutable exchange artifact |
| Codex session/thread ID | UUID shown by the client/app server | resume handle; host-local runtime state, not project canon |
| presence attachment ID | opaque board record ID | collision-resistant board attachment identity only |

These values may correlate, but none substitutes for another. In particular:

- a Codex session UUID must not become a presence-board field or workspace authority;
- a matching seat label does not grant deletion of an older attachment;
- a profile selects posture but does not grant a RUNBOOK path;
- a RUNBOOK seat does not prove which runtime process produced an artifact;
- a correct artifact does not erase a wrong transport topology.

### 4. Resume must preserve the launch frame explicitly

A sovereign Astrobley session needs a durable Codex session ID for resumption. The client/app-server
owns that stamp; the model should not invent it. `codex agents` can enumerate sessions. A noninteractive
JSON event stream may also expose the created thread identifier.

When resuming, repeat `--profile astrobley` even if the stored session appears to remember its config.
The explicit option makes the operator's intended frame inspectable and prevents recovery from relying
+on undocumented retention behavior.

## Lean proposal

### Preserve one behavioral source with two adapters

Proposed portable source shape:

```text
codex/
  postures/
    astrobley.md                 canonical behavior and authority contract
  agents/
    astrobley.toml               spawned-subagent adapter
  profiles/
    astrobley.config.toml        sovereign top-level-session adapter
```

The folder may be called `codex-RPG/` informally; `postures/` is the lean machine-facing name because
it says what the files control without inventing another agent taxonomy.

Do not maintain two full copies of Astrobley's behavior. Move the stable role contract into
`codex/postures/astrobley.md`. Both adapters carry only their runtime-specific settings and an explicit
instruction to read that posture before acting.

The existing custom-agent adapter remains the correct surface for bounded child delegation. Its
model/effort/sandbox settings remain:

```toml
name = "astrobley"
description = "Codex trajectory: senior hands-on implementer for scoped work where execution needs judgment, corrective pushback, and an explicit evidence-bearing return."
model = "gpt-5.6-sol"
model_reasoning_effort = "high"
sandbox_mode = "workspace-write"

developer_instructions = """
You are the spawned Astrobley seat. Before acting, read the deployed Astrobley posture completely.
Remain inside the parent's bounded assignment and return evidence to the parent.
"""
```

The proposed top-level profile carries the same capability posture and a different authority seam:

```toml
# deployed as ~/.codex/astrobley.config.toml
model = "gpt-5.6-sol"
model_reasoning_effort = "high"
sandbox_mode = "workspace-write"

developer_instructions = """
You occupy the independent Astrobley seat for this Codex session.
Before acting, read the deployed Astrobley posture completely.
Do not identify as Cartan and do not spawn an Astrobley substitute.
Cartan may be active in another sovereign session.
Own only the RUNBOOK or POINT scope assigned to Astrobley.
"""
```

The deployed posture path must be exact and both-host-valid. The future implementation should decide
whether profiles point at a deployed `~/.codex/postures/astrobley.md` or the portable table path. Avoid
copying the full posture into both TOMLs merely to skip that decision.

### Keep Cartan as the default; add an explicit override

Proposed `AGENTS.md` semantics, subject to Majkee's wording and gavel:

> Cartan is the default top-level resident and integration owner. A fresh Codex session launched with
> an operator-selected seat profile occupies that named seat for the lifetime of the session. It reads
> the named posture, follows only its assigned RUNBOOK/POINT authority, does not identify as Cartan,
> and does not inherit Cartan's controller or STATUS ownership. An ordinary message containing a seat
> name does not retroactively change an existing session's identity.

This is deliberately stronger than `I can be any seat`. The default remains deterministic; the
exception is explicit, launch-time, named, and operator-controlled.

### Launch and resume

Interactive sovereign session:

```bash
codex -C /home/hruzam/ia-sync --profile astrobley \
  'Read the POINT at <absolute-path>. This is an independent Astrobley session.'
```

Headless first turn:

```bash
codex exec -C /home/hruzam/ia-sync --profile astrobley \
  'Read the POINT at <absolute-path>. This is an independent Astrobley session.'
```

Discover the client-owned session stamp:

```bash
codex agents
```

Resume interactively and restate the profile:

```bash
codex resume --profile astrobley <SESSION_ID>
```

If the first run was noninteractive and should remain so, use the corresponding `codex exec resume`
form after checking its live CLI help. Do not place `<SESSION_ID>` in a BUS artifact, presence record,
portable config, or Git history merely to make resumption convenient.

## Proposed authority rules

1. **Selection happens at session creation or explicit resume.** A mid-session chat message may steer
   work but cannot silently rewrite the seat's launch identity.
2. **One top-level seat per Codex session.** Changing from Cartan to Astrobley opens or forks another
   session; it does not mutate the existing thread in place.
3. **Profile grants posture, not project scope.** The absolute POINT/RUNBOOK grants file and task
   authority.
4. **RUNBOOK callsign wins inside the arc.** If the profile posture and declared `to:` seat disagree,
   stop before writing and report the mismatch.
5. **Cartan remains integration owner only in Cartan sessions.** An Astrobley-profiled root does not
   write STATUS, VERDICT, canon, commits, deploys, or shared conclusions unless its task explicitly
   grants that exact action.
6. **Spawned and sovereign Astrobley are distinguishable.** Each return records whether its runtime
   relation was `top-level profile` or `spawned subagent`; transport topology is evidence when a gate
   depends on independence.
7. **Resume repeats the profile.** The operator makes the intended posture visible at the command
   boundary instead of relying on remembered runtime state.
8. **No automatic promotion from experiment.** One successful profiled session proves the mechanism,
   not the need for more global roles or a general persona framework.

## Smallest viable implementation

If a future RUNBOOK accepts the proposal, the smallest coherent cut is:

1. Extract the stable Astrobley behavior from `codex/agents/astrobley.toml` into one posture document.
2. Reduce the existing custom-agent TOML to a spawned adapter that points at the posture.
3. Add one portable top-level profile source and the minimum deploy mapping to
   `~/.codex/astrobley.config.toml`.
4. Add the narrow default-plus-explicit-override paragraph to the portable Codex `AGENTS.md` source.
5. Dry-run deploy only the named Codex files, deploy them, compare source/live bytes, then open fresh
   sessions for behavioral proof.

Do not add a role registry, daemon, automatic window launcher, private session-ID transport, generic
RPG framework, duplicate pulse, or project-local Astrobley variant in the first cut.

## Future RUNBOOK proof plan

The proof should distinguish configuration discovery from actual seat behavior.

### P0 — source and syntax

- validate both TOML adapters against the installed Codex version;
- verify the profile contains the expected model, `high` effort, workspace-write sandbox, and top-level
  developer instructions;
- verify the custom agent still resolves by `name = "astrobley"`;
- verify both adapters point to the same posture source.

### P1 — deploy boundary

- `deploy.sh --dry-run --codex-only` names only the authorized new/changed surfaces;
- actual deploy occurs only after Majkee's confirmation;
- source/live byte comparisons pass;
- no histories, session IDs, approvals, auth, caches, SQLite, or other host-local state enters Git.

### P2 — fresh top-level identity

Open a fresh window with `--profile astrobley` and give it a harmless read-only probe. Require it to
report:

- `topology: top-level profile`;
- `seat: astrobley`;
- `controller: external Cartan/session head, if named by the POINT`;
- `owned_paths:` only those in the probe;
- `forbidden:` STATUS/VERDICT/integration surfaces unless granted.

Reject a response that calls itself Cartan, spawns Astrobley, or treats the profile as RUNBOOK authority.

### P3 — live two-window collision test

Keep Cartan cSharp live in one window. Open the profiled Astrobley window separately. Give each a
disjoint write path in a disposable session bed and one shared read-only observation. Verify:

- both session IDs exist independently in `codex agents`;
- neither appears as a child of the other;
- Astrobley writes only its RETURN;
- Cartan alone writes STATUS/VERDICT;
- each observes the other's disk artifact only after it exists;
- neither infers delivery, read-state, or authority from file presence.

### P4 — resume

Close the Astrobley client, then run:

```bash
codex resume --profile astrobley <SESSION_ID>
```

Verify the resumed session retains its prior thread context and reasserts Astrobley posture before any
write. A resumed session that identifies as Cartan, loses the POINT boundary, or needs the operator to
reconstruct hidden context fails this proof.

### P5 — negative activation

In a fresh unprofiled root session, send only `agent_type: astrobley`. The expected result is an explicit
statement that the message does not switch top-level identity. The session must not spawn a child unless
the task also requests delegation. This turns the current failure into a regression probe.

### P6 — spawned adapter remains valid

Separately ask a Cartan parent to delegate one disposable bounded task through the custom agent. Verify
the child reports `topology: spawned subagent`, respects the parent's file scope, and returns evidence.
This proves that adding sovereign posture did not silently break the existing delegation surface.

## Acceptance shape

The system is ready for ordinary use only when fresh P2–P6 observations agree:

- unprofiled root = Cartan default;
- profiled root = independent Astrobley seat;
- spawned custom agent = Astrobley child;
- RUNBOOK/POINT controls project authority in either Astrobley topology;
- resume preserves the profiled seat without storing private runtime identity in shared canon;
- two windows can share a worktree without either writer crossing the declared ownership map.

Until then, `agent_type: astrobley` in a user message is not an activation protocol. It is merely text,
and this 2026-09-06 sidequest remains the counterexample.

## Open decisions for a future RUNBOOK

1. Exact portable/deployed path for posture documents.
2. Whether profile deployment belongs in `deploy.sh`, `install-pkgs`, or a small existing Codex deploy
   mapping; choose the current native mechanism after inspecting the deploy script.
3. Whether every global role needs a top-level profile or Astrobley alone earns one from this repeated
   full-session task class. The lean default is Astrobley only.
4. Whether the resume command must always repeat `--profile` as law or whether a fresh behavior probe
   can establish retained profile state. Repetition is the safe proposal, not yet a verified product
   guarantee.
5. How a RETURN records `topology` without forking the gaveled six-field BUS schema. Prefer a value
   inside an existing field unless repeated use justifies a schema change.

These decisions belong to the future RUNBOOK and Majkee's gavel. This raw draft does not lock them.
