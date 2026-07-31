---
name: first-person-voice
description: >
  Invoke as /first-person-voice. Enforce first-person voice in agent cards,
  system prompts, and identity sections — the agent speaks as itself, not as
  instructions given to it. Apply when authoring or reviewing any agent definition.
---

When I write agent identity content, I use first-person voice throughout.

## Rule

All agent system prompt body content is written as the agent speaking about itself.

| Wrong | Correct |
|-------|---------|
| `You are @Atlas. You read primitives.` | `I am @Atlas. I read primitives.` |
| `You will stay inside scope.` | `I stay inside scope.` |

## Applies to

- Agent card body (system prompt text)
- Scheme inject directives
- Identity sections in CLAUDE.md / AGENTS.md

## Does NOT apply to

- `description:` frontmatter field — third-person trigger text is correct there
- `name:`, `model:`, `tools:` — YAML metadata, not identity content
- Planning documents, reports, raw notes
