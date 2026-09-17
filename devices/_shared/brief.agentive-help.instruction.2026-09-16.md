# brief — agentive-help: small lookup viewer for the agentive termux bed

status: INSTRUCTION ONLY — not built, not deployed. Written by @Metaterminal (terminal-layer
seat, human-invoked, standalone) at majkee's request. Hand to whichever seat implements
`devices/_shared/termux/` work (this repo's convention: a "head" seat authors/reviews,
@Delta does surgical file authoring under it — see
`.dev/session/codex-remote-control-cli-01-wrapper/RUNBOOK.md` prompt-3 for the house shape
of this kind of brief). Metaterminal does not implement or deploy this itself — see
"who does what" at the end.

## why

`devices/_shared/termux/README.md` is a static help card — one file, scroll to find your
answer. On a phone keyboard that's real friction: no lookup, no structure, and nothing in
it is ever landed back into your shell without retyping. This brief replaces "one README"
with a small, **editable, 2-level tree of short markdown notes** plus a viewer that does
three things in sequence: load the right note, show it, and stage it in a tmux buffer so
its content can be pasted straight into the working pane (or, symmetrically with
`agentive-send`, pushed out to the Android clipboard) — no retyping on a phone keyboard.

## the tree (2 levels, editable, portable source)

```
devices/_shared/termux/help/<category>/<topic>.md
```

- Level 1 = `<category>` (a directory): e.g. `hosts/`, `keys/`, `approvals/`, `buffer/`.
- Level 2 = `<topic>.md` (a file): one short markdown note per topic, plain prose +
  fenced command blocks. No frontmatter required; keep each note short enough to read on
  a phone popup without scrolling much.
- Lives in `devices/_shared/termux/help/` in **ia-sync source** (portable, git-tracked) —
  same PUSH-only install law as the rest of `devices/_shared/termux/`
  (`devices/_shared/termux-bootstrap.md`; devices never pull). It deploys as plain files,
  no build step — editing a note is a one-line commit + normal push flow, nothing else
  changes.
- Seed it initially by lifting sections straight out of the current `README.md` (e.g.
  `hosts/bed.md`, `keys/s1-s4.md`, `approvals/asking-mode.md`, `buffer/paste.md`) — do not
  duplicate content between the README and the tree; the README should end up pointing at
  `agentive-help` for the details it currently spells out inline, not repeating them.

## the command — `bin/agentive-help` (naming matches `agentive-door` / `agentive-seed` / `agentive-send`)

Three-stage pipeline, in order:

1. **loadmd** — resolve `<category>/<topic>` (or just `<category>` → list its topics, or
   no args → list all categories) to a path under `help/`, read the file. Absolute path
   internally, per house law ("absolute binaries/paths in every wrapper command," home
   PATH scar). No-arg / partial-arg case must degrade to a menu, not an error — that's the
   whole point of a phone-friendly lookup over a scroll-and-search README.

2. **display to window help** — show the loaded note **without disturbing the current
   pane's layout**, since the whole point is you're mid-session in a seat window. Use
   `tmux display-popup`, not a split:
   ```sh
   tmux display-popup -w 85% -h 85% -E "sh -c 'cat -- \"$file\"; read -n1 -p \"[any key to close]\"'"
   ```
   (tmux ≥ 3.2 required — office/home both confirmed 3.7x live, per
   `01-wrapper/STATUS.md` C0 probe — no version gate needed.) Popup closes on keypress,
   returns you to exactly where you were. If a note is long enough to want scrolling,
   pipe through `${PAGER:-less -R}` inside the popup instead of `cat`.

3. **print to buffer** — stage the raw note text into a **named** tmux buffer (named, so
   it doesn't clobber whatever's already in the default buffer from `agentive-send`):
   ```sh
   tmux set-buffer -b agentive-help -- "$(cat -- "$file")"
   ```
   Two consumption paths, both worth wiring since they're nearly free once the buffer is
   set:
   - **Inbound to the pane** (the common case — a note contains a command you want to run
     without retyping it on a phone keyboard): `tmux paste-buffer -b agentive-help`,
     bindable to an extra-keys row entry alongside the existing S1–S4/PASTE/DETACH set.
   - **Outbound to the device clipboard** (symmetric with `agentive-send`, which goes
     clipboard → tmux buffer; this is the reverse leg): only meaningful when run
     device-side inside Termux —
     `tmux show-buffer -b agentive-help | termux-clipboard-set`. Do not build this as a
     PC-side assumption; `termux-clipboard-set` only exists on the device.

## constraints (carried over from the sibling wrapper work — do not relitigate)

- No new daemon, no new listener, no web layer, no protocol — plain files + tmux
  primitives only, same as `bin/bed` / `bin/agentive-send`.
- PUSH-only install; devices never pull (`devices/_shared/termux-bootstrap.md`).
- Additive only: the tree is new, the README gets thinned to point at `agentive-help`
  rather than losing content — never a silent delete of what's already documented.
- Absolute paths/binaries in the script (home PATH scar — `claude` is not on home's
  non-interactive SSH PATH; do not assume any binary's location, resolve or hardcode).
- Keep the tree host-agnostic: nothing device-specific or host-specific belongs in a
  `help/*.md` note's *content* — if a note needs to branch by host, that's a sign it
  belongs in `bin/bed`'s registry lookup instead, not hand-duplicated per host.

## acceptance sketch (for whoever picks this up to turn into a real gate)

- `agentive-help` with no args lists categories; `agentive-help hosts` lists topics under
  `hosts/`; `agentive-help hosts/bed` opens the popup with that note's content.
- Popup opens and closes cleanly inside a live `agentive` bed window without disturbing
  the other seat windows (1–4) or the living session in window 0.
- `tmux paste-buffer -b agentive-help` after a lookup lands the note's command text in
  the current pane, verified once from Redmi's Termux keyboard (the friction case this
  exists for).
- One round-trip verified device-side: `tmux show-buffer -b agentive-help | termux-clipboard-set`
  followed by a manual paste into a non-terminal app, confirming the outbound leg.

## who does what

- **This brief** — written by @Metaterminal, staged in a `/tmp` sandbox, not committed,
  not deployed. Terminal-layer scope (tmux/PTY mechanism), squarely mine to author; I do
  not implement scripts against source or push to devices — that crosses into the
  wrapper-session's own execution lane (head + @Delta + Cartan counter-sign, per
  `01-wrapper/RUNBOOK.md`).
- **Implementation** — whichever seat you route this to writes `help/` seed notes +
  `bin/agentive-help` under `devices/_shared/termux/`, gets it head-reviewed the same way
  `bin/bed`/`bin/agentive-seed` were (STATUS.md c2_progress shows that review caught 4
  real defects last time — repeat that step, don't skip it for a smaller script).
- **Deploy** — PUSH flow to the Redmi, same as everything else in that directory; not
  mine to run.
- **You** — decide whether this rides as a new small session/task or as an addendum
  inside a future `codex-remote-control-cli-0N` sibling; it wasn't named in the existing
  backlog-siblings list, so treat it as fresh scope rather than smuggling it into the
  01-wrapper's already-passed gate.
