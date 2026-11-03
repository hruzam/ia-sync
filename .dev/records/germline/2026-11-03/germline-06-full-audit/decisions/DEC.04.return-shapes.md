# DEC.04 — Return shapes: three decisions from U7
Prepared by Flight (G06) 2026-10-21 for Majkee + myShell review. Processed evidence, alternatives, consequences, recommendation. **Not a gavel. No ledger invented.** Evidence: units/RESULT.U7.md, _bus/oraculum.assess.U7.return.md, _bus/field.U7.return.md (attributed). Audit-only: nothing edited. RETURN side only — invocation grammar (C1) stays with Composer's Cartan.

## D14 — One header grammar for every germline return (README), including the program instance
Evidence: the house already writes `key: value · key: value` lines (stamp lines, `selected:`, `CARRIED TO … · <ref>`, mail filenames); Houston's proof block is prescribed, the kind line's position is not (observed first in C-def.2 only); programs have no proof or kind line (U3: the `:54` stamp check is unobservable); saddle uses bare `READY`/`HELD`; Epoch's constraint (RESULT.U3 §10): a separator must survive paste into shell, YAML and Markdown — ` · ` does, `&` does not; your direction: output maximally understandable, generic shape for a reader/parser or app.
Options: (a) name the grammar in `germline/README.md` (three lines: `header := [route-line] proof-line+ kind-line`; `proof := <abs path> · stamp: <8hex>[ · k: v]*`; `kind := <kind-key>: <value>[ · k: v]*`, one line, first after the proof block; body free) and apply the instances — Houston `card: X · verdict: Y` (position only), programs `<controller> · stamp` / `<fn> · stamp · expected:` + `fn: X · result: Y`, saddle `fn: saddle-project · result: READY`; (b) Houston only (identity edit), programs untouched; (c) nothing — keep per-file shapes.
Consequences: (a) one parser contract without a parser (split on ` · `, then first `: `); your programs gain the visible expected-value check and a first token; three of your files change (both CONTROLLERs, saddle fn) plus identity :123 (re-roll, re-witness); invocation lines untouched. (b) programs stay unobservable. (c) parsers need per-file heuristics.
Recommendation: (a). Alternative inside (a): leave `READY`/`HELD` bare and put the kind line before it (two first tokens — weaker). Destinations: `germline/README.md:10–11`; `identity.md:123`; `.majkee/.germline/programs/*/CONTROLLER.md:54` and the five fn Return lines (yours).

## D15 — "The hole" moves from identity to the consult card
Evidence: identity :127–128 defines the hole (frame defect · required properties); consult :39–40/:46 already names it ("the shelf has a hole") as the payload of `unclear`; no other card returns a hole today; U2 §6 — one owner per post-bootstrap rule.
Options: (a) consult owns, identity cites; (b) identity keeps it, consult cites (if audit `judge` findings should also return holes); (c) leave the duplicate.
Consequences: (a) identity shorter and vendor/card-blind; consult re-roll. (b) one line in consult; identity unchanged. (c) drift risk only.
Recommendation: (a), unless you intend holes from audit findings too — then (b). Small; batch with the other identity/card edits (one GO, one re-witness).

## D16 — Delivery sentence (germline-wide)
Evidence: "delivered" is defined nowhere; zero two-sided receipts exist (the carry pair is a link, one writer); every surface closes by the consumer's act (mail archive-move, bus VERDICT, HANDSHAKE `consumed-by:`/reply); G01 showed the cost — relays drop stamps, and one PASS row lacks itemized stamp lines; HANDSHAKE :35 "by the existing house mechanism, no new one"; AGENTS.md bias against registries; myShell §1.6 "no second dispatcher/registry".
Options: (a) one sentence in `germline/README.md` beside the witness rule (D13): "A return is delivered when the consumer's first act on disk quotes its proof block and kind line verbatim; a record that relays a return without them is a relay, not evidence, and does not close the exchange." HANDSHAKE adds one cite; (b) `consumed-by:` on every return; (c) a receipt ledger; (d) nothing.
Consequences: (a) no mechanism, one rule, fixes the G01 failure mode; myShell's available/delivered/consumed stay vocabulary. (b) inline tool returns have no file to prepend to. (c) a registry. (d) the next relay-without-stamps counts as proof again.
Recommendation: (a). Destination: `germline/README.md` (unstamped; rides the D1/D13 README rewrite).

## Non-decisions (mech, one GO + one re-witness batch)
Kind-line position (identity :123); bus/consult boundary sentence (consult :33); audit :26–27 clauses (`_bus/` landing takes the six headings; neutral/unassigned landing → inline + `out of card: landing unassigned → invoker`); identity cite lines for verdict values, `said/inferred`, proof-block extras; HANDSHAKE cite. Not decided: per-finding kind lines for audit (after telemetry); sitting's shape (first real sitting).

## Review path (for Majkee + myShell)
Review file: `/home/hruzam/ia-sync/.dev/session/germline-06-full-audit/decisions/DEC.04.return-shapes.md`
Invocation line: `/gavel-loop /home/hruzam/ia-sync/.dev/session/germline-06-full-audit/decisions/DEC.04.return-shapes.md`
Flight's view: D14 and D16 are ready; D15 is ready but trivial — qualify it with the batch.
