#!/usr/bin/env zsh
# =============================================================================
# temple-mail-manage.zsh — E: mailbox read-state manager (temple family)
#
# Interface:
#   TUI (no args)
#   --list
#   --archive <receiver>/<filename>
#   --restore <receiver>/<filename>
#
# Canon: implements decision 0010 read-state transition
#   presence in inbox/ = unread; move to archive/ = read; receiver-owns
#
# Note: EXECUTED script — never sourced (uses exit/stty);
#   discovers _mail by walking up from $PWD
#
# Provenance: adopted from temple/tools/mail-switch.zsh provisorium,
#   2026-07-11, gavel majkee; key name per @Janus claviature verdict
#   (gate visible in the name).
# =============================================================================

# Find _mail directory
dir="$PWD"
mail_root=""
while true; do
  if [[ -d "$dir/_mail" ]]; then
    mail_root="$dir/_mail"
    break
  fi
  [[ "$dir" == "/" ]] && break
  dir=$(dirname "$dir")
done

if [[ -z "$mail_root" ]]; then
  echo "Error: _mail directory not found in any parent directory." >&2
  exit 1
fi

typeset -ga tui_lines
typeset -ga tui_types
typeset -ga tui_paths

_move_mail_file() {
  local rec=$1
  local fname=$2
  local verb=$3
  local src dest_dir dest

  if [[ "$verb" == "archive" ]]; then
    src="$mail_root/$rec/inbox/$fname"
    dest_dir="$mail_root/$rec/archive"
  else
    src="$mail_root/$rec/archive/$fname"
    dest_dir="$mail_root/$rec/inbox"
  fi
  dest="$dest_dir/$fname"
  if [[ ! -f "$src" ]]; then
    echo "Error: File $src does not exist." >&2
    return 1
  fi
  mkdir -p "$dest_dir"
  mv "$src" "$dest"
}

_scan_mail() {
  local map_file=$1
  tui_lines=()
  tui_types=()
  tui_paths=()

  local -a rec_dirs
  rec_dirs=( "$mail_root"/*(N/) )

  local total_files=0
  local target_subdir
  local -a files

  for r_dir in ${(o)rec_dirs}; do
    local r=$(basename "$r_dir")
    for target_subdir in inbox archive; do
      files=( "$r_dir"/$target_subdir/*(N.) )
      if [[ -z "$map_file" && "$target_subdir" == "inbox" && ${#files} -gt 0 ]]; then
        tui_lines+=("$r")
        tui_types+=("header")
        tui_paths+=("")
      fi

      for f in ${(o)files}; do
        if [[ -n "$map_file" ]]; then
          printf '%s\t%s\t%s\t%s\n' "$target_subdir" "$r" "$(basename "$f")" "$f" >> "$map_file"
        elif [[ "$target_subdir" == "inbox" ]]; then
          tui_lines+=("") # placeholder
          tui_types+=("file")
          tui_paths+=("$f")
          (( total_files++ ))
        fi
      done
    done
  done

  if [[ -z "$map_file" && total_files -eq 0 ]]; then
    tui_lines+=("(empty)")
    tui_types+=("empty")
    tui_paths+=("")
  fi
}

# Parse arguments
if [[ "$1" == "--list" ]]; then
  _scan_mail
  for i in {1..${#tui_lines}}; do
    if [[ "${tui_types[i]}" == "header" ]]; then
      echo "${tui_lines[i]}"
    elif [[ "${tui_types[i]}" == "file" ]]; then
      echo "  [ ] $(basename "${tui_paths[i]}")"
    else
      echo "${tui_lines[i]}"
    fi
  done
  exit 0
elif [[ "$1" == "--archive" ]]; then
  if [[ -z "$2" ]]; then
    echo "Error: Missing argument for --archive" >&2
    exit 1
  fi
  rec_file="$2"
  if [[ "$rec_file" != */* ]]; then
    echo "Error: Invalid argument format. Expected <receiver>/<filename>" >&2
    exit 1
  fi
  rec="${rec_file%%/*}"
  fname="${rec_file#*/}"
  _move_mail_file "$rec" "$fname" archive || exit 1
  exit 0
elif [[ "$1" == "--restore" ]]; then
  if [[ -z "$2" ]]; then
    echo "Error: Missing argument for --restore" >&2
    exit 1
  fi
  rec_file="$2"
  if [[ "$rec_file" != */* ]]; then
    echo "Error: Invalid argument format. Expected <receiver>/<filename>" >&2
    exit 1
  fi
  rec="${rec_file%%/*}"
  fname="${rec_file#*/}"
  _move_mail_file "$rec" "$fname" restore || exit 1
  exit 0
elif [[ -n "$1" ]]; then
  echo "Usage: $0 [--list | --archive <receiver>/<filename> | --restore <receiver>/<filename>]" >&2
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
  printf '# view\treceiver\tfilename\tfullpath\n' > "$tsvfile"
  _scan_mail "$tsvfile"

  actions=$(python3 "${0:A:h}/mail-palette.py" --map "$tsvfile")
  palette_status=$?
  (( palette_status != 0 )) && break

  while IFS=$'\t' read -r rec_file verb; do
    [[ -z "$rec_file" ]] && continue
    rec="${rec_file%%/*}"
    fname="${rec_file#*/}"
    _move_mail_file "$rec" "$fname" "$verb" || {
      _cleanup
      exit 1
    }
  done <<< "$actions"
done

rm -f -- "$tsvfile"
tsvfile=""
_cleanup
exit 0
