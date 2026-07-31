# The keyboard — AI interactive surface map (claviature)

`~/.config/zsh/guides/keyboard.md · audience: operator+agent · machine: office · verified: 2026-07-11`
`status: LOCKED 2026-07-11 — majkee gavel · @Janus REVISE folded · amended same-day after the
style-repair production (aliases-only convention now LAW: guide-for-builder.md §Architecture rules).`
`lineage: the agentive/human-friendly claviature is a larva inheritance (temple/legacy-wall.md).`
`scope: the AI keyboard (ai/keyboard.zsh). The GLOBAL claviature is BUILT: derived 'keys' panel —
guides/claviature.global.spec.md.`

---

## The grammar (LOCKED)

1. **One interactive surface per family** — `keyboard.zsh`: **aliases and comments ONLY, no
   function bodies** (tightened 2026-07-11, operator-gaveled). Bodies live in scope-named
   engines wired by `base.zsh`. **LAW: `guide-for-builder.md` §Architecture rules —
   pattern-read BEFORE writing.**
2. **Key shape: `<family>-<action>`** — forward derivability from *intent*; the registry is an
   intent map, never an engine-origin map (Janus).
3. **One gated family = one prefix.** Everything temple-gated is `temple-<action>`.
4. **The shim class:** read-only panel keys allowed — max one per engine, panel-listed, never
   for state-writing operations. Writes carry the full gated name (`temple-mail-manage`).
   *Origin:* shims are anti-merge compensation — the valve that keeps the doorbell-merge
   instinct parked (07-08 log; split is load-bearing, 0009-L5).

### Prefix registry (intent-keyed)

| prefix | intent | gate |
|---|---|---|
| `g-` / `gemini-` | talk to a Gemini seat | — |
| `agy-` | talk through Antigravity CLI | — |
| `rc-` | Claude Code remote control | — |
| `temple-` | temple business (mail · doorbell · trees) | **GATED (0009)** |
| `harness-` | settings-card freshness | — |
| `fr-` | freya.devenv transport | — (P11) |
| `bo-` | fantasyobchod.devenv transport | — (P11) |
| `devenv-` | devenv panel/help | — (P11) |
| `keys` | the derived global panel itself (bare, like `g`) | — (P12) |
| `project-` | project-map surface (paths · git status · batch commit · fzf picker) | — (P15) |
| `zenith-` | zsh config RAG assistant (Haiku · read-only · broken-wiring log) | — (P16) |

> The machine-readable twin of this table lives in `ai/keys.zsh` (family + singles maps,
> gavel C). New family = one line there; unregistered keys surface in UNSORTED.

---

## Key map (mirrors `keyboard.zsh` partitions — keep 1:1 on any keyboard change)

| P | family | keys | bodies in |
|---|---|---|---|
| 1 | general CLI | `g` · `g-ver` · `g-help` · `agy-ver` · `agy-help` | — |
| 2 | safety / YOLO | `g-yolo` · `g-skip` · `agy-yolo` · `agy-skip` | — |
| 3 | Gemini seats | `g-orby` · `g-bluebottle` (+ `gemini-*` long forms) — retired 2026-07-31: `g-vega` · `g-astro` · `g-astro-yolo` (chairs → Codex, 0005 A1; see `codex-relay.contract.md`) | per-agent `.sh` (executed) |
| 4 | agy wrappers | `agy-orby` — retired 2026-07-31: `agy-vega/astro/astro-yolo` · `agy-astrobley` | `gemini-processor.sh` |
| 5 | — | retired 2026-07-11: Gemini Epoch seat killed (accident; **@Epoch = Claude line only**) | — |
| 6 | hygiene | `gemini-fresh` · `agy-fresh` | `gemini-processor.sh` |
| 7 | help | `ai-help` (**master** — prints all sections) | `claude.zsh`; Gemini section in `gemini-processor.sh` |
| 8 | Claude RC | `rc-status` · `rc-freya` · `rc-reposoma` · `rc-nabla` · `rc-stop` | `claude.zsh` |
| 9 | temple panel | `doorbell-run` · `doorbell-smoke` · `doorbell-log` · `transport-selftest` · `mail-pick` (shim) · `temple-mail-manage` (E — write, full name) | `temple-*.zsh` |
| 10 | temple utilities | `tree-snapshot <project>` · `temple-help` | `temple-tree.zsh` · `claude.zsh` |
| 11 | devenv transport | `fr-sync/deploy/status` · `bo-sync/deploy/status` · `devenv-help` | `devenv.zsh` (pull --rebase built in) |
| 12 | global claviature | `keys` · `keys --plain` (agents) · `keys --all` (include shell internals) | `keys.zsh` (`_keys`) |
| 13 | octopus launcher | `octo` | `claude.zsh` (`_octo`) |
| 14 | editor-pin keymap | `pinkeys` | `claude.zsh` (`_pinkeys`) |
| 15 | project-map surface | `project-paths [--plain\|--paths]` · `project-git-status` · `project-commit-all [--dry\|--push]` · `project-help` · **Alt-p** (ZLE picker) | `temple-project-surface.zsh` |
| 16 | Zenith-ZSH RAG | `zenith-zsh` (interactive) · `zenith-zsh "query"` (one-shot) | `zenith-zsh.sh` (executed) → agent `zenith-zsh.md` |

Harness: `harness-stale` (base.zsh P2). Partition/engine inventory (authoritative):
`guide-for-builder.md` §Architecture rules — point, never copy.

## Agent invocation form

```bash
zsh -c 'source ~/.config/zsh/ai/base.zsh && <key> [args]'
```

---

## Warts — final ledger (resolved 2026-07-11)

| # | wart | resolution |
|---|---|---|
| 1 | shims vs functions double-naming | shims stay as a **named class**: read-only, one per engine, panel-listed; writes never shimmed |
| 2 | opaque `aihs-` | renamed → `harness-stale` |
| 3 | bare `epoch` | dissolved by extermination — accidental cross-line seat killed; @Epoch = Claude line only |
| 4 | P100 `tempail` | died with engine-E adoption (`temple-mail-manage`) |
| 5 | help panels | `ai-help` = single master; raw derived layer beneath = `keys` (P12) |

## Post-production reconciliation (2026-07-11)

All audit-session edits survived the style-repair production; new engines
(`claude.zsh` · `devenv.zsh` · `gemini-processor.sh` · `keys.zsh`) conform to the grammar;
`base.zsh` header repaired (was self-describing as `ai.zsh`).

## Standing instrument

- **Global claviature BUILT** (`keys`, spec: `guides/claviature.global.spec.md`) —
  UNSORTED baseline 120 keys = the lazy-retrofit backlog (session_* · substrate_* · piql-* ·
  php* …); register families one line at a time as folders get touched.
  **Pending: operator finger on `keys` in a live shell (L5 gate).**
