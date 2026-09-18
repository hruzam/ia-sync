---
goal: the tunnel's parametrization is reachable per-vault and canon describes it truthfully — a named preset drives a real thread instead of the operator remembering flags
gate: a preset named in `zsh/registries/tunnel.json` opens a tunnel thread whose sandbox AND reasoning effort demonstrably match that preset, proven by one live turn (`tun status` + one `tun ask`)
participant_1: [trajectory, {brand: "Claude Code", model: opus-5, effort: high}, host: "home"]
status_owner: trajectory
---

# RUNBOOK — tunnel-upgrade-01-parametrization

Run shape: **from hand, light trace** (operator call). Minimum compliant file set only —
this RUNBOOK + STATUS.md. No PAD (no human-run sequential steps), no `_bus/` (solo seat),
no `dock.md`.

## prompt-0

Upgrade the Claude↔Codex tunnel so its settings are reachable per-vault, and correct the
canon that currently describes them wrongly. Authoring surface is
`/home/hruzam/ia-sync/zsh/ai/tunnel-codex.{py,zsh}` — **compose-first: never edit
`/home/hruzam/.config/zsh/ai/` directly** (`/home/hruzam/ia-sync/SYNC_DISCIPLINE.md`).
Documentation surface is `/home/hruzam/reposoma/raw.guides/tunnel/`.

Gating follows `/home/hruzam/ia-sync/protocole/colors/PROTOCOLE.md`: reads and zero-quota
probes run free; append-only dev-layer writes are done-and-declared; canon, deployed
surfaces, and anything spending quota stop for @majkee.

### T1 — correct canon (audited edit, NOT gavel-gated)

Four statements in `/home/hruzam/reposoma/raw.guides/tunnel/` contradict observed 0.154.0
behaviour. These are **meaning-preserving factual corrections**, so they are normal audited
edits, not gavel ceremony (calibration: the DRAFT/gavel wall is reserved for changes that
turn a behavioural pattern or a decision).

1. `res/user-run.md` — "multi-repo work would force `danger-full-access`" is mechanically
   false; `sandbox_workspace_write.writable_roots` covers several repos while everything
   else stays EROFS. **Correct the mechanism, preserve the policy** as an explicit house
   choice rather than a necessity — @majkee's standing preference is unresolved, so the
   rewrite must not silently delete the restriction.
2. `res/settings.md` — Route B is described as unavoidably global; per-spawn `-c` gives
   per-vault scope (no-daemon: one app-server per verb).
3. `res/user-run.md` + `dev-journal.tunnel.md` — "sandbox fixed at thread birth" is 0.152.1
   weather; 0.154.0 exposes per-turn `sandboxPolicy`. Document it as **declined by house
   rule**, not as impossible.
4. `/home/hruzam/ia-sync/AGENTS.md` — three wrong host facts: tmux "absent on home" (it is
   3.7c and live), tmux version row says 3.7b, and `ls -d ~/projects` is listed as an
   office-only discriminator but exists on home. These are host-resolution claims, the
   highest-cost kind to leave wrong.

### T2 — shim: reach the knobs

**Opens with a live verification turn, not closes with one.** Handshake acceptance of
`-c sandbox_workspace_write.writable_roots=[…]` is proven; a *born thread honouring it* is
NOT. If threads ignore spawn-level sandbox config, T3's registry loses half its value and
the design changes — so spend that ping first.

Then, smallest primitive that covers the most:
- forward `-c key=value` pairs when spawning `codex app-server --stdio`
- context-occupancy % in the usage tail, computed from `last.input_tokens /
  modelContextWindow` (never from `total_token_usage`)
- `close` prints threadId + transcript path before discarding state (orphan-guard)

Verification order is fixed: selftest (zero quota) → `deploy.sh --dry-run` → deploy →
selftest against the live copy → one live `tun ask "ping"`.

### T3 — registry + subchapter

`zsh/registries/tunnel.json` (fifth sibling to `ai/hosts/palette/projects.json`) plus a
`res/registry.md` chapter. **Bundler, not compiler:** store vendor key spelling verbatim
(`sandbox_mode`, `model_reasoning_effort`, `writable_roots`, `network_access`); invent only
the bundle name. Colour labels map to PROTOCOLE tiers. Seed three presets, one per colour —
registries rot when seeded speculatively.

T3 introduces new behaviour, so the chapter lands marked `[DRAFT]` pending @majkee's gavel.
No self-gavel of canon, ever.

## Known constraints and destructive holds

- **Commits are held by @majkee** — "we commit later, it requires a gentle approach."
  Nothing in this session commits or pushes.
- **Office is quiet** (operator declaration, this session): no inbound sync from
  `hruzam-120922` while this runs. This is what makes T2's deploy safe to attempt at all.
- **`deploy.sh` is itself modified and uncommitted by another session** — it adds a
  `~/.nanorc` leg (additive, `-f`-guarded, benign to the zsh leg). Consequence: running
  `deploy.sh` for T2 will ALSO deploy `nano/nanorc`, another session's uncommitted work.
  Surface this to @majkee before the deploy leg, not after.
- **ia-sync worktree is dirty with foreign work** — 8 modified + 4 untracked paths that are
  not this session's (`deploy.sh`, `journal.host-cleanup.md`, `zsh/session/runbook.py`,
  `zsh/system/dashboard.md`, `zsh/session/help/**`, `nano/`, `terminal/`). Do not stage,
  revert, or clean anything outside this session's own files.
- **Law 2.4** — the operator opens the tunnel table; no seat enables itself. Every `send`
  and `ask` spends real ChatGPT quota from the shared pool.
- **Never touch `~/.codex/thread-writer-locks/`** (@Cartan verdict 2026-09-03).

## references

Point, never copy.

- Knob semantics, the three routes, deploy discipline: `raw.guides/tunnel/res/settings.md`
- Parametrization ceiling, `-c` keystone, session-hygiene facts:
  `raw.guides/tunnel/src/observation.parametrization-and-session-hygiene.2026-09-18.md`
- Kernel enforcement (Landlock + seccomp):
  `raw.guides/tunnel/src/observation.sandbox-enforcement-mechanism.2026-09-17.md`
- Field-usage lessons ladder: `raw.guides/tunnel/dev-journal.tunnel.md`
- Exchange law: `/home/hruzam/ia-sync/HANDSHAKE.md` §TABLE
- Gating tiers: `/home/hruzam/ia-sync/protocole/colors/PROTOCOLE.md`
- Session standard: `~/reposoma/raw.guides/{runbook,status}/GUIDE.md` (held resident by
  @field for this session — ask rather than re-read)

## Deferred out of this session

**Session-control verbs** (`tun threads` / `tun bind` / `tun name` over `thread/list` +
`thread/setName`). Separable capability, larger surface, does not serve this gate — it
earns its own session. Protocol support confirmed present; shim exposes none of it.
