#!/usr/bin/env zsh
# system/zram.zsh — zram swap engine (status + parameter management)
# Scope: cross-machine wherever zram-generator is installed (home live 2026-11-12,
# see journal.host-cleanup.md + .dev/session/zram-guard-implementation/pad.1-zram-guard.md).
# Aliases live in system/keyboard.zsh; sourced by system/base.zsh. Defines only.
#
# Files owned (same constants as the PAD):
#   /etc/systemd/zram-generator.conf        [zram0] size / algorithm / priority
#   /etc/sysctl.d/99-zram-swappiness.conf   vm.swappiness
# zswap is runtime-only on purpose (no grub edit) — it reverts to Y on reboot.

_ZRAM_CONF=/etc/systemd/zram-generator.conf
_ZRAM_SYSCTL=/etc/sysctl.d/99-zram-swappiness.conf
_ZRAM_UNIT=systemd-zram-setup@zram0.service

# zram-st — one-screen status
_zram_status() {
    echo "── swap ──";    swapon --show 2>/dev/null || echo "(no swap)"
    echo "── zramctl ──"; zramctl 2>/dev/null || echo "(no zram device)"
    echo "── memory ──";  free -h | sed -n '1,2p;3p'
    echo "── tunables ──"
    echo "vm.swappiness = $(cat /proc/sys/vm/swappiness)"
    echo "zswap         = $(cat /sys/module/zswap/parameters/enabled 2>/dev/null || echo n/a)"
    echo "── config ($_ZRAM_CONF) ──"
    grep -v '^#' "$_ZRAM_CONF" 2>/dev/null || echo "(none)"
    echo "── declared (registry) ──"
    if _machine_get .swap.policy >/dev/null 2>&1; then
        echo "policy        = $(_machine_get .swap.policy)"
        echo "size_mib      = $(_machine_get .swap.zram.size_mib 2>/dev/null || echo -)"
        echo "algorithm     = $(_machine_get .swap.zram.algorithm 2>/dev/null || echo -)"
        echo "priority      = $(_machine_get .swap.zram.priority 2>/dev/null || echo -)"
        echo "swappiness    = $(_machine_get .swap.swappiness 2>/dev/null || echo -)"
        echo "zswap         = $(_machine_get .swap.zswap 2>/dev/null || echo -)"
    else
        echo "(no registry entry — registries/machine.$MACHINE_NAME.json)"
    fi
}

# zram-set [size=4096|4G] [algo=zstd] [prio=100] [swappiness=100] [zswap=on|off] [--no-apply] [--force]
# Rewrites the config for whatever keys are given (others keep their current value),
# then restarts the zram unit. A restart = swapoff, which decompresses every swapped
# page back into RAM — refused when swap-used would not fit in MemAvailable
# (that is how a loaded box freezes/OOMs). --no-apply writes only (takes effect next boot).
_zram_set() {
    local arg k v apply=1 force=0
    local size algo prio swp zsw
    local -a pending
    # current values (defaults = the PAD's)
    size=$(awk -F= '/^zram-size/{gsub(/ /,"",$2);print $2}' "$_ZRAM_CONF" 2>/dev/null); : ${size:=$(_machine_get .swap.zram.size_mib 2>/dev/null)}; : ${size:=4096}
    algo=$(awk -F= '/^compression-algorithm/{gsub(/ /,"",$2);print $2}' "$_ZRAM_CONF" 2>/dev/null); : ${algo:=$(_machine_get .swap.zram.algorithm 2>/dev/null)}; : ${algo:=zstd}
    prio=$(awk -F= '/^swap-priority/{gsub(/ /,"",$2);print $2}' "$_ZRAM_CONF" 2>/dev/null); : ${prio:=$(_machine_get .swap.zram.priority 2>/dev/null)}; : ${prio:=100}
    swp=$(cat /proc/sys/vm/swappiness)
    (( $# )) || { echo "usage: zram-set size=4096|4G algo=zstd prio=100 swappiness=100 zswap=on|off [--no-apply] [--force]"; return 1; }

    for arg in "$@"; do
        case "$arg" in
            --no-apply) apply=0; continue ;;
            --force)    force=1; continue ;;
        esac
        k=${arg%%=*}; v=${arg#*=}
        case "$k" in
            size)
                if [[ "$v" =~ '^[0-9]+[Gg]$' ]]; then v=$(( ${v%[Gg]} * 1024 )); fi
                [[ "$v" =~ '^[0-9]+$' ]] && (( v >= 256 && v <= 16384 )) || { echo "[zram] size: MiB 256–16384 or NG" >&2; return 1; }
                size=$v ;;
            algo)
                grep -qw -- "$v" /sys/block/zram0/comp_algorithm 2>/dev/null \
                    || [[ "$v" =~ '^(zstd|lz4|lzo|lzo-rle|lz4hc|842)$' ]] \
                    || { echo "[zram] algo: unknown '$v'" >&2; return 1; }
                algo=$v ;;
            prio)
                [[ "$v" =~ '^[0-9]+$' ]] && (( v <= 32767 )) || { echo "[zram] prio: 0–32767" >&2; return 1; }
                prio=$v ;;
            swappiness)
                [[ "$v" =~ '^[0-9]+$' ]] && (( v <= 200 )) || { echo "[zram] swappiness: 0–200" >&2; return 1; }
                swp=$v ;;
            zswap)
                case "$v" in on|Y) zsw=Y ;; off|N) zsw=N ;; *) echo "[zram] zswap: on|off" >&2; return 1 ;; esac ;;
            *) echo "[zram] unknown key '$k'" >&2; return 1 ;;
        esac
        pending+=("$k=$v")
    done
    echo "[zram] setting: ${pending[*]}"

    # swappiness + zswap are live-safe (no swapoff)
    if [[ "$swp" != "$(cat /proc/sys/vm/swappiness)" ]]; then
        echo "vm.swappiness=$swp" | sudo tee "$_ZRAM_SYSCTL" >/dev/null \
            && sudo sysctl -q -w vm.swappiness="$swp" && echo "[zram] swappiness = $swp"
    fi
    if [[ -n "$zsw" ]]; then
        echo "$zsw" | sudo tee /sys/module/zswap/parameters/enabled >/dev/null \
            && echo "[zram] zswap = $zsw (runtime only — reverts on reboot)"
    fi

    # device parameters change only if one of them was given
    if (( ${pending[(I)size=*]} || ${pending[(I)algo=*]} || ${pending[(I)prio=*]} )); then
        printf '%s\n' "# managed by zram-set (system/zram.zsh) — $(date +%F)" \
            "[zram0]" "zram-size = $size" "compression-algorithm = $algo" "swap-priority = $prio" \
            | sudo tee "$_ZRAM_CONF" >/dev/null || return 1
        echo "[zram] config written: size=${size}MiB algo=$algo prio=$prio"
        (( apply )) || { echo "[zram] --no-apply: takes effect next boot"; return 0; }

        local used_kib avail_kib
        used_kib=$(awk '/SwapTotal/{t=$2}/SwapFree/{f=$2}END{print t-f}' /proc/meminfo)
        avail_kib=$(awk '/MemAvailable/{print $2}' /proc/meminfo)
        if (( ! force && used_kib * 10 > avail_kib * 8 )); then
            echo "[zram] NOT applied: swap used $((used_kib/1024))MiB vs MemAvailable $((avail_kib/1024))MiB —" >&2
            echo "       swapoff would not fit in RAM. Close things and re-run 'sudo systemctl restart $_ZRAM_UNIT'," >&2
            echo "       or reboot (config is on disk), or --force at your own risk." >&2
            return 2
        fi
        sudo systemctl daemon-reload && sudo systemctl restart "$_ZRAM_UNIT" \
            && echo "[zram] applied" || { echo "[zram] restart failed — systemctl status $_ZRAM_UNIT" >&2; return 1; }
    fi
    _zram_status
}

# zram-reset — undo: remove both config files, swapoff, stop unit (the PAD's revert recipe)
_zram_revert() {
    read -q "?[zram] remove zram swap + config (swapoff)? [y/N] " || { echo; return 1; }
    echo
    sudo swapoff /dev/zram0 2>/dev/null
    sudo systemctl stop "$_ZRAM_UNIT" 2>/dev/null
    sudo rm -f "$_ZRAM_CONF" "$_ZRAM_SYSCTL"
    sudo systemctl daemon-reload
    _zram_status
}

_zram_help() {
    cat <<'H'
zram — swap guard (system/zram.zsh)
  zram-st                          status: swap, zramctl, memory, tunables, config
  zram-set key=val ... [flags]     keys: size=4096|4G  algo=zstd  prio=100
                                        swappiness=100  zswap=on|off
                                   flags: --no-apply (write only) · --force (skip RAM guard)
  zram-revert                      remove config + swapoff (confirms)
Device changes (size/algo/prio) restart the unit = swapoff; refused when swap-used
would not fit in free RAM. swappiness/zswap apply live. zswap is runtime-only.
H
}
