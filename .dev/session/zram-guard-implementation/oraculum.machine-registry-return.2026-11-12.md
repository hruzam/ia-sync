# Return — machine registry + zram consumer

from: Trajectory (session b2f004b4, home) · to: Oraculum → @Cartan audit · re: directive 2026-11-12

## Changed
- NEW `zsh/registries/machine.{home,office,monitor}.json` (schema as directive §2; `jq .` ok on all)
- NEW `zsh/registries/README.md` (file-kind table + file list)
- NEW `zsh/system/machine.zsh` (`_machine_get`, `_machine_show`; defines only)
- NEW `zsh/system/zram.zsh` (earlier this session) — now defaults realized → registry → fallback; `zram-st` has `── declared (registry) ──` block
- `zsh/system/keyboard.zsh`: aliases `machine-show`, `zram-st|set|revert|help`
- `zsh/system/base.zsh`: P8 machine.zsh (before zram), P9 zram.zsh
- `zsh/config.home.zsh`: `export MACHINE_REGISTRY=…` before system/base.zsh source
- `zsh/AGENTS.md` live-map rows (machine.zsh, zram.zsh, machine.<host>.json)
- root `AGENTS.md`: RAM line → pointer to `ram_class_gb`
- `journal.host-cleanup.md`: folded into today's HOME entry (+ seeding exception, mirror owed)
- PAD `pad.1-zram-guard.md` reports 3–6 filled earlier

## Commands / outcomes
- `git pull --rebase --autostash origin main` → up to date
- `zsh -n` on all touched .zsh → clean; `jq .` on 3 JSON → ok
- `deploy.sh --zsh-only --dry-run` → only the above files (plus pre-existing undeployed `tools/`); then `deploy.sh --zsh-only` (home only) → ok
- §5.4 from fresh `zsh -ic`: `$MACHINE_REGISTRY` = /home/hruzam/.config/zsh/registries/machine.home.json;
  `machine-show` prints file; `_machine_get .swap.policy` → `zram`; absent path → rc 1, no output;
  `zram-st` shows declared block (policy zram, 4096, zstd, 100, 100, off-runtime);
  `unset MACHINE_REGISTRY` → `_machine_get .swap.zram.size_mib` → 4096 (fallback works);
  file moved aside → `zram-st` prints "(no registry entry …)", `zram-set` prints usage; file restored.

## Deviations / notes
- Partition numbering: machine = P8, zram = P9 (zram was P8 before the registry partition was inserted).
- `-ic` shells print a gitstatus/`setopt monitor` error without a TTY — pre-existing, unrelated.
- `zram-set` was not run live (needs sudo TTY); only validation/usage paths exercised. On office/monitor
  (`policy: none`, no zram-generator) `zram-set` would still write a config — not blocked; say if you want a guard.
- Presence: marked 7d0b06dc44ca0e87d1e5080bbb1ab38a, unmarked by that id.

## Not touched
office/monitor config files, ssh/deploy/install on other hosts, zram size, hosts.json, machines.json,
deploy.sh, ai/, `_mail/home/inbox/`, the gaveled guide-for-builder.md.

## Open items carried (not solved)
home swap full (4G/4G) — sizing = majkee; hosts.json lacks monitor, palette.json root_files lacks
config.monitor.zsh; archx docs still say "no swap" for home.

## Commit
Committed + pushed on operator ask (hash in git log). Also sent mail to office + monitor inboxes (`trajectory.registry-and-zram.2026-11-13.md`): pull+deploy, verify own registry file, optional export mirror, no zram install until majkee decides.
