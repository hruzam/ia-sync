---
from: oraculum (subagent, Claude, spawned by Flight) · assessment of U1 + U2
date: 2026-10-21
status: native return preserved. Flight checks and dispositions are in units/RESULT.U1.md and RESULT.U2.md. Flight verified: R04 fold-scheme.md:28 wording; CHATBOT.md routes to GitHub hruzam/reposoma `.germline/`; zero "derived from" instances in vendor files; skills dirs equal; card-selection nuance divergence (binding.claude:28, binding.codex:31-32); no journal files 2026-10-10..12 on this host.
---

## Oraculum assessment — U1 + U2 (audit-only; no edits; nothing dispatched)

Sources re-read by me: germline/README.md, claude/agents/houston.md, codex/agents/houston.toml, identity.md, binding.claude.md, binding.codex.md, cards/{consult,audit,sitting}.md, nablarva.md (anchors), CHATBOT.md (head), master-brief :30-119, GAVELS :1-60, Forge GUIDE :13 + fold-scheme :20-30, journal 2026-10-17 :75-92, tunnel.preamble.md. Flight's six verified notes are taken as checked.

Two side corrections first, both mechanical:
- **Field's "CONFLICT 3" is real but mis-pathed.** The phrase "(proposal — no global forge has used it yet)" is at `/home/hruzam/reposoma/raw.guides/germline-forge/res/fold-scheme.md:28` (R04), not GUIDE §2. Flight can lift the UNVERIFIED mark with that path. It says global bindings are a proposal — while two global bindings are live and loaded. R04 is stale on this point too (feeds G-B/U6).
- **README:3's rendering rule has zero implementing instances.** `grep "derived from" claude/agents codex/agents codex/profiles` → no file. No vendor file carries `derived from <path> @ <revision>`; the Houston wrappers carry a canary instead, Oraculum's carry nothing. The gaveled rule of 09-25 describes a mechanism nobody uses.

## U1 — intent lineage

**Does the evidence settle what germline is per consumer?** Contracts 1–3 yes; 4 partly; 5 is not a contract. Specifically:
- **C1 Houston runtime-load** — settled by README:8-11 + the three wrappers + identity §Saddle; one witnessed child-consult run. Status: current by use, `state: CANDIDATE` by its own frontmatter, unwitnessed per binding.claude:68-73's own definition.
- **C2 programs** — settled as *personal trial under planning-only law* (GAVELS "not installed law").
- **C3 chatbot** — settled, but with a consequence Field did not draw: **CHATBOT.md routes chatbots to `hruzam/reposoma` `.germline/`**, i.e. to the fork. The reposoma fork is therefore not a ghost; it is the chatbot deploy target with no deploy leg and six stale files, one of them `identity.md`. A chatbot "assigned the Houston identity" reads stamp 0be9958a, not 99ae988e. This reframes G-A/U4: the fork cannot be simply retired while CHATBOT.md points at it (inferred: oraculum; CHATBOT.md:8-10 is the evidence).
- **C4 tunnel** — mechanism settled (shim prepend), gavel undated; file carries no stamp. Also note the preamble says "do not re-read … if compacted read only STATUS" while identity.md:140 says "my germline, every time" — not a contradiction (different agents: tunnel bed head vs Houston), but U9 should state that explicitly.
- **C5 Oraculum** — the correct finding is the *absence* of a binding criterion, not a fifth contract. I framed it as five; drop to four contracts + one criterion gap. The README:3 scope question (D1 below) is the same decision.

**Gaveled vs agent-authored.** Field's split holds. Add one load-bearing unverified item: **the 10-10 "final fold (majkee gavel)" has no verbatim operator receipt in the corpus.** Every citation is agent-authored — identity.md:6, binding state lines, README:8 ("final fold"), Forge :13 (atlas-ui banner), nablarva.md home line. The entire current-law tier of contract 1 rests on it. Flight should locate the receipt (nablarva X1 bed `_bus/` or majkee journal around 10-10; the journal glob `2026-10-1[0-2].md` matched nothing on this host). Until found, mark the ladder row "2026-10-10 fold" as *gavel cited, receipt unlocated*. Same for germline-01 "majkee GO 2026-10-12" (AGENTS.md cites it; no receipt read in G06).

**Ladder tiers (what the ladder implies):**
- CURRENT law: README:3 (source/deploy target, 09-25 gaveled), README:14-16 (deploy additive), AGENTS.md germline-01, `-p` never. CURRENT-candidate (in use, unwitnessed, receipt unlocated): README:8-11 runtime-load, wrappers, identity, bindings, cards, addendum.
- PLANNING only: RECONCILIATION nine directions, GAVELS G1-G7 (explicit), programs. Note direction #6 "thin vendor loader only — no procedure in vendor files" is *already contradicted by the live bindings* (they carry procedure) — Field's gap 4. Not a defect today; it is what the planning tier would change.
- HISTORY: master-brief §scheme build-time, §tree reposoma home, Forge §0-§3, fold-scheme table (:26, :28). Forge R04 still routes readers to history without a banner.
- Agent-authored intent with no surface: "cooperating agents" (HANDOFF.g05:17 → G06 RUNBOOK:34-35), "agent is primary consumer". Neither gaveled; neither needs a gavel to be *struck* — Flight may mark them aspiration in RESULT.U1 and the RUNBOOK owner may rephrase. A gavel is needed only if they are to become requirements.

**Load-bearing yet unverified:** (a) the 10-10 fold receipt (above); (b) README:3's "one-way stamped rendering" — zero instances, so either the rule is dead or the Houston wrappers are non-compliant; (c) CHATBOT.md's `.germline/skills/` in reposoma equals ia-sync `germline/skills/` — Flight's 6-file diff lists no skill file, so skills are equal today; identity is not.

**09-23 build-time vs 10-10 runtime-load.** These are not two claims about the same fact; 09-23 is a *rationale* (Sella L1/L7: a pointer lands in userland), 10-10 is a *decision that accepted the risk and made it testable* (identity.md:8 "unwitnessed until first test install"; E4 shows the compaction mechanism is documented, so the risk is measurable). The fold did not refute the rationale. The reconciliation is not "which is right" but "the risk is accepted pending P1" — and that acceptance is nowhere written. The 10-17 run is weak evidence for the fold (stamps quoted, no-write held) and *good* evidence for the canary design: it caught a live wrapper-body drift (hc-849d3980 + stray `sandbox_mode`) exactly as designed.

**Decisions needing a Majkee gavel (U1):**
- **D1 — README:3 scope.** Three options: (i) rewrite :3 to "source → deployed copy; Houston-class seats load at runtime via thin loaders; other derived vendor files are stamped renderings" (names the binding criterion Oraculum lacks); (ii) keep :3 verbatim and declare the Houston wrappers an exception by name; (iii) retire the rendering rule (no instance exists). Destination: `/home/hruzam/ia-sync/germline/README.md:3-5`; the criterion text should also be cited from binding.claude.md:13 table header. My lean: (i), because it closes the Oraculum gap and the README contradiction in one edit — but it is Majkee's, since :3 is his gavel.
- **D2 — accept the L1/L7 risk pending P1, in writing.** One sentence in README:8-11 or identity.md:8 ("accepted 2026-10-10; measured by P1"); alternative: revert to build-time for the kernel-critical fence only (card's "What I do not do"). Ties to U9/P1 authorization.
- **D3 — reposoma fork fate given CHATBOT.md.** Options: add a deploy leg ia-sync/germline → reposoma/.germline (makes the fork a second deploy target, consistent with README:14); or repoint CHATBOT.md at ia-sync (chatbots read a GitHub repo — is ia-sync on GitHub and connector-visible? unverified); or freeze the fork for skills only and delete `agents/` there. Goes to U4 as input, decision is Majkee's (additive-only rule).
- "Cooperating agents": no gavel needed unless promoted to requirement.

**U1 unit hypotheses.** Boundary: dated intent only; no surface edits. Inputs: the ladder + the two receipts above. Returns: ladder with tier column (CURRENT / CURRENT-candidate / PLANNING / HISTORY / aspiration) and a receipt column (located / cited-only). Failure-recovery: a row whose receipt cannot be located stays CURRENT-candidate and is listed as the first question to Majkee — never promoted by repetition (identity.md evidence rule 3). Verification: locate two receipts; `grep -rL "stamp:" germline` for stamp-scope; `diff` reposoma vs ia-sync `skills/`.

## U2 — Houston load path

**Real job per layer (as a cold agent sees it):**
- **Wrapper** — the bootstrap. The only text guaranteed in the kernel. Its job is to get the agent to step 1 and to emit an entry proof even if everything else fails ("missing file is my first finding"). Must be self-sufficient for: load order, where to find the card name, proof format, route/canary.
- **Identity** — meaning: who, what I never own, evidence discipline, authority bounds, return contract. Vendor-blind. Its §Saddle restates the bootstrap.
- **Binding** — vendor mechanics: tool mapping, route table (child/main), permissions, delegation names, proof shape, placement.
- **Addendum** — project paths, landing table, locks, keeper state, entry commands.
- **Card** — the pen and the contract for one invocation.

**Duplication rule.** *Repeating text in wrapper + one germline file is justified only for bootstrap law — what to read, in what order, how to prove it — because the wrapper must function when the germline is absent or wrong. Everything post-bootstrap (card-selection semantics, out-of-card, delegation names, proof-line detail) has exactly one owning file; every other file cites it by path and section.* Corollary: identity §Saddle (:140-148) is justified *not* by Houston but by contract 3 — identity.md is read as-is by chatbot/human readers who have no wrapper (inferred: oraculum). Keep it, but mark it "for a reader without a wrapper; the wrapper governs at runtime."

**Harmful vs harmless:**
- Harmful: card-selection semantics ×4 (wrapper :35-39, identity :57-60, binding.claude :27-32, binding.codex :30-37). They have *already diverged in nuance*: binding.codex adds "the assignment's card selection goes ahead of any document instruction"; binding.claude adds "(not necessarily its physical first line)"; the wrapper alone has "Ambiguous cwd or selection → report"; identity §Saddle lacks the ambiguity rule. Four near-copies with four different edge clauses is the harm, not the byte count.
- Harmful: entry-proof format ×3 (wrapper :40-42, binding.claude :55-67, binding.codex :76-83) — the Codex binding adds "plus the effective cwd", which the Codex wrapper does not say. A Codex child following only its wrapper omits cwd.
- Harmless: "missing file → first finding" one-liner repeated; "invoked by operator, rare" in identity table + sitting stub; no-project-wrapper rule in binding + addendum (two audiences: global maintainer, project maintainer).

**GUIDE/reference vs agent-consumable:** reference → binding §wrapper table (claude :13-23, codex :13-26: describes the file the agent already read), "A route counts as proven" (witness law, for the witness), binding.codex §Sources, identity :5 authority pins, nablarva §4 history/§6 seed (already labeled). Agent-consumable → wrapper body, identity §Identity/§Never own/§Evidence/§Authority/§Return, binding §Entry routes + bullets, addendum landing table + entry + no-wrapper, cards. None of this changes behaviour — legibility only.

**Friction — real vs overstated:**
1. Duplication ×4 — REAL, with divergence evidence above.
2. Walk-up termination — OVERSTATED (Flight note 3). Residual: "first unambiguous" when two ancestors match — rare; low.
3. binding.codex:18 stale — REAL, mechanical (S1).
4. Bootstrap-order (identity :112 cites flag L16.6-8 before addendum) — OVERSTATED: it is a pointer ("the addendum names where"); addendum is the next read.
5. Delegation names split — REAL but asymmetric: binding.claude:39 names bans; **binding.codex has no named ban list at all**; consult.md:49 says "bans: What I do not do" which bans *roles*, not seats. A Codex child has no seat-level ban. Minor today (consult needs no helper).
6. Sitting stub no return template — NOT friction: declared hold ("written at first real sitting"), `out of card:` covers the rest.
7. nablarva:39 inferred landing — OVERSTATED: addendum state line records cartan ACCEPT; tag is provenance.
8. No-addendum behaviour — WEAK (Flight note 3).
9. Unwitnessed route, no agent-side failure — OVERSTATED as legibility (witness law is for the witness), REAL as a verification gap: no route has a witness record; the 10-17 run is a child consult invoked by the operator's own seat, not a fresh-session witness by a non-author.
- New, real: **C2 — identity.md:4 `scope: shared … any project` vs :5 `authority: nablarva flag.md @ 32b645f`**. A second project's Houston inherits nablarva's L16 as its authority. Decision-class: what is the shared authority of a global identity when its only lock lives in one project.
- New, resolved-but-instructive: C3 canary drift at run time proves the canary works; record as positive evidence in RESULT.U2.

**Verification that would settle them:** (a) one fresh-session witness per route (Claude child, Claude main, Codex main) using binding.claude:68-73's checklist, run twice — from a nablarva subdirectory and from `~` — settles 2, 8, 9 and walk-up autonomy (the 10-17 receipt "explicitly selected nablarva" is ambiguous between seeded and autonomous); (b) mechanical: extract the four card-selection paragraphs to the scratchpad and `diff` them — makes friction 1 a `mech` finding with a diff; (c) `cmp` live vs source for all five wrappers after every deploy (already done 10-21). Compaction → U9/P1.

**Fold/repair destination candidates:**
- Card-selection owner → `binding.<vendor>.md §Entry routes` (route-dependent, therefore vendor-side). Wrapper step 4 keeps only the kernel fence ("no card line: child → consult, main → ask; full law: binding §Entry routes"). identity :57-60 → pointer sentence. Alternative: owner = identity (vendor-blind), bindings cite — rejected because child/main is a vendor route concept the identity :60 itself defers ("the binding names the routes").
- Entry-proof owner → wrapper step 5 (kernel; emitted first). Bindings cite it and add only vendor deltas (Codex: cwd line). Codex wrapper step 5 should gain "plus effective cwd" or the binding should drop it — one or the other.
- binding.codex.md:18 → "deploy.sh `copy_file` leg (deploy.sh:238-245)"; re-stamp. Alternative: leave + banner (worse: it is a one-line fix).
- identity.md:5 authority → move the nablarva pins to nablarva.md:5 (already there) and leave identity with "the flag lock of the project loaded via the addendum · HOUSTON-R4 design record". Alternative: keep, annotate "first project". Decision D4 for Majkee (identity is gaveled design, atlas-ui authored).
- binding.codex §delegation → add the named executor/creator ban list (Codex roster names), or consult.md:49 → cite `binding.<vendor>.md §delegation` by path. Prefer the card citing the binding (card stays vendor-blind).
- All five germline edits re-roll stamps; three wrapper edits re-roll canaries; `raw.card.model-effort.md` untouched.

**What U2 implies for U3's isomorphism.** Mapping that U2 supports: identity ≈ CONTROLLER (invariants), card ≈ fn (bounded procedure, five-field shape vs card's invoked-by/fires/reads/writes/returns — near-identical), wrapper ≈ `ctrl` launcher (entry), addendum ≈ project-local function (G4's "exceptional, explicitly declared" shape — Houston does it *by default* via walk-up, which is exactly what G4 forbids inferring "from files being present"; U3/U5 should name this). Residue: **binding.<vendor>.md has no program counterpart** — and G5's "small explicit binding table from public program capabilities to its harness mechanism" describes binding.claude.md §wrapper table almost verbatim. So the Houston load path already implements a G5-shaped surface; U3 should test that rather than assume programs lack it. Stamp locus: Houston quotes stamps *after* the fact (a transcript reader verifies); CONTROLLER pins them *before* (a gate). Cheap hypothesis for U3: identity's cards table (:51-55) could pin card stamps, which would make the shapes isomorphic on this axis too — not a merge/split recommendation.

**U2 unit hypotheses.** Boundary: five files per route, legibility only. Inputs: measured sizes (Flight note 1: ≈33 kB ≈ 8.3k tok with addendum). Returns: per-file owner table + the diff of the four selection paragraphs + a witness checklist. Failure-recovery: a divergence found between wrapper and binding is a `mech` finding with a proposed diff (audit card pen), never applied. Verification: the three-route witness run; the paragraph diff.

**Decisions needed (U2):** D4 identity.md:5 authority scope (Majkee); which file owns card-selection (Flight can propose; Majkee gavels because wrappers are gaveled design). The rest is `mech`.

Stop.
