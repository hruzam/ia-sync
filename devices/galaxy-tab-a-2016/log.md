# galaxy-tab-a-2016 — action log (append-only)

- 2026-08-18 — Recon from office: tailnet online; sshd not running (connection refused).
- 2026-08-19 — sshd up on 8022 (operator started it). Key auth denied — pubkeys not
  seated yet. Ping works via DERP relay only. No changes made on-device.
- 2026-08-19 — Operator ran bootstrap step 2 (home pull only). Verified: home→tablet
  key auth OK (`id_ed25519`, 1 key in authorized_keys). Office→tablet still denied.
- 2026-08-19 — Tablet reached home host shell passwordless via Tailscale SSH
  (`ssh hruzam@hruzam`) — finding recorded; ACL fix drafted, awaiting operator paste.
- 2026-08-19 — Office-key relay-append attempt blocked by permission classifier;
  returned to operator hands (bootstrap step 2, office line).
