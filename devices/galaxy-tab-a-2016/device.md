# galaxy-tab-a-2016 — device card

| Fact | Value |
|---|---|
| Tailscale IP | 100.127.230.71 |
| Android | **8.1.0 / API 27**, Samsung **SM-T585**, `armeabi-v7a` (live check 2026-09-29) |
| Patch state | EOL since ~2019 — **trust class: contain** |
| Termux | **0.118.1 / F-Droid**, arm packages (checked 2026-09-29); sshd on 8022, key-only |
| Tailnet connectivity | online 2026-09-29; Termux SSH verified from office and home |
| home → device key auth | ✅ home ed25519 seated 2026-08-19 |
| office → device key auth | ✅ office RSA relayed via home 2026-08-20 |
| Device→PC access | **Writable tmux on office + home**, authorized by majkee 2026-09-29; native registered SSH key, source-IP restriction retained |
| Wireless debugging | not possible (pre-Android-11); adb needs USB-first `adb tcpip 5555` |
| Device→PC JIT access | Own encrypted ed25519 key; both hosts force `tmux new-session -A -s agentive` (home adds `-u` for UTF-8). Use `bed office` / `bed home`; passphrase entered on tablet only |
| Key fingerprint | `SHA256:UHP76eQdepkhSTgnDED9YRRFPIUKhFKKh6v6b0xm65U` — device public key matches both hosts |
| Termux convenience | Existing shared `bed`, extra keyboard row and widget scripts pushed 2026-09-29; `office` / `home` aliases use `bed`; Widget app itself not installed/verified |
| Shift keys | `S-TAB` sends Shift+Tab directly; `SHIFT` in the Termux row is separate from Android keyboard Shift; physical TAB/S-TAB byte check and operator confirmation passed 2026-09-29 |
| Terminal font | JetBrainsMono Nerd Font Regular, same SHA256 as Redmi; operator confirmed improved appearance 2026-09-29 |
| Writable access proof | Galaxy → office AND home: key auth, create session, type/execute, detach, reconnect **PASS** 2026-09-29 |
| Wired connection | Samsung USB device detected on office 2026-09-29; no ADB authorization claimed |

## Lock-screen check

- **PASS, operator report 2026-09-29:** session survived 10 minutes with Galaxy's screen locked. This closes the pending 10-minute session-survival check.

## Notes

- 2026-08-18: built-in recorder issue resolved by operator directly (alternate app;
  recordings recovered from Android/data). No agent action taken on-device.
- 2026-08-19: tablet demonstrated passwordless `ssh hruzam@hruzam` into home host —
  Tailscale SSH, tailnet-identity auth. The weak spot, confirmed live.
