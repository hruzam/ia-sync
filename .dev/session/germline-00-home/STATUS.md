# STATUS: germline-00-home

```yaml
updated: 2026-09-25 15:30 CEST
writer: atlas-ui · claude
host: office (hruzam-120922)
worktree: >
  /home/hruzam/ia-sync · main · 4db6745 · dirty — this session = .dev/session/germline-00-home/STATUS.md;
  NOT ours = .dev/session/runbook-upgrade-02-app/STATUS.md, journal.host-cleanup.md, pulse.md (other seats).
  /home/hruzam/reposoma · e8c5b30 · clean for this session (.germline/ committed; old dirs removed)
gate: >
  After commit + deploy, a fresh Claude session and a fresh Codex session each resolve
  buffering-cycle from ~/reposoma/.germline/skills/ via chatbot-port (update-ask path answered
  no; --check reports equal), with ~/.germline resolving on office and .shared/ +
  raw.shared-skills/ absent from reposoma - three receipts recorded in STATUS.
checkpoint: >
  prompt-1 complete and verified 2026-09-25 15:26 — deploy.sh ran whole-table (operator output pasted
  to atlas-ui); live == table for both chatbot-port twins (~/.claude/skills/chatbot-port/SKILL.md,
  ~/.agents/skills/chatbot-port/SKILL.md); readlink ~/.germline = /home/hruzam/reposoma/.germline;
  git -C ~/reposoma ls-files .germline = README.md, CHATBOT.md, skills/skill.buffering-cycle.md;
  .shared/ and raw.shared-skills/ absent. Receipt 3 of 3 (symlink + absence) is therefore RECORDED HERE.
  Side effect, by majkee's call = the ovitmugen seat's committed zsh brick (0b95adf) went live in the same deploy.
in_flight: none
recovery_probe: >
  diff -q /home/hruzam/.claude/skills/chatbot-port/SKILL.md /home/hruzam/ia-sync/claude/skills/chatbot-port/SKILL.md;
  readlink /home/hruzam/.germline — both silent/resolving = prompt-1 holds, only the two fresh-session
  receipts are missing; any difference = re-run bash /home/hruzam/ia-sync/deploy.sh (idempotent) before prompt-2
holds: >
  proofs are interactive sessions only — print mode -p is never used; the Claude proof answers the
  update-ask with "no" (no re-fold, no overwrite); _staging/codex/ untouched; .germline/agents/ stays empty;
  no sync.sh (would overwrite the table with live copies — currently equal, but the rule stands)
next: majkee runs prompt-2 (RUNBOOK) — fresh Claude session `/chatbot-port buffering-cycle` → answer no, then `/chatbot-port --check`; fresh Codex session `$chatbot-port buffering-cycle` → no, then `$chatbot-port --check` — and pastes both receipts to atlas-ui
expected: "Claude receipt shows the update-ask for skill.buffering-cycle.md and --check silent/equal at @8da748a; Codex receipt shows the same two outcomes from ~/reposoma/.germline/skills/ — atlas-ui records both verbatim in checkpoint and closes the gate"
```
