# Jev test and settings task card

Cartan · 2026-11-05. Working task breakdown, not a replacement RUNBOOK or STATUS.
STATUS owns the selected next action. No account access or paid call is released by this card.

## Input and output from Bash

The machine-readable task card is the existing `jev.case/v1` JSON packet. A human or agent
authors it; Bash passes the file as data. There is no natural-language task compiler and no
shell code inside the card. `case.example.json` is a labelled synthetic brief-review example.
Copy and edit its target, evidence, missingness, questions, predicates, options and rubrics.
Use a new protocol/rubric version when their meaning changes. Supply actual evidence text;
a path alone does not cause Jev to read that file.

From the repository root:

```bash
bash .dev/session/jev-01-codex-pilot/tasks/prepare-task.sh \
  .dev/session/jev-01-codex-pilot/tasks/case.example.json hlm
```

The helper prints the path of a private `/tmp/jev-task-*/result.json`. It validates the
packet, opens an isolated offline engagement, rebinds only session/channel, freezes input,
and exports settings, request reference and recorded history. The original card is unchanged.
No model/budget/key is configured; no inference or judgment is fabricated. Preserve results
elsewhere when needed: temporary storage is not durable custody. The result schema is a
local helper artifact, not a new engine/API contract. The helper calls current source.
The optional second argument labels the requester `hlm` or `agent`; omission means unknown.
CLI session identity remains separate and follows the engine's origin resolution. A child
runtime with conflicting Codex identifiers must use the direct CLI with an explicit origin;
this small helper does not guess which conflicting value is authoritative.

For an already deliberately configured engagement, use the actual installed engine from Bash:

```bash
# Set these to existing selected values; do not paste illustrative identifiers unchanged.
python3 -B ~/.config/zsh/jev/jev.py --root "$JEV_ROOT" \
  --session "$JEV_SESSION" --channel main settings > settings.json
python3 -B ~/.config/zsh/jev/jev.py --root "$JEV_ROOT" \
  --session "$JEV_SESSION" --channel main prepare case.json > prepared.json
```

That card must contain the exact selected session/channel. The implemented channel is `main`
only; the selector is explicit but additional channel names are not implemented. `show` and
`ref` export saved results. Local history export is not a provider billing download.
Real `send REQUEST --credential-file PATH` remains a separate operator-terminal operation,
with frozen model/bound/allowance and fresh payload confirmation. It is absent from the helper.

## Ordered tasks and acceptance

| ID | Work | Completion evidence |
|---|---|---|
| T00 | Record CLI session and hlm/agent/unknown requester | CLI-PROVENANCE.md; legacy replay and original response identity survive cross-client references/reuse; controller null |
| T01 | Exercise card → prepare → local result from Bash; test settings/binding failures | Synthetic helper run, unchanged input hash, stored exact bound input, no credentials/HTTP; invalid input refuses |
| T02 | Formalize a small real U01/U02 evaluation set | Versioned predicates and evidence; independent labels; ambiguous/unsupported/contradictory cases; deterministic comparator; train/tune and holdout groups separated |
| T03 | Make settings and spending operationally inspectable | Read-only provider key-status snapshot/export, expiry/reset and remaining balance, timestamps and source labels; unknown/stale/error distinct; local ledger untouched |
| T04 | Resolve settings maintenance | Explicit proposed policy-revision design with preserved cumulative spend/reservations and frozen earlier requests; no refill by changing channel/bed; offline tests before release |
| T05 | Configure and test one live pilot | Operator-selected model, total allowance, request bound/provenance, limited expiring provider key and remote backstop evidence; fresh per-send approval; raw reply and known/unknown cost retained |
| T06 | Evaluate stair/cascade/wandering consumers | Predeclared stop/no-progress/resource rules, lineage and selection policy, comparator and cost/quality outcomes; no scheduler implied by current primitives |
| T07 | Write operator guide and assess CLI coverage | Commands agree with deployed source; one editable guide home; actual Claude integration separately exercised if requested |
| T08 | Dogfeed this conversation through real Jev with one-use authority | Completed November 5: one HTTP200/VALID call,15/15 baseline agreement,USD0.001226022; raw/dogfeed-result.2026-11-05.md; grant consumed |
| T09 | Versioned transcript capture/export (P0) | TRANSCRIPT-MEASUREMENTS.md; source identity/content/coverage and recovery fixtures; not implemented |
| T10 | Named measurement projection (P1) | Full labelled values, units, schema/producer/input references and missingness; optional embeddings deferred |
| T11 | Readable Jev memory view — cooperating implementer | Installed by cooperating seat; synthetic playground available; _bus/09.cartan.point.md requests peer fixture check; broader acceptance pending |

T00 is implemented and office-installed (VERDICT07); T01 passed its offline positive/negative
checks. T03 is the next implementation gap to close before T05; the proposed
read-only billing command does not exist yet. T04 is a proposed extension, not permission to
silently mutate the present immutable opening contract. T02 can proceed with existing research.
T05 requires actual operator choices and individual approval. T06 does not require building a
general workflow engine first. Track execution in STATUS, not by treating this table as proof.

The T08 audit exercises live plumbing but does not close the original pilot gate. Its aggregate
unanswered probability0.15 versus summed per-group probabilities0.03 gives T02 a concrete
conditional-coherence question to investigate before calibrated IF behavior. No further paid
sample is authorized by this task entry.

## Formulating meaningful judgments

Start with a bounded question over supplied evidence, such as whether a task brief leaves
a required operational constraint unresolved, or whether a cited passage supports a claim.
State what counts as support/omission, what evidence is missing, the alternatives or ordered
rubric, and what downstream decision the observation could inform. Hold an independent
outcome/label apart from the model reply. Known answers and exact rules are useful controls;
do not spend inference on deterministic work that a checklist or parser already settles.

A Noul output is a model probability, not proof of empirical calibration. Choice and Score
also apply: a question need not be a future random event to have uncertain evidential support.
Check option coverage/order sensitivity and wording stability before interpreting confidence.
If IF behavior is needed, define versioned thresholds and an UNCERTAIN route outside the model;
invalid input is ERROR. No opinion authorizes shell execution or another paid call.

Use Oraculum's existing `publications/inner-circle/jev-usage/implementer-brief.md`, usage atlas
and experiments in `/home/hruzam/nabla-lab/`, including its November 4 addendum. Another broad
research pass is unnecessary. A bounded Sol consultation is useful only for an unresolved
predicate, evaluation design or calibration question, with concrete cases and a requested return.

## Settings and spending: three distinct surfaces

1. `jev settings` reads the selected engagement's immutable opening policy and replayed local
   total/spent/reserved/available USD, unresolved liabilities and overruns. It does not download
   a balance or modify settings. `open --budget --model --allow-model` sets policy at creation;
   reopening requires the same policy. No budget edit/refill/local expiry command exists.
2. Provider control belongs to a separate dedicated API key. Recommend a deliberate finite cap,
   explicit expiry and no automatic reset for the first cumulative-allowance pilot. A recurring
   reset is a different policy from expiry. Choose actual amounts/dates before creation. Keep
   management credentials out of the inference path. A documented cap is not exercised proof
   of enforcement for this account/endpoint or an excuse to discard uncertain costs.
3. Provider usage is a separate observed snapshot. Compare dedicated-key scope and time window
   with local records; other clients, resets, delayed usage and uncertain requests can disagree.
   Never auto-settle an unknown request from an aggregate balance difference.

Primary documentation checked November 5 (no authenticated request):

- [Create key](https://openrouter.ai/docs/api/api-reference/api-keys/create-a-new-api-key):
  credit `limit`, optional `expires_at`, reset policy and BYOK inclusion; API creation uses a
  management credential. No key was created here.
- [Current key](https://openrouter.ai/docs/api/api-reference/api-keys/get-current-api-key):
  `GET /api/v1/key` reports usage, remaining limit, expiry and applicable budget information.
  T03 should use the selected inference key for inspection, not a management key.
- [Activity export](https://openrouter.ai/docs/cookbook/administration/activity-export):
  Activity supports time/group filters and CSV/PDF exports of spend, tokens and requests.
  These are provider reports; BYOK spend can be estimated.

Manual route now: inspect/configure the dedicated key in OpenRouter and export from Activity.
No billing-download command, key issuer or encrypted credential manager is shipped in Jev.
T03's tests should cover expired/disabled/unlimited keys, mismatched scope, absent fields,
HTTP failure and secret-free snapshots, with fixtures first and account access separately scoped.

## November 5 research and reader handoffs

T09/T10 incorporate Oraculum's capture/measurement research in this session; see
[the coverage map](TRANSCRIPT-MEASUREMENTS.md). T03/T04 remain the next engine work.
The [calibration brief](../raw/cartan.calibration-research-brief.2026-11-05.md) asks main
Oraculum for a bounded protocol under T02; no new paid sample is released.
The [reader handoff](../raw/HANDOFF.jev-memory-reader.2026-11-05.md) is ready for majkee
to relay; it supports existing records and does not depend on completing T09/T10.
