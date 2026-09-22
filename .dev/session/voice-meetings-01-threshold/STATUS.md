# STATUS: voice-meetings-01-threshold

```yaml
updated: 2026-09-22 06:09 CEST
writer: atlas-ui · anthropic
host: office
worktree: >
  /home/hruzam/ia-sync · main · 69056b0 · dirty —
  .dev/session/voice-meetings-01-threshold/ (new bed, uncommitted) and pulse.md (router line)
gate: >
  Each test in the fixed battery (paprika · blackout) has been run once as its SINGLE-agent
  version against each vendor voice (claude-voice · gpt-voice) with a run record on disk, and a
  VERDICT per test×vendor scores its three checkpoints clear / assisted / miss — four VERDICT
  files exist in loops/.
checkpoint: >
  session opened — RUNBOOK + STATUS authored, router line in /home/hruzam/ia-sync/pulse.md;
  zero loops run; living home with both test designs + both seat briefings in place at
  /home/hruzam/ia-sync/.dev/session/voice-meetings/ (ia-sync e59dd2f, pushed)
in_flight: none
recovery_probe: >
  ls /home/hruzam/ia-sync/.dev/session/voice-meetings-01-threshold/loops/ 2>/dev/null —
  absent or empty → no loop has started; an NN.*.return.md with no matching NN.*.verdict.md →
  a run landed and awaits evaluation (wake atlas-ui on prompt-0); a matching return+verdict pair →
  that loop is closed. Count *.verdict.md — 4 means the gate is met.
holds: >
  /home/hruzam/ia-sync/.dev/session/voice-meetings/ is the living home — never prune it;
  single-voice runs only; battery fixed (paprika + blackout); no deploy.sh from this bed;
  commits to ia-sync by operator or @Delta only
next: >
  majkee runs loop 01 — paprika × claude-voice, single-agent version per RUNBOOK prompt-1 — and
  drops /home/hruzam/ia-sync/.dev/session/voice-meetings-01-threshold/loops/01.paprika.claude.return.md
expected: >
  that file exists with a transcript (paste or absolute path), the exact model version, and an
  examiner-leaks line (`none` or verbatim); atlas-ui is then woken on prompt-0
```
