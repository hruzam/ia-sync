# remote-cli

Host-side controls for living terminal sessions. The shared operator guide remains
`~/reposoma/raw.guides/remote-cli/GUIDE.md`; this folder owns the shell implementation.
Session history and live state stay with tmux and the application on the host.

Control-panel law: [zsh/AGENTS.md](../AGENTS.md#control-panel-convention-canonical--operator-gaveled-2026-07-07--tightened-2026-07-11).
`keyboard.zsh` contains aliases, `remote-cli.sh` contains the bash/zsh engine, and
`base.zsh` loads both through the existing `system/base.zsh` on office and home.
The `remote-*` family appears in `keys`; `rc-*` continues to mean Claude RC.

In an existing host shell, load once after deployment:

```zsh
source ~/.config/zsh/remote-cli/base.zsh
remote-help
```

| Command | Effect on the chosen window |
|---|---|
| `remote-fit [target]` | `window-size latest`: follow the most recently active client |
| `remote-wide [target]` | `window-size largest`: follow the largest attached client |
| `remote-status [target]` | Print target, effective policy and dimensions in character cells |

Omit the target inside a tmux shell to use its window. From another host terminal,
give a session/window or pane ID, for example `remote-fit 'agentive:0'`.
For an application already occupying the pane, press **Ctrl+B**, release, **:**,
and enter this tmux command (no shell alias needed):

```tmux
run-shell 'bash /home/hruzam/.config/zsh/remote-cli/remote-cli.sh fit "#{pane_id}"'
```

Change `fit` to `wide` or `status` as needed. This targets the window you are viewing.
No special launch step is needed; any existing tmux session can use these controls.
Connect through the existing doors: `bed office` on the phone, `tso -t office` from
another PC, then **Ctrl+B**, **s** to select a session.

The policy lasts until changed or the window closes; it affects all panes and linked
views of that window. New windows keep the global default. There is still one size
per shared window: alternating PC/phone use fits this model. Simultaneous independent
widths need separate application interfaces, such as the native Codex App Server
trial recorded in the wrapper session's `raw/cartan.codex-pocket-probe.2026-09-11.md`.
These helpers neither start that server nor migrate a conversation into it.

The guide's older “shrunk to the smaller screen” description is conditional on tmux's
policy: office was configured with `largest` when this helper was authored. The
commands make this choice explicit per window. See the
[tmux manual, window-size](https://man.openbsd.org/tmux.1#window-size) and
[tmux FAQ](https://github.com/tmux/tmux/wiki/FAQ#why-do-i-see-dots-around-a-session-when-i-attach-to-it).

Compose here and deploy outward. Home receives the same source through its normal
pull/deploy; office testing does not establish home or phone verification.
