#!/bin/bash
# Quick Resource Monitoring Commands for Terminal
# Copy-paste friendly one-liners and short scripts
# Generated: 2026-06-28

# ============================================================================
# INSTANT CHECKS (No setup, just paste)
# ============================================================================

# Everything in one view
echo "=== QUICK SYSTEM OVERVIEW ===" && uptime && echo "---" && free -h && echo "---" && df -h | grep /dev && echo "---" && top -bn1 | head -5

# Just CPU usage
top -bn1 | grep "^%Cpu"

# Just memory usage
free -h | grep Mem

# Just disk usage
df -h | grep /dev

# Just load average
uptime

# ============================================================================
# PROCESS MONITORING
# ============================================================================

# Top 5 CPU hogs
ps aux --sort=-%cpu | head -6

# Top 5 memory hogs
ps aux --sort=-%mem | head -6

# Find specific process
ps aux | grep firefox  # Replace 'firefox' with your process

# Kill by name
pkill firefox  # Gentler
pkill -9 firefox  # Force kill

# ============================================================================
# DETAILED MONITORING (with watch for live updates)
# ============================================================================

# Watch memory (updates every 1 second)
watch -n 1 free -h

# Watch disk (updates every 5 seconds)
watch -n 5 'df -h | grep /dev'

# Watch top processes (updates every 2 seconds)
watch -n 2 'ps aux --sort=-%cpu | head -10'

# Watch CPU load
watch -n 2 uptime

# ============================================================================
# USING SUBSTRATES (load functions first)
# ============================================================================

# Load all monitoring substrates
source ~/reposoma/raw.guildes/archx/bash.substrates.sh

# Then use any of these:
substrate_system_overview          # Full report
substrate_cpu_top 5                # Top 5 by CPU
substrate_memory_top 5             # Top 5 by memory
substrate_disk_snapshot            # Disk usage
substrate_network_snapshot         # Network connections
substrate_process_find firefox     # Find by name
substrate_resource_alert 80 80 85  # Alert if thresholds exceeded
substrate_cpu_watch 2              # Live CPU watch
substrate_memory_watch 2           # Live memory watch

# ============================================================================
# FIND WHAT'S USING FILES/PORTS/MEMORY
# ============================================================================

# What's using port 8080?
ss -tlnp | grep :8080
lsof -i :8080

# What's using this file?
lsof /path/to/file
fuser /path/to/file

# What's using a directory?
lsof +D /home/user

# ============================================================================
# DISK SPACE HUNTING
# ============================================================================

# Find largest directories in /home
du -sh /home/* | sort -hr

# Find files larger than 1GB
find /home -type f -size +1G -exec ls -lh {} \;

# Find files modified in last 7 days
find /home -type f -mtime -7 -exec ls -lh {} \; | head -20

# Disk usage tree (depth 2)
du -sh /home/* /home/*/*  | sort -hr | head -20

# ============================================================================
# MEMORY ANALYSIS
# ============================================================================

# Memory by process (total VM and resident memory)
ps aux --sort=-%mem | awk '{print $6, $11}' | head -10

# Count how many processes each user has
ps aux | awk '{print $1}' | sort | uniq -c | sort -rn

# Memory usage by process over time
echo "Timestamp,Memory_Used" > mem_log.csv
for i in {1..10}; do
  echo "$(date +%H:%M:%S),$(free | grep Mem | awk '{print $3}')" >> mem_log.csv
  sleep 10
done

# ============================================================================
# CPU LOAD ANALYSIS
# ============================================================================

# Show load average (easier to read)
uptime | awk -F'load average:' '{print "Load:", $2}'

# Compare load to CPU count
echo "CPUs: $(grep -c ^processor /proc/cpuinfo) | Load: $(uptime | awk -F'average:' '{print $2}')"

# Historical load (last 15 minutes in buckets)
sar 1 60 2>/dev/null || echo "sar not installed, use: watch -n 5 uptime"

# ============================================================================
# NETWORK MONITORING
# ============================================================================

# All connections
ss -tunap

# Just listening ports
ss -tlnp

# Connection count by state
ss -tan | awk '{print $1}' | sort | uniq -c

# Network bandwidth (if iftop installed)
iftop -n  # -n: numeric (no DNS lookup)
# Or use vmstat for simpler view:
vmstat 1 5 | tail -3  # 'bi' and 'bo' are bytes in/out

# ============================================================================
# PERFORMANCE TROUBLESHOOTING CHECKLIST
# ============================================================================

# When system is slow, run this sequence:

# 1. Check load
uptime

# 2. Find CPU hogs
ps aux --sort=-%cpu | head -5

# 3. Find memory hogs
ps aux --sort=-%mem | head -5

# 4. Check I/O (disk read/write)
vmstat 1 3

# 5. Check disk space
df -h | grep /dev

# 6. Check network
ss -tan | awk '{print $1}' | sort | uniq -c

# Full troubleshooting flow:
echo "=== PERFORMANCE TROUBLESHOOTING ===" && \
  echo "LOAD:" && uptime && \
  echo "CPU HOGS:" && ps aux --sort=-%cpu | head -4 && \
  echo "MEMORY HOGS:" && ps aux --sort=-%mem | head -4 && \
  echo "DISK:" && df -h | grep /dev && \
  echo "I/O:" && vmstat 1 2 | tail -1

# ============================================================================
# INTERACTIVE MONITORING (Recommended)
# ============================================================================

# Best interactive tools (press these keys to control):
htop             # Press: P=CPU, M=Memory, T=Tree, F10=Quit
top              # Press: P=CPU, M=Memory, z=colors, q=Quit

# Watch combined info (updates every 2 sec)
watch -n 2 'echo "=== LOAD ===" && uptime && echo "=== MEMORY ===" && free -h && echo "=== TOP CPU ===" && ps aux --sort=-%cpu | head -5'

# ============================================================================
# SAVE MONITORING DATA
# ============================================================================

# Snapshot to file
{
  echo "=== Snapshot at $(date) ==="
  echo "Load: $(uptime)"
  echo "Memory: $(free -h | grep Mem)"
  echo "Disk: $(df -h | grep /dev)"
  echo "Top processes:"
  ps aux --sort=-%cpu | head -5
} > sysmon_$(date +%Y%m%d_%H%M%S).txt

# Continuous logging (every 60 seconds)
while true; do
  {
    date
    uptime
    free -h | grep Mem
    ps aux --sort=-%cpu | head -3
    echo "---"
  } >> /tmp/sysmon.log
  sleep 60
done &

# View the log
tail -f /tmp/sysmon.log

# ============================================================================
# NOTES
# ============================================================================

# • Idle CPU (93%+) = System is not busy → fast response expected
# • Available Memory (6.4 GB) = Can allocate without swapping
# • Disk Usage (22%) = Plenty of space left
# • No swap configured = Everything in RAM, no slowdown from disk swaps

# Key metrics:
# - CPU idle > 50% = CPU not bottleneck
# - Available memory > 1 GB = No memory pressure
# - Disk usage < 80% = Sufficient space
# - Load average < CPU count = System not overloaded

# ============================================================================
