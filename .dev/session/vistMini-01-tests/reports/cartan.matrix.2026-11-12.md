# Cycle 01 — pre-registered adapter test matrix

Author: home:cartan · 2026-11-12 · baseline: ia-sync `d7ad037`.
Scope: `_bus/01.trajectory.point.md`. This document must be committed before the first adapter/fixture test. The parent will record its commit in the report. No tests or tmux fixtures have been run in this cycle at registration time; version/read-only endpoint inspections from earlier exchanges are not transport tests.

## Hypothesis and safety boundary

A small Bash adapter can check a specifically contracted, dedicated agent pane and attempt a literal pointer notification, while refusing known unsafe states. File persistence, byte injection, turn submission, consumption and independently correct work are different observations. Cycle 01 uses stand-ins; it does not demonstrate real Claude/Codex parsing or receipt.

Only explicit server `vist-test` is permitted for adapter and fixtures in this cycle. The adapter requires an explicit pane ID, pointer, and attempt-state location for send. `--check` must be read-only and must not claim an attempt. Trusted stand-ins may identify as claude/codex for this isolated trial, but must not create a way to bypass identity checks in normal sends. Foreground name alone is insufficient: the actual pane process must own the receiver lifetime so an enclosing shell cannot receive Enter after its child exits. If that invariant cannot be established, refuse.

The pointer is one literal ASCII line, at most 200 characters, with a bounded bus ID/path format; newline/control/shell-expansion payloads must refuse. No eval, shell interpolation of pointer content, generic commands or pane text submission as shell code. A dedicated agent can still misinterpret input: this adapter is not an authenticated agent protocol and does not prove semantic safety.

The composer must have an exact recognized ready marker and be empty; occupied, unknown and busy states refuse before modification. The stand-in protocol/marker must be documented by implementation, with no claim the real TUIs already implement it. The attempt key includes message ID and recipient endpoint; repeating the message must not silently send twice. Claiming an attempt is distinct from stamping consumption. Uncertain attempts survive a crash; no blind resend.

## Registered cases (all must run on isolated fixtures)

| ID | Case/setup | Expected result and evidence |
|---|---|---|
| C01 | ready direct-exec agent, valid pointer, `--check` | exit 0; composer/fixture receipt and filesystem attempt state unchanged |
| C02 | ready direct-exec agent, valid pointer, send | exit 0; literal text and separate Enter observed by fixture; exactly one submitted line equals pointer; result labelled notification attempt, not consumption |
| C03 | missing required argument or malformed pane ID | usage refusal; no tmux injection/attempt claim |
| C04 | explicit unknown pane on existing isolated server | distinct unknown-pane refusal; no input/attempt claim |
| C05 | direct receiver has exited; retained dead pane | distinct dead-pane refusal; no pointer executed |
| C06 | live shell/non-agent pane | distinct non-agent refusal; shell sentinel remains absent |
| C07 | recognized agent with occupied composer | distinct occupied-composer refusal; captured draft byte-for-byte unchanged |
| C08 | recognized agent with busy marker | busy refusal; receiver unchanged |
| C09 | same `(msg, endpoint)` sent twice | second attempt refuses duplicate; fixture has exactly one line |
| C10 | receiver exits after pointer text but before Enter | deterministic synchronization; adapter refuses changed/dead receiver or fails safely; no pointer reaches a shell; isolated pane capture/exit state preserved in test output |
| C11 | foreground agent inside enclosing interactive shell | refuse unsafe lifetime or non-agent top-level process; shell fallback sentinel absent |
| C12 | malformed/overlength/non-ASCII/multiline/control/expansion pointer variants | each refuses validation; receiver unchanged; no execution/attempt claim |
| C13 | state directory cannot be created / is a file | nonzero before injecting; no submitted line |
| C14 | crash/kill after attempt reservation, before definite completion | retained attempt prevents repeat; report uncertain delivery, never false receipt; fixture shows zero or one submissions, never two |
| C15 | unrecognized composer/prompt state | refuse unknown input state, no modification |
| C16 | two competing sends of same key | at most one reservation/send; loser refuses; fixture has at most one submitted line |
| C17 | forbidden server such as default/live peer server | refuse locally before any connection or input; no calls to live server |
| C18 | ready stand-in representing each of claude and codex | same adapter contract for both; literal submitted pointer preserved; report stand-ins explicitly |

Expectations above are semantic; the implementation documents numeric exit codes before interpreting results. Refusal categories unknown/dead/non-agent/occupied must have distinct numeric codes as required by POINT. A detected unsafe state is a passing refusal case, not successful delivery. Missing/unrunnable evidence is UNVERIFIED, not PASS. Added coverage after registration must be identified as exploratory or preregistered in a committed amendment before its first run; never rewrite this matrix to match outcomes.

## Deferred semantic cases and live trial boundary

Expired envelope, wrong envelope recipient, unauthorized file path, hop/retry budget, per-recipient stamps, and restart deduplication across a real session must be tested at the envelope/receiver layer. A pointer-only byte adapter cannot infer an envelope's expiry or authority. This cycle may reject malformed pointer paths, but must not count that as a demonstrated semantic recipient/expiry check. The proposal's three ordinary messages each direction, real TUI busy/composer behavior and VIST relevance also remain outside this cycle. The RETURN must name those limits so the head can schedule them; none is implied passed by the isolated adapter.

## Procedure and records

1. Commit this file alone; record its commit before running helper/fixture tests.
2. Author one session-local adapter and isolated test harness with Bash + coreutils + tmux only. Syntax checks follow registration too. Do not modify live configuration, viewer tools, other seats' files, RUNBOOK, STATUS or pulse.
3. Execute all C01–C18, printing case ID, PASS/FAIL and expected/observed result. Capture every validation variant and relevant exit code; bounded polling/fixture handshakes should make race cases deterministic.
4. Use an isolated workspace and exact created pane/session identifiers; never kill unrelated sessions or a server found pre-existing. Avoid timing claims based on arbitrary sleeps. Record versions, commands, UTC, source commits and any deviation.
5. Cartan records results in `reports/cartan.cycle01.2026-11-12.md`, with reproduction command, counterexamples, permission boundary and uncertainty. The six-field RETURN points to those artifacts. Trajectory independently verifies the RETURN and controls STATUS/VERDICT.

No tests of this transport executed at registration. Current known versions from non-test inventory: GNU Bash 5.3.15(1)-release, tmux 3.7c. Runtime sandbox access may require explicit authorized escalation; a denial is evidence, not proof of an absent server or peer. This is a small engineering trial, not statistical validation or a claim of vendor superiority.
