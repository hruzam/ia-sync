#!/usr/bin/env zsh
# =============================================================================
# PSDVS TOOLKIT - Project commands (loaded on demand)
# =============================================================================
# Location: ~/.config/zsh/projects/psdvs-toolkit.zsh
# Loaded when: you run 'psd' command
#
# 2026-07-27 (ADR-001, majkee, relayed via Oraculum): stack swapped Laravel -> Nette
# (per-package) · PHP 8.4 · PostgreSQL 16+ · nette/tester · PHPStan L8 ·
# nette/coding-standard. This toolkit never carried artisan/pint/phpunit aliases
# (those live as shared global aliases in project-switcher.zsh, still valid for
# im/ltp/freya which remain Laravel) — Nette tooling subcommands added below,
# additive only.
# =============================================================================

# =============================================================================
# MAIN COMMAND - psd [subcommand]
# =============================================================================
# This OVERWRITES the launcher function from project-switcher.zsh
# =============================================================================

psd() {
    local cmd="${1:-}"
    
    case "$cmd" in
        -h|--help|help)
            _psd_help
            ;;
        -rep|repomix)
            shift; _psd_repomix "$@"
            ;;
        -repcp|repomix-copy)
            shift; _psd_repomix_copy "$@"
            ;;
        -rn|run|switch)
            project_switch psd
            ;;
        -s|status)
            _psd_status
            ;;
        -e|edit)
            _psd_edit
            ;;
        -env|environment)
            _psd_backup_environment
            ;;
        -gs)
            cd "$PROJECT_PSD_PATH" && git status
            ;;
        -gp)
            cd "$PROJECT_PSD_PATH" && git pull
            ;;
        -ga)
            cd "$PROJECT_PSD_PATH" && git add "$@"
            ;;
        -gc)
            cd "$PROJECT_PSD_PATH" && git commit -m "$*"
            ;;
        -gcs)
            shift; smart_commit "$1" "$2"
            ;;
        -gph)
            cd "$PROJECT_PSD_PATH" && git push
            ;;
        -gh)
            _git_lifecycle_help
            ;;
        -t|test)
            cd "$PROJECT_PSD_PATH" && vendor/bin/tester tests/
            ;;
        -an|analyse)
            cd "$PROJECT_PSD_PATH" && vendor/bin/phpstan analyse
            ;;
        -ll|latte-lint)
            shift; cd "$PROJECT_PSD_PATH" && vendor/bin/latte-lint "${@:-app}"
            ;;
        -nl|neon-lint)
            shift; cd "$PROJECT_PSD_PATH" && vendor/bin/neon-lint "${@:-.}"
            ;;
        "")
            cd "$PROJECT_PSD_PATH"
            echo "[DIR] $(pwd)"
            ;;
        *)
            echo "[ERROR] Unknown: $cmd (use 'psd -h')"
            return 1
            ;;
    esac
}

# =============================================================================
# HELP
# =============================================================================
_psd_help() {
    cat << 'EOF'
+------------------------------------------------------------------+
|                 PSD TOOLKIT - PSDVS Commands                     |
+------------------------------------------------------------------+
|  psd              Quick cd to project                            |
|  psd -h           This help                                      |
|  psd -rn          Full switch (PHP + reload toolkit)             |
|                                                                  |
|  REPOMIX:                                                        |
|  psd -rep         Generate repomix                               |
|  psd -repcp       Generate + copy + clipboard                    |
|                                                                  |
|  ENVIRONMENT:                                                    |
|  psd -env         Backup .zshrc + zsh scripts to project/env/    |
|                                                                  |
|  NETTE (ADR-001, 2026-07-27):                                    |
|  psd -t           vendor/bin/tester                              |
|  psd -an          vendor/bin/phpstan analyse                     |
|  psd -ll          vendor/bin/latte-lint [path=app]               |
|  psd -nl          vendor/bin/neon-lint [path=.]                  |
|                                                                  |
|  GIT:                                                            |
|  psd -gs          git status                                     |
|  psd -gp          git pull                                       |
|  psd -ga <files>  git add                                        |
|  psd -gc <msg>    git commit -m                                  |
|                                                                  |
|  OTHER:                                                          |
|  psd -s           Project status                                 |
|  psd -e           Open in editor                                 |
+------------------------------------------------------------------+
EOF
}

# =============================================================================
# REPOMIX FUNCTIONS
# =============================================================================
_psd_repomix() {
    echo "[*] Generating Repomix..."
    cd "$PROJECT_PSD_PATH" || return 1
    
    if ! command -v repomix &> /dev/null; then
        echo "[ERROR] repomix not found. Install: npm install -g repomix"
        return 1
    fi
    
    local output_file="${PROJECT_PSD_PATH}/repomix-output.xml"
    repomix --output "$output_file"
    
    if [[ -f "$output_file" ]]; then
        echo "[OK] Generated: $output_file ($(du -h "$output_file" | cut -f1))"
    fi
}

_psd_repomix_copy() {
    _psd_repomix || return 1
    
    local copy_dir="${ENV_BACKUP_DIR}/repomix-copies"
    mkdir -p "$copy_dir"
    
    local source_file="${PROJECT_PSD_PATH}/repomix-output.xml"
    local target_file="${copy_dir}/psdvs_$(date +%Y%m%d_%H%M%S).xml"
    
    cp "$source_file" "$target_file"
    echo "[COPY] $target_file"
    
    # Clipboard (Wayland)
    if command -v wl-copy &> /dev/null; then
        cat "$source_file" | wl-copy
        echo "[CLIP] Copied to clipboard"
    fi
}

# =============================================================================
# ENVIRONMENT BACKUP (Fixed version)
# =============================================================================
_psd_backup_environment() {
    echo "=== Backup ZSH Environment ==="
    
    local backup_dir="${ENV_BACKUP_DIR}/zsh-backup"
    local timestamp=$(date +%Y%m%d_%H%M%S)
    
    # Create backup directory
    mkdir -p "$backup_dir"
    
    echo "[*] Backing up to: $backup_dir"
    
    # 1. Copy .zshrc
    if [[ -f "$HOME/.zshrc" ]]; then
        cp "$HOME/.zshrc" "${backup_dir}/.zshrc"
        echo "[OK] .zshrc"
    fi
    
    # 2. Copy entire zsh config directory (with -r for recursive!)
    if [[ -d "$ZSH_CONFIG_DIR" ]]; then
        cp -r "$ZSH_CONFIG_DIR" "${backup_dir}/zsh-config"
        echo "[OK] $ZSH_CONFIG_DIR -> zsh-config/"
    fi
    
    # 3. List what was backed up
    echo ""
    echo "=== Backup Contents ==="
    ls -la "$backup_dir"
    
    if [[ -d "${backup_dir}/zsh-config" ]]; then
        echo ""
        echo "=== zsh-config/ ==="
        ls -la "${backup_dir}/zsh-config"
    fi
    
    echo ""
    echo "[OK] Backup complete: $backup_dir"
    echo "[TIP] Now you can: cd $PROJECT_PSD_PATH && git add env/ && git commit"
}

# =============================================================================
# STATUS / EDIT
# =============================================================================
_psd_status() {
    echo "=== PSDVS Status ==="
    echo "[PATH] $PROJECT_PSD_PATH"
    echo "[PHP]  $PROJECT_PSD_PHP"
    
    if [[ -d "$PROJECT_PSD_PATH/.git" ]]; then
        cd "$PROJECT_PSD_PATH"
        echo "[GIT]  Branch: $(git branch --show-current)"
        echo "[GIT]  Changes: $(git status --porcelain | wc -l) files"
    fi
}

_psd_edit() {
    cd "$PROJECT_PSD_PATH" || return 1
    
    if [[ "$PREFERRED_EDITOR" == "code" ]] && command -v code &> /dev/null; then
        code . & disown
        echo "[OK] Opened in VS Code"
    elif command -v subl &> /dev/null; then
        subl . &
        echo "[OK] Opened in Sublime"
    else
        echo "[ERROR] No editor found"
    fi
}

# =============================================================================
# COMPLETION
# =============================================================================
_psd_completion() {
    local -a commands
    commands=(
        '-h:Help'
        '-rn:Full switch'
        '-rep:Repomix'
        '-repcp:Repomix+copy'
        '-env:Backup environment'
        '-t:vendor/bin/tester'
        '-an:vendor/bin/phpstan analyse'
        '-ll:vendor/bin/latte-lint'
        '-nl:vendor/bin/neon-lint'
        '-gs:Git status'
        '-gp:Git pull'
        '-s:Status'
        '-e:Edit'
    )
    _describe 'command' commands
}
[[ -n "$ZSH_VERSION" ]] && compdef _psd_completion psd 2>/dev/null

echo "[toolkit] psd loaded"