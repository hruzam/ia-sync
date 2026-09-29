# ovitmugen — tmux manager

Agents on the left, switchable like
tabs. Runbook fixed on the right.

```text
┌ frame (C-a) ──────┬─────────────┐
│ left: agents      │ right:      │
│ [cSharp bus …]    │ runbook     │
└───────────────────┴─────────────┘
agents: your normal tmux (C-b)
```

Closing the frame never stops an agent.
ovitmugen only switches views; it never
types into a pane and never closes a
tab where something runs (●).

## Shell commands

```text
ov-up [bed] [@preset|tabs]
  build what is missing, attach frame
ov-up … --dry-run
  print the tmux commands (recipe)
ov-ls [bed] [--json]
  beds · tabs ● agent / ○ idle
ov-tab [bed] <tab>
  left pane → that tab
ov-console [bed]
  the console (keys below)
ov-up <bed> --root <p>/.dev/session
  runbook on that root, tabs in <p>
  (re-roots an existing frame too)
ov-down [bed]           frame only
ov-down [bed] --views   + views
ov-down [bed] --idle    + idle tabs
ov-selftest             test servers
```

Which bed, when left out: the frame's
bed → the RUNBOOK bed of your current
dir (.dev/session/<bed>/) → the only
frame up → else it lists the beds.
Default name = the bed folder name.

Run ov-up from a plain terminal, not
inside tmux (it would nest).

## Frame keys (C-a …)

```text
h l ← →   focus left / right
o         next pane
q + 1/2   pane numbers, jump
z         zoom pane (again = back)
< >       move the split
t         console popup
r         restart pane (dead pane)
s w       switch frames = beds
x         close pane (viewer only)
d         detach, all keeps running
C-a       literal C-a (line start)
```

## Left pane keys (C-b …)

```text
n p 0-9   switch tab
d         detach view → C-a r
s w       ⚠ avoid: leaves the bed
          use T or C-a t instead
```

## Runbook keys (right pane)

```text
T         console for this bed
J K       next / previous bed
1-5       STATUS _bus RUNBOOK
          files raw
3 then Y  copy RUNBOOK content
R         copy card resume: line
m u       presence attach / detach
q  C-c    quit → dead pane → C-a r
```

## Console keys (T · C-a t)

```text
↑↓ j k    choose a tab
Enter     left pane → that tab
a         add a tab
x x       close an IDLE tab
o         open this bed's frame
b         build bed (no tmux yet)
r         refresh
q Esc     back
```

x on a ● tab is refused: end the agent
in its tab first (/exit). The last tab
is refused too (that is ov-down).

## Scenario 1 — new bed

```text
1 /runbook wrote RUNBOOK + STATUS
2 plain terminal:
    cd <proj>/.dev/session/<bed>
    ov-up @csharp
3 right: 3 (RUNBOOK) · Y · m
4 C-a h · start head agent,
  paste prompt-0
5 2nd seat: T · bus · Enter,
  start it · new tab: a
6 done: /exit in each tab (○)
7 ov-down --idle
8 bed closure (STATUS, commit,
  u) follows the RUNBOOK
```

## Scenario 2 — unfinished work

```text
1 ov-ls: bed still there?
  yes → ov-up <bed>
        (revives dead panes)
  no  → cd into the bed dir
        ov-up @csharp
2 right: 1 (STATUS) = where it
  stopped · card → R (resume:)
3 PREPARER in tab cSharp:
  resume / cold start, write
  handoff, /exit → ○
4 REAL cSharp, SAME tab: start,
  reads the handoff.
  One tab = one seat at a time.
5 parallel: T · a "prep" …
  done: T · prep · x x
```

## Scenario 3 — from runbook only

You have just `.dev/session/<bed>/` and
no tmux yet.

```text
1 plain terminal: rb-open
2 J / K to the bed
3 T → "no tmux bed" console
4 b · Enter (name = bed)
      Enter (default tabs,
      or @csharp / names)
5 o → runbook closes, this
  terminal BECOMES the frame:
  left = tabs, right = runbook
6 start agents in the tabs
```

Keep the default name (= bed folder):
then T finds the bed again later.
A typed name works, but T on the bed
won't find it (use ov-ls / C-a s).

Later, the same bed again: rb-open ·
bed · T · o. Or from a shell: ov-up.
Inside a frame, o switches frames.
Inside other tmux, o refuses (nest):
C-b d first, then ov-up <bed>.

## Safety rules

- ov-down and x x never close a tab
  whose program is not a bare shell,
  or whose shell has child processes.
- Views close only while the base
  exists.
- Duplicate tab names: use the id
  from ov-ls (@12).
- ov-down --views/--idle also closes
  t41 columns of the bed (terminals
  drop to their shell; agents stay).
  Don't name a tab `left`.

## Presets

ovitmugen.presets.json, next to the
tool (edit in ~/ia-sync/zsh/session):

```text
"csharp": {
  "tabs": ["cSharp","bus",
           "implement","audit"],
  "fixed": "runbook",
  "split": "40%" }
```

split = width of the right pane.
fixed = runbook or shell.

## Without the tool

Help scope tmux-session, section
"Build a bed by hand".
ov-up <bed> --dry-run prints the exact
commands for your bed.
