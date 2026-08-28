#!/usr/bin/env zsh
# =============================================================================
# temple-cs-manage.zsh — G: cold-start vault state mover (temple family)
#
# Interface:
#   TUI (no args)
#   --list
#   --to-card      <filename>
#   --to-archive   <filename>
#   --to-routines  <filename>
#
# Canon: folder = state (raw.guides/cold-start-card/GUIDE.md) — card/ (live
#   process glue) · routines/ (recurring, never archived by policy, but this
#   tool does not forbid it — the operator's call) · archive/ (drained).
#   Moves NEVER rewrite frontmatter; a card's content is untouched by a move.
#
# Note: EXECUTED script — never sourced (uses exit/stty); resolves the vault
#   root via temple-project-map's `temple-project-root reposoma`, same
#   discipline as cs-palette.zsh — only the folder name `_cold-start` is
#   baked, the map absorbs a reposoma relocation.
#
# Sibling to temple-mail-manage.zsh (mirrors its --list/TUI grammar); the
# cold-start vault has no per-receiver split and three states instead of
# mail's two (inbox/archive), so the verb pair (--archive/--restore) becomes
# three explicit destination flags instead.
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

typeset -ga tui_lines
typeset -ga tui_states
typeset -ga tui_paths

_scan_cs() {
  local map_file=$1
  tui_lines=()
  tui_states=()
  tui_paths=()

  local state
  local -a files
  local total=0
  # NOTE: the loop variable `f` is deliberately NOT `local`-declared inside the
  # per-state loop below — zsh's `local name` (no `=value`, no options) acts as
  # an INSPECTOR and prints the variable's current value to stdout when a
  # local of that name already exists in the same function scope (only a
  # brand-new local stays silent). Re-declaring `local f` once per `state`
  # iteration polluted --list / TUI output with stray "f=<path>" lines.
  # temple-mail-manage.zsh's _scan_mail avoids this the same way: `f` is used
  # as a bare loop variable, never explicitly localized.

  for state in card routines archive; do
    files=( "${_cs_state_dir[$state]}"/*.md(N.) )
    if [[ -n "$map_file" ]]; then
      for f in ${(o)files}; do
        printf '%s\t%s\t%s\n' "$state" "$(basename "$f")" "$f" >> "$map_file"
      done
    else
      if [[ ${#files} -gt 0 ]]; then
        tui_lines+=("$state")
        tui_states+=("header")
        tui_paths+=("")
      fi
      for f in ${(o)files}; do
        tui_lines+=("  $(basename "$f")")
        tui_states+=("file")
        tui_paths+=("$f")
        (( total++ ))
      done
    fi
  done

  if [[ -z "$map_file" && total -eq 0 ]]; then
    tui_lines+=("(empty)")
    tui_states+=("empty")
    tui_paths+=("")
  fi
}

# Parse arguments
if [[ "$1" == "--list" ]]; then
  _scan_cs
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
  echo "Usage: $0 [--list | --to-card <filename> | --to-archive <filename> | --to-routines <filename>]" >&2
  exit 1
fi

# Interactive TUI mode
term_state=$(stty -g 2>/dev/null)
tsvfile=$(mktemp) || exit 1

_cleanup() {
  trap - INT TERM EXIT
  [[ -n "$tsvfile" && -f "$tsvfile" ]] && rm -f -- "$tsvfile"
  tput rmcup 2>/dev/null
  tput cnorm 2>/dev/null
  if [[ -n "$term_state" ]]; then
    stty "$term_state" 2>/dev/null
  else
    stty sane 2>/dev/null
  fi
}

trap _cleanup INT TERM EXIT

tput smcup 2>/dev/null
tput civis 2>/dev/null
stty -icanon -echo

while true; do
  printf '# state\tfilename\tfullpath\n' > "$tsvfile"
  _scan_cs "$tsvfile"

  actions=$(python3 "${0:A:h}/cs-manage-palette.py" --map "$tsvfile")
  palette_status=$?
  (( palette_status != 0 )) && break

  while IFS=$'\t' read -r fname dest; do
    [[ -z "$fname" ]] && continue
    _move_cs_file "$fname" "$dest" || {
      _cleanup
      exit 1
    }
  done <<< "$actions"
done

rm -f -- "$tsvfile"
tsvfile=""
_cleanup
exit 0
