---
from: field (subagent, Claude, spawned by Flight) · unit U2
date: 2026-10-21
status: native return preserved (per-file entries and friction/contradiction/load/run sections reproduced; wording of a few long cells lightly abridged, no claim changed). Flight's corrections are in units/RESULT.U2.md — notably: Field's wrapper/card byte sizes were ESTIMATES and are wrong; measured values are in RESULT.U2.
---

## U2 — Houston load-path audit (Field synthesis, audit-only)

All nine files read in full. Byte sizes from PLAN.md where available (identity 10,179 · binding.claude 5,688 · binding.codex 7,054 · nablarva 11,261). Wrappers and cards estimated from non-blank line counts × ~80 bytes/line: claude wrapper ~3,680 B · toml child ~2,640 B · toml main ~2,560 B · consult ~3,520 B · audit ~2,640 B · sitting ~1,760 B. Tokens ≈ bytes/4.

### Per-file table

**File 1 — claude/agents/houston.md (Claude wrapper)**
- Job for agent: delivers the route identifier (canary `cl-e1a94c37`), exact 5-step load order, card-selection rules, entry-proof format, missing-file behavior. Only vendor-specific entry point read before any germline file.
- Job for human: YAML frontmatter configures the Claude Code runtime, never read as instruction. Line 2 canary-rule comment is for the maintainer.
- Duplicated where: load order steps 1–5 (claude.md:28–44) near-verbatim at identity.md:140–148 (§Saddle), both TOML wrappers (14–30), summarised in binding.claude.md:27–31. Card-selection rule (claude.md:35–39) duplicated at identity.md:57–59, binding.claude.md:27–31, binding.codex.md:30–37.
- Gap: walk-up termination condition unspecified ("walk its ancestors upward", no stop criterion). "First unambiguous readable one" undefined where two ancestors each hold a matching addendum. No cwd-detection guidance to distinguish child vs main (delegated to binding).

**File 2 — codex/agents/houston.toml (Codex child)**
- Job for agent: loader for spawned-child Codex route; canary `hc-9b3f0521`; body functionally identical to Claude wrapper.
- Job for human: name/description/model/model_reasoning_effort are runtime config; comments 1–3 for maintainers.
- Duplicated where: developer_instructions (toml:14–30) duplicates claude.md:28–44 with only the Route line differing.
- Gap: child cwd "not guaranteed" to equal parent's (binding.codex.md:57–58), TOML silent on what to do if walk-up finds nothing because of unexpected cwd. "First reply" semantics on a spawned child undefined here.

**File 3 — codex/profiles/houston.config.toml (Codex main)**
- Job for agent: loader for `codex --profile houston`; canary `hp-7c3e91a4`.
- Job for human: line 3 "deployed by deploy.sh allowlisted leg" is a maintainer note.
- Duplicated where: body identical to toml child except Route line.
- Gap: binding.codex.md:18 says "hand-installed; not in the deploy map"; line 3 here says the opposite. A cold agent reading binding.codex.md gets a false statement (confirmed stale: findings.g06 S1; deploy.sh:238–245).

**File 4 — germline/agents/houston/identity.md**
- Job for agent: primary identity contract — three cards, evidence discipline, capability/authority bounds, return contract, §Saddle. The load's weight-bearing layer.
- Job for human: frontmatter (agent/gen/scope/authority/state/updated/verified/stamp/authored) is provenance. §Vendor delta (132–136) tells maintainers where NOT to put vendor facts.
- Duplicated where: §Saddle (140–148) duplicates wrappers' load order. "A file missing or unreadable is my first finding; I never reconstruct its content from memory" also at claude.md:44 and both TOMLs 32–33.
- Gap: identity.md:112–114 references "the project's flag (L16.6–8)" before the agent has read the addendum (bootstrap order). identity.md:144 "a later layer specialises, never overrides" does not define the boundary.
- Scope/authority: scope = "shared — the architect base seat of any project": gives scope but no explicit prohibition; authority cites nablarva-specific commit pins (flag.md @ 32b645f, nablarva@2ae8636) inside a "shared" file.

**File 5 — binding.claude.md**
- Job for agent: maps identity capabilities to Claude tool names (Read/Grep/Glob/Write/Agent), entry routes by card, delegation bans, consult's absolute no-write rule, entry proof format.
- Job for human: entry routes table is a quick invocation reference. §Placement note (42–44) tells operators not to add project-scope wrappers.
- Duplicated where: card-selection (27–31) duplicates wrapper:35–39 and identity:57–59. Entry proof (55–58) duplicates wrapper:42–48 and binding.codex.md:78–83.
- Gap: "a route counts as proven only after a dated fresh-session witness" (68–73) — the agent has no mechanism to check whether a route has been witnessed; no failure mode for an unwitnessed route.
- Scope/authority: clearest prohibition in the chain — "grants no authority the identity, the card or the project addendum does not already name" (5–6).

**File 6 — binding.codex.md**
- Job for agent: Codex mechanics — two wrapper files, sandbox inheritance caveats, child cwd uncertainty, project wrapper collision warning, native mechanism list.
- Job for human: §Sources (85–87) names Codex docs consulted. Sandbox note (48–51) is a witnessed fact from a specific run.
- Duplicated where: card-selection (30–37) duplicates TOML:23–27 and identity:57–59. Entry proof (78–83) duplicates binding.claude.md:55–58 and both TOMLs.
- Gap: line 43 says the TOML cannot enlarge inherited authority, but gives no guidance if the parent's sandbox REMOVED capabilities the load requires (e.g. Read). Line 18 stale (see File 3).
- Scope/authority: "grants no authority beyond the identity, the selected card and the project addendum" (5–6). Clear.

**File 7 — nablarva/.germline/agents/houston/nablarva.md**
- Job for agent: maps identity roles to nablarva disk paths, names landing paths per card, trigger/intrinsic classes (pointers to flag L16.6–8), keeper state, project procedure (bus format, archive rule, entry paths, no-project-wrappers).
- Job for human: §6 First-audit seed (115–125) and history migration plan (§4, 67–86) are labeled historical provenance.
- Duplicated where: "`.claude/agents/houston.md` and `.codex/agents/houston.toml` must not exist here" (112–113) duplicates binding.claude.md:42–44 and binding.codex.md:54–56. Entry commands (107–108) partially duplicate binding entry-route tables.
- Gap: audit landing path (39) tagged `inferred: atlas`. Line 56 says convergence.md "retired as keeper" but convergence.md carries no marker (findings.g06 S4). Keeper claims point to PROJECT.yaml/wrapper frontmatter, unverifiable inside this load path.
- Scope/authority: "may add paths, procedures and local method; may not override the identity or any lock in flag.md" (4). Only the addendum uses "may not".

**File 8 — cards/consult.md**
- Job for agent: no-write absolute rule, activation conditions, what to read (smallest set), return shape (verdicts + ≤5 constraints), delegation limit (at most one bounded reader).
- Job for human: §What I do not do is a legible spec of hard limits.
- Duplicated where: no-write rule also at binding.claude.md:49–50, binding.codex.md:47–50, wrappers (implied).
- Gap: consult.md:49 "at most one bounded reader" names no eligible agents; ban list lives at binding.claude.md:39. A Codex-route agent reading consult.md finds no cross-reference.

**File 9 — cards/audit.md**
- Job for agent: walk scope (wrapper → organ bodies → whole-animal doc → guides → flag), return tags (mech/judge/cross), pen limits (wrapper mechanics only as diff), route qualification (main = full card; child = audit-as-probe), delegation bounds.
- Job for human: §Keeper (27–29) and tag taxonomy rationale are maintainer context.
- Duplicated where: "audit-as-probe states which route it ran on" (32–34) duplicates binding.claude.md:35 and binding.codex.md:39.
- Gap: audit.md:22 says paths "assigned by the invocation"; nablarva.md:36 gives a naming pattern and defers to the invocation — ambiguous if the invoker omits the filename.

**File 10 — cards/sitting.md**
- Job for agent: declares STUB; five operative lines hold; everything else `out of card:`.
- Job for human: "Status: named, not yet built" tells an operator to write the card first.
- Duplicated where: "invoked by: operator, rare" duplicates identity.md:55.
- Gap: stub does not say what the agent returns for a sitting task; must synthesise from binding.codex.md:45 ("return to the operator and stop").

### Ranked friction list (agent legibility only — cannot observe what an agent actually does)
1. Load-order and card-selection rule duplicated ×5 — no canonical single point; any single-file edit silently diverges.
2. Walk-up termination undefined — claude.md:29–33, toml child:17–21, toml main:17–21; "ambiguous" addendum undefined.
3. binding.codex.md:18 stale vs houston.config.toml:3.
4. Bootstrap order gap — identity.md:112–114 references flag before addendum read.
5. Delegation allow-list split across files (consult.md:49 vs binding.claude.md:39).
6. Sitting stub gives no return template.
7. nablarva.md:39 inferred audit landing path.
8. No-addendum behavior partial — claude.md:34, toml:21; "neutral Houston; I say so in my first line" implies continuing to card step but does not state it.
9. Unwitnessed route requirement — binding.claude.md:68–73, binding.codex.md:82–83; no agent-side failure mode.

### Contradiction list
- C1 binding.codex.md:18 vs houston.config.toml:3 (confirmed stale, S1).
- C2 identity.md:4 scope "shared … any project" vs identity.md:5 authority citing nablarva-specific pins.
- C3 Source canary `hc-9b3f0521` (codex/agents/houston.toml:12) vs observed-run entry receipt canary `hc-849d3980` (journal:87–88). Deployed TOML at time of run differed from ia-sync source; whether substantive unknown.
- C4 Observed run's nablarva addendum stamp `a6498a47` (journal:77) vs current nablarva.md:9 stamp `d9ee9067`; both `updated: 2026-10-17`. Run used an earlier version; historical record only.

### Per-route load size (Field's estimates; see status note — wrapper/card figures estimated)
| Route | Wrapper | identity | binding | addendum | card | Total B | ≈ Tokens |
|---|---|---|---|---|---|---|---|
| Claude child | ~3,680 | 10,179† | 5,688† | 11,261† | ~3,520 | ~34,328 | ~8,582 |
| Codex child | ~2,640 | 10,179† | 7,054† | 11,261† | ~3,520 | ~34,654 | ~8,664 |
| Codex main | ~2,560 | 10,179† | 7,054† | 11,261† | ~3,520 | ~34,574 | ~8,644 |
† PLAN.md-verified. Without addendum (neutral Houston): ~23,000–23,400 B ≈ ~5,750–5,850 tokens. Dominant: identity (~29%) and nablarva (~33%).

### Observed run — what it does and does not prove
Run: journal 2026-10-17 lines 75–92, Houston as Codex child, nablarva, stamps quoted: identity 99ae988e, Codex binding 0c812f6c, nablarva a6498a47, consult 5435b1c7.
Shows (legibility observation): (1) all four stamps quoted in expected positions, consistent with steps 1–4; identity stamp matches current live file. (2) consult no-write followed ("No file was written by Houston", journal:78). (3) `stretches` verdict returned. (4) Walk-up located nablarva despite inherited `.majkee` cwd (journal:75) — but journal:75–76 says the receipt "explicitly selected /home/hruzam/unikuklatrix/nablarva"; the agent may have been given the path in the assignment; walk-up autonomy cannot be determined. (5) the stale-binding friction did not visibly affect the outcome.
Does not prove: Claude child/main route; Codex main route; audit or sitting on any route; walk-up ran autonomously vs seeded; that full file contents were read vs stamps supplied; that the addendum version used (a6498a47) equals the current file (d9ee9067). identity.md:8 says the fold remains unwitnessed until first test install; this is a single Codex child consult, not a route-witness record as defined by binding.claude.md:68–73.

### Uncertainty
Judges legibility only; cannot observe what a running agent internalises or executes. Compaction (U9) and vendor mechanics (U8) excluded. Sitting stub, walk-up termination and delegation allow-list gaps are legibility gaps; behaviour is testable only by a witnessed run.
