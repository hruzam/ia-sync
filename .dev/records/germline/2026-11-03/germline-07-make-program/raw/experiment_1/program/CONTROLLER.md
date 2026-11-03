---
program: tunnel-caretaker-trial
stamp: e1c023a1
scope: experiment_1 only; uncanonical; no deployment
---

# Controller

Job: keep routine tunnel operation out of the main's context while returning a checkable result.
This specimen is consumed by an existing native child; it creates no global agent or service.

Invariants: only the trial's two named Codex peers; explicit recipient and state path on every
operation; read-only target work; no Claude process/API-key/auth change; no uncertain retries;
no source mutation, tmux killing, or Codex lock deletion. The caller supplies authority; this
programme grants none. A matching stamp identifies a file; it does not prove correct execution.

| function id | occasion | file | expected stamp | result |
|---|---|---|---|---|
| audit-tunnel-opening | Two bounded source checks plus controlled comparison/resumption | fn/audit-tunnel-opening.md | e1f023a1 | Evidence-backed trial result or explicit failure/unknown |

Before running the procedure, check its observed stamp against this table. Missing input,
unknown function, mismatch, or unavailable authority means hold with expected/observed evidence.
