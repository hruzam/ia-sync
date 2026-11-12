# Cycle 02 — renderer fixtures pass; live lifetime precondition fails

2026-11-12 · author: home:cartan · baseline `df9339f` · registration `d755c20` · implementation `b94b5f1`.

## Outcome

The final isolated C01–C18 and T01–T16 run passes, exit 0. The scheduled live-send requirement is **BLOCKED**: both registered live endpoints return 26 in read-only adapter checks because the pane's top-level process is a login zsh, not the foreground agent. This is the retained C11 shell-fallback rejection. At publication of this report, no live text or Enter has been injected in this cycle, no send-mode live invocation has occurred, and the explicit live attempt-state directory does not exist. No successful live send, consumption, or gate closure is claimed.

A fresh verifier initially found the registered implementation statically conformant. After checking the actual live refusal/identity evidence, it judged the full POINT02 criterion unsatisfied and recommended BLOCKED while preserving the guard. Those two findings have different scope; fixture/static conformance does not override the live precondition.

## Method and registration

`reports/cartan.tui-contract.2026-11-12.md` was committed as `d755c20` before adapter changes. It separates observed Claude typed and dim-suggestion states, observed Codex busy-placeholder state, footer/cursor evidence and predicted/unobserved idle states. Its C17 amendment changes only examples of forbidden endpoints, because two exact default panes became registered. The registration remains unchanged.

One Astrobley child changed scripts/tests only, made no live calls and did not commit. Cartan reviewed source, raised unsupported continuation and redraw-coherence issues, inspected failed output, independently reran the final suite, then performed two read-only live checks. A separate verifier inspected source/fixtures/history, ran syntax checks, and examined the live evidence after the refusal. Only Cartan made Git mutations in the assigned window. Head-owned RUNBOOK/STATUS/pulse and trajectory files remain unchanged by Cartan.

## Actual commands and results

```sh
bash -n /home/hruzam/ia-sync/.dev/session/vistMini-01-tests/scripts/bus-poke.sh /home/hruzam/ia-sync/.dev/session/vistMini-01-tests/tests/adapter-test.sh /home/hruzam/ia-sync/.dev/session/vistMini-01-tests/tests/fake-agent.sh /home/hruzam/ia-sync/.dev/session/vistMini-01-tests/tests/tmux-interpose.sh
bash /home/hruzam/ia-sync/.dev/session/vistMini-01-tests/tests/adapter-test.sh
```

Final syntax and independent suite exit 0. Parent suite UTC08:57:08–08:57:13, Bash5.3.15(1)-release, tmux3.7c. Complete output follows. All disruptive cases ran only on `vist-test`, using synthetic/redacted fixtures and exact own-session cleanup. Its `/tmp/vist-cycle01.*` prefix remains from cycle01 and does not mean this is old output.

Read-only live checks (the only live adapter invocations):

```sh
bash /home/hruzam/ia-sync/.dev/session/vistMini-01-tests/scripts/bus-poke.sh --check --server default --pane %0 --pointer '[bus 02.c] from home:cartan -> read .dev/session/vistMini-01-tests/_bus/02.cartan.return.md ; ack: none' --state-dir /tmp/vistMini-cycle02-live-attempts
bash /home/hruzam/ia-sync/.dev/session/vistMini-01-tests/scripts/bus-poke.sh --check --server default --pane %1 --pointer '[bus 02.t] from home:trajectory -> read .dev/session/vistMini-01-tests/_bus/02.trajectory.verdict.md ; ack: none' --state-dir /tmp/vistMini-cycle02-live-attempts
```

Both exited 26 before input or reservation. These are internal adapter safety refusals, not sandbox/auto-review denials. Tool escalation already permitted the read-only socket access. A wider Bash allowance would not change the topology or satisfy the lifetime contract.

Diagnostic observation used `tmux -L default display-message -p -t <registered-target> '#{session_name}|#{pane_id}|#{pane_current_command}|#{pane_pid}'`, then read only argv0, comm and the executable link of that top PID under `/proc`. No other process arguments, environment or private session content were copied. Actual data are appended below.

## Meaning of the blocker

Both `%0` and `%1` are shells hosting foreground agents. The adapter requires foreground identity AND top-level agent lifetime. When the foreground agent exits, a surviving shell could receive later input/Enter. All C11 fixtures still pass by refusing that topology. Removing the guard only for the real endpoints would make the passing safety test irrelevant to the scheduled send; that was not done.

No safe path satisfying the current POINT02 was established: it allows the two existing endpoints, read-only observation and one adapter-mediated send only when eligible. It does not authorize disrupting/restarting those agents, replacing endpoint ownership, or weakening the registered lifecycle condition. The unused send allowance is preserved. The head should record BLOCKED and obtain/assign a bounded endpoint-launch or lifetime-contract decision before another live send.

The ordinary completion poke is also pending: the designated adapter refuses the same pane, and POINT02 requires that one live send to be the ready notification. A manual fallback would be a distinct exception, not proof of this test. This report/RETURN is published for review; the head must not infer receipt from file availability.

## Development failures preserved

- First isolated run 08:52:23–28, exit1: four safe post-text27 refusals while renderer redraw changed metadata (C18 Codex, T02 suggestion, T02 reset/dim, T08 Codex placeholder). The adapter now repeats only incoherent read observations within the existing reservation. It never reinjects text. Busy/dead/lifetime changes still fail immediately; Enter still needs a coherent exact non-dim pointer and cursor.
- Source review found unknown continuation rows could be ignored below a dim first line. They now refuse, including cursor-at-start and dim-continuation T05 variants.
- T13's first payload exceeded the global200-byte limit; the final fixture uses173 bytes at width130, isolating wrapping below the global limit. T10 background-color variants were reordered before generic variants so the final suite actually exercises SGR48 as labelled, alongside SGR38 and reset/dim.
- Second worker run 08:54:14–20, exit0; final background-case/docs corrections were then covered by Cartan's independent final run, exit0. No registration expectation was rewritten to match observed output.

## Remaining uncertainty and bounded next action

Real Claude empty/busy states were not controlled or deliberately induced; its real non-dim multiline draft and idle dim suggestion were read-only observations. Codex idle-empty, typed draft and alternative suggestion remain unobserved; own-active placeholder plus Working indicator was observed. The live checks fail before screen classification, so no whole-pipeline live eligibility claim follows from parser fixtures. Footers and busy placement are version/frame-specific; matching process names is not authentication, trimmed hidden whitespace cannot be excluded, and the final observation-to-Enter race remains.

A safe future live trial needs an explicitly authorized launch/transfer arrangement that satisfies the lifetime precondition, or an explicitly reviewed change to that precondition with new counterexamples and registration. Choosing that is the head/operator's decision. Do not restart resident sessions or broaden settings to make this report pass. Any future command must use the newly approved binding; currently even the exact reverse command below is ineligible.

Envelope expiry/recipient/path/hop/per-recipient consumption, 3+3 ordinary messages, VIST relevance and Oraculum's route remain open. No configuration, deploy, canon, viewer change, peer disruption or live injection occurred. This negative live observation is a trial result, not grounds to hide or loosen the guard.

## Requested reverse command (for review; NOT eligible now)

After a new authorized decision and an eligible check, the originally scheduled reverse command would be:

```sh
bash /home/hruzam/ia-sync/.dev/session/vistMini-01-tests/scripts/bus-poke.sh --send --server default --pane %1 --pointer '[bus 02.t] from home:trajectory -> read .dev/session/vistMini-01-tests/_bus/02.trajectory.verdict.md ; ack: none' --state-dir /tmp/vistMini-cycle02-live-attempts
```

Do not run this merely because VERDICT02 was committed: the current read-only check already refused26. The return pointer is103 bytes; reverse pointer112; both fit the observed116-column single-row constraint, but width eligibility cannot override lifetime failure.

## Source fingerprints

```text
271ec258d97dafb571ace56bcb8d53a6160a80631f67f32a41bb28f4d8fe1405  reports/cartan.tui-contract.2026-11-12.md
ad31a2b12a86dc3b9b8afb826f71eadd3ae370cf839a927b12627b6d71076b33  scripts/bus-poke.sh
ccaba59d53efe161c611dd7f4c48fc7788e7f5fe5e540ac0300ffed563a8b396  tests/adapter-test.sh
ad375c4e5b246fbc074dd6c2b19c8192cfec903155a7812028e4f903d1c5057d  tests/fake-agent.sh
1c81e2c4fcae8d225803b01023fc58267d1ef08a890215a39c557427591976ac  tests/tmux-interpose.sh
a22104d3b93284b8314e5405c5b56c0f6b1cb4337111c5cf3610a68e042ce421  tests/README.md
```

## Worker first isolated run (exit1)

```text
UTC=2026-11-12T08:52:23Z bash=5.3.15(1)-release tmux=tmux 3.7c artifacts=/tmp/vist-cycle01.EEPPun
C01 PASS rc=0 read-only state/log absent; composer-equal=yes
C02 PASS rc=0 literal receiver line text-calls=1 separate-Enter-calls=1; 2026-11-12T08:52:23Z notification-attempted server=vist-test pane=%1 msg=c02 receipt=unproven
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
/home/hruzam/ia-sync/.dev/session/vistMini-01-tests/tests/adapter-test.sh: line 69: 1835616 Killed                     bash "$ADAPTER" "$testmode" --server vist-test --pane "$pane" --pointer "$pointer" --state-dir "$scratch/state" "$@" > "$scratch/last.out" 2>&1
C14 PASS killed-after-reservation=137 restart=25 expected=25 no receipt; uncertain claim retained
C15 PASS unknown composer unchanged rc=29 expected=29
C16 PASS competing exits=0,25 exactly-one-line=1
C17 PASS registered amendment: forbidden vist-unregistered:%0 rc=2 expected=2 zero tmux calls
C17 PASS registered amendment: forbidden default:%999999999 rc=2 expected=2 zero tmux calls
C18 FAIL codex stand-in rc=27 literal submission
C18 PASS claude stand-in rc=0 literal submission
T01 PASS claude mirror=claude-empty check=0 expected=0 final=0 no live calls
T02 FAIL claude mirror=claude-suggestion check=0 expected=0 final=27 no live calls
2026-11-12T08:52:25Z refused code=27 receiver changed before Enter (observation=29); attempt uncertain
T02 FAIL claude mirror=claude-reset-dim check=0 expected=0 final=27 no live calls
2026-11-12T08:52:25Z refused code=27 receiver changed before Enter (observation=29); attempt uncertain
T03 PASS claude mirror=claude-typed check=23 expected=23 final=23 no live calls
T03 PASS claude mirror=claude-typed-start check=23 expected=23 final=23 no live calls
T04 PASS claude mirror=claude-whitespace check=23 expected=23 final=23 no live calls
T05 PASS claude mirror=claude-multiline check=23 expected=23 final=23 no live calls
T06 PASS claude mirror=claude-busy check=24 expected=24 final=24 no live calls
T07 PASS codex mirror=codex-busy check=24 expected=24 final=24 no live calls
T08 FAIL codex mirror=codex-placeholder check=0 expected=0 final=27 no live calls
2026-11-12T08:52:26Z refused code=27 receiver changed before Enter (observation=29); attempt uncertain
T09 PASS codex mirror=codex-typed check=23 expected=23 final=23 no live calls
T09 PASS codex mirror=codex-typed-start check=23 expected=23 final=23 no live calls
T10 PASS claude mirror=claude-rgb check=23 expected=23 final=23 no live calls
T10 PASS claude mirror=claude-bg-rgb check=23 expected=23 final=23 no live calls
T10 PASS claude mirror=claude-indexed check=23 expected=23 final=23 no live calls
T10 PASS claude mirror=claude-bg-indexed check=23 expected=23 final=23 no live calls
T10 PASS claude mirror=claude-mixed check=23 expected=23 final=23 no live calls
T11 PASS claude mirror=claude-missing-footer check=29 expected=29 final=29 no live calls
T11 PASS codex mirror=codex-missing-footer check=29 expected=29 final=29 no live calls
T11 PASS codex mirror=codex-alternative check=29 expected=29 final=29 no live calls
T12 PASS claude mirror=claude-historical check=0 expected=0 final=0 no live calls
T12 PASS codex mirror=codex-historical check=0 expected=0 final=0 no live calls
T13 PASS pointer would wrap/overflow validation rc=30 expected=30 unchanged/no reservation
T14 PASS forbidden vist-unregistered:%0 rc=2 no tmux call
T14 PASS forbidden default:%999999999 rc=2 no tmux call
T15 PASS mirrored state changed after text=27 restart=25 expected=27,25 no Enter/receipt
T16 PASS claude mirror=claude-suggestion check=0 expected=0 final=0 no live calls
T16 PASS codex mirror=codex-placeholder check=0 expected=0 final=0 no live calls
SUMMARY failures=4 artifacts=/tmp/vist-cycle01.EEPPun UTC=2026-11-12T08:52:28Z
```

## Worker second isolated run (exit0)

```text
UTC=2026-11-12T08:54:14Z bash=5.3.15(1)-release tmux=tmux 3.7c artifacts=/tmp/vist-cycle01.vzOU3c
C01 PASS rc=0 read-only state/log absent; composer-equal=yes
C02 PASS rc=0 literal receiver line text-calls=1 separate-Enter-calls=1; 2026-11-12T08:54:14Z notification-attempted server=vist-test pane=%1 msg=c02 receipt=unproven
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
/home/hruzam/ia-sync/.dev/session/vistMini-01-tests/tests/adapter-test.sh: line 69: 1837348 Killed                     bash "$ADAPTER" "$testmode" --server vist-test --pane "$pane" --pointer "$pointer" --state-dir "$scratch/state" "$@" > "$scratch/last.out" 2>&1
C14 PASS killed-after-reservation=137 restart=25 expected=25 no receipt; uncertain claim retained
C15 PASS unknown composer unchanged rc=29 expected=29
C16 PASS competing exits=25,0 exactly-one-line=1
C17 PASS registered amendment: forbidden vist-unregistered:%0 rc=2 expected=2 zero tmux calls
C17 PASS registered amendment: forbidden default:%999999999 rc=2 expected=2 zero tmux calls
C18 PASS codex stand-in rc=0 literal submission
C18 PASS claude stand-in rc=0 literal submission
T01 PASS claude mirror=claude-empty check=0 expected=0 final=0 no live calls
T02 PASS claude mirror=claude-suggestion check=0 expected=0 final=0 no live calls
T02 PASS claude mirror=claude-reset-dim check=0 expected=0 final=0 no live calls
T03 PASS claude mirror=claude-typed check=23 expected=23 final=23 no live calls
T03 PASS claude mirror=claude-typed-start check=23 expected=23 final=23 no live calls
T04 PASS claude mirror=claude-whitespace check=23 expected=23 final=23 no live calls
T05 PASS claude mirror=claude-multiline check=23 expected=23 final=23 no live calls
T05 PASS claude mirror=claude-continuation-start check=23 expected=23 final=23 no live calls
T05 PASS claude mirror=claude-dim-continuation-start check=23 expected=23 final=23 no live calls
T06 PASS claude mirror=claude-busy check=24 expected=24 final=24 no live calls
T07 PASS codex mirror=codex-busy check=24 expected=24 final=24 no live calls
T08 PASS codex mirror=codex-placeholder check=0 expected=0 final=0 no live calls
T09 PASS codex mirror=codex-typed check=23 expected=23 final=23 no live calls
T09 PASS codex mirror=codex-typed-start check=23 expected=23 final=23 no live calls
T10 PASS claude mirror=claude-rgb check=23 expected=23 final=23 no live calls
T10 PASS claude mirror=claude-bg-rgb check=23 expected=23 final=23 no live calls
T10 PASS claude mirror=claude-indexed check=23 expected=23 final=23 no live calls
T10 PASS claude mirror=claude-bg-indexed check=23 expected=23 final=23 no live calls
T10 PASS claude mirror=claude-mixed check=23 expected=23 final=23 no live calls
T11 PASS claude mirror=claude-missing-footer check=29 expected=29 final=29 no live calls
T11 PASS codex mirror=codex-missing-footer check=29 expected=29 final=29 no live calls
T11 PASS codex mirror=codex-alternative check=29 expected=29 final=29 no live calls
T12 PASS claude mirror=claude-historical check=0 expected=0 final=0 no live calls
T12 PASS codex mirror=codex-historical check=0 expected=0 final=0 no live calls
T13 PASS pointer-bytes=173 width=130 wrap validation rc=30 expected=30 unchanged/no reservation
T14 PASS forbidden vist-unregistered:%0 rc=2 no tmux call
T14 PASS forbidden default:%999999999 rc=2 no tmux call
T15 PASS mirrored state changed after text=27 restart=25 expected=27,25 no Enter/receipt
T16 PASS claude mirror=claude-suggestion check=0 expected=0 final=0 no live calls
T16 PASS codex mirror=codex-placeholder check=0 expected=0 final=0 no live calls
SUMMARY failures=0 artifacts=/tmp/vist-cycle01.vzOU3c UTC=2026-11-12T08:54:20Z
```

## Cartan final isolated run (exit0)

```text
UTC=2026-11-12T08:57:08Z bash=5.3.15(1)-release tmux=tmux 3.7c artifacts=/tmp/vist-cycle01.B3ND1J
C01 PASS rc=0 read-only state/log absent; composer-equal=yes
C02 PASS rc=0 literal receiver line text-calls=1 separate-Enter-calls=1; 2026-11-12T08:57:08Z notification-attempted server=vist-test pane=%1 msg=c02 receipt=unproven
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
/home/hruzam/ia-sync/.dev/session/vistMini-01-tests/tests/adapter-test.sh: line 69: 1839450 Killed                     bash "$ADAPTER" "$testmode" --server vist-test --pane "$pane" --pointer "$pointer" --state-dir "$scratch/state" "$@" > "$scratch/last.out" 2>&1
C14 PASS killed-after-reservation=137 restart=25 expected=25 no receipt; uncertain claim retained
C15 PASS unknown composer unchanged rc=29 expected=29
C16 PASS competing exits=0,25 exactly-one-line=1
C17 PASS registered amendment: forbidden vist-unregistered:%0 rc=2 expected=2 zero tmux calls
C17 PASS registered amendment: forbidden default:%999999999 rc=2 expected=2 zero tmux calls
C18 PASS codex stand-in rc=0 literal submission
C18 PASS claude stand-in rc=0 literal submission
T01 PASS claude mirror=claude-empty check=0 expected=0 final=0 no live calls
T02 PASS claude mirror=claude-suggestion check=0 expected=0 final=0 no live calls
T02 PASS claude mirror=claude-reset-dim check=0 expected=0 final=0 no live calls
T03 PASS claude mirror=claude-typed check=23 expected=23 final=23 no live calls
T03 PASS claude mirror=claude-typed-start check=23 expected=23 final=23 no live calls
T04 PASS claude mirror=claude-whitespace check=23 expected=23 final=23 no live calls
T05 PASS claude mirror=claude-multiline check=23 expected=23 final=23 no live calls
T05 PASS claude mirror=claude-continuation-start check=23 expected=23 final=23 no live calls
T05 PASS claude mirror=claude-dim-continuation-start check=23 expected=23 final=23 no live calls
T06 PASS claude mirror=claude-busy check=24 expected=24 final=24 no live calls
T07 PASS codex mirror=codex-busy check=24 expected=24 final=24 no live calls
T08 PASS codex mirror=codex-placeholder check=0 expected=0 final=0 no live calls
T09 PASS codex mirror=codex-typed check=23 expected=23 final=23 no live calls
T09 PASS codex mirror=codex-typed-start check=23 expected=23 final=23 no live calls
T10 PASS claude mirror=claude-rgb check=23 expected=23 final=23 no live calls
T10 PASS claude mirror=claude-bg-rgb check=23 expected=23 final=23 no live calls
T10 PASS claude mirror=claude-indexed check=23 expected=23 final=23 no live calls
T10 PASS claude mirror=claude-bg-indexed check=23 expected=23 final=23 no live calls
T10 PASS claude mirror=claude-mixed check=23 expected=23 final=23 no live calls
T11 PASS claude mirror=claude-missing-footer check=29 expected=29 final=29 no live calls
T11 PASS codex mirror=codex-missing-footer check=29 expected=29 final=29 no live calls
T11 PASS codex mirror=codex-alternative check=29 expected=29 final=29 no live calls
T12 PASS claude mirror=claude-historical check=0 expected=0 final=0 no live calls
T12 PASS codex mirror=codex-historical check=0 expected=0 final=0 no live calls
T13 PASS pointer-bytes=173 width=130 wrap validation rc=30 expected=30 unchanged/no reservation
T14 PASS forbidden vist-unregistered:%0 rc=2 no tmux call
T14 PASS forbidden default:%999999999 rc=2 no tmux call
T15 PASS mirrored state changed after text=27 restart=25 expected=27,25 no Enter/receipt
T16 PASS claude mirror=claude-suggestion check=0 expected=0 final=0 no live calls
T16 PASS codex mirror=codex-placeholder check=0 expected=0 final=0 no live calls
SUMMARY failures=0 artifacts=/tmp/vist-cycle01.B3ND1J UTC=2026-11-12T08:57:13Z
```

## Live read-only Claude check (exit26)

```text
2026-11-12T08:57:17Z refused code=26 unknown/dead/non-agent/unsafe/busy receiver
```

## Live read-only Codex check (exit26)

```text
2026-11-12T08:57:18Z refused code=26 unknown/dead/non-agent/unsafe/busy receiver
```

## Read-only top-level identity evidence

```text
UTC=2026-11-12T08:57:55.782669+00:00 metadata=traj-home|%0|claude|1815650 top_argv0='-zsh' top_comm='zsh' top_exe='/usr/bin/zsh'
UTC=2026-11-12T08:57:55.787057+00:00 metadata=cartan-home|%1|codex|1821701 top_argv0='-zsh' top_comm='zsh' top_exe='/usr/bin/zsh'
```
