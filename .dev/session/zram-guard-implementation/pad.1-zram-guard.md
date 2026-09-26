# pad.1-zram-guard — install a persistent zram swap on the home host so RAM bursts stop jamming the desktop

> Operator bring-up surface. Sequential — one step, report back, next step.
> Driver: the maintenance seat at the keyboard on the home host.
> Per-run: this PAD adds only two small files and one systemd swap device. No bootloader / grub
> edit. Worst case = STEP 0's revert recipe removes everything.
>
> Resume this Claude session after a reboot (home host — copy the line):
>   claude --resume 064d3bbe-cd94-42d0-9003-fc26b6e5b47e   # run from /home/hruzam/ia-sync

## Why (one line, not the PAD's job to teach)

Home is ~9.6 GB with **zero swap**; the desktop + terminals + agent sessions spike past the
ceiling in bursts and the kernel has nowhere to page → stutter / OOM. zram gives it a fast,
compressed RAM-backed swap that absorbs those bursts. Full reasoning lives in
`journal.host-cleanup.md`, not here.

## Shared constants (used verbatim in every step — never re-derive)

```
zram config file : /etc/systemd/zram-generator.conf
swappiness file  : /etc/sysctl.d/99-zram-swappiness.conf
zram swap device : /dev/zram0   (4 GiB, zstd)
```

## Precondition

You are on the **home host** (hruzam), at a real terminal that can prompt for the sudo password,
and `zram-generator` is installed (confirmed 1.2.1 on 2026-09-23). STEP 0 verifies all of this
before anything is written.

---

### STEP 0 — state check + record the revert point (non-destructive)

```bash
echo "host: $MACHINE_NAME / $(hostname -s)"
ls /usr/bin/php74 >/dev/null 2>&1 && echo "FINGERPRINT: office (STOP)" || echo "FINGERPRINT: home (ok)"
echo "--- current swap (expected: empty) ---"; swapon --show || echo "(no swap — expected)"
echo "--- zram-generator installed? ---"; pacman -Q zram-generator || echo "MISSING (STOP)"
echo "--- config file already present? ---"; ls -l /etc/systemd/zram-generator.conf 2>/dev/null || echo "(none — good, clean install)"
echo "--- record current tunables to revert to ---"
echo "zswap.enabled = $(cat /sys/module/zswap/parameters/enabled 2>/dev/null)"
echo "vm.swappiness = $(cat /proc/sys/vm/swappiness)"
```

Expected: `FINGERPRINT: home (ok)`, swap empty, `zram-generator 1.2.1-1`, no existing config file.

Branch:
- host = home, zram-generator present → proceed to STEP 1
- `FINGERPRINT: office` OR `zram-generator MISSING` → **STOP**, flag the driver — this PAD is home-only
- config file already exists → **STOP**, a prior install is present; read it before overwriting

Revert recipe (the whole PAD's undo, keep it in view):
```
sudo swapoff /dev/zram0 2>/dev/null; sudo systemctl stop systemd-zram-setup@zram0.service 2>/dev/null
sudo rm -f /etc/systemd/zram-generator.conf /etc/sysctl.d/99-zram-swappiness.conf
sudo systemctl daemon-reload
```

>MAJKEE report 0
```zsh
host: home / hruzam
FINGERPRINT: home (ok)
--- current swap (expected: empty) ---
--- zram-generator installed? ---
zram-generator 1.2.1-1
--- config file already present? ---
(none — good, clean install)
--- record current tunables to revert to ---
zswap.enabled = Y
vm.swappiness = 60

```

---

### STEP 1 — write the zram config

```bash
sudo tee /etc/systemd/zram-generator.conf >/dev/null <<'EOF'
# home host (hruzam) — 2026-09-25, burst/OOM guard on 9.6GB no-swap box
[zram0]
zram-size = 4096
compression-algorithm = zstd
swap-priority = 100
EOF
sudo cat /etc/systemd/zram-generator.conf
```

Expected: the four `[zram0]` lines printed back verbatim.

Branch:
- file printed correctly → proceed to STEP 2
- permission / write error → **STOP**, flag the driver (sudo not working from this terminal)

>MAJKEE report 1
```zsh
# home host (hruzam) — 2026-09-25, burst/OOM guard on 9.6GB no-swap box
[zram0]
zram-size = 4096
compression-algorithm = zstd
swap-priority = 100

```

---

### STEP 2 — activate the zram device

```bash
sudo systemctl daemon-reload
sudo systemctl start systemd-zram-setup@zram0.service
echo "exit: $?"
```

Expected: `exit: 0`, no error text.

Branch:
- `exit: 0` → proceed to STEP 3
- `A dependency job for systemd-zram-setup@zram0.service failed` / `exit: 1` → **REBOOT REQUIRED,
  not a PAD bug.** Diagnosed 2026-09-25: a system update installed kernel 6.18.49 but the box is
  still running 6.18.39, whose module tree was deleted by the update — so the `zram` module can't
  load. STEP 1 already wrote the config, and zram-generator auto-arms at boot, so:
    1. reboot home  →  2. `claude --resume 064d3bbe-cd94-42d0-9003-fc26b6e5b47e` (from /home/hruzam/ia-sync)
    →  3. skip to STEP 3 (zram likely already live); if not, re-run STEP 2 on the new kernel.
- any OTHER unit failure → run `systemctl status systemd-zram-setup@zram0.service --no-pager` and **STOP**, flag the driver

>MAJKEE report 2
```zsh
A dependency job for systemd-zram-setup@zram0.service failed. See 'journalctl -xe' for details.
exit: 1
```

---

### STEP 3 — verify the swap is live (the gate step)

```bash
swapon --show
echo "---"
zramctl
```

Expected: a `/dev/zram0` row in `swapon --show` (TYPE partition, SIZE 4G), and `zramctl` showing
`zram0 … zstd … 4G`.

Branch:
- `/dev/zram0` present at 4G zstd → **SUPPORTED**, proceed to STEP 4
- `swapon --show` still empty → **BLOCKED**, STOP and flag the driver (config parsed but device
  never came up — do not continue)

>MAJKEE report 3
```zsh

```

---

### STEP 4 — make the kernel actually prefer zram (persistent swappiness)

```bash
echo 'vm.swappiness=100' | sudo tee /etc/sysctl.d/99-zram-swappiness.conf
sudo sysctl --system >/dev/null
echo "vm.swappiness now = $(cat /proc/sys/vm/swappiness)"
```

Expected: `vm.swappiness now = 100`. (zram is RAM-fast, so a higher value than the default 60 is
correct — it tells the kernel to lean on zram early instead of stalling.)

Branch:
- `= 100` → proceed to STEP 5
- unchanged (still 60) → re-run `sudo sysctl --system`; if still 60, **STOP**, flag the driver

>MAJKEE report 4
```zsh

```

---

### STEP 5 — quiet the now-redundant zswap (runtime only, no grub)

```bash
echo N | sudo tee /sys/module/zswap/parameters/enabled
echo "zswap enabled now = $(cat /sys/module/zswap/parameters/enabled)"
```

Expected: `zswap enabled now = N`.

Note — deliberate, per operator's call: this is **runtime only**. It reverts to `Y` on the next
reboot because making it permanent would need a bootloader (grub) edit, which we are NOT doing.
Leaving zswap `Y` after a reboot is harmless — with zram present it just adds a little redundant
compression, no correctness impact. If you ever want it permanent without grub, see `## parked`.

Branch:
- `= N` → proceed to STEP 6
- write error → not fatal; note it and proceed to STEP 6 (zram already works)

>MAJKEE report 5
```zsh

```

---

### STEP 6 — final soak check + done

```bash
free -h
echo "---"
swapon --show
echo "--- reboot-persistence proof: config file is on disk, so zram re-arms every boot ---"
ls -l /etc/systemd/zram-generator.conf /etc/sysctl.d/99-zram-swappiness.conf
```

Expected: `free -h` now shows a non-zero `Swap:` line (~4 GiB total), `/dev/zram0` in
`swapon --show`, both config files present.

Branch:
- Swap ~4G present + both files listed → **DONE.** zram re-arms automatically on every boot;
  nothing to run on future home sessions. Report back so the driver can journal it.
- Swap line still `0B` → **STOP**, flag the driver

>MAJKEE report 6
```zsh

```

---

---

## Companion procedure — restore Tailscale MagicDNS (office SSH by name)

> Separate scope from zram, collected here on purpose so nothing is lost. Symptom: new terminals
> fail `tso` / `ssh hruzam-120922` with "Could not resolve hostname … Name or service not known",
> while ping is reachable and already-open office sessions keep working. Cause (found 2026-09-25):
> a system update left `systemd-resolved` **inactive**, so `/etc/resolv.conf` points at the ISP
> resolver instead of Tailscale's `100.100.100.100` → MagicDNS names don't resolve. Tailscale
> itself is up (peer visible at 100.126.182.111).

**You are NOT locked out while fixing this.** office is reachable now via the IP alias in
`~/.ssh/config` (`Host office → 100.126.182.111`), which needs no DNS:

```bash
ssh office            # works today, no MagicDNS needed — use instead of tso
```

### DN0 — capture current state (non-destructive)

```bash
echo "resolved: $(systemctl is-active systemd-resolved)"
echo "--- current resolv.conf nameservers ---"; grep -v '^#' /etc/resolv.conf | grep -i nameserver
echo "--- name resolves? (expected: fails) ---"; getent hosts hruzam-120922 || echo "  NOT resolvable (the bug)"
echo "--- IP fallback still works? ---"; ssh office 'echo reachable-via-IP; hostname -s' 2>&1 | tail -2
```

Expected: `resolved: inactive`, nameservers = ISP (`31.30.90.*`), name NOT resolvable, IP fallback prints `hruzam-120922`.

Branch:
- matches expected → proceed to DN1
- IP fallback also fails → different problem (tailscale/routing), **STOP** and flag the driver

>MAJKEE report DN0
```zsh

```

### DN1 — re-enable systemd-resolved

```bash
sudo systemctl enable --now systemd-resolved
echo "resolved now: $(systemctl is-active systemd-resolved)"
```

Expected: `resolved now: active`.

Branch:
- `active` → proceed to DN2
- fails to start → run `systemctl status systemd-resolved --no-pager` and **STOP**, flag the driver

>MAJKEE report DN1
```zsh

```

### DN2 — hand DNS back to Tailscale (MagicDNS)

```bash
sudo tailscale set --accept-dns=true
sleep 2
echo "--- resolv.conf should now show 100.100.100.100 ---"; grep -v '^#' /etc/resolv.conf | grep -i nameserver
```

Expected: a `nameserver 100.100.100.100` line appears.

Branch:
- `100.100.100.100` present → proceed to DN3
- still ISP-only → try `sudo tailscale up --accept-dns` and re-check; if still wrong, **STOP**, flag

>MAJKEE report DN2
```zsh

```

### DN3 — verify name resolution + SSH by name (the gate)

```bash
getent hosts hruzam-120922
ssh hruzam-120922 'echo ok-by-name; hostname -s' 2>&1 | tail -2
```

Expected: `getent` resolves to `100.126.182.111`, and the ssh line prints `ok-by-name` + `hruzam-120922`.

Branch:
- both succeed → **DONE.** `tso` works again; report back so the driver journals the DNS change.
- name still fails → **STOP**, flag the driver (do not keep retrying blind)

>MAJKEE report DN3
```zsh

```

Revert (if resolved causes any local DNS trouble): `sudo systemctl disable --now systemd-resolved`
— then `ssh office` (IP alias) remains your access path.

---

## new issues seen while running (collect here — do not lose in chat)

Paste anything odd that surfaces mid-run: unexpected output, a second host misbehaving, an update
side-effect. The driver triages these into `/issue-card` cold-start cards later; this fence is just
so they are captured, not lost.

```
```

---

## After the PAD (driver, not operator)

On a DONE verdict, the driver records one line in `journal.host-cleanup.md` (home substrate
change: zram 4G zstd swap added, swappiness=100, zswap runtime-off). That is the single distilled
home — this PAD stays the raw run-log. No file-per-step. This change is home-local (starts only a
systemd swap device; touches no SSH/PHP/packages), so it stays in the journal and does not
escalate to the Houston bus.

## parked

- **Make zswap-off permanent without grub** (optional, only if a reboot proves the redundant
  compression actually costs something measurable): a tiny systemd oneshot writing `N` to
  `/sys/module/zswap/parameters/enabled` at boot avoids the bootloader entirely. Not built here —
  raise it with the driver if you decide you want it.
- **Resize zram** later: edit `zram-size` in the config file, then re-run STEP 2. 4 GiB is a
  conservative start for a 9.6 GB box (compressed store costs ~1–1.5 GB of real RAM under load).
