#!/usr/bin/env zsh
# =============================================================================
# KEYBOARD.ZSH — AI interactive surface: Gemini seats · Claude Code RC
# =============================================================================
# Location: ~/.config/zsh/ai/keyboard.zsh
# Sourced by: ~/.config/zsh/ai/base.zsh (interactive shells + git hook)
#
# Do NOT call this from bare bash or per-agent scripts — use gemini-processor.sh directly.
# Guard at top short-circuits for any non-zsh runtime.
#
# Gemini per-agent scripts (orby.sh, bluebottle.sh) are
# EXECUTED, never sourced. They handle interactive + headless modes internally.
# Kebab shims in PARTITION 3 call them directly by path.
# (vega.sh / astrobley.sh RETIRED 2026-07-31 — chairs vendor-shifted to Codex, 0005 A1;
#  archived in reposoma raw.substrate/archive/. Codex relay: guides/codex-relay.contract.md)
#
# Claude tooling (rc.sh) is EXECUTED via bash; aliases in PARTITION 8.
# =============================================================================

[[ -n "$ZSH_VERSION" ]] || return 1   # guard: zsh only

# ── source dependencies ──────────────────────────────────────────────────────
# gemini-processor.sh: common _gai_* REST + CLI helpers (bash/zsh compatible)
[[ -f ~/.config/zsh/ai/gemini-processor.sh ]] && source ~/.config/zsh/ai/gemini-processor.sh

# ── model constants (per handoff 2026-07-03) ─────────────────────────────────
_GAI_MODEL_PRO="gemini-2.5-pro"      # (ex-Vega tier — seat retired 2026-07-31; kept for engine compat)
_GAI_MODEL_FLASH="gemini-2.5-flash"  # Orby · Bluebottle: stable throughput
_GAI_MODEL_IMPL="gemini-3.5-flash"   # (ex-Astrobley tier — seat retired 2026-07-31; kept for engine compat)

# =============================================================================
# PARTITION 1: General CLI
# =============================================================================
alias g="gemini"
alias g-ver="gemini --version"
alias g-help="gemini --help"

alias agy-ver="agy --version"
alias agy-help="agy --help"

# =============================================================================
# PARTITION 2: Safety / YOLO Modes
# =============================================================================
alias g-yolo="gemini --approval-mode yolo"
alias g-skip="gemini --skip-trust"

alias agy-yolo="agy --approval-mode yolo"
alias agy-skip="agy --skip-trust"

# =============================================================================
# PARTITION 3: Kebab shims → per-agent scripts
# Scripts handle dual-mode: no-arg = interactive, arg = headless (-p flag).
# Scripts are EXECUTED as child processes; shebang is honored by bash subprocess.
# =============================================================================
alias gemini-bluebottle="~/.config/zsh/ai/bluebottle.sh"
alias g-bluebottle="~/.config/zsh/ai/bluebottle.sh"

alias gemini-orby="~/.config/zsh/ai/orby.sh"
alias g-orby="~/.config/zsh/ai/orby.sh"

# vega / astrobley shims retired 2026-07-31 — chairs vendor-shifted to Codex (0005 A1)

# =============================================================================
# PARTITION 4: agy wrappers
# @name selector: untested on agy — omitted until confirmed.
# Model: not pre-lockable on agy — set in-session via /model.
# Engine: ~/.config/zsh/ai/gemini-processor.sh (sourced via base.zsh PARTITION 8)
# Bodies (agy-orby) live in the engine.
# (agy-vega / agy-astro / agy-astro-yolo retired 2026-07-31 — chairs → Codex; engine
#  bodies in gemini-processor.sh are live-only legacy, cleaned by kraken pass.)
# =============================================================================

# =============================================================================
# PARTITION 5: retired 2026-07-11 — Gemini Epoch seat killed (accidental
# cross-line seat; @Epoch lives on the Claude line only). Numbering kept stable.
# =============================================================================

# =============================================================================
# PARTITION 6: Hygiene
# Engine: ~/.config/zsh/ai/gemini-processor.sh (sourced via base.zsh PARTITION 8)
# Bodies (gemini-fresh / agy-fresh) live in the engine.
# =============================================================================

# =============================================================================
# PARTITION 7: Help
# Engine: ~/.config/zsh/ai/gemini-processor.sh (gemini-agents-help) + claude.zsh (_ai_help)
# Bodies live in their scope engines; aliases below expose them on the panel.
# =============================================================================
alias ai-help='_ai_help'

# =============================================================================
# PARTITION 8: Claude Code — Remote Control
# Engine: ~/.config/zsh/ai/claude.zsh (sourced via base.zsh PARTITION 7)
# _RC_SCRIPT and _rc_stop body live in the engine.
# =============================================================================
alias rc-status="bash ${HOME}/.config/zsh/ai/rc.sh status"
alias rc-freya="bash ${HOME}/.config/zsh/ai/rc.sh freya"
alias rc-reposoma="bash ${HOME}/.config/zsh/ai/rc.sh reposoma"
alias rc-nabla="bash ${HOME}/.config/zsh/ai/rc.sh nabla-lab"
alias rc-stop='_rc_stop'

# =============================================================================
# PARTITION 9: Temple transport — operator panel
# Panel only: thin keys over gated engines (ai/temple-*, decision 0009).
# Engine functions (temple-mail, temple-mail-inbox, temple-mail-switch,
# temple-doorbell-run) are defined by base.zsh sourcing the temple family.
# =============================================================================
alias doorbell-run="temple-doorbell-run"
alias doorbell-smoke="zsh ~/.config/zsh/ai/doorbell-smoke.zsh --both"
alias doorbell-log="tail -n 30 ~/.config/zsh/temple-doorbell.log"
alias transport-selftest="zsh ~/.config/zsh/ai/temple-transport-selftest.zsh"
alias mail-pick="temple-mail-switch"
alias temple-mail-manage="zsh ~/.config/zsh/ai/temple-mail-manage.zsh"
alias cs-palette="zsh ~/.config/zsh/ai/cs-palette.zsh"
alias temple-cs-manage="zsh ~/.config/zsh/ai/temple-cs-manage.zsh"

# =============================================================================
# PARTITION 10: Temple utilities — tree-snapshot + temple-help
# =============================================================================
# tree-snapshot: function defined in temple-tree.zsh (sourced via base.zsh PARTITION 5)
# Direct call:  tree-snapshot <project-name>
# Configs:      ~/.config/zsh/registries/tcr/tcr.<project>.json
# Agents:       zsh -c "source ~/.config/zsh/ai/base.zsh && tree-snapshot <project>"
# Guide:        ~/.config/zsh/guides/toolbox.tree-converter.md
#
# temple-help: body in claude.zsh (sourced via base.zsh PARTITION 7)
alias temple-help='_temple_help'

# =============================================================================
# PARTITION 11: Project devenv transport — control panel
# Engine: ~/.config/zsh/ai/devenv.zsh (sourced via base.zsh PARTITION 6)
# Internal entry points (_bo_*, _fr_*, _devenv_help) live in the engine.
# Discipline: always pull --rebase BEFORE running devenv-sync (SYNC_DISCIPLINE.md).
# =============================================================================
alias fr-sync='_fr_sync'
alias fr-deploy='_fr_deploy'
alias fr-status='_fr_status'
alias bo-sync='_bo_sync'
alias bo-deploy='_bo_deploy'
alias bo-status='_bo_status'
alias devenv-help='_devenv_help'

# =============================================================================
# PARTITION 12: Global claviature — derived keys panel
# Engine: ai/keys.zsh (base.zsh P9) · body _keys
# =============================================================================
alias keys='_keys'

# =============================================================================
# PARTITION 13: Seat launchers — ai-metaterminal (terminal-layer seat)
# Engine: ~/.config/zsh/ai/claude.zsh (_metaterminal body, via base.zsh P7)
# =============================================================================
alias ai-metaterminal='_metaterminal'   # human-invoked only; --agent metaterminal + lifecycle frame

# =============================================================================
# PARTITION 14: editor-pin live keymap
# Engine: ~/.config/zsh/ai/claude.zsh (_pinkeys body, via base.zsh P7)
# Prints chord → command table from the INSTALLED Sublime keymap (live parse,
# never cached). Falls back to repo default if no installed keymap present.
# =============================================================================
alias pinkeys='_pinkeys'

# =============================================================================
# PARTITION 15: Project-map interactive surface
# Engine: ~/.config/zsh/ai/temple-project-surface.zsh (base.zsh P10)
# Bodies: _project_paths · _project_git_status · _project_commit_all · _project_pick_zle
# Source: TEMPLE_PROJECT_MAP (temple-project-map.zsh, P0 / base.zsh P3)
#
#   project-paths              — table of all project names + absolute paths
#   project-paths --plain      — "<name>\t<path>" per line  (pipe to agents)
#   project-paths --paths      — paths only, one per line   (xargs input)
#   project-git-status         — git dirty/clean + ahead/behind for every project
#   project-commit-all         — interactive day-phase batch commit across all projects
#   project-commit-all --dry   — preview what would be committed (no writes)
#   project-commit-all --push  — also push after each commit
#   Alt-p (^[p)                — fzf project picker → inserts path at cursor
# =============================================================================
alias project-paths='_project_paths'
alias project-git-status='_project_git_status'
alias project-commit-all='_project_commit_all'
alias project-help='_project_help'
bindkey '^[p' _project_pick_zle   # Alt-p — fzf project picker (inserts path at cursor)

# =============================================================================
# PARTITION 16: Zenith-ZSH — zsh config RAG assistant (Haiku)
# Agent:   ~/.claude/agents/zenith-zsh.md
# Engine:  ~/.config/zsh/ai/zenith-zsh.sh  (executed — no source)
# Log:     ~/.config/zsh/blessings/broken-wiring.json  (inconsistency log)
#
#   zenith-zsh              interactive chatbot — knows keyboard grammar, engine wiring,
#                           guides inventory; answers bash/zsh questions; read-only
#   zenith-zsh "question"   headless one-shot: builds preamble + sends question, exits
# =============================================================================
alias zenith-zsh='bash ${HOME}/.config/zsh/ai/zenith-zsh.sh'

# =============================================================================
# PARTITION 17: Command Palette — curses TUI command launcher
# Engine: ~/.config/zsh/ai/command-palette.zsh (base.zsh P11)
# Bodies: _command_palette · _command_palette_zle · _palette_help · _palette_refresh
# TUI + map are sibling deliverables built in parallel (ai/command-palette.py,
# palette.map at the zsh root) — may not exist on disk yet. Map auto-regenerates
# when any .zsh file is updated.
#
#   command-palette   run the palette; prints the selected command to stdout
#   Alt-k  (^[k)       ZLE widget — inserts selection at cursor
#   palette-help       this panel
#   palette-refresh    manual rebuild of the command map
# =============================================================================
alias command-palette='_command_palette'
alias palette-help='_palette_help'
alias palette-refresh='_palette_refresh'
bindkey '^[k' _command_palette_zle   # Alt-k — command palette (inserts selection at cursor)

# =============================================================================
# PARTITION 18: Codex tunnel
# Experimental runners MOVED 2026-09-22 → experimental/ scope (its own base.zsh +
# keyboard.zsh). exp-list / exp-run / ox-alpha* now live there, not here.
# =============================================================================

# tunnel (TABLE shape) — operator-gated, see raw.guides/tunnel/GUIDE.md
alias tun='zsh ~/.config/zsh/ai/tunnel-codex.zsh'
