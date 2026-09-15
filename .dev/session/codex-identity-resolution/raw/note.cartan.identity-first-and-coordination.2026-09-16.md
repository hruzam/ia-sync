---
title: Cartan handoff — identity first, economical coordination afterward
date: 2026-09-16
author: Cartan
authority: discussion substrate only; no gavel or state replacement
---

# Re-entry and scope

Majkee requested a fresh-session handoff and this note in the identity bed's raw/.
His chosen sequence is identity resolution first, then the runbook/tool follow-up.
The respective STATUS files remain the only present-state authorities.

Read the current identity STATUS, RUNBOOK, and Stage A brief:

- `~/ia-sync/.dev/session/codex-identity-resolution/STATUS.md`
- `~/ia-sync/.dev/session/codex-identity-resolution/RUNBOOK.md`
- `~/ia-sync/.dev/session/codex-identity-resolution/raw/brief.stage-a.identity-decisions.2026-09-09.md`

Observed 2026-09-16: STATUS still reports Stage A awaiting a gavel on decisions 1–5
and the exact AGENTS override paragraph. Portable postures/profiles directories and
the deployed Astrobley posture/profile are absent. The handoff request is not that
gavel. Reconcile any later evidence with the owner; do not recreate Stage A blindly.
The identity RUNBOOK prescribes no delegation in the first cut; discussion of child
agents below does not override it. Only one identity owner should be active.

The existing successor is `~/ia-sync/.dev/session/runbook-tool-01-coordination/`.
"Runbook upgrade 2" describes that follow-up, not a request for a duplicate bed.
Its STATUS already holds execution behind identity closure. Original runbook-upgrade
receipts remain history, not a gate to reopen automatically.

## Model, seat and skills — discussion conclusions, not new behavior proofs

- Sovereign root, spawned child, and model tier are separate coordinates. A stronger
  child does not acquire controller authority. The Astrobley profile proposal concerns
  independent root identity; ordinary mixed-model children do not technically require it.
- The tool surface exposed here permits explicit model/effort on built-in default/worker
  children. Full-history forks inherit parent settings; fork_turns none permits a fresh
  bounded brief with overrides. These are tool arguments, not CLI flags or a universal
  promise about future clients. Current named roles have configured pins: implementer
  Terra/high, architect Sol/xhigh, astrobley Sol/high. Never silently substitute a model.
- Availability, skill selection, full SKILL.md reading, and correct application are
  distinct evidence classes. Name required skills in the child's own brief; do not rely
  on the parent's selection carrying over. Fresh conversation context does not imply an
  empty skill catalog. The harness_builder role already requires codex-harness.
- Medusa is closest to Flight's project-session head mode; Polyp to Vara's PAD mode.
  Vara's pre-routed worker-dispatch track is separate. Polyp does not dispatch workers.
  Skill activation grants neither STATUS ownership nor deployment authority.
- No new spawn, mixed-model, or skill-activation behavior test was run in this discussion.
  Requested configuration, observed runtime metadata, and model self-report stay distinct.

Refresh volatile details against the actual runtime and official sources before execution:
https://learn.chatgpt.com/docs/agent-configuration/subagents and
https://learn.chatgpt.com/docs/build-skills. Local contracts live in
`~/ia-sync/codex/agents/` and
`~/ia-sync/codex/skills/codex-harness/references/cross-runtime-roles.md`.

## Downstream proposal — not identity implementation scope

Majkee questioned costly heads doing clerical continuity work and proposed BUS/STATUS/
RUNBOOK agents or classes, with abstract contracts and concrete implementations.
Cartan recommends a small pilot, not a new lock:

- Compose shared contracts, skills, model/effort, tools and task scope; avoid a permanent
  agent per artifact or deep inheritance framework before a distinct job repeats.
- Scripts check syntax, required fields, references, owner/gate consistency and declared
  outstanding obligations. Valid syntax does not prove truthful evidence or completion.
- One economical controller retains declared ownership. An optional cheap read-only
  coordination helper reports mismatches; it does not ACCEPT on file presence, impersonate
  receipt writers, replace STATUS, or bypass independent verification/gavel.
- Enforce "final" boundaries through permissions and validated write paths, not only prose.
  Keep attention/notifications advisory; no auto-wake, retry, delivery claim or LLM polling.
- Compare missed obligations, false alarms/completions, operator interventions and actual
  token use. Neither savings nor improved reliability has been measured yet.

The successor already contains the team prompts and scoped pilot plan:

- `~/ia-sync/.dev/session/runbook-tool-01-coordination/RUNBOOK.md`
- `~/ia-sync/.dev/session/runbook-tool-01-coordination/STATUS.md`
- `~/ia-sync/.dev/session/runbook-tool-01-coordination/raw/seed.csharp.2026-09-16.md`
- `~/ia-sync/.dev/session/runbook-tool-01-coordination/raw/codex-targeting.preflight.2026-09-16.md`
- `~/ia-sync/_staging/codex/cartan.observation.runbook-bus-status.2026-09-16.md`

## Added by majkee — capture-context as a future context/PTY relay component

Source inspected: `~/.agents/skills/cold-start-card/scripts/capture-context.sh` and
`~/.agents/skills/cold-start-card/scripts/capture_context.py`. Portable source is under
`~/ia-sync/codex/skills/cold-start-card/scripts/`; compare source/live before changes.
Correct invocation from any working directory (the UI's wrapped path is one argument):

```bash
bash ~/.agents/skills/cold-start-card/scripts/capture-context.sh --cwd ~/ia-sync
```

Observed from code and an invocation: the wrapper runs a Python collector printing JSON
with host/tool versions, repo HEAD/branch/upstream, path/status lists, diff statistics,
recent commit metadata, candidate instruction paths, and candidate Codex session metadata.
It is an environment/re-entry snapshot, NOT an exact copy of conversation, model context,
instruction contents, source-file contents, or PTY scrollback. It sends nothing anywhere.

Critical limitation: it sorts up to 100 rollouts by modification time, then picks the
first whose recorded CWD matches. Parallel sessions in ia-sync can therefore yield the
wrong session. Model/effort come from that candidate's latest found turn_context, not
attestation of the requesting process. It reads rollout data internally but excludes
transcript content from emitted JSON. Instruction discovery is heuristic too: for example,
it does not enumerate AGENTS.override.md. Treat results as candidates, not identity proof.

Possible later use: this metadata envelope alongside a deliberately selected transcript
excerpt or PTY capture. Required design questions: exact session/pane identity, source
type, bounded range, timestamps/truncation, secret review/redaction, explicit destination,
and operator approval before sending. Visible PTY output is not complete internal model
context. Do not blindly forward JSON either: paths, commit metadata and session IDs can
be sensitive. Capture, preview and transport are separate operations. No extension,
sender, PTY capture, or external transmission was authorized or built in this handoff.

## Write boundary

Only this note and the central vault card are added. No STATUS, RUNBOOK, receipt,
runtime/source primitive, index, commit, deployment or transport changes. Preserve dirty
peer work; consult current STATUS after clearing the conversation. This dated note is
not a new action queue or authority.
