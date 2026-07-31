# journal.history-index — git history of ia-sync, exported 2026-07-30

> Written because commit bodies ARE the `/multihost` transport: a history burn deletes every
> prompt ever exchanged between office and home. This file carries the record forward as a
> FILE, which survives. SHAs below refer to the pre-burn history — after a recreate they no
> longer resolve; the date + subject is the durable anchor. Full restorable history is
> parked at `~/ia-sync-history-backup/` (local only — it contains credentials).

---

## f6683cc · 2026-06-27 · init: claude skills, gemini agents, zsh config (2026-06-27)


---

## a938a37 · 2026-06-27 · feat: deploy.sh + per-host config.zsh naming (config.<machine>.zsh)

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

---

## 6476444 · 2026-06-27 · docs: add SYNC_GUIDE.md


---

## 8ebfa3b · 2026-06-27 · sync: 2026-06-27


---

## 39922c7 · 2026-06-29 · refactor: move archx substrate library to ia-sync/zsh/archx

- Unified monitoring suite (previously split between ~/.config/zsh and ~/reposoma)
- 45+ substrate functions now in ia-sync for team-wide access
- Updated commands.zsh to source from new location
- Both home and office machines can now deploy identical monitoring setup via deploy.sh
- Added clarifying comment to sync.sh for archx coverage
- All guides (CHEATSHEET, INDEX, RESOURCE_MONITORING) included
- Ready for office machine deployment

---

## b7fae05 · 2026-06-29 · feat: add human-readable monitoring CLI commands to archx suite

- archx-monitor: main command with 6 subcommands
  * system: full system snapshot
  * services: service health check
  * cpu [N]: top N CPU consumers
  * memory: memory breakdown
  * disk [path] [N]: top directories
  * troubleshoot: quick diagnostics
- archx-services: instant service status with ✅/❌ indicators
- archx-help: comprehensive guide with examples
- all: clean formatted output, works in scripts and interactive shells
- solves: noisy substrate output, improves human readability
- location: ~/ia-sync/zsh/archx/ (team-shared, synced via deploy.sh)

---

## 3500e4b · 2026-06-29 · refactor: archive stale project-switcher, sync current configs, ensure archx on both machines

- Archived both project-switcher.zsh versions to zsh/archive/ (for extraction if needed)
  * project-switcher.home.zsh
  * project-switcher.office.zsh
- Removed stale project-switcher.zsh from active configs (both machines)
- Synced current home config to ia-sync/zsh/config.home.zsh
- Added archx sourcing to office config (line ~145)
- Result: both configs now identical except for PHP wiring and project paths
- Both machines will have full archx monitoring suite on next deploy

---

## b437e02 · 2026-06-29 · docs: add office machine setup & audit handoff for agents

- Comprehensive guide for deploying ia-sync to office machine
- Phase 1: Deploy ia-sync (clone + deploy.sh)
- Phase 2: Wire up CLI scripts (symlinks in ~/bin/)
- Phase 3: Load & test config (source ~/.zshrc)
- Phase 4: System audit (hardware, services, tools, valet, paths)
- Phase 5: Create office profile guide (office.md equivalent to home.md)
- Phase 6: Validation checklist (all systems verified)
- Report template for audit findings
- Designed for agent execution with clear success criteria

---

## 224620f · 2026-06-29 · chore: add host-cleanup journal + fix project-switcher bugs

- journal.host-cleanup.md: git bus for office↔home agent coordination
  Office writes findings, Haiku (home) reads tasks and appends results
- zsh/project-switcher.zsh: fix sess/lrv launcher copy-paste bugs (lines
  148/153 called ltp instead of self), fix help text and error message

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

---

## 89eb1d5 · 2026-06-29 · fix: substrate column formatting + services_check + FO path correction

- bash.substrates.sh: replace raw ps aux dumps with aligned printf columns
  (cpu_top, memory_top, system_overview process tables)
- bash.substrates.sh: add missing substrate_services_check() — was called
  by archx-monitor but did not exist, skipping only installed services
- config.office.zsh: fix PROJECT_FO_PATH to ~/www/imago_cz/fantasyobchod
- journal.host-cleanup.md: note FO path fix, add Haiku task to verify home

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

---

## e110e6e · 2026-06-29 · docs: add HOME verification audit response (Haiku)

- Task 1: Docker/composer74 verified (functional, schema correct)
- Task 2: nginx + sites verified (fantasyobchod active, sockets correct)
- Task 3: nginx guides NOT duplicates (both kept, different scopes)
- Task 4: config.zsh Docker-wrapped composer confirmed (as expected)
- Task 5: Overall status — all services healthy, no drift from ia-sync
- New discovery: NEW_COMP_Quick_Start.md (500 lines, very recent, actionable)
- Result: HOME VERIFIED ✅ — No action required, in sync with office expectations

---

## d653ccf · 2026-06-29 · docs: sync team guides from my-env-sync to ia-sync

- home-setup/ (7 guides, 92KB):
  * NEW_COMP_Quick_Start.md — critical Docker vs FPM guide
  * nginx_Setup_Manual_@home.md — complete nginx config
  * OpenCart_Home_Setup_Complete_Guide.md — project reference
  * machine.resource-control.home.md — memory defense
  * nginx_setup_guide.md — multi-PHP context
  * diagnose_opencart_404.md — troubleshooting
  * PHP_Extension_Verification.md — extension checklist

- cross-machine/ (3 guides, 30KB):
  * Repomix_Reference_Guide.md
  * Terminal_Search_Reference_Guide.md
  * Tree_File_Listing_Reference_Guide.md

- guides/README.md — guide matrix, usage reference, maintenance notes

Organization:
  - Home-specific guides for @home setup (nginx, Docker, OpenCart)
  - Cross-machine tool references for both machines
  - README with usage matrix and audit trail

Status:
  - All guides dated 2026-02/03/05 (current)
  - Synced from ~/www/my-env-sync/ (source)
  - Now in ia-sync for team backup & office reference

---

## 1efa004 · 2026-06-29 · sync: home machine zsh configs and Claude agents/skills to ia-sync

ZSH Configs (16 files):
  Core workflow:
    - ai-lifecycle.zsh (AI agent bootstrap)
    - env-sync.zsh (environment variable sync)
    - larva.zsh (coding session framework)
    - git-lifecycle.zsh (git workflow helpers)

  Session & Terminal:
    - session-helpers.zsh (session management)
    - session-syntax.zsh (syntax support)
    - session-measure.zsh (metrics)
    - shared-toolkit.zsh (common utilities)

  System & Extensions:
    - krfb.zsh (tablet extension)
    - substrate.host-id.zsh (machine identification)

  Plus: config backups, utilities
  Excluded: secrets.zsh (credentials, in .gitignore)

Claude Agents (26 new files):
  - Core orchestrators: houston, flight, capcom, janus, hypatia, agol, var
  - Code creators: atlas-auto, atlas-ui, claude.creator.*
  - Specialists: color, epoch, mlok, scribe, delta, recorder, trajectory
  - Support: 42.md, coder-junior

Claude Skills (10 directories):
  - Workflow: buffering-cycle, first-person-voice, goal
  - Agents: hypatia-brief, learn-repomix
  - Architecture: regime-arch
  - Documentation: fetch-agent-docs, fetch-ollama-docs, fetch-qwen-docs
  - Tools: claude-creator

Result: Complete ZSH environment + Claude infrastructure now backed up in ia-sync
- All configs synced from ~/.config/zsh/ (excluding machine-specific secrets)
- All agents synced from ~/.claude/agents/
- All skills synced from ~/.claude/skills/
- Ready for deployment to office machine via deploy.sh

---

## 6016d4a · 2026-06-29 · docs: add OFFICE_DEPLOYMENT_EXECUTION.md (agent-ready deployment plan)

Detailed execution guide for office machine deployment:

Phase 1: Deploy ia-sync
  - Clone/update from GitHub
  - Run non-destructive deploy.sh
  - Verify all deployments (configs, archx, claude)

Phase 2: Wire up CLI scripts
  - Create symlinks in ~/bin/ for archx commands
  - archx-monitor, archx-services, archx-help

Phase 3: Load & test config
  - source ~/.zshrc
  - Test monitoring commands
  - Verify all functions available

Phase 4: System audit
  - Hardware/OS discovery
  - Services status check
  - Development tools inventory
  - Valet status (office-specific)
  - Project paths verification

Phase 5: Create office.md profile
  - Machine specs table
  - Services status table
  - Development setup
  - Office-specific configuration
  - Differences from home

Phase 6: Validation checklist
  - MACHINE_NAME verification
  - Monitoring suite verification
  - Documentation availability
  - Claude infrastructure check
  - Project paths check

Includes:
  - Pre-execution prerequisites check
  - Phase-by-phase bash scripts
  - Expected outputs for each phase
  - Audit report template
  - Success criteria (all ✅ checkpoints)
  - Post-deployment next steps

Ready for office agent execution

---

## 47b3643 · 2026-06-29 · docs: add agent safeguard procedures to deployment guide

Enhanced Phase 1 with agent backup strategy:

SAFEGUARD STEPS:
- Before deploy: Auto-backup existing office agents (timestamped)
- Compare: Check agent count before/after (expected: 26 minimum)
- Verify: Detect if office-custom agents were preserved
- Restore: Procedures to rollback/restore if needed

RATIONALE:
Office machine may have customized agent definitions tuned for office
workflows that are more current than home versions. Deploy.sh uses rsync
which will overwrite same-named agents. This safeguard:
  ✅ Preserves office-only agents (not deleted by rsync)
  ✅ Backs up all existing agents before deployment
  ✅ Detects overwrites via agent count check
  ✅ Provides easy rollback if needed

ADDED SECTIONS:
- Phase 1 Step 0: Automatic agent backup before deploy
- Phase 1 Step 4: Post-deploy agent verification
- New section: Agent safeguard restoration procedures
- Detailed restore steps (single agent, all agents, merge)

RESULT:
Deployment is now fully reversible for agents. Office can safely deploy
knowing existing customized agents are backed up and can be restored if
the home versions aren't suitable.

---

## f879215 · 2026-06-29 · feat: add self-contained office deployment script

Created deploy-office.sh — production-ready deployment for office machine

FEATURES:
- All 6 phases in single executable script
- Automatic agent backup (safeguard)
- Automatic verification at each phase
- Colored output for readability
- Agent count validation
- Timestamped audit report generation
- Post-deployment next steps
- Restoration instructions

PHASES:
1. Deploy ia-sync (with agent backup)
2. Wire up CLI scripts (symlinks)
3. Load & test config
4. System audit
5. Create office.md profile
6. Validation & audit report

AGENT SAFEGUARD BUILT-IN:
- Pre-deploy: Auto-backup to ~/.claude/agents-backup-predeployment-<TS>/
- Post-deploy: Verify agent count and detect overwrites
- Restoration: One-liner recovery if needed

USAGE:
  bash ~/ia-sync/deploy-office.sh

RESULT:
- Generates OFFICE_AUDIT_<TS>.md with complete system profile
- No manual steps needed (fully automated)
- Safe to run multiple times (backed up)
- Office-ready for immediate use after deployment

---

## 9e0f912 · 2026-06-29 · docs: add SONNET_HANDOFF.md — complete office agent briefing

Created comprehensive handoff document for Sonnet (office agent):

CONTENTS:
- Machine identity check (how to verify you're on office)
- Complete ia-sync overview (what it is, what it contains)
- Infrastructure comparison (home vs office differences)
- Deployment status & 6 phases
- Agent safeguard explanation (automatic backup/restore)
- Reading list in priority order
- Immediate tasks (verify prerequisites → deploy → audit)
- Office config reference (all key constants)
- What you'll get after deployment
- Quick reference commands
- Critical reminders
- Success criteria

PURPOSE:
Every time Sonnet is handed off to this task, they read SONNET_HANDOFF.md
first. It contains ALL necessary context — machine identity, infrastructure
differences, deployment steps, file locations, success criteria.

AUTOMATION BENEFIT:
- No context loss between sessions
- Sonnet knows exactly where to find everything
- Clear success criteria to verify
- Automatic agent safeguard built in
- Full office config available

USAGE:
Before handing any office task to Sonnet:
1. Say: 'Read SONNET_HANDOFF.md first'
2. Then give task
3. Sonnet has full context automatically

---

## 1dfe501 · 2026-06-29 · refactor: SONNET_HANDOFF.md — navigation only, no duplicates

Changed from duplicate content to pure navigation guide:

BEFORE:
- Duplicated information from other files
- SONNET_HANDOFF.md contained full briefs already in source docs

AFTER:
- Navigation guide only (this file)
- Points to actual source files with exact reading order
- No duplicated content — read source files for complete picture
- Sonnet gets full context by following reading order

READING ORDER (5 stages):
1. Understand system: README.md → journal.host-cleanup.md → config.office.zsh
2. Understand deployment: OFFICE_DEPLOYMENT_EXECUTION.md
3. Execute: deploy-office.sh (automated)
4. Verify & document: Update journal with findings
5. Reference materials: As needed

PRINCIPLE:
- This file is navigation only
- Source files are authoritative (no duplication)
- Sonnet reads actual docs, gets full context
- Enables cooperation between home and office agents on parallel tasks
- Each agent on its own machine, complete understanding via reading order

---

## 238095d · 2026-06-29 · refactor: remove OFFICE_MACHINE_SETUP.md (redundant with OFFICE_DEPLOYMENT_EXECUTION.md)

REMOVED:
- OFFICE_MACHINE_SETUP.md (high-level phases overview)

WHY:
OFFICE_DEPLOYMENT_EXECUTION.md contains all the same information
(phases, what happens at each step) PLUS the actual executable bash
scripts and detailed instructions. SETUP.md was just the abstract,
EXECUTION.md is the concrete version with scripts.

RESULT:
No redundant files. Single source of truth for office deployment:
OFFICE_DEPLOYMENT_EXECUTION.md (complete + executable)

---

## 05fc699 · 2026-06-29 · fix: restore office agents as canonical, remove junk zsh files

PROBLEM: Haiku (home) synced stale home agents into ia-sync/claude/agents/
and committed home-specific/dead zsh files into ia-sync/zsh/. Running
deploy.sh would have overwritten office's correct agents with home's stale
ones and deployed garbage configs to ~/.config/zsh/.

Agents:
- Replaced ia-sync/claude/agents/ with office's 18 canonical agents
- Removed 8 stale home-only agents (42, claude.creator.*, coder-junior,
  mlok, scribe, trajectory-senior-dev)

ZSH junk removed from ia-sync/zsh/:
- config_backup_docker.zsh (home config artifact)
- substrate.config_backup_docker.zsh (same)
- substrate.host-id.zsh (explicitly parked/dead)
- env-sync.zsh (misnamed repomix generator, not a zsh config)

deploy.sh: exclude gemini/projects.json (machine-specific project paths)
deploy-office.sh: make EXPECTED_COUNT dynamic (was hardcoded 26 for home)

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

---

## 6cee17f · 2026-06-29 · docs: add office machine profile guide (zsh/guides/office.md)

Machine profile for hruzam-120922 (office). Covers:
- Hardware (i5-12400, 15GiB RAM, NVMe disks)
- Critical PHP difference vs home: office has native /usr/bin/php74 CLI,
  so composer74 is a direct binary call, NOT Docker-wrapped like home
- PHP/Valet switching (php74_on/php8_on + valet use phpX)
- Project paths: ~/www/imago_cz/fantasyobchod, + /media/data/projects/
  for psd/ltp/lrv/sess (detachable data disk)
- Service table, monitoring suite, home↔office diff table

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

---

## a3542b1 · 2026-06-29 · add archx/commands.zsh; fix deploy-office.sh bash context + symlink display

- zsh/archx/commands.zsh: new — defines sysmon/cputop/memtop/diskuse/services
  aliases and troubleshoot() function; sourced by config.zsh at shell start
- deploy-office.sh: replace `source ~/.zshrc` (fails in bash via set -euo) with
  a note to user; test archx scripts directly with bash instead
- deploy-office.sh: replace awk symlink display with readlink loop (reliable)

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

---

## 45397ef · 2026-06-29 · journal: Kelvin deploy update + team naming (Kelvin/Shannon)

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

---

## 17d88d1 · 2026-06-29 · zsh: add system/ + piql/ folders; clean substrate.config.home.zsh; journal→Haiku

- zsh/system/shell.zsh: src, ord, hasz, cod, sub2, msrc, svt aliases
- zsh/system/pacman.zsh: update_conflicted_files, down_pack utilities
- zsh/piql/piql.zsh: piql integration stub (office-only, sources piql.env.zsh)
- config.office.zsh: wire system/ + piql/ sources; move piql from direct path to stub
- zsh/substrate.config.home.zsh: removed (home artifact, missed in earlier cleanup)
- journal: Kelvin→Haiku handoff — pull, deploy, system/ wiring instructions

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

---

## 60839b0 · 2026-06-29 · fix PHP switching: per-site nginx for FO, remove broken valet use calls

- project-switcher.zsh: php74_on/php8_on now just start FPM service (no valet use)
  valet use phpX is broken on Arch — package name mismatch (php7.4-fpm vs php74-fpm)
- project-switcher.zsh: phpst now shows socket state + which sites use which PHP
- guides/sudoers.valet-php.conf: drop-in for passwordless FPM/nginx sudo

FO routing fix (manual step for user):
~/.valet/Nginx/fantasyobchod → routes fantasyobchod.l to valet74.sock (PHP 7.4)
This is a permanent per-site config; no more manual php switching for FO.
Apply with: sudo nginx -t && sudo systemctl reload nginx

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

---

## 59cec06 · 2026-06-29 · zsh: browser.zsh, dev launchers, Laravel shortcuts, Shannon agent; fix gitignore

- system/browser.zsh: ffoxLocal, ffoxChatGpt, firefox_virtual_displays
- system/shell.zsh: add dsk, ssr aliases
- project-switcher.zsh: imdev()/imst, fodev()/fost multi-process session launchers
- projects/im-toolkit.zsh: optimize, seeder, che, mig, gpl, dbim shortcuts
- config.office.zsh: source browser.zsh
- claude/agents/shannon.md: piql wiser mechanic agent spec
- .gitignore: anchor projects/ to root (was matching zsh/projects/ unintentionally)

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

---

## 145e7ff · 2026-06-29 · piql: Tailscale cross-machine bridge (office ↔ home)

- piql/tailscale.zsh: tss, tsp, tsping, piql-remote, piql-watch, piql-push,
  piql-ask, piql-expose / piql-expose-off / piql-expose-status
- piql/piql.zsh: source tailscale.zsh via ${0:A:h} relative path
- config.office.zsh: TAILSCALE_PEER="hruzam" (home), PIQL_PORT stub
- config.home.zsh: TAILSCALE_PEER="hruzam-120922" (office), source tailscale.zsh
  (home gets tss/tsp/piql-remote/piql-watch without needing piql locally)

Shannon: review piql-expose before enabling — widens scope to full tailnet.
SSH pull (piql-remote/piql-watch) is read-only and safe as default.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

---

## 2cf4a72 · 2026-06-29 · fix: Freya path + Octane; piql arch confirmed; Shannon spec updated; journal K3

- config.office.zsh: PROJECT_IM_PATH ~/www/freya → ~/www/imago_cz/freya (path bug)
- project-switcher.zsh: imdev() — remove artisan serve (Valet+Octane), add URL freya.l; imoctane alias
- piql/tailscale.zsh: note CLI-only arch, fix log path to session/, update header
- claude/agents/shannon.md: add confirmed piql architecture details (bus/pip.zsh, no HTTP, doctor path)
- journal: Kelvin update 3 — session summary, piql/Tailscale bridge, Freya findings, pending manual steps

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

---

## 42e54a4 · 2026-06-29 · guides: add shell-commands.md — complete office zsh reference

PHP switching, dev session launchers, Tailscale/piql bridge, Laravel shortcuts,
archx monitoring, system utilities, browser, pacman, agents, key file paths.
Readable from both machines (office-only sections marked).

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

---

## c017960 · 2026-06-29 · add remaining project toolkits; gitignore gemini runtime state

fo-toolkit, larva, ltp-toolkit, psdvs-toolkit, session — all now tracked.
gitignore: add gemini/config/projects/ (machine-specific runtime state).

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

---

## 9b9c919 · 2026-06-29 · refactor: remove 8 stale Claude agent definitions

DELETED from claude/agents/:
  - 42.md
  - claude.creator.auto.md
  - claude.creator.sniffer.md
  - claude.creator.ui.md
  - coder-junior.md
  - mlok.md
  - scribe.md
  - trajectory-senior-dev.md

KEPT: 19 active agents
  - Core orchestrators: houston, flight, capcom, var, janus, hypatia, agol
  - Specialized: color, epoch, recorder, symmetry
  - Executors: trajectory, delta, vector
  - Creators: atlas-auto, atlas-ui
  - Other: shannon, zenith, zed-editor-expert

NEXT STEP:
- Home machine: Delete ~/.claude/agents/ directory
- Populate fresh agents in ~/.claude/agents/
- Run: bash sync.sh
- Fresh agents will sync to repo

---

## bbaedda · 2026-06-29 · journal: HOME — pull and deploy response to Kelvin

Haiku (home) executed Kelvin's requested deployment:

COMPLETED:
- git pull origin main (already up to date)
- bash ~/ia-sync/deploy.sh (full deployment)
- All Claude infrastructure deployed
- New piql/tailscale bridge systems deployed
- Shannon agent deployed

VERIFICATION:
- Freya project at ~/www/imago_cz/freya (correct path)
- Tailscale peer: hruzam (100.110.27.60)
- piql architecture: prefilter → bus/pip → claude CLI
- New aliases ready to activate (tss, tsp, piql-ask after source ~/.zshrc)

READY FOR:
- Cross-machine piql queries (piql-ask from home reaches office)
- Tailscale monitoring (tss, tsp commands)
- piql-watch/piql-remote integration

Status: HOME fully synced with OFFICE updates

---

## c7a7777 · 2026-06-29 · office: subl/zed as preferred editors; Maxwell (home agent) spec

- config.office.zsh: PREFERRED_EDITOR=subl, PREFERRED_EDITOR_ALT=zed
- claude/agents/maxwell.md: home maintenance agent — 1:1 Kelvin minus piql

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

---

## 7b382f8 · 2026-06-29 · pre-deploy home cleanup: remove 4 stale zsh files, drop env-sync.zsh

- rm config_backup_docker.zsh, config.zsh.backup (dodge deploy exclude pattern)
- rm substrate.config.home.zsh, substrate.config_backup_docker.zsh
- config.home.zsh: remove env-sync.zsh source (deprecated by ia-sync)

Maxwell audit flagged all four as deploy-junk risk.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

---

## 098f5c2 · 2026-06-29 · sync: 2026-06-29 home — mesh/ added, secrets.zsh excluded


---

## bce57d1 · 2026-06-29 · registry: fix FO/IM paths and office editor on both machines

- FO: ~/www/fantasyobchod → ~/www/imago_cz/fantasyobchod (both home+office)
- IM: ~/www/freya → ~/www/imago_cz/freya (both home+office)
- office PREFERRED_EDITOR: code → subl (matches config.office.zsh fix)

User confirmed home projects now mirror office folder structure.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

---

## 8325655 · 2026-06-29 · fix: remove secrets.zsh from snapshot, harden sync.sh cleanup


---

## 70d7854 · 2026-06-29 · feat: sync.deny registry — explicit never-sync denylist for zsh leg


---

## 829cb61 · 2026-06-29 · fix: undo home sync traps; harden against recurrence

Traps from home batch (8325655):
1. 4 stale files re-added (sync.deny *.bak didn't match *.backup/*_backup_*.zsh)
   → Added explicit filenames to sync.deny + *.backup pattern
2. maxwell.md deleted (agents/ rsync --delete wiped office-only agent)
   → Removed --delete from agents/ leg (additive only; office owns canon)
3. env-sync.zsh re-enabled in config.home.zsh
   → Reverted to comment; add env-sync.zsh to sync.deny TODO if still on home

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

---

## 7382fc9 · 2026-06-29 · docs: SYNC_DISCIPLINE.md — pull-first rules for human + agent operators

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

---

## 4e12834 · 2026-06-29 · maxwell: link SYNC_DISCIPLINE.md in startup + do-not list; journal note for Kelvin

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

---

## cc89ce8 · 2026-06-29 · fix: secret scan false positive on NOPASSWD in sudoers template

Use \bpasswd\b word boundary with -E so NOPASSWD: (sudoers syntax)
doesn't match. sudoers.valet-php.conf contains no credentials.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

---

## b5ac982 · 2026-06-29 · normalizing both


---

## cfc9a5e · 2026-06-29 · fix: 3 traps from home batch + env-sync.zsh root fix

- config.office.zsh: PREFERRED_EDITOR code→subl (stale home copy)
- config.home.zsh: env-sync.zsh re-disabled (3rd time — now also in sync.deny)
- sync.deny: added env-sync.zsh so sync.sh can never re-add it
- mesh/office-wire.zsh: _WOFM_CLAUDE .npm-global→.local/bin (dead binary fixed)

Home action needed: rm ~/.config/zsh/env-sync.zsh (physical file still there)

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

---

## 80dd3da · 2026-06-29 · fix: ssh/remote noise — interactive guard, mesh source, clean wofm do

1. config.home.zsh: source mesh/office-wire.zsh (wofm now available on home)
2. config.office.zsh: guard startup echo with [[ -o interactive ]]
   — wofm do / non-interactive SSH sees no noise
3. mesh/office-wire.zsh:
   - wofm do: drop -l login shell; source config directly (no startup noise)
   - wofm claude: already direct exec, unchanged
   - help: fix stale .npm-global claude path

Note for home: any terminal header should also use [[ -o interactive ]] guard.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

---

## 2e2b4a4 · 2026-06-29 · wofm claude: pass through all args (--agent, --effort, etc.)

printf %q handles quoting for special chars over SSH.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

---

## 6539780 · 2026-06-29 · wofm claude: zsh-native arg quoting via \${(q)*}

Replaces printf %q (bash-centric) with zsh's own quoting.
Handles: empty args, spaces in strings, all claude flags.
claude's own error output returns unmodified via SSH PTY.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

---

## a2eb553 · 2026-06-29 · wofm: use \$TAILSCALE_PEER as host instead of unresolvable 'office' alias

config.home.zsh sets TAILSCALE_PEER=hruzam-120922. Falls back to that
if var unset. Removes dependency on ~/.ssh/config Host alias on home.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

---

## d3ab337 · 2026-06-29 · wofm: hardcode office Tailscale host — don't use TAILSCALE_PEER

TAILSCALE_PEER varies per machine config. wofm is always home→office
so the destination is fixed: hruzam-120922.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

---

## 1706452 · 2026-06-29 · replace wofm with simple office SSH aliases on home

Drop: mesh/office-wire.zsh (deleted), complex wofm function
Add:  office / office-claude / office-piql aliases + office-run()
Requires: ~/.ssh/config Host office → hruzam-120922 (one-time manual step)
sync.deny: block office-wire.zsh from re-entering repo

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

---

## 7082df4 · 2026-06-29 · office-claude: function with full arg passthrough for agents

alias → function so ${(q)*} preserves quoting over SSH.
office-claude --agent shannon / --effort high / --print "..." all work.
office-piql: same for piql dir. office-run: any command on office.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

---

## b55793c · 2026-06-29 · office: one alias, full freedom — drop project-specific wrappers

office → ssh -t office
Then work natively: claude, cd project, --agent anything.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

---

## 9e4fc7e · 2026-06-29 · mesh→ai: office-wire.zsh moved to ai/ scope


---

## a1691ee · 2026-06-29 · sync: 2026-06-29 home — office-wire source line restored


---

## 6ea193a · 2026-06-29 · journal: Kelvin session close — arch tuning done, cross-machine → piql/Houston

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

---

## 889f4a1 · 2026-06-29 · add CLAUDE.md + AGENTS.md — Kelvin saddle for ia-sync repo

Kelvin orients from journal + git log, follows SYNC_DISCIPLINE.md.
Key addition: Kelvin mails piql Houston after substrate changes —
arch tuning and piql are cooperative siblings, not separate scopes.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

---

## e661a29 · 2026-06-29 · kelvin: mail inbox, guide fixes, office config snapshot

- AGENTS.md: add _mail/kelvin/inbox/ to session startup orient sequence
- .gitignore: add _mail/ (ephemeral bus, non-canonical)
- guides/office.md: fix PROJECT_IM_PATH ~/www/freya → ~/www/imago_cz/freya
- guides/home.md: fix FO/IM project paths, editor (Code→Sublime/Zed)
- zsh/config.office.zsh: snapshot current office config (PREFERRED_EDITOR fixed)

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

---

## 597d931 · 2026-06-29 · test Home -> office


---

## dc7cf79 · 2026-06-29 · test Home -> office


---

## 0e2f34a · 2026-06-29 · mail: Gate E closed — maxwell inbox consumed, archive gitignored

- _mail/maxwell/inbox/kelvin.gate-e-home-test.md: delivered + consumed
- Gate E confirmed PASS via Haiku proof mail from home
- .gitignore: _mail/*/archive excluded (inboxes now sync, archives stay local)

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

---

## 70510cd · 2026-06-30 · journal: Kelvin session close 2026-06-30

Gate E done, zsh cleanup, Phase H tasks, mail inbox wired.
Open: linger, office-wire removal, ControlMaster stanza for home.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

---

## bc337d4 · 2026-07-03 · sync: gemini rebuild cleanup + coder patch-protocol 2026-07-03

- Kill: gemini-agents.zsh, gemini-base.zsh (replaced by keyboard.zsh + per-agent scripts)
- Add: keyboard.zsh, processor.sh, bluebottle.sh, orby.sh, vega.sh, astrobley.sh
- Add: personas/astrobley-patch.md (PHP patch-protocol persona, gaveled 2026-07-03)
- Add: ai/README.md, guides/guide-for-user.md, guides/guide-for-builder.md
- Update: AGENTS.md (--patch mode + personas/ documented), epoch.md (Gemini runbook)
- Misc: accumulated agent/skill/config changes from reposoma sessions 2026-07-02/03

---

## d14b77a · 2026-07-03 · before claening house - clean path


---

## 8a2201b · 2026-07-20 · synchronize computers


---

## 21b2eb6 · 2026-07-20 · fix(home): source ai/base.zsh in config.home.zsh — was never wired, whole ai/ scope silently never loaded on home; add sync-discipline rule to catch this class of gap


---

## cc6b1c1 · 2026-07-28 · sync: fold ~/.zshrc into zshrc.{host} on sync/deploy

sync.sh now copies ~/.zshrc → zsh/zshrc.${MACHINE} alongside config.zsh.
deploy.sh restores zshrc.${MACHINE} → ~/.zshrc; excludes zshrc.* from the
bulk rsync to ~/.config/zsh/ to prevent misplacement. SYNC_DISCIPLINE.md
documents the ownership rule and symmetric file-pair table.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

---

## c240a49 · 2026-07-28 · sunc:2026-07-28 office -> zsh sync


---

## 0b63ca1 · 2026-07-28 · fix(sync): exclude host-specific files from the bulk zsh rsync

sync.sh mirrored ~/.config/zsh → zsh/ with --delete and no guard for the
host-specific pair files, so it would:
  - overwrite the OTHER machine's config.{host}.zsh with whatever stale copy
    happened to sit in this machine's ~/.config/zsh/
  - --delete the host files this machine does not have (zshrc.{host})

Caught on office 2026-07-28: a 07-20 config.home.zsh was sitting locally and a
dry run showed it overwriting the repo copy — silently reverting home's
ai/base.zsh fix (21b2eb6), the exact regression that commit documented.

deploy.sh already excluded zshrc.* on its leg; sync.sh never got the matching
guard when the zshrc.{host} mechanism landed. Half-wired feature.

Excludes are hardcoded, NOT added to sync.deny: that registry means "must never
exist in the repo" and its find -delete pass would erase these files outright.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>

---

## 0046a45 · 2026-07-28 · sync: 2026-07-28 office -> repo snapshot

First run with the zshrc.{host} mechanism active: zsh/zshrc.office created
from live ~/.zshrc (2116 B). config.office.zsh refreshed from live config.zsh.
zsh/config.home.zsh deliberately untouched — home owns it.

- new skills: gavel-loop (absorbs retired gavel-ballot), cold-start-card, drop-brief
- agents: atlas-ui, eagle refreshed
- zsh: ai/ scope engines, guides/, psdvs-toolkit, office.php-switch
- gemini: projects.json, antigravity-cli settings

Secret scan flagged 2 files; both verified false positives — devenv-sync-core.sh
matches its own grep pattern list, gemini-processor.sh references GOOGLE_API_KEY
by name and reads it from env. Independent scan for literal key material: clean.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>

---

## dd33e66 · 2026-07-28 · feat(deploy): back up live host files before overwriting them

deploy.sh replaced ~/.zshrc and ~/.config/zsh/config.zsh wholesale from the repo
with no undo path. Any bad, truncated, or stub host file reaching the repo would
destroy the live one irrecoverably — neither has ever been committed from home.

backup_live() copies the target to <file>.bak-YYYY-MM-DD before the overwrite.
One backup per file per day: if today's already exists it is kept, so the FIRST
pre-deploy state of the day survives repeated deploys. Verified in sandbox that
the original content survives two consecutive stub overwrites.

*.bak and *.bak-* are already in sync.deny, so backups never re-enter the repo.

Also documents in SYNC_DISCIPLINE.md that a missing zshrc.{host} is the SAFE
state and must never be stubbed by hand: an empty placeholder passes deploy.sh's
-f test and gets copied over the machine's real ~/.zshrc. Nothing requires the
file to exist — the correct way to create it is to run sync.sh on that machine.

Mail left for @Maxwell at _mail/maxwell/inbox/, pointer in journal.host-cleanup.md.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>

---

## 0c196a8 · 2026-07-28 · sync: 2026-07-28 office — drop dead Write(/etc/ssh) deny rule


---

## 344d733 · 2026-07-28 · docs(sync): deploy before sync on a machine that may be behind

The existing rule ("never reorder steps 2 and 3") does not cover the stale-upload
case. `git pull` updates the repo; `sync.sh` reads the LIVE machine, which a pull
never touches. Only `deploy.sh` refreshes the live set. So pulling first does not
protect against syncing a stale machine.

sync.sh uses rsync --delete on claude/skills/, claude/commands/, gemini/agents/
and gemini/config/projects/. A sync from a stale machine deletes from the repo
every file that machine lacks — 30 skills and 3 commands as of today — and git
records it as a deliberate removal. claude/agents/ is the only protected leg
(additive, per AGENTS.md); that guard was never extended to the others.

@majkee reviewed and chose order discipline over a code guard, so the documented
order is now the only control. Stated explicitly in SYNC_DISCIPLINE.md and in
@Maxwell's mail, whose previous instructions had him syncing before deploying.

No behaviour change — documentation only.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>

---

## c33954c · 2026-07-28 · journal: office relocated — pivot role now situational

Office is physically staying put and reachable over Tailscale; fresh material can
now originate from either machine. Records that this invalidates the "office
controls agent canonical set" premise at sync.sh:30, raises deploy-before-sync
from hygiene to a hard per-session precondition on both machines, and leaves the
agents-only --delete protection resting on a justification that no longer holds.

Skill to formalise the two-way pivot deferred by @majkee.

Journal only — no behaviour change.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>

---

## 2f3e89c · 2026-07-29 · retire registry+normalizer on office; answer home's Q1-Q6

MACHINE<>MACHINE: office -> home. Read the commit body before deploying.

Operator call 2026-07-29: harness.machine-project-registry.json +
normalizer.py are retired on BOTH machines. Office side executed here.

Wiring traced independently by @Eagle and @zenith-zsh before any move —
both CONFIRMED dead on office. Sole caller was config.home.zsh:27
(eval "$(python3 $NORMALIZER $MACHINE_NAME $REGISTRY_FILE)"), and that
file is never sourced by office's chain. No systemd unit, hook, or cron
consumer found.

Office changes:
- normalizer.py            -> zsh/archive/ (live + repo)
- config.home.zsh (stale 07-20, cross-machine contamination)
                           -> archive/substrate.config.home.2026-07-20.zsh
                              (office live only; repo's config.home.zsh
                               is home's canonical 07-28 copy, untouched)
- sync.deny: substrate.config.home.zsh -> substrate.config.home.*
             (artifact has now recurred twice; glob stops the third)
- zsh/AGENTS.md:157 CORRECTED. It claimed the registry "exists nowhere".
  That was false and office-blind -- the file is live on home and read at
  every login. The error was written from office's seat on 07-07 and is
  what let the office block rot unnoticed.
- zsh/AGENTS.md:89 resolved out of the UNCERTAIN table.

Office shell verified after moves: @office loaded, MACHINE_NAME=office,
switcher fo/im/psd/ltp/lrv/sess all resolve, exit 0.

HOME -- SAFE TO PULL AND DEPLOY. deploy.sh's zsh leg is rsync -a with no
--delete, so home's live normalizer.py survives. Nothing breaks.

HOME -- DO NOT delete registry/normalizer yet. config.zsh:27 still evals
it at login; deleting before porting drops every PROJECT_* path. Migrate
to inline exports first, verify a fresh shell, then archive. Full
sequence in _mail/maxwell/inbox/kelvin.office-state.2026-07-29.md.

That mail also answers Houston's Q1-Q6:
- office is exactly origin/main @ c33954c, nothing ahead/behind/stashed;
  the 07-07 "ahead of repo" note was stale
- skills 30/30 identical to repo; --delete trap confirmed in code and it
  covers commands/ too, not just skills/
- hypatia-brief is dead AND so is gavel-ballot (absorbed into gavel-loop
  2026-07-27) -- home should sync 4 of its 6 skills, not 6
- sync.sh has NO dry-run flag; the 07-28 "caught by dry run" was a manual
  rsync -n. Reproducing invocation included.

Also note: MACHINE_NAME is empty in non-interactive shells, so both
scripts fall back to hostname -s (hruzam-120922, not office). Run the
ritual from an interactive shell.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01PuLsYLGuWrw4K9Wv9PdHy8

---

## 821e724 · 2026-07-29 · journal: 2026-07-29 registry retired on office; home migration handoff

Records the AGENTS.md:157 false-claim correction, the Eagle/zenith-zsh
falsification pass, and the ordered migration Maxwell must run on home
before deleting anything.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01PuLsYLGuWrw4K9Wv9PdHy8

---

## a4a4abc · 2026-07-29 · feat(skill): multihost — surgical cross-machine injection transport

MACHINE<>MACHINE: office -> home. Additive, safe to pull.

Encodes the operator's 2026-07-29 communication protocol as a callable
instrument: exchange with the other host by git push message + file;
deploy as backup-first injections; overrides conflicting sync
regulations but never the logic.

Skill, not subagent -- sibling transports (drop-brief, cold-start-card)
are skills, and this is a procedure, not a reasoning seat. No new
runtime layer.

The substance is not the restated order, it is the substrate table:
- deploy.sh zsh+claude legs are rsync -a with NO --delete, so retiring
  a file on one machine cannot break the other. This is the property
  that makes one-sided retirement safe, and it was not written down
  anywhere before today.
- sync.sh skills/ and commands/ DO run --delete, so a sync from a
  stale machine wipes the other side's contributions.
- MACHINE_NAME is empty non-interactively; both scripts then fall back
  to hostname -s and target the wrong host files.
- host files and .bak-*/substrate.* are excluded/denied by construction.

Refusal conditions make "logic must not be harmed" checkable rather
than decorative -- chiefly: absence on my machine is not absence, the
inference that produced the AGENTS.md:157 "exists nowhere" claim about
a file that is live on home.

Carries an explicit sunset (review-by 2026-08-29). The operator called
this temporary; an override with no expiry becomes permanent
regulation by default, which is the rot pattern this cleans up.

Office live skills now 31; repo mirrors live exactly (rsync -n clean).
Home's deploy is additive -- pulling this cannot disturb home's own
skills.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01PuLsYLGuWrw4K9Wv9PdHy8

---

## 2d747aa · 2026-07-29 · mail(home): ACTION-FIRST card — 4 steps, one screen

MACHINE<>MACHINE: office -> home.

HOME, DO THIS:
  1. git pull && bash deploy.sh          <- safe, deploy never deletes
  2. rm -rf ~/.claude/skills/{hypatia-brief,gavel-ballot}   <- both dead
  3. DO NOT delete normalizer.py/registry yet. config.zsh:27
     evals it at login; port to inline exports and verify a shell first.
  4. deploy before sync, every session, both directions.

Full card: _mail/maxwell/inbox/office.ACTION-FIRST.2026-07-29.md

Prior three commits were evidence-dense -- correct content, wrong shape
to act from. This separates the instruction from the proof.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01PuLsYLGuWrw4K9Wv9PdHy8

---

## b4268a8 · 2026-07-29 · fix(skill): multihost — lead with an ACTION-FIRST card, not evidence

MACHINE<>MACHINE: office -> home. Doc-only, safe to pull.

Operator feedback: the first three commits sent home correct content in
the wrong shape. Four documents of evidence, and the four things home
must actually DO were buried inside them.

Adds Lane 0 — the action card — ahead of the existing message/file
lanes. One screen, numbered imperatives in execution order, paste-ready
commands, hazards inline, evidence only as a pointer at the bottom.
Mandatory whenever the other side has more than one action.

Acceptance test now in the skill: can they execute this without opening
anything else? If no, it is not a card yet.

Run-order corrected — the card is written BEFORE the commit, because
the commit body is built from it.

Instance of this shape already pushed for home: 2d747aa.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01PuLsYLGuWrw4K9Wv9PdHy8

---

## 44b9c71 · 2026-07-29 · feat(skill): multihost — commit body becomes the receiver's prompt

MACHINE<>MACHINE: office -> home
ACT: no action. Read only when you next run /multihost.
CARD: none (superseded card for home is office.ACTION-FIRST.2026-07-29.md)
SAFE-PULL: yes — doc-only, no live file touched on either machine
BLOCKED: none
GATE: autonomous-ok

This commit's own header is the first instance of the format it adds.

Operator design: the commit message is not documentation the other side
reads, it is the prompt the receiving agent boots from. git pull is the
delivery. Git is already the bus — authenticated, totally ordered,
durable, and the diff arrives welded to the instruction. No daemon, no
queue, no new transport. For the cross-machine case this replaces
/drop-brief, which needed a push to cross machines anyway.

Adds to the skill:
- sender header: MACHINE<>MACHINE / ACT / CARD / SAFE-PULL / BLOCKED / GATE
- receiver retrieval, oldest-first, with a consumed marker at
  ~/.local/state/multihost/consumed. That path is deliberate: sync.sh
  covers only ~/.claude, ~/.gemini and ~/.config/zsh, so a consumption
  marker can never travel to the other machine and mark its own
  messages already read.
- superseded-prompt rule: newer wins, receiver names what it dropped.

The guard, which is the part that matters:

Push access must not become execution on the other host. A commit body
arrives with no author present to challenge it. So a prompt is a
proposal, not a command. GATE defaults to operator-present whenever it
is absent, and anything that deletes, moves, or overwrites live files
or touches canon must carry operator-present. The receiver runs its own
refusal checks against the instruction regardless of what the sender
asserted -- the sender cannot see the receiver's machine, which is the
entire reason this transport exists. ACT names intent only; commands
live in the card, where they can be read before they are run.

Retrieval verified against this session's four tagged commits.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01PuLsYLGuWrw4K9Wv9PdHy8

---

## b773079 · 2026-07-29 · mail(home): add step 5 — the git prompt bus is now live

MACHINE<>MACHINE: office -> home
ACT: after pulling, run /multihost at session start. Commit bodies addressed to you are prompts.
CARD: _mail/maxwell/inbox/office.ACTION-FIRST.2026-07-29.md
SAFE-PULL: yes — mail file only
BLOCKED: none
GATE: autonomous-ok

Adds the receiver half to home's action card: retrieval command,
consumed marker, and the binding meaning of GATE.

GATE is the line that matters. operator-present means summarise and
wait for @majkee, never self-execute. Missing GATE reads as
operator-present. Office cannot see home's machine, so a prompt from
here is a proposal -- home refuses anything that would break home
regardless of what office asserted, and the same holds in reverse.

Channel is reciprocal from now on: office reads home's commit bodies
by the same command.

Known gap: delivery is pull-based. The receiver only sees a prompt when
it runs /multihost. No wake-up signal exists. If that becomes painful
the fix is a saddle pre-step on both seats, not a daemon.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01PuLsYLGuWrw4K9Wv9PdHy8

---

## a7e1b0f · 2026-07-29 · START HERE — home entry point (supersedes all prior office prompts)

MACHINE<>MACHINE: office -> home
ACT: run the bootstrap below in order. Do not lead with /multihost — it is not installed on home yet.
CARD: _mail/maxwell/inbox/office.ACTION-FIRST.2026-07-29.md
SAFE-PULL: yes — deploy.sh is rsync -a with no --delete, nothing of home's is removed
BLOCKED: do NOT delete normalizer.py or harness.machine-project-registry.json before porting
GATE: operator-present

SUPERSEDES: 2f3e89c a4a4abc 2d747aa b4268a8 44b9c71 b773079
Read those only as evidence. This commit is the instruction.

BOOTSTRAP — the first three steps are ordered for a reason:

  1. cd ~/ia-sync && git pull
  2. bash deploy.sh
       ^ this is what installs the multihost skill onto home.
         It is NOT available before this runs.
  3. START A NEW CLAUDE SESSION.
       ^ skills load at session start. Deploying mid-session does
         not make /multihost appear. Restart, then it exists.
  4. /multihost   (now it works — and the marker is empty, so it
                  will replay this session's prompts oldest-first)

If you want to act before step 3, read the CARD above — it is a plain
file, readable straight after step 1, and it carries every command.

THEN, in order:

  5. rm -rf ~/.claude/skills/hypatia-brief ~/.claude/skills/gavel-ballot
       hypatia-brief: @Hypatia retired to @Oraculum, absent office+repo
       gavel-ballot:  absorbed into gavel-loop 2026-07-27
       Keep and sync your other four: fetch-agent-docs, claude-creator,
       fetch-ollama-docs, fetch-qwen-docs.

  6. Deploy BEFORE sync, every session, both directions. sync.sh runs
     --delete on claude/skills/ AND claude/commands/. A sync from a
     machine that has not pulled wipes the other side's work. There is
     no dry-run flag; preview with:
       rsync -a --delete -n -i ~/.claude/skills/ ~/ia-sync/claude/skills/

  7. THE HAZARD. home's config.zsh:27 still runs
       eval "$(python3 "$NORMALIZER" "$MACHINE_NAME" "$REGISTRY_FILE")"
     Delete the registry or normalizer before porting and home's project
     switcher loses every PROJECT_* path at next login. Order:
       a. python3 ~/.config/zsh/normalizer.py home \
            ~/.config/zsh/harness.machine-project-registry.json
       b. port those exports INLINE into config.zsh (office shape: config.zsh:23-24)
       c. delete the eval line + REGISTRY_FILE / NORMALIZER vars
       d. VERIFY: zsh -ic 'echo $MACHINE_NAME; type fo im psd ltp lrv sess'
       e. only then: mv registry + normalizer.py into archive/
     Do NOT port LRV->larva.zsh or SES->session-helpers.zsh, both archived 07-07.
     Do NOT sync the registry up at any point.

GATE is operator-present because step 5 deletes and step 7 rewrites
home's shell bootstrap. @majkee is walking over to home now and will be
in the seat. Summarise and confirm with him before executing 5 or 7.
Steps 1-4 and 6 are safe to run on sight.

Office state: origin/main, clean, nothing ahead or behind. normalizer.py
and the stale config.home.zsh archived here; office shell verified green
after the moves. Office's consumed marker is set, so office will only
see NEW prompts from home — reply by committing with this same header.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01PuLsYLGuWrw4K9Wv9PdHy8

---

## ad1b54b · 2026-07-29 · fix(skill): multihost is project-local, not global — corrects a7e1b0f

MACHINE<>MACHINE: office -> home
ACT: bootstrap is now shorter. git pull alone delivers /multihost — it does not ride deploy.sh.
CARD: _mail/maxwell/inbox/office.ACTION-FIRST.2026-07-29.md
SAFE-PULL: yes — moves a skill file, touches no live host config
BLOCKED: none
GATE: autonomous-ok

CORRECTS a7e1b0f, which told you deploy.sh installs multihost and that
you must restart after deploying. Wrong. Everything else in a7e1b0f
stands -- especially the normalizer hazard at its step 7.

Corrected bootstrap on home:
  1. cd ~/ia-sync && git pull      <- this alone delivers /multihost
  2. new session, CWD in ~/ia-sync <- skills load at session start
  3. /multihost
deploy.sh is still required, but for the OTHER three skills
(cold-start-card, gavel-loop, drop-brief) and the zsh leg -- not for
multihost.

Moved:
  ~/.claude/skills/multihost/        -> deleted (global live)
  claude/skills/multihost/           -> deleted (sync payload)
  .claude/skills/multihost/SKILL.md  -> added   (project-local)

Operator caught the misplacement. It was wrong on three counts:

- Every path I describe is ia-sync's: sync.sh, deploy.sh, sync.deny,
  journal, _mail. The skill is useless in any other project, so as a
  global it burned context in every unrelated session on both machines.
  Global CLAUDE.md is explicit: separate global agent behavior from
  project-specific constraints.

- As a global it depended on deploy.sh to reach the other machine,
  which is the bootstrap gap flagged in a7e1b0f. Project-local removes
  the gap rather than documenting it: the skill lives inside the repo,
  so git pull IS the delivery. The transport now delivers itself by the
  same mechanism it describes.

- It is reachable only with CWD in ~/ia-sync, which is exactly where
  AGENTS.md says this seat opens. Scope matches use.

Global skill set back to 30/30, live == sync payload, unchanged.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01PuLsYLGuWrw4K9Wv9PdHy8

---

## 4209637 · 2026-07-30 · docs(zsh): close the UNCERTAIN table; record the PHP/composer split

MACHINE<>MACHINE: office -> home
ACT: none now. Read when you pick up the zsh leg — it says which files office will NOT touch.
CARD: none
SAFE-PULL: yes — documentation only, no file moved, no live config changed
BLOCKED: none
GATE: autonomous-ok

Operator call: a grep-level wiring trace from the zsh perspective is
sufficient to state office's status. Home verification is not required
for that. @zenith-zsh and @Eagle traced all six remaining UNCERTAIN
entries; every one is unreachable from office's live sourcing chain.

RESOLUTION IS NOT REMOVAL -- and this is the part that matters for home.

ai-lifecycle.zsh, shared-toolkit.zsh, setup-docker.sh, ai-agents.registry
.json, tasks.js and archive/larva are all dead on office. I archived NONE
of them. They are home-owned files that office merely stores, and the
repo is home's delivery path. Archiving them from office would bury
home's own files under archive/ and degrade home's deploy for zero
office benefit.

That is the difference from normalizer.py, where BOTH machines are
retiring the mechanism -- there, archiving was right. Here it would be
office deciding the disposition of home's property. Disposition
recorded instead: office = store, never source. Home owns.

Recorded the PHP/composer split as the root cause of most home-only
files, because it explains WHY rather than just listing:
  home   PHP 7.4 = Docker image, no native CLI; composer wrappers are
         containers; PHP is selected by WHICH CONTAINER IS CALLED
  office PHP 7.4 and 8 run as two live FPM services simultaneously;
         nginx routes by socket (valet74.sock / valet.sock); php74/php8
         only START services (system/office.php-switch.zsh:32-59)
Anything Docker-shaped in this tree is home's, by consequence.
setup-docker.sh is home-only BECAUSE of this split; shared-toolkit.zsh
is home-only for an unrelated reason (rsync mirror for ~/www/session).

Corrected in guides/home.md: it claimed office project paths are
/media/data/projects/. Wrong since 2026-07-07 when that mount was
declared an empty husk and office repointed to ~/projects/. Same class
of error as AGENTS.md:157 -- a doc asserting a fact about the other
machine that stopped being true. Guide is dated 2026-06-28 and predates
both that repoint and the normalizer retirement.

New KNOWN BROKEN section, one entry, deliberately NOT fixed:
projects/larva.zsh:31 sets LARVA_SCRIPTS_DIR to ~/.config/zsh/larva,
which does not exist on office, so its broadcast/consult/slices/laika
aliases point at nothing. Latent, not fatal -- larva.zsh loads on demand
via lrv, not at startup. Left alone because repointing it would revive a
buried project. Operator decides: repoint to archive/larva/, or strip
the alias block.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01PuLsYLGuWrw4K9Wv9PdHy8

---

## af8cd5d · 2026-07-30 · fix: repo-first direction; correct shared-toolkit + larva disposition

MACHINE<>MACHINE: office -> home
ACT: none. Corrections to yesterday's doc pass; read if you touch the zsh leg.
CARD: none
SAFE-PULL: yes — docs + skill text only
BLOCKED: none
GATE: autonomous-ok

Operator caught me editing ~/.config/zsh live and copying UP to the
repo -- the scrape direction, one turn after I diagnosed it as the root
cause of every failure in this session. Diagnosed the anti-pattern, then
performed it.

Corrected in the skill: injection discipline now says repo-first, deploy
outward, never live-first. Only exception is a first-time import of a
file that exists solely live. This whole commit was done that way: edited
ia-sync, ran deploy.sh, verified the shell, then committed.

Deploying also reproduced the MACHINE_NAME trap live. Run from a
non-interactive bash, deploy.sh fell back to hostname -s and looked for
config.hruzam-120922.zsh. It refused and listed the available host
configs rather than deploying the wrong host's file -- the script's guard
is well built. Re-run under zsh -ic resolved MACHINE_NAME=office and
deployed correctly, with backups of config.zsh and .zshrc.
Shell verified after: all six switchers plus php74/php8/phpst.

Content corrections from the operator:

shared-toolkit.zsh -- I filed it as "home-only for an unrelated reason".
Wrong framing. It mirrors dot-folders to visible folders because older
Claude web browsers could not see dotted paths. Claude Code reads
dotfiles natively now, so the reason it exists is gone. It is also
larva-adjacent (~/www/session). It is an obsolete workaround, a
retirement candidate on BOTH machines -- not a live home-owned file.

larva -- I left a "decide: repoint or strip" question. There is no
question. The larva era was mostly home's and is dead; newer larva
associations exist but stay unpublished until the machines are ~1:1, or
at least level on project and agentive synchronicity. Reframed from
open decision to PARKED-pending-convergence. Rule of thumb recorded:
larva-adjacent wiring is stale by default, do not revive.

guides/home.md -- staleness is systemic, not the one path line I fixed.
The guide predates the machine-convergence work (~2026-05) where office
was reframed onto home's partition layout and ~/ placement to make the
machines as similar as possible. Every "home vs office difference" claim
in it is therefore suspect. Added a banner saying so and pointing at the
current authorities, rather than rewriting a guide home owns.

Also folded the "audit clean duplicates" block the operator had flagged
in AGENTS.md, preserving the concurrency-guard facts (full path
~/.shared/implementation.concurrency-guard.zsh, the 3-agent cap, the
line-260 error) into the ai-lifecycle row instead of dropping them.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01PuLsYLGuWrw4K9Wv9PdHy8

---

## 1770785 · 2026-07-30 · plan: surgical-table doctrine of record; zsh lighthouse points at the table

MACHINE<>MACHINE: office -> home
ACT: answer two facts in your first reply — does ~/.majkee exist on home, and is codex CLI installed there. Then read session/plan/surgical-table.plan.md.
CARD: session/plan/surgical-table.plan.md
SAFE-PULL: yes — plan doc + one doc line in zsh/AGENTS.md
BLOCKED: none
GATE: autonomous-ok

Vocabulary lock: ia-sync IS the surgical table -- the one place cuts
are made, the like-composer for both machines. Name stays ia-sync
(operator: should have been ai-sync, played too far; renaming buys
nothing and breaks everything).

Landed now: one line atop zsh/AGENTS.md -- "Truth is living THERE
(~/ia-sync)". Deployed repo-first, shell verified.

Planned, gated (see the plan file):
1. banner in every named guide -- temple ratification first
2. zenith-zsh repoints to the table + .deployed stamp probe on host
4. codex sync leg -- office has ~/.codex live (0.145.0, 07-25, smoke
   GREEN); leg design done: sync config.toml/hooks.json/skills, deny
   auth.json/installation_id/all state. Build waits on WS5 gavel.
5. ~/.majkee leg -- REALITY CHECK: the folder does not exist on office.
   Design ready (sync like ~/.claude, deny export/, registry-shaped
   majkee.deny). Blocked on home confirming it exists there.

Registry generalization: per-leg deny files (sync.deny, codex.deny,
majkee.deny), one loader -- exclusions become data, not code.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01PuLsYLGuWrw4K9Wv9PdHy8

---

## 6e2a3e6 · 2026-07-30 · feat(sync): ~/.majkee leg + surgical-table banner in all named guides

MACHINE<>MACHINE: office -> home
ACT: after pull+deploy, run sync.sh once on home — it will carry ~/.majkee into the repo (export/ excluded). Verify majkee.deny loaded in its output.
CARD: session/plan/surgical-table.plan.md
SAFE-PULL: yes — new leg is [ -d ]-guarded and deploy stays additive
BLOCKED: none for this; codex leg still waits on WS5 (see below)
GATE: operator-present

~/.majkee leg (operator provided home's tree):
- sync.sh: guarded leg, rsync --delete with majkee.deny registry;
  skips loudly where the folder is absent (verified on office)
- deploy.sh: additive leg, export/ never entered the repo so deploy
  cannot touch process data
- majkee.deny: registry-shaped exclusions (export/ = tcr+repomix
  outputs). config/ WITH the tcr/repomix configs DOES sync.
- .gitignore: /majkee/export/ belt-and-suspenders

Banner (operator blessed, temple already partly informed): applied to
guide-for-builder, guide-for-user, home.md, office.md, index.md.
Process claims only -- edit-in-ia-sync + two reality checks (git log =
intent, rsync -n = reality). Deployed outward, live verified.

Codex roster read (Eagle over temple): WS5 STILL PENDING -- WS4a/4b
blocked on majkee's stone + pad intent; model pin DRAFT; staged
artifacts untouched in .larva/agents-staging. Vega seat persists,
vendor Gemini->Codex per 0005 A1. Codex sync leg stays design-only.
Constraint recorded: gemini exit-2 guards in ai/ are loud-parked
evidence, never prune them via deny-list work.

Confession in the ledger: while testing the majkee skip-path I ran the
FULL sync.sh with undeployed banner edits sitting in the repo -- the
scrape overwrote them with bannerless live copies, exactly the hazard
the banner warns about. Caught by git status, re-applied, deployed
FIRST, then committed. The doctrine keeps proving itself on its author.

GATE operator-present because home's first sync.sh run after this pull
is the moment ~/.majkee enters the repo -- majkee should watch that
output once before it becomes routine.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01PuLsYLGuWrw4K9Wv9PdHy8

---

## 6fa44b6 · 2026-07-30 · feat(agents): codex bed mounted via the surgical table; staging retired

MACHINE<>MACHINE: office -> home
ACT: pull + deploy gives home the codex relay cards and the codex-run wrapper. If codex CLI is not installed on home yet, the cards will sit dormant — harmless.
CARD: session/plan/surgical-table.plan.md (third-pass status at top)
SAFE-PULL: yes — three new files, additive on every leg
BLOCKED: none
GATE: autonomous-ok

Operator gavel (live, MANNED): .larva/agents-staging is old, blessed
over all -- deleted completely. What existed there and mattered (the
codex bed) moved onto the surgical table first:

  claude/agents/codex-coder.md       relay coder -> Codex CLI
  claude/agents/codex-crosscheck.md  blind-triangulation relay (0005 A1)
  zsh/ai/codex-run.zsh               canonical headless wrapper (+x,
                                     zsh -n clean; handles stdin-hang
                                     #20919 and silent-exit #19945)

Deployed on office; live verified. Died with the staging folder:
gemini-subagents/ June copies (astrobley, orby, vega) -- frozen line,
live seats elsewhere, parked 2026-07-24.

This is the MOUNT half of WS5 executed ahead of its bookkeeping half,
by operator's word. Still open for WS5 proper: roster rows, model-pin
gavel (cards ship with DRAFT pins: coder sonnet / crosscheck haiku),
WS4a stone, WS4b pad intent. Official channel updated so agents reading
the runcard are not stranded on stale staging references:
reposoma/maintenance/codex-line/note.staging-retired.2026-07-30.md

Perspective note the operator named: agents trusting only confirmed
official channels would still see "staged, pending WS5". The note in
codex-line/ is the bridge until WS5's bookkeeping lands.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01PuLsYLGuWrw4K9Wv9PdHy8

---

## c648895 · 2026-07-30 · service


---

## c0d525a · 2026-07-30 · fix(zsh): zshrc.home 471 -> 51 lines; monolith archived, credential scrubbed

MACHINE<>MACHINE: office -> home
ACT: review the new zshrc.home BEFORE deploying on home. Then rotate or confirm-dead the fantasyobchod.cz FTP credential (see SECURITY below). Then sync/deploy home as planned.
CARD: none — this commit body is the review sheet
SAFE-PULL: yes — nothing deploys until home runs deploy.sh; old file preserved in archive/
BLOCKED: none
GATE: operator-present

SECURITY, read first: the monolith carried a PLAINTEXT FTP password for
fantasyobchod.cz (user defaultfan) in a comment block at line 424 --
pushed to github in c648895. Repo is PRIVATE (verified via gh), so
exposure is contained, but the credential now lives in git history on
the remote. The archive copy here is REDACTED; history still has it.
Cheapest correct fix: rotate the credential (or confirm the FTP account
is dead -- it is globalFantasyobchodStartScript-era). History rewrite is
possible but needs both machines coordinated; rotation makes it moot.
Also: sync.sh's secret scan never saw this because the file was
hand-added, not synced -- scan-on-commit is an open gap, noted below.

THE REPAIR -- home's .zshrc rebuilt in office's shape (51 lines):
manjaro block · zsync · source config.zsh + project-switcher +
git-lifecycle · small local-alias set · PATH. Same stage as office.

Kept (home-valid): patch/gpt stash utils, dbup, dbfo (creds match
machine facts), hasz, svt history snapshot, npm+local PATH.

Cut, with reasons -- full original at
zsh/archive/zshrc.home.legacy-2026-07-30.zsh (only edit: password
redacted):

- env-sync.zsh source line: deprecated 2026-06-30, archived; the old
  file still sourced it on every login
- valet aliases (va74, p7, p8, globalFantasyobchodStartScript): valet
  is the OFFICE mechanism; home is nginx+docker. Dead on home, and
  valet-use is forbidden-broken on Arch anyway (guides/office.md:76)
- /media/data/projects paths (psdvs, psdvs_zsh, psd_, mkay): office's
  dead mount, declared empty husk 2026-07-07 -- cross-machine
  contamination inside HOME's zshrc, third sighting of this pattern
- wmctrl/X11 family (dsk, ffoxLocal/Production/ChatGpt,
  firefox_virtual_displays): home is Wayland (established in
  pad.1-arch-repair this same day) -- wmctrl is X11-only, dead
- switch_php(): update-alternatives is a Debian mechanism, not Arch --
  never worked on either machine
- DailyScrum machinery (ExtractBetweenTags, AddDailyScrum, TestVypisu,
  gd1/gt1/gd2/gt2/gnt* aliases): StroMy/FO txt-driven git flow,
  pre-harness era; git-lifecycle.zsh is the living successor
- larva-adjacent (## larva block, lvdv, colafi() with dot.shared skill
  copies): larva-adjacent = stale by default (operator rule 2026-07-29)
- FO one-offs against old paths (~/www/fantasyobchod_moje_pozn, t12,
  t13, fup/kup filezilla, msrc hardcoded grep): pre-imago_cz paths
- pacman utilities (update_conflicted_files, __download_packages):
  Arch-VALID and possibly wanted -- parked in archive, candidates for
  archx/ engine if operator wants them promoted; not silently dropped
- duplicate PATH exports (3x npm-global), duplicate heu/gpl/mig/dbps
  definitions shadowing each other

Open (carried): sync.sh secret scan does not run on hand-added files;
a pre-commit scan hook or CI grep is the fix, sized for a later pad.

Home review question, honestly held: some cut aliases may be muscle
memory (dsk was used inside the pad's own aliases; ord, mm). The
monolith is in archive/ verbatim -- pull any survivor back into the
LOCAL ALIASES block during review, that is what the section is for.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01PuLsYLGuWrw4K9Wv9PdHy8

---

## d75efb8 · 2026-07-30 · fix(zshrc): zsync now runs the discipline order — pull --rebase, deploy, sync

MACHINE<>MACHINE: office -> home
ACT: use plain `zsync` for your leveling run — it now does the whole ritual in the right order. Correct sequence: pull --rebase -> deploy.sh -> review -> sync.sh -> push.
CARD: none
SAFE-PULL: yes — alias comment + reorder only
BLOCKED: none
GATE: autonomous-ok

Operator caught my mis-ordered instruction ("pull -> sync -> deploy")
in the previous commit's summary -- that is the documented trap:
a behind machine syncing first scrapes its stale live tree over the
fresh repo, and --delete erases the other side's skills/commands.
Deploy-before-sync is the hard precondition (journal 2026-07-28).

The zsync alias itself encoded the same trap (pull + sync, no deploy).
Both host zshrc files fixed: zsync = pull --rebase && deploy.sh &&
sync.sh && git status, with the reasoning in a comment above it so the
next reader knows WHY the order is load-bearing.

And yes: --rebase, always -- home may carry local commits (c648895
pattern); rebase keeps the machine<>machine channel linear, no merge
knots in the prompt bus.

Office deployed + verified (zsync resolves, shell green).

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01PuLsYLGuWrw4K9Wv9PdHy8

---

## 39b6fa2 · 2026-07-30 · pad(maintenance): pad.2 — home receive + deploy, run and verified

Records the 2026-07-30 home sitting end to end: /multihost receive (8
prompts, 6 superseded), dead-skill retirement, the sync.sh resurrection
race, the registry/normalizer reversal by decision 0008, three swords,
and the deploy itself.

Deploy RUN and VERIFIED: MACHINE_NAME=home, six switchers, 28 PROJECT_*.
Host legs were no-ops because zshrc.home was imported first — that was
the whole point of the import-before-deploy order.

STEP 8 added post-deploy: gemini-line PARKED printed twice. Two source
paths (base.zsh:70 and keyboard.zsh:22 via base.zsh:17) into an engine
with no source guard. NOT a deploy regression — the park block arrived
in 0046a45 and the deploy merely delivered it; the doubling is
pre-existing and office has it too.

Three self-corrections recorded deliberately — a pad that logs only
findings and not the wrong turns is a worse record:
- "all six switchers resolve" checked functions, not paths; 3 of 6 broken
- home's empty PHP74_BIN/PHP8_BIN called a gap; they are empty by design
- first sync.deny exclude test word-split and showed secrets.zsh as
  syncable; rebuilt as an array, it is correctly denied

Charter note in the header and index row: this pad is ia-sync content,
not OS/desktop state, so it stretches maintenance/README.md's stated
scope. Flagged rather than quietly widened — operator decides whether to
widen the clause or relocate the pad.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_015rpDo5YjqcYozEMSR3QowX

---

## 22037b8 · 2026-07-30 · retire(zsh): ai-lifecycle.zsh — both halves, verified green on home

MACHINE<>MACHINE: home -> office
ACT: none. Home-side retirement, already complete and shell-verified. Read if you touch zsh/AGENTS.md.
CARD: none
SAFE-PULL: yes — office never sourced this file; archiving it here changes nothing on office
BLOCKED: none
GATE: autonomous-ok

Operator call 2026-07-30. Retired in ONE pass so no contradiction is
left behind: repo archive + live removal + source line stripped. Doing
only the repo half would have added a tenth entry to the archived-here/
alive-there contradiction set that arms the sync.sh resurrection race.

  zsh/ai-lifecycle.zsh   -> zsh/archive/          (git mv)
  zsh/config.home.zsh:119 source line             REMOVED
  ~/.config/zsh/ai-lifecycle.zsh                  removed on home (.bak-2026-07-30 kept)

zsh/AGENTS.md:93 CORRECTED. It claimed "DEAD — no live source
directive; only caller was config.home.zsh:113, archived 2026-07-29."
Both halves false, and office-blind in exactly the way AGENTS.md:157
was: office archived ITS OWN copy of config.home.zsh and inferred the
caller was gone everywhere. Home's live config.zsh:119 sourced it at
every login, providing four live functions (autonomy-mode, ai-session,
track, ai-agents) plus alias tasks.

Second false claim in the same row: "concurrency guard (home-only,
still valid there)". ~/.shared/ does not exist on home either — the
agent-concurrency cap and nesting detection have never run on either
machine. The bare source at line 260 (no [[ -f ]] guard) errored at
every home login; that error is now gone with the file.

Guard artifact recovered from ~/.remote/.shared/ and preserved at
zsh/archive/implementation.concurrency-guard.zsh. Operator's call if it
is ever wanted again: build fresh, do not revive.

Evidence before acting: zero callers for all four functions anywhere in
the tree. Verified after: MACHINE_NAME=home, six switchers resolve,
28 PROJECT_* exports, exit 0, and the :260 error absent.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_015rpDo5YjqcYozEMSR3QowX

---

## 2aa2591 · 2026-07-30 · harden(deploy): backup every cp leg, drop machine-local files, add --dry-run

MACHINE<>MACHINE: home -> office
ACT: review before your next deploy — this changes deploy.sh behaviour on office too. Try `bash deploy.sh --dry-run` first.
CARD: none — this body is the review sheet
SAFE-PULL: yes — nothing runs until you invoke deploy.sh; --dry-run writes nothing
BLOCKED: none
GATE: operator-present

Operator gaveled options 3 + 1 + 5 from a five-option table.

3 — STOP DEPLOYING three machine-local files:
      settings.local.json  ".local" IS Claude Code's machine-scope
                           convention; deploying it made a machine-local
                           file global. Verified against the docs: there
                           is no user-level .local tier at all, so the
                           copy we were shipping is likely inert.
      houston.goal         an autonomous-run mission. Office's goal must
                           not land on home's disk and boot home's
                           Houston into it.
      recorder.index.json  session memory index, per-machine by nature.
    All three were byte-identical across machines, which is exactly what
    hid the problem.

1 — backup_live() now runs on EVERY single-file leg via a new
    copy_file() helper. Nine cp legs previously overwrote live files
    with no backup, while deploy.sh:12-14 explained why that is unsafe —
    the guard existed and was wired only to config.zsh and ~/.zshrc.
    Home lost its "model": "claude-fable-5[1m]" pin to office's "opus"
    on today's deploy through exactly this hole; only a hand-taken
    backup saved it.

5 — --dry-run / -n. Neither script had a preview mode, so the only way
    to see a deploy's blast radius was to run it. rsync legs get -n -i;
    cp legs report CREATE / UPDATE / same. Verified on home: bash -n
    parses, dry run writes nothing.

Option 4 (0-byte stub guard) deliberately held — option 3 removes the
file class where stubs were likeliest. gemini/config/mcp_config.json is
still 0 bytes in the repo; first machine to populate an mcp config would
have lost it. Now at least it is backed up.

Also in this commit: ai/gemini-processor.sh warns ONCE per shell.
Two legitimate source paths reach that engine — ai/base.zsh:70 directly
and ai/keyboard.zsh:22 via ai/base.zsh:17 — so the park notice printed
twice at every startup on both machines. Neither path is redundant
(base.zsh is the loader per ai/README.md:49; keyboard.zsh needs _gai_*
if sourced standalone), so this is a guard, not a deletion. The return 2
still fires on every source — park semantics unchanged.

Known-open, NOT in this commit: sync.sh's secret scan cannot see quoted
keys. Tested — `\bpassword\s*[=:]` does not match `#"password": "..."`,
because a quote sits between the word and the colon. That is why today's
plaintext FTP credential passed; "the file was hand-added so the scan
never ran" is only half the diagnosis. Fix is
\b(password|passwd|secret|token|api[_-]?key)\b\s*["']?\s*[=:] and it is
queued separately.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_015rpDo5YjqcYozEMSR3QowX

---

## 511de2f · 2026-07-30 · pad(maintenance): pad.2 STEP 5 — correct two false claims of my own

Both errors were bad shell commands, not bad reasoning, and both are
left visible in the pad rather than rewritten. The failure mode is the
useful part of the record.

1. "No zshrc.* existed in the repo for EITHER machine; office is equally
   exposed." False. zsh/zshrc.office has been tracked since 2026-07-29;
   only home's was missing. The check was `ls -l zsh/zshrc* zshrc*` —
   zsh's nomatch on the SECOND pattern aborted the whole command, and I
   read the abort as "neither exists."

2. "Secret-scanned first: 0 hits." False, and this one cleared a live
   credential for commit. Pattern was case-sensitive uppercase with no
   -i; the fallback long-string check was piped through head -10, so I
   stopped reading a truncated set after seeing only paths and aliases.

Also records: sync.sh's own scan would have missed it too (quote-blind
pattern, tested), and the operator's call that the fantasyobchod.cz FTP
account is DEAD — confirm-dead, not rotate.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_015rpDo5YjqcYozEMSR3QowX

---

