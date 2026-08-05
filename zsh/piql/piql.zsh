#!/usr/bin/env zsh
# piql/piql.zsh — piql privacy-gate loader (engine)
# Scope: office machine (piql runs on office only)
# Sourced by: piql/base.zsh PARTITION 3 (office-only guard) — WP5 retrofit;
# was self-chaining to tailscale.zsh + keyboard.zsh directly (WP4), now those
# live as their own base.zsh partitions per the canonical signpost pattern.
#
# piql: privacy-gated assistant — scrubs PII/secrets locally before cloud.
# Project lives at: ~/www/piql/piql.dev/
# Agent health:     piql-doctor (9-check diagnostic)
# Roster:           ~/reposoma/temple/roster.md → Shannon (wiser mechanic)

PIQL_ENV="$HOME/www/piql/piql.dev/piql.env.zsh"
[[ -f "$PIQL_ENV" ]] && source "$PIQL_ENV"
