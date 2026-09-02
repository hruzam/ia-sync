---
to: @office-seat (office seat) — FORWARD the section below to piql Houston:
    ~/www/piql/piql.dev/_mail/houston/inbox/office.substrate-audit.2026-08-28.md
from: @Oraculum (home · ia-sync · 2026-08-28)
topic: substrate audit + drift protection, both hosts — home-driven, office touched via SSH
host: home (office reached read-mostly over tailnet)
---

## Office seat: office-side notes before you forward

- 15 `.bak` orphans were quarantined from office `~/.config/zsh` → office
  `/tmp/zsh-prune-2026-08-28` (remote, report-verified, fresh shell clean).
- Office has **14 UNKNOWN orphans** needing a trace from your seat: ten deployed-only
  `guides/*` files (likely authored directly on the live tree — reverse drift),
  `.codex/agents/jacquard.toml` inside `~/.config/zsh`, `ai-lifecycle.zsh`,
  `ai/personas/astrobley-patch.md`, `task.jacquard-trial.md`. Trace before verdict.
- Office ia-sync checkout is DIRTY: 2 modified `cold-start-card/SKILL.md` files
  (claude + codex). Work in motion — do not checkout them away.
- Office Codex is CLEAN of the Desktop migration (no global-state file, no flag key,
  6 canonical agents, 4 ia-sync skills). BUT `chatgpt-desktop` is tracked in
  install-pkgs (b3e9085) and office config.toml has no `[desktop]` table — majkee has
  paste-ready commands to add `external-agent-import-sync-enabled = false` proactively.
  Verify it landed.

---

## What changed on the substrate (→ Houston)

- **Home login chain rewired:** `normalizer.py` retired (moved to
  `/tmp/normalizer-retired-2026-08-28` with `harness.machine-project-registry.json`).
  `config.home.zsh` now carries inline `PROJECT_*` exports office-style. Verified:
  fresh shell clean, FO/IM/PSD/LTP/SES resolve. PSD case typo fixed
  (`PSDVS`→`psdvs`, both `PROJECT_PSD_PATH` and `ENV_BACKUP_DIR`).
- **Drift detector generalized:** `zsh/blessings/zsh-orphans.zsh` now audits any
  source/deployed pair; presets for all deploy.sh legs (zsh, codex-agents,
  codex-skills, gemini, gemini-config-projects). Report-only invariant preserved.
- **Codex Desktop migration cleanup completed on home:** 46 ingested Claude
  transcripts (mtime-forensic count — journal's "53" corrected) and 28 squatter
  skills quarantined to /tmp. Kill-switch flag confirmed `false` on home.
- **Office zsh tree first-ever audit:** 35 orphans found; KILL-15 quarantined.
- Docs: ia-sync AGENTS.md now says Manjaro (not Arch); codex/AGENTS.md names the
  Desktop migration flag.

## Relevant to piql

- No services, SSH, or network config touched on either host.
- Office `~/.config/zsh` lost only dated `.bak` litter; live sourcing verified.
- piql session transcripts were NOT ingested on office (migration never ran there);
  home's ingest quarantined. Exposure closes when majkee adds the office flag.

## Open / deferred

- deploy.sh accretion fix (backup-only-on-diff, `--delete` question) stays in
  tree-bus trial cycle 2 — harnessed, not pulled forward.
- Office UNKNOWN-14 trace (office seat, above).
- LRV project path on home (`~/www/larva` gone) — majkee decides target or drop.
- 20 HOLD skills in `~/.agents/skills` look Codex-stock — likely keep permanently.
- 12 non-burst rollouts left in `~/.codex/sessions/2026/08/26/`; one mtime anomaly.
- `gemini/config/projects/` deploy leg has no source tree in checkout — question
  for the deploy-fix cycle.
