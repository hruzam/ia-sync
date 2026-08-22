---
name: cold-start-card
description: Create a compact, evidence-backed handoff card for a later Codex session. Use when pausing, repairing, resuming, transferring, or closing work that needs exact host, repository, commit, worktree, rollout/session, transport, authority, first-action, and verification context.
---

# Cold Start Card

Leave the next Codex session a precise re-entry point. The card points to durable sources; it does not copy their full contents or the session transcript.

## Capture the frame

1. Resolve the current repository, applicable `AGENTS.md` chain, host, branch, HEAD, upstream, tracked and ignored project state, recent relevant commits, sandbox/write boundary, and any repository-defined state or transport files.
2. Every agent using this skill must run the bonded entry point `bash scripts/capture-context.sh --cwd "$PWD"` from this skill directory. The Bash primitive resolves and invokes the structured Python collector beside it. Treat its JSON as candidate evidence and verify surprising or task-critical fields directly.
3. If the runtime exposes an active goal or plan, record its status. A Codex rollout JSONL is a track file, not project canon: point to it, session ID, model, and effort, but never copy transcript content.
4. Read local project and mailbox contracts before choosing a destination. For a mailbox, compare its claimed Git lifecycle with `git check-ignore` and `git ls-files`; surface any disagreement and never stage the card implicitly. Prefer an explicitly defined handoff path; otherwise use a project-local session directory such as `.dev/session/codex-claude/`. Ask before writing to a shared mailbox or canonical ledger.

Do not inspect or include `.env`, credentials, authentication state, prompt history, full environment dumps, database contents, or remote URLs containing credentials.

## Compose the card

For a project-local card, name it `CS.<slug>.<YYYY-MM-DD>.md`. Inside a message bus, its README controls the filename, sender, receiver, inbox/archive state, and cleanup lifecycle; do not override that contract with the `CS.` convention. Use YAML frontmatter for facts a fresh agent should parse immediately:

```yaml
---
schema: codex-cold-start/v1
kind: repair-handoff
state: ready
created_at: <ISO-8601 with timezone>
created_by: <seat or user>
audience: next-codex-session
host: { hostname: <physical>, logical: <project name or null> }
project: { root: <absolute path>, branch: <branch>, head: <full SHA>, upstream: <name or null> }
worktree: { tracked: clean|dirty, ignored_project_state: clean|dirty|unknown }
codex: { cli: <version>, session_id: <id or null>, rollout: <absolute path or null>, model: <model or null>, effort: <effort or null> }
task: { objective: <one sentence>, first_action: <one command or inspection> }
authority: { may_write: [<scoped paths>], gated: [<commit/push/deploy/destructive actions>] }
pointers: [<durable source paths>]
---
```

Add only the body sections that carry continuity:

- `Read first`: ordered sources and why each matters.
- `Observed state`: expected versus observed facts, including unexplained curvature.
- `Repair queue`: bounded items with acceptance evidence; mark completed work so it is not repeated.
- `First tool shot`: one safe, copyable read-only command block. Prefer `rg`, `rg --files`, targeted `git`, and the included context script over recursive content dumps.
- `Gates`: decisions or mutations requiring the user.
- `Done when`: concrete checks, including any fresh-session smoke test.

Keep claims distinguishable as `observed`, `reported`, or `inferred`. Include exact commits and paths. Do not claim authorship for state that appeared externally during the session.

## Write and validate

Show a concise destination and scope before a shared or canonical write. For an explicitly requested project-local card, write it directly, then:

1. Parse the YAML frontmatter.
2. Confirm every local pointer exists or label it intentionally absent/external.
3. Re-run critical read-only commands and compare expected with observed output.
4. Report the created path and any gated action not performed.
