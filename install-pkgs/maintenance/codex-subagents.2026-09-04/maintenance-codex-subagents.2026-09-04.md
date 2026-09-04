Repair Astrobley custom-agent discoverability in `/home/hruzam/ia-sync`.

  Use the `codex-harness` and `openai-docs` skills. Diagnose before changing anything; do not assume
  deployment failed.

  Known evidence from 2026-09-04:

  - Host: office (`hruzam-120922`), Codex CLI `0.152.1`.
  - Portable source:
    `/home/hruzam/ia-sync/codex/agents/astrobley.toml`
  - Live target:
    `/home/hruzam/.codex/agents/astrobley.toml`
  - Both files are byte-identical:
    SHA-256 `9d08c3ee857032b84df1322cb996ba7f17103fc1c88aa7b2403c2e4453f581de`
  - `bash deploy.sh --codex-only --dry-run` reports no Astrobley delta.
  - `deploy.sh` correctly maps:
    - `codex/agents/` → `~/.codex/agents/`
    - `codex/skills/` → `~/.agents/skills/`
  - Do not merge or normalize `~/.agents` and `~/.codex`; they serve different discovery surfaces.
  - This prior session successfully spawned `agent_type="astrobley"`, so runtime loading works
  somewhere.
  - Official documentation says custom agents belong in `~/.codex/agents/` or project `.codex/agents/`,
  with `name`, `description`, and `developer_instructions`. Astrobley contains all three:
    https://learn.chatgpt.com/docs/agent-configuration/subagents
  - Official CLI documentation uses `/agent` singular to inspect active/done agent threads. It is not
  documented as an installed-profile inventory. Establish whether the reported `/agents` view is CLI,
  Desktop, command completion, or another UI before treating absence there as a defect.
  - Genuine local documentation drift exists:
    `codex/AGENTS.md` says “Six portable custom agents” and omits Astrobley, while `codex/README.md`
    and `codex/agents/` contain seven roles including Astrobley.

  Required workflow:

  1. Follow ia-sync orientation and `SYNC_DISCIPLINE.md`; inspect the current dirty worktree and
  preserve it.
  2. Confirm current official custom-agent discovery and `/agent` behavior.
  3. Reproduce from a genuinely fresh Codex session:
     - verify Astrobley appears among available spawn agent types;
     - spawn Astrobley by exact `name = "astrobley"`;
     - while it is active, inspect it through the correct client UI or `/agent` command.
  4. Distinguish:
     - deployment/discovery defect;
     - stale-session cache;
     - `/agent` versus `/agents` misunderstanding;
     - documentation-only drift.
  5. Do not copy agent TOMLs into `~/.agents`, edit live `~/.codex` as source, or reorganize either
  skill tree.
  6. Before writing, report the diagnosis, exact proposed source files, deployment target, and proof
  plan; wait for @majkee’s confirmation.
  7. After confirmation, make the smallest source-first repair in `~/ia-sync/codex/`, run syntax/
  content checks, `bash deploy.sh --codex-only --dry-run`, authorized deployment, and fresh-session
  behavioral verification.
  8. Preserve these unrelated existing changes:
     - `.dev/session/runbook-upgrade/RUNBOOK.md`
     - `.dev/session/runbook-upgrade/STATUS.md`
     - `.dev/session/runbook-upgrade/_bus/`
     - `pulse.md`
  9. Do not commit, push, or perform cross-host work without explicit authority.

  Success means Astrobley is proven spawnable from a fresh session and the client’s agent-thread UI
  behaves according to its actual contract. If no runtime defect exists, do not invent one: repair only
  the confirmed documentation drift after approval and explain why `/agents` was the wrong proof.
