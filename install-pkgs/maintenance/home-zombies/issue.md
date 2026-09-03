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
severity: low (no functional impact observed; process-table slots only)
status: open
dedicated: Maxwell (home maintenance seat)
recommend: trace what forks a zsh subshell per interactive shell/tab without reaping it — do not restart systemd --user to force-clear, that's disproportionate for a cosmetic table-slot leak
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

## Next

1. Identify what forks a bare zsh subshell without waiting — likely candidates to check
   first: any zsh `precmd`/`preexec`/`chpwd` hook, async prompt segment, or
   `zsh/system`|`zsh/ai` background helper that uses `(...)`/`{ ... } &` without `&!`
   discipline or without the parent shell ever issuing a `wait`.
2. Confirm whether this also occurs on office (not checked this session — office wasn't
   audited for zombies at all).
3. If a specific hook is found: fix at the source (proper `disown`/`&!` on a raw exec, or
   add an explicit reap), not by touching systemd or killing user shells.
