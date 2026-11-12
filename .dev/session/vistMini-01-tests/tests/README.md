# Cycle 02 screen-inferred adapter and isolated fixtures

Run with Bash; no install/deploy is needed. Required arguments are `--check|--send`, `--server`, `--pane %N`, `--pointer LINE`, and `--state-dir ABS`. Pointer example: `[bus example.01] from home:cartan -> read /tmp/request.md ; ack: none`.

The exact registered live bindings are `default:%0` → Claude and `default:%1` → Codex. All other live endpoints refuse locally. `vist-test` supports the legacy cycle-01 stand-in and the registered runtime mirrors. There is no caller flag that bypasses a live endpoint's classifier; no live endpoint falls back to the legacy layout.

## Contract and limits

`reports/cartan.tui-contract.2026-11-12.md` registers cycle-02 decisions before implementation. The adapter checks Linux top-level PID/start-time/argv0 plus foreground identity, the bottommost runtime composer, its cursor, ANSI dim state, known footer shapes and the registered current busy region. It refuses enclosing-shell lifetimes, non-dim drafts (including detectable whitespace/multiline continuations), unknown layouts, alternate Codex suggestions and pointers that would wrap. Color SGR38/48 payloads do not count as standalone SGR2 dim.

Post-text redraws may require repeated read-only observations within the same reservation. No additional text is injected. Enter is a separate call and requires a coherent view containing the exact non-dim pointer at the expected row/cursor and unchanged process identity. Any failed/uncertain attempt retains its reservation; never erase it and resend without checking the recipient's receipt.

`--check` writes no attempt state or directory and injects nothing. The explicit state location is transport-attempt state, not consumption or STATUS. A successful send reports `receipt=unproven`. The adapter does not authenticate processes, make observations atomic, prove absence of invisible/trimmed input at cursor-start, or cover unseen progress placements. It assumes a trusted, stable, uncontested UI for its scheduled send. Codex own-idle is a predicted contract pending reverse live validation; passing stand-ins do not upgrade it to observed live behavior.

Envelope expiry, recipient authority, path authorization, hop/retry policy and semantic consumption remain receiver-layer work. The parent alone performs one scheduled ordinary live send after publishing RETURN; Trajectory performs the reverse after its VERDICT. Disruptive cases are isolated; child fixture tests never inspect or send to live peers.

## Exit codes

| Code | Meaning |
|---|---|
| 0 | ready snapshot, or notification attempted; receipt remains unproven |
| 2 | usage, missing argument, malformed pane ID, unregistered endpoint |
| 20 / 21 / 22 | unknown/unavailable pane / dead pane / wrong foreground agent |
| 23 / 24 / 25 | occupied or continuation / busy / duplicate or uncertain reservation |
| 26 / 27 / 28 | unsafe top-level lifetime / changed or uncertain post-text state / I/O or interruption |
| 29 / 30 | unknown or incoherent layout / invalid or wrapping pointer |

## Reproduction

Run `bash /home/hruzam/ia-sync/.dev/session/vistMini-01-tests/tests/adapter-test.sh`.

The harness refuses a preexisting `vist-test` session, creates a unique session, cleans up only that session, and leaves evidence under the printed `/tmp/vist-cycle01.*` path. It never resets a server or touches live panes. Trusted Bash stand-ins use `exec -a` and synthetic text; they are renderer fixtures, not real TUIs. External tmux interposition records separate text/Enter calls and synchronizes exit, crash and busy-after-text cases. The production adapter contains no fixture hook.

Output preserves C01–C18 and T01–T16 identifiers. C17's forbidden-endpoint samples were amended in the registered cycle-02 contract because `default:%0` became allowed. Keep earlier failed/aborted logs alongside a later pass. Reports, RETURNS and VERDICTS are owned by the controller/head, not these fixtures.
