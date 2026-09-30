# redmi-15c-5g — device card

| Fact | Value |
|---|---|
| Tailscale IP | 100.105.201.3 |
| Android | **15**, model **2508CRN2BE** (live check 2026-09-29) |
| Trust class | restrict (daily-carry phone; holds operator's Google account) |
| Termux | `googleplay.2026.06.21` (live check 2026-09-29); sshd on 8022 |
| Tailnet connectivity | ✅ online 2026-09-29; Termux SSH verified from both hosts |
| Termux sshd | ✅ key-only (PasswordAuthentication no, hardened 2026-08-20) |
| PC→device key auth | ✅ office RSA + home ed25519 — both seated 2026-08-20 |
| Device→PC access | Writable tmux on both hosts through registered encrypted device key; create/type/execute/detach/reconnect and UTF-8 tests passed 2026-09-29 |
| Host shortcuts | `office` / `home` use `~/bin/bed` with an SSH terminal; fresh shell or `source ~/.bashrc` after the 2026-09-29 update |
| Shift keys | Same shared `S-TAB` macro (`SHIFT TAB`) and `SHIFT` button as Galaxy; deployed and reloaded 2026-09-29 |
| Home display | Forced command uses `tmux -u` (2026-09-29); reconnected Redmi client verified `client_utf8=1`, operator confirmed symbols look correct |
| Wireless debugging | likely available (Android 11+) — no USB needed for adb, if ever wanted |
| Device→PC JIT access | ✅ ed25519 key, restricted entry (agentive tmux, from= guard). Use `ssh hruzam@<pc-ip>` |

## Open

- Banner test (screen-off 10+ min acceptance gate) — wakefulness not yet proven under sleep

## Notes

- The Tailscale app here is logged into the tailnet admin identity (Google account) —
  this device in the wrong hands = admin console access. 2FA posture matters more than
  any on-device hardening.
- Temp password set 2026-08-21 (old one burned by being typed visibly) — set a new one
  on device before running `ssh-copy-id`.
