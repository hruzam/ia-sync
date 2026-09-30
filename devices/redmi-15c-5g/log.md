# redmi-15c-5g — action log (append-only)

- 2026-08-19 — Recon from office: tailnet offline (last seen 1d prior), unreachable.
  No bootstrap done yet.
- 2026-08-21 — Operator brought device on tailnet (Tailscale connected). `pkg install openssh`
  done; `sshd` started once; temp password set. Old password was burned (typed visibly) —
  operator set a fresh one. NO PC keys seated yet. Session closed here; wakefulness not
  yet tested. **Open: set fresh passwd before next ssh-copy-id attempt (Step 1).**
- 2026-08-20 — Step 1 complete: both PC keys seated via push-flow.
  office RSA key: seated (operator ran ssh-copy-id from office).
  home ed25519 key: seated (operator ran ssh-copy-id from home).
  Verified: office→redmi OK; home→redmi OK.
  Termux sshd hardened to key-only (PasswordAuthentication no + KbdInteractiveAuthentication no
  appended to $PREFIX/etc/ssh/sshd_config, sshd restarted). Key-only reconnect verified.
  Temp password no longer matters. Open: Step 2 (JIT keygen + tmux layer).
- 2026-08-20 — Step 0 complete: battery exemption set by operator (Termux + Tailscale no restrictions).
  Termux pinned in Recents. Banner test (screen-off acceptance gate) pending.
- 2026-08-20 — Step 2 complete: JIT keygen done on device (ed25519, passphrase in operator's head).
  Restricted authorized_keys entry added to office + home (operator pasted).
  Entry: command="tmux new-session -A -s agentive", from="100.105.201.3", no-port/agent/X11-forwarding.
  VERIFIED: `ssh hruzam@100.126.182.111` from Termux → landed in agentive tmux on office. ✅
  Note: must specify `hruzam@` explicitly (Termux local user is u0_a329).

- 2026-09-29 — @Cartan live check from office: model 2508CRN2BE, Android 15;
  tailnet online and Xiaomi USB MTP+ADB enumeration present. Termux SSH initially
  refused 8022; after operator start, office→Redmi and home→Redmi key auth passed.
  sshd remains key-only; existing bed script equals repository source. Device key
  remains encrypted, fingerprint SHA256:JFohcXZXQLhyT4zOcEtlrmoR+ZoM1qUKei9V/590k/s
  matches both hosts. Cached ssh-agent was unavailable, so a fresh phone→host test
  awaits operator unlock. No Redmi files or key registrations changed.
- 2026-09-29 — Operator requested Galaxy's S-TAB row on Redmi. Live Redmi properties
  matched the old shared fragment exactly (SHA256 fb30782afebd87ce93e8b9c3f9fa044da934cd4070b710ac739d58e7550754be).
  Pushed the current shared fragment with dedicated S-TAB macro `SHIFT TAB` and
  native SHIFT toggle; retained all existing controls. Backup:
  `~/.termux/termux.properties.before-shift-20260929`. termux-reload-settings succeeded;
  deployed checksum matches source. Termux identifies as `googleplay.2026.06.21`
  (Galaxy uses F-Droid 0.118.1). Physical tap check on Redmi not yet reported.
  Its cached ssh-agent is still unavailable, so outbound round-trip proof remains pending.
- 2026-09-29 — Operator reported the same odd symbols on home as Galaxy. Live home
  tmux client PID 3509 had `client_utf8=0`; its SSH_CONNECTION source was Redmi's
  `100.105.201.3`. Home's Redmi forced command still omitted `-u`. Added only `-u`
  with `enable-tmux-utf8.py` after guarded transformation checks and live dry run.
  Public key, source-IP guard, forwarding restrictions and all other entries preserved.
  Home backup: `~/.ssh/authorized_keys.before-redmi-utf8-20260929T030527333476Z`.
  Existing session left intact; operator asked to detach/reconnect for the new client.
  Verified backup diff contains only that `-u`; current file and backup are mode 0600.
  After operator reconnect, client PID 3702 reports `client_utf8=1` and SSH source
  `100.105.201.3`. Operator confirmed “Yes, looks correct”. Display repair PASS.
- 2026-09-29 — Operator reported missing office sessions and `office bed` failing
  with `open terminal failed: not a terminal`. Redmi still had direct `ssh` aliases,
  unlike Galaxy; SSH reported `requesttty auto`, so adding `bed` sent a remote
  command without a terminal. Pushed `bashrc.fragment`: `office` / `home` now call
  `~/bin/bed` (already uses `ssh -t`), and `~/bin` is on PATH. Exact before-state
  guard passed; backup `~/.bashrc.before-bed-aliases-20260929`; shell syntax and fresh
  interactive alias resolution passed. Post-write SHA256:
  `6f4793d71829a06d2c8d817960841013efda702e65e322d8e9d9affa476e35c4`.
  Office default server's `s`/`w` bindings remain `choose-tree -Zs`/`choose-tree -Zw`.
  Ovitmugen agents share `default`; its frame server is separate (`ovitmugen`, Ctrl+A).
  No runbook/ovitmugen files or host key registrations changed in this alias repair.
  Operator reloaded `.bashrc`, connected with `office`, and confirmed Ctrl+B, s
  shows office sessions. The device agent was then unlocked: Redmi→office and
  Redmi→home both passed create/type/execute/detach/reconnect with writable clients,
  `client_utf8=1`, and intact Czech/arrow/box/block/Powerline bytes. Disposable sessions
  `redmi-verify-0bd7c1541d` (office) and `redmi-verify-ef526871b2` (home) were removed;
  existing user sessions remained intact. The earlier outbound-proof gap is closed.
