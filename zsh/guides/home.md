# Home Machine Capabilities & Configuration

> **⚕ Cut on the surgical table.** This file is deployed from `~/ia-sync` (the surgical
> table — the like-composer syncing both machines). Do not edit it in place: cut in
> ia-sync, deploy outward. Before trusting any machine fact here, reality-check the sync
> part: `git -C ~/ia-sync log --oneline -5 -- zsh/guides/home.md` (intent) **and** repo↔live
> `rsync -n` (reality). Commits say what *should* be deployed; only the diff says what *is*.

**Location:** `~/.config/zsh/guides/home.md`  
**Machine:** Manjaro (Arch-based)  
**Generated:** 2026-06-28  
**Last Updated:** 2026-06-28

> ## ⚠ STALE — read with suspicion (flagged 2026-07-29)
>
> This guide predates the **machine-convergence work** (operator, ~2026-05): office was
> reframed to use the same partition layout and the same `~/` home-folder placement as home,
> deliberately, to make the two machines as similar as possible. **Every "home vs office
> difference" claim below is therefore suspect** — most describe a divergence that has since
> been closed, and the doc has not been re-derived.
>
> Two concrete errors already corrected in place (search ⚠ in this file). Assume more remain.
>
> What is still true and where to check instead:
> - **PHP / composer** — a real, current difference. Authoritative split table:
>   `~/.config/zsh/AGENTS.md` §"The PHP / composer machine split".
> - **Project paths** — `ai/temple-project-map.zsh` is the only place physical paths live.
> - **Machine identity / project vars** — office declares them inline in `config.zsh`.
>   The `harness.machine-project-registry.json` mechanism is retired on office and being
>   retired on home; anything in this guide citing it as the source is out of date.
>
> Do not re-derive this guide from office. Home owns it, and it should be regenerated on
> home once the registry migration lands.

---

## 🖥️ Hardware Specifications

### CPU & Memory
```
Processor:    AMD Ryzen 5 3500U with Radeon Vega Mobile Gfx
Cores:        8 (logical cores available)
Memory:       9.6 GB RAM
Swap:         Not configured (0 GB)
Architecture: x86_64
```

### Storage
```
Root (/):     192 GB (22% used, 143 GB free)
Home (/home): 128 GB (29% used, 87 GB free)
Boot:         256 MB (13% used, 226 MB free)
```

### Network
```
Connection:   Ethernet (192.168.0.6)
IP Version:   IPv4 + IPv6 (fe80::46d2:36d5:40f5:b09d)
```

---

## 📦 Installed Services & Tools

### System Level

| Tool | Installed | Status | Purpose |
|------|-----------|--------|---------|
| **Docker** | ❓ Check | - | Container runtime |
| **PHP 7.4** | ❓ Check | - | Legacy PHP (composer74) |
| **PHP 8.x** | ❓ Check | - | Modern PHP (composer8) |
| **Composer** | ✅ Yes | System | PHP dependency manager |
| **MariaDB** | ✅ Yes | Running | MySQL-compatible DB |
| **nginx** | ❓ Check | - | Web server |
| **Tailscale** | ✅ Yes | Running | VPN tunnel |

### Monitoring Tools

| Tool | Status | Purpose |
|------|--------|---------|
| `top` | ✅ Yes | Basic system monitor |
| `htop` | ✅ Yes | Enhanced process monitor |
| `vmstat` | ✅ Yes | Virtual memory stats |
| `free` | ✅ Yes | Memory breakdown |
| `watch` | ✅ Yes | Repeat commands |
| `ss` | ✅ Yes | Network connections |
| `lsof` | ✅ Yes | Open files/ports |
| `fuser` | ✅ Yes | Process finder |
| `df`/`du` | ✅ Yes | Disk usage |

---

## 🐳 Docker Setup

### Current Status
```bash
# Check if installed
which docker

# Check if running
systemctl is-active docker

# Check if user in group
groups | grep docker
```

### Configuration (if needed)
```bash
# Install
sudo pacman -S docker

# Enable and start
sudo systemctl enable --now docker

# Add user to group
sudo usermod -aG docker $USER
# Then logout/login for group to take effect
```

### Project-Specific Images
Your projects may require custom Docker images:
- `php74-composer` — For FantasyObchod (PHP 7.4)
- `php8-composer` — For modern projects

Check `~/.docker/php74-composer/` and `~/.docker/php8-composer/` for Dockerfiles.

---

## 🐘 PHP & Composer

### Available Versions

#### Home Setup (uses Docker)
```bash
composer74 <args>    # FantasyObchod via Docker
composer8 <args>     # Modern projects via Docker
```

#### Configuration
- **Composer Home:** `~/.composer/`
- **Composer Cache:** `~/.composer/cache/`
- **System Composer:** `/usr/bin/composer`

### Project PHP Requirements

| Project | PHP Version | Framework | Toolkit |
|---------|------------|-----------|---------|
| FantasyObchod (FO) | 7.4 | Custom | `fo-toolkit.zsh` |
| Imago/Freya (IM) | 8.x | Custom | `im-toolkit.zsh` |
| PSDVS | 8.x | Laravel | `psdvs-toolkit.zsh` |
| Laravel Training (LTP) | 8.x | Laravel | `ltp-toolkit.zsh` |

---

## 🗄️ Database (MariaDB)

### Current Status
```bash
# Check if running
systemctl is-active mariadb

# Start if needed
sudo systemctl start mariadb

# Check version
mariadb --version
```

### Default Credentials
```
User:     majkee
Database: fantasyobchod (for FO project)
```

### Privileges
`majkee`@`localhost` does NOT have `CREATE DATABASE` by default — run as root to grant it:

```sql
-- connect as root: sudo mysql -u root
GRANT CREATE ON *.* TO 'majkee'@'localhost';
FLUSH PRIVILEGES;
```

After this, `majkee` can `CREATE DATABASE` without root each time.

### Project Databases
See `~/.config/zsh/harness.machine-project-registry.json` for DB details per project.

### Backup Location
```
ENV_BACKUP_DIR: ~/www/PSDVS/env
```

---

## 🌐 nginx Connector

### Status
```bash
# Check if installed
which nginx

# Check if running
systemctl is-active nginx

# View config
cat /etc/nginx/nginx.conf
```

### Common Tasks

#### Start nginx
```bash
sudo systemctl start nginx
```

#### View access logs
```bash
sudo tail -f /var/log/nginx/access.log
```

#### View error logs
```bash
sudo tail -f /var/log/nginx/error.log
```

#### Test config
```bash
sudo nginx -t
```

#### Reload config
```bash
sudo systemctl reload nginx
```

---

## 🐍 Python Environment

### System Python
```bash
python3 --version      # Should be 3.x
pip3 --version         # Package manager
```

### Project Usage
- **normalizer.py** — `~/.config/zsh/normalizer.py` (config loader)
- **Cloud SDKs** — Google Cloud SDK uses Python

### Common Tasks
```bash
# List installed packages
pip3 list

# Install package
pip3 install <package>

# Create virtual environment
python3 -m venv ~/project-venv
source ~/project-venv/bin/activate
```

---

## 🔌 Tailscale VPN

### Current Status
```bash
# Check if running
systemctl is-active tailscaled

# View status
tailscale status

# Get IP address
tailscale ip -4
```

### Configuration
- **Service:** `tailscaled`
- **Socket:** `/run/tailscale/tailscaled.sock`
- **State:** `/var/lib/tailscale/tailscaled.state`
- **Port:** 41641 (UDP)

### Common Tasks
```bash
# Connect/login
sudo tailscale up

# Disconnect
sudo tailscale down

# View connected devices
tailscale peers
```

---

## 📁 Project Directory Structure

### Standard Paths
```
~/www/                          # Main project directory
├── fantasyobchod/             # FO project
├── freya/                      # IM (Imago) project
├── PSDVS/                      # PSDVS project
├── Laravel-training-project/   # LTP project
└── larva/                      # Larva orchestrator
```

### Configuration Mappings
See `~/.config/zsh/harness.machine-project-registry.json` for exact paths and per-project settings.

### Environment Backups
```
~/www/PSDVS/env/               # PSDVS environment backups
```

---

## 🛠️ Available Toolkits

### Loaded Automatically
Each project has a toolkit (sourced via `project-switcher.zsh`):

| Project | Toolkit File | Purpose |
|---------|--------------|---------|
| FO | `fo-toolkit.zsh` | FantasyObchod-specific commands |
| IM | `im-toolkit.zsh` | Imago/Freya-specific commands |
| PSD | `psdvs-toolkit.zsh` | PSDVS-specific commands |
| LTP | `ltp-toolkit.zsh` | Laravel Training-specific commands |
| LRV | `larva.zsh` | Larva orchestrator |
| SES | `session-helpers.zsh` | Session management |

### Switching Projects
```bash
# Via registry (if configured)
# Usage depends on project-switcher.zsh implementation
```

---

## 📊 System Monitoring

### Quick Commands
```bash
# Overall status
sysmon              # Full system overview
syscheck            # Quick check
alert               # Alert if thresholds exceeded

# CPU
cputop              # Top processes
cpuwatch            # Live monitoring
cpuload             # Load vs cores

# Memory
memtop              # Top processes
memwatch            # Live monitoring
meminfo             # Detailed breakdown

# Disk
diskuse             # Usage overview
disktop             # Top directories
diskwatch           # Live monitoring

# Troubleshooting
troubleshoot        # Full troubleshooting report
```

### Monitoring Guide
Full details in `~/reposoma/raw.guildes/archx/RESOURCE_MONITORING.md`

---

## 🔧 Configuration Management

### ia-sync Repository
Location: `~/ia-sync/`

This repo syncs:
- `~/.claude/` — Claude Code settings, skills, agents
- `~/.gemini/` — Gemini API settings
- `~/.config/zsh/` — Shell configuration

### Backup/Restore Workflow
```bash
# Backup to repo
cd ~/ia-sync
bash sync.sh
git add -A && git commit -m "sync: $(date +%Y-%m-%d)"
git push

# Restore on new machine
bash deploy.sh
```

---

## 🎯 Machine-Specific Notes

### Home vs Office
This is the **home** machine (`MACHINE_NAME=home`).

Machine differences (⚠ corrected 2026-07-29 — this section previously cited
`harness.machine-project-registry.json` as the source; that mechanism is retired on office
and being retired on home. Office declares these as inline exports in `config.zsh`):
- **Editors:** Sublime Text (home) vs Code (office)
- **Project Paths:** `~/www/` (home) vs ~~`/media/data/projects/`~~ → **`~/projects/`** (office).
  `/media/data/projects` was declared an empty unmounted husk 2026-07-07 and repointed;
  the old value here was stale. Authoritative map: `ai/temple-project-map.zsh`.
- **PHP Binaries:** Docker-based (home) vs native, both versions concurrent (office).
  See the split table in `~/.config/zsh/AGENTS.md` — office runs `php74-fpm` and `php-fpm`
  simultaneously with nginx socket routing; home invokes a container per composer call.

### Registry Files
- **Machine Registry:** `~/.config/zsh/harness.machine-project-registry.json`
- **AI Agents Registry:** `~/.config/zsh/ai-agents.registry.json`

---

## 📝 Updating This Guide

### When to Update
- New services installed
- PHP/Docker setup changes
- Database schema changes
- New projects added
- Configuration structure changes

### How to Update
1. Edit this file
2. Run tests/verification
3. Commit to ia-sync repo
4. Update deployment notes

---

## 🚀 Quick Start by Role

### Web Developer
```bash
# Start your project
project-switch FO  # or IM, PSD, LTP

# Check status
sysmon
troubleshoot

# Monitor during work
cpuwatch &
memwatch &
```

### DevOps / System Admin
```bash
# Check infrastructure
sysmon
pacupdate
pacclean

# Monitor services
systemctl status mariadb
systemctl status docker
systemctl status tailscale

# View logs
sudo tail -f /var/log/nginx/access.log
```

### Database Admin
```bash
# Connect to database
mysql -u majkee fantasyobchod

# Check status
systemctl is-active mariadb

# Backup/restore
mysqldump -u majkee fantasyobchod > backup.sql
```

---

## 📞 Getting Help

### Documentation
- **Monitoring:** `~/reposoma/raw.guildes/archx/`
- **Project Toolkits:** `~/.config/zsh/projects/`
- **Configuration:** `~/.config/zsh/harness.machine-project-registry.json`

### Commands
```bash
archx-help          # Monitoring commands
show-guide          # Quick reference
show-index          # Complete index
show-monitoring-guide # Detailed monitoring
```

### System Info
```bash
uname -a            # System info
lscpu               # CPU details
free -h             # Memory details
df -h               # Disk details
```

---

**Status:** ✅ Ready to use  
**Last Verified:** 2026-06-28  
**Machine:** Home workstation (Manjaro)
