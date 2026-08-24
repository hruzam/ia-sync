#!/usr/bin/env zsh
# =============================================================================
# BASE.ZSH — the ai/ signpost (decision 0009 L2)
# =============================================================================
# Location: ~/.config/zsh/ai/base.zsh
# Sourced by: config.zsh (interactive shells) + git post-commit hook (non-interactive)
# Contract: idempotent + side-effect-free on source — defines functions/aliases only,
#           never runs work or prints. Wires the whole ai/ scope in partition order.
# Partition/engine truth: guides/guide-for-builder.md §Architecture rules (LAW).
# =============================================================================

# -----------------------------------------------------------------------------
# PARTITION 1: Gemini agent surface
# -----------------------------------------------------------------------------
# keyboard.zsh: interactive aliases + wrappers for all Gemini seats
# Replaces: gemini-base.zsh (killed) + gemini-agents.zsh (killed)
[[ -f ~/.config/zsh/ai/keyboard.zsh ]] && source ~/.config/zsh/ai/keyboard.zsh

# -----------------------------------------------------------------------------
# PARTITION 2: Harness Freshness Checker Integration
# -----------------------------------------------------------------------------
# Interactive alias for card freshness checks
alias harness-stale="~/.config/zsh/ai/harness-check.zsh --debug"

# -----------------------------------------------------------------------------
# PARTITION 3: Temple Transport Family (0009 — ai/ namespace signpost)
# -----------------------------------------------------------------------------
# Sourced in dependency order; each script's guard short-circuits if already loaded.
# base.zsh MUST stay idempotent + side-effect-free (no work, no prints — sourced
# non-interactively by the git hook).
[[ -f ~/.config/zsh/ai/temple-project-map.zsh ]] && source ~/.config/zsh/ai/temple-project-map.zsh
[[ -f ~/.config/zsh/ai/temple-mail.zsh ]]        && source ~/.config/zsh/ai/temple-mail.zsh
[[ -f ~/.config/zsh/ai/temple-doorbell.zsh ]]    && source ~/.config/zsh/ai/temple-doorbell.zsh
[[ -f ~/.config/zsh/ai/temple-mail-inbox.zsh ]]  && source ~/.config/zsh/ai/temple-mail-inbox.zsh
[[ -f ~/.config/zsh/ai/temple-mail-switch.zsh ]] && source ~/.config/zsh/ai/temple-mail-switch.zsh

# -----------------------------------------------------------------------------
# PARTITION 4: Canon-integrity gate (adr-guard — 0009 L5 verify-it-fires)
# -----------------------------------------------------------------------------
# On-demand alias for the pre-commit canon-integrity gate.
# Run: adr-guard              → check staged diff (same logic as the hook)
#      adr-guard --deliberate-red  → sandbox smoke proof (both fail conditions)
alias adr-guard="zsh ${HOME}/.config/zsh/ai/adr-guard.zsh"

# -----------------------------------------------------------------------------
# PARTITION 5: Temple utilities
# -----------------------------------------------------------------------------
# tree-snapshot: project file-tree as JSON; configs in registries/tcr/
[[ -f ~/.config/zsh/ai/temple-tree.zsh ]] && source ~/.config/zsh/ai/temple-tree.zsh

# -----------------------------------------------------------------------------
# PARTITION 6: Project devenv transport engine
# -----------------------------------------------------------------------------
# _devenv_sync/_devenv_deploy/_devenv_status + per-project entry points (_bo_* / _fr_*)
# Aliases (fr-sync, fr-deploy …) are thin shims in keyboard.zsh PARTITION 11.
[[ -f ~/.config/zsh/ai/devenv.zsh ]] && source ~/.config/zsh/ai/devenv.zsh

# -----------------------------------------------------------------------------
# PARTITION 7: Claude Code RC engine + help functions
# -----------------------------------------------------------------------------
# _rc_stop + _temple_help + _ai_help; aliases (rc-stop, temple-help, ai-help) in keyboard.zsh.
[[ -f ~/.config/zsh/ai/claude.zsh ]] && source ~/.config/zsh/ai/claude.zsh

# -----------------------------------------------------------------------------
# PARTITION 8: Gemini interactive-surface engine
# -----------------------------------------------------------------------------
# agy-vega/orby/astro/astro-yolo + gemini-fresh/agy-fresh + gemini-agents-help
# Aliases in keyboard.zsh PARTITION 4, 6, 7.
# Dual-sourced: bash subprocesses (per-agent launchers) + zsh interactive session.
[[ -f ~/.config/zsh/ai/gemini-processor.sh ]] && source ~/.config/zsh/ai/gemini-processor.sh

# -----------------------------------------------------------------------------
# PARTITION 9: Experimental-runner dispatcher
# -----------------------------------------------------------------------------
[[ -f ~/.config/zsh/ai/experimental.zsh ]] && source ~/.config/zsh/ai/experimental.zsh

# -----------------------------------------------------------------------------
# PARTITION 10: Global claviature — derived keys panel
# Spec: guides/claviature.global.spec.md
# -----------------------------------------------------------------------------
[[ -f ~/.config/zsh/ai/keys.zsh ]] && source ~/.config/zsh/ai/keys.zsh

# -----------------------------------------------------------------------------
# PARTITION 11: Project-map interactive surface
# -----------------------------------------------------------------------------
# _project_paths / _project_git_status / _project_commit_all / _project_pick_zle
# Aliases + bindkey: keyboard.zsh PARTITION 15.
# Requires: temple-project-map.zsh (P3) loaded first.
[[ -f ~/.config/zsh/ai/temple-project-surface.zsh ]] && source ~/.config/zsh/ai/temple-project-surface.zsh

# -----------------------------------------------------------------------------
# PARTITION 12: Command Palette engine
# -----------------------------------------------------------------------------
# _command_palette / _command_palette_zle / _palette_help
# Aliases + bindkey: keyboard.zsh PARTITION 17.
# Wraps ai/command-palette.py against palette.map (both sibling deliverables,
# built in parallel — may not exist on disk yet).
[[ -f ~/.config/zsh/ai/command-palette.zsh ]] && source ~/.config/zsh/ai/command-palette.zsh
