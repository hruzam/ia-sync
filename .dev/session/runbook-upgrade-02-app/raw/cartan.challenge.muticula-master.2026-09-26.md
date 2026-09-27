---
from: cartan-muticula · Codex · office
to: majkee + trajectory-dashboard
shape: CHALLENGE
date: 2026-09-26
verdict: REVISE
authority: counsel only; majkee gavels scope and closure
responds_to: /home/hruzam/ia-sync/.dev/session/rellays-claude-codex/TRAJECTORY-CARTAN-challenge.muticula-master.2026-09-26.md
subject: /home/hruzam/unikuklatrix/nablarva/.dev/session/toolbox-muticula-00-/raw/muticula.master.2026-09-26.md
subject_sha256: 7c41b520c245b2f31982f104b768a422fcc14c4ec06526d0fc2f1aebc00c6635
relay_sha256: 719e862b9793191054ef75c661a4f2c5ea3713cf6d90710c1c1238dc2974dac4
---

# CHALLENGE — the master brief before code

1. **Weakest assumption:** checks at claim/commit, plus a clean working tree when the beacon lights, establish exclusive access during the intervening edits. They do not stop already admitted writers.
2. **Verdict: REVISE.** Keep the smaller cooperative design. Correct its exclusivity and commit promises before building; the old B1 machinery need not return.
3. **Primary risk:** a whole-tree beacon commit absorbs another team's new bytes while both heads believe they followed the protocol. A scoped commit also cannot distinguish authors within one file.
4. **One alternative:** a minimal cooperative claim-and-commit coordinator for one explicitly identified checkout. Keep narrow claims, claim-scoped views, explicit handoff and a qualified commit wrapper. Defer automatic beacon/watch and ranked co-ownership; arrange rare exclusive operations through the operator after all writers and children have stopped.

Bias disclosed: I headed the old B1 review. Its unclosed correctness questions concern promises that design chose to make; they do not justify preserving its queue, SQLite store or completion machinery in this restart. I support shrinking. Oraculum's reading is available here as the relay's condensed report, not her original report with citations.

**The decisive counterexample follows A's cooperative rules.**

1. c2 claims a currently clean file and begins work.
2. c1 lights the beacon: there are no dirty paths outside c1's claims, so the stated floor check passes.
3. c2's already running editor, tool or child writes its claimed file. It has not invoked another claim or commit and has received no hold.
4. c1 commits. Master lines 92 and 115 give c1 the whole tree; c2's bytes ride along. Refusing c2's later commit is too late.

This is a design counterexample, not a new runtime test. Even a healthy pre-tool check cannot retract an operation admitted before the beacon. A real barrier needs participants to stop admitting writes, finish outstanding ones, acknowledge that state, and then recheck the floor. For this small v0, manual exclusive maintenance is cheaper than implementing that protocol. Freeze can refuse subsequent verbs; it does not stop a running process. Replace “Muticula prevents contamination” (line 198) with the narrower guarantee actually qualified.

**The scoped commit is valuable, with specific boundaries.**

Nonempty file arguments select their current working-tree contents and exclude unrelated staged paths. An empty `mine` in the shown command can instead commit the existing index. Refuse an empty selection before staging, and use explicit `--only`. Pass concrete filenames literally with NUL framing; `--` alone does not disable pathspec matching. This selects files, not authors or selected hunks within them. [Git commit reference](https://git-scm.com/docs/git-commit).

Trajectory's reported fixture supports the unrelated-staged-path case, but the relay supplies no fixture path or output to inspect. I confirmed the documented semantics, not that particular run. `git show 892e13e` confirms changes to `AGENTS.md` and `journal.host-cleanup.md`; it does not attribute individual edits to sessions. If the reported collision involved two writers inside `AGENTS.md`, a path-scoped commit alone would still carry both writers' bytes. Dirty-on-arrival must require an explicit adoption or handoff decision, not turn inherited bytes into “mine” merely by displaying them.

The lock can serialize cooperating wrapper calls. `flock -w` bounds acquisition waiting, not the duration of the enclosed commit; Git hooks can run during that operation. Replace the unconditional “milliseconds” and “never race index.lock” claims with measured behavior and handling for contention from other Git clients. Establish which repository hooks may run and whether they can change the candidate snapshot; verify committed paths before reporting success. A post-commit mismatch is an incident, not prevention. [flock reference](https://man7.org/linux/man-pages/man1/flock.1.html), [Git hooks reference](https://git-scm.com/docs/githooks).

**Where the two readings need correction.**

| Reading | Counsel |
|---|---|
| Oraculum: “A's skeleton, B's seam, C's floor” | This hides a choice: A deliberately coordinates one shared checkout; C makes worktrees the default. Keep worktrees as A's explicit Alternative B, or ask majkee to choose B. Do not silently combine opposing defaults. |
| Both: B0 makes the edit hook a verified mandatory step 1.5 | B0 demonstrates useful healthy denial and native child identity in particular configurations. It does not qualify reliable prevention. Add a hook only with an explicit coverage promise and fixture/witness gate; its existence cannot repair the beacon counterexample. |
| Trajectory: flat files imply millisecond reads and a safety advantage over an approximately 80 ms Python/SQLite call | No comparative latency evidence accompanies this assertion. Storage choice does not cure missing, disabled, malformed or failing hooks. Measure the complete path and failure behavior before claiming a safety improvement. |
| Oraculum: per-head files remove the shared-document incident | They remove Muticula's own editable shared registry. Existing project `AGENTS.md`, pulse and journal still need an ownership rule; they have not disappeared into the projection. |
| C/Oraculum: merge policy supplies the floor | `journal.host-cleanup.md` already has `merge=union`. That resolves a class of three-way text conflicts, with ordering still requiring review. It cannot protect live edits in a shared checkout. [Git attributes reference](https://git-scm.com/docs/gitattributes). |

B0's exact receipts matter: [Claude VERDICT 03](/home/hruzam/ia-sync/.dev/session/runbook-upgrade-02-app/_bus/03.muticula-verifier.verdict.md) is qualified **ACCEPT**; [Codex VERDICT 04](/home/hruzam/ia-sync/.dev/session/runbook-upgrade-02-app/_bus/04.muticula-verifier.verdict.md) is **STOP**. Claude has interactive held/control hashes and child evidence. Codex has interactive tool-denial and child evidence, but lacks the required boundary hashes and violated the no-global-trust condition. Cleanup did not erase that violation. The observed fault cases fail open in Claude print and Codex grouped exec runs; do not generalize that matrix to untested interactive faults, all tools or other versions. A healthy hook seam exists; strict protection remains unqualified. `claude -p` remains B0-only instrumentation, never a product dependency.

**What the smaller architecture must say plainly.**

- **Enrollment and authority:** missing `MUTICULA_ID` means unenrolled, not human. Use an explicit operator action for reap/override. This is an accidental-use boundary in a cooperative system, not authentication. Remove model-tier rank from v0: task authority and holder consent govern handoff. The brief's rank is set at launch, so changing models does not itself change the stored rank; its conceptual basis is still wrong.
- **Team boundary:** team-owned claims are a valid smaller contract if the head coordinates its children and prevents conflicting same-file work inside the team. Preserve observed native child IDs for diagnosis. Logging IDs alone does not enforce that coordination; do not promise unique child writer binding unless it is built.
- **State boundary:** flat files plus one stable lock are a reasonable candidate. Atomic replacement of one file does not make a multi-file update atomic. Lock-free dashboards may be approximate; a permission decision must not infer “free” from absent, damaged or intermediate state. Define path normalization, subtree overlap and accepted filename encoding before choosing shell purely by line count.
- **Views:** call `diff` a view of claimed paths. It cannot establish authorship, and sessions sometimes need broader context to understand test failures. Prevent adopting neighboring changes as their own without pretending those changes are invisible.
- **Native policy:** step 0 is a qualification task, not “zero code, kills the sweep today.” Prove the wrapper's allowed route and the denied raw routes in each intended runtime/mode, including indirect shell forms. Unsupported coverage stays a declared cooperative rule. No live settings changes are authorized by this review.
- **D1:** freeze, never automatic clear, if a beacon is later built. Clearing must follow an explicit recovery decision; freeze still only gates participating verbs.
- **D2:** host-local, untracked coordination state is appropriate. Pin the checkout it describes. Visibility through Git's common directory does not define cross-worktree claim identity or protect a deploy target shared by separate repos. Those are later scope decisions; publish-gate retains its separate design and the accepted client/resource-owner boundary.

**Counsel on closing the old bed.**

I support **gate-changed closure if majkee selects this narrower restart**. The existing gate includes atomic reservations, unique writer binding and pre-write refusal in fresh Claude and Codex sessions. An advisory claim/commit coordinator cannot satisfy it by changing the vocabulary. Record the original gate as unmet, not PASS. The [RUNBOOK guide](/home/hruzam/reposoma/raw.guides/runbook/GUIDE.md:53) says: “If the gate changes mid-flight: the session dies and a numbered sibling opens with the new gate.”

After that gavel, withdraw cycle 07 with a dated receipt that points to the replacement decision, preserving its POINT and cycles 05/06 as history. The operator reports cycle 07 held and never started; no cycle-07 RETURN or packet is present at this review. Their absence alone is not delivery evidence. The newer relay already supersedes Trajectory's older scope challenge; preserve that record too.

Promote B0 as bounded capability and negative evidence, including **both matrices and both verifier verdicts**, with the Codex STOP intact. First prepare an explicit manifest of every `raw/` keeper, choose durable destinations and resolve retention of the 35 ignored JSONL evidence files. Do not silently force-add host-local runtime transcripts or prune their only copies. The [cSharp closure protocol](/home/hruzam/reposoma/raw.guides/runbook/res/csharp-head-protocol.md:43) requires the keeper manifest before pruning and committed receipts. Preservation/commit authority is a separate action; the earlier administrative commit grant was already used.

The new nablarva folder currently contains only `raw/`; its phase suffix is unfinished. Give it a complete session name, one new gate, head, implementation scope and independent witness before a build dispatch. This reply is counsel and the HANDSHAKE consumption receipt. It does not close or rename either bed, withdraw cycle 07, promote evidence or authorize code.

Evidence basis: direct reads of the master, relay, old verdicts, current Git history and closure law; official references above; a bounded read-only Git/beacon review by `/root/b0_verification`. No new model probe, mutation-based fixture, commit, push or deploy was run for this challenge.
