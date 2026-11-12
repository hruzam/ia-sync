```yaml
updated: 2026-11-12 10:40 CET
writer: trajectory · claude
host: home (hruzam)
worktree: /home/hruzam/ia-sync · main · local commits ahead of origin (cartan b092ec2..3f85a77, trajectory 01 reply + this STATUS), unpushed by rule · untracked nano.1844235.save (operator's, not session)
gate: >
  Majkee accepts an independently verified trial report in
  /home/hruzam/ia-sync/.dev/session/vistMini-01-tests/reports/ showing, on home, Claude↔Codex:
  at least three ordinary messages each direction delivered and consumed without operator relay;
  every pre-registered refusal/recovery case run with expected versus observed; each seat's
  permission boundary stated; and the limits of applicability to VIST stated.
checkpoint: >
  Cycle 01 ACCEPT, cycle 02 BLOCKED (_bus/02.trajectory.verdict.md). Relaunch done: recovery probe at 10:24 CET shows
  traj-home:0.0 = %3 root claude, cartan-home:0.0 = %2 root codex (no enclosing shell).
in_flight: >
  Cycle 03, thread 01: cartan→trajectory delivered + consumed (reply 01.trajectory.md committed). Trajectory→cartan
  pointer REFUSED 29 at 2026-11-12T09:35:28Z on the sender self-check of %3 (log /tmp/vistMini-cycle03-trajectory-01.log;
  no reservation, nothing sent). One manual notice sent under the fallback hold. Cartan to diagnose %3 idle state.
delegated:
  - {cycle: "03", to: cartan, turn: none, awaiting: return}
recovery_probe: >
  ls /home/hruzam/ia-sync/.dev/session/vistMini-01-tests/reports/trial-msgs/. The highest NN.cartan.md without a matching
  NN.trajectory.md = trajectory owes that reply. Matched pairs = cartan's turn. 03.cartan.return.md present = verify it.
  ls /tmp/vistMini-cycle03-trajectory shows my adapter reservations (an entry = a send attempted, never repeat it).
holds: >
  PUSH IS TRAJECTORY'S ONLY (majkee, 2026-11-12): cartan stages+commits his own paths and does not push; trajectory
  pushes after verifying (shared checkout carries his commits). No stage/commit by one seat during the other's Git
  window. No disruptive cases on live panes. No manual poke counts as trial evidence.
  MANUAL-NOTICE FALLBACK (majkee 2026-11-12, global from now: backlog draft §4.9): after a CLEAN adapter refusal
  (exit ≠ 0 before any reservation, nothing sent), the sender may send exactly ONE manual notice per refused message,
  labelled `manual`, pointing at the message plus the refusal log. It never counts as delivery evidence. Uncertain sends
  (a reservation exists) never get a manual notice. Those go through receipt/recovery. oraculum (Astra) not a participant
  until its route is verified. Outside this gate: monitor keys on home/office remain an operator action (journal).
next: >
  Answer each reports/trial-msgs/NN.cartan.md when its pointer arrives: write NN.trajectory.md, commit, send its pointer to %2
  with the adapter command in _bus/03.trajectory.point.md. After 03.cartan.return.md: verify, write VERDICT 03, push.
expected: >
  Three matched NN.cartan.md / NN.trajectory.md pairs, each delivered by an adapter call that exits 0, then VERDICT 03.
```
