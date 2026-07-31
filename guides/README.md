# Guides & Reference Documentation

Team-shared and machine-specific guides for ia-sync environments.

---

## 📂 Directory Structure

### `home-setup/` — Home Machine Documentation

Comprehensive guides for @home machine (Manjaro, Docker-based PHP 7.4, nginx + PHP-FPM).

**Core references (start here):**
- **NEW_COMP_Quick_Start.md** — Critical guide explaining Docker vs PHP-FPM distinction
  - Two separate PHP 7.4 environments (composer in Docker, runtime on FPM)
  - Extension installation matrix
  - Common errors + quick fixes
  - For @Cursor/@Vega agents
  
- **nginx_Setup_Manual_@home.md** — Complete nginx configuration for OpenCart + Laravel
  - Multi-PHP site setup
  - Socket configuration
  - Performance tuning
  
- **OpenCart_Home_Setup_Complete_Guide.md** — Full FantasyObchod (OpenCart) setup
  - Project structure
  - Module architecture
  - Custom functionality

**Supplementary:**
- **machine.resource-control.home.md** — Memory defense (zswap, earlyoom, ramguard)
- **nginx_setup_guide.md** — Multi-PHP environment setup context
- **diagnose_opencart_404.md** — Troubleshooting guide for 404 errors
- **PHP_Extension_Verification.md** — Extension checklist & installation

### `cross-machine/` — Team Reference Guides

Tool references and utilities useful on both home and office machines.

- **Repomix_Reference_Guide.md** — Using Repomix for codebase documentation
- **Terminal_Search_Reference_Guide.md** — Search patterns & utilities
- **Tree_File_Listing_Reference_Guide.md** — Directory tree reference

---

## 🎯 Usage

### For Home Machine Setup
1. Start with `NEW_COMP_Quick_Start.md` (critical Docker vs FPM explanation)
2. Reference `nginx_Setup_Manual_@home.md` for web server config
3. Use `OpenCart_Home_Setup_Complete_Guide.md` for project-specific details
4. Check `machine.resource-control.home.md` for memory management

### For Office Machine
- See `OFFICE_MACHINE_SETUP.md` in repo root for deployment instructions
- Office machine uses Valet (not nginx), so guides above are home-specific reference only

### For Team/Cross-Machine
- Reference `cross-machine/` guides for tool-specific information
- Applicable to both home and office machines

---

## 📋 Guide Matrix

| Guide | Audience | Machine | Updated | Status |
|-------|----------|---------|---------|--------|
| NEW_COMP_Quick_Start.md | Agents (@Cursor/@Vega) | @home | 2026-03 | ✅ Current |
| nginx_Setup_Manual_@home.md | Developers | @home | 2026-03 | ✅ Active |
| OpenCart_Home_Setup_Complete_Guide.md | Developers | @home | 2026-03 | ✅ Reference |
| machine.resource-control.home.md | System admin | @home | 2026-05 | ✅ Active |
| nginx_setup_guide.md | Developers | @home | 2026-02 | ✅ Supplementary |
| diagnose_opencart_404.md | Developers | @home | 2026-03 | ✅ Troubleshooting |
| PHP_Extension_Verification.md | Developers | @home | 2026-03 | ✅ Reference |
| Repomix_Reference_Guide.md | Team | Cross-machine | 2026-03 | ✅ Tool reference |
| Terminal_Search_Reference_Guide.md | Team | Cross-machine | 2026-03 | ✅ Tool reference |
| Tree_File_Listing_Reference_Guide.md | Team | Cross-machine | 2026-03 | ✅ Tool reference |

---

## 🔄 Maintenance

**Adding new guides:**
1. If home-specific → place in `home-setup/`
2. If cross-machine → place in `cross-machine/`
3. Update this README with entry in guide matrix
4. Commit to ia-sync

**Archiving old guides:**
- Move to `ia-sync/zsh/archive/` with date suffix
- Update links in this README to point to archive

---

## 📌 Notes

- Guides are synced via `ia-sync/sync.sh` → `~/.config/zsh/guides/` on both machines
- HOME machine has additional local guides in `~/.config/zsh/guides/` (home.md, services.md, resource-control.md)
- OFFICE machine gets office.md created during deployment
- Journal (`journal.host-cleanup.md`) tracks audit findings and machine-specific discoveries

---

**Last Updated:** 2026-06-29  
**Maintained by:** @majkee  
**Version:** 1.0
