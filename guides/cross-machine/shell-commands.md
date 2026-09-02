# Shell Command Reference — Office Setup
# ia-sync / guides / cross-machine / shell-commands.md
# Both machines can read this. Office-only commands are marked [OFFICE].

---

## PHP SWITCHING [OFFICE]

Requires sudoers: `sudo cp ~/.config/zsh/guides/sudoers.valet-php.conf /etc/sudoers.d/valet-php`

| Command  | What it does |
|----------|-------------|
| `php74`  | Start php74-fpm (Valet routes fantasyobchod.l → valet74.sock) |
| `php8`   | Start php-fpm (all other Valet sites) |
| `phpst`  | Show FPM service status + socket state |

FPM services: `php74-fpm` (PHP 7.4) and `php-fpm` (PHP 8.x) can both run simultaneously.
fantasyobchod.l is permanently routed to PHP 7.4 via `~/.valet/Nginx/fantasyobchod` — no switching needed.

---

## DEV SESSION LAUNCHERS [OFFICE]

| Command      | What it does |
|--------------|-------------|
| `imst`       | PHP 8 on + cd freya + open editor. URL: http://freya.l |
| `imoctane`   | `php artisan octane:start --server=roadrunner --watch &` |
| `fost`       | PHP 7.4 on + cd fantasyobchod + open editor. URL: http://fantasyobchod.l |

Freya path: `~/www/imago_cz/freya/`
FO path:    `~/www/imago_cz/fantasyobchod/`

---

## PROJECT SWITCHER

| Command           | What it does |
|-------------------|-------------|
| `fo`              | cd to FantasyObchod + load fo-toolkit |
| `im`              | cd to Freya/Imago + load im-toolkit |
| `fo -h`           | fo-toolkit help |
| `im -h`           | im-toolkit help |
| `project_help`    | List all projects + PHP versions |

---

## LARAVEL SHORTCUTS (global, from any directory)

| Command    | What it does |
|------------|-------------|
| `art`      | `php artisan` |
| `migrate`  | `php artisan migrate` |
| `fresh`    | `php artisan migrate:fresh --seed` |
| `tinker`   | `php artisan tinker` |
| `serve`    | `php artisan serve` |
| `che`      | Clear view/cache/config caches |
| `mig`      | `time php artisan migrate:fresh --seed` |
| `gpl`      | `git pull && npm run build && php artisan optimize:clear` |
| `seeder`   | `php artisan db:seed` |
| `optimize` | `php artisan optimize:clear` |

---

## TAILSCALE + PIQL BRIDGE

piql runs on OFFICE only. From home: use SSH-based commands to reach it.

### Network
| Command         | What it does |
|-----------------|-------------|
| `tss`           | `tailscale status` — list all peers |
| `tsip`          | Own Tailscale IP |
| `tsp`           | SSH to TAILSCALE_PEER (other machine) |
| `tsping`        | Ping TAILSCALE_PEER |

`TAILSCALE_PEER` is set per machine in `config.zsh`:
- office: `hruzam` (home, 100.110.27.60)
- home: `hruzam-120922` (office, 100.126.182.111)

### piql cross-machine [HOME → reads from OFFICE]
| Command            | What it does |
|--------------------|-------------|
| `piql-remote`      | Read last piql output from office |
| `piql-pull`        | Alias for piql-remote |
| `piql-watch`       | Tail piql session log from office (streaming) |
| `piql-ask <text>`  | Run piql query on office over SSH, output here |

### piql cross-machine [OFFICE → pushes to HOME]
| Command       | What it does |
|---------------|-------------|
| `piql-push`   | SCP last piql output to home machine |

### piql expose (future — piql has no HTTP endpoint yet)
| Command              | What it does |
|----------------------|-------------|
| `piql-expose`        | Expose PIQL_PORT on tailnet via `tailscale serve` |
| `piql-expose-off`    | Remove tailscale serve |
| `piql-expose-status` | `tailscale serve status` |

Set `PIQL_PORT` in `config.zsh` when piql gets an HTTP endpoint (check `piql.env.zsh`).
Shannon (piql wiser mechanic) must review any piql-expose call before use.

---

## SYSTEM MONITORING (archx suite) [OFFICE]

| Command          | What it does |
|------------------|-------------|
| `sysmon`         | Full system overview (CPU, memory, disk, services) |
| `cputop`         | Top 10 CPU processes |
| `memtop`         | Top 10 memory processes |
| `diskuse`        | Top dirs by disk usage under /home |
| `services`       | Key service status check |
| `troubleshoot`   | Guided fix for common archx issues |
| `archx-monitor`  | Full archx monitoring dashboard |
| `archx-services` | Services health check |

---

## SYSTEM UTILITIES

| Command        | What it does |
|----------------|-------------|
| `src`          | `source ~/.zshrc` — reload shell config |
| `ord`          | `ls -lthr` — list newest last |
| `dsk`          | `wmctrl -s` — switch virtual desktop |
| `ssr`          | `simplescreenrecorder & disown` |
| `hasz`         | Random hex token (21 chars) |
| `cod`          | PHP uniqid() |
| `mygrep`       | `grep -Hrn` |
| `msrc <term>`  | Search in `$PROJECT_FO_PATH` |
| `sub2`         | Sublime Text 2-column layout |
| `svt`          | Append shell history to `~/log/_terminal.txt` |

---

## BROWSER [OFFICE]

| Command     | What it does |
|-------------|-------------|
| `ffxn`      | Firefox new window (Google) |
| `ffxl`      | Open local FO database in Adminer |
| `ffxgpt`    | Open ChatGPT in Firefox |
| `ffxp`      | Open production Imago Adminer (local .zshrc — not synced) |

---

## PACMAN HELPERS

| Command          | What it does |
|------------------|-------------|
| `upconfiles`     | Update conflicting pacman files (finds owning packages) |
| `down_pack`      | Download packages from CSV spec |

---

## MAINTENANCE AGENTS

| Agent    | Invoke with | Role |
|----------|-------------|------|
| office seat | Claude Code / Sonnet (any session) | Office machine maintenance |
| Shannon  | `claude --agent shannon` | piql wiser mechanic — privacy gate audit |
| Houston  | `claude --agent houston` | Architect / phase planner |

Roster: `~/reposoma/temple/roster.md`
Shannon spec: `~/.claude/agents/shannon.md`

---

## FILES TO KNOW

| Path | What |
|------|------|
| `~/.config/zsh/config.zsh` | Machine config (paths, PHP, Tailscale peer) |
| `~/.config/zsh/project-switcher.zsh` | fo/im/php74/php8/imst/fost |
| `~/.config/zsh/system/shell.zsh` | General shell aliases |
| `~/.config/zsh/system/browser.zsh` | Firefox launchers [OFFICE] |
| `~/.config/zsh/system/pacman.zsh` | Pacman helpers |
| `~/.config/zsh/piql/tailscale.zsh` | Tailscale + piql bridge |
| `~/.config/zsh/guides/sudoers.valet-php.conf` | Install to make php74/php8 passwordless |
| `~/.valet/Nginx/fantasyobchod` | Per-site PHP 7.4 routing (not in ia-sync) |
| `~/ia-sync/journal.host-cleanup.md` | Office ↔ home git bus |
