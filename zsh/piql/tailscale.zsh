#!/usr/bin/env zsh
# piql/tailscale.zsh — Tailscale bridge for piql cross-machine access
#
# Shannon: audit any piql-expose call — it widens the attack surface to your
# entire tailnet. SSH pull (piql-remote/piql-watch) is read-only and preferred.
#
# CONFIGURATION (set in config.*.zsh per machine):
#   office:  TAILSCALE_PEER="hruzam"          (home's tailscale hostname)
#            PIQL_PORT="<from piql.env.zsh>"
#   home:    TAILSCALE_PEER="hruzam-120922"   (office's tailscale hostname)
#            PIQL_PORT="<same port>"
#
# piql runs on OFFICE. Architecture: prefilter → bus/pip/pip.zsh → claude CLI + Ollama.
# NO HTTP endpoint — piql-expose() is for future only.
# Cross-machine: piql-ask SSHes to office and runs piql directly (recommended).
# From home: piql-remote, piql-watch, piql-ask. From office: piql-push.

# ─── PIQL CROSS-MACHINE OUTPUT (SSH over Tailscale) ───────────────────────────
PIQL_OUTPUT_FILE="${PIQL_OUTPUT_FILE:-$HOME/.config/piql/last.txt}"
PIQL_LOG_FILE="${PIQL_LOG_FILE:-$HOME/www/piql/piql.dev/session/piql.log}"

# FROM HOME: read last piql output from office
piql-remote() {
    local peer="${1:-$TAILSCALE_PEER}"
    [[ -z "$peer" ]] && { echo "[piql] TAILSCALE_PEER not set"; return 1; }
    ssh "$peer" "cat '${PIQL_OUTPUT_FILE}' 2>/dev/null || echo '[piql] no output file at ${PIQL_OUTPUT_FILE}'"
}
alias piql-pull='piql-remote'

# FROM HOME: live tail of piql log from office (streaming)
piql-watch() {
    local peer="${1:-$TAILSCALE_PEER}"
    [[ -z "$peer" ]] && { echo "[piql] TAILSCALE_PEER not set"; return 1; }
    echo "[piql] watching ${peer}:${PIQL_LOG_FILE} (Ctrl+C to stop)..."
    ssh "$peer" "tail -f '${PIQL_LOG_FILE}'"
}

# FROM OFFICE: push last piql output to peer (home)
piql-push() {
    local peer="${1:-$TAILSCALE_PEER}"
    [[ -z "$peer" ]] && { echo "[piql] TAILSCALE_PEER not set"; return 1; }
    [[ -f "$PIQL_OUTPUT_FILE" ]] || { echo "[piql] no output at $PIQL_OUTPUT_FILE"; return 1; }
    scp "$PIQL_OUTPUT_FILE" "${peer}:${PIQL_OUTPUT_FILE}" && \
        echo "[piql] pushed to $peer:${PIQL_OUTPUT_FILE}"
}

# FROM HOME: run piql query on office via SSH
# Usage: piql-ask "summarize this file: ..."
piql-ask() {
    local peer="${TAILSCALE_PEER}"
    local query="$*"
    [[ -z "$peer" ]] && { echo "[piql] TAILSCALE_PEER not set"; return 1; }
    [[ -z "$query" ]] && { echo "Usage: piql-ask <query>"; return 1; }
    ssh "$peer" "piql '$query'"
}

# ─── TAILSCALE SERVE: expose piql HTTP API on tailnet ────────────────────────
# Shannon: verify piql.env.zsh port before enabling. All tailnet nodes can reach.
# PIQL_PORT must be set in config.*.zsh (check piql.env.zsh for actual value).
PIQL_PORT="${PIQL_PORT:-0}"  # 0 = not configured

piql-expose() {
    [[ "$PIQL_PORT" == "0" ]] && {
        echo "[piql] set PIQL_PORT in config.*.zsh first (check piql.env.zsh)"
        return 1
    }
    echo "[piql] Shannon: confirm this is safe before use"
    tailscale serve --bg "${PIQL_PORT}" && \
        echo "[piql] piql exposed on tailnet at port $PIQL_PORT"
}

piql-expose-off() {
    tailscale serve reset && echo "[piql] tailscale serve removed"
}

piql-expose-status() { tailscale serve status; }
