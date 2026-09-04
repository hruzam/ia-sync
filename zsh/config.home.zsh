#!/usr/bin/env zsh
# =============================================================================
# CONFIG.ZSH - Machine-specific configuration
# =============================================================================
# Location: ~/.config/zsh/config.zsh
#
# PURPOSE:
# - Core bootstrapper that delegates path/variable definition to JSON registry
# - Uses normalizer.py to load 'home' or 'office' configurations
#
# SETUP NEW MACHINE:
# 1. Edit MACHINE_NAME below to either 'home' or 'office'
# 2. Modify ~/.config/zsh/harness.machine-project-registry.json as needed
# =============================================================================

# =============================================================================
# MACHINE IDENTIFIER
# =============================================================================
export MACHINE_NAME="home"

# =============================================================================
# ZSH PATHS
# =============================================================================
export ZSH_CONFIG_DIR="$HOME/.config/zsh"
export TOOLKIT_DIR="$HOME/.config/zsh/projects"

# =============================================================================
# PROJECT PATHS
# =============================================================================
# Migrated 2026-08-28 — normalizer.py + harness.machine-project-registry.json
# retired on home (office dropped this mechanism long ago; see zsh/AGENTS.md
# "RESOLVED 2026-07-29" row). Inline PROJECT_* exports, office-style. Values
# carried verbatim from the registry's "home" block; project-switcher.zsh and
# all toolkits depend on this block.
#
# KNOWN STALE (pre-existing in the registry, carried as-is — not introduced by
# this migration; flagged in journal.host-cleanup.md 2026-08-28 for follow-up):
#   - PROJECT_PSD_PATH: real dir is ~/www/psdvs (lowercase), registry says PSDVS
#   - PROJECT_LRV_PATH: ~/www/larva does not exist on this host

# FantasyObchod (OpenCart, PHP 7.4)
export PROJECT_FO_PATH="$HOME/www/imago_cz/fantasyobchod"
export PROJECT_FO_NAME="FantasyObchod"
export PROJECT_FO_PHP="74"
export PROJECT_FO_TOOLKIT="fo-toolkit.zsh"

# Freya/Imago (Laravel, PHP 8)
export PROJECT_IM_PATH="$HOME/www/imago_cz/freya"
export PROJECT_IM_NAME="Freya/Imago"
export PROJECT_IM_PHP="8"
export PROJECT_IM_TOOLKIT="im-toolkit.zsh"

# PSDVS (PHP 8) — see KNOWN STALE note above
export PROJECT_PSD_PATH="$HOME/www/psdvs"
export PROJECT_PSD_NAME="PSDVS"
export PROJECT_PSD_PHP="8"
export PROJECT_PSD_TOOLKIT="psdvs-toolkit.zsh"

# Laravel Training Project (Laravel, PHP 8)
export PROJECT_LTP_PATH="$HOME/www/Laravel-training-project"
export PROJECT_LTP_NAME="Laravel Training Project"
export PROJECT_LTP_PHP="8"
export PROJECT_LTP_TOOLKIT="ltp-toolkit.zsh"

# Larva (vibe-code orchestr) — see KNOWN STALE note above
export PROJECT_LRV_PATH="$HOME/www/larva"
export PROJECT_LRV_NAME="vibe-code orchestr"
export PROJECT_LRV_ZSH="larva.zsh"
export PROJECT_LRV_TOOLKIT="larva.zsh"

# nabLarva (project harness / session browser)
export PROJECT_NAB_PATH="$HOME/unikuklatrix/nablarva"

# Session (vibe-code sessions)
export PROJECT_SES_PATH="$HOME/www/larva_dev/dev"
export PROJECT_SES_NAME="vibe-code sessions"
export PROJECT_SES_ZSH="session-helpers.zsh"
export PROJECT_SES_TOOLKIT="session-helpers.zsh"
export PROJECT_SES_SHARED_SRC="$HOME/www/larva_dev/dev/.shared"
export PROJECT_SES_SHARED_DST="$HOME/www/larva_dev/dev/shared"
export PROJECT_SES_MAJKEE_SRC="$HOME/www/larva_dev/dev/.majkee"
export PROJECT_SES_MAJKEE_DST="$HOME/www/larva_dev/dev/majkee"

# =============================================================================
# PHP / DB / TOOLING (registry "vars" block — carried verbatim)
# =============================================================================
# PHP74_BIN / PHP8_BIN intentionally empty on home: no native CLI, PHP runs via
# Docker (system/home.php-composer.zsh); office's office.php-switch.zsh is the
# only live consumer of these two vars and is MACHINE_NAME-guarded off on home.
export PHP74_BIN=""
export PHP8_BIN=""
export COMPOSER_BIN="/usr/bin/composer"
export PHP74_FPM_SERVICE="php74-fpm"
export PHP8_FPM_SERVICE="php-fpm"
export DB_USER="majkee"
export DB_NAME_FO="fantasyobchod"
export PREFERRED_EDITOR="subl"
export PREFERRED_BROWSER="firefox"
export ENV_BACKUP_DIR="$HOME/www/psdvs/env"

# =============================================================================
# MACHINE-SPECIFIC REQUIREMENTS (Docker logic for @home)
# =============================================================================
if [[ "$MACHINE_NAME" == "home" ]]; then
    if ! command -v docker &> /dev/null; then
        echo "[SETUP] Docker not installed. Composer won't work."
        echo "        Install: sudo pacman -S docker && sudo systemctl enable --now docker"
    elif ! systemctl is-active --quiet docker 2>/dev/null; then
        echo "[SETUP] Docker not running. Start: sudo systemctl start docker"
    elif ! groups | grep -q docker; then
        echo "[SETUP] Add to docker group: sudo usermod -aG docker $USER && logout/login"
    fi
fi

# =============================================================================
# Larva FROM 2026-02-28
# =============================================================================

[[ -f ~/.config/zsh/larva.zsh ]] && source ~/.config/zsh/larva.zsh
[[ -f ~/.config/zsh/krfb.zsh ]] && source ~/.config/zsh/krfb.zsh
# Secrets: .env/ vault layout (unified with office 2026-07-31 — flat secrets.zsh retired,
# was stale May-era keys; .env/ materialized from zsh/env.vault.age via env-vault open)
[[ -f ~/.config/zsh/.env/secrets.zsh ]] && source ~/.config/zsh/.env/secrets.zsh

# AI AGENT SHELL SYSTEM (Harness freshness & Gemini Base aliases) — mirrors config.office.zsh;
# was missing here entirely, so the whole ai/ scope (keyboard, temple family, devenv, claude
# engine, gemini-processor, keys) never auto-loaded on a real home shell start. Reconstructed 2026-07-20.
[[ -f ~/.config/zsh/ai/base.zsh ]] && source ~/.config/zsh/ai/base.zsh

# nablarva scope (session browser: rb-open, rb-pick, rb-help — wired 2026-09-04)
[[ -f ~/.config/zsh/nablarva/base.zsh ]] && source ~/.config/zsh/nablarva/base.zsh

[[ -f ~/.config/zsh/session-helpers.zsh ]] && source ~/.config/zsh/session-helpers.zsh
[[ -f ~/.config/zsh/env-sync.zsh ]] && source ~/.config/zsh/env-sync.zsh

# =============================================================================
# TAILSCALE — system scope (engine + keyboard, via system/base.zsh — WP5)
# =============================================================================
export TAILSCALE_PEER="hruzam-120922"  # office machine hostname on tailnet
export TS_DASH_PORT="9733"             # HTTP dashboard port (ts-dash)

[[ -f ~/.config/zsh/system/base.zsh ]] && source ~/.config/zsh/system/base.zsh
_ts_header 2>/dev/null  # compact peer status line on every shell open (silent if down)
_dash_header 2>/dev/null  # startup dashboard — @majkee's editable notes (system/dashboard.md)

# =============================================================================
# PIQL CROSS-MACHINE (piql = gemma/ollama on office; home accesses via SSH;
# via piql/base.zsh — MACHINE_NAME-guarded office-only partition inside, WP5)
# =============================================================================
export PIQL_PORT="0"                   # update to match office piql.env.zsh port

# piql-remote, piql-watch, piql-ask — SSH over tailscale to office piql
[[ -f ~/.config/zsh/piql/base.zsh ]] && source ~/.config/zsh/piql/base.zsh

# ~/bin on PATH for local scripts (ramwatch etc.)
[[ -d "$HOME/bin" ]] && export PATH="$HOME/bin:$PATH"

# =============================================================================
# ARCH LINUX MONITORING COMMANDS (Generated 2026-06-28; via archx/base.zsh — WP5)
# =============================================================================
[[ -f ~/.config/zsh/archx/base.zsh ]] && source ~/.config/zsh/archx/base.zsh

# FREYA PROJECT OPS (buffer + devenv buses — thin wrappers over freya.devenv scripts)
[[ -f ~/.config/zsh/freya/base.zsh ]] && source ~/.config/zsh/freya/base.zsh

if [ -f '/home/hruzam/google-cloud-sdk/path.zsh.inc' ]; then . '/home/hruzam/google-cloud-sdk/path.zsh.inc'; fi
if [ -f '/home/hruzam/google-cloud-sdk/completion.zsh.inc' ]; then . '/home/hruzam/google-cloud-sdk/completion.zsh.inc'; fi
