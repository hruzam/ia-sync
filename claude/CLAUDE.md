## General

Be critical, neutral, and practical. Do not default to agreement when the better response is caution or pushback.

Prefer simple native Claude Code patterns over custom runtime abstractions unless the complexity is clearly justified.

Treat `~/.claude/agents/*.md` as runtime truth. Treat any YAML registry or proposal document as design-time guidance only.

## Workspace Rules

Always check the local project `CLAUDE.md` before planning or editing.

If a workspace does not provide `CLAUDE.md`, inspect the nearest project standards or rules files before making assumptions.

Project-local rules override this global file.

If combined line count of `~/.claude/CLAUDE.md` + `./<project>/CLAUDE.md` exceeds 120, immediately notify the user.

## Git And Tools

Use `gh` for GitHub-related work when available.

Do not mention Claude Code in pull request descriptions, comments, or issue comments.

When Bash is unavailable and git inspection or session history is needed: spawn @Delta with the exact command. Session history pattern: `ls -lt ~/.claude/projects/<project-slug>/*.jsonl | head -10`, then grep target files for keywords.

## Architecture Bias

Prefer the smallest safe solution that fits the request.

Separate global agent behavior from project-specific constraints.

Avoid adding generators, registries, or automation layers until repeated maintenance pain justifies them.
