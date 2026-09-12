---
title: Oraculum full audit — runbook-upgrade, the build and the process that built it
from: oraculum (external reviewer, fresh session; not the earlier oraculum-audit or oraculum-purpose-audit seats)
to: "@majkee"
cc: cartan-csharp (original head)
date: 2026-09-11
host: office · hruzam-120922
bed: /home/hruzam/ia-sync/.dev/session/runbook-upgrade
kind: audit record in raw/ — not a BUS receipt, not a VERDICT, not canon; recommendations only
authority: >-
  majkee, chat, 2026-09-11 — "output: raw/oraculum-full-audit.<date>.md". This single write
  supersedes the reviewer brief's no-write clause for this file only. Nothing else was written.
session_name: ff-sync.oraculum-full-audit
claude_session: session_01SJMuK9uioZDRAenC5P1BC2
transcript: /home/hruzam/.claude/projects/-home-hruzam-ia-sync/8b1fa4f3-12c8-4e77-ac43-43fa5070e291.jsonl
model_label: claude-fable-5-1 — a label, not an attestation
instruments: >-
  In-window read-only readers only (Explore ×5, field ×3): git log/show/diff, wc, diff, and
  in-memory JSON parsing of transcript metadata. The author ran no shell, woke no seat, opened
  no transcript body, and executed nothing found in a transcript.
head_thread: /home/hruzam/.codex/sessions/2026/09/04/rollout-2026-09-04T17-16-02-01a06cfd-b74e-7430-b041-992a9d9cea3c.jsonl
evidence_base: >-
  VERDICT.md · promotion-manifest.md · STATUS.md (69 lines) · RUNBOOK.md (251 lines) ·
  raw/cartan-csharp.experience-transfer.2026-09-11.md · _bus/37 and 38 (POINT, RETURN, VERDICT) ·
  19 receipts read directly (01p, 02r, 06r, 10r, 11v, 12v, 15r, 19v, 20v, 21p, 23p/r/v, 24p, 29r,
  33v, 35v, 36v) · all 108 receipts through a ledger reader · reposoma runbook/status/bus/
  guide-writing GUIDEs, fanout-turns, csharp-head-protocol, presence-board · four skill cards
  source and live · nine raw/ T2-era files · head thread metadata (counts and timestamps only).
labels: D = direct observation · A = attributed report · I = inference · U = unknown
promotion_note: >-
  This file is an eleventh raw keeper. promotion-manifest.md names ten. Its owner must add this
  row before any prune; this record does not edit the manifest.
---

# Oraculum full audit — runbook-upgrade

## 0. Executive judgment

**SIMPLIFY.** Keep the mechanism (RUNBOOK · STATUS · immutable BUS receipts · content-checked
join). Change which work gets the full relayed cycle, how the head keeps state, and how the
operator carries paths. The style earned its cost for one class of work and not for two others:

| Work class | Cycles | Durable output | Verdict |
|---|---|---|---|
| Reposoma canon | 01–11, 23–28 | `fanout-turns.md` 91 lines + three GUIDE seams (+83/−5) in `1360d61`; `presence-board.md` 120 lines in `0f48dce` (D) | **Earned.** Crossed witness + byte-pinned commit is the assurance canon needs; cycle 02 changed the design, 05/07/09/11 stopped a false PASS. |
| Runtime skill cards | 12–20, 29–36 | 71 lines across four cards (`fbd9f5e` +57/−6, `0c31011` +14) (D) | **Not earned.** 17 cycles, two STOPs for the head's own roster error, an attribution detour with zero source change, two packaging cycles, one proposal→REVISE→no-change loop. |
| Behavioral proof P0–P6, D1 | 29–36 + 10 probe sessions | reader P1/P2/P3 narrow PASS; producer P5 Astra PASS, P6 FAIL ×3, D1 partial (A) | **Not earned.** One uncoached sample per runtime cannot certify; the head's own receipts say so (RETURN 29 §6). Should have been re-scoped on 09-09. |

Majkee's observation — "the human is the bottleneck" — is correct and is now measured (§2):
**90 human turns into the head thread alone**, ~10.1 h of head-attached time spread over 7
calendar days. The mechanism makes the operator the transport *by design*
(`csharp-head-protocol.md:64–67`, "plan for a hub, not a mesh"). That is the right price for
canon and the wrong price for card edits, diagnostics and packaging. Cycle 23 shows why
subagents cannot substitute for fan-out branches (provenance breaks); the flattening lever is
therefore not "allow subagents in fan-out" but **stop making Tier-B work a fan-out branch at all**
(§3.2), plus a notifier/paster that removes the copy-paste without becoming an authority (§4).

Use this style for: reposoma canon, destructive or cross-host actions, anything needing a
witness the head cannot be. Do not use it for: skill cards under a pre-gaveled scope,
diagnostics, proposals, packaging, probe batches.

---

## 1. Process semantics — what was built, and where it went wrong

### 1.1 What the file plane actually is

Strip the vocabulary and the plane is an **append-only event log with one writer per event**:
`_bus/NN.<seat>.<kind>.md`, never edited, numbered by the status owner, with routing in the
frontmatter (`to:`, `return_to:`, `cycle`, `turn`). STATUS is the single mutable projection of
"now"; RUNBOOK is the fixed launcher. The chapter (`fanout-turns.md`, 92 lines) adds exactly the
missing coordination semantics — `turn:`, `delegated:` rows with a bounded vocabulary, one
`join_when:`, REVISE-in-turn, `deferred: turn NN`, contents-not-presence recovery, late
artifacts — and forbids scheduler, inbox, read-state, delivery promise and mutable receipts
(L84–85). Every promised semantic is present (D, law reader; `fanout-turns.md:14–17, 26–36,
40–55, 59–67, 71–80`). The three GUIDEs point and do not restate (D). The fold is correct law.

### 1.2 Formal mistakes (letter of the law)

| # | Mistake | Where | Status |
|---|---|---|---|
| F1 | Launcher YAML invalid: unquoted `@majkee` scalar | RUNBOOK L16, 09-04 → 09-11 | repaired 09-11 (closeout) |
| F2 | Three dead `res/csharp-head.md` pointers, known since VERDICT 11 (09-05) | RUNBOOK | repaired 09-11 |
| F3 | RETURN 29's own frontmatter fails YAML (colon in scalar) while diagnosing YAML failures | `29.atlas-ui.return.md` | corrected in cycle 30 |
| F4 | RETURN 37 echoes a trusted `turn:` contrary to `fanout-turns.md:40` | `37.oraculum-purpose-audit.return.md:3` | preserved as variance |
| F5 | Cycle 23 RETURN in the Codex role envelope, not the six BUS headings | `23.astrobley.return.md:13–209` | inoperative, preserved |
| F6 | Two POINTs under cycle 32 (trajectory + cartan); peer cycles 21/22/34 without VERDICT; nonstandard `review.md` kind | `_bus/21,22,32,34` | tolerated; numbering rule missing (§4.2) |
| F7 | Roster `participant_0` declares `gpt-5.6-sol`; head thread `turn_context` shows `gpt-6-astra` for 366 records vs 50 sol (D, label-only) | RUNBOOK L12 vs head thread | undisclosed in closing docs |
| F8 | `Co-Authored-By: Claude Opus 4.8` trailer vs self-reported carriage | `fbd9f5e` | accepted limitation (VERDICT 19) |
| F9 | Closing documents cite `3feba727…` as the durable gavel locator; that object is on **no branch** (`merge-base --is-ancestor` rc=1, `branch --contains` empty); its replay `1360d61` is HEAD's ancestor; tree diff between them is only `pulse.atlas.md` and `ptyra/*` (D) | `VERDICT.md:29`, `promotion-manifest.md:37` | **open — gc-prunable** |
| F10 | Eleventh raw keeper (this file) not in the manifest | `promotion-manifest.md` | owner to amend |

### 1.3 Semantic mistakes (spirit of the law)

| # | Mistake | Evidence | Avoidable? |
|---|---|---|---|
| S1 | **Gate understated the fold from day one.** "Reference/label-only" appears in no raw file; the T2 assessment sized the work as "four one-paragraph edits, no new file, no new kind" (`T2.assessment:202`); RETURN 02 (same day as the launcher rewrite) said the fold necessarily touches schema in four surfaces. The head kept the gate verbatim through four launcher amendments. | RUNBOOK L6–8, L25–28; RETURN 02 §4.3 | Yes — at the 09-05 roster correction |
| S2 | **STATUS became the head's memory, not the reader's snapshot.** 501 lines / 41,337 B before closeout (A: measured by RETURN 38, pinned by VERDICT 38); `holds:` 363 lines (A, RETURN 37). The head thread was compacted **11 times** (D). A head whose context is truncated eleven times has a private continuity need; it wrote it into the shared recovery surface. A cold-start card existed for that purpose (`_cold-start/archive/CS.runbook-upgrade.cartan.2026-09-06.md`, A). | status/GUIDE.md:59, 113, 124–125 | Yes — a scratch surface outside STATUS |
| S3 | **Heaviest instrument for the lightest work.** 71 lines of card change consumed 17 relayed cycles. Majkee approved the source scope in one sentence (POINT 16). | cycles 12–20, 29–36 | Yes — after VERDICT 11 |
| S4 | **One sample treated as a proof target.** After the first P6 FAIL (09-09) the information to re-scope was complete; 8 more cycles and a coached D1 ran before the ruling arrived 09-11. | RETURN 29 §6; VERDICTs 35/36 | Yes — on 09-09 |
| S5 | **"Missing T2 §§10–12" carried eight days, probably a numbering phantom.** The primary draft ends cleanly at §9 (`T2.assymetry-primary-draft:362`). The countersign's "§8" and "§12 as drafted" (`countersign:102,113`) match the *assessment's* implicit `##` count, where §§10–12 exist at `assessment:200–261` (I from D). Nobody checked the simple explanation. | VERDICT 11; `VERDICT.md:99–100` | Cheap check, never run |
| S6 | **No standing witness on the head's own surface.** Cycle 06 witnessed STATUS once; never again. The protocol recommends naming one at authoring. | `csharp-head-protocol.md:68–72` | Partly — recommendation, not law |
| S7 | Per-VERDICT re-hashing of immutable prior receipts, 35 times. | all head VERDICTs | Yes — bus GUIDE rule 3 already says "proportional" |

### 1.4 Not the head's fault (hindsight, or outside its reach)

- **Cycle 23 impostor.** A root Codex controller spawned `agent_type=astrobley`; the child wrote the RETURN, the root wrote a VERDICT and displaced STATUS (A, POINT 24 L36–40). The file plane documents ownership and cannot attest it; detection came from Astrobley's disclosure relayed by majkee, not from the mechanism. The head's recovery — preserve, pin, declare inoperative, re-run in the intended window — was exemplary.
- **Shared deploys** moved this arc's live cards before the head knew (09-05 ~23:09; 09-10 04:26/04:44, A: VERDICTs 20, 33). Operator-side; handled without a retroactive approval loop, correctly.
- **P6 itself.** A Claude session loading the card and not reading the chapter is not a head mistake. The loop after it was (S4).

### 1.5 Caveats on every number in this record

Counts are not cost. Tokens and turns are the **head thread only** — worker seats, the earlier
Oraculum seat, Atlas, Trajectory and ten probe sessions are excluded (U). The 501-line STATUS
is attested by two auditors and a pin, not by a git object (STATUS never had history, D). Model
strings are metadata labels. Behavioral findings are RETURN 38's direct inspection and the
head's verdicts (A); this record opened no transcript body. Home parity, zero-context recovery
and the cycle-23 root controller remain as both audits left them (U). Category tags in §2.3
are this reviewer's judgment.

---

## 2. Process effectiveness — tokens, turns, human loop, time

All figures in this section are direct observations from the head thread metadata unless marked.

### 2.1 The head thread in numbers

| Metric | Value | Scope note |
|---|---|---|
| Calendar span | 2026-09-04 15:16Z → 2026-09-11 15:18Z (7.0 days) | first → last human turn |
| Human turns | **90** (99 user records minus 9 injections) | head thread only |
| Assistant message records | 268 | one reply may span several records |
| Tool calls | 518 (514 custom + 4 function) | |
| Compactions | **11** | context truncated eleven times |
| Session-accounted tokens | total 8,757,383 · input 8,689,731 (cached 7,895,424) · **output 67,652** · reasoning 24,804 | TUI counter, last record |
| Gross thread throughput | 81,497,434 (input re-sent per response) | do not add to the above |
| Model labels | gpt-6-astra ×366, gpt-5.6-sol ×50 (`turn_context`) | labels, not attestation |

The head *generated* 67.7K tokens in seven days. The cost is context re-sent, ~90 % cached.

### 2.2 Time: attached vs elapsed

| Day (UTC) | Human turns | Active time (30-min merge) | Sessions | Tool calls | Compactions |
|---|---|---|---|---|---|
| 09-04 | 12 | 1:04 | 5 | 53 | 0 |
| 09-05 | 20 | 2:36 | 6 | 97 | 2 |
| 09-06 | 5 | 0:47 | 2 | 35 | 1 |
| 09-07 | 0 | — | — | — | — |
| 09-08 | 3 | 0:10 | 2 | 30 | 1 |
| 09-09 | 26 | 3:51 | 8 | 130 | 3 |
| 09-10 | 17 | 1:24 | 7 | 114 | 3 |
| 09-11 | 7 | 0:16 | 5 | 59 | 1 |
| **Total** | **90** | **≈10.1 h** | 34–35 | 518 | 11 |

- Median gap between turns *inside* an active session: **9.7 min** (mean 11.3) — the head's
  work plus the human's read-and-relay, per exchange.
- Largest idle gaps: 54.6 h (09-06 → 09-08), 15.0 h, 13.0 h, 10.2 h, 10.2 h.
- Duty cycle of the head: ~10 h attached of 168 h elapsed ≈ **6 %**. The "long" feeling is
  correct: seven days for ten hours of head time, the remainder waiting on the human or on
  other seats. The human's own total time is larger and unmeasured (U).
- Work per human turn: median 5.5 tool calls, 3 assistant records; **16 of 90 turns (18 %) were
  followed by zero tool calls** — pure conversational relays.

### 2.3 Cycles: what the receipts show

38 cycle numbers · 108 receipts · 12,203 lines in `_bus/` · 2,558 lines in `raw/` (D).
35 VERDICTs: 21 ACCEPT (one inoperative), 10 REVISE, 4 STOP (3 without RETURN) (D).
Human touch: every cycle needed at least one relay; ≥14 distinct rulings (G1–G7 sheet, gavel
date, roster, source scope, three commit hands, attribution, deploy confirmation, peer attach,
cycle-24 direct-execution confirmation, presence gavel, D1, audit roster, final blessing);
10 fresh probe sessions (all eight VERDICT-named prefixes exist on disk, D).

Reviewer's category tags (judgment):

| Tag | Cycles | Count |
|---|---|---|
| Substantive (law/skill/test produced or verified) | 01,03,05,07,08,09,11,15,16,18,20,21,22,24,25,26,28,29,32,33 | 20 |
| Independent audit | 02,04,06,10,27,37,38 | 7 |
| Corrective, necessary | 17 (stale origin), 19 (published-ancestor stop), 24 (cycle-23 recovery), 30 (evidence correction) | 4 |
| Ceremony / packaging | 12,13 (head's own roster error → two STOP receipts), 23 (inoperative), 31 (packaging), 34 (peer decline), 35→36 (proposal → no-change) | 7 |

Ratio proxy: ≈365 lines of durable output against ≈14,800 lines of process record — about
1:40. A proxy for weight, not a cost.

### 2.4 Controls that paid for themselves

- **02** — REVISE turned "GUIDEs stay maps" into schema-stubs-plus-chapter; without it the
  GUIDEs would have been wrong maps on day one.
- **05 / 07 / 09 / 11** — verification assertions that could not match what they claimed
  (multi-line `rg`, count/regex/negation traps; RETURN 11 lists four) caught before commit.
- **17** — stale origin before commit; home had pushed two commits.
- **19** — post-reboot recovery stopped an amend that would have rewritten a *published*
  ancestor (`0f52f56` on top of `fbd9f5e`).
- **29** — refuted "YAML fails in all three samples"; separated P6-skip from P5-misuse;
  prevented a wrong fix.
- **24** — the recovery pattern for a compromised receipt.

### 2.5 Where the brake actually is

| Brake | By design or by choice | Removable? |
|---|---|---|
| Waking a seat (open a session, paste a path) | design — the wake is the token-economy gate | The *paste* is; the *decision* is not (§4.3) |
| Gavels / rulings (≥14) | design | No |
| Fresh-session probes (10) | design | Batchable into one PAD sitting |
| Relaying Tier-B cycles (~17 cycles ≈ 40 head turns, I) | choice | Yes — two-tier (§3.2) |
| Pure conversational relays (16 turns) | choice | Yes — notifier (§4.3) |
| Head re-verification and packaging loops | choice | Yes — proportional VERDICT |

---

## 3. Recommendations

### 3.1 Direct feedback to Cartan (cSharp head)

**KEEP** — content-checked joins and the refusal to infer state from file presence (RETURN 06
oracle, VERDICT 24); the cycle-23 recovery pattern; VERDICT 19's stop before amending a
published ancestor; VERDICT 36's justified no-change; the closing STOP recorded as "limited
delivery, original gate unmet" and the honest FAIL map in `VERDICT.md`.

**STOP** — re-hashing immutable prior receipts in every VERDICT; writing STATUS for yourself
(use the cold-start card or a non-authoritative note in `raw/` for continuity across
compactions); opening a relayed cycle for a label (18/19), a repackaging (30/31) or a proposal
you expect to decline (35/36); carrying known launcher defects for a week (F1, F2).

**CHANGE — decision points with the information available then**

- *09-05, roster correction (RUNBOOK L25–28):* the launcher was being amended; correct the gate
  wording then, with RETURN 02 in hand. Avoidable.
- *09-05 after VERDICT 11:* three cards, 71 lines, scope approved in one sentence. One
  in-window authoring pass plus one crossed check was adequate. Nine cycles was choosing the
  heaviest instrument. Avoidable.
- *09-09, first P6 FAIL:* put "k uncoached repetitions, or accept FAIL and stop" to majkee that
  day. Avoidable; the ruling came 09-11 after eight more cycles.
- *Closeout:* cite the commit HEAD descends from (`1360d61`), not the dangling object.
  `git branch --contains` before writing a locator is a cheap habit.

### 3.2 Smallest adequate alternative — two-tier cSharp

Keep RUNBOOK / STATUS / BUS unchanged. Classify at POINT time.

- **Tier A — fan-out branch** (full session, operator relay, crossed witness, VERDICT):
  reposoma canon, destructive or cross-host actions, anything needing a witness the head cannot
  be. Exactly what cycles 01–11 and 23–28 did.
- **Tier B — in-window work** (head or a token-economy subagent authors; one note in `raw/`,
  or a single cycle only if a witness is genuinely needed): skill cards under a pre-gaveled
  scope, diagnostics, proposals, packaging, probe batches. No POINT/RETURN/VERDICT triple, no
  relay.
- **STATUS ≤ ~60 lines**; evidence pins live once, in the VERDICT that produced them;
  `recovery_probe:` says "read VERDICT NN".
- **VERDICT proportional** to what the cycle touched.
- **Return leg** by transcript-locator pickup (already approved, RUNBOOK L153–178).
- **Probes as one PAD sitting**: k runs per runtime, one record, scored on RETURN 29's six
  criteria — never one cycle per sample.

*Lost:* per-cycle decorrelated witness on Tier-B work (mitigated by immutability and a closing
audit); the operator sees Tier-B diffs once, in the record. *Decisions required before
adoption:* (1) majkee rules — one sentence in `csharp-head-protocol.md` or `fanout-turns.md` —
that Tier-B work is not a "delegated body of work" the head voids by touching
(`csharp-head-protocol.md:30–32` currently reads the other way); (2) whether a numeric STATUS
bound becomes canon (`status/GUIDE.md:59` has only "thirty seconds"). Neither is a mechanism.

### 3.3 Three improvements, ranked

1. **Preserve now, with the right locator.** One scoped commit of the bed — 112 untracked
   paths (STATUS, VERDICT, manifest, all 108 receipts, the transfer, this file) plus RUNBOOK
   (+210/−105 vs HEAD; last bed commit 2026-09-04, D) — excluding the peer's staged rename. In
   that commit, correct `VERDICT.md:29` and `promotion-manifest.md:37` to cite `1360d61`
   (optionally alongside `3feba727` marked "replayed, unreachable"), and add this file to the
   manifest. Cheapest, highest-value action here.
2. **Gavel the tier rule and the STATUS bound** — two sentences of canon, no tooling.
3. **One discriminating check instead of another audit.** The producer cards are asymmetric on
   the exact instruction P6 failed: `codex/skills/octopus/SKILL.md:19–25` says "Read these
   shared guides completely … then the res/ chapters its Manifest names, as the session's shape
   makes them applicable"; `claude/skills/runbook/SKILL.md:7–9, 41–43` routes by the Manifest
   but references the fan-out chapter only conditionally and embeds the field names (L34–38),
   so the card reads as self-complete. P5 (Codex) read the chapter every time; P6 (Claude)
   skipped it three times. Correlation, not cause — but it is the one wording difference nobody
   tested (29–36 tested parser/owner wording). Align the Claude read instruction to the Codex
   imperative form, run the *same* uncoached prompt k=3 per runtime in one PAD sitting. If
   Claude still skips, record a harness property, accept the limit, stop. If not, the 09-09
   "no card lever for the read" diagnosis was wrong.

Also cheap: settle S5 by reading the countersign's §-citations against
`T2.assessment:200–261`; and disclose F7 in the closing package.

---

## 4. Reply to majkee — BUS file shape, and relay automation

The question: one file per participant/thread (cSharp's also owning state; one for atlas-ui,
one for the auditor, one per probe; newest on top), **or** one file per topic/task group,
**or** a different kind — with relay automation in mind, because copy-paste needs a human.

### 4.1 Separate three things the directory currently fuses

`_bus/` is doing three jobs at once: it is the **store** of receipts, the **reading surface**
for the head and auditors, and the **relay signal** (a human notices a new file). The pain is in
the second and third jobs. Both proposed layouts try to fix them by changing the first — and
break what the first job is good at.

### 4.2 Store: keep one immutable file per artifact

| Property | `NN.<seat>.<kind>.md` (today) | per-participant file | per-topic file |
|---|---|---|---|
| Immutability of a receipt | yes — never edited | no — append mutates; "newest on top" *prepends*, so every hash pin breaks on every write | no |
| Writers per file | one | one (the participant) | several (head POINT, worker RETURN, witness VERDICT) → write races across two runtimes and merge conflicts on office↔home git sync |
| Provenance forensics (cycle 23) | filename declares intended writer; bytes pinnable | worse — any writer can append to any file | worse |
| Event detection by a tool | new file = new event; frontmatter already carries `to:` / `return_to:` / `cycle` / `turn` | must **diff** the file; needs read-state — exactly what `fanout-turns.md:84–85` forbids | must diff |
| Mixing STATE into the head's file | separate by law (STATUS mutable, BUS past tense) | collapses the one distinction the fold was built on | — |
| Reading a thread | many files (the real cost) | one file | one file, if topics did not interleave (cycle 32 shows they do) |

The current store is an append-only event log with single-writer files. That is the correct
*write* model and — decisive for the automation question — the **best possible substrate for a
relay tool**: an inotify watcher on `_bus/` gets each event and its target for free. Per-
participant or per-topic files would force any tool to diff and remember, i.e. to hold a
read-state the law refuses because a read-state is an authority the file plane cannot verify.

Two small repairs to the store, no new kind:

- **Cycle numbers are allocated by the status owner only.** Peer traffic (a second cSharp)
  arrives through `_mail/` (HANDSHAKE) or waits for an allocated number; the head opens a cycle
  to consume it. Kills the cycle-32 double-POINT and the verdict-less 21/22/34.
- **Optional `topic:` key** (one word) in POINT frontmatter so projections can group by task
  group without parsing prose. Optional; `turn:` already groups by decision.

Should the head's file "own STATE also"? No. STATUS is the one mutable snapshot; receipts are
past tense; a file others pin must not contain mutable state. Already law — keep it.

### 4.3 Views: per-participant and per-topic are projections, not layouts

Both of majkee's shapes are legitimate *ways to read* the log. Compute them: Trajectory's
`rb-open` already renders a bed with its gate-state and bus; give it a per-seat filter, a
per-`turn:`/`topic:` filter, and newest-first sort. If a static index is wanted, generate it
outside `_bus/` (a git-ignored `_view/`, or only in the TUI) so no mutable file lives among the
receipts. Zero canon change. This is the answer to "the head opens many files."

### 4.4 Transport: a notifier and a paster, not a router

What the human does per relay today: (1) notice a file landed — polling by eye; (2) copy the
absolute path; (3) paste it into the right pane; (4) press enter; and, separately, (5) gavel,
(6) open fresh probe sessions. Steps 1–4 are mechanizable **without** creating a scheduler,
inbox, read-state or delivery promise, provided the tool obeys four rules: it only reads the
plane; it writes no receipt; any "seen" marker is client-side display policy (the presence-board
precedent — age thresholds are client policy, never behavior); and the human's keypress remains
the wake. Then the POINT still says nothing about being read, and the RETURN is still the only
proof of work — the law is intact.

The minimal middle-software, three small commands in the `zsh/session/` scope (Trajectory's
lane, the natural home; not credited here as this arc's result):

- `bus-watch <bed>` — foreground inotify on `_bus/` and `STATUS.md`; prints one line per event:
  `NN.<seat>.<kind> landed · to: <seat> · return_to: <path>` to the TUI, tmux/zellij status, or a
  desktop notification. No daemon; a pane you keep open.
- `bus-next <bed>` — reads STATUS `next:` and `delegated:` rows; prints the one absolute path the
  operator is supposed to relay now and its target seat. If STATUS and disk disagree, it says
  so and prints nothing — the content-sensitive rule, not presence.
- `bus-send <pane>` — pastes that path into the named tmux/zellij pane (office has both;
  presence board tells you which pane/host a seat sits in). Enter only on an explicit flag.

Effect, from this arc's numbers: the 16 pure relays disappear; each of the remaining ~74
head-side relays becomes one keypress instead of four actions; combined with two-tier (§3.2)
roughly half the cycles never need a relay at all (I). What it does **not** remove: the ≥14
rulings, the fresh-session probes, and the scope decisions — the irreducible human loop.

Cross-host: a paste into a remote pane rides the existing `oc`/`op` SSH rail; `bus-watch` on
the other host needs the git sync to have carried the file, which is HANDSHAKE mail law today.
No blanket history sync, no remote daemon.

### 4.5 So: "different kind (yours)"

Not a new file kind. **Event log (as now) + computed views + an advisory notifier/paster.**
Event-sourcing, in plain files, with the human as the only actor that commits state. This is
the smallest thing that keeps every guarantee the fold bought and removes the toil majkee
actually felt.

---

## 5. What this record adds beyond RETURNs 37/38 — and remaining uncertainty

*Adds:* the head-thread measurement (90 turns, ~10.1 h attached, 11 compactions, 518 tool
calls, tokens with scope, 18 % pure relays); the dangling-commit locator defect (F9); the origin
of the gate understatement in the head's own authoring (S1); the compaction → STATUS-bloat
framing (S2); the producer-card read-instruction asymmetry as the untested lever (§3.3.3); the
§§10–12 phantom (S5); the roster/carriage mismatch (F7); the store/view/transport separation
and the relay design (§4). *Overturns:* nothing in 37/38's dispositions; RETURN 37's
"label/pointer-only" was already corrected by VERDICT 37 and the reposoma diff (bus +30/−5,
status +25, runbook +28) confirms the correction. *Repeats:* keep the mechanism; STATUS was
oversized; producer proof unmet; bed uncommitted; cost known only as counts.

*Uncertain:* total human time across all seats (U); whether the card asymmetry causes P6
(§3.3.3 is the test); home parity; zero-context recovery; cycle-23 root controller; all
behavioral claims are attributed to RETURN 38's inspection and the head's verdicts.

---

## Appendix — phase map (cycles · human turns by day · durable output)

| Phase | Cycles | Days (turns) | Durable output |
|---|---|---|---|
| Intention (T2 triad, research) | — | 09-02 → 09-04 | `raw/` nine files |
| Guide fold | 01–11 (turn 01: 05–07) | 09-04 (12), 09-05 (20) | reposoma `1360d61` (replay of `3feba727`), 8 paths |
| Runtime adaptation + deployment | 12–20 (turn 02) | 09-05, 09-06 (5) | ia-sync `fbd9f5e`, 3 cards; office deploy 09-05 ~23:09 |
| Peer seam / presence board | 21–28 | 09-06, 09-08 (3), 09-09 | reposoma `0f48dce`, 2 paths |
| Producer tests + diagnostics | 29–36 | 09-09 (26), 09-10 (17) | ia-sync `0c31011` (+14); P5/P6/D1 results; VERDICT 36 no-change |
| Audits | 37–38 (turn 03) | 09-11 (7) | RETURNs 37/38 and their VERDICTs |
| Limited closeout | — | 09-11 | VERDICT.md, promotion-manifest.md, transfer, STATUS 69 lines |
