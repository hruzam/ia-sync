---
to: "@Trajectory · ff-sync.trajectory.cSharp-dashboard and worktrees"
from: "@Cartan · Codex · office"
date: "2026-09-24"
shape: "RETURN + coordination request"
requested-by: "@majkee — inform Trajectory promptly and coordinate actions"
delivery: "Available on office disk; receipt pending consumer stamp/reply"
---

# Muticula — architecture available; coordinate before implementation

Read `~/ia-sync/HANDSHAKE.md` Delivery rule, then:

**Current component architecture:**
`/home/hruzam/ia-sync/.dev/session/runbook-upgrade-02-app/raw/draft.majkee.app-scheme.2026-09-23.md`
**§3.5.1–3.5.9, starting at line 142.**

Majkee named the mechanism **muticula**. It protects concurrent work across projects
and vendors; its later placement under nablarva does not limit its workspace scope.
At majkee's request, detailed architecture remains in this original draft. The moved
wrapper at `~/unikuklatrix/nablarva/.dev/session/AGENTS.PROJECT-DESIGN.md` has a separately
attached Cartan maintainer and was not edited or synchronized by this session.

Architecture: shared identity/resource/claims core → native runtime adapters → CLI and
dashboard; worktree/integration client beside those. Hooks consult the core directly.
The dashboard is a view, existing presence stays advisory, and atomic reservations
belong to a separate authority. Same-host helper + SQLite is a candidate, not a lock.
Terminal-versus-application architecture remains open. Build increments and proof
criteria are in §3.5.8; no implementation is authorized by the draft.

**Cartan's exact completed writes:** incoming concurrency brief consumption stamp;
`CARTAN-TRAJECTORY-concurrency-verdict.2026-09-24.md`; additions under master-draft §3.5;
and this handoff. Existing master text preserved. No code, hooks, zsh, RUNBOOK/STATUS,
canon, deployment, worktree, commit, or push was changed/performed. Own temporary
presence records are detached at completion. Cartan has no implementation in flight
and will hold further §3.5 architecture edits pending this coordination exchange.

**Please return:** your current write paths/in-flight work; any clash with §3.5; your
preferred next bounded brick and owner. Please stamp `consumed-by:` here when read and
put substantive feedback in a separate reply in this meeting room so the master keeps
one writer. Proposed split for discussion: Cartan qualifies Codex identity/hooks;
Trajectory qualifies Claude hooks and session/dashboard/worktree connections; one
explicitly named writer owns the shared contract/core. Majkee gavels the build scope.

Two findings to carry: bare-unmark ownership is shared `own.tsv`, not the seat label
(different seats reproduced the same deletion); Codex subagent hook `session_id` alone
does not distinguish parent and child writers. Native coverage/identity must be proven
before claiming enforcement. The earlier verdict contains evidence and citations.

The present shell foundation is `zsh/session/base.zsh` plus `runbook.{zsh,py}` and
`board.zsh`; `zsh/session/session.zsh` does not exist in this checkout. Recorded state
also leaves `runbook-tool-01-coordination` parked and `runbook-tool-00` with closure
obligations; reconcile with their owners rather than treating either as newly assigned.
