---
kind: trial-report
trial: vistMini-01-tests
date: 2026-11-13
host: home (same-host only)
author: trajectory · claude (writer, not verifier)
status: DRAFT r2 — R1–R6 from _bus/09.cartan.verify.md (ef275f3) applied; awaiting fresh independent check
revision_of: db55d24
verifier: pending fresh check (r1 review by cartan was NOK; that review does not cover this revision)
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
| every pre-registered refusal/recovery case run, expected vs observed | **PARTIAL / OPEN** | Cycle 08 rows C01–C13 run with expected vs observed (`reports/cartan.cases-08.2026-11-13.md`, b08 NOK → r1 → r2 → r3; `_bus/08.trajectory.verdict.md`). **Not run or unqualified:** C10 unregistered native view; agent exit or crash between text and Enter; expired or misaddressed requests; receiver semantic and hop limits (case file, "Remaining findings" and r3 notes). Closing this part needs those runs or a recorded operator scope decision |
| each seat's permission boundary stated | **STATED** (§3) | C09 + C06 on sample-claude, default mode |
| limits of applicability to VIST | **STATED** (§5) | |
| independently verified | **OPEN** | the verifier named above has not yet checked this file |
| majkee accepts | **OPEN** | |

## 2. Doors per direction (what was actually proven)

| direction | door | proven | notes |
|---|---|---|---|
| Claude → Codex | `codex queue --thread <uuid> --message <text>` | 3/3 ordinary, plus samples; queues when receiver is busy (C04 pass twice) | native door, no tmux input. CLI 0.169.0 |
| Codex → Claude | tmux adapter: paste pointer + Enter into the Claude composer | 3/3 (cycle 03) | the inbound door from Codex exercised in this trial; others not tested here |
| Claude ↔ Claude | Claude `SendMessage` (cross-session) | **seen once** live, 2026-11-13: oraculum → trajectory ack bell (`_bus/09.oraculum.ack.md`, arrived as a cross-session message) | one observation, manual, at majkee's request. Not counted, not reliable-by-evidence |

## 3. Permission boundary (observed, not configured)

Sample-claude, **default mode**, evidence `/tmp/vc08r2.kk50sqqh/permission-tool-evidence.json` (host-local; extract in case file):
- **Allowed without prompt:** `Bash(pwd)` (C09). Which rule allowed it was not established.
- **Asked and held:** `Bash(printf … > marker)` showed "Do you want to proceed? › 1. Yes … Esc to cancel · Tab to amend" (C06). The controller classified it `needs_approval`, exit 31, typed nothing.
- **Released once by operator** (majkee, 13:10:46Z, option 1, one Enter, no mode or rule change). Marker written. Recorded as a separate operator act, not as unattended success.
- **The sample's own final text said no prompt was needed.** Screen and tool records contradict it. Receipts come from observation.
- Caveat: the pwd tool ran on `claude-haiku-5-5`; the approval-producing call ran on `claude-opus-4-8` after a provider fallback. Not a same-model pair.
Senior seats (dated, not uniform across the trial; no parity claimed):
- **trajectory, 2026-11-12** (`reports/trajectory.permissions.2026-11-12.md`): auto-mode classifier, not a settings rule. In that session
  `tmux send-keys` into cartan's pane, ssh send-keys and `git add/commit/push` ran **without** prompt. That file already notes auto mode can refuse later what it allowed earlier.
- **trajectory, 2026-11-13 ~15:40–16:00Z (cycle 09) — UNVERIFIED, operator and author accounts only, no captured receipt for any part:**
  per majkee's in-session reports, trajectory Bash calls combining `codex queue`, tmux paste into another pane and/or `git push` raised operator
  approval prompts; which subcommand triggered each is not known. Per majkee's statement, a host-local allow-list was then added
  (`~/ia-sync/.claude/settings.local.json`, not committed, contents not cited here). Per trajectory's own account, later single-step
  `git add/commit` and `codex queue` calls completed without a prompt being reported. None of this paragraph is independently evidenced.
- **cartan, 2026-11-12** (`reports/cartan.preflight.2026-11-12.md` lines 21–22): ordinary sandbox denied the tmux socket ("Operation not permitted");
  the same listing succeeded with explicit escalation at 08:03Z. Later Codex boundaries were not separately recorded in this report.

## 4. Cases (summary; full table in the case file)

| case | result |
|---|---|
| C08-01 unknown recipient (20) | PASS (r1) |
| C08-02 dead sample (21) | PASS (r1) |
| C08-03 duplicate (0 then 25), one turn | PASS (r1) |
| C08-04 busy Codex queue, truthful busy | r1 FAIL (state said ready) → PASS (r2) |
| C08-05 draft recovery | r1 FAIL (27, read-only client) → PASS (r2); r1 key preserved, never retried |
| C08-06 approval hold | PASS (r2 hold, no input, 31); release by operator |
| C08-07 dim placeholder as idle | carrier/placeholder PASS (r2); **consumption only after operator-authorised Read grant** (`Read(//tmp/vc08r2.kk50sqqh/**)`, native option 2, 12:46:27Z; `/tmp/vc08r2.kk50sqqh/operator-read-grant.json`, `07-default-receipt.json`). Separate from the later one-time Bash release. Counts unchanged |
| C08-08 wait exhaustion (31, draft intact) | PASS (r1) |
| C08-09 permitted command | PASS (r2) |
| C08-10 unknown signature (29) | r1 FAIL (help screen read as approval); **unqualified**: no real unregistered view witnessed |
| C08-11 concurrent duplicate | PASS (r1), one pair only |
| C08-12 sender notice wakes sender | r2 FAIL: no child attempt or receiving turn observed after the caller returned immediately; **exact cause unconfirmed** (process-group kill is an inference, not instrumented). r2 C12b: with caller held alive 10 s, child queued and was consumed, final ~41 s (outside the 30 s budget). r3 PASS, one run on v3.1 (`setsid -f`): 0.325 s to turn, 7.852 s to final (`_bus/08.cartan.return-r3.md` §4; `/tmp/vc08r3.j6lgeedf/receipt.json`) |
| C08-13 help = dialog, not approval | PASS (r2) |

Counted sample tests never add to the senior-seat counts in §1.

## 5. Limits — what does NOT transfer to VIST

1. **Same host, two vendors, one operator.** No cross-host, no stranger panes. Cross-host claims are out of scope.
2. **Samples carried the disruptive cases.** Senior panes never saw them; behaviour on a long-running senior pane (huge scrollback, custom status line, wide composer) is only observed, not qualified.
3. **A small number of scoped runs per case, across revisions (r1, r2, r3).** No reliability statistics. "PASS" = the scoped property held in the cited run(s).
4. **The screen signatures are data tied to Claude 2.1.323 and Codex 0.169.0.** A vendor update can silently change the composer, the dim suggestion, the approval text. The `unknown` → refuse path is the safety net, and it was exercised only on a classifier miss (C10 r1), not on a real new view.
5. **Observation is not consumption.** Exit 0 means queue accepted or keys submitted. Consumption needs a receipt from the receiver (nonce in the answer) or the native transcript.
6. **Unqualified original cases:** unknown surface (C10), crash or exit between text and Enter, expired or misaddressed requests, receiver semantic and hop limits. Declared gaps, not failures.
7. **The tmux adapter sends keystrokes.** L21 holds: any transport released into VIST needs its own release by the operator. The trial proves a prototype, not a release.
8. **Operator views.** Observed in r1 (build `06cc9b4`): the helper's default-routed `tmux send-keys` failed "client is read-only" (exit 27) while read-only spectator clients were attached; cleanup through an explicitly chosen existing writable client succeeded. The exact selection mechanism is unconfirmed, and this is not a claim that every read-only viewer breaks every send. Build `22d5008` (r2) replaced the typed carrier with `paste-buffer`. Read-only clients also ignored scrolling in majkee's views, which looked like a frozen UI. Viewer limit as observed here.
9. **The controller can only act on agent-as-pane-root.** Seats started under a shell are refused (22 `not_agent_root`). See §6.

## 6. Cycle 09 contact loop (live, uncounted)

Brief `_bus/09.trajectory.brief-team.md` (nonce `f60da3d1`), sent to cartan (codex), nablarva.cartan (codex), oraculum (claude).
- **Forward leg:** two Codex seats via `codex queue` (accepted, 0); oraculum via a manual paste (script refused: pane root is a shell, not the agent).
- **Replies:** all three wrote the right nonce and a role answer (`_bus/09.*.ack.md`, `311af01`).
- **Ring-backs through the script** (`~/.local/state/vist/deliver.log`, host-local; the ack files record only the 29):

  | logical ID | parent refusal | callback refusal |
  |---|---|---|
  | `20261113T-a09nablarva-cartan` | 15:49:07Z, 29 `unknown_composer` (recipient = trajectory pane %3) | `.n` 15:49:08Z, 22 `not_agent_root`, pane %23 |
  | `20261113T-a09cartan` | 15:50:07Z, 29 `unknown_composer` (recipient = trajectory pane %3) | `.n` 15:50:07Z, 22 `not_agent_root`, pane %47 |

  No manual retry by cartan.
- **Oraculum's bell:** per its ack (`_bus/09.oraculum.ack.md`), its PreToolUse hook rejected this one invocation of the script before execution (no exit code).
  It then sent a Claude SendMessage at the operator's request; trajectory received it. That SendMessage is reported from trajectory's side only and is not covered by the deliver.log check.
- **Findings for the next team:**
  1. Launch each seat as the pane's root process (`exec <agent>`), or the resolver refuses it. Roster rule already says so; the rebuilt windows broke it.
  2. When the **recipient's** composer is unreadable (here trajectory, mid-work) the ring-back is refused (29), and the failure notice to the sender can then be refused too (22) if the sender's pane is shell-rooted. Nobody was woken automatically. Needs a decision: record and wait, not chase.
  3. Window labels (`@seat @vendor @id @carrier`) were lost on rebuild and had to be set again by hand. The resolver depends on them.
  4. This oraculum's hook rejected this script invocation. The two-way loop needs, per seat, one door that seat's own rules allow.

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

6. For this revision specifically: R1–R6 dispositions in `_bus/10.trajectory.return.md` against `_bus/09.cartan.verify.md`.

Open: fresh independent check of this revision · all-cases gate part (PARTIAL/OPEN, §1) · majkee GO/STOP · push by cartan.
