# tmux sessions, windows, panes

tmux hierarchy:

```text
server → session → windows → panes
```

A target is `session:window.pane`. Real office example: `agentive:1.0` means
session `agentive`, window `1`, pane `0`.

## Most used

```sh
tmux ls                                  # what sessions exist
tmux list-windows -a                     # every window, every session
tmux list-clients                        # who is attached where (collision check)
tmux attach -t default_2                 # attach — ONLY if nobody else is on it
t41 default_2 audit                      # 2nd+ terminal → own view, locked to 'audit'
tmux detach-client -t /dev/pts/NN        # kick a stray twin client
```

Inside tmux, after `Ctrl-b`: `s` session tree · `w` window tree · `d` detach ·
`c` new window · `0`–`9` jump window · `z` zoom pane.

Never bare `tmux attach` from a second terminal — see "Find and attach safely".

## Sessions

List sessions:

```sh
tmux list-sessions
```

Create a new named session:

```sh
tmux new-session -s work
```

Attach if present, create if absent (`agentive` is real on office):

```sh
tmux new-session -A -s agentive
```

Attach only; fail if missing:

```sh
tmux attach-session -t agentive
```

Read-only attach:

```sh
tmux attach-session -rt agentive
```

From another machine → office `agentive`:

```sh
ssh -t hruzam@100.126.182.111 'tmux new-session -A -s agentive'
```

Detach without stopping anything: `Ctrl-b`, then `d`.

## More windows in one session

List windows:

```sh
tmux list-windows -t agentive
```

Create and name a window:

```sh
tmux new-window -t agentive -n work
```

Create a window already running a command:

```sh
tmux new-window -t agentive -n repo 'cd /home/hruzam/ia-sync && exec zsh'
```

Attach and select real office window `1`:

```sh
tmux attach-session -t agentive \; select-window -t agentive:1
```

Inside tmux, after the `Ctrl-b` prefix:

- `c` — new window
- `w` — window chooser
- `n` / `p` — next / previous window
- `0`–`9` — select numbered window
- `,` — rename current window
- `&` — kill current window (asks first)

## Panes inside a window

List panes with full targets:

```sh
tmux list-panes -s -t agentive -F '#{session_name}:#{window_index}.#{pane_index} #{pane_current_command}'
```

Split window `1` side-by-side or top/bottom:

```sh
tmux split-window -h -t agentive:1
tmux split-window -v -t agentive:1
```

Select pane `0` explicitly:

```sh
tmux select-pane -t agentive:1.0
```

Inside tmux, after `Ctrl-b`:

- `%` — split left/right
- `"` — split top/bottom
- arrow key — move between panes
- `o` — move to next pane
- `z` — zoom/unzoom current pane
- `x` — kill current pane (asks first)

## Popup without changing the layout

Show a file, scroll with `less`, then return to the same panes:

```sh
tmux display-popup -w 85% -h 85% -E 'less -R /home/hruzam/ia-sync/devices/_shared/agentive-tmux.md'
```

## Named buffer

Load a file without replacing the default buffer:

```sh
tmux load-buffer -b agentive-help /path/to/note.md
```

Paste it into real office pane `agentive:1.0`, or inspect it first:

```sh
tmux paste-buffer -b agentive-help -t agentive:1.0
tmux show-buffer -b agentive-help
```

List or delete named buffers:

```sh
tmux list-buffers
tmux delete-buffer -b agentive-help
```

## Find and attach safely (no twin windows)

Twin windows: two terminals on the same session always show the same window —
"current window" belongs to the **session**, not the terminal. Bare
`tmux attach` grabs the most-recently-used session, so a second terminal
silently lands on top of the first.

**1. Find** — what exists, and what is already occupied:

```sh
tmux list-sessions -F '#{session_name}: #{session_windows} windows'
tmux list-windows -a -F '#{session_name}:#{window_index} #{window_name}'
tmux list-clients -F '#{client_tty} -> #{session_name}'
```

**2. Decide** — is the target session in the `list-clients` output?

- no client on it → plain attach is safe: `tmux attach -t default_2`
- already has a client → join instead (step 3), or you get twin windows

`Ctrl-b s` (tree browser) has the same trap: `Enter` on an occupied session
makes you its second client.

**3. Join** — own view on shared windows/panes, reuse if it already exists:

```sh
tmux attach -t default_2-audit 2>/dev/null \
  || tmux new-session -t default_2 -s default_2-audit \; select-window -t default_2-audit:audit
```

Shortcut (experimental brick, same logic): `t41 default_2 audit`. One join per
bed — 4 terminals on 4 windows = `t41 default_2 cSharp|bus|implement|audit`.

Avoid `new-session -A -t ... \; select-window` — when the session exists, `-A`
attaches (and blocks) before `select-window` runs.

Killing a joined view (`tmux kill-session -t default_2-audit`) closes only that
view; the shared windows live on in `default_2`.

**Fix a twin already in place:** `tmux detach-client -t /dev/pts/NN`, then
re-enter that terminal via step 3.

## Stop deliberately

These terminate running shells/programs:

```sh
tmux kill-window -t agentive:1
tmux kill-session -t agentive
```
