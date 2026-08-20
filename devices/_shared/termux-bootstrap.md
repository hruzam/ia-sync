# Termux bootstrap — operator's steps per device

REVISED 2026-08-21: the original *pull* flow (device fetches PC pubkeys over ssh) died
when both PCs went key-only (harden-host 1.0) — a device with no key cannot password-auth
to pull. Flow is now **push from the PCs**, which hold working keys everywhere.

## 1. On the device (Termux, by hand)

```sh
pkg update && pkg install -y openssh
passwd            # TEMPORARY password — only to receive the first key push
sshd
termux-wake-lock  # stops Android killing Termux+sshd
```

Note: sshd dies on reboot / Termux kill — rerun `sshd` when a connection is refused.

## 2. From the home host (or office — any PC with keys)

```sh
# seat this PC's key (asks the device's temp password once)
ssh-copy-id -p 8022 -o StrictHostKeyChecking=accept-new <device-tailscale-ip>

# seat the OTHER PC's key by relay (no password needed)
ssh <other-pc> 'cat ~/.ssh/id_*.pub' | ssh -p 8022 <device-tailscale-ip> 'cat >> ~/.ssh/authorized_keys'
```

Device IPs: tablet `100.127.230.71` · redmi `100.105.201.3`. Host-key fingerprints for
first-contact verification: home ED25519 `SHA256:AYQ8YIZiUxYSZnMXiq8VH/Csw8uygQ81tf86WPWmRBO`,
office ED25519 `SHA256:Zu4j+Cuu8P9dpuQPoHpEPFnq8fB3EckdgjrDUwe/s/U`.

## 3. Verify + close the password door

From each PC: `ssh -p 8022 <device-ip> 'echo OK'` — then, once BOTH PC keys verify,
harden the device sshd to key-only (next-session task): in Termux
`$PREFIX/etc/ssh/sshd_config` set `PasswordAuthentication no`, restart `sshd`.
The temp password stops mattering at that point.

## Why devices never pull

Doctrine (../README.md): devices are least-trusted; PCs are key-only. All trust flows
PC → device. A device that could password-pull from a PC would mean the PC accepts
passwords — the exact hole harden-host closed.
