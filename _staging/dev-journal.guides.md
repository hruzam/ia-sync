---
title: dev-journal.guides — guides-unification thread (drop-place + running log)
scope: _staging
audience: agent + operator
machine: office (authored) · both (via git)
verified: 2026-08-20
---

# dev-journal.guides — guides-unification thread (drop-place + running log)

`session: REP.Offc.Atlas-fable.guides · opened 2026-08-20 · seat: atlas-ui (Fable) · operator: majkee`
`pattern precedent: dev-journal.sella.md (this folder) — journal here, ONE pointer line in pulse.atlas.md`
`deploy-inert by construction (_staging/ is outside every deploy.sh leg). Git-tracked from birth.`

---

## HANDOFF BLOCK (next incarnation reads THIS first)

**State [2026-08-20]:** P0 GAVELED = **B′** (majkee: "go by B, fair option"). P1 + P1b
DELIVERED same session. **Resume = first unticked box below (P3′ — the move).**
Standing blessing granted same gavel: **every emitted document carries YAML frontmatter**
(token sparing, overview) — dogfooded on this journal, the skill, the manual.

**The lock (P0 → B′):** `raw.guides/` = SINGLE guide surface. Invariant:
**executable/deployed = surgical table · knowledge/readable = temple.** Machine guides
move home to `raw.guides/machine/`; zsh `guides/` → pointer stub + config artifacts;
`guide-publishing.md` project-publish convention survives unchanged. Hard dependency
accepted by operator: reposoma commit hygiene is now load-bearing for guides (no deploy
net).

---

## PLAN OF RECORD

- [x] **P0 — Directionality GAVELED → B′** (majkee, 2026-08-20). Route: @mirror
      position-aware audit (REVISE — staleness coupling) → operator movement (substrate
      colocation + pre-RAG argument) → atlas concession A′→B′ → gavel. First live fire of
      @mirror seat: SUCCESS, contract honored.
- [x] **P1 — `/guide` skill DELIVERED** → table `~/ia-sync/claude/skills/guide/SKILL.md`.
      Bare = derived overview (Glob + one frontmatter Grep, no hand-index) · `<name>` =
      verbatim read (fuzzy basename) · `<scope>` = folder listing. Staleness organ
      (half-life warn + mirror-banner note). 3-line writer law + pointer to manual.
      **⚠ NOT LIVE until `deploy.sh`** (skill must reach `~/.claude/skills/` on both boxes).
- [x] **P1b — `raw.guides/guide-writing.md` DELIVERED** (authored directly in reposoma —
      its rightful home under B′). The full treatment manual: law, scope-folder table,
      frontmatter shape (incl. the emitted-document blessing), 5 writer rules (migrated
      from zsh index convention + new rule 4 "trust disk over doc"), project-agent
      treatment section. Needs reposoma commit.
- [x] **P3′ — THE MOVE: WRITES DONE 2026-08-20** (taxonomy = skill-model slugs, see
      findings entry). 10 files → 9 slugs (services + resource-control = machine-home
      chapters); remote-control rewritten (P2b); CLASS 2 five stay table-side (atlas lean,
      majkee silent — reversible). **残 REMOVALS pending:** @Delta list in findings entry,
      dispatch ONLY after majkee commits reposoma. Original plan text below (superseded
      where it conflicts with the taxonomy gavel):
      zsh guides →
      `raw.guides/machine/`. Per file: add/normalize YAML frontmatter (P2 folded in) →
      Write new home → @Delta git-journaled removal from `ia-sync/zsh/guides/` + live tree
      (deploy ordering!). Candidates (from live tree, 17 files): home.md · office.md ·
      services.md · resource-control.md · remote.md · keyboard.md · claviature.global.
      spec.md · toolbox.tree-converter.md · guide-for-user.md · guide-for-builder.md ·
      guide-temple-mail.md · guide-harness-check.md · guide-regime-session.md ·
      codex-relay.contract.md · codex-relay.metadata-scripting.2026-07-31.md · index.md
      (→ becomes the stub, not moved) · sudoers.valet-php.conf (config artifact — STAYS).
      ⚠ judgment per file: codex-relay.contract.md is load-bearing for agent seats
      (astrobley/vega/mirror point at it) — verify pointers before moving; some guides may
      be `.zsh`-engine-adjacent enough to argue they're "executable-coupled" — adjudicate
      each, don't bulk-move.
- [x] **P2b — DONE 2026-08-20** (`remote-control/GUIDE.md` rewritten against rc.sh truth,
      single-seat law + `--continue` fork trap captured). Original text:
      remote.md content rewrite DURING its move (drift fix): guide teaches tmux;
      engine `ai/rc.sh` (2026-08-15 redesign) is TMUX-FREE (Mode A bare server / Mode B
      `script -qfc` pty, both `setsid nohup`). Rewrite to disk truth; rc.sh itself verified
      table==live byte-identical (deploy clean).
- [x] **P4a — STUB AUTHORED on table 2026-08-20** (`ia-sync/zsh/guides/index.md`
      rewritten: pointer to raw.guides + /guide, stays-here table for CLASS 2 + configs).
      Deploy-inert until majkee's deploy — ordering safe.
- [ ] **P4b — residual guards:** one discipline line in ia-sync README ("surgical
      knowledge → raw.guides, not here") · deploy.sh zsh/guides leg reviewed (stub +
      configs + CLASS 2 only) · verify stub live on both boxes after deploy.
- [x] **HOME MIRROR PASS — DONE 2026-08-20** (executed cross-host by office @Delta under
      the operator voice directive, superseding the local-seat plan below). ia-sync
      commit `329ece4` pushed · reposoma `93e542f` pushed · office deploy OK (SKILL-LIVE
      + stub verified) · home ff-pulls + deploy (MACHINE_NAME=home) OK · 10 lingerers
      removed · stub + HOME-SKILL verified. **🔫 SMOKING GUN FOUND: `ai.md` on home live
      guides/** — the guide RETIRED 2026-07-11 (index: "§1 → guide-harness-check, hygiene
      → guide-for-user"), squatting on home ever since because deploy never deletes =
      majkee's rogue-file theory CONFIRMED with a 40-day specimen. LEFT IN PLACE as
      evidence (report-only rule). Disposition = majkee's word (lean: rm — it's the
      retired corpse, content lives on in its successors). Feeds P5 as evidence #1.
      Home final state: 7 protected + ai.md. Original local-seat plan (superseded):
      1. `git -C ~/reposoma pull` && `git -C ~/ia-sync pull` && `bash ~/ia-sync/deploy.sh`
         (slugs + stub + /guide skill arrive; deploy copies, never deletes)
      2. Remove the 10 deployed lingerers from live `~/.config/zsh/guides/`:
         `cd ~/.config/zsh/guides && rm -v home.md office.md services.md \
          resource-control.md remote.md guide-for-user.md guide-temple-mail.md \
          guide-harness-check.md guide-regime-session.md toolbox.tree-converter.md`
         (recovery archive = ia-sync git history; verified on office pass)
      3. DO NOT touch: index.md (stub) · sudoers.valet-php.conf · keyboard.md ·
         claviature.global.spec.md · guide-for-builder.md · codex-relay.contract.md ·
         codex-relay.metadata-scripting.2026-07-31.md
      4. Verify: `ls ~/.config/zsh/guides/` → exactly the 7 protected files;
         head of index.md shows the pointer-stub frontmatter; tick this box + note here.
- [ ] **P5 — PARKED: guide-drift audit** (eagle/Kraken pass — doc↔code drift detection,
      the P2b bug class; overlaps `harness-stale`). Separate session. This line exists so
      it cannot orphan.
- [x] **CLOSING STEPS — DONE 2026-08-20** (agent-executed under operator voice directive):
      ia-sync `329ece4` + reposoma `93e542f` committed+pushed · deployed office + home ·
      `/guide` skill LIVE on both boxes (active next sessions) · stub live both boxes.
      Both machines converged on the guides layer.

---

## FINDINGS LOG (newest on top)

### [2026-08-20] OPERATOR DIRECTIVE (voice, mobile): full agent-side close-out, BOTH hosts
majkee, live via voice (mobile, ~1h away from desk): Krakens execute EVERYTHING —
ia-sync commit+push+deploy (office), reposoma commit+push, then **cross-host ssh to home**
for pull+deploy+lingerer-cleanup. This is an **explicit operator-authorized exception**
to the 2026-08-01 no-cross-host-ssh curb (his call, his authority, this scope only —
not a precedent). Also his diagnosis on record: deploy copies/overwrites only; extras
beyond repo scope squat in place → the lingerer/rogue-file class (he suspects a past
rogue traced to home lagging). Home extras beyond the expected 7 will be REPORTED, not
deleted (evidence, not litter, until he looks). Wider zsh-layer lingerer audit = P5-adjacent,
stays parked.

### [2026-08-20] DELTA REMOVAL PASS — PASS (office). Live tree was ALREADY clean.
Gate PASSED: reposoma commit `a6a2f38` ("recanonization guides as cc skill design for
future rag approach") carries all 9 slugs, porcelain clean. Executed: 10× `git rm`
STAGED in ia-sync (protect-7 untouched) · loose `raw.guides/guide-writing.md` STAGED rm
in reposoma · recovery verified (all 10 present in ia-sync git history).
**SURPRISE:** live `~/.config/zsh/guides/` held 0 of the 10 — already removed before
Delta ran (operator's own hand, presumably — "I did my part"; ia-sync shows NO operator
commit, so it wasn't a deploy effect). Office live = clean; nothing skipped-unsafe.
**ia-sync working state for majkee's commit (git add -A covers all):** 10× D staged ·
` M index.md` (stub, unstaged) · `?? claude/skills/guide/` (the skill, untracked) ·
`?? _staging/dev-journal.guides.md` (this journal, untracked) · plus a pre-existing
staged `M devices/_shared/agentive-tmux.md` (NOT ours — rides his commit, flagged).
**reposoma:** single staged `D raw.guides/guide-writing.md` awaiting his next commit.
**Home live tree still holds the 10 deployed copies** → HOME MIRROR PASS box stands.

### [2026-08-20] MANIFEST LAW canonized (majkee asked pre-cleanup; atlas drafted + applied)
Side-document handling for slug folders, locked before the Delta cleanup so the
protect-list is law, not judgment: **four classes** — GUIDE.md (canonical entry + THE
MANIFEST) · chapter (`chapter-of:` frontmatter) · attachment (non-md, manifest entry =
only registration) · legacy (manifest-marked "superseded, do not follow", OR deleted —
git history is the archive; kept in place only when it IS the origin record).
**Orphan rule:** sibling not named in GUIDE.md `## Manifest` = drift → flag, never
silently adopt. Slug with only GUIDE.md needs no manifest.
**Applied:** guide-writing/GUIDE.md §Side documents (the law) · /guide skill (orphan
flag organ + never-read-attachments rule) · remote-control/GUIDE.md manifest (3 legacy
files marked in place — they're the origin record of the pty/glyph findings) ·
machine-home/GUIDE.md manifest (2 chapters). **Cleanup consequence:** Delta's protect
rule = anything manifest-registered stays; remote-control legacy trio PROTECTED.

### [2026-08-20] TAXONOMY GAVELED (skill-model) + P3′ EXECUTED — all writes landed
**majkee taxonomy ruling:** folder-per-guide 1:1 with the skill model —
`raw.guides/<slug>/GUIDE.md` (fixed entry filename = hardcoded-resolver contract,
RAG-ready chunk shape) + **chapter lifehack** (chapter files inside the slug = fine
taxonomy slices) + **anti-hell guard** (slugs topic-specific, never generic buckets —
"15 broad folders of unrelated chapters" is the named failure mode).
**CLASS 2 (unruled → atlas lean applied, reversible):** engine-authoring docs STAY
table-side — keyboard.md · claviature.global.spec.md · guide-for-builder.md ·
codex-relay.contract.md · codex-relay.metadata-scripting. Rationale: they govern
*modifying the executable layer*, read at the table with the code (writer rule 4).

**WRITTEN (new homes, frontmatter on, surgical-table banners stripped, pointers fixed):**
- `guide-writing/GUIDE.md` — manual UPDATED to skill-model (supersedes loose
  `raw.guides/guide-writing.md` from earlier today → REMOVE the loose one)
- `remote-control/GUIDE.md` — **REWRITTEN (P2b done)**: tmux-free engine truth, Mode A/B,
  single-seat law, the `--continue` fork trap. NB: slug already held legacy files
  (spawn-rc.sh · spawn-rc-term.sh · remote-control-spawn.md) — historical, left in place,
  GUIDE.md is the entry.
- `machine-office/GUIDE.md` · `machine-home/GUIDE.md` (STALE banner preserved — moved,
  not laundered) + chapters `machine-home/services.md` · `machine-home/resource-control.md`
  (the chapter lifehack, dogfooded)
- `gemini-seats/GUIDE.md` (stale-note frontmatter: vega/astro rows = pre-Codex-shift
  history) · `temple-mail/GUIDE.md` · `harness-check/GUIDE.md` · `tree-snapshot/GUIDE.md`
  · `regime-session/GUIDE.md`
- `/guide` skill REWRITTEN on table for slug/chapter resolution + naming guard.

**@DELTA REMOVAL LIST (dispatch AFTER majkee commits reposoma — harvest-before-remove):**
1. `git rm` from `~/ia-sync/zsh/guides/`: home.md · office.md · services.md ·
   resource-control.md · remote.md · guide-for-user.md · guide-temple-mail.md ·
   guide-harness-check.md · guide-regime-session.md · toolbox.tree-converter.md (10)
2. delete same 10 from live `~/.config/zsh/guides/` on THIS box (deploy.sh copies, never
   deletes — live needs explicit rm; home box mirrors after its pull+deploy)
3. `git rm` loose `~/reposoma/raw.guides/guide-writing.md` (superseded by slug)
4. KEEP table+live: index.md (→ P4 stub) · sudoers.valet-php.conf · the 5 CLASS 2 files

### [2026-08-20] P0 converged → B′ gavel candidate (operator movement + atlas concession)
majkee worked the fork live ("mental paralysis → I can live with reposoma"): the mirror-
model's discipline cost (3 coupled ops) IS the @mirror finding; one maintained source
kills it. His load-bearing arguments: (1) substrate colocation — pre-guide substrates
(raw.research etc.) already live in reposoma; guide lifecycle = research→synthesis→guide,
one repo; (2) reposoma = the pre-RAG corpus — guides elsewhere are RAG-invisible.
**Atlas conceded — lean updated A′→B′.** Reframed invariant that dissolves the table-
doctrine conflict: **executable/deployed = surgical table · knowledge/readable = temple.**
Guides don't execute; they were in zsh/ by adjacency accident. B′ answers the Codex
REVISE better than A′: no sync leg for machine guides = staleness structurally deleted
(reposoma is cloned+pulled on both boxes; `machine:` tag survives).

**B′ shape (gavel candidate):**
- `raw.guides/` = SINGLE read surface (skill's one target). Machine guides MOVE home →
  `raw.guides/machine/` (new scope folder), direct-edit, no banner.
- `guide-publishing.md` project→reposoma publish convention SURVIVES unchanged (piql etc.
  keep authoring in-project, one-way publish + banner). B′ changes only zsh guides'
  citizenship.
- zsh `guides/` → pointer stub + deployable config artifacts only.
- Discipline guards ×3: stub redirect · skill carries the 3-line writer law · one ia-sync
  README line ("surgical knowledge → raw.guides, not here").
- **Skill split (majkee's "manual for project agents" — point-never-copy):** skill stays
  THIN (read paths + 3-line writer law + pointer); the full treatment manual = a guide
  itself, `raw.guides/guide-writing.md`, read THROUGH the skill (dogfood).
- P3 changes meaning under B′: no new sync leg — instead a one-time MOVE (zsh guides →
  raw.guides/machine/, git-journaled) + deploy.sh zsh/guides leg shrinks to stub.

### [2026-08-20] P0 challenge landed — @mirror (Codex/Kontsevich) verdict: REVISE
First live fire of the @mirror seat (built 2026-07-31) — relay worked, contract honored
(weakest assumption · verdict · risk · alternative). Audit summary:
- **Weakest assumption of position A:** machine-layer guides do NOT fit the project-guide
  mirror model's velocity profile. Project guides = author-once, publish-occasionally,
  stale-okay. Machine guides (home.md/office.md/services/reach) = change with machine
  config, must be current-on-read. "One more leg, no new invariants" is brittle because it
  couples THREE uncoordinated operations — `deploy.sh` (copy) · `sync-guides` (publish) ·
  `git commit` (lock) — with nothing forcing them to stay together. Tool is occasional-
  publish, not transactional.
- **Verdict: REVISE** — approach doesn't fail, but staleness risk is UNMITIGATED. Lock only
  with a freshness mechanism: (i) `sync-guides` as a post-copy hook INSIDE `deploy.sh`
  (publish atomic with deploy) · (ii) push-triggered sync · (iii) `/guide` skill pre-read
  staleness warning. "A mirror nobody is contractually keeping fresh is worse than no mirror."
- **Primary risk:** silent guidance divergence — guide edited+deployed on office,
  sync-guides not run, home reads stale mirror, hours lost debugging wrong policy;
  compounds over months.
- **Alternative offered:** git submodule — mount `ia-sync/zsh/guides/` inside `raw.guides/`
  pinned to a commit; transactional freshness, no sync tool.

**Atlas fold (draft, majkee gavels):** ACCEPT the REVISE — mitigation = (i) + (iii)
combined: `sync-guides` call appended as `deploy.sh` post-copy step (one line; deploy and
publish become one act) + `/guide` skill compares mirror banner date vs a cheap freshness
signal and warns. **REJECT the submodule alternative:** contradicts the temple's
simplicity bias (global CLAUDE.md: no automation layers before maintenance pain),
couples reposoma's history to ia-sync (every clone/pull grows a `submodule update` step
for ALL seats including phone/RC sessions), kills the banner mechanism, and reposoma
must stay a flat greppable surface for every agent seat. The hook gives ~the same
freshness guarantee for one line of shell. → P3 shape updated below.

### [2026-08-20] session open — existence checks + the drift find
- **Existence check fired twice:** (1) `raw.guides/guide-publishing.md` already IS a
  gaveled guides→reposoma convention (one-way publish, `sync-guides` zsh tool +
  `registries/config.sync.json`, banner, categories `reach/` · `<project>/` · top-level).
  (2) zsh `guides/index.md` already carries a scope registry (audience/machine/scope/
  verified per guide) + writer convention (5 rules). → This thread is COLLAPSE/EXTEND,
  not greenfield. Only true gap = `/guide` skill.
- **rc.sh deploy state CLEAN:** `~/ia-sync/zsh/ai/rc.sh` == `~/.config/zsh/ai/rc.sh`
  byte-identical (180 lines). No table drift.
- **remote.md is the dirt:** doc↔code drift (guide says tmux; engine is tmux-free since
  2026-08-15 redesign — same day the guide was "verified", the card was refreshed against
  the OLD engine or vice versa). → P2b.
- **Operator context that seeded this:** `tso → claude --continue` on home forked a copy
  of an office session; phone `/remote-control` grabbed the single RC seat → home fork
  orphaned ("remote here lost"). Diagnosis: `--continue` = rehydrated fork, never the live
  session; RC bridge = single-seat, last claimer wins. Rule adopted in-chat: never
  `--continue` for remote access; pin the device = Approach A (systemd always-on RC).
  majkee killed the home fork same session.
- **majkee steers:** guides copied/homed to reposoma · `/guide <name>` skill, scope from
  frontmatter ("fast sip") · one guide per scope folder · zsh layer = shadows or big-audit
  only · Fable seat for breadth (done — `/model fable`) · challenger = @mirror first,
  @Janus fallback ("advisor-advanced not needed now").
- **Journal placement ruled (majkee accepted):** here in `_staging/`, temple flag/pulse
  stay thin — pulse.atlas gets ONE ledger line pointing here.

---

## DECISIONS PENDING (majkee gavels; atlas never locks)
1. **P0 directionality** — A (mirror-model) vs B (reposoma-as-home). Challenger verdict
   pending.
2. **TOML→YAML** — atlas pushback stands unless majkee overrules at P2.
3. **Symlinks→pointer-stub** — atlas pushback (deploy.sh is copy-based; symlinks fragile
   in git) stands unless overruled at P4.
