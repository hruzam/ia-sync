# RUNBOOK: jev-implementation-00-build

```yaml
goal: >-
  A vendor-neutral Jev CLI pilot provides explicitly requested, advisory typed judgments,
  with resumable records under ~/.jev and an optional binding to the owning project session.
gate: >-
  Majkee records GO on a Flight-witnessed pilot that completes an individually approved mixed-type OpenRouter request, preserves its structured reply in recoverable session JSONL, supports local show/file-reference and use/skip/reconsider dispositions from both CLI consumers, and demonstrates per-send confirmation and no execution from a verdict.
participant_1: [cartan, {brand: Codex, model: operator-selected, effort: operator-selected}, {host: office, role: cSharp head and integration owner}]
participant_2: [flight, {brand: Claude Code, model: operator-selected, effort: operator-selected}, {host: office, role: independent design challenger and standing witness}]
participant_3: [astrobley, {brand: Codex, model: role-default, effort: role-default}, {host: office, role: bounded implementation delegate after design review}]
participant_4: [majkee, {brand: human}, {host: office, role: "wake Flight, resolve gavels, approve each send, accept the pilot"}]
status_owner: cartan
head_note: >-
  cSharp — this seat authored the RUNBOOK and stays live through the whole arc as navigator
  and status_owner; it may delegate every body of work and receive only navigation + test
  parts; it closes the session if it can.
```

## Why this session exists

The supplied material contains a useful session-buffer workflow, an older direct-TypeSafe
integration handoff, and a direct-TypeSafe smoke script. The operator chose OpenRouter,
host-local `~/.jev/` persistence, explicit project-session attachment, and a consumer which
can show a reply or point to its file. This session turns that bounded consultation into a
working pilot. Jev supplies judgments; the consumer and operator retain their existing roles.

## Fixed facts and read order

1. Read `/home/hruzam/ia-sync/AGENTS.md` and `/home/hruzam/ia-sync/SYNC_DISCIPLINE.md`.
2. Read this RUNBOOK and `/home/hruzam/ia-sync/.dev/session/jev-implementation-00-build/STATUS.md`.
3. Read `/home/hruzam/ia-sync/.dev/session/jev-implementation-00-build/raw/design.2026-10-01.md`.
4. Read `/home/hruzam/ia-sync/.dev/session/jev-implementation-00-build/raw/provider-recheck.2026-10-01.md`.
5. Inspect `/home/hruzam/ia-sync/.dev/session/jev-implementation-00-build/raw/jev-events.example.jsonl`;
   it is synthetic schema material, not live-provider or approval evidence.

The operator's 2026-10-01 gate permits this authoring/handoff. Flight is woken by the operator
after the first part. Authoring approval does not waive confirmation for any paid request.
The original three files under `raw/` remain provenance; the design identifies superseded
assumptions. The cSharp protocol is a collaboration posture, not a choice of C# language.

## prompt-0 — cartan

```text
You are Cartan, head and sole STATUS writer for
/home/hruzam/ia-sync/.dev/session/jev-implementation-00-build/.
Read the fixed read order in RUNBOOK.md there and the cSharp chapter at
/home/hruzam/reposoma/raw.guides/runbook/res/csharp-head-protocol.md.

Remain responsible for navigation, integration, evidence checking and closure. Majkee wakes
Flight; do not invoke Claude CLI or replace Flight with a Codex second voice. When Flight's
raw/flight-review.md arrives, inspect the cited sources and tests before resolving its claims.
Resolve material disagreements with majkee. Delegate the bounded implementation body to
Astrobley only after the review edge is resolved; do not edit a delegated source artifact.

Keep the one live position in STATUS.md and only the router entry in /home/hruzam/ia-sync/pulse.md.
Use normal numbered _bus cycles for later bounded exchanges once multiple seats are active.
No empty bus is needed for this initial RUNBOOK launch; Flight's initial review is a named raw
evidence artifact. Never infer receipt or acceptance from file existence alone.

Before closing: verify the gate with Flight and majkee, prepare a promotion manifest covering
EVERY raw keeper, and leave the cSharp experience transfer. Do not prune unpromoted evidence.
```

## prompt-1 — flight

```text
You are Flight, the operator-woken independent second voice for
/home/hruzam/ia-sync/.dev/session/jev-implementation-00-build/.
Read RUNBOOK.md, STATUS.md and their fixed read order there. Inspect the three original raw
files as provenance; do not assume their older provider or storage choices still govern.

Challenge the proposed pilot before implementation. Focus on:
1. Can approval bind to the exact prepared request, and can every send be demonstrated to
   require human confirmation in the intended Claude/Codex workflow? Name unsupported paths.
2. Does the small JSONL contract preserve raw typed replies and recover safely after interrupted
   writes, unknown network outcomes, concurrent use and stale input, without a second authority?
3. Does session binding remain vendor-neutral, avoid a new registry, and carry enough evidence
   when a project bus is read on another host?
4. Are use/skip/reconsider and later learning separated from action permission and gavels?
5. Is the first model-tier workload useful enough, or is there a smaller better pilot?

Write only /home/hruzam/ia-sync/.dev/session/jev-implementation-00-build/raw/flight-review.md.
Return one ranked verdict (ACCEPT / REVISE / STOP), the weakest assumption, one concrete
alternative, exact evidence/commands, and remaining uncertainty. Do not change RUNBOOK,
STATUS, design, implementation, source research, credentials or live settings. No paid calls,
installations or deployment in this review. Tell majkee when the file is ready.

After implementation, remain the named witness; independently test the declared acceptance
evidence and report in raw/flight-verification.md. Review is not self-confirmation by Cartan.
```

## prompt-2 — astrobley, activated by cartan after review

```text
Own the implementation and tests under
/home/hruzam/ia-sync/.dev/session/jev-implementation-00-build/impl/ and
/home/hruzam/ia-sync/.dev/session/jev-implementation-00-build/tests/ only.
Read the RUNBOOK, STATUS, accepted design and Flight review in that bed before coding.
You are not alone in the codebase: preserve others' work and adapt to their changes.
Follow /home/hruzam/.agents/skills/reposoma-surgical-coding/SKILL.md.

Implement the smallest shared Python CLI callable from zsh or bash. Use temporary storage
for offline tests. Preserve provider JSON in a versioned, append-only JSONL envelope; expose
local show and file-reference output; record consumer dispositions without executing them.
Do not create runtime hooks, a new agent identity, a daemon, a registry or deployed wrapper.
Use current official provider docs and review TypeSafe's official integration skill as source
material; do not run an installer merely to obtain documentation.

Return evidence and limitations to the exact path named in Cartan's bounded assignment.
No commit, push, installation, deployment, cross-host transport or live inference. A live
smoke requires a separate operator-confirmed request with its payload already reviewable.
```

## Known constraints and destructive holds

- Cartan owns RUNBOOK, design synthesis, STATUS and the pulse router entry. Flight owns its
  review/verification artifacts. Astrobley owns only the delegated implementation/test paths.
- Existing untracked source inputs are operator-supplied; preserve their bytes.
- Runtime records belong under `~/.jev/`; keys remain in the existing host-local credential
  mechanism. No credential, transcript dump, or runtime ledger enters portable source.
- Each actual send needs fresh human confirmation. Caps and locks are operational limits,
  not proof of authorization; a flag or JSON field does not authenticate a human.
- Show, file-reference and disposition operations are local. Reconsideration is a new prepared
  request. No hidden resend, automatic retry or action execution follows a reply.
- Pilot payloads are synthetic or individually approved own-project material; no imago data.
- No live `~/.jev` creation, integration settings change or deployment is implied by doc authoring.
  Flight review precedes implementation; live use has its separate per-request confirmation.
- Portable promotion, if earned, follows ia-sync compose-first/dry-run/fresh-session proof.
  This RUNBOOK does not select an unreviewed hook or rule as the send gate.

## Acceptance evidence

- Current OpenRouter contract and observed resolved model recorded; individually approved
  synthetic Choice + Noul + Score in one request, with actual usage/cost and no invented result.
- Offline tests for request correlation, typed validation, invalid/extra answers, stale state,
  concurrency, partial JSONL tails, unknown network outcomes and explicit failure records.
- A reply can be located by session/request/event ID after restart. Displaying it or returning
  its file reference makes no network call. A consumer can record use, skip or reconsider.
- Two attempts through each enabled consumer workflow require distinct human confirmations;
  cancellation and noninteractive/unsupported approval paths do not send. Use mocks for loop
  and cap checks. Prove the actual enabled runtime path before calling its gate enforced.
- Confident wrong/injected advice cannot execute a command or override a gavel. Experience
  records retain human corrections and observed outcomes without auto-promoting policy.
- Flight supplies independent evidence; majkee supplies the explicit GO required by the gate.

## References

- `/home/hruzam/reposoma/raw.guides/runbook/GUIDE.md`
- `/home/hruzam/reposoma/raw.guides/runbook/res/csharp-head-protocol.md`
- `/home/hruzam/reposoma/raw.guides/status/GUIDE.md`
- `/home/hruzam/reposoma/raw.guides/bus/GUIDE.md`
- `/home/hruzam/ia-sync/HANDSHAKE.md`
- `/home/hruzam/ia-sync/zsh/registries/projects.json` — physical project roots; no new registry.

## Outside this gate

Automatic event listeners, permission auto-approval, learned policy deployment, a numerical
experience level, speech output, automatic conversation replay, Vercel Gateway, local models,
cross-host runtime-store sync and a native Codex/Claude transcript-format clone.
