# Office Machine Profile — wrapper

> **⚕ Cut on the surgical table.** This file is deployed from `~/ia-sync` (the surgical
> table — the like-composer syncing both machines). Do not edit it in place: cut in
> ia-sync, deploy outward. Before trusting any machine fact here, reality-check the sync
> part: `git -C ~/ia-sync log --oneline -5 -- zsh/guides/office.md` (intent) **and** repo↔live
> `rsync -n` (reality). Commits say what *should* be deployed; only the diff says what *is*.
**Machine:** hruzam-120922 (office) · `MACHINE_NAME=office`
**OS:** Manjaro Linux
**Last Updated:** 2026-07-15
**Authority:** @majkee

> **Synthesized state card:** `reposoma/raw.settings/raw.card.machine.office.md`
> Refresh: `half_life_days: 90` — caught by `harness-stale`.
> **Project paths:** `~/.config/zsh/ai/temple-project-map.zsh` (authoritative — Decision 0004 L4)
> **Logical project map:** `reposoma/registry/index.md`

---

## Hardware

| Component | Spec |
|-----------|------|
| CPU | 12th Gen Intel Core i5-12400 (6 cores / 12 threads) |
| RAM | 15 GiB total |
| Disk (root) | 197 GiB NVMe (`/dev/nvme0n1p2`), 42% used |
| Disk (home) | 259 GiB NVMe (`/dev/nvme0n1p4`), 14% used |
| Data disk | `/media/data/` — external/detachable; PSDVS, LTP, Larva, Session projects live here |

---

## PHP Environment

### Architecture — two FPMs, simultaneous, per-site routing

Both `php74-fpm` and `php-fpm` run at the same time. Valet routes each site to the correct FPM via its Unix socket.

```
php74-fpm service
  └── pool valet  →  ~/.valet/valet74.sock   (user=hruzam)
                     ↑ fantasyobchod.l, imagosk.l (per-site nginx hardcodes this socket)

php-fpm service (PHP 8.x)
  └── pool valet  →  ~/.valet/valet.sock     (user=hruzam)
                     ↑ freya.l, psdvs.l, ltp.l, all future Laravel (default Valet routing)
```

Pool configs:
- `/etc/php74/php-fpm.d/valet.conf` → `listen = ~/.valet/valet74.sock`
- `/etc/php/php-fpm.d/valet.conf`   → `listen = ~/.valet/valet.sock`

Both services must be **enabled on boot**:
```bash
sudo systemctl enable php74-fpm php-fpm
```

### PHP CLI binaries (office-specific)

```
/usr/bin/php74   ← PHP 7.4 CLI (AUR php74 package — includes CLI on office, unlike home)
/usr/bin/php     ← PHP 8.x CLI (system default)
/usr/bin/composer
```

```bash
alias composer74='/usr/bin/php74 /usr/bin/composer'   # defined in project-switcher.zsh
```

### Switching commands

Defined in `~/.config/zsh/system/office.php-switch.zsh`, sourced via `config.zsh`.

```bash
php74     # ensure php74-fpm is running → fantasyobchod.l, imagosk.l come alive
php8      # ensure php-fpm is running   → freya.l and all PHP 8.x sites come alive
phpst     # show both FPM statuses, socket state, live CLI versions
```

These commands only `systemctl start` — they never stop the other FPM, never touch enable state.
Run `phpst` after a reboot to start both if needed, or just let `fost` / `imst` trigger them.

### ⚠ Never call `valet use phpX`

`valet use php74` is broken on Arch (Valet expects `php7.4-fpm`; the package is `php74-fpm`).
Even when it partially runs, it calls `systemctl disable` on the other FPM — boot state is
damaged silently. The per-site nginx configs and FPM pools are already correct; `valet use`
adds nothing and can break things.

If Valet state was corrupted by a `valet use` call:
```bash
sudo systemctl enable php74-fpm php-fpm   # restore enable state
echo "8" > ~/.valet/use_php_version       # reset Valet's stored version to PHP 8
```

---

## Valet Setup

### Config

```json
{
  "domain": "l",
  "paths": ["/home/hruzam/.valet/Sites", "/home/hruzam/www"],
  "port": "80"
}
```

`~/.valet/Sites/` takes priority and is where `valet link` creates named symlinks.
`~/www` is a fallback scan (one level deep). All active projects should be linked explicitly.

### Linking projects

```bash
cd ~/www/imago_cz/fantasyobchod && valet link fantasyobchod
cd ~/www/imago_cz/freya         && valet link freya
# imagosk: cd <imagosk-path>    && valet link imagosk
# any new project: cd <path>    && valet link <sitename>
```

Each `valet link <name>` creates `~/.valet/Sites/<name>` → project directory.
Valet's server.php finds the docroot via that symlink.

### Per-site nginx overrides (PHP 7.4 sites only)

PHP 7.4 sites need an explicit nginx config in `~/.valet/Nginx/` to route to `valet74.sock`.
PHP 8.x sites use Valet's default routing — no override needed.

| Site | File | Socket |
|------|------|--------|
| fantasyobchod.l | `~/.valet/Nginx/fantasyobchod` | `valet74.sock` |
| imagosk.l | `~/.valet/Nginx/imagosk` | `valet74.sock` |

To add a new PHP 7.4 site (rare — legacy only):
```bash
cp ~/.valet/Nginx/fantasyobchod ~/.valet/Nginx/<newsite>
# edit server_name line in the new file
sudo systemctl reload nginx
```

### Adding a new PHP 8.x project (standard workflow)

```bash
cd <project-directory>
valet link <sitename>
# done — site available at http://<sitename>.l
```

No PHP config, no nginx file, no socket wiring. Default Valet routing handles everything.

---

## Services

| Service | Status | Notes |
|---------|--------|-------|
| nginx | ✅ active | Managed by Valet |
| php74-fpm | ✅ active | PHP 7.4 — fantasyobchod.l, imagosk.l |
| php-fpm (8.x) | ✅ active | PHP 8.x — freya.l + all others |
| mariadb | ✅ active | |
| tailscaled | ✅ active | VPN |
| docker | ✅ active | Available; not needed for PHP on office (unlike home) |

Both FPM services enabled on boot. Nginx managed by Valet (do not edit `/etc/nginx/` manually).

---

## Project Paths

> **Do not maintain a path table here — paths live in one place only (Decision 0004 L4).**
>
> Authoritative cascade (same as Eagle's resolution order):
> 1. Physical paths → `~/.config/zsh/ai/temple-project-map.zsh`
> 2. Logical map + status → `reposoma/registry/index.md`
> 3. Per-project detail → `reposoma/registry/<project>.md` (beacon)
>
> This guide owns machine-specific context only: PHP setup, Valet routing, services.
> For which projects exist and where they live, follow the cascade above.

---

## Composer Usage

```bash
# FantasyObchod (PHP 7.4)
cd ~/www/imago_cz/fantasyobchod
composer74 install        # /usr/bin/php74 /usr/bin/composer

# Laravel projects (PHP 8)
cd ~/www/imago_cz/freya
composer install          # system composer (PHP 8.x)

# Version check
composer74 --version
composer --version
```

---

## Monitoring

archx commands (`sysmon`, `cputop`, `memtop` etc.) are available — sourced via
`~/.config/zsh/archx/commands.zsh` in `config.zsh`. For memory-pressure tools
(earlyoom, ramwatch, ramguard) see home machine only: `guides/resource-control.md`.

---

## Quick Diagnostics

```bash
# PHP status (FPM services + sockets + live CLI versions)
phpst

# Site reachable?
curl -I http://fantasyobchod.l
curl -I http://freya.l

# Valet links
valet links

# Nginx config test
sudo nginx -t
```

---

## Home vs Office: Key Differences

| Aspect | Home | Office |
|--------|------|--------|
| Web server | nginx (manual, systemctl) | Valet (manages nginx) |
| PHP 7.4 CLI | Docker (`docker run php74-composer`) | Native (`/usr/bin/php74`) |
| composer74 | Docker-wrapped | Direct binary call |
| PHP switching | systemctl only | systemctl only (both FPMs simultaneous) |
| Projects (FO/Freya) | `~/www/imago_cz/{fantasyobchod,freya}` | `~/www/imago_cz/{fantasyobchod,freya}` |
| Projects (PSDVS/LTP/Larva) | `~/www/` | `/media/data/projects/` |
| Docker purpose | PHP 7.4 CLI (needed) | Available but not needed for PHP |
