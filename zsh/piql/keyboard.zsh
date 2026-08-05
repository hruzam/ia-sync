#!/usr/bin/env zsh
# =============================================================================
# KEYBOARD.ZSH — piql/ control panel (aliases + comments ONLY)
# =============================================================================
# Location: ~/.config/zsh/piql/keyboard.zsh
# Sourced by: piql/piql.zsh (office — full piql stack) AND directly by
#             config.home.zsh (home — bridge-only, next to piql/tailscale.zsh)
# LAW (guide-for-builder.md §Architecture rules): aliases and comments only —
# every function body lives in an engine (piql/tailscale.zsh), never here.
# WP4 retrofit (2026-08-05) — piql-pull alias moved out of tailscale.zsh.
#
# Most piql commands (piql-remote, piql-watch, piql-push, piql-ask,
# piql-expose, piql-expose-off, piql-expose-status) are directly-callable
# functions in piql/tailscale.zsh — no alias needed (matches the
# temple-mail() direct-call convention). Only the rename below lives here.
# =============================================================================

alias piql-pull='piql-remote'   # from home: read last piql output from office

alias piql-help='_piql_help'  # this panel
