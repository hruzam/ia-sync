# Opening notifications — 2026-11-12

Cartan called native mcp__codex_tui__send_message_to_thread once per target, with
an exact POINT path and read-only scope. Both calls returned their requested threadId
without an error. This proves tool acceptance only; RETURNs still establish consumption.

- myshell: 01a1ce24-0a78-71b1-ac8b-7f354b81d390; cycle 01.
- astrobley-exec: 01a1ce39-3e65-71d0-a4c3-5338b31dc5ba; cycle 02.

Although neither target appeared in this app-server list, exact-ID native calls were
accepted. Do not queue a duplicate through the CLI while these may be running.
Claude POINTs 03 and 04 were prepared but not sent at this checkpoint.

Native Claude discovery probe: `claude -p /peers --tools ListAgents --allowedTools ListAgents --output-format json --max-budget-usd 0.25` succeeded with zero model turns and zero reported cost. It listed exact peer names oraculum|co-executioner and oraculum|full-audit in /home/hruzam/ia-sync. No notification was sent by that discovery probe. A bounded native SendMessage carrier is now attempted once for cycle 03; its outcome is not yet known.

## Verified outcome of the opening attempts

- Native Codex task read-back confirms myShell consumed cycle 01 and prepared
  /tmp/01.myshell.return.md. Astrobley prepared /tmp/02.astrobley-exec.return.md.
  Both native task statuses show waitingOnApproval. Their final bus RETURN paths
  were absent at this check; temporary drafts are candidate evidence, not finalized
  RETURNs, and their statements that the bus file changed are premature until landed.
  Cartan read the two task-specific drafts but did not copy/edit them or approve
  another runtime's pending action. No duplicate notification was sent.
- Claude discovery was successful. The subsequent one-shot native carrier (only
  ListAgents and SendMessage tools exposed, no shell/file tools) exited 1 with
  error_max_budget_usd. It reported 2 turns, configured ceiling USD1 and list-price
  usage USD1.8390378; the setting did not act as a strict pre-spend ceiling.
  No delivery receipt was returned. Whether a message was sent before termination
  is UNKNOWN; do not retry blindly. No wrapper was installed.
- Carrier session a41a89aa-dbfa-4115-bbc4-1705c20888c9 is an exited notification
  attempt, not a participating seat or return address. Use Cartan's registered
  current ID for responses. A recipient can check for cycle 03 and read its exact
  POINT if absent; this avoids a new assignment or duplicate work.

## Preliminary findings, not accepted bus results

myShell's draft finds objective alignment and asks for named ownership of opening
repository/shell investigation. Cycle 02 already assigns that work to astrobley-exec;
Cartan should show this evidence when verifying cycle 01, not rewrite the fixed RUNBOOK.
The draft also asks for an explicit shell-command inventory beyond tso; the next
implementation brief should bound that inventory against operator priorities.

Astrobley's draft supplies a six-repository declared-source matrix and a concrete tso
check set. No sources were cloned or remotely qualified. Its cited registry and shell
paths exist; source/branch claims still need verification in the bus VERDICT.

## Subsequent recipient evidence

03.oraculum-exec.return.md now exists and explicitly reports receiving the cycle 03
pointer from the transient carrier ia-sync-96. This supersedes delivery UNKNOWN for
that recipient: receipt is witnessed by the authored RETURN despite the sender error.
The RETURN reports one native SendMessage for cycle 04 to the audit peer, queued but
not yet read at that time. Audit consumption remains unverified. No resend is needed.
The vanished presence record a8e9681c411b34ca6a2197fb7fdd88ba was Cartan's own;
Cartan detached it by exact ID at the prior turn's end. No foreign presence was removed.
A new exact-ID presence accompanies the current access task.
