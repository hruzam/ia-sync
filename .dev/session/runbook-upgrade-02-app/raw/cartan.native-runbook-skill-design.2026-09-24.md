# Cartan return — staged `csharp-head` skill design

Date: 2026-09-24  
Disposition: reviewable design only; deploy-inert.

## Result and corrected boundary

Staged skill: `/home/hruzam/ia-sync/.dev/session/runbook-upgrade-02-app/raw/csharp-head/SKILL.md`.

Existing Codex behavior can sustain the current cSharp now. Octopus explicitly says its park is
the skill's exit while a RUNBOOK `head_note:` cSharp stays live under the shared protocol
(`codex/skills/octopus/SKILL.md:100-101`). An exact RUNBOOK prompt plus that `head_note:` is
sufficient for the current head. The gap is discoverable, reusable activation for later arcs,
not runtime inability or a missing state/receipt mechanism.

The staged skill therefore adds no doctrine, template, agent, state file, scheduler, or transport.
It routes the gaveled RUNBOOK/cSharp/STATUS/BUS/fan-out law, preserves one STATUS writer, keeps
Cartan in the main thread, delegates application bodies, and requires a named witness for the
head's own claims. Its description excludes ordinary C# programming requests.

## Proposed source change after @majkee confirms

1. Add `codex/skills/csharp-head/SKILL.md` from the reviewed staged specimen.
2. Add one `csharp-head` row and Octopus/Medusa boundary sentence to `codex/README.md`.
3. Add one cSharp main-thread protocol row to
   `codex/skills/codex-harness/references/cross-runtime-roles.md`.

No changes are proposed to Octopus, Medusa, Claude `/runbook`, AGENTS, config, hooks, custom
agents, or shared reposoma guides.

## Validation and activation

Static validation command:

```text
python3 /home/hruzam/.codex/skills/.system/skill-creator/scripts/quick_validate.py /home/hruzam/ia-sync/.dev/session/runbook-upgrade-02-app/raw/csharp-head
```

Observed: `PASS — Skill is valid!`; `git diff --check` also passed. The staged SKILL is 71 lines.

Deployment source/target after source review:
`/home/hruzam/ia-sync/codex/skills/csharp-head/` → `/home/hruzam/.agents/skills/csharp-head/`.
Cartan/operator must first run `bash /home/hruzam/ia-sync/deploy.sh --codex-only --dry-run`;
actual deployment remains an operator/Cartan action after review.

Fresh-session proof must invoke `$csharp-head` against a disposable two-branch fixture. PASS means
the main thread authors one RUNBOOK and one STATUS, stays active, delegates both product bodies,
updates STATUS before relay, checks durable RETURN/VERDICT contents before joining, uses a named
peer to test the head's claim, and writes no product body. FAIL if it parks as Octopus, implements
as Medusa, treats chat or file presence as proof, creates another state surface, or self-confirms
closure.

Current official OpenAI documentation fetched for this audit states that skill name/description
drive discovery and explicit invocation is available, while current Codex guidance recommends
short discriminating descriptions and progressive disclosure:

- https://developers.openai.com/api/docs/guides/tools-skills
- https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra

No deployable source, live skill, RUNBOOK, STATUS, pulse, POINT, transport, commit, or deployment
was changed by this design pass.
