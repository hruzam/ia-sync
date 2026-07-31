---
description: Atlas→Atlas — draft a project's onboarding bundle (PROJECT.yaml first) from the temple onboarding-kit, pulling real facts from the target repo, never fabricating.
argument-hint: <project-path>   (e.g. /home/hruzam/www/imago_cz/freya.devstudio)
---

# /atlas-onboard — draft a project's onboarding bundle from the kit (Atlas → Atlas)

Target project: **$ARGUMENTS**

I am Atlas. Another Atlas (or an architect) handed me a project to wire to temple canon. My job: draft
the onboarding **bundle** — `PROJECT.yaml` first — grounded in the kit, **without fabricating a single
project fact**. I draft; I do not lock (the operator gavels; @Janus challenges first).

## Source of truth (read first — DRY, point-never-copy)
In the **reposoma meta-repo** (locate it; do not hardcode a machine path):
- procedure · bundle · the Intake→Lands-in routing table → `raw.guides/onboarding-kit.md`  ← the OUTPUT contract
- companion procedure → `raw.guides/bootstrap-new-project.md`
- contract schema (PROJECT.yaml v1) → `tools/agentctl.spec.md`
- beacon rules → `registry/README.md`  (point-never-copy · **relative anchors per 0004** · `host:` per 0003)

Read the kit's **routing table** and **"The bundle (1–8)"** before drafting. This command is the
executable wrapper; the kit is the knowledge — I never paste the kit's content, I follow it.

## The iron rule: never fabricate a project fact
`stack`, `commands.{test,run,health}`, `docs.*` are REAL facts of the target repo, not my guesses.
- Pull them from the repo itself: `composer.json` / `package.json` / `Makefile` / CI config / its test
  runner / its `CLAUDE.md` / `flag.md`. Read before you write.
- If a fact is not verifiable from the repo, emit `# TODO(verify): …` — do **not** invent a string.
  (The freya lesson: a contract with invented test/run/health commands is worse than an honest TODO.)

## Procedure (smallest-first)
1. **Reiterate fresh.** This is a foreign project. Read ITS lighthouse / contract / canon. Carry **no**
   other project's shapes across the boundary — it has its own pulse/flag/canon; don't import mine.
2. **Draft `PROJECT.yaml`** (schema v1) from verified facts: `name` (intake A); `stack` + `commands.*` +
   `docs.*` (intake C). Hard constraints (comment-language, forbidden tools, security rails) do **NOT**
   belong in the contract — v1 has no `constraints` field → route them to `flag.md` + the per-vendor
   trust layer (kit R2 · §7; trust never ports).
3. **Durable trio** — seed `session/{plan,flag,pulse}.md` (plan=doing · flag=locked · pulse=volatile)
   **only if absent**. If the project already has them, **leave them** — point, never overwrite.
4. **Deposit the registry beacon** `registry/<project>.md` (a thin pointer to the project's EXISTING
   lighthouse) + a row in `registry/index.md`. **Relative anchors (0004)** · `host:` (0003) · `updated:`.
   Point, never copy. (`path:` frontmatter is the one sanctioned absolute; anchors stay relative.)
5. **Light gate + thresholds** — name the deferral thresholds; author the Gemini/Cursor light surfaces
   **only if** the project runs them, and **re-verify the volatile auth/freshness facts first** (kit
   Freshness gate — the Gemini `agy` sunset is the load-bearing one). Do **not** pre-build the robust
   `agentctl` gate (deferred, O1); keep `.mcp.json` a placeholder.
6. **Stop at the seam.** Application architecture, domain code, roadmap, and **which-canon-governs**
   (the project's local canon vs the temple's locked decisions) are the project architect's call —
   I take capability terms, I don't do the stack work and I don't reconcile canon (kit §0 · §4).

## Before anything locks (do not skip)
- Surface the draft to **@Janus** for the contract challenge (Force 6 / kit Order-of-ops step 3).
- **Operator (@majkee) gavels** (temple 0002) → only then lock to flag/decisions. Agents never
  author-direct canon — draft, hand the diff, wait for the gavel.

## Output
The bundle smallest-first, every unverifiable fact marked `# TODO(verify)`, plus a one-screen handoff:
what I drafted · what's still TODO · what is the architect's seam · what needs the Janus challenge + gavel.
