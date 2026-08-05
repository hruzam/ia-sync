#!/usr/bin/env zsh
# =============================================================================
# KEYBOARD.ZSH — projects/ control panel (aliases + comments ONLY)
# =============================================================================
# Location: ~/.config/zsh/projects/keyboard.zsh
# Sourced by: project-switcher.zsh (the eager root engine for this scope —
#             see project-switcher.zsh's own eager load in zshrc.home/zshrc.office)
# LAW (guide-for-builder.md §Architecture rules): aliases and comments only —
# every function body lives in an engine (projects/*.zsh), never here.
# WP4 retrofit (2026-08-05).
#
# FLAGGED — NOT a mechanical move, left in place on purpose:
# Unlike ai/system/archx/piql/sync, projects/ toolkits are LAZY-loaded —
# project_switch() (project-switcher.zsh) sources a toolkit file on demand
# only after `fo`/`im`/`ltp`/`psd` is invoked, and that source call OVERWRITES
# the launcher stub with the toolkit's real function. There is no scope-wide
# "always loaded" entry point analogous to ai/base.zsh for the aliases living
# INSIDE those toolkits (e.g. im-toolkit.zsh: art/tinker/migrate/che/mig/gpl/
# dbim/optimize/seeder; projects/larva.zsh: laika/consult/broadcast/slices/
# capcom/trajectory/athena/zenit/horizon/nidus — note larva.zsh is also
# deploy-relocated to zsh-root as ~/.config/zsh/larva.zsh, sourced eagerly
# there, a SEPARATE eager path this file does not touch).
#
# Moving those aliases here would either (a) make them eagerly available
# before the matching project is ever entered — a functional behavior
# change, not a mechanical one — or (b) require sourcing this file from
# inside project_switch() per-toolkit, which is a new sourcing mechanism
# this WP was told not to invent. Left untouched; flagged for the operator.
#
# What DOES live here: nothing yet — this file exists so the scope has a
# wired-in control panel + help entry point (below), satisfying the
# aliases-and-comments-ONLY law for whatever gets added to this scope next.
# Discovery today: fo -h / im -h / ltp -h / psd -h / nab -h (per-toolkit
# case-dispatch help), larva-status, larva-init — see projects-help.
# =============================================================================

alias projects-help='_projects_help'  # this panel
