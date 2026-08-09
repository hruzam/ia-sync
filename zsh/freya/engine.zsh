#!/usr/bin/env zsh
# freya/engine.zsh — function bodies for the freya scope
# Sourced by: freya/base.zsh (PARTITION 2)
# Rule: thin wrappers ONLY. All real logic lives in the canonical scripts under
#       $FREYA_DEVENV_DIR. This file never reimplements them.

_FREYA_BUFFER="${FREYA_DEVENV_DIR}/scripts/freya-buffer.sh"
_FREYA_DEPLOY="${FREYA_DEVENV_DIR}/deploy.sh"
_FREYA_SYNC="${FREYA_DEVENV_DIR}/sync.sh"

# ── buffer bus (git app-code office↔home over Tailscale; vendor develop = read) ──
_freya_buffer() {
  [[ -f "$_FREYA_BUFFER" ]] || { echo "[freya] buffer script not found: $_FREYA_BUFFER"; return 1; }
  bash "$_FREYA_BUFFER" "$@"
}

# ── devenv bus (config/harness office↔home — NOT the git buffer) ─────────────────
_freya_deploy() {
  [[ -f "$_FREYA_DEPLOY" ]] || { echo "[freya] deploy.sh not found: $_FREYA_DEPLOY"; return 1; }
  bash "$_FREYA_DEPLOY" "$@"
}

_freya_sync() {
  [[ -f "$_FREYA_SYNC" ]] || { echo "[freya] sync.sh not found: $_FREYA_SYNC"; return 1; }
  bash "$_FREYA_SYNC" "$@"
}

# ── ferry (office→home cascade — an AGENT, not a script; this just signposts) ────
_freya_ferry() {
  echo "[freya] ferry is an agent, not a shell command:"
  echo "        claude --agent ferry -p 'run freya to G3'"
  echo "        staged home-boot script: ${FREYA_DEVENV_DIR}/ferry/prep-home.sh"
}

# ── help ─────────────────────────────────────────────────────────────────────────
_freya_help() {
  printf "\n  ── freya scope ───────────────────────────────────────\n"
  printf "  buffer bus (git app-code, office↔home over Tailscale):\n"
  printf "    fb            status (bare)      · ahead/behind + transports\n"
  printf "    fb-update     fetch vendor develop + merge (journal-safe)\n"
  printf "    fb-push       mirror branch to reachable transports\n"
  printf "    fb-pull       receive other machine's work (ff-only)\n"
  printf "    fb-doctor     remotes + reachability\n"
  printf "    fb-meili      tripwire: meili app-code churn on develop\n"
  printf "    fb-meili-ack  move the meili tripwire baseline\n"
  printf "  devenv bus (config/harness, office↔home):\n"
  printf "    freya-deploy  stage-IN  · devenv → freya working dir\n"
  printf "    freya-sync    stage-OUT · freya .dev/ → devenv\n"
  printf "    freya-ferry   office→home cascade (agent) — prints how\n"
  printf "  ──────────────────────────────────────────────────────\n"
  printf "  devenv dir: %s\n\n" "${FREYA_DEVENV_DIR}"
}
