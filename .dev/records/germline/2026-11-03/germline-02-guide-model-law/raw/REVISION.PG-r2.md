---
title: Candidate public program law and discretionary GUIDE-book law
revision: PG-r2
date: 2026-10-14
by: Cartan · codex · Medusa
authority: proposal only; Majkee gavels the reviewed revision
scope: germline-02-guide-model-law
---

# Candidate law — PG-r2

This is a paper contract, not installed law or a loader specification approved for building.
Its controlling inputs are the accepted reconciliation and Majkee's 2026-10-14 journal,
accounted by AS-r2 in `ACCOUNTING.sources.md`. The seven decision families remain OPEN in
GV-r2, `GAVELS.program-guide-law.md`. “Must” below describes the candidate's behavior if
accepted; it does not claim a final gavel. Atlas AR-r1 reviewed the retained r1 bytes: proposal PASS with findings, accounting FAIL
on seven omitted sources. PG-r2 corrects the candidate and awaits focused re-review; no final
acceptance exists. `DISPOSITION.atlas.program-guide-law.md` records each finding.

## P1 · Meaning and homes

Binding operational procedure belongs to a public germline program. GUIDE is the book:
orientation, explanations, approaches, tradeoffs, examples, and discretionary action advice.
Model/state remains at its authoritative owner. A caller brings capability and task authority;
the program requires them and does not grant them. These preserve planning directions 1–9
and the reconciliation's Required reader contract.

Working names: a public **program** is a package; a **function** is one bounded job; a
**process** is one invocation; **perform** is the explicit public doorway. Sella already
calls agents “programs” (germline-forge's opening anchor). If Majkee keeps this vocabulary,
qualify it as “public germline program”; it does not rename agents. Alternatives are
`processes/` and another operator-chosen family name. G1 holds the choice.

Candidate global source addresses are
`/home/hruzam/ia-sync/germline/programs/<slug>/CONTROLLER.md` and `fn/<verb-object>.md`.
Execution resolves the deployed `/home/hruzam/.germline/programs/<slug>/`, not its authoring
tree. Project addresses are `<declared-project-root>/.germline/programs/<slug>/`; that
project owns their authoring and placement. These are proposed later destinations only.
They do not authorize a directory, file, or deployment here.

Existing `germline/skills/skill.<slug>.md` already means vendor-neutral methods. G1 must
choose the boundary before a program lands. Recommended candidate: public programs own
shared binding procedure; vendor skills load it; an existing neutral skill containing that
procedure moves once and leaves a pointer, while genuinely separate nonprocedural material
may remain. Alternative: keep the existing `skills/` family as the physical method home and
distinguish controller packages there. Both need measured file-by-file classification and
caller compatibility; neither licenses parallel maintained recipes or bulk migration.

## P2 · Minimum controller and function contract

The controller states program identity, revision/stamp, job boundary, shared invariants,
capability requirements, model roles, and its **Functions table**. The table is the sole
function index, with one row per explicitly selectable job:

| function id | occasion (reader's job) | package-relative file | expected function stamp | result |
|---|---|---|---|---|
| `<verb-object>` | `<one bounded occasion>` | `fn/<verb-object>.md` | `<that file's token>` | `<observable completion>` |

No directory listing, task guessing, private card, or GUIDE supplies hidden functions.
Every table row has one file and every selectable file has one row. A file left by additive
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
For every requested scope, compare the selected function's observed stamp against its table row
before loading its procedure: a mismatch is HELD, the function is not loaded and no operation
runs. This applies even when the caller supplied no additional revision pin; record expected
and observed tokens without fallback. A supplied revision pin is an additional check and its
mismatch also holds before operation. These are candidate rules, still pending G4 gavel.
G4 decides
the minimum identity fields and how deployed currency is checked; no helper is presumed.

## P3 · Rule grain and model seam

Recommended G3 test: a rule belongs in the controller if another occasion could breach it,
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

## P4 · Explicit resolution and selection receipt

Input is an explicit program slug, function id, declared project root when relevant, and scope:
`project`, `global`, or deliberately requested `project-first`. Omission is an unresolved
selection, never implicit precedence. Native vendor skill/agent precedence is not this resolver.
The caller must supply any revision pin and named model/task bindings.

| requested scope | candidate resolution | failure boundary |
|---|---|---|
| project | select the complete package at the declared project's germline | missing/unreadable/incomplete package or table/file stamp mismatch → HELD; no global fallback |
| global | select the deployed global package | missing/unreadable/incomplete or table/file stamp mismatch → HELD |
| project-first | use a complete local package if present; use global only after confirmed local absence | unreadable root, incomplete local package, missing selected function, stamp mismatch or conflict → finding; never fallback |

“Confirmed absence” means an accessible, explicitly declared project scope was checked at the
exact package address and no package exists. Unknown access, no declared project, a present
directory without its controller, and a missing function in a present package are not absence.
Path confinement and any symlink policy must be proven by the later adapter; a function path
escaping the selected package is structurally invalid. All controller/function components
come from one selected package. An explicit global request needs no project root; its candidate
path resolves only the global package and does not probe an unrelated project. If a collision
is already known from named task inputs (as in T4), the receipt records that supplied fact and
the choice/reason; it does not invent knowledge of the unqueried scope. Project/project-first
require the declared project root. Optional collision probing is a separate G4-open choice,
never a hidden input requirement. Never borrow a function from the other scope.

Same-slug **specialisation** is Atlas INSIGHT's proposal, not an accepted resolver detail.
G4 exposes two alternatives:

- S1: a project package declares `specialises: <global controller revision>`, is complete in
  itself, and retains/adds/narrows the declared upstream invariants. Structural comparison
  checks the pinned base. Runtime still uses one package; the base is not a hidden second
  controller. Unverifiable ancestry or stale base pin holds that specialised package.
- S2: scoped packages are separately complete; scope alone selects them, with explicit
  applicable project/global locks as owner inputs. No inheritance metadata is introduced.
  An incompatible package still yields a finding against those locks.

Recommendation is S1 only if Majkee wants an upstream invariant-preservation contract and
accepts its review/currency cost. Neither S1 nor S2 is adopted by this proposal. A topology
that loads one base controller and overlays partial project functions conflicts with coherent
selection; it cannot enter through implementation wording. The paper fixture below has no
specialisation and does not resolve this gavel by example.

For S1, G4 must separately choose whether the specialisation pin is a per-edit stamp/byte
revision or an explicitly governed semantic compatibility revision. The former stales dependents
on every edit, including a typo; the latter needs its own compatibility and invariant-preservation
review. Neither currency policy is implied by `<global controller revision>`.

Minimum candidate selection receipt:

| field | evidence it carries |
|---|---|
| invocation | explicit slug, function, requested scope, declared project root (or not applicable) |
| selection | actual scope, absolute package/controller/function paths, resolution reason and local-absence result when used |
| identity | controller revision/stamp and function expected/observed stamp plus byte identity; caller pins and any declared specialisation pin |
| inputs | named task/model roles, owner addresses and versions actually read |
| qualification | required capabilities, observed availability, granted task/write boundary; grants remain with caller |
| outcome | completed, held, or failed; completion observations or exact failure class, durable evidence destination and recovery probe |

Selection records availability and chosen bytes. Completion records what happened and whether
success observations passed. No receipt grants the pen or substitutes for Majkee's acceptance.

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
keeps its authority and a pointer. Visibility/promotion mechanics remain G6; no card is rewritten.

Vendor-neutral requirements are stated here; enforcement mechanisms have a vendor-native home
that points to this source and contains only mechanism, not another copy of procedure. G5 must
name both homes and owners before any build. A source declaration is not evidence of an effective
sandbox or tool restriction. No agent binding is silently made the common enforcement home.
Candidate global `perform` adapters are thin, explicitly invoked resolvers, never registries,
occasion matchers, census engines or discovery buses. Whether one entry per vendor suffices
requires measured native loading and context evidence. No new adapter is authored in this gate.

## P6 · GUIDE-book contract

Keep one topic per slug and GUIDE.md as the knowledge entry at
`/home/hruzam/reposoma/raw.guides/<slug>/GUIDE.md`. Discretionary prose may explain why one
approach is preferable and show illustrative commands without claiming required procedure.
An illustrative command mirroring a program function may use an explicit `<slug>/<fn>` pointer
to make later comparison possible; Atlas P4 proposes this traceability rule. G2/the audit must
decide it before it becomes binding; no timer or extra recipe is introduced.
The test is behavioral: would correct completion or permitted action depend on obeying this
passage? If yes, its binding content belongs in the program. A command alone is not proof of
binding procedure. An example must not become a second maintained operational recipe.

Recommended G2: keep `res/` for knowledge depth; register chapters individually in GUIDE's
Manifest with `chapter-of`, and other side-directories once each as current slug law specifies.
Alternative: keep a flat GUIDE shelf and relocate independently useful knowledge with explicit
accounting; do not delete it merely to simplify taxonomy. No executable function table in GUIDE
competes with the program table. GUIDE may point to the explicit program/function doorway for
an operation; execution must be correct without opening the book.

`guide read` and `guide write` remain working vocabulary. The current Claude doorway serves
verbatim knowledge and carries writer law; the current Codex doorway separates consult/display
and points to shared writer law. They are observed local sources, not a new contract silently
imposed on both. If guide authoring is binding procedure, it must eventually have one public
method home and a thin native entry; defining it is later implementation. The four v3 deltas
(shape listing, BACKGROUND keyword, Functions orphan register, model writer key) are declined.

G7 belongs to Majkee: retire BACKGROUND as a prescribed slot, or allow it only for an independently
useful history purpose. Neither alternative permits required procedure or rationale hidden there.
No reserved `background` resolver keyword, fixed three sections, or mandatory seed follows from
this proposal. PADs and BACKGROUND authorship remain Majkee's space.

## P7 · Structural review and later proof

Before later promotion/deploy, review explicit selection, full controller/function sufficiency,
exact table/path/occasion identity, expected versus observed per-file tokens, scoped root
confinement, ghost and duplicate registration handling, owner references, capability qualification,
and absence of private/vendor/GUIDE procedural dependencies. Review every source disposition and
each rule's retained rationale. Mechanical validity, semantic review, placement, and runtime
behavior are separate claims. A detector's clean output cannot certify the whole contract.

Atlas's fresh paper review covers P1–P7 and T1–T12 below. A finding carries path:line, inputs
read, revision, outcome, and remaining limits. Cartan reconciles it with an explicit disposition;
changed candidates receive a new revision and affected review coverage. Majkee gavels that
reviewed revision in GV-r2 or its successor. Open architecture rows hold closure until a
specific accepted choice or explicit deferral leaves no hidden binding requirement.

Future implementation conditions, unperformed here:

1. A separately authorized read-only whole-tree measurement classifies **binding procedure**
   versus discretionary knowledge, actual uses, owners and migration dependencies before broad
   conversion. Preserve topic knowledge, mirrors and ownership; do not reuse historical counts.
2. Verify the dated vendor leads against current official primary sources and installed versions
   (details in AS-r2). Native primitives are assessed before any new mechanism.
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
  term. G1 must decide a discriminating vocabulary and one maintained method home; paths alone
  are insufficient evidence that users understand the distinction.

The following are **candidate measurement subjects**, not a catalog/index, commissioned skills,
or a required first build. Names and boundaries remain G1/G3/G5 decisions:

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

This fixture is synthetic prose inside PG-r2. No filesystem below exists or is created.
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
need separate review reasoning and Majkee's decision; the fixture grants neither.

## Exact source anchors

- Basis B1/B2: accepted RECONCILIATION, Accepted planning directions and Required reader
  contract; `/home/hruzam/reposoma/.majkee/journal/2026-10-14.md`, consult close.
- P2/P3/P7 retain named split/sufficiency/rationale/witness claims from staged model-shape,
  WAVE R1/R4/R5 and Symmetry's F3/F4/F7 record; AS-r2 maps their paths and byte identities.
- P4/P5 expose Atlas INSIGHT §§1–4 and 6–7 as candidate detail, especially specialisation,
  ghost handling, enforcement and receipt naming. Its vendor claims remain dated leads.
- P1/P6 placement and shelf comparisons use current germline README, guide-writing GUIDE
  and slug-directories, current Claude/Codex guide doorways, and germline-forge's stale banner.
  All are inventoried in AS-r2; current law is not modified by this comparison.
- P8 uses Majkee's additional wake steering and focused Sella Boundary/§0/L1–L9/§5/glossary
  anchors; tunnel GUIDE/user-run and shim symbol inspection support candidate status and drift,
  not runtime claims. AS-r2 records their identities and later audit disposition.
