# RUNBOOK: guide-model-01-law

```yaml
goal: >
  The builder instruction speaks the model shape: guide-writing carries the gaveled law, is itself
  the first model guide, ships the three templates, and /guide reads guides that way.
gate: >
  The census shows guide-writing clean as shape: model with BACKGROUND.md; its ast/ holds the three
  templates and its src/ is empty; the Claude-side /guide skill carries the reader delta and majkee
  has deployed it; a POINT for the Codex-side skill is on disk for @Cartan; a fresh witness passed
  every row — all committed.
participant_1: [head, {brand: <bind — codex or claude; the cSharp holder>, model: <bind>, effort: high}, host: <bind>, role: "cSharp — navigator and status_owner; binds the seats, hands out the prompts, tests what comes back; never writes the guide or the skill"]
participant_2: [writer, {brand: claude, model: <bind>, effort: high}, host: <bind>, role: "taskline — folds the law, converts guide-writing, applies the Claude-side reader delta, writes the POINT"]
participant_3: [witness, {brand: <bind — not the writer's incarnation>, model: <bind>, effort: medium}, host: <bind>, role: "standing witness — proves the result from a fresh session; authored none of it"]
participant_4: [majkee, {brand: human}, host: <bind>, role: "gavels the law text before the fold; deploys; gavels the result"]
status_owner: head
head_note: "cSharp — this seat authored the RUNBOOK and stays live through the whole arc as navigator and status_owner; it may delegate every body of work and receive only navigation + test parts; it closes the session if it can."
observations_read: none exist — new program (head re-runs `ls ~/ia-sync/.dev/observations/guide-model*` before parking)
```

## Why this session exists

Every later conversion copies what guide-writing teaches, so the builder instruction goes first.
The law is drafted, not gaveled, and the guide that must carry it is still flat. Converting
guide-writing by its own new law is also the cheapest proof the shape works: a law that cannot
express itself is not ready for the tree.

## Fixed facts

- Temple `~/reposoma` holds knowledge; table `~/ia-sync` holds executables (guide-writing law).
- Staged inputs in `~/reposoma/raw.guides/guide-writing/src/`: `model-shape.md` + `write-background.md`
  (the gavel text), `BACKGROUND.guide-writing.seed.md` (the first BACKGROUND — majkee confirms its
  rows), and `GUIDE.template.txt` · `FUNCTION.template.txt` · `BACKGROUND.template.txt`. Outbound
  staging — `src/` empties when they land (`res/slug-directories.md`). Beside it, `raw/` holds the
  review records (Wave's reviews, Symmetry's returns). Until step 2 lands, the census shows
  guide-writing's `src/` and `raw/` as unregistered — expected; the conversion clears it.
- Census: `python3 ~/ia-sync/_staging/guide-census.py ~/reposoma/raw.guides` — read-only, facts only.
- `~/ia-sync/codex/skills/guide/` is @Cartan's turf: POINT, never edit (HANDSHAKE).
- Meeting room for the POINT: `~/ia-sync/.dev/session/rellays-claude-codex/` — name precedent
  `ATLAS-CARTAN-sella-mount.2026-09-01.md`.
- Head protocol: `/guide runbook csharp-head-protocol` — the posture outlives the seat; a change of
  holder follows its transfer ritual.
- Witness protocol: `/guide germline-forge witness` — the author cannot witness.
- **Reading `background`:** every `background` string in this package means `BACKGROUND.md` or points
  to it — the file, its template, its seed, its manifest class, the `/guide <slug> background`
  command. One exception: `write-background` is a guide-writing function (`res/write-background.md`)
  that says how to write one; it is never `BACKGROUND.md`, and the `background` keyword never serves
  it. No chapter is ever named `background*` — the keyword would shadow it.

## prompt-0 — head

```text
You are the head of guide-model-01-law, in the cSharp posture (/guide runbook csharp-head-protocol).
Bed: ~/ia-sync/.dev/session/guide-model-01-law/ — you own STATUS; you never write the guide or the skill.
1 · Precondition: majkee confirms the current guide maintainer has reached a stopping point — no
    guide edits in flight (git -C ~/reposoma status; git -C ~/reposoma log -5 -- raw.guides/).
    The staged files are the reviewed batch: (cd ~ && sha256sum -c ~/ia-sync/_staging/guide-model/SHA256SUMS)
    prints OK on every line. Any FAILED line stops the session.
2 · Bind the seats in the front-matter. Hand prompt-1 to the writer; its step 1 stops for
    majkee's gavel — carry it.
3 · Test what comes back — the census line, the collapse map, the four commits — and write every
    STATUS claim as a path the witness can test.
4 · At the writer's step 5, hand prompt-2 to the witness. Gate when the gate line is observably true.
5 · Before prune: the experience transfer into <bed>/raw/ (transfer ritual) and a promotion
    manifest for every raw/ keeper (scar 4).
```

## prompt-1 — writer

```text
You are the writer of guide-model-01-law. Bed: ~/ia-sync/.dev/session/guide-model-01-law/
Read, in this order, nothing else first:
  ~/reposoma/raw.guides/guide-writing/GUIDE.md + res/slug-directories.md   (every rule survives)
  ~/reposoma/raw.guides/guide-writing/src/model-shape.md + write-background.md   (the gavel text)
  ~/ia-sync/claude/skills/guide/SKILL.md                                  (the reader you amend)

1 · GAVEL THE TEXT. Edit nothing yet. To the head and majkee: every place model-shape.md or
    write-background.md conflicts with, duplicates or weakens guide-writing law — one line each, file:line — beyond the eight
    changes it already lists. Stop until majkee gavels (edits allowed).
2 · CONVERT guide-writing by the gaveled law — it is the first model guide:
    - occasions with evidence → Functions table → functions in res/ (with occasion:) → controller
      (banner, what/not, invariants, the manifest law) → BACKGROUND.md: land src/BACKGROUND.guide-writing.seed.md once majkee has
      confirmed its rows, then add what the collapse map retires into it.
    - src/write-background.md lands as res/write-background.md — the function for
      "write or extend a guide's BACKGROUND.md".
    - res/slug-directories.md becomes a function or a reference chapter — your call, stated.
    - the gaveled law lands inside the guide (controller + functions), not as a parallel chapter.
    - move the three templates src/ → ast/; register ast/ and raw/ (the review records) in the
      Manifest; leave src/ empty.
    - keep the collapse map: every source paragraph → its new home, or retired with the reason.
3 · READER DELTA — Claude side only, in ~/ia-sync/claude/skills/guide/SKILL.md, nothing else there:
    a. listing signal pattern ^(title|machine|verified|shape): → render slug · shape · title · machine · verified
    b. resolution: /guide <slug> background → <slug>/BACKGROUND.md (fixed filename; never served unasked)
    c. orphan flag: the register is ## Manifest plus ## Functions
    d. writer law line 2: add "shape: model when the guide has several occasions (absent = flat)"
4 · POINT for @Cartan: ~/ia-sync/.dev/session/rellays-claude-codex/<WRITER>-CARTAN-guide-skill-shape.<date>.md
    — the four deltas and the path of the Claude-side diff; nothing owed back.
5 · CENSUS on the real tree: guide-writing must read fm ok · shape model · bg y · nothing
    unregistered · nothing dangling · no table-drift. Then majkee deploys the skill (his act), and
    the head hands the witness prompt-2. You never witness.
Commits, one concern each: law + conversion (collapse map in the body) · templates · skill delta · POINT.
Done when the gate line is observably true.
```

## prompt-2 — witness

```text
You are the witness of guide-model-01-law. You authored none of it. Fresh session; start every row
from /guide guide-writing only. Write ~/ia-sync/.dev/session/guide-model-01-law/witness.md, one row
per prompt: exact prompt · PASS looks like · FAIL looks like · observed (first ~5 lines verbatim) ·
verdict. A nudge is a new row.
  1  "Decide the shape of ~/reposoma/raw.guides/tree-snapshot/. Edit nothing."
     PASS: occasions listed with evidence; the verdict follows the split law.
  2  "Decide the shape of ~/reposoma/raw.guides/runbook/. Edit nothing."
     PASS: as row 1.
  3  "Scaffold a new guide 'toy-two-jobs' with two occasions in a fresh WG=$(mktemp -d)."
     PASS: shelves copied from ast/; banner present; two empty functions named by occasion with
     occasion: equal to their rows; no invented content;
     python3 ~/ia-sync/_staging/guide-census.py "$WG" shows the slug clean. Write $WG in the row.
  4  "Why did ~/.config/zsh/guides/ become a stub?"
     PASS: answered from BACKGROUND.md, reached through the controller's pointer — not by reading
     every chapter.
  5  "Record in $WG/toy-two-jobs/ why its two jobs stay in one guide, and the
     option rejected."
     PASS: BACKGROUND.md copied from ast/ with the authority line; exactly three sections; one
     dated Decisions row with its 'instead of'; no rule or command in it.
  6  "Using /guide guide-writing, find the function for translating a guide into Czech, and follow it."
     PASS: reports that no Functions row fits and stops — reads no function, invents no route.
  7  one row per Functions row of the converted guide-writing not covered above.
  8  after majkee's deploy: the /guide listing shows shape; /guide guide-writing background serves
     BACKGROUND.md.
Verdict PASS only if every row passes. Write what stays unproven. Afterwards rm -rf "$WG" — that
directory only.
```

## Known constraints + destructive holds

- Start only after the current guide maintainer has reached a stopping point (majkee confirms) —
  converting over in-flight edits collides.
- Edit only: `guide-writing/` (GUIDE.md, res/, ast/, src/, BACKGROUND.md), `~/ia-sync/claude/skills/guide/SKILL.md`, the POINT file, the bed — and, at gate close, the head's
  promotion of keepers per scar 4.
- Never edit `~/ia-sync/codex/**` — POINT only.
- No other guide is touched; guide-model-02-audit judges them.
- The resolver's served set grows by `background` only.
- Deploy is majkee's act (`deploy.sh`), after his gavel.

## Acceptance evidence

- The SHA256SUMS check (all OK) and the census line for guide-writing (step 5) pasted in STATUS.
- `witness.md`: every row PASS; the unproven list stated.
- The collapse map in the conversion commit body; four commits, one concern each.
- The POINT on disk.
- majkee's two gavel lines (text · result) in STATUS.
- The head's experience transfer on disk in `<bed>/raw/` before prune.

## References

- `~/reposoma/raw.guides/guide-writing/GUIDE.md` · `res/slug-directories.md` — the law this extends
- `~/reposoma/raw.guides/guide-writing/src/model-shape.md` — the gavel text
- `~/ia-sync/claude/skills/guide/SKILL.md` — the reader
- `~/reposoma/raw.guides/germline-forge/res/witness.md` — witness protocol
- `~/ia-sync/HANDSHAKE.md` — POINT shape, ownership by surface
- `~/reposoma/raw.guides/gloss/GUIDE.md` — the sibling BACKGROUND must not become

## What this session deliberately does not do

- Audit or convert any other guide.
- Touch `codex/` — POINT only.
- Build a scaffold script or any automation — templates are copied by hand until friction earns more.
- Resolve the `src/` ↔ `raw/` seam — guide-model-02-audit reports the evidence; majkee gavels.
