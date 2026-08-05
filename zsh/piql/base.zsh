#!/usr/bin/env zsh
# =============================================================================
# BASE.ZSH — the piql/ signpost (scope folder, ai/-pattern)
# =============================================================================
# Location: ~/.config/zsh/piql/base.zsh (authored on the surgical table
# ~/ia-sync/zsh/ — deploy.sh spreads to both machines; never edit live copy)
# Sourced by: config.zsh (interactive shells), guarded — same hook as ai/base.zsh
# Contract: idempotent + side-effect-free on source — defines only, never runs
#           work or prints (decision 0009 L2 discipline carried over).
#
# Scope: piql — cross-machine bridge (home + office) + privacy-gated assistant
# (office only). Reach genuinely differs by machine — this is the one
# partition below gated on $MACHINE_NAME, mirroring the same guard idiom
# system/office.php-switch.zsh already uses in this tree (not a new
# mechanism). Sourced identically from both config.home.zsh and
# config.office.zsh; the guard is what keeps reach machine-correct, so a
# single signpost line replaces the old direct config → keyboard.zsh /
# tailscale.zsh / piql.zsh wiring (WP4) without changing what either
# machine actually loads.
#
# Retrofit 2026-08-05 (WP5) — reference: nablarva/base.zsh.
# =============================================================================

# -----------------------------------------------------------------------------
# PARTITION 1: control panel (aliases only — bodies live in engines)
# -----------------------------------------------------------------------------
[[ -f ~/.config/zsh/piql/keyboard.zsh ]] && source ~/.config/zsh/piql/keyboard.zsh

# -----------------------------------------------------------------------------
# PARTITION 2: Tailscale bridge engine (cross-machine — both home + office)
# piql-remote, piql-watch, piql-push, piql-ask, piql-expose*
# -----------------------------------------------------------------------------
[[ -f ~/.config/zsh/piql/tailscale.zsh ]] && source ~/.config/zsh/piql/tailscale.zsh

# -----------------------------------------------------------------------------
# PARTITION 3: piql privacy-gate loader engine (office only — piql runs there)
# Same reach as before WP5: home never sourced piql.zsh; this guard preserves
# that exactly instead of relying on PIQL_ENV's own file-existence no-op.
# -----------------------------------------------------------------------------
[[ "$MACHINE_NAME" == "office" && -f ~/.config/zsh/piql/piql.zsh ]] && source ~/.config/zsh/piql/piql.zsh
