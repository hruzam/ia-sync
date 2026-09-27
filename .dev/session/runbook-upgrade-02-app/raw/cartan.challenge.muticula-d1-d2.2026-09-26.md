---
from: cartan-muticula · Codex · office
to: majkee + trajectory-dashboard
shape: CHALLENGE addendum
date: 2026-09-26
authority: records majkee's D1/D2 decisions; remaining recommendations are counsel
responds_to: majkee's D1/D2 addendum in this conversation, 2026-09-26
prior_challenge: /home/hruzam/ia-sync/.dev/session/runbook-upgrade-02-app/raw/cartan.challenge.muticula-master.2026-09-26.md
prior_challenge_sha256: 8236ccb95d22d104a93769f249bb5900112a09517f5bad2c6fc635d7867003db
subject: /home/hruzam/unikuklatrix/nablarva/.dev/session/toolbox-muticula-00-/raw/muticula.master.2026-09-26.md
subject_sha256: 7c41b520c245b2f31982f104b768a422fcc14c4ec06526d0fc2f1aebc00c6635
---

# D1/D2 — decision receipt and remaining challenge

**Decisions received from majkee:** D1 tries automatic beacon clearing ("burn") after 2–3 unanswered notices, with freeze as fallback if the trial serves badly. D2 keeps v0 on one host, in `.git/muticula/`, with a host stamp in every record; cross-host overflow remains a future requirement. These supersede my earlier freeze-first recommendation and resolve the two policy choices. The master on disk still has its previous wording and hash; its owner needs to fold this receipt.

1. **Weakest assumption:** an operator-authorized timeout, a burn log and a dirty-path report together make it safe for another writer to proceed. They establish permission and visibility, not that the former writer has stopped.
2. **Verdict: REVISE the guarantees and trial contract.** Accept the operator's burn trial and D2 placement. Automatic clearing must be described as a deliberate availability tradeoff with incomplete exclusion.
3. **Primary risk:** an old operation continues after the burn, while another head sees a dark beacon and starts overlapping work. Its first dirty-path report can be clean; the old operation writes afterward.
4. **One alternative trial shape:** burn the global hold as authorized, revoke that beacon instance's whole-tree commit privilege, preserve ordinary claims and record the unresolved operation. Returning holders and newcomers explicitly reconcile inherited work before adopting it. This bounds the cooperative trial; it still cannot fence an already running editor or child.

**D1: authorization is settled; the invariant needs an amendment.**

Trajectory is right that this can be human-delegated policy. That preserves the principle that authority comes from majkee. It does **not** preserve the master’s literal rule: “Every automatic path ends in refusal or hold, never in release.” Amend it to name the authorized burn exception. Do not describe an intentional relaxation as unchanged protection.

Before a trial packet runs, specify these small but consequential details:

- Pick an exact threshold within the authorized range; my recommendation is **three unanswered notices**. Record the notice interval and what resets the count. Unanswered is not proof that a notice was seen. If the watcher is absent or dead, retain the stated hold behavior; never claim an unseen notice was delivered.
- Bind notices, keep/off and burn to one beacon instance. A late notice or watchdog must not clear a replacement beacon. Serialize the transition with claim/commit decisions and refuse to proceed on unreadable state or a failed burn record.
- Make every burn visible in the durable event record and subsequent command output: host, holder, beacon instance, reason, count and observed dirty paths. Report that footprint as a snapshot, not a complete accounting of future writes or external migration effects.
- Burning the beacon does not reap the team, release its ordinary file claims, adopt its dirty bytes, or terminate its processes. The expired whole-tree privilege cannot survive merely because the old holder resumes. “Dirty on arrival” must lead to an explicit handoff/adoption decision.
- Predeclare the freeze fallback: conflicting writes or commits, a late burn affecting a new beacon, or an unreconstructable ownership state are failures. Count useful unblockings too. Log visibility alone is not a successful concurrency result.

My recommendation remains to qualify this in fixtures before relying on it for live cross-cutting operations. The earlier clean-floor counterexample remains open even before timeout: beacon activation also needs cooperation from already admitted writers. Selecting burn neither fixes that race nor authorizes a build in this turn.

**D2: concur, with local authority kept separate from transported awareness.**

Host-stamped, untracked v0 state fits one host and one identified checkout. Resolve the Git directory rather than assuming `.git` is always a directory; reject foreign-host state as local authority. Host labels provide provenance, not exclusion or authentication. Copying the state directory to another host must not enroll its old owners there.

The existing `~/reposoma/_active/presence.*.md` records are Git-tracked on office. Their [presence-board contract](/home/hruzam/reposoma/raw.guides/runbook/res/presence-board.md) explicitly makes them advisory, host-scoped and potentially delayed; presence or absence grants no lock, takeover or permission. A transported settled journal is likewise historical information. The proposed Muticula journal inside `.git/muticula/` is not automatically tracked: any selected snapshot needs an explicit export. No new board schema or transport is implied here.

[Nablarva flag L2/L3/L4](/home/hruzam/unikuklatrix/nablarva/.dev/session/flag.md:12) supports the distinction: Stage 2 is cross-host, L3 names the same protocol over SSH to one central broker, and L4 records git-as-wire's death. Git synchronization can carry awareness; it cannot grant mutually exclusive live ownership. “One broker” is the future authority direction, not proof that cross-host locking already exists. Its later gate must cover disconnects and old holders resuming; host stamps alone do not solve those cases.

These decisions do not themselves close `runbook-upgrade-02-app`, withdraw cycle 07, promote B0, or authorize new code. The remaining scope and closure counsel stands. The original CHALLENGE stays frozen; read it together with this addendum.
