---
title: 007-researcher — Epoch's role statement and inputs (written against the 006-supervisor brief)
date: 2026-11-25
by: Epoch · Claude · home (hruzam)
scope: how the researcher seat relates to the supervisor seat; facts and scars to carry into P1. No phase started, nothing decided.
status: DRAFT input — not canon; majkee gavels
---
_Written against `../006-supervisor/BRIEF.md` (the supervisor group's intake brief); every "BRIEF" / "BRIEF §" below means that file, not a 007 brief._

# Epoch — role here, in my own words

**What I am.** The researcher seat: I recalibrate to today's date, fetch live sources, and report
claims with source + date + confidence (H official · M reliable secondary · L inferred). I read and
fetch; I do not run Bash; I cannot edit existing files (Delta does); my own writes are reports and
my single-writer log `~/reposoma/pulse.epoch.md`.

**What I am not, relative to `supervisor`.** Not the controller, not a candidate for the seat, not an
authority holder. The supervisor directs; I answer version-sensitive questions for it. My lack of
Bash is a feature for this role — it is why my output is evidence, not action.

**How the supervisor should use me.** Spawn me *before* any decision that depends on a version,
flag, model string, price, path or tool capability — especially the launcher/attach equipment in
BRIEF.md §Wiring map. Brief me with the question and the wanted shape; I return findings (WHAT /
SINCE / SOURCE / CONFIDENCE / IMPACT / ACTION). I never treat my own earlier answers as sources.

## Inputs I can hand over now (as-of, all STALE until re-fetched)

From `raw.settings/raw.card.claude-code.md` (refresh delta 2026-10-08 and 2026-11-23, changelog
`code.claude.com/docs/en/changelog`; latest seen v2.1.330, 2026-11-20). Relevant to BRIEF
constraint 3 ("attach comes from mechanism") and to full-permission equipment:
- `claude attach|logs <partial-name>` shipped v2.1.290 — a **native** attach/log surface;
  candidate alongside the tmux/zellij session in BRIEF §3. Not read in docs, only in the changelog.
- Permission-shaping flags seen: `--permission-prompts none` (v2.1.259, unattended hosts),
  `--restricted` (v2.1.248), auto mode default on (v2.1.284) with `permissions.defaultMode`
  honoured for `auto`/`bypassPermissions` only from user/managed settings or `--permission-mode`,
  never from project/local settings.
- Hooks fail closed: PreToolUse/PermissionRequest matcher errors now BLOCK (v2.1.288); a hook
  that errors no longer blocks a Code Mode script call unless `"onFailure":"block"` (v2.1.329).
  Any "leash" the authority contract relies on needs these facts re-read first.
- `claude remote-control` exists with `--settings <file>` (v2.1.321); Trusted Devices beta.
- Scheduled tasks / `/loop` now run up to 30 days (v2.1.330); `/tasks` lists them (v2.1.329).
- Codex side (card codex-cli, 2026-11-23): 0.171.0 has `codex exec --remote`, `/rc` `/remote`
  remote control and device pairing. Not verified: app-server/thread supervisor semantics —
  relevant to the existing `zsh/ai/tunnel-codex.zsh` surface in BRIEF §4.

## Research questions I can run on request (sources named, no answers pre-supplied)

1. Exact current semantics of `--dangerously-skip-permissions` / `bypassPermissions` / auto mode on
   a persistent session, and what managed settings can still deny — `code.claude.com/docs/en/`
   settings + permissions + changelog.
2. What `claude attach` / `claude logs` actually attach to (background sessions? named sessions?),
   how it interacts with a tmux-held process — CLI reference docs.
3. Codex full-permission mode, app-server thread model, `codex exec --remote`: what is the
   attachable unit — `github.com/openai/codex` releases + docs.
4. Whether the "supervisor"/"controller" wording collides with product terms in either vendor's
   docs (BRIEF §Name evidence was blind-reader based, not doc based).
5. Host pins for tmux/zellij on home / office / monitor (needs a Bash seat; I only specify it).

## Scars from today's scheduler work that bear on BRIEF constraints 1–2

(Evidence: reposoma `324eb4c`, ia-sync `8b4d3ed`, `dc897cc`; ledger in `pulse.epoch.md`.)
- **Authority contract precedes the launcher.** Today a read-only seat's claim ("job not installed")
  was written into a ledger as fact after checking ONE host; the other host was running it. A
  full-permission seat makes that class of error mutate things. Contract must say which claims need
  multi-host evidence before an action.
- **Trigger, not hand-run, is done** (decision 0009 L5): a script moved to a new path while a live
  systemd unit still pointed at the old one is the standing example. Deploy has no `--delete`, so
  "removed from source" does not mean "removed from host" — the supervisor needs an explicit
  removal step per host.
- **Single writer + dirty trees.** Office `~/reposoma` carries uncommitted foreign work; any
  unattended commit loop must stage explicit paths only, never `git add -A`.
- **Header honesty.** I bumped a card's `verified:` date after a PARTIAL read and had to flag it
  myself; an unattended seat needs "never let a status field hide a known gap" written down.
- **Don't relay sub-agent claims as facts.** I repeated a subagent's "key mismatch" claim without
  checking; it was false. Supervisor-level reports should mark relayed vs. verified.
- **Referent rule holds in practice:** mechanism (timer, tmux session, launcher) kept being
  confused with the seat in conversation — BRIEF constraint 1 is worth enforcing in prose too.

## First concrete workload candidate

The autonomous card-refresh loop — `.dev/session/zsh-scheduler-00-epoch-autonomous-card-refresh/raw/HANDOFF.epoch.autonomous-card-refresh.2026-11-23.md`.
It needs exactly the equipment BRIEF describes (headless/attachable process, hard 320-min kill,
per-item commits) and its authority questions (staging vs direct fold, one host, explicit-path
staging) are a small, real test of the supervisor's authority contract. Suggest it as the witness
workload for one runtime, not as scope for this group.

## Not verified

Everything in "Inputs" above is from my own cards and the changelog excerpts read on 2026-11-23,
not from the reference docs; no flag was executed; no host was inspected for tmux/zellij.
