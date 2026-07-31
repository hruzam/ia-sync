# Arch Linux Update Guide

> This guide documents the update process for Arch/Manjaro systems. Generated from live session: 2026-06-28

## Quick Start

### Full System Update (Recommended)
```bash
sudo pacman -Syu
```

**What it does:**
- `-S` = Sync (download from repositories)
- `-y` = Refresh package database
- `-u` = Upgrade (apply available updates)

Combined `-Syu` performs a complete system update in one command.

---

## Command Variants

### Refresh Repos Without Installing
```bash
sudo pacman -Sy
```
Updates the local package database from repositories. Useful before checking what's available.

### Check Available Updates (Non-Root)
```bash
pacman -Qu
```
Shows packages with available updates without needing sudo. Helpful for preview before committing.

### Update Specific Package
```bash
sudo pacman -S package-name
```
Installs or updates a single package.

### Force Update (Advanced)
```bash
sudo pacman -Syyu
```
Use if `-Syu` fails. Downgrades if needed (rarely necessary on Arch).

---

## Pre-Update Checklist

1. **Backup important configs:**
   ```bash
   sudo pacman -Qu | wc -l  # See count of updates
   ```

2. **Check disk space:**
   ```bash
   df -h /var/cache/pacman/pkg/
   ```

3. **Review what will update:**
   ```bash
   pacman -Sup  # Shows full transaction (requires sudo)
   ```

---

## Post-Update Tasks

### Verify Update Success
```bash
pacman -V                    # Check pacman version
uname -a                     # Check kernel
pacman -Qu | wc -l          # Should be 0 if all updated
```

### Clean Old Package Cache (Optional)
```bash
sudo pacman -Sc             # Remove unneeded packages
sudo pacman -Scc            # Remove ALL old packages (aggressive)
```

### Check for Orphaned Packages
```bash
pacman -Qdt
```
Lists packages no longer required by anything. Remove with:
```bash
sudo pacman -Rns $(pacman -Qdtq)
```

---

## System Information Reference

### Latest Verified State (2026-06-28)
| Property | Value |
|----------|-------|
| OS | Manjaro Linux (Arch-based) |
| Kernel | 6.18.26-1-MANJARO |
| Architecture | x86_64 |
| Pacman | 7.1.0 |
| libalpm | 16.0.1 |
| Update Status | Current (no pending updates) |

---

## Useful Pacman Aliases

Add to `~/.bashrc` or `~/.zshrc`:

```bash
alias pacupd='sudo pacman -Syu'          # Quick update
alias pacclean='sudo pacman -Sc'         # Clean cache
alias pacinfo='pacman -Qu | wc -l'       # Count updates
alias pacorphan='pacman -Qdt'            # Show orphans
alias pacremove='sudo pacman -Rns'       # Remove package + deps
```

Then reload shell:
```bash
source ~/.zshrc  # or ~/.bashrc
```

---

## Troubleshooting

### Update Hangs/Takes Long Time
- Check internet connection
- Verify mirror status: `sudo pacman-mirrors --fasttrack`
- Try different mirror: `sudo pacman-mirrors --country US`

### Pacman Lockfile Error
```
error: could not lock database: File exists
```
**Solution:**
```bash
sudo rm /var/lib/pacman/db.lck
sudo pacman -Syu
```

### Dependency Conflict
- Let pacman resolve: `sudo pacman -Syu --overwrite='*'` (use cautiously)
- Or check which packages conflict: `pacman -Qu`

### Downgrade Package
```bash
sudo pacman -U /var/cache/pacman/pkg/package-name-oldversion.tar.zst
```

---

## For Agent Learning: Key Bash Patterns

### Count operations
```bash
pacman -Qu | wc -l                      # Count updates
pacman -Qdtq | wc -l                    # Count orphans
```

### Filter/Parse pacman output
```bash
pacman -Qu | awk '{print $1}'           # Just package names
pacman -Qu | grep -i "kernel\|linux"    # Find specific updates
```

### Conditional logic
```bash
# Only update if updates exist
if [ $(pacman -Qu | wc -l) -gt 0 ]; then
  sudo pacman -Syu
else
  echo "System is current"
fi
```

### Batch operations
```bash
# Remove all orphaned packages
sudo pacman -Rns $(pacman -Qdtq)

# Update all AUR helpers (if using yay/paru)
yay -Syu --noconfirm
```

---

## Update Frequency

**Recommended:** Weekly or before critical work

**Note:** Arch follows a rolling-release model. Updates are continuous and relatively safe, but always backup critical configs before major updates.

---

Generated: 2026-06-28
Status: System fully updated, no pending updates
