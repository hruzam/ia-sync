# galaxy-tab-a-2016 — action log (append-only)

- 2026-08-18 — Recon from office: tailnet online; sshd not running (connection refused).
- 2026-08-19 — sshd up on 8022 (operator started it). Key auth denied — pubkeys not
  seated yet. Ping works via DERP relay only. No changes made on-device.
- 2026-08-19 — Operator ran bootstrap step 2 (home pull only). Verified: home→tablet
  key auth OK (`id_ed25519`, 1 key in authorized_keys). Office→tablet still denied.
- 2026-08-19 — Tablet reached home host shell passwordless via Tailscale SSH
  (`ssh hruzam@hruzam`) — finding recorded; ACL fix drafted.
- 2026-08-19 — Office-key relay-append attempt blocked by permission classifier;
  returned to operator hands (bootstrap step 2, office line).
- 2026-08-20 — Both hosts hardened (harden-host 1.0: MariaDB loopback, sshd key-only,
  ufw). Executed by @Flight, directed by @Oraculum. Journal: ia-sync 2026-08-20 entries.
- 2026-08-21 — **Tailnet ACL pasted by operator** (grants dialect: computers full mesh;
  androids → office/home tcp:22 only; Tailscale SSH back to check/nonroot) +
  `tailscale set --ssh=false` on hosts. Verified from THIS tablet:
  - `ssh hruzam@hruzam` → permission denied (publickey) — passwordless shell GONE ✅
  - `mysql -h 100.110.27.60` → ERROR 2002 errno 115 timeout — 3306 blocked by grant ✅
  - `db-reach` office→home → 12.3.2-MariaDB through tunnel, clean teardown ✅
  Weak-spot thread (opened 2026-08-19): **found → demonstrated → contained. CLOSED.**
- 2026-08-20 — Step 0: battery exemption set by operator (Termux + Tailscale).
  Step 1: office RSA key relayed via home→office→tablet pipe (operator ran from home;
  home ed25519 already seated 2026-08-19). office→tab verified OK.
  Termux sshd hardened to key-only (PasswordAuthentication no + KbdInteractiveAuthentication no).
  Key-only reconnect from office verified.
- 2026-08-20 — Step 2 complete: JIT keygen done on device (ed25519, passphrase in operator's head).
  Restricted authorized_keys entry added to office + home (operator pasted).
  Entry: command="tmux attach -rt agentive", from="100.127.230.71", read-only, no-port/agent/X11-forwarding.
  VERIFIED: `ssh hruzam@100.126.182.111` from tablet Termux → read-only attach to agentive tmux on office.
  Simultaneous view with Redmi confirmed (shared session, scroll history sync). ✅
  Note: must specify `hruzam@` explicitly (Termux local user is u0_a153).

- 2026-09-29 — @Cartan, office, explicit majkee request: promote Galaxy from monitor
  to writable terminal on BOTH hosts. Live identity: SM-T585, Android 8.1.0 / API 27,
  armeabi-v7a. All four tailnet nodes online; both Android devices visible on office USB.
  After operator started `sshd` + `termux-wake-lock`, office and home key auth to Galaxy
  passed. Galaxy's encrypted key fingerprint matches both host registrations.
  Applied `enable-tmux-write.py` after dry runs: only Galaxy's forced command changed
  from `tmux attach -rt agentive` to `tmux new-session -A -s agentive`; other keys,
  key material, source-IP guard and forwarding restrictions retained. Backups:
  office `~/.ssh/authorized_keys.before-galaxy-write-20260929T011946080746Z`;
  home `~/.ssh/authorized_keys.before-galaxy-write-20260929T011951842088Z`.
  Installed existing shared bed + two widget scripts; appended extra-key fragment
  and this device's `bashrc.fragment`, reloaded Termux settings. Device-local before
  copies: `~/.galaxy-setup-20260929/{termux.properties.before,bashrc.before}`.
  Bed SHA256 matches source (`800bc1d52afc1eba03ee9fa6a620e6ce66d7f3d3119d75e22f22fb882ce6d29f`).
  sshd effective config: port 8022, pubkey yes, password and keyboard-interactive no.
  Operator passphrase unlock and writable tmux round trip still pending here.
- 2026-09-29 — Operator reported Galaxy key passphrase forgotten and authorized
  replacement. Requested on-device `ssh-keygen -t ed25519 -f ~/.ssh/galaxy-new -C galaxy`
  with a non-empty passphrase; no private key or passphrase leaves the tablet.
  `enable-tmux-write.py --replacement-key '<PUBLIC key>'` is prepared and checked
  for exact old-entry matching, malformed/duplicate rejection and idempotence.
  Last probe: new public key absent. No rotation or old-key deletion performed yet.
  Resume: read ONLY new .pub, verify encryption; dry-run/apply on both hosts; preserve
  old device files and move new pair to id_ed25519; operator unlocks via bed; run
  `/tmp/galaxy-tmux-probe.py galaxy office` and `... galaxy home` for disposable
  create/type/detach/reconnect proof. No model turns required.
- 2026-09-29 — Key recovery completed after operator generated the new encrypted
  Ed25519 pair on Galaxy. Operator-requested latest screenshot showed key generation;
  screenshot fingerprint and live `.pub` agree:
  `SHA256:UHP76eQdepkhSTgnDED9YRRFPIUKhFKKh6v6b0xm65U`.
  Replaced only Galaxy key material on both hosts, retaining writable tmux command
  and all restrictions. Rotation backups: office suffix `20260929T014619965927Z`,
  home suffix `20260929T014622028447Z`, both under
  `~/.ssh/authorized_keys.before-galaxy-write-<suffix>`. Old key is no longer authorized.
  New pair is Galaxy's `~/.ssh/id_ed25519{,.pub}`; retired encrypted pair remains
  on Galaxy as `id_ed25519.retired-20260929` and `id_ed25519.pub.retired-20260929`.
  No private key or passphrase was transferred. Awaiting operator `bed office` unlock.
- 2026-09-29 — New key unlocked by operator on Galaxy. Office's live client
  reported `readonly=0` and `SSH_CONNECTION=100.127.230.71 ... 100.126.182.111 22`.
  Operator could see tmux but not type: pane `%57` was in copy-mode, not read-only.
  `tmux send-keys -X -t %57 cancel` returned it to the shell; no keymap change.
  Full key list confirmed Ctrl+B, colon already existed (the earlier targeted query
  returned no row and was misleading). Automation was corrected to pace prefix keys
  and quote `=session` for home's zsh; failed probes' own clients/sessions cleaned up.
  Final receipts from `/tmp/galaxy-tmux-probe.py`:
  - PASS galaxy → office: device-key SSH, writable tmux, create, type/execute, detach, reconnect.
  - PASS galaxy → home: device-key SSH, writable tmux, create, type/execute, detach, reconnect.
  Successful disposable sessions `galaxy-verify-d066bef483` (office) and
  `galaxy-verify-571a55ac31` (home) removed; failed home probe
  `galaxy-verify-51445ceed3` also removed. Operator's office client left attached.
  No model turn or existing participant session was killed.
- 2026-09-29 — Operator requested display smoothing. Galaxy had no custom font.
  Installed the already-working Redmi font, identified by fc-scan as JetBrainsMono
  Nerd Font Regular, to Galaxy `~/.termux/font.ttf` and ran termux-reload-settings.
  Source and target SHA256:
  `1c680e8cde9fcf8b88a5605ce8d1fb94dd3fb15841f7ca7bf4c55664855e5611`.
  Operator verdict: “looking much better”. No layout/theme or model configuration change.
- 2026-09-29 — Follow-up: home still displayed odd symbols after the font fix.
  Live home SSH had empty LANG/LC_CTYPE and POSIX locale; Galaxy client flags lacked
  UTF-8, unlike office. Locale availability was fine (en_US.utf8 and C.utf8 present).
  Added ONLY `-u` to Galaxy's home forced tmux command; key, restrictions, office
  entry and host-owned shell configuration unchanged. Source helper gained explicit
  `--utf8`; exact-change/idempotence/drift/duplicate checks and home dry run passed.
  Home backup: `~/.ssh/authorized_keys.before-galaxy-write-20260929T020443102303Z`.
  Existing client needs detach/reconnect; no host session restart required.
  Verification PASS: fresh Galaxy→home `client_utf8=1`; Czech/arrow/box/block/Powerline
  test glyphs preserved in terminal output, plus create/type/detach/reconnect passed.
  Disposable `galaxy-verify-d9f57763b2` removed; original user client left attached.
- 2026-09-29 — Operator requested Claude on office and reported Android keyboard
  Shift + Termux TAB did not combine. Started normal Claude Code 2.1.284 at
  `/home/hruzam/ia-sync` in office `agentive:1`, window `claude-galaxy`, pane `%60`;
  welcome screen and input prompt observed. No initial prompt sent or CLI policy changed.
  Galaxy version measured: Termux 0.118.1 / F-Droid / arm. Verified official v0.118.1
  sources: TerminalExtraKeys recognizes SHIFT in macros; KeyHandler maps shifted TAB
  to ESC [ Z. Added `S-TAB` macro `SHIFT TAB` and the native extra-row `SHIFT` toggle
  in shared termux.properties; deployed to Galaxy only. Existing controls/settings
  retained; parsed active JSON successfully; reload-settings succeeded.
  Device backup: `~/.termux/termux.properties.before-shift-20260929`.
  Final properties SHA256:
  `676ed49df72db90224e300791a762c8bc4405d28b6c66a163ba20f01c5f6449f`.
  Awaiting operator's physical S-TAB tap check; source/config proof is complete.
  References:
  https://github.com/termux/termux-app/blob/v0.118.1/termux-shared/src/main/java/com/termux/shared/terminal/io/TerminalExtraKeys.java
  https://github.com/termux/termux-app/blob/v0.118.1/terminal-emulator/src/main/java/com/termux/terminal/KeyHandler.java
- 2026-09-29 — Follow-up after initial S-TAB failure report: a temporary raw-input
  window in office agentive captured the operator's two taps as `09` (TAB) and
  `1b5b5a` (S-TAB), exactly expected. This proves the physical button through
  Termux → SSH → tmux. Window auto-closed and returned to Claude.
  One direct BTab test on the newly started Claude pane changed its footer from
  auto mode to manual mode; no prompt submitted. Left in manual mode and told operator.
  Operator confirmation: “perfect S-tab running”. No additional keyboard/config
  change was necessary; the earlier failure was not reproduced.
- 2026-09-29 — Operator confirmed: “galaxy looking fine (session survived 10 min
  with locked screen)”. Marked the pending 10-minute lock-screen session-survival
  acceptance check PASS. This receipt is the operator's observation, not a new
  automated measurement or a claim about uninterrupted transport.
