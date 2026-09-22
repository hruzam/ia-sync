#!/usr/bin/env zsh
# Experimental dispatcher — sourced by experimental/base.zsh (P2).
# Runners stay lazy: only exp-run sources no experiment at shell startup.
#
# _exp_list enumerates BOTH brick kinds (2026-09-22 — was runner-only, a real
# discoverability gap: a sourced brick like t41 never showed up). _exp_run stays
# runner-only by design (a sourced brick must load in the interactive shell, not
# a subprocess) — it now just says so instead of "unknown experiment" when the
# id names a real sourced brick.

typeset -g _EXPERIMENTAL_ROOT="${_EXPERIMENTAL_ROOT:-${HOME}/.config/zsh/experimental}"

_exp_list() {
  local -a dirs
  local d id
  local -a rows

  dirs=( "${_EXPERIMENTAL_ROOT}"/*(N/) )   # top-level subdirectories only

  for d in "${dirs[@]}"; do
    id="${d:t}"
    # NB: $'\t' must be its OWN quoted segment, not embedded inside a "..."
    # string — printf sidesteps the whole quoting trap and is unambiguous.
    if [[ -f "${d}/runner.zsh" ]]; then
      rows+=("$(printf '%s\t%s' "${id}" "exp-run ${id}")")
    elif [[ -f "${d}/${id}.zsh" ]]; then
      rows+=("$(printf '%s\t%s  (sourced — call directly, not via exp-run)' "${id}" "${id}")")
    fi
    # neither convention matched: not a brick (e.g. a data-only folder) — skip silently
  done

  if (( ${#rows[@]} == 0 )); then
    print 'No experimental bricks installed.'
    return 0
  fi

  local row
  { for row in "${rows[@]}"; do
      print -- "${row}"
    done } | column -t -s $'\t' 2>/dev/null || print -l -- "${rows[@]}"
}

_exp_run() {
  local id="${1:-}"
  local runner

  if [[ ! "$id" =~ '^[a-z0-9][a-z0-9-]*$' ]]; then
    print -u2 'Usage: exp-run <experiment-id> [arguments]'
    return 2
  fi
  shift

  runner="${_EXPERIMENTAL_ROOT}/${id}/runner.zsh"
  if [[ ! -f "$runner" ]]; then
    if [[ -f "${_EXPERIMENTAL_ROOT}/${id}/${id}.zsh" ]]; then
      print -u2 "exp-run: '${id}' is a sourced brick, not a runner — call it directly: ${id}"
    else
      print -u2 "exp-run: unknown experiment: $id"
      print -u2 'Run exp-list to see installed experiments.'
    fi
    return 2
  fi

  zsh "$runner" "$@"
}
