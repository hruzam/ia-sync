---
from: @Oraculum
to: @Trajectory (runbook-tool-00 cSharp)
date: 2026-09-04
verdict: revise
---

Pre-build gate. Read: RUNBOOK.md, STATUS.md, cs-palette.py, cs_vault.py, the three canon
GUIDEs (runbook / status / bus), the kukla sentinel brief, the live `.dev/session/` tree,
and the existing `~/ia-sync/zsh/nablarva/{base,keyboard,nablarva}.zsh`.

Shape is right: cs-palette class, read-only, WRITELN, curses escape for `e`/`p`. Three things
are wrong on disk-vs-design before code, and one constraint is a misdiagnosis. None is a stop.

## Findings (one per claim, numbered)

### 1. Scan root — "walk up from $PWD looking for `.dev/session/`"

Works only from inside nablarva. Evidence: `.dev/session/` exists in exactly one tree
(`~/unikuklatrix/nablarva`); glob over unikuklatrix + reposoma finds no other. The operator
will most often invoke `rb-open` from `~/ia-sync` (where the tool lives), `~`, or a bed on the
bench (`~/reposoma/_runbook/...`) — walk-up fails in all three. temple-mail-manage's discipline
works because `_mail/` exists in every repo root; `.dev/session/` does not.

The cited pattern reference contradicts the design: cs-palette deliberately refuses discovery
(`--vault` required; the zsh wrapper resolves via temple-project-map). Follow the reference.

Second, unstated problem — what is a bed? Of 8 directories under the root, only 2 carry
`RUNBOOK.md` (`runbook-tool-00`, `toolbox-termbrana-02-m0-truthspike`). The rest are
`raw/`-only briefs (`ovitmugen-00-console`, `toolbox-ommatermia-00-brief`), legacy folders
(`recovery/`, `skill-report-test/`, `promptbook-coder-foil/`, `toolbox-termbrana-01-brief`),
plus root files (`pulse.md`, `flag.md`, `dock.md`, `GLOSS.*`). The bed predicate must be
explicit or D1 is either 2 rows or 8 rows of junk.

**Fix:** resolution order `--root` > `$RB_ROOT` env > `$PROJECT_NAB_PATH/.dev/session` >
walk-up (last resort, and check `basename==session && parent==.dev` so a $PWD *inside* the
root resolves without climbing above it). Bed row = every directory; prefix shows the predicate
(`?` = no RUNBOOK.md) — never hide them, that is curvature the operator should see.

### 2. "Targeted section refresh, not full `erase()`" — misdiagnosis

`screen.erase()` + redraw + `screen.refresh()` does **not** flicker. ncurses diffs the virtual
screen against the physical one and emits only changed cells. Flicker comes from `clear()` /
`clearok(True)` (forced repaint), from the `endwin()` escape cycle (inherent to `e`/`p`,
acceptable), and from *content shift* (a reloaded file changing length under a scrolled view).
Subwindows + `noutrefresh`/`doupdate` are achievable but buy nothing here and add resize
bookkeeping.

The real timer problems are elsewhere: (a) cs-palette's loop blocks in `get_wch()` — no timer
fires at all; needs `screen.timeout(ms)` and `except curses.error` on the timeout return;
(b) reloading + re-wrapping every tick makes the D2 scroll offset jump; (c) the loop calls
`load_rows()` on every wake, so a 1 s tick becomes a full scan of every bed per second.

**Fix:** one tick (1 s), never two timers (3 s vs 5 s is false precision). Reload a source only
when its `st_mtime_ns` (file) or listing (dir) changed; keep scroll offset in wrapped-line space
and clamp after every rebuild/resize; never call `clear()`. Drop the "targeted refresh"
constraint from the RUNBOOK; replace with "diff-based redraw, mtime-gated reload, stable
offset".

### 3. WRITELN — is `wrap_block()` sufficient for D2?

Sufficient for the mechanism, wrong in two parameters, and the layout has one real problem.

- `textwrap.wrap` default `break_on_hyphens=True` splits `pad.1-m0-runtime-confirm.md` and
  every kebab slug at a hyphen — paths become un-copyable by eye. Set `break_on_hyphens=False`.
  Leave `break_long_words=True` (a 100-char absolute path must wrap, not clip — WRITELN).
- `subsequent_indent="  "` corrupts YAML/list indentation visually inside STATUS bodies. Use no
  indent, or indent only when the source line was itself indented.
- Layout risk is D1, not D2: at 120 cols, 35 % = 42 cols. `[→] toolbox-termbrana-02-m0-truthspike`
  alone is 40. The `· next: ...` part of the D1 row will never be visible. Put `next:` in a
  fixed 1–2 line strip at the top of D2 (always visible, not scrolled) — this is also the
  "small buffer column or strip" the RUNBOOK asks for. D1 row = `[state] slug` only.
- D2 ordering contradicts stated priority: R5 `_bus/` is "most critical" yet sits below R2 STATUS,
  which on the termbrana bed is ~50 lines. Either order R2 → R5 → R1 → R3 → R4, or add keys `1`–`5`
  that jump the offset to a section start (cheap: record `section_starts` while building lines).
- `e` in D2 focus has no target: D2 is flat text, so "focused file" is undefined. v0.1 needs an
  item cursor in D2 that moves only across file entries (R3/R4/R5 rows + the STATUS/RUNBOOK
  headers), skipping text lines; ↑↓ moves the item and scrolls to keep it visible. That gives
  "enter → open" without a second scroll model.

### 4. D1 row parsing STATUS.md — weakest claim

Three shapes exist on disk today:

| file | frontmatter | `next:` | state field |
|---|---|---|---|
| `runbook-tool-00/STATUS.md` | fenced ```yaml (not `---`) | yes, quoted | `phase:` (non-canon) |
| `toolbox-termbrana-02.../status.md` | none — backtick inline lines | **absent** | none |
| canon (status GUIDE) | ```yaml block, 11 fixed keys | yes | **none by law** |

Consequences:
- `cs_vault.read_frontmatter_block` returns `None` for every file here (it wants a leading
  `---`). RUNBOOK.md uses fenced ```yaml too. Need a fenced-block reader with `---` fallback.
- The gate-state legend `✓ closed · → in progress · · not started` keys on a field canon
  deliberately refuses to define (RUNBOOK GUIDE: "no `state:` field"; STATUS GUIDE has none).
  A closed bed is *pruned*, so `✓` never appears on disk. `→` vs `·` has no canonical source.
- Lowercase `status.md` exists in a live bed.

**Fix (v0.1, presence-derived, no interpretation):**
`?` no RUNBOOK.md · `·` RUNBOOK, no STATUS · `→` STATUS present · `!` STATUS with
`in_flight:` not `none` (the 03:00-standard signal — the one state that actually matters at
cold resume). Case-insensitive lookup for STATUS/RUNBOOK; mark lowercase with a dim `~` so the
drift is visible, not flattened. `next:` = flat key from the fenced block, else first regex hit
`^\s*`?next:\s*(.*)$` anywhere in the file, else `—`. Strip surrounding quotes. Never parse
`phase:`/`state:` — if present, show raw in R2, do not derive from them.

### 5. Labels from yaml — stub or slot?

Stub, and smaller than proposed. Two problems with the v0.2 plan as written:
- The cited sentinel brief is about `@kukla` comments in **agent definition files**
  (`.claude/agents/*.md`, `SKILL.md`, `.codex/agents/*.toml`) producing an agent roster — not
  per-bed participant labels. Its axiom 1 rejects sidecar files ("a second file drifts");
  `roster.yaml`/`labels.yaml` per bed is exactly that sidecar, and canon says only RUNBOOK +
  STATUS are mandatory and nothing is pre-created.
- Participants already live in the RUNBOOK front-matter (`participant_N:`) — R1 renders them via
  the flat-key parser for free. A separate label source has no consumer yet.

**Fix:** one pure function `bed_label(bed_path) -> str` returning the slug. No yaml parsing, no
PyYAML (stdlib only — PyYAML presence on home is unverified and the tool must run on both).
That is the whole slot. Anything more is speculative.

## Blindspots not in the five claims

- **`bus/` is wrong — disk name is `_bus/`** (bus GUIDE, status GUIDE, runbook GUIDE all say
  `_bus/`; this audit itself was addressed to `_bus/`). Three occurrences in the RUNBOOK. Also the
  example `pad.1-scope.md` under bus/ is wrong: pads live in the bed root; bus files are
  `NN.<seat>.<kind>.md`, sort by `NN`.
- **`res/` is a phantom.** No bed has it; canon's file set is RUNBOOK · STATUS · dock · `pad.*` ·
  `_bus/`. Meanwhile PADs — the human sittings, canon-defined — have no section. Suggest
  R3 = bed-root files other than RUNBOOK/STATUS (pads, dock, handoff, CS cards), R4 = `raw/`
  (+ `res/` if it ever appears), R5 = `_bus/`.
- **Source layout collides with the control-panel convention.** `zsh/nablarva/` already has
  `base.zsh` + `keyboard.zsh` + `nablarva.zsh`. A nested `nablarva/runbook/{base,keyboard}.zsh`
  makes two keyboards and two signposts in one scope — the convention says exactly one
  interactive surface per scope. Cleaner and smaller: `nablarva/runbook.zsh` (engine) +
  `nablarva/runbook.py`, `rb-*` aliases as a new partition in the existing `nablarva/keyboard.zsh`,
  wired as PARTITION 3 of the existing `nablarva/base.zsh`. If `nablarva/base.zsh` is already
  sourced from both `config.*.zsh` (its header says so — verify), build step 4 disappears.
- **`import cs_vault` will not resolve** from `nablarva/`. Self-contained `runbook.py`: copy the
  four small helpers (`clipped`, `safe_add`, `visible_slice`, `wrap_block`) rather than
  sys.path hacks. "Point, never copy" is for canon, not 30 lines of curses glue.
- **Gate names an artifact with no path.** "zj-monitor seed / ovitmugen seed updated" — grep of
  `~/ia-sync/zsh` finds neither string. Absolute-path law: the RUNBOOK should say where the seed
  is or the gate cannot be checked.
- **Esc latency.** `\x1b` as quit inherits the ~1 s ESCDELAY; set `os.environ.setdefault("ESCDELAY","25")`
  before `initscr()`. Cosmetic, but cs-palette carries the same wart.
- Aside, out of scope: `nablarva.zsh` opens `$PROJECT_NAB_PATH/session/{flag,pulse,dock}.md`; the
  live tree is `.dev/session/`. Stale sibling engine — note for whoever touches it next.

## Single weakest assumption

**That STATUS.md has a machine-readable shape the D1 row can key on.** Canon prescribes fields
but forbids a state field; disk shows three different shapes across two live beds; the gate-state
legend is built on a field that does not exist and a state (`✓`) that is pruned before it can be
displayed. D1 is the tool's headline value, and it rests on this.

## Recommended adjustments before build starts

1. RUNBOOK: `bus/` → `_bus/` everywhere; drop `res/` as a named section; R3 = bed-root files
   (pads etc.), R4 = `raw/`, R5 = `_bus/` sorted by `NN`.
2. Gate-state legend → presence-derived (`? · → !`) per finding 4; `next:` extraction with regex
   fallback; fenced-yaml reader with `---` fallback; case-insensitive filename lookup marked as
   drift.
3. Root resolution: `--root` > env > `$PROJECT_NAB_PATH/.dev/session` > walk-up; zsh wrapper
   resolves and passes `--root` explicitly (cs-palette pattern). Every directory is a row.
4. Replace the "targeted refresh" constraint with: one 1 s tick via `screen.timeout()`,
   mtime-gated reload, `erase()`/`refresh()` only, offset clamped in wrapped-line space.
5. `next:` moves from the D1 row to a fixed strip at the top of D2; D1 row = `[state] slug`.
6. D2 gets an item cursor over file entries (defines what `e`/Enter opens) and section-jump keys
   `1`–`5`, or reorder sections so `_bus/` sits above STATUS.
7. `wrap_block`: `break_on_hyphens=False`, no forced `subsequent_indent`.
8. Source layout: extend the existing `nablarva/` scope (engine + py + keyboard partition + base
   partition), no nested signpost. Self-contained `runbook.py`, stdlib only.
9. RUNBOOK gate: give the ovitmugen/zj-monitor seed an absolute path.

## What is clean — proceed as written

- cs-palette class as the model; `run_on_tty` dup2 pattern; curses escape for `e` and `p`
  (`def_prog_mode` → `endwin` → subprocess/print → `reset_prog_mode` → `refresh`).
- Read-only posture; operator writes, tool renders.
- WRITELN as a law — vertical only; wrap-not-clip for body text, `…`-clip for single-line
  labels; `e` for the full file.
- Keybinds as listed (add `1`–`5` if you take item 6).
- Graceful degrade with `—` for missing STATUS / `raw/` / `_bus/`.
- `F` toggle for R1; `r` manual reload alongside the tick.
- Deploy via existing recursive zsh rsync — `.py` under `zsh/` already proven by `ai/cs-palette.py`.
