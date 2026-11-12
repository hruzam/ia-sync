```yaml
updated: 2026-11-12 09:22 CET
writer: trajectory · claude
host: home (hruzam)
worktree: /home/hruzam/ia-sync · main · base 5e29d95 + this bed's opening commit · clean after commit
gate: >
  Majkee accepts an independently verified trial report in
  /home/hruzam/ia-sync/.dev/session/vistMini-01-tests/reports/ showing, on home, Claude↔Codex:
  at least three ordinary messages each direction delivered and consumed without operator relay;
  every pre-registered refusal/recovery case run with expected versus observed; each seat's
  permission boundary stated; and the limits of applicability to VIST stated.
checkpoint: >
  Bed opened. RUNBOOK, this STATUS, reports/trajectory.permissions.2026-11-12.md and
  _bus/01.trajectory.point.md are committed (git log -1 -- .dev/session/vistMini-01-tests/RUNBOOK.md).
  Pre-trial evidence: Claude→Codex poke submitted into cartan-home (ia-sync 2c2b01d era); Codex→Claude
  poke received in traj-home ([bus 2026-11-12T080801Z.home.cartan.02]). Both are ad hoc and outside the matrix.
in_flight: >
  Cycle 01 delegated to cartan (adapter + isolated tests). Cartan's Git window is open until his `ready`.
delegated:
  - {cycle: "01", to: cartan, turn: none, awaiting: return}
recovery_probe: >
  ls /home/hruzam/ia-sync/.dev/session/vistMini-01-tests/_bus/ — 01.cartan.return.md absent = cycle 01
  still with cartan; present = verify it. git -C /home/hruzam/ia-sync log --oneline -- .dev/session/vistMini-01-tests/reports/cartan.matrix.2026-11-12.md
  must show the matrix commit BEFORE any tests/ commit (pre-registration), else REVISE.
  tmux capture-pane -p -t cartan-home:0.0 | tail -5 shows whether cartan is working or idle.
holds: >
  Trajectory does not stage/commit while cartan's Git window is open. No disruptive cases against live
  panes traj-home / cartan-home. oraculum (Astra) is not a participant until its route is verified.
  Pending operator action outside this gate: monitor keys on home/office (journal), not needed here.
next: >
  Wait for cartan's poke, then verify /home/hruzam/ia-sync/.dev/session/vistMini-01-tests/_bus/01.cartan.return.md
  per the bus guide and write _bus/01.trajectory.verdict.md.
expected: >
  01.trajectory.verdict.md exists with a disposition and claim table. The matrix commit precedes the test commits.
```
