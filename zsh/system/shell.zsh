#!/usr/bin/env zsh
# system/shell.zsh — general shell utilities engine
# Scope: cross-machine, non-project, non-monitoring
# Aliases live in system/keyboard.zsh (keyboard convention).
# Sourced by config.zsh (office) and config.home.zsh (home).

_msrc() {
    grep -Hrn "$1" "${PROJECT_FO_PATH:-$HOME/www}"
}

# Zombie / stuck-orphan sweep (2026-09-16, sublime-zombie-tsmount diagnosis).
# A zombie (<defunct>) is inert — it holds nothing but its PID slot and exit
# code, waiting for its parent to reap it; it cannot be killed and does not
# need to be. The actual blockers, if any, are its still-*live* children
# (reparented processes whose PPID is still the zombie's PID). Case that
# motivated this: sublime_text zombie with three live orphan children — two
# killable clean, one wedged in D-state on a stuck ts-mount RPC.
# Read-only by default. Never signals a D-state child: SIGTERM/SIGKILL are
# no-ops there — only the kernel resolving the wait (or a reboot) clears it.
#   zombie-sweep [-k|--kill]
_sys_zombie_sweep() {
    # All locals declared once, up front — NOT re-declared inside the loops
    # below. zsh has a real quirk (verified against a live pty, not a sandbox
    # artifact): a bare `local name` re-declared on a later loop iteration,
    # followed by a separate assignment line, prints the PREVIOUS value as
    # `name=value` stdout noise. Declare-once + assign-in-loop avoids it.
    local do_kill=0 zpid zcomm cpid cstat ccomm
    local -a zpids children
    case "$1" in
        -k|--kill) do_kill=1 ;;
    esac
    command -v pgrep >/dev/null 2>&1 || { echo "[sys] pgrep required, not installed" >&2; return 1; }

    zpids=($(ps -eo pid,stat,comm 2>/dev/null | awk '$2 ~ /Z/{print $1}'))
    if (( ! ${#zpids} )); then
        echo "[sys] no zombie processes found"
        return 0
    fi

    echo "[sys] zombie processes: ${#zpids} — ${(j:, :)zpids}"
    for zpid in "${zpids[@]}"; do
        zcomm=$(ps -o comm= -p "$zpid" 2>/dev/null)
        echo "  · zombie $zpid ($zcomm) — harmless PID-slot leak, clears when its parent reaps it"
        children=($(pgrep -P "$zpid" 2>/dev/null))
        (( ${#children} )) || continue
        for cpid in "${children[@]}"; do
            [[ -d "/proc/$cpid" ]] || continue
            cstat=$(ps -o stat= -p "$cpid" 2>/dev/null | tr -d ' ')
            ccomm=$(ps -o comm= -p "$cpid" 2>/dev/null)
            if [[ "$cstat" == D* ]]; then
                echo "    ⚠ child $cpid ($ccomm) state D (uninterruptible) — cannot be killed; likely blocked on a hung syscall (e.g. a stuck ts-mount — try ts-mount-kill). Clears at reboot only."
            elif [[ "$cstat" == Z* ]]; then
                echo "    · child $cpid ($ccomm) is itself already a zombie — signalling it is a no-op; clears once its parent chain gets reaped."
            elif (( do_kill )); then
                if kill "$cpid" 2>/dev/null; then
                    echo "    ✓ killed orphaned child $cpid ($ccomm) [was state $cstat]"
                else
                    echo "    ✗ failed to signal $cpid ($ccomm)" >&2
                fi
            else
                echo "    · live child $cpid ($ccomm) state $cstat — pass -k to terminate (SIGTERM)"
            fi
        done
    done
    (( do_kill )) || echo "[sys] dry-run — rerun 'zombie-sweep -k' to terminate killable (non-D) children"
}
