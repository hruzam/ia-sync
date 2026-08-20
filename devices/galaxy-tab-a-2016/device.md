# galaxy-tab-a-2016 — device card

| Fact | Value |
|---|---|
| Tailscale IP | 100.127.230.71 |
| Android | ~8.1 (verify with `getprop ro.build.version.release` once office key seated) |
| Patch state | EOL since ~2019 — **trust class: contain** |
| Termux | installed; sshd on 8022, key-only (hardened 2026-08-20) |
| Tailnet connectivity | via DERP relay (no direct path observed) |
| home → device key auth | ✅ home ed25519 seated 2026-08-19 |
| office → device key auth | ✅ office RSA relayed via home 2026-08-20 |
| Device→PC access | ✅ **CLOSED** — ACL applied 2026-08-21; androids→PCs tcp:22 only; Tailscale SSH back to check/nonroot. Verified denied from tablet. |
| Wireless debugging | not possible (pre-Android-11); adb needs USB-first `adb tcpip 5555` |

| Device→PC JIT access | ✅ ed25519 key, read-only restricted entry (agentive tmux -r, from= guard). Use `ssh hruzam@<pc-ip>` |

## Open

- Banner test (screen-off 10+ min acceptance gate) — wakefulness not yet proven under sleep
- Verify Android version (`getprop ro.build.version.release`)

## Notes

- 2026-08-18: built-in recorder issue resolved by operator directly (alternate app;
  recordings recovered from Android/data). No agent action taken on-device.
- 2026-08-19: tablet demonstrated passwordless `ssh hruzam@hruzam` into home host —
  Tailscale SSH, tailnet-identity auth. The weak spot, confirmed live.
