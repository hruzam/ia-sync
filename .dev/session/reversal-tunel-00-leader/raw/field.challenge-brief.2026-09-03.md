---
provenance: Field · 2026-09-03 · for the CHALLENGE pass on Cartan's 01-instrument RUNBOOK
corpus: RETURN (ORACULUM-CARTAN-reverse-tunnel-return.2026-09-03.md) · POINT (cartan.point.2026-09-03.md) · HANDSHAKE.md · tunnel/GUIDE.md · cross-vendor-seat.md · tunnel-codex.zsh · t06-tunnel-v0-roundtrip.md
---

# Field challenge brief — reversal-tunel

## A · Forward-mechanics checklist

The reverse RUNBOOK must mirror each property or explicitly justify divergence (cite anchor).

| # | Property | Forward anchor |
|---|---|---|
| A1 | Thread birth on first send — `open --enable` persists `threadId:null`; thread/start + turn/start run in the SAME subprocess as first `send`; rollout exists before any cross-process resume | zsh:28-38 |
| A2 | Exit-code contract — 0/10/11/12/13/20/30/40/50 each named; downstream automation keys on these numerics | zsh:129-145 |
| A3 | Reconcile law — streamed vs read-back are dual-source; exit 50 on mismatch; neither source silently preferred | zsh:50, 136-140 |
| A4 | State handle discipline — explicit path only (`--state` or env var); exit 13 if absent; no hardcoded default; machine-local; never committed | zsh:108-119 |
| A5 | Law 2.4 gate — operator opens; no seat enables itself; every verb refuses without state file (exit 10); `close` re-arms | zsh:219-228 |
| A6 | Stdout purity — diagnostics on stderr; result text on stdout (send/ask/steer only); close/status produce no stdout | zsh:92-99 |
| A7 | Record-never-retry — on send failure the Claude seat did NOT re-enable or silently retry; HOLD stands | t06:141-143 |
| A8 | Close is local-only — removes local state file; never touches vendor-side artifacts (writer-locks, stored sessions) | zsh:79-88 |
| A9 | Resumed-steer only — no mid-stream steer across subprocesses; v1/daemon deferred | zsh:66-74 |
| A10 | Error-class fidelity — transport failure (exit 30) vs turn failure (exit 40) vs reconcile mismatch (exit 50) are distinct; conflation hides the real failure mode | zsh:129-145, t06:220-225 |

## B · Epistemic map — RETURN §C3 and §B4

Tag: OBS = Oraculum-observed CLI · DOC = documented-vendor · INF = architectural-inference.
Claims Cartan's live observation must confirm or overturn:

| Claim | §ref | Tag | Must confirm or overturn |
|---|---|---|---|
| Resume-while-running semantics — behavior of `--bg --resume <id>` on a RUNNING session id is unspecified | §C3 ¶3 | INF | Probe: attempt once; record whatever happens; do not assume rejection |
| Transcript completeness at Stop-time — `transcript_path` fully written before Stop hook fires (write-ordering) | §C3.3 | INF ("most likely to be wrong" — Oraculum) | Confirm or overturn: is the file complete and flushed at hook invocation? |
| Stop-hook payload parity under --bg — `last_assistant_message` matches `transcript_path` tail exactly | §C3.3 | INF | Confirm: if they can diverge, dual-source reconcile is theater |
| Subagent-transcript opacity — controller sees only the named seat's final yield in `transcript_path`; subagent text is not present | §B4 | DOC (seat CAN spawn subagents) + INF (transcript scope) | Confirm or overturn: if subagent text leaks into `transcript_path`, the reconcile boundary shifts without warning |
| Dedicated-agent hook — Stop/StopFailure hook fires from the seat's agent .md `hooks:` key, not from global settings | §A amendment | DOC (per-agent hooks exist) + INF (payload parity under --bg not live-confirmed) | Confirm: global hook = receipt pollution from every session |

INF-heavy cluster: all four live-semantics claims are inferences. Oraculum explicitly flags §C3 as highest uncertainty. These are the CHALLENGE's primary targets — any one being wrong redraws the reconcile boundary.

## C · Binding constraints — HANDSHAKE §TABLE + cross-vendor-seat.md

A reverse RUNBOOK could accidentally violate any of the following:

| # | Constraint | Anchor |
|---|---|---|
| C1 | Instrument tuple fixed at authoring — `tunnel` does not convert to `mail` on failure; failure lands in STATUS `holds:` with evidence; new instrument requires a numbered sibling session | cross-vendor-seat.md:21-27, Cartan amendment 2 |
| C2 | One RETURN per cycle (open → work → close), not per send — the cycle boundary defines the owed RETURN, not the message count | cross-vendor-seat.md:24 |
| C3 | Delivery rule — silence is not progress; worked reply or dated consumed-by stamp is receipt; a RETURN is not consumed until stamped | HANDSHAKE:28-40 |
| C4 | r4 wording owned by counter-sign flow (Oraculum + Cartan), NOT by the RUNBOOK — the RUNBOOK must not re-word HANDSHAKE §TABLE unilaterally | RETURN §B1 [INF] |
| C5 | Two births kept distinct — handle created by operator enable; stored session born on first task dispatch; the zero-session boundary is part of the proven mechanism | cross-vendor-seat.md:38-40, Cartan amendment 1 |
| C6 | No seat enables itself — Law 2.4; operator's hand opens the table in every direction | cross-vendor-seat.md:56-64 |
| C7 | One handle per host; no second open while TABLE is open; close before the owning session closes or is pruned | cross-vendor-seat.md:86-88, Cartan amendment 3 |
| C8 | Durable outcome lands as files — tunnel is transport, not the record; Delivery rule applies to those outcome files | HANDSHAKE §TABLE:100-104 |
| C9 | Named seat = dedicated agent .md; Stop/StopFailure hook scoped to that file, never global settings | RETURN §A amendment |
| C10 | Local-only close residue must be named — Cartan r3 prohibits unlinking Codex-owned coordination state; the reverse RUNBOOK must explicitly name what local-only close leaves behind in Claude-side storage | HANDSHAKE counter-sign r3:173-178 |

## D · Trap list from t06's FAIL

**What failed (forward):** `open --enable` called `thread/start` in a zero-turn preflight. On codex-cli 0.152.1 `thread/start` allocates a writer-lock but writes NO rollout file. Every subsequent verb ran in a fresh subprocess and opened with `thread/resume` → `-32600 no rollout found` / `thread not loaded`. All three verbs (send, read, resume) failed identically at transport (exit 30). [t06:108-116]

**Root cause:** no-daemon design; `open` and `send` are separate subprocesses; a zero-turn thread cannot bridge that boundary. `lastTurnId:null` in the state file was the early signal — present and unread. [t06:112-119]

**Fix applied (f32eb9a):** thread birth deferred to first `send` (thread/start + turn/start in one connection; rollout exists before any cross-process resume); `open --enable` persists `threadId:null`; exit 12 guards verbs called before any thread exists. [zsh:28-38]

**Residue finding (post-fix, t06 re-run 2):** the shim header claimed the fix "removed the stale-writer-lock residue class." Half-true only: thread/start (and its writer-lock) MOVED from `open` to `send`. `close` is still local-only; the lock remains. Residue class relocated, not eliminated. [t06:253-261]

**Reverse-direction analogs to probe:**

| Analog | Forward trigger | Reverse probe |
|---|---|---|
| D1 Empty-session resume | Zero-turn `thread/start` → no rollout → `thread/resume` fails -32600 | Does `claude --bg --agent <seat>` store a session ID before any task is dispatched? If so, does `--bg --resume <id>` on a never-tasked session fail analogously? Probe: open session, dispatch nothing, attempt resume from a fresh invocation. |
| D2 Local-only close residue | `close` left writer-lock at `~/.codex/thread-writer-locks/<id>.lock`; session state was not cleaned [t06:253-261] | What does reverse local-only close leave in `~/.claude` (session files, local cache)? RUNBOOK must name it; omission leaves the same half-truth the forward shim header made. |
| D3 Surface-error conflation | `steer` on a completed turn: app-server rejected first (-32600) → surfaced as exit 30, not exit 40; shim did not pre-guard completed-turn steer [t06:217-225] | What does `--bg --resume` return when targeting an already-stopped session? Is it the exit-code analog for HOLD, or a protocol rejection that could be mistaken for success? |
| D4 Cross-process session identity | Zero-turn threadId was unresumable across subprocess boundary | Confirm: a `--bg` session born in one invocation is resumable (`--bg --resume <id>`) from a later independent invocation without a no-rollout analog. This is the forward fix's mirror and the instrument's core survival condition. |
