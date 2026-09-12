# @Epoch research report
Date: 2026-09-06
Triggered by: majkee — pre-implementation research for a "presence board" mechanism (ia-sync session-tool project), before building `~/reposoma/_active/` advisory presence files.
Scope: default radar (agentic CLI-runtime landscape) + targeted queries on lock/heartbeat conventions and multi-agent coordination standards. No project contract read for this run (ad-hoc research request naming its own output path).

## Findings

### 1. Claude Code ships built-in worktree isolation, not a presence registry
WHAT changed: Claude Code added native `-w`/`--worktree` support so each session gets its own git worktree (own branch, own working dir), and the desktop app auto-creates a worktree per new session.
SINCE when: reported as shipped ~v2.1.49, Feb 2026 (per secondary blog sources; version number NOT independently confirmed against `code.claude.com/docs/en/changelog` in this run — flag as unverified detail).
SOURCE: https://code.claude.com/docs/en/worktrees ; https://www.mindstudio.ai/blog/claude-code-git-worktree-parallel-branches ; https://www.developersdigest.tech/blog/git-worktrees-claude-code-parallel-agents-guide
CONFIDENCE: M (official docs page confirms the feature exists; the specific version/date is secondary-sourced, not from the changelog itself)
IMPACT: Confirms the industry-favored answer to "avoid collision" is **worktree-per-session**, not a coordination file. Claude Code's own design principle (per docs) is "one concurrent session per worktree" — it does not attempt to detect or warn about two sessions in the *same* worktree; it sidesteps the problem by giving each session a different directory.
ACTION: none — informs design implications below.

### 2. Codex CLI: same story — isolation, not detection
WHAT changed: Codex CLI supports running multiple sessions in parallel, but each is an independent process with no shared awareness; community tooling (e.g. "OMX", agent-swarm wrappers) achieves safety via worktree-per-worker, not via any built-in lock/registry.
SINCE when: ongoing through 2026 (multiple 2026-dated community posts, no single "since" date).
SOURCE: https://codex.danielvaughan.com/2026/04/18/running-multiple-codex-agents-parallel-orchestration/ ; https://www.codeagentswarm.com/en/guides/run-multiple-codex-sessions
CONFIDENCE: M (independent commentators, not OpenAI's own docs — I did not find an official Codex CLI changelog entry addressing concurrent-session detection)
IMPACT: No vendor has shipped native cross-session presence/lock signaling for Codex CLI either.
ACTION: none.

### 3. Cursor: same pattern, plus explicit acknowledgment that two agents in one working copy is a known failure mode
WHAT changed: Cursor's own worktree docs and third-party guides state plainly that "two agents writing to the same file at the same time produce a merge conflict that neither of them knows about" — the recommended fix is prompt-scoping (assign each agent a directory) or worktrees, not a coordination file. Cursor's Aug 19, 2026 update added cloud subagents each getting an isolated VM + repo copy.
SINCE when: Aug 2026 (cloud subagent update); worktree docs current as of this run.
SOURCE: https://cursor.com/docs/configuration/worktrees ; https://www.learncursor.dev/learn/cursor-origin/parallel-agents-merge-conflicts ; https://www.explainx.ai/blog/cursor-event-driven-cloud-agents-isolated-vms-august-2026
CONFIDENCE: M
IMPACT: Reinforces the pattern: the entire 2025-2026 agentic-coding industry has converged on **spatial isolation (worktrees/VMs)** as the answer to concurrency, not **social/advisory signaling (who's here)**. Nobody in the mainstream tool landscape ships what majkee is sketching.
ACTION: This is the key gap the presence board would fill — see design implications.

### 4. No emerging standard for repo-local multi-agent "who's-here" presence metadata
WHAT changed: Searched for `.agent-lock`, session-registry, and AGENTS.md-ecosystem extensions specifically for concurrent-session presence. Found two adjacent-but-different things, neither is what's being proposed:
  (a) An `agent.lock` **file format proposal** (blog, not a standard) — an advisory *configuration pin* (models/skills/MCP servers used, like package-lock.json) — not a mutual-exclusion or presence signal at all.
  (b) The A2A (Agent2Agent) project's "Agent Registry" discussion — this is about **capability/entitlement discovery** for networked agent services (auth schemes, skill schemas, federation), not about "is someone editing this repo right now." Discussion open since June 2025, still unresolved/fragmented as of May 2026, no finalized spec.
SOURCE: https://2amsecurity.substack.com/p/where-is-my-agentlock-file (Apr 15 2026) ; https://github.com/a2aproject/A2A/discussions/741 (last activity May 26 2026)
CONFIDENCE: M-H (directly read both sources; reasonably confident no closer match exists after these targeted searches, but absence-of-evidence has residual risk — did not exhaustively search every AGENTS.md fork)
IMPACT: The presence-board sketch is not reinventing an existing wheel — there is no known off-the-shelf convention for "lightweight, git-synced, advisory, per-session presence marker in a dev repo." It would be a genuinely novel-but-small piece, not a duplicate of a standard.
ACTION: none — validates building it, subject to design cautions below.

### 5. Advisory heartbeat/lease conventions are a well-established pattern OUTSIDE the coding-agent space
WHAT changed: n/a (long-standing distributed-systems pattern, not new in 2026).
SOURCE: general distributed-systems references (lease pattern, DynamoDB lock client staleness-detection issue, Akka lease docs) — https://singhajit.com/distributed-systems/lease/ ; https://singhajit.com/distributed-systems/heartbeat/ ; https://github.com/awslabs/amazon-dynamodb-lock-client/issues/34
CONFIDENCE: M (these are general pattern descriptions, not project-specific dated releases — treat as stable/training-consistent knowledge re-confirmed live, not a 2026 novelty)
IMPACT/pattern summary:
  - **Lease = lock + TTL.** Holder must heartbeat (renew) before TTL expires or another party may reclaim. This is mutual exclusion — NOT what majkee wants (board is advisory-only, never a lock).
  - **Advisory presence != lease.** For pure "who's here" (no reclaim/exclusion), the simpler PID-file / editor-swap-file / tmux-session-list convention is closer: a file exists, its mtime (or an embedded timestamp) says how fresh it is, and staleness is rendered (dimmed / ignored) rather than acted on. No process ever "steals" anything.
  - **mtime vs embedded timestamp:** filesystem mtime is simpler and cannot lie (assuming clocks aren't skewed across machines — a real risk here since ia-sync is explicitly cross-machine via git sync, where mtime can be rewritten by clone/pull operations). An **embedded timestamp in the file body** is the safer choice for a git-synced board, precisely because git checkout does not reliably preserve original mtimes across machines/clones.
  - **TTL values in comparable tools:** editor swap files have no TTL (persist until crash-recovery prompt); PID files are typically checked instantaneously (process either exists or not, no TTL); tmux session discovery (`tmux ls`) is live-process-based, not file/TTL-based at all. None of the close analogues use a numeric "N hours" TTL — that convention comes from distributed leases (30s–120s typical), which is the wrong order of magnitude for a human-paced coding-session board. A TTL in the 1-6 hour range (majkee's own instinct) is more analogous to "is this person still at their desk" than to a machine lease, and has no direct precedent to cite — it is a reasonable but original choice, not an industry-standard number.
ACTION: recommend embedded timestamp (ISO 8601, written at attach/refresh time) over relying on file mtime, given the git-sync cross-machine transport.

## Sections to refresh
- Re-check `code.claude.com/docs/en/changelog` directly (not secondary blogs) if the exact Claude Code worktree-support version/date becomes load-bearing for a claim.
- Re-check OpenAI's own Codex CLI changelog/docs for any native session-awareness feature — this run only found third-party commentary.
- Re-run the A2A registry discussion search in a few months; it was explicitly unresolved/fragmenting as of May 2026 and could converge on something adjacent.
- If majkee wants a stronger claim than "no standard exists," a deeper sweep of AGENTS.md-ecosystem GitHub forks/issues (not just blog posts) would raise confidence from M to H on Finding 4.

## Design implications for the presence board

1. **The sketch is well-aimed, not redundant.** No mainstream tool (Claude Code, Codex CLI, Cursor) or emerging standard (A2A registry, agent.lock) addresses "advisory who's-here for a repo/worktree" — they all solve concurrency by *spatial isolation* (worktree-per-agent), which majkee's team already partially does. The presence board is a genuinely different, complementary layer: it doesn't prevent collision, it makes an existing collision *visible* — which is exactly the "harmless once, hazard eventually" problem stated. Build it.

2. **Reconsider "worktree/repo" as the sole key.** Since the whole industry treats worktree-per-agent as the default safety mechanism, and ia-sync's own practice already uses worktrees for parallel work (per this repo's own session dirs and other projects' patterns), the presence board's most valuable signal may be less "is someone in this exact worktree" (rare collision, since worktrees already separate that) and more "is someone in this *repo* at all, on *either machine*, possibly in a different worktree touching overlapping files." Keep the pointer field granular enough to show worktree/bed, but don't assume worktree-uniqueness eliminates the need for the board — the reported failure mode ("same git repo/worktree simultaneously") suggests it's already happening despite worktree conventions, likely because ad-hoc seats don't always spin up a fresh worktree for quick tasks.

3. **Use an embedded timestamp, not raw mtime, for staleness.** Because transport is git (cross-machine sync via pull), mtimes are not trustworthy signals of "when was this written" after a clone/pull on the other host. Write an ISO 8601 timestamp inside the file body at attach and at each refresh (heartbeat), and compute staleness from that field — this matches how the closest real precedent (DynamoDB-style lease clients) actually implement staleness detection (they use an explicit heartbeat timestamp field, not raw filesystem mtime), even though this board should stay a lease-free, advisory-only design.

4. **Never let it become a lock — explicitly design against reclaim semantics.** The distributed-systems research is unanimous that "lease" implies exclusivity + reclaim. Because the requirement is "advisory only, carries no state beyond someone-is-here," resist any temptation to add "steal if stale" logic (common in lease libraries) — that would silently convert the board into a soft lock and violate the no-daemons/no-hooks culture of this project. Staleness should only ever affect *rendering* (dim in the TUI), never *behavior* (no auto-detach, no auto-anything). This matches the PID-file / swap-file precedent, not the DynamoDB-lease precedent.

5. **TTL choice has no external precedent to lean on — treat it as a UX tuning knob, not a correctness parameter.** Distributed-lease TTLs (30-120s) are the wrong reference class. A 1-6 hour "dim" threshold is reasonable by analogy to human work sessions but is an original choice for this project; expect to tune it empirically rather than cite an authority for it.

6. **Cross-machine lag is a known, accepted tradeoff — no tooling reviewed here solves it better.** Every tool surveyed (Claude Code, Codex, Cursor) that does offer any multi-instance safety net does so within a single machine/VM's filesystem; none has a cross-machine, git-synced presence mechanism to compare against or borrow patterns from. The git-transport lag majkee already flagged as inherent is confirmed as a genuine platform gap, not something being solved elsewhere that could be adopted instead.
