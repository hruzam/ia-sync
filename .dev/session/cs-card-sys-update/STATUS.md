```yaml
updated: 2026-09-17
writer: trajectory
host: home
worktree: "~/ia-sync (main, clean at author time) + ~/reposoma (core) — two-repo session"
gate: >
  A fresh Claude session (updated skill) and a fresh Codex session (tunnel-delivered skill)
  each drop AND re-locate BOTH an issue card and a cold-start card in the one shared vault;
  the gaveled cold-start-card GUIDE carries the issue category, the sort-key rule
  (name vs frontmatter) and its unsorted fallback; and the standalone _issues/ vault from
  this session is reconciled into that shape (folded or kept — majkee's category call).
head_note: "cSharp — Trajectory authored this RUNBOOK and stays as navigator + status_owner; delegates bodies whole, keeps only navigation + test parts; closes if it can."
witness: "assay — counter-signs the gate; the claims in this STATUS are paths it can test"
checkpoint: >
  Phase 1 (@atlas-ui) complete, CROSS-WITNESSED by @assay, PASS. Majkee answered the open
  question (subtree confirmed) and added issues/reactions/ (dateless, IR.<slug>.md, mirrors
  routines/), the coupling invariant, and locked >=7 assoc: as an unraised RULE — recorded in
  RUNBOOK.md "CLOSED 2026-09-17". @Delta added the delta to the Claude skill + [ISSUE-DRAFT]
  GUIDE blocks (self-reported done, NOT yet witnessed — batched with phase 2 per plan).
in_flight: none
recovery_probe:
  cmd: "ls ~/ia-sync/claude/skills/issue-card/ 2>/dev/null && echo BUILT || echo NOT-STARTED"
  reads: >
    BUILT = phase 1 already began (atlas-ui ran) — read this STATUS's next + the skill diff
    before spawning anything again. NOT-STARTED = nothing built yet; the plan is fresh, wake
    per next below. Read-only either way. Witness @assay verifies whichever branch is true.
holds:
  - "GUIDE (reposoma canon) edits are DRAFT until majkee gavels — no self-lock (0002 F4)"
  - "Never delete the two _issues/ seed cards — migrate, leave old path until new shape proven"
  - "No commit / push / deploy from any builder — majkee lands, after the gate proof"
  - "Compose-first: author on ~/ia-sync, never live ~/.claude or ~/.codex"
  - "Head is navigator only — does not edit issue-card/SKILL.md; that voids the delegation"
  - >
    NEW, blocking phase 2: the existing tunnel table
    (~/ia-sync/.dev/session/tunnel-home.state.json, enabled 2026-09-16T23:04:17Z) is
    sandbox type "readOnly" — fixed at `open` time, not changeable per-send. Phase 2 needs
    Cartan to WRITE ~/ia-sync/codex/skills/. Law 2.4: only the operator opens a table — this
    head does not self-enable a new one. `tun status` command + verification: `export
    TUNNEL_CODEX_STATE=~/ia-sync/.dev/session/tunnel-home.state.json && zsh
    ~/.config/zsh/ai/tunnel-codex.zsh status` (confirmed exit 0, enabled:true, sandbox
    readOnly, checked 2026-09-17).
next: >
  BLOCKED on majkee: open a write-capable tunnel table for phase 2 — either
  `tun open --enable --sandbox workspace-write --state
  ~/ia-sync/.dev/session/cs-card-sys-update/tunnel.state.json` (fresh, session-scoped,
  matches the "put it where the work lives" convention), or reopen the existing
  tunnel-home.state.json with workspace-write if majkee wants the same thread/continuity.
  Once open: Trajectory sends the §"Phase 2" prompt (amended for reactions/ + the coupling
  invariant), then @assay batch-witnesses Delta's amendment + Cartan's return together.
expected: >
  A write-capable table open, phase 2 sent, Codex-native issue-card surface built under
  ~/ia-sync/codex/skills/, both this delta and phase 2 cross-witnessed in one @assay pass.
  Gate stays open until BOTH fresh-session proofs (Claude + Codex, drop AND re-locate an
  issue card and a cold-start card) close it, and majkee actually gavels the GUIDE.
```
