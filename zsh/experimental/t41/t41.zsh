#!/usr/bin/env zsh
# =============================================================================
# t41 — tmux session bed. Fold a named session with N named windows.
# =============================================================================
# NAME    : renamed from 4x1 → t41, 2026-09-22 (same session, operator call) —
#           4x1's leading digit was the exact class that broke the palette
#           generator's function-name regex (ai/palette-map-gen.py); t41 (a
#           letter-first identifier) sidesteps that whole class of friction.
#           Old references ("4x1") in the maintainer log / journal history
#           below this date describe the SAME brick under its original name.
# KIND    : interactive sourced function (lives in the shell), NOT an exp-run runner.
# STAGE   : experimental brick, hosted under experimental/t41/ (operator call,
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
#     On canon, when registry.json moves to registries/, set $_T41_REGISTRY instead —
#     this default just stops matching, it does not error (default window set still works).
typeset -g _T41_DIR="${${(%):-%x}:A:h}"

# t41 [session] [win... | @registry-key] — fold/attach a tmux session with N named windows
t41() {
  emulate -L zsh                       # NB: hygiene — local options, don't inherit caller's setopts

  # --- self-check (no tmux side effects) -----------------------------------
  if [[ $1 == --smoke ]]; then
    print "t41: ok · dir=$_T41_DIR · registry=${_T41_REGISTRY:-$_T41_DIR/registry.json}"
    command -v tmux >/dev/null || print -u2 "t41: WARN tmux not found"
    command -v jq   >/dev/null || print -u2 "t41: note jq absent — registry keys disabled, default set still works"
    return 0
  fi
  if [[ $1 == --help || $1 == -h ]]; then
    print -r -- 'usage: t41 [session] [win... | @registry-key]   (default wins: cSharp bus implement audit)'
    print -r -- '       t41 <existing-session> <existing-window>  -> join as a grouped session'
    print -r -- '           locked to that window (second terminal, no twin-window collision)'
    return 0
  fi

  # --- parse ----------------------------------------------------------------
  local s="$1"; (( $# )) && shift      # NB: shift only if there was an arg, else "shift" errors on empty $@
  local -a wins=("$@")                  # remaining args = window names (may be empty, or a single @key)

  # --- registry expansion: `t41 <sess> @key` -------------------------------
  # NB: registry is OPTIONAL. jq missing / file missing / key missing -> wins stays empty
  #     -> falls through to the default set below. Never make this a hard dependency.
  local reg="${_T41_REGISTRY:-$_T41_DIR/registry.json}"
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
    # --- join as a grouped session, locked to one window ---------------------
    # NB: tmux tracks "current window" per SESSION, not per client. A second
    #     terminal that plain-attaches to $s becomes a second client on the
    #     SAME session, so switching windows in either terminal drags the
    #     other along ("twin window" collision). A grouped session (new
    #     session sharing $s's windows/panes via `-t`) tracks its own current
    #     window instead, so two terminals can sit on two different windows
    #     of the same fold without colliding.
    #     Trigger: exactly one window name given, and it already exists in $s.
    if (( ${#wins} == 1 )) && tmux list-windows -t "=$s" -F '#{window_name}' 2>/dev/null | grep -qxF -- "${wins[1]}"; then
      local gs="${s}--${wins[1]}"        # NB: stable name -> re-running the join re-enters, not a pileup
      if ! tmux has-session -t "=$gs" 2>/dev/null; then
        tmux new-session -t "=$s" -s "$gs" -d || return   # NB: -t joins $s's window group; -d, select before attach
      fi
      tmux select-window -t "=$gs:${wins[1]}"
      print -u2 "t41: joining '$s' locked to window '${wins[1]}' (group session '$gs')"
      [[ -n $TMUX ]] && tmux switch-client -t "=$gs" || tmux attach -t "=$gs"
      return
    fi
    print -u2 "t41: '$s' exists — attaching"      # NB: idempotent. Never rebuild a live session.
  else
    tmux new-session -d -s "$s" -n "${wins[1]}" || return   # NB: -d so we can add windows before attach
    local w
    for w in "${wins[@]:1}"; do tmux new-window -t "=$s:" -n "$w"; done
    tmux select-window -t "=$s:${wins[1]}"          # NB: land on the first window, not the last created
  fi

  # NB: inside tmux -> switch-client (no nested session). Outside -> attach.
  [[ -n $TMUX ]] && tmux switch-client -t "=$s" || tmux attach -t "=$s"
}
