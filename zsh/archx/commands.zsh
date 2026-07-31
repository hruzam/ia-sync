#!/usr/bin/env zsh
# archx/commands.zsh — shell aliases for the archx monitoring suite
# Sourced by config.zsh at shell startup

SUBSTRATES="${BASH_SOURCE[0]:-${(%):-%x}}"
SUBSTRATES_PATH="$(dirname "$SUBSTRATES")/bash.substrates.sh"

[[ -f "$SUBSTRATES_PATH" ]] && source "$SUBSTRATES_PATH" 2>/dev/null

# System overview
alias sysmon='substrate_system_overview'

# CPU
alias cputop='substrate_cpu_top 10'

# Memory
alias memtop='substrate_memory_top 10'

# Disk
alias diskuse='substrate_disk_top_dirs /home 10'

# Services
alias services='substrate_services_check'

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
