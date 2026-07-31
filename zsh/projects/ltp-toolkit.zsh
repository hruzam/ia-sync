#!/usr/bin/env zsh
# =============================================================================
# LTP TOOLKIT - Laravel Training Project commands
# =============================================================================
# Location: ~/.config/zsh/projects/ltp-toolkit.zsh
# Loaded when: you run 'ltp' command
# =============================================================================

ltp() {
    local cmd="${1:-}"

    case "$cmd" in
        -h|--help)
            _ltp_help
            ;;
        -rn|run)
            project_switch ltp
            ;;
        -gs)
            cd "$PROJECT_LTP_PATH" && git status
            ;;
        -gp)
            cd "$PROJECT_LTP_PATH" && git pull
            ;;
        -gph)
            cd "$PROJECT_LTP_PATH" && git push
            ;;
        -e)
            cd "$PROJECT_LTP_PATH" && $PREFERRED_EDITOR . &
            ;;
        -serve)
            cd "$PROJECT_LTP_PATH" && php artisan serve
            ;;
        -migrate)
            cd "$PROJECT_LTP_PATH" && php artisan migrate
            ;;
        -fresh)
            cd "$PROJECT_LTP_PATH" && php artisan migrate:fresh --seed
            ;;
        -tinker)
            cd "$PROJECT_LTP_PATH" && php artisan tinker
            ;;
        -test)
            cd "$PROJECT_LTP_PATH" && php artisan test
            ;;
        -route)
            cd "$PROJECT_LTP_PATH" && php artisan route:list
            ;;
        -dev)
            cd "$PROJECT_LTP_PATH" && npm run dev
            ;;
        "")
            cd "$PROJECT_LTP_PATH"
            echo "[DIR] $(pwd)"
            ;;
        *)
            echo "[ERROR] Unknown: $cmd (use 'ltp -h')"
            return 1
            ;;
    esac
}

_ltp_help() {
    cat << 'EOF'
+------------------------------------------------------------------+
|       LTP TOOLKIT - Laravel Training Project Commands            |
+------------------------------------------------------------------+
|  ltp             Quick cd to project                             |
|  ltp -h          This help                                       |
|  ltp -rn         Full switch (PHP 8 + reload toolkit)            |
|                                                                  |
|  GIT:                                                            |
|  ltp -gs         git status                                      |
|  ltp -gp         git pull                                        |
|  ltp -gph        git push                                        |
|                                                                  |
|  LARAVEL:                                                        |
|  ltp -serve      php artisan serve                               |
|  ltp -migrate    php artisan migrate                             |
|  ltp -fresh      migrate:fresh --seed                            |
|  ltp -tinker     php artisan tinker                              |
|  ltp -test       php artisan test                                |
|  ltp -route      php artisan route:list                          |
|                                                                  |
|  FRONTEND:                                                       |
|  ltp -dev        npm run dev                                     |
|                                                                  |
|  OTHER:                                                          |
|  ltp -e          Open in editor                                  |
+------------------------------------------------------------------+
EOF
}

_ltp_completion() {
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
        '-test:Run Laravel tests'
        '-route:Show route list'
        '-dev:Run Vite dev server'
    )
    _describe 'command' commands
}
[[ -n "$ZSH_VERSION" ]] && compdef _ltp_completion ltp 2>/dev/null

echo "[toolkit] ltp loaded"
