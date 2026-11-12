---
state: draft
next: Safety auditor reviews standing device SSH access with Majkee and records retain, narrow or remove decision.
by: Cartan
recorded: 2026-11-12
operator_disposition: Deferred to safety audit by Majkee; leave current live policy unchanged.
---

# Device SSH access — safety-audit follow-up

The operator-supplied saved Tailscale policy allows the intended all-port mesh among
home, office and monitor. It additionally grants tab and redmi standing TCP 22 access
to all three computers. That supplemental rule differs from the earlier requirement
that devices receive access on request. Majkee asked to retain this finding in the
backlog for safety audit; no policy change was made and no further immediate choice
is required from the operator for this item.

The audit should determine whether standing device SSH is wanted, whether its
sources/destinations should be narrower, or whether it should become temporary access
on explicit request. Network permission alone does not authenticate an SSH login;
review the host authentication/trust boundary separately. Do not treat the existing
Tailscale SSH section as replacing ordinary OpenSSH authentication.

Evidence and custody:

- `../session/monitor-01-integration/raw/policy-comparison.2026-11-12.json`
  records the saved export SHA256 and comparison outcome; host aliases and SSH
  section match the intended candidate, while the supplemental grant differs.
- Monitor-local saved export: `~/.local/state/ia-sync/tailnet-policy.live.json`.
  It was supplied by Majkee after confirming a control-plane save, not fetched by API.
- Monitor-local on-request proposal:
  `~/.local/state/ia-sync/tailnet-policy.on-request.proposed.json`.
  This removes only the supplemental device grant; it has not been applied.
- Tracked `zsh/.config/tailnet.access-controls.json` remains the narrower candidate,
  not a snapshot of the saved policy. Its deployed nested copy is inert; shell
  deployment does not save a policy to Tailscale.
- Export/proposal contents remain outside Git. Read local evidence only when
  available; otherwise obtain a fresh saved export, not a guessed reconstruction.

Completion: record Majkee's device-scope decision, compare the resulting saved policy
and relevant SSH behavior against it, and reconcile candidate/documentation references.
Any control-plane change needs authorization for the chosen scope; this backlog
entry is a follow-up assignment, not permission to alter access silently.
