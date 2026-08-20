# agentive — tmux session convention

The `agentive` tmux session is the device→PC access landing zone.
Devices SSH into a PC and are forced by `authorized_keys` to attach to this session.

## Role by device

| Device | authorized_keys command | Access |
|---|---|---|
| redmi-15c-5g | `tmux new-session -A -s agentive` | read+write (creates if absent) |
| galaxy-tab-a-2016 | `tmux attach -rt agentive` | **read-only** (fails if absent — correct: nothing to watch) |

## Usage

Start an agent session on a PC you want accessible:
```sh
tmux new-session -s agentive    # or: tmux new-session -A -s agentive
claude --agent flight            # or any agent invocation
```

Then from Redmi (`ssh hruzam@<pc-ip>`) you land in it interactively.
From tablet (`ssh hruzam@<pc-ip>`) you get a read-only mirror — scroll history,
watch output, but cannot inject keystrokes.

## Per-PC agentive

Each PC has its own `agentive` session. Devices connect to a specific PC by IP:
- office: `ssh hruzam@100.126.182.111`
- home:   `ssh hruzam@100.110.27.60`

## Notes

- The `from=` guard in `authorized_keys` means each device key only works from its
  own tailnet IP — the key is useless if the device is compromised and off the tailnet.
- Redmi passphrase lives only in the operator's head.
- Tablet passphrase lives only in the operator's head.
- If `agentive` doesn't exist, Redmi creates it (via `new-session -A`);
  tablet gets a clean connection-closed (correct — nothing to read).
