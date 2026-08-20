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
- Open: office pubkey seating (operator line, non-urgent); sshd hardening to key-only
  in Termux after that; forced-command tmux layer parked for a next session.
