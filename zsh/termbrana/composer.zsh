#!/usr/bin/env zsh
# Termbrana composition engine; helpers resolve beside this source file.
# Definitions only. Parsing needs no shell/editor/session/tmux integration.
typeset -g _TBC_HELPER="${${(%):-%N}:A:h}/composer.py"

_tbc_python() { command python3 -I -S -B "$_TBC_HELPER" "$@"; }
_tbc_check()  { _tbc_python check "$@"; }
_tbc_parse()  { _tbc_python parse "$@"; }
