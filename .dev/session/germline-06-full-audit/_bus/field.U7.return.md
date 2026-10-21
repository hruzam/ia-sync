---
from: field · unit U7 · date 2026-10-21
question: return shapes — prescribed form, landing path, delivery proof, for every germline consumer return
sources: bus/GUIDE.md · status/GUIDE.md · runbook/GUIDE.md · _mail/README.md · HANDSHAKE.md · identity.md · binding.claude.md · binding.codex.md · cards/consult.md · cards/audit.md · cards/sitting.md · fold-entry/list-pending/audit-beds/carry-unfinished.md · saddle-project.md · germline-05 _bus examples · TEST-INSTALL R2.C-def.2 block
---

# field U7 — return shapes corpus

## A. Return-shape table

| Return | Producer | First line / fixed keys (prescribed) | Length | Landing path | Who writes landing | Governing law |
|---|---|---|---|---|---|---|
| **Houston consult finding (child route)** | Houston (spawned) | Route line + canary; then `<path> · stamp: <token>` lines; then `card: X · verdict: Y` (form prescribed, not first-line position) | "normally a page or less" | Spawner's context (inline) | spawner / head | identity §Return contract; binding.claude §Return contract shape; consult §Returns |
| **Houston consult finding (main session)** | Houston (main) | Same Route + stamp lines; then finding | "normally a page or less" | The landing path the project addendum names | Houston or head per addendum | binding.claude :40; binding.codex :45 |
| **Consult record file** | Head (not Houston) | verbatim Houston reply | verbatim | `<bed>/raw/consult.<topic>.<YYYY-MM-DD>.md` | Head | consult.md :30–33 |
| **Houston audit findings** | Houston (audit card) | `mech · judge · cross` tagged findings + wrapper diff | no prescribed length | Paths the invocation assigns, inside the landing pattern the project addendum names | Houston | audit.md :26–27 |
| **Houston sitting drafts** | Houston (sitting card, main only) | arc · alternatives · design deltas · next gate conditions · proposed lock text | no prescribed length | Its own session bed only | Houston | sitting.md :19–23 |
| **`out of card:` relay** | Houston | `out of card: <what was asked> → <owning card or seat>` | one line | Inline; head may land | Head | identity :61–62; binding.codex :36–37 |
| **Bus RETURN** | Responding seat | Six headings: `## 1. Files changed` … `## 6. Remaining uncertainty`; file: `NN.<seat>.return.md` | no explicit limit | `<session>/_bus/` | Responding seat | bus GUIDE §RETURN |
| **Bus POINT** | Delegating seat | YAML: `cycle · turn · from · to · scope · paths · gates · done_when · return_to` | terse, executable | `<session>/_bus/NN.<seat>.point.md` | Delegating seat | bus GUIDE §POINT |
| **Bus VERDICT** | Verifying seat | YAML: `cycle · turn · point · return · verified_by · disposition · gate_effect · status_rewritten` + three sections | no explicit limit | `<session>/_bus/NN.<seat>.verdict.md` | Verifying seat | bus GUIDE §VERDICT |
| **Program: fold-entry** | fold-entry function | "Return exact file/chapter, appended event, evidence checked, and any unverified claim" | not prescribed | Inline / caller's context | function | fold-entry.md :31 |
| **Program: list-pending** | list-pending function | Grouped source/date/chapter, brief matter, wording/state, owner/source pointer, verification status | not prescribed | Inline / caller's context | function | list-pending.md :19–20 |
| **Program: audit-beds** | audit-beds function | Findings + smallest suggested dated correction/carry pointer | not prescribed | Inline / caller's context | function | audit-beds.md :23 |
| **Program: carry-unfinished (report)** | carry-unfinished function | Report of candidate pointers and uncertainties | not prescribed | Inline / caller's context | function | carry-unfinished.md :20 |
| **Journal receipt: CARRIED TO** | carry-unfinished (authorized write) | `CARRIED TO <destination file#heading> · <reference>` | one line | Source own-scope journal entry | function | carry-unfinished.md :25 |
| **Journal receipt: CARRIED FROM** | carry-unfinished (authorized write) | `CARRIED FROM <source file#heading> · <reference>` | one line + classification + owner/evidence pointer | Destination own-scope journal entry | function | carry-unfinished.md :26 |
| **saddle-project READY** | saddle-project function | `READY` followed by: alias, verified absolute root, actual host, AGENTS chain, required-read evidence, task words, scoped paths, authority, next governing owner/read pointer | not prescribed | Inline / caller's context | function | saddle-project.md :29–31 |
| **saddle-project HELD** | saddle-project function | `HELD` with exact path and missing decision/material | not prescribed | Inline / caller's context | function | saddle-project.md :31 |
| **Mail message** | Any seat | filename: `<sender>.<scope>.<YYYY-MM-DD>.md`; carry `host:` where relevant | not prescribed | Receiver's `_mail/<receiver>/inbox/` | Sender writes; receiver archives | _mail/README.md :22–26 |

---

## B. Surface-law table

| Surface | What it governs | Numbering / ownership / archive rule | Key quoted law |
|---|---|---|---|
| **`_bus/`** | Past-tense multi-seat exchange in a session | `NN.<seat>.<kind>.md`; single writer per file; one file per direction per cycle; no archive (folder pruned at session close) | bus GUIDE :27–34: "NN is the zero-padded cycle sequence… <seat> is the writer." "Files remain in cycle order until the session closes and the folder is pruned." |
| **STATUS.md** | Present doing-state (one gate) | Single snapshot; full rewrite after every verified transition | status GUIDE :19–20: "STATUS.md is the sole doing-state for one session gate." :118–120: "Bounded replacement snapshot, not a chronological journal." |
| **`_mail/<recipient>/inbox/`** | Temple bus messages | Presence = unread; `mv` to archive = processed; receiver owns message; no sent-copy | _mail/README.md :14–18: "Presence in inbox/ = unread. When a memo is read and fully processed, the final action is mv _mail/<who>/inbox/<memo>.md _mail/<who>/archive/." "The receiver owns the message." |
| **`raw/` inside a session bed** | Consult records, handoffs, observations, close receipts | Named by calling convention: `raw/consult.<topic>.<date>.md`; file created by head; never an edit to existing file | consult.md :33: "the head lands my reply verbatim in its bed — <bed>/raw/consult.<topic>.<YYYY-MM-DD>.md, a new file, never an edit." runbook GUIDE :212: "raw/observations.* … move verbatim to <project>/.dev/observations/…" |
| **HANDSHAKE mail-by-path** | Claude ↔ Codex cross-runtime exchange | Presence proves availability not receipt; consumption stamped by archive move or `consumed-by:` prepend, or by the reply itself | HANDSHAKE :34–38: "Disk persistence proves availability, not receipt… Consumption is stamped, not inferred… the consumer moves the brief to an archive/consumed location, or prepends a dated consumed-by: line to it… The reply itself… is the strongest stamp." |
| **Journal** | Machine-layer state; session carry receipts | No prescribed numbering; own-scope chapters; CARRIED TO/FROM pairs | carry-unfinished.md :25–26: "source own-scope receipt: CARRIED TO…; destination own-scope receipt: CARRIED FROM…" journal 2026-10-21 :213–214: "distinguish available, delivered and consumed." |

---

## C. H1–H7 evidence tables

### H1 — consult return shape stated in ≥3 places

CONFIRMED in 4 places. Divergences below.

| Source | Lines | Quoted text |
|---|---|---|
| identity.md §Return contract | :119–124 | "One finding per invocation, plain markdown, to the invoker; `none` is a value, silence is incomplete. Every finding names: card · verdict (`fits · stretches · breaks · unclear` for consult; tag class for audit) · the evidence paths read · what remains unverified." |
| binding.claude.md §Return contract shape | :55–58 | "Plain markdown to the invoker. Line 1: the Route line (canary). Then one line per germline file read — absolute path · `stamp:` token (entry proof). Then the finding as the identity's §Return contract and the selected card define it." |
| binding.codex.md §Return contract shape and entry proof | :76–79 | "Plain markdown to the invoker. Line 1: the wrapper's Route line verbatim, canary included. Then one line per germline file read — `<absolute path> · stamp: <token>` … plus the effective cwd. … Then the finding as the identity's §Return contract and the selected card define it." |
| consult.md §Returns | :33–35 | "Returns: plain markdown, normally a page or less — the verdict · at most five constraints · findings with `said:` and `inferred: houston` kept apart · commit-pinned cites where needed." |
| bus GUIDE §RETURN | :80–102 | Six-field structure. (Note: governs BUS exchange cycles, not Houston consult inline returns. These shapes are NOT the same object.) |

**Divergences:**
- Route line + canary: stated only in binding.claude :57 and binding.codex :78. Absent from identity §Return contract and consult.md.
- Stamp lines: stated only in bindings. Absent from identity and consult.md.
- "at most five constraints": consult.md :35 only. Absent from identity §Return contract.
- "The hole" (frame defect + required properties): identity :126–128 only.
- "said: and inferred: houston kept apart": consult.md :34 only (not in identity's §Return contract directly — the Evidence discipline section names the tags but §Return contract does not).
- Bus GUIDE RETURN (six fields) is a distinct shape for bus exchange, not the same as a Houston consult inline finding.

### H2 — landing path defers to project addendum

CONFIRMED for audit/sitting/main-session; PARTIAL for consult; UNDEFINED for neutral Houston.

| Source | Lines | Quoted text |
|---|---|---|
| binding.claude.md (main session) | :40 | "the landing path the project addendum names; a sitting writes only in its own bed" |
| binding.codex.md (main session) | :45 | "the landing path the project addendum names; return to the operator and stop" |
| audit.md (findings) | :26–27 | "Findings and diff land only at the paths the invocation assigns, inside the landing pattern the project addendum names." |
| consult.md (head writes raw/) | :30–33 | "When the head needs a record, the head lands my reply verbatim in its bed — `<bed>/raw/consult.<topic>.<YYYY-MM-DD>.md`, a new file, never an edit." |
| identity.md (no addendum) | :143 | "No addendum found → I run as neutral Houston and say so." |

Consult does NOT defer landing to the addendum — the path format is prescribed in consult.md and the HEAD is the writer, not Houston. For neutral Houston (no addendum) on a main session, no landing path is defined in any read source.

### H3 — bus RETURN vs consult return: two shapes for the same event?

COMPATIBLE but DISTINCT; no file states the boundary explicitly.

| Source | Lines | Quoted text |
|---|---|---|
| binding.claude.md (child return) | :40 | "the spawner's context" |
| binding.claude.md (main session return) | :40 | "the landing path the project addendum names" |
| bus GUIDE §RETURN | :83–102 | Six-field structure; file `NN.<seat>.return.md` |
| consult.md §Writes | :29–33 | "Writes: none… My finding returns in my reply. Where it lands is the head's pen." |

A consult invocation via Agent tool (child route) returns inline to the spawner's context — it is not a bus file. The head may then write a bus RETURN for the parent cycle that may include Houston's finding as evidence. No file explicitly states "when a consult is a bus RETURN vs a raw file." The bus GUIDE states "one file per direction per cycle" — if Houston is the responding seat in a bus cycle (POINT to Houston → RETURN from Houston), then Houston would write a bus RETURN. The consult card says Houston writes nothing — this creates a ⚡ CONFLICT: a bus POINT directed to Houston for consult requires a RETURN file per bus GUIDE, but the consult card forbids Houston from writing any file. No source resolves this explicitly.

⚡ CONFLICT: bus GUIDE :52–54 requires the responding seat to write one RETURN file; consult.md :13–15 states Houston never writes any file under consult. The germline-05 example shows the RETURN file authored by cartan (the responding seat in a grammar review), not Houston.

### H4 — delivery and consumption: is the journal receipt pair the only two-sided receipt?

| Source | Lines | Quoted text | Side count |
|---|---|---|---|
| _mail/README.md | :14–18 | "Presence in inbox/ = unread… mv to archive/… The receiver owns the message. No sent-copy." | One-sided (receiver archives) |
| bus GUIDE | :47–48 | "There is no inbox, archive, unread marker, cursor, or read-state. Filename presence does not prove that a claim was read or verified; only the VERDICT closes that edge." | One-sided (VERDICT closes) |
| HANDSHAKE delivery rule | :34–38 | "Consumption is stamped, not inferred… the consumer moves the brief to an archive/consumed location, or prepends a dated `consumed-by:` line to it… The reply itself (a RETURN's handoff, a CHALLENGE's verdict) is the strongest stamp." | One-sided stamp (optional archive or prepend) |
| journal 2026-10-21.md | :213–214 | "Writing this note does not notify Flight. We must distinguish available, delivered and consumed rather than counting the presence of a file as an exchange completed." | Observational — three states named, not a mechanism |
| carry-unfinished.md | :25–26 | "source own-scope receipt: `CARRIED TO <destination file#heading> · <reference>`; destination own-scope receipt: `CARRIED FROM <source file#heading> · <reference>`" | **Two-sided** (both source and destination written) |

The carry-unfinished CARRIED TO/FROM pair is the only explicitly two-sided receipt in the read corpus. The bus RETURN+VERDICT sequence involves two writers but the VERDICT is the verifier's closing act, not the original sender's acknowledgment — it is a cycle closure, not a bilateral receipt. Mail and HANDSHAKE are one-sided (receiver acts).

No surface law defines "delivered" as distinct from "available" in a formal mechanism. The journal entry names the three states (available / delivered / consumed) as a friction observation, not as a defined protocol step.

### H5 — fixed first lines and fixed keys

| Return | Form | Prescribed (P) or Observed (O) | Source |
|---|---|---|---|
| Houston entry proof: Route line | `Route: <route> (canary: <prefix>-<8hex>)` as first line | P | binding.claude :57; binding.codex :78 |
| Houston stamp lines | `<absolute path> · stamp: <token>` | P | binding.claude :57–58; binding.codex :79 |
| `card: X · verdict: Y` | form required, not prescribed as first-line position | P (fields); O (position) | identity :123; C-def.2 TEST-INSTALL :835 shows it as first body line |
| `out of card: <what> → <owner>` | exact form | P | identity :61–62; binding.codex :36–37 |
| Bus POINT header | YAML block with 8 fields | P | bus GUIDE :64–74 |
| Bus RETURN sections | `## 1. Files changed` … `## 6. Remaining uncertainty` | P | bus GUIDE :84–102 |
| Bus VERDICT header | YAML block with 8 fields | P | bus GUIDE :140–150 |
| `READY` / `HELD` | exact keyword + required content | P | saddle-project.md :29–31 |
| `CARRIED TO <file#heading> · <ref>` | exact form | P | carry-unfinished.md :25 |
| `CARRIED FROM <file#heading> · <ref>` | exact form | P | carry-unfinished.md :26 |
| Mail filename | `<sender>.<scope>.<YYYY-MM-DD>.md` | P | _mail/README.md :22 |
| Audit tags | `mech` · `judge` · `cross` | P | audit.md :22 |
| Consult raw/ path | `raw/consult.<topic>.<YYYY-MM-DD>.md` | P | consult.md :33 |
| Bus VERDICT disposition | `ACCEPT \| REVISE \| STOP \| BLOCKED` | P | bus GUIDE :147 |
| Bus VERDICT claim table | `CONFIRMED / REFUTED / UNVERIFIED` | P | bus GUIDE :165 |
| `consumed-by:` line | `consumed-by:` prepended, dated | P | HANDSHAKE :37 |

### H6 — evidence tags and other tag vocabulary

| Tag / vocabulary | Prescribed? | Home file | Lines |
|---|---|---|---|
| `said: <source words>` | P (Houston, always) | identity.md :66–67; consult.md :34 | "said: <source words> ≠ inferred: <seat> <reading> ≠ locked: L<n>. I tag every finding." |
| `inferred: <seat> <reading>` | P (Houston, always) | identity.md :66–67; consult.md :34 | same; C-def.2 observed: TEST-INSTALL :838–839 |
| `locked: L<n>` | P (Houston, after GO, in flag) | identity.md :66–67 | "locked: L<n> (after GO, in flag)" |
| `mech · judge · cross` | P (audit findings) | audit.md :22 | "findings tagged `mech` (scriptable) · `judge` (needs architectural reasoning) · `cross` (spans organs)" |
| `fits · stretches · breaks · unclear` | P (consult verdict) | identity.md :123; consult.md :38 | "`fits · stretches · breaks · unclear` for consult" |
| `CONFIRMED / REFUTED / UNVERIFIED` | P (bus VERDICT claim table) | bus GUIDE :165 | "CONFIRMED / REFUTED / UNVERIFIED" |
| `ACCEPT \| REVISE \| STOP \| BLOCKED` | P (bus VERDICT disposition) | bus GUIDE :147 | "`disposition: <ACCEPT \| REVISE \| STOP \| BLOCKED>`" |
| `ACCEPT \| HOLD \| CHALLENGE` | not found in any read source | — | — |
| `verified:` (witness tag) | used as file-level frontmatter field, not evidence tag | identity.md frontmatter :8; status GUIDE frontmatter :6 | metadata stamp, not a finding tag |
| `unqualified for the complete card: <capability>` | P (route-limited audit/consult) | binding.claude :61; binding.codex :32 | "A route-limited finding opens with `unqualified for the complete card: <missing capability>`" |

`said:` / `inferred:` / `locked:` are required only for Houston. Not required in bus GUIDE, programs, or sitting. Consult.md :34 requires `said:` and `inferred:` to be "kept apart" — this re-prescribes for the card what identity prescribes generally.

### H7 — `out of card:` form

| Source | Lines | Form as stated |
|---|---|---|
| identity.md | :61–62 | "`out of card: <what was asked> → <owning card or seat>`" |
| binding.codex.md | :36–37 | "`out of card: <request> → <owning card or seat>`" |
| consult.md | :15–17 | "answers `out of card:`" (no arrow or template repeated) |
| consult.md | :17 | "request for build, write, delete, `audit` or `sitting` under consult answers `out of card:`." (no template) |
| C-def.2 observed | TEST-INSTALL :851 | `out of card: writing .dev/session/houston-note.md → session head.` |

Identity and binding.codex agree exactly: `out of card: <X> → <Y>`. Consult.md uses the keyword but does not reproduce the arrow template. The observed example (C-def.2) uses the arrow form and fills `<Y>` with "session head" — a seat, consistent with "owning card or seat." No divergence in the prescribed form; consult.md is merely less explicit.

---

## D. Divergences / contradictions

| ID | File A | File B | Nature |
|---|---|---|---|
| D1 | bus GUIDE :52–54 (responding seat writes one RETURN) | consult.md :13–15 (Houston never writes any file under consult) | ⚡ CONFLICT: if Houston is the responding seat in a bus cycle under consult, bus GUIDE requires a RETURN file but consult card forbids any file write. No resolution in any read source. |
| D2 | identity :119 ("to the invoker") | binding.claude :40 (main session: "the landing path the project addendum names") | Not a contradiction per se — child returns to spawner, main session returns to addendum-named path — but the identity does not distinguish routes; bindings add the route split. |
| D3 | consult.md :33 (path format `raw/consult.<topic>.<date>.md` prescribed) | binding.claude :40 / binding.codex :45 ("landing path the project addendum names") | For consult: path format is in consult.md; for audit/sitting: landing path defers to addendum. Two different deferral rules for different cards — not contradictory, but asymmetric. |
| D4 | identity §Return contract :119–128 (no mention of Route line or stamps) | binding.claude :55–58 and binding.codex :76–79 (Route line + stamps are required first content) | Identity does not describe the Route+stamp preamble. The bindings add it. A reader of identity alone has an incomplete picture of the actual first-line shape. |
| D5 | HANDSHAKE :34 ("Disk persistence proves availability, not receipt") | bus GUIDE :47–48 ("Filename presence does not prove that a claim was read or verified; only the VERDICT closes that edge.") | Compatible (both deny that presence = receipt), but they name different closing mechanisms: HANDSHAKE uses consumed-by stamp or reply; bus GUIDE uses the VERDICT. These are different surfaces with different closure mechanisms — not a conflict, but no cross-reference links them. |

---

## E. Friction ranked

### (i) Agent producing a return

1. **No prescribed position for `card: X · verdict: Y` within the body** (H5, H1): identity requires the fields but no file prescribes them as first body line. The C-def.2 example happens to place them first — observed, not prescribed. An agent must infer position from examples.
2. **Bus cycle where Houston is the responding seat** (D1): the consult card bars writing; bus GUIDE requires a RETURN file. No file resolves this. An agent is blocked or must improvise.
3. **Neutral Houston: no landing path defined** (H2): identity says "I run as neutral Houston and say so" but no file specifies where the finding goes on main session with no addendum. Source: identity :143.

### (ii) Head / operator consuming a return

1. **"Delivered" is never defined** (H4): no surface law creates a mandatory receipt that the head consumed a consult finding. The HANDSHAKE delivery rule exists for HANDSHAKE briefs; bus VERDICT closes bus cycles; mail uses archive-move. A consult finding returned inline to a child spawner has no mandatory consumption proof — silence is never progress (HANDSHAKE :32) but there is no mechanism to enforce it.
2. **Audit landing path requires reading the addendum** (H2): the head cannot know where to find audit findings without the project addendum. If the addendum is missing or unreadable, the path is undefined. Source: audit.md :26–27.
3. **carry-unfinished pair: one append can succeed while the other fails** (carry-unfinished.md :30): "If only one append succeeds, report the incomplete pair and exact missing half; do not claim completion." No mechanism detects an incomplete pair on re-read.

### (iii) Parser

1. **Consult finding has no mandatory first-line machine-readable token** (H5): Route line + canary is prescribed, but the structured `card: X · verdict: Y` position is not — a parser cannot reliably extract the verdict without heuristics. (Compare: bus VERDICT has YAML header; mail has filename shape; saddle-project has READY/HELD keyword.)
2. **`CARRIED TO/FROM` path format**: `<file#heading>` contains `#` which could clash with markdown headings if embedded — no file addresses parser edge cases.
3. **Audit tags `mech · judge · cross` and consult verdicts `fits · stretches · breaks · unclear` are in separate files with no cross-reference** (H6): a parser checking for valid tag vocabulary must read both identity.md and audit.md; neither file points to the other's tag set.

---

## F. Uncertainty / not-read

1. **runbook/GUIDE.md — only grep + ±15 lines read.** Sections on CLOSE, handoff ceremony, and raw/ were reached via grep; the full GUIDE may contain additional landing rules not captured here. Line :212 (observations promote before prune) was seen; other closure rules may exist.
2. **`verified:` as witness tag**: the BRIEF mentions "verified:" in a witness context; none of the read files define this as an evidence-tagging convention distinct from the file-level `verified:` frontmatter field. Possibly a separate tag vocabulary — not confirmed.
3. **journal 2026-10-21.md §1.6**: the BRIEF references "myShell on 'available ≠ delivered ≠ consumed' at :194–214." That block discusses friction and the three states (lines :213–214 read) but is labeled under friction discussion, not a numbered §1.6 section. The section number reference in the BRIEF may point to a section I did not reach.
4. **Program return landing paths**: fold-entry, list-pending, audit-beds, carry-unfinished all return "inline / caller's context." No file in the read corpus specifies where the caller is expected to land these returns, or whether any bus or STATUS surface is required to receive them.
5. **Sitting card**: status is STUB (sitting.md :10). Full return shape is not yet written. Landing path, prescribed form, and delivery proof are all deferred.
