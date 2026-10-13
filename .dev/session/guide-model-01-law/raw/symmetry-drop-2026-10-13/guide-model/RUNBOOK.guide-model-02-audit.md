# RUNBOOK: guide-model-02-audit

```yaml
goal: >
  A gaveled worklist saying, for every entry in ~/reposoma/raw.guides/, which shape it should have
  (flat · model) and what — if anything — should happen to it, with evidence, so conversion
  sessions can run batch by batch.
gate: >
  Every census entry carries one worklist row with target shape, action and evidence; every "?" row
  and every auditor↔recreator disagreement is gaveled by majkee; worklist + report are filed by path
  to the inbox majkee names.
participant_1: [auditor, {brand: claude, model: <bind>, effort: high}, host: <bind>, role: "walks the tree and proposes every row; writes only worklist.md, report.md, STATUS.md"]
participant_2: [recreator, {brand: <bind — another incarnation; the other vendor decorrelates best>, model: <bind>, effort: high}, host: <bind>, role: "the seat that will rewrite — reconsiders rows during the walk; never edits"]
participant_3: [majkee, {brand: human}, host: <bind>, role: "gavels disagreements and the frozen worklist as one batch"]
status_owner: auditor
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

## prompt-0 — auditor

```text
You are the auditor of guide-model-02-audit.
Bed: ~/ia-sync/.dev/session/guide-model-02-audit/
You write only <bed>/worklist.md, <bed>/report.md and <bed>/STATUS.md. You edit no guide, chapter,
skill, journal or template anywhere.

0 · STRESS FIRST. cp -r ~/reposoma/raw.guides /tmp/ga-sandbox. Plant one dead res/ pointer in a
    GUIDE.md, one unregistered res/ file, one undeclared directory. Run the census on the sandbox:
    all three must show. Record PASS/FAIL in STATUS, then rm -rf /tmp/ga-sandbox. Any miss → stop
    and report: the census is not fit to lean on.
1 · CANON READ. /guide guide-writing — the controller and its functions for deciding shape and for
    converting · ~/reposoma/raw.guides/audit-loop.card.draft.md · this RUNBOOK.
2 · CENSUS on the real tree; paste its output under "## Census" in worklist.md. Mechanical facts
    come from here — do not re-derive them by reading.
3 · WALK — one row per census entry, in this order:
    guide-writing (confirm the 01 conversion) · guide-publishing.md · audit-loop.card.draft.md ·
    harness-check · gloss · runbook · status · PAD · bus · cold-start-card · the rest
    alphabetically · sella last.
    Per entry: read GUIDE.md whole; chapters by header and first screen; raw/, src/ and journals by
    name only. Ask the occasion question first: what different jobs do readers bring here? Then fill
    the row. Cannot decide with evidence → shape "?" — never guess.
4 · RECONSIDERATION, DURING the walk — not after. Send the recreator every "?" row and every fifth
    confident row: the row as written plus its census line — by the bus (/guide bus), or over the
    TABLE if the recreator is a Codex head majkee opened (/guide tunnel). Record the answer in the
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
    proposed conversion batches · what you did NOT touch. File worklist + report by path to the
    inbox majkee names; STATUS points there.
Done when the gate line is observably true.
```

## prompt-1 — recreator

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

## Known constraints + destructive holds

- Read-only on `~/reposoma` and `~/ia-sync` apart from the bed.
- Blind before grounded: `hypotheses.reconcile-only.md` stays outside the bed until step 6; the
  recreator never sees it.
- Cost: the census replaces reading for mechanical facts; chapters get a first screen, not a full
  read, unless the occasion question needs more.
- No follow-up RUNBOOKs here — proposing batches is the output.

## Acceptance evidence

- STATUS: the stress line — three of three plants caught.
- `worklist.md`: the census, then one row per census entry (the counts match); no row without
  evidence; every `model` row lists two or more occasions; no `?` left.
- `report.md`: H1–H5 · the reconcile lines · counts · batches · ownership map · NOT-touched list.
- `git -C ~/reposoma status` and `git -C ~/ia-sync status` show nothing outside the bed.
- Worklist + report filed by path; STATUS points to the filing.

## References

- `~/reposoma/raw.guides/guide-writing/GUIDE.md` — the yardstick, after 01
- `~/reposoma/raw.guides/audit-loop.card.draft.md` — the method
- `~/reposoma/raw.guides/guide-publishing.md` — mirrors and routing
- `~/reposoma/raw.guides/gloss/GUIDE.md` — what BACKGROUND is not
- `~/reposoma/raw.guides/guide-writing/res/write-background.md` — what a BACKGROUND must and must not hold
- `~/reposoma/raw.guides/germline-forge/res/witness.md` — the witness protocol conversions will use
- `~/ia-sync/HANDSHAKE.md` — POINT and ownership by surface
- `~/ia-sync/_staging/guide-census.py` — the census

## What this session deliberately does not do

- Convert, conform, migrate, merge, retire or delete anything.
- Patch the law — a law problem is a finding; 01 re-opens by majkee's word.
- Decide sella.
- Build any tool beyond the census.
