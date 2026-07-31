---
name: remote-write
description: Invoke as /remote-write. Temporary. Drop a task into the mobile↔desktop handoff box ~/.remote/task.md — fill project · who · what · bye, then leave. Drop and go. Pairs with /remote-read.
---
I am the drop side of `~/.remote`. When invoked as `/remote-write`:

1. Gather the four fields (from the invocation, or ask): **project** (which project the task belongs to),
   **who** (who's asking), **what** (the task in plain words), and the **bye** sign-off.
2. One task at a time — if `~/.remote/task.md` already has a filled `what`, warn that an untaken task
   is present and ask before overwriting.
3. Write `~/.remote/task.md`, filling the labels:
   ```
   # task.md — drop one task: fill the labels, save, go. one at a time.
   # take = read once, then this file resets to these blank labels.

   project: <project>
   who: <who>
   what: <what>

   bye :)
   ```
4. **Sync (update on drop):** commit + push to `remote-hub`:
   `git -C ~/.remote add -A && git -C ~/.remote commit -m "drop: <project>" && git -C ~/.remote push origin core`.
   Run via Bash if the seat has it; otherwise dispatch @Delta with that command. (Push is ask-gated.)
5. Confirm the drop in one line and stop. Do NOT act on the task — this is drop-and-go; the desktop
   session takes it via `/remote-read`.
