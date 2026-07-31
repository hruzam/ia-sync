#!/usr/bin/env zsh
# =============================================================================
# TEMPLE-PROJECT-SURFACE.ZSH — interactive surface over TEMPLE_PROJECT_MAP
# =============================================================================
# Location: ~/.config/zsh/ai/temple-project-surface.zsh
# Sourced by: base.zsh PARTITION 10
# Requires: temple-project-map.zsh (P0) loaded first — TEMPLE_PROJECT_MAP must exist.
# Aliases:  keyboard.zsh PARTITION 15
#
# Bodies exposed:
#   _project_paths        → project-paths         list all projects + absolute paths
#   _project_git_status   → project-git-status    git status table across all projects
#   _project_commit_all   → project-commit-all    interactive day-phase batch commit
#   _project_pick_zle     → bindkey '^[p' (Alt-p) fzf picker; inserts path into buffer
#
# Note: loop-local variables MUST be declared at function top (not inside the
# loop body) — re-declaring `local` inside a zsh loop emits the previous value.
# =============================================================================

# ── _project_paths ────────────────────────────────────────────────────────────
# Print all project names and their absolute paths from TEMPLE_PROJECT_MAP.
#   (no args)   human-readable table
#   --plain     "<name>\t<path>" per line (pipe-friendly; agents read this)
#   --paths     absolute paths only, one per line (xargs input)
_project_paths() {
  if (( ${#TEMPLE_PROJECT_MAP[@]} == 0 )); then
    print -u2 "project-paths: TEMPLE_PROJECT_MAP empty — source temple-project-map.zsh first"
    return 1
  fi

  local mode="table"
  case "${1:-}" in
    --plain) mode="plain" ;;
    --paths) mode="paths" ;;
  esac

  local -a names
  names=( ${(ko)TEMPLE_PROJECT_MAP} )   # alphabetical

  local name  # loop var declared once
  case "${mode}" in
    table)
      printf "%-30s %s\n" "PROJECT" "PATH"
      printf "%-30s %s\n" "-------" "----"
      for name in "${names[@]}"; do
        printf "%-30s %s\n" "${name}" "${TEMPLE_PROJECT_MAP[$name]}"
      done
      ;;
    plain)
      for name in "${names[@]}"; do
        printf "%s\t%s\n" "${name}" "${TEMPLE_PROJECT_MAP[$name]}"
      done
      ;;
    paths)
      for name in "${names[@]}"; do
        print -- "${TEMPLE_PROJECT_MAP[$name]}"
      done
      ;;
  esac
}

# ── _project_git_status ───────────────────────────────────────────────────────
# Show git state for every project in TEMPLE_PROJECT_MAP.
# Columns: project · dirty/clean · ↓behind ↑ahead · branch · path
_project_git_status() {
  if (( ${#TEMPLE_PROJECT_MAP[@]} == 0 )); then
    print -u2 "project-git-status: TEMPLE_PROJECT_MAP empty"
    return 1
  fi

  local -a names
  names=( ${(ko)TEMPLE_PROJECT_MAP} )

  # Declare all loop-local vars ONCE here (re-declaring inside loop emits prev value)
  local name root branch dirty ahead_behind ab behind ahead

  printf "%-28s %-7s %-13s %-18s %s\n" "PROJECT" "STATUS" "AHEAD/BEHIND" "BRANCH" "PATH"
  printf "%-28s %-7s %-13s %-18s %s\n" "-------" "------" "------------" "------" "----"

  for name in "${names[@]}"; do
    root="${TEMPLE_PROJECT_MAP[$name]}"

    if ! git -C "${root}" rev-parse --git-dir &>/dev/null 2>&1; then
      printf "%-28s %-7s %-13s %-18s %s\n" "${name}" "no-git" "-" "-" "${root}"
      continue
    fi

    branch=$(git -C "${root}" rev-parse --abbrev-ref HEAD 2>/dev/null)
    branch="${branch%%$'\n'*}"   # strip trailing newline (exit-128 repos output HEAD\n)
    [[ -z "${branch}" ]] && branch="?"

    if [[ -n "$(git -C "${root}" status --porcelain 2>/dev/null)" ]]; then
      dirty="dirty"
    else
      dirty="clean"
    fi

    ab=$(git -C "${root}" rev-list --left-right --count "@{upstream}...HEAD" 2>/dev/null)
    if [[ -n "${ab}" ]]; then
      behind="${ab%%$'\t'*}"
      ahead="${ab##*$'\t'}"
      ahead_behind="↓${behind} ↑${ahead}"
    else
      ahead_behind="-"
    fi

    printf "%-28s %-7s %-13s %-18s %s\n" "${name}" "${dirty}" "${ahead_behind}" "${branch}" "${root}"
  done
}

# ── _project_commit_all ───────────────────────────────────────────────────────
# Walk every project in TEMPLE_PROJECT_MAP; for each with uncommitted changes:
#   1. Print branch, short status
#   2. Prompt for a commit message (empty = skip)
#   3. git add -A && git commit -m "<msg>"
#
# Flags:
#   --dry     show what would be committed, skip all writes
#   --push    also run git push after each successful commit
_project_commit_all() {
  if (( ${#TEMPLE_PROJECT_MAP[@]} == 0 )); then
    print -u2 "project-commit-all: TEMPLE_PROJECT_MAP empty"
    return 1
  fi

  local dry=0 do_push=0
  for arg in "$@"; do
    case "${arg}" in
      --dry)  dry=1 ;;
      --push) do_push=1 ;;
    esac
  done

  local -a names
  names=( ${(ko)TEMPLE_PROJECT_MAP} )

  # Loop-local vars declared once
  local name root status_out msg branch_label
  local committed=0 skipped=0 no_changes=0

  for name in "${names[@]}"; do
    root="${TEMPLE_PROJECT_MAP[$name]}"

    if ! git -C "${root}" rev-parse --git-dir &>/dev/null 2>&1; then
      continue
    fi

    status_out=$(git -C "${root}" status --porcelain 2>/dev/null)
    if [[ -z "${status_out}" ]]; then
      (( no_changes++ ))
      continue
    fi

    branch_label=$(git -C "${root}" rev-parse --abbrev-ref HEAD 2>/dev/null)
    branch_label="${branch_label%%$'\n'*}"
    [[ -z "${branch_label}" ]] && branch_label="?"

    print ""
    print "━━━ ${name} ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    printf "  path:   %s\n" "${root}"
    printf "  branch: %s\n" "${branch_label}"
    print ""
    git -C "${root}" status --short
    print ""

    if (( dry )); then
      print "  [dry] no action taken"
      (( skipped++ ))
      continue
    fi

    print -n "  commit message (empty = skip this project): "
    read -r msg </dev/tty
    if [[ -z "${msg}" ]]; then
      print "  → skipped"
      (( skipped++ ))
      continue
    fi

    git -C "${root}" add -A && git -C "${root}" commit -m "${msg}"
    if (( do_push )); then
      git -C "${root}" push
    fi
    (( committed++ ))
  done

  print ""
  print "project-commit-all done — committed: ${committed}  skipped: ${skipped}  clean: ${no_changes}"
}

# ── _project_pick_zle ─────────────────────────────────────────────────────────
# ZLE widget: fzf project picker.
# Inserts the selected project's absolute path at the cursor position.
# Without fzf: falls back to printing the list in the zle message area.
# Bind in keyboard.zsh PARTITION 15: bindkey '^[p' _project_pick_zle  (Alt-p)
_project_pick_zle() {
  if (( ${#TEMPLE_PROJECT_MAP[@]} == 0 )); then
    zle -M "project-pick: TEMPLE_PROJECT_MAP empty — source temple-project-map.zsh"
    return 1
  fi

  local -a names
  names=( ${(ko)TEMPLE_PROJECT_MAP} )

  if command -v fzf &>/dev/null; then
    # Build tab-delimited list: col1=name (shown), col2=path (preview + result)
    local fzf_list=""
    local n
    for n in "${names[@]}"; do
      fzf_list+="${n}"$'\t'"${TEMPLE_PROJECT_MAP[$n]}"$'\n'
    done

    local selected
    selected=$(printf '%s' "${fzf_list}" \
      | fzf --height=40% --reverse \
            --prompt="project❯ " \
            --with-nth=1 \
            --delimiter=$'\t' \
            --preview='echo {2}' \
            --preview-window=down:1:wrap \
            </dev/tty 2>/dev/tty)

    [[ -z "${selected}" ]] && { zle reset-prompt; return 0; }
    local path="${selected##*$'\t'}"
    LBUFFER+="${path}"

  else
    # Fallback: show list in zle message area (read-only, no insertion)
    local msg="project paths (install fzf for picker):"$'\n'
    local n
    for n in "${names[@]}"; do
      msg+="  ${n}  ${TEMPLE_PROJECT_MAP[$n]}"$'\n'
    done
    zle -M "${msg}"
  fi

  zle reset-prompt
}
zle -N _project_pick_zle

# ── _project_help ─────────────────────────────────────────────────────────────
# Help panel for the project-map surface. Called by ai-help (master panel).
# Alias: project-help (keyboard.zsh PARTITION 15).
_project_help() {
  cat <<'EOF'
project surface — TEMPLE_PROJECT_MAP interactive panel (engine: temple-project-surface.zsh)

  project-paths              list all project names + absolute paths (table)
  project-paths --plain      "<name>\t<path>" per line  (pipe to agents; ~/.remote/task.md)
  project-paths --paths      absolute paths only, one per line  (xargs / while-read input)
  project-git-status         git state for every project: dirty/clean · ↓behind ↑ahead · branch
  project-commit-all         interactive day-phase batch commit across all projects
  project-commit-all --dry   preview what would be committed, no writes
  project-commit-all --push  commit + push in one pass
  Alt-p  (^[p)               fzf project picker — inserts selected path at cursor (ZLE widget)
  project-help               this panel

  Source:  TEMPLE_PROJECT_MAP  (~/.config/zsh/ai/temple-project-map.zsh, P0 / base.zsh P3)
  Engine:  ~/.config/zsh/ai/temple-project-surface.zsh  (base.zsh P10)
EOF
}
