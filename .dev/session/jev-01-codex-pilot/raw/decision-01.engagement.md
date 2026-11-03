---
title: Decision 1 — what one Jev engagement covers
questions_by: cartan
answers_by: majkee
status: accepted via operator chat; see decision-01.receipt.2026-10-27.md
---

to-majkee(jev-01) from-cartan ---

1. **Context.** Jev needs to know which piece of work owns its settings and total spending
   allowance. Otherwise a restart or another session could accidentally look like fresh funding.
2. **Recommendation A.** For this pilot, one engagement means one runbook work folder
   (`bed`), with one durable Jev session and one cumulative USD allowance. Restarting reopens
   that session; attempting to open a second funded session for the same folder refuses.
   Codex and your shell read the same records and record their own use/skip/reconsider.
3. **Consequence.** This keeps the pilot small. It does not yet support several independently
   configured Jev sessions sharing one work folder's budget. If you need that now, choose B
   and describe the intended scope; I will revise the budget ownership design before building.
4. **Your decision:** choose A or describe B below. This chooses the scope only. It does not
   choose the dollar amount, channel meaning, credential path or approve implementation/sending.

- [ ] A — One work folder = one engagement = one durable Jev session = one cumulative allowance.
- [ ] B — I need a different engagement scope: ______________________________

My note:

Operator chat, 2026-10-27, recorded verbatim by Cartan: **“ok, taking it.”**
The accepted scope and limited effect are recorded in `decision-01.receipt.2026-10-27.md`.
The original checkbox presentation above is retained; the chat receipt records the answer.

---

Your answers stay yours. Cartan will not tick a box by inference. This is a new successor
question corresponding to the old sheet's funding-scope question 4; the old sheet remains
unchanged. The complete proposal is `design-packet.2026-10-27.md` beside this file.
