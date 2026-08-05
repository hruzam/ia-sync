#!/usr/bin/env zsh
# archx/commands.zsh — archx monitoring suite engine
# Sourced by config.zsh at shell startup (both machines)
# Aliases:  archx/keyboard.zsh (control panel — aliases + comments only, WP4 retrofit)
# Bodies:   this file (troubleshoot) + archx/bash.substrates.sh (substrate_*)

SUBSTRATES="${BASH_SOURCE[0]:-${(%):-%x}}"
SUBSTRATES_PATH="$(dirname "$SUBSTRATES")/bash.substrates.sh"

[[ -f "$SUBSTRATES_PATH" ]] && source "$SUBSTRATES_PATH" 2>/dev/null

# =============================================================================
# HELP
# =============================================================================
_archx_help() {
    cat << 'EOF'
archx — Arch Linux monitoring commands (engine: archx/commands.zsh + bash.substrates.sh)

  sysmon        one-shot system overview (load, mem, disk, top procs — substrate_system_overview)
  cputop        top 10 CPU-consuming processes (substrate_cpu_top 10)
  memtop        top 10 memory-consuming processes (substrate_memory_top 10)
  diskuse       top 10 largest directories under /home (substrate_disk_top_dirs)
  services      check status of the watched systemd services (substrate_services_check)
  troubleshoot  quick diagnostics dump: load, top-5 CPU, memory, disk, services
EOF
}

# Quick troubleshoot
troubleshoot() {
    echo ""
    echo "╔════════════════════════════════════════════════╗"
    echo "║            QUICK DIAGNOSTICS                   ║"
    echo "╚════════════════════════════════════════════════╝"
    echo ""
    echo "--- LOAD ---"
    uptime
    echo ""
    echo "--- CPU (top 5) ---"
    substrate_cpu_top 5 2>/dev/null
    echo ""
    echo "--- MEMORY ---"
    free -h | awk 'NR==1 {printf "  %-8s %7s %7s %7s\n", "", $1, $2, $6}
                   NR==2 {printf "  %-8s %7s %7s %7s\n", "Mem:", $2, $3, $7}'
    echo ""
    echo "--- DISK ---"
    df -h | grep "^/dev" | awk '{printf "  %-20s %5s used  %s\n", $1, $5, $6}'
    echo ""
    echo "--- SERVICES ---"
    substrate_services_check 2>/dev/null
    echo ""
}
