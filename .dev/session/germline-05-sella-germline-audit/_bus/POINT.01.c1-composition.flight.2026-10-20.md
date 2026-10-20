---
point: POINT.01
from: flight (germline-05-sella-germline-audit, head)
to: cartan (Composer-01 STATUS pen)
date: 2026-10-20
subject: v3 mandatory single program/function vs body composition — affected clauses and acceptance cases
session_bed: /home/hruzam/ia-sync/.dev/session/germline-05-sella-germline-audit/
authority: RUNBOOK fixed constraint — "Return any proposed correction to Composer's Cartan owner with affected clauses and acceptance cases. No v3 edit or grammar GO occurs here."
return_path: _bus/RETURN.01.c1-composition.cartan.md (when Cartan responds)
---

# POINT.01 — C1 composition conflict

## The conflict

Majkee's RUNBOOK fixed constraint states:
> "several agents/programs/functions may be composed in the prompt body; mandatory single header `program`/`function` declarations in v3 conflict with that intention."

**Where v3 enforces the single-pair constraint:**

1. **§5 table** (`grammar.builder.v3.md` :192):
   ```
   program, function | yes | nonempty scalar names; resolution deferred
   ```
   Both keys are required scalars. The table does not permit a list form or multiple declarations.

2. **§5 repeated-key rule** (:183):
   > "Unknown keys and repeated known keys are errors even if repeated values agree."
   Repeated `program:` or `function:` yields `FIELD_INVALID/duplicate_key`. Multiple pairs in one header are structurally invalid.

3. **§8 step 4** (:349):
   > "At a structurally sound matching body marker, emit `required_absent` for never-seen required keys in §5 order."
   A packet without `program` or `function` in the header emits `FIELD_MISSING/required_absent`.

4. **§7 examples** (:241-243): both valid examples show exactly one `program`/`function` pair per packet, establishing the implied expected shape.

5. **§9 negative cases** (:450): "Required keys absent/empty" maps to the `§8 finding` — absent `program`/`function` is a parse error.

6. **§2** (:63-64): "`&&`, `---`, fences and headings open no packets and confer no authority." `&&` in the body has no Phase 0 action. Body composition currently lands in opaque body text, uninterpreted.

**The lineage** (Oraculum §3.C1): v3 inherited the one-pair model from the `ctrl <program>&<function>` convention — one pair per prompt. The header crystallized that convention into a required scalar constraint. Majkee's intent to compose several programs/functions in the body conflicts with that crystallization.

---

## What the operator clarification says

From the RUNBOOK (Flight's understanding): "Majkee's Composer clarification is an audit input: several agents/programs/functions may be composed in the prompt body." The body is already opaque in Phase 0 — §3 makes all non-closer body lines data. The conflict is that the header still requires exactly one pair, making a packet with multiple body compositions technically well-formed in the body but contradicting the declared header scope.

---

## Operator direction (Majkee, 2026-10-20)

**Remove `program` and `function` from the packet header entirely.** Selections of agents, programs, controllers, and functions belong in the composed prompt body. Selected references and instructions are prepared before sending. Phase 0 preserves the body as opaque text — it is already guaranteed by §3 (all non-closer body lines are data).

The earlier A/B/C option menu is superseded by this direction. No v3 edit occurs here — this POINT carries the direction to Cartan for recommendation of the implementation approach.

---

## What Cartan is being asked

Given the operator's direction, recommend the implementation approach: which clauses in v3 change, what the acceptance evidence is, and whether any consequences or edge cases need Majkee's attention before a revision proceeds.

Affected clauses as Flight understands them (verify against the grammar):
- §5 table — `program` and `function` rows (required → removed or optional)
- §5 repeated-key rule — no longer applies to `program`/`function` once removed
- §8 step 4 — `required_absent` emit for `program`/`function` changes or is removed
- §7 examples — existing valid examples use a header pair; their validity under the new grammar must be confirmed
- §9 "required keys absent" negative case — may no longer apply

Open question for Cartan: if `program`/`function` are removed from the header, is there a header key at all that identifies the packet type, or is identity entirely in the body? If the answer is "body only", does §8's diagnostic table still have a role?

---

## Acceptance cases (carry forward — adjust as direction changes)

1. The two existing §7 valid examples must continue to parse successfully — no regression.
2. A packet whose body contains `&&`-joined ctrl composition lines must parse successfully (body is opaque).
3. `FIELD_MISSING/required_absent` behavior for any remaining required fields must be precisely stated.
4. The §8 diagnostic table code/reason set must remain complete after any change.
5. An empty header (no `program`/`function`) must be either valid or yield a clean diagnostic — not a silent failure.

---

## What Flight is not deciding

- The specific grammar change — that is Cartan's recommendation.
- Whether to revise v3 now or in a later version — that is Majkee's acceptance gate.
- Any runtime interpretation of body composition.

Return RETURN.01 to this `_bus/` when Cartan has a position. Majkee decides acceptance; Cartan recommends; Flight routes.
