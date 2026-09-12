# RUNBOOK — runbook-tool-00

```yaml
goal:            A deployable Python TUI (cs-palette class) that reads all RUNBOOK beds
                 from a .dev/session/ tree, lists them with status+frontmatter in D1,
                 and shows the selected bed's R1–R5 sections (RUNBOOK / STATUS / res/ /
                 raw/ / _bus/) in a live-updating D2. WRITELN vertical scroll only.
                 Deployed to both machines via ia-sync zsh/nablarva/runbook/ scope.
gate:            Working TUI confirmed in a fresh shell on office; deploy.sh propagates
                 to home; zj-monitor seed updated to reference the real command (not a
                 naked zsh placeholder). All R1–R5 sections readable; _bus/ auto-reloads.
participant_0:   [@Trajectory, {claude, sonnet, high}, home]   # cSharp · implementer
participant_1:   [@Oraculum, {claude, opus, high}, office]     # second mind · auditor
                                                               # challenges design before
                                                               # build; reviews result
participant_2:   [@majkee, human, home]                        # gavel · enable · hands
status_owner:    @Trajectory
schema_note:     single bed, no siblings. source lives in ia-sync/zsh/nablarva/runbook/;
                 session lives here (nablarva). deploy via deploy.sh (zsh rsync additive).
```

> Position lives in `STATUS.md` (not yet created — @Trajectory owns it).

---

## Why this tool

A session involves multiple RUNBOOK beds under `.dev/session/`. Currently navigating
them is grep + cat. The runbook tool gives a TUI browser:

- D1 (left): all beds under the scanned root, one row per bed, showing
  slug + STATUS `next:` line + gate state
- D2 (right): selected bed's R1–R5 sections, scrollable, WRITELN (↑↓ only)
  - R1 RUNBOOK frontmatter — toggleable off/on (F key)
  - R2 STATUS — where we are now; auto-reload on timer or `r` key
  - R3 res/ — subchapters list (click/enter → open in $EDITOR)
  - R4 raw/ — sources list
  - R5 _bus/ — living bus turns; most critical for multi-session; auto-reload
- Small buffer column or strip: `p` prints selected path to terminal scroll-back
  (same pattern as cs-palette — curses escape → print → restore)
- Labels: loaded from yaml/json per runbook if present; fallback = slug

The tool is NOT a replacement for editing STATUS.md. It is a read-fast / orient-fast
layer. The operator writes; the tool reads and renders.

## Posture

- **WRITELN contract:** no left-right scroll anywhere. Text wraps or clips, never scrolls
  horizontally. Operator sees what fits; `e` opens full file in $EDITOR.
- **Read-only default:** no writes, no status mutations from inside the TUI.
  `e` key opens files in $EDITOR via the curses escape pattern.
- **Scan root:** discovered at call time — walk up from $PWD looking for `.dev/session/`
  (same discipline as temple-mail-manage's `_mail` discovery). Flag `--root` overrides.
- **Labels from yaml:** if a bed contains a `roster.yaml` or `labels.yaml`, participant
  calling signs are loaded from there; otherwise slug is shown.

## Source layout

Extend the existing `zsh/nablarva/` scope — no nested signpost or keyboard (one per scope law).

```
~/ia-sync/zsh/nablarva/
  runbook.py               Python TUI — self-contained, stdlib only; copies the 4 curses
                           helpers from cs-palette (clipped/safe_add/visible_slice/wrap_block)
                           rather than importing cs_vault (does not resolve from here)
  runbook.zsh              engine: _rb_open, _rb_pick, _rb_help bodies
                           added as new PARTITION to existing nablarva.zsh (engine)
  keyboard.zsh             `rb-open`, `rb-pick`, `rb-help` aliases added as PARTITION 3
                           of the existing nablarva/keyboard.zsh — no new file
  base.zsh                 existing signpost; already sources keyboard + engine;
                           wired from config.*.zsh — build step 4 likely disappears
```

Deployed to `~/.config/zsh/nablarva/` via deploy.sh (additive rsync; `.py` under `zsh/`
already proven by `ai/cs-palette.py`).

## Design — TUI sections

### D1 rows

Each row: `[state] slug`
- `?` no RUNBOOK.md  ·  `·` RUNBOOK, no STATUS  ·  `→` STATUS present  ·  `!` STATUS with `in_flight:` not none
- Case-insensitive lookup (STATUS.md / status.md); lowercase variant marked with dim `~` so drift is visible
- Every directory is a row — never hide beds with missing files; the gap is information

### D2 — fixed strip (top, not scrolled)

`next: <value>` from the selected bed's STATUS, always visible.
Extraction: flat key from fenced ```yaml block → regex fallback `^\s*`?next:\s*(.*)$` anywhere → `—`. Strip surrounding quotes.

### D2 sections (selected bed, scrollable)

Sections ordered by priority: STATUS first, then __bus/ (most critical), then RUNBOOK, then other bed files, then raw/.

```
── R2 STATUS ───────────────────────  (auto-reload on tick or `r`)
<contents of STATUS.md>

── R5 __bus/ ────────────────────────  (auto-reload on tick; sorted by NN prefix)
  01.seat.kind.md  02.seat.kind.md  ...

── R1 RUNBOOK ──────────────────────  (toggle F — off collapses this section)
goal:   ...
gate:   ...
participant_N: ...

── R3 bed-root files ───────────────  (pads, dock, handoff, CS cards — not RUNBOOK/STATUS)
  pad.1-scope.md  pad.2-scope.md  ...

── R4 raw/ ─────────────────────────
  source1.md  source2.md  ...
```

Reader: fenced ```yaml block with `---` fallback for frontmatter extraction. No PyYAML — stdlib only.

### D2 item cursor

An item cursor moves across file entries in R2/R3/R4/R5 rows (skips text lines). `Enter` or `e` opens the file
under the item cursor in $EDITOR. Section-jump keys `1`–`5` jump scroll offset to the section start.

### Auto-reload

One 1 s tick via `screen.timeout(1000)`. On each tick: check `st_mtime_ns` of STATUS and `__bus/` listing;
reload and rewrap only when changed. `erase()` + redraw + `refresh()` — no `clear()`, no subwindows.
Scroll offset clamped to valid range after every rebuild/resize.

### ESCDELAY

`os.environ.setdefault("ESCDELAY", "25")` before `curses.initscr()` — avoids ~1 s Esc latency.

### wrap_block parameters

`break_on_hyphens=False` (preserves kebab slugs and paths). `break_long_words=True` (an absolute
path must wrap, not clip — WRITELN law). No forced `subsequent_indent`.

### Scan root resolution

`--root` flag > `$RB_ROOT` env > `$PROJECT_NAB_PATH/.dev/session` > walk-up (last resort; checks
`basename==session && parent==.dev` to stop at the correct level). zsh wrapper resolves and passes
`--root` explicitly — same discipline as cs-palette's `--vault`.

### Keybinds

```
↑ ↓           navigate D1 list / D2 scroll
Tab           switch focus D1 ↔ D2
1–5           jump D2 scroll to section start (R2 / R5 / R1 / R3 / R4)
F             toggle R1 RUNBOOK section visibility
r             manual reload STATUS + __bus/ (also fires on tick)
e             open item-cursor file in $EDITOR (curses escape pattern)
p             print selected bed path to terminal scroll-back (TUI stays)
q / Esc       quit  (ESCDELAY=25ms)
```

## Build sequence (single bed)

1. **Design audit** — @Oraculum reads RUNBOOK, challenges before any code ✓ done 2026-09-04
2. **RUNBOOK revised** — 9 Oraculum adjustments folded ✓ done 2026-09-04
3. **runbook.py** — Python TUI: scan, D1 list, D2 sections, keybinds, 1 s tick, mtime-gated reload
4. **Extend nablarva/ scope** — `runbook.zsh` engine + `keyboard.zsh` PARTITION 3 + verify `base.zsh`
5. **deploy.sh** — propagate to `~/.config/zsh/nablarva/`
6. **Fresh-session verify** — new shell, `rb-open`, confirm D1 + D2 + all sections + auto-reload
7. **Gate close** — majkee confirms; ovitmugen `seeds/monitor.kdl` command line updated
   (path TBD when ovitmugen is built — seed lives at `~/ia-sync/zsh/nablarva/ovitmugen/seeds/`)

## Known constraints

- WRITELN everywhere — no curses `hline` scrollbar, no left pad truncation that
  forces sideways reading. Text wraps at panel width (clipped with `…` if single line).
- Auto-reload for R2/R5 must not cause TUI flicker. Use targeted section refresh,
  not full `screen.erase()` on timer tick.
- Scan must handle beds with missing STATUS.md, missing res/, missing _bus/ — degrade
  gracefully (show `—` not crash).
- `e` (editor) uses the same curses escape pattern as cs-palette: `curses.def_prog_mode()`
  → `curses.endwin()` → subprocess → `curses.reset_prog_mode()` → `screen.refresh()`.

## References — point, never copy

- `~/ia-sync/zsh/ai/cs-palette.py` — TUI pattern reference (curses escape, D1/D2/D3,
  wrap_block, safe_add, visible_slice)
- `~/ia-sync/zsh/ai/cs_vault.py` — shared vault helpers pattern
- `~/reposoma/raw.guides/runbook/GUIDE.md` — RUNBOOK schema (R1–R5 meaning)
- `~/unikuklatrix/nablarva/.dev/session/ovitmugen-00-console/raw/brief.ovitmugen-sentinel.2026-09-04.md`
  — @kukla sentinel design (feeds label loading in v0.2)
- WRITELN rule: page 1 of majkee's handwritten design (2026-09-04)

## What closes this gate

Working TUI in a fresh shell, all sections rendering, bus auto-reload confirmed,
deploy.sh propagated to home, ovitmugen seed updated with real command. @majkee gavelss.
@Oraculum's audit complete (written to `__bus/` before any code starts).
