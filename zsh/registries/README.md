# registries/ — declared data read by engines

## File kinds (the clean line — majkee, 2026-11-12)

| Kind | Files | Holds | Never holds |
|---|---|---|---|
| **config** | `config.<host>.zsh` → `~/.config/zsh/config.zsh` | identity, `source` wiring, pointers | logic, host facts |
| **registry** | `registries/*.json` | stable declared data, read by engines | code; nothing is ever `eval`'d from it |
| **engine** | `<scope>/*.zsh`, `*.sh`, `*.py` | behaviour | host-specific values |
| **keyboard** | `<scope>/keyboard.zsh` | aliases only (existing law) | bodies |
| **machine state** | `/etc/...`, `/proc`, `~/.local/state` | realized + measured values | — (never in the repo) |

Registry = declared intent and nominal class. Live measurements stay in the kernel; realized
config (e.g. zram) stays in `/etc`. An engine may compare declared vs realized; it never copies
one into the other silently.

## Files

- `machine.<host>.json` — per-machine declared intent + class (`ram_class_gb`, `swap.*`). Read by
  `system/machine.zsh` (`_machine_get`, `machine-show`) via `$MACHINE_REGISTRY` (falls back to the
  same path from `$MACHINE_NAME`). Each host's own seat edits its file. First consumer: `system/zram.zsh`.
- `hosts.json` — RC cross-host dispatch (host → tailnet identity). Different purpose.
- `ai.json` — AI runtime registry (remote-control projects etc.).
- `projects.json` — project registry. `palette.json` — palette registry.
- `autonomy-mode.json` — autonomy-mode registry. `tcr/` — per-project tree-snapshot configs.
- `gen-temple-map.sh` — generator script (not data).
