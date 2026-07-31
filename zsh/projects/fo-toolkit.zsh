#!/usr/bin/env zsh
# =============================================================================
# FO TOOLKIT - FantasyObchod (OpenCart) commands
# =============================================================================
# Location: ~/.config/zsh/projects/fo-toolkit.zsh
# Loaded when: you run 'fo' command
# =============================================================================

# =============================================================================
# MAIN COMMAND
# =============================================================================

fo() {
    local cmd="${1:-}"
    
    case "$cmd" in
        -h|--help)
            _fo_help
            ;;
        -rn|run)
            project_switch fo
            ;;
        -gs)
            cd "$PROJECT_FO_PATH" && git status
            ;;
        -gp)
            cd "$PROJECT_FO_PATH" && git pull
            ;;
        -gc)
            cd "$PROJECT_FO_PATH" && git commit -m "$*"
            ;;
        -gcs)
            shift; smart_commit "$1" "$2"
            ;;
        -gph)
            cd "$PROJECT_FO_PATH" && git push
            ;;
        -gh)
            _git_lifecycle_help
            ;;
        -db)
            cd "$PROJECT_FO_PATH" && mariadb --defaults-extra-file="$HOME/.config/zsh/.env/fo-db.cnf"
            ;;
        -adm)
            $PREFERRED_BROWSER -new-tab "http://fantasyobchod.l/adminer?username=root&db=$DB_NAME_FO" &
            ;;
        -e)
            cd "$PROJECT_FO_PATH" && $PREFERRED_EDITOR . &
            ;;
        -heu)
            cd "$PROJECT_FO_PATH" && $PREFERRED_EDITOR cron/heureka-ostra.xml &
            ;;
        "")
            cd "$PROJECT_FO_PATH"
            echo "[DIR] $(pwd)"
            ;;
        *)
            echo "[ERROR] Unknown: $cmd (use 'fo -h')"
            return 1
            ;;
    esac
}

_fo_help() {
    cat << 'EOF'
+------------------------------------------------------------------+
|            FO TOOLKIT - FantasyObchod Commands                   |
+------------------------------------------------------------------+
|  fo              Quick cd to project                             |
|  fo -h           This help                                       |
|  fo -rn          Full switch (PHP 7.4 + reload toolkit)          |
|                                                                  |
|  GIT:                                                            |
|  fo -gs          git status                                      |
|  fo -gp          git pull                                        |
|  fo -gc          git commit                                      |
|  fo -gc <phase> <msg>  Smart commit (e.g., psd -gc alpha "init") |
|  fo -gph         git push                                        |
|  fo -gh          Show UTF-8 Phase Symbols (Help)                 |
|                                                                  |
|  DATABASE:                                                       |
|  fo -db          Open MariaDB CLI                                |
|  fo -adm         Open Adminer in browser                         |
|                                                                  |
|  OTHER:                                                          |
|  fo -e           Open in editor                                  |
|  fo -heu         Open Heureka XML                                |
+------------------------------------------------------------------+
EOF
}

# =============================================================================
# COMPLETION
# =============================================================================
_fo_completion() {
    local -a commands
    commands=(
        '-h:Help'
        '-rn:Full switch'
        '-gs:Git status'
        '-gp:Git pull'
        '-gph:Git push'
        '-db:Database CLI'
        '-adm:Adminer'
        '-e:Editor'
        '-heu:Heureka XML'
    )
    _describe 'command' commands
}
[[ -n "$ZSH_VERSION" ]] && compdef _fo_completion fo 2>/dev/null

echo "[toolkit] fo loaded"