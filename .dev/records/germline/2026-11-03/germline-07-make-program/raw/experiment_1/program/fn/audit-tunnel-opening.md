---
program: tunnel-caretaker-trial
function: audit-tunnel-opening
stamp: e1f023a1
---

# Inputs and output ownership

Caller: Cartan, controlling experiment_1. Contract and authority are in the G07 RUNBOOK and
the applicable numbered POINT. Use the existing source shim
`/home/hruzam/ia-sync/zsh/ai/tunnel-codex.zsh`; do not change it or use a different transport.
The caretaker's only artifact home is
`/home/hruzam/ia-sync/.dev/session/germline-07-make-program/raw/experiment_1/caretaker/`.
Its exact RETURN path is given by POINT. Targets return text and write no project files.

# Procedure

1. Read controller invariants, check this function's expected/observed stamp, and read the
   task/turn bounds. Record the programme paths and tokens in the caretaker receipt.
2. Create distinct explicit vault paths `tunnel.peer-a.state.json` and `tunnel.peer-b.state.json`
   in the caretaker home. Use `open --enable --sandbox read-only --cwd` with the G07 bed as
   workspace and `--preamble none`; do not load any G03 or Nablarva preamble. Resolve and record
   the account's existing default Codex model; no new credentials/provider. Capture preflight
   stderr/exit/time; it is not a model-ready acknowledgement.
3. Issue at most one initial `ask` to each peer using the exact tasks in POINT. Use literal
   argv, not shell interpolation. Set `TUNNEL_CODEX_USAGE=full` and record the original
   output, stderr, exit, elapsed time, exact prompt, and result hash for each invocation.
   Do not discard an outcome to rerun until green.
4. Check each successful reply's exact recipient/run marker, source citations, and source scope.
   Inspect saved threadId/lastTurnId and observed runtime; require distinct thread IDs and a
   read-only effective sandbox. Missing runtime evidence is unverified, not silently accepted.
   The existing ask read-back check must succeed; a state file alone proves no model result.
5. Return a compact comparison of the GUIDE claim and code behavior, plus receipt/result paths,
   identities, available usage/timings, uncertainty, and any decision needed. Do not invent a
   guide defect if the texts agree. Suggest wording only as a draft; never edit the GUIDE.
6. After Cartan's direct comparison, the SAME native caretaker may be re-addressed under a
   later POINT to use `resume`/`read` only. Verify unchanged peer IDs and the newer matching
   comparison-turn results. This tests reuse without spending another target-model turn.

# Stop and recovery

On timeout, reconciliation mismatch, absent identity, approval rejection, or unexpected source
change, retain the command/output and hold the affected peer. Do not automatically send again.
A first-turn failure can leave threadId null because the current shim saves it only after
completion/reconciliation; this is an unknown outcome, not proof that no remote work started.
No live fault injection or transport fix is authorized by this specimen.

Native Codex runtime state may be written by Codex itself. If host sandboxing prevents that,
request the normal narrow tool escalation for the same declared operation; do not bypass
permissions, create new credentials, or substitute another provider. Never retry an ask whose
submission may already have happened.
