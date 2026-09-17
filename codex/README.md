# Codex portable surface

This directory is the compose-first authoring surface for portable Codex behavior on
majkee's office and home hosts. Edit here, review, and deploy outward with `deploy.sh`.
Never harvest live `~/.codex` state back into this repository.

Preview and deploy this surface without touching Claude, Gemini, zsh, or other live
configuration:

```bash
bash deploy.sh --codex-only --dry-run
bash deploy.sh --codex-only
```

## Deployment map

| Repository source | Live target | Semantics |
|---|---|---|
| `codex/AGENTS.md` | `~/.codex/AGENTS.md` | Global Cartan identity and working contract |
| `codex/agents/` | `~/.codex/agents/` | Personal Codex custom agents, additive when present |
| `codex/skills/` | `~/.agents/skills/` | Personal Codex skills, additive when present |

## Global subagent team

`codex/agents/` holds one project-neutral definition for each common delegated role:

| Agent | Role | Default posture |
|---|---|---|
| `architect` | boundaries, options, ADR-ready recommendations | Sol/xhigh, read-only |
| `astrobley` | difficult scoped implementation with senior judgment and explicit return | Sol/high, workspace-write |
| `challenger` | adversarial pre-lock verdict | Sol/xhigh, read-only |
| `researcher` | current primary-source and local evidence | Terra/high, read-only |
| `implementer` | scoped changes and tests | Terra/high, workspace-write |
| `verifier` | independent acceptance gate | Sol/high, workspace-write for test artifacts only |
| `harness_builder` | interactive Codex primitive design and authoring | Sol/xhigh, confirm-before-write |

Projects specialize these agents through their own `AGENTS.md`, `.codex/config.toml`, MCP
servers, and skills. Do not copy these TOMLs into projects or create same-name variants;
add a project-only agent only when its job is genuinely not expressible as a global role
plus local guidance.

`harness_builder` is paired with the `codex-harness` skill. The agent owns judgment and
interaction; the skill owns volatile source routing, primitive selection, and the explicit
Claude↔Codex semantic cross-section.

## Shared procedures

| Skill | Purpose | Cross-runtime invariant |
|---|---|---|
| `codex-harness` | Design and maintain Codex-native primitives | Preserve role meaning and gates, not file parity |
| `buffering` | Hold incremental input or run a creative design arc before release | Claude's cycle and creative-triad semantics in one Codex procedure |
| `cold-start-card` | Leave a verified, temporary re-entry pointer | Point to canonical state; never become another pulse |
| `issue-card` | Preserve defect instances and recurring reaction playbooks | One shared card vault; issue lifecycle stays in its own state subtree |
| `therapy` | Open a held-mirror session with @majkee via `$therapy` | Request-only reflection; one global seat record, shared bed law, and @majkee-only new seeds |
| `octopus` | Sol-grade planning head creates RUNBOOK + STATUS, names the executor, and parks | Expensive judgment is separated from implementation by an operator wake gate |
| `medusa` | Normally Terra-grade working head executes a RUNBOOK and returns curvature upward | Full engineering tools below a fixed gate; architecture remains with Octopus/Cartan |
| `polyp` | Drive a human/model PAD one step and one evidence branch at a time | Raw evidence stays in the PAD; the driver never authors or fixes the work under test |

Cartan remains the identity and integration owner in every protocol. Octopus, Medusa, and
Polyp are operator-selected working postures, not additional global personas. Their model
assignments are default carriages rather than identity locks: the operator selects the model
when opening the session, and each skill states the authority boundary that must survive a
future model change.

Project continuity remains vendor-neutral: settled locks live in the declared `flag.md`, the
project heartbeat/router in `pulse.md`, and the machine contract in `PROJECT.yaml`. When pulse
routes to a live RUNBOOK session, that gate's sole present position is its `STATUS.md`. Codex
does not add a global or per-runtime pulse beside them.

`deploy.sh` copies only these reviewed keep-set paths. It does not copy `config.toml`,
`hooks.json`, rules, credentials, memories, histories, sessions, databases, caches, logs,
installation identity, or trust hashes. Those surfaces are host-local until each earns an
explicit portable design and merge rule.

Candidate observations and experiments belong in `_staging/codex/`, not here. Promotion
into this directory requires evidence, review, and a clear live deployment target.
