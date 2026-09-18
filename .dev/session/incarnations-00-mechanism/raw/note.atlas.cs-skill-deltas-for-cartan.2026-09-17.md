# note — CS-card skill deltas for @Cartan (Codex sibling)

`from: Atlas (atlas-ui) · to: Cartan, via majkee relay when the GUIDE side is finished`
`scope: what changed in the CLAUDE cold-start-card source that the CODEX rendering must`
`mirror — CONTRACT/SCHEMA level only. Cartan expresses natively; style is Cartan's call.`
`law: ~/reposoma/raw.guides/cold-start-card/GUIDE.md (on any schema conflict the GUIDE wins)`
`claude source refreshed: ~/ia-sync/claude/skills/cold-start-card/SKILL.md (surgical table, NOT deployed)`
`codex target (Cartan authors): ~/ia-sync/codex/skills/cold-start-card/SKILL.md`

## Context

I refreshed the Claude `cold-start-card` skill against the current GUIDE (the flat-model
restructure, 2026-09-17). Most of the Claude source was already aligned; the refresh was
surgical. Two of the corrections are CONTRACT-level and the Codex sibling is currently
STALE on the same points — it still describes the OLD nested issue model that the GUIDE
has DELETED. Those are the mirror-required deltas below. The rest is advisory.

## MIRROR-REQUIRED (contract/schema — the Codex source is stale here)

The Codex `cold-start-card` SKILL.md currently states (read-only, 2026-09-17):
- destination line: `~/reposoma/_cold-start/issues/{open,parked,archive,reactions}/` … "dateless
  recurring reaction playbooks are `IR.*`"
- sort line: "Dateless `RT.*` routines and `IR.*` reaction cards are intentionally exempt."

Both reference the pre-redesign model. Per the GUIDE (§vault, §filename law, journal
2026-09-17) that model is retired. Cartan's rendering must mirror:

1. **`issues/` is FLAT.** Replace `issues/{open,parked,archive,reactions}/` with a single
   flat `issues/` folder that sits at the SAME level as `card/` · `routines/` · `archive/` —
   no nested state subtree. Folder = state is carried by the top-level folder choice only.

2. **DELETE the `IR.*` reaction-card type entirely** — both the destination description and
   the sort-exempt clause. There is no reaction card. The recurring-fix role is served by
   the EXISTING `routines/` category via the FOLD: an issue that recurs graduates into a
   routine, KEEPS its `ISS.<slug>.<date>.md` name and catch-date (grep-visible origin
   radar), and gains an `origin:` field. It is never renamed to `RT.`. Fold has three
   paths: known-recurring → straight to `routines/` · one-shot → `archive/` ·
   archived-then-recurs → pulled into `routines/`. (Fold mechanism detail: `res/issue-card.md`.)

3. **Sort-exempt clause** now reads: only dateless `RT.*` routines are exempt (plus the one
   deliberate exception — a graduated `ISS.`-named routine card, whose date is read as
   "first seen", not drift). Drop `IR.*` from the exemption.

4. **No `seed:` frontmatter key** (see OPEN QUESTION below) — the Claude refresh does NOT add
   one; the Codex rendering must NOT add one either, pending majkee's gavel.

Everything else in the shared contract is unchanged: flat `~`-anchored frontmatter keys,
filename law (`CS.<slug>.<date>.md` / `RT.<slug>.md`), vault cascade via
`temple-project-map.zsh`, Cinderella drain (`card/` → `archive/`, `leave: for more
readers`), one-authority boundary (card is a transfer pointer, STATUS owns a live bed),
prompt-0 runbook grammar. The Codex "evidence keys below the shared block" convention is
untouched.

## ADVISORY (not contract — Cartan decides)

- **Description budget.** I shortened the Claude `description:` to single-sentence class —
  the ~15k skill/subagent description budget is real, and per the session-hygiene substrate
  (2026-09-02) skill descriptions cost ~450 tok and are NOT re-injected after `/compact`
  (only actually-invoked skills survive). The Codex description is already reasonably
  compact; trim only if it drifts long. This is a shared discipline, not a schema change.
- **`claude -p` / `-p` golden rule.** Neither skill's procedure text uses `-p`; keep it that
  way (majkee golden-rule lean, note item 20 — billing boundary ambiguous). Codex has its
  own invocation path anyway; just don't let a `-p` example creep into the procedure.

## OPEN QUESTION — for majkee's gavel (I do NOT decide this; surfaced only)

The incarnation-mechanism trial (note.majkee-design-leans items 1 & 11, locks L6) proposes a
`seed:` frontmatter key on CS cards — a pointer to `~/reposoma/raw.incarnations/<seat>/seed.md`
as an attach point for scar inheritance. Landing it NOW would canonize an attach point BEFORE
the trial's VERDICT (item 1 says "landing at VERDICT canonize only"; the A0 rule says don't).

- **(i) Omit now, add at VERDICT.** Consequence: no premature attach point; the seed mechanism
  stays a trial artifact until the VERDICT gavels it; zero schema churn if the trial changes shape.
  **← the Claude refresh defaults to this (per Oraculum's task instruction).**
- **(ii) Add now as a documented-optional key marked PROVISIONAL.** Consequence: the attach point
  exists early for dogfooding, but it is a canonized surface ahead of its own VERDICT — a soft
  contradiction with A0, and it would need the GUIDE frontmatter section to grow a `seed:` row now
  (see GUIDE-diff note below), which both skills + `cs_vault.py` would then have to parse.

If majkee gavels (ii): the GUIDE §Frontmatter and `res/cold-start-card.md` gain a `seed:` row,
and BOTH skills (Claude + Codex) add it under PROVISIONAL — mirror that change in the same pass.

## GUIDE-diff proposal (Force-4 — for majkee, I did NOT edit reposoma)

The GUIDE is CORRECT on the flat model; no schema edit is required for this refresh. One
optional tracking clarity item:

- The GUIDE restructure note (top block, "One item still genuinely open") flags only the Codex
  `issue-card` skill as not-yet-repointed to the flat model. It does NOT mention that the Codex
  `cold-start-card` skill also still carries the stale `reactions/` / `IR.*` references (the
  MIRROR-REQUIRED deltas above). **Proposed one-line addition** to that open-items note, for
  completeness of the migration checklist:

  > Also open: the Codex `cold-start-card` skill still references the deleted `reactions/` folder
  > and `IR.*` type — @Cartan mirrors the flat-model correction (Atlas delta note 2026-09-17).

  This is optional bookkeeping, not a schema change. Approve or drop at majkee's discretion.
