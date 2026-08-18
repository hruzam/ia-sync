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

# Scope signpost (control panel + reserved engine partitions — WP5 retrofit;
# projects/ toolkit aliases themselves stay in their lazy-loaded toolkit
# files, see projects/keyboard.zsh's own header for why).
[[ -f ~/.config/zsh/projects/base.zsh ]] && source ~/.config/zsh/projects/base.zsh

# =============================================================================
# PHP HELPERS — defined in system/office.php-switch.zsh, sourced via config.zsh
# php74 / php8 / phpst are available here because config.zsh sources office.php-switch.zsh
# before project-switcher.zsh is loaded.
# =============================================================================
# CORE SWITCHER LOGIC
# =============================================================================
# project_switch <name> — cd into a project + source its toolkit (fo|im|psd|ltp|lrv|sess)
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
            echo "Available: fo, im, psd, ltp, lrv, sess"
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
    [[ $# -gt 0 ]] && sess "$@"
}

lrv() {
    project_switch lrv
    [[ $# -gt 0 ]] && lrv "$@"
}

# =============================================================================
# DEV SESSION LAUNCHERS (multi-process start)
# =============================================================================

# Start Imago/Freya dev session: PHP 8 FPM + cd + editor
# Freya runs Octane+RoadRunner; site served by Valet at http://freya.l
# For hot-reload dev: use 'imoctane' after imst
imdev() {
    _php8
    cd "$PROJECT_IM_PATH" || return 1
    ${PREFERRED_EDITOR:-subl} . &
    printf "\n  [imdev] Freya session started\n"
    printf "  Path: %s\n" "$PROJECT_IM_PATH"
    printf "  PHP:  %s\n" "$(php -r 'echo PHP_VERSION;' 2>/dev/null)"
    printf "  URL:  http://freya.l (Valet)\n"
    printf "  Tip:  run 'imoctane' for Octane dev server\n\n"
}
alias imst='imdev'  # alias for imdev — start Freya dev session

# Start Octane (RoadRunner) dev server for Freya
alias imoctane='cd "$PROJECT_IM_PATH" && php artisan octane:start --server=roadrunner --watch &'  # Octane dev server for Freya

# Start FantasyObchod dev session: PHP 7.4 FPM + cd + editor
fodev() {
    _php74
    cd "$PROJECT_FO_PATH" || return 1
    ${PREFERRED_EDITOR:-subl} . &
    printf "\n  [fodev] FantasyObchod session started\n"
    printf "  Path: %s\n" "$PROJECT_FO_PATH"
    printf "  URL:  http://fantasyobchod.l\n\n"
}
alias fost='fodev'  # alias for fodev — start FantasyObchod dev session

# =============================================================================
# GLOBAL HELP
# =============================================================================
# project_help — box panel: project shortcuts (fo/im/psd/lrv/ltp/sess) + PHP switch commands
project_help() {
    cat << EOF
+------------------------------------------------------------+
|              PROJECT SWITCHER (@${MACHINE_NAME})                     
+------------------------------------------------------------+
|  fo    -> $PROJECT_FO_NAME (PHP $PROJECT_FO_PHP)
|  im    -> $PROJECT_IM_NAME (PHP $PROJECT_IM_PHP)
|  psd   -> $PROJECT_PSD_NAME (PHP $PROJECT_PSD_PHP)
|  lrv   -> $PROJECT_LRV_NAME (ZSH $PROJECT_LRV_ZSH)
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
# COMMON LARAVEL ALIASES
# =============================================================================
alias art='php artisan'                     # php artisan shortcut
alias tinker='php artisan tinker'            # php artisan tinker REPL
alias migrate='php artisan migrate'          # php artisan migrate
alias fresh='php artisan migrate:fresh --seed'  # drop + re-migrate + reseed the DB
alias serve='php artisan serve'              # php artisan serve (dev HTTP server)

# =============================================================================
# PROJECTS SCOPE HELP (projects/ control panel entry point — projects-help)
# =============================================================================
_projects_help() {
    cat << 'EOF'
projects — per-project toolkits, lazy-loaded on switch (engine: project-switcher.zsh +
projects/*.zsh; keys: projects/keyboard.zsh)

  fo / im / ltp / psd     switch to that project (cd + source its toolkit); then `<name> -h`
                          for its own command panel (case-dispatch: -gs/-gp/-gc/-db/-e/…)
  larva <ovum>            cd to <ovum>/.larva/ task folder (default fo)
  larva-status <ovum>     show active LARVAs (tasks) for an OVUM
  larva-init <ovum> <n>   scaffold a new LARVA folder for an OVUM

  im-toolkit shortcuts (context-free once `im` is active — projects/im-toolkit.zsh):
    art / tinker / migrate / serve / optimize / seeder / che / mig / gpl / dbim

  larva.zsh agent shortcuts (projects/larva.zsh — deploy-relocated to zsh root,
  eager on both machines): laika / consult / broadcast / slices / capcom /
  trajectory / athena / zenit / horizon / nidus

  project_help    box panel: project shortcuts + PHP switch commands
EOF
}

echo "[switcher] Loaded. Commands: fo, im, psd, ltp, lrv, sess, project_help"
