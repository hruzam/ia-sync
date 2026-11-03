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

---

# AR-r2 addendum — focused re-review · 2026-10-14

AR-r1 above is preserved byte-for-byte. It equals `REVISION.AR-r1.md`, checked with `cmp` before this
append. Brief: AB-r2. Revision: **AR-r2**. Same seat and limits as AR-r1. No candidate, STATUS or manifest
was edited.

## Verdict AR-r2

**PASS — the r2 candidate is adequate and faithful.**

- The AR-r1 blocking finding (A1) is cleared.
- P1–P5 and A2–A3 are each resolved or correctly routed to an open gavel.
- G1–G7 remain OPEN (7 of 7 rows read "OPEN — not supplied").
- Two new low findings below are wording only. Neither blocks.

PASS covers proposal adequacy, fidelity and completeness of the bounded input accounting. It is not canon,
runtime proof, a gavel or gate closure. Gate closure still needs Majkee's explicit G1–G7 decisions.

## Reviewed identities

Performed: `sha256sum -c SHA256SUMS.review` → 13/13 OK. Manifest digest
`5cbaf9bcc2702e8e43fd5677c11c6b35ce67ba3165bcf29212678f894f68fa87`, which matches STATUS:25.

| artifact | revision | sha256 |
|---|---|---|
| PROPOSAL.program-guide-law.md | PG-r2 | faea695a66765b0f6d59627d82e6809ddfcd14c5a7da792e552f4288ed60bcee |
| ACCOUNTING.sources.md | AS-r2 | ee9e77c2b0fbeaee982a55262ee3eb0dd16cebd39f2a3a23794ca920ad9f7650 |
| GAVELS.program-guide-law.md | GV-r2 | ba1e6998d7472bf1c9300e56d0180bb60422a4afee433a3c3f29d917892c2cbd |
| REVIEW-BRIEF.atlas.program-guide-law.md | AB-r2 | 2feced5c20893e36c4f4b92dd38298ecf8e078a971bda45e608846777f31163d |
| CHECKPOINT.cartan.program-guide-law.md | CP-r2 | 2cf1c4e919da77d47efa49400073209d4a4731d4642d26e5cda7f0153e4d518a |
| DISPOSITION.atlas.program-guide-law.md | DR-r1 | ba8f3a98cdfbcd084239c0b299b3518e1963f7f6989b035afeac11bbd7ca04ff |

The six REVISION.*-r1 snapshots and `SHA256SUMS.review.r1` hash exactly to the AR-r1 identity table, so the
snapshot mapping is verified. Controls: RUNBOOK `c019e70b…` is unchanged; STATUS is `21b5348e…` (03:45).
Repo main is at `2d6e14a`.

## Reads and checks

**Read:**
- RUNBOOK (unchanged since AR-r1) and STATUS in full; AB-r2 and DR-r1 in full.
- HANDSHAKE: unchanged since AR-r1 (its hash is inside the verified 67), so the earlier read carries over.
- **Full `diff` of PG, AS, GV and CP against their r1 snapshots.** Only the changed hunks are newly reviewed.
  Unchanged text keeps its AR-r1 coverage under the AR-r1 limits.

**Performed:**
1. All 67 AS-r2 identity rows OK: 67 unique paths, and no sealed path among them.
2. A name-coverage loop over every regular file directly in the old bed's `raw/`: 14 of 14 named exactly once.
   I never hashed or opened B50.
3. My AR-r1 receipt is unchanged: `cmp` against `REVISION.AR-r1.md` before this append.
4. YAML frontmatter parses for all six current artifacts.
5. Git: `git diff --check` is clean and the scoped live-surface diff is empty. The pre-existing
   reconciliation is still the only tracked change.
6. Targeted greps to test changed claims:
   - deploy.sh :3, :58, :143, :213-215 (for B21);
   - journal.host-cleanup.md :13, :22, :27-28 (for B25);
   - SYMMETRY-CATALOG :10 (for F-r2-1).
7. A `find` over /home/hruzam for `symmetry-drop*` returned nothing (for F-r2-1).

The v3 15/16/18 counts and the ZIP member counts (18 and 14) were measured in AR-r1. Their underlying bytes
are inside the 67 that verified unchanged, so those results carry over.

**Not read:** the sealed file, in any form.

## Dispositions checked

| AR-r1 id | r2 change (path:line) | result |
|---|---|---|
| A1 | AS-r2:77-79, :127-141, :199-215 | **cleared.** B44–B50 are present. 14/14 old-raw names are covered; the remaining 10 map to B1, B10–B15 and B45. B46–B48 are byte-equal to S01, S03 and S04. B49 (:132) correctly attributes the post-ruling R2 to S02 and never to the older copy. B50 (:133) is a name-only row and is kept out of every checksum list. The sealed member in the old ZIP is still B8 only |
| A2 | AS-r2:89 | **cleared.** 14 members, kept distinct from B44's 18 |
| A3 | AS-r2:88, :100-110, :118-123 | **cleared.** Every cell is now specific. B19 (:101) no longer makes a Codex equality claim. I verified B21 against deploy.sh :213-215 (`--delete` only with `-n`, inventory only) and B25 against journal :28 (office DONE, home pending) |
| P1 | PG-r2:75-80, :113-114 | **cleared.** The table-versus-file stamp check is explicit for every scope before the procedure loads. A missing caller pin cannot make a mismatch loadable (:77). It is labelled as a candidate pending G4 (:79), and GV-r2 G4 asks Majkee to accept or amend it |
| P2 | PG-r2:362-363 | **cleared.** See T11 and T12 below |
| P3 | PG-r2:122-127 | **cleared.** An explicit global request needs no project root and runs no probe. A collision is only a supplied fact. Optional probing is exposed in G4 and is not a hidden input |
| P4 | PG-r2:192-194; GV-r2 G2 | **routed correctly.** The rule is labelled a proposal and is not binding law |
| P5 | PG-r2:298 | **cleared.** Explicit state-path selection and never-unlink-writer-locks are added |
| G4 pin | PG-r2:146-150; GV-r2 G4 | **surfaced and unchosen.** The cost of each pin type is stated: a stamp pin stales on every edit, including typos; a semantic pin needs its own compatibility review. S1 and S2 are both still open, and no overlay is implied |

## Affected paper cases (PG-r2 text only, no runtime)

| case | predicted outcome | rationale |
|---|---|---|
| T3 (:354) | **HELD before procedure load.** Expected 22222222 and observed 22222223 are both recorded; no fallback | it now follows directly from :75-78 and the global row :114, so no inference is needed |
| T4 (:355) | global selected; the project package contributes nothing; the receipt records the supplied collision and the reason | :122-127. No project root is required |
| T11 (:362) | **HELD**: an unresolved selection before any package is loaded | :100 (omission ≠ precedence) and the T11 row |
| T12 (:363) | **HELD** for invalid confinement before the function loads; no external read | P4's confinement sentence (unchanged from r1 :113-114) and the T12 row. It also fails "package-relative file" in P2's table |

T1, T2 and T5–T10 are literally unchanged, so their AR-r1 predictions carry over. The function-to-function
preload result also carries over.

## New findings (low, non-blocking)

- **F-r2-1: unsupported "extracted package" claim.**
  - Where: AS-r2:137 ("the earlier extracted symmetry package remains preserved and cataloged by B15/B8"),
    echoed in CP-r2:95 ("Originals and extracted trees remain in place").
  - Defect: SYMMETRY-CATALOG:10 names the extraction directory `symmetry-drop-2026-10-13/guide-model/`, but no
    such directory exists anywhere under /home/hruzam. The claim is unverified and may be false. The only
    extracted tree I can confirm is the v3 tree.
  - Fix: cite an actual path, or reword to "catalogued by B15; extracted location not inventoried/not found in
    this gate". This is an accounting statement, not a law defect.
- **F-r2-2: second presence id not on the board.**
  - Where: CP-r2:15-16 (presence id `8a9493b2…`).
  - Status: not on the board at review time, same as AR-r1's a409 item. Consistent with a clean unmark, and
    not attestable by me.

## CP-r2 claims attested

- **Verified:** 67 unsealed identities; 14/14 old-raw names with B50 name-only; S01–S16 unchanged; 15/16/18
  carried over through unchanged bytes; B46–B48 equal and B49 differs; the snapshot mapping; my receipt
  unchanged; T1–T12 present; seven rows OPEN; YAML; scoped diff empty; `diff --check` clean.
- **Not attestable:** the presence id (F-r2-2) and the before-state at the start of this wake beyond the AS
  baseline.
- **Unsupported:** "extracted trees remain in place" for the symmetry-drop extraction (F-r2-1).

## Carry-over and remaining limits

- **Carry-over:** AR-r1 coverage applies only to text that is literally unchanged between r1 and r2, which I
  confirmed by `diff`. It applies under AR-r1's limits: paper only; targeted greps, not full reads of
  Sella, germline-forge, tunnel or the shim; older review bodies not rechecked beyond the countersign diff;
  my conflict of interest on S1, the ghost/table rule and receipt naming.
- **Not covered by this paper review:** runtime loading, enforcement, compaction, vendor facts, placement and
  the whole-tree audit. All of them remain unperformed.

## Re-review conditions

- **A change to any of the six current hashes:** review the changed hunks and the cases they touch.
- **A fix that only rewords F-r2-1:** a one-line check, not a re-review.
- **A change to the B1/B2 planning basis or any live surface:** full re-review.
- **Majkee's G1–G7 decisions, if one amends candidate text:** re-review that amendment only.

## Untouched (r2)

I made only this append. Not touched: candidates, DR, STATUS, RUNBOOK, manifests, snapshots, sources, ZIPs,
canon, live surfaces, git, presence and pulse. No spawn, no network, model or tunnel call. The seal stays
unread and unhashed.

# AR-r3 addendum — amended-candidate and source review · 2026-10-14 19:05 CEST

AR-r1 and AR-r2 above are preserved byte-for-byte: the receipt equalled `REVISION.AR-r2.md` (`cmp`) before
this append. Brief: AB-r3 `01af2b9a…` with CB-r2 `61f81621…`. Revision: **AR-r3**. Same seat, same office
host (hruzam-120922, `/usr/bin/php74` present), repo main `2d6e14a`. No candidate, STATUS, manifest, note or
source was edited.

## Verdict AR-r3

**PASS with one closure condition (C1).** The amended PG-r3, AS-r4 and GV-r4 are adequate on paper. They
render all seven decision sections faithfully, and the source accounting is complete and verified.

- G1, G2, G3 and G6: PG-r3 changes only labels. Each recommended r2 candidate is now "accepted" and nothing
  else moved (diffed against `REVISION.PG-r2.md`). My AR-r2 coverage of that text carries over.
- G4, G5 and G7 amendments: these are newly reviewed. All of T13–T23 hold. T1–T12 still hold under the
  revised P2/P4.
- **C1 (closure-holding):** F-r3-1. The exceptional G4 line leaves open where its qualified binding and
  pin live, and how they coexist with the normal global row. Before final acceptance this needs either a
  text fix or Majkee's explicit deferral in words. Under PG-r3:88 a deferral is fail-closed and safe.
- F-r2-1 one-line check: **PASS** (see its section below).
- The other findings are low and do not block.

PASS means planning adequacy only. It is not canon, runtime proof, a composer/loader/native-table result,
a final gavel or gate closure. Closure still needs Majkee's acceptance of the reviewed revision.

## Reviewed identities

Performed: `sha256sum -c SHA256SUMS.review` → 32/32 OK. Manifest digest
`f0243bee8cc5602b7718cebe252e6baed0c39a3214451113b38fee4610c72615` = STATUS checkpoint.

| artifact | revision | sha256 |
|---|---|---|
| PROPOSAL.program-guide-law.md | PG-r3 | ecc6566c7be19659177a8ca0a1b1c7b374046b40aa147918017b0f6a9ab9cbf5 |
| ACCOUNTING.sources.md | AS-r4 | 6a1cc469ab55353ab7724d27a7c4b62ec2591f1b30c6b1b929eebdec5c09654b |
| GAVELS.program-guide-law.md | GV-r4 | 0ec78c049862e0ccd0699da1b320d7b8dedd3e68c77d55543400e8803aaa3434 |
| REVIEW-BRIEF.atlas.program-guide-law.md | AB-r3 | 01af2b9a296ba3e1523b1fdbf6af2a6295ba7ead0e1f981224a8f9bfa51840e4 |
| CHECKPOINT.cartan.program-guide-law.md | CP-r4 | fcf2df3c7138ee1405962f7ef7f5151f6c1d639e35180762bd4c43e5df9ed678 |
| DISPOSITION.atlas.program-guide-law.md | DR-r3 | c90a63043a770bfc3e4d8ad31824af3bfb759dfe48384a0b2838dd2a09710b66 |
| CHECK-BRIEF.atlas.F-r2-1.md | CB-r2 | 61f816216e332d35098b0c72d60c2d968b20867c2837d0e7acbc474bea59a34b |
| DECISIONS.majkee.program-guide-law.md | note | 6f985206ec6735c4200a3b7bfaef0cbc5d47a1e2d113d379198bc6339a5d60b6 |

Controls: RUNBOOK `c019e70b…` is unchanged since AR-r1. STATUS is `b9e183cf…` (18:34). HANDSHAKE is
`9e9309d8…`, unchanged and pinned in AS-r4. The decision note equals `REVISION.DECISIONS.majkee.2026-10-14.md`
(`cmp`).

## Reads and checks

**Read in full:** RUNBOOK, STATUS, AB-r3, CB-r2, the decision note, PG-r3, GV-r4, DR-r3 and CP-r4.

**Read in part:** AS-r4, specifically the header, B1/B2/B10/B15/B51–B53, the F-r2-1 paragraph, the
transitions, the fold table and the identities. AS-r4 rows not touched by the amendment carry over from
AR-r2, because the 70-hash check below proves their sources are unchanged.

**Diffs:**
- PG-r3 vs PG-r2: whole file, with P1/P3/P5/P6 examined section by section.
- B52 vs B53.

**Spot reads of current law:**
- slug-directories `:18–48`.
- RECONCILIATION (B1) `:80–86`.

**Performed (non-mutating):**
- *32-entry manifest and the five carried note identities.* All match retained snapshots: PG-r2
  `faea695a`, GV-r3 `f8433c2e`, AS-r3 `c00fad13`, AR-r2 `ced60304`, DR-r2 `3108c2d9`.
- *Verbatim check by script.* Each of the seven `## G#` sections of the note is an exact substring of
  GV-r4 → 7/7 VERBATIM.
- *Own isolated probe, `python3 -I`.* 70 AS-r4 rows: 70 unique, 70/70 sha256 equal, none sealed. 53 B
  rows. Old raw/ holds 14 files, and all 14 names are covered. The listing used names only; B50 was never
  opened or hashed.
- *B2 owner file.* `/home/hruzam/reposoma/.majkee/journal/2026-10-14.md` is `80238103…` now and clean in
  reposoma git at `fc65a8b`. B52 differs from B53 only by 7 appended lines: a gavel-loop observation that
  points to B51 and claims no authority. No planning-direction text differs.
- *git.* Only the two known tracked-dirty paths. The Houston TEST-INSTALL file is still `f68f01fc…`.
  Scoped diff over germline, claude, codex, zsh, deploy.sh, pulse.md, AGENTS.md, SYNC_DISCIPLINE.md and
  journal.host-cleanup.md is 0 bytes. No trailing whitespace in the six current bed documents.

**Not witnessed:**
- The myShell gavel loop.
- Cartan's first B2 observation at `418f22b5…`. I verify only that the B52 reconstruction hashes to the
  value claimed. Who changed or restored B2 is not attributed.

## Decision-source fidelity

- **GV-r4:49–52 states.** G1/G2/G3/G6 are ACCEPT; G4/G5/G7 are AMENDMENT RECEIVED — REVIEW PENDING. The
  date (2026-10-14) and source hash are recorded. "Closed" wording is correctly not treated as closure
  (GV-r4:55–57; note G4/G5/G7 "Review consequence").
- **G7:** Majkee's own words name the shape (`<guide-slug>/{GUIDE.md,src/journal-...}`, "not same journal
  … 'our vault'"). The carried ruling and PG-r3:239–250 are faithful to them.
- **G4/G5: see F-r3-3.** The quoted operator words support:
  - split possible but not expected;
  - a mechanism should exist;
  - the whole line is loaded agent-side;
  - "gaveled as sharpened".

  The following details come from carrier translation only:
  - which direction is allowed and which is forbidden;
  - the "composer" name and its proof list;
  - the native-table limits.

  That translation ratifies a myShell framing that is not recorded ("That is correct", "closed in this
  shape", "sharpened by you"). The note itself says the translation is not new authority (note:17–20). I
  do not contest the content. Its authority rests on Majkee's final acceptance of the reviewed PG-r3 text.

## Paper walk — T1–T23 (explicit fixture inputs only, PG-r3 text)

| case | prediction from PG-r3 | holds? |
|---|---|---|
| T1 | global/global line + named owner/task inputs suffice (P2:72–74, P3:105–110) | yes |
| T2 | not in table → HELD, no scan (P2:62, :68) | yes |
| T3 | `22222223`≠`22222222` → HELD before load, with or without caller pin (P2:81–86) | yes |
| T4 | explicit global + supplied collision → global only; recorded, not probed (P4:127–129) | yes |
| T5 | no root/access evidence ≠ absence → HELD (P4:125–126, table :123) | yes |
| T6 | partial grant → HELD missing write (P5:182–184) | yes |
| T7 | accessible root + exact absence → global, absence in receipt (P4:123, :125) | yes |
| T8 | local controller, missing fn → HELD, no borrowing (P4:122–126) | yes |
| T9 | unindexed file = ghost, never loaded (P2:66–67) | yes |
| T10 | state-5 vs state-4 / verified=false → HELD, pen unchanged (P3:108–109) | yes |
| T11 | omitted scope → HELD unresolved (P4:117) | yes |
| T12 | `fn/../../outside.md` escapes owning root → HELD (P2:63–64, P4:152–155) | yes |
| T13 | explicit request + both scopes/paths/ids + qualified row + receipt + 44444444 match → eligible; capability/state checks remain (P4:131–145) | yes, on stated inputs, but see F-r3-1 |
| T14 | no compatibility result → HELD (P4:143–144) | yes |
| T15 | local ctrl + global fn → HELD even with PASS (P4:148) | yes |
| T16 | global request, local file, no composition request → global/global (P4:127) | yes for controller toy-1 only (F-r3-1) |
| T17 | contradiction/unknown/stale → HELD, no tidier fallback (P4:143–144) | yes |
| T18 | native row maps a selected function to mechanism + qualification/evidence → in bounds, no grant (P5:192–201) | yes |
| T19 | branches/discovery/routing in native table → invalid (P5:195–201) | yes |
| T20 | owner-proposed src/journal with maintenance only → in bounds, not served (P6:239–249; slug law :47) | yes |
| T21 | required step only in journal → invalid sufficiency/one-home (P2:72–74, P6:244) | yes |
| T22 | 44444445 vs 44444444 → HELD, no global-pin reuse (P2:81–88) | yes |
| T23 | receipt names function absent from table → HELD (P2:65–66, P4:154–155) | yes |

Every outcome above is a paper prediction from the fixture inputs. None is runtime, composer or loading
evidence.

## Findings AR-r3, ranked

**F-r3-1 (medium, C1, fix or explicitly defer) — the qualified binding has no defined home or pin source,
and its coexistence with the normal row is undefined.**

- *Where the pin comes from is unclear:*
  - P2:65–66 says the exception is "represented/qualified by that same function index".
  - The T13 fixture (PG-r3:416–419) puts a project-specific local token (`44444444`) in the *global*
    controller's single selected row.
  - P2:87 ("an explicit qualified binding must supply an agreeing local pin") and T22 ("row/receipt")
    leave open that the task or composer receipt supplies the pin instead.
- *What each reading costs:*
  - If the global table carries per-project stamp pins, every local edit forces a global controller edit
    and a deploy to both hosts.
  - The global controller would also start enumerating project specialisations.
- *The untested case:* T16 uses controller toy-1, while T13 uses toy-composition-2 at the same path. So an
  ordinary global request against the *qualified* controller has no determinable outcome. Either the normal
  global binding coexists, which needs two bindings per id that P2:63–64 does not describe, or global
  callers are HELD because the function has no global binding.
- *What it is:* this is the narrowed residual of the PG-r2 S1/S2 and stamp-vs-semantic pin question. It is
  not S1-vs-S2 any more. The amendment already maps complete scoped lines (S2-like) to *normal*, and pinned
  specialisation (S1-like) to *exceptional, measurement-only*. PG-r3:163–168 overstates what remains open.
- *Remaining parameters, which I do not choose:*
  - (a) pin home: global row vs task/composer-supplied;
  - (b) pin kind: per-edit stamp vs semantic/contract;
  - (c) whether the qualified row coexists with or replaces the normal row.
- *How to clear it:*
  - Cartan states the open parameters and adds a paper case under the qualified controller (an ordinary
    global request) whose outcome follows from the text; **or**
  - Majkee explicitly defers (a)–(c) to germline-03/04 measurement.
- *Effect of a deferral:* until it is resolved, PG-r3:88 ("missing/ambiguous qualification holds") makes
  every exceptional line HELD. That is a stated, fail-closed effect, not hidden law. Normal-line law is
  unaffected.
- *Conflict of interest:* S1 and pinned specialisation came from my INSIGHT; the conflict is disclosed
  again. This finding asks for a choice or deferral and does not favour S1.

**F-r3-2 (low, route) — the G7 src/ seam is understated.**

- PG-r3:252–254 describes the clash only as "src/ is outbound staging".
- Current law (slug-directories:28–35) also says src/ "exists only while a change is being prepared, and
  **empties when it lands**".
- The same lines record a lean that src/ may fold into raw/ and retire.
- A persistent history journal there conflicts with that transience. Its content (process observations)
  also resembles raw/'s inbound role (:21).
- Majkee chose the path explicitly, so this does not block. The routing should say plainly that the G7
  shape needs a later slug-law amendment by the guide-writing owner (redefine src/ or carve out
  `src/journal-…`), and that the src→raw retirement lean must not silently remove it. Live examples:
  `meeting/src`, `sella/src`, `tunnel/src`.

**F-r3-3 (low, route to final gavel wording) — the G4/G5 carrier translation was ratified, but the
framing it ratified is not recorded** (see Decision-source fidelity). Majkee's final acceptance should name
PG-r3 P4/P5 (or the successor hash) explicitly, not just the note. That turns the translated direction
rule, composer proof list and native-table limits into reviewed operator decisions.

**F-r3-4 (low, route) — the native binding table has no currency relation to the public function.**

- P2's mismatch-HELD covers the public function file.
- A native row adapting an older function revision (changed requirements or evidence) has no stated stale
  check.
- PG-r3:209 already defers the schema. Add a sentence that a native row records the public function
  identity it adapts and that a mismatch holds, or name this explicitly among the deferred placement
  details. T18/T19 do not exercise it.

**N-r3-1 (nit) — P2:82, "and the verified line receipt".** This can read as requiring a composer-style
receipt for normal lines too. Suggest "the line's selection receipt (and, for qualified composition, the
composer receipt)". It has no outcome effect.

## Seams checked (no finding)

- **RUNBOOK vs proposal.**
  - RUNBOOK:142–143 ("mix project/global package components") and B1 RECONCILIATION:84 ("never mix local
    and global components") predate G4.
  - RUNBOOK:39–40 makes final resolver details subject to a recorded gavel, and G4 is that gavel.
  - PG-r3:157–161, GV-r4:143–147, DR-r3:38–42 and AS-r4 B1/B10 keep the operational no-mixing hold for
    this bed, so nothing is assembled or loaded.
  - The exception is not silent production permission, a mixed fallback (T14/T17), a second index (T23)
    or a dropped invariant (P4:142, :149–150).
  - Adequate. The final STATUS should restate that G4 supersedes B1:84 for the proposal, not for this bed.
- **G5 vs thin-loader direction.** The table is translation, qualification and evidence only. It does not
  touch the harness programmatically and creates no procedure home, index or grant (P5:192–212). The
  public controller stays the sole index (P5:199). Consistent.
- **G7 vs G2.** res/ survives (PG-r3:246–247). The journal is not resolver-served, matching slug
  law :47. No pen, no mandatory journal, no vault/program journal. Consistent.
- **Normal-line pin policy.** The per-file stamp with universal mismatch-HELD (P2:77–88) is the candidate.
  Majkee's acceptance of PG-r3 accepts it, including the currency cost noted in AR-r2. If Majkee wants a
  semantic pin for normal lines, that must be said; it is not a separate open row.
- **Source movement.** B2 is now at its reviewed bytes (`80238103`). The transient append is preserved
  (B52) and carries no basis content. B1 is equal (within the 70). AR-r2's "changed B1/B2 basis → full
  re-review" condition is met by this full review in any case. It is reported, not waived.

## F-r2-1 one-line check (CB-r2)

**F-r2-1 at AS-r4 `6a1cc469…` / CP-r4 `fcf2df3c…`: PASS.**
- AS-r4:146–151 and CP-r4:40–42 say the earlier symmetry extraction is catalogued by B15/B8 but not found
  or inventoried here.
- The v3 tree and the original archives are named separately.
- There is no blanket-preservation or Cartan full-home-search claim, and grep finds none of the old
  "remains preserved / extracted trees" wording.
- This covers that wording only.

F-r2-2 is unchanged: the historical presence `8a9493b2…` is not attestable and stays a note only.

## CP-r4 claims attested

All attested:
- host, HEAD, note hash and five identities;
- 7/7 verbatim;
- pre-decision manifest `5b79ad77…` pinned as a snapshot;
- 70/14/B50 name-only;
- both B2 snapshot hashes;
- Houston file `f68f01fc…` unchanged;
- scoped live diff empty;
- no helper/table/journal created (no such files in the bed or in the scoped live paths).

Not independently attestable: CP-r4:13 presence id `0c227101…`, and Cartan's own first B2 observation.

## Carry-over and remaining limits

- AR-r2 carries over only for text that did not change: G1/G2/G3/G6 sections, T1–T12 inputs and
  unaffected AS rows, with its limits. G4/G5/G7 coverage is new and here only.
- Unperformed:
  - native loading;
  - effective permissions;
  - compaction;
  - official vendor facts;
  - composer, native table or journal behaviour;
  - deployment placement;
  - the whole-tree guide audit.

  Paper sufficiency cannot prove these.
- Source bodies beyond the named spot reads were not re-read; they are identity-verified only.
- Conflict of interest around S1 is disclosed (F-r3-1).

## Re-review conditions

- **Only F-r3-1 text plus a new case changes:** focused check of those hunks only.
- **Majkee explicitly defers F-r3-1 (a)–(c) with no text change:** no re-review. Cartan records the words.
- **Any other candidate change:** check the changed hunks.
- **F-r3-2/F-r3-4/N-r3-1 wording-only fixes:** fold into the same hunk check.
- **B1/B2 basis or a live surface changes:** full re-review.

## Untouched (r3)

Only this append. Not touched: candidates, DR, CP, STATUS, RUNBOOK, manifests, snapshots, the decision
note, sources, B2, ZIPs, canon, live surfaces, git, presence and pulse. No spawn, no network, model or
tunnel call. The seal stays unread and unhashed.
