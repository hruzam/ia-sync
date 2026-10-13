# @Epoch observations — janus escalate/deescalate, belnap, tertium (jev)
Date: 2026-10-02
Triggered by: majkee — "two janus skills + define-belnap (bash?) + maybe define-tertium, or janus protocol update?"
Scope: default radar (Claude Code skills / subagents primitives). No project contract read.

## Findings

### F1 — A skill's `allowed-tools` does NOT give a subagent Bash
WHAT: `allowed-tools` only PRE-APPROVES listed tools for the invoking turn (clears on next user message). It does not restrict and does not add tools. Under `context: fork`, tools/permissions come from the `agent:` target's definition.
SINCE: current docs (fetched 2026-10-02)
SOURCE: https://code.claude.com/docs/en/skills
CONFIDENCE: H (official docs)
IMPACT: "Can a skill allow bash for belnap?" -> only as a permission pre-approval in the main context. A forked belnap gets Bash only if belnap's agent file lists it in `tools:`.
ACTION: Bash capability lives in the agent file (`tools: [Read, Grep, Glob, Bash]`). Skill = launcher only.

### F2 — Model/effort can be switched per spawn, no new agent file needed
WHAT: Model resolution order: per-invocation `model` param > agent frontmatter `model` > CLAUDE_CODE_SUBAGENT_MODEL env > main model. Aliases: sonnet, opus, haiku, fable. Skills with `context: fork` accept `model:` and `effort:` which apply to the forked subagent.
SINCE: env-var precedence fixed in v2.1.251 (before, env var overrode everything).
SOURCE: https://code.claude.com/docs/en/sub-agents · https://code.claude.com/docs/en/skills
CONFIDENCE: H
IMPACT: janus.md today = `model: opus`, `effort: xhigh`, tools Read/Grep/Glob. Escalate/de-escalate needs NO second Janus file.
ACTION: Two thin skills with `context: fork` + `agent: janus`:
  - janus-escalate:   model: opus,   effort: xhigh
  - janus-deescalate: model: sonnet, effort: high   (effort level is my suggestion, not a doc value)
  Plain `Agent(subagent_type: janus, model: sonnet)` already does the same without any skill; skills only add user-typed `/` convenience + a fixed brief shape.
WATCH: set `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1` anywhere and per-spawn override is silently disabled — check env on both hosts.
WATCH: forked skills run in BACKGROUND by default; `background: false` needs v2.1.218+ — verify installed `claude --version` before relying on it. (UNVERIFIED locally.)
WATCH: exact full model ID for "Opus 5.5" not verified this run; use aliases, not IDs.

### F3 — Belnap with Bash must be its own agent, not a Janus variant
WHAT: janus.md declares "read-only, never execute". Giving Janus Bash breaks its invariant (pure deliberation, cheap, safe to spawn anywhere).
CONFIDENCE: M (design inference from janus.md + F1)
IMPACT: Belnap = four-valued verdict (true / false / both / neither). "Both" and "neither" only become meaningful if the agent can gather evidence (run a probe, diff, test) -> needs Bash. Different capability = different agent.
ACTION: new `belnap.md` (tools incl. Bash). Open: restrict Bash by pattern in `tools:`? Docs fetched show patterns for skill `allowed-tools` (e.g. `Bash(git status *)`) — NOT confirmed for agent `tools:`. Test on pilot, don't assume. Fallback: `disallowedTools` + permission rules in settings.

### F4 — `define-tertium` (proof-by-conflict): not ready; protocol before primitive
WHAT: "Proof-by-conflict" is undefined as a procedure. A skill is just a prompt wrapper; the real work is the protocol (how do two conflicting evidence sets resolve, what output shape).
CONFIDENCE: L (no source — my judgment)
ACTION: Do not create a tertium skill yet. Let belnap pilot produce 3–5 real "both/neither" cases, then define tertium as the escalation rule when belnap returns `both`/`neither` (the excluded third). Fits naming: tertium = protocol doc first, skill later.

## Answer to "skills vs janus protocol update"
- Janus agent file: leave unchanged (unchanged .md = stable behavior; you flagged that guardrail yourself).
- Add: `janus-escalate`, `janus-deescalate` skills (thin, fork -> janus).
- Add: `belnap` AGENT (Bash) + optional `belnap-define` skill launcher (naming law = `<program>-<verb>`; "define-belnap" inverts it).
- Defer: tertium.
- Do not spawn atlas-ui yet: jev pilot unfinished; this file is the handoff.

## Not done / open
- Did not check name collisions for `belnap`, `tertium` in ~/ia-sync roster or jev namespace (naming law sweep still mandatory).
- Did not inspect jev's own spawn mechanism — if jev wraps the CLI differently, F2 per-spawn override may not apply. Needs a check against the jev pilot.

Sections to refresh: [F2 background/version check, F3 Bash-pattern-in-agent-tools test, naming sweep]
