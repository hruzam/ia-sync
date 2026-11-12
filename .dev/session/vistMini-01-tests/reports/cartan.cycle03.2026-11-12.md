# Cycle03 trial — outbound demonstrated, reverse blocked

2026-11-12 · home:cartan · session base e5a5925 · registration b092ec2.

## Final observed result (ordinary trial, before administrative RETURN)

Three Cartan→Trajectory adapter sends returned0 and were consumed, attested by matching committed peer replies. Zero reverse sends are verified successful: t01/t02 refused29 before reservation/input; t03 failed27 after text injection and retains an uncertain reservation. The matching t03 pointer reached Cartan's user turn and its file was consumed, but the route that submitted it is unverified because the sender explicitly logged no Enter. That does not convert27 into adapter success or prove unassisted delivery. The head's thread03 stop rule applies: no04/05, no reservation removal or resend. The3+3 gate is not met; request reverse direction BLOCKED.

All40 distinct isolated C/T/R/F IDs passed after the exact-footer correction. This does not prove the unobserved real Codex typed-input/post-injection contract. The working hypothesis behind27 remains unverified because the failing post-text frame was not preserved. No further live experiment or guessed classifier change was performed.

| Thread | Cartan msg | Outbound evidence | Peer msg | Reverse evidence |
|---|---|---|---|---|
| 01 | 20261112T093315Z.c01 | check0/check0/send0; peer consumption attested | 20261112T093450Z.t01 | clean29; no send; manual notice |
| 02 | 20261112T094906Z.c02 | check0/check0/send0; peer consumption attested | 20261112T095114Z.t02 | clean29; no send; manual notice |
| 03 | 20261112T095553Z.c03 | check0/check0/send0; peer consumption attested | 20261112T095742Z.t03 | send27; text-attempted; no Enter logged; arrival route unverified |

The authoritative final RETURN is `_bus/03.cartan.return.md`; Trajectory alone owns the VERDICT, STATUS and push. The following earlier sections preserve preparation/development observations at their stated times.

## Verified preparation before thread01

The operator relaunched direct agents: default:%3/claude root1845156 and default:%2/codex root1844624. Root argv0 basename matches the expected agent; no shell-parent override. Binding registration was committed before code. The adapter rebind changes only two allowlist entries. Old%0/%1 refuse locally, including zero-tmux-call regression assertions.

Final `bash tests/adapter-test.sh` returned0 at09:29:47–09:29:53Z: all C01–C18 and T01–T16 PASS. Syntax check of adapter/one-shot/test harness and whitespace checks passed. A bounded fresh verifier inspected the registration, implementation and actual regression log and found no material issue. It did not execute a live handoff. No worker or Cartan push occurred; Trajectory owns push.

Initial read-only checks returned Claude%3=0 at09:30:42Z and own-active Codex%2=24 at09:30:44Z. Both passed the lifetime condition; Codex correctly refused busy. No reservation or input resulted from those checks. This is why a bounded turn-end one-shot must get actual0 on both after the controller yields, rather than asserting idle while still active.

Notification path base is explicitly the fixed session bed, registered before code. The helper performs one delay, two read-only checks, then at most one adapter send. Any refusal stops and is retained in its local diagnostic log. It is not a watcher or retry loop. No success or consumption is claimed from scheduling.

The unrelated untracked nano savefile remains untouched/unstaged. Head-owned RUNBOOK/STATUS/pulse/trajectory files were not edited. Git windows travel with the pointers. Only Cartan's assigned paths are committed.

## Thread receipts

Thread01 packet is `reports/trial-msgs/01.cartan.md`. At this report's initial commit, actual send/receipt is pending. Local one-shot output will be `/tmp/vistMini-cycle03-cartan-01.log`; its UTC/cmd/exit results will be promoted in the next received Git window. The peer reply must exist with matching `re` before thread02. Only matched reply content and verified submission support consumption/delivery; availability is not receipt.

## Initial live check outputs

```text
2026-11-12T09:30:42Z check=ready server=default pane=%3 attempt=none
2026-11-12T09:30:44Z refused code=24 unknown/dead/non-agent/unsafe/busy receiver
```

## Source fingerprints before thread01

```text
78df12d792b92c25be29c35a579a9bb3bf06375d465f659f20928ffaf2e03f4a  reports/cartan.binding-03.2026-11-12.md
d37803dae1e2212ad86b63497ca9347a1f61cb053179fac03468fa32d72fd6d1  scripts/bus-poke.sh
29f35d36c6595a8acaabb83ac44912c09d90382ed8f768e6d64e7f6c8f0b370b  scripts/handoff-once.sh
b2ec2a487a77876e4bfc66e79c289a3fea83054723bbcd388c06da33928abadd  tests/adapter-test.sh
4948354d8722559112e1a8cb8c108200a2ce50f91401ce793a3f49df4de41b7a  tests/README.md
```

## Regression output

```text
UTC=2026-11-12T09:29:47Z bash=5.3.15(1)-release tmux=tmux 3.7c artifacts=/tmp/vist-cycle01.ekGtgy
C01 PASS rc=0 read-only state/log absent; composer-equal=yes
C02 PASS rc=0 literal receiver line text-calls=1 separate-Enter-calls=1; 2026-11-12T09:29:48Z notification-attempted server=vist-test pane=%1 msg=c02 receipt=unproven
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
/home/hruzam/ia-sync/.dev/session/vistMini-01-tests/tests/adapter-test.sh: line 69: 1847007 Killed                     bash "$ADAPTER" "$testmode" --server vist-test --pane "$pane" --pointer "$pointer" --state-dir "$scratch/state" "$@" > "$scratch/last.out" 2>&1
C14 PASS killed-after-reservation=137 restart=25 expected=25 no receipt; uncertain claim retained
C15 PASS unknown composer unchanged rc=29 expected=29
C16 PASS competing exits=0,25 exactly-one-line=1
C17 PASS registered amendment: forbidden vist-unregistered:%0 rc=2 expected=2 zero tmux calls
C17 PASS registered amendment: forbidden default:%999999999 rc=2 expected=2 zero tmux calls
C17 PASS registered amendment: forbidden default:%0 rc=2 expected=2 zero tmux calls
C17 PASS registered amendment: forbidden default:%1 rc=2 expected=2 zero tmux calls
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
T14 PASS forbidden default:%0 rc=2 no tmux call
T14 PASS forbidden default:%1 rc=2 no tmux call
T15 PASS mirrored state changed after text=27 restart=25 expected=27,25 no Enter/receipt
T16 PASS claude mirror=claude-suggestion check=0 expected=0 final=0 no live calls
T16 PASS codex mirror=codex-placeholder check=0 expected=0 final=0 no live calls
SUMMARY failures=0 artifacts=/tmp/vist-cycle01.ekGtgy UTC=2026-11-12T09:29:53Z
```

## Thread01 observed outcome and recovery

Cartan one-shot process completed exit0 (tool session57965 reconciled). It logged both checks0 and one send0 at09:34:30–31Z. The committed peer reply b8d41ae matches re/thread and attests submitted-turn receipt and consumption. Reverse01 failed clean29 before send at09:35:28Z, followed by the authorized manual fallback notice (not counted). Current progress is one successful Cartan→Trajectory ordinary delivery and zero successful reverse adapter deliveries; matched files alone do not satisfy3+3.

A read-only idle Claude capture had cursor(2,55), a dim suggestion and expected footer; no background-task marker was seen in that later sample. Exact old failure cause remains unverified. `--check --server default --pane %3 --pointer '[bus recovery01] from home:cartan -> read reports/trial-msgs/01.cartan.md ; ack: none' --state-dir /tmp/vistMini-cycle03-cartan` returned0 at09:44:15Z without reservation/input.

Recovery registration f8ece4d preceded code. It adds bounded initial metadata-coherence observations only (three maximum, no returned-refusal retry) and preserves coherent unknown/busy/occupied/lifetime refusals. Helper clean29 diagnostics remain local-private. R01 transient jitter returns0 after4 metadata reads, R02 persistent jitter returns29 after6, no state/input. Full C/T/R suite exit0. This improves one known source29 path; it is not proof that it caused the earlier live failure or that an unknown background footer is safe.

Thread02 asks the head to verify and explicitly choose recovery of the missing reverse count. It is committed before its handoff; actual send outcome remains pending until its next pointer/log. No push by Cartan; no head-owned files edited; nano savefile untouched. Permission-pair evidence must come from the head's actual Claude approval outcomes, not this agent's tool policy.

### Cartan01 adapter calls

```text
2026-11-12T09:34:22Z handoff-scheduled delay=8 target=%3
2026-11-12T09:34:30Z call mode=--check server=default pane=%2 state=/tmp/vistMini-cycle03-cartan pointer=[bus 20261112T093315Z.c01] from home:cartan -> read reports/trial-msgs/01.cartan.md ; ack: reply
2026-11-12T09:34:30Z check=ready server=default pane=%2 attempt=none
2026-11-12T09:34:30Z result mode=--check pane=%2 exit=0
2026-11-12T09:34:30Z call mode=--check server=default pane=%3 state=/tmp/vistMini-cycle03-cartan pointer=[bus 20261112T093315Z.c01] from home:cartan -> read reports/trial-msgs/01.cartan.md ; ack: reply
2026-11-12T09:34:30Z check=ready server=default pane=%3 attempt=none
2026-11-12T09:34:30Z result mode=--check pane=%3 exit=0
2026-11-12T09:34:30Z call mode=--send server=default pane=%3 state=/tmp/vistMini-cycle03-cartan pointer=[bus 20261112T093315Z.c01] from home:cartan -> read reports/trial-msgs/01.cartan.md ; ack: reply
2026-11-12T09:34:31Z notification-attempted server=default pane=%3 msg=20261112T093315Z.c01 receipt=unproven
2026-11-12T09:34:31Z result mode=--send pane=%3 exit=0
```

### Peer01 clean refusal (no send)

```text
2026-11-12T09:35:20Z handoff-scheduled delay=8 target=%2
2026-11-12T09:35:28Z call mode=--check server=default pane=%2 state=/tmp/vistMini-cycle03-trajectory pointer=[bus 03-01.t] from home:trajectory -> read reports/trial-msgs/01.trajectory.md ; ack: none
2026-11-12T09:35:28Z check=ready server=default pane=%2 attempt=none
2026-11-12T09:35:28Z result mode=--check pane=%2 exit=0
2026-11-12T09:35:28Z call mode=--check server=default pane=%3 state=/tmp/vistMini-cycle03-trajectory pointer=[bus 03-01.t] from home:trajectory -> read reports/trial-msgs/01.trajectory.md ; ack: none
2026-11-12T09:35:28Z refused code=29 unknown/dead/non-agent/unsafe/busy receiver
2026-11-12T09:35:28Z result mode=--check pane=%3 exit=29
```

### Later idle check

```text
2026-11-12T09:44:15Z check=ready server=default pane=%3 attempt=none
```

### Recovery isolated tests

```text
UTC=2026-11-12T09:46:32Z bash=5.3.15(1)-release tmux=tmux 3.7c artifacts=/tmp/vist-cycle01.YXEFjJ
C01 PASS rc=0 read-only state/log absent; composer-equal=yes
C02 PASS rc=0 literal receiver line text-calls=1 separate-Enter-calls=1; 2026-11-12T09:46:32Z notification-attempted server=vist-test pane=%1 msg=c02 receipt=unproven
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
/home/hruzam/ia-sync/.dev/session/vistMini-01-tests/tests/adapter-test.sh: line 69: 1850698 Killed                     bash "$ADAPTER" "$testmode" --server vist-test --pane "$pane" --pointer "$pointer" --state-dir "$scratch/state" "$@" > "$scratch/last.out" 2>&1
C14 PASS killed-after-reservation=137 restart=25 expected=25 no receipt; uncertain claim retained
C15 PASS unknown composer unchanged rc=29 expected=29
C16 PASS competing exits=25,0 exactly-one-line=1
C17 PASS registered amendment: forbidden vist-unregistered:%0 rc=2 expected=2 zero tmux calls
C17 PASS registered amendment: forbidden default:%999999999 rc=2 expected=2 zero tmux calls
C17 PASS registered amendment: forbidden default:%0 rc=2 expected=2 zero tmux calls
C17 PASS registered amendment: forbidden default:%1 rc=2 expected=2 zero tmux calls
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
T14 PASS forbidden default:%0 rc=2 no tmux call
T14 PASS forbidden default:%1 rc=2 no tmux call
T15 PASS mirrored state changed after text=27 restart=25 expected=27,25 no Enter/receipt
T16 PASS claude mirror=claude-suggestion check=0 expected=0 final=0 no live calls
T16 PASS codex mirror=codex-placeholder check=0 expected=0 final=0 no live calls
R01 PASS metadata-once rc=0 expected=0 metadata-reads=4 expected=4 no state/input
R02 PASS metadata-always rc=29 expected=29 metadata-reads=6 expected=6 no state/input
SUMMARY failures=0 artifacts=/tmp/vist-cycle01.YXEFjJ UTC=2026-11-12T09:46:38Z
```

Recovery code committed as `b8523ef`; a fresh bounded verifier inspected source/registration/log and reported PASS, without running live operations. Diagnostics remain private caller output, so next launch uses umask077.

Additional stamp mismatch: the failed peer01 pointer used `03-01.t`, while the committed envelope msg is `20261112T093450Z.t01`. This did not cause preflight29 (it is a separate data contract issue). Thread02 asks the head to use its exact reply-envelope msg in the next pointer, rather than copy an example ID.

### Recovery source fingerprints

```text
c68450ea61d56c960a8f789d94aceead0189240308a4f68341623228718e87ad  scripts/bus-poke.sh
1537cd2463b11fc24d1a3c3a8477accce18d3b412fb99b2045ebc336be44ac16  scripts/handoff-once.sh
4de5064d38e5fcc4f79ad08f085e151570afdc1edbc0254e72bbea6129c043f9  tests/adapter-test.sh
83fc1ad8900d67c1897347432586759f9488b948d3923a8838cf8a6ebbe3f2f0  tests/tmux-interpose.sh
02bc37c8929729fde1b10377399cc4919062544a2321fce7ef531c29534a981c  tests/README.md
```

## Thread02 and observed footer correction

Cartan02 one-shot completed exit0; both checks0 followed by exactly one send0 at09:51:03Z. Peer reply e6ecc03 matches re/thread and now aligns pointer/envelope msg IDs; it attests consumption. Reverse02 clean29 occurred at09:51:40Z, before reservation/send. Its diagnostic supplies an empty composer and the following exact footer, redacted from the otherwise private frame:

```text
  ⏵⏵ auto mode on · 1 shell · ← 1 agent · ↓ to manage
```

The old known-footer predicate required the shortcut hint `(shift+tab to cycle)`, absent during the caller's background shell task. Registration d67334b precedes code96edca6, a literal footer alternative only. Both self/recipient checks remain. F01/F02 allow the exact observed empty/dim-suggestion states; F03 preserves typed23/busy24; F04 rejects unobserved two-shell29. All prior cases plus these four IDs pass (40 distinct registered IDs). Fresh read-only verification PASS; no live calls by the reviewer. This diagnoses the observed reverse02 layout; reverse01 remains unproven because its frame was not recorded.

Counts before03: two successful consumed Cartan deliveries; zero reverse adapter deliveries. Both manual notices are outside count. The head authorized04 after observing only the first failure; after the second failure,03/04 could give only two reverse successes. Thread03 asks the head to authorize a fifth bounded pair rather than pretend the3+3 gate is met. Current STATUS's thread01 snapshot lags the newer thread02 artifacts; this report retains observations only and does not replace head-owned STATUS.

### Cartan02 actual adapter calls

```text
2026-11-12T09:50:54Z handoff-scheduled delay=8 target=%3
2026-11-12T09:51:02Z call mode=--check server=default pane=%2 state=/tmp/vistMini-cycle03-cartan pointer=[bus 20261112T094906Z.c02] from home:cartan -> read reports/trial-msgs/02.cartan.md ; ack: reply
2026-11-12T09:51:03Z check=ready server=default pane=%2 attempt=none
2026-11-12T09:51:03Z result mode=--check pane=%2 exit=0
2026-11-12T09:51:03Z call mode=--check server=default pane=%3 state=/tmp/vistMini-cycle03-cartan pointer=[bus 20261112T094906Z.c02] from home:cartan -> read reports/trial-msgs/02.cartan.md ; ack: reply
2026-11-12T09:51:03Z check=ready server=default pane=%3 attempt=none
2026-11-12T09:51:03Z result mode=--check pane=%3 exit=0
2026-11-12T09:51:03Z call mode=--send server=default pane=%3 state=/tmp/vistMini-cycle03-cartan pointer=[bus 20261112T094906Z.c02] from home:cartan -> read reports/trial-msgs/02.cartan.md ; ack: reply
2026-11-12T09:51:03Z notification-attempted server=default pane=%3 msg=20261112T094906Z.c02 receipt=unproven
2026-11-12T09:51:03Z result mode=--send pane=%3 exit=0
```

### Reverse02 refusal headers (private frame omitted)

```text
2026-11-12T09:51:32Z handoff-scheduled delay=8 target=%2
2026-11-12T09:51:40Z call mode=--check server=default pane=%2 state=/tmp/vistMini-cycle03-trajectory pointer=[bus 20261112T095114Z.t02] from home:trajectory -> read reports/trial-msgs/02.trajectory.md ; ack: none
2026-11-12T09:51:40Z check=ready server=default pane=%2 attempt=none
2026-11-12T09:51:40Z result mode=--check pane=%2 exit=0
2026-11-12T09:51:40Z call mode=--check server=default pane=%3 state=/tmp/vistMini-cycle03-trajectory pointer=[bus 20261112T095114Z.t02] from home:trajectory -> read reports/trial-msgs/02.trajectory.md ; ack: none
2026-11-12T09:51:40Z refused code=29 unknown/dead/non-agent/unsafe/busy receiver
2026-11-12T09:51:40Z result mode=--check pane=%3 exit=29
```

### Exact-footer regression output

```text
UTC=2026-11-12T09:53:59Z bash=5.3.15(1)-release tmux=tmux 3.7c artifacts=/tmp/vist-cycle01.I5BHWG
C01 PASS rc=0 read-only state/log absent; composer-equal=yes
C02 PASS rc=0 literal receiver line text-calls=1 separate-Enter-calls=1; 2026-11-12T09:53:59Z notification-attempted server=vist-test pane=%1 msg=c02 receipt=unproven
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
/home/hruzam/ia-sync/.dev/session/vistMini-01-tests/tests/adapter-test.sh: line 69: 1853695 Killed                     bash "$ADAPTER" "$testmode" --server vist-test --pane "$pane" --pointer "$pointer" --state-dir "$scratch/state" "$@" > "$scratch/last.out" 2>&1
C14 PASS killed-after-reservation=137 restart=25 expected=25 no receipt; uncertain claim retained
C15 PASS unknown composer unchanged rc=29 expected=29
C16 PASS competing exits=25,0 exactly-one-line=1
C17 PASS registered amendment: forbidden vist-unregistered:%0 rc=2 expected=2 zero tmux calls
C17 PASS registered amendment: forbidden default:%999999999 rc=2 expected=2 zero tmux calls
C17 PASS registered amendment: forbidden default:%0 rc=2 expected=2 zero tmux calls
C17 PASS registered amendment: forbidden default:%1 rc=2 expected=2 zero tmux calls
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
T14 PASS forbidden default:%0 rc=2 no tmux call
T14 PASS forbidden default:%1 rc=2 no tmux call
T15 PASS mirrored state changed after text=27 restart=25 expected=27,25 no Enter/receipt
T16 PASS claude mirror=claude-suggestion check=0 expected=0 final=0 no live calls
T16 PASS codex mirror=codex-placeholder check=0 expected=0 final=0 no live calls
F01 PASS claude mirror=claude-shell-empty check=0 expected=0 final=0 no live calls
F02 PASS claude mirror=claude-shell-suggestion check=0 expected=0 final=0 no live calls
F03 PASS claude mirror=claude-shell-typed check=23 expected=23 final=23 no live calls
F03 PASS claude mirror=claude-shell-busy check=24 expected=24 final=24 no live calls
F04 PASS claude mirror=claude-two-shell-empty check=29 expected=29 final=29 no live calls
R01 PASS metadata-once rc=0 expected=0 metadata-reads=4 expected=4 no state/input
R02 PASS metadata-always rc=29 expected=29 metadata-reads=6 expected=6 no state/input
SUMMARY failures=0 artifacts=/tmp/vist-cycle01.I5BHWG UTC=2026-11-12T09:54:05Z
```

## Thread03 stop and uncertainty preservation

Recorded at 2026-11-12T10:12:43Z. The peer authorized04/05 only while expecting successful reverse03, and explicitly required stopping if03 failed again. Actual reverse03 failed27 after text-attempted; therefore no04 or05 packet is created. Existing matching reply files establish content availability and Cartan consumption, not successful adapter submission. A fresh verifier checked all six headers and relevant log/result/state lines, found the live3+3 criterion unmet and recommended BLOCKED. No tests or live calls were run by that reviewer.

The received pointer's mechanism remains unknown: it may not be attributed to the adapter from these artifacts. No claim of operator intervention or policy violation is inferred. Cartan has consumed03.trajectory.md once; that receipt resolves application consumption but not transport attribution. Never clear the uncertain key or blindly resubmit it. A next bounded investigation should first preserve the actual post-text Codex frame; do not assume a dim/paste/footer cause without evidence.

### All Cartan-side live adapter commands

Canonical invocation for rows below: `bash /home/hruzam/ia-sync/.dev/session/vistMini-01-tests/scripts/bus-poke.sh MODE --server default --pane PANE --pointer POINTER --state-dir /tmp/vistMini-cycle03-cartan`.

Initial read-only calls at09:30:42(check%3=0) and09:30:44(check%2=24) used pointer `[bus 20261112T0930Z.c01] from home:cartan -> read reports/trial-msgs/01.cartan.md ; ack: reply`. Later09:44:15 check%3=0 used `[bus recovery01] from home:cartan -> read reports/trial-msgs/01.cartan.md ; ack: none`. Neither created a reservation/input. The three ordinary handoff logs embedded in this report give every subsequent actual MODE/PANE/POINTER/UTC/exit: two checks then one send per thread. Those are nine additional calls, all0. No other parent-side live adapter call occurred before this report's publication. The administrative RETURN's future one-shot is separately logged at `/tmp/vistMini-cycle03-cartan-return.log` and must be attested by the receiving head; it is not a fourth ordinary trial success.

### Cartan03 actual calls

```text
2026-11-12T09:57:19Z handoff-scheduled delay=8 target=%3
2026-11-12T09:57:27Z call mode=--check server=default pane=%2 state=/tmp/vistMini-cycle03-cartan pointer=[bus 20261112T095553Z.c03] from home:cartan -> read reports/trial-msgs/03.cartan.md ; ack: reply
2026-11-12T09:57:27Z check=ready server=default pane=%2 attempt=none
2026-11-12T09:57:27Z result mode=--check pane=%2 exit=0
2026-11-12T09:57:27Z call mode=--check server=default pane=%3 state=/tmp/vistMini-cycle03-cartan pointer=[bus 20261112T095553Z.c03] from home:cartan -> read reports/trial-msgs/03.cartan.md ; ack: reply
2026-11-12T09:57:27Z check=ready server=default pane=%3 attempt=none
2026-11-12T09:57:27Z result mode=--check pane=%3 exit=0
2026-11-12T09:57:27Z call mode=--send server=default pane=%3 state=/tmp/vistMini-cycle03-cartan pointer=[bus 20261112T095553Z.c03] from home:cartan -> read reports/trial-msgs/03.cartan.md ; ack: reply
2026-11-12T09:57:27Z notification-attempted server=default pane=%3 msg=20261112T095553Z.c03 receipt=unproven
2026-11-12T09:57:27Z result mode=--send pane=%3 exit=0
```

### Peer03 uncertain attempt

```text
2026-11-12T09:58:01Z handoff-scheduled delay=8 target=%2
2026-11-12T09:58:09Z call mode=--check server=default pane=%2 state=/tmp/vistMini-cycle03-trajectory pointer=[bus 20261112T095742Z.t03] from home:trajectory -> read reports/trial-msgs/03.trajectory.md ; ack: none
2026-11-12T09:58:09Z check=ready server=default pane=%2 attempt=none
2026-11-12T09:58:09Z result mode=--check pane=%2 exit=0
2026-11-12T09:58:09Z call mode=--check server=default pane=%3 state=/tmp/vistMini-cycle03-trajectory pointer=[bus 20261112T095742Z.t03] from home:trajectory -> read reports/trial-msgs/03.trajectory.md ; ack: none
2026-11-12T09:58:09Z check=ready server=default pane=%3 attempt=none
2026-11-12T09:58:09Z result mode=--check pane=%3 exit=0
2026-11-12T09:58:09Z call mode=--send server=default pane=%2 state=/tmp/vistMini-cycle03-trajectory pointer=[bus 20261112T095742Z.t03] from home:trajectory -> read reports/trial-msgs/03.trajectory.md ; ack: none
2026-11-12T09:58:12Z refused code=27 injected text not exactly visible; no Enter sent
2026-11-12T09:58:12Z result mode=--send pane=%2 exit=27
```

### Attempt directories, as observed before administrative RETURN

```text
/tmp/vistMini-cycle03-cartan
  1e40d898a5c124f0b74656456ff540542183921e71d2cc13d115553259c259c6/state: phase=enter-attempted msg=20261112T093315Z.c01 utc=2026-11-12T09:34:31Z
  a6bf1a8cef5801f1c7716a7d9146b29c803de8a56d72f50f0a14d9c9fea04bdf/state: phase=enter-attempted msg=20261112T094906Z.c02 utc=2026-11-12T09:51:03Z
  c5eeaec3b42e2c1ca8158903f4ea32d8626173bcdd338e72dfd42a21938d8251/state: phase=enter-attempted msg=20261112T095553Z.c03 utc=2026-11-12T09:57:27Z
/tmp/vistMini-cycle03-trajectory
  5e9f0d4a1e1c49f5dbbd3feb9d6da4b40d11ffd50207e36012206f93541ca0f8/state: phase=text-attempted msg=20261112T095742Z.t03 utc=2026-11-12T09:58:09Z
```

Cartan has three `enter-attempted` ordinary keys; Trajectory has one `text-attempted` uncertain key. These phases are attempt evidence, never receipt stamps. The future administrative RETURN may add a separate Cartan key after publication; it does not alter the ordinary counts or this time-bounded snapshot.

## Permission, VIST and acceptance limits

Cartan committed only assigned paths and did not push; the operator nano savefile remains untouched. ia-sync is now writable in the workspace, while `.git` and tmux access still used explicit tool escalation as required. No permission config was changed by Cartan. The requested Claude allowed-push/unlisted-command pair has not yet been independently witnessed: Trajectory must attach its actual redacted command/UTC/decision receipts at its VERDICT/push, not rely on Codex's policy or a settings-file claim. Root cannot establish another runtime's classifier result by running the same command here.

VIST/Oraculum route and bounded context remain unverified, as do receiver-layer expiry/path/recipient/hop semantics and broad reliability. This was a small engineering smoke trial, not statistical validation. The main gate remains open/blocked; there is no operator acceptance in this artifact. Head-owned STATUS still needs reconciliation to these observed later outcomes; Cartan has not edited it. Any future recovery must preserve consumed-message deduplication and the uncertain reservation.
