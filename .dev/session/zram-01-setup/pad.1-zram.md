# zram — copy-paste setup sheet (home, hruzam)

Compressed RAM swap, to give the machine headroom under memory pressure (no swap exists today).
Copy a block, run it. Needs **sudo**. Fully reversible — the UNDO block at the bottom removes
every trace.

Verified on home 2026-09-23: `zram-generator 1.2.1-1` in `extra`, no swap/zram present, no
existing config, live `swappiness=60 page-cluster=3`, 9.6 GB RAM, 8 CPUs, zstd available.

Sizing: `ram / 2` ≈ 4.8 GB compressed device, costing ~1.5 GB real RAM when full → net ~2–3 GB
headroom. Idle Firefox/claude pages compress well; incompressible data does not shrink.

---

## 0 — state before (nothing to undo if you stop here)

```bash
swapon --show; zramctl; echo "swappiness=$(cat /proc/sys/vm/swappiness) page-cluster=$(cat /proc/sys/vm/page-cluster)"
```

Expect: blank swap/zram, `swappiness=60 page-cluster=3`.

## 1 — install the generator

```bash
sudo pacman -S zram-generator
```

## 2 — write the zram config

```bash
sudo tee /etc/systemd/zram-generator.conf >/dev/null <<'EOF'
[zram0]
zram-size = ram / 2
compression-algorithm = zstd
swap-priority = 100
EOF
cat /etc/systemd/zram-generator.conf
```

## 3 — activate now (also auto-starts on every boot)

```bash
sudo systemctl daemon-reload && sudo systemctl start systemd-zram-setup@zram0.service
```

## 4 — verify it's live

```bash
zramctl && swapon --show
```

Expect: a `/dev/zram0` device (~4.8 GB, zstd) and a swap line with priority 100.

## 5 — (optional) tune the kernel to lean on zram early

Swapping to RAM is cheap, so a high swappiness + zero page-cluster suits zram. Skip if you
prefer defaults.

```bash
sudo tee /etc/sysctl.d/99-zram.conf >/dev/null <<'EOF'
vm.swappiness = 180
vm.page-cluster = 0
EOF
sudo sysctl --system | grep -E "swappiness|page-cluster"
```

Expect: `vm.swappiness = 180`, `vm.page-cluster = 0`.

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

Notes: this is a **home substrate change** — it does not deploy to office; repeat there
separately if wanted. Repo rule says durable substrate changes belong in
`journal.host-cleanup.md`; say the word and I'll log a one-liner so the next ad-hoc seat sees it.
zstd vs lz4: zstd gives better ratio at trivial CPU cost on 8 cores — fine here. To cap the
device instead of `ram / 2`, use `zram-size = min(ram / 2, 4096)`.
