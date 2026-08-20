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
