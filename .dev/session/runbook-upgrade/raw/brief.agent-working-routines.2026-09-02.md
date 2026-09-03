---
kind: research-brief
target: external strain (ChatGPT / Asymmetry) — BLIND
purpose: triangulation. Answer independently; do not ask what the other strain found.
authored: 2026-09-02 · Symmetry (claude.ai Opus) · thread agentive-collaboration
method: blind cross-brand fan-out — same questions, no shared findings, results triangulated by @majkee
scope: field practice of working developers with agentic coding harnesses. NOT vendor marketing.
---

# BRIEF — how practitioners actually run agentic coding sessions

## How to answer this

Report **field practice**, not documentation ideals. Where you are reporting a
vendor-documented fact, say so and date it. Where you are reporting community
practice, say roughly how widespread it appears and how confident you are.

**Say plainly when you don't know.** A gap named is worth more here than a
plausible synthesis — this brief is one of two independent answers and the
disagreements between them are the product.

Do not hedge into balance. Where practice has converged, say it converged.
Where it is genuinely contested, name both camps and who holds each.

`#no-invented-attribution` — do not name repos, authors, or scripts you cannot
actually place. "This pattern exists, I cannot source it" is an acceptable answer.

---

## PART 1 — surfaces

1. For **Claude Code**: CLI versus desktop application. What do experienced
   developers report preferring, and for which kind of work? Is it a preference
   or a division of labour?

2. Same question for **Codex**: CLI, IDE extension, desktop, cloud. Do people
   pick one, or move between them?

3. Does the choice of surface change the *shape of the work*, or only the
   ergonomics?

---

## PART 2 — the session routine

4. Is there a recognisable pattern in how developers schedule a working session
   with an agent? Specifically: do they hold **one agent across the whole job**,
   or **split the work across documents** and hand between sessions?

5. Is there a reported tier pattern — a stronger model for planning, a cheaper
   one for execution, then back to the stronger one to review? If so, is the
   handoff manual or handled by the harness? What do people report about whether
   it actually works?

6. What determines when a session **ends**? Context exhaustion, task completion,
   a scope boundary, or nothing in particular?

7. When a session ends and work continues: what carries over, and in what form?

---

## PART 3 — long threads and the two doctrines

8. There appear to be two opposing instincts about long work:
   **(a)** reset often into fresh sessions, carrying a written handoff;
   **(b)** stay in one thread and compress in place when it dilutes.
   Which is more common, in which community, and **why**?

9. Is that split **mechanical** — the harnesses genuinely differ — or
   **cultural** — the same problem solved differently by two communities?
   Argue it rather than asserting it.

10. What does a fresh session **lose** that an in-thread continuation keeps, and
    vice versa? Is anyone solving both at once?

11. For **Codex specifically**: how is a long thread actually managed? Name the
    concrete commands or affordances people use, what each does, and which ones
    experienced users reach for most. Is there anything resembling an explicit
    handoff operation, or is it all in-harness?

---

## PART 4 — the durable files

12. How long should an always-loaded instruction file be? Is there a real number
    in circulation, and is it backed by anything measurable — cost, rule
    adherence, benchmark — or is it folklore?

13. What is the failure mode of a **long** instruction file? Describe the
    mechanism, not just the symptom.

14. Is there an established pattern for splitting a large body of project
    instruction into **an always-loaded part plus parts loaded on demand**? What
    is it called, how is it structured, and what triggers the load?

15. Writing style inside such files: declarative lines versus prose, ordering,
    placement of critical rules. Is any of this measured, or is it taste?

16. Does anyone mark a section of a plan as **closed** or **done** in a way an
    agent respects? How? Or is section-closing simply not solved?

17. Does anyone keep the **immutable plan** and the **volatile working state**
    in *separate files* — the plan frozen after authoring, the state rewritten as
    work proceeds? If yes, what do they call them and does the separation hold up?
    If no, what do they do instead?

18. Multi-writer append logs — several agents plus a human appending to one
    shared file. Does anyone run this successfully, or does it reliably fail?
    If it fails, what is the stated cause?

---

## PART 5 — unattended running

19. People report agent sessions running for hours, or overnight, without
    supervision. **How, mechanically?** Take it apart: what is actually running,
    what stops it, what holds state between steps.

20. Is an overnight run one long session or many short ones? What is the
    evidence either way?

21. What **class of task** is safe to run unattended, and what makes it safe?
    Is verification the constraint, or something else?

22. There is a known pattern of a shell loop that repeatedly restarts an agent
    in non-interactive mode, re-stating the goal each iteration and pointing at
    a state file. Can you place it — a named script, repo, or author? What is
    its actual structure, and what is its stop condition? If you cannot source
    it, say so rather than reconstructing it.

23. **git worktrees** and parallel agents: what is the reported experience?
    Where does parallelism stop paying?

---

## PART 6 — over-preparation

24. What is the community's argument about **over-engineering the preparation**?
    Where is the line between a workflow that pays for itself and process
    theatre? Is there a stated threshold — task size, session count, anything
    concrete — or is it purely instinct?

25. Do people report **abandoning** structure they built? What did they abandon,
    and why? This is the most useful part of the answer if you can find it.

26. How do practitioners decide a piece of their own process is **not earning
    its keep**, and remove it? Does anyone have a retirement mechanism, or does
    process only ever accumulate?

---

## PART 7 — harness mechanics

27. Can a **skill** (a loaded instruction module) restrict or grant which tools
    an agent may use while it is active? Is a tool allowlist declared inside a
    skill actually enforced?

28. What mechanisms *do* reliably constrain an agent's tool access, and how do
    they compose? Give the order of precedence if there is one.

29. Can an agent definition **branch on which model it is running as** — behave
    one way on a small model, another on a large one — as a condition inside its
    own body? Does that work, and if not, what is the working alternative?

30. Is there an established pattern for an agent **escalating** to a stronger
    model or a more senior agent when a decision exceeds its competence?

---

## PART 8 — prior art as a discipline

31. Is there any established practice of asking, **before building**, whether
    the thing already exists as a shipped vendor feature? Do people report
    building things the harness already provided?

32. If such a check exists as a habit, what does it look like, and does it
    survive contact with a deadline?

---

## PART 9 — cross-vendor

33. Does anyone run a workflow that **crosses vendors** — one harness planning,
    another executing, results returning to the first? What is the joint made of?

34. Is there any convention for a **portable** instruction or handoff file that
    more than one vendor's agent reads without translation? How stable is it?

35. For a developer running **several projects at once**: what survives a
    project switch? Is there a layer above the individual project's files, and
    what is in it?

---

## PART 10 — the honest close

36. What do experienced practitioners say they got **wrong** in the first six
    months of working this way?

37. What is the single highest-leverage thing they report, that a careful
    newcomer would not guess?

38. Where is the field's practice **thinnest** — the question everyone is
    working around rather than answering?

---

## Format

Answer by part number. Prose over bullets where the reasoning matters.
Mark each answer with your confidence, and separate **documented fact** from
**community practice** from **your own inference**.

If a question rests on a false premise, say so and answer the better question.
