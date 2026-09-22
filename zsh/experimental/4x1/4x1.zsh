#!/usr/bin/env zsh
# =============================================================================
# 4x1 — tmux session bed. Fold a named session with N named windows.
# =============================================================================
# KIND    : interactive sourced function (lives in the shell), NOT an exp-run runner.
# STAGE   : experimental brick, hosted under experimental/4x1/ (operator call,
#           2026-09-22 — the staging brief originally proposed its own top-level
#           4x1/ scope; kept experimental instead). See the MAINTAINER LOG in
#           experimental/base.zsh for plug date / approval status.
# WIRING  : sourced by experimental/base.zsh PARTITION 3, by EXPLICIT name, gated
#           by `zsh -n` at load (a syntax error skips the source — command absent,
#           not shell dead). NOT sourced from zshrc — one loader on the machine,
#           not two per-host lines to keep in sync.
# CONTRACT: thin. Names windows and attaches. Never cd's, never launches an agent,
#           never writes state. Operator sits in each window and starts the seat.
# -----------------------------------------------------------------------------
# BUILDER / FUTURE-ME NOTES are inline below, prefixed `# NB:`. Read them before editing.
# =============================================================================

# NB: capture THIS file's directory at source time so the folder-local registry.json
#     is found while experimental. `%x` = file being sourced; `:A:h` = abs dir.
#     On canon, when registry.json moves to registries/, set $_4X1_REGISTRY instead —
#     this default just stops matching, it does not error (default window set still works).
typeset -g _4X1_DIR="${${(%):-%x}:A:h}"

# 4x1 [session] [win... | @registry-key] — fold/attach a tmux session with N named windows
4x1() {
  emulate -L zsh                       # NB: hygiene — local options, don't inherit caller's setopts

  # --- self-check (no tmux side effects) -----------------------------------
  if [[ $1 == --smoke ]]; then
    print "4x1: ok · dir=$_4X1_DIR · registry=${_4X1_REGISTRY:-$_4X1_DIR/registry.json}"
    command -v tmux >/dev/null || print -u2 "4x1: WARN tmux not found"
    command -v jq   >/dev/null || print -u2 "4x1: note jq absent — registry keys disabled, default set still works"
    return 0
  fi
  if [[ $1 == --help || $1 == -h ]]; then
    print -r -- 'usage: 4x1 [session] [win... | @registry-key]   (default wins: cSharp bus implement audit)'
    return 0
  fi

  # --- parse ----------------------------------------------------------------
  local s="$1"; (( $# )) && shift      # NB: shift only if there was an arg, else "shift" errors on empty $@
  local -a wins=("$@")                  # remaining args = window names (may be empty, or a single @key)

  # --- registry expansion: `4x1 <sess> @key` -------------------------------
  # NB: registry is OPTIONAL. jq missing / file missing / key missing -> wins stays empty
  #     -> falls through to the default set below. Never make this a hard dependency.
  local reg="${_4X1_REGISTRY:-$_4X1_DIR/registry.json}"
  if [[ ${wins[1]} == @* ]] && command -v jq >/dev/null && [[ -f $reg ]]; then
    wins=(${(f)"$(jq -r --arg k "${wins[1]#@}" '.[$k][]? // empty' $reg 2>/dev/null)"})
  fi
  (( ${#wins} )) || wins=(cSharp bus implement audit)   # NB: single source of the default set

  # --- default session name: first free default_<n> ------------------------
  if [[ -z $s ]]; then
    local n=1
    while tmux has-session -t "=default_$n" 2>/dev/null; do (( n++ )); done   # NB: "=" = exact match
    s="default_$n"
  fi

  # --- build or re-enter ----------------------------------------------------
  if tmux has-session -t "=$s" 2>/dev/null; then
    print -u2 "4x1: '$s' exists — attaching"      # NB: idempotent. Never rebuild a live session.
  else
    tmux new-session -d -s "$s" -n "${wins[1]}" || return   # NB: -d so we can add windows before attach
    local w
    for w in "${wins[@]:1}"; do tmux new-window -t "=$s:" -n "$w"; done
    tmux select-window -t "=$s:${wins[1]}"          # NB: land on the first window, not the last created
  fi

  # NB: inside tmux -> switch-client (no nested session). Outside -> attach.
  [[ -n $TMUX ]] && tmux switch-client -t "=$s" || tmux attach -t "=$s"
}
