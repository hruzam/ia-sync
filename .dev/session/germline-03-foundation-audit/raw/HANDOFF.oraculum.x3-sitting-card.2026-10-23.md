to-germline-03-foundation-audit (its head / myShell(germline)) from-nablarva-X3-architecture-sitting (oraculum(cSharp), Claude MAIN head)

2026-10-23 · office · forge input, not acceptance and not a deploy instruction. Routed here on Majkee's word: "step 5: yes, but we are now on germline-03 --> raw/".
Claim types: said: <source> · inferred: <seat> · locked: L<n>. Nothing here edits ~/.germline/; acceptance and any deploy belong to this forge bed.

## What arrives

1. **Full sitting-card draft** for Houston, written by the X3 sitting child from what the sitting actually did (gavel G8 a: "Houston drafts it in raw/ from what this sitting actually did, and it goes to the germline-01 forge bed after GO"; the forge moved to germline-03, said: majkee 2026-10-23).
   - Source: `nablarva@519a211:.dev/session/nablarva-X3-architecture-sitting/raw/card.sitting.draft.r2.md`, sha256 `2a6baf3fe4bb5c8b94a0dd9ed4cef001ea435154a525a4cf3e7e71a920ab1098`. It was released by its author for the card role, and Cartan cycles 01–02 checked its boundary text: pen, no-spawn, verbatim relay. It does NOT replace the live stub until this bed accepts it.
   - Live stub today: `~/.germline/agents/houston/cards/sitting.md`, stamp `630f58c3`, sha256 `34fe2073…78b3` (equal to `~/ia-sync/germline/agents/houston/cards/sitting.md` at X3 R0, 2026-10-22).
2. **A new lock that touches the Houston addendum.** nablarva flag **L18 · Organ-body homes** was adopted 2026-10-23 (flag commit `5e93688`). The addendum `nablarva/.germline/agents/houston/nablarva.md` §1 still calls this rule "proposed, not locked". The row is now stale (inferred: oraculum). Editing the addendum is forge work here, not X3's.

## Lessons from the first real child sitting (evidence in the X3 bed; inferred: oraculum unless tagged)

- **Entry proof lives in the handback, not in assistant text.** On a Claude child, the first answer is a `SubagentHandback` tool call. The first assistant text was a one-line pre-tool narration. Route evidence must cut the fixed prefix at the first SubagentHandback. Evidence: raw/evidence.houston-route.r2.eagle.2026-10-22.md (head's first cut used the wrong definition), reproduced by assay (raw/witness.r8.assay.2026-10-22.md check 7).
- **Read order deviated from the loader.** The wrapper says to read identity → binding → project addendum → card "in this order". The child read identity (16) → binding (17) → **card (21) → addendum (32)**, all before the first answer, and still printed its stamp lines in canonical order. Assay classified it as "a minor procedural deviation … not a pass on order", non-blocking. Candidate card or binding rule: print stamp lines in actual read order, or enforce the order.
- **No-spawn held, but only by prose.** The wrapper's tools include `Agent`; across 7 handbacks the child made 0 spawns and 22 writes, all new files in its bed's raw/ (raw/evidence.houston-route.final.eagle.2026-10-23.md). The card is still the only fence (binding §"Spawn is bounded by instruction").
- **New-files-only pen works, and costs revisions.** Every correction became a new file (r2…r7; two withdrawn by the child itself). Two failure modes appeared, both self-caught by the child:
  - undeclared reflow in a "narrow" revision (r3, r4);
  - a revision written from memory instead of from the file on disk (r6).
  Candidate card rules: "revise from the bytes on disk, never from memory"; "declare every changed line, formatting included".
- **Lock-citation scope was the dominant defect class.** Eleven instances across review and witness: a `locked: L<n>` tag reaching past the lock's text. The child added a "Citing a lock" section to card r2.
- **Context budget.** The child reached ≈539k subagent tokens over the sitting (arc → 7 draft revisions). Its slips clustered late. Candidate: a sitting card names a budget or handback-size signal at which the head asks the operator about a fresh child.
- **Publication needs explicit release.** The child released each candidate path for its role. The head copied byte-identical (r7 → docs/ARCHITECTURE.md, sha256 equal on both sides, commit f20dda5). Card r2 carries this rule.

## Pointers

- X3 STATUS (R10 record): `nablarva/.dev/session/nablarva-X3-architecture-sitting/STATUS.md`
- Reviews: `…/_bus/01.*`–`03.*` · witnesses: `…/raw/witness.r8*.assay.*` · Majkee's rulings: `…/raw/answers.majkee.*`
- nablarva commits: 519a211 (bed record) · f20dda5 (promotion) · 5e93688 (flag L18–L21). Pushed by Majkee or pending his push.

## Addendum 2026-10-24 — two more addendum facts from X1 check 5 (Houston post-promotion audit, classified "useful" by majkee; "drag yes")

Source: nablarva .dev/session/nablarva-X1-architecture/raw/houston-audit.2026-10-23.post-promotion.md, finding C3. It reports that this handoff carried (a) only.
- **C3(b)** the addendum's architecture row says "today a pre-architecture pointer; becomes the body", but `docs/ARCHITECTURE.md` IS the body since nablarva@f20dda5.
- **C3(c)** the addendum frontmatter `authority: … flag.md @ 32b645f` predates flag L18–L23. Houston classes this as age, a candidate rather than an error.
- New locks since this handoff was written: nablarva flag **L22** (the L12 seal covers every operator vault) and **L23** (L12's retired trio = the nablarva.devenv one), commit 2fbf867. They are relevant if the addendum or bindings cite L12.
