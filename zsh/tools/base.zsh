#!/usr/bin/env zsh
# Tools signpost: definitions only, table/deployed paths both supported.
[[ -n ${_TOOLS_LOADED:-} ]] && return 0
typeset -g _TOOLS_SOURCE_DIR="${${(%):-%N}:A:h}"
source "${_TOOLS_SOURCE_DIR}/tools.zsh"
source "${_TOOLS_SOURCE_DIR}/keyboard.zsh"
typeset -g _TOOLS_LOADED=1
