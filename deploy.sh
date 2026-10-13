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

# --dry-run / -n: report every change without writing anything. rsync legs get
# -n -i; cp legs report via copy_file().
# Scope modes (mutually exclusive — a contradictory pair exits 2):
#   (none)           full deploy. The global germline leg (~/.germline) runs FIRST,
#                    because the Claude/Codex Houston wrappers load from it.
#   --germline-only  only the global germline leg (germline-01, 2026-10-12).
#   --codex-only     only the portable Codex leg (incl. the allowlisted Houston profile).
#                    It does NOT refresh ~/.germline — run --germline-only for that.
# --adopt-germline   germline modes only: allow the first deploy over a PRE-EXISTING
#                    real ~/.germline whose files differ from source (the tree is
#                    copied to ~/.germline.bak-<date> first). Never touches a symlink.
# A "hold" (symlinked ~/.germline, symlinked copy_file destination, unreviewed
# pre-existing tree) skips that item loudly, lets the other legs run, and makes the
# script exit 3 at the end. Under --germline-only that is the whole run.
DRY=0
CODEX_ONLY=0
GERMLINE_ONLY=0
ADOPT_GERMLINE=0
for arg in "$@"; do
  case "$arg" in
    --dry-run|-n) DRY=1 ;;
    --codex-only) CODEX_ONLY=1 ;;
    --germline-only) GERMLINE_ONLY=1 ;;
    --adopt-germline) ADOPT_GERMLINE=1 ;;
    *)
      echo "Usage: $0 [--dry-run|-n] [--codex-only | --germline-only] [--adopt-germline]" >&2
      exit 2
      ;;
  esac
done
if [ "$CODEX_ONLY" = 1 ] && [ "$GERMLINE_ONLY" = 1 ]; then
  echo "ERROR: --codex-only and --germline-only are mutually exclusive (run them one after the other)." >&2
  exit 2
fi
if [ "$ADOPT_GERMLINE" = 1 ] && [ "$CODEX_ONLY" = 1 ]; then
  echo "ERROR: --adopt-germline applies to the germline leg; it contradicts --codex-only." >&2
  exit 2
fi
HOLDS=()
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
if [ "$CODEX_ONLY" = 1 ]; then
  echo "Scope: Codex portable surface only"
fi
if [ "$GERMLINE_ONLY" = 1 ]; then
  echo "Scope: global germline (~/.germline) only"
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
  # Never write through a symlinked destination: cp would overwrite the link's target
  # (and backup_live would save contents, not the link). Migrate the link by hand first.
  if [ -L "$dst" ]; then
    echo "  REFUSE  $label — destination is a symlink ($dst → $(readlink "$dst")); not written"
    HOLDS+=("copy_file: $dst is a symlink")
    return 0
  fi
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

# ── ~/.germline — global germline layer (germline-01, 2026-10-12) ────────────────
# Source: $REPO/germline/ → live: a REAL host-local directory ~/.germline/. Additive
# like the skills legs (no --delete). Fails closed — returns 1, writes nothing — when:
#   * ~/.germline is a symlink (a write would go through into the link target; the
#     operator migrates it by hand, this script never unlinks anything);
#   * ~/.germline is not a directory, or contains symlinks (writes could escape it);
#   * a pre-existing real tree that this script never deployed differs in content
#     from source (needs --adopt-germline, which backs the tree up first).
# Ghost inventory (always, dry and live): live files absent from source. Reported,
# never removed — retire them by hand, with a backup.
deploy_germline() {
  local src="$REPO/germline/" dst="$HOME/.germline"
  local marker="$HOME/.local/state/ia-sync/germline.deployed"
  echo ""
  echo "→ ~/.germline (global germline layer)"

  if [ ! -d "$REPO/germline" ]; then
    echo "  HOLD  $REPO/germline/ is missing — nothing to deploy"
    HOLDS+=("germline: source dir missing")
    return 1
  fi

  if [ -L "$dst" ]; then
    echo "  HOLD  ~/.germline is a SYMLINK → $(readlink "$dst"). Refusing to write through it (dry and live)."
    echo "        deploy.sh never unlinks it. Manual migration, once per host:"
    echo "          1. readlink -f ~/.germline     # verify the target is the old source (~/reposoma/.germline)"
    echo "          2. commit/save that source (reposoma) so nothing uncommitted is lost"
    echo "          3. rm ~/.germline              # the LINK only — never rm -r"
    echo "          4. bash $REPO/deploy.sh --germline-only --dry-run, then without --dry-run"
    HOLDS+=("germline: ~/.germline is a symlink (manual migration pending)")
    return 1
  fi
  if [ -e "$dst" ] && [ ! -d "$dst" ]; then
    echo "  HOLD  ~/.germline exists but is not a directory — move it aside by hand"
    HOLDS+=("germline: ~/.germline is not a directory")
    return 1
  fi

  if [ -d "$dst" ]; then
    local links; links="$(find "$dst" -type l 2>/dev/null | head -5)"
    if [ -n "$links" ]; then
      echo "  HOLD  symlinks inside ~/.germline (rsync could write through them):"
      echo "$links" | sed 's/^/          /'
      HOLDS+=("germline: symlink inside ~/.germline")
      return 1
    fi
    if [ ! -f "$marker" ] && [ -n "$(ls -A "$dst")" ]; then
      # Pre-existing real tree this script has never deployed: compare content (-c)
      # so that mtime-only differences do not count; created files (+++) are fine.
      local differ
      differ="$(rsync -a -n -i -c "$src" "$dst/" | grep '^>f' | grep -v '^>f+++++++++' || true)"
      if [ -n "$differ" ]; then
        if [ "$ADOPT_GERMLINE" != 1 ]; then
          echo "  HOLD  pre-existing real ~/.germline never deployed by ia-sync; these files differ from source:"
          echo "$differ" | sed 's/^/          /'
          echo "        Review them; then re-run with --adopt-germline (backs the tree up to ~/.germline.bak-$(date +%F) first)."
          HOLDS+=("germline: pre-existing ~/.germline differs from source (review, then --adopt-germline)")
          return 1
        fi
        local bak="$dst.bak-$(date +%F)"
        if [ "$DRY" = 1 ]; then
          echo "  [dry] would back up ~/.germline → $(basename "$bak") (--adopt-germline)"
        elif [ -e "$bak" ]; then
          echo "  backup kept: $(basename "$bak") (earlier state today preserved)"
        else
          cp -a "$dst" "$bak"
          echo "  backup: .germline → $(basename "$bak")"
        fi
      fi
    fi
  fi

  ensure_dir "$dst"
  rsync "${RSYNC_FLAGS[@]}" "$src" "$dst/"
  echo "  germline/ $LEG_VERB"
  if [ "$DRY" != 1 ]; then
    mkdir -p "$(dirname "$marker")"
    echo "deployed $(date -Is) from $REPO ($(git -C "$REPO" rev-parse --short HEAD 2>/dev/null || echo no-git))" > "$marker"
  fi

  # Ghost inventory — dry itemisation with --delete, deleting lines only. Never executed live.
  if [ -d "$dst" ]; then
    local ghosts; ghosts="$(rsync -a -n -i --delete "$src" "$dst/" | grep '^\*deleting' | sed 's/^\*deleting *//' | sort || true)"
    if [ -n "$ghosts" ]; then
      echo "  GHOSTS — live files absent from source ($(echo "$ghosts" | wc -l) entries; NOT removed; retire by hand, with a backup):"
      echo "$ghosts" | sed 's/^/          /'
    else
      echo "  ghosts: none"
    fi
  fi
  return 0
}

deploy_codex() {
  # Portable instructions are narrow by design. Codex auth, config, hooks,
  # rules, histories, sessions, SQLite state, caches, logs, and trust hashes
  # stay local.
  echo ""
  echo "→ ~/.codex + ~/.agents/skills"
  ensure_dir "$HOME/.codex"

  if [ -f "$REPO/codex/AGENTS.md" ]; then
    copy_file "$REPO/codex/AGENTS.md" "$HOME/.codex/AGENTS.md" "Codex AGENTS.md"
  fi

  # Houston main-session profile — ALLOWLISTED single file (no wildcard over
  # codex/profiles/). Neutral name on purpose: a project profile would collide with
  # a hand-written one. Loads from ~/.germline, see deploy_germline.
  for f in houston.config.toml; do
    if [ -f "$REPO/codex/profiles/$f" ]; then
      copy_file "$REPO/codex/profiles/$f" "$HOME/.codex/$f" "Codex profile $f"
    fi
  done

  if [ -d "$REPO/codex/agents" ]; then
    ensure_dir "$HOME/.codex/agents"
    rsync "${RSYNC_FLAGS[@]}" "$REPO/codex/agents/" "$HOME/.codex/agents/"
    echo "  Codex agents/ $LEG_VERB"
  fi

  if [ -d "$REPO/codex/skills" ]; then
    ensure_dir "$HOME/.agents/skills"
    rsync "${RSYNC_FLAGS[@]}" "$REPO/codex/skills/" "$HOME/.agents/skills/"
    echo "  Codex skills/ $LEG_VERB"
  fi
}

# Single exit path: a hold anywhere → loud summary + exit 3 (nothing else is aborted).
finish() {
  local label="$1"
  echo ""
  if [ "${#HOLDS[@]}" -gt 0 ]; then
    echo "=== $label complete WITH HOLDS (exit 3) ==="
    printf '  HOLD: %s\n' "${HOLDS[@]}"
    exit 3
  fi
  echo "=== $label complete ==="
}

if [ "$GERMLINE_ONLY" = 1 ]; then
  deploy_germline || true
  finish "Germline deploy"
  exit 0
fi

if [ "$CODEX_ONLY" = 1 ]; then
  deploy_codex
  finish "Codex deploy"
  exit 0
fi

# ── ~/.germline (first: the Houston wrappers below load from it) ─────────────────
deploy_germline || true

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

# hooks/ — scripts wired from agent frontmatter `hooks:` (added 2026-10-08, oraculum-bash-whitelist).
# No --delete: live-only hooks (e.g. guard-destructive.sh) survive until folded onto the table.
if [ -d "$REPO/claude/hooks" ]; then
  ensure_dir "$HOME/.claude/hooks"
  rsync "${RSYNC_FLAGS[@]}" "$REPO/claude/hooks/" "$HOME/.claude/hooks/"
  echo "  hooks/ $LEG_VERB"
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

# ── Codex portable surface ──────────────────────────────────────────────────
deploy_codex

# ── ~/.gemini ─────────────────────────────────────────────────────────────────
echo ""
echo "→ ~/.gemini"
ensure_dir "$HOME/.gemini"

if [ -d "$REPO/gemini/agents" ]; then
  ensure_dir "$HOME/.gemini/agents"
  rsync "${RSYNC_FLAGS[@]}" "$REPO/gemini/agents/" "$HOME/.gemini/agents/"
  echo "  agents/ $LEG_VERB"
fi

for f in state.json GEMINI.md; do
  src="$REPO/gemini/$f"
  if [ -f "$src" ]; then
    copy_file "$src" "$HOME/.gemini/$f" "$f"
  fi
done
# projects.json excluded — machine-specific project paths, not portable
# GEMINI.md added 2026-08-01 — the global "first, be aware" file is a shared
# portable primitive (its own text says so); was live-only + skipped by deploy.

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

# ── ~/.nanorc ─────────────────────────────────────────────────────────────────
if [ -f "$REPO/nano/nanorc" ]; then
  echo ""
  echo "→ ~/.nanorc"
  copy_file "$REPO/nano/nanorc" "$HOME/.nanorc" ".nanorc"
fi

# ── ~/.config/zsh ─────────────────────────────────────────────────────────────
echo ""
echo "→ ~/.config/zsh"
ensure_dir "$HOME/.config/zsh"

# Regenerate generated zsh artifacts from their JSON registries BEFORE the rsync, so
# the fresh copy deploys. temple-project-map.zsh's array is generated from
# registries/projects.json (decision 0008/0004 amended 2026-08-15 — paths live in JSON).
if [ -x "$REPO/zsh/registries/gen-temple-map.sh" ]; then
  if [ "$DRY" = 1 ]; then
    bash "$REPO/zsh/registries/gen-temple-map.sh" --check \
      || echo "  temple-project-map.zsh would be regenerated from projects.json"
  else
    bash "$REPO/zsh/registries/gen-temple-map.sh" | sed 's/^/  /'
  fi
fi

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

finish "Deploy"
echo "Next (out-of-repo installs deploy.sh can't do):"
echo "  bash $REPO/install-pkgs/run.sh update"
