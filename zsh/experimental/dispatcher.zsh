#!/usr/bin/env zsh
# Experimental-runner dispatcher — sourced by experimental/base.zsh (P2).
# Runners stay lazy: only exp-run sources no experiment at shell startup.

typeset -g _EXPERIMENTAL_ROOT="${_EXPERIMENTAL_ROOT:-${HOME}/.config/zsh/experimental}"

_exp_list() {
  local -a runners
  local runner
  runners=( "${_EXPERIMENTAL_ROOT}"/*/runner.zsh(N) )

  if (( ${#runners[@]} == 0 )); then
    print 'No experimental runners installed.'
    return 0
  fi

  for runner in "${runners[@]}"; do
    print -- "${runner:h:t}"
  done
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
    print -u2 "exp-run: unknown experiment: $id"
    print -u2 'Run exp-list to see installed experiments.'
    return 2
  fi

  zsh "$runner" "$@"
}
