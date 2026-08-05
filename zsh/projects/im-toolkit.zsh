#!/usr/bin/env zsh
# =============================================================================
# IM TOOLKIT - Freya/Imago (Laravel) commands
# =============================================================================
# Location: ~/.config/zsh/projects/im-toolkit.zsh
# Loaded when: you run 'im' command
# =============================================================================

# =============================================================================
# MAIN COMMAND
# =============================================================================

im() {
    local cmd="${1:-}"
    
    case "$cmd" in
        -h|--help)
            _im_help
            ;;
        -rn|run)
            project_switch im
            ;;
        -gs)
            cd "$PROJECT_IM_PATH" && git status
            ;;
        -gp)
            cd "$PROJECT_IM_PATH" && git pull
            ;;
        -gph)
            cd "$PROJECT_IM_PATH" && git push
            ;;
        -e)
            cd "$PROJECT_IM_PATH" && $PREFERRED_EDITOR . &
            ;;
        -serve)
            cd "$PROJECT_IM_PATH" && php artisan serve
            ;;
        -migrate)
            cd "$PROJECT_IM_PATH" && php artisan migrate
            ;;
        -fresh)
            cd "$PROJECT_IM_PATH" && php artisan migrate:fresh --seed
            ;;
        -tinker)
            cd "$PROJECT_IM_PATH" && php artisan tinker
            ;;
        "")
            cd "$PROJECT_IM_PATH"
            echo "[DIR] $(pwd)"
            ;;
        *)
            echo "[ERROR] Unknown: $cmd (use 'im -h')"
            return 1
            ;;
    esac
}

_im_help() {
    cat << 'EOF'
+------------------------------------------------------------------+
|            IM TOOLKIT - Freya/Imago Commands                     |
+------------------------------------------------------------------+
|  im              Quick cd to project                             |
|  im -h           This help                                       |
|  im -rn          Full switch (PHP 8 + reload toolkit)            |
|                                                                  |
|  GIT:                                                            |
|  im -gs          git status                                      |
|  im -gp          git pull                                        |
|  im -gph         git push                                        |
|                                                                  |
|  LARAVEL:                                                        |
|  im -serve       php artisan serve                               |
|  im -migrate     php artisan migrate                             |
|  im -fresh       migrate:fresh --seed                            |
|  im -tinker      php artisan tinker                              |
|                                                                  |
|  OTHER:                                                          |
|  im -e           Open in editor                                  |
+------------------------------------------------------------------+
EOF
}

# =============================================================================
# COMPLETION
# =============================================================================
_im_completion() {
    local -a commands
    commands=(
        '-h:Help'
        '-rn:Full switch'
        '-gs:Git status'
        '-gp:Git pull'
        '-gph:Git push'
        '-e:Editor'
        '-serve:Artisan serve'
        '-migrate:Run migrations'
        '-fresh:Fresh migrate + seed'
        '-tinker:Artisan tinker'
    )
    _describe 'command' commands
}
[[ -n "$ZSH_VERSION" ]] && compdef _im_completion im 2>/dev/null

# =============================================================================
# LARAVEL SHORTCUTS (context-free — work from any directory)
# =============================================================================
alias art='php artisan'                         # php artisan shortcut
alias tinker='php artisan tinker'                # php artisan tinker REPL
alias migrate='php artisan migrate'              # php artisan migrate
alias serve='php artisan serve'                  # php artisan serve (dev HTTP server)
alias optimize='php artisan optimize:clear'      # clear all Laravel caches
alias seeder='php artisan db:seed'                # run database seeders
alias che='php artisan view:clear && php artisan cache:clear && php artisan config:clear'  # clear view+cache+config caches
alias mig='time php artisan migrate:fresh --seed'  # drop + re-migrate + reseed, timed
alias gpl='git pull && npm run build && php artisan optimize:clear'  # pull + npm build + clear caches
alias dbim="im && mysql -u root -p"               # switch to Freya + open MySQL CLI

echo "[toolkit] im loaded"