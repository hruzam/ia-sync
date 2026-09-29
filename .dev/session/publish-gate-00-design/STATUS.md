# STATUS: publish-gate-00-design

```yaml
updated: 2026-09-29 (majkee decided Q1; design folded; POINT re-pinned)
writer: trajectory · anthropic
host: office
worktree: >-
  /home/hruzam/ia-sync · main. The bed is tracked since a541808. Other writers' dirty paths
  (journal.host-cleanup.md and others) are not ours; never stage them from here.
gate: >-
  Majkee records GO or STOP on a design package, challenged by Cartan, that fixes the core buffer model and its select/revert/drop rules, the per-project adapter contract with ia-sync's deploy adapter specified, the checkbox-to-plan translation, a JSON CLI contract, placement, and the resource boundary shared with muticula (Git transaction, deploy target).
checkpoint: >-
  prompt-0 is done (majkee's schedule step 2, 2026-09-29). raw/design.publish-gate.2026-09-29.md
  (sha256 873214c7…, 432 lines) covers items (1)–(7), a muticula boundary section that folds
  Cartan's 2026-09-25 memo point by point, and 7 open questions for majkee. A Sonnet Trajectory
  spawn drafted it; the head reviewed it and applied 9 corrections (listed in its frontmatter).
  The most material: the push sends exactly the selected prefix (<sha>:refs/heads/main), and the
  human's drop opens with the beacon in an enrolled checkout. Nothing live changed. The same day
  majkee decided Q1: every unpushed commit stays droppable, even when deployed, with its own
  command and button. This is folded (design sha256 a83551be…), and the POINT was re-pinned before
  any reply.
in_flight: >-
  _bus/01.trajectory.point.md → cartan: CHALLENGE of the design. The RETURN is expected at
  _bus/01.cartan.return.md.
recovery_probe: >-
  sha256sum raw/design.publish-gate.2026-09-29.md must equal the POINT's subject_sha256. In
  ls _bus/, a POINT without its RETURN means the challenge is out, not received.
holds:
  - Design only — no edits to deploy.sh, SYNC_DISCIPLINE.md, zsh/ or live files in this session.
  - Muticula (brief r3) owns claims, the beacon and the commit gate; this design draws a boundary, not ownership.
  - Decided 2026-09-29 (majkee): unpushed ⇒ droppable holds even at deployed_push_pending; drop has its own command and button.
next: >-
  majkee relays POINT 01 to Cartan. After Cartan's RETURN the head folds, and majkee records GO or
  STOP. The six minor open questions can ride with that fold.
expected: >-
  _bus/01.cartan.return.md, then a folded design revision, then majkee's GO/STOP.
```
