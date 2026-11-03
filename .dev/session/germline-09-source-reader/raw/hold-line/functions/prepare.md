---
program: hold-line
function: prepare
stamp: ab41a288
---

# Prepare the two consultation lines

1. On first use, check this function's stamp and hash against controller/sources.json. Check
   task.json and the release boundary. Without a live head grant, perform offline source-pin
   and loadability checks only; return PREPARED-HOLD. Do not treat a plan as execution authority.
2. With a grant, read only its named RUNBOOK/STATUS/POINT and the pinned tunnel GUIDE needed
   for command semantics. Capture that orientation once. Require explicit model/effort,
   named role vaults, role prompts and target-turn limits. Four substantive turns are planned
   (R1/R2, A1/A2); A3 is a conditional final-revision recheck only if separately included in
   the head's release. No extra liveness/orientation-only model turn is required.
3. Verify the existing shim, GUIDE and global preamble hashes. The authoritative authored
   preamble is `/home/hruzam/ia-sync/germline/tunnel/tunnel.preamble.md`; the deployed runtime
   input is `/home/hruzam/.germline/tunnel/tunnel.preamble.md`. They must match the pinned
   revision. The older reposoma copy is not substituted. Drift, unreadability or an empty
   policy returns a hold; do not deploy or rewrite it to make the check pass.
4. Record one explicit vault per role under the release's caretaker evidence home; never
   share a thread ID or use a last-session selector. Before each invocation create an exclusive
   numbered operation record. Existing operation ID refuses execution, irrespective of status.
   Use the pinned existing Codex account/CLI, requested read-only sandbox and source shim.
5. For a NEW target, preflight with `--preamble none`. That is only a local transport check.
   Its first substantive R1/A1 packet establishes its role, scope, bounded read order, result
   format and task at once. Do not prepend “already oriented” to a cold target. Each new target
   may consume the necessary applicable instructions and named task sources for this bootstrap.
6. After validated first-task completion and its orientation acknowledgement, reconcile the
   saved ID/result and capture the bootstrap receipt. Arm the existing vault with
   `open --state <exact-vault> --preamble /home/hruzam/.germline/tunnel/tunnel.preamble.md`.
   This updates local policy without a target turn. Verify the same ID remains, the state
   points to the exact deployed preamble, and source/deployed hashes still match. An existing
   already-oriented target may use that preamble immediately only with a verified orientation
   receipt and explicit bind grant.
7. Use zero-turn resume/read to record effective runtime and actual thread/turn identity after
   the model turn. Birth-time effort snapshots can predate a turn override. Verify post-turn
   sandbox/model/effort; do not fix mismatches by spending another model turn automatically.

Write a compact readiness/operation receipt only in the head-declared evidence home. Capture
program/source revisions, IDs, preamble path/hash, and first completed turn. No whole thread
histories, credentials or caches. Then select consult for follow-up or reconcile for uncertainty.

This is preparation procedure, not an implemented new runner. At execution, the caretaker may
author only the trial-local multi-turn receipt adapter expressly included in its write grant;
the G08 runner/evidence remain unchanged. The native main must not implement that adapter.
