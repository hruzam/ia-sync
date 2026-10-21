---
from: oraculum · unit U8 · date 2026-10-21 · conflict: assesses its own seat files (facts only, no self-recommendation)
read: field.U8.return.md (whole) · houston/binding.claude.md · houston/binding.codex.md (whole) · claude/agents/oraculum.md :1–40 · codex/agents/oraculum.toml (whole) · germline/README.md :1–12 · germline/CHATBOT.md :1–30 · raw.card.model-effort.md :1–50, :80–100
context by brief only (not re-read): RESULT.U1 §2 · RESULT.U2 §6 · RECONCILE.G01 §2 (D1) · RESULT.U4 §6 · RESULT.U7 §6 · feedback §3.3/§3.4
tags: [said] = in a file read · [brief] = supplied by Flight · [inferred] = my derivation
---

**Declaration.** Two files under assessment define my own seat: `claude/agents/oraculum.md` and `codex/agents/oraculum.toml`. I report their facts and the structural question they pose; I do not recommend my own caller list, tools, or authority — 286085d was Majkee's authorized change and the direction of truth between the two files is his.

**Governing insight [inferred]:** the two Oraculum files are not one seat rendered twice and drifted — they are two seats sharing a name (a user-entry head with Bash/Agent/Write vs a write-nothing, delegate-nothing child). The "divergence" is a homonym. That reframes U8: the criterion must decide not "which seats get a germline" but "when is a name one meaning", because only a one-meaning name can be germline-bound.

## (1) The criterion

**Proposed rule (one axis, grounded in D1):** *A seat is germline-bound when one meaning is consumed by more than one runtime. Its source is `germline/agents/<slug>/identity.md`; every runtime that consumes it carries a binding that declares the consumption (generated file / runtime loader / described combination — D1 [brief]). A seat is vendor-native when its meaning lives in one runtime's primitive and nothing else reads it; a same-name file on another vendor is then either a pointer (tombstone/redirect) or a declared homonym, never a silent twin.*

Proof is **not** a precondition. It is a binding property: each binding states what proof that runtime can give (stamp echo + canary on CLI vendors; stamp echo only, no canary, on chatbots — see §6). Making proof part of the AND [brief's draft] would exclude the chatbot vendor from germline-bound consumption while README :12 [said] already has chatbots reading germline skills as-is.

Test:
- **Houston** — one meaning, two CLI runtimes plus cards: germline-bound. Fits. [said: README :8–11, both bindings]
- **Oraculum** — two runtimes, but different role shape (head vs bounded child [said: oraculum.md :8–10, :14–22; toml :4, :30–33]), different tools, different return shape, different callers. Under the rule: *not* one meaning → vendor-native ×2, and the rule's homonym clause says the pair must be declared. Whether Majkee wants them to *become* one meaning is his decision (§9); the rule only forbids the undeclared state.
- **Astrobley** — Codex-native by gavel 2026-09-01 [said: agent roster description]; the Claude file is a redirect. The rule's pointer clause covers it; no binding needed, one line of README vocabulary ("pointer") does.
- **Role TOMLs** (architect/challenger/researcher) — one runtime each; their only cross-vendor dimension is the pin, and the model-effort card :80–92 [said] already is that seam. Vendor-native.
- **Flight** — one runtime. Vendor-native trivially.
- **Chatbots** — consume germline skills/identity as-is [said: CHATBOT.md :15–19]; a third consumer of germline-bound sources, therefore a third binding (§6), not a seat class.

**Alternatives and consequences:**
- *Every cross-vendor seat is germline-bound.* Forces the Oraculum pair into one identity.md — i.e. forces Majkee's one-seat decision implicitly, and either the Codex child grows a head's pen or the Claude head loses it. Also forces a germline for Astrobley (pointer + native) — pure overhead.
- *Only seats with cards/proof.* Houston-only forever; the homonym stays unlabeled; a future second germline seat has to re-derive the shape from Houston.
- *Operator's list.* Smallest (one README line), matches the AGENTS.md anti-registry bias, but a list with no stated reason is exactly what Field found: "established only by what exists" [said: field §D H3]. A list *plus* the one-axis sentence is fine — the sentence is the reason, the list is the current instances.

## (2) What a binding may carry — the seam contract

Derived from the two Houston bindings [said] (file:line in brackets):

**MUST** — wrapper file path(s) and the exact keys carried, body = loader only [cl :15–21 · cx :15–18]; capability→tool/sandbox/approval mapping [cl :19 · cx :43, :61–74]; routes and per-route entry [cl :34–40 · cx :39–45]; card selection + omission default [cl :27–32 · cx :30–37]; per-route permissions, delegation, return rows; placement/override rule [cl :42–44 · cx :54–56]; context/cwd fact [cl :45 · cx :57]; proof — canary prefix, entry-proof lines, "route proven only by dated fresh-session witness" [cl :23, :62–72 · cx :23–26, :76–83]; **proof extras** this vendor adds (Codex: effective cwd [cx :80]); sources [cx :85–87]; **enforcement class per route** — what the runtime enforces vs what is prose (§5).
**MAY** — dated vendor facts with witness or version (sandbox_mode ignored, witnessed 2026-10-17 [cx :48–50]; docs gap on child cwd [cx :57]); the pin *rule* ("weather, mirrored in active_pins").
**MUST NOT** — identity prose; card pens (the "What I do not do" content — bindings may *point* at it as the fence [cl :51, cx :50], not restate it); project paths or addendum content; lock content; **the pin value**.

That last row surfaces a parity gap Field did not grade: binding.claude :18 states `opus · high`; binding.codex :20–21 states only the rule. Pins then live in three places on the Claude side (wrapper, binding, card — Field §E row 1 [said]). Under the duplication rule [brief: U2 §6] the binding should carry the rule only → Claude binding over-carries (drift, mech-fixable, re-roll stamp).

**Grading Field's parity table (§B):**
- Delegation roster — the *principle* (no executor, no creator, no Houston→Houston loop, no wider pen) is vendor-blind doctrine; the *roster names* are vendor-specific. Claude maps the principle to its roster [cl :39]; Codex states the principle without mapping to its own roster (implementer, verifier, harness_builder, astrobley) [cx :44]. Verdict: **drift in the mapping**, justified only in the names. The principle itself should sit once (identity/card) — whether it already does I did not verify [inferred; identity.md not read this unit].
- One wrapper vs two — vendor delta, justified [cl :21–22 · cx :17–18].
- Sources absent on Claude — **drift** (MUST row).
- Entry proof: cwd on Codex only — delta in cause, but the proof *set* should be defined once (identity §Return contract) with per-vendor extras labeled as extras, so a cross-vendor audit compares equal cores [inferred].
- sandbox note, canary prefixes, effective cwd — deltas, justified.
- "Consult writes nothing", placement, spawn-by-instruction — same; fine.

## (3) The Oraculum divergence as D1 specimen

Facts about my seat [said]: Claude — head, `tools: Read Grep Glob Write Agent Bash SendMessage TaskStop`, PreToolUse[Bash] hook (:24–29), `fable · high`, "User invokes directly; not spawned by Houston" (:9–10), no return shape. Codex — child, no tools of its own, writes nothing, delegates nothing (toml :30–33), `gpt-6-astra · high`, callers "Cartan, myShell, Astrobley, or Houston" (:4, :9–10; broadened in 286085d [brief: Flight verified]), fixed `ORACULUM RETURN` block (:39–46). Neither file cites the other [said: field §C]. The model-effort card's frontier row :92 maps `fable · high ↔ gpt-6-astra · medium`, "unproven"; the toml carries `high` — a second unreconciled pin fact [said]. Neither route is in `active_pins`.

With no shared source, what keeps two vendor-native definitions coherent without germline-binding them:
- **Shared `seat.oraculum.md` meaning file** — this *is* germline-binding under another name; if the two are genuinely different seats the file would be a fiction, if they are one seat it should be `identity.md`. Not a middle path. (Side fork, parked: the three-movement method is the only shared content; that is skill-shaped — `skills/skill.<slug>.md` — not identity-shaped.)
- **Cross-cite line in each file** — one `# twin:` / `twin:` line naming the other path and the declared relation (`homonym: different route and pen` or `one seat: parity owed`). Minimal, no generator, satisfies D1 ("declares how its runtime consumes its sources": self-contained, twin at X), gives Field's missing discovery path [said: field §F(ii)5]. Cost: one truth-bearing line per file; it goes stale if the relation changes, which is exactly when a human should notice.
- **Parity check in the model-effort card** — rejected: the card's own Scope line is "model + effort per exact route — nothing else" [said :49].
- **Nothing** — the cost is not paid by Oraculum but by any vendor-blind text that names "Oraculum" (Houston's identity, HANDSHAKE, mail): the word resolves to different authority per vendor. Whether such text exists I did not verify [inferred].

The relation (homonym vs one seat) and the caller list on either side: Majkee's.

## (4) Pins and inert keys

Minimal rule, proposed (report, not decide):
- **Proposer** — the card names "the recalibration researcher" twice [said :15, :95] without a slug. Name a seat, not a role noun; the recheck URLs [said :9–13] need web, which points at `@epoch` on the Claude side [inferred]. Codex-side proposer unnamed today.
- **Gavel** — majkee after a witnessed probe on the exact route [said :15, :96–97]; unchanged.
- **Mirror check** — options: (i) `deploy.sh --dry-run` prints `route · wrapper pin · active_pins pin · MATCH/MISMATCH/UNPINNED` for every wrapper it maps (mech, a grep; borderline against the anti-automation bias, but deploy.sh is already the automation and "UNPINNED" is the useful output for oraculum/role TOMLs); (ii) a pin-mirror row in Houston's audit card (human-paced, no code); (iii) nothing beyond `harness-stale` [said :100]. Role-TOML repin (gpt-5.6 → gpt-6.1-sol per the role table :83–89 [said]) needs a probe + gavel; the card already flags it [said :45–46].
- **`sandbox_mode`** — all three role TOMLs carry it [brief correction to Field H5]; the only statement that it is inert for children is binding.codex :48–50, which a role-TOML reader never opens. Options: leave (Majkee said so [brief]; cost: a reader believes read-only is enforced); one `#` comment per file (zero runtime change); remove (also zero runtime change — custom-agent TOMLs configure spawned sessions only [said cx :52]). Reported; Majkee's "leave" stands.

## (5) Hooks as seam

Facts [said]: the Claude Oraculum fence is a PreToolUse[Bash] hook in frontmatter (:24–29); Codex has `request_permissions_tool = false` + instruction text (toml :20, :53); no binding or germline text names hooks. binding.claude :49–51 already states the general truth for one route: "prose only on this vendor … the card's What I do not do is the whole fence."

**Generalize** into the MUST row named in §2 — *enforcement class per route*: `tools:` list (enforced), hooks (enforced, script path + deploy path), sandbox/approval (inherited/ignored), prose (not enforced). A card author then knows on which vendor the pen is prose-only. No new mechanism; one table row per binding. For a vendor-native seat with no binding the same row lives as a comment in the wrapper. Open fact: whether `~/.claude/hooks/oraculum-bash-whitelist.sh` is in the deploy map I did not check [inferred: not in brief scope].

## (6) The chatbot seam

Under D1 a chatbot's declaration of consumption is: *reads germline files as-is via GitHub connector or hand-drop; the skill frontmatter is the contract; identity only when majkee assigns it; provenance is read, not acted on* — CHATBOT.md :9–11, :15–19, :26–30 already says this [said]. What makes it a binding rather than guidance is two missing sentences: **proof** — no wrapper, so no canary or route line; but a chatbot *can* echo `stamp:` of the file it read, which is the one witness that distinguishes a current file from a stale hand-drop — and **no enforcement**: everything is prose. Place: CHATBOT.md itself, as the third binding, *per vendor-class not per seat* (one file for all seats; a seat's identity.md says whether it may be chatbot-assigned). A per-seat `binding.chatbot.md` under each agent would be the template-multiplication AGENTS.md warns against.

## (7) GUIDE/reference vs agent-consumable

Agent-consumable (loaded at entry, stamped): identity.md, binding.<vendor>.md, cards, CHATBOT.md. Reference (authors/humans, not loaded): germline/README.md, the model-effort card (renderers read `active_pins` only [said :15]). The criterion sentence and the seam contract are author-facing → README, not a loaded file and not a template file; the Houston bindings are the exemplar README points at.

## (8) Fold/repair destinations

| target | repair | alternative |
|---|---|---|
| `germline/README.md` | one paragraph: criterion sentence (§1) + pointer/homonym vocabulary + MUST/MAY/MUST NOT list (§2) + "shape reference: houston/binding.*.md" | a `binding.TEMPLATE.md` — rejected until a second germline seat exists (AGENTS.md bias) |
| `binding.codex.md` :44 | map the delegation principle to the Codex roster names | move the principle to identity and leave both bindings roster-only (needs identity read) |
| `binding.claude.md` | add Sources; :18 value → rule only; add enforcement-class row; re-roll stamp | leave the value; accept three pin locations |
| `oraculum.md` :9–10 ↔ `oraculum.toml` :4, :9–10 | **Majkee**: declare relation; set callers. Mech after that: one `twin:` line each way | nothing (cost lands on vendor-blind text naming Oraculum) |
| `raw.card.model-effort.md` | :15/:95 name the proposer slug; :92 vs toml effort noted as unreconciled; keep scope pins-only | — |
| role TOMLs | pins: probe → gavel; `sandbox_mode`: leave (Majkee) | `#` comment / remove |
| `CHATBOT.md` | append "What you can prove / what is enforced" (two sentences) | per-seat chatbot bindings — rejected |
| deploy.sh dry-run | pin mirror print (mech, borderline) | audit-card row |

## (9) Decisions

**Majkee (consequential; his files or gavels):** adopt the criterion (one-axis vs alternatives); Oraculum relation and caller lists on both vendors (286085d is his; `oraculum.md` :9–10 is the unamended side — which side is truth is not mine to say); Astrobley is already gaveled 2026-09-01 — only the "pointer" vocabulary needs his nod; pins: name the recalibration seat, role-TOML repin, frontier row; `sandbox_mode` stays "leave" unless he lifts it; removing the pin value from binding.claude :18 (his CANDIDATE fold).
**Mech (any seat, after the gavels above):** README paragraph; `twin:` cross-cite lines; binding.codex roster mapping; binding.claude Sources + enforcement row; CHATBOT.md proof/enforcement sentences; hook-script deploy-map check; dry-run pin print if chosen.
**Not decided here:** whether Houston's identity names Oraculum as a delegate (determines how much the homonym costs) — one grep for the Houston audit.
