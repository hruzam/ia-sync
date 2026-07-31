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
REGISTRY_FILE="$HOME/.config/zsh/harness.machine-project-registry.json"
NORMALIZER="$HOME/.config/zsh/normalizer.py"

# =============================================================================
# LOAD REGISTRY VIA NORMALIZER
# =============================================================================
if [[ -f "$NORMALIZER" && -f "$REGISTRY_FILE" ]]; then
    eval "$(python3 "$NORMALIZER" "$MACHINE_NAME" "$REGISTRY_FILE")"
else
    echo "[ERROR] Could not find normalizer or registry file."
fi

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
# COMPOSER CONFIGURATION (@home uses Docker)
# =============================================================================

unalias composer74 2>/dev/null
unalias composer8 2>/dev/null

_check_docker() {
    if ! command -v docker &> /dev/null; then
        echo "[ERROR] Docker not installed"
        echo "[FIX]   sudo pacman -S docker"
        return 1
    fi
    if ! systemctl is-active --quiet docker 2>/dev/null; then
        echo "[ERROR] Docker service not running"
        echo "[FIX]   sudo systemctl start docker"
        return 1
    fi
    if ! groups | grep -q docker; then
        echo "[ERROR] User not in docker group"
        echo "[FIX]   sudo usermod -aG docker $USER && logout/login"
        return 1
    fi
    return 0
}

composer74() {
    _check_docker || return 1
    
    if ! docker image inspect php74-composer &> /dev/null; then
        echo "[SETUP] Building php74-composer image (one-time)..."
        docker build -t php74-composer ~/.docker/php74-composer/
    fi
    
    mkdir -p "$HOME/.composer/cache"
    
    docker run --rm -it \
      -v "$(pwd)":/app \
      -v "$HOME/.composer":/composer \
      -e COMPOSER_HOME=/composer \
      -e COMPOSER_CACHE_DIR=/composer/cache \
      php74-composer \
      --ignore-platform-req=ext-posix \
      --ignore-platform-req=ext-pcntl \
      "$@"
}

composer8() {
    _check_docker || return 1
    docker run --rm -it \
      -v "$(pwd)":/app \
      -v "$HOME/.composer:/tmp/composer" \
      -u $(id -u):$(id -g) \
      composer:latest \
      --ignore-platform-req=ext-posix \
      --ignore-platform-req=ext-pcntl \
      "$@"
}

# =============================================================================
# Larva FROM 2026-02-28
# =============================================================================

[[ -f ~/.config/zsh/larva.zsh ]] && source ~/.config/zsh/larva.zsh
[[ -f ~/.config/zsh/krfb.zsh ]] && source ~/.config/zsh/krfb.zsh
[[ -f ~/.config/zsh/secrets.zsh ]] && source ~/.config/zsh/secrets.zsh

# AI AGENT SHELL SYSTEM (Harness freshness & Gemini Base aliases) — mirrors config.office.zsh;
# was missing here entirely, so the whole ai/ scope (keyboard, temple family, devenv, claude
# engine, gemini-processor, keys) never auto-loaded on a real home shell start. Reconstructed 2026-07-20.
[[ -f ~/.config/zsh/ai/base.zsh ]] && source ~/.config/zsh/ai/base.zsh

[[ -f ~/.config/zsh/session-helpers.zsh ]] && source ~/.config/zsh/session-helpers.zsh
[[ -f ~/.config/zsh/env-sync.zsh ]] && source ~/.config/zsh/env-sync.zsh

# =============================================================================
# TAILSCALE — system scope (engine + keyboard)
# =============================================================================
export TAILSCALE_PEER="hruzam-120922"  # office machine hostname on tailnet
export TS_DASH_PORT="9733"             # HTTP dashboard port (ts-dash)

[[ -f ~/.config/zsh/system/tailscale.zsh ]] && source ~/.config/zsh/system/tailscale.zsh
[[ -f ~/.config/zsh/system/keyboard.zsh  ]] && source ~/.config/zsh/system/keyboard.zsh
_ts_header 2>/dev/null  # compact peer status line on every shell open (silent if down)

# =============================================================================
# PIQL CROSS-MACHINE (piql = gemma/ollama on office; home accesses via SSH)
# =============================================================================
export PIQL_PORT="0"                   # update to match office piql.env.zsh port

# piql-remote, piql-watch, piql-ask — SSH over tailscale to office piql
[[ -f ~/.config/zsh/piql/tailscale.zsh ]] && source ~/.config/zsh/piql/tailscale.zsh

# ~/bin on PATH for local scripts (ramwatch etc.)
[[ -d "$HOME/bin" ]] && export PATH="$HOME/bin:$PATH"

# =============================================================================
# ARCH LINUX MONITORING COMMANDS (Generated 2026-06-28)
# =============================================================================
[[ -f ~/.config/zsh/archx/commands.zsh ]] && source ~/.config/zsh/archx/commands.zsh

if [ -f '/home/hruzam/google-cloud-sdk/path.zsh.inc' ]; then . '/home/hruzam/google-cloud-sdk/path.zsh.inc'; fi
if [ -f '/home/hruzam/google-cloud-sdk/completion.zsh.inc' ]; then . '/home/hruzam/google-cloud-sdk/completion.zsh.inc'; fi