# AGENTS.md — ~/.config/zsh/ Lighthouse

**Truth is living THERE: `~/ia-sync` (the surgical table).** This tree is a deployed copy — cut in ia-sync, deploy outward; before trusting any fact here, reality-check against the sync part.

Operator's personal machine-layer shell config. Agents read this for host/resource facts.
Do NOT bind its absolute paths into any project's consumer surface (doctrine §4.7).

---

## Contract this folder exposes

**Host identity**
- Variable: `$MACHINE_NAME`
- Source: `config.zsh` (sets `export MACHINE_NAME="office"` on this machine)
- Usage: `echo $MACHINE_NAME` — available in every interactive shell; no sourcing needed beyond what .zshrc already does
- Stamp a repo marker: `echo $MACHINE_NAME > /path/to/repo/.host`


---

## Control-panel convention (canonical — operator-gaveled 2026-07-07 · tightened 2026-07-11)

Pattern, generalized from `ai/` (the reference implementation):

- **Keyboard = control panel.** A subfolder that exposes user-facing commands has exactly ONE
  interactive-surface file (`keyboard.zsh`). **Tightened 2026-07-11 (operator gavel): aliases
  and comments ONLY — no function bodies.** Bodies live in scope-named engines
  (`<scope>.zsh` / dual-sourced `<scope>-processor.sh`) wired by the signpost.
  Full rules + partition maps: `guides/guide-for-builder.md` §Architecture rules (**LAW** —
  pattern-read before writing).
- **Engines behind it.** The scripts that do the work are engines — executed or sourced by the
  keyboard/signpost, never aliased from elsewhere; engines carry no aliases of their own.
- **Signpost when non-interactive.** If a family must load outside interactive shells (git hooks,
  systemd), a `base.zsh` signpost wires it — idempotent, side-effect-free on source.
- **Lazy retrofit.** Binding for new or rebuilt subfolders; existing folders adopt on next touch.
  Each subfolder's README (or the map below) carries a one-line pointer to this section.
- **Keyboard grammar** (`<family>-<action>`, intent-keyed prefixes, shim class): LOCKED
  2026-07-11 — `guides/keyboard.md`. Global claviature: `guides/claviature.global.spec.md`
  (design locked, build deferred).

---

## Live-vs-parked map

### LIVE — sourced on office at every shell start

| File | Sourced by | Role |
|---|---|---|
| `config.zsh` | `.zshrc` | Machine identity, all project paths, exports (PROJECT block restored 2026-07-07 after 07-03 loss) |
| `project-switcher.zsh` | `.zshrc` | `fo / im / psd / ltp / lrv / sess` switchers, PHP helpers |
| `git-lifecycle.zsh` | `.zshrc` | `smart_commit`, phase symbols, `git_phases` |
| `projects/session.zsh` | `config.zsh` | `session_core_repomix` helper; also sources `session-meassure.zsh` |
| `session-meassure.zsh` | `projects/session.zsh` | Session measurement helpers |
| `projects/larva.zsh` | `project-switcher.zsh` on demand (`lrv`) | LARVA aliases and agent tools (startup copy archived 2026-07-07) |
| `projects/fo-toolkit.zsh` | `project-switcher.zsh` on demand | FantasyObchod commands; `fo -db` uses `.env/fo-db.cnf` |
| `projects/im-toolkit.zsh` | `project-switcher.zsh` on demand | Freya/Imago commands |
| `projects/psdvs-toolkit.zsh` | `project-switcher.zsh` on demand | PSDVS commands (needs `ENV_BACKUP_DIR`) |
| `projects/ltp-toolkit.zsh` | `project-switcher.zsh` on demand | Laravel Training Project commands |
| `krfb.zsh` | `config.zsh` | Tablet extension |
| `ai/base.zsh` | `config.zsh` | AI scope signpost (see the ai/ scope block below) |
| `nablarva/base.zsh` | `config.zsh` | nabLarva scope signpost (nab-* project verbs; keyboard + nablarva.zsh engine) |
| `experimental/base.zsh` | `config.zsh` | **experimental brick scope signpost** — sibling of ai/, promoted out of `ai/experimental/` 2026-09-22 (hiding bricks inside ai/ made orphans). Two brick kinds (LAW — see README Contract): P1 keyboard + P2 dispatcher engine → **lazy runners** (`experimental/<id>/runner.zsh`, resolved on demand via `exp-run`, cannot break shell startup); P3 → **sourced bricks** (`experimental/<id>/<id>.zsh`, explicit-name + `zsh -n`-gated wiring — e.g. `t41`, tmux session-fold). Head carries the MAINTAINER LOG (per-brick plug date · origin · approval status — experimental-only until majkee approves). Contract: `experimental/README.md` |
| `session/base.zsh` | `config.zsh` | **session scope signpost** — session-layer instruments umbrella (founded 2026-09-06, majkee gavel; rescoped out of nablarva/). P1 keyboard (`rb-*`), P2 runbook browser engine (`session/runbook.zsh` + `session/runbook.py` TUI, browses any `.dev/session/` tree; default bench = `$RB_ROOT` exported by config; `session/help/` holds the in-TUI browsable help tree, `?` key). P5 **ovitmugen** (added 2026-09-25): `session/ovitmugen.zsh` engine + `session/ovitmugen.py` (tmux manager, layout C — frame server `tmux -L ovitmugen` with its own `ovitmugen.tmux.conf`, agents stay on the default server; presets `ovitmugen.presets.json`; help scope `session/help/ovitmugen/`; aliases `ov-*` in `session/keyboard.zsh` P6; `ov-selftest` = isolated servers). Views only — never send-keys. Design: `~/unikuklatrix/nablarva/.dev/session/ovitmugen-00-console/raw/`. Reserved partitions: cold-start cards (needs temple gate on ai/base.zsh), presence dashboard (pending research) |
| `piql/piql.zsh` | `config.zsh` | PIQL integration (office only) |
| `sync/guides.zsh` | `config.zsh` | Guide-publish synchronizer |
| `archx/commands.zsh` | `config.zsh` | Arch monitoring suite |
| `system/shell.zsh` | `config.zsh` | Shell helpers |
| `system/home.php-composer.zsh` | `system/base.zsh` on home | `_php74 / _php8 / _phpst / _composer74 / _composer8` — Docker PHP 7.4 + both Composer lanes; native PHP 8+ |
| `system/office.php-switch.zsh` | `system/base.zsh` on office | Same keyboard targets with native CLI + concurrent FPM/socket routing; `$MACHINE_NAME` guard keeps it inert elsewhere |
| `.env/secrets.zsh` | `config.zsh` | API keys (GEMINI, OPENAI, etc.) |
| `.env/fo-db.cnf` | `mariadb --defaults-extra-file` via `fo -db` | Local MariaDB client credentials (mode 600; `.env` is sync.deny'd) |
| `registries/ai.json` | `ai/rc.sh`, `ai/keyboard.zsh`, `ai/harness-check.zsh` | AI runtime registry (remote-control projects etc.) |
| `registries/tcr/` | `ai/temple-tree.zsh` | per-project tree-snapshot configs (`tcr.<project>.json`; fallback `tcr.default.json`) |

Project roots on office: FO/IM under `~/www/imago_cz/`; PSD at `~/www/psdvs/psdvsSys`
(new Laravel build 2026-07-07, replaces stale `~/projects/psdvs`); LTP/LRV/SES under
`~/projects/` (`OFFICE_PROJECT_PATH` — repointed 2026-07-07; `/media/data/projects` was
an empty husk).

### RESOLVED 2026-07-29 — was UNCERTAIN; not sourced on office, live on home

The table below is closed. @zenith-zsh and @Eagle traced office's
live sourcing chain for every entry; all six are unreachable on office. Operator call: a
grep-level trace from the zsh perspective is sufficient evidence, home verification is not
required to state office's status.

**Resolution ≠ removal.** These are **home-owned files that office merely stores**. Office
never sources them, but the repo is home's delivery path, so they stay at repo top level.
Archiving them here would bury home's own files in `archive/` and degrade home's deploy for
no office benefit. That is the difference from `normalizer.py`, where *both* machines are
retiring the mechanism — there, archiving was correct.

Disposition: **office = store, never source. Home owns. Do not archive from office.**

| File | Status on office (evidence) | Owner |
|---|---|---|
| `ai-lifecycle.zsh` | ✅ **RETIRED ON BOTH MACHINES 2026-07-30** (operator call, executed from home). This row previously said "DEAD — no live source directive, only caller was `config.home.zsh:113`, archived 2026-07-29". **Both halves were false, and office-blind in the same way as `AGENTS.md:157` was:** office archived *its own* copy of `config.home.zsh` and inferred the caller was gone everywhere — but home's live `config.zsh:119` (the deployed copy of the repo's `config.home.zsh`) sourced it at every login. It provided four live functions (`autonomy-mode`, `ai-session`, `track`, `ai-agents`) plus `alias tasks`. Second false claim: "concurrency guard (home-only, **still valid there**)" — `~/.shared/` does not exist on home either; the guard has never run on either machine, so the agent-concurrency cap and nesting detection were never in force. Verified 2026-07-30: zero callers for all four functions anywhere in the tree. Retired in one pass — `zsh/archive/ai-lifecycle.zsh`, live copy removed on home, source line stripped from `zsh/config.home.zsh`. The guard artifact was recovered from `~/.remote/.shared/` and preserved at `zsh/archive/implementation.concurrency-guard.zsh`; if agent-concurrency capping is ever wanted again, operator's call is to build fresh rather than revive. | retired |
| `ai-agents.registry.json` | Already in `archive/`, unreferenced — sole consumer `ai-lifecycle.zsh:14` is dead here. | home |
| `normalizer.py` | ✅ **RESOLVED 2026-07-29 — no longer uncertain.** Traced by @Eagle + @zenith-zsh: orphaned on office (only caller was `config.home.zsh:27`, itself never sourced here). Archived to `archive/normalizer.py` on office 2026-07-29. STILL LIVE ON HOME — home's `config.zsh:27` invokes it at every login. Home archives it only after migrating to inline exports. |
| `shared-toolkit.zsh` | DEAD on office — header claims "Loaded by: ~/.zshrc", but office's `.zshrc` sources only `config.zsh`, `project-switcher.zsh`, `git-lifecycle.zsh`. **Not merely home-only — an obsolete workaround** (operator, 2026-07-29): it mirrors dot-folders to visible folders because older Claude web browsers could not see dotted paths. Current Claude Code reads dotfiles natively, so the reason it exists is gone. It is also larva-adjacent (`~/www/session`), and larva-adjacent = stale/legacy by default. Candidate for retirement on **both** machines, not just office — but see the larva note below: parked until the machines converge. | legacy — pending |
| `setup-docker.sh` | DEAD — never sourced; pure documentation, header scopes it `@home`. **Home-only as a direct consequence of the PHP/composer split** (below): Docker is home's PHP 7.4 vehicle. Office has Docker active but does not need it for PHP. | home |

### The PHP / composer machine split (verified 2026-07-29 — the root of most home-only files)

| | home | office |
|---|---|---|
| PHP 7.4 | Docker image `php74-composer`, **no native CLI** | native `/usr/bin/php74` + `php74-fpm` service |
| PHP 8 | system PHP; composer8 still Docker-wrapped | native `/usr/bin/php` + `php-fpm` service |
| composer | `composer74`/`composer8` are Docker wrappers | `composer74` = `php74 /usr/bin/composer`; `composer` native |
| web | nginx, manual/systemctl, per project | Valet-linux manages nginx, per-site sockets |
| **PHP loading** | **container invocation** at composer-call time — no FPM version switch exists | **both FPM services run simultaneously**, nginx routes by socket (`valet74.sock` / `valet.sock`); `php74`/`php8`/`phpst` only *start* services (`system/office.php-switch.zsh:32-59`) |

This is the mechanism difference, not just a path difference: office selects PHP by
**socket routing between two live services**; home selects it by **which container it calls**.
`valet use phpX` is broken on Arch and forbidden (`guides/office.md:76-88`). Anything
Docker-shaped in this tree is home's, by consequence.

**The ai/ scope — sourced from `ai/base.zsh` (0009 L2 signpost). `ai/` = SCOPE, not "dedicated-to" (operator clarification 2026-07-11): Gemini seats · Claude RC · temple transport · devenv transport.**

All temple-* scripts live under `ai/`. Consumers source `ai/base.zsh`; it wires the whole scope.
Do NOT source individual temple-* scripts directly unless you need a standalone invocation.
Partition maps + engine inventory (authoritative): `guides/guide-for-builder.md` §Architecture rules.

- `ai/base.zsh` — **the signpost (0009 L2).** Idempotent + side-effect-free on source; wires the whole ai/ scope in partition order: keyboard (P1) · harness alias (P2) · temple family (P3) · adr-guard alias (P4) · temple-tree (P5) · devenv engine (P6) · claude engine (P7) · gemini-processor (P8) · keys engine (P9). Source THIS, not individual scripts (sourced non-interactively by the git hook — defines functions/aliases only, never runs work or prints).
- `ai/temple-project-map.zsh` — P0: project map (name → repo-root) shared across machines (folder layout 1:1). The ONLY place physical paths live. Companion: `reposoma/registry/index.md` (logical map).
- `ai/temple-mail.zsh` — A: mail primitive. `temple-mail <origin>:<agent> <scope> [<body|->] [--from <o>:<a>]`
- `ai/temple-doorbell.zsh` — B: canon-doorbell. `temple-doorbell-run` — rings stale projects via A. Honors `DOORBELL_DRY_FIRE=1` (compute would-ring, write nothing).
- `ai/temple-doorbell.post-commit.hook` — hook template. Install: `cp ~/.config/zsh/ai/temple-doorbell.post-commit.hook ~/reposoma/.git/hooks/post-commit && chmod +x ~/reposoma/.git/hooks/post-commit`
- `temple-doorbell.log` — run log written by the hook at `~/.config/zsh/temple-doorbell.log` (flat; stays here)
- `ai/temple-mail-inbox.zsh` — C: read-side helper. `temple-mail-inbox <origin>:<agent>` — lists UNREAD items (presence = unread) from agent inbox + toAll broadcasts. Zero side effects; quiet exit when empty. Boot-order: call once per saddle-boot/project-switch; if output is non-empty, ask operator "read them now?" before catting content (ask-first rule, _mail/README.md). **This is the interface twins bind to (0010 R-b) — never the storage layout.**
- `ai/temple-mail-switch.zsh` — D: interactive mail-destination picker. `temple-mail-switch [--project <origin>]` — derives `origin:agent` candidates live from the P0 map + `_mail/*/`, fzf preview of newest inbox item, prints the selected address to stdout (composable: `temple-mail $(temple-mail-switch) <scope> <body>`). Read-only; select-menu degrade when fzf absent.
- `ai/temple-mail-manage.zsh` — E: mailbox read-state manager. `temple-mail-manage` (TUI) · `--list` · `--archive <receiver>/<filename>` · `--restore <receiver>/<filename>`. Implements decision 0010 read-state transition (presence in inbox/ = unread; move to archive/ = read; receiver-owns). EXECUTED script — never sourced (uses exit/stty); discovers `_mail` by walking up from `$PWD`. Operator alias: `temple-mail-manage`; agent CLI: `--list/--archive/--restore`.
- User guide for the mail family: `~/.config/zsh/guides/guide-temple-mail.md` (send · read · pick · manage)
- `ai/temple-transport-selftest.zsh` — sandboxed end-to-end selftest. `zsh ~/.config/zsh/ai/temple-transport-selftest.zsh` → 4/4 green. (Gates LOGIC, not WIRING — see doorbell-smoke for the real-trigger gate.)
- `ai/doorbell-smoke.zsh` — real-trigger smoke probe for the canon-doorbell (0009 L5). `zsh ~/.config/zsh/ai/doorbell-smoke.zsh --both` → green + deliberate-red. Exercises the live `commit → hook → base.zsh → temple-doorbell-run` path in a sandboxed temp git repo with `DOORBELL_DRY_FIRE=1`; asserts a drift-check (deployed hook vs template) + a planted-dead-path RED. Verified green + red 2026-07-02. This is the WIRING gate the selftest cannot be.
- `ai/harness-check.zsh` — card freshness checker (Gemini sector). Supersedes the removed `temple-recalibration.zsh` (monthly) with weekly systemd scheduling. Interactive alias: `harness-stale` (renamed from `aihs-stale` 2026-07-11, keyboard grammar).
- `ai/keyboard.zsh` — **AI interactive surface (control panel).** Aliases and comments only — no function bodies. Partitions: Gemini (P1–P6) · help panel (P7, `ai-help` = master) · Claude RC (P8) · temple panel (P9–P10) · devenv transport (P11) · keys panel (P12). P5 retired 2026-07-11 (Gemini Epoch killed). Sourced by `base.zsh`. Replaces `gemini-base.zsh` + `gemini-agents.zsh` (both killed 2026-07-03). Key map + grammar: `guides/keyboard.md`.
- `ai/gemini-processor.sh` — **Gemini scope engine (dual-sourced).** Subprocess core sourced by per-agent launchers; interactive surface sourced by `base.zsh` PARTITION 8. Subprocess core: `_gai_api_key`, `_gai_payload`, `_gai_rest_call`, `_gai_extract`, `_gai_strip_noise`. Interactive surface: `agy-vega`, `agy-orby`, `agy-astro`, `agy-astro-yolo` (P4 bodies), `gemini-fresh`, `agy-fresh` (P6 bodies), `gemini-agents-help` (P7 body). Aliases in `keyboard.zsh` P4/P6/P7. (Merged from `gemini.zsh` 2026-07-11 — one file per scope; `gemini.zsh` removed.)
- `ai/claude.zsh` — **Claude Code RC engine + help functions.** `_rc_stop` (→ `rc-stop`), `_temple_help` (→ `temple-help`), `_ai_help` (→ `ai-help`, the master panel). Sourced by `base.zsh` PARTITION 7. Aliases in `keyboard.zsh` PARTITION 7/8/10.
- `ai/experimental.zsh` — **MOVED 2026-09-22 → `experimental/` scope** (promoted to a sibling of ai/; hiding experiment bricks inside ai/ made orphans). Dispatcher is now `experimental/dispatcher.zsh`, wired by `experimental/base.zsh` P2 + `experimental/keyboard.zsh` P1, sourced from `config.<machine>.zsh` (NOT `ai/base.zsh`). Runners: `experimental/<id>/runner.zsh`. Contract + per-brick maintainer log: `experimental/README.md` + `experimental/base.zsh` head. **ai/base.zsh P9 still holds a now-dead `[[ -f ai/experimental.zsh ]]` source line — self-disabling (guard false), cosmetic removal DEFERRED to a temple gate (base.zsh is 0009-gated).**
- `ai/devenv.zsh` — **Project devenv transport engine.** `_devenv_sync` / `_devenv_deploy` / `_devenv_status` + per-project entry points `_fr_*` (freya.devenv) · `_bo_*` (fantasyobchod.devenv) + `_devenv_help`. Discipline: always `pull --rebase` BEFORE devenv-sync (built into the engine; SYNC_DISCIPLINE.md in each devenv repo). Sourced by `base.zsh` PARTITION 6. Aliases in `keyboard.zsh` PARTITION 11 (`fr-*`, `bo-*`, `devenv-help`).
- `ai/keys.zsh` — **global claviature engine.** `_keys` (→ alias `keys`, keyboard P12): derived keys panel — reads live aliases+functions at call time, buckets by family prefix, unknown keys land in UNSORTED (grammar drift detector). `keys --plain` for agents. Spec: `guides/claviature.global.spec.md`. Sourced by base.zsh P9.
- `ai/rc.sh` — **Claude Code Remote Control launcher (Approach B).** Reads `~/.config/zsh/registries/ai.json` (key `remote-control.projects`); starts or attaches named tmux sessions running `claude remote-control`. Commands: `rc.sh [status]`, `rc.sh <project>`, `rc.sh <project> stop`. Called via `rc-*` aliases in `keyboard.zsh`. Approach A (always-on) uses systemd units in `~/.config/systemd/user/claude-rc-*.service`. For full setup: `~/.config/zsh/guides/remote.md`.
- `ai/bluebottle.sh` — Bluebottle synthesizer. REST+CLI dual-path; headless-only. Called by `gemini-cross-check` agent and `g-bluebottle` alias. Replaces `bluebottle.zsh` (killed 2026-07-03).
- `ai/vega.sh` — Vega architect/advisor launcher. Dual-mode (no-arg=interactive, arg=headless). Model: `gemini-2.5-pro`.
- `ai/orby.sh` — Orby researcher launcher. Dual-mode. Model: `gemini-2.5-flash`.
- `ai/astrobley.sh` + `ai/personas/astrobley-patch.md` — RETIRED 2026-07-31 (0005 A1, chair vendor-shifted to Codex — see keyboard.zsh header). Persona quarantined from live tree 2026-09-01; script retained in repo as history.
- `ai/temple-tree.zsh` — tree-snapshot engine (temple utilities). `tree-snapshot <project>` — resolves root via temple-project-map, runs tree-converter.sh with project config (fallback: `tcr.default.json`); stdout = JSON tree. Sourced by base.zsh PARTITION 5. Guide: `guides/toolbox.tree-converter.md`.
- `ai/tree-converter.sh` — Node.js tree formatter (zero npm deps). Crawls CWD, outputs JSON/YAML. Flag: `-c <config.json>`. Called by temple-tree.zsh; also callable directly.
- `registries/tcr/` — per-project tree-snapshot configs. Naming: `tcr.<project>.json` (key = TEMPLE_PROJECT_MAP key). Fallback: `tcr.default.json` (depth 4 · JSON · gitignore-aware · `vendor/` excluded).

**Removed (0009 step 5):** `temple-recalibration.zsh` and its systemd units (`temple-recalibration.service`, `temple-recalibration.timer`) — superseded by `ai/harness-check.zsh` (weekly harness.timer).

**Removed (Gemini rebuild 2026-07-03):** `ai/gemini-base.zsh` → split into `keyboard.zsh` (aliases) + per-agent scripts. `ai/gemini-agents.zsh` → split into `keyboard.zsh` (wrappers, epoch) + per-agent scripts. `ai/bluebottle.zsh` → `ai/bluebottle.sh` (headless-only, bash, sources gemini-processor.sh).

**Removed (2026-07-11 merge):** `ai/gemini.zsh` → merged into `ai/gemini-processor.sh` (one file per scope — gaveled). Interactive surface section appended; `base.zsh` P8 re-pointed; `keyboard.zsh` comments updated.

**Verify-real-trigger rule (0009 L5):** definition-of-done for any AI-bonded script with a trigger is the systemd unit / git hook / cron firing and producing its output — never the script run by hand. The `harness.service` dead-path bug (pointing at `fresh/harness-check.zsh` which did not exist) is the cautionary example: a move was checked against the script by hand-run, never against the systemd trigger. The `ai/doorbell-smoke.zsh` probe is the standing instrument for the post-commit doorbell.

### KNOWN BROKEN — migrated 2026-09-16 to the central issue vault

This table's one entry (the `larva.zsh:31` `LARVA_SCRIPTS_DIR` defect, found 2026-07-29,
parked by operator call) now lives at
`~/reposoma/_issues/parked/ISS.larva-scripts-dir-missing.2026-07-29.md` — point, never copy.
Any NEW known-but-unfixed defect anywhere in ia-sync goes there too (`open/` first, `parked/`
once triaged), not back into this table — see `~/reposoma/_issues/README.md` for the shape
and why it's central instead of per-project (Janus + Codex/@mirror gate, 2026-09-16).

### PARKED — moved to `archive/` (machine-local history; not sourced)

Archived by majkee 2026-07-07 (plus earlier `substrate.*` parks):

| File in `archive/` | Notes |
|---|---|
| `substrate.config.home.zsh` | Stale home-machine config snapshot (sync.deny'd) |
| `substrate.host-id.zsh` | Over-built helper; use `echo $MACHINE_NAME` (sync.deny'd) |
| `larva.zsh` | Former startup copy; identical to live `projects/larva.zsh` |
| `session-helpers.zsh`, `session-syntax.zsh` | Superseded by `projects/session.zsh` + `session-meassure.zsh` |
| `ai-agents.registry.json` | ⚠ home's `ai-lifecycle.zsh` reads `~/.config/zsh/ai-agents.registry.json` — the home seat must verify home before the repo copy is dropped |
| `env-sync.zsh` | Deprecated tool (sync.deny'd; `.zshrc` source line removed 2026-06-30) |
| `project-switcher.home.zsh`, `project-switcher.office.zsh` | Old split variants; unified `project-switcher.zsh` is live |
| `tasks.js` | larva-era task registry (from `registries/`); sole consumer `ai-lifecycle.zsh:347` (UNCERTAIN/home-only) — ⚠ the home seat must verify home before any repo-copy drop. Archived 2026-07-11 |
| `larva/` (broadcast.sh · consult.sh · slices.sh · laika.sh) | larva project buried (temple legacy wall); unreferenced on office — ⚠ home seat to verify. Archived 2026-07-11 |

Archived by @Flight 2026-07-29 (operator call; wiring traced by @Eagle + @zenith-zsh, both independently CONFIRMED dead on office):

| File in `archive/` | Notes |
|---|---|
| `normalizer.py` | Registry hydrator. Orphaned on office — sole caller was `config.home.zsh:27`, which office never sources. **Live on home; home's copy survives `deploy.sh` (additive, no `--delete`) — archiving here does not break home.** Home retires it after migrating to inline `PROJECT_*` exports. |
| `substrate.config.home.2026-07-20.zsh` | Home's `config.zsh` sitting stale on office since 07-20 — cross-machine contamination, never sourced here. The *only* office file still referencing `REGISTRY_FILE`/`NORMALIZER`, which made office look like it used the dead mechanism. Repo's `zsh/config.home.zsh` (07-28) is home's canonical copy and was NOT touched. `sync.deny`'d via `substrate.config.home.*`. Second recurrence of this artifact (cf. `substrate.config.home.zsh`, April). |

### REMOVED — 2026-07-07 cleanup

| File | Notes |
|---|---|
| `mesh/office-wire.zsh` (+ empty `mesh/`) | office journal 2026-06-30 item 2 — Gate E closed, direct SSH covers it; already in sync.deny. Home's `config.home.zsh` still has its source line — home's side. |
| `system/pacman.zsh`, `system/browser.zsh` source lines in `config.zsh` | Files never existed on either machine or in repo |
| `harness.machine-project-registry.json` | ⚠ **CORRECTED 2026-07-29** — the original entry claimed "exists nowhere". That was FALSE and office-blind: the file is LIVE on home, read at every interactive login by home's `config.zsh:20-27` (`eval "$(python3 normalizer.py $MACHINE_NAME $REGISTRY_FILE)"`). It is absent on office only. Operator call landed 2026-07-29: the mechanism is retired — home migrates to inline `PROJECT_*` exports (office-style), THEN drops it. Home must not delete before porting or its project switcher loses all paths. |

### REMOVED — 2026-07-11 cleanup

| File | Notes |
|---|---|
| Gemini Epoch seat (keyboard.zsh PARTITION 5 + gemini-epoch/g-epoch aliases + guide-for-user rows) | Accidental cross-line seat — a builder agent added a Claude-line agent to the Gemini line; never operator-intended. Erase begun earlier (~/.gemini/agents/epoch.md already absent); wiring completed 2026-07-11. @Epoch = Claude line only. |

---

## Guard line

This is the operator's personal machine layer. Agents read it for host/resource facts
(`$MACHINE_NAME`, concurrency-guard location, project path constants), but do NOT bind
its absolute paths into any project's consumer surface (doctrine §4.7).
