---
to: "@Cartan (cartan-muticula)"
from: "@Trajectory (trajectory-dashboard · Claude · office)"
shape: "POINT (informational — nothing owed back; attach as evidence to cycle 01 if useful)"
date: "2026-09-24"
asked-by: "@majkee — study the boundaries programs hardcode, not community opinion"
relates-to: "/home/hruzam/ia-sync/.dev/session/runbook-upgrade-02-app/_bus/01.trajectory-dashboard.return.md"
---

# Hardcoded good manners — how real programs keep writers apart, mapped to muticula

Written in the meeting room, not your bed: my cycle-01 write scope was the RETURN only.
Two legs: **primary sources** (man7 man pages, git/kernel docs, RFC 9110, svnbook, Chubby and
Gray–Cheriton papers — via @Epoch) and **observed behavior on this host** (throwaway repos in
`/tmp`, removed after — via @Delta, one probe re-run by me). Labels: **[obs]** seen here ·
**[src]** primary source · **[rec]** my recommendation · **[unver]** not yet proven.

## 1. What this host actually enforces (observed, kernel 7.1.3 · git 2.55.0)

| Mechanism | Observed | Tier |
|---|---|---|
| git `index.lock` present → `git add`/`commit` | exit 128, "Unable to create …index.lock: File exists. Another git process seems to be running … or the lock file may be stale" | program-enforced; atomic `O_EXCL` create |
| git `refs/heads/<current>.lock` → commit | exit 128, "cannot lock ref 'HEAD'" | same pattern (Delta's first run locked a non-current ref — void; re-run by me) |
| `git switch feat` while `feat` is checked out in another worktree | exit 128, "'feat' is already used by worktree at …" | program-enforced branch exclusivity |
| `git worktree lock --reason` then `remove` | exit 128, "cannot remove a locked working tree, lock reason: …; use 'remove -f -f'" | reservation + reason + explicit double-force override |
| main `index.lock` vs `git add` inside a second worktree | allowed (exit 0) | per-worktree index — isolation real, but only per checkout |
| `flock -n -x` while held / plain `echo >>` while held | exit 1 / write succeeds | advisory only — binds cooperating callers |
| zsh `noclobber` | "file exists", `>|` overrides | courtesy, operator override |
| kernel LSMs | `capability,landlock,lockdown,yama,bpf`; fanotify built in | Landlock available unprivileged; no mandatory locking (removed in 5.15 [src]) |
| sandbox tools | `bwrap 0.12.0`, `unshare`, `systemd-run` present | confinement available without new install |

## 2. The recurring design moves (primary sources)

1. **One atomic arbiter, never read-then-write.** `O_EXCL` create, `fcntl(F_SETLK)`, `rename()`
   over, a consensus commit, or HTTP `If-Match` — every sound mechanism is a single arbitrated step.
2. **Two different lifetimes, two different primitives.** Kernel locks (`flock`/`fcntl`, dpkg's
   `lock-frontend`) **release on process death** — no stale state, but cannot outlive the process.
   Lock *files* (git, pacman, Vim, LibreOffice) and VCS reservations (SVN, Perforce, ClearCase)
   **survive a crash** and need an explicit human/admin release.
3. **Holder identity written into the lock.** Emacs `.#file` symlink → `user@host.pid:boot`; Vim
   swap stores host/user/pid; SVN/Perforce record the authenticated user + workspace. flock/fcntl/
   ETag carry no identity at all — identity is a deliberate layer, not free.
4. **Stale handling splits in two:** liveness-based expiry (Chubby, ZooKeeper, etcd, K8s Lease)
   vs human judgment (git, pacman, LibreOffice, Vim E325). None of the file-lock tools auto-steal.
5. **Steal is explicit and audited** where it exists: `svn lock --force` (atomic break+relock,
   server-logged), `git worktree remove -f -f`, ClearCase admin unreserve.
6. **Fencing is the only thing that stops a *stale* holder from acting.** Chubby sequencers,
   ZooKeeper zxid, etcd `mod_revision` — the *resource* rejects a lower generation at write
   time. Kubernetes Lease states outright that it does no fencing. git/pacman/Vim/Emacs have none.
7. **The refusal text names both hypotheses and the next step** — git: "another process is running,
   *or* the lock is stale". It doesn't claim the file is free and doesn't just exit silently.
8. **Mandatory only at an engineered chokepoint.** POSIX chose advisory-by-default; Windows
   `CreateFile` share modes chose mandatory-by-default (the contrast). Linux removed its mandatory
   escape hatch in 5.15.

## 3. Mapped onto muticula §3.5 (confirmations and one new seam)

- **Confirms** — the SQLite `BEGIN IMMEDIATE` choice already *is* pattern 2's kernel tier: SQLite
  serializes writers with `fcntl` locks, so the decision transaction self-releases on crash while the
  **claim row** carries the crash-surviving reservation. §3.5.6 keeps the two lifetimes apart
  deliberately; the primary sources say that split is right, and that merging them is the classic
  bug. **[src]**
- **Confirms** — claim `generation` checked at admission = fencing (pattern 6). That is exactly
  what the file-lock family lacks. Keep it at the write path (hook), not only at acquire. **[src]**
- **Confirms** — "no automatic expiry; operator `recover`" matches git/pacman/SVN practice.
  Borrow SVN's shape: recovery is one audited transition (old owner → new owner, receipt),
  never a delete-then-create gap. **[rec]**
- **Borrow** — Emacs/Vim identity: store `actor_id` **plus** host, pid, and boot id as *displayed
  liveness evidence* (the dashboard can say "holder pid 4211 not running") — evidence for the
  operator's `recover`, never an automatic takeover. **[rec]**
- **Borrow** — git's conflict message shape for adapters: owner + scope + "live, or stale → here
  is how to check and recover". **[rec]**
- **Lean on git, don't reimplement** — git already refuses the same branch in two worktrees and
  guards worktree removal with a lock + reason. The B5 worktree client can use `git worktree lock
  --reason <claim_id>` as its native marker and keep muticula's store as the authority. **[rec]**
- **New seam — Landlock for the uncovered shell lane.** §3.5.6 says arbitrary shell commands escape
  path coverage and need "a controlled execution wrapper/sandbox". Landlock is unprivileged,
  present here, and irrevocable once applied: a wrapper can run an agent's shell command with write
  access limited to that actor's **currently granted** subtrees (plus scratch/tmp). It is not a
  coordination tool (no peers, no signaling) — it is **confinement that makes the store's decision
  physically true** for that process. `bwrap` is the heavier fallback. **[rec, unver]**
- **Reject** — fanotify permission events: the only kernel-mediated veto, but it needs
  CAP_SYS_ADMIN, stalls the caller forever if the listener hangs, and gates `open`, not each write.
  Wrong tier for a cooperative same-user tool. **[src]**
- **Reject** — lease expiry/heartbeat (Chubby/etcd/K8s style) for v0: it needs a live service and
  contradicts the no-auto-takeover rule; K8s itself warns it does not prevent split-brain. **[src]**

## 4. Layering this suggests (candidate, not a design lock)

| Layer | Primitive | Covers |
|---|---|---|
| decision | SQLite txn (`fcntl`, self-releasing) | atomic acquire/admit/release |
| reservation | claim row + generation + holder evidence | survives crash; operator recover |
| pre-write, edit tools | Claude/Codex PreToolUse deny | enrolled edit tools |
| pre-write, shell lane | Landlock-confined command wrapper | shell writes outside granted scope **[unver]** |
| commit time | git `pre-commit` + `reference-transaction` (abort-capable) | foreign staged paths, ref updates |
| isolation | `git worktree` + `worktree lock --reason` | independent writers |
| display | dashboard reads snapshot + liveness evidence | never decides |

## 5. Corrections and open items

- Delta's report called git's lock "kernel-enforced": wrong — the kernel makes the create atomic;
  the refusal is git's own rule. A program ignoring git can still write the index.
- Epoch called dpkg `lock-frontend` "mandatory": it is an advisory `fcntl` lock that every dpkg
  front end honors; its real virtue is self-release on crash.
- **[unver]** Landlock confinement of a Claude/Codex shell tool call — needs a probe: can a
  wrapper apply a ruleset per command without breaking the tool, and is a denied write reported
  back to the agent cleanly? Candidate for B3 ("unsupported shell/background paths visible or
  refused"), not for B0.
- **[unver]** `FAN_PRE_ACCESS` (Linux 6.14+) on this 7.1 kernel — irrelevant if fanotify stays
  rejected; noted only because Epoch flagged it as the one high-volatility claim.
- Unchanged: B0 (native pre-write deny probe, both runtimes) stays the first packet in my RETURN;
  this research does not reorder it.
