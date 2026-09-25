# ovitmugen — tmux manager (frame + agents)

One terminal: **agents on the left, switchable like tabs** · **runbook fixed on the right**.

```text
┌─ frame (tmux -L ovitmugen, prefix C-a) ──────────────────────┐
│ left: view <slug>--left          │ right: runbook (fixed)    │
│ [0:cSharp 1:bus 2:implement*]    │                           │
└──────────────────────────────────┴───────────────────────────┘
agents live in your normal tmux: base <slug> + views <slug>--*
```

Closing the frame never stops an agent. ovitmugen only switches *views*; it never
types into a pane.

## Commands

```sh
ov-up tunnel-01                  # build base + 4 tabs + left view + frame, attach
ov-up tunnel-01 @csharp          # tabs from a preset (ovitmugen.presets.json)
ov-up tunnel-01 front api db     # your own tab names
ov-up tunnel-01 --dry-run        # print the tmux commands = the manual recipe
ov-tab tunnel-01 bus             # left pane → bus  (name, index or @id)
ov-ls                            # every bed: ● agent running · ○ empty shell
ov-ls tunnel-01 --json           # machine-readable (termbrana later)
ov-console tunnel-01             # pick a tab with Enter
ov-down tunnel-01                # close the frame only (agents untouched)
ov-down tunnel-01 --views        # + close all views (tabs stay in the base)
ov-down tunnel-01 --idle         # + close tabs with NO running agent
ov-selftest                      # isolated test servers, zero side effects
```

Run `ov-up` from a **plain terminal**. From inside tmux it refuses (it would nest) and
prints the attach line to use later.

Tabs start as empty shells. Start each agent yourself (`claude --agent …`).

## Keys inside the frame (prefix C-a)

- `C-a t` — console popup (Enter = switch left pane, `a` = add tab, `q` = close)
- `C-a h` / `C-a l` — focus left (agents) / right (runbook)
- `C-a <` / `C-a >` — move the split (default left 60 / right 40)
- `C-a d` — detach the frame (everything keeps running)
- `C-a C-a` — send a literal `C-a` (shell: start of line)
- mouse click — focus a pane

Inside the left pane the agents' own tmux still uses `C-b`. `C-b d` there detaches the
inner view: the left pane goes dead. `ov-up <slug>` reconnects it.

## Safety rules

- `ov-down` never closes a tab whose pane runs anything but a bare shell, or whose shell
  has child processes.
- Views are closed only while the base exists (closing the last view of a missing base
  would kill the windows).
- Duplicate tab names are refused by name; use the id from `ov-ls` (`@12`).

## Presets

`~/ia-sync/zsh/session/ovitmugen.presets.json` (deployed next to the tool):

```json
{ "csharp": { "tabs": ["cSharp","bus","implement","audit"], "fixed": "runbook", "split": "40%" } }
```

`split` is the width of the fixed right pane. `fixed` is a named command: `runbook` or `shell`.

## Without the tool

The same result by hand: scope **tmux-session**, section "Build a bed by hand".
`ov-up <slug> --dry-run` prints the exact commands for your bed.
