---
kind: handoff
from: trajectory (claude, vistMini-01 builder; session 06352fda-5b7f-4621-b7d1-617be6bc51a4, retiring)
to: helper-utils-00-tmux local team (the two sessions below)
date: 2026-11-14
status: advice, uncanonical. Majkee owns scope; this assigns nothing.
team:
  codex:
    resume: codex resume 01a1d43b-a84f-79e0-abab-b37147f48a7c
  claude:
    session: d1ca16e9-073e-46d9-ba7d-26a816c38a67
    resume: claude --resume d1ca16e9-073e-46d9-ba7d-26a816c38a67
related:
  - ~/reposoma/.majkee/.germline/programs/tmux-bed/README.md   # switch-off / clean / rebuild commands, written 2026-11-14
  - ~/ia-sync/.dev/records/vist/2026-11-14/vistMini-01-tests/   # archived trial that ran 11 agent windows in one tmux session
---

# From someone who just ran 11 agents in one tmux session: do it this way

Your goal (goal-substrate) is a friendly personal helper. Ours was agent-to-agent delivery. We used the same tmux, and these are the lessons
that cost us real cycles. Take what fits.

## 1. Rules that would have saved us time

1. **Start the agent as the pane's root process**: `tmux new-window … 'exec claude …'`, not a shell that then runs `claude`.
   With a shell root you can't tell "agent alive" from "agent exited, shell waiting". Anything typed then runs in the shell.
   Majkee's rebuilt windows had shell roots; our delivery tool refused all of them.
2. **Labels are data; set them in the same command that creates the window.** Window options (`@seat @vendor @id`) are what
   tools read. Names get renamed. A rebuild without labels made every seat unreachable until labels were set again by hand.
3. **One agent per window, and no second pane with live output in an agent window.** tmux 3.7c tracks activity per *window*
   (`#{pane_last_activity}` is empty here), and window lookups return the *active* pane. A status pane next to an agent makes the
   agent look busy forever, and a click into it retargets tools. Use a second **status line** for metadata:
   `tmux set -t <s> status 2; tmux set -t <s> 'status-format[1]' '…#{@seat}…'`. This answers your "native footer vs metadata pane" thread.
4. **Grouped sessions for independent views** (`tmux new-session -d -t <s> -s <s>-<viewer>`). You already found this.
   Extra: a **read-only** client (`attach -r`) also blocks scrolling, so the pane looks frozen. And `send-keys` from scripts can fail
   "client is read-only" when such a viewer is attached. `paste-buffer` + `-t <pane>` avoided it for us.
5. **Never `tmux kill-server`.** Several unrelated sessions share the default server. Kill by session name.
6. **Trust and security dialogs are answered by majkee's hand, never by script keys.**
7. **The JSON scheme should hold the data the tools need, not layout taste:** session, window index, cwd, launch command, the labels.
   Layout and comfort can be defaults in the helper.

## 2. Epistemic question for you to qualify (not answered here)

> **Can agent sessions run, or be read, in raw (zero-pane) mode?**

What we know, as leads to check, not facts for your version:
- **Read, no pane needed:** Claude transcripts are JSONL under `~/.claude/projects/<cwd-slug>/<session>.jsonl`; Codex rollouts under
  `~/.codex/sessions/YYYY/MM/DD/rollout-*-<thread>.jsonl`. `tmux capture-pane -p -t <pane>` reads a screen without attaching;
  `tmux pipe-pane` can log a pane to a file. A detached tmux session needs no client at all.
- **Run headless:** `claude -p` (with `--resume <id>`) and `codex exec` (with `resume <thread>`) run without a TUI.
- **The trap:** the same session running in a TUI *and* resumed headless means two writers. In vistMini a Codex native send hit
  "active writer" (-32600). Qualify: what each CLI does when a second process opens a live session, and whether reading a growing JSONL
  while it is written is safe (partial last line).
- Why it matters to you: a helper that reads transcripts and `capture-pane` could show status **without** any extra pane, which solves rule 3.

## 3. How I'd work it, as a senior dev

- Smallest living thing first: one scheme file → one command that builds the session exactly as §1 says → one command that shows inventory.
  Use it for a week before adding features.
- Verify each claim on the installed version (`tmux -V`, `claude --version`, `codex --version`) and write the version next to it.
  Formats and footers change between releases.
- Keep your helper **out of agent delivery**. It arranges and shows sessions. Sending messages between agents is VIST's problem, behind a separate release (nablarva L21).
  The two projects meet only at the data (labels, ids), so they can run in parallel.
