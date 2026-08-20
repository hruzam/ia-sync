version:     1.0
hosts:       home office
automation:  manual

# harden-host — tailnet/LAN exposure hardening

developed-on: office · 2026-08-20 · origin: tailnet security audit 2026-08-19
(session REP.office.oraculum-fable). Findings: MySQL on 0.0.0.0 (both hosts),
password-auth sshd (home), no firewall (both).

Rollback: `sudo rm /etc/my.cnf.d/99-bind-local.cnf /etc/ssh/sshd_config.d/99-key-only.conf`,
`sudo ufw disable`, restart mariadb + reload sshd.

<!-- install:check -->
```bash
command -v ufw >/dev/null 2>&1 || { echo "ufw not installed (pacman -S ufw)"; exit 1; }
grep -q 'Include /etc/ssh/sshd_config.d' /etc/ssh/sshd_config || { echo "sshd_config.d not included"; exit 1; }
[ -d /etc/my.cnf.d ] || { echo "/etc/my.cnf.d missing — mariadb not installed?"; exit 1; }
```
<!-- /install:check -->

## Manual steps (sudo)

LAN subnet: home = 192.168.0.0/24 — **verify on office** with `ip -4 route | grep -v tail`.

```bash
sudo bash -euo pipefail -c '
LAN="192.168.0.0/24"
# 1. MySQL -> localhost only
printf "[mysqld]\nbind-address = 127.0.0.1\n" > /etc/my.cnf.d/99-bind-local.cnf
systemctl restart mariadb 2>/dev/null || systemctl restart mysqld
# 2. sshd -> key-only (no-op effect on office, already set)
printf "PasswordAuthentication no\nKbdInteractiveAuthentication no\nPermitRootLogin no\n" \
  > /etc/ssh/sshd_config.d/99-key-only.conf
sshd -t && systemctl reload sshd
# 3. ufw baseline — tailscale0 open (androids gated by tailnet ACL, not ufw);
#    LAN keeps ssh, web, KDE Connect, krfb (tablet side-monitor)
ufw default deny incoming; ufw default allow outgoing
ufw allow in on tailscale0
ufw allow from $LAN to any port 22 proto tcp
ufw allow from $LAN to any port 80 proto tcp
ufw allow from $LAN to any port 1714:1764 proto tcp
ufw allow from $LAN to any port 1714:1764 proto udp
ufw allow from $LAN to any port 5900 proto tcp
ufw --force enable
# verify
ss -tln | grep ":3306"
sshd -T | grep -iE "^(passwordauth|kbdinteract|permitroot)"
ufw status numbered
'
```

Then record it: `bash run.sh mark harden-host`

Flow: save the file → bash run.sh update (gates prereqs on this host) → run the sudo block → mark harden-host → repeat on home (git pull there first, or via your ssh session). The runner's state file then honestly tracks which machine is hardened — no SYNC_DISCIPLINE trap.

Two more things I learned in there worth noting: netOrchestrating (your symmetric home↔office SSH file-bus between tmux panes) and tmux-pin-bus already exist — so the "reach a live Claude/Codex session from the phone" design from yesterday won't start from zero; it extends an existing tmux culture. Good news for the forced-command layer.
