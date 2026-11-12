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
participant_1: [trajectory, {brand: claude, model: claude-opus-5-5, effort: medium}, host: home, role: cSharp head, navigator, status_owner, reviewer of cartan's work]
participant_2: [cartan, {brand: codex, model: GPT-6.1-Sol, effort: high}, host: home, role: implementation partner (astrobley when delegating), challenger, standing witness of trajectory's STATUS claims]
participant_3: [oraculum, {brand: codex, model: GPT-6-Astra, effort: high}, host: unverified, role: VIST context source only; joins only after its route is verified, never as a transport head]
participant_4: [majkee, {brand: human}, host: any, role: operator, permissions, gavel]
status_owner: trajectory
head_note: cSharp — this seat authored the RUNBOOK and stays live through the whole arc as navigator and status_owner; it may delegate every body of work and receive only navigation + test parts; it closes the session if it can.
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

## prompt-0 — trajectory

```text
You are trajectory, cSharp head of /home/hruzam/ia-sync/.dev/session/vistMini-01-tests/.
Read RUNBOOK.md and STATUS.md there. Own STATUS, pulse routing, cycle numbering and Git
windows. Delegate implementation by POINT in _bus/; verify each RETURN by the bus guide and
write the VERDICT. Never edit cartan's files. Bring majkee only permissions and decisions.
```

## prompt-1 — cartan

```text
You are cartan (home:cartan), implementation partner and standing witness in
/home/hruzam/ia-sync/.dev/session/vistMini-01-tests/. Read RUNBOOK.md, STATUS.md and the
newest _bus/NN.trajectory.point.md addressed to you. Do exactly that POINT and write its
RETURN (six fields) at the return_to path. You own scripts/, tests/ and your reports/ files.
Never edit RUNBOOK, STATUS, pulse or trajectory's files. You may test any STATUS claim and
say so in your RETURN. Commit only inside the Git window the POINT gives you.
```

## prompt-2 — oraculum (only after its route is verified)

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
- **No new channel at large:** no daemon, watcher, generic remote shell, global settings change,
  deploy, or promotion to canon. ovitmugen stays viewer-only.
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
- Any VIST work beyond reading oraculum's context note.
