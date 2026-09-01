# Guide: Adding a New Gemini Agent Seat

> **⚕ Cut on the surgical table.** This file is deployed from `~/ia-sync` (the surgical
> table — the like-composer syncing both machines). Do not edit it in place: cut in
> ia-sync, deploy outward. Before trusting any machine fact here, reality-check the sync
> part: `git -C ~/ia-sync log --oneline -5 -- zsh/guides/guide-for-builder.md` (intent) **and** repo↔live
> `rsync -n` (reality). Commits say what *should* be deployed; only the diff says what *is*.

`~/.config/zsh/guides/guide-for-builder.md`

> **⚠ SCOPE SHRUNK 2026-07-31.** The Gemini line is PARKED (2026-07-24 wall) and the
> **Vega + Astrobley chairs vendor-shifted to Codex** (0005 A1 + transition 2026-07-31) —
> their launchers/personas are archived in reposoma `raw.substrate/archive/`. This guide
> now governs only the surviving ears-and-eyes seats (**Orby · BlueBottle**) and future
> Gemini multimedia seats. For the Codex relay family (@Vega · @Astrobley · @Mirror) the
> authority is `zsh/guides/codex-relay.contract.md` — point there, do not extend this
> guide with Codex wiring.

---

## How to add a new agent seat

### 1. Create the agent definition file

Path: `~/.gemini/agents/<name>.md`

Minimum frontmatter:
```yaml
---
name: <name>
description: "One-line description used for agent routing decisions"
model: gemini-2.5-flash   # or gemini-2.5-pro / gemini-3.5-flash per seat role
temperature: 0.7           # range 0.0–2.0; default 1
---
Your agent system prompt begins here...
```

Model guidance (per handoff 2026-07-03):
- `gemini-2.5-pro`   — thinking/advisor seats (accept auto-switch risk under load)
- `gemini-2.5-flash` — researcher/recalibrator seats (most stable; recommended for headless)
- `gemini-3.5-flash` — implementer seats (GA since 2026-05-19; superior agentic benchmarks)
- Do NOT use `gemini-3.1-pro-preview` — documented hang/loop failures (tracked p1)

### 2. Create the launcher script

Path: `~/.config/zsh/ai/<name>.sh`

Shebang: `#!/usr/bin/env bash`  
Pattern: dual-mode — no-arg = interactive, arg = headless (`-p` flag per handoff Q1).  
Sources: `gemini-processor.sh` for `_gai_*` REST helpers.

Minimal template:
```bash
#!/usr/bin/env bash
# <name>.sh — <Seat name> launcher (interactive + headless)
# Model: <model> | Role: <role>

_MODEL="<model>"
_SEAT="<name>"

source ~/.config/zsh/ai/gemini-processor.sh 2>/dev/null || true

if [[ $# -eq 0 ]]; then
  echo "[${_SEAT}] Interactive | ${_MODEL} → switch seat: /agents"
  GEMINI_MODEL="${_MODEL}" gemini
else
  echo "[${_SEAT}] Headless | ${_MODEL} | @${_SEAT}"
  GEMINI_MODEL="${_MODEL}" gemini -p "@${_SEAT} $*"
fi
```

Make it executable:
```bash
chmod +x ~/.config/zsh/ai/<name>.sh
```

### 3. Wire into keyboard.zsh

Add kebab shims in **PARTITION 3** of `~/.config/zsh/ai/keyboard.zsh`:
```zsh
alias gemini-<name>="~/.config/zsh/ai/<name>.sh"
alias g-<name>="~/.config/zsh/ai/<name>.sh"
```

Update `gemini-agents-help()` in `ai/gemini-processor.sh` (interactive surface section; exposed as-is — no alias needed since functions are directly callable) to include the new seat.

### 4. Update AGENTS.md

Add a row to the file map in `~/.config/zsh/AGENTS.md` (temple transport family section).

### 5. Update ai/README.md

Add a row to the File map table in `~/.config/zsh/ai/README.md`.

### 6. Run stress test

```bash
bash ~/.config/zsh/ai/<name>.sh "test probe"
```

Expected: headless response printed to stdout, exit 0.

---

## How to add a new project devenv transport

When a new temple project pair (`<project>/` + `<project>.devenv/`) is bootstrapped, its
devenv transport commands must be wired into the machine layer. This is a **separate step
from the devenv scaffold** — it adds the keyboard aliases and engine entry points that make
`<proj>-sync / <proj>-deploy / <proj>-status` work in the shell.

**Read both files fresh from disk before editing.** The standing fresh-read rule applies.
Dispatch edits to @Delta or @Trajectory; verify with `zsh -n` after each file.

### 1. Add entry points to `ai/devenv.zsh`

Pick a 2–4 char prefix from the project slug (e.g. `fr` = freya, `bo` = fantasyobchod,
`ps` = psdvsSys). Match the existing `_fr_*` / `_bo_*` pattern exactly.

Place the new block in `ai/devenv.zsh` next to the existing per-project sections:

```zsh
# <project> devenv transport
_<prefix>_sync()   { _devenv_sync   "<absolute-path-to-devenv>"; }
_<prefix>_deploy() { _devenv_deploy "<absolute-path-to-devenv>"; }
_<prefix>_status() { _devenv_status "<absolute-path-to-devenv>"; }
```

The absolute path is the devenv repo root, e.g.:
`/home/hruzam/www/<scope-group>/<project>.devenv`

### 2. Add aliases to `keyboard.zsh` PARTITION 11

Control-panel rule: aliases only, no function bodies. Add in P11 next to existing devenv aliases:

```zsh
alias <prefix>-sync="_<prefix>_sync"
alias <prefix>-deploy="_<prefix>_deploy"
alias <prefix>-status="_<prefix>_status"
```

Also update the `devenv-help` body (in `devenv.zsh`) to include the new project line.

### 3. Activation gate — ia-sync required

The new aliases are NOT available until:
1. `ia-sync` is run (propagates `devenv.zsh` + `keyboard.zsh` to the devenv repo)
2. Shell is reloaded (`source ~/.config/zsh/ai/base.zsh` or new terminal)

Until then the aliases resolve to "command not found". This is expected — flag it to the operator.

### 4. Add entry to `temple-project-map.zsh`

At the same time, add the project's physical path to P0 (same ia-sync gate):

```zsh
[<project>]="/home/hruzam/www/<scope-group>/<project>"
```

Update the `# mapped:` sync comment at the top of the file.

### Checklist

- [ ] `ai/devenv.zsh`: `_<prefix>_sync/deploy/status()` entry points added
- [ ] `ai/devenv.zsh`: `devenv-help` body updated to list the new project
- [ ] `keyboard.zsh` P11: three aliases added (`<prefix>-sync`, `<prefix>-deploy`, `<prefix>-status`)
- [ ] `temple-project-map.zsh`: `[<project>]="<path>"` entry + sync comment updated
- [ ] `zsh -n ai/devenv.zsh` — syntax clean
- [ ] `zsh -n ai/keyboard.zsh` — syntax clean
- [ ] `ia-sync` run → shell reload → smoke test: `<prefix>-status`

> Full bootstrap procedure for a new project pair: `/new-project` skill
> (`~/.claude/skills/new-project/SKILL.md`).

---

## Persona files (patch-protocol mode)

Persona files are plain text system instructions, operator-tunable without touching the script.

Location: `~/.config/zsh/ai/personas/<seat>-<mode>.md`

Active personas:
| File | Used by | Purpose |
|---|---|---|
| `personas/astrobley-patch.md` | `astrobley.sh --patch` | PHP implementer — diff-only output contract — RETIRED 2026-07-31 |

> NOTE (2026-09-01): astrobley.sh retired 2026-07-31 (Codex vendor-shift); the persona mechanics below are historical.

**How to tune:**
- Edit `personas/astrobley-patch.md` directly — plain text, no frontmatter, no special format.
- The OUTPUT CONTRACT section is load-bearing (diff-only or `QUESTION:` — no prose).
  Change the language/framework description above it freely; do not remove the contract.
- Language-specific versions: create `personas/astrobley-patch-<language>.md` and point the
  caller at it. The persona file path is `_PERSONA_FILE` in the `--patch` branch of `astrobley.sh`.

## CHECKLIST

- [ ] `~/.gemini/agents/<name>.md` created (frontmatter: name, description, model, temperature)
- [ ] `~/.config/zsh/ai/<name>.sh` created and executable (`chmod +x`)
- [ ] `keyboard.zsh` PARTITION 3: kebab shims added (`gemini-<name>`, `g-<name>`)
- [ ] `ai/gemini-processor.sh`: `gemini-agents-help()` updated (interactive surface section)
- [ ] `~/.config/zsh/AGENTS.md` file map row added
- [ ] `~/.config/zsh/ai/README.md` file map row added
- [ ] `ia-sync`: run sync.sh after all changes

---

## Architecture rules (gaveled 2026-07-11)

### Control-panel convention

`keyboard.zsh` is the control panel. It contains **aliases and comments only — no function bodies.**
Function bodies belong in scope-named engines, sourced by `base.zsh`. The pattern:

```
base.zsh                signpost — sources everything
  keyboard.zsh          control panel — aliases only
  gemini-processor.sh   Gemini scope engine — dual-sourced (subprocess core + interactive surface)
  claude.zsh            Claude RC engine (_rc_stop, _temple_help, _ai_help)
  devenv.zsh            devenv transport engine (_bo_*, _fr_*, _devenv_help)
```

When adding a new body to the Gemini interactive surface, put it in `gemini-processor.sh`
(interactive surface section, clearly marked).
When adding a new body to the Claude/RC surface, put it in `claude.zsh`.
When adding an entirely new scope, create a new `<scope>.zsh` engine and wire it in `base.zsh`.

### Processor scope-naming rule

Processor files (shared REST/helper libraries) carry the scope prefix: `gemini-processor.sh` not `processor.sh`.
Example: if a second processor family were added for a different line, it would be `<scope>-processor.sh`.
Per-agent scripts source by `SCRIPT_DIR` so the rename is self-contained within the scope.

### .sh vs .zsh rule

One file per scope. When a scope's function bodies serve **both** the interactive shell and bash
subprocesses, the scope file is a single dual-sourced `.sh` (shebang `#!/usr/bin/env bash`).
`gemini-processor.sh` is the exemplar: sourced by bash launchers (subprocess core) and sourced
by `base.zsh` P8 (interactive surface). All bodies must be bash/zsh compatible — no zsh-specific
syntax in dual-sourced files.

- **`.zsh`** — pure interactive-only engines: sourced only into the zsh interactive shell;
  may use zsh-specific syntax. `claude.zsh`, `devenv.zsh` are current examples. All `.zsh`
  entries in `base.zsh` partitions follow this rule.
- **`.sh`** — either executed as a standalone bash subprocess (per-agent launchers), OR
  dual-sourced across bash and zsh (scope engines like `gemini-processor.sh`). Shebang is
  `#!/usr/bin/env bash`. Must be bash/POSIX compatible throughout.

Ambiguous case: a script that uses zsh syntax but is only ever executed (never sourced) → `.zsh`
(zsh shebang, zsh semantics). A script that is bash-compatible and intended for non-zsh contexts
or dual-sourcing → `.sh`.

### Partition map — base.zsh (as of 2026-07-11)

| Partition | Content |
|---|---|
| P1 | `keyboard.zsh` — control panel |
| P2 | `harness-stale` alias (inline) |
| P3 | Temple transport family (`temple-project-map.zsh`, `temple-mail.zsh`, `temple-doorbell.zsh`, `temple-mail-inbox.zsh`, `temple-mail-switch.zsh`) |
| P4 | `adr-guard` alias (inline) |
| P5 | `temple-tree.zsh` — tree-snapshot engine |
| P6 | `devenv.zsh` — devenv transport engine |
| P7 | `claude.zsh` — Claude RC engine + help functions |
| P8 | `gemini-processor.sh` — Gemini scope engine (dual-sourced: subprocess core + interactive surface) |
| P9 | `keys.zsh` — global claviature engine (derived keys panel) |

### Partition map — keyboard.zsh (as of 2026-07-11)

| Partition | Content | Bodies in |
|---|---|---|
| P1 | General CLI aliases (`g`, `g-ver`, `g-help`, `agy-ver`, `agy-help`) | — |
| P2 | Safety/YOLO aliases (`g-yolo`, `g-skip`, `agy-yolo`, `agy-skip`) | — |
| P3 | Kebab shims → per-agent `.sh` scripts | — |
| P4 | `agy-*` wrappers alias `agy-astrobley` only; bodies in `gemini-processor.sh` | `gemini-processor.sh` |
| P5 | Retired 2026-07-11 (Gemini Epoch seat killed) | — |
| P6 | Hygiene comment; bodies in `gemini-processor.sh` | `gemini-processor.sh` |
| P7 | `alias ai-help='_ai_help'`; Gemini help body in `gemini-processor.sh`, top-level help body in `claude.zsh` | `gemini-processor.sh`, `claude.zsh` |
| P8 | Claude Code RC aliases (`rc-status`, `rc-freya`, `rc-reposoma`, `rc-nabla`, `rc-stop`) | `claude.zsh` |
| P9 | Temple transport panel aliases | `temple-*.zsh` |
| P10 | Temple utilities (`temple-help` alias); body in `claude.zsh` | `claude.zsh` |
| P11 | devenv transport aliases (`fr-*`, `bo-*`, `devenv-help`) | `devenv.zsh` |
| P12 | `alias keys='_keys'` — global derived panel | `keys.zsh` |
| P13 | `alias octo='_octo'` — Octopus head launcher (drops into the session head — Medusa in project seats) | `claude.zsh` |

*Claude-agent launcher recipe (P13 / `octo` is the first): `_<name>` body in `claude.zsh` →
`alias <name>='_<name>'` in a new keyboard.zsh partition → register the bare name in
`keys.zsh` `_KEYS_SINGLES_MAP`. Docs-only edits (no zsh syntax) may skip the `zsh -n` gate.*

### Engine inventory (updated 2026-07-15)

| Engine | Sourced by | Bodies |
|---|---|---|
| `ai/gemini-processor.sh` | `base.zsh` P8 (interactive surface) + per-agent launchers (subprocess core) | `_gai_api_key`, `_gai_payload`, `_gai_rest_call`, `_gai_extract`, `_gai_strip_noise`, `agy-vega`, `agy-orby`, `agy-astro`, `agy-astro-yolo`, `gemini-fresh`, `agy-fresh`, `gemini-agents-help` |
| `ai/claude.zsh` | `base.zsh` P7 | `_rc_stop`, `_temple_help`, `_ai_help`, `_octo` |
| `ai/devenv.zsh` | `base.zsh` P6 | `_devenv_sync`, `_devenv_deploy`, `_devenv_status`, `_bo_*`, `_fr_*`, `_devenv_help` |
| `ai/devenv-sync-core.sh` | `*.devenv/sync.sh` + `*.devenv/deploy.sh` (external, not base.zsh) | `_devenv_resolve_app_dir`, `_devenv_sync_deny_init`, `_devenv_sync_deny_cleanup`, `_devenv_secret_scan`, `_devenv_print_footer`, `_devenv_deploy_guard`, `_devenv_git_exclude_guard`, `_devenv_print_deploy_footer` |
| `ai/temple-tree.zsh` | `base.zsh` P5 | `tree-snapshot` |
| `ai/temple-*.zsh` | `base.zsh` P3 | temple mail/doorbell family |
| `ai/keys.zsh` | `base.zsh` P9 | `_keys` |

---

## Maintenance log

### 2026-07-15 — devenv-sync-core.sh added (office)

New shared function library `ai/devenv-sync-core.sh` created. Sourced by
`*.devenv/sync.sh` and `*.devenv/deploy.sh` across all project devenv repos.
Replaces copy-pasted APP_DIR resolution, sync.deny handling, secret scan, and
deploy-guard logic that was previously duplicated in each project script.

Full record: `/home/hruzam/reposoma/maintenance/sync_deploy/devenv-dry-refactor.2026-07-15.md`

### 2026-07-27 — ai-install :: gemini (npm prefix + allow-scripts fix, office)

`gemini` CLI (npm package `@google/gemini-cli`) installs were silently falling back to the
system `/etc/npmrc` (`prefix=/usr`) — no `prefix` override yet existed in `~/.npmrc` — causing
`EACCES` on any `npm install -g`, including a routine version bump. Fixed by persisting
`prefix=/home/hruzam/.npm-global` in `~/.npmrc`. A second, recurring symptom — npm warning on
every install because two transitive native deps (`@github/keytar`, `node-pty`) aren't covered
by the `allow-scripts` policy — is fixed the same way: `allow-scripts=@github/keytar,node-pty`
persisted via `npm config set ... --location=user` (a one-time inline flag on the install
command does **not** persist across future installs).

Full description + command loop: `guides/guide-for-user.md` §ai-install :: gemini.

---

## Pointer

User guide (invoking agents): `~/.config/zsh/guides/guide-for-user.md`
