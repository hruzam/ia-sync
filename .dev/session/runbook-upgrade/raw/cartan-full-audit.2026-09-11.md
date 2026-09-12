---
title: "Full audit of runbook-upgrade: effectiveness, process defects, and relay design"
date: "2026-09-11"
author: "Cartan — independent auditor, not cartan-csharp/status_owner"
session: "runbook-upgrade"
session_id: "01a0918e-9ab0-7053-88d8-d829f1fad954"
session_id_evidence: "CODEX_SESSION_ID and CODEX_THREAD_ID agree with auditor rollout session_meta"
transcript_path: "/home/hruzam/.codex/sessions/2026/09/11/rollout-2026-09-11T19-40-37-01a0918e-9ab0-7053-88d8-d829f1fad954.jsonl"
audited_session_id: "01a06cfd-b74e-7430-b041-992a9d9cea3c"
audited_transcript_path: "/home/hruzam/.codex/sessions/2026/09/04/rollout-2026-09-04T17-16-02-01a06cfd-b74e-7430-b041-992a9d9cea3c.jsonl"
host: "office — hruzam-120922"
repository_head: "7c6c3fb5e8211e3d68910e5d5450e8c8b9629c5b"
scope:
  - "Process semantics, formal and practical mistakes, and caveats"
  - "Effectiveness: recorded tokens, turns, operator involvement, flow, and time"
  - "Recommendations and the smallest adequate workflow"
  - "Participant/thread/topic BUS layouts and a bounded relay-automation proposal"
status: "Audit evidence and recommendations; not canon or implementation authorization"
authority: "Majkee requested this report in raw; existing limited-stop disposition remains unchanged"
usage_scope: "Original head rollout lines 1–5485 inclusive, through completed closeout; other sessions excluded"
usage_prefix_sha256: "fce241b4b8cf63e995f3568ea4ac423f7844f50757e57507c642e4ff31ec3712"
preservation: "New raw keeper; inclusion in the owner's preservation manifest/commit remains pending"
---

**Executive judgment: simplify.** Independent review, explicit ownership, and checked
recovery decisions earned their place here. The evidence does not justify repeating
the full coordination and certification workload for a comparable task. Useful shared
rules and skill changes were delivered, while the original producer gate remained
unmet. Limited delivery is the accurate outcome. This is a proportionality judgment,
not measured financial return or a demonstrated comparison with a cheaper workflow.

Use this style for consequential changes spanning independent owners, repositories,
or runtimes, especially when interrupted work must remain inspectable. For ordinary
patches, use one implementing seat and targeted independent review when warranted.
For exploratory behavioral tests, use a bounded evaluation followed by a disposition;
do not make each observation a new round of architectural approval.

This report consolidates the preceding chat audit and adds scoped usage measurements
and the requested BUS/relay comparison. Direct observation, historical reports,
recommendations, and unknowns remain separate. No model was launched for a new probe,
no transcript command was replayed, and private reasoning content was not inspected.

| Dimension | Evidence | Confidence and measurement gap |
|---|---|---|
| Outcome | Direct: fan-out and presence chapters match their cited commits; four inspected office source/live skill pairs match. Selected original outputs reproduce bounded P5 draft success, P6 semantic failure, and incomplete D1 recovery. | High for artifacts and sampled outputs. General reliability, home parity, and downstream value are unknown. |
| Assurance | Reviews identified incorrect recovery semantics, unsupported causal claims, invalid YAML, and changed Git preconditions. | High that these discrepancies were identified; moderate for their preventive value. No avoided-loss estimate. |
| Operator burden | 86 operator-message records in the scoped head trace, after excluding injected instruction/environment/skill messages. They include relays, repeated submissions, rulings, interruptions, and navigation requests. | High for record count, not 86 distinct decisions or unnecessary interventions. Human labor and interactions in other windows are unmeasured. |
| Flow and time | 81 unique head task starts, 78 completions, 3 recorded interruptions. Completed-turn durations sum to 6h18m06.292s. The observed segment spans nearly seven days. | High for recorded telemetry. Completed duration includes tool/approval waits where recorded; it is neither CPU time nor human labor. Calendar gaps are not classified as waste. |
| Recovery | Receipts document resumed recovery stopping a stale amendment. Current launcher and STATUS parse. A fresh replacement-head recovery trial was proposed but not demonstrated. | High for current syntax; historical recovery is attributed evidence. Safe operation without prior context remains unproved. |
| Complexity and token volume | 108 BUS files, 800,565 bytes, across numeric prefixes 01–38. Head-only ledger: 605 unique response records, 80,571,920 total tokens, including cached input. Current STATUS: 69 lines/4,702 bytes. | High for scoped counts. BUS volume includes presence work and audits. Tokens are repeated model input/output volume, not unique content, billing, or a waste estimate. |

The [closing disposition](/home/hruzam/ia-sync/.dev/session/runbook-upgrade/VERDICT.md:25)
correctly distinguishes delivered law, deployed bytes, observed behavior, and accepted
limits. Reposoma commit 3feba727 contains eight paths, including a 91-line fan-out
chapter and schema/authority changes; describing it as only three pointer edits would
understate the accepted scope. The presence contract at 0f48dce is a separate useful
output. Neighboring TUI/Termux implementations are not this arc's delivery.

The consequential findings, ranked:

1. **Behavioral verification was necessary; verification activity did not substitute
   for working behavior.** The latest P6 output parses, but uses incorrect delegation
   fields and proposes reopening missing or rejected work without resolving execution
   uncertainty. D1 reads the required material and parses its drafts, yet still makes
   unsafe inferences from file absence/presence. P5's bounded success is useful evidence,
   not a live crash/restart demonstration. These observations justify behavior checks
   alongside deployment checks; they identify neither a model-level cause nor a proven
   wording cure. Cartan should have presented the stop/continue choice earlier, once
   deployed bytes and unresolved behavior were established. This does not make the later
   operator-authorized diagnostics illegitimate.
   [Invocation map](/home/hruzam/ia-sync/.dev/session/runbook-upgrade/VERDICT.md:39)

2. **The marginal value of verification varied substantially.** Cycle 29 materially
   corrected evidence: not every sample failed YAML; the supposed causal guide skeleton
   parsed; blanket folded-scalar advice could damage collections or command newlines.
   Keep that scrutiny. Cycle 30 also had a real issue: the proposed cut lacked literal
   source anchors. Calling all of 30/31 formatting ceremony would be unfair. The avoidable
   preparation error was not requesting a checked unified diff when requesting an exact
   proposal. Cycle 31 then made the right proportional decision: accept an independently
   checked patch despite remaining command-reporting defects.
   [29](/home/hruzam/ia-sync/.dev/session/runbook-upgrade/_bus/29.cartan-csharp.verdict.md:15),
   [31](/home/hruzam/ia-sync/.dev/session/runbook-upgrade/_bus/31.cartan-csharp.verdict.md:46)

   Attribution was a weaker branch: cycle 18 established the source result but withheld
   acceptance over an unverifiable model trailer, leading toward amendment. A neutral
   attribution policy settled beforehand would have avoided that branch. Once publication
   changed the preconditions, stopping the amendment was a valuable control. The lesson
   is to avoid creating an unprovable acceptance condition, not to ignore an existing one.
   [18](/home/hruzam/ia-sync/.dev/session/runbook-upgrade/_bus/18.cartan-csharp.verdict.md:80),
   [19](/home/hruzam/ia-sync/.dev/session/runbook-upgrade/_bus/19.cartan-csharp.verdict.md:40)

3. **Cartan managed evidence more consistently than operator flow.** Computer moves and
   network failures explain some re-entry burden; they are not head-created delays.
   Nevertheless, the operator repeatedly requested recaps, precise prompts, or the next
   relay. On September 9 the operator asked whether independent work could run, and Cartan
   then offered an already-owed display check. This establishes a scheduling opportunity,
   not a particular time saving. The mistaken split of Atlas UI and harness-builder into
   two participants also required an operator roster correction and two STOP receipts.
   [Head exchange, line 3594](/home/hruzam/.codex/sessions/2026/09/04/rollout-2026-09-04T17-16-02-01a06cfd-b74e-7430-b041-992a9d9cea3c.jsonl:3594),
   [roster correction](/home/hruzam/ia-sync/.dev/session/runbook-upgrade/_bus/12.cartan-csharp.verdict.md:17)

   The human was performing both judgment and transport. Canon rulings, changed-scope
   decisions, and stop/continue choices served a purpose. Repeatedly carrying a finished
   result or locating the proper window need not require the same level of human attention.
   Shared deployment confusion shows that a hold in one task does not coordinate another
   authorized owner's full deploy. It does not establish that the other owner acted
   without permission.

4. **File integrity helped recovery, but ownership remained socially enforced.**
   Cycle 23's plausible filename and envelope carried an inoperative head verdict.
   The execution-chain account came through operator-relayed disclosure. Cartan correctly
   preserved the evidence, rejected the purported advancement, and obtained a separately
   accountable return. More hashes would not establish the writer.
   [Corrective POINT 24](/home/hruzam/ia-sync/.dev/session/runbook-upgrade/_bus/24.cartan-csharp.point.md:34)

   Closeout has substantially improved the historical defects. I verified repaired
   launcher YAML and references, the shorter STATUS, and nine inherited raw keepers
   matching the pinned Git commit. The new transfer and BUS/closeout preservation remain
   pending, as disclosed. The manifest protects evidence without demanding another
   permanent archive. The present snapshot is much better; its 69 lines still do not
   establish the guide's thirty-second usability aspiration.
   [STATUS](/home/hruzam/ia-sync/.dev/session/runbook-upgrade/STATUS.md:30),
   [preservation plan](/home/hruzam/ia-sync/.dev/session/runbook-upgrade/promotion-manifest.md:44)

**To Cartan — KEEP:** challenge substantive claims against artifacts, distinguish
deployed bytes from behavior, protect concurrent work, and withdraw actions when their
preconditions change. Cycles 19, 29, and 31 show good judgment. Keep the honest limited
stop and the refusal to rewrite cycle 23 into an apparent success.

**STOP:** making historical reporting perfection a recurring advancement condition
after the relevant artifact is independently established. Stop treating uncertain model
attribution as something more procedural effort can necessarily resolve. Stop carrying
closed assurance narratives in current state.

**CHANGE:** request the reviewable artifact earlier, make each relay explicit about who
acts next and what is already authorized, surface independently runnable work, and put
the stop/continue choice before the operator when the evidence does not satisfy the gate.
Apply launcher checks to your own deliverable as well as producer samples.

**Majkee's BUS question: keep immutable receipts; improve the reading and delivery
interface over them.** A participant, a runtime thread, and a task are different
coordinates. A logical participant can move to a replacement thread; one thread can
serve several tasks; one task can involve several participants. File layout should not
collapse those distinctions.

| Layout | What it helps | What it costs | Judgment here |
|---|---|---|---|
| One newest-first file per participant or thread | Convenient personal history; per-participant writing can retain a clear writer. | It accumulates unrelated tasks, disperses each task's acceptance chain, and changes whole-file hashes on each prepend. Per-thread files also fragment continuity after replacement. Stable entry IDs and framing would be needed. | Useful as a generated view; no demonstrated benefit from replacing the evidence format with it. |
| One file per topic/task group | Author, review, correction, and decision can be read together. | Multiple writers need coordination, or one assembler becomes a bottleneck. Broad topics can become another history-sized STATUS. An automated reader still needs explicit entry identity, bindings, and completion rules. | Better grouping for reading; weak reason for a shared writable source file. |
| Existing immutable receipts with task/cycle and participant filters | Keeps exact handoff identity and independent ownership while offering both views. | File count remains; the viewer/relay needs bounded parsing and a session-to-endpoint mapping. | Smallest adequate choice for the observed problems. |

Show newest cycles first for orientation, but show POINT → RETURN → VERDICT in logical
order within each cycle. A late correction belongs to its explicit binding, not whichever
file was most recently modified. Participant filters should follow the logical seat;
runtime thread IDs belong in provenance and endpoint bindings. STATUS remains the
head-owned current state; do not create an additional STATE inside a cSharp history file.
Ordinary output-only probe observations can live in their evidence artifact; a probe does
not automatically need its own standing BUS participant or transcript copy.

Part of this interface already exists. The inspected
[runbook browser source](/home/hruzam/ia-sync/zsh/session/runbook.py:623) groups receipts
by cycle newest-first and deliberately reports file presence without declaring acceptance.
It also has [path/content copying](/home/hruzam/ia-sync/zsh/session/runbook.py:743).
This is source inspection, not a new runtime or deployment verification. Extend the
owned tool if the operator chooses; do not credit these peer features to runbook-upgrade.

For the proposed middleware, automate carriage under explicit authority:

- The operator binds a logical seat to an exact host, workspace, and session endpoint.
  The head issues an authorized POINT; the relay checks its recipient and binding before
  delivery. A thread ID or filename alone does not grant that session head authority.
- Send the exact POINT path when the recipient can resolve the same artifact. Cross-host
  operation needs verified artifact availability and an explicit path mapping first.
  Do not reconstruct the brief by summarizing chat or paste it into an unidentified pane.
- Bring completion/RETURN locators back to the designated verifier. Transport submission,
  receipt availability, verified acceptance, and STATUS advancement remain distinct.
  The relay does not author acceptance or silently acquire STATUS ownership.
- Keep any retry/delivery bookkeeping machine-local and subordinate to the session.
  If delivery may have happened before a timeout, show the uncertainty and reconcile it
  before resending. A deduplication key can help, but does not itself prove exactly-once
  execution across a crash.

Start with an operator-triggered delivery-and-collection action, removing manual copying.
After that bounded mechanism is demonstrated, the operator may authorize automatic
forwarding of already-issued, in-scope POINTs and completion locators. Keep human decisions
at new scope, canon, meaningful risk, unresolved identity, and final disposition. Copying
text should not be the mechanism that forces those decisions.

This is a proposed transport boundary, not a claim that current vendor APIs already
provide it. The BUS guide permits a project mechanism to point at a filename, while the
cSharp chapter currently describes operator-carried transport. Automatic waking/steering
therefore needs an explicit local trial ruling and, for general adoption, reconciliation
of that canon. This report does not authorize a daemon, unattended session launch, or
cross-host send.
 [BUS contract](/home/hruzam/reposoma/raw.guides/bus/GUIDE.md:47),
 [cSharp transport](/home/hruzam/reposoma/raw.guides/runbook/res/csharp-head-protocol.md:62)

**The smallest adequate workflow for this task** is one controller, one builder with
explicitly approved cross-surface write scope, and one independent reviewer. The builder
supplies the concrete diff and checks; the reviewer examines consequential semantics and
the actual diff; the operator makes the required canon/deployment decisions; the controller
checks integration and current preconditions. Behavioral evaluation has a bounded scope
and an explicit disposition. Keep RUNBOOK, compact STATUS, and immutable receipts.

This gives up some specialization and repeated independent reconstruction. It retains
author/reviewer separation, durable evidence, repository protection, and human authority.
Consolidating builder scope requires the operator's decision. Shorter state and proportionate
verification already fit existing law. A new transport permission does not waive source,
commit, deployment, or verification boundaries.

I recommend only **three improvements**:

1. **Demand the checked diff at the first exact-change proposal.** Carry verified evidence
   by reference and reopen changed or unresolved claims. Cycle 31 is the useful precedent.
2. **Improve the existing relay interface before changing BUS storage.** Offer cycle/topic
   and participant views, then one bounded delivery/collection action. The smallest
   discriminating transport check is one approved read-only handoff whose completion
   notification is interrupted: verify correct endpoint binding, no duplicate execution,
   recovery of the actual RETURN, and the operator actions required. No broad audit is
   needed to decide whether that prototype earns further work.
3. **Exercise the missing recovery promise when next needed.** Give a fresh reader a
   frozen folder with stale STATUS, a landed terminal verdict, and a branch whose execution
   state is unknown. Check the proposed next action and whether it avoids duplicate
   dispatch; record operator clarifications. This is a different seam from transport
   recovery and does not establish a general reliability rate.

Before adopting the middleware, majkee needs to decide the receiving-session binding,
the bounded automatic-forwarding authority, and the owner of the relay's local lifecycle.
Before changing storage or global wake/transport law, a canon ruling is needed. The
recommended first trial can preserve the current BUS format and every existing acceptance
boundary. These are decisions for a later concrete proposal, not permission questions
blocking this report.

**What this adds beyond 37/38:** direct operator-thread evidence about navigation and
scheduling, checked post-audit repairs, current record inventory, and a deduplicated
head-only usage/duration ledger. It also distinguishes necessary patch precision from
avoidable reporting churn and answers the storage/transport question using the existing
browser source. Much of the main judgment confirms 37/38. Those audits were read early;
this is not a blind replication.

The earlier claim that token totals were simply unknown is now narrowed: this head's
recorded segment is measurable, while whole-team cost and a causal allocation to this
style remain unknown. General reliability, fresh-head recovery, historical actor
provenance, home parity, human labor, and comparative workflow performance remain open.
Another broad review would add little without new operational evidence.

---

**Supporting measurement detail.** Units and boundaries matter more than apparent precision.

The usage corpus is the original head rollout named in frontmatter, lines 1–5485 inclusive.
It begins at 2026-09-04 15:16:02.375 UTC with recovery into work already in progress and
ends with completed closeout at 2026-09-11 14:13:45.925 UTC. Thus it does not measure the
earlier work preceding that recovery. It excludes subsequent preservation discussion,
the request to commission this audit, this auditor's own usage, and all separate
builder/reviewer/probe runtime usage. Peer results pasted into the head count only as
input processed by the head, not as the peers' own execution usage.

| Recorded field | Tokens |
|---|---:|
| input_tokens | 79,912,877 |
| cached_input_tokens — included within input | 74,172,288 |
| output_tokens | 659,043 |
| reasoning_output_tokens — included within output | 210,981 |
| total_tokens = input + output | 80,571,920 |

Method: select token_usage_record entries in that prefix; key by (thread_id, response_id);
sum each unique record's usage fields once. There are 605 records and 605 unique keys,
with no duplicate conflicts. Every record's input plus output equals total; cached input
is within input and reasoning output within output. Every cumulative thread increment
matches that record's usage, and the summed fields equal the final thread_token_usage
at line 5483. Cumulative turn/thread fields were not added to those per-response amounts.
Only numeric reasoning-usage metadata was read; reasoning text was excluded.

The separate event_msg/token_count stream decreases five times, at line pairs
1581→1596, 2066→2082, 3252→3265, 3339→3351, and 4956→4973. Its final snapshot at line 5484
is 7,831,869 total tokens, not the thread ledger's 80,571,920. I do not infer the exact
runtime cause of those differences, sum those snapshots, or add them to the response
ledger. This discrepancy is why the report names its selected telemetry surface.
The ledger supports recorded volume, not independently reconciled provider billing.
Repeated/cached input is not unique source material and is not automatically waste.

Turns are runtime task IDs, not BUS cycles, logical coordination turns, or human decisions.
The prefix contains 81 unique task_started IDs, 78 unique task_complete IDs, and three
uncompleted IDs corresponding to interruption events. Summing duration_ms once per
completed task gives 22,686,292 ms; their recorded intervals do not overlap. The three
interrupted-task durations are excluded. These intervals include whatever tool, permission,
or other waits the runtime counted. Nearly seven days of elapsed span cannot be converted
into idle labor or attributed to the head.

The 86 operator-message records count response_item messages with role=user once, excluding
the three AGENTS instruction injections, six environment injections, and two skill
injections. They are not 86 independent relays: examples include repeated submissions
around interruptions, short approvals, result locators, substantive decisions, and thanks.
No attempt was made to price them or infer the operator's typing/reading time.

BUS counts are a current inventory of this bed's _bus files, not a usage ledger:

| Numeric prefix band | Included phase | Files | Bytes |
|---|---|---:|---:|
| 01–11 | Documentation fold and its checks | 33 | 230,864 |
| 12–20 | Roster/runtime/attribution/deployment coordination | 24 | 156,566 |
| 21–28 | Peer/presence work, including inoperative cycle 23 | 22 | 172,158 |
| 29–36 | Producer correction and diagnostic work, including a peer POINT | 23 | 162,423 |
| 37–38 | Purpose-fit audit POINTs, RETURNs, and head VERDICTs | 6 | 78,554 |
| Total | Same 108 files counted once | 108 | 800,565 |

These are explicit filename bands, not exact labor allocation. They include a nonstandard
peer review filename and multiple writers within some numeric prefixes. Neither 38 prefixes
nor the number of verdicts is a success denominator.

The historical 501-line STATUS is supported by the independently recorded observations
and pin in [VERDICT 38](/home/hruzam/ia-sync/.dev/session/runbook-upgrade/_bus/38.cartan-csharp.verdict.md:66);
the current 69-line version was measured directly. Current source/live equality and the
selected P5/P6/D1 original-output parsing were rechecked in this auditor session. Other
historical verification commands remain attributed reports, not this auditor's reruns.
The old full T2 draft referenced by the inherited critique remains unavailable.

This report adds a raw keeper beyond the previously ten-keeper closeout. A concurrent
oraculum-full-audit.2026-09-11.md also appeared during verification; it was not read or
modified. The original head must refresh the actual keeper inventory before a future
preservation claim can cover all raw files. This auditor has not changed that
owner-controlled manifest, STATUS, canon, source code, Git index, or deployed state.
Transcript files remain host-local; this report records locators and bounded measurements
rather than copying their histories.
