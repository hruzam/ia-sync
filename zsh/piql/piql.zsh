#!/usr/bin/env zsh
# piql/piql.zsh — piql shell integration layer
# Scope: office machine (piql runs on office only)
# Sourced by config.office.zsh
#
# piql: privacy-gated assistant — scrubs PII/secrets locally before cloud.
# Project lives at: ~/www/piql/piql.dev/
# Agent health:     piql-doctor (9-check diagnostic)
# Roster:           ~/reposoma/temple/roster.md → Shannon (wiser mechanic)

PIQL_ENV="$HOME/www/piql/piql.dev/piql.env.zsh"
[[ -f "$PIQL_ENV" ]] && source "$PIQL_ENV"

# Tailscale bridge — piql-remote, piql-watch, piql-push, piql-ask, tss, tsp
PIQL_DIR="${0:A:h}"
[[ -f "${PIQL_DIR}/tailscale.zsh" ]] && source "${PIQL_DIR}/tailscale.zsh"

# Control panel — aliases + comments only (WP4 retrofit)
[[ -f "${PIQL_DIR}/keyboard.zsh" ]] && source "${PIQL_DIR}/keyboard.zsh"
