#!/usr/bin/env zsh
# =============================================================================
# PROJECT SWITCHER - Uses config.zsh for all paths
# =============================================================================
# Location: ~/.config/zsh/project-switcher.zsh
#
# REQUIRES: config.zsh must be sourced BEFORE this file
# All PROJECT_* and TOOLKIT_DIR variables come from config.zsh
# =============================================================================

# =============================================================================
# VERIFY CONFIG LOADED
# =============================================================================
if [[ -z "$TOOLKIT_DIR" ]]; then
    echo "[ERROR] config.zsh not loaded! Source it first."
    return 1
fi

# =============================================================================
# PHP HELPERS (use config variables)
# =============================================================================
php74_on() {
    echo "[*] Switching to PHP 7.4..."
    sudo systemctl stop "$PHP8_FPM_SERVICE" 2>/dev/null
    sudo systemctl start "$PHP74_FPM_SERVICE" 2>/dev/null
    
    if systemctl is-active --quiet "$PHP74_FPM_SERVICE"; then
        echo "[OK] PHP 7.4 active"
        php -v | head -n1
    else
        echo "[ERROR] Failed to start PHP 7.4"
    fi
}

php8_on() {
    echo "[*] Switching to PHP 8.x..."
    sudo systemctl stop "$PHP74_FPM_SERVICE" 2>/dev/null
    sudo systemctl start "$PHP8_FPM_SERVICE" 2>/dev/null
    
    if systemctl is-active --quiet "$PHP8_FPM_SERVICE"; then
        echo "[OK] PHP 8.x active"
        php -v | head -n1
    else
        echo "[ERROR] Failed to start PHP 8"
    fi
}

alias php74='php74_on'
alias php8='php8_on'

phpst() {
    echo "=== PHP Status ==="
    echo "CLI: $(php -v 2>/dev/null | head -n1)"
    echo "PHP 7.4 FPM ($PHP74_FPM_SERVICE): $(systemctl is-active $PHP74_FPM_SERVICE 2>/dev/null)"
    echo "PHP 8.x FPM ($PHP8_FPM_SERVICE): $(systemctl is-active $PHP8_FPM_SERVICE 2>/dev/null)"
}

# =============================================================================
# CORE SWITCHER LOGIC
# =============================================================================
project_switch() {
    local project="$1"
    local project_path=""
    local toolkit_file=""

    # 1. SETUP VARIABLES (from config.zsh)
    case "$project" in
        fo)
            project_path="$PROJECT_FO_PATH"
            toolkit_file="$TOOLKIT_DIR/$PROJECT_FO_TOOLKIT"
            ;;
        im)
            project_path="$PROJECT_IM_PATH"
            toolkit_file="$TOOLKIT_DIR/$PROJECT_IM_TOOLKIT"
            ;;
        psd)
            project_path="$PROJECT_PSD_PATH"
            toolkit_file="$TOOLKIT_DIR/$PROJECT_PSD_TOOLKIT"
            ;;
        ltp)
            project_path="$PROJECT_LTP_PATH"
            toolkit_file="$TOOLKIT_DIR/$PROJECT_LTP_TOOLKIT"
            ;;
        lrv)
            project_path="$PROJECT_LRV_PATH"
            toolkit_file="$TOOLKIT_DIR/$PROJECT_LRV_TOOLKIT"
            ;;
        sess)
            project_path="$PROJECT_SES_PATH"
            toolkit_file="$TOOLKIT_DIR/$PROJECT_SES_TOOLKIT"
            ;;
        *)
            echo "[ERROR] Unknown project: $project"
            echo "Available: fo, im, psd"
            return 1
            ;;
    esac

    # 2. SWITCH DIRECTORY
    if [[ -d "$project_path" ]]; then
        cd "$project_path"
        echo "[DIR] $project_path"
    else
        echo "[ERROR] Path not found: $project_path"
        return 1
    fi

    # 3. LOAD TOOLKIT (always source - overwrites launcher function)
    if [[ -f "$toolkit_file" ]]; then
        source "$toolkit_file"
    else
        echo "[WARN] Toolkit not found: $toolkit_file"
    fi
}

# =============================================================================
# LAUNCHER FUNCTIONS
# =============================================================================
# These exist at terminal startup.
# When called:
# 1. project_switch sources the toolkit
# 2. Toolkit OVERWRITES this function with the real one
# 3. If args passed, call the new function immediately
# =============================================================================

fo() {
    project_switch fo
    [[ $# -gt 0 ]] && fo "$@"
}

im() {
    project_switch im
    [[ $# -gt 0 ]] && im "$@"
}

psd() {
    project_switch psd
    [[ $# -gt 0 ]] && psd "$@"
}

ltp() {
    project_switch ltp
    [[ $# -gt 0 ]] && ltp "$@"
}

sess() {
    project_switch sess
    [[ $# -gt 0 ]] && ltp "$@"
}

lrv() {
    project_switch lrv
    [[ $# -gt 0 ]] && ltp "$@"
}

# =============================================================================
# GLOBAL HELP
# =============================================================================
project_help() {
    cat << EOF
+------------------------------------------------------------+
|              PROJECT SWITCHER (@${MACHINE_NAME})                     
+------------------------------------------------------------+
|  fo    -> $PROJECT_FO_NAME (PHP $PROJECT_FO_PHP)
|  im    -> $PROJECT_IM_NAME (PHP $PROJECT_IM_PHP)
|  psd   -> $PROJECT_PSD_NAME (PHP $PROJECT_PSD_PHP)
|  psd   -> $PROJECT_LRV_NAME (ZSH $PROJECT_LRV_ZSH)
|  ltp   -> $PROJECT_LTP_NAME (PHP $PROJECT_LTP_PHP)
|  sess  -> $PROJECT_SES_NAME (ZSH $PROJECT_SES_ZSH)
|                                                            
|  After switching: <project> -h for commands                
+------------------------------------------------------------+
|  php74  -> Switch to PHP 7.4                               
|  php8   -> Switch to PHP 8.x                               
|  phpst  -> Show PHP status                                 
+------------------------------------------------------------+
|  Paths from: ~/.config/zsh/config.zsh                      
+------------------------------------------------------------+
EOF
}

# =============================================================================
# COMMON LARAVEL/COMPOSER ALIASES
# =============================================================================
alias art='php artisan'
alias tinker='php artisan tinker'
alias migrate='php artisan migrate'
alias fresh='php artisan migrate:fresh --seed'
alias serve='php artisan serve'
alias composer74='$PHP74_BIN $COMPOSER_BIN'
alias composer8='$PHP8_BIN $COMPOSER_BIN'

echo "[switcher] Loaded. Commands: fo, im, psd, ltp, lrv, sess, project_help"