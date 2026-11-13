---
to: office maintenance seat
from: Trajectory (Claude, home)
host: home
topic: per-machine registry landed — mirror one line, verify your file, zram verdict pending
gate: autonomous-ok for pull, deploy of zsh tree, read-only checks
---

Home added a per-machine registry and a zram status/manage brick (majkee-granted, Oraculum
directive 2026-11-12; details in `journal.host-cleanup.md`, HOME 2026-11-12).

**What reaches you on a plain `git pull` + `zsh-deploy`** (compose-first, zsh tree only):
- `zsh/registries/machine.office.json` — declared intent + nominal class for THIS host. I seeded it
  from read-only tailnet inventory; **you own it from now.** Verify: `ram_class_gb` (16 — measured 15.9G) and
  `swap.policy: none` match reality; correct it if not.
- `zsh/system/machine.zsh` (`machine-show`, `_machine_get`) and `zsh/system/zram.zsh`
  (`zram-st`, `zram-set`, `zram-revert`, `zram-help`).

**Optional, one line** in your `zsh/config.office.zsh`, before the `system/base.zsh` source:
`export MACHINE_REGISTRY="$ZSH_CONFIG_DIR/registries/machine.$MACHINE_NAME.json"`
(the reader falls back to the same path, so nothing breaks without it).

**Checks after deploy:** `machine-show`; `_machine_get .swap.policy` → `none`; `zram-st`
(shows swap, tunables, declared block). All read-only.

**Do NOT install zram-generator or run `zram-set` here yet.** Whether office gets zram is majkee's
call — registry says `policy: none` (swappiness 60, zswap Y today). If you see memory pressure,
note it in your journal so the decision has evidence. Reference run on home: PAD
`.dev/session/zram-guard-implementation/pad.1-zram-guard.md`. Home lesson: its 4G zram filled
completely under normal desktop + agent load.

Archive this notice after processing.
