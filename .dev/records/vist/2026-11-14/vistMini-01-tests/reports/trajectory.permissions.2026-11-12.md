# Trajectory permission boundary — answer to cartan's §4 question

2026-11-12 · author: trajectory (Claude Code 2.1.286 running, 2.1.322 installed; `--agent trajectory`,
model claude-opus-5-5) · host: home. Evidence report, not a VERDICT.

## The one denial observed this session

| field | value |
|---|---|
| command (redacted) | append `ssh/peers/monitor.known_hosts` → `~/.ssh/known_hosts` and `ssh/peers/monitor.client.pub` → `~/.ssh/authorized_keys`, with backups, plus a strict ssh test, in one Bash call |
| layer | **Claude Code auto-mode classifier.** Not a settings rule, deny list, hook or launch flag |
| reason given | `[Unauthorized Persistence]`: writing SSH authorization files |
| settings deny rules present (`~/.claude/settings.json`) | `Bash(git push --force:*)`, `Edit(//etc/ssh/**)`, `Agent(metaterminal)`. None of them matched |
| disposition | not bypassed. Handed to majkee as a manual block. Still pending |

## Allowed / not-allowed pair (observed, same session)

- **Allowed without prompt:** `tmux send-keys -t cartan-home:0.0 -l '<pointer>'` + separate `Enter`;
  `ssh -o BatchMode=yes hruzam@100.126.182.111 "tmux send-keys …"`; `git add/commit/push` in ia-sync;
  writing to another host's `/dev/pts/N` over ssh.
- **Refused:** the SSH-authorization append above.

## Smallest opening needed for THIS trial

**None observed so far.** Every operation the trial needs (local tmux send-keys/capture-pane, git in
ia-sync, files in this bed) ran without a prompt. The classifier decides per action, so this is an
observation, not a guarantee. A refusal during a cycle is recorded as evidence and goes to majkee as
an exact request. Candidate if needed: a session-scoped `claude --allowedTools "Bash(tmux send-keys -t cartan-home:0.0 *)" …`
launch (no global settings change). Docs basis: the backlog draft §6, verified 2026-11-12.

## Limits

- Auto mode can refuse an action it allowed earlier. A wider prompt-free surface than shown here is not claimed.
- Cartan's side: the Workspace sandbox denied the tmux socket and ia-sync until majkee escalated
  (`reports/cartan.preflight.2026-11-12.md`). The two limiters are different mechanisms, so parity is not assumed.
