#!/usr/bin/env zsh
# system/tailscale.zsh — Tailscale scope engine
# Scope: cross-machine (home + office); pure tailscale, no piql wiring
# Sourced by: config.zsh (via keyboard.zsh companion)
# Aliases surface: system/keyboard.zsh
# Dashboard script: system/ts-dash.py
#
# CONFIGURATION — set in config.*.zsh per machine:
#   export TAILSCALE_PEER="hruzam-120922"   # home → office
#   export TAILSCALE_PEER="hruzam"          # office → home
#   export TS_DASH_PORT="9733"              # optional, default 9733

_TS_ENGINE_DIR="${0:A:h}"
TS_DASH_PORT="${TS_DASH_PORT:-9733}"

# ─── STATUS ───────────────────────────────────────────────────────────────────

_ts_ls() {
    local self_ip
    self_ip=$(tailscale ip -4 2>/dev/null || echo "?")
    # Filter to peer lines only (start with IP digit) — drops health warnings and self-line
    local out
    out=$(timeout 3 tailscale status 2>/dev/null | grep -E '^[0-9]' | grep -v "^${self_ip}") || {
        echo "[ts] tailscaled not running or timed out"
        return 1
    }

    printf "\n  ── Tailscale peers (%s) ─────────────────────\n" "$(hostname -s)"
    printf "  ◈ %-22s %s  (self)\n" "$(hostname -s)" "$self_ip"
    while IFS= read -r line; do
        [[ -z "$line" ]] && continue
        local ip host rest
        ip=$(awk '{print $1}' <<< "$line")
        host=$(awk '{print $2}' <<< "$line")
        rest=$(awk '{for(i=5;i<=NF;i++) printf $i" "}' <<< "$line" | xargs)
        if [[ "$rest" == "-" || -z "$rest" ]]; then
            printf "  ○ %-22s %s\n" "$host" "$ip"
        else
            printf "  ● %-22s %s  [%s]\n" "$host" "$ip" "$rest"
        fi
    done <<< "$out"
    printf "  ─────────────────────────────────────────────\n\n"
}

# Compact one-liner for shell startup — 2s timeout, fully silent if tailscaled is down.
# Called from config.*.zsh after sourcing this engine.
_ts_header() {
    local self_ip
    self_ip=$(tailscale ip -4 2>/dev/null || echo "?")
    # Peer lines only — skip self, health warnings, empty
    local out
    out=$(timeout 2 tailscale status 2>/dev/null | grep -E '^[0-9]' | grep -v "^${self_ip}") || return 0
    local total online=0
    total=$(wc -l <<< "$out")
    while IFS= read -r line; do
        [[ -z "$line" ]] && continue
        local rest
        rest=$(awk '{for(i=5;i<=NF;i++) printf $i" "}' <<< "$line" | xargs)
        [[ "$rest" != "-" && -n "$rest" ]] && (( online++ ))
    done <<< "$out"
    printf "  ts %-16s  %d/%d peers online  — ts-ls for details\n" \
        "$self_ip" "$online" "$total"
}

# ─── CONNECTION ───────────────────────────────────────────────────────────────

_ts_ping() {
    local peer="${1:-$TAILSCALE_PEER}"
    [[ -z "$peer" ]] && { echo "[ts] TAILSCALE_PEER not set"; return 1; }
    tailscale ping "$peer"
}

# Direct SSH — fast, no output before connect
_ts_ssh() {
    local peer="${1:-$TAILSCALE_PEER}"
    [[ -z "$peer" ]] && { echo "[ts] TAILSCALE_PEER not set in config.zsh"; return 1; }
    ssh "$peer"
}

# SSH with pre-connect reachability check
_ts_session() {
    local peer="${1:-$TAILSCALE_PEER}"
    [[ -z "$peer" ]] && { echo "[ts] TAILSCALE_PEER not set in config.zsh"; return 1; }
    printf "\n  connecting → %s\n  ping: " "$peer"
    if timeout 3 tailscale ping --c 1 "$peer" &>/dev/null; then
        printf "reachable ✓\n\n"
    else
        printf "no response (proceeding anyway)\n\n"
    fi
    ssh "$peer"
}

# ─── DASHBOARD ────────────────────────────────────────────────────────────────

_ts_dash() {
    local script="${_TS_ENGINE_DIR}/ts-dash.py"
    [[ ! -f "$script" ]] && { echo "[ts] dashboard script not found: $script"; return 1; }
    local old_pid
    old_pid=$(lsof -ti tcp:"$TS_DASH_PORT" 2>/dev/null)
    [[ -n "$old_pid" ]] && kill "$old_pid" 2>/dev/null && sleep 0.3
    echo "[ts] dashboard → http://localhost:${TS_DASH_PORT}  (ts-dash-stop to kill)"
    TS_DASH_PORT="$TS_DASH_PORT" python3 "$script" &
    sleep 0.5
    xdg-open "http://localhost:${TS_DASH_PORT}" 2>/dev/null &
}

_ts_dash_stop() {
    local pid
    pid=$(lsof -ti tcp:"$TS_DASH_PORT" 2>/dev/null)
    if [[ -n "$pid" ]]; then
        kill "$pid" && echo "[ts] dashboard stopped (port $TS_DASH_PORT)"
    else
        echo "[ts] no dashboard running on port $TS_DASH_PORT"
    fi
}

# Open Tailscale admin panel in browser — no local server needed
_ts_web() {
    xdg-open "https://login.tailscale.com/admin/machines" 2>/dev/null || \
        echo "  open: https://login.tailscale.com/admin/machines"
}

# ─── HELP ─────────────────────────────────────────────────────────────────────

_ts_help() {
    printf "\n  ── Tailscale ─────────────────────────────────────\n"
    printf "  tss              raw status table\n"
    printf "  tsip             my tailscale IP (100.x.x.x)\n"
    printf "  ts-ls            formatted peer list (online/offline)\n"
    printf "  tsping [host]    ping peer  · default: \$TAILSCALE_PEER\n"
    printf "  tsp [host]       ssh to peer (fast, no header)\n"
    printf "  tso [host]       ssh with pre-connect status line\n"
    printf "  ts-dash          start HTTP status dashboard (port %s)\n" "$TS_DASH_PORT"
    printf "  ts-dash-stop     stop dashboard\n"
    printf "  ts-web           open login.tailscale.com/admin/machines\n"
    printf "  ts-help          this panel\n"
    printf "  ──────────────────────────────────────────────────\n"
    printf "  peer: \$TAILSCALE_PEER=%s\n\n" "${TAILSCALE_PEER:-(not set)}"
}
