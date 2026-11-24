---
title: 006-supervisor — group intake brief
date: 2026-11-24
by: Trajectory · Claude · home (hruzam)
scope: intake only — name, referent, constraints, source map; no phase started
---

# 006-supervisor — intake brief

## Intent (Majkee, 2026-11-23/24)

One vendor-invariant seat, callable as a Claude agent and as a Codex agent, running as a
full-permission open-bash process the operator can attach to. On first sight it should read
as the controller of the system. Cartan's full-permission Codex mode is the Codex-side
model of the wanted equipment; the Claude side needs the same equipment.

## Name: `supervisor` (operator-kept 2026-11-24)

Reserved vocabulary: `control` / `ctrl` / `controller` belong to
`.dev/session/germline-A3-guide-to-controller/`; this group does not use that root.

Naming evidence (first-impression reads, no repo context, 2026-11-23/24):

| reader | strongest "attachable controller" | weakest | note |
|---|---|---|---|
| Claude Haiku (blind) | supervisor (control half), console (attach half) | driver | |
| Claude Sonnet (blind) | supervisor | driver | attach is the weaker half; reached via a client |
| Codex / Cartan (CHALLENGE) | supervisor — proceed | — | runner-up `driver` (vendor split: Claude reads it as passive adapter) |

Earlier craft-name round (machinist, helm, warden, steward, …) is superseded by the
operator's criterion "reads as controller in real code".

`supervisorcli` was assessed and not adopted as the seat name: a CLI names a one-shot client,
the opposite of a persistent attachable seat, and it names the launcher rather than the seat
(exactly the referent risk below). The command-line entry follows the existing `ai-<seat>`
convention instead.

## Constraints carried into P1

1. **Referent rule (Cartan):** `supervisor` is the persistent, interactive seat that directs
   the system. The launcher / tmux|zellij session that keeps it alive is mechanism, not a
   second "supervisor".
2. **Equipment ≠ authority:** full bash and attach are equipment. Authority (what it may
   decide, mutate, deploy, delete, commit/push; what stays Majkee's) is its own contract,
   stated once in shared identity and expressed natively per vendor. Authority contract
   precedes any full-permission launcher.
3. **Attach comes from mechanism, not the name.** Candidate: named multiplexer session
   (tmux present on office and home; zellij present on both). Host pins: resolve at entry.
4. **Existing "supervisor" surfaces to reconcile, not duplicate:**
   - `codex/skills/codex-harness/SKILL.md:36,39` — "exec/SDK/app-server supervisor" (concept match).
   - `zsh/ai/tunnel-codex.zsh` — "Codex app-server stored-thread supervisor" (termbrana 03-tunnel
     v0, not deployed). Decide: reuse as Codex-side mechanism, cite, or keep distinct.
5. **Overlap check:** `claude/agents/metaterminal.md` (Claude-only, human-invoked only, never
   deploys, not a spawn target) — reuse/fold/keep-separate disposition owed in P1.
6. **Bridge to A3 is optional and later:** supervisor may consume A3 controller/function
   outputs; A3 ownership and acceptance stay A3's.

## Wiring map (source → deploy target; compose in repo, never in live dirs)

| surface | source | pattern to copy |
|---|---|---|
| shared identity | `germline/agents/supervisor/identity.md` | `germline/agents/oraculum/` |
| native bindings | `germline/agents/supervisor/binding.{claude,codex}.md` | same |
| Claude agent | `claude/agents/supervisor.md` | `claude/agents/oraculum.md` |
| Codex agent | `codex/agents/supervisor.toml` | `codex/agents/oraculum.toml` |
| launcher | `zsh/ai/claude.zsh` `_supervisor` + `zsh/ai/keyboard.zsh` alias `ai-supervisor` + `zsh/ai/keys.zsh` | `_metaterminal` / PARTITION 13 |
| deploy | `deploy.sh` dry-run, then deploy | SYNC_DISCIPLINE.md |

Scoped acceptance: Majkee accepts a supervisor seat with a reviewed cross-vendor authority
contract, native Claude and Codex entries plus attachable launcher, dry-run-verified deploy and
fresh-session witnesses on both runtimes (or named deferrals).
