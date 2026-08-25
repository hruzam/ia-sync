---
name: adb-pull
description: >
  Pull a file or directory from an Android phone/tablet to a local destination.
  Use when the operator says "get file X from tablet/phone to Y", "pull <path> off my
  phone", or similar — grabbing something off a connected Android device onto this
  workstation. Prefers adb over USB (fastest, most reliable); falls back to MTP
  (gio mount) if adb isn't available or the device isn't listed. Always verifies the
  pulled file with a local size check.
---

When this skill is active I move a file or folder off an Android device onto this
workstation, preferring the fastest reliable path and verifying what actually landed.

## Procedure

1. **Check adb first** — this is the fast path:
   ```bash
   adb devices -l
   ```
   - Device listed as `device` → authorized, go straight to pull (step 3).
   - Device listed as `unauthorized` → tell the operator to accept the RSA prompt on the
     device screen, then re-run `adb devices -l`.
   - Nothing listed, or `adb: command not found` → fall back to MTP (step 2).
   - Only reachable over tailnet (no cable) with adb-over-network already enabled on the
     device: `adb connect <tailnet-ip>:5555`, then retry `adb devices -l`. One-line
     fallback only — don't build anything around this.

2. **MTP fallback** (only if adb didn't work):
   ```bash
   gio mount -l
   gio mount -d <device>   # if not auto-mounted
   ```
   If `gio` finds nothing and no MTP tooling is installed, tell the operator to install
   `jmtpfs` or `mtp-tools` and stop there — don't attempt a manual FUSE mount myself.

3. **Pull with adb** once a device is confirmed:
   ```bash
   adb pull "<device-path>" "<local-dest>"
   ```
   - Default `<local-dest>` to `~/Downloads` if the operator didn't specify one, keeping
     the original filename.
   - Works for both a single file and a whole directory — no special-casing needed.

4. **Verify** every pull:
   ```bash
   ls -lh "<local-dest>"
   ```
   Report the resulting size back to the operator to confirm the transfer looks intact
   (non-zero, roughly matches what was expected).

## Guardrails

- adb over USB is the default path — only fall back to MTP when adb genuinely isn't an
  option (not installed, device not listed).
- Don't silently retry `adb connect` in a loop — one attempt, report the result.
- Don't skip the `ls -lh` verification step; a pull that returns exit 0 but a truncated
  file is the failure mode this guards against.
