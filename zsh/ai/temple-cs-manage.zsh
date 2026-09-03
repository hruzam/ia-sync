#!/usr/bin/env zsh
# =============================================================================
# temple-cs-manage.zsh — G: cold-start vault manager (temple family)
#
# Interface:
#   TUI (no args)       — cs-palette.py: D1/D2/D3 explorer + move keys
#   --list              — print all cards grouped by state, sorted
#   --to-card      <filename>
#   --to-archive   <filename>
#   --to-routines  <filename>
#
# Sort flags (--list and TUI both honour these):
#   --sort-date    filename-embedded YYYY-MM-DD newest-first (default)
#   --sort-name    alphabetical by filename
#   Env var TEMPLE_SORT=date|name sets the session default.
#   In TUI: press 's' to cycle sort modes.
#
# Canon: folder = state (raw.guides/cold-start-card/GUIDE.md).
#   Moves NEVER rewrite frontmatter; a card's content is untouched by a move.
#
# Note: TUI is cs-palette.py (merged from cs-manage-palette.py 2026-09-03 —
#   explorer + move in one view). CLI flags (--list/--to-*) remain for
#   scripting. EXECUTED script — never sourced.
# =============================================================================

[[ -f "${0:A:h}/temple-project-map.zsh" ]] && source "${0:A:h}/temple-project-map.zsh"

if ! typeset -f temple-project-root >/dev/null; then
  echo "temple-cs-manage: temple-project-map.zsh not found/sourced — cannot resolve reposoma root." >&2
  exit 1
fi

reposoma_root=$(temple-project-root reposoma) || exit 1
vault_root="${reposoma_root}/_cold-start"

if [[ ! -d "$vault_root" ]]; then
  echo "temple-cs-manage: vault not found at $vault_root" >&2
  exit 1
fi

typeset -A _cs_state_dir
_cs_state_dir=(card "$vault_root/card" routines "$vault_root/routines" archive "$vault_root/archive")

# ---------------------------------------------------------------------------
# Pre-parse sort flags — may appear anywhere in $@; TEMPLE_SORT env sets default.
# ---------------------------------------------------------------------------
sort_mode="${TEMPLE_SORT:-date}"
typeset -a _remaining_args
for _arg in "$@"; do
  case "$_arg" in
    --sort-date) sort_mode=date ;;
    --sort-name) sort_mode=name ;;
    *) _remaining_args+=("$_arg") ;;
  esac
done
set -- "${_remaining_args[@]}"
unset _arg _remaining_args

# _find_cs_file <filename> — search card/, routines/, archive/ for filename;
# prints "<state>\t<fullpath>" on the first hit, returns 1 if not found.
_find_cs_file() {
  local fname=$1
  local state
  for state in card routines archive; do
    local candidate="${_cs_state_dir[$state]}/$fname"
    if [[ -f "$candidate" ]]; then
      printf '%s\t%s\n' "$state" "$candidate"
      return 0
    fi
  done
  return 1
}

# _move_cs_file <filename> <dest-state> — locate the file in whichever state
# folder holds it, mv it into <dest-state>. No frontmatter rewriting, ever.
_move_cs_file() {
  local fname=$1
  local dest=$2
  local hit src_state src_path
  if ! hit=$(_find_cs_file "$fname"); then
    echo "Error: '$fname' not found in card/, routines/, or archive/." >&2
    return 1
  fi
  src_state="${hit%%$'\t'*}"
  src_path="${hit#*$'\t'}"
  if [[ "$src_state" == "$dest" ]]; then
    echo "Note: '$fname' is already in $dest/ — no move." >&2
    return 0
  fi
  local dest_dir="${_cs_state_dir[$dest]}"
  mkdir -p "$dest_dir"
  mv "$src_path" "$dest_dir/$fname"
}

# _sort_files_by_date — read fullpaths from stdin, print sorted newest first.
# Files without YYYY-MM-DD in name sort last.
_sort_files_by_date() {
  python3 -c "
import re, sys
pairs = []
for path in sys.stdin.read().splitlines():
    if not path:
        continue
    fname = path.rsplit('/', 1)[-1]
    m = re.findall(r'\d{4}-\d{2}-\d{2}', fname)
    pairs.append((m[-1] if m else '', path))
pairs.sort(key=lambda x: x[0], reverse=True)
print('\n'.join(p for _, p in pairs))
"
}

# _scan_cs_list — build tui_lines/tui_states/tui_paths for --list output.
# Uses sort_mode to order files within each state group.
_scan_cs_list() {
  tui_lines=()
  tui_states=()
  tui_paths=()

  local state
  local -a files sorted_files
  local total=0

  for state in card routines archive; do
    files=( "${_cs_state_dir[$state]}"/*.md(N.) )

    if [[ "$sort_mode" == "date" && ${#files} -gt 0 ]]; then
      sorted_files=( ${(f)"$(printf '%s\n' "${files[@]}" | _sort_files_by_date)"} )
    else
      sorted_files=( ${(o)files} )
    fi

    if [[ ${#files} -gt 0 ]]; then
      tui_lines+=("$state")
      tui_states+=("header")
      tui_paths+=("")
    fi
    for f in $sorted_files; do
      tui_lines+=("  $(basename "$f")")
      tui_states+=("file")
      tui_paths+=("$f")
      (( total++ ))
    done
  done

  if [[ total -eq 0 ]]; then
    tui_lines+=("(empty)")
    tui_states+=("empty")
    tui_paths+=("")
  fi
}

typeset -ga tui_lines tui_states tui_paths

# ---------------------------------------------------------------------------
# Dispatch
# ---------------------------------------------------------------------------
if [[ "$1" == "--list" ]]; then
  _scan_cs_list
  for i in {1..${#tui_lines}}; do
    echo "${tui_lines[i]}"
  done
  exit 0
elif [[ "$1" == "--to-card" || "$1" == "--to-archive" || "$1" == "--to-routines" ]]; then
  if [[ -z "$2" ]]; then
    echo "Error: Missing filename for $1" >&2
    exit 1
  fi
  dest="${1#--to-}"
  _move_cs_file "$2" "$dest" || exit 1
  exit 0
elif [[ -n "$1" ]]; then
  echo "Usage: $0 [--sort-date|--sort-name] [--list | --to-card <filename> | --to-archive <filename> | --to-routines <filename>]" >&2
  exit 1
fi

# TUI mode — cs-palette.py (merged explorer + mover: D1/D2/D3 + c/x/t keys)
exec python3 "${0:A:h}/cs-palette.py" --vault "$vault_root" --sort "$sort_mode"
