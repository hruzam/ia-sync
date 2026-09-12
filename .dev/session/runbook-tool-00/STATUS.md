# STATUS — runbook-tool-00

```yaml
status_owner: @Trajectory
last_updated: 2026-09-06
phase:        d-done
next:         "HOLD on res/examples.md (majkee 2026-09-10 — wait for possible further requirements, then write once). @majkee: git ops (3 repos) + home pull/deploy + rb-selftest there (owed home evidence). Bed closure on majkee's call after that."
```

> **Bed-location (updated 2026-09-09):** MOVED to `~/ia-sync/.dev/session/runbook-tool-00/`
> by majkee's explicit ask (supersedes the 09-06 hold-until-close note) — sits beside
> `runbook-upgrade` for function comparison. Stub with pointer left at the old nablarva
> path (bus receipts cite it; receipts are never edited). Rewired same sitting: board
> record detached+reattached (immutable-record law; new id e305125c…), RB_ROOT bench
> repointed to `~/ia-sync/.dev/session` in BOTH configs, deployed on office.

## Where we are

v0.1 verified by @majkee 2026-09-05 ("checked, nice work") — tool lives on both machines.
v0.2 built same day on four majkee requests: buffer pane · group fold/jump · colors ·
internal reader. Deployed on office; home needs git pull + deploy (majkee runs git himself).

## What is finished

- [x] RUNBOOK.md written
- [x] nablarva session dir created: `.dev/session/runbook-tool-00/`
- [x] @Oraculum design audit — `_bus/oraculum.audit.2026-09-04.md`
- [x] RUNBOOK revised — 9 adjustments, `bus/`→`_bus/`, source layout, D1/D2 design
- [x] runbook.py (Python TUI) — 2026-09-04
- [x] extend nablarva/ scope (runbook.zsh + keyboard.zsh P5 + base.zsh P3) — 2026-09-04
- [x] deploy.sh run — all 5 nablarva/ files confirmed in ~/.config/zsh/nablarva/ — 2026-09-04
- [x] fresh-session verify — majkee confirmed on home 2026-09-05
- [x] v0.1 gate — majkee accepted 2026-09-05
- [x] v0.2 built + deployed on office — 2026-09-05:
      - `b` buffer pane — `p` collects paths, pane shows them, all print to scroll-back at quit
      - group model — section headers are fold nodes: `J`/`K` jump groups, `Enter`/space folds
      - colors — gate states, section headers, file-type tint (json/yaml/zsh-sh-py/kdl),
        markdown heading/checkbox/fence/yaml-key emphasis in bodies
      - internal reader — `Enter` on any file: WRITELN scroll view (PgUp/PgDn g/G), `e` to editor
- [x] RESCOPED to `zsh/session/` umbrella — majkee gavel 2026-09-06 ("nablarva can be
      a different animal"). New scope: base.zsh + keyboard.zsh + runbook.{zsh,py};
      nablarva/ de-wired (verified isolated); tool is project-agnostic — proven by
      browsing ia-sync's own .dev/session/ (9 beds incl. [!] in-flight). Default
      bench = $RB_ROOT export in both config.*.zsh. cs-cards + dashboard = reserved
      partitions (cs fold-in needs temple gate on ai/base.zsh).
- [x] @Epoch presence-board research — `raw/research.presence-board.byEpoch.2026-09-06.md`
      Verdict: real gap, no existing convention; embed ISO timestamp (don't trust mtime
      over git); staleness renders, never acts (no steal-on-stale — advisory must not
      become a soft lock). Dashboard design waits on majkee read.
- [x] Peer thread opened with cartan-csharp (runbook-upgrade bed) — majkee gavel
      2026-09-06. POINT 21 → Cartan RETURN 21 (case lock accepted; presence-board
      law = one `runbook/res/presence-board.md` leaf, his side; two of my claims
      corrected: closing law already exists in GUIDE "On gate closure" — `_closed/`
      withdrawn; both-machine claim was forward-dated) → my REVIEW 22 (consumption
      stamp + identity proposal + client schema needs). Board clients FROZEN until
      Cartan's exact-format draft + majkee gavel.
- [ ] v0.2 + rescope verify on home (pull + deploy there; live-tree orphans already
      cleaned via SSH — only base/keyboard overwrite pending)
- [x] Presence-board contract GAVELED — majkee 2026-09-09, reposoma commit 0f48dce
      (`raw.guides/runbook/res/presence-board.md`, Manifest-registered). My RETURN 25
      verdict: USABLE AS-IS; both optional suggestions declined by law side — binding
      to canon unchanged per RETURN 25 §5. Canon-vs-reviewed diff verified: one line
      (DRAFT banner → GAVELED banner), content pin 0bcd6c40… matches VERDICT 28.
      CAVEAT (VERDICT 28 curvature 1): local reposoma commit only — no push; home
      does NOT have the law yet; home carry needs its own evidence.
- [x] BOARD CLIENT built + deployed (office) — 2026-09-09, order flip gaveled.
      Grammar once in runbook.py (composer + strict parser incl. calendar check);
      CLI `runbook.py board list|mark|unmark`; zsh organ P3 (board.zsh engine,
      rb-mark/rb-unmark/rb-board); TUI: B modal, D1 ● marker, m/u keys, tick
      refresh. Ownership law enforced (own-state ~/.local/state/session-board/,
      machine-local; foreign unmark rejected — tested). Board home
      ~/reposoma/_active/ created; FIRST REAL RECORD = this session attached to
      this bed (presence.8e2e0a78….md). Advisory boundary held: render-only
      staleness, no auto-delete, no liveness inference.
      Guide placement Q answered: guide-session.md stays in zsh/guides/ (doctrine
      §4.7 — no machine paths into canon; precedent: temple-mail-manage, cs-palette).
- [x] A+B gaveled sequence done — 2026-09-09 (Cartan consultation folded, non-authoritative):
      A: next: block scalars (>-,|) resolved; in_flight strict-but-truthful (raw value
      in warn strip); unknown-not-healthy rule; GUI-editor detach fix (subl/code) with
      visible outcome; board modal WRITELN. Selftest `rb-selftest` (runbook.py
      selftest): sandboxed, 18/18 PASS — caught+fixed a real bug (mark now refuses
      contract-invalid records, e.g. bed outside ~).
      B: guide written — raw.guides/session-browser/GUIDE.md (temple, per B′ law
      2026-08-20; corrects my earlier zsh/guides/ placement answer — that layer is a
      pointer stub; majkee's reposoma instinct was right, own slug not runbook/res/).
      Reposoma commit = majkee's git ops.
- [x] C1 (v0.3 core) — 2026-09-10: TUI rewritten to tree + content pane. Left =
      one tree (beds → STATUS/_bus/RUNBOOK/files/raw, twigs, counts, ● marks);
      right = pure content (bed → cold-start overview incl. board attachments;
      file → doc; group → listing); strip (next:/in_flight) kept; narrow <60 cols
      = focused pane fullscreen; place memory (selection+expanded) host-local
      ui.json; y = copy path to clipboard (wl-copy/xclip, buffer fallback);
      modal reader retired (content pane supersedes). Selftest reshaped for tree
      model — 19/19 PASS, deployed office.
- [x] C1.5 mirror view — 2026-09-10 (majkee ask): `v` flips tree column left↔right
      (persisted in place memory) + `rb-open -R`. One code path, no fork.
- [x] C2 CS-card entrance — 2026-09-10: vault reader (card/=live, routines/=RT,
      archive/=AR), tolerant matcher (runbook:/root:/pointers:, ~-expanded,
      inside-bed test), per-bed `cs cards (N)` group, top-level ≋ vault node with
      derived landing arrows, Enter on card = land on its bed here / "missing
      here — elsewhere, not finished" when target is outside this root. Never
      archives, never launches. Selftest 26/26 incl. matcher; deployed office.
      Live proof: 38 real cards render; my own 09-05 card correctly shows NO
      landing (pointers pre-date the bed move — honest drift display).
- [x] C3 — 2026-09-10: board modal rewritten — row-cursor (arrows always move,
      selection visibly highlighted), records GROUPED BY WORKSPACE (display-only
      derived convergence view: "~/ia-sync — 2 sessions"), Enter on a valid
      local-host record lands on its bed in the tree; invalid records grouped
      at the end with reasons.
- [x] C4 — 2026-09-10: Y = copy exact file/card content to clipboard (relay
      prep — formatting preserved; copying claims nothing); y = path (from C1);
      P = buffer maintainer modal (majkee ask, same batch): row cursor, x
      removes a line, X clears, y copies a line; survivors print at quit.
- [x] C5 vault umbrellas + resume — 2026-09-10 (majkee asks): vault groups cards
      under project umbrellas (project: key preferred — 16 cards carry it; slug
      derived for the 22 older ones; display-only, no format change), umbrellas
      fold, newest-first by date: key or filename date. Card view shows resume:
      when present (11 cards); `R` copies it to clipboard for pasting into the
      target window — auto-seeding a NAMED window stays ovitmugen scope.
      Selftest 33/33; deployed office.
- [x] Closure-receipt proposal SETTLED: declined by cartan (POINT 34, 2026-09-10)
      — sound reasoning: existence-only receipt can't honestly claim "closure
      verified" (my own board contract validates contents and denies closure
      inference — precedent cuts against me); real contract cost understated.
      Client residue: glyphs stay observational (guide wording pinned); no ✓,
      no closure parser, finished-means-pruned stands. Reopenable on concrete
      need. Lesson logged: my bus turn number 32 collided with a concurrent
      Atlas cycle 32 — check the bus immediately before writing, not minutes
      before; concurrent writers are exactly the presence problem itself.
- [x] C6 pre-acceptance polish — 2026-09-10 (majkee asks): ● badge moved to fixed
      prefix slot before bed name (visible even when slug clips); pane divider
      movable `<`/`>` in 5% steps (20–80, persisted); `A A` = drain move — the
      canonical Cinderella lifecycle, consumed card → archive/, two-press
      confirm, routines refused by law, explicit-only (opening never archives).
      Boundary drawn: browser = read + land + drain; authoring/edit/restore
      stays cs-palette/temple-cs-manage — write-assign of pointers rejected
      (single-writer law on foreign cards; matcher derives instead).
      Selftest 37/37; deployed office.
- [x] C GATE CLOSED — majkee gavel 2026-09-10: acceptance test passed (Cartan's
      30s cold-recovery, fresh terminal).
- [x] D receipt navigation — 2026-09-10, display-only per POINT 34 rails:
      _bus/ content view groups receipts by cycle (newest first, kind+seat per
      file, unnumbered files surfaced not hidden); head-review aid states
      file-presence facts only ("return file present · no verdict file:
      cycle N") — never pass/fail, a filename is never a verdict. Live proof:
      runbook-upgrade's 95-file bus renders grouped; cycles 21/22/33 surfaced.
      Selftest 41/41; deployed office.
- [ ] res/examples.md — the idiot-walkthrough chapter for session-browser GUIDE
      (promised post-final; final is now)
- [ ] home carry: majkee git ops (3 repos) + home pull/deploy + rb-selftest
      there = the still-owed home evidence
- [ ] bed closure when majkee calls it: promote per GUIDE On gate closure →
      detach board record → prune
- [ ] D (later): receipt navigation, display-only
- [ ] home carry: reposoma push/pull (law + board record) + ia-sync pull/deploy —
      majkee's git ops; home evidence separate per VERDICT 28
- [ ] ovitmugen build opens after this closes
