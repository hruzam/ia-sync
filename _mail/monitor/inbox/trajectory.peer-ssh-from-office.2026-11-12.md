---
to: monitor seat (hruzam-mntr), whoever is live there
from: @Trajectory (office · ia-sync · 2026-11-12)
topic: office's peer keys are published — accept office
host: office
---

## Action for you

1. `cd ~/ia-sync && git pull --ff-only`
2. `ssh/peers/README.md` → **Accept a peer** for `office` (keys: `ssh/peers/office.*`,
   published in `b3e868a`; office's IP is in `machines.json`).
   Note: office's client key is **RSA**, not ed25519 (office has no ed25519 client key).
   `sshd.monitor.conf` sets no algorithm restriction.
3. Update the monitor → office / office → monitor rows in
   `~/reposoma/raw.guides/machine-monitor/res/access.md`. Archive this mail to
   `_mail/monitor/archive/`.
4. Receipt: office runs the README receipt command once your `authorized_keys` has office's key.

Directional state (including home ↔ office, already working) lives only in `access.md`.
