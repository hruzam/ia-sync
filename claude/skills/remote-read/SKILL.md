---
name: remote-read
description: Invoke as /remote-read. Temporary. Take the task from the mobile↔desktop handoff box ~/.remote/task.md — read once, memorize it, then reset the file to its blank header. Take and erase. Pairs with /remote-write.
---
I am the take side of `~/.remote`. When invoked as `/remote-read`:

1. **Sync first:** pull latest from `remote-hub`: `git -C ~/.remote pull --ff-only origin core`
   (Bash, or dispatch @Delta).
2. Read `~/.remote/task.md`. If `what` is empty → say "no task" and stop.
3. If `what` is filled: surface the task (project · who · what) and hold it in working context — memorize it.
4. **Erase once read** — reset `~/.remote/task.md` to its blank header only (labels, no content):
   ```
   # task.md — drop one task: fill the labels, save, go. one at a time.
   # take = read once, then this file resets to these blank labels.

   project:
   who:
   what:

   bye :)
   ```
5. **Sync (update on take):** commit + push the reset:
   `git -C ~/.remote add -A && git -C ~/.remote commit -m "take: <project>" && git -C ~/.remote push origin core`
   (Bash, or dispatch @Delta).
6. Then act on the task inside the named `project` — go there and do it. Take and erase.
