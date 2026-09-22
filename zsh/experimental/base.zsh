#!/usr/bin/env zsh
# =============================================================================
# BASE.ZSH — the experimental/ signpost (scope folder, ai/-pattern)
# =============================================================================
# Location: ~/.config/zsh/experimental/base.zsh (authored on the surgical table
# ~/ia-sync/zsh/ — deploy.sh spreads to both machines; never edit live copy)
# Sourced by: config.<machine>.zsh (interactive shells), guarded
# Contract: idempotent + side-effect-free on source — defines only, never runs
#           work or prints (decision 0009 L2 discipline).
#
# Scope: experimental — opt-in, portable experiment bricks that earn a run but
# not yet a first-class Claude/Codex/Gemini surface. Promoted to its own level
# (sibling of ai/) 2026-09-22: naming them "experimental" but hiding them inside
# ai/ made orphans.
#
# Two brick kinds, distinguished by entrypoint filename (LAW — see README Contract):
#   experimental/<id>/runner.zsh — LAZY exp-run runner. Nothing loads at shell
#     startup; the dispatcher only ever `zsh`'s it on demand (mechanical safety —
#     a broken runner cannot break the shell, only its own invocation).
#   experimental/<id>/<id>.zsh   — SOURCED interactive brick (P3 below). Loads at
#     shell startup by EXPLICIT name, `zsh -n`-gated (a syntax error skips the
#     source — command absent, not shell dead). Define-only: no work, no prints.
# Contract for adding a brick: experimental/README.md.
# =============================================================================

# -----------------------------------------------------------------------------
# MAINTAINER LOG — plugged experimental bricks
# -----------------------------------------------------------------------------
# STANDING RULE: every brick below is EXPERIMENTAL ONLY until @majkee approves
# its graduation to a first-class surface (Claude/Codex/Gemini/a stable scope).
# Until approved it stays here — opt-in, lazy via exp-run or explicit-sourced via
# P3, never wired into a stable scope. A brick has two possible fates: GRADUATE
# (remove its row here, move it out — canon elsewhere) or TRASH (deemed
# inappropriate; remove its row here as the LAST step of the purge procedure in
# README.md "Remove a brick" — quarantine, verify, THEN purge, never in one step).
#
# Format: <id/file> — plugged <date> — <origin> — <what it probes> — <status>
#
#   ox-alpha              — plugged 2026-09-22 — promoted from ai/experimental/
#                           — OpenRouter stealth/ox-alpha reasoning-model probe;
#                             reference runner brick — EXPERIMENTAL ONLY (not approved)
#   reincarnation-session — plugged 2026-09-22 — promoted from ai/experimental/
#                           — tmux bed (claude-0/1, codex-0) with pipe-pane
#                             transcript; loose script, not an exp-run brick
#                           — EXPERIMENTAL ONLY (not approved)
#   4x1                    — plugged 2026-09-22 — staged by @Metaterminal, wired by
#                           @Trajectory (advisor-advanced consulted: proceed, Option A)
#                             — tmux session-fold bed, N named windows, thin/no-cage;
#                             SOURCED brick (P3), not a runner; brief proposed its own
#                             top-level 4x1/ scope, hosted here instead (operator call)
#                           — EXPERIMENTAL ONLY (not approved)
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# PARTITION 1: control panel (aliases only — bodies live in the dispatcher)
# -----------------------------------------------------------------------------
[[ -f ~/.config/zsh/experimental/keyboard.zsh ]] && source ~/.config/zsh/experimental/keyboard.zsh

# -----------------------------------------------------------------------------
# PARTITION 2: dispatcher engine (_exp_list / _exp_run bodies; runners stay lazy)
# -----------------------------------------------------------------------------
[[ -f ~/.config/zsh/experimental/dispatcher.zsh ]] && source ~/.config/zsh/experimental/dispatcher.zsh

# -----------------------------------------------------------------------------
# PARTITION 3: sourced-function bricks (interactive; loaded at shell startup)
# Wired by EXPLICIT NAME ONLY — never globbed — one line per brick, added in the
# SAME edit as its maintainer-log row above. MECHANICAL GATE: `zsh -n` must pass
# or the brick is skipped (degrades to "command absent", never "shell dead").
# Bricks must be define-only: no work, no prints on source (0009 L2 discipline).
# -----------------------------------------------------------------------------
[[ -f ~/.config/zsh/experimental/4x1/4x1.zsh ]] \
  && zsh -n ~/.config/zsh/experimental/4x1/4x1.zsh 2>/dev/null \
  && source ~/.config/zsh/experimental/4x1/4x1.zsh
