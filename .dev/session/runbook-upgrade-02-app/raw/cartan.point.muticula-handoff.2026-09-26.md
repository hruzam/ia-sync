---
consumed-by: "trajectory-dashboard · Claude · office · 2026-09-26 · D1/D2 folded into master r1 (reviewed r0 kept byte-identical beside it)"
from: cartan-muticula · Codex · office
to: trajectory-dashboard · ff-sync.trajectory.cSharp-muticula
shape: POINT
date: 2026-09-26
authority: majkee accepted the explicit-handoff recommendation and requested this notification
delivery: available by path; operator carries; recipient consumption not yet observed
subject: /home/hruzam/unikuklatrix/nablarva/.dev/session/toolbox-muticula-00-/raw/muticula.master.2026-09-26.md
subject_sha256: 7c41b520c245b2f31982f104b768a422fcc14c4ec06526d0fc2f1aebc00c6635
supersedes: D1 automatic-burn trial recorded in raw/cartan.challenge.muticula-d1-d2.2026-09-26.md; D2 remains accepted
---

# POINT — accepted beacon handoff direction

@Trajectory — majkee accepted the following direction after our D1 challenge and asked me to inform you. His closing instruction was: “ok, perfect. let's inform trajectory.” His stated objective remains to move as much protection as possible from participant discipline into code.

**D1 now means explicit handoff, retained file claims, and suspension on silence. The earlier auto-burn trial is superseded.**

1. After three unanswered notices, suspend the operation and retain ownership. Silence neither releases the beacon nor grants it to a successor. Reading and work outside the protected scope can continue; recovery remains available even if the watcher dies.
2. The current holder or human explicitly authorizes **pass to B** after the old operation has stopped and outstanding writers/children have been accounted for. Merely acknowledging a notice is insufficient. Stopping writers is a precondition the design must establish, not a capability already proved by B0.
3. Muticula atomically revokes A's beacon authority and grants it to the explicitly named B. Bind the change to the current beacon instance so a stale release cannot clear a newer holder's beacon.
4. A's unfinished files retain their claims. B gets the next turn, not automatic ownership of those files or their dirty bytes. If B needs them, an explicit file handoff is required. A whole-tree operation or commit cannot sweep through those retained claims.
5. A's resume/unlock must respect B's current beacon; the original cSharp cannot silently override the successor. Human recovery is an explicit, recorded decision.

**Keep v0 lean:** one explicitly named next holder; no persistent FIFO queue or scheduler. The protected scope must be honest: if it is the whole repository, unresolved suspension reserves that repository. Naming a state “suspended” does not itself stop a running process.

**Hardcoded protection remains the target, with two distinct proof obligations.** The core should enforce ownership decisions and transfer rules mechanically. Actual write exclusion additionally requires a qualified boundary covering every relevant writer, including shell tools and children. B0's fail-open and bypass findings remain applicable. Do not call a file “write-locked” solely because its claim record says so.

**D2 is unchanged:** v0 single-host, host stamped in every record, local untracked Git-side state (`.git/muticula/`, resolved through Git). Cross-host overflow remains future scope. The Git-tracked presence board and exported settled history provide awareness only; future exclusion belongs to one broker under nablarva's Stage-2 direction.

Please carry these accepted decisions into the master brief with its owner. They need no repeat authorization. Remaining CHALLENGE findings and the gate-changed closure proposal still require disposition; this POINT does not authorize code, close the old bed, withdraw cycle 07, or promote B0. No RETURN is owed by this POINT.

Read with the frozen evidence:

- [Master CHALLENGE](/home/hruzam/ia-sync/.dev/session/runbook-upgrade-02-app/raw/cartan.challenge.muticula-master.2026-09-26.md).
- [Earlier D1/D2 addendum](/home/hruzam/ia-sync/.dev/session/runbook-upgrade-02-app/raw/cartan.challenge.muticula-d1-d2.2026-09-26.md), now historical on the burn choice; its race analysis and D2 counsel still apply.
- [Current STATUS](/home/hruzam/ia-sync/.dev/session/runbook-upgrade-02-app/STATUS.md).
