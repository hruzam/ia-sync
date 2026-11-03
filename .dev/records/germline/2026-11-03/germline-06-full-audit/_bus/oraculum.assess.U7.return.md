---
from: oraculum · unit U7 · date 2026-10-21
unit: U7 — return shapes (prescribed form · landing · delivery proof)
mode: audit-only; nothing edited, nothing dispatched
read: field.U7.return.md · bus/GUIDE.md :15–120 · HANDSHAKE.md :20–49 · identity.md :55–149 · binding.claude.md :30–69 · binding.codex.md :28–87 · cards/consult.md · cards/audit.md · germline/README.md · carry-unfinished.md · saddle-project.md :24–35 · journal 2026-10-21 :190–219 · _mail/README.md :1–40 · RECONCILE.G01 §1 · RESULT.U3 §6/§9 · RESULT.U5 §6 · RESULT.U6 §6 · claude/agents/houston.md :24,:40–42
---

# Oraculum — U7 assessment

**Governing insight (inferred: oraculum).** A return is three concentric envelopes — *proof block* (which files loaded, by stamp), *kind line* (what sort of answer this is), *body* (free text) — and the corpus already has the first two as `key: value · key: value` lines. What is missing is not a shape but two sentences: the kind line's *position* (contiguous, first after the proof block) and the statement that *a consult is never a bus seat*. Delivery needs no new mechanism: the proof block, quoted verbatim by the consumer's first act on disk, is the receipt — relays that drop it are not evidence (RECONCILE §1, `said:` "relay heads drop stamps (C2, X1 release) → proof point is the child's own first answer").

## (1) Consult return — one owner per piece

Apply U2 §6: bootstrap law (what to read · in what order · how to prove it) may live in wrapper + one germline file; everything post-bootstrap has exactly one owner.

| piece | today | owner (proposal) | why |
|---|---|---|---|
| Route line + canary | wrapper :40, bindings :57/:78 | **wrapper** (bootstrap) + **binding.<vendor>** as the one germline twin | vendor-specific by nature (canary is the wrapper's); identity stays vendor-blind (:131–133) |
| stamp lines `<abs path> · stamp: <tok>` | wrapper :41, bindings, README :9–11 | **wrapper** (bootstrap) + **README :10–11** (germline-wide stamp rule) ; bindings carry only vendor extras (`cwd`, `selected:` per U5 §6) | README already owns the stamp rule; the bindings' copy is the "proof-line detail" U2 §6 names as post-bootstrap → one owner = binding for the extras only |
| `card: X · verdict: Y` fields | identity :123 | **identity §Return contract** — add the position: *"the first line after the proof block"* | vendor-blind, card-blind grammar; today position is observed (C-def.2) not prescribed (Field H5) |
| verdict vocabulary | identity :123 **and** consult :36–40 | **card** (consult: `fits…`; audit :20: `mech·judge·cross`); identity cites "values: the card" | identity :123 is a duplicate of consult :36–40 |
| "≤5 constraints · page or less" | consult :34 | **consult card** (unchanged) | card-local economy |
| `said:`/`inferred:` kept apart | identity :66 **and** consult :34 | **identity §Evidence discipline**; consult cites | duplicate |
| "the hole" (frame defect · required properties) | identity :127–128 | **consult card**, beside `unclear` (:39–40, :46 "the shelf has a hole") ; identity cites | it is the payload of one consult verdict. *Alternative:* keep in identity if audit `judge` findings also return holes — then consult cites. (inferred) |

**Minimal complete prescription** (Houston, any card, any vendor):

```
Route: … (canary: <prefix>-<8hex>)              ← wrapper (bootstrap)
<abs path> · stamp: <tok>[ · cwd: …][ · selected: …]   ← one per file, load order (bootstrap; extras: binding)
card: <card> · verdict: <value>                  ← identity: first line after the proof block
<body as the card prescribes>                    ← card
```

Answer to the question "wrapper, binding, identity or card?": **proof block = bootstrap (wrapper + README/binding); kind line = identity; body = card.** The wrapper does *not* carry the kind line — card semantics are post-bootstrap (U2 §6), and when the germline fails to load the first finding is the missing file, which needs no card header.

## (2) The bus/consult boundary

Flight's reading holds; I tested it and it is an **unwritten boundary, not a conflict**. Evidence: bus GUIDE :34 `said:` "`<seat>` is the writer" + consult :13 `said:` "I never write… no exception for my own finding" ⇒ a consult Houston cannot appear in a `_bus/` filename at all. The runtime already resolves a mis-addressed POINT: C-def.2 answered `out of card: writing .dev/session/houston-note.md → session head` (Field H7). So D1 is already closed mechanically; what is missing is the sentence that stops a head from writing `return_to: _bus/NN.houston.return.md` under consult in the first place.

**Does :56 imply it?** No. "No bus for one seat" governs single-seat *sessions*, not which seats may write. The implication comes from :34 + consult :13, by inference only.

**The sentence (owner: consult card §Writes, after :33):**
> *"A POINT addressed to me under consult is answered in the invoker's context, never as `_bus/NN.houston.return.md` — I am never a bus seat under this card; the head's own RETURN cites `raw/consult.<topic>.<date>.md` (or quotes my proof block and kind line verbatim) as its evidence. Under audit or sitting a `_bus/` landing is possible only when the invocation assigns it, and then takes the bus GUIDE's six headings."*

Placement alternatives: bindings' `return` row (:40/:45) — rejected, vendor-neutral rule would need two copies; bus GUIDE — rejected, U6 §6 (a GUIDE carries no germline rule's operative wording). Audit card :26–27 gets the half-clause "(a `_bus/` landing takes the bus GUIDE's six headings)" — that is the only place the GUIDE needs to be *pointed to* from the germline.

## (3) Delivered / consumed — what exists, what is warranted

What each surface already provides (said, per Field B):

| surface | available | delivered | consumed |
|---|---|---|---|
| `_mail/` | inbox presence | — (next orient walk) | `mv` to archive (:16–17) |
| `_bus/` | file presence | — by design (:57 "no doorbell") | VERDICT only (:48) |
| HANDSHAKE | disk (:30) | — | `consumed-by:` prepend / archive move / **the reply** (:35–39) |
| Agent-tool return | n/a | **runtime-guaranteed** (tool result lands in the spawner's context) | the head's next act citing it (raw/ record · STATUS `holds:` · RUNBOOK constraints — consult :29–33) |
| journal carry | — | — | `CARRIED TO/FROM` pair |

Correction to Field H4 (inferred): the carry pair is **not** a bilateral receipt. One writer (the function) appends to two scopes it owns; it is a *link*, not a handshake. So the corpus has zero two-sided receipts, and that is fine — every surface closes by the **consumer's act**, never by the sender's.

**Is a general mechanism warranted? No.** HANDSHAKE :35 already says `said:` "by the existing house mechanism, no new one"; identity :115 "ceremony is earned by evidence"; AGENTS.md bias. The rule is already three-quarters written across HANDSHAKE :38 ("the reply itself is the strongest stamp") and RESULT.U6 §6 ("relayed text is not proof"). Proposed single sentence, germline-wide:

> *"A return is delivered when the consumer's first act on disk quotes its proof block and kind line verbatim; a record that relays a return without them is a relay, not evidence, and does not close the exchange."*

That is exactly what went wrong in G01 (C-def.claude PASS "stamp lines not itemized in the Assay row"). Alternatives: (i) `consumed-by:` on every return — rejected, inline tool returns have no file to prepend to; (ii) a receipt ledger/registry — rejected by bias and by myShell §1.6 ("no second dispatcher/registry"); (iii) nothing — rejected, RECONCILE §1 shows the cost. myShell's three states stay as *vocabulary* (available · delivered · consumed) in the sentence's gloss, not as states a mechanism tracks.

## (4) One header grammar — RETURN side only

The house already converges on one line form: `key: value` pairs joined by ` · ` (stamp lines, `CARRIED TO … · <ref>`, mail filenames, U5's `selected:`). I propose naming it, not inventing it:

```
header   := [route-line] proof-line+ kind-line
route    := Route: <text> (canary: <prefix>-<8hex>)         — agents with a wrapper only
proof    := <absolute path> · stamp: <8hex>[ · <key>: <value>]*   — one per file read, load order
kind     := <kind-key>: <value>[ · <key>: <value>]*          — exactly one line; first after proof block
body     := free text (card/fn prescribes content, not shape)
```

Parser contract without a parser: split a line on ` · `, then each field on the first `: `. ` · ` (U+00B7) survives paste into shell, YAML and Markdown — Epoch's binding constraint (RESULT.U3 §10) — unlike `&`.

Instances:
- **Houston:** `card: consult · verdict: stretches` — unchanged content, position fixed. `out of card: <X> → <Y>` is already a kind line (key `out of card`); leave.
- **Programs (U3 §6, now in the same grammar):** proof `<controller abs path> · stamp: <tok>` / `<fn abs path> · stamp: <tok> · expected: <tok>` (the expected-value table check made visible — the programs' one structural advantage); kind `fn: carry-unfinished · result: report | pair | incomplete-pair`. Values are each fn's own; the grammar fixes only the keys.
- **saddle-project:** `fn: saddle-project · result: READY` then the READY content. This moves the bare `READY`/`HELD` first token (saddle :28–31) into a value — Majkee's corner, mark as *his* edit. *Alternative:* leave `READY`/`HELD` bare and put the kind line before it — weaker, two first-tokens.

**Leaves unchanged:** Route line; stamp lines; `out of card:`; `CARRIED TO/FROM` (a journal receipt line, not a return header); bus POINT/RETURN/VERDICT (bus surface, YAML, outside germline); mail filename; audit `mech·judge·cross` and `said:/inferred:` (body-level line tags — already parser-friendly, stay free text). **Changes:** kind-line position (identity :123); program proof + kind lines (both CONTROLLERs :54, five fn Return lines); saddle READY/HELD value form (optional). **Does not touch** invocation lines — `fn:` echoes the invoked name, it does not define `ctrl X&Y` (C1 stays with Cartan).

Home: `germline/README.md` beside the stamp rule :10–11, three lines; wrapper carries the Houston instance (bootstrap, already :40–42); bindings cite; controllers carry the program instance.

## (5) Neutral Houston · audit without addendum

Rule (owner: audit card :26–27, one clause; identity :144 cites): *"No addendum → the landing path is the one the invocation assigns, inside the invoking session's bed; neither assigned nor addendum-named → the reply is the landing: findings return inline, I open with `out of card: landing unassigned → invoker`, and write nothing."* Consult is unaffected (head's pen already — consult :29–33; no bed → the reply is the record). Sitting unaffected (own bed, :19–23). Alternative: a global default such as `~/ia-sync/.dev/observations/` — rejected: a landing registry, and ia-sync is one project among many.

## (6) GUIDE/reference vs agent-consumable at runtime

- **Agent (Houston) needs at runtime:** identity §Return contract, binding §Return shape, card §Returns/§Writes — nothing else. Plus bus GUIDE §RETURN :80–102 **only** when POINTed under audit/sitting with a `_bus/` landing (hence the audit-card pointer in (2)).
- **Programs need:** their fn + controller; no GUIDE.
- **Head only:** bus GUIDE §What/§Verifying/curvature, status GUIDE (Houston never writes STATUS), `_mail/README` (temple bus between seats), HANDSHAKE (cross-runtime — Houston is never a party; the head and Cartan are).
- **Reference, human:** bus GUIDE :17–25, HANDSHAKE §Presence, journal 2026-10-21 :198–214.

## (7) Fold / repair destinations (nothing applied)

| finding | primary destination | alternative |
|---|---|---|
| kind-line position | identity :123 — "…, as the first line after the proof block" | each card §Returns |
| verdict vocabulary duplicate | identity :123 → "values: the card"; consult :36–40 owns | leave (harmless) |
| `said:/inferred:` restated | consult :34 → cite identity :66 | leave |
| the hole | consult :39–40/:46 (owner); identity :127–128 → cite | keep in identity, consult cites |
| proof-block extras (`cwd`, `selected:`) | bindings :57–60 / :78–81 only; identity gets one cite line "proof block: wrapper + binding" | identity carries it (rejected: vendor-blind) |
| bus/consult boundary sentence | consult :33 (after "cites it in …") | bindings `return` row :40/:45 (two copies) |
| `_bus/` landing takes six headings | audit :26–27 half-clause | bus GUIDE (rejected, U6 §6) |
| neutral / unassigned landing | audit :26–27 clause; identity :144 cite | global default dir (rejected) |
| delivery sentence | README beside the one-witness rule (U6 §6 destination) | HANDSHAKE only (ia-sync-local; misses programs) |
| HANDSHAKE :35–39 | add one cite to README's sentence (Flight-editable, no stamp) | — |
| header grammar (three lines) | README :10–11 | identity (rejected: programs don't read it) |
| program proof + kind lines | both CONTROLLERs :54; fn Return lines fold-entry :31, list-pending :19, audit-beds :23, carry :30, saddle :28 — Majkee's corner | engine README prompt template (reference, weaker) |
| bus GUIDE :56 | no change | — |
| sitting.md stub | nothing until written; grammar applies when it is | — |

Every identity/card/binding edit re-rolls a stamp and, under the one-witness rule, needs a fresh-session witness per route — batch into **one GO**, one re-witness.

## (8) Decisions

**Consequential (Majkee):**
1. Adopt the one header grammar germline-wide (README), including the program instance — it touches his personal programs (READY/HELD as value) and sets the parser-friendly shape he asked for (RESULT.U3 §9 item 4).
2. The hole moves to the consult card (identity edit → re-roll → re-witness).

**Mech (author with GO; Flight may draft):** kind-line position; boundary sentence in consult §Writes; audit `_bus/`/neutral-landing clauses; identity cite lines; README delivery sentence; HANDSHAKE cite; program proof/kind lines (Majkee as author of his files).

**Not decided here / for whom:** whether audit findings carry a per-finding kind line (`finding: mech · …`) — later, after audit telemetry exists (identity :115). C1 invocation grammar — Cartan, untouched. Sitting's return shape — written at the first real sitting.

**Tags.** `said:` all quoted line refs above; `inferred: oraculum` — the three-envelope reading, "carry pair is a link not a handshake", "D1 is an unwritten boundary already closed at runtime by `out of card:`", the grammar's key set and value sets. Not read: status GUIDE body, sitting.md body, nablarva addendum, any `.jsonl`.
