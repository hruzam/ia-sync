# zsh/scheduled — timed jobs (systemd user units)

What lives here:
- `harness-check.zsh` — settings-card freshness checker. Writes the stale-cards mail `zsh.stale-settings-cards-<ISO-week>.md`.
- `harness.service` / `harness.timer` — weekly systemd user units (Mon 09:00, Persistent).

Deploy: `deploy.sh` copies the script to `~/.config/zsh/scheduled/` (zsh rsync leg) and the
`*.service` / `*.timer` units to `~/.config/systemd/user/` (`deploy_scheduled_units`), then runs
`systemctl --user daemon-reload`.

Enable policy: `SCHEDULED_ENABLE_HOSTS` in deploy.sh (default `office`). Only office enables the
timer. The job publishes the stale-cards mail from its OWN clone
(`~/.local/share/harness/reposoma-mail`, override `HARNESS_MAIL_REPO`; deploy.sh creates it on
enable hosts): fetch → `reset --hard origin/core` + `clean` (in the clone only) → if this week's
file is already in `_mail/toAll/inbox/` or `archive/`, exit 0 → else write it, commit that one
path with a clone-local identity, `push origin HEAD:core` (3 attempts). It never touches the
live `~/reposoma`. Zero stale → no file, no commit. Guards abort before any write if the clone is
the live tree, not its own toplevel, or has a different `origin`; `flock` prevents overlap.
Other hosts get the units installed but the timer is NOT enabled; they run `harness-stale`
(scans the live tree, writes nothing) interactively only.

Rule 0009-L5 (verify the real trigger, not the script by hand):
  systemctl --user start harness.service
  journalctl --user -u harness.service -n 50
