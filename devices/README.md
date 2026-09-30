# devices/ — portable Android devices workspace

Not projects. This domain holds the **device cards, setup logs, and shared bootstrap
material** for the portable devices on the tailnet (Termux + Tailscale). Work on a device
is done *over SSH from a computer*; this folder is the memory of that work, synced to both
machines via ia-sync.

## Inventory

| Device | Tailscale IP | Termux sshd port | Android | Trust class |
|---|---|---|---|---|
| galaxy-tab-a-2016 | 100.127.230.71 | 8022 | 8.1.0 / API 27 (SM-T585; verified 2026-09-29) | **contain** — least trusted |
| redmi-15c-5g | 100.105.201.3 | 8022 | 15 (2508CRN2BE; verified 2026-09-29) | restrict |

Computers (for reference): office `hruzam-120922` = 100.126.182.111 · home `hruzam` = 100.110.27.60.

## Security doctrine (agreed 2026-08-19, session REP.office.oraculum-fable)

**Operator amendment, 2026-09-29:** Galaxy is now a working terminal like Redmi.
Both devices may create and maintain tmux sessions on both hosts using their own
passphrase-protected SSH keys. The registered keys force writable `agentive` entry;
source-IP and forwarding restrictions remain. This supersedes the old Galaxy
monitor-only role and the blanket no-device-to-PC path statement below. A writable
tmux shell provides the host user's command execution; it is not a security sandbox.

1. **Devices are the least-trusted tailnet nodes.** They receive connections from the
   computers; they get **no standing path toward the computers** (target state: Tailscale
   ACL default-deny androids→PCs).
2. **Device→PC access, when needed, is just-in-time:** SSH key on the device encrypted
   with a passphrase held only in the operator's head, plus a restricted
   `authorized_keys` entry (`from=` the device's tailnet IP) on the PC side. No shared
   rotating passwords, no custom auth layers.
3. **Termux sshd is key-only** once keys are seated — password auth off.
4. Tailnet key expiry stays **enabled** for devices (disable only for computers).

## Conventions

- Each device folder: `device.md` (current facts + restrictions) and `log.md`
  (dated, append-only actions).
- `_shared/` holds material common to all devices (bootstrap steps, sshd config
  fragments). Point, never copy, from device folders.
- Update the device card in the same session as the change — the card is the truth.
