#!/usr/bin/env bash
# ia-sync/deploy.sh — restore synced AI/shell config to proper locations
# Safe: no --delete; only overwrites, does not remove existing local files.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Machine identity resolution chain (machines.json wired 2026-07-31 — kills the
# silent-skip trap where hostname `hruzam-120922` matched no config.<name>.zsh):
#   1. MACHINE_NAME env override (explicit wins)
#   2. machines.json lookup: hostname -s → .machines[<host>].logical (needs jq)
#   3. raw hostname -s (legacy fallback — may silently skip host-config legs)
MACHINE="${MACHINE_NAME:-}"
if [ -z "$MACHINE" ] && command -v jq >/dev/null && [ -f "$REPO/machines.json" ]; then
  MACHINE="$(jq -r --arg h "$(hostname -s)" '.machines[$h].logical // empty' "$REPO/machines.json")"
fi
MACHINE="${MACHINE:-$(hostname -s)}"

# --dry-run / -n: report every change without writing anything. Neither this
# script nor sync.sh had a preview mode, so the only way to see a deploy's blast
# radius was to run it. rsync legs get -n -i; cp legs report via copy_file().
DRY=0
if [ "${1:-}" = "--dry-run" ] || [ "${1:-}" = "-n" ]; then
  DRY=1
fi
RSYNC_FLAGS=(-a)
LEG_VERB="deployed"
if [ "$DRY" = 1 ]; then
  RSYNC_FLAGS+=(-n -i)
  LEG_VERB="[dry] would deploy (itemised above)"
fi

echo "=== ia-sync deploy started at $(date) ==="
echo "Machine: $MACHINE"
if [ "$DRY" = 1 ]; then
  echo "*** DRY RUN — nothing will be written ***"
fi

# Backup a live file before deploy overwrites it. Host-specific files (~/.zshrc,
# config.zsh) are replaced wholesale from the repo with no undo otherwise — a bad or
# stub file in the repo would destroy the live one irrecoverably.
# One backup per file per day: if today's already exists we keep it, so the FIRST
# pre-deploy state of the day survives repeated deploys.
# *.bak / *.bak-* are in sync.deny, so these never travel back into the repo.
backup_live() {
  local target="$1"
  [ -f "$target" ] || return 0
  local stamp; stamp="$(date +%F)"
  local bak="${target}.bak-${stamp}"
  if [ -f "$bak" ]; then
    echo "  backup kept: $(basename "$bak") (earlier state today preserved)"
  else
    cp "$target" "$bak"
    echo "  backup: $(basename "$target") → $(basename "$bak")"
  fi
}

# Deploy one file: back the live copy up first, then overwrite. Every single-file
# leg goes through this. Before 2026-07-30 the nine cp legs below overwrote live
# files with no backup at all, while the comment above explained why that is unsafe
# — the guard existed but was only wired to config.zsh and ~/.zshrc.
copy_file() {
  local src="$1" dst="$2" label="$3"
  if [ "$DRY" = 1 ]; then
    if [ ! -f "$dst" ]; then
      echo "  [dry] CREATE  $label"
    elif ! cmp -s "$src" "$dst"; then
      echo "  [dry] UPDATE  $label (backup would be taken)"
    else
      echo "  [dry] same    $label"
    fi
    return 0
  fi
  backup_live "$dst"
  cp "$src" "$dst"
  echo "  $label deployed"
}

# mkdir that respects --dry-run
ensure_dir() {
  if [ "$DRY" = 1 ]; then
    [ -d "$1" ] || echo "  [dry] mkdir   $1"
  else
    mkdir -p "$1"
  fi
}

# ── ~/.claude ────────────────────────────────────────────────────────────────
echo ""
echo "→ ~/.claude"

if [ -d "$REPO/claude/skills" ]; then
  ensure_dir "$HOME/.claude/skills"
  rsync "${RSYNC_FLAGS[@]}" "$REPO/claude/skills/" "$HOME/.claude/skills/"
  echo "  skills/ $LEG_VERB"
fi

if [ -d "$REPO/claude/agents" ]; then
  ensure_dir "$HOME/.claude/agents"
  rsync "${RSYNC_FLAGS[@]}" "$REPO/claude/agents/" "$HOME/.claude/agents/"
  echo "  agents/ $LEG_VERB"
fi

if [ -d "$REPO/claude/commands" ]; then
  ensure_dir "$HOME/.claude/commands"
  rsync "${RSYNC_FLAGS[@]}" "$REPO/claude/commands/" "$HOME/.claude/commands/"
  echo "  commands/ $LEG_VERB"
fi

# NOT deployed — machine-local by nature, deliberately excluded 2026-07-30:
#   settings.local.json  — ".local" IS Claude Code's machine-scope convention;
#                          deploying it made a machine-local file global
#   houston.goal         — an autonomous-run mission; office's goal must not
#                          land on home's disk and boot home's Houston into it
#   recorder.index.json  — session memory index, per-machine by nature
# All three were byte-identical across machines, which is exactly what hid the
# problem. If a genuinely shared default is ever wanted, ship it under a name
# that does not collide with the machine-local file.
for f in settings.json CLAUDE.md; do
  src="$REPO/claude/$f"
  if [ -f "$src" ]; then
    copy_file "$src" "$HOME/.claude/$f" "$f"
  fi
done

# ── ~/.gemini ─────────────────────────────────────────────────────────────────
echo ""
echo "→ ~/.gemini"
ensure_dir "$HOME/.gemini"

if [ -d "$REPO/gemini/agents" ]; then
  ensure_dir "$HOME/.gemini/agents"
  rsync "${RSYNC_FLAGS[@]}" "$REPO/gemini/agents/" "$HOME/.gemini/agents/"
  echo "  agents/ $LEG_VERB"
fi

for f in state.json; do
  src="$REPO/gemini/$f"
  if [ -f "$src" ]; then
    copy_file "$src" "$HOME/.gemini/$f" "$f"
  fi
done
# projects.json excluded — machine-specific project paths, not portable

ensure_dir "$HOME/.gemini/config"
for f in mcp_config.json; do
  src="$REPO/gemini/config/$f"
  if [ -f "$src" ]; then
    copy_file "$src" "$HOME/.gemini/config/$f" "config/$f"
  fi
done
if [ -d "$REPO/gemini/config/projects" ]; then
  rsync "${RSYNC_FLAGS[@]}" "$REPO/gemini/config/projects/" "$HOME/.gemini/config/projects/"
  echo "  config/projects/ $LEG_VERB"
fi

ensure_dir "$HOME/.gemini/antigravity-cli"
for f in settings.json keybindings.json; do
  src="$REPO/gemini/antigravity-cli/$f"
  if [ -f "$src" ]; then
    copy_file "$src" "$HOME/.gemini/antigravity-cli/$f" "antigravity-cli/$f"
  fi
done

# ── ~/.majkee ─────────────────────────────────────────────────────────────────
# Additive like every deploy leg — never deletes. export/ never entered the
# repo (majkee.deny), so nothing here can touch the machine-local process data.
if [ -d "$REPO/majkee" ]; then
  echo ""
  echo "→ ~/.majkee"
  ensure_dir "$HOME/.majkee"
  rsync "${RSYNC_FLAGS[@]}" "$REPO/majkee/" "$HOME/.majkee/"
  echo "  ~/.majkee $LEG_VERB (additive; export/ is machine-local, untouched)"
fi

# ── ~/.config/zsh ─────────────────────────────────────────────────────────────
echo ""
echo "→ ~/.config/zsh"
ensure_dir "$HOME/.config/zsh"

# Sync everything except machine-specific host files (deployed separately below)
rsync "${RSYNC_FLAGS[@]}" \
  --exclude='config.*.zsh' \
  --exclude='zshrc.*' \
  "$REPO/zsh/" "$HOME/.config/zsh/"

# Deploy machine-specific config.zsh
CFG="$REPO/zsh/config.${MACHINE}.zsh"
if [ -f "$CFG" ]; then
  copy_file "$CFG" "$HOME/.config/zsh/config.zsh" "config.${MACHINE}.zsh → config.zsh"
else
  echo "  WARNING: config.${MACHINE}.zsh not found in repo — config.zsh NOT deployed"
  echo "  Available host configs:"
  ls "$REPO/zsh/config."*.zsh 2>/dev/null | sed 's|.*/||' | sed 's/^/    /' || echo "    (none)"
fi

# Deploy machine-specific .zshrc — root shell entry point, host-specific
ZSHRC_SRC="$REPO/zsh/zshrc.${MACHINE}"
if [ -f "$ZSHRC_SRC" ]; then
  copy_file "$ZSHRC_SRC" "$HOME/.zshrc" "zshrc.${MACHINE} → ~/.zshrc"
else
  echo "  WARNING: zshrc.${MACHINE} not found in repo — ~/.zshrc NOT deployed"
  echo "  Available host zshrc files:"
  ls "$REPO/zsh/zshrc."* 2>/dev/null | sed 's|.*/||' | sed 's/^/    /' || echo "    (none)"
fi

echo ""
echo "=== Deploy complete ==="
echo "Next (out-of-repo installs deploy.sh can't do):"
echo "  bash $REPO/install-pkgs/run.sh update"
