# ia-sync Session Memory

**Project:** ia-sync (machine project registry, agent launchers, zsh lifecycle)  
**Session root:** `/home/hruzam/ia-sync/session/`  
**Scope:** GitHub-reconciliation checkpoint — 34 repos on hruzam account, local placement inventory  
**Status:** Read-only investigation complete; awaiting human confirmation for next steps  

---

## §0 Pinned (Current State)

**Active phase:** GitHub-reconciliation reporting (read-only, no mutations)  
**Current blocker:** 5 CANDIDATE repos + 8 NOT-FOUND repos need placement decisions  
**Who owes what:** @majkee to confirm per-repo go-ahead (pull, clone, placement)  
**Reference:** @Vector completed the scan (delegated, strictly read-only via `gh repo list`)  

---

## §1 Narrative

2026-07-20: @Vector executed read-only reconciliation of 34 repos on GitHub account hruzam, cross-checked against local filesystem + git remotes. Output: 18 pull-candidates (existing local folders, remotes verified); 5 CANDIDATE repos (real decision needed: forks with mismatched local remotes, or missing remote config); 8 NOT-FOUND repos (real placement decision needed: no local folder yet, hypotheses offered); 3 uncloned forks (flagged separately, intentional gaps?). No mutations executed. Awaiting @majkee's go-ahead for per-repo dirty/divergence checks before pulling.

---

## §2 Locked (!D)

| Decision | Details | Date |
|----------|---------|------|
| Home shell bootstrap: no delete-before-port on normalizer.py / registry | Do NOT delete `~/.config/zsh/normalizer.py` or `~/.config/zsh/harness.machine-project-registry.json` until BOTH are done, in order: (1) Home's `PROJECT_*` exports ported inline into `zsh/config.home.zsh`; (2) FRESH login shell verifies all `PROJECT_*` paths resolve (`fo im psd ltp lrv sess` all green). Only after both pass may files be removed. Rationale: `~/.config/zsh/config.zsh:26-30` defines every `PROJECT_*` by `eval`-ing normalizer.py output against registry JSON; if either file missing, guard fails → `[ERROR] Could not find normalizer or registry file` → all six project switchers break (same class as 2026-07-07 office audit repair). Source: office seat (@Kelvin), relayed via @majkee. Scope: home machine only. Status: binding on @Houston and any implementer. | 2026-07-29 |

---

## §3 Open (?Q)

| Question | Scope | Date |
|----------|-------|------|
| Which of the 18 pull-candidates to actually pull, after dirty-check? | Dirty/divergence check needed per-repo before pulling — machine has been unsynced long time | 2026-07-20 |
| Resolution for 5 CANDIDATE repos (claude-code-config.AnastasiyaW fork, gemini-cli fork, kukla, StroMy, fantasyobchod fork) | Forks with local remotes pointing to parent (not fork) or missing remote config — clarify intent | 2026-07-20 |
| Placement choice for 8 NOT-FOUND repos | fantasyobchod.devenv, applications-in-common, applications-in-common.devenv, repomix-store, freya.full-sync.git-ignore-limited, RAG.notion, docs, othergit — folder-name hypotheses offered, needs confirmation | 2026-07-20 |
| Should 3 uncloned forks be cloned locally? | awesome-claude-code, claude-code-hooks-mastery, mcp-server-architect — may be intentional gaps | 2026-07-20 |

---

## §4 Philosophical (?P)

---

## §5 Gaps (?G)

| Gap | Detail |
|-----|--------|
| Stale registry reference | `~/ia-sync/zsh/harness.machine-project-registry.json` is stale: PSD path case mismatch (psdvsSys); LTP path now actually holds psdvsSys, not Laravel-training-project · flagged for Kelvin/Maxwell (registry owner), not edited by this task | 2026-07-20 |
| 404 dangling reference | `~/www/legacy.session` remote points to `hruzam/Session.git`, which 404s on GitHub (deleted/renamed repo) · separate issue, not investigated | 2026-07-20 |

---

## §6 Fine Notes (~N)

| Note | Detail |
|------|--------|
| Folder name mismatches ~N | Several repos have stale or case-mismatched folder names vs GitHub canonical names (e.g., larva → larva.v0, psdvsSys → Laravel-training-project) — recorded per-repo, not auto-fixed |
| Pull readiness ~N | 18 pull-candidates are confirmed local + remote matches, but machine has been unsynced a long time — dirty/divergence check is mandatory before blind pull |
| Office reply channel ~N | Office delivers its replies to home in the GIT COMMIT MESSAGE body, not as a file in `_mail/`. After fetching, read `git log origin/main` bodies to retrieve them. Noted 2026-07-29. |

---

## §7 Fork Points (*F)

| Fork | Detail |
|------|--------|
| @Eagle orientation agent *F | User floated building a real orientation agent (@Eagle) conditional on this session proving valuable · not a commitment, provisional idea pending outcome of this reconciliation cycle |

---

## §R Registries

### Scope: 34 GitHub Repos on hruzam Account

**18 pull-candidates** (local folder exists + remote verified):
- remote-hub (`~/.remote`)
- reposoma (`~/reposoma`)
- nabla-lab (`~/nabla-lab`)
- freya.devenv (`~/www/imago_cz/freya.devenv`)
- psdvsSys (`~/www/Laravel-training-project` — folder name stale)
- ia-sync (`~/ia-sync`)
- oldSync (`~/www/oldSync`)
- subai.devenv (`~/www/ovum/subai.devenv`)
- piql.dev (`~/www/piql/piql.dev`)
- larva.dev (`~/www/ovum/larva.dev`, backup at larva.dev-bckp same remote)
- reposoma.devenv (`~/www/ovum/reposoma.devenv`)
- freya.devstudio (`~/www/imago_cz/freya.devstudio`)
- ovum.bus (`~/www/ovum/bus/ovum.bus`)
- larva (`~/www/ovum/larva.v0` — folder name mismatch)
- agents-sources (`~/www/agent_builds_sources` — no name resemblance)
- LARVA_PEPAGI (`~/www/LARVA_PEPAGI`)
- PSDVS (`~/www/psdvs` — case mismatch vs registry only)
- gemini-cli-mcp-servers.ksprashu (`~/www/_agents/gemini-cli-mcp-servers.ksprashu`)

**5 CANDIDATE repos** (real decision needed):
- claude-code-config.AnastasiyaW (fork; local remote points to parent, not fork)
- gemini-cli (fork; same pattern)
- kukla (local repo exists, no remote configured, no commits)
- StroMy (three name-candidate folders, none are git repos)
- fantasyobchod (fork; three candidate folders all point to parent org, not fork)

**8 NOT-FOUND repos** (real placement decision needed):
- fantasyobchod.devenv
- applications-in-common
- applications-in-common.devenv
- repomix-store
- freya.full-sync.git-ignore-limited
- RAG.notion
- docs
- othergit

**3 forks with no local clone** (flagged separately, may be intentional):
- awesome-claude-code
- claude-code-hooks-mastery
- mcp-server-architect

---

## §A Archive

(none yet)
