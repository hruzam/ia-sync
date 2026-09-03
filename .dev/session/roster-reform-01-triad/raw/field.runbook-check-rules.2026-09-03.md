---
kind: substrate — runbook-check detection rules
date: 2026-09-03
source-session: fc.repos-atlas-opus.polyp-medusa (fold seat) — @field second pass
specimen: ~/www/ovum/larva.dev/session/@larva.vector-language/{CLAUDE.md, config.json}
status: substrate — PROMOTED 2026-09-03 to ~/reposoma/raw.guides/runbook/raw/field.runbook-check-rules.2026-09-03.md (gate closure; that copy is authoritative, this one prunes with the session — safe to delete)
purpose: >
  The 8 patterns a Vara "runbook-check" pass must detect (caveats / missing gavels /
  config-drift). Preserved VERBATIM here because they lived only in the fold seat's context
  (cycle 03 gate a). They land as a skill's detection rules when the runbook GUIDE lands.
---

# Runbook-check detection rules — larva.dev specimen

The specimen is a `@Recorder` agent (`"version": "0.1"`) for larva.dev. It never ran in
production — the `<FILL_*>` placeholders are still in the config. Every deferred decision shows
as a scar, making it an ideal specimen.

## The 8 patterns

**Pattern 1 — Ungaveled name / parallel alternates**
`config.json:5–7`: `"name": "@Recorder", "_alternates": ["@Cockpit", "@RedEggs"], "_comment":
"Pick one in 'name' field; remove this _alternates list once decided."` Three names active
simultaneously; no gavel closed the choice. **Rule:** any `_alternates` array or comment
containing "once decided" = open question → `?Q`.

**Pattern 2 — Unfilled structural placeholders**
`config.json:27`: `"api_key": "<FILL_API_KEY>"` and `config.json:33`: `"session_root":
"<FILL_SESSION_ROOT>"`. The config runs as-is with broken values. **Rule:** any `<FILL_*>`
token in a structural (non-comment) field = blocking gap → `?G`.

**Pattern 3 — Hardcoded dated model version, will drift**
`config.json:16`: `"id": "claude-haiku-4-5-20251001"`. Harness convention uses abstract tier
names (`haiku`/`sonnet`/`opus`); this pins a dated release. Upgrade path buried in `_comment_id`:
`"Upgrade to claude-sonnet-4-6 only if Recorder starts needing judgment calls"` — a conditional
decision in a comment, never gaveled. **Rule:** `claude-*-YYYYMMDD` in a model field = config-drift
candidate; a conditional upgrade criterion in `_comment` = inline governance = missing gavel.

**Pattern 4 — Behavior constraints in `_comment` fields, not in rules**
`config.json:23`: `"temperature": 0.2, "_comment_temperature": "0.0–0.3 range. Do not exceed
0.5."` — a ceiling that should be a hard rule, living in a comment no agent reads. `config.json:49`:
`"infer_ungavelled_decisions": false, "_comment_infer_decisions": "Set to true only if you start
needing the Recorder to spot…"` — a conditional behavior flip described in a comment, never
evaluated, never gaveled. **Rule:** `_comment` fields containing "Set to true only if," "Do not
exceed," or "only if you start needing" = inline governance = missing gavel.

**Pattern 5 — Experimental section, no trial record, no retirement record**
`config.json:119–124`: `"auto_promote_questions_after_days": null` and `"weekly_digest": false`
labeled `experimental`, with `"Off — start lean"` comments. No record of whether they were
trialed and found lacking, or never reached. **Rule:** `experimental` fields with null/false and
a "start lean" rationale = gap (were they trialed?) → `?G`.

**Pattern 6 — Duplicate definitions without canonical-source pointer**
`CLAUDE.md:39–46`: full marker convention table (`?Q`, `!D`, `?P`, `~N`, `?G`, `*F`).
`config.json:56–63`: identical markers block in `"markers": {...}`. Two sources, no pointer; any
edit to one diverges silently. **Rule:** same structured data in two files with no `→ see <file>`
cross-reference = drift risk → `?G`.

**Pattern 7 — Project-local hierarchy inversion vs global roster**
`config.json:86–90`: `"secondary": ["@Voice", "@Houston", "@Cursor", "@Scribe"]`. @Houston is the
global primary architect-tier seat, listed as secondary here (larva.dev framed it as a lineage
reference, not an active participant). A check cannot know intent from rank alone, but can flag.
**Rule:** any global-tier architect (Houston, Oraculum) in a project-local `secondary` list = flag
for human review.

**Pattern 8 — Draft-stage indicator with no promotion record**
`config.json:10`: `"version": "0.1"`. No gavel promoting it out of draft. **Rule:** `version: 0.x`
with no companion promotion note = draft stage → `?Q`.

## Consolidated detection rules

| Pattern | Detection rule | Marker |
|---|---|---|
| Ungaveled alternates | `_alternates` list or "once decided" in comment | `?Q` |
| Unfilled structural placeholders | `<FILL_*>` token in non-comment field | `?G` |
| Dated model version | `claude-*-YYYYMMDD` in model field | drift flag |
| Inline governance | `_comment` with "Set to X only if," "Do not exceed," conditional flip | missing gavel |
| Untrialed experimental | `experimental: null/false` + "start lean," no trial record | `?G` |
| Duplicate definition, no pointer | Same structured data in two files, no cross-ref | drift risk `?G` |
| Hierarchy inversion | Global-primary seat in project-level secondary list | review flag |
| Draft-stage indicator | `version: 0.x`, no promotion note | `?Q` |
