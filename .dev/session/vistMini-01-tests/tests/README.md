# Cycle 02 screen-inferred adapter and isolated fixtures

Run with Bash; no install/deploy is needed. Required arguments are `--check|--send`, `--server`, `--pane %N`, `--pointer LINE`, and `--state-dir ABS`. Pointer example: `[bus example.01] from home:cartan -> read /tmp/request.md ; ack: none`.

The cycle-03 registered live bindings are `default:%3` → Claude and `default:%2` → Codex, after direct-agent relaunch. The old `%0`/`%1` and all other live endpoints refuse locally. `vist-test` supports the legacy cycle-01 stand-in and the registered runtime mirrors. There is no caller flag that bypasses a live endpoint's classifier; no live endpoint falls back to the legacy layout.

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

Output preserves C01–C18 and T01–T16 identifiers. C17/T14 include the old bindings as local refusals following `reports/cartan.binding-03.2026-11-12.md`. Keep earlier failed/aborted logs alongside a later pass. Reports, RETURNS and VERDICTS are owned by the controller/head, not these fixtures.

For cycle03, notification paths beginning `reports/` or `_bus/` resolve under the fixed session bed `/home/hruzam/ia-sync/.dev/session/vistMini-01-tests/`, never the caller's cwd. `scripts/handoff-once.sh TARGET POINTER ABS_STATE_DIR` is a one-shot controller command: after one8-second delay, it checks both registered endpoints once, then performs one adapter send only if both were ready. End the launching controller turn promptly so its own receiver can become idle. Any refusal stops; there is no loop, retry, watcher or manual fallback. Capture stdout/stderr outside the checkout and promote outcomes in the next Git window. The helper never commits or pushes.

Recovery registration `reports/cartan.handoff-recovery-03.2026-11-12.md` adds R01/R02: before reserving/input, at most three snapshots may be read only when metadata changed during capture. A coherent unknown layout still refuses immediately. This is bounded observation within a single adapter call, never retry after a returned refusal. A clean29 makes the one-shot print local-private diagnostic metadata/ANSI cells while preserving the refusal code. Capture its output with `umask 077` under `/tmp`; redact relevant excerpts before promotion, since frames may contain operator text. The earlier live29 cause remains unverified until such a frame identifies it.

`reports/cartan.shell-footer-03.2026-11-12.md` registers the exact observed one-shell/one-agent Claude task footer. F01/F02 accept empty/dim-suggestion input with that footer; F03 still rejects typed/busy states; F04 rejects an unobserved two-shell variant. Both endpoint checks remain in the one-shot. The diagnostic proves the reverse02 cause, not the uncaptured reverse01 cause.
