---
name: devenv-sync
description: >
  Invoke as /devenv-sync [path]. Pre-flight orientation for agents before touching sync or
  deploy scripts inside any *.devenv repo. Reads SYNC_DISCIPLINE.md and registry.json,
  maps the ownership model, confirms APP_DIR for this machine, runs pre-flight git status.
  Path optional when CWD is already the devenv root.
tools:
  - Read
  - Bash
---

I am the `/devenv-sync` skill — pre-flight orientation for the devenv sync/deploy layer.
Before any agent touches `sync.sh` or `deploy.sh`, I load the project's rules and confirm
the workspace is safe to proceed.

## 1. Locate the devenv root

Use the path argument if provided. Otherwise inspect CWD:
- CWD ends in `.devenv` → use it
- CWD is the app repo → look for a sibling `<project>.devenv/` directory
- Neither → ask the operator to name the devenv root before continuing

Devenv root = directory containing `sync.sh`, `deploy.sh`, `registry.json`, and
`SYNC_DISCIPLINE.md`.

## 2. Read project config

Read both files from the devenv root:
- `SYNC_DISCIPLINE.md` — project-specific W3 table, conflict rules, red flags
- `registry.json` — hostname-keyed `app_dir` entries

Identify the `app_dir` for the current machine (key = `$MACHINE_NAME`).
If the key is missing: report and stop — safe sync requires a valid registry entry.

## 3. Architecture — three layers

The devenv pattern is uniform across all projects:

```
fr-sync / bo-sync          ← keyboard aliases (ai/keyboard.zsh P11)
        ↓ call ↓
ai/devenv.zsh              ← interactive engine (pull --rebase built in here)
        ↓ calls ↓
*.devenv/sync.sh           ← thin wrapper (one per project)
        ↓ sources ↓
~/.config/zsh/ai/devenv-sync-core.sh  ← 8 shared functions (ia-sync backed up)
        ↓ reads ↓
registry.json              → app_dir (per machine)
```

**Two invocation paths — critical distinction:**

| Path | Who uses it | Pull --rebase |
|------|-------------|---------------|
| Keyboard alias (`fr-sync`, `bo-sync`) | Interactive shell | **Built into devenv.zsh** — automatic |
| Direct bash (`bash sync.sh`) | Autonomous agents | **Manual** — you must pull first |

When an agent calls `bash sync.sh` directly, bypassing the keyboard engine, pull discipline
falls entirely on the agent. No pull = overwrite risk.

**Directions:**
- `sync.sh` — app → repo (stage-OUT: copies W3 paths from the live app into the devenv repo)
- `deploy.sh` — repo → app (receive: pushes repo state back into the live app folder)

**If core not found:** `sync.sh` exits `FATAL: sync core not found`.
Recovery: `bash ~/ia-sync/deploy.sh` to restore the core, then retry.

## 4. Ownership model

| Tier | Meaning | Devenv behavior |
|------|---------|-----------------|
| **W1** | Tool-managed (Boost / MCP) — never touched by devenv scripts | excluded from both sync and deploy |
| **W2** | Staged lane — synced into repo for visibility; deploy skips | sync app→repo; never deploy back |
| **W3** | Majkee-owned — safe mirror in both directions | sync + deploy |

**Known W1 paths — must never appear in `git diff --staged`:**

| Project | W1 paths |
|---------|----------|
| freya | `.claude/skills/` managed set (except `freya-context/`) · `.cursor/skills/` · `boost.json` · `.mcp.json` |
| fantasyobchod | none currently — flat W3 sync |

> Table baked in at skill-write time. If a project is missing or a path looks stale:
> cross-check the **"Not mirrored"** section of `SYNC_DISCIPLINE.md` — already loaded
> in step 2. No additional read needed.

**`CLAUDE.local.md` rule:** synced app→repo and **committed as a W3 backup** into the
PRIVATE devenv repo (like `AGENTS.md`). `git add -A` stages it — that is correct. The
app-side guard in `deploy.sh` (`$APP_DIR`) still keeps it out of the public team app repo;
never remove that one. Do NOT re-add a `$DEVENV_REPO` exclude — that previously blocked the
backup (policy flipped 2026-07-27; SYNC_DISCIPLINE.md is the record).

**`CLAUDE.md` (W2 — Boost-managed):** fr-sync backs it up and diffs; never deployed back
— the live Boost-managed copy is never overwritten.

Present the full W3 table from `SYNC_DISCIPLINE.md` (loaded in step 2) here.

## 5. Key invariants — all projects, always

1. **Pull before sync.** When calling `bash sync.sh` directly: `git pull --rebase origin main`
   first, no exceptions. Full sequence: `pull → sync.sh → git add -A → commit → push`.
   Keyboard aliases (`fr-sync`, `bo-sync`) have pull built in — know which path you are on.
2. **`CLAUDE.local.md` is a committed W3 backup** in the private devenv repo — `git add -A`
   stages it, that is intended. It stays excluded on the APP side only (deploy.sh guard).
3. **W1 paths are untouchable.** If any W1 path appears in `git diff --staged`, stop and flag.
4. **Agents stage only.** Run `sync.sh` if instructed. Run `git add -A`. Stop there.
   Commits and pushes are majkee's moves.
5. **No sync.sh without explicit instruction.** Do not run it speculatively.
6. **agents/ and dev/ are additive.** Never `git rm` files here unless the operator named
   them explicitly. More than 2 `git rm` targets at once = red flag.

## 6. Pre-flight check

Run `git status` in the devenv root and report:
- Uncommitted changes already present → read them before adding more
- Files you did not touch showing up → flag before proceeding
- Behind origin → pull first

Do not proceed if the workspace state is unclear.

## 7. Red flags — stop immediately, flag to operator

- `git status` shows files you did not touch
- `git pull` results in a merge conflict
- A file from `sync.deny` appears in `git diff --staged`
- More than 2 `git rm` targets in one operation
- Secret scan exits 1 (sync.sh internal)
- Deploy-guard fires and the mismatch is unclear (freya: `_devenv_deploy_guard` in core)
- `sync.sh` exits `FATAL: sync core not found`
- Any W1 path appears in staged diff

When a red flag fires: commit nothing, note the situation, leave the decision to the operator.

## 8. Ready gate

After loading, report:
- Devenv root: `<path>`
- Project: `<name>` (from devenv dirname)
- APP_DIR for this machine: `<resolved path>` (or MISSING — stop)
- Pre-flight git status: clean / anomalies noted

Then: **"What do you need — sync (app→repo), deploy (repo→app), or inspect first?"**

Wait for operator instruction before touching any files.
