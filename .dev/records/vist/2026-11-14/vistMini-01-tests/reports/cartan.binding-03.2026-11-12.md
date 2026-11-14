# Cycle 03 binding registration

2026-11-12 · home:cartan · baseline `e5a5925` · commit BEFORE adapter changes.

The operator relaunched the endpoints. Read-only `tmux -L default display-message` and `/proc/<pane_pid>/cmdline` first-argument/executable inspection at09:24:38Z found:

| Binding | Session | Foreground | Root PID | Root argv0 basename | Result |
|---|---|---|---|---|---|
| default:%3 | traj-home | claude | 1845156 | claude | direct agent, lifetime precondition now satisfied |
| default:%2 | cartan-home | codex | 1844624 | codex | direct agent, lifetime precondition now satisfied |

Claude executable resolves to the installed2.1.322 version; Codex argv0 and executable resolve to its native vendor binary. No process arguments beyond argv0, private operator draft or thread handle is retained here. Both panes are116 columns wide. Root PID/start-time, renderer, busy, composer and reservation checks remain unchanged. `%0` and `%1` become unregistered and must refuse before any tmux call. The binding is host-local to this live server lifetime, not a portable identity guarantee.

## Changes registered

1. Change only the two static live adapter entries to `%3→claude` and `%2→codex`. Preserve `vist-test`, every lifetime/readiness guard and all C/T fixtures. Extend C17/T14 to show old `%0`/`%1` also refuse locally. No global configuration, deploy, live interruption or manual trial poke.
2. Notification paths for this live trial are **relative to the fixed session bed** `/home/hruzam/ia-sync/.dev/session/vistMini-01-tests/`, never to either shell's cwd. Thus `read reports/trial-msgs/01.trajectory.md` identifies the absolute file under that bed. Envelopes/body pointers retain the absolute base. This is a scoped, explicit path binding, not another mailbox/registry or changed canon. Full repo-relative reverse pointers are121 bytes at the originally suggested ID and would wrap; shorter bed-relative pointers preserve message IDs and sender identity without weakening the no-wrap guard.
3. To satisfy POINT03's requirement that both `--check` calls pass before a send, a small `scripts/handoff-once.sh` may perform a bounded delayed command. It sleeps8 seconds once to let its controller finish the current turn, checks `%2` and `%3` exactly once, then sends exactly one pointer through the adapter only if both checks exit0. Any refusal exits, with UTC/mode/pane/result printed; no loop, watcher, daemon, manual fallback, clearing or retry. Launch it through the existing tool's ongoing-process facility and end the controller turn; retain its output under `/tmp` for the next received pointer. This is one scheduled tool action, not a standing process. It accepts only target `%2` or `%3` and explicit pointer/state directory; fixed server default. Both seats may use it for their assigned handoffs.

## Registered verification and trial schedule

- Run unchanged C01–C18 and T01–T16 semantics, adding stale-endpoint examples to the existing forbidden-binding cases. Every test fixture remains on `vist-test`; no live adverse case.
- Run read-only live checks. A controller's active receiver is expected to refuse busy24; this is not a successful initial readiness proof. The delayed one-shot must obtain actual check0 from both after the turn ends BEFORE its send. Root-direct evidence alone never substitutes for readiness0.
- Thread01: Cartan writes/commits `reports/trial-msgs/01.cartan.md` (UTC envelope, ack reply, hop1/2, one real question), then schedules its one-shot. Its actual adapter calls/results are recorded by the one-shot output; no success is preclaimed. After the pointer arrives, Trajectory owns the Git window, writes/commits matching `01.trajectory.md`, and sends its reply via the adapter when Cartan is idle. The next Cartan message waits for that reply pointer.
- Threads02/03 repeat under the same ownership/receipt contract. Cartan then writes `03.cartan.return.md` with actual calls and matched receipts, commits only, and sends its RETURN pointer through the adapter. Trajectory alone pushes and writes VERDICT03.
- If any one-shot fails, preserve its log/reservation, record the failed stage and stop. No automated re-poke or manual input counts. The local runtime log is diagnostics, not STATUS or consumption. Promote its exact outcomes into Cartan's report in the next Git window.

The unrelated untracked `nano.1844235.save` (1221 bytes, predates this work) remains untouched and unstaged; only assigned paths are committed. It is not evidence or an input to this trial. No observer reads its contents.
