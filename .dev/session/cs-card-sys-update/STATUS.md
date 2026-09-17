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
  - "GUIDE (reposoma canon) edits are DRAFT until majkee gavels — no self-lock (0002 F4)"
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
  Two exit-30 failures on the new table, cause of the second one undiagnosed (possible
  contention with the unrelated resident reinc-mech Codex session — not confirmed, not
  acted on). Majkee's call: retry a third send as-is, wait for the resident session to
  finish/idle first, or investigate the coordination lock further before retrying. Once a
  send actually succeeds and Cartan returns real scratch output: @assay reviews it first,
  @Delta promotes (mechanical copy) into ~/ia-sync/codex/skills/, @assay re-verifies the
  promoted copy is byte-identical to what it reviewed.
expected: >
  A successful phase-2 send, Codex-native issue-card surface drafted into
  /tmp/cartan-sandbox-test/codex/skills/issue-card/, reviewed, then promoted into
  ~/ia-sync/codex/skills/, cross-witnessed by @assay. Gate stays open until BOTH
  fresh-session proofs (Claude + Codex, drop AND re-locate an issue card and a cold-start
  card) close it, and majkee actually gavels the GUIDE.
```
