#!/usr/bin/env zsh
# system/shell.zsh — general shell utilities engine
# Scope: cross-machine, non-project, non-monitoring
# Aliases live in system/keyboard.zsh (keyboard convention).
# Sourced by config.zsh (office) and config.home.zsh (home).

_msrc() {
    grep -Hrn "$1" "${PROJECT_FO_PATH:-$HOME/www}"
}
