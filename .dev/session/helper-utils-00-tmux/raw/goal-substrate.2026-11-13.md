# Personal tmux helper — goal substrate for Claude

Date: 2026-11-13 · From: Cartan / Codex · To: the cooperating Claude session

Majkee explicitly ended buffering and asked Cartan to write this handoff at this
path. It captures his request and the discussion so far. It is an uncanonical
goal substrate, not an approved architecture or an implementation RUNBOOK.
Majkee will explain the Claude ↔ Cartan cooperation method later; this document
does not assign either participant control of the other or start a transport.

## What Majkee wants

A small, personal, friendly and “idiot resistant” utility for managing tmux
sessions while he learns tmux syntax. He already has small zsh helpers in his
`.majkee/` personal vault and imagines another such helper, with local files
named something like `scheme-XXXX.json`.

He can provide the intended CWD, tmux session name and window names. Each window
must be able to start in its own directory. The helper should make managing
that arrangement comfortable without demanding fluency in raw tmux commands.
The exact JSON schema, command name and final code location remain open.

He welcomes ideas, but wants a small living utility, not promotion into shared
canon or a new harness framework.

## The main problem: the current arrangement feels like a cage

An existing session helper has been useful. Its fixed pane arrangement now
gets in the way: switching between CLI sessions takes roughly three shortcut
steps instead of the one he has with independent terminal views. He also cannot
observe two CLI sessions together in the arrangement he is describing.

Most hosts comfortably show two terminal windows side by side. Home, the host
of this discussion, can fit three, but he usually avoids using its full width:
the very wide view is uncomfortable. Do not make filling the monitor a goal.

The desired freedom is to open and arrange independent CLI views manually,
at least initially, and use his familiar terminal/desktop shortcuts to move
between them. Two simultaneous visible CLI conversations are a normal case.
An optional third view should not dictate the design.

Keep terminology explicit: desktop terminal windows/tabs are different from
tmux windows, and a CLI conversation is different again. Do not turn his
request for independent visible views into another forced tmux layout.

## Proposed per-CLI metadata display, in Majkee's words and proportions

For each CLI view A, he imagines a horizontal divider:

- A-1: the CLI TUI, occupying roughly 85% of the view.
- A-2: a smaller pane beneath it, displaying that CLI session's metadata.

Two such independent views can sit side by side. The useful fixed pairing here
is one CLI with its own metadata, rather than two CLIs bound into a fixed pair.
He does not need the utility to place the two desktop views automatically.

The metadata should recognize the vendor and show, in this order:

1. Model and reasoning effort.
2. CWD.
3. Context remaining.
4. CLI session name/title, reacting to later name changes.
5. CLI session ID.
6. The path to the session's JSONL conversation transcript.

The display must respond to terminal width changes. When narrow, continue on
following lines rather than hiding or truncating the information. Treat the
85/15 split as an approximate starting point: exactly how to keep all fields
visible at narrow widths is still a design decision.

Codex already displays much of what he needs in its own status line. The
stronger immediate need is Claude CLI, where he had not found an equivalent
setting. He is describing the desired information and visibility, not asking
us to assume that every vendor exposes every field through the same mechanism.

## A separate living manager

Majkee also wants the utility to remain available as a living manager in a
separate tmux window or pane, scoped to the current matter. It should help him
manage sessions while the CLI views remain independently usable.

The manager's exact actions are not settled. Scheme launching, live listing,
attaching, creating windows, renaming, stopping and other actions must not all
be treated as already requested features. Resolve the smallest useful set.

## Cartan's suggestions — offered, not yet accepted as design locks

- Preview a scheme's names and directories before launching it.
- Repeated launches should reuse existing work, preserving running processes
  and directories the user has changed since launch.
- Validate paths and explain errors in ordinary language.
- Keep opening/resuming separate from destructive actions; make destructive
  intent explicit and require confirmation where appropriate.
- Show or offer the equivalent tmux command so the helper teaches the syntax.
- Distinguish a saved launch recipe from actual live state; consider whether
  the manager should also recognize manually opened sessions.
- Keep scope/matter labels, tmux names and vendor conversation titles separate.
- Bind metadata to the actual CLI session, not merely its CWD or whichever
  transcript happens to be newest. Multiple sessions may share one directory.
- Missing, stale or estimated values should be visibly identified rather than
  presented as exact live metadata.

Ordinary clients attached to the same tmux session share its selected window.
Independent views therefore require an explicit choice of separate sessions,
grouped sessions with independent selection, or another verified arrangement.
This is an implementation consideration, not a choice already made by Majkee.

## Existing material and evidence to reconcile

Read the sibling [claude-export.md](claude-export.md). It was already present
when this handoff was written. It reports Claude-side probes and contains an
explicitly untested sidecar sketch; this handoff does not certify those probes.

Useful existing source in ia-sync:

- `zsh/session/help/ovitmugen/HELP.md`
- `zsh/session/ovitmugen.py`, `ovitmugen.zsh`, `ovitmugen.tmux.conf`
- `zsh/session/help/tmux-session/HELP.md`, including the existing independent-view helper

Ovitmugen's documented outer frame, inner agent tabs and fixed runbook pane
are relevant to the navigation complaint. Confirm which helper Majkee means
before treating ovitmugen as the exact tool to replace.

At handoff authoring, `claude/settings.json` already had an uncommitted
`statusLine` addition and `claude/hooks/statusline.sh` was untracked. They belong
to work already in progress. Cartan read them and did not change or deploy them.

There is a concrete evidence disagreement to investigate:

- The official [Claude status-line documentation](https://code.claude.com/docs/en/statusline)
  describes multiline output, width input through `COLUMNS`/`LINES`, and fields
  covering the requested metadata, including session effort and session name.
- The sibling Claude export reports that the installed native status line
  truncates, with no multiline control, and proposes reading local session files
  and JSONL instead. It labels several resulting fields approximate or config-only.

Do not silently choose one account. Verify the installed CLI's actual rendering
and data feed. A metadata pane fed by the native status-line callback is another
candidate to investigate; it could avoid reconstructing context from transcripts.
Its feasibility and side effects have not been tested here.

Cartan observed `tmux 3.7c` and Claude Code `2.1.323` on home during this discussion.
No metadata pane was built or tested by Cartan. Reliable external Codex metadata
access also remains unverified; an existing native footer does not prove that
every value can be exported to another pane.

## What success should feel like

Majkee can keep two CLI conversations visible, switch focus with his usual
single terminal/desktop action, and read the correct metadata beneath each
without losing long fields when resizing. A separate manager helps with the
current matter. A saved recipe saves typing without forcing screen placement
or disturbing work that is already running.

## Open threads and current authorization

- Final home of the personal utility and schemes; do not infer the exact
  `.majkee/` path from shorthand alone.
- Minimum first-version management actions and meaning of a matter/scope.
- Native footer versus dedicated metadata pane, including installed-version proof.
- Independent tmux view arrangement and resize/height behavior.
- Exact identity binding, metadata freshness, rename updates and vendor adapters.
- Cross-host path differences, if the same scheme will travel.
- Claude ↔ Cartan cooperation method: Majkee will explain later.

The present instruction authorizes this handoff. It does not authorize this
document to invent the cooperation protocol, assign implementation ownership,
alter existing helpers, deploy runtime changes, or promote the proposal to canon.
Continue from Majkee's next cooperation instructions and the applicable local gates.

## Operator follow-up: independent attachments and usable history

After this handoff, Majkee created `helper-utils-00-tmux` and attached two desktop
terminals to it. Both followed the same single window, preventing independent
navigation. He explicitly asked Cartan to resolve that and the lack of usable
scroll/PageUp/PageDown history before resuming the CLI sessions there.

He also wants the eventual helper to include specific defaults that prevent
both problems. Treat independent attachments and discoverable working scrollback
as first-version requirements, rather than optional polish.

Cartan prepared two grouped views, moved the two existing clients into them,
and applied an experimental workspace-scoped comfort profile. The observed
setup, shortcuts, limitations and reproduction commands are in
[live-tmux-setup.2026-11-13.md](live-tmux-setup.2026-11-13.md).
This is a bounded live remedy; it does not settle the larger utility design.
