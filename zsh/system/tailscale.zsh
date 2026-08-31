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

# Dashboard lifecycle rebuilt 2026-08-05 (Jacquard trial, revision r1 accepted):
# lsof-free discovery (pgrep + /proc), identity-verified kills (never signal a PID
# without proving it still belongs to ts-dash.py), loud degradation on missing tools,
# server output redirected. Polish: &! disown — no job-control notices in the shell.

_ts_dash_pid_matches() {
    local pid="$1" script="${_TS_ENGINE_DIR}/ts-dash.py"
    [[ "$pid" == <-> && -r "/proc/$pid/cmdline" && -r "/proc/$pid/environ" ]] || return 2
    local -a args environment
    args=("${(@0)$(</proc/$pid/cmdline)}")
    (( ${args[(Ie)$script]} )) || return 1
    environment=("${(@0)$(</proc/$pid/environ)}")
    (( ${environment[(Ie)TS_DASH_PORT=$TS_DASH_PORT]} )) && return 0
    if [[ "$TS_DASH_PORT" == 9733 ]] && (( ! ${environment[(I)TS_DASH_PORT=*]} )); then
        return 0
    fi
    return 1
}

_ts_dash_find_pids() {
    if ! command -v pgrep >/dev/null 2>&1; then
        echo "[ts] cannot discover dashboard: pgrep is required but not installed" >&2
        return 127
    fi
    local matches pgrep_status pid verify_status
    matches=$(pgrep -f -- "${_TS_ENGINE_DIR}/ts-dash.py")
    pgrep_status=$?
    (( pgrep_status == 1 )) && return 0
    if (( pgrep_status != 0 )); then
        echo "[ts] dashboard discovery failed: pgrep exited $pgrep_status" >&2
        return "$pgrep_status"
    fi
    for pid in ${(f)matches}; do
        _ts_dash_pid_matches "$pid"
        verify_status=$?
        if (( verify_status == 0 )); then
            print -r -- "$pid"
        elif (( verify_status == 2 )) && [[ -d "/proc/$pid" ]]; then
            echo "[ts] cannot verify dashboard PID $pid via /proc; refusing to signal it" >&2
            return 2
        fi
    done
}

_ts_dash() {
    local script="${_TS_ENGINE_DIR}/ts-dash.py"
    [[ ! -f "$script" ]] && { echo "[ts] dashboard script not found: $script"; return 1; }
    if ! command -v python3 >/dev/null 2>&1; then
        echo "[ts] cannot start dashboard: python3 is required but not installed" >&2
        return 1
    fi
    if ! command -v sleep >/dev/null 2>&1; then
        echo "[ts] cannot start dashboard: sleep is required but not installed" >&2
        return 1
    fi
    _ts_dash_stop --quiet || return 1
    TS_DASH_PORT="$TS_DASH_PORT" python3 "$script" >/dev/null 2>&1 &!
    typeset -g _TS_DASH_PID=$!
    sleep 0.5
    if ! _ts_dash_pid_matches "$_TS_DASH_PID"; then
        echo "[ts] dashboard failed to start on port $TS_DASH_PORT" >&2
        typeset -g _TS_DASH_PID=""
        return 1
    fi
    echo "[ts] dashboard → http://localhost:${TS_DASH_PORT}  (ts-dash-stop to kill)"
    if command -v xdg-open >/dev/null 2>&1; then
        xdg-open "http://localhost:${TS_DASH_PORT}" >/dev/null 2>&1 &!
    else
        echo "[ts] xdg-open not installed; open the dashboard URL manually"
    fi
}

_ts_dash_stop() {
    local quiet="${1:-}" retained="${_TS_DASH_PID:-}"
    local found pid verify_status
    local -a pids
    if [[ -n "$retained" ]]; then
        _ts_dash_pid_matches "$retained"
        verify_status=$?
        if (( verify_status == 0 )); then
            pids+=("$retained")
        elif [[ -d "/proc/$retained" ]]; then
            echo "[ts] retained PID $retained is not a verified dashboard; refusing to signal it" >&2
        fi
    fi
    found=$(_ts_dash_find_pids) || return 1
    for pid in ${(f)found}; do
        (( ${pids[(Ie)$pid]} )) || pids+=("$pid")
    done
    if (( ! ${#pids} )); then
        typeset -g _TS_DASH_PID=""
        [[ "$quiet" != --quiet ]] && echo "[ts] no dashboard running on port $TS_DASH_PORT"
        return 0
    fi
    if ! command -v sleep >/dev/null 2>&1; then
        echo "[ts] cannot stop dashboard: sleep is required but not installed" >&2
        return 1
    fi
    for pid in "${pids[@]}"; do
        _ts_dash_pid_matches "$pid"
        verify_status=$?
        if (( verify_status != 0 )); then
            echo "[ts] dashboard PID $pid changed or became unverifiable; refusing to signal it" >&2
            return 1
        fi
        if ! kill "$pid"; then
            echo "[ts] failed to signal dashboard PID $pid" >&2
            return 1
        fi
    done
    sleep 0.3
    found=$(_ts_dash_find_pids) || return 1
    if [[ -n "$found" ]]; then
        echo "[ts] dashboard did not stop (PID(s): ${(j:, :)${(f)found}})" >&2
        return 1
    fi
    typeset -g _TS_DASH_PID=""
    [[ "$quiet" != --quiet ]] && echo "[ts] dashboard stopped (port $TS_DASH_PORT)"
    return 0
}

# Open Tailscale admin panel in browser — no local server needed
_ts_web() {
    xdg-open "https://login.tailscale.com/admin/machines" 2>/dev/null || \
        echo "  open: https://login.tailscale.com/admin/machines"
}

# ─── FILE TRANSFER ────────────────────────────────────────────────────────────

# Transporter pad — mirrored on both machines (home + office).
# wiring truth: ~/.majkee/@transporter on each host.
_TS_TRANSPORTER="${HOME}/.majkee/@transporter"

# Pull a file from the peer at the same absolute path (symmetric mirror copy).
# Creates local directory structure if absent. Fast Tailscale tunnel — no git needed.
_ts_pull() {
    local filepath="${1}"
    local peer="${2:-$TAILSCALE_PEER}"
    [[ -z "$filepath" ]] && { echo "[ts] usage: ts-pull <filepath> [peer]"; return 1; }
    [[ -z "$peer" ]] && { echo "[ts] TAILSCALE_PEER not set"; return 1; }
    local dir
    dir=$(dirname "$filepath")
    if [[ ! -d "$dir" ]]; then
        mkdir -p "$dir" && echo "[ts] created: $dir"
    fi
    scp "${peer}:${filepath}" "${filepath}" && echo "[ts] pulled: ${filepath}"
}

# Push a local file to the peer at the same absolute path (symmetric mirror copy).
# Creates remote directory structure if absent. Complement of _ts_pull.
_ts_push() {
    local filepath="${1}"
    local peer="${2:-$TAILSCALE_PEER}"
    [[ -z "$filepath" ]] && { echo "[ts] usage: ts-push <filepath> [peer]"; return 1; }
    [[ -z "$peer" ]] && { echo "[ts] TAILSCALE_PEER not set"; return 1; }
    local dir
    dir=$(dirname "$filepath")
    ssh "$peer" "mkdir -p '${dir}'" || { echo "[ts] failed to create remote dir: ${dir}"; return 1; }
    scp "${filepath}" "${peer}:${filepath}" && echo "[ts] pushed: ${filepath}"
}

# Beam file(s) into the transporter pad on the peer (~/.majkee/@transporter/).
# With arg: drops one file (from anywhere) into the remote pad by basename.
# No arg:   rsyncs the entire local pad to the remote pad.
# Both machines mirror the same pad path — C-type symmetric transporter.
_ts_beam() {
    local target="${1}"
    local peer="${2:-$TAILSCALE_PEER}"
    [[ -z "$peer" ]] && { echo "[ts] TAILSCALE_PEER not set"; return 1; }
    ssh "$peer" "mkdir -p '${_TS_TRANSPORTER}'" 2>/dev/null
    if [[ -n "$target" ]]; then
        local dest="${_TS_TRANSPORTER}/$(basename "${target}")"
        scp "${target}" "${peer}:${dest}" && echo "[ts] beamed: $(basename "${target}") → ${peer}:${dest}"
    else
        if ! command -v rsync >/dev/null 2>&1; then
            echo "[ts] ts-beam (no-arg pad sync) requires rsync — not installed" >&2
            return 1
        fi
        rsync -az --info=progress2 "${_TS_TRANSPORTER}/" "${peer}:${_TS_TRANSPORTER}/" && \
            echo "[ts] pad synced → ${peer}:${_TS_TRANSPORTER}/"
    fi
}

# ─── REMOTE MOUNT (sshfs) ──────────────────────────────────────────────────────

# Mount the peer's filesystem locally via sshfs — then any app (Sublime Text, a
# file manager, grep) finds/opens/edits/saves it as a normal local folder. No
# editor plugin, no server-side install — rides the SFTP subsystem built into any
# normal sshd. sshfs is already present on both machines (pacman, extra repo).
#   ts-mount [peer] [remote-path] [local-mountpoint]
#   remote-path default: peer's home dir (sshfs default when omitted)
#   local-mountpoint default: ~/mnt/<peer>
_ts_mount() {
    local peer="${1:-$TAILSCALE_PEER}"
    local remote="${2:-}"
    local mnt="${3:-${HOME}/mnt/${peer}}"
    [[ -z "$peer" ]] && { echo "[ts] TAILSCALE_PEER not set — pass a peer"; return 1; }
    command -v sshfs >/dev/null 2>&1 || { echo "[ts] sshfs not installed (pacman -S sshfs)"; return 1; }
    if mountpoint -q "$mnt" 2>/dev/null; then
        echo "[ts] already mounted: $mnt"
        return 0
    fi
    mkdir -p "$mnt" || { echo "[ts] failed to create mountpoint: $mnt"; return 1; }
    if sshfs "${peer}:${remote}" "$mnt" -o reconnect,ServerAliveInterval=15,ServerAliveCountMax=3; then
        echo "[ts] mounted ${peer}:${remote:-\~} → $mnt"
    else
        echo "[ts] mount failed: ${peer}:${remote} → $mnt" >&2
        return 1
    fi
}

# Unmount a ts-mount point (idempotent — safe to call when nothing is mounted).
#   ts-umount [local-mountpoint]   default: ~/mnt/$TAILSCALE_PEER
_ts_umount() {
    local mnt="${1:-${HOME}/mnt/${TAILSCALE_PEER}}"
    if ! mountpoint -q "$mnt" 2>/dev/null; then
        echo "[ts] not mounted: $mnt"
        return 0
    fi
    if fusermount -u "$mnt" 2>/dev/null || umount "$mnt" 2>/dev/null; then
        echo "[ts] unmounted: $mnt"
    else
        echo "[ts] unmount failed: $mnt (is a shell/app still using it?)" >&2
        return 1
    fi
}

# ─── DATABASE TUNNEL (cross-host, over tailscale) ─────────────────────────────

# Reach the peer's loopback-bound MariaDB by forwarding a local port through the
# tailscale SSH tunnel. The DB stays bound to 127.0.0.1 on both hosts (hardened by
# ia-sync/install-pkgs/harden-host.md) — nothing is re-opened to the network.
# Guide: reposoma/raw.guides/reach/mariadb-cross-host.md
#   db-reach [peer] [local_port]   default port 3307, peer = $TAILSCALE_PEER
_db_reach() {
    local peer="${1:-$TAILSCALE_PEER}" lport="${2:-3307}"
    [[ -z "$peer" ]] && { echo "[db-reach] TAILSCALE_PEER not set — pass a peer"; return 1; }
    if ss -tln 2>/dev/null | grep -q "127.0.0.1:${lport} "; then
        echo "[db-reach] 127.0.0.1:${lport} already listening — tunnel likely up"
        return 0
    fi
    if ssh -fN -L "${lport}:127.0.0.1:3306" "$peer"; then
        echo "[db-reach] ${peer}:3306 → 127.0.0.1:${lport}   (mysql -h 127.0.0.1 -P ${lport} -u <admin> -p)"
    else
        echo "[db-reach] failed to open tunnel to ${peer}" >&2
        return 1
    fi
}

# Tear down the tunnel opened by _db_reach (matches the exact forward spec).
#   db-reach-down [local_port]   default 3307
_db_reach_down() {
    local lport="${1:-3307}"
    if pkill -f "ssh -fN -L ${lport}:127.0.0.1:3306"; then
        echo "[db-reach] tunnel on 127.0.0.1:${lport} closed"
    else
        echo "[db-reach] no tunnel found on 127.0.0.1:${lport}"
    fi
}

# Route one browser profile through the peer's public egress without exposing a
# proxy port to the LAN or tailnet. In Firefox, use SOCKS v5 at 127.0.0.1:1080
# and enable proxy DNS. Downloads remain on the machine running Firefox.
# Guide: reposoma/raw.guides/browser-egress/GUIDE.md
#   web-reach [peer] [local_port]   default port 1080, peer = $TAILSCALE_PEER
_web_reach() {
    local peer="${1:-$TAILSCALE_PEER}" lport="${2:-1080}"
    [[ -z "$peer" ]] && { echo "[web-reach] TAILSCALE_PEER not set — pass a peer"; return 1; }
    if ss -tln 2>/dev/null | grep -q "127.0.0.1:${lport} "; then
        echo "[web-reach] 127.0.0.1:${lport} already listening — proxy likely up"
        return 0
    fi
    if ssh -fN -D "127.0.0.1:${lport}" -o ExitOnForwardFailure=yes "$peer"; then
        echo "[web-reach] browser egress via ${peer} at SOCKS v5 127.0.0.1:${lport} (enable proxy DNS)"
    else
        echo "[web-reach] failed to open SOCKS proxy to ${peer}" >&2
        return 1
    fi
}

# Start/reuse the default web-reach proxy and open an isolated Firefox profile.
# The profile's user.js is owned by this helper; the operator's normal profile is untouched.
#   web-reach-firefox [url]   default URL = about:blank
_web_reach_firefox() {
    local url="${1:-about:blank}"
    local profile="${HOME}/.mozilla/firefox/office-egress"

    command -v firefox >/dev/null 2>&1 || {
        echo "[web-reach] firefox not found" >&2
        return 1
    }
    _web_reach || return 1

    if pgrep -af firefox 2>/dev/null | grep -Fq -- "--profile ${profile}"; then
        echo "[web-reach] office-egress Firefox already running — use its existing window"
        return 0
    fi

    mkdir -p -m 700 -- "$profile" || return 1
    chmod 700 -- "$profile"
    (
        umask 077
        {
            print -r -- 'user_pref("network.proxy.type", 1);'
            print -r -- 'user_pref("network.proxy.socks", "127.0.0.1");'
            print -r -- 'user_pref("network.proxy.socks_port", 1080);'
            print -r -- 'user_pref("network.proxy.socks_version", 5);'
            print -r -- 'user_pref("network.proxy.socks_remote_dns", true);'
        } >| "${profile}/user.js"
    ) || return 1

    firefox --new-instance --profile "$profile" "$url" >/dev/null 2>&1 &!
    echo "[web-reach] isolated Firefox opened; downloads stay on $(hostname -s)"
}

# Tear down the proxy opened by _web_reach (matches the exact forward spec).
#   web-reach-down [local_port]   default 1080
_web_reach_down() {
    local lport="${1:-1080}"
    if pkill -f "ssh -fN -D 127.0.0.1:${lport}"; then
        echo "[web-reach] SOCKS proxy on 127.0.0.1:${lport} closed"
    else
        echo "[web-reach] no SOCKS proxy found on 127.0.0.1:${lport}"
    fi
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
    printf "  ts-pull <path>   pull same-path file from peer (mirror copy)\n"
    printf "  ts-push <path>   push same-path file to peer (mirror copy)\n"
    printf "  ts-beam [file]   beam file into peer pad · no arg = sync whole pad\n"
    printf "  ts-help          this panel\n"
    printf "  ── cross-host DB (loopback DB over the tunnel) ────\n"
    printf "  db-reach [port]  tunnel peer MariaDB → 127.0.0.1:3307 (default)\n"
    printf "  db-reach-down    close the db-reach tunnel\n"
    printf "  ── browser egress (Firefox at home, network via peer) ─\n"
    printf "  web-reach        SOCKS v5 proxy at 127.0.0.1:1080 via peer\n"
    printf "  web-reach-firefox [url]  open isolated Firefox through peer\n"
    printf "  web-reach-down   close the web-reach proxy\n"
    printf "  ── remote mount (sshfs — browse/edit peer files locally) ─\n"
    printf "  ts-mount [peer] [path] [mnt]  sshfs-mount peer path · default mnt: ~/mnt/<peer>\n"
    printf "  ts-umount [mnt]  unmount a ts-mount point · default: ~/mnt/\$TAILSCALE_PEER\n"
    printf "  ──────────────────────────────────────────────────\n"
    printf "  peer: \$TAILSCALE_PEER=%s\n" "${TAILSCALE_PEER:-(not set)}"
    printf "  pad:  %s\n\n" "${_TS_TRANSPORTER}"
}
