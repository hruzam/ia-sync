---
title: Codex server with separate desktop and Redmi interfaces
date: 2026-09-11
recorded_at: "2026-09-11T22:37:35+02:00"
author: Cartan
host: office
session_id: "01a0918e-9ab0-7053-88d8-d829f1fad954"
transcript: "/home/hruzam/.codex/sessions/2026/09/11/rollout-2026-09-11T19-40-37-01a0918e-9ab0-7053-88d8-d829f1fad954.jsonl"
test_thread_id: "01a091fe-3ef5-7451-8eab-2f6126a95c77"
authority: observation
result: local-inspection-and-operator-confirmed-probe
---

# Result

The operator demonstrated the intended pocket workflow on Redmi: a separately
rendered Codex interface to the office test conversation, an approval answered on
the phone and reflected in both desktop interfaces, and continued conversation
after the requested mobile-data and phone-lock/reconnect sequence.

This is a bounded working trial of `codex --remote` with App Server. It is not a
test of `codex remote-control` pairing or an OpenAI Android app connection. The
phone still uses Termux and SSH; its Codex interface executes on office.

## Setup actually used

- Installed CLI: `codex-cli 0.154.0`.
- Office server, started by the operator in an ordinary terminal:
  `codex app-server --listen unix:///run/user/1000/codex-pocket-test.sock`.
- Two separate desktop Codex processes connected to that endpoint, outside tmux.
  A host process inspection observed the server on `pts/4` and clients on
  `pts/32` and `pts/31`; neither client had a `TMUX` environment marker.
- The working conversation is the `test_thread_id` above. These are interfaces
  to that conversation, not three separately prompted agents.
- Redmi's existing SSH key forces entry into the `agentive` tmux session.
  Cartan therefore prepared a separate detached `pocket-codex` session with its
  own Codex interface. No SSH-key or forced-command changes were made.

Phone-view creation command, retained as evidence rather than a command to rerun
over an existing session:

```sh
tmux new-session -d -s pocket-codex -n codex \
  -c /home/hruzam/ia-sync -x 45 -y 24 \
  /home/hruzam/.local/bin/codex resume \
  --remote unix:///run/user/1000/codex-pocket-test.sock \
  01a091fe-3ef5-7451-8eab-2f6126a95c77
```

Immediately after creation, tmux reported pane `%29`, `command=codex`, `dead=0`,
no attached clients, and initial dimensions 45 by 24 character cells. Those are
initial test dimensions, not a measurement of Redmi's eventual display.
Only the phone attaches to this tmux view; the desktop interfaces keep their own
terminals. This avoids using the desktop's terminal dimensions for the phone.

## Evidence and limits

| Check | Observation | Basis / limit |
|---|---|---|
| Two desktop interfaces | Both remained open and displayed the same conversation. | Operator report plus separate host process/TTY inspection. Exact text wrapping was not independently measured. |
| Shared approval state | Both desktop interfaces displayed a pending request; approving in the second cleared it and showed `pocket-approval-ok` in both. | Operator confirmation. Does not establish an exactly-once execution guarantee. |
| Phone display | After selecting `pocket-codex`, the operator answered “nice - working” to the portrait-fit check. | Operator visual assessment; no screen capture or layout measurements. |
| Phone approval | The operator approved the `/usr/bin/printf 'phone-approval-ok\n'` request on Redmi and confirmed the result in both desktop probes. | Operator confirmation across the three interfaces. |
| Return while mobile | The operator confirmed `phone-return-ok` appeared on phone and desktop after the requested mobile-data, approximately two-minute lock, and return/reconnect sequence. | Operator report; elapsed lock time and network path were not independently measured. |

An earlier proposed thread, `01a091e1-3add-7062-bda6-62dadb686147`, failed resume
with “no rollout found.” Its referenced rollout file and saved-thread row were
absent when checked. Cartan proposed sending a first ordinary message as a
discriminating check. The later successful test used the different ID recorded
above; the evidence does **not** prove that first-message persistence alone
explains the earlier failure or the change of ID.

## Current use and remaining boundary

On Redmi, connect with `bed office`, then press **Ctrl+B**, release, press **s**,
and select **pocket-codex**. Repeat that selection after an SSH reconnect if needed.

Keep office awake and the foreground server terminal open. The server has not
been installed as a supervised background service. Server shutdown, host sleep or
reboot, loss of all clients, and recovery after those events remain untested.
This trial does not establish a reliability rate or performance/cost estimate.

The existing Cartan audit conversation was not migrated to App Server. Adoption
for real work still needs a deliberate choice about server lifetime and how
existing sessions enter it. This raw observation does not change the original
wrapper RUNBOOK, its STATUS ownership, or its deployment rules.

The documented connection mechanisms are in the [CLI reference](https://learn.chatgpt.com/docs/developer-commands?surface=cli)
and [App Server protocol](https://learn.chatgpt.com/docs/app-server). Local CLI help
and the observed trial provide the version-specific evidence here.
