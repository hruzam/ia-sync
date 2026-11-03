# BRIEF U7 → field (Flight, 2026-10-21) — return shapes: what germline agents/programs return, where it lands, how delivery is proven
Audit-only. Read in full; no edits outside your return file; no verdicts, no dispatch.

## Read in full (absolute paths)
1. /home/hruzam/reposoma/raw.guides/bus/GUIDE.md (whole) — POINT / RETURN / VERDICT shapes, numbering, archive
2. /home/hruzam/reposoma/raw.guides/status/GUIDE.md (whole) — STATUS fields, holds, checkpoint, recovery
3. /home/hruzam/reposoma/raw.guides/runbook/GUIDE.md — only the sections on session surfaces, handoff/CLOSE and "where returns land" (grep: RETURN, raw/, _bus, CLOSE, handoff; read ±15 lines)
4. /home/hruzam/reposoma/_mail/README.md (whole) — addressing law, message format, archive ownership
5. /home/hruzam/ia-sync/HANDSHAKE.md (whole) — POINT / RETURN / CHALLENGE meeting shapes, mail by path
6. Germline return contracts: /home/hruzam/ia-sync/germline/agents/houston/identity.md §Return contract (grep "Return contract", read the section) and §Evidence discipline (`said:`/`inferred:`/`locked:`); binding.claude.md :55–73 and binding.codex.md :76–83 (return shape + entry proof); cards/consult.md :29–40 (Writes/Returns/Verdicts); cards/audit.md (whole, 2.3 kB); cards/sitting.md (whole, 1.3 kB)
7. Program return contracts (already audited in U3 — read only the Return/Output lines): /home/hruzam/reposoma/.majkee/.germline/programs/journal-continuity/fn/{fold-entry,list-pending,audit-beds,carry-unfinished}.md and project-saddle/fn/saddle-project.md (READY/HELD; CARRIED TO/FROM receipts)
8. One real example of each surface: /home/hruzam/ia-sync/.dev/session/germline-05-sella-germline-audit/_bus/POINT.01*.md and RETURN.01*.md (Glob; read the headers + first 30 lines of each) · /home/hruzam/reposoma/.majkee/journal/2026-10-21.md :194–214 (myShell on "available ≠ delivered ≠ consumed") · TEST-INSTALL R2.C-def.2 block (/home/hruzam/ia-sync/.dev/session/germline-01-builds-and-deploy/raw/TEST-INSTALL.houston.2026-10-10.md :826–854) as an entry-proof + consult return example

## One question
For every return a germline consumer produces (Houston entry proof; consult verdict; audit findings + diff; sitting drafts; `out of card:`; program READY/HELD; journal receipts CARRIED TO/FROM; a relay to the operator), what is its prescribed shape (first line, fixed keys/tags, length, landing path, who writes it), which surface law governs where it lands (bus GUIDE numbering/ownership, STATUS holds, mail addressing, journal), and how delivery/consumption is proven — as the files literally state it. Then: where the shapes are stated more than once (identity vs binding vs card vs GUIDE) and whether they agree.

## Hypotheses to TEST
H1 Return shape is stated in ≥3 places for consult (identity §Return contract, binding §Return contract shape, consult.md §Returns, bus GUIDE RETURN) — quote each; list divergences (verdict first? entry proof first? length? tags?).
H2 Every landing path defers to the project addendum (binding "the landing path the project addendum names") — confirm for consult/audit/sitting; what happens for neutral Houston (no addendum) — is a landing path defined anywhere?
H3 Bus GUIDE POINT/RETURN/VERDICT ownership (Flight owns POINT+VERDICT, respondent owns RETURN) vs Houston's consult (returns inline to the invoker; the head lands it verbatim as `raw/consult.<topic>.<date>.md`) — compatible, or two shapes for the same event? Does any file say when a consult is a BUS RETURN vs a raw file?
H4 Delivery/consumption: does any surface law define "delivered" or "consumed" (a receipt that the addressee read it)? Quote _mail/README archive-ownership rule, bus GUIDE, HANDSHAKE; compare to myShell §1.6's three states (available / delivered / consumed) and to the program receipts CARRIED TO/CARRIED FROM (a paired receipt). Is the journal receipt pair the only two-sided receipt in the corpus?
H5 Parser-friendliness (operator direction): which returns have a FIXED first line or fixed keys today (entry proof Route line + `path · stamp:` lines; `card: X · verdict: Y`; `out of card: <request> → <owner>`; `READY`/`HELD`; `CARRIED TO <file#heading>`; bus header fields; mail frontmatter)? Quote the exact prescribed forms; mark which are prescribed vs merely observed in examples.
H6 Evidence tags `said:` / `inferred:` / `locked:` — prescribed in identity; used in the C-def.2 example; required anywhere else (cards, programs, bus GUIDE)? Any other tag vocabulary in use (`mech · judge · cross`; `fits · stretches · breaks · unclear`; `verified:` in witness) — list all with their home file.
H7 `out of card:` form — identity :61–62 "`out of card: <what was asked> → <owning card or seat>`" vs binding.codex :36–37 vs consult.md :13–17 vs observed C-def.2 ("out of card: writing .dev/session/houston-note.md → session head.") — same form?

## Return shape (write yourself, verbatim; then ≤15-line inline summary)
Return file: /home/hruzam/ia-sync/.dev/session/germline-06-full-audit/_bus/field.U7.return.md — header `from: field · unit U7 · date`, then:
A. Return-shape table (return · producer · first line / fixed keys · length · landing path · who writes · governing law · prescribed-in).
B. Surface-law table (bus · status · mail · journal · raw/ · HANDSHAKE: what each governs, numbering/ownership/archive rule, quoted).
C. H1–H7 evidence tables (quote text with every line ref; line numbers from files as read today).
D. Divergences / contradictions (file:line pairs).
E. Friction for (i) an agent producing a return, (ii) a head/operator consuming it, (iii) a parser (ranked, cited).
F. Uncertainty / not-read.
Bounds: ≤ 4,000 words. Separate prescribed / observed / historical. Stop when A–F are filled.
