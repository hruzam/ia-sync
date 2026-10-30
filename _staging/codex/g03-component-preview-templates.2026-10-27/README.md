# G03 — component preview template candidates

> Re-entry pointer added 2026-10-29: read [the dated handoff](HANDOFF.2026-10-29.md) for the
> packet map, revised recommendation and preservation record. The initial comparison below
> is retained; later proposals 08–10 carry the developed design.

Drafts for Majkee's review, 2026-10-27. Author: Cartan(G03), office.
These are deploy-inert examples under ia-sync/_staging/codex/. They do not amend germline,
native skills/agents, project authority, G03's audit inputs or G09's frozen trial.

## What was thought before reading

[00.before-reading.md](00.before-reading.md) records the initial alternatives and the
ordered-union idea, captured before further source or documentation reads in this turn.
The initial five-field minimum was then narrowed to a familiar two-field candidate A.

## Three alternatives

| Candidate | Files | Benefit | Cost / consequence |
|---|---|---|---|
| A: skill-style minimum | [01.skill-style.template.md](01.skill-style.template.md) | Small name/description preview; familiar authoring shape | Richer previews need explicit body-section extraction or a mapping; a controller/card does not become a native skill merely by using this header |
| B: richer neutral component | [controller](02.controller.template.md), [function](03.function.template.md), [card](04.card.template.md) | One file carries typed identity, scope, selection, dependency and output metadata | More authoring/validation and potential repetition; this proposed header needs our own reader and must not be assumed acceptable as native SKILL.md frontmatter |
| C: adapt existing formats | [05.legacy-mapping.example.yaml](05.legacy-mapping.example.yaml) | Existing source files remain intact; normalizes what they already declare | Small adapter upkeep; unknown descriptions/dependencies remain missing, and derived identity needs provenance |

My lean: use C to preview today's corpus; use A for simple new methods. Trial B only where
scope/dependency previews demonstrably help. Let one reader-owned collection definition serve
all candidates, rather than copying view definitions into every component. No format choice
is locked by this packet.

### What the vendor comparison actually establishes

OpenAI documents progressive disclosure through skill name/description, then the selected
SKILL.md body; optional agents/openai.yaml carries additional interface/policy/dependency
configuration. Candidate A borrows the discovery shape. It is not a native installation or
runtime witness. [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills)

Claude Code documents additional frontmatter fields, including a metadata map for custom
tooling. Its documentation distinguishes the fields accepted by Claude Code from the smaller
set accepted in other skill packaging/upload paths. Rich custom fields are therefore not
automatically portable. [Claude Code: Skills, frontmatter](https://code.claude.com/docs/en/skills#frontmatter-reference)

The cumulative collections proposed here are our reader design. These sources do not establish
that either vendor implements these collection names or merge rules. Native agent TOML,
native skill envelopes and germline component meaning remain separate representations.

## One file can expose several cumulative collections

Yes. B's controller example contains all fields once. A reader can project progressively more:

```text
catalog = kind + name + description + observed source path
select  = catalog + id + scope + use_when + maturity
inspect = select + loads + outputs + authority + context + stamp + observed source hash
revision = catalog + stamp + observed source hash
```

[06.collections.example.yaml](06.collections.example.yaml) gives the exact proposed field
paths and composition rules. Collections can be requested together: select + revision uses
the ordered union, without repeating catalog fields. A separate request reads the body.

For example, catalog for the controller candidate would expose:

```yaml
kind: controller
name: example-tunnel-caretaker
description: Coordinate prescribed consultation operations and return concise evidence to the task head.
source.path: <observed path of 02.controller.template.md>
```

Select adds scope and trigger metadata. Inspect additionally shows dependencies and the
return contract's metadata. Merely inspecting loads does not read those files or invoke
a function; the actual governing loader and assignment determine any load plan.

### Proposed deterministic rules

1. Expand included collections before local fields; preserve declaration order.
2. Deduplicate field paths, retaining their first occurrence. Preserve nested list order.
3. Report missing fields explicitly as null plus origin/missing information. Do not invent
   an authored description from a heading or silently rename scope as description.
4. Reject duplicate YAML keys, unknown included collections and include cycles.
5. A reader can retain unselected fields without putting them into the model's preview.
   Unknown extension fields do not silently enter an existing collection.
6. Cross-file results remain separate records with provenance. Field collection is not
   last-writer-wins semantic inheritance; disagreements remain visible.
7. Preserve the loader's actual identity/binding/project/card order. A collection supplies
   information; it does not enlarge write scope, select a card or grant operations.

The helper can parse the full header locally while sending only the requested projection to
the model. This targets model context intake, not fewer physical bytes read. No token, cost,
latency or retained-context benefit is claimed without measurement.

## What these drafts intentionally expose

- Rich headers contain unresolved angle-bracket paths, maturity draft and stamp null.
  They are templates, not stamped deployable components.
- The collection definitions live with the proposed reader, outside component content.
  Separate collections in one header would also be possible, at the cost of repeated policy.
- C maps today's Houston card fields directly, but keeps its absent description missing.
  It maps the G09 controller/function title explicitly; prose is not silently interpreted as
  structured authority or dependencies.
- A bounded excerpt can supplement a legacy preview if labelled as source text with its
  range/truncation. Such an excerpt is not a substitute for the complete selected contract.
- Existing controller context policy already calls for first-use reads and named deltas;
  B makes that policy inspectable. Missing context still requires reconciliation.
- Runtime-specific model, tool, invocation and hook settings stay in their native bindings.
  A browsing helper displays source text and does not evaluate embedded source commands.

## Verification and decision edge

This packet is suitable for reviewing formats and rules. Local drafting checks parsed all
four template headers and both YAML examples, expanded catalog/select/inspect/revision to
4/8/14/6 distinct ordered fields, distinguished a missing field from an explicit null, and
confirmed all three mapped source examples exist. At that check, all 418 protected file
hashes matched the before-state, including G03/G09 inputs and foreign dirty work.
No production reader, native installation, runtime invocation, live task change, deployment
or performance claim follows from these checks.

For adoption, Majkee would select the format and the first concrete consumer. The next bounded
implementation should demonstrate a catalog/select/inspect projection over a card, a controller
and a function, with provenance and missing fields visible. G09 inputs remain untouched.
