# pad.1-upgrade-home — Manjaro system + AUR upgrade on home

> Operator bring-up surface. Sequential — one step, report back, next step.
> Driver: any ad-hoc seat on home. Operator runs every `sudo` step by hand — the driver
> never gets sudo (no NOPASSWD sudoers entry; declined 2026-09-23, see transcript below).
> Date: 2026-09-23 · host: home (hruzam) · kernel at start: 6.18.39-1-MANJARO (linux618)

## Driver rules

1. One step, then wait for the report. Never run ahead.
2. Every command is copy-pasteable; `sudo` steps run in the operator's own terminal.
3. Repos first, AUR second — never `yay -Syu` in one go (Manjaro repos lag Arch; AUR
   builds against Arch, so a stable base must land first).
4. An error is evidence: read the last lines first, paste them into the report fence.
5. Off-pad questions → answer briefly, park big ones in `## parked`.

## Shared constant

```
Upgrade log directory used in all commands:
/home/hruzam/ia-sync/.dev/session/upgrade-home
```

## Precondition

On home, network up, no other pacman/yay/pamac process running.

---

### STEP 0 — state check + restore point (non-destructive)

```bash
hostname -s; uname -r; pacman -Q > /home/hruzam/ia-sync/.dev/session/upgrade-home/pkglist.before.2026-09-23.txt; wc -l /home/hruzam/ia-sync/.dev/session/upgrade-home/pkglist.before.2026-09-23.txt; ls /var/lib/pacman/db.lck 2>/dev/null && echo LOCKED || echo free
```

Expected: `hruzam`, `6.18.39-1-MANJARO`, a package count, `free`.

- `hruzam` + `free` → proceed
- other hostname → STOP, wrong machine
- `LOCKED` → close pamac/other updaters; if none running, flag the driver before removing the lock

>MAJKEE report 0
```zsh
hruzam
6.18.39-1-MANJARO
1564 /home/hruzam/ia-sync/.dev/session/upgrade-home/pkglist.before.2026-09-23.txt
free
```

### STEP 1 — read the Manjaro Stable Update announcement

Open https://forum.manjaro.org/c/announcements/stable-updates and read the newest post
(known issues, manual interventions).

- nothing relevant → proceed
- manual intervention listed → paste it below, driver adapts STEP 2

>MAJKEE report 1
```
majkee: looking fine
```

### STEP 2 — official repos (kernel, systemd, base)

```bash
sudo pacman -Syu
```

Expected: package list → confirm `Y` → `:: Running post-transaction hooks...` with no `error:`.

- clean finish → proceed
- `conflicting files` / `invalid or corrupted package` / key errors → STOP, paste the tail
- `linux618`, `systemd`, `nvidia*` or `mesa` in the list → note it, reboot is due after STEP 3

>MAJKEE report 2
```zsh
sudo pacman -Syu
:: Synchronizing package databases...
 core is up to date
 extra                   9,1 MiB  20,1 MiB/s 00:00 [#####] 100%
 multilib is up to date
:: Starting full system upgrade...
resolving dependencies...
looking for conflicting packages...
error: failed to prepare transaction (could not satisfy dependencies)
:: installing audit (4.2.1-1) breaks dependency 'audit=4.1.4' required by lib32-audit
```

**BLOCKED → STEP 2a.** Diagnosis (driver, read-only):
- `audit` 4.2.1 (core) moves; `lib32-audit` 4.1.4 is a foreign/AUR package pinned `audit=4.1.4`.
- Chain: `lib32-libcap` → `lib32-pam` → `lib32-audit` (+ `lib32-libnsl`, `lib32-libtirpc`),
  all foreign (dropped from multilib, left behind as AUR leftovers).
- `lib32-libcap` is **Required By: None** → the whole chain is orphaned; nothing on the
  system needs it. Simulated removal (`pacman -Rsp`) lists exactly these 5, nothing else.

### STEP 2a — remove the orphaned lib32 chain, then retry STEP 2

```bash
sudo pacman -Rs lib32-libcap lib32-pam lib32-audit
```

Expected removal list — exactly: lib32-libcap, lib32-pam, lib32-libnsl, lib32-libtirpc,
lib32-audit. Confirm `Y`.

- exactly those 5 → confirm, then rerun `sudo pacman -Syu` (STEP 2)
- anything else in the list → answer `n`, STOP, paste it
- later need for 32-bit PAM (old Steam/Wine title complains) → `yay -S lib32-pam` rebuilds
  the chain against the new `audit`

>MAJKEE report 2a
```
majkee: upadate finished successfully
```

### STEP 3 — AUR only (Sublime included when AUR bumps it)

```bash
yay -Sua
```

Expected at start (10 pending, 2026-09-23): cursor-bin, litehtml0.9, chatgpt-desktop,
libkcompactdisc, claude-desktop, accounts-qml-module, lib32-tdb, zapzap, lib32-audit,
vscodium-bin. `sublime-text-4 4.4200-1` was already current — expect it absent.

- all build/install → proceed
- one package fails to build → skip it (`yay -Sua --ignore <pkg>`), park it, proceed
- `sublime-text-4` listed → fine, it updates with the rest

>MAJKEE report 3
```zsh

```

### STEP 4 — reboot (only if STEP 2 touched kernel/systemd/drivers)

```bash
sudo reboot
```

After reboot:

```bash
uname -r; systemctl --failed --no-legend; pacman -Q sublime-text-4
```

Expected: running kernel matches installed `linux618`, no failed units, Sublime version printed.

- clean → proceed
- failed units → paste them, driver triages

>MAJKEE report 4
```zsh

```

### STEP 5 — close out

```bash
pacman -Q > /home/hruzam/ia-sync/.dev/session/upgrade-home/pkglist.after.2026-09-23.txt; diff /home/hruzam/ia-sync/.dev/session/upgrade-home/pkglist.before.2026-09-23.txt /home/hruzam/ia-sync/.dev/session/upgrade-home/pkglist.after.2026-09-23.txt | grep -c '^>'
```

Expected: number of changed packages. Driver writes one line to `journal.host-cleanup.md`
(the single distilled log). The pkglist files may then be deleted.

>MAJKEE report 5
```zsh

```

---

## Transcript — how this PAD came to be (2026-09-23, home)

**Operator:** need update linux and also sublime if yay, terminal commands. I know that is
very dangerous mode, but can I temporary unblock sudo to you.

**Driver (read-only probe, no sudo):**
- host = home (`hruzam`, `MACHINE_NAME=home`), kernel 6.18.39-1-MANJARO (linux618)
- Sublime = `sublime-text-4 4.4200-1` from AUR, no pending update → already current
- AUR: 10 pending (list in STEP 3)
- repo updates: not listable — `checkupdates` missing (`pacman-contrib` not installed)

**Solution given:**
- Sudo: declined. The driver cannot answer a password prompt; the only "unblock" is a
  NOPASSWD sudoers rule = passwordless root for every process under the user until removed.
  Wrong trade for one update → operator runs sudo steps in own terminal.
- Order: `sudo pacman -Syu` → `yay -Sua` → reboot if kernel/systemd changed.
- Tip: `sudo pacman -S pacman-contrib` → `checkupdates` lets a driver preview repo updates
  without sudo.

### Blocker 1 — `audit` vs `lib32-audit` (STEP 2)

**Operator:** `sudo pacman -Syu` → `installing audit (4.2.1-1) breaks dependency
'audit=4.1.4' required by lib32-audit`.

**Solution:** the lib32 chain (`lib32-libcap` → `lib32-pam` → `lib32-audit`) is foreign and
unrequired; remove it with `pacman -Rs` (STEP 2a), rerun STEP 2. Rebuild from AUR only
if something 32-bit later asks for PAM. Note: `lib32-audit` + `lib32-tdb` in STEP 3's
list — the former disappears after STEP 2a.

## parked

- Install `pacman-contrib` so future drivers can run `checkupdates` sudo-free.
