# ovitmugen — tmux manager (frame + agents)

One terminal: **agents on the left, switchable like tabs** · **runbook fixed on the right**.

```text
┌─ frame (tmux -L ovitmugen, prefix C-a) ──────────────────────┐
│ left: view <bed>--left           │ right: runbook (fixed)    │
│ [0:cSharp 1:bus 2:implement*]    │                           │
└──────────────────────────────────┴───────────────────────────┘
agents live in your normal tmux (prefix C-b): base <bed> + views <bed>--*
```

Closing the frame never stops an agent. ovitmugen only switches *views*; it never types
into a pane, and it never closes a tab where something runs (●).

## All keys — one table

```text
WHERE              KEY            DOES
shell              ov-up [bed] [@preset|tabs]   build what is missing, attach the frame
shell              ov-up … --dry-run            print the tmux commands (= manual recipe)
shell              ov-ls [bed] [--json]         dashboard: beds · tabs ● agent / ○ idle · frame
shell              ov-tab [bed] <tab>           left pane → tab (name, index, @id)
shell              ov-console [bed]             the console (see below)
shell              ov-down [bed] [--views|--idle]  peel: frame · +views · +idle tabs
shell              ov-selftest                  isolated test servers, zero side effects
frame  (C-a …)     h  l  ← →                    focus left (agents) / right (runbook)
frame              o                            next pane
frame              q  then a number             pane numbers (stay until a key)
frame              z                            zoom the focused pane (again = back)
frame              < >                          move the split (default 60 / 40)
frame              t                            console popup
frame              r                            restart the focused pane (after a quit / detach)
frame              s  w                         switch between FRAMES (= between beds)
frame              x                            close the focused pane (asks; viewer only)
frame              d                            detach — everything keeps running
frame              C-a                          a literal C-a (shell: start of line)
left pane (C-b …)  n  p  0-9                    switch tab inside the left pane
left pane          d                            detaches the inner view → pane dead → C-a r
left pane          s  w   ⚠ avoid               moves the left pane OFF its bed — use T / C-a t
runbook (right)    T                            the console, for the frame's bed
runbook            J K · 1-5 · 3 then Y         jump beds · bed parts · copy RUNBOOK content
runbook            R                            copy a cold-start card's resume: line
runbook            m  u                         presence: attach / detach the selected bed
runbook            q  (or C-c)                  quit runbook → "Pane is dead" → C-a r
console            ↑↓ / j k · Enter             choose a tab · switch the left pane to it
console            a                            add a tab (empty shell)
console            x x                          close an IDLE tab (● and the last tab refused)
console            b                            build this bed when it has no tmux yet
console            r · q / Esc                  refresh · back
```

**Which bed?** When `[bed]` is left out: the frame's bed (inside a frame) → the RUNBOOK bed
of your current directory (`…/.dev/session/<bed>/`) → the only frame that is up → otherwise
the command lists the beds. Default name = the bed's folder name, kept 1:1 so runbook finds it.

Run `ov-up` from a **plain terminal** (inside tmux it refuses: it would nest).

## Scenario 1 — a clean new bed: prepare → work → close

```text
1  /runbook has written <project>/.dev/session/<bed>/RUNBOOK.md + STATUS.md
2  plain terminal:  cd <project>/.dev/session/<bed>/  →  ov-up @csharp
   → frame "<bed>": left = tab cSharp (empty shell), right = runbook
3  right pane: select the bed · 3 (RUNBOOK) · Y copies it · m marks your presence
4  C-a h → left pane: start the head agent (claude --agent …), paste prompt-0
5  a second seat? T (or C-a t) → Enter on "bus" → start it there. Need another tab: a
6  moving around: T / C-a t for tabs · C-a h / C-a l for panes · C-a d to leave
7  gate closed: in each tab end its agent (/exit) → tab turns ○
8  ov-down --idle   (from the bed dir, or inside the frame: no name needed)
   → frame, views and idle tabs closed; any ● tab is kept and reported
9  the bed's own closure (STATUS, commit, presence u) follows the RUNBOOK, not tmux
```

## Scenario 2 — unfinished business: reincarnate, prepare, then cSharp

```text
1  ov-ls → is the bed still there?
   yes (tabs listed)  → ov-up <bed>   reattaches; dead panes are revived
   no  (reboot/gone)  → cd …/.dev/session/<bed>/ → ov-up @csharp   same names, empty tabs
2  right pane: select the bed · 1 (STATUS) → where it stopped; select its cold-start
   card · R copies the resume: line
3  PREPARER in tab cSharp: resume or cold start (paste R, or claude --resume), let it
   gather and write the handoff (STATUS / raw/), then /exit → tab turns ○
4  REAL cSharp in the SAME tab: start it; it reads the handoff and takes the head.
   One tab = one seat at a time: the preparer leaves before the head sits.
5  parallel instead? T → a "prep" → preparer works there while cSharp waits in cSharp;
   when prep is done: T → select prep → x x (closes only once it is ○)
6  close as in scenario 1, steps 7–9
```

## Safety rules

- `ov-down` and `x x` never close a tab whose pane runs anything but a bare shell, or whose
  shell has child processes. `x x` also refuses the last tab (that is `ov-down`).
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
`ov-up <bed> --dry-run` prints the exact commands for your bed.
