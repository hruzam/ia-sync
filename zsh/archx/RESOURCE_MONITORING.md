# PC Resource Monitoring Guide

> Comprehensive guide for observing CPU, memory, disk, and network usage via terminal  
> System: Manjaro (AMD Ryzen 5 3500U, 8 cores, 9.6 GB RAM)  
> Generated: 2026-06-28

---

## 🚀 Quick Start: One-Liners

### Instant System Overview
```bash
# Everything at a glance (CPU, Memory, Processes)
top -bn1 | head -20

# Real-time monitoring (interactive)
htop

# Memory snapshot
free -h

# CPU, Load, and Top Processes
uptime && echo "---" && top -bn1 | head -12
```

### Watch Resources Change Live
```bash
# Update every 2 seconds
watch -n 2 'free -h && echo "---" && top -bn1 | head -12'

# Memory timeline
watch -n 1 free -h

# CPU usage timeline
watch -n 1 'top -bn1 | head -5'
```

---

## 📊 Available Tools on Your System

| Tool | Installed | Purpose |
|------|-----------|---------|
| `top` | ✅ Yes | CPU/Memory usage, process list |
| `htop` | ✅ Yes | Enhanced `top` with colors & tree view |
| `vmstat` | ✅ Yes | Virtual memory, I/O, CPU stats |
| `free` | ✅ Yes (alias) | Memory usage breakdown |
| `watch` | ✅ Yes | Repeat commands at intervals |
| `ps` | ✅ Yes (built-in) | List processes, filter by CPU/memory |
| `ss` | ✅ Yes | Network connections & statistics |
| `lsof` | ✅ Yes | List open files (find what uses files) |
| `fuser` | ✅ Yes | Find processes using files/ports |
| `lscpu` | ✅ Yes (built-in) | CPU info |
| `df` | ✅ Yes (built-in) | Disk space usage |
| `du` | ✅ Yes (built-in) | Directory sizes |

---

## 🔍 Detailed Monitoring Recipes

### CPU Monitoring

#### 1. Overall CPU Usage
```bash
# Snapshot
top -bn1 | head -3

# Output:
# top - 23:30:48 up 28 min,  1 user,  load average: 0,50, 0,59, 0,83
# Tasks: 272 total, 1 running, 269 sleep, 0 d-sleep, 0 stopped, 2 zombie
# %Cpu(s):  3,3 us,  2,7 sy,  0,0 ni, 93,4 id,  0,5 wa,  0,0 hi,  0,0 si,  0,0 st
```

**Read this as:**
- `3.3% us` = User processes (your apps)
- `2.7% sy` = System/kernel
- `93.4% id` = Idle (available)
- `0.5% wa` = Waiting for I/O

#### 2. CPU Per Core
```bash
# Show usage per core
top -bn1 | grep "^%Cpu"

# Or per-thread view
htop  # Then press 'F' → 1 to see per-core
```

#### 3. Top CPU Consumers (Processes)
```bash
# Top 10 by CPU
ps aux --sort=-%cpu | head -11

# Continuous update (every 2 sec)
watch -n 2 'ps aux --sort=-%cpu | head -11'

# Just names and percentages
ps aux --sort=-%cpu | awk '{print $11, $3}' | head -10
```

#### 4. Load Average
```bash
# Shows: 1-min, 5-min, 15-min average
uptime

# Compare to CPU count (yours: 8 cores)
echo "Load average threshold (8 cores): $(grep -c ^processor /proc/cpuinfo)"
```

---

### Memory Monitoring

#### 1. Total Memory Status
```bash
# Easy-to-read format
free -h

# Output shows: Total | Used | Free | Shared | Buff/Cache | Available
# Example output from your system:
#               total        used        free      shared  buff/cache   available
# Mem:           9,6Gi       3,2Gi       835Mi       136Mi       6,0Gi       6,4Gi
# Swap:             0B          0B          0B
```

**Key interpretation:**
- `used`: Actively used by processes
- `buff/cache`: Cached data (can be freed if needed)
- `available`: Free + cache available to apps

#### 2. Memory Per Process
```bash
# Top 10 memory hogs
ps aux --sort=-%mem | head -11

# Show only PID, %MEM, command
ps aux --sort=-%mem | awk '{print $2, $4, $11}' | head -10

# Find memory usage of specific app
ps aux | grep firefox | head -1

# Continuous view
watch -n 2 'ps aux --sort=-%mem | head -11'
```

#### 3. Virtual Memory / Swap
```bash
# Detailed memory stats
vmstat 1 5  # (shows 5 iterations, 1 sec apart)

# Column explanations:
# r    = processes running on CPU
# b    = processes blocked on I/O
# swpd = swap used (should be 0 on your system)
# free = free memory
# buff = buffer memory
# cache = page cache
# si/so = swap in/out (watch these!)
# us/sy/id/wa = CPU percentage
```

#### 4. Find Memory Leaks
```bash
# Memory growth over time (run every 10 seconds, log results)
for i in {1..30}; do
  echo "$(date +%H:%M:%S): $(free -h | grep Mem | awk '{print $3 " / " $2}')"
  sleep 10
done

# If "used" keeps growing while nothing is running, you have a leak
```

---

### Disk Monitoring

#### 1. Overall Disk Usage
```bash
# Summary (all filesystems)
df -h

# Human-readable with totals
df -h | tail -n +2  # Skip header

# Your system:
# /dev/nvme0n1p4  192G   40G  143G  22% /
# /dev/nvme0n1p5  128G   35G   87G  29% /home
```

#### 2. Directory Sizes
```bash
# Total size of directory
du -sh /home

# Top 10 largest directories
du -sh /home/* | sort -hr | head -10

# Deep dive (show tree)
du -sh /home/*/* | sort -hr | head -20

# Find files > 1GB
find /home -type f -size +1G -exec ls -lh {} \;
```

#### 3. Disk I/O Activity
```bash
# Virtual memory stats (includes I/O)
vmstat 1 3

# Watch for high 'bi' (bytes in) or 'bo' (bytes out) columns
```

#### 4. Monitor Specific Partition
```bash
# Watch a partition fill up
watch -n 5 'df -h | grep nvme0n1p4'

# Alert when usage exceeds threshold
if [ $(df / | tail -1 | awk '{print $5}' | sed 's/%//') -gt 80 ]; then
  echo "WARNING: Root partition > 80% full!"
fi
```

---

### Network Monitoring

#### 1. Current Connections
```bash
# All connections (TCP + UDP)
ss -tunap

# TCP only
ss -tup

# UDP only
ss -uup

# Just listening ports
ss -tlnp

# Count connections
ss -tunap | wc -l
```

#### 2. Connection Statistics
```bash
# Summary stats
ss -s

# Output shows: TCP, UDP, ICMP, IPv4, IPv6 stats
```

#### 3. Find Process Using Port
```bash
# What's listening on port 22?
ss -tlnp | grep :22

# Find process using port 8080
lsof -i :8080

# Find process using UDP 5353
lsof -i udp:5353
```

#### 4. Monitor Bandwidth (If `iftop` installed)
```bash
# Check if installed
which iftop

# If not, use network stats from vmstat
vmstat 1 5  # Watch 'bi' and 'bo' columns
```

---

### Process Monitoring

#### 1. Find Specific Process
```bash
# Search by name
ps aux | grep firefox

# More elegant
pgrep firefox

# With details
pgrep -la firefox
```

#### 2. Process Tree
```bash
# Show parent-child relationships
ps auxww --forest

# Or with pstree if available
pstree -p -u  # -p: PID, -u: username

# For specific app
ps auxww --forest | grep -A 5 firefox
```

#### 3. Kill Resource Hog
```bash
# First, identify it
top  # Press M (sort by memory) or P (by CPU)

# Kill by PID
kill 1234

# Or by name
pkill firefox

# Force kill
kill -9 1234
```

#### 4. Continuous Process Monitoring
```bash
# Real-time (interactive)
htop

# Auto-update every 2 seconds
watch -n 2 'ps aux --sort=-%cpu | head -15'

# Focus on one process
watch -n 1 'ps aux | grep firefox'
```

---

### Combined Monitoring

#### 1. Everything at Once
```bash
# Quick dashboard
echo "=== SYSTEM LOAD ===" && uptime && \
echo "=== CPU ===" && top -bn1 | head -4 && \
echo "=== MEMORY ===" && free -h && \
echo "=== DISK ===" && df -h | grep nvme && \
echo "=== TOP PROCESSES ===" && ps aux --sort=-%cpu | head -5
```

#### 2. Interactive Dashboard
```bash
# Best option: use htop
htop

# Keyboard shortcuts in htop:
# P = sort by CPU
# M = sort by memory
# T = tree view
# F4 = filter
# F5 = tree view toggle
# F10 = quit
```

#### 3. Watch Multiple Things
```bash
# Update every 3 seconds
watch -n 3 'echo "CPU:"; top -bn1 | head -5; echo "MEMORY:"; free -h'
```

---

## 📈 System Status: Your Machine

### Hardware Specs
```
Processor:   AMD Ryzen 5 3500U with Radeon Vega Mobile Gfx
Cores:       8
Memory:      9.6 GB
Swap:        0 GB (none)
Storage:     /: 192GB (22% used), /home: 128GB (29% used)
```

### Current Usage (Snapshot)
```
CPU:         93.4% idle (3.3% user, 2.7% system)
Load:        0.50 (1m), 0.59 (5m), 0.83 (15m)
Memory:      3.2 GB / 9.6 GB (34% used), 6.4 GB available
Swap:        Not configured
Network:     Connected (192.168.0.6)
```

### Top Resource Consumers
```
1. pamac-daemon        (CPU: 24%, MEM: 5.3%)
2. claude.exe          (CPU: 12.6%, MEM: 4.4%)
3. plasmashell         (CPU: 9.5%, MEM: 4.1%)
4. kwin_wayland        (CPU: 6.5%, MEM: 2.8%)
5. sublime_text        (CPU: 3.3%, MEM: 2.3%)
```

---

## 🛠️ Useful Aliases

Add to `~/.bashrc` or `~/.zshrc`:

```bash
# Quick monitoring
alias sysstat='echo "=== LOAD ===" && uptime && echo "=== CPU ===" && top -bn1 | head -4 && echo "=== MEMORY ===" && free -h'
alias memtop='ps aux --sort=-%mem | head -11'
alias cputop='ps aux --sort=-%cpu | head -11'
alias diskuse='du -sh /home/* | sort -hr'
alias netstat='ss -tunap'
alias watch-memory='watch -n 1 free -h'
alias watch-disk='watch -n 5 "df -h | grep -E \"Filesystem|nvme\"'
alias open-ports='ss -tlnp'
alias find-process='ps aux | grep'  # Usage: find-process firefox
```

Reload shell:
```bash
source ~/.zshrc
```

---

## 📊 Monitoring Strategies

### Strategy 1: Quick Health Check (30 seconds)
```bash
uptime && free -h && df -h | grep nvme
```

### Strategy 2: Find Performance Bottleneck
```bash
# 1. Check CPU
top -bn1 | head -5

# 2. Check Memory
free -h

# 3. Check Disk I/O
vmstat 1 3

# 4. Check specific hogs
ps aux --sort=-%cpu | head -5
ps aux --sort=-%mem | head -5
```

### Strategy 3: Continuous Monitoring (Production)
```bash
# Log to file every 60 seconds
while true; do
  echo "=== $(date) ===" >> /tmp/sysmon.log
  echo "Load: $(uptime | awk -F'load average:' '{print $2}')" >> /tmp/sysmon.log
  free -h | grep Mem >> /tmp/sysmon.log
  top -bn1 | grep "^%Cpu" >> /tmp/sysmon.log
  sleep 60
done &

# View logs
tail -f /tmp/sysmon.log
```

### Strategy 4: Investigate High Memory/CPU
```bash
# Find the culprit
ps aux --sort=-%mem | head -5

# Get its details
ps aux | grep [p]rocess-name  # Note: [p] avoids matching grep itself

# Monitor just that process
watch -n 1 'ps aux | grep [p]rocess-name'

# Check what it's doing
lsof -p 1234  # 1234 = PID

# Kill if needed
kill -9 1234
```

---

## 🔧 Advanced: Custom Monitoring Scripts

### Script 1: CPU Alert
```bash
#!/bin/bash
THRESHOLD=80
while true; do
  CPU=$(top -bn1 | grep "^%Cpu" | awk '{print 100-$8}' | cut -d. -f1)
  if [ "$CPU" -gt "$THRESHOLD" ]; then
    echo "⚠️  CPU ALERT: $CPU% (threshold: $THRESHOLD%)"
    ps aux --sort=-%cpu | head -3
  fi
  sleep 10
done
```

### Script 2: Memory Alert
```bash
#!/bin/bash
THRESHOLD=80
while true; do
  MEM=$(free | grep Mem | awk '{printf("%.0f", $3/$2 * 100)}')
  if [ "$MEM" -gt "$THRESHOLD" ]; then
    echo "⚠️  MEMORY ALERT: $MEM% (threshold: $THRESHOLD%)"
    ps aux --sort=-%mem | head -3
  fi
  sleep 10
done
```

### Script 3: Disk Alert
```bash
#!/bin/bash
THRESHOLD=80
df -h | grep -v "^Filesystem" | while read line; do
  USAGE=$(echo $line | awk '{print $5}' | sed 's/%//')
  if [ "$USAGE" -gt "$THRESHOLD" ]; then
    MOUNT=$(echo $line | awk '{print $NF}')
    echo "⚠️  DISK ALERT: $MOUNT is $USAGE% full"
  fi
done
```

---

## 🎯 Common Use Cases

| Use Case | Command |
|----------|---------|
| App using all CPU? | `top` then `P` to sort by CPU |
| RAM filling up? | `free -h` then `watch -n 1 free -h` |
| Disk running out? | `df -h` then `du -sh /* \| sort -hr` |
| Port in use? | `ss -tlnp \| grep :8080` or `lsof -i :8080` |
| What's slowing system? | `htop` + sort by CPU/memory |
| Process using file? | `lsof /path/to/file` or `fuser /path/to/file` |
| Monitor during task? | `watch -n 2 'free -h && ps aux \| head -10'` |
| Log metrics hourly? | Cron job running monitoring script |

---

## 📚 Reference

- **Man Pages:** `man top`, `man htop`, `man vmstat`, `man ps`, `man ss`, `man lsof`
- **Arch Wiki:** https://wiki.archlinux.org/title/Systemd
- **Performance:** https://wiki.archlinux.org/title/Improving_performance

---

Generated: 2026-06-28  
Status: Ready to use on your Manjaro system
