# pad.5-shell-harmonize-verify — office login shell → zsh, remote-reach test protocol

> mode: authored MANNED 2026-07-31 (Flight/office, majkee via tailscale) · **walk: Monday,
> majkee physically AT office** — every step is safe with you in the chair; nothing here can
> strand you remotely.
> **State at authoring:** `chsh -s /usr/bin/zsh` ALREADY RUN on office (operator, 2026-07-31).
> Untested — no new login opened since. Home already `/usr/bin/zsh`, needs nothing.
> **Why this pad exists:** office's login shell was `/bin/bash`, so SSH sessions from home
> got no zsh harness (`tsp: command not found` — the whole `~/.config/zsh` universe absent).
> Desktop terminals were immune (terminal profile launches zsh directly). chsh closes the gap;
> this pad proves it. Charter fit: OS/account-level state — exactly this folder's scope.
> **Reassurance:** chsh affects only NEW logins. Any session already open (Freya work, tmux,
> agents) is untouched, before and after.

Sequential — run one STEP, paste output into its `>MAJKEE report` slot, then next.

---

### STEP 0 — you are at office, physically. Confirm the account record

```sh
getent passwd hruzam | cut -d: -f7
```

Expected: `/usr/bin/zsh`. If it still says `/bin/bash`, the chsh didn't take — rerun
`chsh -s /usr/bin/zsh`, log out/in of the desktop once, and restart this pad.

>MAJKEE report 0
```zsh

```

---

### STEP 1 — the exact failing case, reproduced safely: SSH into office FROM office

This is the same login path home uses (sshd → login shell), with zero remote dependence —
you're testing the door while standing inside the house.

```sh
ssh localhost 'echo SHELL=$SHELL' 
ssh -t localhost 'type tsp; echo PEER=$TAILSCALE_PEER'
```

Expected: `SHELL=/usr/bin/zsh` · `tsp is an alias for _ts_ssh` · `PEER=hruzam`.
That is the 2026-07-31 bug dead: SSH sessions now get the full harness.
(If `ssh localhost` refuses: `ssh 127.0.0.1`, or note it — office sshd may bind tailnet only;
then test STEP 1 from the home leg in STEP 3 instead, still safe.)

>MAJKEE report 1
```zsh

```

---

### STEP 2 — the new direction: office → home, aliases end-to-end

```sh
tsping          # tailscale-level: peer answers
tsp hostname    # ssh-level: should print "hruzam", passwordless, no prompt
```

Expected: ping pongs; `tsp hostname` → `hruzam`. This proves the authorized_keys line +
engine + aliases as one chain. (`tsp` with an argument passes it to ssh — see
`system/tailscale.zsh:74`.)

>MAJKEE report 2
```zsh

```

---

### STEP 3 — the original complaint, from the real seat: home → office lands in zsh

From any home shell (or your phone's home session — this is the remote leg, safe now
because you are AT office if anything surprises):

```sh
ssh hruzam-120922 'echo SHELL=$SHELL'
ssh -t hruzam-120922        # interactive: expect zsh prompt, ts header, switcher banner
# inside:  type tsp   → alias  ·  exit
```

Expected: `SHELL=/usr/bin/zsh`, and the interactive session greets you with the zsh
startup surface instead of a bare bash `$`.

>MAJKEE report 3
```zsh

```

---

### STEP 4 — eagle-on-home trigger, the landed recipe (atlas T3 close-out)

From office:

```sh
ssh hruzam '~/.npm-global/bin/claude --version'
# then the real thing, cheap prompt:
ssh hruzam '~/.npm-global/bin/claude -p "reply exactly: EAGLE-RAIL-OK" 2>&1 | tail -2'
```

Expected: version prints (2.1.220 at authoring); second command returns EAGLE-RAIL-OK.
Absolute path is mandatory — home's claude is npm-global, PATH only in .zshrc, invisible
to non-interactive shells. Recipe of record: `~/.remote/memory.md` (landed 2026-07-31).

>MAJKEE report 4
```zsh

```

---

### STEP 5 — OPTIONAL · reboot-over-tailscale drill, safest possible day

Only if you want the drill on record, and ONLY because you are physically present (a failed
boot needs hands; today they're attached). Skip freely — substrate is already verified
(tailscaled+sshd enabled, Linger=yes, no LUKS, sleep.target masked).

```sh
# from home session (or phone): 
ssh hruzam-120922 'sudo reboot'
# wait ~60-90 s, then:
ssh hruzam-120922 'uptime; systemctl --user is-active claude-rc-freya.service'
```

Expected: uptime shows minutes, claude-rc services self-started (Linger). Do NOT run this
step remotely on a day you've just upgraded the kernel without a local boot test.

>MAJKEE report 5
```zsh

```

---

## Close-out

All green → the machines are harmonized at every layer: shell, tunnel, keys, aliases,
agent trigger. Note results here; Flight archives the verdict into pulse + this pad on
the next session. Anything red → paste the report, do not improvise fixes at the chair —
the failing layer is diagnosable from the reports above.

## Still open (after this pad)

- Atlas T4 — H8 load-bearing test (`pin_bus.push()` via remote SSH) — operator-run,
  separate sitting, its own protocol (netOrchestrating territory).
