---
name: reposoma-surgical-coding
description: Reposoma surgical coding discipline — state assumptions, minimum change, verify outcomes. Use for any bounded implementation (Claude thinking-coder, Cursor engine-coder, Gemini practical-coder).
---

# Reposoma Surgical Coding

Vendor-neutral skill shared across surgical coding lanes. **Do not duplicate this text inside agent cards** — reference this skill instead.

**Tradeoff:** Biases toward caution over speed. For trivial one-liners, use judgment.

## 1. Think Before Coding

Do not assume. Do not hide confusion. Surface tradeoffs.

Before implementing:

- State assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them — do not pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what is confusing. Ask.

## 2. Simplicity First

Minimum code that solves the problem. Nothing speculative.

- No features beyond what was asked.
- No abstractions for single-use code.
- No flexibility or configurability that was not requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite.

Ask: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

Touch only what you must. Clean up only your own mess.

When editing existing code:

- Do not improve adjacent code, comments, or formatting.
- Do not refactor what is not broken.
- Match existing style even if you would do it differently.
- If you notice unrelated dead code, mention it — do not delete it unless asked.

When your changes create orphans:

- Remove imports, variables, and functions your changes made unused.
- Do not remove pre-existing dead code unless asked.

Every changed line should trace directly to the task or user request.

## 4. Goal-Driven Execution

Define success criteria. Loop until verified.

Examples:

- "Add validation" → tests for invalid inputs, then make them pass
- "Fix the bug" → reproduce with a test, then make it pass
- "Refactor X" → tests pass before and after

For multi-step work, state a brief plan with verify steps:

```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
```

Weak criteria ("make it work") require clarification before coding.

## Working

This skill is working when diffs stay small, rewrites from over-engineering drop, and questions come before implementation.
