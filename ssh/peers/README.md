# ssh/peers — public-key exchange between the three computers

Public keys are not secrets, so the exchange does not need secrecy. It only needs
**integrity**: proof that a key really came from the host that claims it. Two
authenticated channels already exist, so a USB stick is not needed:

1. **git**: each host commits its own keys. Only the account owner can push,
   because pushes to GitHub require SSH authentication.
2. **the tailnet**: `ssh-keyscan <tailnet-ip>` gets a reply only from that node,
   because WireGuard ties each tailnet IP to one node key.

A host key is trusted when the two channels agree: the fingerprint committed here
must match the one `ssh-keyscan` returns over the tailnet.

This repository is **PUBLIC**. Only `*.pub` and `known_hosts` lines go here.
Never commit a private key (`id_*` without `.pub`, `ssh_host_*_key`).

## Files (one set per logical host; each host publishes only its own)

| File | Content | Used by peers in |
|---|---|---|
| `<host>.known_hosts` | `/etc/ssh/ssh_host_ed25519_key.pub` as a known_hosts line | `~/.ssh/known_hosts` |
| `<host>.client.pub`  | `~/.ssh/id_ed25519.pub` | `~/.ssh/authorized_keys` |

## Publish (on each host, once)

```sh
cd ~/ia-sync && git pull --ff-only
H=<home|office|monitor>; N=$(hostname -s); IP=$(tailscale ip -4)
{ echo "# $H host key, self-published $(date +%F)"
  echo "# $(ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub | awk '{print $2}')"
  echo "$N,$N.tail36b8ab.ts.net,$IP $(awk '{print $1" "$2}' /etc/ssh/ssh_host_ed25519_key.pub)"
} > ssh/peers/$H.known_hosts
{ echo "# $H client key, self-published $(date +%F)"
  echo "# $(ssh-keygen -lf ~/.ssh/id_ed25519.pub | awk '{print $2}')"
  echo "$(awk '{print $1" "$2}' ~/.ssh/id_ed25519.pub) $H-$N"
} > ssh/peers/$H.client.pub
git add ssh/peers/$H.* && git commit -m "ssh/peers: publish $H keys" && git push
```

## Accept a peer (on each host, for each other host P)

```sh
cd ~/ia-sync && git pull --ff-only
# 1. Host trust: committed fingerprint must equal the live tailnet scan.
ssh-keygen -lf ssh/peers/P.known_hosts
ssh-keyscan -t ed25519 <P-tailnet-ip> 2>/dev/null | ssh-keygen -lf -
#    Equal → append. Different → STOP and journal it.
grep -v '^#' ssh/peers/P.known_hosts >> ~/.ssh/known_hosts
# 2. Login authorization: back up first, append only what is missing.
cp -a ~/.ssh/authorized_keys ~/.ssh/authorized_keys.before-peers-$(date +%F) 2>/dev/null
touch ~/.ssh/authorized_keys   # monitor has none yet; grep -f needs the file to exist
grep -v '^#' ssh/peers/P.client.pub | grep -vxFf ~/.ssh/authorized_keys >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
# 3. Receipt: from P, run  ssh hruzam@<this-host> hostname
```

Status of each direction: `~/reposoma/raw.guides/machine-monitor/res/access.md`.
