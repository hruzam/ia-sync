#!/usr/bin/env bash
# devenv-sync-core.sh — shared function library for devenv sync wrappers
# Source this file; do not execute directly.
# Used by: freya.devenv/sync.sh, fantasyobchod.devenv/sync.sh (and future devenvs)
#
# Functions exported:
#   _devenv_resolve_app_dir  <registry.json> <machine>  → prints app_dir or exits 1
#   _devenv_sync_deny_init   <repo>                     → populates EXCLUDE_ARGS array
#   _devenv_sync_deny_cleanup <target_dir> <repo>       → defence rm pass against sync.deny
#   _devenv_secret_scan      <dir> [dir ...]            → returns 1 if secrets found
#   _devenv_print_footer     <repo> <machine>           → prints next-steps footer

# ── APP_DIR resolution ────────────────────────────────────────────────────────
_devenv_resolve_app_dir() {
  local reg="$1" machine="$2"
  python3 -c "
import json, sys
try:
    reg = json.load(open(sys.argv[1]))
except json.JSONDecodeError as e:
    print('ERROR: registry.json is invalid JSON: ' + str(e), file=sys.stderr)
    sys.exit(1)
m = sys.argv[2]
entry = reg.get(m)
if not entry:
    keys = list(reg.keys())
    print('ERROR: host key \"' + m + '\" not in registry.json', file=sys.stderr)
    print('Available keys: ' + ', '.join(keys), file=sys.stderr)
    print('Add your key to registry.json (see template.registry.md) and re-run.', file=sys.stderr)
    sys.exit(1)
print(entry['app_dir'])
" "$reg" "$machine"
}

# ── sync.deny — load excludes ─────────────────────────────────────────────────
# Populates EXCLUDE_ARGS array in caller scope (must be declared before calling).
_devenv_sync_deny_init() {
  local repo="$1"
  local deny_file="$repo/sync.deny"
  EXCLUDE_ARGS=()
  if [ -f "$deny_file" ]; then
    while IFS= read -r line; do
      [[ -z "$line" || "$line" == \#* ]] && continue
      EXCLUDE_ARGS+=(--exclude="$line")
    done < "$deny_file"
    echo "  deny registry: ${#EXCLUDE_ARGS[@]} exclude(s) loaded from sync.deny"
  else
    echo "  WARN: sync.deny not found — no excludes applied"
  fi
}

# ── sync.deny — defence rm pass ───────────────────────────────────────────────
# Removes any deny-listed files that slipped through rsync (defence-in-depth).
_devenv_sync_deny_cleanup() {
  local target_dir="$1" repo="$2"
  local deny_file="$repo/sync.deny"
  if [ -f "$deny_file" ]; then
    while IFS= read -r line; do
      [[ -z "$line" || "$line" == \#* ]] && continue
      find "$target_dir" -maxdepth 6 -name "$line" -delete 2>/dev/null && true
    done < "$deny_file"
    echo "  deny cleanup pass done"
  fi
}

# ── Secret scan ───────────────────────────────────────────────────────────────
# Returns 1 if any secret pattern is found (caller should exit 1).
# Skips dirs that do not exist.
_devenv_secret_scan() {
  local scan_hit=0
  local dirs=()
  for d in "$@"; do
    [ -d "$d" ] && dirs+=("$d")
  done
  if [ "${#dirs[@]}" -eq 0 ]; then
    echo "  (no dirs to scan — skipped)"
    return 0
  fi
  grep -rn -iE \
    -e 'api[_-]key\s*[=:]' \
    -e 'secret\s*[=:]' \
    -e '\bpassword\s*[=:]' \
    -e '\bpasswd\s*[=:]' \
    -e 'BEGIN.*PRIVATE.*KEY' \
    -e '^sk-' \
    -e 'ghp_' \
    -e 'ghs_' \
    "${dirs[@]}" 2>/dev/null \
    && scan_hit=1 || true

  if [ "$scan_hit" -eq 1 ]; then
    echo ""
    echo "WARNING: Potential secrets detected above. Review before pushing."
    return 1
  else
    echo "Clean — no secret patterns found."
    return 0
  fi
}

# ── Deploy-guard check ───────────────────────────────────────────────────────
# Reads .deploy-stamp written by sync.sh and compares vs. current app git state.
# Returns 1 on guard failure unless --force is passed; caller should exit 1.
_devenv_deploy_guard() {
  local repo="$1" app_dir="$2" force="${3:-}"
  local stamp_file="$repo/.deploy-stamp"

  if [ -f "$stamp_file" ]; then
    echo ""
    echo "→ Deploy-guard check"
    local stamp_branch stamp_head stamp_date
    stamp_branch=$(grep '^app_branch=' "$stamp_file" | cut -d= -f2)
    stamp_head=$(grep  '^app_head='   "$stamp_file" | cut -d= -f2)
    stamp_date=$(grep  '^stamp_date=' "$stamp_file" | cut -d= -f2)

    local cur_branch cur_head cur_dirty guard_fail=0
    cur_branch=$(git -C "$app_dir" branch --show-current 2>/dev/null || echo "unknown")
    cur_head=$(git   -C "$app_dir" rev-parse --short HEAD 2>/dev/null || echo "unknown")
    cur_dirty=$(git  -C "$app_dir" status --porcelain 2>/dev/null | wc -l | tr -d ' ')

    if [ "$stamp_branch" != "$cur_branch" ]; then
      echo "  GUARD: branch mismatch"
      echo "    stamp   : $stamp_branch  (synced $stamp_date)"
      echo "    current : $cur_branch"
      guard_fail=1
    fi
    if [ "$stamp_head" != "$cur_head" ]; then
      echo "  GUARD: HEAD moved"
      echo "    stamp   : $stamp_head  (synced $stamp_date)"
      echo "    current : $cur_head"
      guard_fail=1
    fi
    if [ "$guard_fail" -eq 1 ]; then
      if [ "$force" = "--force" ]; then
        echo "  WARNING: --force passed — proceeding despite guard mismatch."
        echo "  Make sure you understand what diverged before continuing."
      else
        echo ""
        echo "ERROR: Deploy-guard fired — target state has moved since last sync."
        echo "       Run 'git pull --rebase && bash sync.sh' to resync first."
        echo "       Or pass --force to override (human operator only)."
        return 1
      fi
    else
      echo "  Guard OK: branch=${cur_branch} head=${cur_head} dirty=${cur_dirty}"
    fi
  else
    echo ""
    echo "NOTE: No deploy-stamp found. Run sync.sh once to initialize the guard."
    echo "      Proceeding without guard check (first deploy)."
  fi
}

# ── Git exclude guard ─────────────────────────────────────────────────────────
# Ensures <entry> is in <git_root>/.git/info/exclude. Safe to call on any repo.
_devenv_git_exclude_guard() {
  local git_root="$1" entry="$2"
  local exclude_file="$git_root/.git/info/exclude"
  if [ -f "$exclude_file" ] && ! grep -qF "$entry" "$exclude_file" 2>/dev/null; then
    echo "$entry" >> "$exclude_file"
    echo "  added $entry to .git/info/exclude (auto)"
  fi
}

# ── Deploy complete footer ────────────────────────────────────────────────────
_devenv_print_deploy_footer() {
  echo ""
  echo "=== Deploy complete ==="
}

# ── Next-steps footer ─────────────────────────────────────────────────────────
_devenv_print_footer() {
  local repo="$1" machine="$2"
  echo ""
  echo "=== Sync complete ==="
  echo "Next:"
  echo "  git -C \"$repo\" add -A"
  echo "  git -C \"$repo\" commit -m \"sync: $(date +%Y-%m-%d) $machine\""
  echo "  git -C \"$repo\" push"
}
