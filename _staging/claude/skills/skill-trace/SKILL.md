---
name: skill-trace
description: Invoke as /skill-trace <path>. Dry-run tracer — lists every !`command` hydration that would fire in a skill before the model sees the body, and resolves each to its output. The make -n analog for skill hydration. For agent .md files: reports "agent body is static — no hydration fires."
schema: 1
disable-model-invocation: true
arguments:
  - name: path
    description: Path to the SKILL.md or agent .md file to inspect.
allowed-tools: Read, Bash
---

I trace `!` hydration in skill files — the dry run before invocation.

**D2′ guardrail:** unchanged `.md` ≠ unchanged behavior; the model is a moving target.

## Hydration syntax

In a SKILL.md body, lines of the form:
```
!`<shell command>`
```
fire once, top-to-bottom, before Claude sees the content. Each is replaced with the
command's stdout. This is the hydration I trace.

Agent `.md` bodies are static system prompts — no preprocessing pass, no `!` hydration.

## Steps

**1 — Read the file at $path**

**2 — Classify**

Scan frontmatter (between the opening `---` and closing `---`):
- Skill markers: `allowed-tools`, `disable-model-invocation`, `arguments`, `context:`, `when_to_use`
- Agent markers: `tools:`, `maxTurns:`, `disallowedTools:`

If classified as **agent**, report and stop:
```
── skill-trace ──────────────────────────────────
File:   $path  [AGENT]
Result: agent body is a static system prompt — no ! hydration fires. Nothing to trace.
────────────────────────────────────────────────
```

If classification is ambiguous (frontmatter absent or no marker found): report as UNKNOWN,
note the ambiguity, stop — do not guess.

**3 — Extract hydration lines (SKILL only)**

Scan the body (content after the closing `---` of frontmatter) for lines matching:
`` !`<any shell command>` ``

Collect each match with its line number and raw command text, in document order.

If none found:
```
── skill-trace ──────────────────────────────────
File:   $path  [SKILL]
Found:  0 hydration commands — body reaches model as-is.
────────────────────────────────────────────────
```
Stop.

**4 — Resolve each command**

For each `` !`command` `` found: run it via Bash. Capture stdout + stderr.
Note the exit code if non-zero.

**5 — Report**

```
── skill-trace ──────────────────────────────────
File:   $path  [SKILL]
Found:  N hydration command(s)

[line N] !`<command>`
→ <stdout output, or "[exit N] <stderr>" on failure>

[line M] !`<command>`
→ <stdout output>
────────────────────────────────────────────────
These are the exact substitutions that fire before the model sees the skill body.
```

## EXIT / OUTPUT

Returns the trace report above. Headlessly invocable:
`agent("/skill-trace ~/.claude/skills/crosscheck/SKILL.md")`

The skill body is never invoked — this is inspection only.
