# Termux bootstrap — run BY HAND on each device (operator's steps)

These are the only steps that need human hands on the device. Everything after runs
over SSH from a computer.

## 1. Install + start sshd

```sh
pkg update && pkg install -y openssh
sshd
termux-wake-lock
```

`termux-wake-lock` keeps Android from killing Termux (and sshd with it).
Note: sshd dies on reboot / Termux kill — rerun `sshd` when a session bounces
with "connection refused".

## 2. Seat the computers' public keys (passwordless PC→device)

Run on the device; each line asks for that computer's Linux user password once:

```sh
mkdir -p ~/.ssh
ssh hruzam@100.126.182.111 'cat ~/.ssh/id_*.pub' >> ~/.ssh/authorized_keys   # office
ssh hruzam@100.110.27.60  'cat ~/.ssh/id_*.pub' >> ~/.ssh/authorized_keys   # home
chmod 600 ~/.ssh/authorized_keys
```

## 3. Report back

Tell the session the device is up; an agent verifies with:
`ssh -p 8022 <device-tailscale-ip> 'echo SSH_OK'`

## Later hardening (done over SSH by agents, logged per device)

- Disable password auth in `$PREFIX/etc/ssh/sshd_config` (`PasswordAuthentication no`)
  — only after key auth is verified from both computers.
- Generate the device's own passphrase-protected keypair for just-in-time
  device→PC access (doctrine item 2 in ../README.md).
