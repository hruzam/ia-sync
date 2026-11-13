---
kind: trial-report
trial: vistMini-01-tests
date: 2026-11-13
host: home (same-host only)
author: trajectory · claude (writer, not verifier)
status: DRAFT — awaiting independent check
verifier: <cartan or assay: fill when named>
decision: majkee GO / STOP
tooling_state: scripts/vist-deliver.sh v3.1 (37887e7) = evidence tooling, NOT released (L21)
sources: STATUS.md · _bus/ · reports/cartan.cases-08.2026-11-13.md · ~/.local/state/vist/deliver.log (host-local, not committed)
---

# vistMini-01 — trial report (Claude ↔ Codex, home)

Rule for this report: every claim names its file. A seat's account of its own behaviour is not evidence.
The verifier should re-check the "evidence" column, not trust this prose.

## 1. Gate, part by part

| gate part | result | evidence |
|---|---|---|
| ≥3 ordinary messages each direction, no operator relay | **MET** | Codex→Claude 3/3 via tmux adapter (cycle 03). Claude→Codex 3/3 via `codex queue`: q01 `_bus/05.*`, q02 `_bus/06.*`, q03 `_bus/07.*` (`_bus/07.trajectory.verdict.md`, nonce `f54df1d7`) |
| every pre-registered refusal/recovery case run, expected vs observed | **MET with declared gaps** | `reports/cartan.cases-08.2026-11-13.md` (b08 NOK → r1 partial → r2 partial → r3 scoped PASS); `_bus/08.trajectory.verdict.md` |
| each seat's permission boundary stated | **STATED** (§3) | C09 + C06 on sample-claude, default mode |
| limits of applicability to VIST | **STATED** (§5) | |
| independently verified | **OPEN** | the verifier named above has not yet checked this file |
| majkee accepts | **OPEN** | |

## 2. Doors per direction (what was actually proven)

| direction | door | proven | notes |
|---|---|---|---|
| Claude → Codex | `codex queue --thread <uuid> --message <text>` | 3/3 ordinary, plus samples; queues when receiver is busy (C04 pass twice) | native door, no tmux input. CLI 0.169.0 |
| Codex → Claude | tmux adapter: paste pointer + Enter into the Claude composer | 3/3 (cycle 03) | the only inbound door from Codex today |
| Claude ↔ Claude | Claude `SendMessage` (cross-session) | **seen once** live, 2026-11-13: oraculum → trajectory ack bell (`_bus/09.oraculum.ack.md`, arrived as a cross-session message) | one observation, manual, at majkee's request. Not counted, not reliable-by-evidence |

## 3. Permission boundary (observed, not configured)

Sample-claude, **default mode**, evidence `/tmp/vc08r2.kk50sqqh/permission-tool-evidence.json` (host-local; extract in case file):
- **Allowed without prompt:** `Bash(pwd)` (C09). Which rule allowed it was not established.
- **Asked and held:** `Bash(printf … > marker)` showed "Do you want to proceed? › 1. Yes … Esc to cancel · Tab to amend" (C06). The controller classified it `needs_approval`, exit 31, typed nothing.
- **Released once by operator** (majkee, 13:10:46Z, option 1, one Enter, no mode or rule change). Marker written. Recorded as a separate operator act, not as unattended success.
- **The sample's own final text said no prompt was needed.** Screen and tool records contradict it. Receipts come from observation.
- Caveat: the pwd tool ran on `claude-haiku-5-5`; the approval-producing call ran on `claude-opus-4-8` after a provider fallback. Not a same-model pair.
- Senior seats: trajectory runs auto mode with a safety classifier that stops typing into other panes, `codex queue` and `git push` for operator approval. This was observed repeatedly during the trial. A local allow-list was added by majkee after cycle 09. Cartan's boundary is Codex's own and was not tested beyond the sample.

## 4. Cases (summary; full table in the case file)

| case | result |
|---|---|
| C08-01 unknown recipient (20) | PASS (r1) |
| C08-02 dead sample (21) | PASS (r1) |
| C08-03 duplicate (0 then 25), one turn | PASS (r1) |
| C08-04 busy Codex queue, truthful busy | r1 FAIL (state said ready) → PASS (r2) |
| C08-05 draft recovery | r1 FAIL (27, read-only client) → PASS (r2); r1 key preserved, never retried |
| C08-06 approval hold | PASS (r2 hold, no input, 31); release by operator |
| C08-07 dim placeholder as idle | PASS (r2) |
| C08-08 wait exhaustion (31, draft intact) | PASS (r1) |
| C08-09 permitted command | PASS (r2) |
| C08-10 unknown signature (29) | r1 FAIL (help screen read as approval); **unqualified**: no real unregistered view witnessed |
| C08-11 concurrent duplicate | PASS (r1), one pair only |
| C08-12 sender notice wakes sender | r2 FAIL (caller exit killed child) → r3 PASS (`setsid -f`, 0.3 s to turn, 7.9 s to final) |
| C08-13 help = dialog, not approval | PASS (r2) |

Counted sample tests never add to the senior-seat counts in §1.

## 5. Limits — what does NOT transfer to VIST

1. **Same host, two vendors, one operator.** No cross-host, no stranger panes. Cross-host claims are out of scope.
2. **Samples carried the disruptive cases.** Senior panes never saw them; behaviour on a long-running senior pane (huge scrollback, custom status line, wide composer) is only observed, not qualified.
3. **One run per case.** No reliability statistics. "PASS" = the scoped property held once, with the evidence cited.
4. **The screen signatures are data tied to Claude 2.1.323 and Codex 0.169.0.** A vendor update can silently change the composer, the dim suggestion, the approval text. The `unknown` → refuse path is the safety net, and it was exercised only on a classifier miss (C10 r1), not on a real new view.
5. **Observation is not consumption.** Exit 0 means queue accepted or keys submitted. Consumption needs a receipt from the receiver (nonce in the answer) or the native transcript.
6. **Unqualified original cases:** unknown surface (C10), crash or exit between text and Enter, expired or misaddressed requests, receiver semantic and hop limits. Declared gaps, not failures.
7. **The tmux adapter sends keystrokes.** L21 holds: any transport released into VIST needs its own release by the operator. The trial proves a prototype, not a release.
8. **Operator views.** A read-only tmux client breaks `send-keys` (exit 27 in r1, fixed by `paste-buffer`) and ignores scroll keys. This looks like a frozen UI. It is a viewer limit.
9. **The controller can only act on agent-as-pane-root.** Seats started under a shell are refused (22 `not_agent_root`). See §6.

## 6. Cycle 09 contact loop (live, uncounted)

Brief `_bus/09.trajectory.brief-team.md` (nonce `f60da3d1`), sent to cartan (codex), nablarva.cartan (codex), oraculum (claude).
- **Forward leg:** two Codex seats via `codex queue` (accepted, 0); oraculum via a manual paste (script refused: pane root is a shell, not the agent).
- **Replies:** all three wrote the right nonce and a role answer (`_bus/09.*.ack.md`, `311af01`).
- **Ring-backs through the script:** cartan and nablarva.cartan both refused **29 `unknown_composer`** (trajectory's composer unreadable while I was mid-work). The failure notice back to them was then refused **22 `not_agent_root`** because their windows were rebuilt with the agent under a shell. Both exit codes are in the ack files. `deliver.log` has the lines.
- **Oraculum's bell:** its Bash hook refused the script (no exit code). It sent a Claude SendMessage instead at the operator's request, which landed.
- **Findings for the next team:**
  1. Launch each seat as the pane's root process (`exec <agent>`), or the resolver refuses it. Roster rule already says so; the rebuilt windows broke it.
  2. When the sender's composer is unreadable the ring-back fails (29) and the notice path can fail too (22). The operator got no automatic wake. Needs a decision: a seat should record and wait, not chase.
  3. Window labels (`@seat @vendor @id @carrier`) were lost on rebuild and had to be set again by hand. The resolver depends on them.
  4. An oraculum with a Bash whitelist cannot ring the script. The two-way loop needs one door per seat that the seat is allowed to use.

## 7. Decisions recorded on the way

- Manual notice fallback only after sender-side refusals (`~/ia-sync/.dev/_backlog/cross-host-session-bus.md` §4.9, revised cycle 06).
- Keeper = watch-and-advise only. Cartan owns push and `/clear` (`STATUS.md` `decision_20261113_keeper`, majkee verbatim).
- Uncertain keys preserved, never retried: t03 and `sent/c08r1-05-ae3ee8e7`.

## 8. What I would ask the verifier to check

1. §1 counts against `_bus/05..07` and the cycle 03 files.
2. §3 permission pair against `/tmp/vc08r2.kk50sqqh/permission-tool-evidence.json` and `post-return-bash-approval.json`.
3. §4 case results against the case file, row by row.
4. That §5 does not overclaim anything §4 rests on.
5. §6 exit codes against `~/.local/state/vist/deliver.log` (lines for `20261113T-a09*`).

Open: verifier named · majkee GO/STOP · push by cartan.
