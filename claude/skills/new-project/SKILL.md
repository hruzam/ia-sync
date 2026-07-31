---
name: new-project
description: >
  Invoke as /new-project <name>. Bootstrap a new temple project pair — app repo + devenv sibling.
  Walks the topology canon checklist: scope-group MANDATE · harness scaffold · devenv scaffold ·
  registry beacon + index row · machine-layer wiring · devenv transport wiring · shell commands
  block. Confirms before writing each layer. Emits shell commands (git init · gh repo create ·
  first sync run) — never executes them. Use after the project name and scope-group are decided.
  Spine: raw.canon/canon.project-topology.md (gaveled 2026-07-14).
---

I am the `/new-project` skill — the bootstrap procedure for a new temple project pair.
I walk the topology canon checklist in order, confirm before writing each layer, and
emit the shell commands block at the end. I do not execute shell commands.

**Spine:** `raw.canon/canon.project-topology.md` (gaveled 2026-07-14)
**Template:** `reposoma/registry/_beacon.template.md`
**After bootstrap:** `/project-read <project>` · `/devenv-sync` · `/project-regular-self-report`

---

## 1. Intake

Ask for all six before proceeding:

1. **Project name** — exact slug (lowercase · hyphens · no dots unless family convention e.g. `freya.devstudio`)
2. **Scope-group** — the parent folder under `~/www/`. Canon examples:
   - `imago_cz/` — client Imago (freya, fantasyobchod)
   - `psdvs/` — psdvsSys org
   - `elements-factory/` — UI playground family
   - `ovum/` — temple infrastructure
   - New scope-group: name it now; majkee decides
3. **Host** — `office` | `home` | `both`
4. **Purpose** — one-sentence description (goes into beacon + AGENTS.md)
5. **Stack** — `<framework · version · language · key deps>` — or `open` if undecided at bootstrap
6. **GitHub visibility** — `private` | `public`

Do not write anything until all six are confirmed.

---

## 2. MANDATE check — scope-group

> "A bootstrap without a scope-group is a **stop-item**, not a style preference."
> — `canon.project-topology.md`

The pair lives at:
```
~/www/<scope-group>/<project>/
~/www/<scope-group>/<project>.devenv/
```

If the scope-group does not exist yet: include `mkdir -p ~/www/<scope-group>/` as step 0
in the shell commands block (step 9). Never skip the group folder — the 2026-07-14
applications-in-common relocation (8 pointer rewires, one full executor run) is the
canonical cost receipt.

---

## 3. App harness scaffold

Show the full file list below, confirm once, then write all.

**Files to create inside `~/www/<scope-group>/<project>/`:**

```
AGENTS.md
CLAUDE.md
.gitignore
.dev/flag.md
.dev/pulse.md
.dev/PROJECT.yaml
.dev/dev.journal.json
.dev/_mail/toAll/inbox/.gitkeep
.dev/_mail/toAll/archive/.gitkeep
.claude/rules/00-discipline.md
.claude/agents/.gitkeep
.claude/skills/.gitkeep
```

**Mail seats:** seed `toAll/` only (inbox + archive). Other seat folders (`atlas/`, `epoch/`,
etc.) are created on-demand when the first mail to that seat is actually sent. Do not
pre-create them.

---

### AGENTS.md

```markdown
# <project> — lighthouse

<one-line purpose>

## The loop

read harness (AGENTS.md → flag → pulse → PROJECT.yaml) → find next gate →
design as handoff → challenge before lock → record durably → keep pulse current

## Hard rules

- Canon is gaveled by @majkee. Draft; he gavels; then it locks and we hold the line.
- Flag.md locks are invariants — no seat crosses them without a gavel.
- Read this project's harness fresh each session. Never carry memory from another project.
- Authoring surface = this repo (`.dev/` · `.claude/`). gitignored — never committed.

## Delegation table

| Task | Route to |
|---|---|
| Phase planning / gate design | @Houston |
| Implementation | @Trajectory / @Delta |
| Research | @Epoch |
| Primitive creation | @Atlas |
```

---

### CLAUDE.md

```markdown
@AGENTS.md
```

---

### .gitignore

```gitignore
# Temple harness — gitignored; transported via <project>.devenv/
AGENTS.md
CLAUDE.md
.dev/
.claude/
.mcp.json
```

Add project-specific ignores below (e.g. `.env`, `vendor/`, `node_modules/`).

---

### .dev/flag.md

```markdown
# <project> — flag (locked decisions)

Newest lock on top. Locks are invariants — no seat crosses without a gavel (@majkee).

## L1 — Stack

<framework · version · language · key deps — or "open: decided per experiment">

## L2 — Branch model

Single branch: `core`. Direct commits; no PRs for solo work.

## L3 — Authoring surface

Harness authored here (`.dev/` · `.claude/`) — gitignored. Transported via `<project>.devenv/`.

## L4 — Language

English for all agent-facing content (AGENTS.md · flag · pulse · mails).
```

Add project-specific locks as they are gaveled. Never edit a locked entry — append only.

---

### .dev/pulse.md

```markdown
# <project> — pulse

Newest on top.

## Phase 0 — bootstrap [DONE <YYYY-MM-DD>]

Bootstrap complete. Harness scaffolded. Devenv pair live.

**Pending:**
- Gate Phase 1 goal with @Houston
- Run first devenv sync (ia-sync → shell reload → /devenv-sync)
```

---

### .dev/PROJECT.yaml

```yaml
project: <project>
stack: <framework · language · key deps — or "open">
host: <office|home|both>
mcp: none
agents: []          # added per-session as Foreman rule permits
skills: []
devenv:
  transport_path: ~/www/<scope-group>/<project>.devenv
  branch: core
  sync_discipline: SYNC_DISCIPLINE.md
```

---

### .dev/dev.journal.json

```json
[
  {
    "date": "<YYYY-MM-DD>",
    "phase": "0",
    "event": "bootstrap",
    "note": "Project pair created. Harness scaffolded. Devenv live. Phase 1 pending gate."
  }
]
```

---

### .claude/rules/00-discipline.md

```markdown
# Agent discipline

- Token economy: read only what the task requires.
- Delegation: do not exceed your seat's scope. Route upward when unsure.
- Hard stops: if a flag.md lock is at risk, stop and surface — never cross without a gavel.
- Authoring: no disk writes without operator confirmation.
- Machine layer edits (zsh, base.zsh, devenv.zsh): dispatch to @Delta with fresh-read-first.
```

---

## 4. Devenv scaffold

Show the file list, confirm once, write all.

**Files to create inside `~/www/<scope-group>/<project>.devenv/`:**

```
README.md
SYNC_DISCIPLINE.md
sync.sh
deploy.sh
sync.deny
registry.json
template.registry.json
.gitignore
claude/agents/.gitkeep
claude/rules/.gitkeep
claude/skills/.gitkeep
dev/.gitkeep
```

Use `psdvsSys.devenv` or `applications-in-common.devenv` as the reference shape for
`sync.sh` / `deploy.sh` / `SYNC_DISCIPLINE.md` — read one of those files fresh,
substitute the project name, adapt W3 paths.

**registry.json shape:**
```json
{
  "<MACHINE_NAME>": { "app_dir": "/home/hruzam/www/<scope-group>/<project>" }
}
```
Include only hosts where the project actually lives. For a not-yet-deployed host:
`"<host>": { "app_dir": "" }` — empty signals not deployed there yet.

**SYNC_DISCIPLINE.md** must include:
- W1 / W2 / W3 ownership table (start minimal — expand as the project grows)
- Pull-before-push invariant
- sync.deny baseline (`.env` · secrets)

**.gitignore:**
```gitignore
*
!.gitignore
!README.md
!SYNC_DISCIPLINE.md
!sync.sh
!deploy.sh
!sync.deny
!registry.json
!template.registry.json
!claude/
!claude/**
!dev/
!dev/**
```

---

## 5. Registry — beacon + index row

**5a. Create beacon** `reposoma/registry/<project>.md`.
Read `reposoma/registry/_beacon.template.md` for the exact frontmatter schema, then fill:

```yaml
---
beacon: <project>
path: /home/hruzam/www/<scope-group>/<project>
repo: github.com/hruzam/<project> (app) · github.com/hruzam/<project>.devenv (harness) — both <visibility>, branch core
host: <office|home|both>
status: bootstrap
contract: .dev/PROJECT.yaml
lighthouse: AGENTS.md
sibling-of: []
shares: []
deposited-by: atlas
updated: <YYYY-MM-DD>
---

# <project> — beacon

<one-line purpose>

## Read first
- contract  → .dev/PROJECT.yaml
- decisions → .dev/flag.md
- state     → .dev/pulse.md
- lighthouse → AGENTS.md

## Shared anchors
(empty at bootstrap — fill in as sibling relationships form)
```

**5b. Add row to `reposoma/registry/index.md`** under `## Projects`:
```
| <project> | <office|home|both> | bootstrap | [`registry/<project>.md`](<project>.md) | `AGENTS.md` · `.dev/PROJECT.yaml` · `.dev/flag.md` |
```

Do NOT create a file under `registry/projects/` — that format is retiring. Beacon only.

If siblings are known at bootstrap: add them to `sibling-of:` in the beacon frontmatter
AND add a row to the `## Sibling-graph` section of `registry/index.md`. Also update
the counterpart beacons to point back.

---

## 6. Machine layer — temple-project-map.zsh

**File:** `~/.config/zsh/ai/temple-project-map.zsh`

⚠ **Fresh-read rule (standing warning):** read the file from disk before editing —
never act from held session memory. The file is touched by multiple sessions.
If Bash is available: spawn @Delta with the exact edit below.

**Add one entry** to `TEMPLE_PROJECT_MAP`:
```zsh
[<project>]="/home/hruzam/www/<scope-group>/<project>"
```

**Update the sync comment** at the top of the file:
```zsh
#   mapped:  reposoma · ... · <project>
```

**🔴 Activation gate:** this entry is not live until:
1. `ia-sync` runs (propagates the file to the devenv repo)
2. Shell is reloaded (`source ~/.config/zsh/ai/base.zsh` or new terminal)

Until then, `temple-project-root <project>` exits non-zero. Flag this to the operator.

---

## 7. Devenv transport wiring

**Files:** `~/.config/zsh/ai/devenv.zsh` + `~/.config/zsh/ai/keyboard.zsh` PARTITION 11

⚠ **Read both files fresh before editing.** Dispatch to @Delta or @Trajectory — these are
machine-layer files requiring fresh-read-first, correct engine placement, and `zsh -n`
syntax verification after any change.

**7a. devenv.zsh** — add per-project entry points.
Derive a 2–4 char prefix from the project slug (e.g. `fr` = freya, `bo` = fantasyobchod,
`ps` = psdvsSys). Match the existing `_fr_*` / `_bo_*` pattern exactly:

```zsh
# <project> devenv transport
_<prefix>_sync()   { _devenv_sync   "<abs-path-to-devenv>"; }
_<prefix>_deploy() { _devenv_deploy "<abs-path-to-devenv>"; }
_<prefix>_status() { _devenv_status "<abs-path-to-devenv>"; }
```

**7b. keyboard.zsh PARTITION 11** — add aliases (control-panel rule: aliases only, no bodies):
```zsh
alias <prefix>-sync="_<prefix>_sync"
alias <prefix>-deploy="_<prefix>_deploy"
alias <prefix>-status="_<prefix>_status"
```

Update the `devenv-help` body in PARTITION 11 to include the new project line.

**🔴 Same ia-sync + shell reload gate applies** — new aliases not available across machines
until ia-sync runs.

---

## 8. TCR tree-snapshot config (optional)

`~/.config/zsh/registries/tcr/tcr.<project>.json`

Ask: *"Add a custom tree-snapshot config? (yes / skip — falls back to tcr.default.json)"*

Default is fine for most projects. Add a custom config only if the project has unusual
depth, extra vendor/build folders, or a different output format needed.

If yes, read `tcr.default.json` and adapt:
```json
{
  "depth": 4,
  "output": "json",
  "gitignore": true,
  "exclude": ["vendor", "node_modules", "<project-specific-folder>"]
}
```

---

## 9. Shell commands block

Emit this block to the operator — do NOT execute. Operator runs it, or delegates to
@Trajectory / @Delta.

```bash
# === <project> — bootstrap shell commands ===
# Run in order. Each step depends on the previous.

# 0. Scope-group (skip if it already exists)
mkdir -p ~/www/<scope-group>/

# 1. App repo
cd ~/www/<scope-group>/<project>
git init --initial-branch=core
gh repo create <project> --<private|public> --source=. --remote=origin
git add -A
git commit -m "bootstrap: harness scaffold (Phase 0)"
git push -u origin core

# 2. Devenv repo
cd ~/www/<scope-group>/<project>.devenv
git init --initial-branch=core
gh repo create <project>.devenv --private --source=. --remote=origin
git add -A
git commit -m "bootstrap: devenv scaffold"
git push -u origin core

# 3. Machine layer activation (after ia-sync + machine-layer edits from steps 6-7)
ia-sync
source ~/.config/zsh/ai/base.zsh        # or open a new terminal
temple-project-root <project>           # smoke test — should resolve the path

# 4. First devenv sync (after machine layer is live)
# Run /devenv-sync first to verify registry.json + pre-flight state
# Then the keyboard alias: <prefix>-sync
# Or direct: bash ~/www/<scope-group>/<project>.devenv/sync.sh
#   (pull manually first when calling bash directly — see /devenv-sync for the rule)
```

---

## 10. Post-bootstrap checklist

Surface after the shell commands block:

```
✅ App harness scaffolded:    ~/www/<scope-group>/<project>/
✅ Devenv scaffolded:         ~/www/<scope-group>/<project>.devenv/
✅ Registry beacon:           reposoma/registry/<project>.md
✅ Registry index:            row added to registry/index.md
✅ Machine map entry written: temple-project-map.zsh

⏳ ia-sync + shell reload     → machine-layer wiring live after this
⏳ Git repos:                 step 1–2 shell commands
⏳ First devenv sync:         /devenv-sync → <prefix>-sync

Optional / later:
□ TCR config    tcr.<project>.json (if custom tree-snapshot needed)
□ Sibling edges if known — update counterpart beacons + registry/index.md sibling-graph
□ Project card  /project-regular-self-report <project> (after first real work session)
             → Phase 2 (new card): fills A–G intake mounting points from
               raw.guides/project-intake.md. If a raw.guides/intake/<project>.intake.md
               exists (pre-filled founding record), the skill reads it automatically.
             → once written, harness-stale catches it when half_life_days: 30 expires.
□ Phase 1 gate  /project-read <project> → @Houston for phase design
```

---

## Rules

- Do not write any file until step 1 (intake) is complete and confirmed.
- Confirm before writing each layer (steps 3–8 separately). Never bulk-write all layers.
- Machine-layer edits (steps 6–7) require a **fresh read from disk** before writing.
  Dispatch to @Delta or @Trajectory. Do not write from held session memory.
- Steps 6–7 (devenv.zsh + keyboard.zsh) must pass `zsh -n` syntax check after edit.
- Shell commands (step 9) are emitted, never executed.
- Do NOT create files under `registry/projects/` — beacon format only (step 5).
- `toAll/` is the only `_mail/` folder seeded at bootstrap. Other seat folders on-demand.
- Scope-group missing = stop-item (step 2). Do not proceed without one.
- Canon wins on any doubt: `raw.canon/canon.project-topology.md`.
