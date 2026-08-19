# redmi-15c-5g — device card

| Fact | Value |
|---|---|
| Tailscale IP | 100.105.201.3 |
| Android | TBD (modern MIUI/HyperOS expected — likely Android 13+) |
| Trust class | restrict (daily-carry phone; holds operator's Google account) |
| Termux | installed per operator; sshd state unknown |
| Tailnet connectivity | ❌ offline (last seen 2026-08-18) — Tailscale app likely disconnected |
| PC→device key auth | not seated |
| Device→PC access | none intended (doctrine: default-deny; JIT via passphrase key if needed) |
| Wireless debugging | likely available (Android 11+) — no USB needed for adb, if ever wanted |

## Open

- Bring on tailnet: open Tailscale app → connect
- Run `_shared/termux-bootstrap.md` steps 1–2
- Verify Android version + wireless debugging availability

## Notes

- The Tailscale app here is logged into the tailnet admin identity (Google account) —
  this device in the wrong hands = admin console access. 2FA posture matters more than
  any on-device hardening.
