# B0 operator gavel and dispatch amendments — 2026-09-25

Authority: majkee carried Trajectory's message into this Cartan thread: **GO on B0,
fixture-only packet defined in VERDICT 01**, with the amendments below. This authorizes the
scoped test runs, not product implementation, deployment, staging, commit or push.

- `claude -p` is B0 test instrumentation only. No muticula build, product adapter, script or
  later brick may invoke or depend on it. This constraint is recorded in RUNBOOK.
- Claude's headless fault/coverage results require interactive healthy deny/unheld-control
  and subagent confirmations in the same fixture with the same healthy guard. Separate mode
  results; a divergence is evidence. Include both `--bare` and `disableAllHooks` in the matrix.
- The added Claude case and interactive confirmations expand its finite bound from eight
  to eleven fresh main sessions: the original eight headless cases, one bare case, and two
  interactive confirmations. At most one child in each subagent case; no automatic rerun
  expansion. Codex retains eight cases, using interactive healthy/control and subagent cases
  within that bound; report a native limitation rather than claim headless equivalence.
- Claude runner uses `--model haiku`, `--permission-mode acceptEdits`,
  `--setting-sources project,local` and fixture `--settings`; allows Agent for the subagent
  case. Record actual flags and effective layers, including bare-mode differences and trust.
- Trajectory reports Claude Code 2.1.282. Cartan independently checked that `af35200` touches
  only `claude/settings.json` and removes the old SessionStart hook; live user hook event names
  are currently empty. Runners must pin their own actual version/layers per run.
- Cycles 03 (trajectory-dashboard/Claude) and 04 (harness-builder/Codex) belong to fan-out
  turn 01. Both POINTs and STATUS precede relay. Native delegation carries the Codex runner;
  its full CLI fixture sessions supply its lane evidence. No native child return substitutes
  for the durable cycle receipt. Muticula-verifier is the independent witness for both lanes.
- Each lane records its own presence attachment on this bed and detaches that exact ID.
  Use lane-private `RB_STATE` for the temporary owner ledger to avoid racing the known shared
  `own.tsv` defect. Presence is the sole allowed out-of-fixture metadata mutation.
- No deploy.sh during B0 or germline construction. Germline remains another team's scope;
  Trajectory acknowledges receipt and reports no planned writes there.
- Rewire the two live citations in RUNBOOK and the original draft, then remove only the four
  verified redirect stubs. The four raw originals and the earlier relocation JSON stay intact;
  frozen BUS paths resolve through that recorded mapping. Historical source strings in that
  map are evidence, not stale live links. Current operator instruction supersedes the earlier
  temporary-stub retention rule; gate and historical receipts remain unchanged.
- Commit authority is still absent. Cartan remains sole proposed committer of the reviewed
  exchange set; concurrent germline and unrelated machine edits must be excluded.
- Majkee clarified that the `.remote` leftovers reference was mistaken wording: the hook-side
  issue is already solved. No additional `.remote` task belongs to this session.
