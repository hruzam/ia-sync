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

# Deliberately minimal bootstrap. Local PHP and remote project execution are
# undecided. Do not source home/office project, PHP, database or service wiring.
# Tailnet enrollment and SSH authorization remain pending; see the machine guide.
