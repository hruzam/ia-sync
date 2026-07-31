# Session helpers for `~/www/session`.

[[ -f ~/.config/zsh/session-meassure.zsh ]] && source ~/.config/zsh/session-meassure.zsh

function session_core_repomix() {
    emulate -L zsh

    local config_path="${1:-$HOME/www/session/.setup/library/core_repomix_local.core.json}"
    local output_dir="${2:-$HOME/www/session/.setup/library}"
    local date_stamp
    local output_path

    if [[ ! -f "$config_path" ]]; then
        echo "Missing repomix config: $config_path"
        return 1
    fi

    if [[ ! -d "$output_dir" ]]; then
        echo "Missing output directory: $output_dir"
        return 1
    fi

    date_stamp="$(TZ="${SESSION_REPOMIX_TZ:-Europe/Prague}" date +%Y_%m_%d)"
    output_path="${output_dir}/core_repomix_${date_stamp}.md"

    echo "session_core_repomix -> $output_path"

    builtin cd "$HOME" || return 1
    npx repomix --config "$config_path" --style markdown --output "$output_path"
}
