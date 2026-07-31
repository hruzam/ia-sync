# `_staging/` — the build buffer · a stone of truth

**What this is.** The deploy-inert build buffer of the surgical table. Autonomous builds
(@atlas-auto — spec in, primitive out, no human watching) land HERE first, never on the live
keep-set. Everything under `_staging/` is git-tracked from birth and sits outside every `deploy.sh`
leg (which only spreads `claude/{agents,skills,commands}/`, `gemini/`, `majkee/`, `zsh/`). So a build
buffered here is **recoverable, cross-machine, and cannot go live by itself.**

## Why it exists — the story

On **2026-07-30** the old drop-folder `.larva/agents-staging/` — a pre-temple-era buffer wired to
atlas-auto and long forgotten inside the reposoma repo — was deleted in a rough sweep. A **pre-codex
agent went with it.** It may be rescuable from git history; but "may be" is the whole point:

> A build buffer must never be a place where work can vanish without proof.

This folder is the answer. It lives on the **surgical table** (the composer, `~/ia-sync`), git-tracked
the moment anything is written to it — so the loss that happened cannot happen here.

## The flow

1. atlas-auto writes a build into `_staging/claude/agents/<name>.md` (or `_staging/zsh/…`, etc.).
2. A reviewer reads it. No human watched it being made — **this is the gate.**
3. Promote: `mv _staging/claude/agents/<name>.md → claude/agents/<name>.md` (the keep-set).
4. `bash ~/ia-sync/deploy.sh` spreads it live on this machine; commit + push; the other machine
   `git pull` + `deploy.sh`.

Until step 3 the build is buffered — versioned, portable, inert.

## The law it serves — HARVEST BEFORE REMOVE

Nothing legacy is deleted in a rush. Extract the value, record the provenance, then remove only with
git-recoverability. This buffer is where that discipline begins: **work is captured before it is judged.**

## Do not "tidy" this away

An empty `_staging/` is normal — it drains as builds are promoted. Its emptiness is not litter; it is a
table wiped clean between cuts. **The folder stays.**

---
Surgical-table doctrine: `session/plan/surgical-table.plan.md`.
Retirement of `.larva/agents-staging/` recorded in
`reposoma/maintenance/codex-line/note.staging-retired.2026-07-30.md`.
