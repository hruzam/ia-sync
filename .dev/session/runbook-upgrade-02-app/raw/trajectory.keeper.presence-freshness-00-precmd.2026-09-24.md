---
what: "Promotion keeper — closed session presence-freshness-00-precmd"
from: "trajectory-dashboard (its status_owner)"
date: "2026-09-24"
disposition: "CLOSED — superseded, gate NOT met; never executed"
authority: "majkee gavel 2026-09-24 (close it; move its property here, where muticula's RUNBOOK lives)"
originals: "git show 88ad438:.dev/session/presence-freshness-00-precmd/RUNBOOK.md (and STATUS.md) — history lives in git"
---

# Keeper — presence-freshness-00-precmd

**Why closed.** Its gate was a zsh `precmd` presence-board check. Cartan's concurrency verdict
showed `precmd` fires only before an interactive prompt — never on an agent's tool calls or in a
non-interactive shell — so it could inform the human, not the writers that collide. muticula
(`runbook-upgrade-02-app`) supersedes it and explicitly excludes reviving parked precmd pilots.
The bed is pruned; this file carries what survives.

## Verified facts worth keeping (each checked on office, 2026-09-22..24)

1. `~/reposoma/_active/` presence records **are git-tracked** (`git ls-files _active/`). A detach
   shows as a git deletion; records travel between hosts via reposoma commits. (The closed
   RUNBOOK first said "not tracked" — a misread, corrected before any execution.)
2. Bare `rb-unmark` detached **every** record on the host (5 unrelated ones, restored by majkee
   with `git -C ~/reposoma restore _active/`). Root cause per Cartan's source read: the host-wide
   `~/.local/state/session-board/own.tsv`, not the seat label. Safe practice until repaired:
   `rb-unmark <exact-id>` only. The docstring in `zsh/session/runbook.py` `board_unmark`
   ("never another owner's record") contradicts that behavior.
3. Targeted unmark proven precise live: mark two, unmark one by id, the other survived.
4. `precmd_functions` is used nowhere in `zsh/` — a precmd client would be the first such hook.
5. zsh `precmd` does not run for non-interactive commands (Cartan: `zsh -f -c` probe).

## Test cases muticula can reuse (B4 dashboard/session client)

- Separate-process arrival: shell A running, process B attaches → A learns it **without** a
  manual re-check (for muticula: dashboard snapshot revalidation, not precmd).
- Silent control: nothing changed → nothing printed.
- Degrade: read path unavailable → silent no-op; shell/client never blocks or breaks.
- Multi-client delivery policy: two clients see the same new event once each; a newly opened
  client does not burst stale "new" notices. A shared "seen" set needs a transaction, not only an
  atomic rename (Cartan's note: rename publishes, it does not serialize read/diff/update).
- Cleanup of any test attachment by exact id — never bare unmark.

## Not carried forward (deliberately)

The precmd mechanism itself, its gate, and its prompt-0 — superseded, not deferred.
