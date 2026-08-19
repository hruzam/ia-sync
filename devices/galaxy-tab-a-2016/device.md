# galaxy-tab-a-2016 — device card

| Fact | Value |
|---|---|
| Tailscale IP | 100.127.230.71 |
| Android | ~8.1 (verify with `getprop ro.build.version.release` once office key seated) |
| Patch state | EOL since ~2019 — **trust class: contain** |
| Termux | installed; sshd on 8022 (manual start — dies on reboot/Termux kill) |
| Tailnet connectivity | via DERP relay (no direct path observed) |
| home → device key auth | ✅ works (home `id_ed25519` seated 2026-08-19 by operator) |
| office → device key auth | ❌ pending — operator to run office pull line (bootstrap step 2) |
| Device→PC access | ⚠️ **LIVE via Tailscale SSH** — tablet reached home shell passwordless 2026-08-19. Closes when ACL draft is applied. |
| Wireless debugging | not possible (pre-Android-11); adb needs USB-first `adb tcpip 5555` |

## Open

- Seat OFFICE pubkey (operator hands; relay append was classifier-blocked by design)
- Apply tailnet ACL (androids initiate nothing) — kills the live Tailscale-SSH path
- Verify Android version, package inventory
- Harden Termux sshd to key-only after both keys verified

## Notes

- 2026-08-18: built-in recorder issue resolved by operator directly (alternate app;
  recordings recovered from Android/data). No agent action taken on-device.
- 2026-08-19: tablet demonstrated passwordless `ssh hruzam@hruzam` into home host —
  Tailscale SSH, tailnet-identity auth. The weak spot, confirmed live.
