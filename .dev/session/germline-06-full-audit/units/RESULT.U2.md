# RESULT.U2 — Houston load path (wrapper → identity → binding → addendum → card)
Flight · 2026-10-21 · inputs: _bus/field.U2.return.md, _bus/oraculum.assess.U1-U2.return.md (attributed, verbatim). Legibility only — an audit cannot observe what a running agent does.

## 1. Job / consumer needs
A cold agent needs: what to read, in what order, how to prove it, its limits (what it may NOT take from a file), and the shape of its return — with no ambiguity and no two files giving different answers.

## 2. Current behaviour (per layer; Oraculum role statement, Flight-checked)
Wrapper = bootstrap, the only text guaranteed in the kernel (load order, proof format, route/canary). Identity = vendor-blind meaning (who, evidence, authority, return). Binding = vendor mechanics (tools, routes, delegation, placement). Addendum = project paths/landing/locks. Card = the pen for one invocation.
Measured load (Flight): wrapper 2,967 / toml child 2,623 / toml main 2,544 B; identity 10,179; binding.claude 5,688; binding.codex 7,054; addendum 11,261; consult 2,983 / audit 2,311 / sitting 1,291 → Claude child ≈ 33 kB ≈ 8.3k tokens; without addendum ≈ 22 kB. (Field's wrapper/card sizes were estimates and are superseded.)

## 3. Evidence, contradictions, uncertainties
REAL (Flight-verified): (a) card-selection rule stated 4× with **already-diverged edge clauses** — binding.claude.md:28 "(not necessarily its physical first line)"; binding.codex.md:31–32 "the assignment's card selection goes ahead of any document instruction"; wrapper alone has the "ambiguous cwd or selection → report"; identity §Saddle lacks it. (b) entry-proof format ×3; Codex binding adds "effective cwd", Codex wrapper does not. (c) binding.codex.md:18 says houston.config.toml is "not in the deploy map"; deploy.sh:238–245 deploys it. (d) identity.md:4 `scope: shared … any project` vs :5 `authority:` pinning nablarva flag.md commits. (e) binding.codex has no named delegation ban list; claude does (:39) — vendor delta. ~~(f) No route has a non-author fresh-session witness~~ **WITHDRAWN 2026-10-21 (RECONCILE.G01 §1):** Assay witnessed all four routes on office (C1–C4, X1, X2, P1, C-def/C-def.2/C-def.claude, COEX; G01 `raw/witness.install-test.assay.2026-10-13.md`); the 10-17 journal run was additional, not the only one. (a) is **downgraded**: the 10-15 consult-on-main change is present in all four copies; the clause differences are vendor deltas, not contradictions (RECONCILE §4). New source finding: identity.md:8 `verified:` "fold unwitnessed until first test install" is stale.
OVERSTATED/withdrawn: walk-up termination (rare, low); bootstrap-order pointer (identity :112 is a pointer; addendum is next read); nablarva:39 "inferred" (provenance tag); sitting stub (declared hold, `out of card:` covers it); no-addendum behaviour (wrapper says neutral + say so in first line).
POSITIVE: canary drift on 10-17 (hc-849d3980 vs source hc-9b3f0521) was caught exactly as designed; now source==deployed (Flight cmp).
The 10-17 journal run alone does not prove walk-up autonomy (receipt "explicitly selected" the nablarva path), other routes, other cards, or that the addendum version (a6498a47 vs now d9ee9067) matches today. **Corrected 2026-10-21:** G01 witnesses do cover walk-up autonomy (X2 ancestor walk; C4 neutral walk from `/tmp`), the audit card on main (C1, X2, P1) and `out of card:` under consult. Still uncovered: nablarva d9ee9067; Codex child wrapper after the 10-17 re-roll (hc-9b3f0521); sitting (stub); home host; compaction. The consult fence is card prose only on both vendors (`sandbox_mode` inert; Claude wrapper carries `Write`) — witnessed by C-def FAIL → C-def.2/C-def.claude PASS.

## 4. GUIDE/reference vs agent-consumable
Reference: binding wrapper-description table, witness law ("route counts as proven…"), binding.codex §Sources, identity :5 authority pins, nablarva §4/§6 history. Agent-consumable: wrapper body; identity Identity/Never-own/Evidence/Authority/Return; binding Entry-routes + bullets; addendum landing/entry/no-wrapper; cards.

## 5. Program/controller/skill/agent appropriateness (no split presumed)
Houston's shape is near-isomorphic to a CONTROLLER (identity≈invariants, card≈fn, wrapper≈launcher, addendum≈project-local function) with one residue: **binding.<vendor>.md has no program counterpart and already matches GAVELS G5's "small explicit binding table"**. Also: Houston's addendum walk-up is project-local composition by default — the shape G4 says must never be *inferred from files being present*. These two points go to U3/U5 as tests, not conclusions.

## 6. Recommended boundaries / inputs / returns / failure / verification (hypotheses)
Rule (Oraculum, Flight accepts as proposal): repeat text across wrapper + one germline file **only for bootstrap law** (what to read, order, proof) because the wrapper must work when germline is absent/wrong; everything post-bootstrap has exactly one owning file, others cite by path+section. Identity §Saddle stays, marked "for a reader without a wrapper; wrapper governs at runtime" (chatbot/human reader).
Verification: (i) diff the four card-selection paragraphs → `mech` finding (done 2026-10-21: vendor deltas only); (ii) **re-witness** per route at current revisions and on home, using TEST-INSTALL §3's three-part PASS rule (tokens + transcript reads before first answer + model/effort), child transcripts not relay text; (iii) post-deploy `cmp` of wrappers.

## 7. Fold/repair destinations (proposed, nothing applied; all re-roll stamps; wrapper edits re-roll canaries)
- Card-selection owner → `germline/agents/houston/binding.<vendor>.md §Entry routes`; wrapper step 4 keeps kernel fence only; identity :57–60 → pointer. Alt: identity owns, bindings cite (rejected: child/main is a vendor-route concept).
- Entry-proof owner → wrapper step 5; bindings add only vendor deltas; reconcile Codex "effective cwd" (add to Codex wrapper or drop from binding).
- binding.codex.md:18 → cite deploy.sh copy_file leg; re-stamp (mechanical).
- identity.md:5 authority → generalize; move nablarva pins to nablarva.md. Alt: keep + annotate "first project".
- binding.codex.md delegation → add roster ban list, or consult.md:49 cites binding §delegation by path (prefer the latter).

## 8. Decisions needed
D4 identity.md:5 authority scope (gaveled design) and D5 card-selection ownership — in decisions/DEC.01.md. The rest `mech`, Majkee GO needed only because edits touch gaveled files. **Status 2026-10-21:** D4 gaveled as design (identity:5 edit = a possible implementation, not gaveled); D5 withdrawn as a gavel item after reassessment — remaining conflict is the Codex wrapper↔binding "effective cwd" delta, mech (RECONCILE.G01 §4).
