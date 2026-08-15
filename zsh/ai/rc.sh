#!/usr/bin/env bash
# rc.sh — Claude Code Remote Control launcher/engine (tmux-free, A/B hybrid).
#
# Redesigned 2026-08-15 (operator gavels: "minimize the tmux layer"; then "support
# the agent+effort form too"). Two launch modes, NEITHER uses tmux:
#
#   MODE A — bare server (no preset flags):
#       claude remote-control --name <rc>
#     A session FACTORY: connect from the phone/browser and it spawns a NEW session
#     in the project dir; you pick the agent inside. No pty needed → plain
#     `setsid nohup … &`. Catch URL is an environment: .../code?environment=…
#
#   MODE B — preset agent/model/effort (any of --agent/--model/--effort given):
#       claude [--agent A] [--model M] [--effort E] --remote-control <rc>
#     A specific INTERACTIVE session with those settings, exposed to Remote Control.
#     Interactive ⇒ needs a pty; we give it one WITHOUT tmux via `script -qfc`,
#     detached with `setsid nohup`. Catch URL is that session: .../code/session_…
#     This is what makes "/rc-launch launch trajectory" literally true.
#
# Both survive ssh disconnect and register to your Claude account — catch from the
# mobile app / claude.ai/code the same way. LOCAL spawn only; cross-host dispatch is
# the /rc-launch skill's job (it ssh's to the host and calls THIS engine there).
#
# Registry data lives in JSON (projects.json = paths, ai.json = RC params +
# launch-defaults). This script stays a clean executive — no project literals.
#
# Usage:
#   rc.sh                        list live RC servers + registered/launchable projects
#   rc.sh status                 same
#   rc.sh <project>              MODE A — bare server (pick agent inside)
#   rc.sh <project> --agent A [--model M] [--effort E] [--name N]
#                                MODE B — preset session, phone-reachable
#   rc.sh <project> stop         stop the RC session/server
#   (--detach/--no-attach accepted for skill-compat; always detached — no-op)
set -uo pipefail

REG_DIR="${RC_REG_DIR:-${HOME}/.config/zsh/registries}"   # override for pre-deploy testing
PROJECTS="${REG_DIR}/projects.json"      # authoritative paths
REGISTRY="${REG_DIR}/ai.json"            # RC params + launch-defaults
LOG_DIR="${HOME}/.cache/rc"              # per-project launch logs (hold the catch URL)

_check_jq() { command -v jq &>/dev/null || { echo "rc.sh: jq required" >&2; exit 1; }; }

# claude may live off the non-interactive PATH (e.g. ~/.npm-global/bin over ssh) —
# resolve a real binary so headless/cross-host launches work.
_claude_bin() {
  if command -v claude &>/dev/null; then command -v claude; return; fi
  local c
  for c in "$HOME/.npm-global/bin/claude" "$HOME/.local/bin/claude" \
           "$HOME/.claude/local/claude" /usr/local/bin/claude; do
    [ -x "$c" ] && { echo "$c"; return; }
  done
  echo "claude"   # last resort — errors loudly if truly absent
}

# ---- resolvers (all read JSON; no hardcoded literals) ----
_project_path() {  # projects.json authoritative; ai.json path is legacy fallback (e.g. nabla-lab)
  local p="$1" path
  path=$(jq -r --arg p "$p" '.projects[$p] // empty' "$PROJECTS" 2>/dev/null)
  [ -z "$path" ] && path=$(jq -r --arg p "$p" '."remote-control".projects[$p].path // empty' "$REGISTRY" 2>/dev/null)
  echo "$path"
}
_rc_name()        { local n; n=$(jq -r --arg p "$1" '."remote-control".projects[$p].rc_name // empty' "$REGISTRY" 2>/dev/null); [ -n "$n" ] && echo "$n" || echo "$1"; }
_default_model()  { jq -r '."remote-control"."launch-defaults".model  // "opus"' "$REGISTRY" 2>/dev/null; }
_default_effort() { jq -r '."remote-control"."launch-defaults".effort // empty'  "$REGISTRY" 2>/dev/null; }

# a running RC session/server (either mode) carries "remote-control" + the rc_name on
# its command line. `script`-wrapper and claude child both match — either proves alive.
_server_pid() { pgrep -af -- 'remote-control' 2>/dev/null | grep -F -- "$1" | awk 'NR==1{print $1}'; }

_reach() {  # report the catch URL (env for A, session for B); URL lands a moment after boot
  local rcname="$1" log="$2" mode="$3" url="" i
  for i in 1 2 3 4 5; do
    url=$(sed -e 's/\x1b\[[0-9;?]*[a-zA-Z]//g' "$log" 2>/dev/null \
          | grep -oE 'https://claude\.ai/code(\?environment=|/session_)[A-Za-z0-9_]+' | tail -1)
    [ -n "$url" ] && break
    sleep 1
  done
  echo "OK: '$rcname' running (mode $mode, tmux-free)"
  echo "   • Remote Control : ${url:-<visible in the Claude app, or: tail -f $log>}"
  echo "   • Claude app     : open the session named '$rcname'"
  [ "$mode" = A ] && echo "   • note           : mode A spawns a fresh session — pick the agent inside"
  echo "   stop: rc.sh <project> stop"
}

_start() {
  local project="$1" agent="$2" model="$3" effort="$4" rcname="$5"
  _check_jq
  local path; path=$(_project_path "$project")
  if [ -z "$path" ]; then
    echo "rc.sh: unknown project '$project'. Known: $(jq -r '.projects|keys|join(", ")' "$PROJECTS")" >&2; exit 1
  fi
  [ -d "$path" ] || { echo "rc.sh: project '$project' → '$path' not present on this host ($(hostname))" >&2; exit 1; }
  [ -z "$rcname" ] && rcname=$(_rc_name "$project")

  local log="${LOG_DIR}/${project}.log"
  mkdir -p "$LOG_DIR"

  # mode: B iff any preset (agent/model/effort) requested; else A
  local mode=A
  [ -n "$agent$model$effort" ] && mode=B

  if [ -n "$(_server_pid "$rcname")" ]; then
    echo "rc.sh: RC session for '$rcname' already running (pid $(_server_pid "$rcname")) — reusing."
    _reach "$rcname" "$log" "$mode"
    return 0
  fi

  local bin; bin=$(_claude_bin)
  if [ "$mode" = A ]; then
    ( cd "$path" && setsid nohup "$bin" remote-control --name "$rcname" >"$log" 2>&1 </dev/null & )
  else
    # fill model/effort from launch-defaults when not explicitly passed
    [ -z "$model" ]  && model=$(_default_model)
    [ -z "$effort" ] && effort=$(_default_effort)
    local inner="$bin"
    [ -n "$agent" ]  && inner="$inner --agent $agent"
    [ -n "$model" ]  && inner="$inner --model $model"
    [ -n "$effort" ] && inner="$inner --effort $effort"
    inner="$inner --remote-control \"$rcname\""
    # `script` gives the interactive session a pty WITHOUT tmux; setsid detaches it
    ( cd "$path" && setsid nohup script -qfc "$inner" /dev/null >"$log" 2>&1 </dev/null & )
  fi
  _reach "$rcname" "$log" "$mode"
}

_stop() {
  local project="$1" rcname; rcname=$(_rc_name "$project")
  local pid; pid=$(_server_pid "$rcname")
  if [ -n "$pid" ]; then
    # kill both the script wrapper (mode B) and the claude child
    pkill -f -- "remote-control.*$(printf '%s' "$rcname" | sed 's/[][\\.*^$/]/\\&/g')" 2>/dev/null
    pkill -f -- "$rcname" 2>/dev/null
    echo "rc.sh: stopped RC session '$rcname' (was pid $pid)"
  else
    echo "rc.sh: not running: '$rcname'"
  fi
}

_list_status() {
  _check_jq
  echo "live RC sessions:"
  local any=""
  while IFS= read -r key; do
    local rcname; rcname=$(_rc_name "$key")
    if [ -n "$(_server_pid "$rcname")" ]; then echo "  $key  →  '$rcname'  RUNNING"; any=1; fi
  done < <(jq -r '."remote-control".projects | keys[]' "$REGISTRY" 2>/dev/null)
  [ -z "$any" ] && echo "  (none registered running)"
  echo
  echo "registered projects (ai.json remote-control.projects):"
  jq -r '."remote-control".projects | to_entries[] | "  \(.key)  →  rc_name=\(.value.rc_name)  available=\(.value.available)"' "$REGISTRY" 2>/dev/null
  echo
  echo "launchable projects (projects.json): $(jq -r '.projects|keys|join(", ")' "$PROJECTS" 2>/dev/null)"
}

# ---- main ----
case "${1:-}" in
  ""|status) _list_status; exit 0 ;;
esac

project="$1"; shift
if [ "${1:-}" = "stop" ]; then _stop "$project"; exit 0; fi

agent=""; model=""; effort=""; rcname=""
while [ $# -gt 0 ]; do
  case "$1" in
    --agent)               agent="${2:-}";  shift 2 ;;
    --model)               model="${2:-}";  shift 2 ;;
    --effort)              effort="${2:-}"; shift 2 ;;
    --name)                rcname="${2:-}"; shift 2 ;;
    --detach|--no-attach)  shift ;;   # always detached — no-op
    *) echo "rc.sh: unknown option '$1'. Usage: rc.sh <project> [--agent A --model M --effort E --name N | stop]" >&2; exit 2 ;;
  esac
done

_start "$project" "$agent" "$model" "$effort" "$rcname"
