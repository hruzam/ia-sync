#!/usr/bin/env zsh
# ai/palette-help.zsh — thin sourceable wrapper around palette-help.py
# Defines-only; not wired to any real scope yet. Future migration points
# each `_<scope>_help` at `_palette_help <that scope's keyboard.zsh>`.

_palette_help() {
    python3 "${0:A:h}/palette-help.py" "$@"
}
