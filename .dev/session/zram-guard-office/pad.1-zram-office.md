# zram — copy-paste setup sheet (office, hruzam-120922)

Compressed RAM swap, to give the machine headroom under memory pressure (no swap exists
today). Copy a block, run it. Needs **sudo** — this host has no NOPASSWD (`sudo -n true`
→ "a password is required"), so an agent cannot run these non-interactively; majkee runs
each block at a real terminal. Fully reversible — the UNDO block at the bottom removes
every trace.

Sibling artifacts: `.dev/session/voice-meetings-01-threshold/pad.1-zram.md` (home, clean
sheet, verified 2026-09-23) and `.dev/session/zram-guard-implementation/pad.1-zram-guard.md`
(home, step-gated live run 2026-09-25 — **stalled at STEP 2** on a kernel-module-tree
mismatch, never completed; no zram entry exists anywhere in `journal.host-cleanup.md`
before today). This sheet follows the clean-sheet shape, adapted for office's fingerprint,
RAM size, and the reboot gate below.

Verified on office 2026-09-28: `zram-generator` NOT installed (1.2.1-1 available in
`extra`), no swap/zram present, live `swappiness=60 page-cluster=3 zswap=Y`, ~15Gi/16GB RAM,
zstd available.

Sizing: `ram / 2` ≈ 7.5 GB compressed device (zram-generator computes this itself — no
hardcoded number needed, unlike home's fixed `4096`). Real RAM cost only grows with what's
actually swapped, shrunk by the compression ratio — idle Firefox/claude/codex pages compress
well; incompressible data does not shrink.

---

## 0 — PRECONDITION: reboot first (hard gate, confirmed not assumed)

Office is running kernel `7.1.3-1-MANJARO`, but `/usr/lib/modules/7.1.3-1-MANJARO` **does
not exist on disk** — removed by the 2026-09-22/26 update that installed `linux71 7.1.13-2`
without a reboot since (`uptime -s` → 2026-09-22 01:48). This is the *exact* failure that
stalled the home attempt ("dependency job for systemd-zram-setup@zram0.service failed …
module tree was deleted by the update"). Loading the zram module will fail identically until
this box reboots — not a maybe, the directory is verifiably gone right now.

```bash
ls /usr/bin/php74 >/dev/null 2>&1 && echo "FINGERPRINT: office (ok)" || echo "FINGERPRINT: NOT office (STOP)"
uname -r; ls -d /usr/lib/modules/$(uname -r) 2>&1
```

Expect (pre-reboot, today): `FINGERPRINT: office (ok)`, then `7.1.3-1-MANJARO` followed by
"No such file or directory".

**The target kernel already has its module tree on disk**
(`/usr/lib/modules/7.1.13-2-MANJARO` exists now), so the reboot should land clean — this
isn't a new ask, it's the reboot already owed since 2026-09-26 for the Plasma/Qt/mesa/kernel
bundle. Per the journal: majkee reboots after agent sessions finish — timing is your call,
not a thing to force mid-session.

After reboot, re-run the two commands above. Proceed only once the `ls -d` line prints a
real path (not an error).

## 1 — state before (nothing to undo if you stop here)

```bash
swapon --show; zramctl; echo "swappiness=$(cat /proc/sys/vm/swappiness) page-cluster=$(cat /proc/sys/vm/page-cluster)"
```

Expect: blank swap/zram, `swappiness=60 page-cluster=3`.

## 2 — install the generator

```bash
sudo pacman -S zram-generator
```

## 3 — write the zram config

```bash
sudo tee /etc/systemd/zram-generator.conf >/dev/null <<'EOF'
[zram0]
zram-size = ram / 2
compression-algorithm = zstd
swap-priority = 100
EOF
cat /etc/systemd/zram-generator.conf
```

## 4 — activate now (also auto-starts on every boot)

```bash
sudo systemctl daemon-reload && sudo systemctl start systemd-zram-setup@zram0.service
echo "exit: $?"
```

Expect: `exit: 0`, no error text. If it fails with the same "dependency job … failed"
message, STEP 0's check was wrong or skipped — re-check `uname -r` against
`/usr/lib/modules/`, do not retry blind.

## 5 — verify it's live

```bash
zramctl && swapon --show
```

Expect: a `/dev/zram0` device (~7.5G, zstd) and a swap line with priority 100. **Paste this
output back so it can be confirmed from this side too.**

## 6 — (optional) tune the kernel to lean on zram early

```bash
sudo tee /etc/sysctl.d/99-zram.conf >/dev/null <<'EOF'
vm.swappiness = 100
EOF
sudo sysctl --system | grep -E "swappiness|page-cluster"
```

Expect: `vm.swappiness = 100`. RAM-backed swap is cheap to hit, so leaning on it earlier
than the default 60 is correct — home's live run (STEP 4) used the same value for the same
reason.

---

## UNDO — remove everything

```bash
sudo swapoff /dev/zram0 2>/dev/null; sudo systemctl stop systemd-zram-setup@zram0.service
sudo rm -f /etc/systemd/zram-generator.conf /etc/sysctl.d/99-zram.conf
sudo systemctl daemon-reload
sudo pacman -R zram-generator          # optional: also remove the package
sudo sysctl vm.swappiness=60 vm.page-cluster=3   # restore live tunables (until next boot)
swapon --show; zramctl                 # confirm gone
```

---

Notes: office substrate change, local to this host only — does not deploy via `deploy.sh`
and touches no SSH/PHP/nginx/tailscale, so per the home PAD's own precedent this stays in
`journal.host-cleanup.md` and does not escalate to the Houston bus. Say the word once it's
live (or if STEP 4 fails) and the journal gets a one-liner either way.
