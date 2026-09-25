# Cartan audit — persistent cSharp head in Codex

Date: 2026-09-24  
Scope: design evidence only; no skill, runtime, deploy, transport, or canonical file changed.  
Frame: `/home/hruzam/ia-sync`, office (`hruzam-120922`, php74 + valet), Codex CLI 0.156.1;
worktree already dirty outside this report and left untouched.

## Invariant to preserve

A cSharp is one main-thread head that authors the fixed RUNBOOK and stays through the arc as
`status_owner` and navigator. It delegates implementation bodies whole, keeps STATUS the sole
present position, coordinates durable POINT → RETURN → VERDICT receipts, requires a named peer
to test its own claims, and closes only on verified evidence. The posture is a protocol, not a
new identity or worker.

Authority: `raw.guides/runbook/res/csharp-head-protocol.md:18-35,45-72`; RUNBOOK declares one
head/status owner at `raw.guides/runbook/GUIDE.md:137-151`; STATUS single-writer fan-out fields
are at `raw.guides/status/GUIDE.md:80-91`; full-session joins are at
`raw.guides/runbook/res/fanout-turns.md:12-27,38-67`; receipt ownership and verification are at
`raw.guides/bus/GUIDE.md:50-58,118-150`.

## Finding: capability exists; named activation does not

| Needed behavior | Existing | Absent |
|---|---|---|
| Author RUNBOOK + STATUS | Octopus does this (`codex/skills/octopus/SKILL.md:31-49`). | Octopus must park and may not spawn (`:51-60,85-101`); it cannot be the persistent head. |
| Stay as status owner and coordinate workers | Cartan is the controller; Medusa can delegate, preserve one writer, inspect returns, and update STATUS (`codex/skills/medusa/SKILL.md:38-68`). | Medusa receives an existing RUNBOOK, may implement directly, and returns architecture upward (`:12-14,70-83`); those are different cSharp authority seams. |
| Durable cross-runtime receipts | Shared BUS + fan-out law already supplies POINT/RETURN/VERDICT, one writer per file, joins, cold recovery, and human relay without delivery claims. | Native subagent return messages alone do not establish cross-runtime receipt or STATUS join state. |
| Persistent cSharp trigger | A RUNBOOK `head_note:` plus an exact prompt can make generic Cartan follow the shared chapter today; Octopus acknowledges this at `:100-101`. | No Codex skill is discoverable by the distinct request “author and stay as cSharp”; the name/purpose sweep found only Octopus, Medusa, and Polyp. |

Claude's `/runbook` is not the missing persistent primitive: it also plans and parks
(`claude/skills/runbook/SKILL.md:27-44,62-95`) and explicitly says its exit differs from cSharp.
Copying it would reproduce the gap.

There is one doctrine curvature to keep visible: `res/token-economy.md` is DRAFT
(`:7-10`) although Octopus routes delegation to it. The gaveled cSharp and fan-out chapters,
BUS, and STATUS are sufficient for authority and receipts; executor-cost advice remains advisory.

## Recommendation — one thin `csharp-head` skill

Add a reusable workflow skill, not an agent and not a second RUNBOOK implementation. Keep
Octopus's plan-and-park contract and Medusa's working-head contract unchanged. The skill should
route to the shared guides and express only Codex-native activation/delegation seams.

Proposed source after @majkee confirms:

1. `codex/skills/csharp-head/SKILL.md` — the only new runtime primitive.
2. `codex/README.md` — add one shared-procedure row and its boundary from Octopus/Medusa.
3. `codex/skills/codex-harness/references/cross-runtime-roles.md` — record cSharp as a main-thread
   Cartan protocol, not a delegated role.

Do not add a custom agent, hook, config, script, template, or copied guide. Do not modify the
Claude skill. `csharp-head` avoids accidental routing from ordinary C# language requests while
preserving the protocol's displayed name `cSharp`.

Trigger: explicit `$csharp-head`, or an operator request that one Cartan head author a RUNBOOK
and stay as cSharp across delegated work. It must reuse a live session whose gate already covers
the request and refuse ordinary one-step work.

Expected output/operation:

- At opening: author only the project-approved RUNBOOK, initial STATUS, and minimal pulse router;
  declare the verbatim cSharp `head_note:`, Cartan as head/status owner, @majkee where gavel or
  relay is required, and a named standing witness.
- During the arc: the main thread writes head-owned POINTs, replaces STATUS before dispatch,
  delegates disjoint bodies, checks returned artifacts, and joins only terminal verified cycles.
  Full CLI/vendor branches use BUS + fan-out; in-window subagents use native delegation, but any
  gate-bearing claim still lands as a durable receipt before STATUS advances.
- Authority: no application artifact authorship by the head; no competing STATUS writer; no
  self-confirmed gate; gate/architecture/destructive-scope change returns to @majkee and opens a
  numbered sibling when the gate changes.
- At close: verified gate, promotion manifest for every keeper, cSharp experience transfer in
  the bed's `raw/`, router removal, then project-law pruning. No new durable memory surface.

## Activation and verification gate

Source deploy path is already defined: `codex/skills/` → `~/.agents/skills/`
(`codex/README.md:15-22`; `deploy.sh:99-120`). Cartan/operator, not this audit, performs:

1. `python3 /home/hruzam/.codex/skills/.system/skill-creator/scripts/quick_validate.py /home/hruzam/ia-sync/codex/skills/csharp-head`
2. `cd /home/hruzam/ia-sync && bash deploy.sh --codex-only --dry-run`
3. After review, operator deploys with `bash deploy.sh --codex-only`.
4. In a fresh Codex main session, invoke `$csharp-head` against a disposable two-branch fixture.
   PASS requires: one RUNBOOK, one STATUS writer, cSharp head remains active, bodies are delegated,
   STATUS is written before relay, RETURN/VERDICT contents are checked before join, a named peer
   tests the head's claim, and no implementation file is written by the head. FAIL if it parks as
   Octopus, implements as Medusa, treats chat as receipt, or self-confirms closure.

Current OpenAI documentation supports a skill for this boundary: skills are reusable workflow
instructions discovered through name/description, with explicit invocation available; current
guidance recommends short discriminating descriptions and progressive disclosure rather than
duplicated itineraries:
`https://developers.openai.com/api/docs/guides/tools-skills` and
`https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra`.

This proposal is unconfirmed and deploy-inert. The current session can proceed immediately by
putting the cSharp `head_note:` and shared-guide paths into its RUNBOOK prompt; the skill would
make that already-gaveled posture a stable Codex invocation for later arcs.
