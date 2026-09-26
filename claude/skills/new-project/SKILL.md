---
name: new-project
description: >
  Invoke as /new-project <name>. Bootstrap a new temple project — DEFAULT shape is a
  flat single repo (code + harness together); the sync/deploy twin (app repo +
  <project>.devenv sibling) is built only by exception, gated on a canon-listed reason.
  Walks the topology canon checklist: scope-group MANDATE · harness scaffold ·
  registry beacon + index row · machine-layer wiring (registries/projects.json) ·
  shell commands block. Confirms before writing each layer. Emits shell commands
  (git init · gh repo create) — never executes them. Use after the project name and
  scope-group are decided.
  Spine: raw.canon/canon.project-topology.md (gaveled 2026-07-14 · amended 2026-09-02:
  flat is the default, twin is the exception).
---

I am the `/new-project` skill — the bootstrap procedure for a new temple project.
I walk the topology canon checklist in order, confirm before writing each layer, and
emit the shell commands block at the end. I do not execute shell commands.

**Default shape:** flat single repo — code and harness live in one git home, tracked
together. Cross-host = `git pull` / `git push`. No transport scripts, no sibling repo.

**Exception (rare):** the sync/deploy twin — `<project>/` (app) + `<project>.devenv/`
(harness transport) — earned ONLY by (1) foreign human writers needing the harness
versioned apart from the code, or (2) the authoring surface not being the live deploy
tree. Number of hosts is explicitly NOT a reason — git solves hosts. See the Appendix
at the end of this skill if a twin is genuinely justified.

**Spine:** `raw.canon/canon.project-topology.md` (gaveled 2026-07-14 · amended
2026-09-02 — flat default, twin by exception)
**Shape template:** `reposoma/raw.guides/project-topology/flat.md`
**Registry template:** `reposoma/registry/_beacon.template.md`
**After bootstrap:** `/project-read <project>` · `/project-regular-self-report`

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
4. **Purpose** — one-sentence description (goes into beacon + AGENTS.md + PROJECT.yaml)
5. **Stack** — `<framework · version · language · key deps>` — or `open` if undecided at bootstrap
6. **GitHub visibility** — `private` | `public`

Do not write anything until all six are confirmed.

---

## 2. MANDATE check — scope-group

> "A bootstrap without a scope-group is a **stop-item**, not a style preference."
> — `canon.project-topology.md`

The project lives at:
```
~/www/<scope-group>/<project>/
```

If the scope-group does not exist yet: include `mkdir -p ~/www/<scope-group>/` as step 0
in the shell commands block (step 7). Never skip the group folder — the 2026-07-14
applications-in-common relocation (8 pointer rewires, one full executor run) is the
canonical cost receipt.

---

## 3. Harness scaffold (flat — default)

Show the full file list below, confirm once, then write all.

**Files to create inside `~/www/<scope-group>/<project>/`:**

```
AGENTS.md
CLAUDE.md
GEMINI.md
.gitignore
.dev/PROJECT.yaml
.dev/flag.md
.dev/pulse.md
.dev/dev.journal.json
.dev/_mail/toAll/inbox/.gitkeep
.dev/_mail/toAll/archive/.gitkeep
.claude/rules/00-discipline.md
.claude/agents/.gitkeep
.claude/skills/.gitkeep
```

Exactly the file set a twin would hold split across `<project>.devenv/claude/` +
`dev/` — the same files, just at home, all **tracked in the same git repo as the code**.

**Mail seats:** seed `toAll/` only (inbox + archive). Other seat folders (`atlas/`,
`epoch/`, etc.) are created on-demand when the first mail to that seat is actually
sent. Do not pre-create them.

**Reference bed:** `~/www/kuklana/jar-kuba/` is a correct flat bed cut by this
procedure — read it if any template below is ambiguous.

---

### AGENTS.md

```markdown
# <project> — lighthouse

<one-line purpose>

## Repo shape
Flat single repo (`raw.guides/project-topology/flat.md`). Harness + code in one git
home; cross-host = `git pull --rebase` / `git push` on `core`. Parallel or risky work:
`git worktree add ../<project>-<topic> -b dev/<topic>` — never a second clone.

## The loop

read harness (AGENTS.md → flag → pulse → PROJECT.yaml) → find next gate →
design as handoff → challenge before lock → record durably → keep pulse current

## Hard rules

- Canon is gaveled by @majkee. Draft; he gavels; then it locks and we hold the line.
- Flag.md locks are invariants — no seat crosses them without a gavel.
- Read this project's harness fresh each session. Never carry memory from another project.
- Harness (`.dev/` · `.claude/`) is tracked in this repo, not gitignored — this is a
  flat bed, not a devenv twin.

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

### GEMINI.md

```markdown
@AGENTS.md
```

---

### .gitignore — hygiene only

```gitignore
# Temple harness is TRACKED in a flat repo — never ignore .dev/ or .claude/

# secrets — never
.env
.env.*
*.key
*.pem
*.credentials

# noise
*.log
*.bak
*.bak-*
*.tmp
.DS_Store

# runtime / build artefacts — per project
# target/  node_modules/  vendor/  <pin stores>  <media drop-places>

# Claude Code personal (untracked by convention)
.claude/settings.local.json
```

Add project-specific build-artefact ignores under the last comment block. If you find
yourself adding `.dev/*` or `.claude/` to this file, you are rebuilding the twin by
hand — stop and read `raw.guides/project-topology/flat.md` and the Appendix below.

---

### .dev/PROJECT.yaml

```yaml
project: <project>
purpose: >
  <one-sentence purpose>
stack: <framework · language · key deps — or "open">
host: <office|home|both>
harness:
  shape: flat            # one repo; harness tracked in place; cross-host = git pull
  authoring: project
branch: core
mcp: none
agents: []          # added per-session as Foreman rule permits
skills: []
```

No `devenv:` transport block in the default (flat) shape — there is nothing to
transport, the repo itself is the transport.

---

### .dev/flag.md

```markdown
# <project> — flag (locked decisions)

Newest lock on top. Locks are invariants — no seat crosses without a gavel (@majkee).

## L1 — Stack

<framework · version · language · key deps — or "open: decided per experiment">

## L2 — Branch model

Single branch: `core`. Direct commits; no PRs for solo work.

## L3 — Repo shape

Flat single repo — harness (`.dev/` · `.claude/`) tracked in place, not gitignored.
Cross-host = `git pull` / `git push`. See `raw.guides/project-topology/flat.md`.

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

Flat bed scaffolded (harness tracked in place).

**Pending:**
- `git init` (branch `core`) + first commit + `gh repo create` — see the emitted shell block.
- `registries/projects.json` entry (ia-sync table) via @Delta — activates after commit +
  `deploy.sh` + shell reload.
- Gate Phase 1 goal with @Houston
```

---

### .dev/dev.journal.json

```json
[
  {
    "date": "<YYYY-MM-DD>",
    "phase": "0",
    "event": "bootstrap",
    "note": "Flat bed scaffolded. Harness tracked in place, one repo with the code. Phase 1 pending gate."
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
- Machine layer edits (zsh, base.zsh, registries/*.json): dispatch to @Delta with fresh-read-first.
```

---

## 4. Registry — beacon + index row

**4a. Create beacon** `reposoma/registry/<project>.md`.
Read `reposoma/registry/_beacon.template.md` for the exact frontmatter schema, then fill:

```yaml
---
beacon: <project>
path: /home/hruzam/www/<scope-group>/<project>
repo: github.com/hruzam/<project> — <visibility>, branch core, flat (harness tracked in repo)
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

**4b. Add row to `reposoma/registry/index.md`** under `## Projects`:
```
| <project> | <office|home|both> | bootstrap | [`registry/<project>.md`](<project>.md) | `AGENTS.md` · `.dev/PROJECT.yaml` · `.dev/flag.md` |
```

Do NOT create a file under `registry/projects/` — that format is retiring. Beacon only.

If siblings are known at bootstrap: add them to `sibling-of:` in the beacon frontmatter
AND add a row to the `## Sibling-graph` section of `registry/index.md`. Also update
the counterpart beacons to point back.

---

## 5. Machine layer — registries/projects.json

**File:** `~/ia-sync/zsh/registries/projects.json` — the **table** copy; the AUTHORITATIVE
source for physical repo-root paths (decision 0008/0004, amended 2026-08-15).
`deploy.sh` rsyncs `~/ia-sync/zsh/` → `~/.config/zsh/` — an edit made only to the live
`~/.config/zsh/registries/projects.json` is **silently erased** on the next deploy
(2026-09-26 near-miss, pajdulium bootstrap). Edit the table; deploy makes it live.
Optional: mirror the same edit to live for immediate use, then `diff` both → identical.

⚠ **Fresh-read rule (standing warning):** read the file from disk before editing —
never act from held session memory. The file is touched by multiple sessions.
If Bash is available: spawn @Delta with the exact edit below.

**Add one entry** under `"projects"`:
```json
"<project>": "/home/hruzam/www/<scope-group>/<project>"
```

**Never hand-edit** `~/.config/zsh/ai/temple-project-map.zsh`. Its
`TEMPLE_PROJECT_MAP` array is **GENERATED** from `registries/projects.json` by
`registries/gen-temple-map.sh`, which `deploy.sh` runs before the zsh rsync — a
hand-edit to the generated array is silently overwritten on the next deploy. Edit the
JSON, never the generated file.

**🔴 Activation gate:** this entry is not live until:
1. Commit + push `zsh/registries/projects.json` in `~/ia-sync` (stage that file only —
   the table often holds other sessions' uncommitted work).
2. `bash ~/ia-sync/deploy.sh -n` → review → `bash ~/ia-sync/deploy.sh`
   (runs `gen-temple-map.sh`, then rsyncs to live). Other host: `git pull` + `deploy.sh`.
3. Shell is reloaded (`source ~/.config/zsh/ai/base.zsh` or new terminal)

Until then, `temple-project-root <project>` exits non-zero. Flag this to the operator.

---

## 6. TCR tree-snapshot config (optional)

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

## 7. Shell commands block

Emit this block to the operator — do NOT execute. Operator runs it, or delegates to
@Trajectory / @Delta.

```bash
# === <project> — bootstrap shell commands ===
# Run in order. Each step depends on the previous.

# 0. Scope-group (skip if it already exists)
mkdir -p ~/www/<scope-group>/

# 1. Repo (flat — harness + code together, one git home)
cd ~/www/<scope-group>/<project>
git init --initial-branch=core
git add -A
git commit -m "bootstrap: flat harness scaffold (Phase 0)"
gh repo create <project> --<private|public> --source=. --remote=origin
git push -u origin core
# Local-only for now? Defer the `gh repo create` + push lines until ready to host
# remotely — the local repo is already valid without a remote.

# 2. Machine layer activation (after the step-5 edit on the ia-sync table)
cd ~/ia-sync
git add zsh/registries/projects.json    # this file only
git commit -m "project map: + <project>"
git push
bash ~/ia-sync/deploy.sh -n             # dry run — review the list
bash ~/ia-sync/deploy.sh
source ~/.config/zsh/ai/base.zsh        # or open a new terminal
temple-project-root <project>           # smoke test — should resolve the path
```

---

## 8. Post-bootstrap checklist

Surface after the shell commands block:

```
✅ Harness scaffolded (flat): ~/www/<scope-group>/<project>/
✅ Registry beacon:           reposoma/registry/<project>.md
✅ Registry index:            row added to registry/index.md
✅ Machine map entry written: ~/ia-sync/zsh/registries/projects.json (table)
                               (regenerates temple-project-map.zsh on next deploy —
                                never hand-edit the generated file)

⏳ ia-sync commit + deploy.sh + shell reload → machine-layer wiring live after this
⏳ Git repo:                  step 1 shell commands (git init / commit / gh repo create)

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
- Confirm before writing each layer (steps 3–6 separately). Never bulk-write all layers.
- Machine-layer edits (step 5) require a **fresh read from disk** before writing.
  Dispatch to @Delta. Do not write from held session memory. Edit
  `~/ia-sync/zsh/registries/projects.json` only — never the live-only copy, never the
  generated `temple-project-map.zsh`.
- Shell commands (step 7) are emitted, never executed.
- Do NOT create files under `registry/projects/` — beacon format only (step 4).
- `toAll/` is the only `_mail/` folder seeded at bootstrap. Other seat folders on-demand.
- Scope-group missing = stop-item (step 2). Do not proceed without one.
- Flat is the default shape. Do NOT build the twin (devenv sibling) unless one of the
  two canon-listed reasons in the Appendix applies — and say so out loud before doing it.
- Canon wins on any doubt: `raw.canon/canon.project-topology.md`.

---

## Appendix — Exception: twin (Shape A), only if canon-justified

Canon default (amended 2026-09-02) is flat. Build the sync/deploy twin — `<project>/`
(app repo) + `<project>.devenv/` (harness git-home + transport) — **only** when one of
these is true, and say which one to the operator before proceeding:

1. **Foreign human writers** need the harness versioned apart from the code.
2. **Authoring surface ≠ live deploy tree** — the place you author is not the place
   that runs.

Number of hosts is explicitly **not** a reason — git solves hosts.

If justified, the harness scaffold in step 3 changes shape: `.gitignore` ignores
`.dev/` and `.claude/` instead of tracking them (the app repo never carries the
harness), `PROJECT.yaml` carries a `devenv:` transport block instead of
`harness: {shape: flat}`, and AGENTS.md's "Repo shape" paragraph is replaced with a
"Harness transport" paragraph naming the devenv sibling. Then run the two steps below
in addition to (not instead of) step 3's code-side files.

### Devenv scaffold

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
substitute the project name, adapt W3 paths. (Note: `applications-in-common.devenv`
was itself retired to flat on 2026-09-02 — read it as a historical reference only.)

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

**App-side `.gitignore` (twin variant — differs from step 3's hygiene-only default):**
```gitignore
# Temple harness — gitignored; transported via <project>.devenv/
AGENTS.md
CLAUDE.md
.dev/
.claude/
.mcp.json
```
Add project-specific ignores below (e.g. `.env`, `vendor/`, `node_modules/`).

**App-side `PROJECT.yaml` devenv block (replaces the flat `harness:` block):**
```yaml
devenv:
  transport_path: ~/www/<scope-group>/<project>.devenv
  branch: core
  sync_discipline: SYNC_DISCIPLINE.md
```

### Devenv transport wiring

**Files:** `~/.config/zsh/ai/devenv.zsh` + `~/.config/zsh/ai/keyboard.zsh` PARTITION 11

⚠ **Read both files fresh before editing.** Dispatch to @Delta or @Trajectory — these are
machine-layer files requiring fresh-read-first, correct engine placement, and `zsh -n`
syntax verification after any change.

**Devenv.zsh** — add per-project entry points.
Derive a 2–4 char prefix from the project slug (e.g. `fr` = freya, `bo` = fantasyobchod,
`ps` = psdvsSys). Match the existing `_fr_*` / `_bo_*` pattern exactly:

```zsh
# <project> devenv transport
_<prefix>_sync()   { _devenv_sync   "<abs-path-to-devenv>"; }
_<prefix>_deploy() { _devenv_deploy "<abs-path-to-devenv>"; }
_<prefix>_status() { _devenv_status "<abs-path-to-devenv>"; }
```

**keyboard.zsh PARTITION 11** — add aliases (control-panel rule: aliases only, no bodies):
```zsh
alias <prefix>-sync="_<prefix>_sync"
alias <prefix>-deploy="_<prefix>_deploy"
alias <prefix>-status="_<prefix>_status"
```

Update the `devenv-help` body in PARTITION 11 to include the new project line.

**🔴 Same activation gate applies** — new aliases not available across machines until
the ia-sync commit + `deploy.sh` (both hosts) + shell reload.

### Twin shell commands (in place of the default step 7)

```bash
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

# 3. Machine layer activation (after the table edits: projects.json + devenv wiring)
cd ~/ia-sync
git add zsh/registries/projects.json <devenv wiring files>   # these files only
git commit -m "project map + devenv wiring: <project>"
git push
bash ~/ia-sync/deploy.sh -n && bash ~/ia-sync/deploy.sh
source ~/.config/zsh/ai/base.zsh
temple-project-root <project>

# 4. First devenv sync (after machine layer is live)
# Then the keyboard alias: <prefix>-sync
# Or direct: bash ~/www/<scope-group>/<project>.devenv/sync.sh
#   (pull manually first when calling bash directly)
```

**Twin registry beacon `repo:` line:**
```
repo: github.com/hruzam/<project> (app) · github.com/hruzam/<project>.devenv (harness) — both <visibility>, branch core
```
