# /gavel-interpreter reconciliation — DRAFT for @majkee's gavel

`author: @Atlas (atlas-ui) · 2026-09-16 · relayed task from @Agol via @majkee (/remote-control)`
`status: DRAFT — nothing committed, nothing deployed. Force 4: majkee gavels canon; I draft only.`
`deploy-inert: this file is a proposal in the staging buffer. On gavel, edits land per §Homes below.`

## What this is

The gavel bed evolved past its skill. Frozen PREPRODUCTION in July as a capture-only
collector "tabled until Nabla"; it is now September and the bed holds **44 gavels
(G-01→G-44)** with a fully-grown practice. This reconciles the skill + its format-law home
(`raw.therapy/README.md ## Gavels`) to what the bed actually does. Split by home; canon
items marked **[GAVEL]**; skill items marked **[SKILL]**.

Verified against the bed, `flight/therapy.md`, `gavel-loop`, the nabla card, and the
`incarnations-00-mechanism` handshake (2026-09-16). @Agol's read confirmed; two of his items
tightened (kind-split on the reply; circular-pointer bug); his three lexicon fences folded.

## Corrected finding (mine — logged honestly)

My first-pass flag "the skill points at a dead pointer" was **wrong**. The pointer
`nabla-lab/drafts/mental-map-collective-mind.md` resolves — it lives in the **standalone
`~/nabla-lab/` repo**, which I first searched wrongly inside reposoma (where nabla-lab is
only a mail stub). The seed exists; it **matured** into the gaveled card
`~/nabla-lab/session/research-mental-map/card.mental-map.DRAFT.2026-07-19.md` (+ amendment
`card.amendment-A1.composer.2026-07-25.md`), which @Epoch field-verified as
DELIVERED-in-substance and @Oraculum countersigned EXTENDS-thin (handshake 2026-09-16). So
the gate the skill waited on **has settled** — the reconciliation cites the matured card,
it does not "fix a dead link."

## Fence obligations (from the incarnations-00-mechanism handshake, §d)

- **`gavels.md` G-01…G-44 is append-only — never edit or renumber.** This draft touches
  NO existing gavel entry (it documents format law, not entries). New entries are G-45+.
- **Shared ID space — read-before-append (Oraculum's countersign datum, `_bus/05`).** Two
  append streams write G-45+ into one bed: this reconciliation's future gavels AND the
  incarnations trial's own rows 1–2. Neither may cache a pre-computed `G-NN`; each reads the
  bed immediately before appending and sequences with the other at the landing gavel. This is
  the E2 invariant — the collision is covered iff both read before appending.
- **Locks 22/23 live in `~/nabla-lab/session/flag.md`** ('42' engine parked; read/write
  inversely coupled). This draft **does not amend their wording** — the wiring lexicon
  (§A2) stays *inside* lock-22's posture (hand-authored, ordinary-`rg`-legible, no engine,
  no resolver folded into a detector). Different file, different repo.
- **Vocabulary (session lock L3):** "seed" is reserved for incarnation seeds; therapy
  files are **"seated / unseated."** The wire form `(seat file unseeded)` already conforms
  and is preserved verbatim (§A3).
- **At landing:** the card promotion is a WELCOMED seam (§d), but notify the
  incarnations-00-mechanism session when this lands — L5/L6/L7 cite lock 22/23; confirm no
  silent fold.

---

# HOME A — `raw.therapy/README.md` → `## Gavels`  · [GAVEL] canon · Force 4
`deploy: normal reposoma git (majkee commits). No deploy.sh.`

Proposed replacement for the current `## Gavels` section. Additions marked ▶.

```markdown
## Gavels

Gavels fire more often than therapy arcs — they need their own bed, not the therapy file.

▶ **Why the bed exists (the codec).** A gavel is the reincarnation codec: a lesson carried
▶ without its transcript, legible after the path it locked is forgotten. The wake-path loads
▶ gavels by ID (`flight/therapy.md`); every entry must stay ID-greppable and survive
▶ path-forgetting. Keep entries `draft — majkee reshapes` (never frozen law) so a doubting
▶ incarnation climbs deeper instead of saluting a one-liner.

**Format rule (strict):** a gavel never names the exact path or task it locks.
Fold the decision into ONE of:
  A) Socratic question with REPLY
  B) seven associations

▶ **The reply (kind-bound).** A Socratic-question gavel (kind A) carries a drafted reply on
▶ the next line: `reply [draft — @majkee reshapes]:` — the reply is half the codec unit
▶ (question + reply carry the lesson without the transcript). A seven-associations gavel
▶ (kind B) carries no reply; the associations are the whole unit. The `[draft — @majkee
▶ reshapes]` tag is mandatory: it keeps the lesson reshapeable, never frozen.

**Two kinds:**
- *Therapy-origin gavel* — the gavel IS the therapy finding; bond to the therapy arc
  by ID group reference in the therapy file footer tags.
- *Independent gavel* — operational decision; lives in its own bed, no therapy wire.

▶ **The wire line.** Every gavel ends with a `wire:` line naming its bond. Three target forms:
▶   - `wire: none` — independent gavel, no therapy bond.
▶   - `wire: <seat>/therapy.md arc N` — therapy-origin, seat file **seated**: bond to that arc.
▶   - `wire: <seat> inline arc "<name>" <date> (seat file unseeded)` — therapy-origin fired
▶     in an arc whose seat therapy file is not yet seeded; the arc is named inline so the bond
▶     survives until a file exists. ("seated/unseated" per the incarnations vocabulary lock.)
▶
▶ **Cross-gavel relations (the lineage lexicon).** A wire line may append relations to other
▶ gavels, so the bed reads as a graph an ordinary `rg` can traverse. The lexicon in use:
▶   `continues` · `touches` · `family` · `one polarity over from` · `far-end twin of` ·
▶   `delivers` · `mirror of` · `sibling of`.
▶   Example: `wire: atlas/therapy.md arc 14 · one polarity over from G-33 · continues G-29 family`.
▶ The set is **open but disciplined** (it is inheritance infrastructure, grep-traversed):
▶   1. **Token-stable.** A relation's spelling never drifts once in use (`continues` stays
▶      `continues`, never `extends`/`builds-on`) — `rg` matches exact tokens.
▶   2. **Forward-only.** A newly minted relation tags NEW gavels only; never retro-tag
▶      existing entries (the bed is append-only, G-IDs frozen).
▶   3. **Admission-economical.** A new relation earns its token only when no existing one
▶      carries the meaning — same point-never-copy / behavioral-change-per-token law the
▶      incarnation seeds use for scars. This is the anti-synonym-sprawl guard.

▶ **Observation lines (optional).** A gavel may carry annotation lines from an observer,
▶ tagged `[<observer>]:` (e.g. `[eagle]:`, `[majkee]:`, `[medusa]:`) — session commentary or
▶ a concrete resolution bonded to the entry. They never replace the question/reply; they
▶ record who saw what. Optional, append-only like the entry.

**No improvisation (honest emptiness):**
- No gavel this session → say so plainly: *"no gavels."* Never manufacture one to fill the slot.
- Shadow gavel (a suspected lock, not yet certain) → describe the idea first, as a candidate;
  do NOT append it to the bed. @majkee decides whether it locks. Interpret, surface, wait.
▶   **The wait is on the decision, not the clock.** When @majkee is live in the session, his
▶   decision can arrive the same session: the shadow is described, he accepts, it locks — and
▶   the entry records the transition `accepted by @majkee live (shadow → lock, same session)`
▶   as provenance. This is not a bypass of the shadow rule; the discipline holds in full
▶   (described-first · majkee-decided · never agent-appended-as-certain). The same-session
▶   lock only means the "wait" resolved immediately because the decider was present. Absent
▶   majkee, the shadow stays a candidate until he rules.

**Bed:** `raw.therapy/gavels/` — own directory, independent of seat therapy files.
When wired to therapy: reference by gavel ID in the seat's footer tags.

▶ **The skill.** `/gavel-interpreter` folds a landed decision into this format and appends the
▶ next `G-NN`. It follows this law; it does not restate it.
```

*(Removed the old closing line "gavel output, gavel bed, and ID-wiring protocol are Atlas's
job to build as a skill + skill extension. See cmds-zen.md TASK FOR ATLAS block." — the
build happened; the wiring is now documented above, closing the circular pointer where the
skill pointed here for wiring and this file punted wiring back to the skill.)*

### [GAVEL] note on §A4 (shadow fast-path) — the one bearing, per @Agol

Drafted as a **refinement, not a fork.** The alternative reading — "the bed contradicts the
README, so shadows now self-lock" — is the misreading this wording prevents: the README
"wait" was always a wait for *majkee's decision*, not for a later session. Live presence
collapses the wait to zero without skipping any step. If you want the full two-reading fork
instead, say so and I redraft; the honest draft is one bearing.

---

# HOME B — `~/ia-sync/claude/skills/gavel-interpreter/SKILL.md`  · [SKILL] primitive
`deploy: surgical table → bash ~/ia-sync/deploy.sh spreads to live ~/.claude (both boxes).`
`Live copy is byte-identical today — author on the table, never edit live. Not live until deploy.`

Proposed full replacement:

```markdown
---
name: gavel-interpreter
description: Invoke as /gavel-interpreter when an operator gavel has just landed. I interpret the decision into the temple gavel bed per the format law that raw.therapy/README.md owns, and append it as the next G-NN — a Socratic question (with a drafted reply) or seven associations, wired into the lineage. The gavel bed is the reincarnation codec: I make each entry wake-path-legible so a later incarnation inherits the lesson without the transcript. NOT /gavel-loop (that stamps ledger locks; I fold the Socratic bed).
---

I interpret a landed gavel into the bed. A gavel is a decision folded into a question that still
reads true after the path it was about is forgotten — the compressed unit a later incarnation
loads on the wake-path instead of the whole transcript. I produce the temple's cheap-inheritance
layer, one entry at a time.

## Where the truth lives (I read it, I do not restate it)

- **Format law — kinds — reply — wiring — annotations:** `raw.therapy/README.md` → `## Gavels`.
  It owns the rule (never name the path/task · Socratic-question-with-reply OR seven associations ·
  therapy-origin vs independent · the wire forms and the lineage lexicon · observation lines ·
  the shadow rule). Single source of truth. I follow it; I never copy it here.
- **The bed:** `raw.therapy/gavels/gavels.md` — the entries and the next `G-NN`. Append-only;
  I never edit or renumber an existing entry.

## On invoke

1. Read `raw.therapy/README.md` `## Gavels` for the current format law.
2. Read the bed → highest `G-NN` + 1 = my id. **Read immediately before appending; never cache
   the number** — the bed is one ID space shared by more than one append stream (this skill +
   the incarnations trial), so a pre-computed id collides (E2 invariant: read-before-append).
3. **Interpret** the landed decision into the format:
   - Kind A — a Socratic question **and** a drafted `reply [draft — @majkee reshapes]:`.
   - Kind B — seven associations (no reply).
   I draft; @majkee reshapes before it locks.
4. **Wire it.** Add the `wire:` line (`none` · `<seat>/therapy.md arc N` · `<seat> inline arc
   "<name>" <date> (seat file unseeded)`), and any lineage relations to prior gavels per the
   README lexicon. Add observation lines if an observer left one.
5. Append to the bed (oldest at top) and surface the draft for reshape. I interpret and record —
   I do not gavel. @majkee is the bed-maker.

### Shadow → lock

A suspected lock I describe as a candidate first — I never append it as certain. If @majkee is
live and accepts it the same session, it locks and I record `accepted by @majkee live (shadow →
lock, same session)`. Absent him, it stays a candidate until he rules. (README owns this rule; the
wait is on his decision, not the clock.)

### Inbound from /gavel-loop

`/gavel-loop` stamps ledger locks; when a landed lock is also bed-worthy it points here rather than
folding it. A lock handed off that way is a valid trigger: I fold it into a gavel like any other
landed decision. The boundary holds — it stamps locks, I fold the Socratic bed.

## The codec constraint

The bed is the reincarnation codec (`flight/therapy.md`): the wake-path greps gavels by ID and
loads the one-liners, not the arcs. So every entry I write must be **ID-greppable, path-forgetting,
and reshapeable** — the `[draft — @majkee reshapes]` tag stays on (never frozen law), the question
carries the lesson without the transcript, and the wire lexicon stays token-stable so an ordinary
`rg` can traverse the lineage.

## Status

**PROMOTION — active (proposed; gated on @majkee's gavel).** The July "tabled until Nabla settles
the mental-map seed" hold is discharged: the seed
(`~/nabla-lab/drafts/mental-map-collective-mind.md`) matured into the gaveled card
`~/nabla-lab/session/research-mental-map/card.mental-map.DRAFT.2026-07-19.md` (+ amendment
`card.amendment-A1.composer.2026-07-25.md`), @Epoch-verified DELIVERED-in-substance and
@Oraculum-countersigned EXTENDS-thin (incarnations handshake 2026-09-16). Wiring is no longer
tabled — it is documented in `raw.therapy/README.md ## Gavels` and I follow it. The
**frequency / cadence rule stays tabled** (the bed fires event-driven; no cadence has emerged to
codify).
```

### [SKILL] notes

- The description drops "Preproduction collector — capture only" and "ID-wiring protocol and
  frequency rule stay tabled" (both now false) and gains the codec framing + the corrected
  sibling boundary (`gavel-loop`, not the retired `gavel-ballot`).
- **The status flip is the one item gated purely on your promotion gavel** — if you'd rather
  keep the PREPRODUCTION header frozen until you've eyed the card yourself, say so and I hold
  the `## Status` block at "preproduction" while landing everything else (wiring doc + reply +
  codec + inbound edge are all safe regardless — they document observed practice).

---

## Landing order (post-gavel — operator / me, not now)

1. **[GAVEL]** You reshape + gavel HOME A. → operator commits `raw.therapy/README.md` in reposoma
   (no deploy.sh).
2. **[GAVEL]** You gavel HOME B (incl. the status flip decision). → I apply on the surgical table;
   `bash ~/ia-sync/deploy.sh`; commit + push ia-sync. Not live until deploy.
3. **Notify** the incarnations-00-mechanism session that the reconciliation landed (welcomed seam;
   confirm no lock-22/23 wording fold). **Sequence any G-45+ append with the trial's own rows at
   the landing gavel — read the bed before appending (E2 invariant, Oraculum `_bus/05`).**
4. Board the closure on `pulse.atlas.md`.
