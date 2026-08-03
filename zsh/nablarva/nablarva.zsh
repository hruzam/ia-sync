#!/usr/bin/env zsh
# =============================================================================
# NABLARVA.ZSH — the nab engine (project verbs)
# =============================================================================
# Location: ~/.config/zsh/nablarva/nablarva.zsh (table-authored; deploy.sh spreads)
# Sourced by: nablarva/base.zsh P2
# Vars from config.<machine>.zsh: PROJECT_NAB_PATH · PROJECT_NAB_DEVENV
# Contract: definitions only on source; work happens when nab() is called.
# Docs-only phase — no build/test verbs until gavel docket item 2 (v1 language).
# =============================================================================

nab() {
    local cmd="${1:-}"

    case "$cmd" in
        -h|--help|help)
            _nab_help
            ;;
        -s|status)
            _nab_status
            ;;
        -e|edit)
            _nab_edit
            ;;
        # --- harness surfaces (flag L9: flag+pulse canon, dock uncanonical) ---
        -f|flag)
            _nab_open "$PROJECT_NAB_PATH/session/flag.md"
            ;;
        -p|pulse)
            _nab_open "$PROJECT_NAB_PATH/session/pulse.md"
            ;;
        -d|dock)
            _nab_open "$PROJECT_NAB_PATH/session/dock.md"
            ;;
        # --- devenv transport (harness git-home) ---
        -sync)
            bash "$PROJECT_NAB_DEVENV/sync.sh"
            ;;
        -dep|deploy)
            echo "[WARN] deploy overwrites app-side harness with devenv snapshot."
            echo "       Never run when app-side is ahead of last sync. Sync first."
            read -q "REPLY?Proceed? [y/N] " && echo && bash "$PROJECT_NAB_DEVENV/deploy.sh"
            ;;
        # --- git (app repo: substrate + docs only; harness is gitignored) ---
        -gs)
            cd "$PROJECT_NAB_PATH" && git status
            ;;
        -gp)
            cd "$PROJECT_NAB_PATH" && git pull
            ;;
        -ga)
            shift; cd "$PROJECT_NAB_PATH" && git add "$@"
            ;;
        -gc)
            shift; cd "$PROJECT_NAB_PATH" && git commit -m "$*"
            ;;
        -gph)
            cd "$PROJECT_NAB_PATH" && git push
            ;;
        "")
            cd "$PROJECT_NAB_PATH"
            echo "[DIR] $(pwd)"
            ;;
        *)
            echo "[ERROR] Unknown: $cmd (use 'nab -h')"
            return 1
            ;;
    esac
}

# =============================================================================
# HELP
# =============================================================================
_nab_help() {
    cat << 'EOF'
+------------------------------------------------------------------+
|               NAB ENGINE - nabLarva Commands                     |
+------------------------------------------------------------------+
|  nab              Quick cd to project                            |
|  nab -h           This help                                      |
|                                                                  |
|  HARNESS:                                                        |
|  nab -f           Open session/flag.md  (locks + docket)         |
|  nab -p           Open session/pulse.md (canonical doing-state)  |
|  nab -d           Open session/dock.md  (uncanonical scratch)    |
|                                                                  |
|  DEVENV TRANSPORT (harness git-home):                            |
|  nab -sync        Stage harness app -> devenv (sync.sh)          |
|  nab -dep         Deploy devenv -> app (guarded; sync first!)    |
|                                                                  |
|  GIT (app repo — substrate + docs; harness gitignored):          |
|  nab -gs / -gp / -ga <f> / -gc <msg> / -gph                      |
|                                                                  |
|  OTHER:                                                          |
|  nab -s           Project status                                 |
|  nab -e           Open in editor                                 |
|  nab-keys         List the keyboard panel                        |
+------------------------------------------------------------------+
EOF
}

# =============================================================================
# STATUS / EDIT / OPEN
# =============================================================================
_nab_status() {
    echo "=== nabLarva Status ==="
    echo "[PATH]   $PROJECT_NAB_PATH"
    echo "[DEVENV] $PROJECT_NAB_DEVENV"

    if [[ -d "$PROJECT_NAB_PATH/.git" ]]; then
        cd "$PROJECT_NAB_PATH"
        echo "[GIT]    Branch: $(git branch --show-current)"
        echo "[GIT]    Changes: $(git status --porcelain | wc -l) files"
    fi
    if [[ -f "$PROJECT_NAB_PATH/session/pulse.md" ]]; then
        echo "[PULSE]  $(grep -m1 '^## ' "$PROJECT_NAB_PATH/session/pulse.md")"
    fi
}

_nab_edit() {
    cd "$PROJECT_NAB_PATH" || return 1

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

_nab_open() {
    local target="$1"
    if [[ ! -f "$target" ]]; then
        echo "[ERROR] Not found: $target"
        return 1
    fi
    if command -v subl &> /dev/null; then
        subl "$target" &
    else
        ${PREFERRED_EDITOR:-vi} "$target"
    fi
}

# =============================================================================
# COMPLETION
# =============================================================================
_nab_completion() {
    local -a commands
    commands=(
        '-h:Help'
        '-f:Open flag.md'
        '-p:Open pulse.md'
        '-d:Open dock.md'
        '-sync:Harness app->devenv'
        '-dep:Deploy devenv->app (guarded)'
        '-gs:Git status'
        '-gp:Git pull'
        '-gph:Git push'
        '-s:Status'
        '-e:Edit'
    )
    _describe 'command' commands
}
[[ -n "$ZSH_VERSION" ]] && compdef _nab_completion nab 2>/dev/null
