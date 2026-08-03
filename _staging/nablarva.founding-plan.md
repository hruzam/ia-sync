# nablarva — founding plan (gaveled synthesis, 2026-08-01)

**Status:** approved via /buffering-cycle smooth phase (majkee, 2026-08-01).
**Seat:** atlas-ui (office). Krakens dispatched per phase.
**This file:** the plan of record until the project harness exists; then it moves into
`nablarva/` and this copy dies.

---

## Identity

- **Project:** `nablarva` — the temple's experimental bed for agentive primitives.
  Currently living on **home** as `kuklab/provisorium/` (ad-hoc name). `kuklab/` is the
  parent folder, not a machine.
- **Devenv sibling:** `nablarva.devenv` (temple topology canon).
- **Git:** two private repos, same names, via `gh` CLI.
- **Model:** the AUR flow without the borrowed name — experimental builds live here,
  are read before they run, and get **promoted** to the surgical table (`~/ia-sync/`)
  only after review. Never auto-deploy from here.
- **Metaphor layer (culture, off the disk contract):** the larva stage — builds here are
  larvae; promotion to the surgical table is metamorphosis. Sits beside the factory's
  marine line (medusa · polyp · larvaTmux) without touching it.

## Naming law for primitives born here (atlas = designer)

- **Agents = real programs:** terse lowercase Unix-tool names, man-page bodies,
  one name = one job, grep-able. No poetry on the disk contract.
- **Skills = class methods:** `<program>-<verb>` (invoked *on* a program).
- **Duplicate/interference check is mandatory before any name lands:** sweep
  `~/.claude/agents/`, `~/ia-sync/claude/{agents,skills}/`, `~/.config/zsh/` functions +
  aliases, and PATH binaries. (`larva.zsh` in projects scope is retired old-era — flag
  to majkee if found live; not a naming constraint.)

## Phases

| Ph | Work | Executor | State |
|----|------|----------|-------|
| A | Scout home over tailscale (100.110.27.60): locate `kuklab/provisorium/`, read its PROJECT.yaml if present — that defines the pull scope (@Eagle). Then rsync ONLY the scoped content → `~/kuklab/nablarva/` on office. Home otherwise untouched: majkee re-clones home via git by hand and cleans it himself | @Eagle scout → atlas pull | **DONE 2026-08-01** — real home path was `~/provisorium/nabLarva` (no `kuklab` on home; `kuklab/` created office-side). 9 md files / 76K pulled to `~/kuklab/nablarva/`. No harness, no git in payload — Phase B authors fresh |
| B | Harness bed: AGENTS.md · flag · pulse · PROJECT.yaml + `guides/` scaffold per /new-project checklist | atlas + @Eagle | **B0 DONE** — placement ruled `~/kukla/nablarva` (home-root scope-group, majkee gavel over www; canon amendment parked). **B1 drafted** 2026-08-01: AGENTS.md · PROJECT.yaml · session/{plan,flag,pulse} · docs/ · parked beacon · .gitignore. @Janus challenge dispatched; majkee gavel next. GAVELED 2026-08-02 with amendments: scope-group renamed → `~/unikuklatrix/`; plan.md abolished (flag L9, survival survey); uncanonical `session/dock.md` born |
| C | `nablarva.devenv` sibling + synchro wiring | @Trajectory | **DONE 2026-08-02** — template applications-in-common.devenv (freshest, self-contained); flat layout; sync verified |
| D | `git init` ×2 · `gh repo create` ×2 (private, same names) | atlas | **DONE 2026-08-02** — hruzam/nablarva + hruzam/nablarva.devenv, both PRIVATE, branch core |
| E | zsh wiring | zenith-zsh map → @Eagle table-confirm → atlas | **AUTHORED 2026-08-02** — own scope folder `ia-sync/zsh/nablarva/{base,keyboard,nablarva}.zsh` (ai/-pattern, majkee-directed; first project-scoped keyboard-exp) + config.office.zsh hook + temple-project-map entries. Verified in isolation. **DEPLOY = majkee's trigger** |
| F | Inject experimental builds — REROUTED (majkee gavel 2026-08-02, flag L10): temple pilots (incl. Pilot 3 routing A/B) → **elements-factory experiment space**; Pilots 1–2 stay structural → surgical table; nablarva history stays pure animal | atlas, step-by-step with majkee | rerouted |
| G | Pads for manual testing: @Eagle locates larvaTmux pad pattern in the factory; copy the pattern in | @Eagle → @Delta | pending |
| H | Philosophy layer | atlas | **FOLDED 2026-08-02** — (2) promotion protocol = flag L6; (3) D2′ guardrail = flag L7. (1) provenance-header template deferred to the FIRST experimental build (factory-side per L10) — write it where the build happens, not speculatively |

## Parked (surfaced at close, per buffering-cycle underline rule)

- **Registry beacon** (`registry/nablarva.md` + index row) — reposoma is read-only under
  the pending two-sided merge. The beacon text lives inside `nablarva/` ready-to-drop;
  majkee/Houston lands it in reposoma after the merge.
- **Home-side wiring** — majkee wires home manually later; office is the live copy.

## Verification gates

- A: `ls` the pulled tree, byte-count sanity vs home, no partial rsync.
- D: `gh repo view` both repos private.
- E: new shell sources clean; no function/alias collisions in the tree.
- F: each build carries the PKGBUILD-analog header before it lands.
