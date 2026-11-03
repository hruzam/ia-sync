from: oraculum · unit U4 · date 2026-10-21

Audit-only. Read: field.U4.return, MIGRATE, design.global-germline-deploy, ISS.germline-migration-tail (archive), germline/README, CHATBOT.md, deploy.sh :1–125 + :130–375, DEC.01 D3, RECONCILE.G01 §3, RESULT.U1 §2–3, RESULT.U3 §9, binding.codex.md :1–40, SYNC_DISCIPLINE :10–22/:89–92, fold-scheme.md :16–33, fork README, journal :38–53, TEST-INSTALL §5. Read-only checks today (no deploy, no ssh): `find`/`diff -rq` source↔fork, fork `git status` (clean), `git log` on both, marker file, nablarva X1 `tunnel.state.json`. Flight corrections (a)–(c) carried. Tags: **[said]** = quoted/observed in a file today · **[inferred]** = my reading · **[unverified]** = no record either way.

**Governing insight.** On 2026-10-12 the chatbot channel was split in half: its *write* side moved to ia-sync (chatbot-port SKILL "only write destination: `~/ia-sync/germline/skills/`", design §4.4) while its *read* side stayed on the fork (CHATBOT.md:9 `hruzam/reposoma`). Every new skill ported since then is invisible to chatbots by construction; the skills dirs are equal today only because nothing new was ported **[inferred from the two pointers + `diff -rq`]**. The fork is therefore not a stale copy to retire — it is the read end of a distribution channel with no leg, no owner and no detector. D3 is a channel decision, not a cleanup decision.

## (1) Deploy/source model — sound where it is a mechanism, phrase where it is a procedure

**Sound and complete for the host (office):** source `ia-sync/germline/` → `deploy_germline()` → real `~/.germline` **[said: deploy.sh:143–224]**. Four fail-closed classes (symlink; non-dir; interior symlinks; undeployed pre-existing tree that differs → `--adopt-germline` with `cp -a` backup) — all hold in dry and live, write nothing, exit 3 via `finish` **[said :155–201, :260–270]**. Order: germline before wrappers in a full run **[said :22–23, :284–285]**. Marker `~/.local/state/ia-sync/germline.deployed` carries date + commit **[said :209–211; today: `fcee387`, 2026-10-17; no `germline/` commit since — `git log fcee387..HEAD -- germline/` empty; consistent with Flight's diff=0]**. Wrappers: Claude agent + Codex child rsync'd, Codex profile allowlisted `copy_file` with symlink refusal and backup **[said :104–121, :241–245]**.

**Where it is only a phrase or stale:**
- *Ghost retirement* = "retire by hand, with a backup" (deploy.sh:217, README:16). No steps, no backup location, no record rule. Zero ghosts have ever been listed (MIGRATE §2 "expect ghosts: none"; today none) — so the gap is latent, not bleeding.
- *Drift detection is manual triangulation.* Nothing reads the marker. "Is live current?" today needed journal:53 (`e3231c3`), marker (`fcee387`), HEAD (`55e6157`) and a `diff -rq`. The model is drift-*detectable*, not drift-*reporting*.
- *"Known window" is expired.* MIGRATE:77 says a full deploy on a symlinked host is harmless "because the symlink still resolves to identical files". False since the fork diverged (6 files, identity 0be9958a vs 99ae988e) **[said: diff today]**. On a still-symlinked home, a full `deploy.sh` would land current wrappers (canaries re-rolled 10-17) over the old fork identity — stamp proofs would quote stale tokens. Not harmless; order matters (§4).
- *binding.codex.md:18* "hand-installed; not in the deploy map" **[said]** — superseded by deploy.sh:241 and journal:46 **[said]**. TEST-INSTALL §5:121 "profile stays a hand `cp`" and fold-scheme:31 "no deploy leg" repeat the same stale claim. Note the cost: binding.codex is a *loaded* file; fixing :18 re-rolls `0c812f6c` → Codex routes need re-witness. Bundle with RECONCILE §4(i), do not fix alone.
- *Write-side leak already happened once:* reposoma commit `5357179` (2026-10-14, "germline-02") touched `.germline/` after the source moved **[said: git log]** — the preamble was authored into the fork first (ISS card :24). "Sole edit surface" was discipline, not mechanism.

## (2) Stamp rule — what it should literally cover

README:10 "every loaded germline file" **[said]**. Today stamped: identity, two bindings, three cards (6). Unstamped: `skill.buffering-cycle.md` (frontmatter `name/description/source/twin`), `tunnel.preamble.md` (no frontmatter), README, CHATBOT **[said: Field grep; Flight verified]**. Three readings:

- **A — narrow the sentence:** "every file an agent loads at entry and must prove it read (identity · bindings · cards · project addenda)". Skills/preamble declared out of scope by a second sentence. Cheapest; leaves the preamble unprovable.
- **B — stamp everything under `germline/`.** Uniform, parser-friendly; but a stamp on CHATBOT.md/README proves nothing (nobody quotes it) and burdens edits.
- **C — two-tier by consumer (recommended):** `stamp:` on files whose reader must *prove* the read (the entry chain, plus the tunnel preamble — it is prepended by a tool, and `tunnel.state.json` records only the path, not the content, so a first-line stamp is the only delivery proof; cheap, no agent cost). Files read *as-is* by chatbots/humans (skills, CHATBOT, README) declare provenance keys instead — CHATBOT.md:26 already names `source`, `twin`, `source-commit`. Literal rule: *"A file an agent must prove it read carries `stamp:` and quotes it; a file read as-is carries `source`/`source-commit`; a file carries exactly one of the two."* This matches Majkee's parser direction (RESULT.U3 §9): one key set per file class, no per-file heuristics.

What stamp-less files should declare under C: skills — add `source-commit: ia-sync@<short>` at port time (chatbot-port already owns this key); preamble — a one-line `[stamp: xxxxxxxx]` at line 1 or keep stamp-less and declare it in README as tool-delivered. No edit proposed here; destination §7.

## (3) The fork — all live consumers, prerequisites, options

**Fork content today [said]:** `agents/houston/{identity,binding.claude,binding.codex,cards/{audit,consult,sitting}}`, `CHATBOT.md`, `README.md`, `skills/skill.buffering-cycle.md`, `tunnel/tunnel.preamble.md`. Equal to source: CHATBOT, skills, audit, sitting. Differ: identity, both bindings, consult, README, preamble (fork preamble is the *older* 2026-10-08 text; source carries the 10-17 generalisation). Git clean; last commit 2026-10-14. No `agents/houston/reposoma.md` → reposoma's "project layer" holds zero project content; the folder is 100 % global copies.

**Consumers:**
1. **Chatbots via GitHub connector → `hruzam/reposoma .germline/`** — pointer CHATBOT.md:9 (both copies) **[said]**. Whether any chatbot currently has the connector attached: **[unverified]**.
2. **Chatbot project-memory hand-drops** — snapshots, not pointers; no file edit can re-point them; drift by design **[said: CHATBOT.md:9–10, :40–41]**.
3. **Home host `~/.germline` symlink → the fork** — if home is still symlinked **[unverified today; last record journal:53 "home pending" 2026-10-14]**, the fork is home's *live runtime layer* for Houston. Field missed this consumer; it is the reason MIGRATE §3 gates on both hosts, and it inverts TEST-INSTALL §5's pull order once the fork is stripped (home would pull a gutted reposoma *before* migrating → unreadable identity, the exact first finding).
4. **Forge fold-scheme.md :26, :28, :31** — GUIDE pointers naming the fork as source + "deploy.sh has no `.germline` leg by design" **[said; stale]**. Reader = a seat forging the next agent. Also the U6 destination (RESULT.U1 §7).
5. **Fork README:14** — self-description "global root is this repo … `~/.germline` is a host symlink here" **[said; stale]**.
6. **Tunnel preamble in the fork — no live consumer found.** nablarva X1 `tunnel.state.json:9` points at `/home/hruzam/.germline/tunnel/tunnel.preamble.md` (deployed copy) **[said]**; the termbrana handoff of 2026-10-21 cites the ia-sync source path **[said]**. The ISS card's "tunnel-03 points at the nablarva bed copy" is superseded on this evidence (whether that thread is still open: **[unverified]**).
7. **Archived ISS card** — its steps 4–5 (delete fork copies, commit reposoma) were not executed **[said: files exist]**; the card sits in `archive/` = solved. The record is wrong about itself.

**Complete prerequisite list for any fork disposition** (D3): P1 connector access to private `hruzam/ia-sync` tested by the operator (one `ls` through the connector) **[unverified either way, Flight (c)]** · P2 inventory of chatbots holding a Houston identity assignment or a project-memory copy (operator says; no file can) · P3 home `~/.germline` state verified (ssh or a home seat) and, if still symlinked, migrated **or** an explicit ordering rule that home migrates before any reposoma pull of a stripped fork · P4 a chosen retirement scope that names CHATBOT.md's consumer (neither MIGRATE §3 nor the ISS card does) · P5 fold-scheme + fork README re-pointed in the same move (else the stub lies next to a GUIDE that still says source).

**Options, with the chatbot route at each step:**
- **MIGRATE §3 as written** (rm agents/houston/*, skills/, CHATBOT.md; README stub). Route **breaks at the commit** — CHATBOT.md and skills vanish from the only place CHATBOT.md points. Only safe after P1 + re-home. As a *final* step it is correct; as a disposition it is incomplete.
- **ISS-card scope** (rm agents/houston/**, fix README:14). Skills route keeps working; identity row of CHATBOT.md:18 points at nothing → must be edited in the same commit. Stops serving the stale identity. Does **not** rejoin the write side: future skill ports still never reach the fork. Honest only if README says "skills here are a frozen snapshot".
- **Re-home CHATBOT.md to ia-sync** (needs P1). Route works at every step if ordered: P1 → edit CHATBOT.md in ia-sync (repo + path `germline/`, no dot) → push ia-sync → *then* MIGRATE §3 on reposoma (after P3). Single source, zero new mechanism, rejoins write and read sides. Hand-drop consumers unaffected (snapshots). **Recommended if P1 passes.**
- **Mirror leg ia-sync → reposoma/.germline.** Route works at every step. Costs: a second target under README:15's additive rule; the "deploy" that reaches a chatbot is the *push*, so the leg is rsync + commit + push in another repo — deploy.sh has never committed anywhere; reintroduces global copies inside a project layer (design §2's defect in a milder form — walk-up is path-only now, so not a collision, but structural debt); drift between fork and GitHub becomes a third gap. If chosen, mirror into a non-dot folder (`reposoma/germline/`) so the project layer stays clean. **Fallback if P1 fails.**
- **Freeze fork for skills+CHATBOT, remove agents/.** = ISS scope + a written freeze. Same write-side defect; acceptable only as a holding state with a date.
- **Leave.** Stale identity served; new skills never arrive; home runtime (if symlinked) keeps reading the fork — the one option that also keeps home's Houston alive untouched, which is why it is the de-facto state. Costs grow per edit.

## (4) Home — what must be recorded, and a watchdog

Before any home run **[as written: MIGRATE §2, TEST-INSTALL §5, deploy.sh:157–161]**: `readlink -f ~/.germline` output; reposoma / nablarva / ia-sync HEADs after pull; confirmation that the fork is *not yet stripped* (P3 ordering); `deploy.sh --germline-only --dry-run` output (expect 10 new files today — MIGRATE says 9; `tunnel/` was added 10-14). Order: pull all three → `rm` link → `--germline-only` dry → live → `diff -rq` → stamps grep → **only then** a full `deploy.sh --dry-run` (the "Known window" comfort no longer applies). After: `ls -ld`, `diff -rq`, marker content, exit code of the full dry run, journal entry on `journal.host-cleanup.md`, and the three-route Houston witness at current revisions (RECONCILE P5). Record the home node ID from `machines.json` as the host proof (AGENTS.md "Which host am I on?").

Watchdog: **warranted, as one open card**, not a routine. Today "home pending" lives only in journal:53 and an *archived* card; absence of an open card is being read as pending — exactly the "absence ≠ proof" trap. The card's job is to hold the P3 gate physically: "no fork retirement until this card is archived". Alternative: a journal HOME-NEEDS line only — cheaper, but it cannot gate. Majkee said home migration is separate operational work; the card records the gate, it does not schedule the work.

## (5) GUIDE/reference vs agent-consumable

Agent-consumable today: **deploy.sh:19–32 header** (the best contract that exists — modes, holds, exit codes); README:14–16 scope sentence (keep terse; add one drift-check line and point to the header rather than paraphrase). Human discipline, fine as is: SYNC_DISCIPLINE:20/:92; AGENTS.md `~/.germline` section. Runbook with a live half: MIGRATE — §1 and office §2 are history; home §2 is live; §3 is a proposal; "Known window" is stale → annotate, do not rewrite. Reference: design doc (CANONICAL), ISS card (needs a status line), fold-scheme table (U6). Unassigned: ghost procedure (belongs beside the README scope lines or in SYNC_DISCIPLINE, not in deploy.sh prose).

## (6) Recommended contract for the deploy path (note, not design)

Boundary: one source dir → one host-local target; the script never unlinks, deletes, commits or pushes. Inputs: `$REPO/germline/`, flags, host state (link/dir/marker). Returns: per-leg verb line; `HOLDS[]`; exit 0 / 2 (usage) / 3 (holds); marker on live runs; ghost list (report-only). Failure: the four hold classes + ghosts; a hold under `--germline-only` is the whole run. Verification (operator, listed not run): `diff -rq ~/ia-sync/germline ~/.germline`; marker commit vs `git rev-parse --short HEAD`; `grep -h '^stamp:'` on the entry chain. **Parser-friendly shape (Majkee's direction):** a `--status` mode (or the marker itself) emitting one fixed key=value block — `host= source_commit= marker_commit= live_state=real|symlink|missing diff_files= ghosts= holds=` — consumable identically by a seat, a human, or a hardcoded app. Nothing else in the leg needs to change for that.

## (7) Fold/repair destinations (none applied)

| finding | primary destination | alternative |
|---|---|---|
| fork README:14 symlink text | `/home/hruzam/reposoma/.germline/README.md:14` — one neutral line now ("global source moved to `~/ia-sync/germline/` 2026-10-12; this folder: see D3") | wait for D3 and write the final stub (MIGRATE §3 text) |
| fold-scheme :26/:28/:31 | `/home/hruzam/reposoma/raw.guides/germline-forge/res/fold-scheme.md` staleness banner at :22 + row fixes → U6 | banner only |
| binding.codex :18 | `/home/hruzam/ia-sync/germline/agents/houston/binding.codex.md:18` → "allowlisted `copy_file` (deploy.sh:241)"; re-roll stamp; bundle with RECONCILE §4(i); then re-witness Codex routes | leave + README note (no — a loaded file must not lie about its own install) |
| README stamp scope | `/home/hruzam/ia-sync/germline/README.md:10–11` option C sentence | option A |
| ghost procedure | `/home/hruzam/ia-sync/germline/README.md:15–16` three steps: `mv` ghost → `~/.germline.ghosts-<date>/<path>` · journal line · dry re-run shows none | `SYNC_DISCIPLINE.md` after :92; or a `--retire-ghosts` flag (rejected now: zero ghosts ever) |
| CHATBOT.md | `/home/hruzam/ia-sync/germline/CHATBOT.md:9,:11,:18` after P1 (repo + `germline/` path) | if P1 fails: keep pointer, add mirror leg |
| MIGRATE "Known window" | append dated note at `MIGRATE.germline.2026-10-12.md:77` | — |
| ISS card archived-but-undone | status line on the archived card, or re-open as the home/P3 card (§4) | journal line |
| TEST-INSTALL §5:121 "hand cp" | dated note (history file) | — |

## (8) Decisions

**Consequential (Majkee):**
- **D3 — not ripe.** Missing, exactly: **P1** connector access to private ia-sync (one operator test; decides re-home vs mirror) · **P2** which chatbots hold a Houston identity or a memory copy · **P3** home state verified, or the ordering rule adopted · **P4** scope choice (§3-as-written / ISS / re-home-then-§3) stated against CHATBOT.md:18. With P1 answered, the recommendation writes itself: re-home if yes, mirror-to-non-dot-folder if no; MIGRATE §3 then becomes the last step after home.
- **Watchdog card for home / P3 gate** — operator choice, not a gavel (§4).
- **Stamp scope option C** — touches README:8–11 (fold-era text); cheap, but it is Majkee's sentence to confirm.

**Mech (no gavel; some re-roll stamps):** fork README:14 neutral line; fold-scheme banner (U6); binding.codex:18 (bundled, re-witness); MIGRATE Known-window note; ISS card status; ghost three-step text; `--status` note into the later-writing handoff. Not proposed: running anything; deleting anything in the fork.

**Pending underlines:** the fork's 2026-10-14 write (`5357179`) means a second author surface was used after the move — RUNBOOK should name who may write into `reposoma/.germline` until D3 lands (default: nobody). The X1 `tunnel.state.json` evidence lifts the ISS card's preamble claim; whether tunnel-03 is still live is unverified.
