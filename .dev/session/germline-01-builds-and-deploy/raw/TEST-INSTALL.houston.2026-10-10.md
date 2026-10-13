# TEST-INSTALL — Houston thin wrappers (final fold 2026-10-10, Janus-REVISE fix)

`for: majkee (manual install + test) · author: atlas(harness), oraculum rows "final fold" + "fix" · no deploy.sh, no commit`
`host: office (hruzam-120922) only until the commit/pull order in §5 has run`

## 0. Pre-checks (read-only) and journal

- **Journal:** the `## OFFICE — 2026-10-09` entry in `~/ia-sync/journal.host-cleanup.md` is reconciled to a
  *planned* install (source `~/ia-sync/codex/profiles/houston.config.toml`, status OPEN). Change it to
  "installed <date time>" only after the `cp` in §1 actually runs. Journal rules hold: newest first, one entry
  per host-day, merge same-day work.

```zsh
readlink -f ~/.germline                                             # → /home/hruzam/reposoma/.germline
ls ~/.germline/agents/houston/ ~/.germline/agents/houston/cards/    # identity · binding.claude · binding.codex · cards/{audit,consult,sitting}
ls /home/hruzam/unikuklatrix/nablarva/.germline/agents/houston/     # nablarva.md ONLY
ls /home/hruzam/unikuklatrix/nablarva/.claude/agents/houston.md /home/hruzam/unikuklatrix/nablarva/.codex/agents/houston.toml 2>&1   # both absent (a project wrapper would override the global one)
grep -H '^stamp:' ~/.germline/agents/houston/*.md ~/.germline/agents/houston/cards/*.md /home/hruzam/unikuklatrix/nablarva/.germline/agents/houston/nablarva.md
```

## 1. Expected stamp tokens (from the files; re-grep before testing — any edit regenerates a token)

| absolute path | stamp |
|---|---|
| `/home/hruzam/reposoma/.germline/agents/houston/identity.md` | `0be9958a` |
| `/home/hruzam/reposoma/.germline/agents/houston/binding.claude.md` | `80c9168c` |
| `/home/hruzam/reposoma/.germline/agents/houston/binding.codex.md` | `cac6a05d` |
| `/home/hruzam/reposoma/.germline/agents/houston/cards/consult.md` | `fbc11800` |
| `/home/hruzam/reposoma/.germline/agents/houston/cards/audit.md` | `e517cc86` |
| `/home/hruzam/reposoma/.germline/agents/houston/cards/sitting.md` | `effacaf6` |
| `/home/hruzam/unikuklatrix/nablarva/.germline/agents/houston/nablarva.md` | `2ebbb49b` |

The loader may quote either `~/.germline/…` or its realpath; both are the same file.

## 2. Install (three copies, by hand)

```zsh
cp ~/ia-sync/claude/agents/houston.md           ~/.claude/agents/houston.md
mkdir -p ~/.codex/agents
cp ~/ia-sync/codex/agents/houston.toml          ~/.codex/agents/houston.toml
cp ~/ia-sync/codex/profiles/houston.config.toml ~/.codex/houston.config.toml
date '+%F %T'    # install time — every test head below must start AFTER this
```

## 3. Tests — fresh heads only

**Every row runs in a FRESH head started after the install** (a new `claude` / `codex` process; record its start
time). Never from a session that was already running — it holds the old agent list and old instructions.
Run `git -C /home/hruzam/unikuklatrix/nablarva status --short` before and after each row.

| # | route | head start | how | expect | effective model · effort |
|---|---|---|---|---|---|
| C1 | Claude main | __:__ | `cd /home/hruzam/unikuklatrix/nablarva && claude --agent houston`; first prompt without a card line, then `card: audit` on a small scope | 4 stamp lines (identity · binding.claude · nablarva.md · cards/audit.md); without a card line it asks you to choose — offer **audit only** (`sitting` is a stub, not testable yet) | opus · high? |
| C2 | Claude child | __:__ | fresh head in nablarva; `Agent → houston` with `card: consult` + one small move | stamps incl. `cards/consult.md`; consult shape (verdict · ≤5 constraints · said/inferred); no file written | opus · high? |
| C3 | Claude child | __:__ | same, no card line; then `card: consult` + "run an audit" | defaults to consult; then `out of card:` | opus · high? |
| C4 | neutral | __:__ | `cd /tmp && claude --agent houston`, `card: consult` | first line says neutral Houston (no addendum read) | opus · high? |
| X1 | Codex child | __:__ | fresh Codex head in nablarva; `spawn_agent` houston with `card: consult` | stamps + effective cwd + selected addendum path; consult shape | gpt-6.1-sol · high? |
| X2 | Codex main | __:__ | `codex --profile houston -C /home/hruzam/unikuklatrix/nablarva`, no card line, then `card: audit` | stamps; asks you to choose — offer **audit only** (sitting = stub); Houston identity not blurred by AGENTS.md's Cartan text | gpt-6.1-sol · high? |

**PASS per row requires all three:**
1. **Tokens match** §1 for every file the row should read (a wrong or missing token = FAIL, even if the prose looks right).
2. **Transcript shows the reads:** a Read / exec of each exact absolute path *before the first answer* —
   Claude: `~/.claude/projects/-home-hruzam-unikuklatrix-nablarva/*.jsonl` (child rows: also the `subagents/`
   transcripts); Codex: the rollout under `~/.codex/sessions/` for that head's start time.
3. **Effective model and effort recorded** in the last column from the transcript or the session status line
   (not from the wrapper text). A mismatch with the pin is a finding, not a pass.

Expected first findings: **none**, once the nablarva pointers (AGENTS.md, AGENTS.PROJECT-DESIGN.md, PROJECT.yaml
comment) are fixed — oraculum is fixing them in parallel. Any other first finding is real; record it.

## 4. Rollback (by hand, on every host that received the files — rsync never deletes)

```zsh
# a) live copies (run on office; and on home too if it was deployed there)
rm -f ~/.claude/agents/houston.md ~/.codex/agents/houston.toml ~/.codex/houston.config.toml

# b) X0 project renders + project bindings (staged moves/deletes, uncommitted)
cd /home/hruzam/unikuklatrix/nablarva
git restore --staged .dev/session/nablarva-X1-architecture/raw/archive.x0-renders
git checkout HEAD -- .claude/agents/houston.md .codex/agents/houston.toml .codex/profiles/houston-nablarva.config.toml \
  .germline/agents/houston/binding.claude.md .germline/agents/houston/binding.codex.md
A=.dev/session/nablarva-X1-architecture/raw/archive.x0-renders
cp $A/nablarva.md .germline/agents/houston/nablarva.md
cp $A/identity.md /home/hruzam/reposoma/.germline/agents/houston/identity.md
rm -r /home/hruzam/reposoma/.germline/agents/houston/binding.claude.md \
      /home/hruzam/reposoma/.germline/agents/houston/binding.codex.md \
      /home/hruzam/reposoma/.germline/agents/houston/cards
# pointer fixes in nablarva + reposoma README/pin card (added by oraculum after assay F2)
git checkout HEAD -- AGENTS.md PROJECT.yaml .dev/session/AGENTS.PROJECT-DESIGN.md
git -C /home/hruzam/reposoma checkout HEAD -- .germline/README.md raw.settings/raw.card.model-effort.md

# c) ia-sync back to the pre-row state (claude/agents/houston.md was ` D` = majkee's backup removal — rm is CORRECT here;
#    `git checkout` would resurrect the OLD pre-L16 houston that majkee deliberately removed — assay F1 overruled by oraculum)
rm ~/ia-sync/claude/agents/houston.md ~/ia-sync/codex/agents/houston.toml
rm -r ~/ia-sync/codex/profiles
```

If already committed and pulled on home: revert the commits, pull on both hosts, then run (a) by hand on **both** hosts —
`deploy.sh` rsyncs `codex/agents/` without delete, so a removed repo file stays live until you remove it.

## 5. After GO — commit order (majkee)

1. **reposoma** (germline identity · bindings · cards · README · `raw.card.model-effort.md`) → push.
2. **nablarva** (addendum · archive · removal of project wrappers/bindings) → push.
3. **ia-sync** (three wrappers · journal · this bed) → push.

On **home**: `git pull` reposoma **before** any `deploy.sh` there — wrappers deployed without the germline would load
missing files (first finding: unreadable identity). Then pull nablarva, then ia-sync + `deploy.sh`; the profile stays a
hand `cp` on each host.

---

# C. protocole from majkee

## C.1. claude main

**SCENARIO**
- model: `calude-opus-5-5` , effort: ? (probably high), id: `93316906-8726-436c-b2df-526b40505d1d`
```
(1) hello with no card line → it should ask you to choose; answer audit · (2) card: audit +
"Mechanics
(2) card: audit + "Mechanics
 only, small scope: check that every pointer to Houston's homes resolves — AGENTS.md:40,  PROJECT.yaml:16,
 .dev/session/AGENTS.PROJECT-DESIGN.md frontmatter. Findings only, write nothing."

```

**`Houston` wrote:**

```
Problems found

mech-1: verified wrong. The prose links in the design wrapper won't open.
In .dev/session/AGENTS.PROJECT-DESIGN.md:26-27 (Document role), the Claude and Codex binding links are written as [Claude](~/.germline/...) and [Codex](~/.germline/...). Markdown doesn't expand ~. Renderers read it as a folder literally named ~ under .dev/session/, so the links are broken when clicked.
- The paths are right; only the link form is wrong. Line 25's addendum link uses a relative path and works.
- Suggested fix: use an absolute file:///home/hruzam/.germline/... target, or keep the ~ path as plain code text with no link. The second option suits a wrapper meant "for all runtimes", and it fits an old item in addendum §6 about absolute host paths not belonging in such a wrapper.
- This is your call; I haven't tested how your viewer renders these links.

mech-2: verified out of date. The addendum's own leftover note no longer holds.
Addendum §4 (nablarva.md:63-65) still says the wrapper's bindings: frontmatter and the PROJECT.yaml:16 comment "still say the bindings sit beside this addendum". Rows 7 and 9 above show both were fixed in b57e199.
- The fix is to delete or close that sentence in the addendum.
- In the same frontmatter, revision: unresolved — uncommitted at authoring is also out of date: the file is now committed. The fix is to record the commit.
- This edit is in the addendum, not the wrapper. That puts it outside my editing scope, so you'd make it yourself.

Not checked

- Whether binding.codex.md is current. I confirmed the file exists but didn't read it or its stamp.
- The wrapper's source: line (pointing into an ia-sync session folder). It isn't one of Houston's homes, so it was out of scope.
- Every other part of the full audit walk: organ bodies, docs/ARCHITECTURE.md, and the flag compared against what's actually built.
- Whether any viewer actually renders the ~ links. This conclusion comes from how Markdown resolves link paths, not from a test.

to-majkee ---
- mech-1: choose a fix for AGENTS.PROJECT-DESIGN.md:26-27, either an absolute file:/// link or plain code text with no link, then commit it.
- mech-2: edit the addendum yourself (outside my scope): remove the out-of-date §4 note and replace revision: unresolved with the commit.
---

```

> please, hoston, give me recommendations.

***houstons results***
Copy from hand - explained why
```
- run: 2026-10-12 · main session `claude --agent houston` · cwd /home/hruzam/unikuklatrix/nablarva (from env; no shell for `pwd -P`)
- entry proof (turn 1, no card line): identity 0be9958a · binding.claude 80c9168c · addendum nablarva 2ebbb49b → asked operator for audit|sitting, no silent consult ✔
- turn 2: `card: audit` + "mechanics only, pointers to Houston homes, write nothing" → audit card e517cc86 loaded; findings returned, nothing written ✔
- turn 3: asked to fold into this file → `out of card:` (no Edit tool; whole-file Write refused; landing outside addendum §2) → block handed to operator ✔
- pointer check: 10/10 resolve — AGENTS.md:40 (addendum · binding.claude · binding.codex · identity · cards/audit) · PROJECT.yaml:16 key + comment · wrapper frontmatter maintainer.source / .bindings / role+card. No project-scope houston wrappers present.
- mech-1 (verified wrong): AGENTS.PROJECT-DESIGN.md:26-27 links use `](~/.germline/…)`; markdown doesn't expand `~` → broken when clicked. Fix: plain code text with no link, or a `file:///` link.
- mech-2 (verified out of date): addendum §4 L63-65 leftover note is already fixed by b57e199; frontmatter `revision: unresolved` is out of date. Operator edits it (outside Houston's editing scope).
- not checked: binding.codex.md contents/stamp · wrapper `source:` line · full audit walk · viewer rendering of `~` links.
- witness verdict: ______ (operator)

What this run showed about the upgraded build. The stamp lines, card selection, write-nothing limit and out of card: refusal all behaved as the binding describes. The missing Edit tool meant I couldn't insert text into an existing file. If you want Houston to fold results into files like this in future, that's a binding decision: add Edit to the tools, or keep the rule that you paste.
```

---


## C.2. claude spawn

**SCENARIO**
- main: `claude-sonnet-4-6`, effort: `high`, id: `fbcd0dc3-120c-4c92-9596-c89aae2fcb76`
```
send: "Spawn houston: card: consult + "Move: rename .dev/session/AGENTS.PROJECT-DESIGN.md to 
/PROJECT-DESIGN.md at the repo root, leaving a stub at the old path. Does it fit L16.9?"
```

**`Houston` | main wrote:**

```
Houston verdict: stretches.

On L16.9 alone the move fits — the lock names roles, not paths, and moving a durable document out of .dev/session/ reduces drift. The full specified move (rename + stub) is a stretch: it can go ahead under these 5 constraints.

---

Constraints

1. Live gate cites old path. ovitmugen-01 RUNBOOK (L14,42,68-69) and STATUS (L17,21) both point acceptance at AGENTS.PROJECT-DESIGN.md § KEYS CODE. A pointer-only stub breaks that reference mid-gate. Either wait until ovitmugen-01 closes, or have the stub point section-by-section (§ KEYS CODE → /PROJECT-DESIGN.md § KEYS CODE). Any RUNBOOK/STATUS edits belong to that gate's head.
2. Stub is pointer-only (L16.10). New path, move date, commit. No content. It must stay as long as flag L14·D5 holds "beside AGENTS.PROJECT-DESIGN.md" — that phrase goes stale but must not be rewritten (L15).
3. Pointer fan-out in one commit. PROJECT.yaml:15 · AGENTS.md Session-surfaces sentence · addendum §1 table row · AGENTS.stridularium-design.md:3 sibling line · the wrapper's own 23 relative links (all break at root). Archived renders/X1 raw/ copies are history — leave them.
4. Draft status must move with the file. At the root it can be mistaken for canon. status: working-draft and the PROJECT.yaml note must travel with it.
5. Sibling fate must be decided explicitly. AGENTS.stridularium-design.md is the same species. Moving only one splits the convention. The decision can be "stays" — but it must be stated. Pointer edits afterward are audit-card mechanics (a diff majkee commits, L16.14). X1 head should log the move in STATUS holds:.

---

Side notes for next audit (Houston flagged, not asked)
- addendum §4 "known residue" (wrapper bindings: pointing beside the addendum) looks resolved — the line may be stale.
- ovitmugen RUNBOOK:92 calls the wrapper "append-only (Cartan)": predates keeper migration and is in tension with a rename.

---

to-majkee ---
Decision needed before the move executes:
  A. Wait for ovitmugen-01 to close, OR approve section-level stub pointers now?
  B. Sibling AGENTS.stridularium-design.md: moves with PROJECT-DESIGN.md, or stays?
Once decided, pointer fan-out (constraint 3) is a single commit (audit-card mechanics).
X1 head to log in STATUS holds: after the commit.
```

---

## C.3. claude spawn

**SCENARIO**
tester agent: `claude --resume a191ed8d-67da-4ba2-8d57-aaef2a33c636`
- main: `claude-sonnet-4-6`, effort: `high`, id: ``
```
 send: "Spawn houston" with no card line, same question → defaults to consult; then card: consult + "…and run a full audit" → expect out of card:
```


***prompt***
```
0. Read all first.
1. Spawn houston -> Let him hold on `sendMessage`: "Move: rename .dev/session/AGENTS.PROJECT-DESIGN.md to /PROJECT-DESIGN.md at the repo root, leaving a stub at the old path. Does it fit L16.9?"
2. Report what model and effort houston is.. I will task him during session. Have not only this first one.
3. I'll tell you where report|log his relplies.
```
**`Houston` | main wrote:**

```
@tester (claude-sonnet-4-6) relay · 2026-10-13 · round 1

/home/hruzam/.germline/agents/houston/identity.md · stamp: 0be9958a
/home/hruzam/.germline/agents/houston/binding.claude.md · stamp: 80c9168c
/home/hruzam/unikuklatrix/nablarva/.germline/agents/houston/nablarva.md · stamp: 2ebbb49b
/home/hruzam/.germline/agents/houston/cards/consult.md · stamp: fbc11800

# Consult: move the wrapper to `/PROJECT-DESIGN.md`, with a stub at the old path

Card: consult. Verdict: stretches. The move fits L16.9. The strain is with L16.10 and two neighbouring files, so you can proceed if you carry the constraints below.

Move: rename `.dev/session/AGENTS.PROJECT-DESIGN.md` to `/PROJECT-DESIGN.md` at the repo root, and leave a stub at the old path.

## Findings

1. L16.9 doesn't lock a location. `locked: L16.9` says only "PROJECT-DESIGN.md = thin animal wrapper and index". The full record uses the same bare name in every place (nablarva@2ae8636:.dev/architect-now-uncanonical/project-documentation.symmetry.2026-10-06.md, K2/K3 and the homes table). The current path comes from my addendum §1 table, which is not a lock. Moving the file therefore reopens no lock.
2. The move fits L16.9 better than the current home. L16.9 also says "session = temporary work". inferred: houston: keeping a durable wrapper under `.dev/session/` puts it among the temporary session surfaces. A root file next to `AGENTS.md` and `PROJECT.yaml` matches its role, and the new name matches the lock word for word.
3. The stub is where it stretches. L16.10 says "One home per fact". A stub that holds anything beyond a pointer becomes a second home. It would also break the `§ KEYS CODE` anchors that the live bed `ovitmugen-01-basement` cites. Those citations are by absolute path in RUNBOOK.md L14/42/69 and STATUS.md L17/21. The stub keeps the file path working, but the anchor will not exist inside it.
4. It splits the pair. `.dev/session/AGENTS.stridularium-design.md` (frontmatter L3) calls itself the "sibling" of the same species. `flag.md` L14·D5 (line 102) describes it as "beside AGENTS.PROJECT-DESIGN.md". After the move, that flag text describes a location that no longer exists. The flag is append-only (L15), so it can't be edited.
5. Who changes what. inferred: houston: L16.14 limits the audit pen to "pointers, `checked:` stamps, one-liners". Renaming a canonical home is more than that, so majkee or the head makes the move and commits it. I write nothing.

## Constraints

1. The stub is a pointer only. It contains one line to `/PROJECT-DESIGN.md` and no content. Record a removal condition — "removed when no live bed cites the old path". Don't leave it open-ended.
2. Update every pointer in the same commit: `PROJECT.yaml:15` (project-design:), the `AGENTS.md:32` saddle line, the `pulse.md:10` mention, and the addendum's §1 table row and §4 wrapper references. The addendum change is a diff for majkee to commit. Re-check each target by text, not by line number.
3. Don't edit `ovitmugen-01-basement`'s RUNBOOK or STATUS. The stub covers their path citations until that bed closes. Tell that head about the `§ KEYS CODE` anchor.
4. Decide the sibling. Either move `AGENTS.stridularium-design.md` the same way, or record why it stays in `.dev/session/`. Either way, list the stale "beside" wording in L14·D5 under the flag's `## Archived index` (L15). Don't rewrite the flag text.
5. Don't touch history. Pins under `.dev/architect-now-uncanonical/` and `raw/archive.x0-renders/` stay. Only live pointers move.

## Evidence read

- `.dev/session/flag.md` (L9, L9′, L12, L14·D5, L15, L16.1–15)
- Grep for PROJECT-DESIGN in `PROJECT.yaml`, `AGENTS.md`, `pulse.md`, `AGENTS.stridularium-design.md`, ovitmugen-01-basement RUNBOOK and STATUS
- `~/.germline` (no hits — global germline needs no change)

## Not verified

- Wrapper body's own relative links (may break when file moves to root)
- All 37 files that mention the name — most are session/archive history
- Anything outside the repo (ia-sync, Codex config) that may hard-code the old path

No helper spawned. No file written.
```
***prompt***
```
Message to @houston: "
1. activate `card_consult`
2. run a full audit
" 


```

```
@tester (claude-sonnet-4-6) relay · 2026-10-13 · round 2

/home/hruzam/.germline/agents/houston/identity.md · stamp: 0be9958a
/home/hruzam/.germline/agents/houston/binding.claude.md · stamp: 80c9168c
/home/hruzam/unikuklatrix/nablarva/.germline/agents/houston/nablarva.md · stamp: 2ebbb49b
/home/hruzam/.germline/agents/houston/cards/consult.md · stamp: fbc11800

I can't run the full audit under the consult card, so I haven't started one. The two steps you asked for contradict each other.

1. "activate `card_consult`": done. I read card_consult as card: consult, which this child session was already running, so nothing changed.
2. "run a full audit":
   out of card: full audit (whole-animal walk, findings plus a wrapper-mechanics diff) → card: audit, on a main session

Why I stopped instead of auditing:
- The card doesn't allow it. A consult checks one move, writes nothing and returns at most five constraints. Walking the whole animal and producing a diff is the audit card's job (identity §The three cards; cards/consult.md).
- This route can't run a complete audit. I'm a spawned child. An audit here is only an audit-as-probe — it would open with `unqualified for the complete card` and would not write the findings and .diff pair that addendum §2 assigns.
- The probe needs its own card line. An audit-as-probe would need an explicit `card: audit`. Your message names consult, so I didn't switch cards myself.

To get the full audit:
- Start a main session in the project root with `claude --agent houston` (interactive, not -p), and give it the line `card: audit`.
- Give it the output filenames. Per addendum §2 they go under `.dev/session/<invoking bed>/raw/houston-audit.<YYYY-MM-DD>[.<cycle>].md` and `….diff`. If one already exists for 2026-10-07, add a suffix.
- If you'd rather have a quick limited pass from this child route first, re-invoke with `card: audit` explicitly. That gives a probe that declares its limits, not the real audit.

The consult finding delivered earlier on the PROJECT-DESIGN.md move (verdict: stretches) still stands. No files written, no helper spawned.

to-majkee ---
Pick a route for the full audit:
  (a) main session — `claude --agent houston` in /home/hruzam/unikuklatrix/nablarva, give `card: audit` and output filenames; or
  (b) re-invoke this child with `card: audit` for a limited probe first.
---
```

---

## C.4. claude main in `/temp`

**SCENARIO**
- `claude --resume f3c91546-89c3-41d1-8694-197648e91f70`
**`Houston` wrote:**
```
row: C4 neutral
how: cd /tmp && claude --agent houston
send: card: consult + "Who are you and which project layer did you load?" → expect "neutral, no addendum"
```

```
/home/hruzam/.germline/agents/houston/identity.md · stamp: 0be9958a
/home/hruzam/.germline/agents/houston/binding.claude.md · stamp: 80c9168c
/home/hruzam/.germline/agents/houston/cards/consult.md · stamp: fbc11800

Neutral Houston: I found no project addendum, so no project layer is loaded.

Who I am: @Houston, the grounding architect. I check whether a move still fits the project as it exists: its locks, its declared architecture, its organs and its code. I have three cards: consult, audit and sitting. I don't own lifecycle, the gavel, build or divergence. (said: identity.md §Identity, §What I never own)

Which project layer I loaded: None.
- I had no shell, so I couldn't run pwd -P. I used the working directory the environment reports, /tmp.
- I walked up from there: checked /tmp/.germline/agents/houston/*.md and /.germline/agents/houston/*.md. Neither exists.
- /tmp is not under /home/hruzam, so the global ~/.germline was never a candidate. The loader excludes it anyway.
- No flag, no L16 locks, no RUNBOOK and no landing path are in scope. Anything project-specific would come back as unclear.

Card: consult, from the explicit line in your message.

Finding: stretches. This route is a main session, because no parent agent spawned me.
- The binding's route table allows consult only on a child route. A main session gets audit or sitting. (said: binding.claude.md §Entry routes)
- The loader and the binding only cover the case where a main session gets no card line. An explicit card: consult on a main session isn't covered either way.
- I ran it as a consult because it's read-only and writes nothing, so nothing is at risk. But the gap is real. (inferred: houston)
- Constraint: the binding should either list consult on the main route or have the loader answer out of card: for it there.

Not verified:
- I read the working directory from the environment, not from pwd -P.
- This reply can't count as a route witness, because Houston doesn't witness itself (binding §Entry proof and route proof). Your expected result, "neutral, no addendum", matches what happened. A separate fresh-session witness still needs to record it in a project bed.
```

```
 recap: You're testing whether Houston loads with no project layer from /tmp, and it did: neutral, no addendum, consult card. Next, have a separate fresh session record the witness, and decide whether consult should be allowed on a main session. (disable recaps in /config)
```

---

## X.1. codex as child

**SCENARIO**
main: `01a13284-8b4c-7ff1-9729-2db76ebcc11e`
```
how: fresh codex -C ~/unikuklatrix/nablarva
send: "Delegate to the houston subagent:" card: consult + "Move: rename .dev/session/AGENTS.PROJECT-DESIGN.md to /PROJECT-DESIGN.md at the repo root, leaving a stub at the old path. Does it fit L16.9?"
```


***prompt***
```
0. Read all points here first.
1. Delegate to the houston subagent:" card: consult + "Move: rename .dev/session/AGENTS.PROJECT-DESIGN.md to /PROJECT-DESIGN.md at the repo root, leaving a stub at the old path. Does it fit L16.9?"
2. Report what model and effort houston is.
3. I'll tell you where report|log his relplies.
```


> cartan, report here:

**`Houston` | `Cartan` main wrote:**
```
```



---

**Copy|PASTE**
---

## C.5. claude spawn

**SCENARIO**
```
```

**`Houston` | main wrote:**

```
```

---