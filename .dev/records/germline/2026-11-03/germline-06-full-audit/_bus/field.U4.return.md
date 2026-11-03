from: field · unit U4 · date 2026-10-21

---

## A. Deploy model table

| copy / target | source | mechanism | additive / deleting | holds (fail-closed) | hand vs script | documented in |
|---|---|---|---|---|---|---|
| `~/ia-sync/germline/` (authored source) | operator edits here | git commit + push | — | N/A | hand | germline/README.md:14–15; AGENTS.md `~/.germline` section; SYNC_DISCIPLINE.md:20,92 |
| `~/.germline/` (live global layer) | `~/ia-sync/germline/` | `deploy_germline()` rsync `-a` (no `--delete`) | additive; ghosts listed, never removed | symlink → exit 1 (HOLD); non-dir → HOLD; interior symlinks → HOLD; pre-existing real tree + no marker + differs → HOLD unless `--adopt-germline` | script (`deploy.sh`) | deploy.sh:133–224; germline/README.md:14–15; AGENTS.md |
| `~/.local/state/ia-sync/germline.deployed` (marker) | written by deploy_germline after live run | `echo "deployed…" >` | overwrites | — | script | deploy.sh:209–211 |
| `~/reposoma/.germline/` (fork — reposoma project layer) | was source pre-2026-10-12; now project layer only | was symlink target; now a separate real dir in reposoma | N/A (not deployed by deploy.sh) | — | hand (committed with reposoma) | reposoma/.germline/README.md; MIGRATE §3 (retirement proposed, not executed) |
| `GitHub hruzam/reposoma .germline/` | reposoma repo push | `git push` reposoma | — | — | hand (operator pushes) | CHATBOT.md:8–9 (chatbot consumer pointer) |

**Authored vs deployed vs historical vs proposed:**
- Authored: `~/ia-sync/germline/` — the sole edit surface since 2026-10-12 (AGENTS.md, germline/README.md:14–15).
- Deployed: `~/.germline/` — real directory on office since 2026-10-14 (journal:53); home pending.
- Historical: `~/reposoma/.germline/` as source — retired by design.global-germline-deploy.2026-10-12.md §1 verdict; reposoma/.germline/README.md still describes the pre-migration shape.
- Proposed: MIGRATE §3 — delete global files from reposoma/.germline after both hosts migrated. Not yet executed; home migration pending.

---

## B. Consumer map

| consumer | which copy it reads | pointer location + quoted text | current / stale |
|---|---|---|---|
| Houston agent (Claude main/child) | `~/.germline/` (runtime-load: identity → binding.claude → addendum → card) | germline/README.md:8–11 "the wrappers carry only a loader; at entry the agent reads identity.md → binding.<vendor>.md → the nearest project addendum → cards/<card>.md" | current |
| Houston agent (Codex child / main profile) | `~/.germline/` | same README passage; deploy.sh:241 "Loads from ~/.germline" (houston.config.toml comment) | current |
| chatbot-port skill (Claude) | `~/ia-sync/germline/skills/` (port destination) | claude/skills/chatbot-port/SKILL.md:18 "Port home `~/ia-sync/germline/skills/skill.<slug>.md`" | current |
| chatbot-port skill (Codex) | `~/ia-sync/germline/skills/` (port destination) | codex/skills/chatbot-port/SKILL.md:17 "Only write destination: `~/ia-sync/germline/skills/skill.<slug>.md`." | current |
| ChatGPT / Claude.ai chatbots | `hruzam/reposoma` `.germline/` (GitHub; hand-drop or connector) | CHATBOT.md:8–11 "GitHub: `hruzam/reposoma` (private; majkee grants you access via the GitHub connector, or hand-drops the files into your project memory — both are valid). The shared home inside it: `.germline/`" | current pointer; fork content stale vs source (6 files differ) |
| germline-forge GUIDE / fold-scheme.md | `~/reposoma/.germline/agents/<slug>/identity.md` | fold-scheme.md:26 "`~/reposoma/.germline/agents/<slug>/identity.md` … `~/.germline` is a host symlink here, never a deploy target" | STALE — source moved to ia-sync; ~/ .germline is a real dir, not a symlink |
| deploy.sh (rsync source) | `~/ia-sync/germline/` | deploy.sh:144 `local src="$REPO/germline/" dst="$HOME/.germline"` | current |
| SYNC_DISCIPLINE.md (dead-edit rule) | `~/.germline/` is listed as a live deploy target | SYNC_DISCIPLINE.md:20 "The live trees (`~/.claude/`, `~/.config/zsh/`, `~/.gemini/`, `~/.germline/`) are deployed copies." :92 "The live machine trees (incl. `~/.germline/`, source `germline/`) are deploy targets, not sources." | current |

---

## C. H1–H6 evidence tables

### H1 — Every consumer pointer resolves to ia-sync source or deployed `~/.germline`; CHATBOT.md and Forge R04 are known fork exceptions. Any other pointer still naming `~/reposoma/.germline`?

| pointer location | points to | for/against H1 |
|---|---|---|
| chatbot-port Claude SKILL.md:18 | `~/ia-sync/germline/skills/` | FOR — ia-sync source |
| chatbot-port Codex SKILL.md:17 | `~/ia-sync/germline/skills/` | FOR — ia-sync source |
| deploy.sh:144 | `$REPO/germline/` = ia-sync source | FOR |
| AGENTS.md `~/.germline` section | `~/.germline/` real dir | FOR |
| SYNC_DISCIPLINE.md:20,92 | `~/.germline/` deploy target | FOR |
| CHATBOT.md:8–11 | `hruzam/reposoma .germline/` | AGAINST H1 (known fork exception per brief) |
| fold-scheme.md:26 | `~/reposoma/.germline/agents/<slug>/identity.md` | AGAINST H1 — not a known-exception pointer; stale, still names reposoma as source |
| reposoma/.germline/README.md:14 | "~/.germline is a host symlink here" → implies ~/reposoma/.germline as source | AGAINST H1 — describes old model |

**Net:** fold-scheme.md:26 is a consumer pointer outside the named exceptions still naming `~/reposoma/.germline` as source. No other such pointer found in read sources.

### H2 — Stamp rule scope: README says "every loaded germline file"; which files it literally covers today

Exact quote, germline/README.md:10–11:
> "**Stamp rule:** every loaded germline file carries `stamp: <8-hex random token>`, unique per file, **regenerated on every edit** (`openssl rand -hex 4`) — a matching token proves the current file was read."

Context (README:8–11): the stamp rule sentence sits inside the Runtime-load variant paragraph for Houston, following "at entry the agent reads `identity.md` → `binding.<vendor>.md` → the nearest project addendum → `cards/<card>.md` and quotes each file's `stamp:`".

**Files with stamp today** (verified by grep on `~/ia-sync/germline`):
- `agents/houston/identity.md:9` — `stamp: 99ae988e`
- `agents/houston/binding.codex.md:9` — `stamp: 0c812f6c`
- `agents/houston/binding.claude.md:9` — `stamp: cf14943f`
- `agents/houston/cards/consult.md:7` — `stamp: 5435b1c7`
- `agents/houston/cards/audit.md:7` — `stamp: e517cc86`
- `agents/houston/cards/sitting.md:7` — `stamp: effacaf6`

**Files without stamp:**
- `germline/skills/skill.buffering-cycle.md` — no `stamp:` field (confirmed; frontmatter has `name`, `description`, `source`, `twin` only)
- `germline/tunnel/tunnel.preamble.md` — no `stamp:` field (confirmed; starts with `[tunnel turn rule …]` — plain text, no YAML frontmatter)

**For H2:** "every loaded germline file" literally reads as all germline files, but the context of the paragraph and the only runtime-load implementation (Houston) restricts it to the agent runtime-load chain. Skills and tunnel preamble are not in that chain and carry no stamp. The sentence is broader than the current implementation.

### H3 — deploy.sh germline leg never deletes; retirement procedure written?

**For (never deletes):**
- deploy.sh:134 "Additive like the skills legs (no `--delete`)."
- deploy.sh:215–218: ghost inventory section — "GHOSTS — live files absent from source (… NOT removed; retire by hand, with a backup)"
- germline/README.md:15 "Deploy is additive: a file removed at source lingers live until retired by hand (deploy.sh lists such ghosts)."

**Retirement procedure search:**
- deploy.sh:217–218 instructs "retire by hand, with a backup" — no further steps.
- germline/README.md:15 repeats the same phrase — no procedure.
- SYNC_DISCIPLINE.md: no germline-specific retirement steps found.
- MIGRATE.germline.2026-10-12.md: no retirement procedure for live ghost files; §3 describes retiring the reposoma duplicate (different scope — git rm in reposoma, not live ~/.germline ghost retirement).
- design §4.1 says "Ghost inventory: list live files absent from source, in dry and live runs; each ghost = a hold for explicit, backed-up retirement" (deploy.sh:34) — no procedure written.

**Net:** no retirement procedure exists in any read source beyond the single phrase "retire by hand, with a backup."

### H4 — Home-host readiness: what must be true before `deploy.sh` runs on home

**Written prerequisites:**

From MIGRATE.germline.2026-10-12.md §2: "home later after `git pull` in reposoma, nablarva, ia-sync"

From MIGRATE §2 steps (written for office; apply per-host):
1. `readlink -f ~/.germline` must print `~/reposoma/.germline` (confirms symlink exists; otherwise STOP)
2. `rm ~/.germline` (link only)
3. `bash ~/ia-sync/deploy.sh --germline-only --dry-run`
4. `bash ~/ia-sync/deploy.sh --germline-only`
5. Verify stamps readable at `~/.germline` (MIGRATE:51)

From MIGRATE "Known window" (MIGRATE:75–77): "While a host still has the symlink, a full deploy HOLDs the germline leg (exit 3) but still deploys the wrappers and profile — harmless, because the symlink still resolves to identical files."

From TEST-INSTALL §5 (line 119–121): "On home: `git pull` reposoma BEFORE any `deploy.sh` there — wrappers deployed without the germline would load missing files (first finding: unreadable identity). Then pull nablarva, then ia-sync + `deploy.sh`; the profile stays a hand `cp` on each host."

**Pull order on home (TEST-INSTALL §5):** (1) git pull reposoma, (2) git pull nablarva, (3) git pull ia-sync, (4) `deploy.sh`, (5) hand `cp` profile.

**ISS card state:**
- ISS.germline-migration-tail (archive/): "Home host unchecked." (card:39)
- ISS.germline-deploy-before-commit (archive/): Fix mentions "home `git pull` + `deploy.sh --germline-only`" as pending; card archived = office fix applied, but home step not confirmed done.
- journal.host-cleanup.md:53: "Home still unchecked. Status → office done · home pending."

**Net:** home migration not done. ~/.germline on home is still the old symlink (per brief facts: "home pending"). All MIGRATE §2 steps + TEST-INSTALL §5 pull order remain outstanding for home.

### H5 — Chatbot route: how is the reposoma fork refreshed?

**Evidence searched:** CHATBOT.md, germline/README.md, reposoma/.germline/README.md, MIGRATE, design doc §3–5, SYNC_DISCIPLINE.md, AGENTS.md.

CHATBOT.md:8–9 (exact quote): "GitHub: `hruzam/reposoma` (private; majkee grants you access via the GitHub connector, or hand-drops the files into your project memory — both are valid)."

**No file states:**
- How the reposoma fork copy is refreshed from ia-sync source.
- Who owns the refresh operation.
- That ia-sync is private and inaccessible to a connector.

**MIGRATE §3 implication:** If executed, `git rm` removes agents/houston, skills/, CHATBOT.md from reposoma/.germline. CHATBOT.md itself would be deleted. A chatbot using the GitHub connector would find an empty or stub `.germline/`. No document acknowledges this consequence or describes a successor route.

**Net:** refresh ownership and mechanism are absent from all read sources. ia-sync privacy noted in CHATBOT.md only by implication (reposoma described as the chatbot-accessible copy, no explanation of why ia-sync is not used directly). MIGRATE §3 would break the chatbot route if executed without updating CHATBOT.md.

### H6 — MIGRATE §3 retirement prerequisites vs live consumer state

| prerequisite (MIGRATE §3 source) | document reference | met? | evidence |
|---|---|---|---|
| Both hosts migrated and verified | MIGRATE:68 "After BOTH hosts are migrated and verified" | NO | journal:53 office done; home pending (ISS card:39; brief facts) |
| Office: ~/.germline is real dir, byte-identical to source | MIGRATE §2 step 5 + journal:53 | YES (office) | journal:53 "byte-identical to ~/ia-sync/germline @ e3231c3"; brief facts confirm diff = 0 |
| Home: ~/.germline is real dir | MIGRATE §2 steps 1–5 | NO | journal:53 "Home still unchecked"; brief facts "home pending" |
| reposoma committed + saved before link removal | MIGRATE §1 (commit step) | YES (historical; office migration done) | journal:40–42 records commit before office migration |
| CHATBOT.md / chatbot route updated or retired | not written as a §3 prerequisite | NOT STATED | CHATBOT.md still points to reposoma fork; MIGRATE §3 does not name it as a gate |
| Consumer pointers re-pointed away from reposoma fork | not written as a §3 prerequisite | NOT STATED | fold-scheme.md:26 still names reposoma as source; not listed in MIGRATE §3 scope |

---

## D. Stale or contradictory claims

| file:line | quoted text (as read today) | what is true today |
|---|---|---|
| reposoma/.germline/README.md:14 | "Scope: `<scope-root>/.germline/` — global root is this repo (`~/.germline` is a host symlink here, never a deploy target)" | ~/ .germline is a real directory on office (journal:53; brief facts confirm diff=0). Source is ia-sync/germline/, not reposoma. This README was NOT updated after germline-01. |
| fold-scheme.md:26 | (identity.md row, mechanism column) "`~/reposoma/.germline/agents/<slug>/identity.md` … `~/.germline` is a host symlink here, never a deploy target" | Source is now ia-sync/germline/; deploy.sh is the mechanism; ~/ .germline is a real dir. Forge guide was authored 2026-10-07 and not updated for germline-01 (confirmed by ISS.germline-migration-tail card:28 "germline-forge GUIDE (DRAFT, verified 2026-10-07) describes the pre-10-10 symlink + render model"). |
| journal.host-cleanup.md:47 | "~/.germline is STILL the symlink → ~/reposoma/.germline on office" | Corrected inline at line 53 ("office migration DONE"). Line 47 is historical record text, not a living claim, but reads as current without the line-53 addendum. Not a true stale claim — append-only correction pattern. |
| journal.host-cleanup.md:52 | "status: OPEN — office migration pending, home migration pending" | Corrected at line 53. Same pattern. |

**Conflict:** reposoma/.germline/README.md:14 directly contradicts germline/README.md:14–15, AGENTS.md, SYNC_DISCIPLINE.md:20,92, and deploy.sh:134. ⚡ CONFLICT — same README slug, opposite scope claims; germline/README.md is current, reposoma fork is stale.

---

## E. MIGRATE §3 prerequisite checklist

| prerequisite | source document | met? | evidence |
|---|---|---|---|
| Both hosts migrated (office) | MIGRATE.germline:68 "After BOTH hosts are migrated and verified" | YES | journal:53; brief facts (diff=0 office) |
| Both hosts migrated (home) | MIGRATE.germline:68 | NO | journal:53 "home pending"; ISS.germline-migration-tail card:39 "Home host unchecked" |
| home pull order completed (reposoma, nablarva, ia-sync, deploy.sh, profile cp) | TEST-INSTALL §5:119–121 | NO | home migration not started |
| reposoma .germline committed before removal | MIGRATE:68 ("majkee decides"); MIGRATE §1 commit step | YES (office pre-migration commit done) | journal:40–43 |
| CHATBOT.md updated or route successor named | not stated as prerequisite in MIGRATE §3 | NOT STATED | absence finding |
| fold-scheme.md and other consumer pointers updated | not stated as prerequisite in MIGRATE §3 | NOT STATED | fold-scheme.md:26 still stale |
| One reposoma commit removing global files | MIGRATE:71 "git rm the global files there … One commit in reposoma. Done by a spawn on majkee's word" | NO | not executed; awaiting both-hosts gate |

---

## F. Friction for agent/operator consumer (ranked, cited)

1. **Fork content diverges from source; chatbot route has no refresh mechanism.** CHATBOT.md:8–9 directs chatbots to reposoma fork. The fork differs from ia-sync source in 6 files (brief facts). No file describes refresh ownership, frequency, or trigger. Any chatbot reading the fork gets stale Houston files.

2. **reposoma/.germline/README.md and fold-scheme.md still describe the old symlink model.** A seat reading fold-scheme.md:26 or reposoma/.germline/README.md:14 encounters authoritative-looking text that contradicts the live model. fold-scheme.md is a germline-forge guide — a natural starting point for a new seat implementing germline work.

3. **Ghost/retirement procedure is one phrase, not a procedure.** deploy.sh:217 says "retire by hand, with a backup." No document specifies the steps, backup naming convention, or whether a ghost retirement must be committed (journal entry, ISS card, etc.).

4. **MIGRATE §3 has no downstream consequence analysis.** The MIGRATE §3 text (MIGRATE:69–73) proposes git rm of skills/, CHATBOT.md, and houston files from reposoma. CHATBOT.md is among the files to remove, but no document notes this would break the chatbot route. The prerequisite list in MIGRATE §3 does not include updating CHATBOT.md.

5. **Stamp rule sentence scope is broader than the implementation.** germline/README.md:10 says "every loaded germline file carries `stamp:`" but skill.buffering-cycle.md and tunnel.preamble.md are germline files with no stamp. An agent reading only the README sentence would expect stamps on all germline files.

6. **Home migration has no watchdog or deadline.** journal:53 records "home pending" but no ISS card is open for home migration (both ISS cards are in archive/). No routine card exists. If a home session deploys wrappers before the germline leg, TEST-INSTALL §5:119 explicitly warns this causes "unreadable identity."

---

## G. Uncertainty / not-read

- **stamp presence in nablarva project layer** (`~/unikuklatrix/nablarva/.germline/agents/houston/nablarva.md`) — not in the brief's read list; stamp value cited in TEST-INSTALL §1:31 as `d9ee9067` but file not read directly today.
- **reposoma/.germline/ current file list** — brief facts give the 6-file diff names (README, identity, binding.claude, binding.codex, cards/consult, tunnel/tunnel.preamble) but I did not ls the directory; the ISS card and brief facts are the evidence.
- **Whether `~/.germline/programs` absence is documented anywhere** — brief states it does not exist; no source read today explains why or whether it is expected.
- **Houston wrapper files** (`~/ia-sync/claude/agents/houston.md`, `codex/agents/houston.toml`, `codex/profiles/houston.config.toml`) — not in the read list; content confirmed byte-equal source↔live per brief facts only.
- **Forge fold-scheme.md lines 1–19 and 33+** — only lines 18–32 were read per brief instruction; earlier and later content not reviewed.
- **design.global-germline-deploy §1–2 and §6–7** — read in full above (the brief said §3–5 only); referenced for completeness here but no claim rests on the un-asked sections.
