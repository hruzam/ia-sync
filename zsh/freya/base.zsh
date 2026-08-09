#!/usr/bin/env zsh
# freya/base.zsh — the freya scope signpost
# Location: ~/.config/zsh/freya/base.zsh  ·  sourced by config.zsh
# Deployed from: ~/ia-sync/zsh/freya/  (via deploy.sh / zsync)
#
# WHAT THIS IS: a thin shell aggregation over the freya project's CANONICAL
# scripts, which live in the freya.devenv companion repo — NOT here. No logic
# lives in this scope; every alias calls out to freya.devenv/{scripts,deploy,sync}.
# Two buses, kept distinct (see freya-buffer skill):
#   · buffer bus  — git app-code office↔home over Tailscale (freya-buffer.sh)
#   · devenv bus  — config/harness office↔home (deploy.sh / sync.sh)
#
# Contract: idempotent, side-effect-free on source.

# Where the freya.devenv companion repo lives. Consistent on both machines;
# override in config.office.zsh / config.home.zsh only if a machine differs.
export FREYA_DEVENV_DIR="${FREYA_DEVENV_DIR:-$HOME/www/imago_cz/freya.devenv}"

# PARTITION 1: control panel (aliases only — no bodies)
[[ -f ~/.config/zsh/freya/keyboard.zsh ]] && source ~/.config/zsh/freya/keyboard.zsh

# PARTITION 2: engine (function bodies — thin wrappers)
[[ -f ~/.config/zsh/freya/engine.zsh ]] && source ~/.config/zsh/freya/engine.zsh
