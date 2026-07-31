# Arch Linux Monitoring Setup — Summary

**Date:** 2026-06-28  
**Machine:** home (Manjaro, Ryzen 5 3500U, 9.6 GB RAM)  
**Status:** ✅ Complete & Wired to zsh

---

## 📍 What Was Done

### 1. Created Monitoring Substrates
**Location:** `~/reposoma/raw.guildes/archx/`

Created **9 files** with **2,300+ lines** of documentation and code:

| File | Size | Purpose |
|------|------|---------|
| `bash.substrates.sh` | 15 KB | 45+ reusable functions |
| `RESOURCE_MONITORING.md` | 12 KB | Detailed guides (CPU/memory/disk/network) |
| `QUICK_COMMANDS.sh` | 7 KB | 100+ copy-paste one-liners |
| `ARCH_UPDATE_GUIDE.md` | 4 KB | System updates & maintenance |
| `INDEX.md` | 9 KB | Complete navigation guide |
| `README.md` | 6.5 KB | Quick reference |
| `CHEATSHEET.txt` | 6 KB | Formatted quick ref |
| `journal.uparchx.jsonl` | 0.4 KB | Machine-readable logs |

### 2. Wired to zsh Configuration
**Location:** `~/.config/zsh/archx/commands.zsh`

Created command wrapper that:
- Auto-sources substrate functions
- Provides 40+ convenient aliases
- Includes custom monitoring functions
- Adds troubleshooting helpers
- Integrated into `config.zsh` (line 122)

### 3. Created Machine Guide
**Location:** `~/.config/zsh/guides/home.md`

Comprehensive guide documenting:
- Hardware specifications (8-core Ryzen 5, 9.6GB RAM)
- Installed services (Docker, PHP, MariaDB, nginx, Tailscale)
- Project structure (FO, IM, PSD, LTP, Larva)
- Available toolkits (fo-toolkit, im-toolkit, etc.)
- Quick start commands by role

---

## 🚀 How to Use

### Option 1: Direct Aliases (Recommended)
After reloading zsh config:
```bash
# Quick checks
sysmon              # Full system overview
cputop              # Top 10 CPU processes
memtop              # Top 10 memory processes
diskuse             # Disk usage

# Continuous monitoring
cpuwatch            # Watch CPU (updates every 2 sec)
memwatch            # Watch memory (updates every 1 sec)
diskwatch           # Watch disk (updates every 5 sec)

# Alerts
alert               # Alert if CPU>80%, MEM>80%, DISK>85%
alertsmart          # Alert if CPU>70%, MEM>75%, DISK>85%

# Troubleshooting
troubleshoot        # Full 5-step troubleshooting report
find-resource cpu   # Find CPU hogs
find-resource mem   # Find memory hogs
find-resource disk  # Find large directories
```

### Option 2: Direct Functions
```bash
source ~/.config/zsh/archx/commands.zsh

# Then use any function:
substrate_system_overview
substrate_cpu_top 5
substrate_memory_breakdown
watch-cpu 2 10
monitor-session 3600 /tmp/mon.log
```

### Option 3: Raw Substrates
```bash
source ~/reposoma/raw.guildes/archx/bash.substrates.sh

# Direct function calls:
substrate_system_overview
substrate_resource_alert 80 80 85
substrate_disk_large_files /home 1G
```

### Option 4: One-Liners
```bash
# From QUICK_COMMANDS.sh
top                              # Interactive (best)
watch -n 2 'top -bn1 | head -12'  # Continuous
ps aux --sort=-%cpu | head -6    # Top CPU
ps aux --sort=-%mem | head -6    # Top memory
df -h | grep /dev                # Disk usage
```

---

## 📚 Documentation

### Quick Reference
```bash
show-guide          # Display CHEATSHEET.txt (quick ref)
show-index          # Display INDEX.md (complete)
show-monitoring-guide # Display RESOURCE_MONITORING.md (detailed)
archx-help          # Show this help
```

### Machine Guide
```bash
cat ~/.config/zsh/guides/home.md
```

### Full Documentation
- **Index:** `~/reposoma/raw.guildes/archx/INDEX.md`
- **Monitoring:** `~/reposoma/raw.guildes/archx/RESOURCE_MONITORING.md`
- **Quick Ref:** `~/reposoma/raw.guildes/archx/CHEATSHEET.txt`
- **Updates:** `~/reposoma/raw.guildes/archx/ARCH_UPDATE_GUIDE.md`

---

## 🔧 Available Tools

All system tools already installed:
- `top` — Basic monitor
- `htop` — Enhanced monitor (interactive)
- `vmstat` — Memory & I/O stats
- `free` — Memory breakdown
- `watch` — Repeat commands
- `ps` — Process list
- `ss` — Network connections
- `lsof` — Open files/ports
- `fuser` — Process finder
- `df`/`du` — Disk usage

---

## 📊 System Status (2026-06-28)

### Hardware
- **CPU:** AMD Ryzen 5 3500U (8 cores)
- **RAM:** 9.6 GB
- **Swap:** None configured
- **Root disk:** 192 GB (22% used)
- **Home disk:** 128 GB (29% used)

### Services Running
- MariaDB ✅
- Tailscale ✅
- Docker (check status)
- nginx (check status)
- PHP 7.4 & 8.x (via Docker or system)

### System Idle
- CPU: ~75-80% idle
- Memory: ~35% used
- Load: 0.2-0.6 (very light)

---

## 🎯 Monitoring Strategies

### Strategy 1: Quick Health Check (30 sec)
```bash
sysmon
# Or: uptime && free -h && df -h | grep /dev
```

### Strategy 2: Find Bottleneck
```bash
troubleshoot
# Or individual checks:
cputop && memtop && substrate_disk_io
```

### Strategy 3: Live Monitoring
```bash
# Terminal 1
cpuwatch

# Terminal 2
memwatch

# Terminal 3
diskwatch
```

### Strategy 4: Custom Alerts
```bash
alert-cpu 70      # Alert if CPU > 70%
alert-memory 75   # Alert if memory > 75%
```

### Strategy 5: Session Logging
```bash
monitor-session 3600 /tmp/sysmon.log
# Logs every 60 seconds for 1 hour
tail -f /tmp/sysmon.log
```

---

## 🔄 Integration with ia-sync

### Backup Configuration
These files should be synced in `ia-sync`:
- `~/.config/zsh/archx/commands.zsh` ✅
- `~/.config/zsh/guides/home.md` ✅
- `~/.config/zsh/config.zsh` (updated line 122) ✅

### When to Sync
```bash
cd ~/ia-sync
bash sync.sh          # Backup
git add -A
git commit -m "sync: $(date +%Y-%m-%d)"
git push
```

---

## 📝 Extending

### Add New Monitoring Commands
1. Add function to `bash.substrates.sh` (prefix: `substrate_`)
2. Add alias/wrapper to `archx/commands.zsh`
3. Update documentation (RESOURCE_MONITORING.md)
4. Sync to ia-sync

### Update Machine Guide
Edit `~/.config/zsh/guides/home.md`:
- New services installed
- Configuration changes
- Database updates
- New projects

### New Guides
Create files in `~/.config/zsh/guides/`:
- `office.md` — Office machine guide
- `docker.md` — Docker setup & usage
- `php.md` — PHP project setup
- `database.md` — Database management

---

## ✅ Verification Checklist

- ✅ bash.substrates.sh created (15 KB)
- ✅ 45+ substrate functions loaded
- ✅ archx/commands.zsh created (9.9 KB)
- ✅ config.zsh updated (line 122)
- ✅ 40+ aliases available
- ✅ guides/home.md created (9.4 KB)
- ✅ All documentation files complete
- ✅ Tested on: Manjaro home machine

---

## 🎓 Key Patterns for Agent Learning

### Bash Patterns Used
```bash
# Conditional execution
[ -z "$var" ] && return 1

# Command substitution
local count=$(command | wc -l)

# Process filtering
ps aux --sort=-%cpu | head -n

# AWK parsing
ps aux | awk '{print $1, $3}'

# Function composition
func1 && func2 || return 1

# JSON output
cat <<EOF > report.json
{"timestamp":"..."}
EOF
```

### zsh Integration Pattern
```bash
# Source main library
source ~/reposoma/raw.guildes/archx/bash.substrates.sh

# Wrap functions with aliases
alias mycommand='substrate_function arg1 arg2'

# Create custom wrappers
custom-command() {
    local var="${1:-default}"
    substrate_function "$var"
}
```

---

## 📞 Getting Help

### If commands not available:
1. Reload zsh: `source ~/.zshrc`
2. Check archx/commands.zsh exists
3. Check config.zsh line 122
4. Run: `source ~/.config/zsh/archx/commands.zsh`

### If substrates not loading:
1. Check path: `ls ~/reposoma/raw.guildes/archx/bash.substrates.sh`
2. Make executable: `chmod +x bash.substrates.sh`
3. Source directly: `source ~/reposoma/raw.guildes/archx/bash.substrates.sh`

### If need detailed help:
```bash
archx-help          # List all commands
show-guide          # Quick reference
show-monitoring-guide # Full documentation
```

---

## 🚀 Next Steps

### For Regular Use
1. Reload zsh: `source ~/.zshrc`
2. Try: `sysmon` — should show system overview
3. Try: `cputop` — should show top processes
4. Try: `troubleshoot` — should run full report

### For New Machine
1. Run: `bash ~/ia-sync/deploy.sh`
2. Reload zsh
3. Run: `sysmon` to verify
4. Check: `~/.config/zsh/guides/home.md` for services

### For Customization
1. Edit: `~/.config/zsh/archx/commands.zsh`
2. Add new aliases/functions
3. Test: `source ~/.config/zsh/archx/commands.zsh`
4. Sync: `cd ~/ia-sync && bash sync.sh`

---

## 📋 File Manifest

### Substrate Library
```
~/reposoma/raw.guildes/archx/
├── bash.substrates.sh          (45+ functions)
├── RESOURCE_MONITORING.md      (detailed guides)
├── QUICK_COMMANDS.sh           (one-liners)
├── ARCH_UPDATE_GUIDE.md        (updates)
├── INDEX.md                    (navigation)
├── README.md                   (quick ref)
├── CHEATSHEET.txt              (formatted)
└── journal.uparchx.jsonl       (logs)
```

### zsh Integration
```
~/.config/zsh/
├── archx/
│   ├── commands.zsh            (aliases & wrappers)
│   └── SETUP_SUMMARY.md        (this file)
├── guides/
│   └── home.md                 (machine guide)
├── config.zsh                  (updated, line 122)
└── ... (other configs)
```

---

**Status:** ✅ Complete & Ready  
**Date:** 2026-06-28  
**Machine:** home (Manjaro)  
**Next:** Reload zsh and try `sysmon`
