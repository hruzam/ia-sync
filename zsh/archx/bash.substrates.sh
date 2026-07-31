#!/bin/bash
# Arch Linux / Manjaro Bash Substrates for Agent Learning
# These are reusable command patterns agents can learn from and compose
# Generated: 2026-06-28

# ============================================================================
# SECTION 1: Update & Sync Operations
# ============================================================================

# Full system update (atomic, idempotent)
substrate_full_update() {
  echo "[SUBSTRATE] Running full system update..."
  sudo pacman -Syu --noconfirm
  return $?
}

# Refresh package database only (no installation)
substrate_refresh_db() {
  echo "[SUBSTRATE] Refreshing package database..."
  sudo pacman -Sy
  return $?
}

# Check for available updates without sudo (read-only)
substrate_check_updates() {
  local count=$(pacman -Qu | wc -l)
  echo "[SUBSTRATE] Available updates: $count"
  pacman -Qu
  return 0
}

# ============================================================================
# SECTION 2: Information Gathering
# ============================================================================

# Get system version info
substrate_system_info() {
  echo "[SUBSTRATE] System Information:"
  echo "Kernel: $(uname -r)"
  echo "Architecture: $(uname -m)"
  echo "Pacman: $(pacman -V | head -1)"
  return 0
}

# Count packages (various states)
substrate_count_packages() {
  local total=$(pacman -Q | wc -l)
  local explicit=$(pacman -Qe | wc -l)
  local deps=$(pacman -Qd | wc -l)
  local updates=$(pacman -Qu | wc -l)
  local orphans=$(pacman -Qdtq 2>/dev/null | wc -l)

  echo "[SUBSTRATE] Package Statistics:"
  echo "  Total installed: $total"
  echo "  Explicitly installed: $explicit"
  echo "  Dependencies: $deps"
  echo "  Available updates: $updates"
  echo "  Orphaned packages: $orphans"
  return 0
}

# List orphaned packages
substrate_list_orphans() {
  echo "[SUBSTRATE] Orphaned Packages:"
  pacman -Qdtq
  return 0
}

# ============================================================================
# SECTION 3: Cleanup Operations
# ============================================================================

# Clean package cache (safe: keeps all current packages)
substrate_clean_cache() {
  echo "[SUBSTRATE] Cleaning old package cache..."
  sudo pacman -Sc --noconfirm
  return $?
}

# Aggressive cache clean (removes all cached packages, saves disk space)
substrate_clean_cache_aggressive() {
  echo "[SUBSTRATE] Aggressive cache cleanup..."
  sudo pacman -Scc --noconfirm
  return $?
}

# Remove orphaned packages
substrate_remove_orphans() {
  local orphan_count=$(pacman -Qdtq 2>/dev/null | wc -l)
  if [ "$orphan_count" -eq 0 ]; then
    echo "[SUBSTRATE] No orphaned packages found"
    return 0
  fi

  echo "[SUBSTRATE] Removing $orphan_count orphaned packages..."
  sudo pacman -Rns $(pacman -Qdtq) --noconfirm
  return $?
}

# ============================================================================
# SECTION 4: Query Operations (Read-Only, No Sudo)
# ============================================================================

# Search for package by name
substrate_search_package() {
  local query="$1"
  [ -z "$query" ] && { echo "Usage: substrate_search_package <package-name>"; return 1; }

  echo "[SUBSTRATE] Searching for packages matching: $query"
  pacman -Ss "$query" | head -20
  return 0
}

# Get package info
substrate_package_info() {
  local pkg="$1"
  [ -z "$pkg" ] && { echo "Usage: substrate_package_info <package-name>"; return 1; }

  echo "[SUBSTRATE] Package information for: $pkg"
  pacman -Si "$pkg" 2>/dev/null || pacman -Qi "$pkg" 2>/dev/null
  return 0
}

# List files in installed package
substrate_package_files() {
  local pkg="$1"
  [ -z "$pkg" ] && { echo "Usage: substrate_package_files <package-name>"; return 1; }

  echo "[SUBSTRATE] Files in package: $pkg"
  pacman -Ql "$pkg"
  return 0
}

# ============================================================================
# SECTION 5: Conditional/Logic Patterns
# ============================================================================

# Update only if updates exist
substrate_conditional_update() {
  echo "[SUBSTRATE] Checking if updates needed..."
  local count=$(pacman -Qu | wc -l)

  if [ "$count" -gt 0 ]; then
    echo "[SUBSTRATE] Found $count updates, proceeding..."
    sudo pacman -Syu --noconfirm
    return $?
  else
    echo "[SUBSTRATE] System is current, no updates needed"
    return 0
  fi
}

# Safe cleanup flow (check → remove orphans → clean cache)
substrate_safe_cleanup_flow() {
  echo "[SUBSTRATE] Starting safe cleanup flow..."

  substrate_count_packages || return 1

  local orphan_count=$(pacman -Qdtq 2>/dev/null | wc -l)
  if [ "$orphan_count" -gt 0 ]; then
    substrate_remove_orphans || return 1
  fi

  substrate_clean_cache || return 1
  echo "[SUBSTRATE] Cleanup flow complete"
  return 0
}

# ============================================================================
# SECTION 6: Parsing/Filtering Patterns
# ============================================================================

# Extract just package names from pacman output
substrate_parse_package_names() {
  echo "[SUBSTRATE] Extracting package names from updates..."
  pacman -Qu | awk '{print $1}'
}

# Filter updates by keyword
substrate_filter_updates() {
  local keyword="$1"
  [ -z "$keyword" ] && { echo "Usage: substrate_filter_updates <keyword>"; return 1; }

  echo "[SUBSTRATE] Updates matching: $keyword"
  pacman -Qu | grep -i "$keyword"
}

# Size of package cache
substrate_cache_size() {
  echo "[SUBSTRATE] Package cache size:"
  du -sh /var/cache/pacman/pkg/
}

# ============================================================================
# SECTION 7: Error Handling Patterns
# ============================================================================

# Resolve pacman lockfile issue
substrate_fix_lockfile() {
  if [ -f /var/lib/pacman/db.lck ]; then
    echo "[SUBSTRATE] Removing stale pacman lockfile..."
    sudo rm /var/lib/pacman/db.lck
    echo "[SUBSTRATE] Lockfile removed, retrying update..."
    sudo pacman -Syu --noconfirm
    return $?
  else
    echo "[SUBSTRATE] No lockfile found"
    return 0
  fi
}

# ============================================================================
# SECTION 8: Reporting & Logging
# ============================================================================

# Generate JSON report of system state
substrate_json_report() {
  local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  local kernel=$(uname -r)
  local updates=$(pacman -Qu | wc -l)
  local orphans=$(pacman -Qdtq 2>/dev/null | wc -l)

  cat <<EOF
{
  "timestamp": "$timestamp",
  "kernel": "$kernel",
  "updates_available": $updates,
  "orphaned_packages": $orphans,
  "pacman_version": "$(pacman -V | head -1 | awk '{print $NF}')",
  "system_current": $([ "$updates" -eq 0 ] && echo "true" || echo "false")
}
EOF
}

# ============================================================================
# SECTION 9: CPU Monitoring
# ============================================================================

# Quick CPU snapshot
substrate_cpu_snapshot() {
  echo "[SUBSTRATE] CPU Snapshot:"
  top -bn1 | head -4
  return 0
}

# Top processes by CPU
substrate_cpu_top() {
  local limit="${1:-10}"
  echo "[SUBSTRATE] Top $limit by CPU usage:"
  printf "  %-12s %6s %5s %5s  %s\n" "USER" "PID" "%CPU" "%MEM" "COMMAND"
  printf "  %-12s %6s %5s %5s  %s\n" "------------" "------" "-----" "-----" "-------"
  ps aux --sort=-%cpu | awk 'NR>1 {printf "  %-12s %6s %5s %5s  %s\n", $1, $2, $3, $4, $11}' | head -"$limit"
  return 0
}

# CPU load average
substrate_cpu_load() {
  echo "[SUBSTRATE] Load Average (1m, 5m, 15m) vs CPU count:"
  local cpus=$(grep -c ^processor /proc/cpuinfo)
  local load=$(uptime | awk -F'load average:' '{print $2}')
  echo "CPUs: $cpus | Load: $load"
  return 0
}

# Watch CPU usage continuously
substrate_cpu_watch() {
  local interval="${1:-2}"
  echo "[SUBSTRATE] Watching CPU (update every $interval sec, Ctrl+C to stop)..."
  watch -n "$interval" 'top -bn1 | head -5'
  return 0
}

# ============================================================================
# SECTION 10: Memory Monitoring
# ============================================================================

# Memory snapshot
substrate_memory_snapshot() {
  echo "[SUBSTRATE] Memory Snapshot:"
  free -h
  echo ""
  vmstat 1 2 | tail -1
  return 0
}

# Top processes by memory
substrate_memory_top() {
  local limit="${1:-10}"
  echo "[SUBSTRATE] Top $limit by memory usage:"
  printf "  %-12s %6s %5s %5s  %s\n" "USER" "PID" "%CPU" "%MEM" "COMMAND"
  printf "  %-12s %6s %5s %5s  %s\n" "------------" "------" "-----" "-----" "-------"
  ps aux --sort=-%mem | awk 'NR>1 {printf "  %-12s %6s %5s %5s  %s\n", $1, $2, $3, $4, $11}' | head -"$limit"
  return 0
}

# Memory detailed breakdown
substrate_memory_breakdown() {
  echo "[SUBSTRATE] Memory Breakdown:"
  free -h | grep -E "^Mem|^Swap"
  echo ""
  echo "Details:"
  free -b | awk 'NR==2 {
    total=$2; used=$3; free=$4; shared=$5; cache=$6; avail=$7;
    printf "  Total:  %.2f GiB\n", total/1024/1024/1024;
    printf "  Used:   %.2f GiB\n", used/1024/1024/1024;
    printf "  Free:   %.2f GiB\n", free/1024/1024/1024;
    printf "  Cache:  %.2f GiB\n", cache/1024/1024/1024;
    printf "  Avail:  %.2f GiB\n", avail/1024/1024/1024;
  }'
  return 0
}

# Watch memory continuously
substrate_memory_watch() {
  local interval="${1:-2}"
  echo "[SUBSTRATE] Watching memory (update every $interval sec, Ctrl+C to stop)..."
  watch -n "$interval" free -h
  return 0
}

# ============================================================================
# SECTION 11: Disk Monitoring
# ============================================================================

# Disk usage snapshot
substrate_disk_snapshot() {
  echo "[SUBSTRATE] Disk Usage:"
  df -h | grep -E "^Filesystem|^/dev"
  return 0
}

# Top directories by size
substrate_disk_top_dirs() {
  local path="${1:-.}"
  local limit="${2:-10}"
  echo "[SUBSTRATE] Top $limit largest directories in $path:"
  du -sh "$path"/* 2>/dev/null | sort -hr | head -"$limit"
  return 0
}

# Watch disk usage
substrate_disk_watch() {
  local interval="${1:-5}"
  local path="${2:-.}"
  echo "[SUBSTRATE] Watching disk usage (update every $interval sec, Ctrl+C to stop)..."
  watch -n "$interval" "df -h | grep -E '^Filesystem|^/dev'"
  return 0
}

# Disk I/O stats
substrate_disk_io() {
  echo "[SUBSTRATE] Disk I/O (bi=bytes in, bo=bytes out):"
  vmstat 1 3 | tail -2
  return 0
}

# Find large files
substrate_disk_large_files() {
  local path="${1:-.}"
  local size="${2:-1G}"
  echo "[SUBSTRATE] Files larger than $size in $path:"
  find "$path" -type f -size +$size -exec ls -lh {} \; 2>/dev/null | awk '{print $5, $NF}'
  return 0
}

# ============================================================================
# SECTION 12: Network Monitoring
# ============================================================================

# Network connections snapshot
substrate_network_snapshot() {
  echo "[SUBSTRATE] Network Connections:"
  ss -tunap 2>/dev/null | head -15
  return 0
}

# Network statistics
substrate_network_stats() {
  echo "[SUBSTRATE] Network Statistics:"
  ss -s 2>/dev/null || echo "ss command failed"
  return 0
}

# Listen ports
substrate_network_listening() {
  echo "[SUBSTRATE] Listening Ports:"
  ss -tlnp 2>/dev/null
  return 0
}

# Find process by port
substrate_network_find_port() {
  local port="$1"
  [ -z "$port" ] && { echo "Usage: substrate_network_find_port <port>"; return 1; }
  echo "[SUBSTRATE] Process using port $port:"
  ss -tlnp 2>/dev/null | grep ":$port" || lsof -i ":$port" 2>/dev/null
  return 0
}

# ============================================================================
# SECTION 13: Process Monitoring
# ============================================================================

# Process search
substrate_process_find() {
  local name="$1"
  [ -z "$name" ] && { echo "Usage: substrate_process_find <process-name>"; return 1; }
  echo "[SUBSTRATE] Processes matching: $name"
  pgrep -la "$name"
  return 0
}

# Process tree
substrate_process_tree() {
  local name="$1"
  if [ -z "$name" ]; then
    echo "[SUBSTRATE] Process tree (all):"
    ps auxww --forest | head -30
  else
    echo "[SUBSTRATE] Process tree for: $name"
    ps auxww --forest | grep -A 10 "$name" | head -20
  fi
  return 0
}

# Real-time process monitor (interactive)
substrate_process_monitor() {
  echo "[SUBSTRATE] Interactive process monitor (htop)..."
  htop || top
  return 0
}

# ============================================================================
# SECTION 13b: Service Status Check
# ============================================================================

# Check status of key services with aligned column output
substrate_services_check() {
  local services=("nginx" "php74-fpm" "php-fpm" "mariadb" "tailscaled" "docker" "valet")
  printf "  %-20s  %s\n" "SERVICE" "STATUS"
  printf "  %-20s  %s\n" "--------------------" "------"
  for svc in "${services[@]}"; do
    if systemctl list-unit-files --type=service 2>/dev/null | grep -q "^${svc}.service"; then
      if systemctl is-active --quiet "$svc" 2>/dev/null; then
        printf "  %-20s  ✅ active\n" "$svc"
      else
        printf "  %-20s  ❌ inactive\n" "$svc"
      fi
    fi
  done
  return 0
}

# ============================================================================
# SECTION 14: System Overview
# ============================================================================

# Full system report (CPU, Memory, Disk, Network)
substrate_system_overview() {
  echo "[SUBSTRATE] ========== SYSTEM OVERVIEW =========="
  echo ""
  echo "--- SYSTEM LOAD ---"
  uptime
  echo ""
  echo "--- CPU ---"
  local cpus=$(grep -c ^processor /proc/cpuinfo)
  local load=$(uptime | awk -F'load average:' '{print $2}' | xargs)
  local cpu_idle=$(top -bn1 | grep "^%Cpu" | awk '{print $8}' | cut -d. -f1)
  local cpu_used=$((100 - cpu_idle))
  printf "  %-10s %s\n" "Cores:" "$cpus"
  printf "  %-10s %s%%\n" "Used:" "$cpu_used"
  printf "  %-10s %s\n" "Load avg:" "$load"
  echo ""
  echo "--- MEMORY ---"
  free -h | awk 'NR==1 {printf "  %-8s %7s %7s %7s %7s\n", "", $1, $2, $3, $6}
                 NR==2 {printf "  %-8s %7s %7s %7s %7s\n", "Mem:", $2, $3, $4, $7}
                 NR==3 {printf "  %-8s %7s %7s %7s\n",     "Swap:", $2, $3, $4}'
  echo ""
  echo "--- DISK ---"
  printf "  %-20s %6s %6s %6s %5s  %s\n" "FILESYSTEM" "SIZE" "USED" "AVAIL" "USE%" "MOUNT"
  df -h | grep "^/dev" | awk '{printf "  %-20s %6s %6s %6s %5s  %s\n", $1, $2, $3, $4, $5, $6}'
  echo ""
  echo "--- TOP PROCESSES (CPU) ---"
  printf "  %-12s %6s %5s %5s  %s\n" "USER" "PID" "%CPU" "%MEM" "COMMAND"
  ps aux --sort=-%cpu | awk 'NR>1 {printf "  %-12s %6s %5s %5s  %s\n", $1, $2, $3, $4, $11}' | head -4
  echo ""
  echo "--- TOP PROCESSES (MEM) ---"
  printf "  %-12s %6s %5s %5s  %s\n" "USER" "PID" "%CPU" "%MEM" "COMMAND"
  ps aux --sort=-%mem | awk 'NR>1 {printf "  %-12s %6s %5s %5s  %s\n", $1, $2, $3, $4, $11}' | head -4
  echo ""
  echo "[SUBSTRATE] ========== END OVERVIEW =========="
  return 0
}

# Alert on resource thresholds
substrate_resource_alert() {
  local cpu_threshold="${1:-80}"
  local mem_threshold="${2:-80}"
  local disk_threshold="${3:-80}"

  echo "[SUBSTRATE] Resource Alert Check (CPU>$cpu_threshold%, MEM>$mem_threshold%, DISK>$disk_threshold%)"

  # Check CPU
  local cpu=$(top -bn1 | grep "^%Cpu" | awk '{print 100-$8}' | cut -d. -f1)
  if [ "$cpu" -gt "$cpu_threshold" ]; then
    echo "⚠️  CPU ALERT: ${cpu}% usage"
    ps aux --sort=-%cpu | head -3
  fi

  # Check Memory
  local mem=$(free | grep Mem | awk '{printf("%.0f", $3/$2 * 100)}')
  if [ "$mem" -gt "$mem_threshold" ]; then
    echo "⚠️  MEMORY ALERT: ${mem}% usage"
    ps aux --sort=-%mem | head -3
  fi

  # Check Disk
  df -h | grep -v "^Filesystem" | while read line; do
    local usage=$(echo "$line" | awk '{print $5}' | sed 's/%//')
    if [ "$usage" -gt "$disk_threshold" ]; then
      local mount=$(echo "$line" | awk '{print $NF}')
      echo "⚠️  DISK ALERT: $mount is ${usage}% full"
    fi
  done

  return 0
}

# ============================================================================
# USAGE EXAMPLES FOR AGENTS
# ============================================================================

# Example 1: Full maintenance cycle
# substrate_conditional_update && substrate_safe_cleanup_flow

# Example 2: Status check before critical operation
# substrate_system_info && substrate_count_packages && substrate_json_report > report.json

# Example 3: Monitor specific package
# substrate_search_package "linux-headers"

# Example 4: One-liner report
# echo "=== SYSTEM STATE ===" && substrate_json_report | jq '.'

# Example 5: Resource monitoring
# substrate_system_overview
# substrate_cpu_top 5
# substrate_memory_top 5
# substrate_disk_snapshot

# Example 6: Continuous monitoring
# substrate_cpu_watch 2
# substrate_memory_watch 1
# substrate_disk_watch 5 /home

# Example 7: Alert on high usage
# substrate_resource_alert 80 80 85

echo "[SUBSTRATES] Loaded. Available functions:"
compgen -A function | grep "^substrate_" | sort
