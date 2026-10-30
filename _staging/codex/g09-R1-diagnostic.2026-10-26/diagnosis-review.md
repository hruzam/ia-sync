# Independent diagnosis review

2026-10-26 · `/root/g09_package_review` · read-only preparation/diagnosis reviewer.

VERDICT: PASS

TASK: Verify the prepared G09 R1 diagnosis artifacts, their source/evidence bindings, stated
limits, and recovery prerequisites without running probes or runtime/model operations.

RAN: Parsed all diagnostic JSON with jq; read all three probe helpers and candidate patch;
inspected run_operations.py and tunnel-codex.py; recomputed SHA-256 for source, R1 receipt,
vault and prompt; compared receipt/vault contents and timeout/checkpoint paths. No helper executed.

EVIDENCE: Source/receipt/vault/prompt hashes match. Exact prompt binds to thread
01a176f7-532b-7722-9324-0ecb92694073, turn 01a176f7-53a6-7b83-b203-b86b08ec15ac,
interrupted, 12 commands, 4 web searches, 3 commentary messages and no completed final.
Receipt/vault unchanged. PID observation directly proves namespace-dependent visibility,
not the original checker's namespace. Source deadlines explain the remaining wait; the exact
original RPC is unrecorded. Unapplied checkpoint preserves known ID without lastTurnId.
Adapter guard findings match actual source.

FAILURES: none; no unsupported causal promotion found in the submitted diagnostic artifacts.

REPRODUCE: Recompute SHA256 of zsh/ai/tunnel-codex.py and G09's R1 receipt/vault/prompt;
parse diagnostic JSON; compare helper/source code statically. Probe output files are exclusive
evidence and should not be overwritten by casually rerunning their scripts.

RESIDUAL RISK: Recovery uses the exact recovered ID, zero-turn read/resume only until a new
grant, no resend and no commentary-as-completion. Before further dispatch, normalize structured
read-only state; permit identity-only recovery without completed lastTurnId; retain completed
bootstrap checks for normal dispatch; recheck pins/release. Checkpoint cannot recover an ID
when the client never received thread/start's response.
