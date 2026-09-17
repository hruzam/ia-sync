# RUNBOOK: cold-start-card system grows an issue category (Claude + Codex)

```yaml
goal: >
  Extend the cold-start-card SYSTEM so it also carries "issue" cards — same vault, same
  mechanism, a different category — not the parallel _issues/ vault built earlier this
  session. A new issue-card skill (sibling of cold-start-card) plus lockstep edits to the
  cold-start-card skill AND its GUIDE. Claude side by atlas-ui; Codex side by Cartan over
  the tunnel. Issue cards carry >=7 associations (in frontmatter AND a one-sentence
  description) and a durable sort key.
gate: >
  A fresh Claude session (updated skill) and a fresh Codex session (tunnel-delivered skill)
  each drop AND re-locate BOTH an issue card and a cold-start card in the one shared vault;
  the gaveled cold-start-card GUIDE carries the issue category, the sort-key rule
  (name vs frontmatter) and its unsorted fallback; and the standalone _issues/ vault from
  this session is reconciled into that shape (folded or kept — majkee's category call).
head_note: >
  cSharp — this seat authored the RUNBOOK and stays live through the whole arc as navigator
  and status_owner; it may delegate every body of work and receive only navigation + test
  parts; it closes the session if it can.
participant_1: [trajectory, {brand: "Claude Code", model: sonnet, effort: high}, host: "home", role: "cSharp head — first-in last-out navigator + single status writer; delegates bodies whole, never authors the skill itself"]
participant_2: [atlas-ui, {brand: "Claude Code", model: sonnet, effort: high}, host: "home", role: "phase-1 taskline — carries the Claude skill + GUIDE body whole"]
participant_3: [cartan, {brand: "Codex CLI", model: gpt-5.6-sol, effort: high}, host: "home", instrument: tunnel, role: "phase-2 taskline — carries the Codex skill + harness body whole"]
participant_4: [assay, {brand: "Claude Code", model: sonnet, effort: high}, host: "home", role: "standing witness — natively sees every diff across BOTH repos; test -f's the head's STATUS claims, counter-signs the gate; NOT a builder (crossed witnesses)"]
participant_5: [majkee, {role: "transport + gavel — switches the head's model, opens the tunnel between phases, wakes every seat, gavels the GUIDE change"}, host: "home"]
status_owner: trajectory
schema_note: "runbook GUIDE manifest as of 2026-09-17; head protocol = res/csharp-head-protocol.md (GAVELED 2026-09-04); cross-vendor instrument = res/cross-vendor-seat.md (DRAFT) + raw.guides/tunnel/GUIDE.md"
```

## Why this session

Two turns ago the operator asked for an issue-card mechanism. It was gated (Janus + Codex/
@mirror both said central-in-reposoma, not per-project) and BUILT this session as a standalone
`~/reposoma/_issues/` vault (reposoma commit `6e26f63`, ia-sync `6aa67de`). TURN 2 then
reframed it: an issue is **not a separate mechanism** — it is the cold-start-card mechanism
with a different **category** ("same vault, because same mechanism"). So the standalone vault
is now the wrong shape and this session folds it back into the cold-start family, and grows
that family cross-vendor (Claude skill + GUIDE, then Codex skill + harness).

TURN 2 also voided Janus's one open flip-condition: "reposoma will always travel with my
project — that is knowledge, this is the way." A project never has reposoma absent, so no
local-only consumer can ever need project-local issue files. Central is now unconditional.

## The three directive facts (from TURN 2 — settled, not open)

1. **Same vault, same mechanism, new sibling skill.** `issue-card` is a NEW skill *similar to*
   `cold-start-card`, writing into the SAME vault under an issue category — not a second vault,
   not a fork of the mechanism.
2. **>=7 associations per issue**, expressed in BOTH the frontmatter AND a one-sentence
   description ("know, not said" — tacit discriminators an agent can filter on without opening
   the body). The sort script only needs the date; the extra associations do not complicate it.
3. **Lockstep.** The existing `cold-start-card` skill AND its GUIDE change in the same pass as
   the new issue-card skill — one family, one GUIDE, kept coherent.

## The ONE open design question (phase 1 settles it WITH majkee — do not silently resolve)

**Category shape + sort key.** The cold-start vault's folders (`card/` `routines/` `archive/`)
are STATES. An issue also has state (open / parked / resolved). So the builder must decide, with
majkee, how "category" and "state" compose in one vault. Two candidate shapes, pick one:
  - (a) category by filename prefix + `kind:` frontmatter (`ISS.*` vs `CS.*`), sharing the same
    state folders; or
  - (b) an issue subtree with its own state folders under the shared vault root.

And the sort key itself — **by name or by frontmatter?** Carry the research verdict (see
References → `raw/date-name-frontmatter.md`, Epoch + ChatGPT): **filename is the durable radar**
(a date in the name survives clone/checkout/host-move; mtime does not — different epistemic
classes), **frontmatter is the richer manifest**, body is the payload. Lean: sort by the
filename date as primary; the >=7 associations live in frontmatter. **Any card lacking the
marked sort key lands in an UNSORTED bucket** (the drift-detector pattern the `keys`/claviature
engine already uses) rather than being silently mis-ordered.

## CLOSED 2026-09-17 — majkee's answer, amends phase 1's draft (before phase 2 builds)

Phase 1 (@atlas-ui) drafted `issues/{open,parked,archive}` — a subtree, option (b), sort by
filename date. Majkee confirmed the subtree call AND added scope atlas-ui's draft does not
yet have. Recorded verbatim-in-spirit, four points:

1. **New category needed: a "how to react" knowledge layer for repetitive/recurring defects**
   — not the same thing as an `open`/`parked`/`archive` dated incident card. This is what
   cold-start's `routines/` already IS (dateless, never archived, recurring glue) — same
   principle, issue-scoped. **Add `issues/reactions/` — dateless, never archived, filename
   `IR.<slug>.md` (mirrors `RT.<slug>.md` exactly: no date, it recurs).** A reaction card
   answers "we've seen this pattern before, here's how to handle it" — distinct from a dated
   incident card in `open/`/`parked/` which answers "this specific instance happened on X."
   Resolved dated incidents still go to `archive/` as already built — confirmed correct, no
   change needed there.
2. **Standing coupling invariant, not just today's symmetry call.** Cold-start's vault location
   and issue's vault location move together, always, in the same commit — never independently.
   This is a LAW to write once into the GUIDE next to the vault tree (one line), not a
   dedicated follow-up task — folded into the amendment below.
3. **>=7 associations is a RULE, locked** — not a guideline. Trajectory's read, asked for
   directly: do not raise the floor above 7; more tags become upkeep burden for marginal
   retrieval gain, against this family's own smallest-safe-solution doctrine. 7 stays the
   floor; a card is free to carry more if it naturally has more, but 7 is not raised.
4. **Tunnel is live** — phase 2 (@Cartan) is unblocked, but sequenced AFTER this amendment so
   Codex builds against the true final spec, not phase 1's now-incomplete draft.

**Delegated as a surgical, well-defined follow-up to @Delta** (not atlas-ui again — the shape
is now fully specified, zero open judgment left): add `issues/reactions/` to the new skill +
the GUIDE draft (still `[ISSUE-DRAFT]`, still no self-gavel) + the coupling-invariant line.
@assay witnesses this together with phase 2's return, batched (token economy).

## Phase 1 — @atlas-ui (Claude), spawned by @Trajectory on majkee's go

Prompt (copy-paste; absolute paths; atlas-ui writes to the surgical table `~/ia-sync/`, never
live `~/.claude/`):

```
You are @atlas-ui building the issue-card addition to the cold-start-card SYSTEM, host home,
surgical table ~/ia-sync. Read first, in order:
  ~/reposoma/raw.guides/cold-start-card/GUIDE.md        (the law you are extending)
  ~/ia-sync/claude/skills/cold-start-card/SKILL.md      (the sibling skill to match + edit)
  ~/reposoma/_issues/README.md + the two seed cards      (what folds in)
  ~/ia-sync/.dev/session/cs-card-sys-update/RUNBOOK.md   (this file — the three facts +
                                                          the one open question)
Build:
  1. A NEW skill ~/ia-sync/claude/skills/issue-card/SKILL.md — sibling of cold-start-card,
     SAME vault, issue category, >=7 associations in frontmatter + a one-sentence description,
     durable sort key, UNSORTED fallback for cards missing it.
  2. Lockstep edits to ~/ia-sync/claude/skills/cold-start-card/SKILL.md AND
     ~/reposoma/raw.guides/cold-start-card/GUIDE.md so the family is coherent (category system,
     sort rule, unsorted rule) — the GUIDE is CANON: draft the change, do NOT self-gavel;
     majkee gavels.
  3. Fold ~/reposoma/_issues/ into the decided shape. Do NOT delete the two seed cards —
     migrate them. Reversible: leave the old path until the new shape is proven.
Settle the ONE open question (category-vs-state shape + name-vs-frontmatter sort) WITH majkee
before writing the schema — it is his call, carry the research lean, do not assert through it.
Do not deploy. Do not commit. Report what changed + the unresolved decision if any.
```

## Phase 2 — @Cartan (Codex) over the tunnel, after majkee opens it

Same task, Codex-native. Cartan reads the cold-start-card GUIDE (shared law) and builds the
Codex surface — never copies the Claude skill. Prompt authored into the tunnel per
`~/reposoma/raw.guides/tunnel/GUIDE.md` when the tunnel is live (not pre-written here — the
tunnel handle and enable layer are majkee's to open; see `res/cross-vendor-seat.md`).

```
You are @Cartan, first-class Codex participant, host home, working dir ~/ia-sync. Read the
shared law ~/reposoma/raw.guides/cold-start-card/GUIDE.md (as amended in phase 1) and the
Claude skill pair as REFERENCE, not to copy. Build the Codex-native issue-card surface under
~/ia-sync/codex/skills/ + any codex harness wiring it needs, expressing the SAME vault /
category / sort / unsorted rules in Codex's own primitives. A new Codex primitive is proven
only from a FRESH Codex session (0009 L5) — dry-run + verify before it is called live. Draft
canon; do not gavel. No commit, no deploy.
```

## cSharp discipline (this arc runs the gaveled head protocol)

- **Standing witness = @assay** (participant_4). It sees every diff across `~/ia-sync` and
  `~/reposoma`; the head's STATUS claims are written as paths @assay can `test -f` / `git diff`,
  and it counter-signs the gate. The head's own STATUS is its least-verified surface — a named
  peer fixes that, not the head's own rigor. @assay never builds here (a witness of its own work
  is no witness).
- **Head is navigator, not author.** @Trajectory delegates the skill bodies whole to atlas-ui
  (phase 1) and Cartan (phase 2) and receives back only navigation + test parts. Reaching into a
  delegated skill file voids the delegation — the head does not edit `issue-card/SKILL.md`.
- **The four scars — taken free, not re-derived** (roster-reform-01-triad):
  1. STATUS claims are testable paths a peer verifies.
  2. A RETURN that exists only in chat closes nothing — files first, then the word.
  3. Never cite `_mail/*/inbox/` in durable artifacts — durable evidence lands in the bed's
     `raw/` or the temple evidence home.
  4. Before any prune: an explicit promotion manifest naming EVERY `raw/` keeper.
- **Transfer ritual at close.** The sitting head authors an experience-transfer into this bed's
  `raw/` (five blocks: inherited head_note · what to read · counter-signed rules · scars priced ·
  the one lesson) — majkee carries it to the next cSharp. Chat is not a record.

## Side quest, parked — converging pattern, NOT in this arc's gate

Pulled from office over tailnet 2026-09-17 (scp, read-only, origin
`/tmp/metaterminal-20260916-012151/brief.agentive-help.instruction.md`, written by
@Metaterminal): a brief for `agentive-help` — a phone-side Termux lookup viewer for
`devices/_shared/termux/`. Full text lives at its permanent home,
`devices/_shared/brief.agentive-help.instruction.2026-09-16.md` (moved out of this arc's
`raw/` — it's not this arc's substrate, just parked here for the pull).

**Why majkee called it converging, not identical:** same underlying shape as this arc — a
small, editable, categorized tree of short markdown notes
(`help/<category>/<topic>.md`, 2 levels) plus a lookup mechanism with a no-args-degrades-to-
menu behavior, additive-only discipline, absolute-path law. Different audience (phone
keyboard via tmux popup/buffer, not an agent's frontmatter-first scan) and a fully separate
deliverable (`devices/_shared/termux/`, PUSH-only to devices, no relation to the
cold-start/issue-card vault or reposoma). Worth reading for cross-pollinated ideas (the
no-args → menu degradation is a clean analogue to this arc's UNSORTED-bucket fallback), NOT
worth merging into this gate.

**Explicitly out of scope here.** The brief's own "who does what" section says routing is
majkee's call — "new small session/task or an addendum inside a future
`codex-remote-control-cli-0N` sibling" — not this arc. Not actioned, not routed, just
carried as context per the operator's ask.

## Known constraints + destructive holds

- **GUIDE is canon (reposoma).** Any `cold-start-card/GUIDE.md` edit is DRAFT until majkee
  gavels (0002 · Force 4). Neither builder self-locks it.
- **Never delete the seed cards.** `_issues/open/ISS.ts-mount-double-daemon-no-guard.2026-09-16.md`
  and `_issues/parked/ISS.larva-scripts-dir-missing.2026-07-29.md` are real backlog — migrate,
  leave the old path until the new shape is proven, then remove in a reviewed commit.
- **Compose-first.** atlas-ui authors on `~/ia-sync/` (surgical table); live `~/.claude/` /
  `~/.codex/` are deploy targets, never authoring sources.
- **No commit / push / deploy from any builder.** Those are majkee's, after the gate proof.
- Two repos move here: skills + this session live in `~/ia-sync` (branch `main`), GUIDE +
  vault + seed cards in `~/reposoma` (branch `core`). Pull-before-push discipline on both.

## References (point, never copy)

- `~/reposoma/raw.guides/cold-start-card/GUIDE.md` — the law being extended; "folder=state, no
  status: field", filename law, frontmatter-as-truth
- `~/ia-sync/claude/skills/cold-start-card/SKILL.md` — the sibling to match + edit
- `~/reposoma/_issues/README.md` + `open/` + `parked/` — this session's build that folds in
- `~/ia-sync/.dev/session/cs-card-sys-update/raw/date-name-frontmatter.md` — Epoch + ChatGPT
  research: radar(filename) / manifest(frontmatter) / payload(body); mtime is non-authoritative;
  date-in-name survives clone (the sort-key evidence)
- `~/reposoma/raw.guides/tunnel/GUIDE.md` + `raw.guides/runbook/res/cross-vendor-seat.md` —
  how the phase-2 Codex tunnel opens
- reposoma `6e26f63` · ia-sync `6aa67de` — the standalone `_issues/` vault this session reverses

## What this session deliberately does NOT do

- Build the cs-palette / temple-cs-manage TUI equivalents for issues — not asked; a later pass.
- Deploy or commit anything — the runbook head parks; builders draft; majkee gates and lands.
- Resolve the category-vs-state shape by inference — that is phase 1's decision WITH majkee.
