# Codex inbound channels — cycle04 research

2026-11-12 · home:cartan. TaskA researched by a bounded researcher child; Jev evidence crawled independently by two read-only children after majkee's steering. Cartan checked current tool metadata, local CLI help/version, Jev handoff/CACHE/VERDICT excerpts and the one authorized Astra contact result. No queue/exec turn, daemon, setting change or tmux input was performed.

## Candidate comparison

Home CLI reports `codex-cli 0.167.2`. Available syntax is not proof that another process can submit to the current displayed TUI safely.

| Candidate | Status / local version evidence | Live displayed thread? | Non-Codex sender requirements / limit |
|---|---|---|---|
| App-server JSON-RPC `thread/resume` then `turn/start` | Documented API; local app-server/schema commands labelled experimental | Can address a stored thread; joining another live writer was not established | Initialized client and actual server transport/endpoint, thread ID; listener authentication for nonlocal connections. A fresh subprocess is not automatically the TUI's owner. |
| `codex queue --thread ID --message TEXT` | Documented command, present in0.167.2 help; optional `--resume` | Intended existing-session queue; live owner delivery/wake/busy behavior not proven here | CLI and exact ID/name; selected local/remote server for resume, appropriate auth for remote. Resume may warn yet exit successfully. Without resume, active-writer behavior/daemon effects and receipt are unverified. No queue was sent. |
| `codex exec resume ID PROMPT` | Present in local help | Resumes stored state in a noninteractive process; safe attachment to a concurrent foreground TUI is unverified | CLI/session identity and execution authorization. Do not assume a new process is an inbound message to an existing owner. |
| Current `mcp__codex_tui__send_message_to_thread` | Available tool metadata: existing task follow-up, max1000 UTF-8 bytes; optional model omitted | Jev supplies historical same-host main-peer evidence. Current Astra target fails during resume with active-writer conflict | Requires this enabled tool/current task ID; no auth/socket argument exposed. No equivalent external Claude/script entry was established by Jev. Acceptance itself is not consumption. |
| PTY / pipe / tmux | Input works for owned CLI subprocesses; no plain pipe target binding to another TUI | Byte transport, not a thread API | Needs correct process/PTY ownership and submission semantics. Cycle03 reverse failed27 and the operator supplied Enter; timing/paste explanation remains a hypothesis, not a verified fix. |

Official sources: [app-server lifecycle/transports](https://learn.chatgpt.com/docs/app-server), [queue/CLI commands](https://learn.chatgpt.com/docs/developer-commands?surface=cli#codex-queue). These describe supported surfaces, not a receipt from our live target. CLI help was checked locally; no credentials or private process arguments were read.

## Jev: the earlier working Cartan route

Newest relevant bed is `/home/hruzam/ia-sync/.dev/session/jev-01-codex-pilot/`; cooperation artifacts landed in `d911046379b5981b831e5811b0dd288ec8f935b2`. The handoff and RUNBOOK explicitly place both peers on **office**. Two existing **main** Codex sessions exchanged native TUI notifications. This was not a spawned-child `collaboration.send_message` exchange.

The recorded call in `raw/HANDOFF.tui-bus-substrate.2026-11-10.md:24–41` is:

```javascript
await tools.mcp__codex_tui__send_message_to_thread({
  threadId: "01a1aa8a-b5d4-70d3-9823-4f44f05af2d2",
  prompt: "Received RETURN. VERDICT and next POINT are available at the exact bus paths."
});
```

The handoff says incoming events carried `source_thread_id` and an input path. Model was omitted. Durable ownership and verified results remained in `_bus`; tool acceptance alone was never treated as reading/completion. No duplicate nudges or overlapping assignments were allowed.

Evidence beyond the handoff note: `CACHE.md:219–233` records native notifications for cycles09–11; `_bus/11.cartan-reader.return.md` reports the assigned work; `_bus/11.cartan.verdict.md:13–26` independently checks diffs, eight tests and the original counterexamples. Cited artifacts include `raw/reader-cycle-11/before-check.json`, `change-0.diff` and `raw/reader-cycle-11-cartan-check.json`. Cartan inspected the handoff, CACHE and independent VERDICT excerpts; the crawlers checked the supporting artifacts. No raw transport envelopes/message IDs or proof that both seats shared one server process were found. The source explicitly disclaims permanent handle availability and cross-host transport.

Office/server clarification from majkee's steering: `raw/context-capture.2026-11-10.json:4–21,415–423` records office/hruzam-120922, observed CLI0.167.0, an `app-server-daemon/releases/0.167.0...` package path, and head metadata `originator=codex-tui`, `source=vscode` (session started on0.164.0). That is not the same observed frame as today's home CLI0.167.2. Package provenance does not establish a running server's PID/socket or prove which backend hosted both peers. `RUNBOOK.md:84` says no Claude carrier/tunnel, but that does not establish absence of an underlying Codex app-server.

The tunnel wrapper itself documents and implements a fresh `codex app-server --stdio` subprocess per invocation (`zsh/ai/tunnel-codex.zsh:19–22`, `tunnel-codex.py:264–289`). Jev's observed front-end call was the TUI tool, not that shell wrapper. The records do **not** establish whether both ultimately shared an office app-server backend. No endpoint/ownership receipt was found; the operator has been asked for the earlier launch command and shared-server details. No server was contacted or started to infer the answer.

Thus Jev demonstrates a working runtime-native peer channel plus file-based consumption/verification. It does not demonstrate an external Claude adapter or a workaround for an independently held writer.

## Current Astra contact — observed mismatch

The task-supplied target `01a1ceb4-452c-76e0-954a-3160ceadc2ed` is readable through the current tool: correct `oraculum|v:codex,cwd:nablarva` title/cwd, status `notLoaded`, zero turns. The exact Jev-native send tool was attempted once, with the authorized question and no model override. It returned:

```text
thread/resume failed: thread 01a1ceb4-452c-76e0-954a-3160ceadc2ed already has an active writer (code -32600)
```

A subsequent read and nonblocking wait still showed `notLoaded`, no turns and no answer. Stored readability and writer ownership disagree; this is evidence, not grounds to unlink a lock or commandeer the session. Different client ownership/state or changed runtime behavior are possible explanations, **not established causes**. No second send or alternate queue was attempted, because active-writer behavior and duplicate/orphan delivery were unverified.

`reports/oraculum.vist-context.2026-11-12.md` preserves the contact receipt, explicitly not an Astra-authored VIST answer. A next bounded probe should first establish the owning endpoint/current handle, then test one native/queue delivery with an explicit file receipt. Queue/exec are candidates, not already-verified live doors. No daemon or watcher was left running.

## Operator Enter clarification

Majkee explicitly says he pressed Enter for t03 and POINT04. t03's previously unverified submission route is therefore **operator relay**, not an adapter success. Trajectory's fast-burst/paste-window explanation and observed success with sleep1 are a useful hypothesis; no controlled test here establishes causality or makes keystroke delivery the recommended next step.
