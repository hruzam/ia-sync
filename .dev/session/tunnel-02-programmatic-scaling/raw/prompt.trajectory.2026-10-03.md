---
kind: pre-runbook-prompt
date: 2026-10-03
from: cartan
to: trajectory
predecessor: /home/hruzam/ia-sync/.dev/session/tunnel-upgrade-01-parametrization
bed: /home/hruzam/ia-sync/.dev/session/tunnel-02-programmatic-scaling
resume_id: e6276187-0ac9-439f-a4fd-72ebdbd19a0d
return_to: /home/hruzam/ia-sync/.dev/session/tunnel-02-programmatic-scaling/raw/trajectory.handoff.2026-10-03.md
---

# Trajectory — resume the predecessor and transfer its unfinished work

## Operator entry

The predecessor transcript exists on office at
`/home/hruzam/.claude/projects/-home-hruzam-ia-sync/e6276187-0ac9-439f-a4fd-72ebdbd19a0d.jsonl`
(file presence checked 2026-10-03; no resume performed by Cartan).

```sh
cd /home/hruzam/ia-sync
claude --resume e6276187-0ac9-439f-a4fd-72ebdbd19a0d
```

Give the resumed session this prompt file. If the transcript is unavailable on another
host, tell Majkee; a fresh reconstruction is not the same resumed incarnation.

## Prompt for Trajectory

You are the resumed Trajectory who authored the tunnel parametrization session.
Majkee requests your experience and an evidence-backed handoff BEFORE Cartan authors
the sister RUNBOOK in `/home/hruzam/ia-sync/.dev/session/tunnel-02-programmatic-scaling/`.
This assignment is preparation: reconcile what remains, give your engineering view,
and write the handoff. It does not start the old T2 live turn or implementation.

Re-resolve the host before trusting inherited context: your earlier transcript was
written on home and copied to office. Follow the current repository instructions.
Read in order:

1. `/home/hruzam/ia-sync/.dev/session/tunnel-upgrade-01-parametrization/STATUS.md`
   and its sibling `RUNBOOK.md`. Name stale statements rather than obeying them blindly.
2. `/home/hruzam/reposoma/_cold-start/archive/CS.tunnel-upgrade.2026-09-21.md`.
   The card is now in `archive/`; its former `card/` path is absent. Archive placement
   alone does not prove the old RUNBOOK gate was met.
3. `/home/hruzam/ia-sync/.dev/session/tunnel-upgrade-01-parametrization/raw/protocole1.jpg`,
   `protocole2.jpg`, and `protocole3.jpg` in that same directory.
4. `/home/hruzam/ia-sync/zsh/ai/tunnel-codex.py`,
   `/home/hruzam/ia-sync/zsh/ai/tunnel-codex.zsh`, and
   `/home/hruzam/ia-sync/zsh/ai/tunnel-codex.selftest.zsh`.
5. `/home/hruzam/reposoma/raw.guides/tunnel/res/settings.md`,
   `/home/hruzam/reposoma/raw.guides/tunnel/res/user-run.md`, and the relevant observations
   under `/home/hruzam/reposoma/raw.guides/tunnel/src/`.

## New direction from Majkee

Protocol 1 is the first pilot: Codex/Cartan is the persistent cSharp head; a temporary
Claude BUS holds initiative, consults the head through the tunnel, dispatches work
within the declared scope, and returns evidence. Cartan owns navigation and STATUS.
Atlas UI independently prepares the provisional BUS agent or skill under Majkee's
direct control, following `.germline` source/rendering doctrine.

If tunnel delivery fails, Majkee may carry the exchange by hand between head and BUS.
Both delivery routes will be declared when the sister session is authored, preserving
the same roles, assignment, and receipts. Record failures as practical evidence;
manual delivery cannot count as proof that the tunnel passed.

The prepared sister bed is the home for the new run and its inherited unfinished work.
Creating a bed does not itself create or bind a Codex thread. Identify the minimum
head birth/binding/continuation support needed; preserve the distinction between a
fresh head and delivery to an already-running interactive conversation.

## Cartan's audit — leads to verify, not substitutes for your evidence

- **T1 landed:** documentation corrections in reposoma `fb0cb15`; host corrections
  in ia-sync `5af457f`. The old STATUS still says both "no task started" and T1
  "done, uncommitted". Reconcile these against history.
- **Vault untracking landed:** ia-sync `d2f8734`; `tunnel*.state.json` remains ignored.
  Central vault relocation itself is still unfinished.
- **T2/T3 absent in the inspected source:** no `-c` passthrough, occupancy percentage,
  recovery details on close, `--vault`, or preset registry/chapter. Source and deployed
  Python/zsh copies matched on office on 2026-10-03; last shim commit was `5a0a59f`.
- **Version evidence:** Cartan observed codex-cli 0.159.3 on office on 2026-10-03;
  the old findings concern 0.154.0. Recheck before claiming present behavior.
- **Probe weakness:** an added writable root under default-writable `/tmp` cannot
  establish that `writable_roots` was honored. Separate the added root from all
  default roots or explicitly control them; distinguish birth from resumed turns.
- **Status weakness:** `tun status` prints local saved JSON. It does not freshly
  inspect effective runtime policy or reasoning effort. The old recovery command
  with an explicit missing state path yields code 10, not code 13.
- **Timeout curvature:** the September 10 observation reports short waits and exit
  zero. Current source has a configurable 120-second default and a ProtocolError
  path to exit 30. Explain what the original evidence does and does not establish;
  a remaining-deadline value in an error is not necessarily total elapsed time.
- **State documentation disagrees:** central relocation versus owner-adjacent state,
  and cross-host thread claims in user-run versus HANDSHAKE. List the documentation
  affected by carrying the accepted relocation into the sister session.

## Required handoff

Write only your report at
`/home/hruzam/ia-sync/.dev/session/tunnel-02-programmatic-scaling/raw/trajectory.handoff.2026-10-03.md`.
Put any necessary supporting evidence in that bed's `raw/trajectory/` directory.
Other participants share this repository; do not revert or absorb their edits.

Use these sections:

1. **Original intent and lessons:** what Majkee wanted, which choices were settled,
   which were proposals, and what you learned that the existing files fail to carry.
2. **Verified inheritance:** T1, T2, T3, vault handling, and deferred session-control
   work; for each, give done/unfinished/unverified, a path or commit, and its destination
   in the sister effort. Preserve the old gate's actual unfulfilled state.
3. **Smallest workable Protocol 1:** the minimum transport, settings, head-context,
   permissions, serialization, failure/recovery, and receipt changes; distinguish what
   v0 already supplies. Keep workers and BUS separate from the head's authority.
4. **Verification order:** cost-free checks first, then explicitly scoped live proofs
   after operator enable. Cover real sandbox/effort behavior, a subsequent turn on
   the same head, one complete collaboration cycle, and uncertain-delivery recovery.
5. **Dependencies and boundaries:** Atlas's provisional primitive; Ovitmugen's CLI/file
   integration; scope that belongs to existing Nablarva work instead of another build.
6. **Disagreements and remaining uncertainty:** push back on Cartan's audit and the
   proposed plan where warranted. Name any question that changes the forthcoming RUNBOOK.

Relevant boundary pointers:

- `/home/hruzam/reposoma/raw.guides/runbook/res/csharp-head-protocol.md`
- `/home/hruzam/reposoma/raw.guides/bus/GUIDE.md`
- `/home/hruzam/ia-sync/HANDSHAKE.md`
- `/home/hruzam/ia-sync/protocole/colors/PROTOCOLE.md`
- `/home/hruzam/unikuklatrix/nablarva/.dev/session/ovitmugen-01-basement/RUNBOOK.md`
- `/home/hruzam/unikuklatrix/nablarva/.dev/session/nablarva-02-pipe-qualification/STATUS.md`

Ovitmugen's previous `00-console` bed is closed; `01-basement` is current. Live-session
injection qualification is separate work, not an assumed capability of this tunnel.
Read foreign project instructions before expanding an investigation there.

For this preparation, use file/history inspection and cost-free introspection. No
model turn, tunnel enable, deploy, commit, push, primitive activation, or old-bed
closure is authorized by this prompt. Do not edit the new RUNBOOK or another seat's
files. Return the handoff path to Majkee; he carries it to Cartan. Cartan reads it and
Atlas's independent contribution before authoring the sister RUNBOOK.
