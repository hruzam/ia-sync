# Independent views and scrollback — live setup

2026-11-13 · Cartan · home · requested directly by Majkee after the goal handoff.

## Before and after

Before: base `helper-utils-00-tmux`, one window `claude` (`@7`, pane `%9`, idle
zsh), two attached clients (`/dev/pts/19`, `/dev/pts/28`). They necessarily shared
the current window. No `~/.tmux.conf` existed. The pane already had a 50,000-line
history capacity, but no recorded history at inspection.

After:

| Terminal at setup | Attached view | Selected window |
| --- | --- | --- |
| `/dev/pts/19` | `helper-utils-00-tmux--claude` | `claude` (`@7`, `%9`) |
| `/dev/pts/28` | `helper-utils-00-tmux--codex` | `codex` (`@9`, `%11`) |

The base remains unattached. Both views share its window list and processes,
but select windows independently. Either view can navigate both windows; these
names are starting positions, not restrictions. Selecting the same underlying
window in both views still displays the same process, as expected.

The new Codex window starts in `/home/hruzam/ia-sync`. Both panes remain shells;
Cartan did not launch, resume, stop or migrate either vendor CLI.

## Comfort profile

[tmux-comfort.conf](tmux-comfort.conf) is experimental source in this raw folder,
manually loaded into the running default tmux server. It is not wired into deploy
or startup. It sets `mouse on` and `history-limit 50000` for this base and its two
views. Both windows use `window-size latest` so an unattached base's dimensions
do not dictate their displayed size.

- Mouse wheel upward enters tmux history in this workspace, even for programs
  using the alternate screen; subsequent wheel scrolling uses copy-mode.
- `Shift+PageUp` enters history and pages upward without a prefix.
- `Shift+PageDown` pages down while in history.
- While in history, ordinary `PageUp` / `PageDown` work; `q` returns to live input.
- Built-in fallback: `Ctrl-b`, then `[` enters history; `Ctrl-b`, then `PageUp`
  enters it and pages up. A terminal may intercept shifted shortcuts, so retain
  and document this fallback.

Key bindings are server-wide in tmux. The custom root bindings therefore check
the exact workspace group; other groups keep the observed default wheel action
and receive shifted page keys normally. This profile intentionally prefers tmux
history over application-specific mouse-wheel actions in this workspace.

History means output retained by tmux. It does not guarantee that a TUI's entire
conversation is retained as terminal lines, and cannot recover discarded history.
The configured history limit generally governs newly created panes; the existing
Claude pane was independently observed already at 50000.

## Attach later

From a plain terminal outside tmux, use the appropriate view:

```sh
tmux attach -t helper-utils-00-tmux--claude
```

In the second terminal:

```sh
tmux attach -t helper-utils-00-tmux--codex
```

Do not attach both terminals to the base or to the same view. The helper should
eventually handle allocating/reusing independent views and explain collisions.

To reproduce after recreating the base: preserve/create its `claude` and `codex`
windows; create each missing view with
`tmux new-session -d -t '=helper-utils-00-tmux' -s <view-name>`; select its intended
window; then source the comfort profile with `tmux source-file <profile-path>`.
Set each window's `window-size` to `latest`. Do not blindly recreate existing work.

## Verification and remaining limits

Live queries confirmed two different selected windows, one client per view,
both views in the base's group, mouse enabled, and both panes at history capacity
50000. Loaded root bindings were inspected.

Using `tmux send-keys -K` against the new idle Codex client, Cartan verified:
`Shift+PageUp` → `pane_in_mode=1`, `pane_mode=copy-mode`;
`Shift+PageDown` kept copy-mode active; `q` → `pane_in_mode=0`.
This exercises tmux's actual client key dispatch. It does not prove the desktop
terminal forwards those physical shortcuts, or substitute for a human wheel test
inside a running vendor TUI. No conversation prompt was submitted.

Pre-change options, root bindings, clients and window IDs were saved locally at
`/tmp/helper-utils-tmux-before-6zlduetf/before.json`. This is temporary host-local
evidence, not portable source. The existing uncommitted Claude status-line work
and sibling export were preserved. No global startup config, deployed shell
source, RUNBOOK, STATUS or pulse was changed.
