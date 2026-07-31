# Blessing check — system-tailscale
_scope: system/tailscale.zsh + system/keyboard.zsh · session 2026-07-20_

> @majkee — run these before continuing. After all boxes checked, the scope is blessed.

---

## Syntax

- [ ] `zsh -n ~/.config/zsh/system/tailscale.zsh && echo OK` → `OK`
- [ ] `zsh -n ~/.config/zsh/system/keyboard.zsh && echo OK` → `OK`
- [ ] `source ~/.config/zsh/system/tailscale.zsh` → no errors

## Command surface

- [ ] `ts-help` → panel prints, 10 rows, peer line shows `$TAILSCALE_PEER`
- [ ] `_ts_header` → one line: `ts 100.x.x.x  N/M peers online — ts-ls for details`
- [ ] `ts-ls` → formatted table, self (◈) + peers (● or ○)
- [ ] `alias tss` → `tss=tailscale status`
- [ ] `alias tso` → `tso=_ts_session`

## Dashboard

- [ ] `ts-dash` → server starts, browser opens
  - verify: `lsof -ti tcp:9733 | wc -l` → `1`
- [ ] `ts-dash-stop` → server killed
  - verify: `lsof -ti tcp:9733 | wc -l` → `0`

## Startup integration

- [ ] Open a new terminal → `ts` status line appears at top (from `_ts_header`)

## Scope hygiene

- [ ] `piql/tailscale.zsh` is clean — original piql functions only, no `_ts_*` bodies
  - `grep -c 'piql-remote\|piql-watch\|piql-ask' ~/.config/zsh/piql/tailscale.zsh` → `3`
- [ ] `piql/ts-dash.py` does NOT exist
- [ ] `system/ts-dash.py` exists

---

_All checked → scope blessed. Uncheck = flag to Eagle or Flight before syncing to ia-sync._
