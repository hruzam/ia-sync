#!/usr/bin/env zsh
# Monitor bootstrap — authored in ia-sync, deployed to ~/.config/zsh/config.zsh.
# New independent host hruzam-mntr; operator declaration 2026-11-12.
# Guide: ~/reposoma/raw.guides/machine-monitor/GUIDE.md
export MACHINE_NAME="monitor"
export ZSH_CONFIG_DIR="$HOME/.config/zsh"

# Keep local executables reachable without accumulating duplicate PATH entries.
typeset -U path
path=("$HOME/.local/bin" "$HOME/bin" $path)
export PATH

# Shared bricks follow the builder guide: config -> base -> keyboard + engines.
# Loading defines commands; it does not run experiments, connect peers or start services.
export RB_ROOT="$HOME/ia-sync/.dev/session"
[[ -f "$ZSH_CONFIG_DIR/ai/base.zsh" ]] && source "$ZSH_CONFIG_DIR/ai/base.zsh"
[[ -f "$ZSH_CONFIG_DIR/experimental/base.zsh" ]] && source "$ZSH_CONFIG_DIR/experimental/base.zsh"
[[ -f "$ZSH_CONFIG_DIR/session/base.zsh" ]] && source "$ZSH_CONFIG_DIR/session/base.zsh"
[[ -f "$ZSH_CONFIG_DIR/archx/base.zsh" ]] && source "$ZSH_CONFIG_DIR/archx/base.zsh"
[[ -f "$ZSH_CONFIG_DIR/system/base.zsh" ]] && source "$ZSH_CONFIG_DIR/system/base.zsh"

# Shared system keyboard includes workstation PHP aliases, but monitor has no
# PHP engines. Hide those aliases until this host has its own runtime decision.
unalias php74 php8 phpst composer74 composer8 tmcp cod 2>/dev/null

# Local PHP/project scopes remain undecided. Peer commands take an explicit target;
# no default home/office peer or startup network probe is selected for monitor.
