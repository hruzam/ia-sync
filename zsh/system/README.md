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
| `tailscale.zsh` | Tailscale engine | `_ts_ls` `_ts_header` `_ts_ping` `_ts_ssh` `_ts_session` `_ts_dash` `_ts_dash_stop` `_ts_web` `_ts_help` |
| `ts-dash.py` | Python HTTP dashboard server — called by `_ts_dash` | — |
| `shell.zsh` | General shell utilities engine | `_msrc` |
| `office.php-switch.zsh` | PHP version switcher — office only (`$MACHINE_NAME` guard) | `php74` `php8` `phpst` |

---

## Command surface (tailscale scope)

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

---

## How to add a command to this scope

Three steps, in order:

**1. Write the body in the correct engine** (`tailscale.zsh` for tailscale commands,
`shell.zsh` for general shell utilities):

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

## Pending work

- **office.php-switch.zsh** — not yet split into keyboard/engine. Low priority:
  office-only, rarely touched.
