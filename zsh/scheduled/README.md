# zsh/scheduled — timed jobs (systemd user units)

What lives here:
- `harness-check.zsh` — settings-card freshness checker. Writes the stale-cards mail `zsh.stale-settings-cards-<ISO-week>.md`.
- `harness.service` / `harness.timer` — weekly systemd user units (Mon 09:00, Persistent).

Deploy: `deploy.sh` copies the script to `~/.config/zsh/scheduled/` (zsh rsync leg) and the
`*.service` / `*.timer` units to `~/.config/systemd/user/` (`deploy_scheduled_units`), then runs
`systemctl --user daemon-reload`.

Enable policy: `SCHEDULED_ENABLE_HOSTS` in deploy.sh (default `office`). Only office enables the
timer and writes the stale-cards mail; the mail is committed by a human or agent. Other hosts get
the units installed but the timer is NOT enabled; they run `harness-stale` interactively only.

Rule 0009-L5 (verify the real trigger, not the script by hand):
  systemctl --user start harness.service
  journalctl --user -u harness.service -n 50
