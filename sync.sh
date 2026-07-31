#!/usr/bin/env bash
# ia-sync/sync.sh — sync selected AI/shell config into this repo
# Allowlist approach: only explicitly enumerated paths are copied.
# Run from any directory; repo root is auto-detected.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_CLAUDE="$HOME/.claude"
SRC_GEMINI="$HOME/.gemini"
SRC_ZSH="$HOME/.config/zsh"
MACHINE="${MACHINE_NAME:-$(hostname -s)}"

echo "=== ia-sync sync started at $(date) ==="
echo "Repo root : $REPO"
echo "Machine   : $MACHINE"

# ── ~/.claude ────────────────────────────────────────────────────────────────
echo ""
echo "→ ~/.claude"
DST="$REPO/claude"
mkdir -p "$DST"

if [ -d "$SRC_CLAUDE/skills" ]; then
  rsync -a --delete "$SRC_CLAUDE/skills/" "$DST/skills/"
  echo "  skills/ synced"
fi

if [ -d "$SRC_CLAUDE/agents" ]; then
  rsync -a "$SRC_CLAUDE/agents/" "$DST/agents/"
  echo "  agents/ synced (additive — no --delete; office controls agent canonical set)"
fi

if [ -d "$SRC_CLAUDE/commands" ]; then
  rsync -a --delete "$SRC_CLAUDE/commands/" "$DST/commands/"
  echo "  commands/ synced"
fi

for f in settings.json settings.local.json houston.goal recorder.index.json CLAUDE.md; do
  src="$SRC_CLAUDE/$f"
  if [ -f "$src" ]; then
    cp "$src" "$DST/$f"
    echo "  $f copied"
  fi
done

# ── ~/.gemini ─────────────────────────────────────────────────────────────────
echo ""
echo "→ ~/.gemini"
DST="$REPO/gemini"
mkdir -p "$DST"

if [ -d "$SRC_GEMINI/agents" ]; then
  rsync -a --delete "$SRC_GEMINI/agents/" "$DST/agents/"
  echo "  agents/ synced"
fi

for f in state.json projects.json; do
  src="$SRC_GEMINI/$f"
  if [ -f "$src" ]; then
    cp "$src" "$DST/$f"
    echo "  $f copied"
  fi
done

mkdir -p "$DST/config"
for f in mcp_config.json; do
  src="$SRC_GEMINI/config/$f"
  if [ -f "$src" ]; then
    cp "$src" "$DST/config/$f"
    echo "  config/$f copied"
  fi
done
if [ -d "$SRC_GEMINI/config/projects" ]; then
  rsync -a --delete "$SRC_GEMINI/config/projects/" "$DST/config/projects/"
  echo "  config/projects/ synced"
fi

mkdir -p "$DST/antigravity-cli"
for f in settings.json keybindings.json; do
  src="$SRC_GEMINI/antigravity-cli/$f"
  if [ -f "$src" ]; then
    cp "$src" "$DST/antigravity-cli/$f"
    echo "  antigravity-cli/$f copied"
  fi
done

# ── ~/.majkee ─────────────────────────────────────────────────────────────────
# Operator's personal seat folder — synced like ~/.claude (both machines, same
# destination). Guarded: leg no-ops on a host that doesn't have it (office as
# of 2026-07-30; home is the origin). Exclusions live in majkee.deny (per-leg
# deny registry — data, not code).
SRC_MAJKEE="$HOME/.majkee"
if [ -d "$SRC_MAJKEE" ]; then
  echo ""
  echo "→ ~/.majkee"
  DST="$REPO/majkee"
  mkdir -p "$DST"
  MAJKEE_EXCLUDES=()
  if [ -f "$REPO/majkee.deny" ]; then
    while IFS= read -r line; do
      [[ -z "$line" || "$line" == \#* ]] && continue
      MAJKEE_EXCLUDES+=(--exclude="$line")
    done < "$REPO/majkee.deny"
    echo "  deny registry: ${#MAJKEE_EXCLUDES[@]} exclude(s) loaded from majkee.deny"
  else
    echo "  WARN: majkee.deny not found — no excludes applied"
  fi
  rsync -a --delete ${MAJKEE_EXCLUDES[@]+"${MAJKEE_EXCLUDES[@]}"} "$SRC_MAJKEE/" "$DST/"
  echo "  ~/.majkee synced (export/ stays machine-local per majkee.deny)"
else
  echo ""
  echo "→ ~/.majkee — absent on this host, leg skipped"
fi

# ── ~/.config/zsh ─────────────────────────────────────────────────────────────
echo ""
echo "→ ~/.config/zsh"
DST="$REPO/zsh"
mkdir -p "$DST"

# Build rsync exclude args from sync.deny registry
DENY_FILE="$REPO/sync.deny"
EXCLUDE_ARGS=()
if [ -f "$DENY_FILE" ]; then
  while IFS= read -r line; do
    [[ -z "$line" || "$line" == \#* ]] && continue
    EXCLUDE_ARGS+=(--exclude="$line")
  done < "$DENY_FILE"
  echo "  deny registry: ${#EXCLUDE_ARGS[@]} exclude(s) loaded from sync.deny"
else
  echo "  WARN: sync.deny not found — no excludes applied"
fi

# Host-specific repo files are NOT mirrored from the live dir — they are written
# explicitly below (config.${MACHINE}.zsh, zshrc.${MACHINE}). They must be excluded
# here or rsync would (a) overwrite the other machine's file with a stale local copy
# and (b) --delete the ones this machine doesn't have. Not in sync.deny: that registry
# means "must never exist in the repo", and these must.
rsync -a --delete \
  --exclude='config.*.zsh' \
  --exclude='zshrc.*' \
  "${EXCLUDE_ARGS[@]}" "$SRC_ZSH/" "$DST/"

# config.zsh: save with machine name so multiple hosts can coexist
if [ -f "$SRC_ZSH/config.zsh" ]; then
  cp "$SRC_ZSH/config.zsh" "$DST/config.${MACHINE}.zsh"
  echo "  config.zsh → config.${MACHINE}.zsh"
fi

# ~/.zshrc: save with machine name — host-specific root shell entry point
if [ -f "$HOME/.zshrc" ]; then
  cp "$HOME/.zshrc" "$DST/zshrc.${MACHINE}"
  echo "  ~/.zshrc → zshrc.${MACHINE}"
fi

# Defence-in-depth: explicit rm pass for every deny-listed pattern
if [ -f "$DENY_FILE" ]; then
  while IFS= read -r line; do
    [[ -z "$line" || "$line" == \#* ]] && continue
    find "$DST" -maxdepth 3 -name "$line" -delete 2>/dev/null && true
  done < "$DENY_FILE"
  echo "  deny cleanup pass done"
fi

# ── Secret scan ───────────────────────────────────────────────────────────────
echo ""
echo "=== Secret scan ==="
SCAN_HIT=0
grep -rn -iE \
  -e 'api[_-]key\s*[=:]' \
  -e 'secret\s*[=:]' \
  -e '\bpassword\s*[=:]' \
  -e '\bpasswd\s*[=:]' \
  -e 'BEGIN.*PRIVATE.*KEY' \
  -e '^sk-' \
  -e 'ghp_' \
  -e 'ghs_' \
  "$REPO/claude" "$REPO/gemini" "$REPO/zsh" 2>/dev/null \
  && SCAN_HIT=1 || true

if [ "$SCAN_HIT" -eq 1 ]; then
  echo ""
  echo "WARNING: Potential secrets detected above. Review before pushing."
  exit 1
else
  echo "Clean — no secret patterns found."
fi

echo ""
echo "=== Sync complete ==="
echo "Next: git add -A && git commit -m \"sync: \$(date +%Y-%m-%d)\" && git push"
