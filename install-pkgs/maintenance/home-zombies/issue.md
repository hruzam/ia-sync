---
kind: issue
date: 2026-09-03
brand: claude
seat: trajectory
project: ia-sync
root: ~/ia-sync
host: home (hruzam)
commit: 76f0390 (main)
task: 30 zombie processes on home, oldest 16d20h — root cause not yet found
severity: low (no functional impact; process-table slots only — benign)
status: root-cause-found (fix not yet applied)
dedicated: Maxwell (home maintenance seat)
root_cause: powerlevel10k (1:1.20.17-1) → bundled gitstatus v1.5.5 forks a transient [zsh] helper per interactive shell startup that is never reaped, because job-control (setopt monitor) glitches during init. One zombie + one gitstatusd daemon per interactive shell.
recommend: benign — safe to leave; operator can proceed with any other work anytime. Track/repair helpers only if it ever becomes harmful (e.g. daemon/zsh count climbs unbounded or RAM pressure). Zombies clear when their shell/tab closes; a reboot zeroes the count. Real fix (if ever wanted) is to stop the reap failure, not to mass-kill. Do NOT restart systemd --user.
disposition: no action required — parked benign; revisit only on a harm signal
pointers:
  - ~/ia-sync/journal.host-cleanup.md (session that surfaced this, 2026-09-03, Trajectory/office ↔ home via SSH)
  - ~/.config/zsh/system/tailscale.zsh
  - ~/.config/zsh/nablarva/nablarva.zsh
  - ~/.config/zsh/projects/psdvs-toolkit.zsh
---

# Home zombies — 30 defunct processes, pattern unexplained

## How this surfaced

Found as a side effect of the Sublime-for-Laravel desk provisioning session
(`~/reposoma/_runbook/freya/sublime-for-laravel/`), not sought out. Sublime Text was
quit on home twice during that session and each time left a `<defunct>` parent plus
orphaned live children (`plugin_host-*`, an `LSP-Laravel` server binary) that had to be
killed by hand. Operator asked to search the whole box for anything else "holding on."

## Observation 1 — scope: 30 zombies total, not just Sublime

```
ps -eo stat | grep -c "^Z"   →  30
```

4 belong to the Sublime session (`sublime_text`, 2× `plugin_host-*`, 1× the
`server-v0.0.31-x64-linux` LSP-Laravel binary — all children of the same dead
`sublime_text` parent, all cleared/killed during the session).

**The other 26 are all `[zsh] <defunct>`.** This is the actual open issue — it predates
this session and is still accumulating. Ages observed span from 16 days 20h43m down to
11 minutes old at capture time, roughly one to a few per day.

## Observation 2 — every zsh zombie has a live zsh as its direct parent

Traced 5 samples spread across the full age range:

| zombie pid | age | live parent pid | parent cmd | cgroup |
|---|---|---|---|---|
| 2078 | 16d20h44m | 2056 | `/bin/zsh` | `app-org.kde.konsole-1991.scope/tab(2003)` |
| 10412 | 16d11h52m | 10372 | `-zsh` (login) | `session-4.scope` |
| 795419 | 6d06h49m | 795397 | `/bin/zsh` | `app-org.kde.konsole-1629.scope/tab(795338)` |
| 858886 | 1d07h47m | 858864 | `/bin/zsh` | `app-org.kde.konsole-806114.scope/tab(858802)` |
| 908659 | 11m | 908493 | `/bin/zsh` | `app-org.kde.konsole-806114.scope/tab(908434)` |

Pattern: an interactive zsh (one per Konsole tab, or the plain login-session shell)
forks a **zsh child**, that child exits, and the parent interactive shell never reaps
it. Not tied to any one Konsole tab lifetime — new tabs accumulate new ones over time,
old tabs' zombies just sit there.

Because the defunct entry shows `[zsh]` rather than an external binary name, whatever
forked it either (a) backgrounded a shell function/brace-group rather than a raw exec'd
binary, or (b) is a subshell `(...)` construct that never got to exec anything external
before finishing.

## Observation 3 — ruled out: the `&!`/`disown` call sites already in the config

```
grep -rn "disown\|&!" ~/.config/zsh --include="*.zsh"   →  6 hits, 3 files
```

- `system/tailscale.zsh`: 3× `&!` — all wrap a **raw external binary** as the last
  command (`python3 ...`, `xdg-open ...`, `firefox ...`). On success these `exec()` into
  the external program, so a leftover zombie from these would show as `[python3]`,
  `[xdg-open]`, or `[firefox]` defunct — not `[zsh]`. Does not match what's observed.
- `nablarva/nablarva.zsh` and `projects/psdvs-toolkit.zsh`: `code . & disown` — same
  reasoning, `code` is the exec target, and `disown` only detaches it from job-control
  bookkeeping, it doesn't change who reaps it. Also not a `[zsh]`-shaped match.

**Conclusion: the known fire-and-forget call sites in the tracked zsh config are not the
source.** Root cause is still open — something else forks a bare zsh subshell (function,
brace group, or process substitution) per interactive session without the parent ever
calling `wait()`/collecting `SIGCHLD` for it.

## Environment

```
kernel:   6.18.39-1-MANJARO
systemd:  261 (261.1-1-manjaro)
uptime:   16 days, 20:47 (matches oldest zombie's age closely — likely dates to near
          this uptime's start, i.e. last boot/session start on home)
```

## Why not just clear them

- A zombie cannot be signaled/killed — it's already exited, only a process-table entry
  awaiting `wait()` by its parent.
- The Sublime-related ones' true parent was already dead; their orphaned *live* children
  were killed directly (safe, unrelated to the reaping mechanism).
- The 26 zsh zombies' parents are live, normal interactive shells (Konsole tabs, login
  session) — killing those parents to force a reap would close the user's actual
  terminal tabs. Not done.
- The only process positioned to force-reap silently is `systemd --user` (pid 1154, the
  session's own reaper) — restarting that would tear down the whole user session
  (dbus, other services). Disproportionate for 30 table slots with zero measured CPU/RAM
  cost. Left alone.

## ROOT CAUSE — FOUND (2026-09-03, second pass)

The bare-zsh-subshell forker is the **prompt**, not anything in the tracked `zsh/` config.

### The stack
- `~/.zshrc` sources `/usr/share/zsh/manjaro-zsh-prompt`
- → `source /usr/share/zsh-theme-powerlevel10k/powerlevel10k.zsh-theme`
- powerlevel10k `1:1.20.17-1` bundles **gitstatus v1.5.5**
  (`/usr/share/zsh-theme-powerlevel10k/gitstatus/usrbin/gitstatusd`)

### The mechanism (why a `[zsh]` zombie per shell)
At every interactive shell startup, p10k calls `gitstatus_start`, which:
1. spawns a **persistent `gitstatusd` daemon** (this is the live `Sl` process — expected,
   one per shell, does its job and stays), and
2. forks a **transient background `[zsh]` helper subshell** (gitstatus's setup/watchdog
   around the daemon's FIFO).

The helper finishes almost immediately — but the interactive parent shell never `wait()`s
on it, so it becomes `[zsh] <defunct>` and sits there for the shell's entire lifetime. It
is only reaped when the parent shell exits (then init adopts and collects it).

### Why the reap fails — the observed trigger
A fresh `zsh -ic` probe emitted:

```
(anon):setopt:7: can't change option: monitor
```

Something in the init chain runs `setopt monitor` (enable job control) in a scope where it
can't take effect. Job control / `monitor` is exactly what makes zsh track and reap
background jobs ("[1] done"). With it glitching at the moment gitstatus backgrounds its
helper, the finished child is never collected → persistent zombie.

### The correlation that proves it (counts, same session)

```
zombies (zsh defunct):  26
gitstatusd daemons:     29
```

Near 1:1 — one zombie + one gitstatusd per interactive p10k shell. Ages line up per-shell,
e.g. gitstatusd 2059 (age 16-21:22) ↔ zombie 2078 (age 16-21:20), same parent shell 2056.
The small 26-vs-29 gap is normal churn (a few shells' zombies already reaped, or shells
still mid-prompt-init).

### Accumulation
Home uptime at capture: **16 days, 21h** (single boot). Every Konsole tab / login session
opened across those 16 days that is still alive contributes one zombie + one daemon. 26 is
simply "≈26 long-lived interactive shells since boot." Not a runaway leak — bounded by the
number of open shells.

## Impact — benign

- A zombie is already-exited: **zero CPU, zero real RAM, one PID-table slot.** Default PID
  max is ~4 million; 26 is nothing.
- The live `gitstatusd` daemons are the only real (small) RAM cost, and they are *expected*
  p10k behavior, not a leak.
- **Unrelated** to the Sublime freeze / stuck sshfs mount investigated the same session —
  entirely different mechanism (that one is a dead FUSE mount, D-state, see journal).

## Secondary observation (not the ticket, but noted)

`pgrep -c -x zsh` = **143 live zsh** at capture. Far more than the ~26–29 interactive
shells. Most are presumably non-interactive `zsh -c` helpers (agent tooling,
`tree-snapshot`, subshells) that don't load p10k and so don't contribute zombies. High but
not alarming; worth an eyeball if it keeps climbing.

## Disposition (2026-09-03, operator steer)

Operator's call: **not harmful — proceed with other work anytime.** No repair scheduled.
Only stand up tracking/repair helpers if a genuine harm signal appears (unbounded growth in
`gitstatusd`/live-`zsh` counts, or measurable RAM pressure). Until then this ticket is a
parked reference, not a queued task.

## Fix options (Maxwell's call — default: do nothing)

- **A. Leave it.** Harmless. Each zombie clears when its tab/shell closes. Recommended
  unless it's bothering something. (Not fixed by a reboot's sake — but a reboot naturally
  resets the count to zero.)
- **B. Update powerlevel10k.** *Low confidence this helps* — `1.20.17` is already current
  and gitstatus v1.5.5 is the current bundle, so this is not a stale-version bug. The
  reap failure is environmental (the `monitor` setopt), not a fixed-upstream defect.
- **C. Fix the real trigger.** Track down what runs `setopt monitor` in a bad scope during
  init (the `can't change option: monitor` line) and correct it, or make gitstatus's helper
  explicitly `&! disown`. This is the proper fix but needs care in a minified theme +
  manjaro config chain.
- **D. Blunt but effective:** set `POWERLEVEL9K_DISABLE_GITSTATUS=true` in p10k config —
  removes both the daemon and the zombie, at the cost of a slower git prompt segment.

## Still open

- Whether office shows the same pattern (office was never audited for zombies — it runs the
  same manjaro/p10k stack, so it very likely does).
- Do NOT touch `systemd --user` (pid 1154) to force-clear — disproportionate; it's the
  session reaper and restarting it tears down the user session.
