# Global claviature — LOCKED design spec · BUILT

`~/.config/zsh/guides/claviature.global.spec.md · audience: builder+operator · machine: office · verified: 2026-07-11`
`status: DESIGN LOCKED + BUILT 2026-07-11 (majkee re-gaveled F → build-before-audits, so the
drift detector serves the audit sessions). Final L5 gate PENDING: operator finger on 'keys'
in a live shell (Sunday).`
`consumes: temple board row "claviature" (global half — consumable after operator verify).`
`floor: guides/keyboard.md (LOCKED grammar).`

---

## Governing insight

**Derive, don't register — the locked grammar is what makes derivation possible.**
A derived panel reads the live shell at call-time (defined aliases + functions), buckets them
by the locked family prefixes, and prints the whole machine's keyboard. No registry → cannot
rot. No merge → cannot become the monolith (killed 2026-07-03). Anything outside a known
family surfaces in UNSORTED — **the naming grammar becomes a live drift-detector.**

## Gaveled decisions (majkee, 2026-07-11)

| G | decision |
|---|---|
| A | Engine home: `ai/` + wired via `base.zsh` — agents get it too. **Doctrine note (majkee):** `ai/` = SCOPE, not "dedicated-to." *Build note: shipped as `ai/keys.zsh` (scope-named engine, culture-off-disk rule — same rule gavel B applied to the key name; substance of A intact).* |
| B | Master key: **`keys`** — one deliberate bare word (like `g`); "claviature" stays off the machine surface. |
| C | Family list = constant arrays inside the engine (prefix map + singles map). Registers FAMILIES, never keys — the one named deviation from "register nothing." Extension = one line. |
| D | Unknown keys print under **`UNSORTED (grammar drift)`** — lint by visibility, never hidden. |
| E | Lazy retrofit stays — subfolders adopt their own keyboard.zsh on next touch. |
| F | ~~Build after reconciliation + audits~~ → **re-gaveled "build" 2026-07-11:** built before the audits so the panel watches them. |

## As built (2026-07-11)

- **Engine:** `ai/keys.zsh` — `_keys [--plain] [--all]`, sourced by `base.zsh` PARTITION 9.
  Alias `keys` in `keyboard.zsh` PARTITION 12 (aliases-only convention held).
- **Noise filter (post-build tune, same day):** zsh/plugin runtime machinery (p10k, compinit,
  zle widgets… — `_KEYS_NOISE` patterns array, extension = one line) is hidden from UNSORTED
  and summarized as `(+ N shell internals hidden — 'keys --all' to include)`. Rationale: a
  drift detector nobody can read detects nothing; internals are not keyboard keys. `--all`
  is the escape hatch — nothing is invisible, only folded.
- **Baseline at build:** 120 genuine UNSORTED keys (session_* · substrate_* ~47 fns · piql-* ·
  php* · composer* · +vi-* · misc). **This is the lazy-retrofit backlog made visible** —
  register families (one line each) as subfolders get touched; the two project audits are
  expected to consume part of this list.
- **Agent form:** `zsh -c 'source ~/.config/zsh/ai/base.zsh && keys --plain'`.
- Verified non-interactively (Trajectory + Delta, exit 0, epoch-free). **Operator finger =
  the standing L5 gate — run `keys` and `keys --all` in a live shell.**

## Maintenance

- New key → appears automatically. New family → one line in the prefix/singles map.
  Forgot the line → the key shows in UNSORTED until registered. Noise pattern missing →
  one line in `_KEYS_NOISE`.
- Curated help panels (`ai-help`, `temple-help`, `devenv-help`) remain the prose layer ABOVE
  this raw derived layer — two layers, different jobs.
- **Builder LAW** for any change: `guides/guide-for-builder.md` §Architecture rules,
  pattern-read BEFORE writing.
