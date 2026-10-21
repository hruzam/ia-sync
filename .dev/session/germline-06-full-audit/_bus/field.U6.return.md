---
from: field · unit U6 · date 2026-10-21
task: GUIDE layering — Sella and Germline Forge vs the system as it is
---

## A. File/section inventory

| path | lines | frontmatter: verified / half_life_days / banner | sections read |
|---|---|---|---|
| germline-forge/GUIDE.md | 150 | verified: 2026-10-07 · half_life_days: 30 · banner line 13 (STALE, 2026-10-14) | ALL (§0–§7, Sella anchor, Manifest, Lineage) |
| germline-forge/res/checks.md | 89 | verified: 2026-10-07 · no half_life_days · NO banner | ALL (§1–§5) |
| germline-forge/res/fold-scheme.md | 77 | verified: 2026-10-07 · no half_life_days · NO banner | ALL (§1–§5) |
| germline-forge/res/witness.md | 52 | verified: 2026-10-07 · no half_life_days · NO banner | ALL (§1–§5) |
| sella/GUIDE.md | 404 | verified: 2026-09-01 · half_life_days: 42 · NO banner | ALL (manifest, boundary, §0–§6, glossary) |
| guide-writing/GUIDE.md | ~127 | verified: 2026-09-04 · no half_life_days · — | staleness/banner rule only (frontmatter shape block, lines 80–95) |
| findings.g06.md | 68 | — (prior evidence) | "Guidance pass" and "E4 vendor facts" sections only |

Glob germline-forge/**: six files found — GUIDE.md, res/checks.md, res/fold-scheme.md, res/witness.md, raw/observations.atlas-ui.2026-10-07.md, raw/note.atlas-ui-to-carrier.2026-10-07.md. No manifest, README, or index file present beyond GUIDE.md. The two raw/ files are listed in GUIDE.md §Manifest as "raw (uncanonical)" — not read per BRIEF scope.

---

## B. Claim table

**germline-forge/GUIDE.md**

| line | claim (quoted) | type | status | note |
|---|---|---|---|---|
| 13 | "⚠ STALE in part (2026-10-14, atlas-ui): §0–§3 describe the pre-2026-10-10 model … Superseded by the Houston runtime-load fold (2026-10-10) and germline-01" | pointer | current | banner self-declares scope of stale content |
| 18 | "Sella says WHY … This guide says HOW, dated. Where they disagree, Sella wins and this guide is stale." | doctrine | current | explicit subordination law; layer claim |
| 28 | "render/<vendor>/<slug>.md = identity ⊕ addendum ⊕ binding, byte-copied into three marker pairs" | procedure | superseded-model | no render/ directory in current source; GUIDE banner covers §0–§3 |
| 59–61 | "identity … ~/reposoma/.germline/agents/<slug>/identity.md … ~/.germline symlink … deploy.sh has no .germline leg by design" | dated fact | stale | germline-01 (GO 2026-10-12): source ~/ia-sync/germline/ → real ~/.germline/; deploy.sh copies it; fold-scheme:26 is the canonical location of this claim |
| 88 | "on claude 2.1.292 a child can spawn and inherits the parent's effective permissions — the runtime does not fence a child; the card must" | dated fact | current | L16.14 confirmed; spawn fencing in card still required |
| 98–103 | "Behaviour is proven only by a fresh session, witnessed by a seat that authored none of it (L16.8)" | doctrine | current | |
| 109–113 | "The operator names destinations … copies source and render … the global render reaches both machines through deploy.sh" | procedure | superseded-model | runtime-load: no render copy step; global wrapper deploy via deploy.sh still applies |

**germline-forge/res/checks.md**

| line | claim (quoted) | type | status | note |
|---|---|---|---|---|
| 4 | "commands run in zsh from the package root during the Houston forge (three freezes); each failure mode below was observed" | dated fact | superseded-model | all three checks reference render/ paths |
| 14–15 | "git hash-object — germline/agents/<slug>/identity.md project/<project>.md binding/claude.md … render/claude/<slug>.md render/codex/<slug>.md" | procedure | superseded-model | render/ no longer exists; check meaningless as written; byte-check principle could transfer to wrapper |
| 28–36 | six diff lines against render/<vendor>/<slug>.md marker sections | procedure | superseded-model | no marker-wrapped renders; body equality principle not applicable |
| 50–55 | stamp currency script reads "first body line = stamp" from render/$r/<slug>.md | procedure | superseded-model | runtime wrappers carry a canary (binding.claude.md:23) not a three-element stamp; script not portable |
| 87–88 | "batch frontmatter edits with body edits and declare 'final' — a vendor partner recomposes once, not after every metadata touch" | doctrine | superseded-model | no partner composition step in runtime-load; lesson still valid as a discipline norm |

**germline-forge/res/fold-scheme.md**

| line | claim (quoted) | type | status | note |
|---|---|---|---|---|
| 26 | "~/reposoma/.germline/agents/<slug>/identity.md … ~/.germline is a host symlink … deploy.sh has no .germline leg by design" | dated fact | stale | same as GUIDE.md:59–61; no banner on this chapter |
| 28 | "(proposal — no global forge has used it yet)" re global bindings | dated fact | stale | CONFIRMED at fold-scheme:28 per findings.g06 UPDATE 2026-10-21; global bindings live: binding.claude cf14943f, binding.codex 0c812f6c |
| 40 | "The /agents wizard is removed in claude 2.1.292" | dated fact | stale | E4: removed before 2.1.281; exact version not found; wizard is absent but version claim wrong |
| 43 | "Codex 0.160.0 exposes --profile, not --agent" | dated fact | current | E4: --profile CONFIRMED (conf M) |
| 45–46 | "deploy.sh is additive rsync per leg … never touches .germline or config.toml" | dated fact | stale | germline-01: deploy.sh now has a .germline copy leg |
| 48–49 | "The runtime artifact is not the render. Claude: a copy of the render at the destination." | procedure | superseded-model | runtime-load: wrapper is not a render; identity loaded by wrapper via tool-read at runtime |

**germline-forge/res/witness.md**

| line | claim (quoted) | type | status | note |
|---|---|---|---|---|
| 9 | "law: the author does not witness (L16.8). A subagent the author spawns is a PRE-CHECK … a witness is a seat spawned or woken by someone else" | doctrine | current | |
| 12–16 | test copy placed/removed by witness; "record: client version · host · date · render blob · test-copy cmp · P3 marker" | procedure | current | "render blob" means deployed wrapper blob in runtime-load; mechanism still applies |
| 28 | "the /agents wizard is gone; identity is behavioural" | dated fact | stale | wizard gone (CONFIRMED); claimed in witness proof row context; exact version wrong (per E4) |
| 38–43 | rules 1–4 (one prompt per row; verbatim or secondhand; witness declarations as hard as behaviour; runtime does not fence a child, card must) | doctrine | current | |
| 45–47 | "Exactly the witness's 'may claim' list … Nothing the witness did not observe … A later freeze that changes only metadata keeps the claims; a body change … reopens the proofs" | doctrine | current | |

**sella/GUIDE.md**

| line | claim (quoted) | type | status | note |
|---|---|---|---|---|
| 7 | "verified: 2026-09-01; half_life_days: 42" | dated fact | stale | past due ~2026-10-13; no banner added |
| 129–131 | "agents = programs, skills = methods, harness = OS … the compiler is stochastic and drifts" | doctrine | current | |
| 150–153 | "KERNEL … agent .md definition … USERLAND … CLAUDE.md … skill BODY (loaded at trigger)" | doctrine | current | predicts tool-read identity enters userland, not kernel |
| 185 | "paging | compaction: skill bodies survive 5,000 tokens each, 25,000 combined, newest first; CLAUDE.md re-injected from disk" | dated fact | CONFIRMED (E4) | |
| 214 | "background | true = always background (background default since v2.1.198)" | dated fact | CONTRADICTED (E4) | docs/changelog: default since 2.1.232 |
| 275–277 | "NO dry-run/trace mode exists on the platform (verified 2026-08-02) — there is no bash -x analog" | dated fact | partially CONTRADICTED (E4) | claude --debug, /doctor, /context exist as partial inspection; too strong as stated |
| 293–298 | "Only the kernel layer survives inattention … CLAUDE.md is a user message and compaction prunes userland; the kernel is the only resident memory." | doctrine | current | predicts runtime-load identity (tool-read) degrades at compaction; Sella offers no mitigation |
| 444 | "→ build / fold / prove / promote procedure, dated: raw.guides/germline-forge/GUIDE.md (DRAFT 2026-10-07)" | pointer | current | pointer still resolves; pointed guide is partially stale |

---

## C. H1–H7 evidence tables

**H1 — banner in GUIDE.md; absence in res/***

CONFIRMED. GUIDE.md:13 carries: `> **⚠ STALE in part (2026-10-14, atlas-ui):** §0–§3 describe the pre-2026-10-10 model (build-time render files, body-equality checks) and §2 the reposoma home + ~/.germline symlink. Superseded by the Houston runtime-load fold (2026-10-10) and germline-01 (majkee GO 2026-10-12: source ~/ia-sync/germline/ → deployed real ~/.germline/). Current truth: ~/ia-sync/germline/README.md. Re-distill pending.`

checks.md frontmatter (lines 1–5): `chapter-of: germline-forge · title: … · verified: 2026-10-07 · commands run in zsh from the package root during the Houston forge` — no banner, no half_life_days.
fold-scheme.md frontmatter (lines 1–5): same pattern; no banner.
witness.md frontmatter (lines 1–5): same; no banner.

All three chapters describe render-model procedures without a staleness marker, while the GUIDE's own banner declares §0–§3 superseded. The chapters are §0–§3 content made concrete.

**H2 — checks.md: render model vs runtime-load**

| check | still meaningful | verdict | runtime-load twin needed? |
|---|---|---|---|
| 1 verify_cmd (checks.md:14–15) — hash render/ files against README manifest | No — no render/ files | MEANINGLESS as written | yes: hash source files (identity.md, binding.md) against an equivalent manifest |
| 2 body equality (checks.md:28–36) — diff render/ marker sections vs source bodies | No — no marker-wrapped renders | MEANINGLESS as written | yes: compare deployed wrapper vs identity + binding (cmp or diff) |
| 3 stamp currency (checks.md:50–55) — first body line of render pins source blobs | No — wrapper carries a canary (binding.claude.md:23), not a three-element stamp | MEANINGLESS as written; principle transferable | yes: canary check (wrapper's canary = binding's declared canary) |
| §4 who/when (checks.md:68–73) — carrier before dispatching a POINT | No — no multi-writer render package | MEANINGLESS for runtime-load | replaced by: deployer verifies hash before deploy.sh push |
| §5 composition pipeline (checks.md:77–85) — pipeline script for composing render | No — no composition step | MEANINGLESS | replaced by: deploy.sh copy leg (already exists) |

**H3 — witness.md vs G01 PASS rule**

G01 PASS rule (from findings.g06 E4/RECONCILE.G01): tokens + transcript reads + model/effort; child transcript not relay.

| G01 component | witness.md counterpart | match / gap |
|---|---|---|
| tokens | not stated | GAP — witness.md records client version and render blob, not token count |
| transcript reads | line 11: "carrier relays replies verbatim (first ~5 lines)"; rule 2 line 39: "Verbatim or secondhand" | PARTIAL match — "verbatim first ~5 lines" is a surrogate; G01 names "transcript reads" as a distinct PASS dimension |
| model/effort | "client version" (line 15) | PARTIAL — version recorded, effort not |
| child transcript not relay | line 11: "carrier relays replies verbatim" implies relay is the mechanism; G01 explicitly disallows relay for PASS | MISSING — witness.md makes relay the standard mechanism; G01 disallows it |

Extras in witness.md not in G01 PASS: test copy placement/removal (§1); P3 write-check marker; author ≠ witness law (L16.8); verbatim → secondhand marking; §4 "verified: may say" contract. These are procedural detail G01 presupposes.

**H4 — Sella L1/L7: tool-read identity; compaction re-read**

L1 (sella:248–252): `"Identity and ground-truth declarations → kernel (agent .md, skill description)"` — predicts that identity must reside in kernel to retain authority.

L7 (sella:293–298): `"Only the kernel layer survives inattention … CLAUDE.md is a user message and compaction prunes userland; the kernel is the only resident memory."` — under runtime-load, identity.md is loaded by a wrapper via tool-read; that content enters as a tool result in userland, not kernel. L7 directly predicts such identity content does NOT survive compaction.

Sella nowhere discusses the tool-read identity loading pattern or whether tool results survive compaction. No mitigation offered. No test described.

E4 finding (reused): tool-read content — up to 5 recently read files ≤5k tokens each are re-read after compaction; larger → path reference; subagent .md body survival undocumented (conf M). identity.md is ~2.5k tokens (likely under cap) but competes for the 5-file slot with later reads. L7's prediction stands as a concern but the mechanism is testable (E4 P1).

**H5 — Sella vendor-dated facts (carry from E4)**

| location | claim (quoted) | E4 classification |
|---|---|---|
| sella:185 | "5,000 tokens each, 25,000 combined, newest first; CLAUDE.md re-injected from disk" | CONFIRMED |
| sella:214 | "background default since v2.1.198" | CONTRADICTED — default since 2.1.232 |
| sella:275–277 | "NO dry-run/trace mode exists on the platform (verified 2026-08-02)" | partially CONTRADICTED — inspection tools exist |
| fold-scheme:40 | "The /agents wizard is removed in claude 2.1.292" | CONTRADICTED — removed before 2.1.281; exact version not found |
| fold-scheme:43 | "Codex 0.160.0 exposes --profile, not --agent" | CONFIRMED (conf M) |
| witness:28 | "the /agents wizard is gone" | CONFIRMED (absent); version attribution wrong |
| GUIDE.md:7 (frontmatter) | "witnessed by assay on claude 2.1.292; Codex routes per codex-cli 0.160.0" | 2.1.292 as test version is a fact; codex-cli 0.160.0 NOT FOUND in docs |

Note: omitClaudeMd and background contradictions are in fold-scheme.md and Sella respectively; neither is in the witness or checks chapters. E4 confirms Sella paging row is the one dated fact in Sella that is CONFIRMED.

**H6 — Layering claims; guide-writer law compliance**

Does either guide say which statements are law vs reference vs pointer?

Forge GUIDE.md:18: `"not: a new Sella law. Sella says WHY … This guide says HOW, dated. Where they disagree, Sella wins and this guide is stale."` — explicitly labels itself as a HOW/procedure guide subordinate to Sella doctrine. No per-claim labeling.

Sella frontmatter `precedence:` (sella:12): distinguishes doctrine (Sella wins) from volatile CLI/vendor facts (dated live source wins). L8 (sella:300–305) further distinguishes behavioral doctrine from version claims. But individual claims within the body are not labeled law/reference/pointer — the reader infers from context.

guide-writing/GUIDE.md staleness rule (lines 80–95): requires `verified: YYYY-MM-DD` on every guide; volatile content → `half_life_days:`, `recheck:`, `verify_cmd:`; chapters carry only `title:` + `chapter-of:`. No explicit requirement for a staleness banner.

Compliance:
- Forge GUIDE.md: `verified`, `half_life_days`, `recheck` all present → COMPLIANT with fields; manual banner is above requirement.
- Forge res/*.md: carry `title:` + `chapter-of:` per chapter rule → COMPLIANT with the chapter header rule; no `half_life_days` required by law; but content is stale without a banner — the law does not require a banner, only the fields; the gap is the operator's to fill.
- Sella GUIDE.md: `verified`, `half_life_days` present → fields COMPLIANT; past due since ~2026-10-13 with no banner — law does not mandate a banner, but `half_life_days` implies the `/guide` staleness organ would flag it.

**H7 — Agent-need vs human-explanation; GUIDE↔germline duplication**

| rule (GUIDE location) | GUIDE claim type | germline location | same / diverged |
|---|---|---|---|
| "the author does not witness (L16.8)" — witness:9 | doctrine for the witness seat | identity.md:79–82 "No self-confirmation. Fresh architecture eyes … check new or reopened locks, any breaks, consequential design I authored" — Houston-specific scope | DIVERGED in scope: witness.md states a universal forge law; identity.md states a Houston-specific audit rule; the principle overlaps but neither cites the other |
| "the runtime does not fence a child; the card must" — witness:40, GUIDE:88 | doctrine for card authors | identity.md (via binding.claude.md:19 — tools allowlist `Agent`; identity implies "no card spawns an executor" per BRIEF) | SAME in effect; germline operationalizes it; GUIDE names the law; no text duplication |
| "Promotion = reviewed merge, never auto-deploy" — GUIDE:109–113; Sella:443 | doctrine for operators/builders | NOT in germline; promotion is an operator act, not an agent rule | no duplication needed — agent has no promotion authority |
| "Stamp currency / canary rule" — checks.md:47–63 | procedure for package builders | binding.claude.md:23 "canary … re-rolled whenever the wrapper body changes; echoed as first line of entry proof" | DIVERGED: checks.md describes a three-element stamp on renders; binding.claude.md carries a single canary for runtime detection; different mechanism, related purpose |
| "Card selection — explicit card: line; no silent default on main session" — identity.md:57–59 | doctrine for agents (runtime rule) | identity.md:57–59 directly | germline IS the authoritative location; GUIDE does not restate this rule; no duplication |
| Sella L7 "identity/limits in kernel" — sella:293–298 | doctrine for primitive builders | NOT in germline (germline is the kernel artifact; the law is for its builders, not for Houston at runtime) | no duplication; correct separation |
| Sella L9 "Anchors, not full reads" — sella:307–312 | doctrine for primitive builders | NOT in germline | correct; agents follow this by receiving anchors, not by stating the law |

---

## D. GUIDE↔germline duplication map (summary)

No verbatim text duplication found between Forge/Sella GUIDE content and germline source files. Three structural relationships:

1. **GUIDE carries builder procedure; germline carries runtime rule.** Example: GUIDE checks.md carries the three build-time checks; germline binding.claude.md carries the canary rule. Related purpose; different mechanism; no overlap.
2. **GUIDE carries doctrine; germline operationalizes it.** Example: Sella L7 says identity must be in kernel; germline's loader design is the operationalization; neither restates the other.
3. **One rule diverged in scope.** Witness.md:9 states the "author does not witness" law universally; identity.md:79–82 states a Houston-specific "no self-confirmation" rule for audit work. The GUIDE law is broader; germline rule is narrower. An agent asked to witness another agent's forge would find no explicit authority in germline — only in GUIDE.md.

---

## E. Friction for a seat that reads the GUIDE first (ranked, cited)

1. **Stale canonical paths with no banner on the chapters.** A seat reads fold-scheme:26 ("~/reposoma/.germline/agents/<slug>/identity.md … ~/.germline is a host symlink") and treats it as the live destination. GUIDE.md has the banner but the chapter has none; a seat reading the chapter directly (via `/guide germline-forge fold-scheme`) gets no warning. Impact: deploy to wrong path; fail to find live identity. Source: fold-scheme:26; contradicted by AGENTS.md germline-01.

2. **Three checks are described as operative; all three reference render/.** A seat asked to "run the three checks" on a current package will execute shell commands that reference paths that do not exist (`render/<vendor>/<slug>.md`). Zero exits are guaranteed — but for wrong reasons (no render = no mismatch found). Source: checks.md:14–15, 28–36, 50–55. No runtime-load equivalent offered.

3. **Witness PASS criteria incomplete relative to G01.** A seat writing a witness brief from witness.md alone will omit token counts, model/effort record, and will use relay as the transcript mechanism — all of which G01 disallows or augments. Source: witness.md:11–15 vs findings.g06 E4/RECONCILE.G01 PASS rule.

4. **Sella past half-life, no banner.** A seat reads Sella's paging row, background default, and /agents claim without knowing the guide is past due. Two of three are CONTRADICTED. Source: sella:7 (verified 2026-09-01), sella:214 (background CONTRADICTED), fold-scheme:40 (/agents CONTRADICTED).

5. **Fold-scheme §2 table row for global bindings says "(proposal — no global forge has used it yet)".** Global bindings are now live. A seat designing a new forge would treat global bindings as unproven prior art. Source: fold-scheme:28; contradicted by findings.g06 UPDATE 2026-10-21 (CONFIRMED at fold-scheme:28).

---

## F. Uncertainty / not-read

- **germline-forge/raw/ files not read.** `raw/observations.atlas-ui.2026-10-07.md` (31 dated lessons, GUIDE §7 source) and `raw/note.atlas-ui-to-carrier.2026-10-07.md` — not read per BRIEF scope; may contain additional procedure claims.
- **Sella src/ and raw/ receipts not read.** The Sella GUIDE points to [S1]–[S5] in `raw.research/` — not read; vendor-dated claims classified using E4's already-verified findings only.
- **guide-writing GUIDE.md read partially.** Only lines 80–127 read (staleness/banner rule). The manifest law and writer rules were read (lines 58–127); other sections (read-order, discipline note) not examined.
- **germline identity.md read to line 90.** The spawn-fencing rule ("no card spawns an executor") is referenced in the BRIEF as living in identity; confirmed in spirit via binding.claude.md:19 tools list; the exact identity line was not reached in the read window.
- **Claims from findings.g06 E4 carried as prior evidence without re-fetching.** Epoch's vendor doc readings (official docs 2026-10-21) accepted as stated; no independent web check performed per BRIEF instruction.
- **fold-scheme:43 "omitClaudeMd" not found.** E4 cites fold-scheme as a location for omitClaudeMd; reading fold-scheme found no such mention. Line 43 reads: "Codex 0.160.0 exposes --profile, not --agent; files in .codex/agents/ configure spawned sessions." The omitClaudeMd claim in E4 may refer to a different file or a misattribution; classified UNVERIFIABLE from this read.
