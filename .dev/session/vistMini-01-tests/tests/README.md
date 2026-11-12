# Cycle 01 fixture adapter

Run from any directory with Bash; no install/deploy is needed:

```sh
bash /home/hruzam/ia-sync/.dev/session/vistMini-01-tests/scripts/bus-poke.sh \
  --check --server vist-test --pane %N \
  --pointer '[bus example.01] from home:cartan -> read /tmp/request.md ; ack: none' \
  --state-dir /tmp/explicit-attempt-state
```

`--send` replaces `--check`. Only `vist-test` is accepted in this cycle. `--check` writes no attempt state, creates no directory, and injects no input. Both modes refuse a previously reserved message+server+pane key. The caller supplies an explicit temporary/machine-local state path; it is transport attempt state, never a consumption stamp or session STATUS. Do not erase a reservation to retry an uncertain send without checking the receiver's receipt.

## Receiver contract and limits

This prototype requires Linux `/proc` and an explicitly trusted dedicated top-level agent process whose argv0 and tmux foreground command both identify as `codex` or `claude`. It records top-level PID plus process start time and rechecks them before Enter. An enclosing shell with a foreground child refuses. This is not authentication against malicious processes that spoof names or change their own input semantics.

The contracted stand-in draws a single prompt `❯ ` at screen origin, cursor `(2,0)`, and needs enough width for the one-line pointer. Any draft, including only spaces, refuses. `esc to interrupt` refuses as busy. The adapter accepts only a bounded ASCII pointer grammar (maximum 200 bytes); after literal injection, it requires the exact pointer and corresponding cursor position before issuing a separate Enter call. It does not promise an atomic handoff across those observations. A change/timeout after text injection leaves an uncertain reservation; it does not clear partial input or resend.

The real Claude/Codex TUIs have not been shown to implement this receiver contract. The cycle intentionally does not send to their live panes. Do not use this helper for a live peer merely by changing the server check. Envelope expiry, recipient authority, request path authorization, hop/retry budgets and consumption belong to a separate receiver/protocol layer.

## Exit codes

| Code | Meaning |
|---|---|
| 0 | read-only ready snapshot, or text/Enter notification attempted; receipt remains unproven |
| 2 | usage, missing argument, malformed pane ID, or forbidden server |
| 20 | unknown/unavailable pane or tmux read failure |
| 21 | dead pane |
| 22 | non-agent foreground command |
| 23 | occupied composer, including whitespace/cursor mismatch |
| 24 | busy marker |
| 25 | duplicate or uncertain prior/concurrent attempt |
| 26 | unsafe top-level process lifetime/identity |
| 27 | receiver/composer changed after text attempt; no Enter |
| 28 | state or injection I/O failure/interruption; inspect any reservation |
| 29 | unrecognized composer |
| 30 | invalid pointer grammar/encoding/length |

## Isolated tests

```sh
bash /home/hruzam/ia-sync/.dev/session/vistMini-01-tests/tests/adapter-test.sh
```

The harness refuses if `vist-test` already has sessions. It creates one uniquely named session, cleans up only that exact session, and preserves logs/state under the printed `/tmp/vist-cycle01.*` directory. It never resets/kills the server or inspects live peer panes. A trusted Bash stand-in uses `exec -a` to represent each agent; its prompt contract is deliberately explicit, not an emulation claim. External test-only tmux interposition synchronizes C10 (stand-in exits after text) and C14 (adapter killed after reservation before send). The adapter contains no test hook or bypass. The wrapper records calls so C02 can attest separate text/Enter invocations and C17 can attest zero tmux calls.

`reports/cartan.matrix.2026-11-12.md` is the pre-registration. Output labels C01–C18 and individual C12 variants; failures and aborted fixture runs must be retained alongside a later passing run. The final report and independent VERDICT belong to Cartan and Trajectory respectively, outside these implementation-owned files.
