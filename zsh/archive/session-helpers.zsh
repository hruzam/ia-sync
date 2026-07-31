# =============================================================================
# SESSION HELPERS - ~/.config/zsh/session-helpers.zsh
# =============================================================================
# Pair env vars (required by shared-toolkit.zsh):
# Derived from $PROJECT_SES_PATH — hydrated by normalizer.py from
# harness.machine-project-registry.json. Falls back to PROJECT_SES_PATH
# if the registry does not yet export the granular SESSION_* vars.
export SESSION_SHARED_SRC="${PROJECT_SES_SHARED_SRC:-${PROJECT_SES_PATH}/.shared}"
export SESSION_SHARED_DST="${PROJECT_SES_SHARED_DST:-${PROJECT_SES_PATH}/shared}"
export SESSION_MAJKEE_SRC="${PROJECT_SES_MAJKEE_SRC:-${PROJECT_SES_PATH}/.majkee}"
export SESSION_MAJKEE_DST="${PROJECT_SES_MAJKEE_DST:-${PROJECT_SES_PATH}/majkee}"

# Session measure helper (optional, sourced if present)
[[ -f ~/.config/zsh/session-meassure.zsh ]] && source ~/.config/zsh/session-meassure.zsh

# Shared toolkit (shpub, shdiff, shstat, shsyntax)
[[ -f ~/.config/zsh/shared-toolkit.zsh ]] && source ~/.config/zsh/shared-toolkit.zsh

# Syntax phase (session-syntax subcommand + _session_init_phase_syntax)
[[ -f ~/.config/zsh/session-syntax.zsh ]] && source ~/.config/zsh/session-syntax.zsh

# =============================================================================
# session-init
# Manual entrypoint — call at the start of a LARVA work session.
# Runs all _session_init_phase_* functions in order.
# Future phases: add _session_init_phase_<name> in their sibling *.zsh files.
# =============================================================================
session-init() {
    echo "┌─ session init ───────────────────────────────────────"

    # Phase: syntax
    echo "│"
    _session_init_phase_syntax

    echo "│"
    echo "│  session-syntax open   -> full layer in Sublime"
    echo "│  session-syntax help   -> all subcommands"
    echo "└──────────────────────────────────────────────────────"
}

# =============================================================================
# session_core_repomix [config_path] [output_dir]
# =============================================================================
function session_core_repomix() {
    emulate -L zsh

    local config_path="${1:-${PROJECT_SES_PATH}/.shared/libraries/core_repomix_local.core.json}"
    local output_dir="${2:-${PROJECT_SES_PATH}/_repomix/}"
    local date_stamp
    local output_path

    if [[ ! -f "$config_path" ]]; then
        echo "[ERROR] Missing repomix config: $config_path"
        return 1
    fi

    if [[ ! -d "$output_dir" ]]; then
        echo "[ERROR] Missing output directory: $output_dir"
        return 1
    fi

    date_stamp="$(TZ="${SESSION_REPOMIX_TZ:-Europe/Prague}" date +%Y_%m_%d)"
    output_path="${output_dir}/core_repomix_${date_stamp}.md"

    echo "[*] session_core_repomix -> $output_path"

    builtin cd "$HOME" || return 1
    npx repomix --config "$config_path" --style markdown --output "$output_path"
}
