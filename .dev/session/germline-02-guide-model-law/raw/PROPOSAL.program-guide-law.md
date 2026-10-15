---
title: Candidate public program law and discretionary GUIDE-book law
revision: PG-r3
date: 2026-10-14
by: Cartan · codex · Medusa
authority: proposal only; Majkee gavels the reviewed revision
scope: germline-02-guide-model-law
---

# Candidate law — PG-r3

This is a revised paper contract, not installed law or a production loader. Majkee's carried
decision note DECISIONS.majkee.program-guide-law.md identifies PG-r2/AS-r3/GV-r3 and AR-r2
by exact hash. G1/G2/G3/G6 accept the current candidates; G4/G5/G7 supply amendments.
GV-r4 records exact source words, carried translations and acceptance/review status. AS-r4
accounts current inputs and observed B2 revision movement. DR-r3 records the reconciliation.

AR-r2 PASS applies to its retained r2 identities, not automatically to PG-r3. The amendments,
their affected cases and F-r2-1 wording check require Atlas's next receipt. Final closure is
not inferred from the note's quoted “closed” wording; its explicit review consequences and
current operator instruction hold closure. All implementation/live-surface holds remain.

## P1 · Meaning and homes

Binding operational procedure belongs to a public germline program. GUIDE is the book:
orientation, explanations, approaches, tradeoffs, examples, and discretionary action advice.
Model/state remains at its authoritative owner. A caller brings capability and task authority;
the program requires them and does not grant them. These preserve planning directions 1–9
and the reconciliation's Required reader contract.

G1 accepts these planning names: a public **germline program** is a package; a **function**
is one bounded job; a **process** is one invocation; **perform** is the thin explicit public
doorway. Sella's existing agent-program sense remains distinct; this does not rename agents.
`guide read|write` remains working vocabulary. The accepted family/entry is
`programs/<slug>/CONTROLLER.md` with `fn/<verb-object>.md`; old alternatives remain in r2
history, not competing destinations.

Candidate global source addresses are
`/home/hruzam/ia-sync/germline/programs/<slug>/CONTROLLER.md` and `fn/<verb-object>.md`.
Execution resolves the deployed `/home/hruzam/.germline/programs/<slug>/`, not its authoring
tree. Project addresses are `<declared-project-root>/.germline/programs/<slug>/`; that
project owns their authoring and placement. These are proposed later destinations only.
They do not authorize a directory, file, or deployment here.

Existing `germline/skills/skill.<slug>.md` already means vendor-neutral methods. The accepted
G1/G6 candidate boundary puts shared binding procedure in public programs and native entry
logic in thin loaders. A general method moves once, leaving authority-specific material and
a pointer at its former private/neutral home; separate nonprocedural material may remain.
Exact source moves and caller compatibility still require later measured owner review; no
parallel maintained recipe or bulk migration is authorized.

## P2 · Minimum controller and function contract

The controller states program identity, revision/stamp, job boundary, shared invariants,
capability requirements, model roles, and its **Functions table**. The table is the sole
function index, with one row per explicitly selectable job:

| function id | occasion (reader's job) | declared file binding (normally package-relative) | expected function stamp | result |
|---|---|---|---|---|
| `<verb-object>` | `<one bounded occasion>` | `fn/<verb-object>.md` | `<that file's token>` | `<observable completion>` |

No directory listing, task guessing, private card, or GUIDE supplies hidden functions.
Every selectable function has an explicit controller-table row and one declared file binding
for the selected line. Normal rows use package-relative files. G4's exceptional composition
must be explicitly represented/qualified by that same function index and verified against its
selected binding; a composer receipt cannot invent another index or an undisclosed function. A file left by additive
deploy but absent from the table is a ghost: report it at structural review; never load it.
A missing table-named file is a broken package, not an occasion to search elsewhere.

A selected function identifies its program and exact occasion, carries its own revision/stamp,
declares scoped requirements and explicit task/model inputs, and gives bounded actions,
success observations, output ownership, and specific failure/recovery evidence. Controller
plus this function plus those named inputs must suffice for the job. It may point at a later
occasion but cannot require another function as a preload. Required rationale stays beside
the rule it qualifies: removing it would change correct behavior.

Stamp candidate: retain the current per-file eight-hex-token convention, regenerated on edits;
the table pins the function's token, not a copy of the controller's token. Quote actual paths
and observed tokens and record byte/revision identity. A matching token or hash proves identity
only; it does not prove full reading, correct instruction placement, execution, or compliance.
For every requested scope, including explicitly qualified composition, compare the selected
function's observed stamp against its table row's selected binding and the verified line receipt
before loading its procedure: a mismatch is HELD, the function is not loaded and no operation
runs. This applies even when the caller supplied no additional revision pin; record expected
and observed tokens without fallback. A supplied revision pin is an additional check and its
mismatch also holds before operation. A normal row's default global pin is not silently reused
for a local alternative: an explicit qualified binding must supply an agreeing local pin.
Missing/ambiguous qualification holds. Exact metadata/schema and pin-currency implementation
remain future measurement choices, not authority to create a composer/helper here.

## P3 · Rule grain and model seam

G3 accepts the planning rule-grain test: a rule belongs in the controller if another occasion could breach it,
or breach is costly/irreversible. Otherwise an occasion-specific rule belongs in its function.
Shared invariants load before dispatch. An expensive job-specific prohibition is therefore
visible to all readers, with the concrete branch left in the selected function. Keep its
working rationale there too. Do not erase a scoped rule merely because the controller lacks
its wording; contradiction and omission of a required shared invariant are different defects.

Program grain is larger than an invocation skill and smaller than a whole topic book, earned
by distinct bounded jobs. One function is often one command set. Size alone does not decide
the split. A never-independent function folds into its caller; a function needing a second
function is not sufficient. Finish the job first, then keep context clean, then save tokens.

Model roles resolve through explicit caller inputs to the actual owner's state/schema:
for example RUNBOOK's fixed gate and STATUS's present position. No mandatory MODEL.md is
invented. The controller names each role and required validity/revision evidence; the function
names the concrete inputs it uses. Missing, unreadable, contradictory, or stale required state
produces a finding before mutation. Reading owner state does not acquire its pen. Receipts
belong at the caller's explicitly authorized evidence destination, not in program source.

## P4 · Explicit whole-line resolution and exceptional composition

G4's carried amendment normally selects one coherent line: controller and selected function
from one scope, loaded on the agent side through the shared germline path. Explicit input
still names slug, function, scope, relevant project root, required task/model bindings and
revision pins. Omitted scope is unresolved selection, never vendor precedence or auto-discovery.

| request | normal coherent line | failure boundary |
|---|---|---|
| global | global controller + global function | missing/unreadable/incomplete or stamp mismatch → HELD; no unrelated project probe |
| project | local controller + local function at the declared project | missing/unreadable/incomplete or stamp mismatch → HELD; no global-function borrowing |
| project-first | complete local line when present; complete global line only after confirmed local absence | unreadable/incomplete local package, missing function or mismatch → HELD; never implicit mixed composition |

Confirmed absence requires an accessible declared project root and no package at the exact
address. A missing controller in a present directory or a missing function is not absence.
Global-only remains global/global even if local files exist. A known collision supplied as
task input is recorded as such, not used to invent a project probe. Unsolicited collision
probing, automatic occasion matching and ghost loading remain outside explicit selection.

**Exceptional global-controller/project-function line:** possible but not the expected
split-program shape. It requires an explicit project-composition request, both declared
component scopes/paths/identities and a composer-verified whole-line result. The public
controller's function index must explicitly qualify the selected binding; file presence,
a receipt naming an otherwise undisclosed function, or silent fallback is insufficient.
No production metadata schema, composer implementation or automatic selection mechanism is
chosen by this proposal. The normal and exceptional declarations must remain distinguishable.

The composer is a future framework-development/measurement mechanism: it proves which
controller/function are selected, their scope and revision identity, compatibility and
contradiction result. Its evidence must show the complete line the agent is to load, retained
controller invariants, table/binding agreement and sufficiency with explicit model/task inputs.
A hash/stamp alone cannot prove compatibility. Missing, stale, ambiguous or contradictory
evidence → HELD; no operation or borrowed fallback. Loading the whole line on the agent side
still needs a later fresh-session witness; the paper declaration is not that witness.

An explicitly selected local controller plus local function is a valid local whole line.
**Local controller plus global function is forbidden**, even with an asserted composer PASS.
Composition never grants capabilities, relaxes owner locks, replaces public requirements with
private grants, or lets a function require another function as a preload.

Each component stays confined to its explicitly declared owning root: global controller in
the global package, exceptional local function in the designated project package. A path
escape is not a composition declaration. Composer proof cannot reclassify arbitrary files
or add rows to the controller's sole function index.

This G4 amendment supersedes PG-r2's blanket same-package/no-overlay *proposal* sentence.
RUNBOOK's operational no-mixing hold remains in force for this authoring gate: no components
are assembled, installed or loaded here. Atlas must review this proposal seam; the later
audit may measure it only under a separately authorized scope. The accepted original planning
direction remains the default coherent line; only this explicitly carried exception changes it.

S1 pinned specialisation versus S2 separately complete scoped packages, and per-edit stamp/byte
versus semantic compatibility pin policy, were alternatives in PG-r2. The decision note chooses
the whole-line/composer shape but does not name one of those detailed policies. They remain
unresolved implementation/design parameters for review, not silently chosen defaults or
implicit closure-ready deferrals. Atlas must identify any parameter requiring a further
explicit Majkee choice before acceptance; no compiler, registry or pin manager is authored here.

Minimum line receipt records explicit request (including exceptional composition if any),
selected controller/function scopes and paths, table row/qualified binding, expected/observed
pins and byte identities, required model/task owner inputs, qualification and caller authority,
compatibility/contradiction evidence, agent-load evidence or its unperformed status, and
completion/failure/recovery observations at the caller's authorized evidence destination.
Selection, composer compatibility, agent loading and completion are separate evidence claims.

## P5 · Public capability and enforcement boundary

A public program serves a human, chatbot, or seat without a named private identity. It must not
depend on a card, identity, vendor file, or GUIDE for required procedure. Required model inputs
may be owner-held/private data explicitly supplied by an authorized caller; requiring a data
role is different from requiring a private controller. Caller qualification is checked before
side effects. Partial grants produce a held result with the missing requirement, never an
assumed downgrade or a helper doing the forbidden write.

Private cards retain invokers, grants, and agent-specific authority. A card may optionally call
a public program by explicit selection. Public programs never point back to cards or require
that route. A general-purpose method promoted from a card moves once; the former private home
keeps its authority and a pointer. G6 accepts this visibility/promotion candidate; concrete moves still require later owner
review and task authority. No card is rewritten.

G5's carried amendment permits a small **explicit native binding table** from named public
capabilities/functions to that vendor's harness or CLI mechanism. It is entered through the
vendor's native route and points down to the shared public method. Its content is native
translation, qualification and evidence adaptation only; it supplies no operational branches,
permissions or second procedure body that the public program lacks.

The table does not discover work, route tasks, list a function census or choose an occasion.
The explicit public controller table remains the only function index. A native binding maps
an already selected named capability/function to an available mechanism and evidence shape;
it cannot create an undisclosed public function or grant a caller missing authority.

The public controller declares requirements and evidence. It never programmatically touches
the vendor harness, names a private card as prerequisite or auto-configures an adapter.
The native adapter performs/proves the vendor-bound translation under the caller's actual
authority. Declaration of tools/sandbox is not proof of effective restriction; runtime
placement, qualification and compaction behavior still need independent evidence.

Exact binding-table file/schema, enforcement homes/owners and qualifying native routes remain
future measured placement details. The note authorizes this proposal shape, not production
loaders or changes to vendor harnesses. Thin public perform entries do not become registries
or auto-senders. No native adapter/table/helper is authored, installed or invoked here.

## P6 · GUIDE-book contract

Keep one topic per slug and GUIDE.md as the knowledge entry at
`/home/hruzam/reposoma/raw.guides/<slug>/GUIDE.md`. Discretionary prose may explain why one
approach is preferable and show illustrative commands without claiming required procedure.
An illustrative command mirroring a program function may use an explicit `<slug>/<fn>` pointer
to make later comparison possible. G2 accepts this optional traceability candidate; it is
not a requirement to maintain a second recipe, new timer or resolver.
The test is behavioral: would correct completion or permitted action depend on obeying this
passage? If yes, its binding content belongs in the program. A command alone is not proof of
binding procedure. An example must not become a second maintained operational recipe.

G2 accepts `res/` for registered knowledge depth: chapters individually in GUIDE's Manifest
with `chapter-of`, other side-directories once each as current slug law specifies. Topic
knowledge is preserved; no flattening/deletion follows merely from this law proposal. No executable function table in GUIDE
competes with the program table. GUIDE may point to the explicit program/function doorway for
an operation; execution must be correct without opening the book.

`guide read` and `guide write` remain working vocabulary. The current Claude doorway serves
verbatim knowledge and carries writer law; the current Codex doorway separates consult/display
and points to shared writer law. They are observed local sources, not a new contract silently
imposed on both. If guide authoring is binding procedure, it must eventually have one public
method home and a thin native entry; defining it is later implementation. The four v3 deltas
(shape listing, BACKGROUND keyword, Functions orphan register, model writer key) are declined.

G7's carried amendment retires BACKGROUND as a prescribed slot and permits only an optional
guide-local maintenance/history journal in this shape:
`<guide-slug>/{GUIDE.md,src/journal-...}`.
It records guide-relevant process observations and maintenance shifts. Its name/suffix is not
a new vault naming rule. It is not Majkee/myShell's daily vault journal, a session STATUS,
required procedure, required rationale, a resolver input or a second maintained recipe.

G7 names the history position, not a closed list of slug directories: G2's registered res/
knowledge depth remains. No journal is mandatory. Permission to write still belongs to the authorized guide owner/task;
the shape grants no pen. GUIDE may point to the optional local journal through its manifest;
the resolver continues to serve knowledge entry/chapters, never this src/ journal automatically.
No global journaling mechanism or program-level journal is introduced.

The current slug-directory law calls src/ outbound staging. A retained guide-local src/journal
is a proposed concrete use that must be reconciled in the later owning law/placement audit;
no current guide manifest or src/ taxonomy is amended here. Necessary operational rationale
remains beside its public-program rule. PAD and vault-journal authority are unchanged.

## P7 · Structural review and later proof

Before later promotion/deploy, review explicit selection, full controller/function sufficiency,
exact table/path/occasion identity, expected versus observed per-file tokens, scoped root
confinement, ghost and duplicate registration handling, owner references, capability qualification,
and absence of private/vendor/GUIDE procedural dependencies. Review every source disposition and
each rule's retained rationale. Mechanical validity, semantic review, placement, and runtime
behavior are separate claims. A detector's clean output cannot certify the whole contract.

Atlas's next paper review checks the complete amended candidate and explicit decision/source
accounting, including new composition/native-binding/journal cases below. AR-r2 retains only
its unchanged-text coverage and stated limits until that receipt. The observed B2 digest change
and restoration are reported; the existing full-review trigger is not silently waived. A finding carries path:line, inputs
read, revision, outcome, and remaining limits. Cartan reconciles it with an explicit disposition;
changed candidates receive a new revision and affected review coverage. Majkee gavels that
reviewed revision in GV-r4 or its successor. Open architecture rows hold closure until a
specific accepted choice or explicit deferral leaves no hidden binding requirement.

Future implementation conditions, unperformed here:

1. A separately authorized read-only whole-tree measurement classifies **binding procedure**
   versus discretionary knowledge, actual uses, owners and migration dependencies before broad
   conversion. Preserve topic knowledge, mirrors and ownership; do not reuse historical counts.
2. Verify the dated vendor leads against current official primary sources and installed versions
   (details in AS-r4). Native primitives are assessed before any new mechanism.
3. After naming/home gavels, prove global/project placement and revision currency at destinations,
   deliberate ghost retirement and fallback failures. Commit/deploy authorization stays separate.
4. Fresh independent Claude and Codex sessions demonstrate actual controller/function loading,
   permission qualification, negative behavior and persistence of costly invariants through
   compaction. No paper receipt or hash can substitute.
5. Promotion moves one method to one maintained home and verifies old callers/pointers and owner
   state. Any future reporting timer needs a new proposal; it never repairs or certifies meaning.

Majkee's steering in this wake requires the **next session to be audit-only**. Recommended
working label: `germline-03-foundation-audit`, separately authored after this planning acceptance.
It assesses the Sella/germline/program/builder seams, actual method uses and owners, candidate
programs, source/current-law drift and official vendor facts; it returns findings and a measured
worklist. It installs or rewrites nothing. Only after that audit and its gavels should a separately
authorized sibling, provisionally `germline-04-program-loader-proof`, build a measured pilot and
prove native loading/placement. These labels are proposals, not opened sessions or new launchers.
Conversions remain separately authorized. The old guide-model-02 audit is historical, not this
next gate and never authority to read the sealed hypotheses.

## P8 · Foundation stones for builders; candidate programs

Majkee's additional direction in this wake is to put the foundation here, including the relations
between Sella, germline, public programs, and builders, and possible programs such as tunnel use
by an agent. This section records that direction without naming its candidate details as locked.

| object | owns | seam with the other objects |
|---|---|---|
| Sella | experimental primitive-building discipline: suitable contract/layer, small entry, explicit return/failure, dated behavior proof and reviewed promotion | governs construction; its “agent = program” vocabulary and platform claims do not silently define the new public-package taxonomy |
| germline | vendor-neutral authored meaning and scope; global source on ia-sync, deployed copy and separate project layer | homes identity/private authority and shared methods; does not grant caller capabilities or session ownership |
| public program | one shared binding job family, controller invariants, bounded functions and owner-model seam | supplies reusable procedure; agent-specific cards may call it; GUIDE explains it; vendor entry loads it |
| native skill/agent/hook | the smallest needed entry, role or enforcement mechanism for that runtime | references shared meaning; proves instruction placement and effective capability; does not duplicate the method |
| builder | measures the existing sources, separates identity/method/binding, proposes homes, builds only the accepted delta and returns proof | is the authoring role, not a new authority above Sella, owner locks, the operator or session law |
| RUNBOOK/STATUS law | fixed gate and sole live position, status ownership and recovery | governs the session a builder works inside; Sella governs the primitive being built |

Retained foundation anchors are Sella §§Boundary, 0, L1/L3/L4/L7/L8/L9, and §5 item 4;
invariance-autonomy's measurement-before-body/method/nothing; current germline README; and the
germline-forge precedence/proof principles. Necessary working rationale stays with each method.
“Retained” does not canonize Sella: its current header explicitly says DRAFT/experimental and
G3-HELD. Its vendor tables and kernel/compaction assertions are dated leads, not freshly proven
platform facts. The full corpus need not be copied into each public controller.

Three visible seams need the later audit rather than wording that resolves them here:

- Sella L1 currently places procedural playbooks in skill bodies; accepted planning direction
  puts shared binding procedure in germline programs with thin vendor loaders. Proposed builder
  interpretation: distinguish authoring home from the runtime's instruction placement, then
  prove that placement. This is a candidate adaptation, not a Sella edit or assumed enforcement.
- Sella §5 still calls pulse the doing-state; current runbook/status law makes pulse a router
  and STATUS the sole gate position. This session follows its current named law. The audit must
  account the stale map; no Sella/pulse patch belongs here.
- Sella's “program = agent” and germline's existing neutral `skills/` meet the new public-package
  term. G1 has selected public-program vocabulary and one maintained method home; the audit still
  checks the relationship with existing Sella/neutral-skill terminology without renaming canon.

The following are **candidate measurement subjects**, not a catalog/index, commissioned skills,
or a required first build. Names/boundaries are measurement subjects within the recorded G1/G3 and amended G5 boundary:

| candidate public package / bounded functions | user and explicit owner inputs | why it may earn a program; audit evidence needed |
|---|---|---|
| tunnel / assist-user, run-approved-turn, recover-result | an agent using an already operator-enabled handle; explicit handle/thread, task authority, turn outcome and evidence target | GUIDE and user-run currently combine strict operational rules with explanations; measure agent occasions, preserve operator-only enable, explicit state-path selection (no implicit handle), single-writer, read-before-retry and never-unlink-Codex-writer-locks constraints; compare instructions with shim |
| primitive-build / measure-method, draft-binding, verify-placement | an authorized builder; named source pair, destination authority, native route and required proof | shared building method spans vendors; measure against existing builders/skills and germline-forge before making a second builder procedure |
| guide-author / write-book, classify-binding-passage | a guide writer; exact source/topic, owner rights and accepted public-method destination | separates discretionary authoring advice from binding writer procedure; do not presume conversion or delegate the gavel |
| session-position / verify-checkpoint, replace-position | the assigned STATUS owner; exact RUNBOOK gate, evidence, current snapshot and write grant | repeated recovery/one-next-action discipline may be a shared bounded method; the owner still alone writes STATUS |

For the tunnel candidate, a possible native **tunnel-user skill** would be only an explicit
loader of `tunnel/assist-user` or another named function. It is not a role, enable grant, alias
for the tunnel engine, or automatic sender. The public controller serves any qualified caller;
an agent-user function may require shell/handle access while a human-facing assistance function
may return instructions only. Audit must decide whether these are independent functions, one
program, or merely existing method reuse. No send, selftest or live probe runs in this gate.

Concrete source drift already merits audit: user-run says no in-thread trim exists, while
current shim source defines `compact`/`thread/compact/start`; its older policy description also
predates source `--override` handling. This is source inspection, not a fresh protocol trial.
The later audit must compare dated docs with code and official facts before extracting a strict
recipe. Merely moving the old text into germline would preserve its stale claims.

## Paper fixture — explicit inputs only

This fixture is synthetic prose inside PG-r3. No filesystem below exists or is created.
Atlas reasons from the stated inputs; no command runs and no state is written.

**Task:** perform `checkpoint-note/freeze-note`, scope `global`, evidence target
`/fixture/task/evidence/note.md`. Caller is a human with read and write capability, explicitly
authorized by this fixture's task to write that target. No agent card or GUIDE is supplied.

**Controller:** `/fixture/global/programs/checkpoint-note/CONTROLLER.md`, revision `toy-1`,
stamp `11111111`. Invariants: write only the task's granted target; never change owner state;
never invent completion evidence; no mutation when input revision or evidence disagrees.
Requires: read owner state and write granted evidence target. Model role `owner-state` is bound
by the task. Its entire Functions table is:

| function id | occasion | file | expected stamp | result |
|---|---|---|---|---|
| freeze-note | record a verified note | fn/freeze-note.md | 22222222 | note pins supplied owner revision and evidence |
| inspect-note | inspect an existing note | fn/inspect-note.md | 33333333 | comparison result without writes |

**Selected function:** `/fixture/global/programs/checkpoint-note/fn/freeze-note.md`, program
`checkpoint-note`, occasion `record a verified note`, stamp `22222222`. Read `owner-state` and
task-grant/evidence inputs. Require `verified=true`, matching task-expected revision, and a
supplied completion-evidence reference. Write a note containing only that revision, evidence
reference and selection receipt at the granted target. Success: the returned note has these
values and owner state is unchanged. Invalid input or incomplete grant → hold without write,
record missing requirement. Write failure → report failure and inspect the target before retry;
do not claim completion. No other function is read.

**Owner/task inputs:** `/fixture/task/STATUS`, owner `task-head`, revision `state-4`,
`verified=true`, evidence reference `/fixture/task/evidence/check-4`, task-expected revision
`state-4`. This models owner state, not a new MODEL.md. The evidence reference is supplied as
verified by the task for paper purposes; that is not a live observation.

| case | changed explicit input | expected paper result under candidate P2–P5 |
|---|---|---|
| T1 completion | baseline above | global controller + freeze-note + named owner/task inputs suffice; note pins state-4/check-4; no guide/card/other-function dependency |
| T2 missing function | request `translate-note`, absent from table | hold unmatched selection; no function scan or invented route |
| T3 stale stamp | freeze-note observed token `22222223`, table expects `22222222` | hold before operation; mismatch named; no fallback |
| T4 scope collision | complete project package has same slug and a freeze-note with its own tokens; explicitly request global | global selected; project contributes no component; receipt states scope choice |
| T5 unavailable project scope | request project-first but no project root/access evidence exists | hold; not confirmed absence; no global fallback |
| T6 incomplete grants | baseline caller may read but has no grant to write the target | hold missing write authority; no helper or private-card assumption |
| T7 confirmed absence | project-first; accessible declared project root; exact package confirmed absent; global fixture valid | global fallback with explicit absence evidence in receipt |
| T8 broken local package | project-first; local controller exists but selected file is missing | hold incomplete local package; no borrowing/global fallback |
| T9 ghost file | baseline plus unindexed fn/translate-note.md left at destination | ghost structural finding; requested translate-note still fails table selection; no ghost load |
| T10 owner-state failure | baseline owner revision state-5 conflicts with task-expected state-4, or verified=false | hold exact state/evidence mismatch without write; model owner's pen unchanged |
| T11 omitted scope | baseline task omits its scope | HELD unresolved selection before any package/function load; no implicit precedence |
| T12 escaping path | baseline table names `fn/../../outside.md` | HELD invalid package confinement before function load; no external procedure read or operation |

These examples test the candidate, not effective runtime behavior. G3 adds a paper grain test:
the target boundary is a costly shared invariant; the `verified=true` note branch is scoped;
its mutation prohibition is eagerly present in the controller. G4's specialisation alternatives
need separate review reasoning and Majkee's decision; the baseline fixture has no exceptional composition; additional cases below expose it.

## Amended paper cases — no runtime or composer built

These use synthetic explicit inputs only. The baseline T1–T12 retains its normal global-line
inputs and outcomes. For the exceptional fixture, the global controller is explicitly named
as toy-composition revision 2, with the same shared invariants and model requirements. Its
single selected table row qualifies a project-function binding for the requested job, with
expected local token 44444444. Task input names the project root and local function path;
that local function has token 44444444 and is sufficient under the named global controller.
The global controller path is `/fixture/global/programs/checkpoint-note/CONTROLLER.md`,
stamp 55555555. Task input binds project root `/fixture/project` and local function
`/fixture/project/.germline/programs/checkpoint-note/fn/freeze-note.md`, stamp 44444444;
its program/occasion and owner-state/read/write inputs are the same bounded job as T1.
The supplied measurement receipt identifies these components, scopes, row and pins,
reports compatible/no contradiction and the whole agent-load line. This is an assumed paper
input, not real semantic or loading proof, and fixes no production metadata format.

| case | explicit variation | paper outcome |
|---|---|---|
| T13 declared exceptional line | request global-controller/project-function composition with the complete explicit fixture inputs/qualified row and valid measurement receipt | eligible selected global/local whole line; caller capability and owner-state checks still apply; real agent-load proof remains unperformed |
| T14 missing composition proof | same explicit request but no composer compatibility/contradiction result | HELD; no inference from file presence, no operation or global fallback |
| T15 forbidden reverse | local controller + global function, even with asserted measurement PASS | HELD forbidden direction; composer never grants this shape |
| T16 ordinary global | baseline global request, local function exists but no explicit composition request | global/global only; local file ignored, no scope discovery |
| T17 incompatible/unknown line | exceptional fixture reports contradiction, unknown compatibility or stale component identity | HELD; retain the finding; never select a tidier scope by fallback |
| T18 permitted native binding | explicitly selected public function/capability is mapped by a native table to a mechanism plus qualification/evidence adaptation, no procedure copy | within G5's proposal boundary; runtime enforcement/load proof still required and no grant inferred |
| T19 native procedure/router creep | table carries public procedure branches or discovers/tasks/routes/selects unrequested functions | invalid alternate procedure/index boundary; reject the proposal instance |
| T20 optional guide-local journal | guide owner explicitly proposes src/journal-... containing only guide maintenance/history | within amended G7; no vault/program journal, required read or automatic resolver service |
| T21 hidden procedure in journal | completion requires an instruction available only in that journal | invalid G7/P2 sufficiency and one-home boundary; move required method to public operational home under later authority |
| T22 local token mismatch | qualified composition row/receipt expects 44444444 but local file token is 44444445 | HELD before procedure load; no use of default global pin or borrowed file |
| T23 undisclosed function | composer receipt names a function absent from the public controller table | HELD; receipt cannot add an index entry or make a ghost selectable |

G4 supplies the exceptional shape only for declared framework measurement; no T13 input is
manufactured by this task. Whole-line agent loading, compatibility and native enforcement are
later proofs, not outputs of this paper walkthrough.

## Exact source anchors

- Basis B1/B2: accepted RECONCILIATION, Accepted planning directions and Required reader
  contract; `/home/hruzam/reposoma/.majkee/journal/2026-10-14.md`, consult close.
- P2/P3/P7 retain named split/sufficiency/rationale/witness claims from staged model-shape,
  WAVE R1/R4/R5 and Symmetry's F3/F4/F7 record; AS-r4 maps their paths and byte identities.
- P4/P5 expose Atlas INSIGHT §§1–4 and 6–7 as candidate detail, especially specialisation,
  ghost handling, enforcement and receipt naming. Its vendor claims remain dated leads.
- P1/P6 placement and shelf comparisons use current germline README, guide-writing GUIDE
  and slug-directories, current Claude/Codex guide doorways, and germline-forge's stale banner.
  All are inventoried in AS-r4; current law is not modified by this comparison.
- P8 uses Majkee's additional wake steering and focused Sella Boundary/§0/L1–L9/§5/glossary
  anchors; tunnel GUIDE/user-run and shim symbol inspection support candidate status and drift,
  not runtime claims. AS-r4 records their identities and later audit disposition.

Decision authority for PG-r3's amendments is the exact operator note at
`/home/hruzam/ia-sync/.dev/session/germline-02-guide-model-law/raw/DECISIONS.majkee.program-guide-law.md`;
GV-r4 quotes it verbatim and distinguishes carrier translation from operator words. No current
candidate hash is called reviewed until Atlas returns the required receipt.
