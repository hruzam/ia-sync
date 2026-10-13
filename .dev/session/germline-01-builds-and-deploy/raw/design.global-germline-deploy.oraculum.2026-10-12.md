# Design — global germline as a normal deploy target (germline-01)

`author: oraculum(cSharp) · 2026-10-12 · status: CANONICAL — majkee GO 2026-10-12 (implementation: trajectory) · supersedes on GO: ~/reposoma/.germline/README.md "Scope" paragraph (gaveled 2026-09-25) and ~/ia-sync/AGENTS.md:121-123 ("never a deploy target … must not get one") · checked by: cartan (tunnel, POINT 10) — see §6`

## 1. Verdict (one sentence)

The global germline must be authored in ia-sync and **deployed** to a real `~/.germline/` like agents and skills; reposoma becomes an ordinary project whose `.germline/` is its own project layer.

## 2. The defect it fixes

`~/.germline` is a symlink to `~/reposoma/.germline`. The runtime loader must exclude the global layer when it walks up from cwd looking for a project addendum (wrappers: "never select the global `~/.germline` or its realpath (`~/reposoma/.germline`)"). Therefore a session inside `~/reposoma` can never load a reposoma project layer: **global and reposoma-local are the same folder.** Any repo used as the global source has this defect; ia-sync does not, because ia-sync is the composer, not a project anyone works *in* as a germline-bearing project (its `.dev/session/` beds use their own project layers if ever needed — see §5 Q3).

## 3. Target shape

```text
~/ia-sync/germline/                    ← SOURCE (authored, reviewed, committed here — like claude/agents, codex/skills)
  agents/<slug>/identity.md · binding.<vendor>.md · cards/*.md
  skills/skill.<slug>.md               (vendor-neutral methods, chatbot-readable)
  CHATBOT.md · README.md
        │ deploy.sh: deploy_germline()  rsync "$REPO/germline/" "$HOME/.germline/"   (same flags as skills legs)
        ▼
~/.germline/                           ← LIVE global layer, a real directory on every host (never a symlink)

<project>/.germline/agents/<slug>/<project>.md   ← PROJECT layer, lives in that project's repo (nablarva, reposoma, …)
```

Loader rule becomes path-only: "never select `~/.germline` itself"; the `realpath (~/reposoma/.germline)` clause is deleted.

## 4. Changes (one reviewed row, implementer = trajectory; commit/push/deploy = majkee)

1. `git mv`-equivalent: global files from `~/reposoma/.germline/{agents,skills,CHATBOT.md,README.md}` → `~/ia-sync/germline/` (content byte-identical; stamps unchanged — moving is not editing). Reposoma keeps `.germline/` only for reposoma-scoped layers (empty today; keep a README stub saying so).
2. `deploy.sh` (cartan RETURN 10 folded):
   - `deploy_germline()` **fails closed** if `-L "$HOME/.germline"` (dry and live) — the script never unlinks it; it also refuses an unexpected pre-existing real tree until reviewed/backed up.
   - rsync leg (additive, like skills — no `--delete`) **plus a ghost inventory**: list live files absent from source, in dry and live runs; each ghost = a hold for explicit, backed-up retirement.
   - order: germline leg runs **before** the Claude/Codex wrapper legs in a full deploy; `--germline-only` is an explicit mode; contradictory flag combinations are rejected (`--codex-only` exits early today — document or extend).
   - Codex profile leg: **allowlisted** `houston.config.toml` via `copy_file` (no wildcard); `copy_file` must reject a symlinked destination (`-L "$dst"`); update the portable-scope comment.
3. Host migration, both hosts, once, by the operator: verify the link target → commit/save the reposoma source → `rm ~/.germline` (the symlink only — never `rm -r`) → `deploy.sh --germline-only --dry-run` → `deploy.sh --germline-only`. Journal entry per host.
4. Re-point writers/readers: Houston wrappers (drop the realpath clause) · `~/ia-sync/AGENTS.md:121-123` · `~/ia-sync/{claude,codex}/skills/chatbot-port/SKILL.md` (port home → `~/ia-sync/germline/skills/`) · germline README (source = ia-sync; deploy target = ~/.germline) · nablarva AGENTS.md:40 stays `~/.germline/...` (path unchanged — no edit).
5. SYNC_DISCIPLINE: `~/.germline` joins the list of live trees that are deploy targets, not sources (dead-edit rule applies).

## 5. Open questions (for cartan, then majkee)

- Q1 rsync deletion: the skills legs never delete; a germline file removed at source would linger live. Accept (same as skills) or add `--delete` for this leg only?
- Q2 Codex sandbox: a nablarva-cwd Codex session (workspace-write, writableRoots []) must READ `~/.germline` — with a real dir under $HOME instead of a symlink into another repo, is read access unchanged? (cartan's own read under `:root` worked; children/profile unproven.)
- Q3 Does any ia-sync bed or the temple need its own project layer, and would ia-sync's `germline/` folder be mistaken for one by the walk-up (cwd inside `~/ia-sync` → finds `~/ia-sync/germline/`? No — the loader looks for `.germline/` (dot), the source folder is `germline/` (no dot). Confirm the naming keeps them apart.)
- Q4 Stamp/commit-pin provenance: germline files cite "commit-pin at majkee's commit" in reposoma — becomes the ia-sync commit.

## 6. Cartan's check (RETURN 10, 2026-10-12 — REVISE, folded above)

- Weakest assumption: a normal rsync leg is safe on the first deploy — it is not while `~/.germline` is a symlink (writes through into reposoma). → fail-closed `-L` check; operator unlinks by hand.
- Q1: no unconditional `--delete`; ghost inventory instead.
- Q2: docs say workspace-write allows reads outside the workspace and children inherit the parent's ceiling; a real dir under $HOME should not reduce access — **unproven for a fresh child and a fresh profile session**; the manual test must record each route's reads + effective policy/refusals.
- Q3: `germline/` (source) and `.germline/` (project layer) never collide; do not lock "ia-sync never needs a project layer".
- Q4: stamps survive a byte-identical move; future provenance = `ia-sync@<commit>:germline/…`; reposoma pins stay as history, never rewritten.
- Also: `copy_file` follows symlinked destinations; profile leg must be allowlisted.

**Canonical README line (cartan):** `~/ia-sync/germline/ is the reviewed global source; deploy.sh copies it to a real host-local ~/.germline/ (never a symlink), while <project>/.germline/ remains that project's separate scoped layer.`

## 7. Next

majkee GO → trajectory implements §4 in ia-sync (rb-mark; `--dry-run` evidence; no commit/push/deploy) → assay witnesses → majkee commits, migrates office, then home (pull reposoma + ia-sync first).
