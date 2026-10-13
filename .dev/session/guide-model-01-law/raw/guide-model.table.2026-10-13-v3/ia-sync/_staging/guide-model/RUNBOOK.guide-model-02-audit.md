# RUNBOOK: guide-model-02-audit

```yaml
goal: >
  A gaveled worklist saying, for every entry in ~/reposoma/raw.guides/, which shape it should have
  (flat · model) and what — if anything — should happen to it, with evidence, so conversion
  sessions can run batch by batch.
gate: >
  Every census entry carries one worklist row with target shape, action and evidence; every "?" row
  and every auditor↔recreator disagreement is gaveled by majkee; worklist.md and report.md are on disk
  in the bed, and the promotion manifest carries them to ~/reposoma/raw.guides/guide-writing/raw/
  before prune.
participant_1: [head, {brand: <bind — codex or claude; the cSharp holder>, model: <bind>, effort: high}, host: <bind>, role: "cSharp — navigator and status_owner; binds the seats, tests what comes back; never writes rows"]
participant_2: [auditor, {brand: claude, model: <bind>, effort: high}, host: <bind>, role: "taskline — walks the tree and proposes every row; writes only worklist.md and report.md"]
participant_3: [recreator, {brand: <bind — another incarnation; the other vendor decorrelates best>, model: <bind>, effort: high}, host: <bind>, role: "standing witness — the seat that will rewrite; reconsiders rows during the walk; never edits"]
participant_4: [majkee, {brand: human}, host: <bind>, role: "gavels disagreements and the frozen worklist as one batch"]
status_owner: head
head_note: "cSharp — this seat authored the RUNBOOK and stays live through the whole arc as navigator and status_owner; it may delegate every body of work and receive only navigation + test parts; it closes the session if it can."
observations_read: <head fills: ls ~/ia-sync/.dev/observations/guide-model* — what 01 left, or "none exist">
# precedent seats, not an assignment: oraculum (audit-loop card) · atlas-ui (germline forge) · cartan (cross-vendor check)
```

## Why this session exists

Most guides were written as documents to read. Some are consulted for several different jobs, and
every reader pays for all of them. guide-writing now says which guides earn the model shape
(`/guide guide-writing`, converted in guide-model-01-law). Nobody has held the whole tree against
it. This session decides, row by row, with evidence — and changes nothing.

## Fixed facts

- **Yardstick:** guide-writing as gaveled in 01. The law decides — not this RUNBOOK, not taste. If the
  law looks wrong mid-walk, that is a finding for majkee, never a patch.
- **Method:** the temple audit loop, specialised (`~/reposoma/raw.guides/audit-loop.card.draft.md`):
  auditor ≠ recreator · the audit writes nothing into canon · challenge before report · blind before
  grounded · an audit that cannot fail is show.
- **Order (majkee, 2026-10-13, review R2):** this whole-tree pass runs before any conversion; the
  per-guide line starts from its frozen worklist. Do not pipeline audit and conversion.
- **Timebox:** one pass over the tree. A re-walk is a new sibling session. If this audit spawns tooling
  beyond the census, it has failed (temple-audit seed law).
- **Census:** `python3 ~/ia-sync/_staging/guide-census.py ~/reposoma/raw.guides` — read-only, facts
  only, never verdicts. Receipt 2026-10-12: 39 entries · 26 slug folders · 6 folders without
  `GUIDE.md` · 7 loose files.
- **Exception zones (guide-writing law):** published mirrors (`<!-- PUBLISHED MIRROR` banner) →
  `route`, never converted here. Legacy loose files migrate on a real touch, never in bulk — a
  conversion is a real touch; a flat-and-fine loose file stays loose unless majkee gavels otherwise.
- **Ownership:** `~/reposoma/raw.guides/sella/` is promotion-gated doctrine with a Cartan mount — report
  on it; its verdict is majkee's. `~/ia-sync/codex/**` is Cartan's turf — POINT, never edit.
- **Head:** the cSharp protocol (`/guide runbook csharp-head-protocol`) — a posture, not a seat; a
  change of holder follows its transfer ritual.
- **The uncanonical layer** (`raw/`, `src/`, journals) is registered and pointed to — never judged for
  rewrite.

## Verdict vocabulary

One row per census entry. **Shape:** `flat` · `model` · `?`. A `model` row lists at least two
occasions with evidence, or it is not model. **Action**, exactly one:

| action | means |
|---|---|
| `none` | fine as it stands |
| `conform` | metadata only — frontmatter, manifest lines, `chapter-of:`, `shape:`, dangling pointers |
| `convert` | collapse to model (guide-writing's convert function) |
| `split` | two topics in one slug → two guides |
| `merge → <entry>` | same topic as another entry |
| `retire` | superseded or tombstone — per guide-writing's legacy law |
| `route → <owner>` | mirror or project-owned content — the fix belongs at its source |

**Flags:** the law's defect codes — L1–L4 meaning · C1–C4 chain · K1–K5 compression — each with
`path:line`.

## Worklist row format

`~/ia-sync/.dev/session/guide-model-02-audit/worklist.md` — the pasted census first, then:

```text
### NN · <entry>   (<kind> · <lines> lines · <n> res)
- occasions: (1) <job> — <path:line> · (2) …        ← required for model; "one: <job>" for flat
- shape: <now> → <target>
- action: <one action>
- flags: <codes, each with path:line>
- reason: <one or two lines — the claim; the evidence stays in the lines above>
- recreator: agreed | counter — <one reason>
- gavel: <majkee's word, when needed>
```

## prompt-0 — head

```text
You are the head of guide-model-02-audit, in the cSharp posture (/guide runbook csharp-head-protocol).
Bed: ~/ia-sync/.dev/session/guide-model-02-audit/ — you own STATUS; you never write rows.
1 · If you did not head 01, read the experience transfer majkee carries from 01, and the
    observations_read line, before binding seats.
2 · Bind the seats in the front-matter. Hand prompt-1 to the auditor and prompt-2 to the recreator.
3 · Record the auditor's stress line; write every STATUS claim as a path the recreator can test.
4 · Gate when the gate line is observably true. Before prune: the experience transfer into
    <bed>/raw/, and a promotion manifest that moves worklist.md and report.md to
    ~/reposoma/raw.guides/guide-writing/raw/ (scar 4).
```

## prompt-1 — auditor

```text
You are the auditor of guide-model-02-audit.
Bed: ~/ia-sync/.dev/session/guide-model-02-audit/
You write only <bed>/worklist.md and <bed>/report.md; STATUS belongs to the head — report to it.
You edit no guide, chapter, skill, journal or template anywhere.

0 · STRESS FIRST. SB=$(mktemp -d); cp -r ~/reposoma/raw.guides/. "$SB"/ — a fresh directory you
    own; use "$SB" for every step. Plant one dead res/ pointer in a GUIDE.md, one unregistered
    res/ file, one undeclared directory. Run the census on "$SB": all three must show. Report
    PASS/FAIL to the head, then rm -rf "$SB" — that directory only. Any miss → stop and report:
    the census is not fit to lean on.
1 · CANON READ. /guide guide-writing — the controller and its functions for deciding shape and for
    converting · ~/reposoma/raw.guides/audit-loop.card.draft.md · this RUNBOOK.
2 · CENSUS on the real tree; paste its output under "## Census" in worklist.md. Mechanical facts
    start from here — its header lists what it checks and what it does not. Verify by reading
    anything it flags oddly, and anything outside its checks.
3 · WALK — one row per census entry, in this order:
    guide-writing (confirm the 01 conversion) · guide-publishing.md · audit-loop.card.draft.md ·
    harness-check · gloss · runbook · status · PAD · bus · cold-start-card · the rest
    alphabetically · sella last.
    Per entry: read GUIDE.md whole; chapters by header and first screen; raw/, src/ and journals by
    name only. Ask the occasion question first: what different jobs do readers bring here? Then fill
    the row. Cannot decide with evidence → shape "?" — never guess.
4 · RECONSIDERATION, DURING the walk — not after. Send the recreator every "?" row and every fifth
    confident row: the row as written plus its census line — by the bus (/guide bus), or over the
    TABLE if the recreator is a Codex seat majkee opened one for (/guide tunnel). Record the answer in the
    row. A counter keeps both reasons in the row and goes to majkee.
5 · HORIZONTAL FINDINGS — one invariant across the whole tree → report.md, not rows:
    H1 frontmatter law vs practice: which no-YAML guides are gaveled canon using backtick headers
    H2 the src/ ↔ raw/ seam in use: evidence for or against slug-directories' recorded lean
       (src/ folds into raw/) — report, don't solve
    H3 manifests naming files that no longer exist; manifest headings that differ from the law's
    H4 folders without GUIDE.md: guide, record or data — and where each belongs
    H5 topic overlap between entries — merge candidates, from your own reading
6 · RECONCILE — only after your walk is frozen: majkee hands you hypotheses.reconcile-only.md. One
    line per hypothesis: converge · diverge · not testable — with the row it touches.
7 · FREEZE + RETURN. Every row agreed or gaveled. report.md in RETURN shape: counts per action and
    shape · top findings · ownership map (rows needing a Cartan POINT, rows needing majkee) ·
    proposed conversion batches · what you did NOT touch. Files first, then the word: both stay
    in the bed; tell the head and majkee their paths. Never cite _mail/*/inbox/ in either file —
    mail is consumed.
Done when the gate line is observably true.
```

## prompt-2 — recreator

```text
You are the recreator of guide-model-02-audit — the seat that will run the conversions later. You
reconsider; you never edit. First read /guide guide-writing (the controller and its convert
function). For each row the auditor sends, answer in one line: agree, or counter with ONE reason.
Test the row from your side: could you actually convert this guide by the law? Are the occasions
real and distinct, would each function finish its job alone, is there a story worth a BACKGROUND?
Ask for the evidence a row lacks rather than supplying your own leaning.
You never see hypotheses.reconcile-only.md.
```

## Proposed batch order — the report applies it; the next head authors the sessions

1. `convert` rows that other guides lean on (session-shape canon) — each still its own gavel.
2. `convert` rows flagged L2 (lazy safety line) or K3 (teaching bloat) — the biggest gain.
3. `conform` rows — cheap; still one guide per commit.
4. `merge` · `split` · `retire` · `route` — each needs majkee's word.
5. sella — only by majkee's word, with Cartan in the loop.

One session per batch, one gate per session: `guide-model-03-…`, `-04-…`.

How a batch runs — majkee's arrangement (2026-10-13), which is the cSharp protocol's three postures:
the **head** (cSharp; Cartan likely first, transferable) releases one guide at a time from the frozen
worklist; each guide gets a fresh **taskline** group holding only `/guide guide-writing`, the guide
and its row, and carrying the conversion whole; a Claude seat in the **consultant** posture audits
each conversion alongside, in its own stream — collapse map, census, witness — and counter-signs it.
A Codex seat editing temple guides works an agreed task named in the batch RUNBOOK (HANDSHAKE: on
Claude turf, Cartan edits within an agreed task).

## Known constraints + destructive holds

- Read-only on `~/reposoma` and `~/ia-sync` apart from the bed. One exception, the head's, after
  majkee's gavel: promote worklist.md and report.md to `~/reposoma/raw.guides/guide-writing/raw/`,
  move session-process keepers per scar 4, and prune the bed per the runbook's gate-closure law.
  No guide canon changes.
- A seat that has read `hypotheses.reconcile-only.md` before step 6 cannot be bound as auditor or
  recreator — that excludes this program's authoring thread and Wave's 2026-10-13 conversation.
- Blind before grounded: `hypotheses.reconcile-only.md` stays outside the bed until step 6; the
  recreator never sees it.
- Cost: the census replaces reading for the facts it checks; chapters get a first screen, not a
  full read, unless the occasion question needs more.
- No follow-up RUNBOOKs here — proposing batches is the output.

## Acceptance evidence

- STATUS: the stress line — three of three plants caught.
- `worklist.md`: the census, then one row per census entry (the counts match); no row without
  evidence; every `model` row lists two or more occasions; no `?` left.
- `report.md`: H1–H5 · the reconcile lines · counts · batches · ownership map · NOT-touched list.
- `git -C ~/reposoma status` and `git -C ~/ia-sync status` show nothing outside the bed.
- worklist.md and report.md on disk in the bed; the promotion manifest names their destination in
  `~/reposoma/raw.guides/guide-writing/raw/`; no `_mail/*/inbox/` path cited in either.
- The head's experience transfer on disk in `<bed>/raw/` before prune.

## References

- `~/reposoma/raw.guides/guide-writing/GUIDE.md` — the yardstick, after 01
- `~/reposoma/raw.guides/audit-loop.card.draft.md` — the method
- `~/reposoma/raw.guides/guide-publishing.md` — mirrors and routing
- `~/reposoma/raw.guides/gloss/GUIDE.md` — what BACKGROUND is not
- `~/reposoma/raw.guides/guide-writing/res/write-background.md` — what a BACKGROUND must and must not hold
- `~/reposoma/raw.guides/germline-forge/res/witness.md` — the witness protocol conversions will use
- `~/reposoma/raw.guides/runbook/res/csharp-head-protocol.md` — the head posture and transfer ritual
- `~/ia-sync/HANDSHAKE.md` — POINT and ownership by surface
- `~/ia-sync/_staging/guide-census.py` — the census

## What this session deliberately does not do

- Convert, conform, migrate, merge, retire or delete anything in the guide tree — the head's
  closing promotion and bed prune are the only writes outside the bed.
- Patch the law — a law problem is a finding; 01 re-opens by majkee's word.
- Decide sella.
- Build any tool beyond the census.
