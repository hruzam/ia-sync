# RUNBOOK: monitor-01-integration

```yaml
goal: >-
  Integrate monitor into the existing machine and project architecture, with matching
  repository paths, useful zsh commands, verified computer access and independent audit.
gate: >-
  Majkee accepts monitor's agreed repository layout, shell integration and computer access
  after independent verification, with remaining limitations explicitly recorded.
participant_1: [cartan, {brand: codex, model: operator-selected, effort: operator-selected}, {host: monitor, role: cSharp head and integration owner}]
participant_2: [oraculum-exec, {brand: claude, model: claude-fable-5-2 requested, effort: unverified}, {host: monitor, role: execution coordinator through bounded workers}]
participant_3: [astrobley-exec, {brand: codex, model: GPT-6-Sol reported, effort: medium reported}, {host: monitor, role: heavier implementation and technical investigation}]
participant_4: [myshell, {brand: codex, model: unverified, effort: unverified}, {host: monitor, role: goal alignment and personal continuity support}]
participant_5: [oraculum-audit, {brand: claude, model: unverified, effort: unverified}, {host: monitor, role: independent architecture assessment with technical witnesses}]
participant_6: [majkee, {brand: human}, {host: monitor and peers, role: scope decisions trusted host confirmation and final acceptance}]
status_owner: cartan
head_note: >-
  cSharp — this seat authored the RUNBOOK and stays live through the whole arc as navigator
  and status_owner; it may delegate every body of work and receive only navigation + test
  parts; it closes the session if it can.
observations_read:
  - /home/hruzam/ia-sync/.dev/observations/germline.scars.g06.flight.2026-10-22.md
```

## Why this session exists

Majkee requested a successor-ready implementation track for the new monitor host, then
explicitly selected cSharp coordination, recurring myShell goal checks and a separate
Sol execution session. Existing Jev sessions supply evidence, not ownership of this gate.
No predecessor monitor observations exist at authoring. This bed owns integration;
project-specific runtime changes retain the destination project's own gates.

## Fixed scope and work distribution

The requested repositories are nablarva, nabla-lab, vacuole, applications-in-common,
pajdulium-web and pajdulium-studio; ia-sync and reposoma already exist. Preserve the
same username and verified absolute paths across machines. Known path candidates:

| Repository | Candidate monitor destination |
|---|---|
| nablarva | /home/hruzam/unikuklatrix/nablarva |
| nabla-lab | /home/hruzam/nabla-lab |
| vacuole | /home/hruzam/vacuole |
| applications-in-common | /home/hruzam/www/elements-factory/applications-in-common |
| pajdulium-web | /home/hruzam/www/kuklana/pajdulium-web |
| pajdulium-studio | /home/hruzam/www/kuklana/pajdulium-studio |

Verify source identity, remote, branch, worktree state, and destination before cloning.
The physical map's old nabla-lab omission conflicts with newer standalone-repo evidence.
Vacuole's beacon records a private local repository with remote pending; do not invent
its remote or copy its private content in a diagnostic report. Clone presence alone
does not establish project readiness or transfer ignored state.

Work packages are released as bounded POINTs, not as an overlapping task swarm:

1. Qualify participant identities, notification routes and goal alignment; independently
   investigate repository/path gaps and shell deployment boundaries.
2. Verify selected repository sources and restore the agreed layout. Oraculum-exec
   coordinates appropriate workers; astrobley-exec owns difficult technical work.
3. Integrate monitor shell commands and maps. Add an interactive host choice when `tso`
   has no explicit peer, preserving explicit peer and `-t` behavior. Cancellation
   must not connect anywhere; noninteractive calls must not hang on a prompt.
   Resolve selected logical names through the existing host map to SSH-resolvable
   destinations. Peer visibility, network reachability and SSH login are distinct.
4. Verify six directed ordinary-SSH paths among home, office and monitor, and the
   selected tailnet access policy. Devices retain access only on request.
5. Audit the actual changes and recovery evidence independently, repair via new
   bounded cycles, and seek Majkee's acceptance. Promote durable findings before closure.

Cartan retains scope, dependencies, acceptance and the sole STATUS pen. Oraculum-exec
coordinates workers inside assigned packages; it does not acquire STATUS ownership.
Astrobley-exec receives owned files and concrete acceptance checks, not a duplicate head
assignment. Delegated workers are not alone in the codebase: preserve unrelated edits,
coordinate disjoint writes, and return evidence. A verifier never fixes its review target.

## Communication contract

Use /home/hruzam/reposoma/raw.guides/bus/GUIDE.md for numbered POINT/RETURN/VERDICT
cycles and /home/hruzam/reposoma/raw.guides/runbook/res/fanout-turns.md for grouped turns.
One writer per file; only cartan replaces STATUS. Direct peer discussion is allowed
inside an assigned scope; changes to ownership or scope return to Cartan.

Notifications contain an exact bus pointer and cycle, not a second assignment:

```text
to-oraculum-exec from-cartan:

---
cycle NN: read /home/hruzam/ia-sync/.dev/session/monitor-01-integration/_bus/NN.cartan.point.md
Return only through the declared path; report your actual session identity.
---
```

The envelope labels the destination; it does not implement routing. Verify the live
recipient before sending. Codex native thread messaging and `codex queue --thread UUID`
are available candidates; acceptance/queueing is not proof of consumption. Discover
Claude's supported peer route separately. A reported UDS path is not a validated API.
Do not inject keystrokes into a focused terminal, improvise a raw socket protocol,
resume an already-owned TUI through a second writer, or add a watcher/daemon.

Children are registered by their parent with observed handle, runtime, assigned scope
and return path. Cross-root child addressing is unproven until tested. Parent relay
is an explicit fallback, never a claim that direct delivery works. A future wrapper
is justified only for a proven route, exact recipient binding, message-size checking,
honest queue/delivery outcome and safe failure. No new global role/config is implied.

Send once after files are complete. Wait for completed turns and content-bearing
RETURNs; no repeated nudges, self-scheduled polling or automatic retry storm. A new
assignment gets a new cycle. Manual exact-path relay remains available if native
delivery is unavailable. Native notifications may start paid turns; keep them bounded.

Cartan asks myShell for a bounded goal check at each phase boundary, before a scope
expansion and at successor transfer. myShell compares the stated objective with current
STATUS/evidence, returns drift or alignment, and keeps no competing project task state.
No timer or permanent monitoring process is required. Cartan adjudicates the result.

## prompt-0 — Cartan successor

###### prompt

```text
You are Cartan, cSharp head for /home/hruzam/ia-sync/.dev/session/monitor-01-integration.
Read its RUNBOOK.md and STATUS.md, then only the currently referenced POINTs and evidence.
Resolve host and applicable project instructions. Run STATUS.recovery_probe before work.
Observe and register YOUR actual session ID and return route in a new numbered self-
registration POINT; the prior Cartan UUID is provenance, never your reply address.
Qualify receipt with myShell and the execution coordinator before releasing new work.
You alone replace STATUS. Delegate heavy bodies to the already-running execution seats;
receive concise claims and evidence, verify those claims, and write the join.
At phase boundaries and scope changes ask myShell whether work still serves Majkee's goal.
Keep the entrance small: do not reread all Jev history or global therapy records.
Do not confuse the presence of a bus file with a finished turn, an ACK, or a passing test.
Current roster handles are in this bed's raw/entry-evidence.md; verify them before reuse.
```

## prompt-1 — Oraculum execution coordinator

###### prompt

```text
Read /home/hruzam/ia-sync/.dev/session/monitor-01-integration/RUNBOOK.md and STATUS.md.
Resolve your actual main-entry Oraculum scope from the live germline and return its entry proof.
Your seat label here is oraculum-exec. Cartan owns the gate and sole STATUS pen.
Coordinate explicitly assigned packages through bounded execution workers under their
own roles. You may delegate those packages within the operator's grant; your strategic
role does not itself implement code, deploy, or bypass hooks. No edits before a POINT
names owned paths, effects and acceptance checks. Reply in the POINT's exact RETURN path.
Register each worker's observed address and ownership before treating it as reachable.
Use supported doorbells only; if unavailable, report the exact path for operator relay.
```

## prompt-2 — Astrobley execution seat

###### prompt

```text
Read /home/hruzam/ia-sync/.dev/session/monitor-01-integration/RUNBOOK.md and STATUS.md.
Your task label is astrobley-exec; report your actual session ID, model/effort if observable,
and effective role. This label does not silently change your loaded role or permissions.
Own difficult implementation packages only when a POINT assigns exact paths and effects.
You are not alone in the codebase. Preserve others' edits; no shared STATUS writes, no
peer-host config edits, no implicit commit/push/deploy. Return concise evidence, failed
checks and remaining uncertainty; do not make Cartan replay your whole investigation.
First task is the read-only opening POINT addressed to you, not broad implementation.
```

## prompt-3 — myShell

###### prompt

```text
From your existing myShell session, read /home/hruzam/ia-sync/.dev/session/monitor-01-integration/RUNBOOK.md
and STATUS.md and the POINT addressed to myshell. Check goal alignment against Majkee's
explicit objective; identify scope drift, missing desired outcomes and avoidable head load.
Return the bounded assessment to the exact bus path. This grants that RETURN, not ownership
of ia-sync STATUS or project implementation. Your personal journal remains governed by
/home/hruzam/reposoma/.majkee/AGENTS.md. Do not create a parallel project doing-state.
```

## prompt-4 — Independent audit coordinator

###### prompt

```text
Read /home/hruzam/ia-sync/.dev/session/monitor-01-integration/RUNBOOK.md and STATUS.md.
Your seat label is oraculum-audit, distinct from oraculum-exec. Resolve your own main-entry
scope and report identity. Assess architecture independently; use separately assigned
technical witnesses for code/runtime review. Do not review your own implementation or
repair the target under audit. Own only your POINT's RETURN and scoped evidence.
Check host identity, path parity, deployed/source agreement, ignored-secret boundaries,
access scope, cancellation/noninteractive behavior, rollback and six directional SSH receipts.
Name unverified claims and assessor conflicts. Return findings to Cartan; no STATUS writes.
```

## Known constraints and destructive holds

- PHP installation and project runtime placement remain deferred to Majkee. Do not start
  PHP projects, services, containers or installs merely because their repositories arrive.
- Home and office own their host configs. Preserve project pins, including Nablarva's
  Termbrana restrictions. Uniform paths do not require identical machine capabilities.
- No email-account inspection. Private keys, credentials, auth state and plaintext secrets
  remain host-local. Do not inspect or transfer them as part of inventory/clone work.
- Follow compose-first. Never run retired sync.sh. Gitignore is not an rsync exclusion.
  The existing monitor .env directory contains the requested policy candidate; do not
  overwrite it or force a vault extraction. Policy file presence does not apply policy.
- Verify SSH host identity using trusted evidence before login. A historical fingerprint
  disagreement is a hold, not permission to disable StrictHostKeyChecking.
- Do not modify a live session's model, profile or prompt history to make transport work.
- Changes to portable harness primitives or governing canon require their own applicable
  scope and review; this RUNBOOK is not blanket permission to rewrite the architecture.
- Current user authorization permits participant briefing and bounded access tests before
  successor handoff. Inferred scope extensions return to Majkee.

## Acceptance evidence

- Repository matrix: source, destination, remote/branch/commit, worktree and path agreement;
  project entry instructions read at destination; absent local state explicitly distinguished.
- Shell checks: fresh interactive PTY on monitor, explicit and selected host routes, -t,
  cancellation, unavailable peers and noninteractive behavior; scoped dry-run and rollback.
- Six directional SSH identity receipts, actual live policy scope, and device-on-request
  behavior. Offline origins or missing trusted keys remain UNVERIFIED, never inferred PASS.
- Separate audit findings, corrective-cycle receipts and verified dispositions. A final
  myShell goal check and Majkee acceptance close the gate.

## References and scar application

- /home/hruzam/reposoma/raw.guides/runbook/GUIDE.md and /home/hruzam/reposoma/raw.guides/status/GUIDE.md — one gate and one present state.
- /home/hruzam/reposoma/raw.guides/bus/GUIDE.md and /home/hruzam/reposoma/raw.guides/runbook/res/fanout-turns.md — cycles and joins.
- /home/hruzam/ia-sync/.dev/session/jev-01-codex-pilot/raw/HANDOFF.tui-bus-substrate.2026-11-10.md — native Codex proof and its limits.
- /home/hruzam/reposoma/raw.guides/machine-monitor/res/access.md — prior access setup and unfinished checks.
- /home/hruzam/ia-sync/machines.json and /home/hruzam/ia-sync/zsh/registries/projects.json — compare maps with observed identity and paths.
- /home/hruzam/reposoma/raw.therapy/cartan/therapy.md, last-turn/G-52 — small entry with reachable evidence; no fresh gavels.
- /home/hruzam/ia-sync/.dev/observations/germline.scars.g06.flight.2026-10-22.md — S1 checked newer Nabla-lab evidence; S3 checked cited text; S4 transport ACK is not a witness; S5 audit is separate; S6 dependent implementation waits for verified source mapping.

Closure follows the shared RUNBOOK promotion/prune rules. No per-session journal or
duplicate task registry is introduced. Session IDs and observations belong in evidence;
the RUNBOOK's role contracts remain fixed through successor changes.
