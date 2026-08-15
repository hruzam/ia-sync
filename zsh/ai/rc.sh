#!/usr/bin/env bash
# rc.sh — Claude Code Remote Control launcher/engine (tmux on-demand, agent-aware).
#
# Generalized 2026-08-15 (absorbs reposoma/raw.guides/remote-control/spawn-rc-term.sh):
#   • ANY project resolves via registries/projects.json (not just the registered trio)
#   • agent / model / effort params, defaulted from registries/ai.json launch-defaults
#   • real pty from tmux (so `claude --remote-control` pairs, no --print fallback)
#   • render polish proven over ssh: attach with `tmux -u -2`, allow-passthrough,
#     status off, truecolor — fixes missing glyphs (spinner/pointers/logo) + colors
#   • LOCAL spawn only. Cross-host dispatch is the /rc-launch skill's job (it ssh's
#     to the target host and calls THIS engine there).
#
# Wiring: registry data lives in JSON (projects.json = paths, ai.json = RC params,
# hosts.json = host identities). This script stays a clean executive — no literals.
#
# Usage:
#   rc.sh                        list live rc-* sessions + registered projects
#   rc.sh status                 same
#   rc.sh <project>              start-or-attach (interactive; auto-detaches if no TTY)
#   rc.sh <project> stop         stop the session
#   rc.sh <project> [opts]       start with opts:
#       --agent <a>  --model <m>  --effort <e>  --name "<RC name>"  --detach
set -uo pipefail

REG_DIR="${RC_REG_DIR:-${HOME}/.config/zsh/registries}"   # override for pre-deploy testing
PROJECTS="${REG_DIR}/projects.json"      # authoritative paths
REGISTRY="${REG_DIR}/ai.json"            # RC params + launch-defaults
HOSTS="${REG_DIR}/hosts.json"            # host identities (for the ssh reach line)

_check_jq() { command -v jq &>/dev/null || { echo "rc.sh: jq required" >&2; exit 1; }; }

# ---- resolvers (all read JSON; no hardcoded literals) ----
_project_path()   {  # projects.json is authoritative; ai.json path is fallback for
                      # legacy-registered projects intentionally absent from the map (e.g. nabla-lab)
  local p="$1" path
  path=$(jq -r --arg p "$p" '.projects[$p] // empty' "$PROJECTS" 2>/dev/null)
  [ -z "$path" ] && path=$(jq -r --arg p "$p" '."remote-control".projects[$p].path // empty' "$REGISTRY" 2>/dev/null)
  echo "$path"
}
_rc_name()        { local n; n=$(jq -r --arg p "$1" '."remote-control".projects[$p].rc_name // empty' "$REGISTRY" 2>/dev/null); [ -n "$n" ] && echo "$n" || echo "$1"; }
_default_agent()  { jq -r --arg p "$1" '."remote-control"."launch-defaults"."per-project"[$p].agent // empty' "$REGISTRY" 2>/dev/null; }
_default_model()  { jq -r '."remote-control"."launch-defaults".model  // "opus"' "$REGISTRY" 2>/dev/null; }
_default_effort() { jq -r '."remote-control"."launch-defaults".effort // empty'  "$REGISTRY" 2>/dev/null; }
_self_host() {
  local h=""
  [ -n "${MACHINE_NAME:-}" ] && h=$(jq -r --arg m "$MACHINE_NAME" '.hosts[]|select(.machine_name==$m)|.tailscale_dns' "$HOSTS" 2>/dev/null)
  [ -z "$h" ] && h=$(tailscale status --json 2>/dev/null | jq -r '.Self.DNSName // empty' | sed 's/\.$//' || true)
  [ -z "$h" ] && h=$(hostname)
  echo "$h"
}

_reach() {  # detached-mode report: the three viewports onto the one tmux session
  local session="$1" agent="$2" model="$3" effort="$4"
  local host url
  host=$(_self_host)
  url=$(tmux capture-pane -p -t "$session" 2>/dev/null | grep -oE 'https://claude\.ai/code/session_[A-Za-z0-9]+' | head -1 || true)
  echo "OK: '$session' held in tmux — agent=${agent:-<default>} model=$model${effort:+ effort=$effort}"
  echo "   • home→host    : ssh ${host} -t 'tmux -u -2 attach -t $session'"
  echo "   • host desktop : WAYLAND_DISPLAY=wayland-0 XDG_RUNTIME_DIR=${XDG_RUNTIME_DIR:-/run/user/$(id -u)} konsole -e tmux -u -2 attach -t $session"
  echo "   • Remote Control: ${url:-<visible on the first screen once you attach>}"
  echo "   stop: tmux kill-session -t $session"
}

_polish() {  # tmux render fixes (proven over ssh 2026-08-15); safe if already set
  local session="$1"
  tmux set-option -ga terminal-overrides ",*:Tc"       2>/dev/null || true
  tmux set-option -g  default-terminal "tmux-256color" 2>/dev/null || true
  tmux set-option -ga terminal-features "*:RGB"        2>/dev/null || true
  tmux set-option -g  allow-passthrough on             2>/dev/null || true
  tmux set-option -t "$session" status off             2>/dev/null || true
}

_start() {
  local project="$1" agent="$2" model="$3" effort="$4" detach="$5" rcname="$6"
  _check_jq
  local path; path=$(_project_path "$project")
  if [ -z "$path" ]; then
    echo "rc.sh: unknown project '$project'. Known: $(jq -r '.projects|keys|join(", ")' "$PROJECTS")" >&2; exit 1
  fi
  [ -d "$path" ] || { echo "rc.sh: project '$project' → '$path' not present on this host ($(hostname))" >&2; exit 1; }
  # agent is OPTIONAL at the engine level (empty → claude's default agent, preserving
  # the legacy rc-freya/rc-nabla aliases). The /rc-launch skill enforces "agent required".
  [ -z "$rcname" ] && rcname=$(_rc_name "$project")
  local session="rc-${project}"

  if tmux has-session -t "$session" 2>/dev/null; then
    echo "rc.sh: session '$session' already alive — reusing."
  else
    local cmd="claude"
    [ -n "$agent" ]  && cmd="${cmd} --agent ${agent}"
    cmd="${cmd} --model ${model}"
    [ -n "$effort" ] && cmd="${cmd} --effort ${effort}"
    cmd="${cmd} --remote-control '${rcname}'"
    tmux new-session -d -s "$session" -c "$path" "$cmd"
  fi
  _polish "$session"

  # auto-detach when there is no controlling TTY (agent/headless/cross-host caller)
  if [ "$detach" = "0" ] && [ ! -t 1 ]; then detach=1; fi

  if [ "$detach" = "0" ]; then
    exec tmux -u -2 attach -t "$session"
  fi
  _reach "$session" "$agent" "$model" "$effort"
}

_stop() {
  local project="$1"; local session="rc-${project}"
  if tmux has-session -t "$session" 2>/dev/null; then
    tmux kill-session -t "$session"; echo "rc.sh: stopped $session"
  else
    echo "rc.sh: not running: $session"
  fi
}

_list_status() {
  _check_jq
  echo "live rc-* tmux sessions:"
  tmux ls 2>/dev/null | grep '^rc-' | sed 's/^/  /' || echo "  (none)"
  echo
  echo "registered projects (ai.json remote-control.projects):"
  jq -r '."remote-control".projects | to_entries[] | "  \(.key)  →  session=\(.value.tmux_session)  available=\(.value.available)"' "$REGISTRY" 2>/dev/null
  echo
  echo "launchable projects (projects.json): $(jq -r '.projects|keys|join(", ")' "$PROJECTS" 2>/dev/null)"
}

# ---- main ----
case "${1:-}" in
  ""|status) _list_status; exit 0 ;;
esac

project="$1"; shift
if [ "${1:-}" = "stop" ]; then _stop "$project"; exit 0; fi

# defaults (per-project agent default may be empty → required, caller/skill asks)
agent="$(_default_agent "$project")"
model="$(_default_model)"
effort="$(_default_effort)"
detach=0
rcname=""
while [ $# -gt 0 ]; do
  case "$1" in
    --agent)          agent="${2:-}";  shift 2 ;;
    --model)          model="${2:-}";  shift 2 ;;
    --effort)         effort="${2:-}"; shift 2 ;;
    --name)           rcname="${2:-}"; shift 2 ;;
    --detach|--no-attach) detach=1;    shift ;;
    *) echo "rc.sh: unknown option '$1'. Usage: rc.sh <project> [--agent a --model m --effort e --name N --detach | stop]" >&2; exit 2 ;;
  esac
done

_start "$project" "$agent" "$model" "$effort" "$detach" "$rcname"
