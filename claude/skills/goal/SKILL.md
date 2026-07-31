---
name: goal
description: Load the current autonomous goal from ~/.claude/houston.goal and begin execution. Invoke as /goal.
---

I look for the goal file in this order:
1. `./.houston.goal` (project-local, current directory)
2. `~/.claude/houston.goal` (global fallback)

I use the first file that exists and is non-empty (ignoring lines starting with `#`).

If the file exists and contains a directive: I begin immediately, no confirmation.

If neither file exists or both are empty:
- I print: "no goal is set — write a goal into .houston.goal or ~/.claude/houston.goal"
- I read `flag.md` and `session/plan/session.plan.md` for context
- I wait for instructions

Goal file format:
```
GOAL: <one sentence — what must be done>
CONSTRAINTS: <optional — what must not happen>
OUTPUT_PATH: <optional target path>
```
