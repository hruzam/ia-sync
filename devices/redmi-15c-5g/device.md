# redmi-15c-5g — device card

| Fact | Value |
|---|---|
| Tailscale IP | 100.105.201.3 |
| Android | TBD (modern MIUI/HyperOS expected — likely Android 13+) |
| Trust class | restrict (daily-carry phone; holds operator's Google account) |
| Termux | installed; openssh installed 2026-08-21; sshd started once |
| Tailnet connectivity | ✅ online (verified ~2026-08-21) |
| Termux sshd | ✅ key-only (PasswordAuthentication no, hardened 2026-08-20) |
| PC→device key auth | ✅ office RSA + home ed25519 — both seated 2026-08-20 |
| Device→PC access | none intended (doctrine: default-deny; JIT via passphrase key if needed) |
| Wireless debugging | likely available (Android 11+) — no USB needed for adb, if ever wanted |

| Device→PC JIT access | ✅ ed25519 key, restricted entry (agentive tmux, from= guard). Use `ssh hruzam@<pc-ip>` |

## Open

- Banner test (screen-off 10+ min acceptance gate) — wakefulness not yet proven under sleep
- Verify Android version (`getprop ro.build.version.release`)
- Document tmux `agentive` convention (shared with tablet) in `_shared/`

## Notes

- The Tailscale app here is logged into the tailnet admin identity (Google account) —
  this device in the wrong hands = admin console access. 2FA posture matters more than
  any on-device hardening.
- Temp password set 2026-08-21 (old one burned by being typed visibly) — set a new one
  on device before running `ssh-copy-id`.
