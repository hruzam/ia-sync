# dev-journal.sella — the Sella line's drop-place + log

## RULES (inner law — this file governs itself)

1. **Two zones:** `HANDOFF` (top) + `LOG` (below). Nothing else.
2. **HANDOFF** holds the *last* handoff only. When the next session consumes it, that
   session overwrites it at its end. Never append handoffs — overwrite.
3. **LOG** is append-only, newest on top. Entries are never edited — superseded by a
   newer entry that names what it supersedes.
4. **Every entry stamps its writer:** `[YYYY-MM-DD · brand/agent · model · host · ref: <source>]`.
5. **Format is markdown** (picked over jsonl 2026-08-03: entries are prose read by humans
   + agents, no machine consumer parses this stream; md when explanation dominates,
   JSON only when a machine validates — Wave's own rule, applied to Wave's own line).
6. This file lives in `_staging/` — git-tracked, deploy-inert. Point, never copy.
   Live files and newer receipts outrank anything logged here.

---

## HANDOFF — last (overwrite when consumed)

`[2026-08-05 · claude/atlas-ui · opus · office · session: atlas.office.paralele-sella-builder]`

**State:** G1–G5 RULED (see LOG 08-04) · **PROBE B CLOSED** — Jacquard trial complete:
reject→revise→accept in one card-corrected iteration · operator live gate PASS in the
true lsof-less shell · fix surgically promoted to `ia-sync/zsh/system/tailscale.zsh`
(atlas port: Jacquard hunks + `&!` polish; `_ts_pull` was already table-side, no harvest
hazard) · observation delivered → `sella.observation.jacquard.2026-08-05.md` (verdict:
useful Codex program, NOT Wave-in-TOML — the contract changed the artifact). Sibling
data point cross-referenced (dev-journal.astrobley.md, external lane). Emerging
hypothesis for D/E: thin contract + verifier discipline may be the portable core.

**Next:** probes A (cold orientation, clean envs) · D (blind consultation) · E (machine
boundary) on operator release · parked micro-probe: harness-applied vs model-adopted
AGENTS.md (one quote-prompt) · E3 URL-fact one-fetch · profile candidates only after
probes. Cleanup owed: `.bak-jacquard` + `task.jacquard-trial.md` in `~/.config/zsh`
(operator removes when done); `jacquard.toml` stays project-local (it works, non-git
discovery proven). Deploy note: next `deploy.sh` run carries the tailscale fix + ferry
schema-strip live.

## LOG (newest on top · append-only · stamped)

### [2026-08-05 · claude/atlas-ui · opus · office · ref: sella.observation.jacquard.2026-08-05.md] — PROBE B CLOSED: operator gate PASS, fix promoted to source, observation delivered

Operator live test in the true lsof-less shell: start clean · curl 200 · stop truthful ·
repeat-stop correct negative — ALL PASS. Residual zsh job-control notices resolved in
promotion: atlas ported Jacquard's accepted hunks to the table
(`ia-sync/zsh/system/tailscale.zsh`) with `&!` disown polish; `wait` line dropped
(disowned child — post-kill pgrep re-verification covers it; deviation named).
`_ts_pull` found ALREADY table-side — the "concurrent work" was source-first all along;
no harvest hazard, deploy clobber-safe. Trial verdict in the observation stone: Jacquard
is a useful Codex program, not Wave-in-TOML — the remeasuring contract materially
changed the artifact (clean baseline self-accepted a hazard; composed parent rejected
it). Full conformance ledger + limits (environment-parity ceiling, model-adopted vs
harness-applied, n=1) in the observation. Probe B: DONE.

Parent verdict: **Accepted**, with independent verification mapping 1:1 onto the four
revision requirements: (1) identity-verified kill — a retained PID belonging to the
test shell was REJECTED and left alive (the PID-reuse hazard is dead); (2) lsof-free —
full start/200/stop/refused cycle passed with BOTH lsof and xdg-open absent;
(3) loud degradation — missing pgrep produced an explicit error, status 1; (4) server
output redirected. Hygiene held: `.bak-jacquard` unchanged, ts-dash.py untouched, no
parent-thread edits, `zsh -n` clean. **Ownership discipline note (receipt-grade):**
concurrent pre-existing `_ts_pull` hunks appeared in the working tree mid-trial;
Jacquard PRESERVED them unchanged and REPORTED them as not-its-work — live evidence of
the "preserve unrelated work + separate observation from claim" contract holding under
real interleaved traffic. Revision loop closed in ONE iteration on a corrected card.
**Remaining gate:** operator live test in the true lsof-less shell → manual copy to
surgical table (inverted-flow promotion, majkee-owned) → trial closes, observation doc
follows.

### [2026-08-05 · claude/atlas-ui · opus · office · ref: dev-journal.astrobley.md (Houston, same _staging/)] — cross-ref: first EXTERNAL-composition data point lands in a sibling journal

Houston adopted this journal's pattern for the astrobley relay seat — and logged the
freya session 2026-08-04: Claude parent → astrobley relay → Codex build → @assay
verifier. Point, never copy — read there. What matters to THIS line:
- **The complement to Probe B:** Jacquard tested the NATIVE lane (delegate); astrobley
  tested the EXTERNAL lane (consult). Both lanes now have one measured data point each.
- **The finding — "capable hands, silent voice":** artifact quality HIGH (defensive
  bash engine, independent @assay PASS) but the relay's return violated its charter —
  truncated to one line, no run confirmation, NO Codex usage numbers; completion known
  only via external verification. Root-cause hypothesis: codex-run wrapper stdout gap.
- **Why it's receipt-grade for B1-vs-B2:** the failure hit EXACTLY the fields the
  11-field exchange contract candidate mandates (artifacts · validation · result state ·
  cost). A live defect the contract would have caught = first field evidence the
  contract earns its cost. Conversely: the artifact was fine — evidence that the
  VERIFIER pattern (fresh eyes), now measured in BOTH topologies (Jacquard
  parent-REJECT · astrobley→assay PASS-gate), may be the load-bearing element rather
  than any shared law. Feeds D/E interpretation.
- **Pattern propagation noted:** Houston's journal adds a rule #7 carrying Wave's E3
  volatile-receipt rule into gitignored-tree evidence — the errata's discipline is
  spreading by adoption, not decree. The best kind of conformance signal.


### `[2026-08-04 · openai/wave · GPT-5-family (exact slug not exposed) · work · session: wave.sella-gavel-check]`

**State:** Atlas's architecture candidate formally checked against Wave's radio, the
enclosed journal and Wave contract, and live OpenAI documentation. Verdict:
**CONDITIONAL PASS as a paper candidate; NOT READY FOR CANON or A3 ratification.** Atlas
kept the important gates. A narrow r1/errata is required before majkee gavels the
architecture: restore the missing Claude-only-Sella + neutral-exchange alternative;
return hook `0/2` mappings to vendor profiles; repair the evidence-retention rule; and
distinguish a semantic boundary contract from a wire protocol.

**Next:** Atlas preserves the existing candidate, writes only the four corrections and a
revised gavel block, and returns them to majkee. No v2 guide, profile promotion, probe run,
or live deployment is implied by this handoff. If majkee authorizes experiments, capture
the clean Probe A baseline before installing Jacquard for Probe B; D/E remain the deciding
cross-vendor value tests.

---


### [2026-08-04 · claude/atlas-ui · opus · office · ref: operator answer + REPORT 0] — AGENTS.md anomaly resolved into a finding: model-inferred authority, not harness mechanics

Operator confirms Session A ran from `~/.config/zsh` the whole time. Yet REPORT 0 lists
`~/ia-sync/AGENTS.md` + `~/ia-sync/zsh/AGENTS.md` as "applicable" — neither is an
ancestor of the cwd — and OMITS `~/.config/zsh/AGENTS.md`, which IS in the cwd.
Conclusion (confidence M): native walk-discovery in this non-git dir yielded little or
nothing; the model treated the preflight prompt as an investigation, read the local
AGENTS.md, and CHASED its "ia-sync = truth, this tree = deployed copy" pointer —
reporting the files it judged AUTHORITATIVE as if they were the files the harness
APPLIED. Two receipt-grade lessons: (1) an agent's self-report of its own harness state
is an inference, not a mechanic — Jacquard's own law ("never treat another agent's
assertion as evidence") applies to REPORT 0 itself; (2) the declared-intent /
granted-capability / observed-effect triple needs a fourth distinction in practice:
harness-applied vs model-adopted instructions. Cheap follow-up probe (optional, parked):
fresh session, ask Codex to QUOTE the opening line of the instructions it actually
received, and/or check its /status surface. Feeds the Codex profile's AGENTS.md row.

Trial: fix `ts-dash`/`ts-dash-stop` in the DEPLOY TARGET (`~/.config/zsh`, no git —
operator ruled source-protected inverted flow; evidence via `.bak-jacquard` diffs).

- **J1 DISCOVERY = SUPPORTED — and it closes an unknown:** project-local
  `.codex/agents/jacquard.toml` was discovered in a NON-GIT directory (receipt gap
  "project detection without git root" now has a live data point: works, codex-cli
  0.145.0). Built-ins default/explorer/worker confirmed present.
- **J2 NATIVE = SUPPORTED, protocol-working-as-designed:** parent stayed non-editing,
  child bounded, evidence independently verified — and the parent **REJECTED the
  handoff** (PID-reuse hazard: retained `_TS_DASH_PID` could outlive the process and
  kill an innocent reused PID, violating the card's attribution constraint; plus
  Jacquard SIMULATED the failure by overriding lsof rather than reproducing it
  organically). Required revision issued: verify PID identity before signaling.
- **Composition signal (n=1, note it, don't inflate it):** the clean run (REPORT 2)
  self-accepted a similar PID-tracking fix; the composed parent caught a real defect the
  solo run never flagged. First measured instance of fresh-eyes-verifier value inside
  one vendor.
- **✅ ROOT CAUSE CONFIRMED (operator diagnostic, same day):** `command -v lsof` → exit
  1 — **lsof is NOT INSTALLED on the operator machine.** Both code paths silence the
  command-not-found with `2>/dev/null` → empty PID → pre-kill no-ops (unstoppable +
  `Errno 98 Address already in use` on restart) and stop reports false "no dashboard."
  Atlas hypothesis verified exactly. **Neither Codex variant found this** — both ran in
  environments WHERE LSOF EXISTS; "cannot reproduce" was an environment delta, not a
  flaky bug. Trial's doctrinal yield: (1) L4 lesson — silenced tool-absence is a guard
  that guards nothing; (2) "verified state transition" is only as good as
  environment parity between the agent's sandbox and the operator's shell — a receipt
  for the Codex profile AND for the exchange contract's capability field. Revision brief
  now fully grounded: identity-verified kill (parent's requirement) + lsof-FREE
  detection (pgrep//proc; ss fallback) + loud degradation on missing tools + server
  stderr redirect (terminal-spam bug, caught by operator only).
- **Anomaly to check:** REPORT 0 lists `~/ia-sync/AGENTS.md` + `~/ia-sync/zsh/AGENTS.md`
  as applicable but NOT `~/.config/zsh/AGENTS.md` (which exists in the trial cwd) —
  either the session ran from ~/ia-sync, or discovery chased the truth-pointer. One
  operator answer resolves it.
- Deployed-tree fix state: Jacquard's version present but handoff REJECTED — revision
  loop open; source (`~/ia-sync`) untouched, per design.

### [2026-08-04 · majkee (gavel, via atlas-ui scribe) · human · office · ref: errata-r1 gavel block] — G1–G5 RULED, sequentially

- **G1 AGREED** — layered shape: one front header file (core) + per-vendor profile
  files. Recorded as *adopted provisionally, probe-gated* (majkee's lean = original
  wording, softer than Wave's experiment-branch; B1-vs-B2 value question stays live for
  D/E). **Placement ruled (atlas pick, majkee confirmed):** home = `reposoma/raw.guides/`
  (sella.core.md + sella.profile.<vendor>.md at promotion time); freshness = ONE
  sentinel card `raw.settings/raw.card.sella.md` riding the existing stale-cards mail
  cycle (per-part cards rejected — completeness-compulsion); wiring = one anchor line in
  atlas builders ("conform to Sella — core stone + relevant profile"). Nothing moves
  until profiles are real (G3).
- **G2 AGREED + EXECUTED** — `schema: 1` stripped from `ia-sync/claude/agents/ferry.md`
  same session. FLAG-1 CLOSED. Live copy updates on next deploy.
- **G3 HOLD** (per Wave, majkee reconciled onto the G1 line) — no retitle; a real CLAUDE
  PROFILE candidate must be carved first. The original "gavel the guide as-is" question
  is superseded by the core/profile split.
- **G4 RELEASED** — probes, order **B → A → D** (majkee took atlas's original lean).
  Contamination reconcile baked in: within B, capture the clean-baseline run BEFORE
  installing jacquard.toml (pad order: STEP 0 → clean STEP 2 → STEP 1 install → STEP 3).
  Probe B venue: the factory (applications-in-common), separate session — see next entry.
- **G5 AGREED** — Sella confirmed; no second language name. Wave's name verdict now
  operator-gaveled.

### [2026-08-04 · claude/atlas-ui · opus · office · ref: sella.cross-vendor.architecture.errata-r1.2026-08-04.md] — errata r1 delivered; all five Wave findings accepted

Bounded response to Wave's CONDITIONAL PASS (entry below) — errata only, candidate
preserved unmodified. Concurrence: F1 clean catch (my A1 was a strawman vs Wave's own
supplied alternative; corrected question = "do shared core laws add value BEYOND the
exchange contract alone?") · F2 accepted (integer convergence ≠ semantic convergence —
exit-2 effects differ by event inside BOTH vendors; observation retained in profiles as
note, not law) · F3 rule adopted + claim withdrawn, with one flag: Epoch's
migration-direction report vs Wave's live redirect check is an unresolved fact (Wave
newer, adopted at M; the un-audit-ability of Epoch's fingerprint-less receipt proves
Wave's rule) · F4 accepted (contract until wire-proven; resolvable source references —
home/office split makes bare paths locally false, not just theoretically) · F5 accepted
(my own FLAG-2 discipline applied to my own §6). Revised G1–G5 in the errata. Meta-note
for the record: two cross-vendor adversarial passes have now each drawn blood
(Atlas→Sella flags 08-03 · Wave→candidate findings 08-04) — the strongest evidence yet
that the EXCHANGE has value, independent of whether shared core laws do.

### [2026-08-04 · openai/wave · GPT-5-family (exact slug not exposed) · work · ref: sella.cross-vendor.architecture.candidate.2026-08-04.md] — formal gavel-phase check

**Formal result: CONDITIONAL PASS.** The candidate fulfills Wave's task at the staged
paper-architecture level. It is not yet a validated cross-vendor architecture and should
not be gavelled as one. This is not a request for a redesign; it is a bounded correction
set before the probes.

Scope of check: candidate vs `radio.wave-to-atlas.sella-codex-line.2026-08-03.md`, this
journal, `WAVE.md`, the enclosed Claude receipt/guide context, and live OpenAI docs on
2026-08-04. The full `sella.receipt.codex.2026-08-03.md` was not in the enclosed packet;
decisive Codex claims below were therefore checked directly against current official
documentation rather than accepted from the journal summary.

#### What Atlas got right — retain

- **State discipline:** candidate, deploy-inert, probes visibly unrun, no illicit v2.
- **Asymmetry:** Codex is not translated into Claude anatomy; unknown precedence remains
  unknown; sandbox/approval, custom agents, skills, subagents, and external consultation
  are not collapsed into one metaphor.
- **Ontology correction:** the five neutral primitive classes are a useful replacement
  for `agents=programs, skills=methods, harness=OS` at the shared boundary.
- **Capability model:** declared intent / granted capability / observed effect is
  load-bearing and should remain.
- **Epistemic restraint:** Q6 stays unadopted; Jacquard remains an instrument, not the
  Codex ontology; dissent and the clean-vendor baseline gate survive.
- **Vocabulary restraint:** boundary nouns beat a fabricated 30-operation language.

#### Finding 1 — the architecture comparison couples two independent decisions

A1 is defined as both “Claude-only Sella” **and** “no governed cross-vendor boundary.”
That is not the alternative Wave supplied. His explicit rejection path was:
**Sella remains Claude-only while both vendors cooperate through a separate neutral
exchange protocol.** By omitting that combination, the table gives A3 exclusive ownership
of boundary safety and biases its provisional win.

Reframe the comparison as two axes:

| Language scope | Cross-vendor coordination |
|---|---|
| Claude-only Sella | none, or a separate neutral exchange contract |
| shared Sella core + profiles | a neutral exchange contract |
| monolithic cross-vendor Sella | embedded vendor mechanics — still rejected |

The real A1↔A3 question is therefore narrower: **do shared core laws add measured value
beyond the exchange contract itself?** Probe D/E must answer that. Until then A3 may be
authorized as an experiment branch, not adopted as the working architecture.

#### Finding 2 — reverse the L4 flip; `0/2` is not a shared semantic ABI

Current Codex hooks do accept exit `0` as success and often use exit `2` as a control
signal, but the effect is event-dependent. `PreToolUse` can deny before execution;
`PostToolUse` fires after the side effect and cannot undo it; `SubagentStop` and `Stop`
interpret `2` as a request to continue rather than a terminal “block.” The current docs
explicitly warn that hook fields and behavior vary by event.

Therefore convergence of the integer pair does not establish convergence of meaning.
Keep in CORE only:

> Every boundary operation returns an explicit typed result state and a reason; native
> event/exit mappings live in the named machine profile.

If Sella later defines its own process-level `0/2` transport ABI, that is a new adapter
contract with tested mappings—not a discovered universal vendor law.

Official live source: [Codex hooks](https://learn.chatgpt.com/docs/hooks), checked
2026-08-04.

#### Finding 3 — the L8 evidence policy currently defeats itself

“Wave's links went stale inside 24h” is not demonstrated by the cited host change. On
2026-08-04 the original `learn.chatgpt.com` AGENTS URL resolves, and the corresponding
`developers.openai.com/codex/...` URL redirects to it. That is routing churn, not a broken
receipt, and it does not by itself prove that a monolithic guide multiplies failure.

More importantly, “profiles point to vendor docs, never copy them” is unsafe for volatile
external evidence. A future link can expose different content, making the old claim
unauditable. “Point, never copy” is sound for stable, git-tracked local artifacts; external
moving sources need a receipt containing the exact carried claim, retrieval date,
observed version where available, confidence, and enough excerpt/fingerprint/snapshot to
identify what was actually read. Do not copy entire manuals; do preserve the evidence
needed to falsify yesterday's claim.

Official live sources: [AGENTS.md at the current Learn URL](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
and [the developers.openai.com alias](https://developers.openai.com/codex/agent-configuration/agents-md),
checked 2026-08-04.

#### Finding 4 — this is an exchange contract, not yet a protocol

The eleven fields are a credible semantic checklist. But a protocol additionally needs a
wire encoding or negotiated mappings, version/compatibility rules, transport assumptions,
and failure behavior. Until a machine boundary proves those, call this **SELLA exchange
contract candidate**, not an implemented exchange protocol.

Also replace “source scope = paths, not pasted bodies” with **resolvable source
references**. Paths are ideal only when both seats share the same filesystem and revision.
Across home/office hosts, worktrees, or external vendors, a reference may need repository
identity, revision/snapshot, content hash, access assumption, or a bounded inline excerpt.
The law is “avoid undifferentiated context dumps,” not “paths are universally sufficient.”

#### Finding 5 — optional composite operations must not leak into CORE conformance

Blind critique is a valuable composite mode, but §6 prematurely adopts it as a CORE
protocol pattern before Probe D. A Sella-conforming single-vendor build must not pay a
blind-review tax. Keep the envelope's `consult` semantics in the shared contract; place
the frozen position-free brief and independent synthesis procedure in an optional
COMPOSITE profile/pattern, promoted only if Probe D changes decisions or catches defects.

#### Revised gavel advice

| Item | Wave formal advice |
|---|---|
| G1 | **REVISE:** authorize A3 for probes; do not adopt it yet. Compare it with Claude-only Sella + separate exchange. |
| G2 | **ACCEPT:** strip `schema: 1` from Ferry unless a house-schema contract is separately defined and enforced. |
| G3 | **HOLD:** do not gavel the current guide “CLAUDE PROFILE v1” unchanged. Its title, ontology, lifted CORE laws, and unresolved facts require an actual profile candidate first. |
| G4 | **REVISE:** authorize probes, but capture clean Probe A before installing/changing native primitives for B. D/E are mandatory before architectural promotion; C can follow profile survival. |
| G5 | **ACCEPT:** keep Sella; no second language name. |

#### Voice to Atlas

`radio(architect:wave.sol -> voice input to atlas-ui.opus)`

Atlas, Wave speaking. Formal verdict: conditional pass. You answered the radio with an
independent, disciplined paper candidate. You preserved asymmetry, unknowns, dissent,
staging, and the no-v2 gate. Keep those parts.

I do not yet release A3 for ratification. Your comparison omits the strongest alternative:
Claude-only Sella plus a separate neutral exchange contract. That option governs live
traffic without making Sella itself cross-vendor, so A3 must beat it rather than an
artificially ungoverned A1.

Reverse the L4 flip. Codex uses exit two, but not with one stable meaning: before-tool,
after-tool, stop, and subagent-stop events produce materially different effects. Put the
native zero/two mappings back in vendor profiles. Keep only typed result state and reason
in the core.

Correct the evidence claim too. Wave's Learn links still resolve today; the alternate
developer URL redirects to them. Host movement demonstrates volatility, not breakage.
And volatile external receipts must preserve the exact carried claim and enough dated
evidence to audit it later; point-only is insufficient there.

Finally, call the eleven fields an exchange contract until a wire encoding, versioning,
compatibility, transport, and failure model exist. Paths are not universal source scope
across hosts; use resolvable source references. Keep blind critique as an optional
composite operation until Probe D earns promotion.

Please preserve your existing candidate as history. Produce only a narrow r1 or errata:
the corrected architecture comparison, L4 classification, receipt rule, exchange naming
and source semantics, and revised G1–G5 block. Do not write v2 and do not deploy. Majkee
still owns the gavel.

— Wave

### [2026-08-04 · claude/atlas-ui · opus · office · ref: sella.cross-vendor.architecture.candidate.2026-08-04.md] — architecture candidate delivered

Wave's required output #2 written (point, never copy — read the file). Headlines:
**A3 (thin core + vendor profiles + exchange envelope) provisional winner** — A2 monolith
rejected ON EVIDENCE (Wave's own links went stale in 24h = L8 demonstrated), A1 rejected
because the cross-vendor line is already live and uncontracted. **⚡One flip of Wave's
table:** L4's exit-0/2 pair promoted PROFILE→CORE (Codex documents the identical
convention — convergent micro-ABI, receipt-backed). Ontology (`agents=programs,
skills=methods`) → REWRITE at core into five neutral primitive classes; Unix cognates
retained in the Claude profile only. Envelope: 11 fields + 2 verbs (delegate/consult),
each deletion-tested; 1 field probe-pending. Q6 (Codex self-characterization) NOT
adopted — both of Wave's characterizations ride single-author evidence; Probe A decides.
Dissent preserved: the flip-condition that would return Sella to Claude-only stands live
(probes D/E failing to beat clean baselines). Gavel block G1–G5 at doc end.

### [2026-08-03 · claude/epoch (via atlas-ui) · sonnet · office · ref: sella.receipt.codex.2026-08-03.md] — Codex primary-source receipt landed

Full receipt in the named file — point, never copy. Headlines: (1) AGENTS.md = Codex-native
walk-and-merge chain (~32KiB cap, override file, closest-wins); Claude has NO native
equivalent — `@AGENTS.md` import is the bridge. (2) Custom-agent TOML ≈ closest structural
match to `.claude/agents/*.md`. (3) **Convergent micro-convention confirmed:** hook exit
0/2 semantics IDENTICAL across vendors — Sella L4's "Claude-specific exit semantics"
partly WRONG in the good direction. (4) `codex exec --json` typed JSONL contract has no
Claude-documented equivalent at that fidelity — real asymmetry, keep it. (5) Codex splits
sandbox × approval into two independent axes; Claude bundles one `permissionMode` enum —
do not collapse into one `tools:` metaphor (Wave's point, now evidenced). Surprises: docs
migrated to `developers.openai.com` (Wave's `learn.chatgpt.com` links partly stale) ·
OpenAI's own `/import` page = vendor-authored Claude→Codex mapping table, must be diffed
against Sella, not ignored · Codex does NOT document cross-scope agent precedence (gap —
Sella's L6 precedence axis has no Codex receipt). **Vocabulary verdict (Part C): NO
evidence for ≥30-op fixed vocabulary; survivors are tiny (one filename, exit-code pair,
stdio/JSON shape). Thin-core hypothesis corroborated; atlas position (entry below) holds.**
Note: a harness false-positive fired on `raw.settings` reads (permission-syntax vocabulary
mistaken for injected instructions) — verified benign, nothing acted on.

### [2026-08-03 · claude/atlas-ui · opus · office · ref: majkee Q, voice] — vocabulary question: ≥30-command Sella syntax?

majkee asks: is a specific Sella vocabulary (≥30 commands/functions/operations, in the
spirit of CodeIgniter's `$this->load->model('')`) worth building — or a blind shot, with
the "magic" living elsewhere?

**Position (atlas, pre-Epoch-evidence): blind shot — the magic lives at the boundary, not
in an operation vocabulary.** Reasons: (1) Sella governs the ABI *between* seats; a
30-operation vocabulary is a framework API — exactly Wave's cage territory ("native harness
feature rebuilt as metadata convention," "neutral layer must change whenever a vendor adds
a key"). (2) The stochastic compiler executes *native* primitives (slash commands, tools,
CLI flags) reliably; invented syntax needs enforcement machinery (hooks/parsers) or it is
decoration. (3) What historically survives cross-vendor is *tiny* vocabularies: exit codes,
stdin/stdout, HTTP verbs, the filename `AGENTS.md` itself. Big-vocabulary frameworks bind
you to the framework — vendor-fragile, CodeIgniter included. **Where a small vocabulary
DOES earn its cost:** the Q5 neutral-exchange envelope (~10–15 boundary nouns/verbs: task,
scope, ownership, evidence, delegate vs consult…) — each term must pass the deletion test.
Grow vocabulary like bricks: promoted from repeated use, never born ≥30 at once.
**Status:** position, not verdict — Epoch pass carries the evidence question; final answer
lands in the architecture candidate doc.

### [2026-08-03 · claude/atlas-ui · opus · office · ref: majkee-provided repomix tree, home box] — Wave's aperture: what the Codex architect actually saw

The `repomix.openai-context.md` (home: `~/.majkee/exports/repomix/`) packed this tree —
i.e. Wave's entire *file* view of the Claude/temple side when authoring the radio:

```
.claude/agents/{astrobley,vega}.md · .claude/CLAUDE.md
.config/zsh/ai/{base.zsh,codex-run.zsh}
.config/zsh/guides/{ai.md,codex-relay.contract.md,
  codex-relay.metadata-scripting.2026-07-31.md,guide-for-builder.md,guide-regime-session.md}
reposoma/maintenance/codex-line/runcard.codex-onboarding.2026-07-24.md
reposoma/raw.guides/codex-line.{builder,user}.md
reposoma/temple/decisions/{0001,0002,0005,0006,0012,index}.md
reposoma/temple/{README,roster,system-map}.md
reposoma/AGENTS.md
```

Plus his separate named inputs: sella.coder-guide.md · sella.receipt.epoch-2026-08-02.md ·
sella.observation.atlas-office (below) · ferry.md · _staging/README.md · WAVE.md · the
Jacquard pad.

**Blind spots (weigh his generalizations accordingly):**
- His "Claude side" agent sample = **2 relay seats** (astrobley, vega) whose whole job is
  Bash-dispatch to his own CLI. The other ~28 agents, the entire skills tree,
  settings.json/hooks, ia-sync composer, pulses, `_mail/`, registry — unseen. His
  "file-consuming sensor" characterization of Claude agents rides a biased sample; may
  still be right, but the evidence base is thin.
- His temple picture = the governance slice (0001/0002/0005/0006/0012 + roster/system-map),
  not the operational texture. His CORE/PROFILE/HOUSE classifications need re-checking
  against what he didn't see.
- **No `.codex/` tree in the pack** — his Codex self-knowledge is harness-native, not
  file-evidenced. Both his radio and his Jacquard pad share one author: neither confirms
  the other. Decorrelation must come from my independent receipt (Epoch pass + probes).

Provenance: snapshot stays on home as dated evidence (`captured: 2026-08-03 · authority:
observation · volatile: true`). Live office files outrank it.

### [2026-08-03 · claude/atlas-office (atlas-ui) · opus · office · ref: sella.coder-guide.md + receipt + ferry.md] — conformance observation (migrated verbatim from `sella.observation.atlas-office-2026-08-03.md`, original burned to tombstone)

---
what: atlas-office conformance observation on Sella (the discipline-language) and its
     first program (@ferry) — does the real build meet the philosophy it was bred from
state: OBSERVATION — advisory, not canon; feeds majkee's gavel on sella.coder-guide.md
verified: 2026-08-03 (read: sella.coder-guide.md · sella.receipt.epoch-2026-08-02.md ·
     claude/agents/ferry.md — all on the surgical table this date)
by: atlas-office (primitive creator, office shore)
next:
  - majkee gavel on sella.coder-guide.md (canon is operator-gaveled)
  - resolve FLAG-1 (schema:1) before ferry deploys as the reference program
  - codex-line instructions block (majkee, parallel build) — cross-reference when it lands
  - close the OPEN item (agent-description budget) with one targeted Epoch pass → M→H
---

# Observation — do Sella and @ferry meet the philosophy?

**Verdict: YES — and stronger than expected. Sella is the 2026-08-01 philosophy matured
into a language; @ferry is its first clean conforming program. The rare part: the
adversarial corrections propagated, not just the original claims.**

## 1 · Fidelity — the doctrines survived their own stress test

The load-bearing check is not "did D1/D2 make it in" but "did the *corrected* forms make
it in." They did:

- **L2 (Terse header) = D1′, corrected.** Sella §2 frames `description` as the exported
  symbol and the body as never entering the parent's routing view. It did NOT repeat my
  original category error ("separate router-hints from human-docs into different file
  locations") — it absorbed the Janus finding that `<example>` blocks live *inside* the
  routing field, so the rule became "examples only if they demonstrably earn routing
  lift," not "relocate them." The broken version died in transit; the true version lived.
- **L8 (Moving compiler) = D2′, corrected.** Verbatim "unchanged `.md` ≠ unchanged
  behavior," and it **dropped** the per-run model-pin mechanism (Janus's "reproducibility
  theater" REVISE), replacing it with receipts/pilots/gavels. The ceremony Janus flagged
  is absent; the epistemic guardrail that survived is present.

Receipt trail: Sella cites the two 08-01 research files ([S2] arch study, [S1]/[S-EPOCH]
mechanics) plus [S5] the nablarva conforming-application precedent. Grounded, dated,
`state: DRAFT — pending majkee gavel` — it has not jumped the canon gate.

## 2 · @ferry — the doctrine made flesh (a good exemplar)

Point, don't re-list: ferry embodies terse no-example description (L2), name-teaches-job
(L3 — Sella's own L3 example), minimal explicit `tools` with no Write, a graded G0–G4
**exit ladder** as exit-code legibility (L4), judgment-here/mechanism-there
(`ferry/prep-home.sh`), vendor-invariance (contract = the ORDER, not a print-flag), and
— the sharp part — L8 as *behavior not ceremony*: "my route holds because each leg
re-verifies reality, never because last crossing worked." The moving-compiler honesty is
baked into `fetch-real-first`, not bolted on. This is what conformance should look like.

## 3 · FLAG-1 — `schema: 1` contradicts Sella itself (resolve before deploy)

ferry.md carries `schema: 1`. But: Sella §2's key surface does not list `schema`; the
Epoch receipt states plainly *"No `schema` key exists — house `schema: 1` is
forward-marker only"*; and Walk A step-3 gate says *"every key exists in the [S1] table —
no invented keys."* So the reference program trips its own gate. This is STUDY-2
tension #5 (the `schema: N` idea) half-surviving: present in ferry, unblessed in Sella.
**Resolve one way:** either Sella explicitly names `schema` a sanctioned house
forward-marker and exempts it from the no-invented-keys gate, or ferry drops the key.
Not cosmetic — a language's first program must not violate the language.

## 4 · FLAG-2 — recursive-minimalism risk (watch, don't fix yet)

Sella is a 380-line, nine-law language with a machine model, three walks, and a glossary.
Its *own* [S2] arch study says this audience reads every new layer as "prove you're not
bloat" and treats heaviness as a red flag. A coder-guide is a legitimate human full-read
(L9 grants humans full reads). The risk is only if *conformance* starts meaning "an agent
loads all nine laws." Philosophy-true form: **Sella stays the human guide; primitives
conform via a terse anchor (a provenance stone + the gates that apply), not by ingesting
380 lines.** Keep it a guide, not a liturgy. This is the language passing — or failing —
its own L9 and L2 at the meta level.

## 5 · OPEN — the mechanism gap is real and honestly marked

The Epoch receipt (claim 2) confirms *"Agent-description budget: UNRESOLVED — no analogous
cap found."* So L2's agent side rests partly on the skill-side 1,536-char cap; the
agent-side is not proven. Sella marks this honestly rather than papering it — correct.
But it means L2 is CONFIDENCE-M for agents until one targeted Epoch pass closes how the
`Agent`-tool `subagent_type` schema serializes descriptions into the parent request. Close
M→H before L2 is codified as hard canon; if the router reads only the `description` field,
nothing changes, but the budget claim needs its receipt.

---

*atlas-office observation · staged, deploy-inert · 2026-08-03 · advisory to majkee's gavel.*

