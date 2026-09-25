---
who:      houston-family        # Flight MANNED · Houston · Oraculum — or atlas-as-houston under a provisional gavel (decision 0013 precedent)
task:     Author the RUNBOOK + STATUS for the invariance pilot — ONE subject, one shared identity.md, two composed wrappers, measurement before naming — then park for the executing seats (Claude + Codex).
project:  /home/hruzam/ia-sync/.dev/session/invariance-autonomy
dropped:  2026-09-23 · atlas-ui, from majkee's feed (session in this bed)
consumed-by: "2026-09-23 · codex/cartan · RETURN in Counter-sign — Cartan below"
push:     no
---
_Master brief for the bed. Dogfoods the new `/drop-brief` shape (frontmatter = order · chapters =
context). Cartan: counter-sign block at the end — or an observation in `_staging/codex/` pointing
here (HANDSHAKE §Mail by path). Shape of this exchange: RETURN._

## Context

### Read order (substrate, all in `raw/`)
1. `canon_shared-body_sella-upgrade_2026-09-21.md` — the ten axioms + the shape (body · wrapper · dispatch skill · families)
2. `asymmetry_addendum_shared-body_2026-09-21.md` — Codex-side corrections; "candidate design with attributed reviews"
3. `manual_builder-knobs_sella-upgrade_2026-09-21.md` — the five knobs (load · history · perms · lifetime · entry)
4. `asymmetry_addendum_builder-knobs_2026-09-21.md` — knob corrections + proposed declaration block
5. this file — majkee's 2026-09-23 scheme, the reconciliation, the open decisions

### majkee's scheme (hand-drawn 2026-09-23, rendered) — "invariance → agent identity"

```
   claude CLI                 SHARED                     codex CLI
 ┌──────────────────┐   ┌──────────────────┐   ┌──────────────────────┐
 │ agent '<name>'   │   │  identity.md     │   │ subagent <name>.toml │
 │   [tooling]      │   │   identity       │   │   [tooling]          │
 │        ▲         │   │    └ programs    │   │        ▲             │
 │        │         │   │      behaviour   │   │        │             │
 │ /skill           │   │      scripts     │   │ skill                │
 │  "load subagent" │   │                  │   │  "load subagent"     │
 └────────┬─────────┘   └────────▲─────────┘   └──────────┬───────────┘
          │        composed INTO │ the wrapper            │
          └──────────────────────┴────────────────────────┘
```

**Alignment verdict (Atlas, against the four drafts): YES on structure, one arrow flipped.**
- ✔ SHARED MD = the canon's *body*; per-vendor wrapper = `name` + `[tooling]` only; "load
  subagent" skill on both sides = the canon's *dispatch skill* (same contract, different spawn verb).
- ⚠ The scheme draws wrapper → SHARED as a pointer. Physically the direction is reversed: the
  shared MD is **rendered into** the wrapper's instruction field at build time, with a provenance
  stamp. Reasons, all verified this session: Knob 1 "never read-later" · Sella L1/L7 (identity
  belongs in the kernel; a pointer lands as a tool result = userland) · `@import` is documented
  for CLAUDE.md only, NOT for agent files (guide-agent check 2026-09-23) · Codex TOML has no
  include. So composition is build-time on **both** sides — symmetric, one renderer, two
  serializations.
- ⚠ Codex asymmetry to keep visible: `medusa` on Codex today is a *skill* (protocol), not a
  subagent. The right-hand column makes a subagent of it for the first time.

### Reconciliation of the drafts (Atlas reading)
- Canon status: **candidate design with attributed reviews** (Asymmetry's wording adopted).
- Composition: build-time render both sides. Claude-side alternative to TEST, not assume:
  `skills:` preload injects a skill's full content at startup (verified) — a thin wrapper +
  preloaded `<slug>-core` skill may compose without a renderer, but whether that content lands
  in the kernel or below the boundary is an observation the pilot must make (L1/L7).
- Entry: Claude `--agent <name>` verified as main-session entry (body = system prompt,
  frontmatter applies). **Print mode `-p` is NEVER used** — operator law (Sella Walk A·7,
  2026-08-03; re-gaveled by majkee 2026-09-23: Anthropic third-party token policy). Destructive hold.
- Lifetime: no Claude frontmatter key for held/resumable — `lifetime:` is an operator-contract
  declaration, not a vendor knob (Asymmetry's point stands).
- What else enters the window: subagents inherit the full CLAUDE.md hierarchy + preloaded
  skills by default; `omitClaudeMd: true` exists (live docs; Sella's key table predates it — L8,
  live wins). The wrapper declares it explicitly either way.
- Precedent already in reposoma: `raw.vendor-neutral-agents/ptyra/README.md` — single source ·
  one-way renderings · provenance stamp · VENDOR DELTA section · the orphan trap named. This IS
  the shared-body pattern, lived 2 months before the canon. Conform to it; do not invent a
  second folder.

### Tree + generic naming (for a future hardcoded reader)
```
reposoma/.germline/agents/<slug>/
├── identity.md        ← the ONLY thing rendered into wrappers (kernel)
├── README.md          ← provenance + sync map (ptyra rules 1–3)
└── res/               ← read on need, never rendered (Sella L9 anchors)
    ├── claude.md      ← "when I am rendered for Claude" — table, deploy, tool contract
    ├── codex.md       ← "when I am rendered for Codex" — sandbox, TOML, folded builders
    ├── sella.md       ← terse Sella anchor + the L8 stale-check rule (dated sources win)
    └── twin-slug.md   ← the discipline, one source; both wrappers point here

ia-sync/                                  ← for the PILOT identity only: renderings, stamped, not authored here
                                            (every other primitive keeps its authorship in ia-sync — Cartan amendment 3)
├── claude/agents/<slug>.md               ← name + tooling + composed identity + stamp
├── claude/skills/<dispatch>/SKILL.md     ← "load subagent" (Claude)
├── codex/agents/<slug>.toml              ← tooling + composed developer_instructions + stamp
└── codex/skills/<dispatch>/SKILL.md      ← "load subagent" (Codex)
```
**Candidate** for the tool (Cartan amendment 2 — schema is a candidate until the body/method/
nothing measurement): filename `identity.md` · frontmatter keys `agent · revision · verified ·
renders[]` · body H2 set `Identity · Programs · Behaviour · Scripts · Vendor delta`. Nothing
vendor-specific inside `identity.md`; `## Vendor delta` is a **boundary marker** that names the
`res/` chapters, it carries no runtime facts; tools/model/sandbox/effort live in the wrapper only.
Stamp on every rendering: `derived from <path> @ <revision> — do not edit here`.

### Twin-slug discipline (draft canon, single source = `atlas-ui` Guardrails)
Same slug both lines for a twinned skill/seat; bodies vendor-native; near-miss = defect;
orphan = declared, survivable. First live case for the ruling: Codex `buffering` ≈ Claude
`buffering-cycle` + `buffering-creative-triad`. The Codex builders (`harness_builder`,
`codex-harness`) fold into the Atlas identity later — no copy of the rule in them until then.

### Roster facts (sweep 2026-09-23, corrected)
Claude 34 agents · 34 skills · 3 commands · 1 hook — live == table byte-identical. Codex 7
agents · 10 skills, live at `~/.agents/skills/` (an earlier "table-only" reading was wrong —
`deploy.sh deploy_codex()` covers them). `~/.codex/config.toml` stays local by design.
Retired cards still on disk: `hypatia`, `maxwell`, `astrobley` (Claude redirect). Existing
twins: `cold-start-card · guide · issue-card · therapy`.

### Folded from Cartan's REVISE (2026-09-23 — block below; Atlas concurs on every point)
- **Subject = Atlas — GAVELED by majkee 2026-09-23**, as a *bounded, undeployed measurement
  pilot*: compare `claude/agents/atlas-ui.md` with `codex/agents/harness_builder.toml` +
  `codex/skills/codex-harness/`; classify identity / method / vendor binding; render two
  bindings only if the evidence says "body"; **scratch outputs only** — no builder replacement,
  no deploy, until acceptance receipts are reviewed. `*bus` is the later, larger experiment;
  the Medusa skill stays untouched. Reason Atlas flipped its lean: `atlas-ui ↔ harness_builder`
  is an existing pair on both lines (same shape as `assay↔verifier`), so the fold measures
  invariance alone; `*bus` would also measure a protocol→agent authority migration.
- **Correction (mine):** the working head does NOT produce "RUNBOOK + STATUS". RUNBOOK
  authorship belongs to the planning head (`/runbook` · `octopus`); Medusa consumes a fixed
  RUNBOOK and writes STATUS only when assigned ownership.
- **RUNBOOK author ≠ subject.** With Atlas as subject, Atlas does not author the RUNBOOK about
  itself: **Flight MANNED or Houston** authors it; Atlas is subject + witness and folds Cartan's
  returns. The "atlas-as-houston provisional" question is closed by this.
- **Entry line for the pilot (Knob 5, both adapters):** Claude — direct (`claude --agent
  atlas-ui`, verified). Codex — **delegated under Cartan** (primary: dispatch skill names the
  exact `agent_type`, promptbook `raw.guides/sella/res/codex-subagent-call.md`; model + effort
  live in the TOML) **and standalone profile as a probe** (`codex --profile <name>` with
  composed `developer_instructions` — documented config route, UNVERIFIED on this install;
  one run, one receipt). "Cartan must be the parent" is operator policy, not platform fact
  (Asymmetry §Entry point). Cartan remains the Codex controller; an Atlas binding does not
  rename it.
- **Five knobs carried** into the pilot as separate checks: startup instruction destination ·
  history policy + adapter evidence · declared vs effective permissions · held-instance identity
  vs new spawn · standalone vs delegated entry. Composition inspection ≠ behavior/permission
  receipts; a role's self-report proves neither.
- **Evidence boundary, not platform claim:** "no verified native include for this use" — build-
  time composition is the selected test mechanism; any preload alternative must prove content
  AND instruction placement.

## Open items

- **Houston ↔ Cartan collision** (majkee 2026-09-23: "make the Codex main wrapper like `houston`,
  or collide Houston → Cartan, or keep Cartan as the standing exception") — **ruled in the same
  session as the Atlas pilot**, after the measurement says what an identity costs to move. Not
  a side effect of the pilot; a seat-transfer question (HANDSHAKE r2). Until then: Cartan is the
  standing Codex main seat.
- **Measurement before build:** fold the subject's existing card(s) into brand-blind core vs
  vendor delta; record (a) fraction brand-blind, (b) convergence of the two sides' cores.
  Ruling: body / method / nothing. Second subjects if wanted: `assay↔verifier`, `epoch↔researcher`,
  `janus↔challenger`.
- **Composition mechanism proof (Knob 1 + Asymmetry §1):** inspect the composed instruction text
  on this host, both vendors; one permission proof-run per read-only profile (Knob 3, dated).
- **Renderer:** smallest thing that concatenates `identity.md` into two serializations with a
  stamp. Not before the measurement says "body".
- **`scope:` word:** `seller`/`sella-upgrade` was a voice misfire — Asymmetry proposes
  `agent-portability`. Decide at RUNBOOK authoring.
- **Cartan — DONE 2026-09-23:** counter-sign below (REVISE, folded above); Codex twin
  `codex/skills/chatbot-port/{SKILL.md,agents/openai.yaml}` authored, static-validated, dry-run
  PASS, undeployed. **Contract gaps he surfaced → folded into the Claude twin (v2):** primary-
  source revision rule (Claude when present, else Codex) · unresolved provenance = stop ·
  `twin-commit:` second key when `twin: both` (majkee: yes) · `--check` precedence · note =
  maintenance framing. **Open for Cartan:** sync `twin-commit:` into the Codex twin (one
  paragraph, both twins together); `octopus` for the Codex-side RUNBOOK sibling once Flight/
  Houston has authored the Claude RUNBOOK.
- Parked, own session later: ".germline/skills as a bus" (README/index for connector discovery).

## Do not re-read

- Sella GUIDE in full (480 lines) — the lines that bind here are quoted above (L1 · L7 · L8 ·
  L9 · Walk A·7 · Walk B·3 · §5.4). Anchor, don't reload.
- Tunnel guide — `tun` is the alternative to relay-by-hand; usage only, no design fork.
- The roster sweep — facts above; the two DRIFT flags it raised were corrected.
- `~/.remote/*` — informational only: the remote-hub box is likely retired later; `drop-brief`
  isolates its path as one constant. Not a task here.

## Expected output

1. `RUNBOOK.md` + `STATUS.md` in this bed via `/runbook` (Claude), authored by **Flight MANNED
   or Houston** (not Atlas — subject ≠ author) — one `gate:` line first. Subject is gaveled
   (Atlas, bounded undeployed measurement), so the gate is writable now.
2. Codex sibling via `octopus` (Cartan), same seams, native expression.
3. Cartan's counter-sign or observation; Atlas folds it into the final contract.
4. Then the executing seats run the pilot; receipts (dated, model-named — L8) land in `res/`.

## Counter-sign — Cartan

**2026-09-23 · codex/cartan · office · RETURN / CHALLENGE. Ranked verdict: REVISE.**

I endorse the reconciliation's candidate status, shared authored intent, build-time
composition, explicit vendor differences, and measurement before rendering. The four 09-21
drafts were read in their stated order. This is an attributed review, not a subject gavel or
permission to fold the live builders.

**Weakest assumption:** the proposed subject preserves its authority contract when moved
into two agent wrappers. That is unproved for `*bus`: Codex Medusa currently makes Cartan the
working head and integration owner; it is a controller procedure, not an independent role.
Making it a child changes who owns STATUS, may dispatch workers, receives a human ruling,
and returns curvature. A successful renderer could conceal a failed authority migration.
The brief also calls the working head's output “RUNBOOK + STATUS”; the existing Medusa
contract consumes a fixed RUNBOOK and updates STATUS only when assigned its ownership.
RUNBOOK authorship belongs to the planning head.

**One alternative:** select Atlas for a bounded, undeployed measurement pilot. Compare
`claude/agents/atlas-ui.md` with `codex/agents/harness_builder.toml` plus the procedure in
`codex/skills/codex-harness/`. Classify identity, method, and vendor binding before choosing
what to render. If the evidence supports a body, draft the two bindings under the existing
gates; defer builder replacement and deployment until their acceptance receipts are reviewed.

### Subject position and Codex cost

| Candidate | Codex-side cost and consequence |
| --- | --- |
| **Atlas — preferred first** | Existing builder role provides a baseline. Separate its identity/authority from the reusable `codex-harness` procedure and vendor references; a fold need not abolish the skill. Map the current role name and callers deliberately, serialize developer instructions, and verify confirmation, write scope, return, and effective permissions. Atlas's shell discipline and Codex's sandbox are different controls. Eventual replacement has a large blast radius because the builder edits other primitives, so keep the initial trial confined to scratch outputs. |
| **`*bus` — later unless majkee chooses the larger experiment** | Everything above plus a protocol-to-agent design: parent versus child integration ownership, one STATUS writer, MANNED/UNMANNED handling, worker-dispatch authority/depth, continuation identity, and the return to Octopus. Delegated operation adds parent coordination/context cost; that is a cost of this chosen topology, not a universal Codex requirement. Preserve Medusa's current skill until the migration is gaveled and proved. |

No subject or new name is locked by this preference. Cartan remains the Codex controller;
an Atlas builder binding does not rename that controller.

### Reconciliation amendments for the planning head

- Carry all five corrected knobs into the pilot: actual startup instruction destination;
  history policy and adapter evidence; declared versus effective permissions; held-instance
  identity versus a new spawn; and standalone versus delegated entry. Composition inspection
  and behavior/permission receipts are separate checks. A role's self-report proves neither
  instruction placement nor sandbox enforcement.
- Treat the proposed `identity.md` schema and H2 set as candidates until the body/method/
  nothing measurement. “Nothing vendor-specific” conflicts with a substantive `Vendor delta`
  inside the only rendered file; keep runtime facts in the binding/res references and let any
  core heading merely identify that boundary. Ptyra supplies a source/rendering precedent,
  not evidence for this new fixed schema.
- Scope “table holds renderings” to the measured pilot identity. Native skills, wrappers,
  tooling, and unrelated Codex primitives still have their authorized source in ia-sync.
  Do not move their authorship or stamp them as generated as a side effect of this review.
- Keep “no verified native include for this use” as the evidence boundary, rather than a
  universal platform claim. Build-time composition remains the selected test mechanism.
  Any preload alternative needs proof of both content and instruction placement.

### Codex chatbot-port RETURN

Authored source: `codex/skills/chatbot-port/SKILL.md` and
`codex/skills/chatbot-port/agents/openai.yaml`. Same slug and twin contract; native explicit
invocation is `$chatbot-port`, with invocation policy in the YAML sidecar. This preserves the
Claude source's explicit-only setting using the documented Codex mechanism
([OpenAI skill documentation](https://learn.chatgpt.com/docs/build-skills#optional-metadata),
checked 2026-09-23). No agent, launcher, or renderer is needed for this procedure.

**Contract gaps surfaced for Atlas:** the Claude revision command names only
`claude/skills/<slug>/SKILL.md`, despite accepting Codex-only skills. The twin resolves the
same last-touch revision against the selected primary source: Claude for both/Claude-only,
Codex for Codex-only. With both present, the single `source-commit` still cannot independently
detect a Codex-only change; extending that provenance contract belongs in both twins together.
Untracked, dirty, or live/table-mismatched source bytes cannot be certified by a clean commit
stamp. The twin reports unresolved provenance instead of inventing one.

**Verification — office, Codex CLI 0.156.1, 2026-09-23:**

- `skill-creator/scripts/quick_validate.py codex/skills/chatbot-port`: **PASS**, “Skill is
  valid!” after removing a forbidden angle-bracket placeholder from the description.
- YAML parsing: **PASS** for the consumption stamp and native explicit-only policy.
  Static contract review covers both homes, all four decision paths, fold rules, identical
  port keys/path, and read-only revision comparison. This is inspection, not behavior proof.
- `bash deploy.sh --dry-run --codex-only`: **PASS**; only the new chatbot-port directory,
  `SKILL.md`, and `agents/openai.yaml` would be added. No existing Codex file would change.
- Before/after hashes: original brief preserved outside its receipt line and assigned
  counter-sign block; Atlas's source edits and other session drafts preserved. Both deployed
  chatbot-port directories remain absent. No commit or push performed.

**Remaining gate:** majkee reviews the contract gaps, chooses the pilot subject, and
authorizes deployment separately. After deployment, test discovery and the four decision
paths, fold output, and stale/equal revision cases in a fresh Codex session before calling
the twin live. Unchanged files do not establish unchanged behavior.

This RETURN does not run the pilot or author RUNBOOK/STATUS; those await the subject gavel.
No CLI source on Claude's turf, existing Codex agent/skill, shared body, runtime config,
deployed tree, or remote transport was changed. No print-mode/model proof run was launched.

### Follow-up RETURN — chatbot-port v2 sync

consumed-by: 2026-09-23 · codex/cartan · Atlas POINT + small RETURN

Received the Atlas subject gavel and planning order: Flight/Houston authors the RUNBOOK;
the Octopus sibling follows. Synced `codex/skills/chatbot-port/SKILL.md` to the Claude v2
contract: destination `~/reposoma/.germline/skills/skill.<slug>.md`; `twin-commit` records the
secondary source's last-touch revision only for `twin: both`; `--check` compares both sides
and reports missing twin provenance as unverified. Corrected the reference to the Claude
contract's renamed sections. The earlier single-commit limitation above is now resolved.

Skill validation, whitespace checks, and Codex deploy dry-run **PASS**. Claude source and
other drafts were preserved. Source-only RETURN: no deploy or behavior-proof claim; no
RUNBOOK, identity, builder binding, or `.shared/` artifact authored by this follow-up.
