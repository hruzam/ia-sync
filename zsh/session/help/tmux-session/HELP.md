# tmux sessions, windows, panes

tmux hierarchy:

```text
server → session → windows → panes
```

A target is `session:window.pane`. Real office example: `agentive:1.0` means
session `agentive`, window `1`, pane `0`.

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

## Stop deliberately

These terminate running shells/programs:

```sh
tmux kill-window -t agentive:1
tmux kill-session -t agentive
```
