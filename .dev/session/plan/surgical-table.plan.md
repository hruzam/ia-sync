# Surgical Table doctrine — plan of record

**Gaveled direction (@majkee, 2026-07-30, buffering-cycle):** ia-sync is the **surgical
table** — the one place cuts are made, serving as the like-composer that syncs both
machines. Everything else (live `~/.config/zsh`, live `~/.claude`, guides, agent wiring)
is a deployed copy. Doctrine line: *"something is written, but never forget to ask for a
reality check in the sync part."*

Written on office @ `af8cd5d`. Status 2026-07-30 (second pass): 1 BLESSED + APPLIED (banner in builder, user, home,
office, index). 3 DONE. 5 BUILT (leg live in sync.sh/deploy.sh + majkee.deny; office
skip-path verified — `~/.majkee` confirmed home-side, tree provided by operator:
config/{repomix/repomix.codex.json, tcr}, _drops@chatGPT/, export/{repomix,tcr}).
4 still gated: Eagle read the temple roster — **WS5 PENDING**, blocked on WS4a (majkee's
stone) + WS4b (pad intent); model pin still DRAFT; artifacts still in .larva/agents-staging.
Vega seat persists, vendor swapped Gemini→Codex (0005 A1). One constraint for the future
codex leg: gemini `exit 2` guard files in `~/.config/zsh/ai/` are loud-parked evidence —
preserve, never prune. 2 (zenith repoint + .deployed stamp) remains the open build.
Third pass, same day: operator gaveled the MOUNT ahead of WS5 bookkeeping —
`.larva/agents-staging` deleted (old, blessed over all; gemini-subagents June copies died
with it), codex bed moved onto the table (`claude/agents/codex-{coder,crosscheck}.md`,
`zsh/ai/codex-run.zsh`) and deployed. Cards carry DRAFT model pins — WS5 still owes the
roster rows + pin gavel + WS4a/4b. Official channel updated:
`reposoma/maintenance/codex-line/note.staging-retired.2026-07-30.md`.

---

## 1 · Banner in every named guide — TEMPLE PROPOSAL (not yet applied)

Targets: `guides/guide-for-builder.md`, `guides/guide-for-user.md`, `guides/home.md`,
`guides/office.md`, `zsh/README` surfaces, and the temple's own copies. Process-claims
only, so it cannot rot:

> **⚕ Cut on the surgical table.** This file is deployed from `~/ia-sync` (the surgical
> table — like a composer for both machines). Do not edit it in place: edit in ia-sync,
> deploy outward, verify. Reality check before trusting any machine fact here:
> `git -C ~/ia-sync log --oneline -5 -- <repo path of this file>` (intent) **and**
> `rsync -n` repo↔live (reality). Commits say what *should* be deployed; only the diff
> says what *is*.

Routing: @majkee carries it to the temple; applied to guides only after ratification.
Rationale for both checks: the MACHINE_NAME fallback incident (2026-07-30) — commits
looked perfect while `config.zsh` was silently not deployed.

## 2 · zsh experts repoint to the table — option (a), BUILD

- `zenith-zsh` agent card: keep in `~/.claude/agents/` (already synced). Rewire its scope:
  canonical wiring/reading surface = `~/ia-sync/zsh/` (repo copy); live `~/.config/zsh/`
  is the deployed instance it may *verify against*, not the place it treats as truth.
- Weight sits on the table: wiring docs, RAG substrate references point at ia-sync paths.
- **On-host sync probe (operator ask):** `deploy.sh` writes a stamp on every run —
  `~/.config/zsh/.deployed` containing `<commit> <date> <machine>`. Anyone on the host
  can read sync state in place: `cat ~/.config/zsh/.deployed` vs `git -C ~/ia-sync
  rev-parse --short HEAD`. Stamp is live-only: add `.deployed` to `sync.deny`.

## 3 · One line in zsh AGENTS.md — DONE (this commit)

Added at the top of the lighthouse, live + repo, deployed repo-first.

## 4 · Codex CLI sync leg — DESIGN (build waits on WS5 gavel)

Facts (Eagle over `reposoma/maintenance/codex-line/` + local inspection, 2026-07-30):
- Installed on **office** 2026-07-25, codex-cli 0.145.0, smoke GREEN (@Trajectory).
  **Home install status: not documented anywhere.** Runcard names no machine.
- Program: nabla-lab, canon `0005 Amendment A1`. Harness artifacts staged in
  `.larva/agents-staging/`, deploy pending **WS5 roster gavel**. Runcard:105 already
  anticipates an ia-sync commit for this.
- Gemini line frozen 2026-07-24; its patch-protocol transfers vendor-free.

Leg design (`codex/` in ia-sync, guarded `[ -d ~/.codex ]` so it no-ops where absent):

| Path | Verdict | Why |
|---|---|---|
| `config.toml` | SYNC (114 B, no secret-ish content — re-verify before first sync) | user-level config; project-level silently drops safety keys, so user-level is the only real config |
| `hooks.json` | SYNC | exists by default at install — diff, don't assume empty |
| `skills/` | SYNC | analogue of claude skills leg |
| `auth.json` | **NEVER** (mode 600 credential) | codex.deny |
| `installation_id` | **NEVER** — machine identity | codex.deny |
| `*.sqlite*`, `cache/`, `log/`, `sessions/`, `shell_snapshots/`, `models_cache.json`, `packages/`, `plugins/` | NEVER — state, not config | codex.deny |

## 5 · `~/.majkee` sync leg — DESIGN (blocked on a fact)

**Reality check finding: `~/.majkee` does not exist on office.** It presumably lives on
home — office cannot inspect it. This is itself the doctrine in action: the item as
stated assumed a path this machine cannot confirm.

Design (activates via the same `[ -d ]` guard the other legs use):
- Synced like `~/.claude` — full leg, `majkee/` in the repo.
- Excluded: `export/` (tcr + repomix outputs, process data) — **registry-shaped**, not
  hardcoded: per-leg deny file `majkee.deny`, same format and loader as `sync.deny`.
- Repomix exclusion of `~/.majkee` in outputs: `tcr.*` config concern, separate registry.

## Registry generalization (falls out of 4+5)

`sync.deny` today is zsh-leg-only. Generalize to per-leg deny registries — `sync.deny`
(zsh, unchanged name), `codex.deny`, `majkee.deny` — one loader in `sync.sh`. Precedent
already in the tree: `registries/config.sync.json` drives the guide-publish sync the same
declarative way. Smallest change that makes exclusions data instead of code.

## Naming note (operator ruling)

`ia-sync` stays `ia-sync` (should have been `ai-sync`; renaming now buys nothing and
breaks paths, scripts, mail routing). The **vocabulary** name is *surgical table* — use
it in prose; the path stays as it is.

## Open (parked, own loop)

- Home-side facts: does `~/.majkee` exist there; is codex installed there — first
  `/multihost` reply from home should answer both.
- WS5 gavel → unblocks codex leg build + wrapper/agent-card deploy.
- Temple ratification → unblocks banner application (item 1).
- Banner + stamp + repoint (item 2 build) — after the above land.
