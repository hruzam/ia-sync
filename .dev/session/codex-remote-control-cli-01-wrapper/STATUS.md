# STATUS — codex-remote-control-cli-01-wrapper

updated: 2026-09-10
writer: trajectory (oStar head · status_owner — seated by the v3 redraft under majkee's
  gavel, session fc-sync.trajectory-cSharp.cli-remotes)
host: office (fingerprint: /usr/bin/php74 present)
worktree: /home/hruzam/ia-sync · main · dirty with OTHER sessions' files (ownership holds,
  untouched)

gate: From the Redmi, wrapper v0 over the existing `agentive` rail drives a full Codex TUI
on office — one live bash-approval confirmed from the phone keyboard, session surviving
phone lock + reattach — with ZERO `authorized_keys` changes.

checkpoint: v3 RUNBOOK seated (oStar head; scope gaveled: autonomy + host-bed command +
  4-seat sub-tabs + shared prompt buffer + PTYRA paste target + Claude both-doors).
  C0 office side PASSED by head probe 2026-09-10:
  - `Linger=yes` (no operator mutation needed)
  - `tmux has-session -t agentive` → exists live
  - `~/.local/bin/claude` + `/usr/bin/php74` present
  Home probe same day: tmux 3.7c present over tailnet; `claude` NOT on non-interactive
  SSH PATH (absolute-binary law derives from this). C0 CLOSED 2026-09-10, both phone
  lanes verified live by the head:
  - adb lane: Redmi authorized via home (`adb devices` → device, model 2508CRN2BE);
    Termux + Tailscale installed, Android 15, battery 91%; Xiaomi input-injection toggle
    ("USB debugging (Security settings)") deliberately NOT enabled — C1 stays human.
  - USB ssh lane: `adb forward tcp:18022 tcp:8022` on home → ssh Termux over the cable
    (USB-LANE-OK; home key already seated) — provisioning possible with zero network.
  - tailnet lane: Redmi online; office → `ssh -p 8022 hruzam@100.105.201.3` OK
    (TAILNET-LANE-OK; office key seated). sshd + termux-wake-lock running (majkee hands).

in_flight: none

rotation_2026-09-10: device→PC key rotated (old passphrase lost — recovery, not architecture;
  majkee gavel "anyway → proceed"): head generated fresh ed25519 on the Redmi over the
  verified lane; majkee pasted the swapped entries on BOTH PCs by hand (classifier blocked
  the head, per session.next.md JIT law — correctly) — backups
  `~/.ssh/authorized_keys.pre-rotation-2026-09-10` on office + home; caged options
  byte-identical, only key material changed. New passphrase set BY majkee on-device
  (ssh-keygen -p, 12:07) — never in files/chat. Verified: entries grep=1 on both PCs;
  journal shows attempts from pinned 100.105.201.3; BatchMode "denials" were the
  passphrase working as designed. Cleanup owed at close: `~/.ssh/id_ed25519*.old` on
  phone + the two .pre-rotation backups. Friction → C2 scope: ssh-agent in wrapper
  (one unlock per Termux boot).

recovery_probe: `ls /home/hruzam/ia-sync/devices/_shared/termux/ 2>/dev/null`
  → listing exists = prompt-3 (wrapper) authored; check checkpoint for Redmi push state.
  → "no such file" = pre-wrapper; session sits at C0-phone / C1.

holds:
  - no authorized_keys edits (dispatcher = pain-gated v1)
  - other sessions' files incl. dirty AGENTS.md: no stage/commit/stash/edit
  - OWED EDIT (not ours to land): AGENTS.md prose "tmux absent on home" is wrong —
    evidence: live probe 2026-09-10, `ssh hruzam@100.110.27.60 'tmux -V'` → 3.7c;
    table row was already right. Land by its owner or re-flag at gate close.
  - full deploy.sh under palette.map hold — targeted flows only
  - tunnel: state explicit, never committed; never unlink ~/.codex/thread-writer-locks/*;
    one stored thread for the whole session (each send = real ChatGPT turns)
  - devices never pull; tablet read-only; Codex approvals stay ON
  - absolute binaries in every wrapper command (home PATH scar)
  - single RC cloud seat — last claimer wins; no --continue for remote

c1_progress (2026-09-10, in flight): auth chain PASS — majkee entered the living agentive
  bed from the Redmi (attached atlas-ui claude session `…-722`). Friction so far:
  (a) glyph boxes → FIXED live: head pushed JetBrainsMono Nerd Font over the lane to
  `~/.termux/font.ttf` + termux-reload-settings; (b) wants buttons/aliases/wrapper cover
  → confirms C2 scope (extra-keys macros, widgets, bed aliases, ssh-agent);
  (c) passphrase-per-connect → ssh-agent queued. OWED for gate: codex approval from
  phone + lock ≥2 min + reattach.

next: majkee finishes prompt-2 (C1 driving test) with his hands, same sitting —
  Redmi Termux → ssh hruzam@100.126.182.111 → forced `agentive` → codex → confirm one
  bash-approval FROM THE PHONE → lock ≥2 min → reattach; friction notes back to the head.
  (Phone-side C0 — Termux sshd :8022 up + optional adb auth on home — folds into the same
  sitting.)

expected: C1 PASS + friction list recorded here → head spawns @Delta for prompt-3 (wrapper
  build incl. bin/bed host-slots, 4-seat windows, prompt buffer) → majkee opens the tunnel
  table once for Cartan's counter-sign → C3 checklist → C4 frame → gate close with
  transfer letter + promotion manifest.
