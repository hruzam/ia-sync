# Machine Resource Control — @home

`status: active`
`since: 2026-05-18`
`machine: home (Manjaro KDE Plasma, Ryzen 5 3500U, 9.6GB RAM)`
`authority: @majkee`

---

## Problem this solves

9.6 GB RAM, no swap by default. Firefox + Cursor + VS Code (all Electron or heavy JS) can exhaust available memory. Without swap, the kernel stalls trying to reclaim pages — the system freezes rather than degrading gracefully. This setup prevents that.

---

## Layer 1 — Kernel: zswap

Compressed in-RAM swap. No disk wear, ~2× effective RAM headroom under pressure.

**Install (one-time, requires reboot):**
```bash
sudo sed -i 's/quiet splash/quiet splash zswap.enabled=1 zswap.compressor=lz4 zswap.max_pool_percent=20/' /etc/default/grub
sudo grub-mkconfig -o /boot/grub/grub.cfg
# reboot
```

**Verify after reboot:**
```bash
cat /sys/module/zswap/parameters/enabled   # should print Y
```

---

## Layer 2 — OOM prevention: earlyoom

Kills the heaviest suspect process at 15% free RAM — before the kernel freezes trying to decide.

**Install:**
```bash
sudo pacman -S earlyoom
```

**Configure** `/etc/default/earlyoom`:
```
EARLYOOM_ARGS="-r 60 -m 15 -s 0 --avoid '(plasmashell|kwin_wayland|Xwayland|sddm)' --prefer '(firefox|cursor|code)'"
```
- `-m 15` — trigger at 15% free RAM (edit this to tune aggression)
- `--prefer` — targets freeze suspects first
- `--avoid` — never kills compositor or desktop shell

**Enable:**
```bash
sudo systemctl enable --now earlyoom
sudo systemctl status earlyoom
```

---

## Layer 3 — Agent tooling: ramguard MCP server

A local MCP server exposing RAM tools to Claude Code agents (@Mlok, etc.).

**Location:** `~/.claude/mcp/ramguard/server.py`
**Config:** `~/.claude/mcp/ramguard/config.json`

```json
{
  "threshold_warn_percent": 15,
  "suspects": ["firefox", "cursor", "code"],
  "protected": ["plasmashell", "kwin_wayland", "Xwayland", "sddm"]
}
```

**Dependencies:**
```bash
pip3 install --user --break-system-packages mcp psutil
```

**Registration** (already done, recorded here for new machine setup):
```bash
claude mcp add ramguard python3 ~/.claude/mcp/ramguard/server.py
```

**Tools exposed:**
- `ram_status` — full RAM/swap + top 10 consumers
- `freeze_suspects` — firefox/cursor/code footprint only
- `kill_process(pid, confirm=True)` — SIGTERM with protected-process guard

---

## Layer 4 — CLI: ramwatch

Human-facing script. Source of truth: `~/bin/ramwatch` (backed up via `my-env-sync`).

```bash
ramwatch               # full report
ramwatch --suspects    # freeze apps only
ramwatch --kill 1234   # interactive kill
```

---

## Layer 5 — KDE login: numlockx autostart

**File:** `~/.config/autostart/numlockx.desktop`

Activates Num Lock at KDE session start (phase 1, before most apps). No reboot needed — active on next login.

**SDDM login screen** (requires sudo, one-time):
```bash
echo -e '\n[General]\nNumlock=on' | sudo tee -a /etc/sddm.conf.d/kde_settings.conf
```

---

## Agent/tool backup note

`~/.claude`, `~/.gemini`, `~/.cursor` are backed up by `sync-env.zsh backup` — excluding `*.jsonl`, `sessions/`, `tmp/`. This includes the ramguard MCP registration in `~/.claude.json` and `~/.claude/mcp/`.

When restoring to a new machine: run `sync-env.zsh sync`, then reinstall Python deps (Layer 3) and run the sudo commands (Layers 1, 2, 5) manually.

---

## Tuning reference

| What to change | Where |
|---|---|
| earlyoom threshold | `/etc/default/earlyoom` → `-m <percent>` |
| ramguard warn threshold | `~/.claude/mcp/ramguard/config.json` → `threshold_warn_percent` |
| ramguard suspects/protected | same config.json |
| zswap pool size | `/etc/default/grub` → `zswap.max_pool_percent=<n>` |
