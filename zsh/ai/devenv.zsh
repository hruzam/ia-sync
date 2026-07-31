#!/usr/bin/env zsh
# devenv.zsh — project devenv transport engine
# Sourced by: ~/.config/zsh/ai/base.zsh (PARTITION 6)
# Aliases:    ~/.config/zsh/ai/keyboard.zsh (PARTITION 11)
#
# Engines for per-project git devenv repos (fantasyobchod.devenv · freya.devenv).
# Discipline: always pull --rebase BEFORE running devenv-sync (SYNC_DISCIPLINE.md).
# Pull uses the checked-out branch's upstream tracking — devenv default branches
# differ per repo (freya.devenv: core), so no branch name is hardcoded here.
#
# Internal entry points (aliased in keyboard PARTITION 11):
#   _bo_sync  _bo_deploy  _bo_status  _fr_sync  _fr_deploy  _fr_status  _devenv_help

_DEVENV_BO="/home/hruzam/www/imago_cz/fantasyobchod.devenv"
_DEVENV_FR="/home/hruzam/www/imago_cz/freya.devenv"

_devenv_sync() {
  local devenv="$1"
  local name="$2"
  echo "[devenv] Syncing ${name} — pull first, then stage-OUT"
  git -C "${devenv}" pull --rebase || {
    echo "[devenv] ERROR: git pull failed — resolve before syncing"
    return 1
  }
  bash "${devenv}/sync.sh"
}

_devenv_deploy() {
  local devenv="$1"
  local name="$2"
  echo "[devenv] Deploying ${name} — pull then stage-IN"
  git -C "${devenv}" pull --rebase || {
    echo "[devenv] ERROR: git pull failed — resolve before deploying"
    return 1
  }
  bash "${devenv}/deploy.sh"
}

_devenv_status() {
  local devenv="$1"
  local name="$2"
  echo "[devenv] Status: ${name}"
  git -C "${devenv}" status
  echo ""
  git -C "${devenv}" log --oneline -5
}

# ── fantasyobchod.devenv internal entry points (aliased in keyboard PARTITION 11) ──
_bo_sync()    { _devenv_sync   "${_DEVENV_BO}" "fantasyobchod.devenv" }
_bo_deploy()  { _devenv_deploy "${_DEVENV_BO}" "fantasyobchod.devenv" }
_bo_status()  { _devenv_status "${_DEVENV_BO}" "fantasyobchod.devenv" }

# ── freya.devenv internal entry points (aliased in keyboard PARTITION 11) ────
_fr_sync()    { _devenv_sync   "${_DEVENV_FR}" "freya.devenv" }
_fr_deploy()  { _devenv_deploy "${_DEVENV_FR}" "freya.devenv" }
_fr_status()  { _devenv_status "${_DEVENV_FR}" "freya.devenv" }

_devenv_help() {
  cat <<'EOF'
devenv.zsh — project devenv transport (engine: ai/devenv.zsh · keys: keyboard.zsh PARTITION 11)

  fantasyobchod.devenv:
    bo-sync      pull --rebase + sync.sh  (app → repo)
    bo-deploy    pull --rebase + deploy.sh (repo → app)
    bo-status    git status + log -5

  freya.devenv:
    fr-sync      pull --rebase + sync.sh  (app → repo)
    fr-deploy    pull --rebase + deploy.sh (repo → app; deploy-guard fires on mismatch)
    fr-status    git status + log -5

  Discipline: always pull before sync; see SYNC_DISCIPLINE.md in each devenv.
  Pull rides upstream tracking — devenv default branches differ (freya: core).
  freya deploy-guard: deploy.sh stamps branch+HEAD at sync; refuses deploy on mismatch.
  CLAUDE.md lane: fr-sync backs up freya/CLAUDE.md and diffs — never deploys it back.
EOF
}
