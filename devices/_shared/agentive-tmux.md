# agentive — tmux session convention

The `agentive` tmux session is the device→PC access landing zone.
Devices SSH into a PC and are forced by `authorized_keys` to attach to this session.

## Role by device

| Device | authorized_keys command | Access |
|---|---|---|
| redmi-15c-5g | office: `tmux new-session -A -s agentive`; home: `tmux -u new-session -A -s agentive` | read+write (creates if absent) |
| galaxy-tab-a-2016 | office: `tmux new-session -A -s agentive`; home: `tmux -u new-session -A -s agentive` | read+write (operator amendment, 2026-09-29) |

## Usage

Start an agent session on a PC you want accessible:
```sh
tmux new-session -s agentive    # or: tmux new-session -A -s agentive
claude --agent flight            # or any agent invocation
```

From either device, `bed office` / `bed home` opens writable tmux. The connector
unlocks that device's own key through ssh-agent; the passphrase stays on-device.
Both devices' `office` / `home` aliases use this connector after a fresh shell or
`source ~/.bashrc`. Direct `ssh -t hruzam@<pc-ip>` remains available.

Use `office` or `bed office` in local Termux. The old `office` alias was plain SSH:
`office bed` therefore sent a remote command without requesting a terminal, and
the host's forced tmux command failed with `open terminal failed: not a terminal`.
The current aliases use `bed`, which explicitly requests a terminal with `ssh -t`.

Switch sessions with **Ctrl+B, s**, windows with **Ctrl+B, w**; create a window with
**Ctrl+B, c**. To create another session, **Ctrl+B, :** then `new-session -s NAME`.
Detach with **Ctrl+B, d** (or the extra-row DETACH key); remote work keeps running.

Both chooser keys use the current tmux server: `s` starts at sessions, `w` expands
their windows. On office, the devices land on the `default` server, which also holds
ovitmugen's agent sessions. Ovitmugen's separate `ovitmugen` server contains frames
with a **Ctrl+A** prefix; those frames do not appear in the default server's chooser.

## Per-PC agentive

Both devices' home entries explicitly use `tmux -u`: home's SSH connection does not
carry a UTF-8 locale, so an unqualified tmux client replaced non-ASCII glyphs.
This flag fixes output encoding; the device font is a separate setting. Existing
clients need one detach/reconnect to use the corrected command; sessions survive.

Each PC has its own `agentive` session. Devices connect to a specific PC by IP:
- office: `ssh hruzam@100.126.182.111`
- home:   `ssh hruzam@100.110.27.60`

## Termux tips

**Visible output but typing does nothing:** if tmux is in copy/scroll mode, press
**q** to return to the shell. A writable client can still be in copy mode (Galaxy
case verified 2026-09-29); that is separate from SSH read-only restrictions.

**Kill a stuck session (broken pipe / SSH hung):**
Long-press anywhere on the terminal area → popup: COPY | PASTE | MORE → tap MORE → **Kill session**.
Opens a new clean session. The `agentive` tmux on the PC is unaffected — SSH broken pipe
auto-detaches the client; reconnect with `office` or `home` from the new session.

**Reconnect after screen lock drops Tailscale:**
Open Tailscale app → wait for green on all nodes → then `office` / `home` in a new session.
MIUI fix: Settings → Apps → Manage apps → Tailscale → Battery saver → No restrictions + Autostart on.
Samsung fix: Battery → Background usage limits → Never sleeping apps → add Tailscale + Termux.

## Notes

- The `from=` guard restricts each key to its device's tailnet source IP. It does not
  contain a compromised device that can still reach the tailnet.
- Redmi passphrase lives only in the operator's head.
- Tablet passphrase lives only in the operator's head.
- If `agentive` doesn't exist, either device creates it via `new-session -A`.
- Writable tmux permits shell commands as the host user. The forced command is a
  landing convention, not a sandbox; native model approval settings remain separate.
