# G09 run-01 — closeout report

2026-10-26 · Cartan, replacement cleanup integrator.
Reconstructed from preserved evidence after Majkee reported killing the failed local head.
This is not the old head's introspective self-report. Unknown measurements remain unknown.

## 1. Goal and observed outcome

Goal: build a read-only zsh browser for germline, guides and native skills while testing a
fresh main delegating consultation mechanics. Planned roles were main architect, caretaker,
native Astrobley and two tunneled research/audit roles with substantive follow-ups.

Actual work stopped during C1. R1 consumed one attempt and completed no validated consultation.
A1, D1/CONTRACT, Astrobley and the source-reader product never started. PRODUCT UNVERIFIED;
DELEGATION INDETERMINATE; acceptance gate unmet. No run-02 is authorized here.

## 2. Actors and resource disposition

| Resource | Final supported disposition |
|---|---|
| Old main/native caretaker `/root/caretaker` | Root termination operator-reported; old native handle inaccessible here and retired from reuse |
| R1 thread `01a176f7-532b-7722-9324-0ecb92694073` | Archived-only; current selected read reports notLoaded |
| R1 turn `01a176f7-53a6-7b83-b203-b86b08ec15ac` | Interrupted, no completed final answer |
| Researcher vault | Closed after byte-exact ignored snapshot; vault and shim lock absent |
| Auditor vault / product | Never created |
| Known R1/checker/app-server PIDs | Exact host-namespace checks return ENOENT for 1319728, 1923120, 1923121; no signals needed |
| Old G09 presence `0eb2477c980739d8179ff6a38daa9bbe` | Removed by exact ID; other attachments unchanged |
| Replacement `/root/g09_sanitation` | Bounded verification completed; own app-server closed; no further assignment |

This is scoped resource disposition, not proof of whole-host quiescence or independent
destruction of an inaccessible native context.

## 3. Sequence and confirmed findings

The requested profile was gpt-6.1-sol/high/read-only on CLI 0.164.0. Preflight succeeded;
the initial ask failed locally after 120.811s. Its 4.124s diagnostic is the remaining queue
wait inside a phase deadline, not whole-operation elapsed time. Exact original RPC phase and
inherited timeout environment were not recorded. Majkee later supplied prior use of 1800s.

The first-turn ID existed in memory but was saved only after successful turn/reconciliation.
G03 recovered the exact prompt-bound interrupted turn without a model turn: 12 commands,
four web searches, three commentary messages, no final answer. The checkpoint patch remains
unapplied. Sandbox/PID visibility and adapter guard defects are documented in the G03 diagnosis.

Original cleanup archived R1 and closed the vault, then failed its final process check on
`/proc/1/ns/pid` permission. Cycle06 never delivered RETURN/VERDICT or the report. Replacement
cycle07 verified current archived/closed state and the exact known PIDs without that gate or
a broad process scan. Its first sandboxed metadata probe failed on host-local SQLite setup;
the preserved, normally escalated read-only check succeeded. No retirement was repeated.

## 4. Program consumption and main context

Controller/functions and prompts were pinned; that does not independently prove model loading,
read order or retained context. Warm follow-up/preamble behavior was not exercised.

The main's event record reports the three-file 707-word starter packet PLUS nine additional
task-document reads, ordinary shared-law/harness reads, a truncated batch and rereads, and
selected operational-evidence intake. It records zero routine main tunnel CLI operations.
The capsule body was measured as 71 words/559 file bytes; other recorded counts disagree.
Native/target token totals, actual context occupancy and monetary cost are unavailable.
The starter-packet size alone establishes no clean-head benefit or germline necessity.

## 5. Preservation and remaining work

All 61 protected original files and nine foreign-file hashes match the pre-retirement manifest.
The only removed original is the allowed vault, preserved exactly with ignored snapshots.
RUNBOOK and the pre-close STATUS/release snapshots remain intact; current dispatch release is
false. No original adapter/shim, source input or product code was repaired. No permanent
thread/lock deletion, unrelated kill, deploy, commit, prune or restart occurred.

Before a new run: authorize/verify the transport checkpoint and adapter guards; record timeout
policy explicitly; preserve run-01 accounting; count actual main intake; prepare a fresh run
contract/controller in the same G09 bed. Old native termination remains operator-reported.

## 6. Evidence pointers

Paths are relative to `/home/hruzam/ia-sync/.dev/session/germline-09-source-reader/`:

- `raw/closeout/PRESERVATION.run-01.json`, authority files and `snapshots/`.
- `raw/closeout/resources/{03.archive-R1,05.snapshot-vault,06.close-vault}.json`.
- `raw/closeout/sanitation/{07.selected-verification,08.r1-metadata-elevated,09.processes-elevated}.json`.
- `_bus/07.caretaker.return.md`, `_bus/07.cartan.verdict.md`, `raw/closeout/SANITATION.final.json`.
- `raw/control/main-events.json`, `raw/result/main-context.json`, original R1 receipt/packet.

Vault SHA256 `5789ba86…69e6e9`; R1 receipt `c1f19531…e8938c1`; adapter `5795c074…4d47d572`.
Full hashes are in preservation/sanitation receipts. Detailed transport evidence remains under
`/home/hruzam/ia-sync/_staging/codex/g09-R1-diagnostic.2026-10-26/`.
