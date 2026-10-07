---
type: field-feedback
date: 2026-10-07
author: trajectory(support) · requested by majkee
source_session: nablarva-X0-restarted (2026-10-05 … 2026-10-07, office hruzam-120922)
evidence: ~/unikuklatrix/nablarva/.dev/observations/nablarva-X0-restarted.trajectory.2026-10-05.md (complete-grain, T1–T11) · history nablarva@d1c4b1e:.dev/session/nablarva-X0-restarted/raw/
shim: ia-sync/zsh/ai/tunnel-codex.{zsh,py} @ ffee9f6 · codex-cli observed 0.160.0 → 0.160.1 (managed daemon)
status: backlog for the transport owner — nothing here is built except F7 (done)
---

# Tunnel field feedback — nablarva-X0 (first multi-seat use)

This is the first real use of the tunnel with several seats: one carrier (oraculum, Claude), one
bound Codex head (Cartan), an Atlas seat on a yielded slot, and the operator switching between
the TUI and the tunnel. It covered about 17 turns, one context reset, two re-binds and one Codex
upgrade during the session. Each entry is a short summary with a pointer to the full evidence
(`§Tn` = section in the observations file named above). Point, never copy.

## Defects and gaps — ranked

| # | sev | finding | evidence | proposed change |
|---|---|---|---|---|
| F1 | high | **0.160.x: the TUI is a client of the shared managed daemon** (`codex app-server --listen unix:// --managed-daemon`). After TUI `/exit` ("Disconnected… Any running work continues"), the daemon holds the thread as its writer. The shim's own `app-server --stdio` then fails `thread/resume` with `-32600 thread … already has an active writer`. This time it cleared within about 3 min. The release interval is not characterised. The guide's rule "TUI /exit = release" is broken. | §T10 B | (a) **connect the shim to the daemon** (`--remote unix://` exists on 0.160.1). That removes the writer conflict and the TUI sees tunnel turns live. This is the structural fix, but it needs a protocol study first. (b) Stop-gap: `tun resume --wait` polls `~/.codex/thread-writer-locks/<id>.lock` until it is gone, with a bounded timeout, and never touches the lock. (c) Guide/user-run: rewrite §Switching TUI↔tunnel. |
| F2 | high | **Approval requests are declined silently.** `_auto_decline` (`tunnel-codex.py:414`, called at :409 and :487) answers every server→client request with an error. The escalated command fails, and no stderr line, state field or exit code shows it. | §T1 | Report every decline: one stderr line (method + command summary) plus a `declinedApprovals` list in the state file, shown by `tn-st`. Keep it a decline; just make it visible. |
| F3 | high | **A timeout kills the turn.** Deadline → `ProtocolError` (:483) → `finally transport.close()` (:844-845) → the app-server is terminated → the server turn is interrupted. The default of 120 s is too low for design turns. Observed: 269 s and 362 s on turns that succeeded. | §T5 1 | Raise the default, or (better) make the timeout cover inactivity rather than the whole turn. Document in GUIDE §Usage that a timeout is not a give-up. Use `TUNNEL_CODEX_TIMEOUT=1800` for design turns until then. |
| F4 | med | **`_stamp_runtime` omits `approvalsReviewer`.** `tn-st` cannot show whether auto-review is active; the rollout has to be read. | §T9, §T11 | Add `approvalsReviewer` (and the permission profile id if it is present) to the stamped keys. |
| F5 | med | **Approval and reviewer cannot be set from the tunnel.** The 0.160.0 schema accepts `approvalPolicy`/`approvalsReviewer` on `ThreadResumeParams` and `TurnStartParams`. The shim sends neither. The only route today is a TUI round trip, and that trips F1. | §T1, §T10–T11 | Open-time knobs `tun open --approval-policy … --approvals-reviewer …` (law 2.4: intent is set at open, never per send). The same reasoning as the declined per-send sandbox override applies. |
| F6 | med | **A TUI policy change lives in `thread_settings_applied` events, not in `turn_context`.** `turn_context` is written only when a turn runs. My first check read it and reported stale state twice. | §T10 A | Guide/user-run: the correct check is `grep '"thread_settings_applied"' <rollout> \| tail -1 \| jq '.payload.thread_settings'`. Better: after F4, `tun resume` + `tn-st` is the check. |
| F7 | low | Exit 13 read as "must run from the bed folder". | §T3, §T6 | **DONE** ia-sync `ffee9f6`: an added stderr hint says the address is per shell. Deployed, selftest 96/96. |
| F8 | low | **Lock residue and race.** Only send/ask/steer take `<state>.lock`. `close` removes it even mid-turn. O_EXCL create-then-write-pid has a window where a second caller reads pid 0 and treats the lock as stale. Inferred from source, not reproduced. `lastTurnId` advances only on success, so `steer` after a timeout targets the previous turn. | §T2 (with Cartan's audit) | Write the pid atomically (tmp + link/rename). Have `close` refuse while a live pid holds the lock. Have steer refuse when the last verb ended in error. |
| F9 | low | `tn-use <slug>` resolves under `$RB_ROOT` (`~/ia-sync/.dev/session`), so beds in other repos need an absolute path. | §T2 | Accept `<repo>:<bed>`, or resolve from the git root of `$PWD`. Or just document it. |
| F10 | low | A thread created by `/clear` (or `/new`) and left with zero turns has no rollout, so `resume` gives `-32600 no rollout found`. The id is unusable. This is the same fact as the shim's THREAD BIRTH note, now observed on the TUI side. | §T8 | Guide/user-run §Context reset: give the new thread a real first turn (the rebrief) before binding. Prefer `/compact` when the thread id must survive. |
| F11 | info | `.gitignore` in consumer repos: `**/tunnel*.state.json` misses `.lock`/`.tmp` residue. | §T2 | Recommend `**/tunnel*.state.json*` in the guide. |

## Process lessons (for the guide / protocol, not the shim)

- **No `<placeholders>` in paste-ready lines.** zsh reads `<…>` as a redirect (§T8). Write
  `NEW_ID` and add a "replace" note.
- **Context reset at about 80 %** came after about 15 turns. One rebrief turn produced a 1.5 MB rollout,
  so a fresh head does not start light (§T7, §T9).
- **Bind ≠ birth, again:** after a reset, model and effort follow the TUI defaults
  (`gpt-6-astra/xhigh` → `gpt-6-sol/medium`). Check runtime after every re-bind.
- **The carrier trace shape works and is worth standardising:** background ask, stdout
  `.out`, stderr `.err`, `.meta` with start, end, exit and turn id (§T5).
- **An approval slot belongs in any multi-seat protocol:** when a decline is reported, the
  carrier logs it, asks the operator, and carries the decision back as the next turn.

## Open verifications (owner: whoever next drives a live tunnel)

1. On 0.160.1, does a tunnel turn run with the thread's stored `approvals_reviewer: auto_review`?
   Check the last `turn_context` after the first tunnel turn (§T11).
2. L8 on 0.160.1: run the selftest and one live `ask`. Only a `resume` has been proven so far (§T10).
3. Characterise the daemon's writer-release delay after TUI `/exit` (F1).
