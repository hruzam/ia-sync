# pad.1-palette — command palette operator test

> Mission: zsh command palette (Alt-k) · session atlas.office.building · 2026-08-05
> Convention: elements-factory rule 20-sessions-pads (pads hold raw runs)
> Precondition: Assay gate PASS · run on THIS machine before commit/push
> (sync discipline order: edit → deploy local → test → commit → push)

## Group 1 — deploy to this machine

1. `cd ~/ia-sync && bash deploy.sh --dry-run`
   - expected: lists NEW files (zsh/ai/command-palette.py, .zsh, palette-map-gen.py,
     zsh/palette.map, zsh/registries/palette.json, 4× <scope>/keyboard.zsh)
     + MODIFIED (ai/base.zsh, ai/keyboard.zsh, ai/keys.zsh, help-touched engines).
     Nothing unexpected outside zsh/.
2. `bash deploy.sh`
   - expected: applies cleanly; .bak files for covered modified files.

>MAJKEE report: dry-run surprises? deploy errors?

## Group 2 — cold shell + help surface

3. Open a NEW terminal (fresh interactive zsh).
   - expected: no startup errors/noise from P11/P17 wiring.
4. `palette-help`
   - expected: help panel — command-palette · palette-refresh · Alt-k · map path ·
     auto-regen note · generator pointer.
5. `archx-help`, `piql-help`, `sync-help`, `projects-help`
   - expected: each prints its scope panel (new WP4 heredocs).

>MAJKEE report: any missing/ugly panel?

## Group 3 — the TUI (the real test)

6. Press **Alt-k**
   - expected: two-pane TUI — left scope tree (ai · system · projects · piql ·
     sync · archx · root, with counts, ~145 total), right help pane.
7. Arrows: ↓↑ move · → expands a scope · ← collapses. Help pane follows cursor
   (command / one-liner / engine / scope).
8. Type `mail` — tree flattens to matches; Backspace edits; **Esc once** clears
   filter (back to tree), **Esc again** cancels (prompt unchanged, nothing inserted).
9. Alt-k again → navigate to any command → **Enter**
   - expected: TUI closes, command text sits AT YOUR CURSOR on the prompt line —
     not executed. Edit/Enter as normal.
10. Narrow the terminal below ~60 cols, Alt-k
    - expected: degrades (help pane hides/stacks), no crash. KEY_RESIZE mid-open ok.

>MAJKEE report: feel of tree · filter · insert-at-cursor · anything janky?

## Group 4 — composer self-revealing loop

11. `palette-refresh`
    - expected: one line `palette: 145 commands` (±).
12. `touch ~/.config/zsh/ai/claude.zsh` then **Alt-k**
    - expected: imperceptible pause (auto-regen ~0.2s), palette opens normally —
      map mtime now newer than the touched file.
13. `python3 ~/.config/zsh/ai/palette-map-gen.py --root ~/.config/zsh --check; echo "exit=$?"`
    - expected: findings [1]-[4] zero · [5] nablarva excluded · [6] none · exit=0.

>MAJKEE report: staleness pause acceptable? check output clean on the LIVE tree?

## Verdict → prediction mapping

| # | prediction | verdict (ok / issue) |
|---|---|---|
| P1 | deploys with zero collateral outside zsh/ | ok |
| P2 | fresh shell loads clean, all help panels render | ok |
| P3 | TUI: tree+filter+insert-at-cursor work as designed | ok |
| P4 | self-revealing loop closes (touch → auto-regen → visible) | ok |

Overall: **PASS** → commit + push + deploy other machine · FAIL → report to Flight, kraken reiterates.
