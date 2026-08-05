#!/usr/bin/env zsh
# command-palette.zsh — Command Palette engine (curses TUI launcher)
# Sourced by: ~/.config/zsh/ai/base.zsh (PARTITION 11)
# Aliases:    ~/.config/zsh/ai/keyboard.zsh (PARTITION 17)
#
# Wraps ai/command-palette.py (python3 stdlib curses TUI — sibling deliverable, built in
# parallel; may not exist on disk yet) against palette.map (TSV manifest at the zsh root —
# sibling deliverable, built in parallel).
#
# Contract: python3 command-palette.py --map <path>
#   selection made  → prints selected command to stdout, exit 0
#   cancelled       → nothing to stdout, exit 1
#   map missing     → exit 2
#   TUI renders via /dev/tty so stdout stays capturable by the caller.
#
# Bodies exposed:
#   _command_palette       → command-palette   plain-shell entry; prints selection to stdout
#   _command_palette_zle   → bindkey '^[k' (Alt-k); inserts selection at cursor
#   _palette_help          → palette-help      help panel
#
# Map resolution: ${PALETTE_MAP:-${ZDOTDIR:-$HOME/.config/zsh}/palette.map}
# TUI resolution: sibling to this engine's own runtime location (${0:A:h} — cf.
#                 system/tailscale.zsh, piql/piql.zsh).

_PALETTE_ENGINE_DIR="${0:A:h}"
_PALETTE_TUI="${_PALETTE_ENGINE_DIR}/command-palette.py"

# ── _palette_map_path ─────────────────────────────────────────────────────────
_palette_map_path() {
  print -- "${PALETTE_MAP:-${ZDOTDIR:-$HOME/.config/zsh}/palette.map}"
}

# ── _palette_precheck ─────────────────────────────────────────────────────────
# Guard: python3 present + TUI script present + map file present.
# On failure sets _palette_precheck_msg (one clear line) and returns 1.
_palette_precheck() {
  local map="$1"

  if ! command -v python3 &>/dev/null; then
    _palette_precheck_msg="command-palette: python3 not found — install python3 to use the palette"
    return 1
  fi
  if [[ ! -f "${_PALETTE_TUI}" ]]; then
    _palette_precheck_msg="command-palette: TUI script not found at ${_PALETTE_TUI}"
    return 1
  fi
  if [[ ! -f "${map}" ]]; then
    _palette_precheck_msg="command-palette: map file not found at ${map}"
    return 1
  fi
  return 0
}

# ── _palette_regen_if_stale ───────────────────────────────────────────────────
# Rebuild map if stale: map missing or any *.zsh file (recursive) is newer.
# Silent on success. On failure with existing map: one stderr line, continue.
# On failure with no map: one stderr line, return 1.
_palette_regen_if_stale() {
  local map="$1"
  local root
  root="${_PALETTE_ENGINE_DIR:h}"
  root="$(_palette_map_path)"
  root="${root:h}"

  local needs_regen=0
  if [[ ! -f "${map}" ]]; then
    needs_regen=1
  else
    if find "${root}" -name '*.zsh' -newer "${map}" -print -quit 2>/dev/null | grep -q . 2>/dev/null; then
      needs_regen=1
    fi
  fi

  if (( needs_regen )); then
    if python3 "${_PALETTE_ENGINE_DIR}/palette-map-gen.py" --root "${root}" >/dev/null 2>&1; then
      return 0
    fi
    if [[ -f "${map}" ]]; then
      print -u2 "palette: map regen failed, using stale map"
      return 0
    else
      print -u2 "palette: map regen failed and no existing map found"
      return 1
    fi
  fi
  return 0
}

# ── _palette_refresh ──────────────────────────────────────────────────────────
# Unconditionally rebuild the map. Prints command count on success.
# On failure: one stderr line, return 1.
_palette_refresh() {
  local map
  local root
  map="$(_palette_map_path)"
  root="${map:h}"

  if python3 "${_PALETTE_ENGINE_DIR}/palette-map-gen.py" --root "${root}" >/dev/null 2>&1; then
    local count
    count=$(tail -n +2 "${map}" 2>/dev/null | wc -l)
    print "palette: ${count} commands"
    return 0
  else
    print -u2 "palette: refresh failed"
    return 1
  fi
}

# ── _command_palette ──────────────────────────────────────────────────────────
# Plain-shell entry: resolve map + TUI, guard, run, print selection to stdout.
_command_palette() {
  local map
  map="$(_palette_map_path)"

  local _palette_precheck_msg
  if ! _palette_precheck "${map}"; then
    print -u2 "${_palette_precheck_msg}"
    return 1
  fi

  if ! _palette_regen_if_stale "${map}"; then
    return 1
  fi

  python3 "${_PALETTE_TUI}" --map "${map}"
}

# ── _command_palette_zle ──────────────────────────────────────────────────────
# ZLE widget: run the TUI with terminal input from /dev/tty, capture stdout.
# On exit 0, insert the selection at the cursor. On nonzero exit, just redisplay.
_command_palette_zle() {
  local map
  map="$(_palette_map_path)"

  local _palette_precheck_msg
  if ! _palette_precheck "${map}"; then
    zle -M "${_palette_precheck_msg}"
    return 1
  fi

  local sel
  if sel=$(python3 "${_PALETTE_TUI}" --map "${map}" </dev/tty); then
    LBUFFER+="${sel}"
  fi
  zle redisplay
}
zle -N _command_palette_zle
# bindkey lives in keyboard.zsh PARTITION 17 (control-panel convention — matches
# the P15 precedent: temple-project-surface.zsh registers `zle -N`, keyboard.zsh
# owns the `bindkey` wiring next to the alias).

# ── _palette_help ──────────────────────────────────────────────────────────────
# Help panel for the command-palette surface. Called by ai-help (master panel).
# Alias: palette-help (keyboard.zsh PARTITION 17).
_palette_help() {
  cat <<'EOF'
command-palette — curses TUI command launcher (engine: ai/command-palette.zsh)

  command-palette         run the palette; prints the selected command to stdout
  Alt-k  (^[k)             ZLE widget — runs the palette, inserts selection at cursor
  palette-help             this panel
  palette-refresh          manual rebuild of the command map

  Map file:   ${PALETTE_MAP:-$ZDOTDIR/palette.map}  (default: ~/.config/zsh/palette.map)
              TSV manifest: scope<TAB>command<TAB>help<TAB>engine
  Generator:  ai/palette-map-gen.py  — builds/refreshes palette.map from the tree
              (sibling deliverable; rebuilds automatically when any .zsh file is updated)
  TUI:        ai/command-palette.py  — python3 stdlib curses; renders via /dev/tty
              so stdout stays capturable

  Engine: ~/.config/zsh/ai/command-palette.zsh
EOF
}
