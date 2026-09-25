# RUNBOOK: germline-00-home

```yaml
goal: >
  ~/reposoma/.germline/ is the canonical, git-tracked, vendor-blind home (agents/ · skills/),
  reachable at ~/.germline on office; both chatbot-port twins write there; the pilot port lives
  there; the two working homes (.shared/, raw.shared-skills/) are gone.
gate: >
  After commit + deploy, a fresh Claude session and a fresh Codex session each resolve
  buffering-cycle from ~/reposoma/.germline/skills/ via chatbot-port (update-ask path answered
  no; --check reports equal), with ~/.germline resolving on office and .shared/ +
  raw.shared-skills/ absent from reposoma - three receipts recorded in STATUS.
participant_1: [atlas-ui, {brand: claude, model: fable, effort: high}, host: office, role: planning head (atlas-as-houston, provisional gavel 2026-09-25) + Claude-side author]
participant_2: [majkee, {brand: human, model: none, effort: none}, host: office, role: operator - rm, symlink, commit, deploy, fresh-session proofs, chatbot hand-drop]
participant_3: [cartan, {brand: codex, model: gpt-5.6-sol, effort: xhigh}, host: office, instrument: resident, role: Codex twin owner - source sync done 2026-09-25; Codex fresh-session proof]
status_owner: atlas-ui
```

## Why this session exists

One gate, three repos (reposoma · ia-sync · live homes), an operator-only leg (rm · ln · commit ·
deploy) and cross-vendor proof. The design is gaveled (2026-09-25, name `.germline`); this session
only makes the home exist and proves both twins read it. Not a one-sentence diff: three seats, two
runtimes, one destructive step.

## Fixed facts

- Scope rule: `<scope-root>/.germline/` is the source. Global root = `~/reposoma`; `~/.germline`
  is a host-local **symlink**, never a deploy target or a `deploy.sh` leg. Project scope =
  `<project-root>/.germline/`, same structure, inside the project's own repo.
- Object rule: source (`identity.md`, `skill.<slug>.md`) → reposoma; rendering (Claude `.md`, Codex
  `.toml`, `SKILL.md`) → ia-sync table → `deploy.sh` → live. Reposoma never depends on ia-sync.
- `.germline/skills/skill.<slug>.md` are flat chatbot files, NOT native Codex skill folders; no
  runtime root registers `.germline` (Cartan RETURN 2026-09-25).
- Codex twin `/home/hruzam/ia-sync/codex/skills/chatbot-port/SKILL.md` already writes to
  `.germline/skills/` and implements `twin-commit:` — uncommitted at HEAD `1de7f27`.
- Claude twin `/home/hruzam/ia-sync/claude/skills/chatbot-port/SKILL.md` still names
  `.shared/skills` (committed in `1de7f27`) - prompt-0 fixes it.
- Pilot port exists twice, byte-identical, both untracked:
  `/home/hruzam/reposoma/.shared/skills/skill.buffering-cycle.md` and
  `/home/hruzam/reposoma/raw.shared-skills/skill.buffering-cycle.md` (`source-commit: 8da748a`).
- `.germline/agents/` stays EMPTY here; the Atlas identity pilot fills it in its own bed.
- Print mode `-p` is never used - every proof is an interactive session.

## prompt-0 — atlas-ui (this seat; Write/Edit only, no shell mutation)

```text
Bed: /home/hruzam/ia-sync/.dev/session/germline-00-home/ - read RUNBOOK.md, then STATUS.md.
Do, in order, then rewrite STATUS:
1. Write /home/hruzam/reposoma/.germline/README.md - the rule only (<= 12 lines): source vs
   stamped one-way rendering; never edit a rendering; global/project scope; agents/ + skills/
   layout; NO index of skills (parked: germline-as-bus).
2. Write /home/hruzam/reposoma/.germline/skills/skill.buffering-cycle.md byte-identical to
   /home/hruzam/reposoma/.shared/skills/skill.buffering-cycle.md.
3. Edit /home/hruzam/ia-sync/claude/skills/chatbot-port/SKILL.md: every `.shared/skills` ->
   `.germline/skills` (description, Constants, What-I-do-not-do).
4. Edit /home/hruzam/ia-sync/.dev/session/invariance-autonomy/raw/master-brief.2026-09-23.md:
   line 72 `reposoma/.shared/agents/<slug>/` -> `reposoma/.germline/agents/<slug>/`; any
   `.shared/skills` -> `.germline/skills`. Cartan's counter-sign block untouched.
5. Edit /home/hruzam/reposoma/pulse.atlas.md: `.shared/skills` -> `.germline/skills`.
6. Edit /home/hruzam/ia-sync/AGENTS.md - one line under "Machine facts (stable)" or a new
   2-line section: `~/.germline` -> symlink to `~/reposoma/.germline` (canonical source, both
   hosts); never a deploy target.
Executor: this seat, in-window (surgical edits; no kraken, no spawn).
Done-when: `grep -rn '\.shared' <the five files>` returns nothing; STATUS rewritten with
in_flight none and next = prompt-1.
```

## prompt-1 — majkee (operator shell, office)

```text
rm -r /home/hruzam/reposoma/.shared /home/hruzam/reposoma/raw.shared-skills
ln -s /home/hruzam/reposoma/.germline /home/hruzam/.germline
cd /home/hruzam/reposoma && git add .germline pulse.atlas.md && git commit -m "germline-00-home: canonical shared home + pilot port" && git push
cd /home/hruzam/ia-sync && git add claude/skills/chatbot-port codex/skills/chatbot-port .dev/session/germline-00-home .dev/session/invariance-autonomy/raw/master-brief.2026-09-23.md pulse.md AGENTS.md && git commit -m "germline-00-home: twins -> .germline, bed, router" && git push
bash /home/hruzam/ia-sync/deploy.sh
```
Commit ONLY those paths - ia-sync carries other seats' dirty work (cartan-muticula bed,
presence-freshness deletions, rellays files, journal). Then one journal line in
`/home/hruzam/ia-sync/journal.host-cleanup.md`: symlink created on office; home does
`git -C ~/reposoma pull && ln -s ~/reposoma/.germline ~/.germline` on its next session.
Tell atlas-ui when done - it rewrites STATUS.

## prompt-2 — proofs (majkee opens both; never -p)

```text
Fresh Claude session (any cwd):  /chatbot-port buffering-cycle
  expect: "skill.buffering-cycle.md exists - update only?"  -> answer: no
  then:  /chatbot-port --check   expect: silent (equal @8da748a)
Fresh Codex session (cd ~/ia-sync && codex, Cartan seat):  $chatbot-port buffering-cycle -> no
  then:  $chatbot-port --check   expect: equal / silent
Symlink: ls -l /home/hruzam/.germline ; ls /home/hruzam/reposoma/.shared /home/hruzam/reposoma/raw.shared-skills  (expect: link shown; both dirs absent)
Paste the three receipts to atlas-ui -> STATUS rewritten, gate closed.
```

## Known constraints + destructive holds

- `rm -r` is limited to the two named untracked dirs; nothing else in reposoma is deleted.
- `pulse.md` is a shared router with a live neighbour (`cartan-muticula`, runbook-upgrade-02-app):
  this session adds exactly one line and never edits other rows.
- `_staging/codex/` is Cartan's turf - pointed, never edited.
- No `sync.sh` before `deploy.sh` (it would overwrite the table with stale live copies).
- No README index in `.germline/skills/`; no `.germline/agents/*` content; no ptyra migration.
- Print mode `-p`: never (operator law, Sella Walk A.7; re-gaveled 2026-09-23).

## Acceptance evidence

- `git -C /home/hruzam/reposoma ls-files .germline` lists README.md + skills/skill.buffering-cycle.md.
- `readlink /home/hruzam/.germline` = `/home/hruzam/reposoma/.germline`.
- Claude receipt + Codex receipt from prompt-2, verbatim in STATUS `checkpoint:`.
- Optional receipt (not gate): majkee hand-drops `skill.buffering-cycle.md` into one chatbot project
  and it names the five phases back correctly - recorded in STATUS when it happens.

## References

- `/home/hruzam/ia-sync/.dev/session/invariance-autonomy/raw/master-brief.2026-09-23.md` - the design, tree, Cartan's REVISE (subject Atlas)
- `/home/hruzam/ia-sync/_staging/codex/germline-home.return.2026-09-25.md` - Cartan's RETURN: Codex twin synced; which Codex consumers may read germline
- `/home/hruzam/reposoma/raw.vendor-neutral-agents/ptyra/README.md` - the source/rendering precedent the README rule points to
- `/home/hruzam/ia-sync/HANDSHAKE.md` - meeting shapes, delivery rule, mounts
- `/home/hruzam/reposoma/raw.guides/runbook/GUIDE.md` · `status/GUIDE.md` - the law this bed obeys

## What this session deliberately does not do

- The Atlas identity pilot (`.germline/agents/atlas/identity.md`, renderer, measurement) - own bed.
- Any `deploy.sh` leg or ensure-step for the symlink - manual until it ever drifts.
- `.germline` discovery index / connector bus - parked, own session.
- Houston <-> Cartan collision, `scope:` word, `buffering` near-miss ruling - pilot session.
- Home box - journal note only; no cross-host action from here.
- Migration of `raw.vendor-neutral-agents/ptyra/` or the per-vendor chatbot agent folders.
