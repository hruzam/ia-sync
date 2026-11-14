# RUNBOOK: vistMini-01-tests

```yaml
goal: >
  Two resident senior seats from different vendors (Claude, Codex) on one host cooperate
  through one vendor-neutral message contract without the operator relaying each message,
  and the evidence says exactly how far that holds and where it breaks.
gate: >
  Majkee accepts an independently verified trial report in
  /home/hruzam/ia-sync/.dev/session/vistMini-01-tests/reports/ showing, on home, Claude↔Codex:
  at least three ordinary messages each direction delivered and consumed without operator relay;
  every pre-registered refusal/recovery case run with expected versus observed; each seat's
  permission boundary stated; and the limits of applicability to VIST stated.
participant_1: [trajectory, {brand: claude, model: claude-opus-5-5, effort: medium}, host: home, role: report author, evidence witness]
participant_2: [cartan, {brand: codex, model: GPT-6.1-Sol, effort: high}, host: home, role: long-run head, navigator, status_owner, integration and push owner]
participant_3: [oraculum, {brand: claude, model: Fable-5.2, effort: medium}, host: home, role: keeper watch-and-advise only]
participant_4: [majkee, {brand: human}, host: any, role: operator, permissions, gavel]
participant_5: [nablarva.cartan, {brand: codex, model: GPT-6.1-Sol, effort: high}, host: home, role: Nablarva hotline outside trial implementation]
participant_6: [previous.cartan, {brand: codex, model: GPT-6.1-Sol, effort: high}, host: home, role: previous controller; read-only after activation18]
status_owner: cartan
head_note: Majkee transferred the long-run head, STATUS, push and gated refresh to Cartan on 2026-11-13; Trajectory remains report author. The gate below is unchanged.
observations_read: none exist
```

## Why this session exists

Today (2026-11-12) home↔office Claude↔Claude pokes and one Claude→Codex poke worked by hand.
The open questions are safety (wrong pane, busy pane, agent exits before Enter), receipt
(delivery is not consumption), permissions (both runtimes gate tool use differently) and whether
any of it is useful for VIST. That needs a bounded trial with pre-registered cases. More ad-hoc pokes would not answer it.

## Fixed facts

- Host: home (`hruzam`). Shared checkout `/home/hruzam/ia-sync`, branch `main`. Both seats use it.
- Live endpoints on the default tmux server: `traj-home:0.0` (claude), `cartan-home:0.0` (codex).
- Wire contract under test: `/home/hruzam/ia-sync/.dev/_backlog/cross-host-session-bus.md`,
  as amended by cartan's REVISE and `protocol-proposal.md` in this bed. It is a draft, not canon.
- Inputs prepared by cartan: `protocol-proposal.md` (gate draft, ownership, test matrix),
  `reports/cartan.preflight.2026-11-12.md` (reuse probe, sandbox observations).
- Trajectory's permission evidence: `reports/trajectory.permissions.2026-11-12.md`.

## Historical prompt-0 — trajectory (superseded by POINT10 and current STATUS)

```text
You are trajectory, cSharp head of /home/hruzam/ia-sync/.dev/session/vistMini-01-tests/.
Read RUNBOOK.md and STATUS.md there. Own STATUS, pulse routing, cycle numbering and Git
windows. Delegate implementation by POINT in _bus/; verify each RETURN by the bus guide and
write the VERDICT. Never edit cartan's files. Bring majkee only permissions and decisions.
```

## Historical prompt-1 — cartan (superseded by the operator transfer and current STATUS)

```text
You are cartan (home:cartan), implementation partner and standing witness in
/home/hruzam/ia-sync/.dev/session/vistMini-01-tests/. Read RUNBOOK.md, STATUS.md and the
newest _bus/NN.trajectory.point.md addressed to you. Do exactly that POINT and write its
RETURN (six fields) at the return_to path. You own scripts/, tests/ and your reports/ files.
Never edit RUNBOOK, STATUS, pulse or trajectory's files. You may test any STATUS claim and
say so in your RETURN. Commit only inside the Git window the POINT gives you.
```

## Historical prompt-2 — VIST scientific context source (not the current keeper assignment)

```text
You are oraculum in /home/hruzam/unikuklatrix/nablarva. Your own instructions and state
ownership stay in force. Asked of you: one bounded VIST context note, delivered at the path
the POINT names: what VIST is for, the collaboration flow it expects, and what this trial
would need to show before claiming relevance. Nothing else.
```

## Known constraints + destructive holds

- **Scoped exception:** `raw.guides/runbook/res/csharp-head-protocol.md` says "the operator is the
  transport". majkee authorizes direct peer messaging for this trial only. The guide is not rewritten.
- **Git windows are serialized:** one seat stages/commits/pulls/pushes at a time in the shared
  checkout. A window opens by POINT (cartan) or by trajectory's own turn. It closes with the
  writer's `ready` poke or RETURN. Never stash, reset, rebase or commit the other seat's work.
- **Live panes:** never run disruptive cases (busy, occupied composer, exit-before-Enter, crash)
  against `traj-home` or `cartan-home`. Only on an isolated server (`tmux -L vist-test`).
- **No new channel at large:** no global daemon, generic remote shell, global settings change, deploy, or promotion to canon. Majkee explicitly authorised a bounded, removable host-local controller check-in and caching on 2026-11-13. It queues only the controller and expires; it is not transport release. ovitmugen stays viewer-only.
- **Mail citing:** durable artifacts cite this bed, never `_mail/*/inbox/` (cSharp scar 3).
- **Public repo:** no tokens, session messaging tokens, private keys or personal data in any file.
- Permission limiters are not bypassed. A needed opening goes to majkee as an exact, session-scoped request.

## Acceptance evidence

- `reports/` holds cartan's trial report with the pre-registered matrix (see `protocol-proposal.md`
  §Scientific test plan), and every case shows expected vs observed with UTC, versions and commits.
- `_bus/` holds a VERDICT by the non-author seat for every cycle that produced report evidence.
- majkee's acceptance, recorded in STATUS before closure.

## References

- `/home/hruzam/reposoma/raw.guides/runbook/GUIDE.md` — session shape, one gate.
- `/home/hruzam/reposoma/raw.guides/runbook/res/csharp-head-protocol.md` — head posture, crossed witnesses.
- `/home/hruzam/reposoma/raw.guides/status/GUIDE.md` — STATUS anatomy and recovery probe.
- `/home/hruzam/reposoma/raw.guides/bus/GUIDE.md` — POINT / RETURN / VERDICT.
- `/home/hruzam/ia-sync/HANDSHAKE.md` — delivery vs consumption, the meeting shapes.
- `/home/hruzam/ia-sync/.dev/_backlog/cross-host-session-bus.md` — the wire draft under test.

## What this session deliberately does not do

- Cross-host (office/monitor) runs. Home only. Cross-host is a sibling session if this gate holds.
- Rewriting HANDSHAKE, the bus guide or the backlog draft into canon. Findings feed them after closure.
- The Codex TABLE tunnel revalidation on 0.167.2.
- VIST shared-layer implementation/activation beyond the authorised documentary evidence analysis; X0 scope and actuator release remain separate.

## Current operator scope — 2026-11-13 group restart

Majkee authorises repairing observed seat labels, directly coordinating this resident group, finite local check-ins/cache, and labelled manual fallback when an intended channel fails. Preserve actual drafts/approval prompts and process identity. Keeper remains watch-and-advise only. Cartan owns STATUS and push. POINT10–13 form turn10; no worker Git mutation until the controller grants a window or integrates those explicitly assigned outputs. The prototype's safety refusals remain evidence, not permissions to ignore an unknown target. Native Codex queue is used directly for known Codex identities; no forced resume/writer takeover. VIST progress is routed through the owning Nablarva task bed and its live locks, with hotline advice before implementation.

Current unique seat routing after activation18 (bindings are observations, recheck before input):

| POINT to | Native identity | Role / owned output |
|---|---|---|
| trajectory | Claude06352fda-5b7f-4621-b7d1-617be6bc51a4 | report author, POINT10 |
| previous.cartan | Codex01a1ce98-6aa1-7021-b9cd-99805a07b2b2 | retired controller, read-only |
| cartan | Codex01a1d58a-3b43-7221-bf9b-fa98b219df6b | activated head, STATUS/push, POINT18; previously next.cartan |
| oraculum | Claudec266d10a-ecda-4f89-9f18-f29b59e3130e | keeper, POINT12 |
| nablarva.cartan | Codex01a1d582-c6ce-74f1-9e66-44715424aa2c | hotline, POINT13 |

The global custom Oraculum child is an analysis-only consultation, distinct from the resident Claude keeper. No roster change creates canon authority.

Controller activation18 follows accepted read-back17 and pushed continuity cache: sole pen moves from Codex01a1ce98 to Codex01a1d58a. Documentary fixture inventory is the next authorised unit; original gate and Majkee GO/STOP stay open. Previous head handles late notices read-only.
