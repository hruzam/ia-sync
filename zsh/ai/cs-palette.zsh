#!/usr/bin/env zsh
# =============================================================================
# cs-palette.zsh — F: cold-start vault explorer (curses TUI, D1/D2/D3)
#
# Interface:
#   cs-palette [--sort-date|--sort-name|--sort-mtime]
#
# Sort flags (also honoured via TEMPLE_SORT env var):
#   --sort-date   filename-embedded YYYY-MM-DD, newest first (default)
#   --sort-mtime  filesystem modification time, newest first
#   --sort-name   alphabetical by filename
#   Env var TEMPLE_SORT=date|mtime|name sets the default for this terminal.
#   In TUI: press 's' to cycle through sort modes.
#
# Resolves the vault root via temple-project-map's `temple-project-root
# reposoma` — the only baked literal in this whole tool is the folder name
# `_cold-start` (raw.guides/cold-start-card/GUIDE.md "point, never copy" —
# only the folder name is hardcoded anywhere; the map absorbs a reposoma move).
#
# Note: EXECUTED script — never sourced. Self-sufficient (sources
# temple-project-map.zsh by path so it works standalone, same discipline as
# temple-mail-manage.zsh not depending on base.zsh already being loaded).
#
# Explorer only — never mutates the vault. cs-palette.py prints the selected
# card's resume: to real stdout on Enter; everything else (e/r/a/q) stays
# inside the TUI. Moving cards between card/archive/routines/ is
# temple-cs-manage's job, not this one's.
# =============================================================================

[[ -f "${0:A:h}/temple-project-map.zsh" ]] && source "${0:A:h}/temple-project-map.zsh"

if ! typeset -f temple-project-root >/dev/null; then
  echo "cs-palette: temple-project-map.zsh not found/sourced — cannot resolve reposoma root." >&2
  exit 1
fi

reposoma_root=$(temple-project-root reposoma) || exit 1
vault="${reposoma_root}/_cold-start"

if [[ ! -d "$vault" ]]; then
  echo "cs-palette: vault not found at $vault" >&2
  exit 1
fi

# Pre-parse sort flag; TEMPLE_SORT env is read by cs-palette.py directly.
sort_arg=""
for _arg in "$@"; do
  case "$_arg" in
    --sort-date)  sort_arg="--sort date"  ;;
    --sort-mtime) sort_arg="--sort mtime" ;;
    --sort-name)  sort_arg="--sort name"  ;;
  esac
done
unset _arg

exec python3 "${0:A:h}/cs-palette.py" --vault "$vault" ${=sort_arg}
