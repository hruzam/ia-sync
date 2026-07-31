#!/usr/bin/env bash
# install-pkgs/run.sh — lightweight local package-install runner ("local AUR")
#
# Tracks which install-pkgs tasks are installed on THIS machine and applies
# updates idempotently, AUR-`-Syu`-style but dependency-free (jq only).
#
# State is PER-MACHINE and never synced:  ~/.local/state/ia-sync/installed.json
# — this is deliberate. Never record install state in the repo, or office will
# claim something "installed" that home never ran (the SYNC_DISCIPLINE trap).
#
# Verbs:
#   run.sh list            show tasks for this host: available vs installed vs state
#   run.sh status          alias of list
#   run.sh update          install/upgrade every auto task that is new or stale
#   run.sh mark <slug> [v] record a task as installed (for manual tasks)
#   run.sh unmark <slug>   forget a task (for reinstall / testing)
#
# Task contract — each install-pkgs/<slug>.md declares (machine-parseable):
#   version:     <semver>       bump when the recipe changes
#   hosts:       home office    which machines this installs ON (space list)
#   automation:  auto|manual    auto = runner executes; manual = runner gates + waits
#   src-root:    ~/path         (optional) project root the recipe copies FROM
# and may contain two sentinel-wrapped bash blocks:
#   <!-- install:check --> ... <!-- /install:check -->   preconditions; exit≠0 to refuse
#   <!-- install:run   --> ... <!-- /install:run   -->   idempotent, non-destructive install
# Blocks receive $SRC (expanded src-root), $FRIENDLY, $MACHINE, $PKGDIR in their env.

set -uo pipefail

PKGDIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MACHINE="$(hostname -s)"
case "$MACHINE" in
  hruzam-120922) FRIENDLY=office ;;
  hruzam)        FRIENDLY=home ;;
  *)             FRIENDLY="$MACHINE" ;;
esac

STATE_DIR="${XDG_STATE_HOME:-$HOME/.local/state}/ia-sync"
STATE_FILE="$STATE_DIR/installed.json"
mkdir -p "$STATE_DIR"
[ -f "$STATE_FILE" ] || printf '{"host":"%s","installed":{}}\n' "$MACHINE" > "$STATE_FILE"

# ── helpers ───────────────────────────────────────────────────────────────────
_field() { # _field FILE KEY → value of first `KEY:` line, trimmed
  grep -m1 -E "^$2:" "$1" 2>/dev/null | sed -E "s/^$2:[[:space:]]*//; s/[[:space:]]+$//"
}

_hosts_match() { # _hosts_match "home office" → 0 if this machine is in the list
  local h; for h in $1; do [ "$h" = "$FRIENDLY" ] && return 0; done; return 1
}

_newer() { # _newer INSTALLED AVAILABLE → 0 if AVAILABLE strictly newer (empty INSTALLED counts as newer)
  [ -z "$1" ] && return 0
  [ "$1" = "$2" ] && return 1
  [ "$(printf '%s\n%s\n' "$1" "$2" | sort -V | tail -1)" = "$2" ]
}

_installed_ver() { jq -r --arg s "$1" '.installed[$s].version // ""' "$STATE_FILE"; }

_record() { # _record SLUG VERSION
  local tmp; tmp="$(mktemp)"
  jq --arg s "$1" --arg v "$2" --arg t "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
     '.installed[$s] = {version:$v, at:$t}' "$STATE_FILE" > "$tmp" && mv "$tmp" "$STATE_FILE"
}

_forget() {
  local tmp; tmp="$(mktemp)"
  jq --arg s "$1" 'del(.installed[$s])' "$STATE_FILE" > "$tmp" && mv "$tmp" "$STATE_FILE"
}

_extract() { # _extract FILE BLOCK → bash between the block's sentinels, code fences stripped
  awk -v b="$2" '
    $0 == "<!-- install:" b " -->"  { inb=1; next }
    $0 == "<!-- /install:" b " -->" { inb=0 }
    inb { if ($0 ~ /^```/) next; print }
  ' "$1"
}

_run_block() { # _run_block FILE BLOCK → execute the block, return its exit code (empty = no-op success)
  local body; body="$(_extract "$1" "$2")"
  [ -z "${body//[[:space:]]/}" ] && return 0
  bash -c "$body"
}

_export_env() { # make src-root + identity available to blocks
  local src; src="$(_field "$1" src-root)"; src="${src/#\~/$HOME}"
  export SRC="$src" FRIENDLY MACHINE PKGDIR
}

_tasks() { find "$PKGDIR" -maxdepth 1 -name '*.md' ! -name 'README.md' 2>/dev/null | sort; }

# ── verbs ─────────────────────────────────────────────────────────────────────
cmd_list() {
  printf '%-22s %-12s %-7s %-9s %s\n' TASK HOSTS AVAIL INSTALLED STATE
  printf '%-22s %-12s %-7s %-9s %s\n' '----' '-----' '-----' '---------' '-----'
  local f slug hosts ver auto inst state
  for f in $(_tasks); do
    slug="$(basename "$f" .md)"
    ver="$(_field "$f" version)";     [ -z "$ver" ]   && ver='?'
    hosts="$(_field "$f" hosts)";     [ -z "$hosts" ] && hosts='?'
    auto="$(_field "$f" automation)"; [ -z "$auto" ]  && auto='manual'
    inst="$(_installed_ver "$slug")"
    if ! _hosts_match "$hosts"; then
      state="n/a (other host)"
    elif [ -z "$inst" ]; then
      state="not-installed ($auto)"
    elif [ "$inst" = "$ver" ]; then
      state="current"
    elif _newer "$inst" "$ver"; then
      state="STALE (have $inst)"
    else
      state="ahead? (have $inst)"
    fi
    printf '%-22s %-12s %-7s %-9s %s\n' "$slug" "$hosts" "$ver" "${inst:-–}" "$state"
  done
}

cmd_update() {
  local f slug hosts ver auto inst label chk_out chk_rc out rc
  for f in $(_tasks); do
    slug="$(basename "$f" .md)"
    hosts="$(_field "$f" hosts)"
    _hosts_match "$hosts" || continue
    ver="$(_field "$f" version)"
    auto="$(_field "$f" automation)"; [ -z "$auto" ] && auto='manual'
    inst="$(_installed_ver "$slug")"

    if [ -n "$inst" ] && [ "$inst" = "$ver" ]; then
      printf '  %-22s %-9s already current, skip\n' "$slug" "$ver"; continue
    fi
    if [ -n "$inst" ] && ! _newer "$inst" "$ver"; then
      printf '  %-22s installed %s ahead of repo %s, skip\n' "$slug" "$inst" "$ver"; continue
    fi

    label="$ver"; [ -n "$inst" ] && label="$inst→$ver"
    _export_env "$f"

    # check phase — gates both auto and manual
    chk_out="$(_run_block "$f" check 2>&1)"; chk_rc=$?
    if [ "$chk_rc" -ne 0 ]; then
      printf '  %-22s check failed: %s\n' "$slug" "$(printf '%s' "$chk_out" | head -1)"
      continue
    fi

    if [ "$auto" = 'manual' ]; then
      printf '  %-22s %-9s manual — run steps in %s, then: run.sh mark %s\n' \
        "$slug" "$label" "$(basename "$f")" "$slug"
      continue
    fi

    # auto install phase
    out="$(_run_block "$f" run 2>&1)"; rc=$?
    if [ "$rc" -eq 0 ]; then
      _record "$slug" "$ver"
      printf '  %-22s %-9s installing... ok\n' "$slug" "$label"
      [ -n "$out" ] && printf '%s\n' "$out" | sed 's/^/      /'
    else
      printf '  %-22s %-9s install FAILED (not recorded)\n' "$slug" "$label"
      [ -n "$out" ] && printf '%s\n' "$out" | sed 's/^/      /'
    fi
  done
}

cmd_mark() {
  local slug="${1:-}" ver="${2:-}"
  [ -z "$slug" ] && { echo "usage: run.sh mark <slug> [version]"; return 1; }
  local f="$PKGDIR/$slug.md"
  [ -f "$f" ] || { echo "no such task: $slug"; return 1; }
  [ -z "$ver" ] && ver="$(_field "$f" version)"
  _record "$slug" "$ver"
  echo "marked $slug = $ver installed on $MACHINE ($FRIENDLY)"
}

cmd_unmark() {
  local slug="${1:-}"
  [ -z "$slug" ] && { echo "usage: run.sh unmark <slug>"; return 1; }
  _forget "$slug"
  echo "unmarked $slug on $MACHINE ($FRIENDLY)"
}

echo "host: $MACHINE ($FRIENDLY) · state: $STATE_FILE"
case "${1:-list}" in
  list|status) cmd_list ;;
  update)      cmd_update ;;
  mark)        shift; cmd_mark "$@" ;;
  unmark)      shift; cmd_unmark "$@" ;;
  *) echo "usage: run.sh [list|update|mark <slug> [ver]|unmark <slug>]"; exit 1 ;;
esac
