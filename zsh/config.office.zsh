#!/usr/bin/env zsh
# =============================================================================
# CONFIG.ZSH - Machine-specific configuration (@office)
# =============================================================================
# Location: ~/.config/zsh/config.zsh
# =============================================================================
#
# PURPOSE:
# - All paths and constants in ONE place
# - Different per machine (@home vs @office)
# - Logic files (project-switcher.zsh, toolkits) stay IDENTICAL
#
# SETUP NEW MACHINE:
# 1. Copy this file to ~/.config/zsh/config.zsh
# 2. Edit MACHINE_NAME and paths below
# 3. Copy all other files without changes
# =============================================================================

# =============================================================================
# MACHINE AND MEDIA PROJECT IDENTIFIER
# =============================================================================
export MACHINE_NAME="office"
export OFFICE_PROJECT_PATH="$HOME/projects" # 2026-07-07: /media/data/projects is an empty unmounted husk; psdvs/ltp/larva/session live here

# =============================================================================
# PATH CONFIGURATION
# =============================================================================
# Order matters: first listed = highest priority
typeset -U PATH  # Prevents duplicate entries

path=(
    #"$HOME/.local/bin"              # Local scripts (repomix-gen, etc.)
    "$HOME/.npm-global/bin"         # Global npm packages
    "$HOME/.config/composer/vendor/bin"  # Composer global packages
    $path                           # Keep existing system PATH
)

# =============================================================================
# ZSH PATHS
# =============================================================================
export ZSH_CONFIG_DIR="$HOME/.config/zsh"
export TOOLKIT_DIR="$HOME/.config/zsh/projects"

# =============================================================================
# PROJECT PATHS
# =============================================================================
# Restored 2026-07-07 — block was lost in the 2026-07-03 "clean path" edit
# (see ia-sync journal); project-switcher.zsh and all toolkits depend on it.

# FantasyObchod (OpenCart, PHP 7.4)
export PROJECT_FO_PATH="$HOME/www/imago_cz/fantasyobchod"
export PROJECT_FO_NAME="FantasyObchod"
export PROJECT_FO_PHP="74"
export PROJECT_FO_TOOLKIT="fo-toolkit.zsh"

# Freya/Imago (Laravel 13, PHP 8.3+, Octane+RoadRunner, Valet at freya.l)
export PROJECT_IM_PATH="$HOME/www/imago_cz/freya"
export PROJECT_IM_NAME="Freya"
export PROJECT_IM_PHP="8"
export PROJECT_IM_TOOLKIT="im-toolkit.zsh"

# PSDVS (Nette per-package, PHP 8.4) — new build 2026-07-07, replaces stale ~/projects/psdvs;
# canonical shape/distro handled by reposoma/temple agents (not zsh's concern)
# 2026-07-27 (ADR-001): stack swapped Laravel -> Nette; PROJECT_PSD_PHP stays "8"
# (this toolkit only buckets 7.4 vs 8.x, no finer granularity — see office.php-switch.zsh)
export PROJECT_PSD_PATH="$HOME/www/psdvs/psdvsSys"
export PROJECT_PSD_NAME="PSDVS"
export PROJECT_PSD_PHP="8"
export PROJECT_PSD_TOOLKIT="psdvs-toolkit.zsh"

# Laravel Training Project (Laravel, PHP 8+)
export PROJECT_LTP_PATH="$OFFICE_PROJECT_PATH/ltp"
export PROJECT_LTP_NAME="Laravel Training Project"
export PROJECT_LTP_PHP="8"
export PROJECT_LTP_TOOLKIT="ltp-toolkit.zsh"

# Larva (vibe coding records, *.md, *.sh, *.zsh)
export PROJECT_LRV_PATH="$OFFICE_PROJECT_PATH/larva"
export PROJECT_LRV_NAME="vibe-code sessions"
export PROJECT_LRV_ZSH="larva.zsh"
export PROJECT_LRV_TOOLKIT="larva.zsh"

# Session (vibe coding records, *.md, *.sh, *.zsh)
export PROJECT_SES_PATH="$OFFICE_PROJECT_PATH/session"
export PROJECT_SES_NAME="vibe-code sessions"
export PROJECT_SES_ZSH="session.zsh"
export PROJECT_SES_TOOLKIT="session.zsh"

# nabLarva (larva V3 — agent<>agent ladder; scope-group ~/unikuklatrix; docs-only
# until gavel docket item 2 lands a v1 language — no PHP/build vars by design).
# Own scope folder nablarva/ (ai/-pattern, NOT the projects/ toolkit mechanism);
# wired via the nablarva/base.zsh source hook below, next to ai/base.zsh.
export PROJECT_NAB_PATH="$HOME/unikuklatrix/nablarva"
export PROJECT_NAB_NAME="nabLarva"
export PROJECT_NAB_DEVENV="$HOME/unikuklatrix/nablarva.devenv"

# Env backups (consumed by psdvs-toolkit.zsh)
export ENV_BACKUP_DIR="$PROJECT_PSD_PATH/env"

# =============================================================================
# PHP CONFIGURATION
# =============================================================================
export PHP74_BIN="/usr/bin/php74"
export PHP8_BIN="/usr/bin/php"
export COMPOSER_BIN="/usr/bin/composer"

export PHP74_FPM_SERVICE="php74-fpm"
export PHP8_FPM_SERVICE="php-fpm"

# =============================================================================
# DATABASE
# =============================================================================
export DB_USER="majkee"
export DB_NAME_FO="fantasyobchod"

# =============================================================================
# EDITOR / BROWSER
# =============================================================================
export PREFERRED_EDITOR="subl"
export PREFERRED_BROWSER="firefox"

# =============================================================================
# TAILSCALE + PIQL CROSS-MACHINE
# =============================================================================
export TAILSCALE_PEER="hruzam"       # home machine (tailscale status → hruzam)
export PIQL_PORT="0"                 # update from piql.env.zsh when known
export TS_DASH_PORT="9733"             # HTTP dashboard port (ts-dash)

# =============================================================================
# NPM / NODE (for future use)
# =============================================================================
# export NODE_PATH="/usr/bin/node"
# export NPM_PATH="/usr/bin/npm"

echo "[config] @${MACHINE_NAME} loaded"


# =============================================================================
# Larva FROM 2026-02-28
# =============================================================================

# LARVA system plugin — loads on demand via `lrv` switch (projects/larva.zsh);
# startup copy ~/.config/zsh/larva.zsh archived 2026-07-07

#Tablet Extension
[[ -f ~/.config/zsh/krfb.zsh ]] && source ~/.config/zsh/krfb.zsh

#GEMINI STUFF
[[ -f ~/.config/zsh/.env/secrets.zsh ]] && source ~/.config/zsh/.env/secrets.zsh

# AI AGENT SHELL SYSTEM (Harness freshness & Gemini Base aliases)
[[ -f ~/.config/zsh/ai/base.zsh ]] && source ~/.config/zsh/ai/base.zsh
[[ -f ~/.config/zsh/nablarva/base.zsh ]] && source ~/.config/zsh/nablarva/base.zsh

#SESSION HELPERS
[[ -f ~/.config/zsh/projects/session.zsh ]] && source ~/.config/zsh/projects/session.zsh

# PIQL INTEGRATION (office only — privacy gate; cross-machine bridge partitions
# live in piql/base.zsh, MACHINE_NAME-guarded — see that file's header)
[[ -f ~/.config/zsh/piql/base.zsh ]] && source ~/.config/zsh/piql/base.zsh

#GUIDE-PUBLISH SYNCHRONIZER
[[ -f ~/.config/zsh/sync/base.zsh ]] && source ~/.config/zsh/sync/base.zsh

# =============================================================================
# ARCH LINUX MONITORING COMMANDS (archx suite)
# =============================================================================
[[ -f ~/.config/zsh/archx/base.zsh ]] && source ~/.config/zsh/archx/base.zsh

# =============================================================================
# SYSTEM UTILITIES (shell helpers, PHP switching)
# =============================================================================
# pacman.zsh / browser.zsh source lines removed 2026-07-07 — files never existed.
# office.php-switch.zsh is office-dedicated (home switches PHP via Docker in
# config.home.zsh); reach preserved via MACHINE_NAME guards inside
# system/base.zsh (see that file's header) — WP5 retrofit.
[[ -f ~/.config/zsh/system/base.zsh ]] && source ~/.config/zsh/system/base.zsh
_ts_header 2>/dev/null  # compact peer status line on every shell open (silent if down)
_dash_header 2>/dev/null  # startup dashboard — @majkee's editable notes (system/dashboard.md)

# mesh/office-wire.zsh removed 2026-07-07 per Kelvin journal 2026-06-30 item 2
# (Gate E closed — direct SSH covers everything wofm did)

# =============================================================================
# PROJECT-LOCAL ZSH LAYERS (volatile · on-demand only · NOT sourced here)
# =============================================================================
# Breadcrumb only — no sourcing, no global registration. applications-in-common
# carries a volatile factory CLI layer, activated manually per session:
#   source /home/hruzam/www/elements-factory/applications-in-common/.dev/zsh/_base.zsh
# Bare `fact` = keyboard once live. Card / authority:
#   /home/hruzam/www/elements-factory/applications-in-common/.dev/zsh/README.md
# =============================================================================