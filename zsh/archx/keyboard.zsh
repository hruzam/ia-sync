#!/usr/bin/env zsh
# =============================================================================
# KEYBOARD.ZSH — archx/ control panel (aliases + comments ONLY)
# =============================================================================
# Location: ~/.config/zsh/archx/keyboard.zsh
# Sourced by: config.home.zsh / config.office.zsh (right after archx/commands.zsh)
# LAW (guide-for-builder.md §Architecture rules): aliases and comments only —
# every function body lives in an engine (commands.zsh, bash.substrates.sh),
# never here. WP4 retrofit (2026-08-05) — aliases moved out of commands.zsh.
# =============================================================================

# ── Monitoring shortcuts ──────────────────────────────────────────────────────
# Bodies in: archx/bash.substrates.sh (substrate_*)
alias sysmon='substrate_system_overview'    # one-shot system overview
alias cputop='substrate_cpu_top 10'         # top 10 CPU processes
alias memtop='substrate_memory_top 10'      # top 10 memory processes
alias diskuse='substrate_disk_top_dirs /home 10'  # top 10 largest dirs under /home
alias services='substrate_services_check'   # watched systemd services status

# ── Help ───────────────────────────────────────────────────────────────────────
alias archx-help='_archx_help'  # this panel

# troubleshoot: directly-callable function, body in archx/commands.zsh — no
# alias needed (matches the temple-mail() / piql-remote() direct-call convention).
