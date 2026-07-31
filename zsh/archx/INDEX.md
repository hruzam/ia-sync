# Arch Linux Guides Index

Complete documentation for system management and resource monitoring.  
**Location:** `~/reposoma/raw.guildes/archx/`  
**Generated:** 2026-06-28  
**System:** Manjaro (AMD Ryzen 5 3500U, 8 cores, 9.6 GB RAM)

---

## 📚 Available Guides

### 1. **README.md** — Start Here
- Overview of all files
- Quick command reference
- System specifications
- Common workflows

### 2. **ARCH_UPDATE_GUIDE.md** — System Updates
- Full system update procedures
- Pre/post-update checklists
- Troubleshooting updates
- Useful aliases
- Package management commands

### 3. **RESOURCE_MONITORING.md** — PC Resource Usage
- CPU monitoring (usage, top processes, load average)
- Memory monitoring (usage, breakdown, per-process)
- Disk monitoring (usage, directories, I/O)
- Network monitoring (connections, ports, bandwidth)
- Process monitoring (find, tree, kill)
- Combined monitoring dashboards
- Advanced monitoring scripts
- Alert systems

### 4. **QUICK_COMMANDS.sh** — Copy-Paste Recipes
- Instant one-liners (no setup)
- Process monitoring commands
- Watch patterns (live updates)
- Disk space hunting
- Memory analysis
- CPU load analysis
- Troubleshooting checklists
- Performance tuning
- Data logging patterns

### 5. **bash.substrates.sh** — Reusable Functions
- **System Updates (7 functions):** update, refresh, check, cleanup
- **Information Gathering (3 functions):** system info, package stats, orphans
- **Cleanup Operations (3 functions):** cache cleaning, orphan removal
- **Package Queries (3 functions):** search, info, file listing
- **Conditional Logic (2 functions):** conditional updates, safe cleanup flow
- **Parsing/Filtering (3 functions):** parse names, filter, cache size
- **Error Handling (1 function):** fix lockfile
- **CPU Monitoring (4 functions):** snapshot, top, load, watch
- **Memory Monitoring (5 functions):** snapshot, top, breakdown, watch, detailed
- **Disk Monitoring (5 functions):** snapshot, top dirs, watch, I/O, large files
- **Network Monitoring (4 functions):** connections, stats, listening, find port
- **Process Monitoring (3 functions):** find, tree, monitor
- **System Overview (2 functions):** overview, resource alert
- **Total: 45+ reusable functions**

### 6. **journal.uparchx.jsonl** — Session Log
- Machine-readable update logs
- Expandable for future sessions
- Format: JSON lines (one object per line)

---

## 🚀 Quick Start

### For Humans

#### Monitor resources now:
```bash
# Everything at once
top

# Or use substrates
source ~/reposoma/raw.guildes/archx/bash.substrates.sh
substrate_system_overview
substrate_resource_alert 80 80 85

# Or copy-paste from QUICK_COMMANDS.sh
watch -n 2 'free -h && echo "---" && top -bn1 | head -12'
```

#### Update system:
```bash
sudo pacman -Syu
```

### For Agents

#### Load substrates:
```bash
source ~/reposoma/raw.guildes/archx/bash.substrates.sh

# Use functions
substrate_conditional_update
substrate_safe_cleanup_flow
substrate_system_overview
substrate_cpu_top 5
substrate_memory_top 5
substrate_resource_alert 80 80 85
```

---

## 📊 Available Tools

| Tool | Status | Purpose |
|------|--------|---------|
| `top` | ✅ | CPU & memory monitoring (basic) |
| `htop` | ✅ | CPU & memory (enhanced, interactive) |
| `vmstat` | ✅ | Virtual memory & I/O stats |
| `free` | ✅ | Memory breakdown |
| `watch` | ✅ | Repeat commands at intervals |
| `ps` | ✅ | Process list & filtering |
| `ss` | ✅ | Network connections |
| `lsof` | ✅ | List open files & ports |
| `fuser` | ✅ | Find processes by file/port |
| `df` | ✅ | Disk space usage |
| `du` | ✅ | Directory sizes |

---

## 🎯 Common Tasks

### Task: Find What's Using CPU
```bash
# Quick answer
top -bn1 | head -5

# Using substrates
source bash.substrates.sh
substrate_cpu_top 5
```

### Task: Find What's Using Memory
```bash
# Quick answer
ps aux --sort=-%mem | head -6

# Using substrates
substrate_memory_top 10
```

### Task: Monitor Disk Usage
```bash
# Watch fill up
watch -n 5 'df -h | grep /dev'

# Using substrates
substrate_disk_watch 5 /home
```

### Task: Find Large Files
```bash
find /home -type f -size +1G -exec ls -lh {} \;
substrate_disk_large_files /home 1G
```

### Task: Check Network Activity
```bash
# Connections
ss -tunap

# Using substrates
substrate_network_snapshot
substrate_network_listening
```

### Task: Alert on High Usage
```bash
# Set custom thresholds (CPU > 70%, MEM > 75%, DISK > 85%)
substrate_resource_alert 70 75 85
```

---

## 📈 Monitoring Patterns

### Pattern 1: Quick Health Check
```bash
uptime && free -h && df -h | grep /dev
```

### Pattern 2: Interactive Monitoring
```bash
htop  # Press P for CPU, M for memory
```

### Pattern 3: Continuous Logging
```bash
while true; do
  echo "$(date): $(free | grep Mem | awk '{print $3 "/" $2}')"
  sleep 10
done >> memory.log
```

### Pattern 4: Troubleshooting Flowchart
```bash
# 1. Check load
uptime

# 2. Top processes
ps aux --sort=-%cpu | head -5

# 3. Memory pressure
free -h

# 4. Disk I/O
vmstat 1 3

# 5. Disk space
df -h | grep /dev
```

---

## 🛠️ Troubleshooting

### System Slow?
1. Run `substrate_system_overview` to get full picture
2. Look for processes using > 80% CPU: `substrate_cpu_top 5`
3. Look for processes using > 80% memory: `substrate_memory_top 5`
4. Check disk I/O: `substrate_disk_io`
5. Kill if needed: `pkill process-name`

### Running Out of Memory?
1. Check breakdown: `substrate_memory_breakdown`
2. Find hogs: `substrate_memory_top 10`
3. Kill least critical: `pkill -9 process-name`
4. Or reboot if necessary

### Disk Full?
1. Check usage: `substrate_disk_snapshot`
2. Find large dirs: `substrate_disk_top_dirs /home 20`
3. Find large files: `substrate_disk_large_files /home 100M`
4. Delete or move files
5. Clean cache: `substrate_clean_cache`

### Update Fails?
1. Check docs: `ARCH_UPDATE_GUIDE.md` § Troubleshooting
2. Try lock fix: `substrate_fix_lockfile`
3. Or refresh mirrors: `sudo pacman-mirrors --fasttrack`

---

## 📞 Files Quick Reference

| File | Lines | Purpose |
|------|-------|---------|
| README.md | 280 | Navigation & overview |
| ARCH_UPDATE_GUIDE.md | 199 | System updates |
| RESOURCE_MONITORING.md | 500+ | Resource monitoring |
| QUICK_COMMANDS.sh | 250+ | Copy-paste one-liners |
| bash.substrates.sh | 500+ | 45+ reusable functions |
| journal.uparchx.jsonl | 1 | Session log (expandable) |
| INDEX.md | This | Guide index |

**Total:** 2,000+ lines of documentation and code

---

## 🔄 Workflow Examples

### Workflow: Daily Maintenance
```bash
source bash.substrates.sh
substrate_system_info
substrate_count_packages
substrate_resource_alert 80 80 80
substrate_conditional_update && substrate_safe_cleanup_flow
substrate_system_overview
```

### Workflow: Performance Investigation
```bash
source bash.substrates.sh
substrate_system_overview              # Full snapshot
substrate_cpu_watch 2                  # Watch CPU for 10 sec
substrate_memory_watch 2               # Watch memory for 10 sec
substrate_process_tree firefox         # Tree of specific app
```

### Workflow: Continuous Monitoring
```bash
# Terminal 1: Watch resources
watch -n 2 'substrate_system_overview'

# Terminal 2: Log to file
while true; do
  substrate_resource_alert 70 75 85 >> /tmp/alerts.log
  sleep 60
done
```

---

## 💡 Pro Tips

1. **Alias commonly used commands:** Add to `~/.zshrc`:
   ```bash
   alias sysmon='substrate_system_overview'
   alias memtop='substrate_memory_top 10'
   alias cputop='substrate_cpu_top 10'
   ```

2. **Save snapshots before/after changes:**
   ```bash
   substrate_system_overview > before.txt
   # ... make changes ...
   substrate_system_overview > after.txt
   diff before.txt after.txt
   ```

3. **Monitor during installation/builds:**
   ```bash
   watch -n 1 'substrate_memory_snapshot && substrate_cpu_snapshot'
   ```

4. **Create alerts for overnight runs:**
   ```bash
   (while true; do substrate_resource_alert 85 85 90; sleep 300; done) &
   # ... long task ...
   ```

---

## 🎓 For Agent Learning

### Key Bash Patterns in bash.substrates.sh

- **Conditional execution:** `[ -z "$var" ] && return 1`
- **Process filtering:** `ps aux --sort=-%cpu | head -n`
- **AWK parsing:** `awk '{print $1, $3}' | head -10`
- **Command substitution:** `local count=$(pacman -Qu | wc -l)`
- **Heredoc templates:** `cat <<EOF ... EOF`
- **Function composition:** `func1 && func2 || return 1`
- **Error handling:** `return $?`
- **JSON generation:** Output formatted JSON for logging

---

## 📝 Updating This Guide

To add new monitoring capabilities:

1. **Add function to bash.substrates.sh** with `substrate_` prefix
2. **Add section to RESOURCE_MONITORING.md** with explanation
3. **Add one-liner to QUICK_COMMANDS.sh**
4. **Update this INDEX.md** with new function count
5. **Log to journal.uparchx.jsonl** when deployed

---

## Status

✅ **Complete and ready to use**
- 45+ reusable substrate functions
- 6 documentation files
- Tested on your system
- Ready for agent learning

**Next update:** As needed when new tools installed or new patterns discovered

---

Generated by Claude Code — 2026-06-28
