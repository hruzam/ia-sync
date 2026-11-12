# Cycle 01 — isolated notification adapter trial

2026-11-12 · investigator: home:cartan · implementation child: Astrobley · fresh read-only review: verifier.

## Result and boundary

The final isolated C01–C18 suite passed, exit 0, on GNU Bash 5.3.15(1)-release and tmux 3.7c, on Linux home (`hruzam`). Cartan ran the final tree independently at 08:33:33–08:33:35 UTC. The adapter is restricted to server `vist-test` and a trusted one-line stand-in prompt contract; no live-peer test was run. This is partial evidence toward the RUNBOOK gate, not a closed gate or real Claude/Codex delivery proof. Trajectory's independent VERDICT remains owed.

## Registration, source and method

- Session baseline: `d7ad037` (RUNBOOK/STATUS/POINT opening).
- Pre-registration: `b983476be52dd75a7e22feedf53962f03cfe400c` at 08:24:17 UTC; matrix unchanged since registration.
- First fixture run began at 08:28:51 UTC. No adapter/fixture tests ran before registration in this cycle. Read-only inventory/version checks preceded it.
- Final tested code committed as `949ea36`; no production code change occurred between Cartan's successful run and that commit. Source fingerprints below identify the exact tree.
- One bounded Astrobley child authored only scripts/tests, with no Git or transport authority. Cartan inspected source, retained failed outputs, raised whitespace-only composer and fixture-readiness counterexamples, and reran the final files. A separate verifier read the RUNBOOK, POINT, matrix, code, fixtures and README; inspected commit order and syntax; reported PASS with no material findings for the fixture-only scope. It did not execute the full harness and does not replace Trajectory's VERDICT.

The pre-registered matrix is `reports/cartan.matrix.2026-11-12.md`. Semantic case expectations were not relaxed after seeing output. Additional assertions check separate text/Enter calls, zero tmux calls for a forbidden server and a unique scratch sentinel for an expansion payload; these strengthen the same registered cases, not new claimed experiments.

## Reproduction commands and outcomes

Run from any cwd, with no existing sessions on isolated server `vist-test`:

```sh
bash -n /home/hruzam/ia-sync/.dev/session/vistMini-01-tests/scripts/bus-poke.sh /home/hruzam/ia-sync/.dev/session/vistMini-01-tests/tests/adapter-test.sh /home/hruzam/ia-sync/.dev/session/vistMini-01-tests/tests/fake-agent.sh /home/hruzam/ia-sync/.dev/session/vistMini-01-tests/tests/tmux-interpose.sh
bash /home/hruzam/ia-sync/.dev/session/vistMini-01-tests/tests/adapter-test.sh
```

Both final checks returned 0. Cartan captured the second command with `> /tmp/vist-cycle01.parent.log 2>&1`; its complete output is below. The expected killed-child line is C14's deliberately interrupted adapter, not a harness crash. The test harness refuses an existing `vist-test` session, creates one uniquely named session, and cleans up only that exact session. It leaves scratch artifacts at the printed `/tmp` path; those paths are host-local diagnostics, not a cross-host evidence store. The decisive output is preserved in this tracked report.

`git -C /home/hruzam/ia-sync diff --exit-code d7ad037 -- .dev/session/vistMini-01-tests/RUNBOOK.md .dev/session/vistMini-01-tests/STATUS.md .dev/session/vistMini-01-tests/_bus/01.trajectory.point.md .dev/session/vistMini-01-tests/reports/trajectory.permissions.2026-11-12.md pulse.md` returned 0. Cartan did not edit the head's files. Syntax and staged whitespace checks passed. Only matrix, implementation, own report and own RETURN are committed by Cartan in this window.

## Interpretation

- C01: check mode made no attempt-state/log and left the composer unchanged.
- C02/C18: both trusted runtime stand-ins received the literal pointer. The wrapper observed one text call and a separate Enter call. Exit 0 is labelled `receipt=unproven`.
- C03–C08/C15/C17: malformed input, unavailable/dead/non-agent/occupied/busy/unknown states and a forbidden server refused. Whitespace-only drafts were checked with cursor state as well as pane text.
- C09/C16: duplicate/concurrent callers submitted one line at most using atomic reservation in the supplied state directory.
- C10/C11: an exited direct receiver was detected before Enter, and an enclosing interactive shell with a foreground agent was refused by the top-level identity check. No submitted line or shell fallback was observed in those controlled fixtures.
- C12/C13: invalid literal payloads and unusable state refused; the deliberately malicious-looking literal never executed its unique scratch sentinel.
- C14: SIGKILL after reservation produced 137; a new invocation refused 25, preserving uncertainty without a false receipt or blind resend. This test interrupts before text injection; it does not prove every possible crash timing.

Numeric codes are documented in `tests/README.md`: 2 usage/server; 20 unknown/read failure; 21 dead; 22 non-agent; 23 occupied; 24 busy; 25 duplicate/uncertain; 26 unsafe lifetime; 27 changed after text; 28 I/O/interruption; 29 unknown composer; 30 invalid pointer.

## Preserved mismatches and development outcomes

| Run | Observed result | Disposition |
|---|---|---|
| First, 08:28:51–56 UTC | exit 1, two fixture FAILs: C06 screenshot changed while shell initialized; C11 noninteractive process group exposed bash/code22 rather than the intended foreground codex/root bash/code26 | preserve log; synchronize a recognizable shell prompt and create a genuinely interactive enclosing-shell fixture; production identity checks not weakened |
| Second, 08:29:53 UTC | exit 2 at shell readiness; predicate expected a trailing space that tmux trims | preserve log; readiness predicate tests the stable marker; no protocol expectation changed |
| Third, 08:30:35–37 UTC | C01–C18 PASS, exit 0 | final assertion/hygiene changes then tested by Cartan's separate final run |
| Cartan final, 08:33:33–35 UTC | C01–C18 PASS, exit 0 | full output below; head verification pending |

Source review also found that stripping trailing spaces could mistake a whitespace-only draft for empty. The adapter now checks cursor position under its explicit stand-in contract; C07 includes both text and whitespace-only drafts and compares text plus cursor before/after. Real TUI layouts do not yet inherit that contract.

## Permissions, uncertainty and next boundary

The ordinary sandbox denied the tmux socket and ia-sync writes in earlier exchanges. Explicit authorized escalation permits this cycle's source writes, Git operations and isolated fixture execution; no configuration/allowlist change was made. Trajectory's own report states no further permission opening is needed for this trial so far; its SSH-authorization denial is outside this scope. Those are different enforcement mechanisms, not assumed parity.

All execution fixtures are Bash/coreutils/tmux, including Linux `/proc` inspection. The adapter does not authenticate process names: the trusted fixtures intentionally use `exec -a`. Matching a top-level PID/start time prevents the tested enclosing-shell fallback but does not eliminate the final observation-to-Enter race, malicious receiver behavior, external pane respawn/reconfiguration, or concurrent operator input. If text is injected and the later check fails, the adapter leaves a reservation and may leave partial input; it does not silently erase/retry it. Check mode proves only its contracted snapshot, not future writability or delivery.

Deduplication holds within the same supplied attempt-state directory and endpoint key; removing/changing that local state is not covered. The state directory is a local transport attempt record, not a consumption stamp, extra STATUS or BUS unread registry. Filesystem/identity environment is trusted; there is no hostile-local-process security claim.

Deferred as registered: real TUI ready/busy/occupied behavior; three ordinary live messages each direction; envelope expiry/recipient/path authority; hop/retry budgets and per-recipient consumption; other crash timings; cross-host or cross-platform runs; VIST context and applicability. A pointer-only adapter cannot infer those semantics. No deploy, canon, runtime setting, viewer modification, RUNBOOK/STATUS/pulse edit or live-peer experiment occurred. A final ready poke is a separately authorized control-plane handoff and is not counted as a trial result.

The head should verify these files and the final output, then schedule the next bounded receiver/live-contract investigation if appropriate. Simply removing `vist-test` validation would not make this a live-TUI adapter.

## Source fingerprints

```text
8c594a4e2c2f597d817e468b7aaed8da31f8148d1d353d2ff564e97b3eb69c4e  reports/cartan.matrix.2026-11-12.md
c5492b00cfd434a9bf8a6d4c0dfd48eaa9c1d12e15b03b4f3992e4cba8c71abb  scripts/bus-poke.sh
04d04c2425dbc1f09cf055ad9f4d8962ed7956f64061865f6fde7adf449a7748  tests/adapter-test.sh
765c3a28c7690c277cabf7282a46bc89b7de0003701fb1596ad7103c229aa86e  tests/fake-agent.sh
a5f1e3e8b1b342ef4b8a726f88d992ba13d28c555031142b6b7d7c2eac89414e  tests/tmux-interpose.sh
56d85dbe2a47e668e2ed25eda98769db353f2285d4329f63ff0573a7f51e8212  tests/README.md
```

## Development first run: failed fixtures

```text
UTC=2026-11-12T08:28:51Z bash=5.3.15(1)-release tmux=tmux 3.7c artifacts=/tmp/vist-cycle01.8Bcw7w
C01 PASS rc=0 read-only state/log absent; composer-equal=yes
C02 PASS rc=0 literal receiver line; 2026-11-12T08:28:51Z notification-attempted server=vist-test pane=%1 msg=c02 receipt=unproven
C03 PASS malformed pane rc=2 expected=2
C03 PASS missing args rc=2 expected=2
C04 PASS unknown pane rc=20 expected=20
C05 PASS retained dead pane=1 rc=21 expected=21 log-absent=yes
C06 PASS non-agent shell rc=22 expected=22
C06 FAIL shell content changed
C07 PASS occupied draft unchanged rc=23 expected=23
C07 PASS whitespace draft unchanged rc=23 expected=23
C08 PASS busy unchanged rc=24 expected=24
C09 PASS first=0 duplicate=25 received-lines=1
C10 PASS exit after text before Enter rc=27 expected=27 pane-dead=1 no shell parent/no receipt
C11 FAIL foreground=bash enclosing shell refused rc=22 expected=26 fallback sentinel absent
C12 PASS validation variant=1 rc=30 expected=30 composer unchanged
C12 PASS validation variant=2 rc=30 expected=30 composer unchanged
C12 PASS validation variant=3 rc=30 expected=30 composer unchanged
C12 PASS validation variant=4 rc=30 expected=30 composer unchanged
C12 PASS validation variant=5 rc=30 expected=30 composer unchanged
C12 PASS validation variant=6 rc=30 expected=30 composer unchanged
C12 PASS validation variant=7 rc=30 expected=30 composer unchanged
C13 PASS state path is file rc=28 expected=28 no submission
/home/hruzam/ia-sync/.dev/session/vistMini-01-tests/tests/adapter-test.sh: line 52: 1830151 Killed                     bash "$ADAPTER" "$testmode" --server vist-test --pane "$pane" --pointer "$pointer" --state-dir "$scratch/state" "$@" > "$scratch/last.out" 2>&1
C14 PASS killed-after-reservation=137 restart=25 expected=25 no receipt; uncertain claim retained
C15 PASS unknown composer unchanged rc=29 expected=29
C16 PASS competing exits=0,25 exactly-one-line=1
C17 PASS forbidden default server rc=2 expected=2 (local validation)
C18 PASS codex stand-in rc=0 literal submission
C18 PASS claude stand-in rc=0 literal submission
SUMMARY failures=2 artifacts=/tmp/vist-cycle01.8Bcw7w UTC=2026-11-12T08:28:56Z
```

## Development second run: aborted fixture

```text
UTC=2026-11-12T08:29:53Z bash=5.3.15(1)-release tmux=tmux 3.7c artifacts=/tmp/vist-cycle01.LJgqeU
C01 PASS rc=0 read-only state/log absent; composer-equal=yes
C02 PASS rc=0 literal receiver line; 2026-11-12T08:29:54Z notification-attempted server=vist-test pane=%1 msg=c02 receipt=unproven
C03 PASS malformed pane rc=2 expected=2
C03 PASS missing args rc=2 expected=2
C04 PASS unknown pane rc=20 expected=20
C05 PASS retained dead pane=1 rc=21 expected=21 log-absent=yes
shell fixture failed readiness: c06
```

## Development third run: passing before final assertions

```text
UTC=2026-11-12T08:30:35Z bash=5.3.15(1)-release tmux=tmux 3.7c artifacts=/tmp/vist-cycle01.KCDrz2
C01 PASS rc=0 read-only state/log absent; composer-equal=yes
C02 PASS rc=0 literal receiver line; 2026-11-12T08:30:35Z notification-attempted server=vist-test pane=%1 msg=c02 receipt=unproven
C03 PASS malformed pane rc=2 expected=2
C03 PASS missing args rc=2 expected=2
C04 PASS unknown pane rc=20 expected=20
C05 PASS retained dead pane=1 rc=21 expected=21 log-absent=yes
C06 PASS non-agent shell rc=22 expected=22
C07 PASS occupied draft unchanged rc=23 expected=23
C07 PASS whitespace draft unchanged rc=23 expected=23
C08 PASS busy unchanged rc=24 expected=24
C09 PASS first=0 duplicate=25 received-lines=1
C10 PASS exit after text before Enter rc=27 expected=27 pane-dead=1 no shell parent/no receipt
C11 PASS foreground=codex enclosing shell refused rc=26 expected=26 fallback sentinel absent
C12 PASS validation variant=1 rc=30 expected=30 composer unchanged
C12 PASS validation variant=2 rc=30 expected=30 composer unchanged
C12 PASS validation variant=3 rc=30 expected=30 composer unchanged
C12 PASS validation variant=4 rc=30 expected=30 composer unchanged
C12 PASS validation variant=5 rc=30 expected=30 composer unchanged
C12 PASS validation variant=6 rc=30 expected=30 composer unchanged
C12 PASS validation variant=7 rc=30 expected=30 composer unchanged
C13 PASS state path is file rc=28 expected=28 no submission
/home/hruzam/ia-sync/.dev/session/vistMini-01-tests/tests/adapter-test.sh: line 68: 1831208 Killed                     bash "$ADAPTER" "$testmode" --server vist-test --pane "$pane" --pointer "$pointer" --state-dir "$scratch/state" "$@" > "$scratch/last.out" 2>&1
C14 PASS killed-after-reservation=137 restart=25 expected=25 no receipt; uncertain claim retained
C15 PASS unknown composer unchanged rc=29 expected=29
C16 PASS competing exits=25,0 exactly-one-line=1
C17 PASS forbidden default server rc=2 expected=2 (local validation)
C18 PASS codex stand-in rc=0 literal submission
C18 PASS claude stand-in rc=0 literal submission
SUMMARY failures=0 artifacts=/tmp/vist-cycle01.KCDrz2 UTC=2026-11-12T08:30:37Z
```

## Cartan independent final run

```text
UTC=2026-11-12T08:33:33Z bash=5.3.15(1)-release tmux=tmux 3.7c artifacts=/tmp/vist-cycle01.3GiG2S
C01 PASS rc=0 read-only state/log absent; composer-equal=yes
C02 PASS rc=0 literal receiver line text-calls=1 separate-Enter-calls=1; 2026-11-12T08:33:33Z notification-attempted server=vist-test pane=%1 msg=c02 receipt=unproven
C03 PASS malformed pane rc=2 expected=2
C03 PASS missing args rc=2 expected=2
C04 PASS unknown pane rc=20 expected=20
C05 PASS retained dead pane=1 rc=21 expected=21 log-absent=yes
C06 PASS non-agent shell rc=22 expected=22
C07 PASS occupied draft unchanged rc=23 expected=23
C07 PASS whitespace draft unchanged rc=23 expected=23
C08 PASS busy unchanged rc=24 expected=24
C09 PASS first=0 duplicate=25 received-lines=1
C10 PASS exit after text before Enter rc=27 expected=27 pane-dead=1 no shell parent/no receipt
C11 PASS foreground=codex enclosing shell refused rc=26 expected=26 fallback sentinel absent
C12 PASS validation variant=1 rc=30 expected=30 composer unchanged
C12 PASS validation variant=2 rc=30 expected=30 composer unchanged
C12 PASS validation variant=3 rc=30 expected=30 composer unchanged
C12 PASS validation variant=4 rc=30 expected=30 composer unchanged
C12 PASS validation variant=5 rc=30 expected=30 composer unchanged
C12 PASS validation variant=6 rc=30 expected=30 composer unchanged
C12 PASS validation variant=7 rc=30 expected=30 composer unchanged
C12 PASS literal expansion payload never executed (unique scratch sentinel absent)
C13 PASS state path is file rc=28 expected=28 no submission
/home/hruzam/ia-sync/.dev/session/vistMini-01-tests/tests/adapter-test.sh: line 69: 1832357 Killed                     bash "$ADAPTER" "$testmode" --server vist-test --pane "$pane" --pointer "$pointer" --state-dir "$scratch/state" "$@" > "$scratch/last.out" 2>&1
C14 PASS killed-after-reservation=137 restart=25 expected=25 no receipt; uncertain claim retained
C15 PASS unknown composer unchanged rc=29 expected=29
C16 PASS competing exits=0,25 exactly-one-line=1
C17 PASS forbidden default server rc=2 expected=2 no tmux call (local validation)
C18 PASS codex stand-in rc=0 literal submission
C18 PASS claude stand-in rc=0 literal submission
SUMMARY failures=0 artifacts=/tmp/vist-cycle01.3GiG2S UTC=2026-11-12T08:33:35Z
```
