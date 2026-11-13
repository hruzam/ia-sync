#!/usr/bin/env zsh
# system/machine.zsh — per-machine registry reader (defines only)
# Data: registries/machine.<host>.json (declared intent + nominal class; never eval'd).
# Pointer: config.<host>.zsh exports MACHINE_REGISTRY; when unset, the same path is
# derived from $MACHINE_NAME so hosts that have not mirrored the export still work.
# Aliases live in system/keyboard.zsh. File-kind rule: registries/README.md.

# _machine_get <jq-path>  e.g. _machine_get .swap.zram.size_mib
# Prints the value (nothing if absent); non-zero when file/jq missing or path absent.
_machine_get() {
    local f="${MACHINE_REGISTRY:-$HOME/.config/zsh/registries/machine.$MACHINE_NAME.json}" out
    [[ -n "$1" && -r "$f" ]] && command -v jq >/dev/null 2>&1 || return 1
    out=$(jq -r "$1 // empty" "$f" 2>/dev/null) || return 1
    [[ -n "$out" ]] || return 1
    print -r -- "$out"
}

_machine_show() {
    local f="${MACHINE_REGISTRY:-$HOME/.config/zsh/registries/machine.$MACHINE_NAME.json}"
    [[ -r "$f" ]] || { echo "[machine] no registry: $f" >&2; return 1; }
    command -v jq >/dev/null 2>&1 && jq . "$f" || cat "$f"
}
