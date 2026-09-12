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

c1_verdict (2026-09-10): PASSED, crossed receipts.
  - auth chain: Redmi → forced agentive → living sessions witnessed BOTH sides
    (claude atlas-ui `…-722`; codex TUI `01a08ad5-…-fee9f`, head pane captures)
  - approval: codex first honestly refused the receipt (automatic review) → majkee
    switched /approvals to asking mode → dialog confirmed FROM THE PHONE; pane witness
    "✔ You approved codex…mktemp /tmp/codex-phone-approval.XXXXXX" + artifact
    /tmp/codex-phone-approval.MRktSw (13:08)
  - survival: kicked by app-switch + connection abort + lock-screen wake — the 21-day-old
    agentive bed never died; after battery exemptions even the Termux client survived lock
  - gate clause note (gaveled at rotation): "zero authorized_keys changes" read as no
    access-ARCHITECTURE changes; like-for-like key rotation recorded above.
  Friction list (feeds C2): (a) glyph boxes → FIXED live (JetBrainsMono Nerd Font pushed
  to ~/.termux/font.ttf); (b) wants buttons/aliases/cover → extra-keys macros + widgets +
  bed aliases; (c) passphrase-per-connect → ssh-agent once per boot; (d) transient aborts
  → auto-retry attach loop; (e) stale client pins geometry → `window-size largest`;
  (f) codex ships in automatic review → help card documents /approvals asking mode;
  (g) HyperOS exemptions (No restrictions Termux+Tailscale, pin in Recents) → README
  provisioning step.

c2_progress (2026-09-10): AUTHORED + HEAD-REVIEWED. @Delta built 7 files under
  /home/hruzam/ia-sync/devices/_shared/termux/ (termux.properties extra-keys w/ S1–S4 +
  PASTE + DETACH · bin/bed host-picker w/ ssh-agent-once + retry-on-255 · bin/agentive-seed
  4 windows + window-size largest · bin/agentive-send · 2 widgets · README). Head review
  found 4 defects (agent re-prompt leak, retry-on-any-exit, INVERTED battery advice,
  claude-on-phone fiction) — Delta correction round applied, verified line-by-line by
  head, sh -n PASS on all scripts. NOT pushed to device yet.
  Cartan counter-sign (tunnel thread on majkee's shared channel .dev/session/
  tunnel.state.json): round 1 NOK (agent-bootstrap race; bare tmux vs absolute-binary
  law) → fixed. Round 2 NOK (no re-check inside lock; lock released before ssh-add) →
  finding 1 ACCEPTED (double-checked locking applied), finding 2 DECLINED by head
  ruling: lock across an interactive passphrase prompt = stale-lock hazard on abandoned
  prompt, worse than a rare duplicate prompt; residual risk accepted, rationale in
  bin/bed comment. Transport note for transfer letter: tunnel shim wait-window dies on
  research-grade turns (two interrupted turns; 'no web search, local reads only'
  workaround holds) — tunnel v1 candidate.

c2_verdict (2026-09-10): COUNTERSIGN-OK (Cartan, round 3, tunnel thread on majkee's
  shared channel — operator's standing pattern: .dev/session/tunnel.state.json, root
  path + per-bed pattern both commit-proofed in .git/info/exclude). PUSHED + INSTALLED
  on the Redmi over :8022: ~/bin/bed (+ $PREFIX/bin symlink, on PATH), ~/.shortcuts/*,
  extra-keys appended to ~/.termux/termux.properties + reloaded. Both beds SEEDED
  (agentive-seed): office = living codex on window 0 + seats 1–4; home = fresh bed 0–4;
  window-size largest set. NOTE: Termux:Widget APP not installed on device (only
  com.termux present) — home-screen taps need it (F-Droid, must match Termux install
  source); typed `bed office` is the equivalent path meanwhile. NOTE: S1–S4 buttons
  reach windows 1–4; the living codex sits on window 0 (Ctrl+b 0 by hand, or future S0).

GATE: PASSED 2026-09-10 (verbatim gate above). Evidence set: C1 crossed receipts
  (approval from phone + artifact /tmp/codex-phone-approval.MRktSw + lock/kick survival,
  pane captures both sides) · C2 pushed+installed, Cartan COUNTERSIGN-OK r3 · acceptance:
  button rows live (screenshot 13:47), DETACH clean, re-entry with NO passphrase (agent
  persistence), PASTE from mobile notes app landed in office shell (PTYRA lane proven).

closing_sweep (owed before prune):
  - [x] transfer letter → raw/trajectory.experience-transfer.2026-09-10.md
  - [x] C4 frame → res/reaudit.cold-start-frame.md
  - [x] piql-Houston mail (ssh surface: device key rotation both PCs) — sent to the
        houston bus as trajectory.device-key-rotation.2026-09-10.md (inbox → archive
        after read; no inbox path cited per scar 3)
  - [ ] C3 both-doors: head launches claude in seat 1; majkee verifies same session in
        mobile app (1 min of his hands)
  - [x] shell-seat landing: SHIPPED for PC path as bin/agentive-door (561e324) —
        tso -t enters through it. Phone path DEFERRED by majkee ("I'll manage on
        phone later"): needs his one-line forced-command paste per PC
        (command="sh /home/hruzam/ia-sync/devices/_shared/termux/bin/agentive-door",
        options + from= pin unchanged); trade-off noted: reattach lands on shell,
        C-b l returns to the TUI. S0 button not needed meanwhile.
  - [ ] journal entry + commit + prune: DEFERRED — journal.host-cleanup.md and AGENTS.md
        are dirty under other owners (hold); majkee sequences the commit
  - promotion manifest (scar 4) — raw/ keepers, EVERY one:
    * codex-remote-control-cli/raw/brief.implementation.byAsymmetry.2026-09-04.md → keep
      with program (02/03 siblings still feed on it)
    * codex-remote-control-cli/raw/brief.implementation.session-bed.v2.bySymmetry.2026-09-04.md
      → same
    * 01-wrapper/raw/trajectory.experience-transfer.2026-09-10.md → PROMOTED 2026-09-11 to
      incarnations-00-mechanism/raw/ (the next cSharp arc opened there; majkee-directed move,
      stub left at the old path); therapy fold still owed
    * tunnel.state.json (root, git-invisible) → operator's standing channel, NOT pruned
    * phone ~/.ssh/id_ed25519*.old + both PCs' authorized_keys.pre-rotation-2026-09-10
      → delete after majkee confirms new key stable (his call at prune)

adjacent_strand (post-gate, majkee-requested 2026-09-10 — NOT wrapper-gate work, sequence
  its own commit/deploy separately):
  - home bed locale FIXED: agentive-seed exports LANG=en_US.UTF-8 (bricks/flat-color came
    from a bed born under bare non-interactive locale); home server re-seeded + glyph-
    verified (═╰ ✓). office bed was already UTF-8 (born from a login shell Aug 20).
  - PC→PC bed access: `tso -t|--bed <peer>` added to _ts_session in
    zsh/system/tailscale.zsh (engine body; keyboard.zsh comment updated — aliases-only law
    respected). Twin of phone `bed`; peer is any resolvable tailnet name (3rd PC = zero
    code); LANG injected in the remote command. zsh -n PASS, 5-case dispatch matrix PASS.
  - DEPLOYED (majkee blessing 2026-09-10): office live via targeted flow (backups
    .bak-2026-09-10); commits 68b6661 (flag) + 561e324 (agentive-door: tso -t lands on a
    plain-shell seat) pushed; home = pull + targeted cp (finishing block handed over).
    Guide concentrated: /guide remote-cli (reposoma c1b35a3). Tunnel shim wait-window
    issue journaled: raw.guides/tunnel/dev-journal + src/observation (reposoma 7cf85c4).

next: PARKED TO THE PAD — all deferred testing (C3 both-doors · tso -t maiden voyages ·
  phone loop · widget one-tap · phone-door decision · rotation cleanup gate) lives in
  pad.1-deferred-testing.md in this folder. Driver: @Vara live session (doubles as the
  new walker's field test), majkee's hands, sat whenever he picks it up. After the pad:
  journal entry + prune sequencing (majkee's gate; journal.host-cleanup.md dirty under
  another owner).
