```yaml
updated: 2026-09-17
writer: trajectory
host: home
worktree: >
  ~/ia-sync (main) + ~/reposoma (core, HEAD 8397205 as of 2026-09-17 ~11:45). Reposoma
  moved three commits past 2f59340 (fc4b6dd, 4c8ce71, 8397205) via office/other-session
  sync ("reposoma is now fresh from office" — majkee). Verified all three individually:
  fc4b6dd IS majkee committing the two-gap-fix diff, byte-for-byte identical to what
  @assay witnessed — no loss, no drift. 4c8ce71 added one unrelated GEMINI.md
  wired-surfaces row + a Trajectory therapy file (different Claude session, Fable model —
  confirms parallel work exists but did not conflict here). 8397205 is a broad
  reincarnations/mail/registry sync, entirely unrelated to this arc. Reposoma is CLEAN
  (git status empty), no contradiction found. GUIDE.md's [ISSUE-DRAFT] banner and both
  fixes remain intact and still un-gaveled.
gate: >
  A fresh Claude session (updated skill) and a fresh Codex session (tunnel-delivered skill)
  each drop AND re-locate BOTH an issue card and a cold-start card in the one shared vault;
  the gaveled cold-start-card GUIDE carries the issue category, the sort-key rule
  (name vs frontmatter) and its unsorted fallback; and the standalone _issues/ vault from
  this session is reconciled into that shape (folded or kept — majkee's category call).
head_note: "cSharp — Trajectory authored this RUNBOOK and stays as navigator + status_owner; delegates bodies whole, keeps only navigation + test parts; closes if it can."
witness: "assay — counter-signs the gate; the claims in this STATUS are paths it can test"
checkpoint: >
  Phase 1 (@atlas-ui) built, CROSS-WITNESSED by @assay, PASS. Majkee confirmed the subtree
  shape, added issues/reactions/ (dateless, IR.<slug>.md, mirrors routines/), the coupling
  invariant, and locked >=7 assoc: as an unraised RULE (RUNBOOK "CLOSED 2026-09-17"). Majkee
  then committed that draft himself (2f59340) — still [ISSUE-DRAFT]-tagged, not gaveled.

  First tunnel contact made with @Cartan (tun ask, read-only send, no files written) — full
  findings at raw/cartan.tunnel-contact.2026-09-17.md. Cartan named two GUIDE gaps and cited
  2f59340. Per majkee's standing caution (assume Codex may carry stale training data —
  verify, don't trust the claim), the head independently re-verified all three against disk:
  (1) filename-parsing-law vs sort-key contradiction — CONFIRMED real. (2) reaction-card
  frontmatter undocumented in canon — CONFIRMED real. (3) commit 2f59340 — CONFIRMED real,
  majkee's own commit, not a hallucination. Sandbox-permissions claim ("excludes
  ~/ia-sync/codex/") was later RESOLVED WRONG — see holds below.

  @Delta fixed both confirmed GUIDE gaps in one pass, on top of 2f59340. CROSS-WITNESSED
  TWICE (head's own direct check + @assay independent PASS, zero failures): gaveled law
  untouched, reaction frontmatter field-set matches the live skill exactly (cosmetic
  key-order only, non-blocking), no commit, no self-gavel language, 32 insertions / 0
  deletions. Genuinely commit-ready.

  Majkee opened a fresh workspace-write tunnel table rooted at /tmp/cartan-sandbox-test
  (a scratch mirror, NOT the real repo — Cartan drafts there, @assay reviews, @Delta
  promotes; the real repo is never write-exposed to Cartan). The real, complete phase-2
  build message was sent ONCE per majkee's no-piecemeal instruction, then had to be resent
  after a real infra fix — two exit-30 failures so far, thread never born either time
  (threadId still null, no quota-spending turn completed):
    - Attempt 1 (8.5s, clear stderr): ~/.agents/skills/canvas/SKILL.md had
      description: '' (empty) — crashes codex_core session init on any FRESH thread birth
      (the earlier read-only contact reused an ALREADY-born thread, skipping skill
      reload — why this never surfaced before). Not ia-sync-authored, live-only/vendor
      file — fixed directly (real description string, no behavior change), scanned all
      sibling ~/.agents/skills/*/SKILL.md for the same defect, found none else.
    - Attempt 2 (identical resend, 0.88s, EMPTY stderr): different symptom, cause NOT
      diagnosed. Found a pre-existing, unrelated, legitimate resident Codex session
      already running (tmux `reinc-mech`, correlates with the separate
      incarnations-00-mechanism work visible in pulse.md) plus a shared
      ~/.codex/thread-writer-locks/.coordination.lock — POSSIBLE resource contention,
      NOT confirmed, NOT acted on. Deliberately did not touch/kill that resident session
      to test the theory. Stopped after two failures rather than guess a third time.

  Majkee then superseded the tunnel route himself: ran Cartan DIRECTLY (not through my
  tunnel), on a model he calls "Sol," authorized building the Codex primitive straight into
  ia-sync source. Cartan self-reported: built codex/skills/issue-card/SKILL.md +
  agents/openai.yaml, lockstep cold-start-card/SKILL.md + README.md edits, quick_validate.py
  PASS, git diff --check PASS, deploy --codex-only --dry-run PASS, no commit/push/deploy.

  HEAD INDEPENDENTLY VERIFIED THIS CLAIM FROM HOME — DOES NOT CHECK OUT:
  codex/skills/issue-card/{SKILL.md,agents/openai.yaml} DO NOT EXIST on home's disk.
  `git status --short codex/` is completely EMPTY (no uncommitted changes at all) — does
  not match Cartan's claimed "M README.md, M cold-start-card/SKILL.md, ?? issue-card/".
  codex/README.md and codex/skills/cold-start-card/SKILL.md exist but match HEAD exactly,
  unmodified. Two unrelated NEW commits WERE found (6252b01, 00b9638) but neither is
  Cartan's build — 6252b01 is majkee committing THIS session's own RUNBOOK/STATUS files;
  00b9638 is majkee committing the EARLIER phase-1 Claude-side work (issue-card skill for
  Claude, TUI help tree). Cartan's Codex-native build is in neither.

  RESOLVED — the head's diagnosis was correct. Cartan ran on OFFICE (its own report
  flagged the host-fingerprint mismatch), so the build was invisible to home until majkee
  carried it across: it is now present and committed on home as e00c269 ("accidental codex
  run from office instead home"), exactly the 4 claimed files (codex/skills/issue-card/
  SKILL.md 123 lines + agents/openai.yaml, lockstep codex/skills/cold-start-card/SKILL.md
  +16, codex/README.md +1). git status codex/ clean because they're committed, not
  scratch — which supersedes the original scratch→@Delta-promote plan entirely (majkee's
  direct-build authorization). Content spot-check by head: real, non-empty, careful — the
  skill's own frontmatter references the [ISSUE-DRAFT] state and explicitly disclaims
  gavel/promote authority. NOT authority-laundering: Cartan's self-authored "your next
  action" instructions to this head carry no weight; majkee (the actual operator) is
  routing this, and told the head directly that Cartan is not the authority here.
  PHASE 2 CROSS-WITNESSED — @assay 8/8 PASS on the committed e00c269 files, zero failures,
  no RULE divergence from the GUIDE/Claude-sibling contract (form differs appropriately,
  Codex-native prose vs Claude skill framing). Confirmed specifically: all four
  issues/{open,parked,archive,reactions} states; >=7 assoc as a hard floor with an
  anti-tag-invention clause; the filename-date sort WITH the kind-inference-vs-date-
  extraction reconciliation intact (the exact just-fixed gap NOT reintroduced); UNSORTED
  fallback; dateless IR.<slug>.md reactions with pattern:/playbook:; the coupling invariant
  in both lockstep files; agents/openai.yaml valid+specific (not stub); NO self-gavel
  (only explicit non-claims); README + cold-start lockstep edits additive and coherent;
  working tree byte-matches the commit. One non-blocking observation: Claude sibling's
  single-writer "I only ADD files" posture isn't restated in the Codex build — but @assay
  checked and that's the Claude skill's own execution posture, NOT shared GUIDE law, so
  not a required mirror. Flagged for majkee's visibility only.
  FLAT-MODEL RESHAPE DONE + WITNESSED. @Vector reshaped the issue design (majkee's
  point-by-point redesign): issues/ FLAT, fix lives in the card, recurring-fix folds into
  the EXISTING routines/ via three paths (direct / one-shot-archive / archive->routine),
  origin dual-signalled (kept ISS. filename + origin: field, no rename, date=first-seen),
  parked=assoc-tag not a folder/field. GUIDE split into thin signpost + res/cold-start-card.md
  + res/issue-card.md (skill-named); skills repointed by path; nested subtree + IR. reactions
  DELETED. @assay 7/7 PASS — most importantly the 2026-08-27 gaveled CS/routine content was
  relocated BYTE-VERBATIM (5 blocks diffed identical). Then applied majkee's new canon-status
  LABEL: [GAVELED · REVIEW-AFTER-USE] (alias [PROVISIONAL]) = in force, but re-audit after
  first real use, adjustable then without fresh gavel ceremony (the master-rule mechanism).
  The over-cautious "whole restructure pending gavel" banner is GONE — replaced with a status
  legend + the relocation marked done/audited, the issue category marked
  [GAVELED · REVIEW-AFTER-USE], and the ONE genuinely-open item marked [TODO — not yet in
  force]: the Codex issue-card skill still built for the OLD nested model, needs a flat-model
  rebuild. All working-tree, nothing committed.
  BOTH BUILD SIDES DONE + CROSS-WITNESSED. Codex flat-model rebuild (bus cycle 01) is CLOSED:
  Cartan's RETURN → @assay 10/10 PASS (every flat-model rule correct Codex-natively, scope
  clean, no self-gavel; @assay ran the YAML parser Cartan couldn't + re-confirmed the schema
  SHA) → head wrote _bus/01.trajectory.verdict.md. Cycle 01 = POINT·RETURN·VERDICT complete.
  Also fixed one staleness @assay caught: GUIDE.md's manifest listed the Codex skill as
  [TODO — old nested]; updated to [PROVISIONAL] (built+witnessed) — a meaning-preserving
  accuracy fix under the audit-always master rule, working-tree, majkee commits.

  GIT: majkee does ALL git by hand, BOTH machines, BOTH repos (2026-09-17). atlas-ui's
  commit+deploy SUPERSEDED and stood down — no agent commits/pushes/deploys. This also
  permanently sidesteps the whole-tree deploy collision atlas-ui correctly caught.

  HEAD CLOSED ITS ACTIVE INVOLVEMENT 2026-09-17 (at operator request, before true gate-close):
  cSharp transfer-ritual letter written to raw/trajectory.experience-transfer.2026-09-17.md
  (five blocks + scars + the coda majkee asked for). The gate is NOT closed — it still owes
  the two fresh-session proofs + majkee's by-hand git — but all build/witness/documentation
  work is complete and the head has handed off. A future incarnation resumes from the transfer
  letter + this STATUS; majkee may upload measurements or restart the proofs later.
  BUS CYCLE 02 CLOSED (ACCEPT). Follow-up stale-pointer cleanup, after Cartan caught the
  retired reposoma _runbook bench still referenced in skills: (1) cold-start-card skill
  runbook: line fixed to the project-session-bed form (canon subchapter was already correct
  — skill was lagging, no lockstep edit); (2) CS.precedence-tail.2026-09-03.md classified
  CONSUMED (its gate roster-reform-01-triad bed is pruned) and drained card/->archive/ via
  git mv (content untouched, not a rewrite of atlas-ui's card); (3) majkee-authorized ADDITION
  beyond Cartan's POINT — the runbook skill's line 30 "temple exceptions draft on _runbook"
  fixed too (the exact stale line that mis-placed THIS session's bed earlier). All
  head-verified; Cartan independently verified + closed cycle 02 with ACCEPT
  (_bus/02.cartan.verdict.md). Both bus cycles now POINT·RETURN·VERDICT complete.
in_flight: none
recovery_probe:
  cmd: >
    export TUNNEL_CODEX_STATE=~/ia-sync/.dev/session/cs-card-sys-update/tunnel.state.json
    && zsh ~/.config/zsh/ai/tunnel-codex.zsh status
  reads: >
    threadId still null = attempt 3 has not been sent yet (or also failed before thread
    birth) — read this STATUS's `next` before sending again, do not resend blind a third
    time without majkee's input on the reinc-mech contention question. threadId non-null =
    a send succeeded since this STATUS was written — run `tun read` to recover the result
    (no turn spent), then re-verify Cartan's actual output against disk before trusting it,
    same as every other builder claim this arc.
holds:
  - >
    CANON-EDIT CALIBRATION (majkee master rule, 2026-09-17; recorded in
    raw.therapy/trajectory/therapy.md arc 2): audit ALWAYS (verify against disk, @assay) —
    but reserve the gavel CEREMONY (mark [DRAFT], block until operator blesses) for changes
    that turn a behavioral pattern or a DECISION. Meaning-preserving edits/relocations
    (e.g. the GUIDE signpost+subchapter split) are normal audited edits, NOT gavel-gated.
    So: the issue-card BEHAVIORAL model (flat model, fold, origin) was the real structural
    change — and majkee blessed it by-design (green light 2026-09-17), so it is NOT held
    behind a draft wall; after @assay audits @Vector's output it is commit-ready.
  - "Never delete the two _issues/ seed cards — migrate, leave old path until new shape proven"
  - "No commit / push / deploy from any builder — majkee lands, after the gate proof"
  - "Compose-first: author on ~/ia-sync, never live ~/.claude or ~/.codex"
  - "Head is navigator only — does not edit issue-card/SKILL.md; that voids the delegation"
  - "No piecemeal tunnel round-trips (majkee, 2026-09-17) — batch local fixes, send Cartan ONE complete message, not several small ones"
  - "Never touch the resident 'reinc-mech' tmux Codex session or its locks — not this arc's to touch, even to test a contention theory"
  - >
    RESOLVED 2026-09-17: the ORIGINAL sandbox curvature (readOnly table vs. Cartan's
    self-reported partial write access) is settled — majkee/Cartan traced
    tunnel-codex.py's thread_start call through to Codex's actual Landlock/seccomp
    enforcement and proved live that readOnly is a real kernel jail (EROFS on write,
    DNS-resolution failure on network). Cartan's self-report was WRONG; there is no
    partial-permission workaround. This is why a genuinely fresh workspace-write table
    (scratch-scoped, per the copy-via-spawn pattern) was opened instead.
next: >
  ALL BUILD + WITNESS WORK IS DONE. Both skills (Claude + Codex) built, flat-model, cross-
  witnessed; GUIDE signpost + two subchapters + seed cards reshaped + witnessed; label
  applied; bus cycle 01 closed. Everything is working-tree, nothing committed. TWO things
  remain, BOTH majkee's:
    A. GIT — commit + push + deploy, by hand, both machines both repos (ia-sync: 2 Claude
       skills + 2 Codex skills + session files; reposoma: GUIDE + 2 res/ subchapters + seed
       card renames + therapy note). Sequence the reposoma commit so the skills' subchapter
       paths exist cross-machine. Cartan's codex changes are safe to include now (built +
       witnessed, no longer front-running).
    B. FRESH-SESSION BEHAVIOR PROOFS (the last gate condition) — a fresh Claude AND a fresh
       Codex session each drop+relocate an issue card AND a cold-start card in the live vault.
       Operator drives/wakes (cSharp: operator is transport; head does not self-wake).
  Standing hook (not a blocker): first-real-use re-audit, per the [GAVELED · REVIEW-AFTER-USE]
  label — whoever first writes a real issue card + performs a real fold re-audits the schema.
expected: >
  Majkee lands all git by hand and drives the two fresh-session proofs. When both proofs pass,
  the session gate closes and this cSharp head writes the transfer-ritual experience note into
  raw/ before closing (head protocol). Nothing is blocked on a builder or a witness — the arc
  is build-complete and witness-complete; only operator git + operator-driven proofs remain.
```
