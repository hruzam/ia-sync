---
card: guide.remote-control
brand: Anthropic — Claude Code · Remote Control
kind: knowledge-card · RELATIVE (volatile, RAG-refreshable)
verified: 2026-08-15
half_life: ~4-6 weeks
half_life_days: 42
recheck:
  - https://code.claude.com/docs/en/remote-control
  - https://code.claude.com/docs/en/desktop-linux
  - https://github.com/anthropics/claude-code/releases
verify_cmd: claude --version
---

# Remote Access — Claude Code

## VOLATILE — read first

- Requires claude >= v2.1.51. Check: `claude --version`
- Requires Pro, Max, or Team plan. Remote Control is not available on Free tier.
- Feature flag may change; verify against changelog before debugging an outage.

---

## Overview

Two approaches to run Claude Code sessions accessible from a mobile phone:

- **Approach A (systemd)** — always-on. Services start at boot, restart on failure. Best for
  projects you want permanently available without manual action.
- **Approach B (rc.sh / tmux)** — on-demand. You launch a session when you need it, attach
  from anywhere. Lower overhead; no background processes when idle.

Both expose the session via Claude's Remote Control protocol (outbound HTTPS only, no open
inbound ports). The Claude mobile app connects via `claude.ai/code`.

---

## Requirements

| Requirement | Detail |
|-------------|--------|
| claude CLI | >= v2.1.51 |
| Plan | Pro / Max / Team |
| Network | Outbound HTTPS (443) — no inbound ports needed |
| tmux | Approach B only |
| Tailscale | SSH fallback only (Approach C) |

---

## Approach A — systemd (always-on)

### How it works

A `Type=simple` user service runs `claude remote-control --name "<project>"` in the project
directory. The service restarts automatically on failure with a 15-second backoff. Services
depend on `network-online.target` so they wait for connectivity before starting.

### Setup (enable services)

```bash
# Reload systemd after creating service files
systemctl --user daemon-reload

# Enable individual services
systemctl --user enable claude-rc-freya.service
systemctl --user enable claude-rc-reposoma.service
systemctl --user enable claude-rc-nabla-lab.service
```

### Enable on boot

Requires lingering to be enabled so user services survive logout:

```bash
loginctl enable-linger hruzam
```

### Management commands

```bash
# Start
systemctl --user start claude-rc-freya.service

# Stop
systemctl --user stop claude-rc-freya.service

# Status
systemctl --user status claude-rc-freya.service

# Logs (live)
journalctl --user -u claude-rc-freya.service -f

# Logs (last 50 lines)
journalctl --user -u claude-rc-freya.service -n 50
```

Replace `freya` with `reposoma` or `nabla-lab` as needed.

### Projects registered

| Service file | Project | WorkingDirectory |
|---|---|---|
| `claude-rc-freya.service` | Freya | `/home/hruzam/www/imago_cz/freya` |
| `claude-rc-reposoma.service` | Reposoma | `/home/hruzam/reposoma` |
| `claude-rc-nabla-lab.service` | Nabla Lab | `/home/hruzam/nabla-lab` |

Service files location: `~/.config/systemd/user/`

---

## Approach B — tmux on-demand (rc.sh)

### How it works

`rc.sh` reads the project registry (`~/.config/zsh/registries/ai.json`, key `remote-control`)
and manages named tmux sessions. Each session runs `claude remote-control --name "<project>"` in
the project directory. Sessions persist until explicitly stopped or the machine reboots.

Requires `jq` and `tmux`.

### Usage

```bash
# List all projects and current session status
rc.sh

# Start or attach RC session for a project
rc.sh freya
rc.sh reposoma
rc.sh nabla-lab

# Show status of all sessions
rc.sh status

# Stop a session
rc.sh freya stop
```

### Session lifecycle

1. First call to `rc.sh <project>` — creates a detached tmux session, starts `claude remote-control`,
   then attaches your terminal to it.
2. Detach from session — press `Ctrl-b d`. The RC process keeps running.
3. Re-attach from any terminal — `rc.sh <project>` again.
4. Stop — `rc.sh <project> stop` kills the tmux session and the RC process.

Script location: `~/.config/zsh/ai/rc.sh`

---

## Approach B+ — agent-aware engine + `/rc-launch` skill (2026-08-15)

The tmux engine (`ai/rc.sh`) was generalized and a phone-friendly launcher skill added.
Absorbs the proven `spawn-rc-term.sh` (real pty + render polish), which is now retired.

### What changed in `rc.sh`
- **Any project** launches, not just the registered trio — paths resolve from
  `registries/projects.json` (authoritative; `ai.json` path is a fallback for `nabla-lab`,
  which is intentionally absent from the map).
- **agent / model / effort** are first-class:
  `rc.sh <project> [--agent a] [--model m] [--effort e] [--name N] [--detach]`.
  Defaults come from `ai.json` → `remote-control.launch-defaults` (model=opus, effort=high,
  per-project agent). Empty agent → claude's default agent (preserves `rc-freya`/`rc-nabla`).
- **Real pty + render polish** folded in: attach with `tmux -u -2` (UTF-8 glyphs — spinner,
  pointers, logo — plus 256-color), `allow-passthrough on`, per-session `status off`.
- **`--detach`** starts a catchable session and prints the three reach lines instead of
  attaching (the headless / agent / cross-host path). Auto-detaches when there is no TTY.

### `/rc-launch` skill (the phone front)
Invoke `/rc-launch` and say e.g. "launch flight on nablarva at office". The skill gathers
`{host, project, agent, model, effort}` — host + project + agent required (asks if missing),
model + effort default — checks the host is reachable, then dispatches the engine:
- **local** (host == this box): `bash ai/rc.sh <project> --agent … --detach`
- **remote** (cross-host): `ssh <user>@<tailscale_dns> -t 'bash ai/rc.sh <project> … --detach'`

### Registries (data lives in JSON; zsh stays a clean executive)
| file | holds |
|---|---|
| `registries/projects.json` | authoritative project → path (GENERATES `temple-project-map.zsh` at deploy via `gen-temple-map.sh`) |
| `registries/ai.json` → `remote-control.launch-defaults` | model, effort, per-project agent |
| `registries/hosts.json` | host-label → tailscale identity + locality (cross-host dispatch) |

Cross-host needs the tailnet ssh link working (tailscale ssh or an authorized key). If ssh
fails, the skill reports the exact command tried — it does not fix auth. Origin of the
real-pty/glyph findings: `reposoma/raw.guides/remote-control/` (majkee, 2026-08-14/15).

---

## Approach C — SSH fallback via Tailscale

When no RC session was pre-started and you need access:

1. SSH into the machine via Tailscale: `ssh hruzam@<tailscale-ip>`
2. Start a tmux session manually: `tmux new -s fallback`
3. Navigate to the project directory and run: `claude remote-control --name "Manual"`
4. Detach and connect from the Claude app.

Get current Tailscale IP: `tailscale ip -4`

---

## Connecting from mobile

1. Open the Claude app on iOS or Android.
2. Go to the **Code** tab (bottom nav).
3. Select **Connect to desktop** — scan QR code or navigate to `claude.ai/code`.
4. The active RC session appears and you can attach to it.

---

## Troubleshooting

**RC connection dropped overnight (tmux approach)**

tmux sessions survive, but the RC protocol has a ~10-minute network idle timeout.
Run `/remote-control` inside the Claude session to reconnect without restarting the session.

**"Remote Control not yet enabled"**

Plan check: feature requires Pro, Max, or Team. Free plan shows this error.

**systemd service fails to start / `claude not found`**

The service uses `/usr/bin/env claude`. If `claude` is installed via a user-local package manager
(e.g. npm in `~/.local/...`), set `Environment=PATH=...` in the service file to include that path.
Check with: `which claude`

**tmux session shows running but RC is not reachable**

The `claude remote-control` process inside the session may have exited. Attach to the session
(`rc.sh <project>`), check the terminal output, and restart the command if needed.

---

## Machine scope

This guide covers the **home machine** (Manjaro, hruzam). The `available` flag in the registry
controls which projects rc.sh will launch on a given machine. Set `"available": false` for any
project that does not reside on the current machine — rc.sh will exit with an error rather than
silently failing.

Registry path: `~/.config/zsh/registries/ai.json` — key `remote-control.projects`.

To add a new project: extend the registry JSON with the new entry and create the corresponding
service file in `~/.config/systemd/user/` following the existing pattern. Run
`systemctl --user daemon-reload` after adding the service file.

---

**Last Updated:** 2026-08-15  
**Machine:** home (Manjaro)
