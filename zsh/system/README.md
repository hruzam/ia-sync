# system/ — shell scope

General shell utilities and system-level tooling. Cross-machine unless a file
carries an explicit `$MACHINE_NAME` guard.

**Law:** `~/.config/zsh/guides/guide-for-builder.md §Architecture rules` —
read before touching any file here.

---

## File map

| File | Role | Bodies |
|---|---|---|
| `keyboard.zsh` | Control panel — aliases + comments only | — |
| `dashboard.zsh` | Startup dashboard engine | `_dash_header` |
| `dashboard.md` | Startup dashboard content — @majkee edits this to change what prints on shell open | — |
| `tailscale.zsh` | Tailscale engine | `_ts_ls` `_ts_header` `_ts_ping` `_ts_ssh` `_ts_session` `_ts_dash` `_ts_dash_stop` `_ts_web` `_ts_help` |
| `ts-dash.py` | Python HTTP dashboard server — called by `_ts_dash` | — |
| `shell.zsh` | General shell utilities engine | `_msrc` |
| `home.php-composer.zsh` | Home PHP/Composer engine — Docker PHP 7.4 + Composer, native PHP 8+ | `_php74` `_php8` `_phpst` `_composer74` `_composer8` |
| `office.php-switch.zsh` | Office PHP/Composer engine — native CLI + concurrent FPM services | `_php74` `_php8` `_phpst` `_composer74` `_composer8` |

@majkee edits `dashboard.md` directly to change the startup dashboard content — no code changes are needed for content edits.

---

## Command surface

### PHP + Composer

The keys are identical on both hosts; the engine follows each machine's runtime:

| Alias | Home | Office |
|---|---|---|
| `php74 [args]` | PHP 7.4 CLI in `php74-composer` Docker image | start `php74-fpm` + status |
| `php8 [args]` | native `/usr/bin/php` (PHP 8+) | start `php-fpm` + status |
| `phpst` | Docker/image/native CLI status | both FPMs, sockets, and CLI versions |
| `composer74 [args]` | `php74-composer` Docker image | `/usr/bin/php74 /usr/bin/composer` |
| `composer8 [args]` | `composer:latest` Docker image | native `/usr/bin/composer` |

### Tailscale

Run `ts-help` in the shell for the live panel. Reference:

| Alias | Body | What |
|---|---|---|
| `tss` | `tailscale status` | raw status table |
| `tsip` | `tailscale ip -4` | my tailscale IP |
| `ts-ls` | `_ts_ls` | formatted peer list |
| `ts-header` | `_ts_header` | compact startup line |
| `tsping [host]` | `_ts_ping` | ping peer · default `$TAILSCALE_PEER` |
| `tsp [host]` | `_ts_ssh` | ssh to peer (fast) |
| `tso [host]` | `_ts_session` | ssh with pre-connect check |
| `ts-dash` | `_ts_dash` | start HTTP dashboard (port `$TS_DASH_PORT`, default 9733) |
| `ts-dash-stop` | `_ts_dash_stop` | stop dashboard |
| `ts-web` | `_ts_web` | open Tailscale admin panel in browser |
| `ts-help` | `_ts_help` | command panel |
| `web-reach [peer] [port]` | `_web_reach` | loopback SOCKS v5 proxy through peer (default `127.0.0.1:1080`) |
| `web-reach-firefox [url]` | `_web_reach_firefox` | start the proxy and open an isolated Firefox profile through peer egress |
| `web-reach-down [port]` | `_web_reach_down` | close the browser-egress proxy |

Full procedure: `~/reposoma/raw.guides/browser-egress/GUIDE.md` (`/guide browser-egress`).

---

## How to add a command to this scope

Three steps, in order:

**1. Write the body in the correct engine** (`tailscale.zsh` for tailscale commands,
`shell.zsh` for general shell utilities, or the host PHP engine):

```zsh
_ts_mycommand() {
    # function body here — no aliases inside
}
```

**2. Add the alias to `keyboard.zsh`** under the correct scope block:

```zsh
alias ts-mycommand='_ts_mycommand'   # one-line description
```

**3. Add a row to `_ts_help`** in `tailscale.zsh` (keep it in sync with keyboard.zsh):

```zsh
printf "  ts-mycommand     what it does\n"
```

Then: `zsh -n system/tailscale.zsh && zsh -n system/keyboard.zsh` — syntax clean before committing.

---

## Wiring

Both files are sourced from `config.zsh` (and `config.home.zsh` for home):

```zsh
[[ -f ~/.config/zsh/system/tailscale.zsh ]] && source ~/.config/zsh/system/tailscale.zsh
[[ -f ~/.config/zsh/system/keyboard.zsh  ]] && source ~/.config/zsh/system/keyboard.zsh
```

`_ts_header` is called once after sourcing to print the peer status line on shell open.

---
