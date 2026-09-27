# RUNBOOK: publish-gate-00-design

```yaml
goal: >-
  A reviewed design for a project-agnostic publish gate: a buffer of unpublished commits from
  many sessions that the operator can inspect, select, revert or drop before publishing, with a
  per-project adapter where publishing means more than git push. ia-sync's adapter is the first
  (publish = deploy the committed snapshot + push); nablarva inherits the core, not the adapter.
gate: >-
  Majkee records GO or STOP on a design package, challenged by Cartan, that fixes the core
  buffer model and its select/revert/drop rules, the per-project adapter contract with ia-sync's
  deploy adapter specified, the checkbox-to-plan translation, a JSON CLI contract, placement,
  and the resource boundary shared with muticula (Git transaction, deploy target).
participant_1: [trajectory, {brand: anthropic, model: operator-selected, effort: high}, {host: office, role: design author and status_owner}]
participant_2: [cartan, {brand: openai, model: operator-selected, effort: operator-selected}, {host: office, instrument: mail, role: challenger — muticula boundary and design review; no authorship of this design}]
participant_3: [majkee, {brand: human, model: none, effort: none}, {host: office, role: operator transport and gavel}]
status_owner: trajectory
schema_note: runbook/GUIDE.md verified 2026-09-17; status/GUIDE.md and bus/GUIDE.md verified 2026-09-05
```

## Why this session exists

`deploy.sh` ships the working tree, so one session's deploy can put another session's
uncommitted work live (nearly happened 2026-09-25 with germline's chatbot-port skill). Majkee
gaveled **deploy only what is committed** (2026-09-25) and asked for a dashboard over the commit
buffer — deploy all, pick, revert, delete — then recognized the general shape: every project
needs a gate for publishing work from several sessions; only ia-sync also deploys.

## Fixed facts (settled before this session)

- **Gaveled (majkee 2026-09-25):** deploy only committed content.
- **Direction (majkee 2026-09-25):** one gate — in ia-sync, publish = deploy the snapshot and push,
  in that order, so everything in the buffer is unpushed and **drop is legal inside it**; logic in
  `zsh/sync/` scope; nablarva inherits the core. Checkboxes → flags (`(?)` = his proposal, to
  architect, not a decision).
- Operator's `(?)` convention: a `(?)` marks a proposal for architecting, never an order.
- `deploy.sh`: one `$REPO` source variable (35 uses), additive (no `--delete`), no record of the
  deployed commit, one repo-writing step (`gen-temple-map.sh`), only `--codex-only` as a leg flag.
- Muticula (`runbook-upgrade-02-app`) already names a Git-transaction resource and a deploy-target
  resource; this design must not become a second owner of either.

## prompt-0 — trajectory (design author · status_owner)

```text
You are Trajectory, author and status_owner of publish-gate-00-design.
Read /home/hruzam/ia-sync/.dev/session/publish-gate-00-design/RUNBOOK.md and STATUS.md,
then /home/hruzam/ia-sync/deploy.sh, /home/hruzam/ia-sync/SYNC_DISCIPLINE.md,
/home/hruzam/ia-sync/zsh/AGENTS.md (sync/ scope, control-panel convention),
and muticula's resource model in
/home/hruzam/ia-sync/.dev/session/runbook-upgrade-02-app/raw/draft.majkee.app-scheme.2026-09-23.md §3.5.4
plus /home/hruzam/ia-sync/.dev/session/runbook-upgrade-02-app/raw/trajectory.b1-packet.2026-09-25.md.
Write the design to
/home/hruzam/ia-sync/.dev/session/publish-gate-00-design/raw/design.publish-gate.<date>.md covering:
(1) buffer model — live pointer per host, unpublished commits, authorship from trailers, deploy
legs touched, no-op commits; the authoring host vs the receiving host (pulled, not deployed);
(2) actions — publish-to-here, revert (pushed), drop (unpushed; foreign commits need operator
confirmation), with the orphan-file listing for backward moves;
(3) adapter contract — how a project declares that publish runs more than push; ia-sync adapter:
deploy from a HEAD snapshot (--ref), per-host deployed stamp, flock, orphan listing, explicit
--worktree escape;
(4) checkbox-to-plan translation — ticks become a printed plan of literal commands, confirmed
before execution;
(5) JSON CLI contract (nablarva-consumable); (6) placement in zsh/sync/ with the control-panel
convention; (7) boundary with muticula — who owns the Git transaction and deploy-target resources.
Then write a POINT to cartan in this bed's _bus/ asking for a CHALLENGE on the design.
Design only: no edits to deploy.sh, SYNC_DISCIPLINE.md, zsh/ or any live file in this session.
Done-when: design file + Cartan's challenge receipt exist; STATUS names majkee's GO/STOP as next.
```

## prompt-1 — cartan (challenger)

```text
You are Cartan, challenger for publish-gate-00-design. Read this bed's RUNBOOK.md, STATUS.md,
the design file under raw/, and the POINT addressed to you in _bus/. Challenge it: single
weakest assumption, one verdict (proceed / revise / stop), primary risk, one alternative —
with particular attention to the resource boundary with muticula (Git transaction, deploy
target), which you head. Write only the RETURN path the POINT names. No edits elsewhere.
```

## Known constraints and destructive holds

- Design only. No change to `deploy.sh`, `SYNC_DISCIPLINE.md`, `zsh/` or any live file here;
  implementation is a numbered sibling after GO.
- No `deploy.sh` run during germline construction or muticula B-bricks (their holds apply).
- No history rewriting of pushed commits in any design path; drop applies to unpushed only.
- `claude -p` is not a building block for anything designed here (majkee policy 2026-09-25).
- `deploy.sh` must not grow a germline leg (germline gavel 2026-09-25).

## Acceptance evidence

- The design file, covering items (1)–(7) of prompt-0.
- Cartan's CHALLENGE RETURN in `_bus/`, with its disposition carried into STATUS.
- Majkee's recorded GO or STOP.

## References

- `/home/hruzam/ia-sync/deploy.sh` · `/home/hruzam/ia-sync/SYNC_DISCIPLINE.md` · `/home/hruzam/ia-sync/zsh/AGENTS.md`
- `/home/hruzam/ia-sync/.dev/session/runbook-upgrade-02-app/` — muticula (resource model, B1 packet)
- `/home/hruzam/ia-sync/.dev/session/runbook-upgrade-02-app/raw/TRAJECTORY-CARTAN-research.hardcoded-boundaries.2026-09-24.md` — flock / lock-file patterns
- `/home/hruzam/unikuklatrix/nablarva/.dev/session/flag.md` — L6, L12 (worktrees; the inheriting framework)
- `/home/hruzam/reposoma/raw.guides/runbook/GUIDE.md` · `status/GUIDE.md` · `bus/GUIDE.md`

## What this session deliberately does not do

- Implement anything (deploy.sh changes, CLI, dashboard) — sibling `publish-gate-01-*` after GO.
- Build the dashboard view (ovitmugen tab or TUI panel) — later, over the CLI.
- Decide nablarva's language or store, or claim the nablarva framework's publishing semantics.
- Own muticula's resources — boundary only.
