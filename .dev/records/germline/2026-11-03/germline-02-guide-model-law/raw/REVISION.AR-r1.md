---
title: Atlas fresh-reader review — PG-r1 / AS-r1 / GV-r1 (germline-02-guide-model-law)
revision: AR-r1
date: 2026-10-14
by: Atlas · claude · atlas-ui (independent read-only witness, woken by Majkee)
brief: REVIEW-BRIEF.atlas.program-guide-law.md (AB-r1)
authority: evidence only — no gavel, no STATUS edit, no candidate rewrite; Majkee returns this path to Cartan
verdict: FAIL — narrow and additive. PG-r1 and GV-r1 PASS with findings; AS-r1 FAILs the completeness criterion (A1)
---

# REVIEW — Atlas → Cartan (via Majkee) · RETURN shape

## Verdict

**FAIL — narrow and additive. Not a design rejection.**

- **PG-r1 (proposal) — PASS with findings.** It is faithful to the accepted basis (all nine directions
  plus the reader contract). All ten paper cases resolve under its own text, with one inference gap (P1).
  Nothing in it requires a GUIDE, card or vendor file, and it keeps every alternative visible.
- **GV-r1 (gavels) — PASS.** G1–G7 map 1:1 onto the RUNBOOK register (RUNBOOK:147-157). All seven are OPEN
  and none is filled in by inference. W1–W5 accurately record the steering given in the wake.
- **AS-r1 (accounting) — FAIL on completeness.** It misses seven actual files in the old bed's `raw/`,
  one of which is a divergent revision of an adopted source (A1). RUNBOOK:161 and :172 require complete
  source accounting and complete retention, so the gate cannot close on AS-r1.

**To clear:** an additive AS-r2 adds rows for A1, decides P1 (explicit text or an explicit G4 deferral),
and a new SHA256SUMS.review is issued. Re-review then covers only the changed rows, the P2/P4 lines and
T3. The rest of this receipt carries over if their bytes are unchanged.

PASS here means the proposal is adequate and faithful. It is never canon, runtime proof or gate closure.

## Candidate identity (performed: `sha256sum -c SHA256SUMS.review` → 5/5 OK)

| artifact | revision | sha256 |
|---|---|---|
| PROPOSAL.program-guide-law.md | PG-r1 | 9400540da9975db66d34abfe2db331e67056149203b1df7d18fb74c46f0a5eda |
| ACCOUNTING.sources.md | AS-r1 | bc123bf26c2932f7145a52f4788e0f4242dc37b6b5f47a70bad33e866ba27920 |
| GAVELS.program-guide-law.md | GV-r1 | d2405accab42b94e9c321bea2891380a0cd2b9f2d3bbdf0e36a8b90e1ed09e5a |
| REVIEW-BRIEF.atlas.program-guide-law.md | AB-r1 | 88f12259bb831014bb301402eb97025d9ca3027b9b9fd6d20285094f79cecc35 |
| CHECKPOINT.cartan.program-guide-law.md | CP-r1 | 373b3d0caaf0e91b987a599e94fc82c9ccbfd04fbc0cc3dbf72317f18755cbf7 |
| SHA256SUMS.review (manifest) | — | 43ac6b79d5da744094dd6b1e7dca35603a00b57b39c5ff602aa6e7f448165363 (matches STATUS:18) |
| controls (not in manifest) | RUNBOOK c019e70b… · STATUS bd045dc0… (updated 03:17) | |

Repo: `/home/hruzam/ia-sync` main @ `2d6e14a216a8b6379d5aefe806ead10aa66b5460`. Host: office (hostname
hruzam-120922 · /usr/bin/php74 · valet · MemTotal 16131320 kB).

## Inputs actually read

- **In full:** RUNBOOK.md · STATUS.md · HANDSHAKE.md · AB-r1 · PG-r1 · AS-r1 · GV-r1 · CP-r1 ·
  RECONCILIATION (B1) · journal 2026-10-14 (B2) · SOURCE-ACCOUNTING (B14) · my RETURN (B13) and INSIGHT (B10).
  I read the reconciliation, SOURCE-ACCOUNTING, RETURN and INSIGHT earlier in this same session, before the
  brief arrived. Their bytes match AS-r1's baseline, so the read stands.
- **Targeted greps only, used to test specific claims:** germline/README.md (lines 4, 10, 12, 15-18) ·
  sella/GUIDE.md (header:6, :28, :250, :427, :473, plus the "program" vocabulary) · tunnel/res/user-run.md:58 ·
  tunnel-codex.zsh:86, :231 · tunnel-codex.py:795, :1012 · guide-writing/GUIDE.md:67, :95 ·
  slug-directories.md:20 · germline-forge/GUIDE.md:10, :13, :37 · tunnel/GUIDE.md (`--enable` lines).
- **One diff, for A1:** the two countersign revisions (bed-raw versus the v3 S02), compared with `diff`.
- **ZIP member names only** (`unzip -Z1` / `-l`): no member was extracted or read.
- **Not read:** `hypotheses.reconcile-only.md`, in any form. I saw its file name in a directory listing and
  its member name in a ZIP listing. I did not open, hash or extract it.

## Checks performed (non-mutating) versus inspection

Each check below was run, not just inspected:

1. Candidate manifest: 5/5 OK, and the manifest digest equals STATUS:18.
2. All 61 AS-r1 identity rows (`sha256sum -c`): 61 OK, 61 unique paths, and no sealed path among them.
3. v3 root `SHA256SUMS`: 15/15 OK, at digest 640e3069…ff0d. It names no sealed path.
4. v3 tree contents: 18 files in total and 16 under reposoma/ + ia-sync/. The only staged file that is
   missing from the root manifest is `ia-sync/_staging/guide-model/SHA256SUMS`.
5. Root and nested receipts: root PACKAGE equals nested PACKAGE, and root SHA256SUMS equals nested
   SHA256SUMS (`cmp`).
6. Git: status, scoped diff and `diff --check`.
7. YAML frontmatter: all five candidate files parse, and so does the STATUS block (`in_flight: none`).
8. Office inbox listing, presence-board listing and member counts in the ZIPs.

Everything else in this receipt is inspection and reasoning on paper.

## T1–T10 paper walk

The walk uses only PG-r1:297-347 plus the rules it cites. I filled no gaps from memory.

| case | predicted outcome | rationale (PG-r1 line) | holds? |
|---|---|---|---|
| T1 completion | COMPLETED. Note pins state-4 and check-4; receipt written at the granted target; owner state unchanged | controller invariants :307-309 · the table pins freeze-note at 22222222 (:314), and the file stamp is 22222222 (:318) · inputs :326-328 · grant :303-304 · sufficiency :64 | yes. The receipt's "byte identity" field (:141) has no fixture value, which is acceptable on paper |
| T2 missing function | HELD. Selection is unmatched; no scan | :57 and :60. The table is the only index | yes |
| T3 stale stamp | HELD before operation. **Supported only by inference**, see P1 | :69-71 says the table pins the function token, but the only explicit runtime reject is for a *caller-supplied* pin (:73). The `global` row (:107) does not list a stamp mismatch | partial |
| T4 scope collision | global selected; the project package contributes nothing | :114-116 | yes. See P3 for the probing question |
| T5 unavailable project | HELD. This is not confirmed absence; no fallback | :110-112 and :108 | yes |
| T6 incomplete grants | HELD. The missing write requirement is named; no helper, no card | :154-156 and :311 | yes |
| T7 confirmed absence | global fallback, with the absence evidence in the receipt | :108, :110 and :140 | yes |
| T8 broken local package | HELD as an incomplete local package; no borrowing or fallback | :60, :108 and :112 | yes |
| T9 ghost file | structural finding; translate-note still fails selection; the ghost is never loaded | :58-59 and :57 | yes |
| T10 owner-state failure | HELD. The state-5/state-4 mismatch or `verified=false` is named; no write; the owner's pen is untouched | :93-94 and :308-309 | yes |
| function→function preload (extra) | sufficiency defect. Structural review rejects it; fold the function or merge it | :65-66 and :87-88. Fixture :324 says "No other function is read" | yes |

Shared invariants load before dispatch (:80). The grain test applied at :344-346 is consistent with G3. No
case depends on a GUIDE, private card or vendor file.

### G4 S1/S2: discussed, not chosen

Disclosure: S1 comes from my own INSIGHT §4.1 (Houston's "specialise, never replace"). Discount my framing
of it accordingly.

- **S1 cost to weigh:** germline README:10 regenerates a random 8-hex stamp on every edit. If `specialises:`
  pins a stamp, any global edit, even a typo, stales every specialised project package, which then holds.
  PG-r1:121 pins a "controller revision" instead, while INSIGHT said "@ stamp". G4 must say which, because
  the two give very different currency costs.
- **S2 cost to weigh:** a project package can silently drop a global invariant. That is detectable only if
  the invariant also exists as an explicit lock that the caller passes in as owner input (:125-127).
  Otherwise drift is structurally invisible.
- **Neither option lets in a mixed-scope overlay.** PG-r1:131-133 and :116 forbid it, and the fixture
  grants neither (:346-347). I accept no overlay by implication.

## Findings: proposal (PG-r1), ranked

- **P1 (medium): runtime stamp-mismatch rule is implicit.**
  - Where: PG-r1:69-74, :104-108; T3 at :336.
  - Defect: the only explicit runtime reject is for a caller-supplied pin (:73). A mismatch between the
    table's expected stamp and the file's observed stamp is named at structural review (:202) and in the
    `project-first` row (:108). It is not stated as a rule at selection for `global` or `project`, yet T3
    predicts a hold.
  - Fix, either way: state it in P2 ("a function whose observed stamp differs from its table row is not
    loaded; HELD"), or mark it explicitly as G4-open and qualify T3's expected result. INSIGHT §4.2 proposed
    the explicit rule.
- **P2 (low): no paper case for an omitted scope or an escaping path.**
  - Where: :100 and :113-114.
  - Defect: an omitted scope is an unresolved selection, and a function path that escapes the package is
    invalid. Both rules are stated, but neither has a paper case.
  - Fix: optionally add T11/T12. This is not required for adequacy.
- **P3 (low): does an explicit `global` request probe the project scope?**
  - Where: :115-116.
  - Defect: "If both scopes contain the slug, the receipt names both" assumes the resolver knows the
    project scope. That is undefined when only `global` was requested, and so is whether a declared
    project root is needed at all. T4 passes either way.
  - Fix: state this, or list it under G4.
- **P4 (low): illustrative commands in a GUIDE can drift.**
  - Where: P6, :175-178.
  - Defect: "An example must not become a second maintained recipe" has no hook that makes drift visible.
  - Fix, a candidate only: an illustrative command that mirrors a program function points at that
    function by `<slug>/<fn>`. Leave it to the audit or G2.
- **P5 (low): one tunnel invariant is missing from the audit list.**
  - Where: P8, :279.
  - Defect: the list names operator-only enable, single-writer and read-before-retry. It omits the
    explicit state-path gate (HANDSHAKE:189-190: `--state` or `TUNNEL_CODEX_STATE`, else exit 13) and the
    never-unlink-writer-locks rule on `close` (HANDSHAKE:173-178).
  - Fix: add both as audit subjects.

**Fidelity confirmed:**

- Directions 1–9 and the reader contract appear at P1:20-24, P2:64, P3, P5:151-168 and P6:184-185.
- The journal B2:17-19 open families are all present as G1, G5, G6 and G7.
- The "drops 'or lacks'" scope lean matches P3:82-83.
- P8's seams are real on disk: Sella header:6 says DRAFT/G3-HELD, :250 puts playbooks in skill bodies,
  :427 and :473 call pulse the doing-state, and the "program" sense sits at :18 and :129.
- The tunnel drift is real: user-run:58 says there is no trim, against zsh:86 `compact` and py:795
  `--override`.
- The tunnel-user entry is described as a loader only, with no enable grant, no implicit sender and no
  card dependency (:284-289).
- The audit-only next session is a proposal only (:229-237). No germline-03 bed exists in
  `.dev/session/`.

## Findings: accounting (AS-r1), ranked

- **A1 (major, the blocking finding): seven actual files in the old bed's `raw/` are not accounted.**
  - Where: AS-r1:71-128 has no rows for them.
  - What is missing:
    - `raw/guide-model.table.2026-10-13-v3.zip` (199ca591…a5). This is the v3 archive itself.
      RECONCILIATION:36 and :50-51 name it as preserved evidence. It has 18 file members and no sealed
      member.
    - `raw/POINT.Cartan-to-Atlas.germline-02-reconciliation.2026-10-13.md` (fe2b04ac…a5). This is the
      brief my RETURN answered; RETURN:3 cites it.
    - Bed-raw copies of the four Symmetry/WAVE reviews. RECONCILIATION:19-20 names them in "Read with".
      - The addendum (f774588a…), batch-verification (0112d2ee…) and verification-return (ec6461f9…) are
        byte-equal to S01, S03 and S04. The WAVE files use dotted names.
      - **The countersign diverges.** The bed-raw copy (11e73bcc…a25) is the **pre-ruling** revision:
        "SIGN WITH CONDITIONS" with R2 "one decision for majkee". The v3 S02 copy (6bfb00f8…) is the
        **post-ruling** "SIGN; ruled 2026-10-13: whole-tree pass first".
      - S02 adopts the R2 whole-tree-first lesson (AS-r1:48). The provenance of that ruling exists only in
        the v3 revision. AS-r1 should name both revisions and state which one carries the adopted claim.
    - `raw/hypotheses.reconcile-only.md`. It is correctly left unread, but it has no "sealed, unread,
      declined by name" row. Only the sealed ZIP member is mentioned (B8, AS-r1:88).
  - Why it blocks: closure needs every bed-level input accounted (RECONCILIATION:46-55; RUNBOOK:161 and
    :172). By the letter, prompt-0:81-87 did not name these files. By the gate's criterion, they count.
- **A2 (low): B7's member count is wrong.**
  - Where: AS-r1:87.
  - Defect: it says the earlier table ZIP has "13 non-directory members". `unzip -Z1` shows 14: 2 PACKAGE
    files, 2 RUNBOOKs, census, census.py, 6 src files and 2 raw reviews.
- **A3 (low): several "named use" cells are generic.**
  - Where: AS-r1:98, :101, :104-108, :116-119, :121.
  - Defect: these rows (AGENTS, deploy.sh, HANDSHAKE, journal, PROTOCOLE, pulse, SYNC_DISCIPLINE and the
    runbook/status law) share one cell text. It says nothing specific about, for example, deploy.sh's
    additive-ghost listing, which P2:58-59 relies on. B19 (the Claude doorway) also reuses "Codex
    source/live compare equal", which applies to B4 and B20, not B19.
  - Fix: tighten the wording. Nothing is wrong in substance.

**What holds:**

- S01–S16 match the 16 staged files on disk exactly.
- The 15-versus-16 explanation is correct (AS-r1:28-36), and so are the root and nested equalities.
- The R01/R02 dispositions are sound.
- Retain, reinterpret and decline follow source precedence.
- Every superseded topology is named: GUIDE-as-controller, BACKGROUND slot, res/ functions, the four
  skill deltas and the old launchers.
- The later-fold table (AS-r1:130-139) names a destination and an authority for each row, and none is
  executed.
- The dated vendor leads are framed as leads only (AS-r1:141-157).

## Gavel register (GV-r1)

No defect. W3–W5 are recorded without locking a choice (GV-r1:29-31). The acceptance table shows NOT MET
and no implementation authority (GV-r1:72-74).

One note for Majkee: G4 hides the stamp-versus-revision pin question inside S1 (see above). Please surface
it explicitly.

## CP-r1 claims attested

| claim (CP-r1 line) | result |
|---|---|
| office frame (:12-13) | **verified**: hostname, php74, valet and MemTotal 16131320 kB match exactly |
| office inbox empty (:13) | **verified** at review time |
| presence id a409df1f… attached (:14-15) | **not verifiable now**: the id is absent from `~/reposoma/_active/`. That is consistent with a later unmark; I can't attest it |
| reconciliation retains its starting bytes (:20-21) | **verified against the AS-r1 baseline** (2a50e8ab…). The bytes from before his wake are outside my reach |
| five-file manifest (:24-26) | **verified** |
| 61 named hashes equal (:30-32) | **verified**, but the claim is "named". It is true and **not** a completeness claim (see A1) |
| 15/15 at 640e3069…; 16 staged; nested = root; PACKAGE equal; 18 total (:33-37) | **verified**, all of it |
| 43 non-v3 rows plus 61 identity rows; T1–T10 present; seven OPEN (:38-41) | **verified** |
| `git diff --check` clean; scoped live diff empty; the reconciliation is the only tracked change; new files are in the bed only (:42-44) | **verified**. Git status shows ` M` reconciliation plus `??` bed files only |
| no Atlas receipt; brief not consumed (:45-46) | true until this file. **This receipt is the consumption stamp** (HANDSHAKE:35-39) |

## Remaining limits

- This is a paper walk. It proves nothing about runtime loading, permission enforcement, compaction,
  placement, vendor facts or the measurement of the whole guide tree. PG-r1:214-227 correctly lists these
  as later conditions.
- My source spot-checks were targeted greps, not full reads of Sella, the germline-forge guide, the tunnel
  guide or the shim.
- I did not read the older Symmetry/WAVE review bodies beyond the countersign diff, so the adopted R1, R2,
  R4, R5, F3, F4 and F7 claims are accepted as AS-r1 characterises them.
- Conflict of interest: S1, the ghost/table rule and the receipt naming come from my own INSIGHT.

## Re-review conditions

- **Any change to a candidate's bytes** voids the identity table above. Review the changed lines plus every
  case or finding they touch.
- **AS-r2 adding A1's rows**: review those rows only.
- **PG-r2 settling P1**: review P2/P4 and T3.
- **A changed planning basis** (B1/B2 hash) or **any live-surface diff**: full re-review.

## Untouched

I wrote only this file. I did not touch RUNBOOK, STATUS, the candidate files, any source, the old bed, the
ZIPs, canon, germline/claude/codex/zsh, deploy, git, presence or pulse. I spawned nothing and made no model,
tunnel or network call. The sealed file stays unread.
