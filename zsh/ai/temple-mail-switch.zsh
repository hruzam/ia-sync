#!/usr/bin/env zsh
# temple-mail-switch.zsh — D: interactive mail-destination picker (temple family)
# host: office  (MACHINE_NAME=office)
# implements: 0010 R-b — read-side bound to temple-mail-inbox interface conventions
#
# Interface:
#   temple-mail-switch [--project <origin>]
#
# Output (stdout): exactly <origin>:<agent> on selection; nothing on ESC/cancel
# Exit code: 0 on selection, 1 on ESC/cancel/error
#
# Composable:
#   temple-mail $(temple-mail-switch) <scope> <body>
#
# Ordering: plain mtime-newest (temple-mail-inbox has no read-state convention —
#   no read-state invented here; 0010 R-b)
#
# Invariants (hard):
#   1. All physical paths resolved exclusively via temple-project-root (0004 L4)
#   2. Read-only: no mail writes, no mkdir, no read-state mutation
#   3. Read-side bound to temple-mail-inbox interface/conventions where they exist (0010 R-b)
#
# Degrade: if fzf is absent, falls back to a numbered zsh select menu (no preview),
#   same output contract.
#
# Depends on: temple-project-map.zsh (P0) — sources automatically if not loaded.

# --- Capture script directory at source time — needed by the function at runtime ---
_temple_mail_switch_dir="${0:h}"

# --- Load P0 if needed ---
if (( ${+functions[temple-project-root]} == 0 )); then
  _temple_mail_switch_map="${0:h}/temple-project-map.zsh"
  if [[ -f "$_temple_mail_switch_map" ]]; then
    source "$_temple_mail_switch_map"
  else
    print -u2 "temple-mail-switch: cannot find temple-project-map.zsh — source it first"
    return 1
  fi
  unset _temple_mail_switch_map
fi

temple-mail-switch() {
  local _usage="Usage: temple-mail-switch [--project <origin>]"
  local _filter_project=""

  # --- Parse arguments ---
  while (( $# > 0 )); do
    case "$1" in
      --project)
        if [[ -z "$2" ]]; then
          print -u2 "temple-mail-switch: --project requires an argument"
          print -u2 "$_usage"
          return 1
        fi
        _filter_project="$2"
        shift 2
        ;;
      --help|-h)
        print -- "$_usage"
        return 0
        ;;
      *)
        print -u2 "temple-mail-switch: unknown option '$1'"
        print -u2 "$_usage"
        return 1
        ;;
    esac
  done

  # --- Validate filter project if given ---
  if [[ -n "$_filter_project" ]]; then
    if [[ -z "${TEMPLE_PROJECT_MAP[$_filter_project]}" ]]; then
      print -u2 "temple-mail-switch: unknown project '${_filter_project}' — check TEMPLE_PROJECT_MAP"
      return 1
    fi
  fi

  # --- Determine which projects to scan ---
  local _projects=()
  if [[ -n "$_filter_project" ]]; then
    _projects=("$_filter_project")
  else
    _projects=("${(@k)TEMPLE_PROJECT_MAP}")
  fi

  # --- Build candidates with mtime sort key ---
  # Format of each raw entry: <mtime>:<origin>:<seat>
  # Ordering: plain mtime-newest (newest inbox activity first; no invented read-state)
  local _raw_candidates=()
  local _origin _root _mail_dir _seat_dir _seat _inbox _newest_name _mtime

  for _origin in "${_projects[@]}"; do
    # Paths only via temple-project-root (0004 L4); skip projects that fail
    # (other-host projects, missing dirs) — suppress error for multi-project full runs
    _root="$(temple-project-root "$_origin" 2>/dev/null)" || continue
    _mail_dir="${_root}/_mail"
    [[ -d "$_mail_dir" ]] || continue
    # *(N/) — null-glob + directory-only qualifier
    for _seat_dir in "${_mail_dir}"/*(N/); do
      _seat="${_seat_dir:t}"  # :t = tail (basename) in zsh
      _inbox="${_seat_dir}/inbox"
      _mtime=0
      if [[ -d "$_inbox" ]]; then
        # Find newest .md file by mtime — no glob (avoids nullglob issues in subshells)
        _newest_name="$(ls -t "$_inbox" 2>/dev/null | grep '\.md$' | head -1)"
        if [[ -n "$_newest_name" ]]; then
          _mtime="$(stat -c%Y "${_inbox}/${_newest_name}" 2>/dev/null)" || _mtime=0
        fi
      fi
      _raw_candidates+=("${_mtime}:${_origin}:${_seat}")
    done
  done

  if (( ${#_raw_candidates[@]} == 0 )); then
    print -u2 "temple-mail-switch: no mail seats found${_filter_project:+ for project '${_filter_project}'}"
    return 1
  fi

  # Sort by mtime descending (newest inbox activity first), then extract origin:seat
  local _candidates=()
  local _raw _rest
  while IFS= read -r _raw; do
    _rest="${_raw#*:}"    # strip leading <mtime>: — remainder is <origin>:<seat>
    [[ -n "$_rest" ]] && _candidates+=("$_rest")
  done < <(printf '%s\n' "${_raw_candidates[@]}" | sort -t: -k1,1rn)

  # --- Interactive selection ---
  local _selection=""

  if command -v fzf &>/dev/null; then
    # fzf path — preview shows head -40 of newest inbox file; frontmatter is self-describing
    local _map_file="${_temple_mail_switch_dir}/temple-project-map.zsh"

    # Build preview script: single-quoted to prevent zsh expansion here; MAPFILE
    # replaced below with the actual resolved path.
    # {} is replaced by fzf with the selected origin:agent line (no special chars → safe).
    local _preview_body
    _preview_body='line={}; origin="${line%%:*}"; agent="${line##*:}"; source "MAPFILE" 2>/dev/null; root=$(temple-project-root "$origin" 2>/dev/null) || { printf "(cannot resolve %s)\n" "$origin"; exit 0; }; inbox="${root}/_mail/${agent}/inbox"; if [[ ! -d "$inbox" ]]; then printf "(no inbox: %s)\n" "$line"; exit 0; fi; newest=$(ls -t "$inbox" 2>/dev/null | grep "\.md$" | head -1); if [[ -n "$newest" ]]; then head -40 "${inbox}/${newest}"; else printf "(inbox empty: %s)\n" "$line"; fi'
    # Substitute MAPFILE placeholder with the real path (path has no MAPFILE substring)
    _preview_body="${_preview_body/MAPFILE/${_map_file}}"

    _selection="$(printf '%s\n' "${_candidates[@]}" | fzf \
      --prompt "mail-dest> " \
      --header "Select destination (origin:agent) — ESC to cancel" \
      --preview "${_preview_body}" \
      --preview-window "right:50%:wrap")"
    local _fzf_status
    _fzf_status=$?
    if (( _fzf_status != 0 )) || [[ -z "$_selection" ]]; then
      return 1
    fi
  else
    # Degrade path: numbered zsh select menu (no preview) — same output contract
    print -u2 "temple-mail-switch: fzf not found — using select menu (no preview)"
    local PS3="Select mail destination [#]: "
    select _selection in "${_candidates[@]}"; do
      [[ -n "$_selection" ]] && break
      print -u2 "Invalid selection — enter a number from the list"
    done
    # Empty after loop = EOF (Ctrl-D) or no valid entry
    if [[ -z "$_selection" ]]; then
      return 1
    fi
  fi

  # Output contract: exactly origin:agent to stdout, nothing else
  print -- "$_selection"
}
