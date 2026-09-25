# STATUS: germline-00-home

```yaml
updated: 2026-09-25 (prompt-0 done; time in git)
writer: atlas-ui · claude
host: office (hruzam-120922)
worktree: >
  /home/hruzam/ia-sync · main · b2b7901 · dirty — this session = AGENTS.md,
  claude/skills/chatbot-port/SKILL.md, .dev/session/invariance-autonomy/raw/master-brief.2026-09-23.md,
  .dev/session/germline-00-home/ (untracked); cartan = codex/skills/chatbot-port/SKILL.md,
  _staging/codex/germline-home.return.2026-09-25.md (untracked); NOT ours = zsh/AGENTS.md (ovitmugen seat).
  /home/hruzam/reposoma · 2b12c55 · dirty — this session = .germline/ (untracked), pulse.atlas.md,
  _active/presence.6216b5b6f62207de689452cdd1e44c74.md (untracked); to remove = .shared/, raw.shared-skills/ (untracked)
gate: >
  After commit + deploy, a fresh Claude session and a fresh Codex session each resolve
  buffering-cycle from ~/reposoma/.germline/skills/ via chatbot-port (update-ask path answered
  no; --check reports equal), with ~/.germline resolving on office and .shared/ +
  raw.shared-skills/ absent from reposoma - three receipts recorded in STATUS.
checkpoint: >
  prompt-0 complete and verified — /home/hruzam/reposoma/.germline/{README.md,CHATBOT.md,skills/skill.buffering-cycle.md}
  exist (CHATBOT.md = chatbot-facing saddle — repo + path + read rules, no index; port byte-identical to the .shared copy); Claude twin, master-brief (l.72 → .germline/agents),
  pulse.atlas.md, ia-sync AGENTS.md repointed; pulse.md router line already committed in b2b7901
  (swept in by the muticula commit); Codex twin synced by cartan (uncommitted). Remaining `.shared`
  strings are not ours (cartan's historical text in the brief l.289; pulse.atlas.md l.2546 larva.dev entry)
in_flight: none
recovery_probe: "readlink /home/hruzam/.germline; ls -d /home/hruzam/reposoma/.shared /home/hruzam/reposoma/raw.shared-skills 2>&1; git -C /home/hruzam/reposoma ls-files .germline — no link + both dirs present + ls-files empty = prompt-1 never started; link present but dirs present or ls-files empty = prompt-1 partial, rerun the unmet lines of prompt-1 (all idempotent except ln, which fails loudly if the link exists); link + dirs absent + ls-files lists 2 files = prompt-1 done, go to prompt-2"
holds: "rm -r limited to /home/hruzam/reposoma/.shared and /home/hruzam/reposoma/raw.shared-skills (operator only); ia-sync commit = explicit paths only (AGENTS.md, claude/skills/chatbot-port, codex/skills/chatbot-port, .dev/session/germline-00-home, the master-brief) — zsh/* belongs to the ovitmugen seat, cartan-muticula bed to its head; pulse.md already committed, do not re-stage others' rows; _staging/codex/ untouched; no sync.sh before deploy.sh; no -p ever; .germline/agents/ stays empty"
next: majkee runs prompt-1 (RUNBOOK) in an office shell — rm the two dirs, ln -s the symlink, commit reposoma (.germline pulse.atlas.md _active/presence.6216b5b6f62207de689452cdd1e44c74.md), commit ia-sync by explicit paths, push both, bash /home/hruzam/ia-sync/deploy.sh — then tells atlas-ui
expected: "readlink /home/hruzam/.germline = /home/hruzam/reposoma/.germline; both old dirs absent; git -C /home/hruzam/reposoma ls-files .germline lists README.md + CHATBOT.md + skills/skill.buffering-cycle.md; diff -q /home/hruzam/.claude/skills/chatbot-port/SKILL.md /home/hruzam/ia-sync/claude/skills/chatbot-port/SKILL.md silent (deployed == table)"
```
