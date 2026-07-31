# Machine Resource Control — @home

**Location:** `~/.config/zsh/guides/resource-control.md`  
**Status:** Active  
**Since:** 2026-05-18  
**Machine:** home (Manjaro KDE Plasma, Ryzen 5 3500U, 9.6GB RAM)  
**Authority:** @majkee

---

## Problem This Solves

9.6 GB RAM with no swap by default. Firefox + Cursor + VS Code (all heavy Electron apps) can exhaust available memory. Without swap, the kernel stalls trying to reclaim pages — the system freezes instead of degrading gracefully.

This setup prevents that through a 5-layer defense system.

---

## Layer 1 — Kernel: zswap (Compressed RAM Swap)

Compressed in-memory swap. No disk wear, ~2× effective RAM headroom under pressure.

### Install (One-Time, Requires Reboot)

```bash
sudo sed -i 's/quiet splash/quiet splash zswap.enabled=1 zswap.compressor=lz4 zswap.max_pool_percent=20/' /etc/default/grub
sudo grub-mkconfig -o /boot/grub/grub.cfg
# Reboot your system
```

### Verify After Reboot

```bash
cat /sys/module/zswap/parameters/enabled
# Should print: Y
```

### How It Works
- Compresses pages in RAM when memory pressure occurs
- Uses LZ4 compression (fast, decent ratio)
- Max 20% of RAM (1.9 GB on your system)
- Transparent — apps don't notice

---

## Layer 2 — OOM Prevention: earlyoom

Kills the heaviest suspect process at 15% free RAM — **before** the kernel freezes trying to decide.

### Install

```bash
sudo pacman -S earlyoom
```

### Configure

**File:** `/etc/default/earlyoom`

```ini
EARLYOOM_ARGS="-r 60 -m 15 -s 0 --avoid '(plasmashell|kwin_wayland|Xwayland|sddm)' --prefer '(firefox|cursor|code)'"
```

**Parameters:**
- `-m 15` — Trigger at 15% free RAM (increase for more tolerance, decrease for earlier action)
- `--prefer` — Kill these apps first if memory is critical
- `--avoid` — Never kill these (desktop shell, window manager, login screen)
- `-r 60` — Check every 60 seconds

### Enable

```bash
sudo systemctl enable --now earlyoom
sudo systemctl status earlyoom
```

### Customization

**If you want more aggressive killing:**
```bash
# Edit to -m 10 (trigger at 10% free RAM)
sudo nano /etc/default/earlyoom
```

**If you want to protect different apps:**
```bash
# Example: protect Sublime Text too
EARLYOOM_ARGS="-r 60 -m 15 -s 0 --avoid '(plasmashell|kwin_wayland|Xwayland|sddm|sublime)' --prefer '(firefox|cursor|code)'"
```

---

## Layer 3 — Agent Tooling: ramguard MCP Server

A local MCP server exposing RAM tools to Claude Code agents.

### Location
```
~/.claude/mcp/ramguard/server.py
~/.claude/mcp/ramguard/config.json
```

### Configuration

**File:** `~/.claude/mcp/ramguard/config.json`

```json
{
  "threshold_warn_percent": 15,
  "suspects": ["firefox", "cursor", "code"],
  "protected": ["plasmashell", "kwin_wayland", "Xwayland", "sddm"]
}
```

### Installation (One-Time)

```bash
# Install Python dependencies
pip3 install --user --break-system-packages mcp psutil

# Register with Claude Code
claude mcp add ramguard python3 ~/.claude/mcp/ramguard/server.py

# Verify
claude mcp list | grep ramguard
```

### Available Tools

**In Claude Code agents, you can now use:**

```bash
# Get full RAM status + top 10 consumers
ram_status

# Get freeze-suspect apps only (firefox, cursor, code)
freeze_suspects

# Kill a process (with protected-process guard)
kill_process(pid=1234, confirm=True)
```

### When It's Useful

Agents can now:
- Check RAM before starting intensive operations
- Monitor memory during long-running tasks
- Kill non-critical apps automatically if memory drops below threshold
- Alert you via Claude Code if system is under memory pressure

---

## Layer 4 — CLI Tool: ramwatch

Human-facing script. Source of truth: `~/bin/ramwatch` (backed up via ia-sync).

### Usage

```bash
# Full report with top 10 memory consumers
ramwatch

# Show only freeze-suspect apps (firefox, cursor, code)
ramwatch --suspects

# Interactively kill a process
ramwatch --kill 1234
```

### What It Shows

```
RAM Status: 3.2 GB / 9.6 GB (33%)
Free: 6.4 GB
Swap: 0 B / 0 B

Top Memory Consumers:
  1. firefox         450 MB
  2. cursor          380 MB
  3. code            290 MB
  4. plasmashell     420 MB
  5. kwin_wayland    130 MB
```

---

## Layer 5 — KDE Login: Numlock Autostart

Activates Num Lock at KDE session start (minor, but nice-to-have).

### Configuration

**File:** `~/.config/autostart/numlockx.desktop`

Activates Num Lock at KDE session start. No reboot needed — active on next login.

### SDDM Login Screen (Optional)

**Requires sudo, one-time setup:**

```bash
echo -e '\n[General]\nNumlock=on' | sudo tee -a /etc/sddm.conf.d/kde_settings.conf
```

---

## 🎯 Monitoring & Tuning

### Check Current State

```bash
# Memory usage
free -h

# zswap status
cat /sys/module/zswap/parameters/enabled
cat /sys/module/zswap/parameters/compressor

# earlyoom running
systemctl is-active earlyoom

# Top memory apps
ps aux --sort=-%mem | head -10
```

### Tuning Reference

| What to Change | Where |
|---|---|
| earlyoom trigger threshold | `/etc/default/earlyoom` → `-m <percent>` |
| ramguard warn threshold | `~/.claude/mcp/ramguard/config.json` → `threshold_warn_percent` |
| ramguard suspects/protected | same config.json |
| zswap pool size | `/etc/default/grub` → `zswap.max_pool_percent=<n>` |
| zswap compression | `/etc/default/grub` → `zswap.compressor=` |

### Example: More Aggressive Configuration

If your system freezes often:

```bash
# 1. Lower earlyoom trigger
sudo nano /etc/default/earlyoom
# Change -m 15 to -m 10

# 2. Increase zswap pool
sudo sed -i 's/zswap.max_pool_percent=20/zswap.max_pool_percent=30/' /etc/default/grub
sudo grub-mkconfig -o /boot/grub/grub.cfg
# Reboot

# 3. Restart earlyoom
sudo systemctl restart earlyoom
```

---

## 📊 Backup & Restore

All tools are backed up via ia-sync:

- `~/.claude/mcp/ramguard/` — MCP server
- `~/bin/ramwatch` — CLI tool
- `/etc/default/earlyoom` — earlyoom config

### When Restoring to New Machine

```bash
# 1. Sync ia-sync
bash ~/ia-sync/deploy.sh

# 2. Install earlyoom
sudo pacman -S earlyoom

# 3. Reinstall Python deps
pip3 install --user --break-system-packages mcp psutil

# 4. Register ramguard
claude mcp add ramguard python3 ~/.claude/mcp/ramguard/server.py

# 5. Enable earlyoom
sudo systemctl enable --now earlyoom

# 6. Reboot to activate zswap (if not already configured)
```

---

## ⚠️ Warning Signs

**If you see these, your memory is under pressure:**

- Apps taking seconds to respond
- Disk thrashing (loud disk, slow everything)
- System freezing for 10+ seconds
- earlyoom killing processes

### Response Checklist

1. Run `ramwatch` to see what's using memory
2. Close unnecessary apps (Firefox, Cursor, VS Code)
3. Check for memory leaks: `ps aux --sort=-%mem | head -10`
4. If problem persists, consider:
   - Lowering earlyoom threshold: `sudo nano /etc/default/earlyoom`
   - Increasing zswap pool: `/etc/default/grub`
   - Reboot to clear memory

---

## 🔍 Verification Checklist

After setup:

```bash
# 1. zswap enabled
cat /sys/module/zswap/parameters/enabled
# Should output: Y

# 2. earlyoom running
systemctl is-active earlyoom
# Should output: active

# 3. ramwatch available
~/bin/ramwatch --version
# Or just run: ramwatch

# 4. ramguard registered
claude mcp list | grep ramguard
# Should show: ramguard (available)
```

---

## 📚 Reference

### Files Involved

```
/etc/default/grub                    ← zswap kernel parameters
/etc/default/earlyoom                ← earlyoom config
~/.claude/mcp/ramguard/              ← MCP server
~/bin/ramwatch                       ← CLI tool
~/.config/autostart/numlockx.desktop ← Num Lock autostart
```

### Logs & Debugging

```bash
# earlyoom activity
journalctl -u earlyoom -n 50
sudo grep -i earlyoom /var/log/syslog

# zswap stats
cat /sys/module/zswap/parameters/*

# System memory pressure
watch -n 1 'free -h && echo && ps aux --sort=-%mem | head -5'
```

---

## 🎓 How It All Works Together

```
Heavy Memory Load (Firefox + Code + Cursor)
    ↓
Layer 1: zswap compresses pages in RAM
    ↓
RAM pressure increases (15% free)
    ↓
Layer 2: earlyoom detects, kills least critical app (e.g., Firefox)
    ↓
System continues working smoothly
    ↓
Layer 3: Claude agents monitor via ramguard MCP
    ↓
Layer 4: You check status with ramwatch CLI
    ↓
No freeze, no kernel lockup, graceful degradation ✅
```

---

**Status:** ✅ Complete & Ready  
**Last Updated:** 2026-06-29  
**Next Review:** When adding memory-intensive projects or tools
