# Next-session prompt — device access layer (paste as opening message)

Continue the device-access work from session `REP.office.oraculum-fable` (2026-08-18 → 21).

## Orient first (read in this order)
1. `~/ia-sync/devices/README.md` — doctrine + inventory
2. `~/ia-sync/devices/galaxy-tab-a-2016/log.md` and `~/ia-sync/devices/redmi-15c-5g/log.md` — device state
3. `~/ia-sync/devices/_shared/termux-bootstrap.md` — REVISED push-flow (devices never pull; PCs are key-only)
4. `~/ia-sync/journal.host-cleanup.md` — 2026-08-20 entries (hardening, db-reach)
5. `~/ia-sync/zsh/system/tailscale.zsh` — existing ts/db-reach engine (extend, don't duplicate)
6. `~/ia-sync/install-pkgs/README.md` — task contract, if anything needs reproduction on both hosts

## State (as of session close 2026-08-21, ~05:00)
- Both PCs hardened (harden-host 1.0): MariaDB loopback, sshd key-only, ufw.
- Tailnet ACL live (grants dialect): computers full mesh; androids → office/home **tcp:22 only**;
  Tailscale SSH = check/nonroot + `--ssh=false` on hosts. Verified from the tablet (denied publickey;
  3306 times out). db-reach verified office→home live.
- Tablet: home key seated & verified. Office key NOT seated (pull-flow died against key-only sshd).
- Redmi: openssh installed, sshd started once, NO keys seated, temp password BURNED (typed visibly) —
  set a fresh one.
- **KEY FINDING (2026-08-21 ~05:00): both devices' Termux sshd goes silent when screens sleep** —
  TCP accepts (kernel) but no SSH banner (frozen process). Android app-freezers beat termux-wake-lock.
  All device-side SSH work requires the device AWAKE + Termux FOREGROUND, until fixed properly.

## Step 0 — device wakefulness (prerequisite for everything below)
1. On BOTH devices: battery exemption for Termux + Tailscale (Redmi/MIUI: Manage apps →
   Battery saver → No restrictions + autostart; Samsung: Battery → Unmonitored/Never sleeping apps).
2. Pin Termux in Recents (lock icon) on both.
3. Consider `Termux:Boot` addon (F-Droid; must match Termux install source) to autostart
   `sshd + termux-wake-lock` on boot — evaluate in-session.
4. Re-test banner from a PC: `timeout 5 bash -c 'exec 3<>/dev/tcp/<dev-ip>/8022; head -c 32 <&3'`
   → must print `SSH-2.0-…` with the device screen OFF for 10+ min. That is the acceptance gate.

## Step 1 — finish key seating (push-flow, devices awake)
- Redmi: `passwd` (fresh), then from a PC: `ssh-copy-id -p 8022 -o StrictHostKeyChecking=accept-new 100.105.201.3`,
  then relay the other PC's key (see termux-bootstrap.md §2).
- Tablet: relay office key via home (home→tablet key works):
  `ssh hruzam@100.126.182.111 'cat ~/.ssh/id_*.pub' | ssh -p 8022 100.127.230.71 'cat >> ~/.ssh/authorized_keys'`
- Verify from both PCs: `ssh -p 8022 <dev-ip> 'echo OK'`.
- Host-key fingerprints for first contact: home ED25519 `SHA256:AYQ8YIZiUxYSZnMXiq8VH/Csw8uygQ81tf86WPWmRBO`,
  office ED25519 `SHA256:Zu4j+Cuu8P9dpuQPoHpEPFnq8fB3EckdgjrDUwe/s/U`.

## Step 2 — the JIT device→PC access build (the main goal)
1. **Keygen on each device** (operator's hands): `ssh-keygen -t ed25519` WITH a strong passphrase
   (lives only in operator's head, never in files).
2. **PC-side restricted entries** in `~/.ssh/authorized_keys` on office + home — operator pastes
   (classifier blocks agents from writing these, correctly):
   - Redmi (field phone, interactive):
     `command="tmux attach -t agentive",no-port-forwarding,no-agent-forwarding,no-X11-forwarding,from="100.105.201.3" ssh-ed25519 AAAA… redmi`
   - Tablet (reader, weakest device, read-only):
     `command="tmux attach -rt agentive",no-port-forwarding,no-agent-forwarding,no-X11-forwarding,from="100.127.230.71" ssh-ed25519 AAAA… tab`
3. **tmux convention**: an `agentive` session on each PC where Claude/Codex runs; document in
   `devices/_shared/` (note existing tmux-pin-bus + netOrchestrating primitives — build on them).
4. **Termux sshd → key-only** on both devices after both PC keys verified
   (`$PREFIX/etc/ssh/sshd_config`: `PasswordAuthentication no`, restart sshd). Temp passwords die here.
5. Update device cards + logs; if steps are reproducible, cut an `install-pkgs` task (manual).

## Gates
- Operator gavels every `authorized_keys` edit on the PCs.
- Test matrix before closing: redmi→office attach works; tab→home read-only attach works and
  CANNOT inject keystrokes; both devices still blocked from everything non-22; banner test passes
  with screens off (Step 0.4).

## Housekeeping
- ia-sync commit: `devices/`, `zsh/.config/tailnet.access-controls.json`, this file.
- Consider relocating the ACL reference copy out of `zsh/.config/` (deploys to an odd nested path).
