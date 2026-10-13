# atlas-ui package — `shuttle`, the provisional BUS seat (review stage)

`what: one vendor-neutral source + one Claude rendering for the temporary BUS seat of Protocol 1.`
`state: REVIEW — nothing here is loaded by any runtime until majkee promotes it (below).`
`authored: 2026-10-03 · atlas-ui · brief: ../brief.atlas-ui.2026-10-03.md · return: ../atlas-ui.return.2026-10-03.md`

## Layout

```
germline/agents/shuttle/identity.md   source — gen: germline · scope project:ia-sync · lifetime = this bed
render/claude/shuttle.md              Claude rendering = frontmatter + stamp + identity body + Claude VENDOR DELTA
README.md                             this file — activation · deactivation · loading · proofs
```

Rule (`~/reposoma/.germline/README.md`): source → stamped one-way rendering; never edit the
rendering; re-render from source. The rendering here is hand-composed (no renderer exists yet);
its stamp says `revision: unresolved` until the source is committed.

## Activation — majkee only, after review

1. Promote the source: `mkdir -p ~/ia-sync/.germline/agents/shuttle && cp germline/agents/shuttle/identity.md ~/ia-sync/.germline/agents/shuttle/identity.md`
2. Promote the rendering: `mkdir -p ~/ia-sync/.claude/agents && cp render/claude/shuttle.md ~/ia-sync/.claude/agents/shuttle.md`
3. Commit both in ia-sync; then replace the stamp's `<revision: unresolved …>` in the rendering with
   `git -C ~/ia-sync log -1 --format=%h -- .germline/agents/shuttle/identity.md` and commit again.
   (Two commits because the revision does not exist before the first.)
4. No `deploy.sh` leg is involved: `~/ia-sync/.claude/` is read in place by Claude Code when the
   session's cwd is inside ia-sync. It is NOT the surgical table (`~/ia-sync/claude/`) and does not
   reach `~/.claude/` or the home box's live tree.

## Loading mechanism — and how it is checked

- Claude Code loads project agents from `<cwd>/.claude/agents/*.md`. `name: shuttle` = the selector.
  Precedence (Sella L6, agents): project beats user — no global `shuttle` exists, so no shadowing.
- The `gen: germline` sign lives in the **source** frontmatter; in the rendering it is the first body
  line (HTML comment) — no invented keys in a native agent file (Sella Walk A·3). If an unknown
  frontmatter key is later proven tolerated, majkee may move it up; not assumed here.

## Proofs — claimed vs. still needing a fresh-session behavior proof

| # | claim | status | proof (fresh session, never `-p`) |
|---|---|---|---|
| 1 | `cd ~/ia-sync && claude --agent shuttle` enters the seat with its body as system prompt | UNVERIFIED (project-scoped direct entry) | run it; first turn must name the bed and refuse to act without a RUNBOOK |
| 2 | sending needs an enabled table (exit 10) — **this does NOT prevent the seat from running `open --enable` itself** | exit 10 CLAIMED from the shim contract; operator-only enable = INSTRUCTION unless separately enforced | from the seat: `tun send "x"` with no table → exit 10, nothing created. Optional enforcement (majkee's call, not built): project `~/ia-sync/.claude/settings.json` deny on `Bash(*tunnel-codex.zsh open*)` — then prove the deny fires |
| 3 | head binding check works | CLAIMED | `tun status` must show `threadId` + runtime stamp (`cwd`, sandbox, effort, model, instructionSources) equal to the RUNBOOK's; mismatch → seat stops. Birth (reading A) only if authorized: first `send` carries the head brief, receipt records `birth`. Bind (reading C) is the operator's `open --thread` + `resume`, never the seat's |

Mechanism vs prose (Trajectory's scar: "gates must be mechanisms or files read at decision time,
not sentences in a brief"). Mechanical today (BRICK-01, 2026-10-03 — uncommitted in ia-sync, deployed
on office): exit 10 (send needs a table) · exit 61 (`<state>.lock`, one turn in flight) · exit 50
(send/ask reconcile mismatch) · `--cwd` persisted in the handle (head identity) · `tun status` runtime
stamp (binding check). Prose only: write scope · operator-only `open` (unless the deny rule above) ·
the scribe boundary (rule 8b). The prose rules are exactly what proof #4's diff review watches.
| 4 | write scope holds | PROSE ONLY — tools allow more | Assay-grade review of the first cycle's diff: only `_bus/NN.shuttle.*` and `raw/shuttle/**` touched |
| 5 | model/effort pinned | CLAIMED (frontmatter) | `/status` or the session header in the fresh session shows sonnet · high |
| 6 | head's effective permissions | OUT OF SCOPE for this seat — RUNBOOK acceptance evidence (Cartan: `tunnel-codex.py:306`) | dated proof-run by the head's owner |

## Deactivation — at the tunnel-02 gate

Owner: the cSharp head's closing sweep (first in, last out), with majkee's hand for the writes:
`git rm ~/ia-sync/.claude/agents/shuttle.md`; move `~/ia-sync/.germline/agents/shuttle/` into the
bed's `raw/atlas-ui/retired/` (or delete — majkee's call); one line in `journal.host-cleanup.md`.
If the pilot proves the shape, the *lessons* fold into Flight's project-session mode as "working
head under a foreign head" — the seat itself still retires. Closing the pilot must not leave a
standing role, here or in the global roster.

## Not in this package

No Codex twin (brief). No `_bus/` files (born only when the session has two live seats). No
RUNBOOK (Cartan authors it). No tunnel handle (operator's `open --enable` creates it).
