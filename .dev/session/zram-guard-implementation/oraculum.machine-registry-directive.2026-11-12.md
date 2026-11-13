# Directive — per-machine registry (`machine.<host>.json`) + first consumer (zram)

from: oraculum (direct main, home, 2026-11-12) · to: the living Claude session working zram
(cwd `zsh/registries`, session `b2f004b4`) · authority: majkee, relayed in Oraculum's session
shape: RETURN — reply with a file next to this one (see "Return") · audit after: @Cartan

This answers your relayed question. Majkee's decision: **yes, a registry — one file per
machine, reached from `config.zsh`** — and he wants a clean line between script and data.
You hold the uncommitted zram files, so you implement; nobody else writes in this tree meanwhile.

## 1. File kinds (the clean line)

| Kind | Files | Holds | Never holds |
|---|---|---|---|
| **config** | `config.<host>.zsh` → `~/.config/zsh/config.zsh` | identity, `source` wiring, pointers | logic, host facts |
| **registry** | `registries/*.json` | stable declared data, read by engines | code; nothing is ever `eval`'d from it |
| **engine** | `<scope>/*.zsh`, `*.sh`, `*.py` | behaviour | host-specific values |
| **keyboard** | `<scope>/keyboard.zsh` | aliases only (existing law) | bodies |
| **machine state** | `/etc/...`, `/proc`, `~/.local/state` | realized + measured values | — (never in the repo) |

Facts-live-once, applied: the registry holds **declared intent and nominal class**. Live
measurements stay in the kernel; the realized zram config stays in `/etc`. An engine may
compare declared vs realized; it never copies one into the other silently.

## 2. Files to create

`zsh/registries/machine.home.json`, `machine.office.json`, `machine.monitor.json`.
Named `machine.*` to match `machines.json` / `$MACHINE_NAME` and to stay clear of the
existing `registries/hosts.json` (RC dispatch — different purpose, do not touch).
All three deploy to every host through the normal zsh rsync (no `deploy.sh` change); each
host reads only its own. Ownership follows `config.<host>.zsh`: the host's own seat edits
its file. This first seeding of all three from home is a one-time exception under majkee's
grant — say so in the journal.

Values measured read-only over the tailnet today (2026-11-12):

| | home | office | monitor |
|---|---|---|---|
| MemTotal | 10048552 kB (lsmem 10G) | 16131256 kB (15.9G) | 12151568 kB (12G) |
| swap now | zram0 4G zstd prio 100, **4G of 4G used** | none | none |
| zram-generator | 1.2.1-1 | not installed | not installed |
| swappiness / zswap | 100 / N | 60 / Y | 60 / Y |
| jq | present | present | present |

Schema (home shown; keep keys identical across hosts):

```json
{
  "_meta": {
    "role": "Per-machine registry: declared intent + nominal class for THIS host. Not measurements (kernel) and not realized state (/etc).",
    "reached_by": "config.<host>.zsh exports MACHINE_REGISTRY; engines read via _machine_get (system/machine.zsh). Never eval'd.",
    "owner": "this host's seat, same rule as config.<host>.zsh",
    "seeded": "2026-11-12 from read-only tailnet inventory"
  },
  "machine": "home",
  "ram_class_gb": 10,
  "swap": {
    "policy": "zram",
    "zram": { "size_mib": 4096, "algorithm": "zstd", "priority": 100 },
    "swappiness": 100,
    "zswap": "off-runtime"
  }
}
```

office: `ram_class_gb` 16, `"swap": { "policy": "none" }`. monitor: `ram_class_gb` 12, same.
`policy: none` records what is true and intended today; whether those hosts get zram is
majkee's call, not this task's. Do not change home's 4096 either (see open items).

## 3. Wiring

1. **`zsh/config.home.zsh`** (home-owned, you are on home): one line before the
   `system/base.zsh` source:
   `export MACHINE_REGISTRY="$ZSH_CONFIG_DIR/registries/machine.$MACHINE_NAME.json"`
   A pointer, not a startup parse: no `jq` fork and no `eval` at every shell start. That is
   the difference from the retired `normalizer.py` + `harness.machine-project-registry.json`
   mechanism, which must not come back.
2. **Do NOT edit `config.office.zsh` / `config.monitor.zsh`** (other hosts' seats). The
   reader falls back to the same path when `MACHINE_REGISTRY` is unset, so they work after a
   plain deploy. Flag the one-line mirror in the journal for those seats.
3. **New engine `zsh/system/machine.zsh`** — defines only:
   - `_machine_get <jq-path>` → `jq -r "<path> // empty"` on
     `${MACHINE_REGISTRY:-$HOME/.config/zsh/registries/machine.$MACHINE_NAME.json}`;
     prints nothing and returns non-zero when the file or `jq` is missing.
   - `_machine_show` → pretty-print the file.
   Alias `machine-show` in `system/keyboard.zsh`. Source it in `system/base.zsh` as its own
   partition **before** the zram partition.
4. **`zsh/system/zram.zsh`** — the first consumer, two small changes, nothing auto-applied:
   - `_zram_set` defaults: realized conf → registry (`.swap.zram.*`) → today's hardcoded
     fallback. Behaviour on home is unchanged.
   - `_zram_status`: add a `── declared (registry) ──` block (policy, size, algo, prio,
     swappiness, zswap) so drift between declared and realized is visible on one screen.

## 4. Docs (same session)

- New `zsh/registries/README.md`: the table from §1 plus one line per registry file. This
  is the home of the file-kind rule; do not edit the gaveled `guides/guide-for-builder.md`.
- `zsh/AGENTS.md` live map: rows for `system/machine.zsh`, `system/zram.zsh`,
  `registries/machine.<host>.json`.
- Root `AGENTS.md`, "Which host am I on?": the RAM line says "home ~11.6 GiB / 12 GB". That
  is wrong — 11.6 GiB is **monitor**; home measures 9.58 GiB. Replace the hard numbers with
  a pointer to `registries/machine.<host>.json` (`ram_class_gb`) so the class lives once.
  Mark presence (`rb-mark`, unmark by exact id) for this root-level edit.
- `journal.host-cleanup.md`: fold into today's HOME entry — what landed, the seeding
  exception, the mirror line owed by office and monitor seats, the AGENTS.md RAM correction.

## 5. Order and checks

1. `git pull --rebase origin main` first (your uncommitted work is yours to carry).
2. Make the edits. `zsh -n` every touched `.zsh`; `jq . ` every new JSON.
3. `bash deploy.sh --zsh-only --dry-run`, read it, then `bash deploy.sh --zsh-only` — **home only**.
4. Verify from a fresh shell (`zsh -ic`): `echo $MACHINE_REGISTRY`; `machine-show`;
   `_machine_get .swap.policy` → `zram`; `zram-st` shows the declared block; with
   `MACHINE_REGISTRY` unset the fallback still resolves; with the file moved aside
   `zram-st` and `zram-set` (usage path) still work.
5. Commit and push per `SYNC_DISCIPLINE.md` steps 6–7. If your session needs an explicit
   operator ask before committing, stop there and say so in the return.

Out of scope — do not do: any ssh write, deploy or install on office or monitor; resizing
zram; touching `hosts.json`, `machines.json`, `deploy.sh`, `ai/` or the mail in `_mail/home/inbox/`.

## 6. Open items you should carry into the return, not solve

- Home's zram is full (4G of 4G used, ~2.1 GiB available). Sizing is majkee's decision.
- `registries/hosts.json` has no `monitor` row; `palette.json` `root_files` lacks
  `config.monitor.zsh`. Separate drift, separate task.
- `archx/` docs still say "no swap" for home.

## Return

Write `oraculum.machine-registry-return.2026-11-12.md` beside this file: files changed,
commands with outcomes, the §5.4 check outputs, anything you deviated from and why, what you
did not touch, commit hash or "not committed". Then tell majkee; he pokes Oraculum by hand.
Oraculum then hands this directive plus your return to @Cartan for an independent audit.
