version:     1.0
hosts:       monitor
automation:  manual

# Monitor — inbound OpenSSH preparation

Guide and acceptance track:
`~/reposoma/raw.guides/machine-monitor/res/access.md`.
This is ordinary OpenSSH over the existing tailnet, not Tailscale SSH.
PHP, databases, desktop sharing and project execution are outside this task.

## Preconditions

Confirm hostname `hruzam-mntr`, intended tailnet membership and the registered node
identity in `machines.json`. Review `ssh/sshd.monitor.conf`. The root sshd config
must include `/etc/ssh/sshd_config.d/*.conf`; this was observed on monitor.
Existing drop-in at the destination must be backed up before replacement.

## Operator steps

```sh
cd ~/ia-sync
sudo ssh-keygen -A
# If the destination already exists, preserve it before installing:
sudo test ! -e /etc/ssh/sshd_config.d/00-monitor.conf || \
  sudo cp -an /etc/ssh/sshd_config.d/00-monitor.conf /etc/ssh/sshd_config.d/00-monitor.conf.before-monitor
sudo install -m 644 ssh/sshd.monitor.conf /etc/ssh/sshd_config.d/00-monitor.conf
sudo sshd -t && sudo systemctl enable --now sshd
sudo sshd -T | rg '^(pubkeyauthentication|passwordauthentication|kbdinteractiveauthentication|permitrootlogin|allowusers) '
ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub
```

This prepares a key-only listener. It does not authorize any client key and does
not prove remote access. Default OpenSSH listen addresses include LAN and tailnet;
this file is authentication policy, not a firewall rule. Authorize only the intended
home/office public keys and verify host-key trust using the access guide. If any
effective authentication setting disagrees, stop before claiming readiness.

Record this task installed only after reviewing the effective settings and service
state. Four-direction SSH acceptance is tracked separately in the guide.
Rollback for this new host: disable/stop sshd, then restore the previous drop-in
if one existed, or remove only the newly installed 00-monitor.conf.
