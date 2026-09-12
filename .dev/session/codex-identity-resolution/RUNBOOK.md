# RUNBOOK — codex-identity-resolution

```yaml
goal:            One Astrobley behavior source (posture) with two Codex-native adapters — the existing
                 spawned custom agent and a new sovereign top-level profile — plus a narrow
                 default-plus-explicit-override paragraph in the portable Codex AGENTS.md, deployed and
                 behaviorally proven, so the operator can appoint a named top-level seat at session
                 creation without weakening Cartan's default residency.
gate:            Fresh-session proofs P2–P6 (draft §Future RUNBOOK proof plan) agree on the seat map —
                 unprofiled root = Cartan default · `--profile astrobley` root = sovereign Astrobley ·
                 spawned custom agent = bounded Astrobley child · resume preserves the profiled seat ·
                 negative activation refused — over a deployed single-posture source, with open
                 decisions 1–5 gaveled and the observed commands recorded in the closing VERDICT.
participant_0:   [cartan, {codex, gpt-5.6-sol, high}, office, resident]
participant_1:   [@majkee, human, office]
status_owner:    cartan (from wake; planning head wrote the initial snapshot)
schema_note:     raw.guides/runbook/GUIDE.md verified 2026-09-05 + res/cross-vendor-seat.md (DRAFT)
```

> **Read once.** Position belongs only in `STATUS.md`.

## Why this session exists

The 2026-09-06 sidequest proved that `agent_type: astrobley` pasted into a running Codex root window
is not an identity switch: the root stayed controller, spawned a child, then crossed ownership by
acting as Cartan. The full observation and the lean proposal live in
`raw/draft.codex-session-identity-resolution.2026-09-06.md` — this session implements that proposal's
"smallest viable implementation" and runs its proof plan. The draft's five "Open decisions for a
future RUNBOOK" belong to this session and @majkee's gavel.

Installed-feature check: Codex profiles (`$CODEX_HOME/<profile>.config.toml`, `--profile`) are the
native mechanism; the delta built here is posture extraction, repo wiring, deploy mapping, and the
behavioral proof. A future Codex CLI that launches a top-level session directly from a custom-agent
file would retire the profile adapter — record that seam, do not design around it.

## Fixed implementation shape (draft §Smallest viable implementation)

1. Extract stable Astrobley behavior from `/home/hruzam/ia-sync/codex/agents/astrobley.toml` into
   one posture document (portable home per gaveled decision 1; draft proposes `codex/postures/`).
2. Reduce the custom-agent TOML to a spawned adapter pointing at the posture.
3. Add one portable top-level profile source deploying to `~/.codex/astrobley.config.toml`
   (mechanism per gaveled decision 2).
4. Add the default-plus-explicit-override paragraph to `/home/hruzam/ia-sync/codex/AGENTS.md`
   (wording subject to @majkee's gavel; draft §Keep Cartan as the default).
5. Dry-run deploy the named Codex files only, deploy after confirmation, compare source/live bytes,
   then prove behavior from fresh sessions (P2–P6).

## prompt-0 — cartan (resident · sole implementer and STATUS writer)

Executor grade: senior judgment throughout — identity seams, deploy boundary, and doctrine wording
are all in play; no delegation in the first cut.

Read, in order:

1. `/home/hruzam/ia-sync/.dev/session/codex-identity-resolution/raw/draft.codex-session-identity-resolution.2026-09-06.md`
2. `/home/hruzam/ia-sync/SYNC_DISCIPLINE.md` and `/home/hruzam/ia-sync/deploy.sh` (the Codex
   deploy mapping as it actually is — decision 2 evidence)
3. `/home/hruzam/ia-sync/codex/agents/astrobley.toml` and `/home/hruzam/ia-sync/codex/AGENTS.md`
4. `/home/hruzam/reposoma/raw.guides/runbook/res/cross-vendor-seat.md` (your own instrument contract)

Then, staged:

- **Stage A — decision brief.** Propose concrete answers to draft open decisions 1–5 with disk
  evidence (deploy.sh mechanism, path choices, BUS-field choice for `topology`). Write the brief to
  `raw/`, update STATUS, park for @majkee's gavel. Author nothing under `codex/` before the gavel.
- **Stage B — author + P0.** After the gavel: implement steps 1–4 above exactly as gaveled, run
  draft P0 (TOML validity, model/effort/sandbox fields, name resolution, shared posture pointer),
  record results in `raw/`.
- **Stage C — deploy boundary (P1).** Produce the dry-run deploy naming only the authorized Codex
  surfaces; park for @majkee's confirmation; after deploy, byte-compare source/live. No push, no
  cross-host carry, no reposoma writes.
- **Stage D — proof support.** Author the exact probe prompts and expected-report shapes for P2–P6
  into `raw/`; @majkee runs the fresh windows. Record observed behavior only — never infer a proof
  from files existing. Close with a VERDICT recording the observed commands, the seat map, and a
  promotion manifest naming every `raw/` keeper.

## prompt-1 — @majkee (gavel and fresh-session hands)

Gavel the Stage A decision brief (open decisions 1–5) and the AGENTS.md override wording. Confirm
the dry-run before any deploy. Open the fresh windows for P2–P6 yourself — including the P3
two-window collision test (Cartan live in one window, `--profile astrobley` in another, disjoint
write paths in a disposable session bed) and the P4 resume (`codex resume --profile astrobley
<SESSION_ID>` from `codex agents`). Your observed commands, not the candidate spellings here, are
what the closing VERDICT records.

## Known constraints and destructive holds

- Live `~/.codex` is a deploy target, never an authoring source. No session IDs, histories,
  approvals, auth, caches, or other host-local state enter Git — `<SESSION_ID>` stays out of BUS
  artifacts, portable config, and history.
- No deploy without a dry-run naming only the authorized surfaces and @majkee's explicit
  confirmation (SYNC_DISCIPLINE). Deploy is additive — plan for stale-file cleanup if paths move.
- The worktree is shared with live sessions (`runbook-upgrade`, `reversal-tunel-00-leader`,
  `codex-remote-control-cli-01-wrapper`); their dirty files and holds are protected. This session
  writes only under its own folder, `codex/`, and the pulse router line. @majkee owns commits.
- Astrobley only (decision 3 lean default) unless the gavel says otherwise. No role registry,
  daemon, window launcher, session-ID transport, or generic persona/RPG framework in the first cut.
- P3 uses a disposable session bed — never `runbook-upgrade/_bus/` or any live session's surfaces.
- The AGENTS.md paragraph is a proposal until @majkee gavels its wording; the stronger-than-
  `I can be any seat` semantics (explicit, launch-time, named, operator-controlled) are the floor.

## references — point, never copy

- `/home/hruzam/ia-sync/.dev/session/codex-identity-resolution/raw/draft.codex-session-identity-resolution.2026-09-06.md`
- `/home/hruzam/ia-sync/HANDSHAKE.md`
- `/home/hruzam/reposoma/raw.guides/runbook/res/cross-vendor-seat.md`
- `/home/hruzam/ia-sync/SYNC_DISCIPLINE.md` · `/home/hruzam/ia-sync/deploy.sh`
- `https://learn.chatgpt.com/docs/config-file/config-reference` (profiles; consulted 2026-09-06)

## What closes this gate

Decisions 1–5 gaveled; sources authored and deployed with byte-match; fresh-session observations
P2–P6 agree with the draft's §Acceptance shape; the closing VERDICT records the observed commands
and seat map; a promotion manifest names every `raw/` keeper.

## Deliberately out of scope

No presence-board implementation (res/presence-board.md domain), no profiles for other seats, no
Claude-side seat changes, no BUS schema fork for `topology` (prefer an existing field per decision
5), no home-host deploy (arrives with the normal pull+deploy cycle), no automation of window
launching or session-ID discovery.
