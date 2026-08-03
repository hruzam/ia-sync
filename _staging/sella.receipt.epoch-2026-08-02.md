# Receipt — @Epoch live capability pass, 2026-08-02

`purpose: source-of-record for claims in sella.coder-guide.md marked [S-EPOCH]. This`
`file travels WITH the guide (→ raw.research/agent-docs/ after the reposoma merge).`
`method: live fetch of code.claude.com/docs (sub-agents · skills · hooks · changelog),`
`snapshot accurate as of fetch time 2026-08-02; re-verify version gates before builds.`

## Claims carried into the guide

1. **No dry-run for `!command` substitution exists** (L5). Only control:
   `disableSkillShellExecution: true` global kill-switch (bundled/managed skills
   exempt). Reviewing an untrusted skill = manually reading the `!` lines.
   Confidence H (official skills doc, fetched 2026-08-02).
2. **Terse-description lean is official** (L2): docs recommend description-based
   delegation + trigger phrases ("use proactively"); example-laden descriptions are
   community convention, never doc-blessed. Skills: `description`+`when_to_use`
   truncate at 1,536 chars (documented). Agent-description budget: UNRESOLVED —
   no analogous cap found; flagged for follow-up. Confidence H / M as noted.
3. **Hooks exit-code semantics** (L4): exit 2 = the only blocking code; exit 1 does
   NOT block (logged, continues). Confidence H.
4. **Agent frontmatter surface 2026-08** (source model): name, description, tools,
   disallowedTools, model, permissionMode, maxTurns, skills, mcpServers, hooks,
   memory (user/project/local), background, effort, isolation (worktree), color,
   initialPrompt. No `schema` key exists — house `schema: 1` is forward-marker only.
   Confidence H (v2.1.219 gate, 2026-07-24).
5. **`paths` glob-gated skill activation** is a real documented trigger mechanism
   beyond description matching. Confidence H.
6. **Background-by-default is platform law** since v2.1.198 (subagents) / v2.1.218
   (`context: fork` skills); subagent messages are never permission approval.
   Confidence H.
7. **Platform absorbed the lifehacks**: memory, effort, isolation, paths — formerly
   community tricks, now first-class fields. Confidence H.

## Not covered (refresh before relying)

- agent-teams / workflows docs (adjacent primitives, unfetched this pass)
- `prompt`/`agent` hook handler types (single-source, uncorroborated)
- per-event blocking table (synthesized, spot-check before hardcoding)
