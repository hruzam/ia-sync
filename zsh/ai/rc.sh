#!/usr/bin/env bash
# rc.sh — Claude Code Remote Control launcher/engine (bare-server, tmux-free).
#
# Redesigned 2026-08-15 (operator gavel: "minimize the tmux layer — behave like a
# user running the command in a terminal"). Option A:
#   • launches `claude remote-control --name <rc>` DIRECTLY, detached via
#     `setsid nohup … &` — no tmux, no pty. Survives ssh disconnect.
#   • the RC server registers to your Claude account: catch the session from the
#     mobile app / claude.ai/code. No host-side attach needed.
#   • agent/model/effort are NOT selected at launch in this mode (the interactive
#     flag-form needs a pty; the bare server does not accept them). You pick the
#     agent INSIDE the caught session. The /rc-launch skill still passes those
#     flags for compatibility — we accept and note them, we do not fail.
#   • LOCAL spawn only. Cross-host dispatch is the /rc-launch skill's job (it ssh's
#     to the target host and calls THIS engine there).
#
# Wiring: registry data lives in JSON (projects.json = paths, ai.json = RC params).
# This script stays a clean executive — no hardcoded project literals.
#
# Usage:
#   rc.sh                        list live RC servers + registered/launchable projects
#   rc.sh status                 same
#   rc.sh <project>              start-or-report the RC server (detached, tmux-free)
#   rc.sh <project> stop         stop the RC server
#   rc.sh <project> [opts]       accepted for skill-compat (ignored in bare mode):
#       --agent <a>  --model <m>  --effort <e>  --detach  --no-attach
#       --name "<RC name>"        (this one IS honored — overrides the registry rc_name)
set -uo pipefail

REG_DIR="${RC_REG_DIR:-${HOME}/.config/zsh/registries}"   # override for pre-deploy testing
PROJECTS="${REG_DIR}/projects.json"      # authoritative paths
REGISTRY="${REG_DIR}/ai.json"            # RC params (rc_name etc.)
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
_rc_name() { local n; n=$(jq -r --arg p "$1" '."remote-control".projects[$p].rc_name // empty' "$REGISTRY" 2>/dev/null); [ -n "$n" ] && echo "$n" || echo "$1"; }

# a running RC server is identified by its `--name <rcname>` on the command line
_server_pid() { pgrep -f -- "remote-control --name ${1}" 2>/dev/null | head -1; }

_reach() {  # bare-server report: the catch URL (registered to your account)
  local rcname="$1" log="$2" url=""
  # the URL lands in the log a moment after boot
  local i
  for i in 1 2 3 4 5; do
    url=$(grep -oE 'https://claude\.ai/code\?environment=[A-Za-z0-9_]+' "$log" 2>/dev/null | tail -1)
    [ -n "$url" ] && break
    sleep 1
  done
  echo "OK: '$rcname' running (bare server, tmux-free) — pick the agent inside the session"
  echo "   • Remote Control : ${url:-<visible in the Claude app, or: tail -f $log>}"
  echo "   • Claude app     : open the session named '$rcname'"
  echo "   stop: rc.sh <project> stop"
}

_start() {
  local project="$1" rcname="$2"
  _check_jq
  local path; path=$(_project_path "$project")
  if [ -z "$path" ]; then
    echo "rc.sh: unknown project '$project'. Known: $(jq -r '.projects|keys|join(", ")' "$PROJECTS")" >&2; exit 1
  fi
  [ -d "$path" ] || { echo "rc.sh: project '$project' → '$path' not present on this host ($(hostname))" >&2; exit 1; }
  [ -z "$rcname" ] && rcname=$(_rc_name "$project")

  local log="${LOG_DIR}/${project}.log"
  mkdir -p "$LOG_DIR"

  if [ -n "$(_server_pid "$rcname")" ]; then
    echo "rc.sh: RC server for '$rcname' already running (pid $(_server_pid "$rcname")) — reusing."
    _reach "$rcname" "$log"
    return 0
  fi

  local bin; bin=$(_claude_bin)
  ( cd "$path" && setsid nohup "$bin" remote-control --name "$rcname" >"$log" 2>&1 </dev/null & )
  _reach "$rcname" "$log"
}

_stop() {
  local project="$1" rcname; rcname=$(_rc_name "$project")
  local pid; pid=$(_server_pid "$rcname")
  if [ -n "$pid" ]; then
    pkill -f -- "remote-control --name ${rcname}" && echo "rc.sh: stopped RC server '$rcname' (was pid $pid)"
  else
    echo "rc.sh: not running: '$rcname'"
  fi
}

_list_status() {
  _check_jq
  echo "live RC servers:"
  pgrep -af -- 'remote-control --name' 2>/dev/null | sed -E 's/.*--name /  /' | sort -u || true
  [ -z "$(pgrep -f -- 'remote-control --name' 2>/dev/null)" ] && echo "  (none)"
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

# accept skill-compat flags. In bare-server mode agent/model/effort are NOT applied
# at launch (the pty-bound interactive form is retired here) — we note and continue.
rcname=""
noted=""
while [ $# -gt 0 ]; do
  case "$1" in
    --name)                    rcname="${2:-}"; shift 2 ;;
    --agent|--model|--effort)  noted="${noted} $1=${2:-}"; shift 2 ;;
    --detach|--no-attach)      shift ;;   # always detached now — no-op
    *) echo "rc.sh: unknown option '$1'. Usage: rc.sh <project> [--name N | stop]" >&2; exit 2 ;;
  esac
done
[ -n "$noted" ] && echo "rc.sh: note — bare-server mode ignores launch-time${noted}; select the agent inside the session." >&2

_start "$project" "$rcname"
