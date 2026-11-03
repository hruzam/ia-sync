# Predeclared assessment — experiment_2

Written before dispatching either target turn. This trial has two fresh peer threads and
one target turn per peer; the same native caretaker operates both. It does not compare
caretaker versus direct operation, and does not isolate effort from other changes to G07.

| check | acceptance evidence |
|---|---|
| Receipt recovery | Local fake command completes; caller discards returned value; inspection still validates receipt and output hashes. |
| Uncertain completion | Pending live runner differs from dead/unknown runner; neither permits another invocation of that operation. |
| Integrity and duplication | Altered output is rejected; duplicate operation does not execute the fake command twice. |
| Recipient isolation | New IDs are distinct from one another and G07; exact peer marker and source-specific answer. |
| Peer A content | Cites GUIDE preflight/no-thread, first-send birth and zero-turn read/recovery; distinguishes preflight from task completion. |
| Peer B content | Cites initialize/account/model preflight, in-memory birth ID and save after successful turn/reconcile; failure is source-inferred, not live-observed. |
| Runtime | Recorded pinned CLI version; independent resume reports selected model/low/readOnly and networkAccess false. |
| Durable result | Ask exits zero; parent reads same latest completed turn; final text matches ask output without usage tail. |
| Bounds | Exactly one completed turn per fresh peer, <=180 final words, named source/read-command budget followed or discrepancy reported. |

Report target total input, cached subset, output, last-input context and wall time separately.
G07's initial pair is the nearest historical reference; compare only descriptively. Prompts,
read limits, runtime version/date, inherited instructions, caching and scheduling can differ.
No whole-route usage telemetry is available for Cartan and the native caretaker; no total
token-saving, subscription-quota or monetary claim can be scored from target totals alone.

The local receipt checks test a wrapper, not the transport's known first-turn persistence gap.
A disappeared/dead local runner cannot establish whether the remote side accepted a turn.
No live fault, compaction, cross-root persistence or destructive recovery is exercised here.
