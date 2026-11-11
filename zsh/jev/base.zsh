#!/usr/bin/env zsh
# Jev signpost: definitions only; safe to source from the table or deployed tree.
[[ -n ${_JEV_LOADED:-} ]] && return 0
typeset -g _JEV_SOURCE_DIR="${${(%):-%N}:A:h}"
source "${_JEV_SOURCE_DIR}/jev.zsh"
source "${_JEV_SOURCE_DIR}/keyboard.zsh"
typeset -g _JEV_LOADED=1
