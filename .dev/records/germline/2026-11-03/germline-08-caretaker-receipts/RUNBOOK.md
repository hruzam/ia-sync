# RUNBOOK: germline-08-caretaker-receipts

```yaml
goal: >-
  Exercise receipt-first completion checking and a deliberately bounded low-effort
  Codex profile using two fresh read-only tunnel tasks.
gate: >-
  Majkee accepts a verified disposition of receipt-first recovery and two fresh low-effort
  tasks, including result quality, effective runtime, target usage and comparison limits,
  without promotion or transport-source changes.
participant_1: [Cartan, {brand: codex, model: resident, effort: current}, {host: office, role: navigator, STATUS owner and verifier}]
participant_2: [caretaker, {brand: codex, model: gpt-5.6-terra, effort: high}, {host: office, role: same bounded native implementer child}]
participant_3: [Majkee, {brand: human, model: none, effort: none}, {host: office, role: authorization and acceptance}]
status_owner: Cartan
observations_read: none exist for germline
```

Majkee selected Cartan's receipt-first / bounded-profile recommendation with “taking your
lean” on 2026-10-26. G07's experiment_1 records and fixed gate remain unchanged; this sibling
contains the newly authorized follow-up. It is experiment_2, not a replay of an old operation.

## Bounds

- Keep the existing source shim unchanged. No global agent, skill, config, deployment or daemon.
- Re-address `/root/experiment_1_caretaker` if available; no permanence claim across root restart.
- First implement and verify a deploy-inert runner with local fake commands only. Persist an
  exclusive operation record before invocation; inspect the durable record after an empty
  tool return. Existing pending/completed/unknown records must refuse re-execution.
- Distinguish completed-and-validated, still-running and unknown outcomes. A dead runner,
  corrupt receipt, nonzero exit, or missing vault is not permission to resend a model task.
- Then at most TWO target-model turns: one on each of two fresh explicit vaults, read-only,
  requested `gpt-6.1-sol` / `low`, using the existing account. Pin the Codex binary and capture
  its version. Verify effort after zero-turn resume; open-time intent alone is insufficient.
- Named tasks repeat G07's guide/source questions with corrected, narrow read instructions.
  No live transport fault injection. Any comparison with G07 is descriptive, not causal.
- Model turns cannot be transparently retried or substituted. If low is unavailable, record
  the failure and stop that branch. No Claude process/SDK, new key, auth or provider change.
- Persist selected protocol reply fields only; no histories, tool transcripts, auth or caches.
- No old vault reuse, lock deletion, tmux killing, thread deletion, commit, push or deployment.
- G03 review, source freeze and candidate assessment remain separate. Read no Nablarva inputs.

## Method and proof

This is a durable operation journal and conservative reconciliation, not an exactly-once
remote transport. Exclusive local records prevent accidental local resubmission; they cannot
prove whether a remotely accepted task survived a crash before its thread ID was persisted.
Atomic receipt replacement and output hashes are established mechanisms. The local open
question is whether the caretaker actually consults them when tool output is absent.

Deterministic checks cover a lost tool return after completion, a live pending runner, a dead
pending runner, altered output and duplicate invocation. Fresh tasks check source citations,
recipient markers, effective runtime and independently read-back result identity. Target
usage is measured; main/caretaker usage and subscription cost remain unavailable unless an
actual telemetry source appears. No fabricated total-cost or context-savings conclusion.

Existing capability: the source shim accepts `open --override effort=low`; official protocol
documentation describes per-turn effort and persistence on later turns:
[Codex App Server](https://learn.chatgpt.com/docs/app-server). Account availability is tested,
not inferred from that example.

## prompt-0 — Cartan

Read this RUNBOOK and STATUS. Delegate only the current numbered POINT, verify its cited
artifacts, and own the VERDICT and STATUS. Complete local receipt checks before releasing
the two live turns. Freeze task prompts before dispatch; reconcile actual receipts before
classifying any empty tool result. Preserve G07 and every handed-off bus record.
