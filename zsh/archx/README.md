# Arch Linux / Manjaro Update & Maintenance Guide

**Purpose:** Central documentation hub for Arch system updates and maintenance. Designed for both human reference and agent learning.

**Last Updated:** 2026-06-28  
**System State:** Manjaro 6.18.26-1 (Arch-based) — Current (all updates applied)

---

## 📁 Files in This Directory

### 1. **ARCH_UPDATE_GUIDE.md** (Primary Reference)
Human-readable guide covering:
- Quick start commands
- Pre/post-update checklists
- Troubleshooting common issues
- System information snapshot
- Useful shell aliases

**Start here for:** Learning how to update, understanding what commands do, fixing problems

### 2. **bash.substrates.sh** (Agent Learning)
Reusable bash functions organized by category:
- Update & sync operations
- Information gathering
- Cleanup operations
- Query operations (read-only)
- Conditional/logic patterns
- Parsing & filtering
- Error handling
- JSON reporting

**Use this for:** Composing update scripts, learning reusable patterns, building automation

### 3. **journal.uparchx.jsonl** (Session Log)
Machine-readable JSON lines log of update sessions.

**Format:**
```json
{
  "timestamp": "ISO-8601",
  "session_id": "unique-identifier",
  "action": "system_update|cleanup|check",
  "status": "completed|pending|error",
  "system": {...},
  "command": "...",
  "result": "success|failure"
}
```

**Use this for:** Tracking update history, agent auditing, trend analysis

### 4. **RESOURCE_MONITORING.md** (Resource Monitoring)
Comprehensive guide to CPU, memory, disk, and network monitoring with recipes and tools.

### 5. **QUICK_COMMANDS.sh** (Copy-Paste One-Liners)
Quick reference with instant commands, watch patterns, and troubleshooting flows.

### 6. **README.md** (This File)
Index and navigation guide.

---

## 🚀 Quick Start

### For Humans
```bash
# Update everything
sudo pacman -Syu

# Check what will update
pacman -Qu

# Clean up old packages
sudo pacman -Sc
```

See `ARCH_UPDATE_GUIDE.md` for detailed explanations.

### For Agents
```bash
# Load the substrate library
source ~/reposoma/raw.guildes/archx/bash.substrates.sh

# Use reusable functions
substrate_system_info
substrate_check_updates
substrate_conditional_update
substrate_safe_cleanup_flow

# Get JSON report for logging
substrate_json_report
```

See `bash.substrates.sh` for all available functions.

---

## 📊 System Snapshot (2026-06-28)

| Property | Value |
|----------|-------|
| **Distro** | Manjaro Linux (Arch-based) |
| **Kernel** | 6.18.26-1-MANJARO |
| **Architecture** | x86_64 GNU/Linux |
| **Pacman** | 7.1.0 |
| **libalpm** | 16.0.1 |
| **Updates Available** | 0 (system current) |
| **Last Full Update** | 2026-06-28 |

---

## 📚 Command Reference

### Essential Commands

| Task | Command |
|------|---------|
| Full update | `sudo pacman -Syu` |
| Check updates | `pacman -Qu` |
| Search package | `pacman -Ss <name>` |
| Package info | `pacman -Si <name>` (remote) or `pacman -Qi <name>` (local) |
| Clean cache | `sudo pacman -Sc` |
| Remove orphans | `sudo pacman -Rns $(pacman -Qdtq)` |
| Fix lockfile | `sudo rm /var/lib/pacman/db.lck` |

### Flags Explained

- `-S` → Sync (download from repos)
- `-y` → Refresh database
- `-u` → Upgrade (install updates)
- `-c` → Clean (remove files)
- `-Q` → Query (list packages)
- `-R` → Remove (uninstall)
- `-s` → Search
- `-i` → Info (detailed info)
- `-d` → Dependencies (deps only)
- `-t` → Unrequired (orphans)
- `-q` → Quiet (minimal output)

---

## 🔧 Common Workflows

### Workflow 1: Safe Maintenance Cycle
```bash
# Check what needs doing
pacman -Qu              # See updates
pacman -Qdtq            # See orphans
du -sh /var/cache/pacman/pkg/  # See cache size

# Execute updates
sudo pacman -Syu

# Clean up
sudo pacman -Rns $(pacman -Qdtq)  # Remove orphans
sudo pacman -Sc         # Clean old packages
```

### Workflow 2: Automated Status Check
```bash
source ~/reposoma/raw.guildes/archx/bash.substrates.sh
substrate_json_report | jq '.'
```

### Workflow 3: Conditional Update (Only If Needed)
```bash
if [ $(pacman -Qu | wc -l) -gt 0 ]; then
  sudo pacman -Syu
else
  echo "System current"
fi
```

---

## ⚠️ Troubleshooting

### Update Hangs
```bash
# Try refreshing mirrors
sudo pacman-mirrors --fasttrack

# Or specify different country
sudo pacman-mirrors --country US
```

### Lockfile Error
```bash
# Remove stale lockfile
sudo rm /var/lib/pacman/db.lck
sudo pacman -Syu
```

### Dependency Conflict
```bash
# Let pacman resolve conflicts
sudo pacman -Syu --overwrite='*'  # Use cautiously
```

See `ARCH_UPDATE_GUIDE.md` § Troubleshooting for more.

---

## 📖 For Agent Learning

### Key Patterns Used in bash.substrates.sh

1. **Conditional Logic**
   ```bash
   if [ $(pacman -Qu | wc -l) -gt 0 ]; then
     # Do update
   fi
   ```

2. **Command Parsing**
   ```bash
   pacman -Qu | awk '{print $1}'  # Extract names
   pacman -Qu | wc -l              # Count results
   ```

3. **Error Handling**
   ```bash
   sudo pacman -Syu || return 1    # Stop on failure
   [ -f /path ] && rm /path        # Conditional removal
   ```

4. **JSON Reporting**
   ```bash
   cat <<EOF > report.json
   {"timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)", ...}
   EOF
   ```

5. **Composition**
   ```bash
   # Chain operations
   substrate_conditional_update && substrate_safe_cleanup_flow
   ```

---

## 📝 Extending This Guide

### Adding New Sessions
Append to `journal.uparchx.jsonl`:
```bash
echo '{"timestamp":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","action":"update","status":"completed"}' >> journal.uparchx.jsonl
```

### Adding New Substrates
Add functions to `bash.substrates.sh`:
```bash
substrate_my_function() {
  echo "[SUBSTRATE] Doing something..."
  # your code
  return $?
}
```

### Updating Documentation
- Quick fixes: Edit `ARCH_UPDATE_GUIDE.md`
- Major changes: Update this README and journal

---

## 📞 Reference

- **Arch Docs:** https://wiki.archlinux.org/title/Pacman
- **Manjaro Docs:** https://manjaro.org/support/
- **Status:** Check `/var/log/pacman.log` for detailed update history
- **Mirrors:** `pacman-mirrors --status` or `sudo pacman-mirrors --interactive`

---

## 🎯 Next Steps

1. **Review:** Read `ARCH_UPDATE_GUIDE.md` for complete reference
2. **Automate:** Source `bash.substrates.sh` and use in scripts
3. **Monitor:** Log updates to `journal.uparchx.jsonl` for trend analysis
4. **Extend:** Add custom substrates for your specific workflows

---

Generated by: Claude Code (Arch Update Session 2026-06-28)  
Status: Complete & Ready for Agent Learning
