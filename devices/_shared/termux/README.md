# Termux Agentive Bed

Phone ↔ office/home tmux workbench — 4 concurrent seat windows via single bed.

## Install

PC→device PUSH flow ONLY (per `/home/hruzam/ia-sync/devices/_shared/termux-bootstrap.md` law; devices never pull).

Target paths on device:
- `~/.termux/termux.properties` — merge `termux.properties` fragment + reload with `termux-reload-settings`
- `~/bin/bed` — phone-side + PC-side host connector
- `~/.shortcuts/office-attach` — Termux:Widget home-screen one-tap for office
- `~/.shortcuts/home-attach` — Termux:Widget home-screen one-tap for home
- `~/.termux/font.ttf` — JetBrainsMono Nerd Font (already pushed 2026-09-10)

## Device Provisioning (HyperOS)

After Termux install:

1. Battery saver: set "No restrictions" for Termux AND Tailscale (stops the HyperOS app freezer from killing SSH/VPN on background/lock — verified 2026-09-10)
2. Recents: pin Termux (fast re-entry)
3. Setup:
   - Start `sshd` — `sshd` in Termux terminal
   - Persistent wake-lock — `termux-wake-lock` in Termux terminal
   - Run after any Termux restart

## Usage

**Connect to a host:**
```bash
bed office     # office workbench (100.126.182.111)
bed home       # home workbench (100.110.27.60)
```

**From phone home-screen:**
- Tap `office-attach` or `home-attach` — one-tap Termux:Widget shortcut

**Keyboard:**
- `S1`–`S4` — switch between 4 seat windows (tmux window select)
- `PASTE` — Android clipboard paste (hands-free PTYRA voice loop: talk → ChatGPT copies result → tap PASTE)
- `DETACH` — close bed (Ctrl+B d)

**Approvals gate:** Codex may default to automatic review. Switch to asking mode with `/approvals` so approvals are real (gate law: approvals stay ON).

## Claude Both-Doors

One cloud seat, last claimer wins.

**Inside the bed (on attached host):**
```bash
~/.local/bin/claude <prompt>    # absolute path required; runs CLI against cloud seat
```

**Inside a living session:**
```
/remote-control    # rebind active app seat to this session's Claude context
```

The cloud seat persists across connections; `/remote-control` reassigns which session owns it.

## Add a Host

One row in `/home/hruzam/ia-sync/machines.json` + one case in `bin/bed`:
```sh
  my-host)
    IP="100.x.y.z"
    ;;
```

## Notes

- SSH from phone lands in `tmux new-session -A -s agentive` (forced command, cannot be overridden)
- Windows 1–4 are seat slots — multiple sessions can coexist in one bed
- absolute path required on hosts; claude never runs on the phone
