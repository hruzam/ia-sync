# RUNBOOK: germline-A5-reader-navigation

```yaml
goal: >-
  Run a bounded navigation experiment that measures whether familiar routing
  structure helps readers recover distributed facts and act on current evidence.
gate: >-
  Majkee accepts an evidence-backed disposition of the four-subject navigation
  experiment, including fixture equivalence, retrieval transcripts, semantic
  scores, harness limits and a concrete return to A3's reading-design question.
participant_1: [cartan, {brand: codex, model: operator-selected, recommended_grade: Terra, effort: operator-selected}, {role: Medusa working head and sole STATUS owner}]
participant_2: [majkee, {brand: human}, {role: activation and final disposition}]
participant_3: [reader-01, {brand: codex, model: gpt-6.1-terra, effort: low}, {role: fresh structured-entry subject}]
participant_4: [reader-02, {brand: codex, model: gpt-6-luna, effort: low}, {role: fresh prose-entry subject}]
participant_5: [reader-03, {brand: codex, model: gpt-6.1-terra, effort: low}, {role: fresh prose-entry subject}]
participant_6: [reader-04, {brand: codex, model: gpt-6-luna, effort: low}, {role: fresh structured-entry subject}]
status_owner: cartan
observations_read: none exist
```

Prepared by Oraculum on 2026-10-30 at Majkee's request for a Cartan/Medusa handoff.
Preparation does not start the executor. Majkee's explicit launch of prompt-0
activates the bounded work below, including its four subject attempts. The initial
STATUS is prepared for Cartan's logical seat; no Cartan execution is claimed.

## Where this bed belongs

The serial identifiers identify work; they do not prescribe a completion order.

| Bed | Role | Relationship |
|---|---|---|
| A3 guide-to-controller | Design and integration | Consumes relevant evidence; owns its own review/acceptance |
| A4 reader-shapes | Completed small supplied-fact pilot, acceptance pending | Baseline: four 12/12 responses; no discriminating layout signal; loader confound |
| A5 reader-navigation | This bounded experiment | Tests discovery of distributed facts; returns a result pointer to A3 |

```text
A4 supplied-fact evidence ──→ A5 navigation question
          └─────────────────────────┐
A5 navigation evidence ─────────────┴──→ A3 design decisions
```

A5 can run before A3 finishes its design. It does not close A4, advance A3's
checkboxes or acquire either session's pen. No further numbered bed is pre-created.

## prompt-0 — Cartan in Medusa posture

```text
$medusa
Work in /home/hruzam/ia-sync as Cartan, logical seat cartan, using:
/home/hruzam/ia-sync/.dev/session/germline-A5-reader-navigation/RUNBOOK.md
and /home/hruzam/ia-sync/.dev/session/germline-A5-reader-navigation/STATUS.md.
Read /home/hruzam/.agents/skills/medusa/SKILL.md and the complete shared STATUS guide.
Resolve actual host, instructions, runtime identity and concurrent work. Do not inherit
Oraculum's profile merely because Oraculum prepared these documents. If the runtime
identity conflicts with Cartan/Medusa, return the exact mismatch before subject calls.
Read A4's RESULT and DEVIATIONS as bounded evidence, then prepare the fixture and
freeze described below. Write only in this A5 bed and its minimal pulse route.
After the required preflight and freeze pass, run the four specified fresh subjects
once, using message-mediated document requests and the exact recorded budget.
Preserve requests, deliveries and replies before sending another turn. Score against
the frozen rubric, write the continuity receipt and return evidence for A3.
Do not run further subjects, change shared runtime configuration, deploy, publish,
prune or edit other session state. Stop with evidence at a genuine scope/authority
boundary. Routine fixture drafting and verification do not need per-step approval.
```

Medusa is a working posture, not a profile or separate owner. Follow the skill's
MANNED/UNMANNED rule; unclear presence means UNMANNED. If consequential curvature
requires a new design, return it through Majkee to Cartan/Octopus with A3's owner
included as appropriate. Do not spawn an adviser to manufacture an architectural GO.

## The experimental question

Does a familiar structured routing entrance help locate and apply distributed
evidence compared with equivalent prose? This is a controlled message-mediated
reading experiment. It does not test autonomous filesystem search or prove a
training-data mechanism. Every result must preserve that boundary.

Only the entrance presentation varies. The underlying document bodies, filenames,
facts, authority, task questions, document budget and serving responses are identical.
Structured entrance: ordinary component/source table, with explicit relationship
words. Prose entrance: the same clauses and order in paragraphs. Both give the same
routes and meaning; do not handicap the baseline with obscure invented terms.

## Preflight and ownership

1. Read A4's exact deviation. Resolve the selected main and subject routes from
   available local configuration and native facilities. Record what is observed,
   requested and unknown; do not assert effective model/effort from a request alone.
2. Use the same neutral subject role and base instructions for both arms. Request
   no parent conversation history; do not promise that this strips developer-level
   instructions. Avoid unintended Oraculum loaders. Do not edit global profiles to
   obtain a cleaner experiment. If neutral entry is unavailable, return the limitation
   before consuming subjects, with the smallest viable alternative for operator choice.
3. Required runtime entry reads remain permitted and must be disclosed. Fixture
   retrieval then occurs only through the head's document-serving messages. This is
   an instruction boundary, not a claimed technical sandbox. Record any observed
   outside reads or missing trace evidence; never conceal them as zero cost.
4. Use only existing native facilities. A small local transcript/check utility may
   live under this bed if useful. Do not build a new agent framework, database or
   transport. No full rollout/authentication/history scan to obtain telemetry.
5. The working head owns fixture authoring, integration and scoring. Subjects write
   no files and receive no answer key or peer replies. No extra model calls for
   helpers/reviewers are included in this release. If a sound result needs them,
   prepare the bounded reason and return it.

## Fixture to author and freeze before dispatch

Create two entry documents plus seven shared synthetic documents under `raw/fixture/`.
These are invented examples with no live operation behind them. Use stable source
IDs and revisions; preserve all assertions in a fact ledger. A file's existence in
the fixture is not evidence that a real operation occurred.

| Synthetic document | Required content |
|---|---|
| `components/plan.md` | draft-plan requires current inventory and accepted constraints; produces a proposal; cannot execute it |
| `state/inputs.md` | current inventory available; accepted constraints missing |
| `rules/review.md` | operative revision 4 requires two distinct reviewers |
| `contracts/copy.md` | recovery checks operation receipt and current target; retry can overwrite later changes and needs its own authority |
| `operations/copy-17.md` | durable receipt records completion at 10:05 with output digest A0; reporting connection was lost at 10:06 |
| `state/target.md` | current target digest B1; a subsequent edit recorded at 10:10; preserve the edit while reconciling desired state |
| `archive/notes.md` | explicitly historical review-revision-3 notes, plus unrelated material; no current authority |

Each entrance points to these same documents with the same factual role descriptions.
Do not expose the missing prerequisite, required review count or copy outcome in the
entrance. Route descriptions help selection; the body supplies decisive evidence.

The common task states that a proposed plan is needed, one reviewer has approved,
an inherited revision-3 summary says that suffices, and the copy's report was lost.
Ask for the next valid action for each situation and citations to the necessary
evidence. Do not give the reader all decisive source IDs in the question.

Freeze the fact ledger, both entrance bodies, shared documents, exact task/serving
messages, assignment table and scoring rubric in `raw/FREEZE.json` before dispatch.
Hash every contributing input. Check equal facts and order across entry variants;
measure presentation-size differences. Fixture wording may be refined before freeze
to eliminate ambiguity, while preserving the specified facts and comparison.

## Twelve semantic scoring items

The head expands these into a scored rubric before freeze, without adding hidden
requirements. Each earns 0 or 1 for meaning, not preferred wording.

| Case | Four required distinctions/actions |
|---|---|
| Plan | Both inputs recognized; accepted constraints identified as missing; contract located/cited; draft remains a proposal with no execution authority |
| Review | Gate unsatisfied; revision 4/two distinct reviewers governs; revision-3 summary is stale for this rule; one further distinct approval needed |
| Copy | Receipt establishes historical completion despite lost report; current target changed after that completion; preserve later changes and withhold blind retry; cite both receipt/current-state evidence and return desired-state reconciliation as unresolved |

Record source retrieval correctness, unnecessary retrievals, budget exhaustion,
unsupported claims and authority mistakes separately from the twelve-item score.
Do not invent extra credit or retroactive wording requirements. A correct guess
without the required source evidence does not earn an evidence-dependent item.

## Subject route and budget

Use four fresh subjects: Terra structured, Luna prose, Terra prose, Luna structured,
in that order; at most two concurrent. Requested identifiers are in the roster.
Use opaque subject names in their prompts so condition labels do not prime them.
No crossover, correction feedback, subject substitution or repeated exposure.

Each receives the common task and its entrance. It can reply:

```text
READ <one or two listed relative document paths>
```

or submit its final answer. The head serves the exact frozen bodies for valid paths,
with path and revision headers. Unknown/out-of-scope requests receive the same
prewritten unavailable response in both arms; no coaching or extra hint. A request
for a duplicate document is served verbatim and still counts toward the allowance.

Per subject: at most **four request rounds, six document deliveries and one final
answer**. At most two documents per request. Thus at most five subject response
turns and twenty across the four subjects. Required runtime initialization is
disclosed separately; it does not authorize reading private fixture keys.
After the limit, use the frozen final-answer request; partial knowledge is acceptable.
No additional model spend is authorized by an incomplete answer or failed dispatch.

Record every attempt before sending. If a returned handle cannot be resumed, retain
the partial result and report the route failure; do not silently respawn a substitute.
Freshness, model/effort requests and delivered bytes are separate evidence categories.

## Evidence and recovery

The local bus records one POINT/RETURN/VERDICT cycle per subject, following
`/home/hruzam/reposoma/raw.guides/bus/GUIDE.md`. Within its cycle, the head preserves
exact multi-turn messages in `raw/runs/<subject>/transcript.jsonl`; do not create a
new bus file for every step. Parent landing of native replies is explicitly attributed.
Subjects do not read the bus or another subject's transcript.

Before each model send, STATUS names the in-flight subject/round and possible effect.
Record the requested handle, message hash and budget admission in `raw/DISPATCH.json`.
After the return, preserve it and account for remaining budget before continuing.
If interruption leaves admission uncertain, inspect actual native state and the
recorded exchange. No evidence of completion is not permission for a duplicate send.

Required outputs, created when their work occurs:

- `raw/PREFLIGHT.md`: entry/harness evidence and limitations.
- `raw/FREEZE.json`: input hashes and preregistered comparison.
- `raw/DISPATCH.json`, per-subject transcripts and bus returns/verdicts.
- `raw/SCORES.json`: each item with cited answer/source support; disagreements visible.
- `raw/CONTINUITY-RECEIPT.md`: actual inherited understanding, expansion, friction,
  cost evidence, repairs and custody; use A3's candidate template proportionately.
- `RESULT.md`: descriptive outcomes, comparison limits, applicability to A3 and
  concrete next discriminator. Do not equate four subjects with a robust model ranking.

Measure served document counts/bytes, request rounds, unsupported answers and correction
burden. Record actual telemetry only when exposed without broad historical inspection.
Unknown token use, total cost and internal reads stay unknown. Serving a document
proves delivery through this mechanism, not comprehension or absence of outside access.

## Return and preservation

Return the result and exact paths to Majkee for A3 S02/S07/S08. The A3 head decides
how it affects the design; Cartan does not rewrite A3's STATUS or checkboxes here.
If the trial is compromised, preserve the attempted result and its limits; a negative
or incomplete outcome can still support an honest disposition of this gate.

Independent acceptance and any shared-guide/skill promotion belong to the operator's
later decision. Before pruning, preserve surviving findings and observations under
the shared RUNBOOK law. Preparing a result does not itself close or delete the bed.

## Bounded references

- `/home/hruzam/.agents/skills/medusa/SKILL.md`
- `/home/hruzam/reposoma/raw.guides/status/GUIDE.md`
- `/home/hruzam/reposoma/raw.guides/runbook/GUIDE.md`
- `/home/hruzam/ia-sync/.dev/session/germline-A4-reader-shapes/RESULT.md`
- `/home/hruzam/ia-sync/.dev/session/germline-A4-reader-shapes/raw/DEVIATIONS.md`
- `/home/hruzam/ia-sync/.dev/session/germline-A3-guide-to-controller/raw/reader-design/README.md`
- `/home/hruzam/ia-sync/.dev/session/germline-A3-guide-to-controller/raw/reader-design/continuity-receipt.template.md`

Read only the relevant depth. This handoff supplies the experiment; recovering the
whole earlier conversation is not a prerequisite.
