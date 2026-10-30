# Source reader mountain — proposed working trial

2026-10-26 · Cartan · office · main @ 5c26d80 · deploy-inert proposal, not a live RUNBOOK.

## Operator intent and disposition

Majkee proposed a real task: a zsh brick for germline, guides and OpenAI/Anthropic skills,
possibly with a later Slint or other UI. He selected **browse/read existing sources first**.
He proposed a main architect, IT support, native Astrobley implementing, and researcher/auditor
consultation through tunnels, with at least two substantive turns per role.

This is a suitable mountain. It produces a useful tool and requires actual architectural
judgment about provenance, source versus deployed copies, guide resolution and vendor semantics.
Its first slice is bounded enough that operational trouble need not consume the main's head.

Two outcomes are judged separately: whether the reader works, and whether delegating the
whole consultation capability leaves the main able to reason about the work. Neither outcome
alone proves that germline needs a new global controller/composition design. An ordinary skill,
existing roles and a small local program remain the simpler comparison.

## Existing foundation (observed, no implementation in this preparation)

- `zsh/experimental/README.md`: lazy `experimental/<id>/runner.zsh`; offline help; maintainer
  log row; source validation/deploy dry-run. No startup source line is needed for a lazy runner.
- `zsh/experimental/dispatcher.zsh`: `exp-list` / `exp-run`; `_EXPERIMENTAL_ROOT` can select
  the repo's source tree in an isolated shell for an undeployed end-to-end check.
- `codex/skills/guide/SKILL.md`: guide catalog from frontmatter, slug → GUIDE, unambiguous
  substring chapter resolution under res/, and full source display. Side directories are
  not ordinary chapters. This procedure is an input contract, not already a shell browser.
- `germline/README.md`: ia-sync/germline is authored source; ~/.germline is deployed;
  identities/bindings/cards and skill.*.md have distinct jobs. No durable index by design;
  discovery bus is parked. The proposed reader derives a transient catalog only.
- `codex/skills/chatbot-port/SKILL.md`: source/deployed-home and twin provenance precedents;
  its port/write procedure is outside the reader's scope.
- `zsh/ai/command-palette.zsh`, `zsh/session/runbook.{zsh,py}`: existing selection/display
  patterns. Reuse a small pattern where suitable; do not import unrelated session machinery.

Preparation used a read-only explorer and vendor researcher. The researcher initially cited
OpenAI Agents API capability-directory behavior; Cartan rejected that substitution and obtained
Codex CLI-specific documentation before including the discovery rules below.

## First product slice

Working brick ID: `source-reader`, subject to the execution-time existence sweep.

User journey: choose germline / guide / Codex skill / Claude skill; filter the catalog; select
one item; read its source with its exact origin visible. Guide chapters resolve under the
existing guide contract. Return to the catalog or exit. Noninteractive catalog/show operations
must support verification without a TUI. A picker uses existing terminal facilities with a
plain-list fallback; no new UI framework is needed for this slice.

Sources are a declared, inspectable set of roots, established in researcher turn R1:

1. Authored germline under ia-sync/germline, with its existing file kinds preserved.
2. Temple guides under ~/reposoma/raw.guides, honoring GUIDE/res boundaries.
3. Authored Codex/Claude skill trees under ia-sync/codex/skills and ia-sync/claude/skills.
4. Existing user/vendor-system/plugin skill roots explicitly identified from native layout
   or the provided runtime catalog. Include vendor-supplied installed skills when present;
   label them separately from operator-authored skills. No recursive scan of the whole home
   or arbitrary plugin caches. Unsupported/unidentified roots remain explicit gaps.

Each entry exposes kind, name/title, vendor where relevant, exact path, and source/installed
origin when known. Same-named entries remain distinguishable. Reading a source reports no
runtime activation. Unresolved provenance is shown honestly instead of silently choosing a copy.
Missing/empty roots and ambiguous chapter requests have usable, bounded responses.

Candidate implementation scope after operator release:

- `zsh/experimental/source-reader/runner.zsh`: thin lazy entry, offline --help.
- `zsh/experimental/source-reader/source-reader.py`: stdlib discovery/selection/read behavior,
  if that is smaller than shell-only implementation after R1.
- The brick's README and meaningful fixture/CLI checks.
- One new maintainer-log row in `zsh/experimental/base.zsh`, with exclusive ownership of that
  row; no unrelated wiring or alias changes.

The prototype reads sources without rewriting them or executing their instructions. Installing,
porting, building wrappers, deployment and native skill activation are later scopes. Slint/GUI
is a possible second presentation surface; no framework choice or GUI dependency is locked here.

## Vendor facts that constrain the reader

Codex documents repository walk-up `.agents/skills`, user `~/.agents/skills`, admin and bundled
system skills. Same-name skills are not merged. Presence/discovery does not witness selection
of the full skill body. [Official Codex skills](https://learn.chatgpt.com/docs/build-skills).

Claude documents personal/project/plugin skill locations and its own invocation and name
resolution rules. Its skill body loads on use. The reader preserves these differences and
does not translate all vendors into one precedence model.
[Official Claude skills](https://code.claude.com/docs/en/skills).

The local source map is also evidence; historical local paths do not override current vendor
documentation. Conversely, vendor docs do not prove that a particular host has a source or
enabled plugin. Validate the declared roots during R1 without opening auth/history/state.

## Team and two substantive rounds

| role | seat/mechanism | first substantive assignment | second substantive assignment |
|---|---|---|---|
| Architecture/integration | Cartan main | Set the product boundary and resolve actual contract conflicts | Judge product evidence, delegation burden and remaining germline question |
| IT support | Existing native caretaker | Prepare two named consultation threads and receipt-based dispatch | Maintain the same threads through follow-up and reconcile final identities/results |
| Implementation | Native `astrobley` | Implement the accepted source-reader slice and meaningful checks | Address research/audit findings, rerun affected checks and hand off final artifact |
| Research | First named Codex tunnel thread | Establish actual source roots, existing contracts and vendor differences | Check the implemented discovery/provenance against those sources; expose gaps |
| Independent audit | Second named Codex tunnel thread | Challenge the acceptance criteria and identify counterexamples before implementation | Inspect the actual artifact, independently exercise read-only behavior and verdict |

Researchers and auditors are separate threads. Their findings are bounded evidence, never
canonical authority. Auditor gets the agreed brief/source contract, not an obligation to
endorse the researcher's or implementer's conclusion. Each second turn is a real follow-up,
not a liveness ping to satisfy a count.

Round order: caretaker readiness → R1 and A1 → one main architectural disposition → Astrobley
I1 → R2 and A2 on the actual artifact → Astrobley I2. If I2 changes audited behavior, one
bounded auditor recheck A3 verifies the final revision before acceptance. A remaining issue
after that correction returns as a specific decision, not an indefinite retry loop.

Main, caretaker and Astrobley use three native seats; researcher/auditor live behind the
two tunnel threads. Preparation delegates above are not those future live-trial threads.
Begin the actual run in a fresh Cartan root with the short entry/contract packet: this planning
conversation already contains the operating details, so using it cannot demonstrate their
absence from the main's context. Instantiate the existing caretaker role in that root and
reuse its handle within the run; do not assume a child handle transfers across root restart.
Concrete target profiles are selected and recorded at release based on the substantive jobs;
G08's low-effort source checks do not qualify low effort for the whole audit by assumption.

## The capability the main consumes

One short, deploy-inert entry card in the future task bed says:

> Use hold-line for this task's research and audit consultations. Delegate channel setup,
> routing, receipt checks, continuity and bounded recovery to the named caretaker. Ask in task
> language. Return supported findings, contrary evidence, unknowns and required decisions.
> Keep operational logs behind pointers. An uncertain remote outcome never permits resend.

`hold-line` is a proposed local program name, not an installed skill or new global role.
Use the existing role contracts. A live `$hold-line` skill is a later promotion only if the
procedure earns reuse. Main retains navigation, architectural choices and STATUS; it can
inspect narrowed primary evidence when a decision needs it.

Prepared at Majkee's request on 2026-10-26: the loadable test specimen now lives under
`.dev/session/germline-09-source-reader/raw/hold-line/`: main `ENTRY.md`, caretaker
`controller.md`, selected `functions/*.md`, `task.json` and `sources.json`. The shelf has no
live RUNBOOK/STATUS or execution grant. Cold substantive bootstrap precedes arming the global
deployed tunnel preamble for warm turns; source/deployed pins and the older mirror's drift
are recorded. Read the main entry only in the fresh head; mechanics remain with the caretaker.

Caretaker owns all model CLI/app-server operation and per-turn operation IDs. Reuse G08's
receipt-first discipline, adapting the trial-local records to multiple numbered turns per
thread; preserve G08 evidence and source transport. A returned tool message alone is never
completion authority. Recovery is bounded to read/resume/inspection; ambiguous submission,
auth changes, source fixes or scope changes return a hold. No automatic uncertain-send replay.

Only Codex model calls use the existing account. Reading Anthropic skills is source reading;
it does not authorize `claude -p`, an Anthropic SDK, new keys or a new authentication route.

## Predeclared proof and measures

Product acceptance:

- A user reaches and reads an existing item from each available source family through the
  source-tree brick; declared unavailable roots remain visible as gaps.
- Catalog entries and selected source bytes match actual files. Same names across origins
  stay distinct; guide ambiguity is not silently resolved; source/installed copies are labeled.
- Offline help, empty/missing roots, noninteractive output and a plain-list fallback work.
- Read operations leave input trees unchanged; source instructions are displayed as data.
- Relevant syntax/fixture/CLI checks and deploy dry-run pass. No deployment is inferred from
  the dry-run; a fresh deployed-shell witness remains a separate final release if wanted.

Main-context acceptance (the primary experiment):

- After the execution release, expected routine tunnel commands issued by main: **zero**.
  Count every exception and its cause. Genuine decisions and narrowed evidence inspection
  are allowed; log them separately from operational rescues.
- Main initially consumes one entry/contract packet, target **<=800 words**. Role returns
  default to **<=300 words plus evidence paths**; preserve contrary evidence/unknowns even
  when that requires a declared overrun or focused follow-up. These are trial targets, not
  prior measurements or hard truncation rules.
- Record the number/bytes of main-visible returns, full-source opens, operational logs pulled
  into main, and decisions. Use actual artifact sizes; do not invent unavailable native token
  telemetry. Count setup/research preparation separately rather than hiding its cost.
- Auditor tests at least one concrete counterexample involving provenance, duplicate names or
  guide resolution. Check that it survives the caretaker's compression and reaches main when
  consequential. No artificial live tunnel failure is required.
- Final dispositions are separate: PRODUCT PASS/REVISE; DELEGATION USEFUL/REVISE/INDETERMINATE;
  GERMLINE CONTRIBUTION supported/unsupported/indeterminate, with the ordinary-role alternative.

Record target usage/time and native usage if exposed, but set no invented dollar or latency
promise. This one run is not a controlled proof of whole-route savings or permanent memory.
Do not turn failure of the main-context target into product failure, or product success into
proof that the germline architecture is necessary.

## Release and durable execution surface

This document completes the current assessment/planning request. No product code or trial
model turn is released by its existence. After operator selection, prepare a numbered sibling
task bed (candidate `germline-09-source-reader`) with one fixed RUNBOOK gate and Cartan-owned
STATUS, the entry card, disjoint write paths, frozen task prompts and numbered bus cycles.

Proposed gate: Majkee accepts the independently checked read-only source-reader artifact and
a separately evidenced disposition of the main's consultation burden, with no source activation
or architecture promotion implied.

Keep G03's Atlas/source-freeze gate and G07/G08 evidence unchanged. Preserve foreign dirty
work. Read no further Nablarva material, write no global primitive, deploy nothing and perform
no commit/push as part of this plan.
