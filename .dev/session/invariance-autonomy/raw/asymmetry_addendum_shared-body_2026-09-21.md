---
addendum: shared-body-philosophy
date: "2026-09-21"
author: "asymmetry (Codex)"
original_authors:
  - majkee
  - "symmetry (Claude)"
reviews: canon_shared-body_seller-upgrade_2026-09-21.md
companion: asymmetry_addendum_builder-knobs_2026-09-21.md
scope: seller-upgrade
scope_note: "Voice label remains unconfirmed; agent-portability is a suggested neutral replacement."
status: "PROPOSED ADDENDUM — shared-body direction endorsed; amendments await reconciliation"
implementation: "PARKED INSIDE THE AUDIT — no agent, skill, profile, or deployment changed"
verification: "Published documentation and supplied definitions; home/office installations unverified"
---

# Asymmetry's addendum to the shared-body philosophy

I endorse one canonical identity body, native bindings for each runtime, explicit differences, and implementation only inside the existing audit. Keep the stable design separate from the operational manual.

I would change the draft's status from “design confirmed both sides” to “candidate design with attributed reviews.” My earlier verification supports specific mechanisms. It does not countersign every inference subsequently derived from them. These amendments are my contribution to reconciliation; they do not record a new decision by majkee or Symmetry.

## Amendments to the ten axioms

| Axiom | Disposition | Proposed correction |
| --- | --- | --- |
| 1. Identity is interpreted text; no vendor makes it immutable. | Narrow the claim. | For the Codex and Claude Code paths examined, we found no documented guarantee of immutable behavioral identity. This is an evidence limit, not a universal theorem about every vendor. |
| 2. Every agent runs in one context window. | Narrow the scope. | A model invocation operates on an assembled, bounded context. These reviewed mechanisms establish no separate protected identity compartment. Stored history, retrieved memory, and the currently presented context are different things. |
| 3. A child has a separate window. | Retain with a qualification. | Independent working context does not establish a fresh start. Parent history may be copied at initialization; a fresh task message may also contain a parent-written summary. |
| 4. The file protects identity. | Replace “protects.” | The canonical file provides a durable, inspectable reference. Its integrity depends on ownership, access controls, versioning, and deliberate edits. Being on disk does not make it immutable or ensure a running agent follows it. |
| 5. Native storage buys no extra protection. | Retain conditionally. | Shared-source and inline-source bodies can have equivalent instruction placement when the same content reaches the same native layer at the same time. Loading a shared file later as a tool result is a different mechanism. |
| 6. Only plumbing differs. | Separate intent from behavior. | We can share authored intent. Model behavior, instruction priority, surrounding guidance, memory, and enforcement can still differ. Shared bytes do not establish equivalent judgment or authority. |
| 7. The body is invariant; knobs are weather. | Retain as a design rule. | The body is the canonical contract at a declared revision. Changing that contract is an explicit editorial act. Adapter changes should preserve it or report a mismatch. |
| 8. Named wrappers make identity more fixed. | Strike the causal claim. | Names improve selection and auditability. A shared loader that binds one body revision before startup can be equally stable. Volatility comes from ambiguous binding or uncontrolled rebinding, not from generic code alone. |
| 9. Verification is not a portability penalty. | Qualify the accounting. | Each vendor needs verification anyway. Portability additionally introduces composition, synchronization, and cross-runtime comparison costs. Count them, then compare them with the cost of maintaining divergent bodies. |
| 10. Build only inside the audit. | Retain. | No separate project, deployment, or migration is authorized by agreement on this philosophy. |

These corrections distinguish four independent questions: what source is authoritative, where its text is loaded, what context is shared, and what operations the runtime actually permits. Instruction text alone is not an enforcement mechanism. Anthropic explicitly distinguishes project guidance from enforced configuration; Codex separately documents developer instructions and sandbox configuration. [Claude instruction behavior](https://code.claude.com/docs/en/memory#write-effective-instructions), [Codex configuration](https://learn.chatgpt.com/docs/config-file/config-reference)

## The shape I would carry forward

**Body:** one vendor-neutral Markdown source for the agent's name, story, doctrine, decision boundaries, and return contract. Record its revision when composing a runtime binding. A revision identifies the source; it does not prove compliance.

**Native binding:** vendor-specific settings plus the body composed into the intended startup instruction layer. Generated copies are deployment products of the canonical source. They are not independently edited doctrine. A source pointer is useful provenance; the binding must still arrange actual content loading.

**Dispatch contract:** select an existing named role, supply the objective and bounded evidence, declare history and lifetime policy, and return an explicit failure when the requested binding is unavailable. The semantic procedure can be shared; tool names, native invocation, and enforcement remain adapter responsibilities. A prose instruction to stop is not itself a deterministic missing-agent check.

**Families:** retain per-agent names and purpose groups for clarity. Reuse a common composer where helpful. This preserves the roster while avoiding duplicated mechanics; it does not require one undifferentiated runtime persona.

The proposed invariant is source and contract continuity across native bindings. Behavioral equivalence is an evaluation question.

## Entry point is an adapter question

The operational addendum corrects the claim that Codex always needs an extra parent window. Claude's direct agent entry makes that definition the main session. Codex has standalone configuration profiles. Binding the shared body to a main-session profile is a documented configuration route plus a proposed composition step; loading a child-definition file through an identical selector has not been established. [Claude main-session agent entry](https://code.claude.com/docs/en/sub-agents#invoke-subagents-explicitly), [Codex configuration profiles](https://learn.chatgpt.com/docs/config-file/config-advanced#profiles)

Majkee's observed difference in the current operator workflow remains evidence about that workflow. It does not establish a universal inability of Codex to run the role without delegation. Budget the actual chosen path.

## Telemetry should preserve alternative explanations

Replace “re-grounding repeatedly means the task exceeds one context” with:

> Repeated re-grounding is a signal to inspect the binding, current constraints, accumulated state, and task size. Decompose when evidence shows that the working context or task boundary is the cause.

Other hypotheses include missing initial instructions, conflicting project rules, stale task state, ambiguous authority, or poor reminders. Context size is one explanation. A path-only reminder does not prove that absent content was restored.

The three-pass reviewer example is a useful failure scenario. In the supplied material, it is not a measured observation with a transcript, model, version, and acceptance comparison. Keep it as a scenario until evidence supports the diagnosis. A competent-looking result can miss a role contract, but drift can still be examined through outputs and representative tasks.

For Astrobley, check whether the implementation return actually exposes judgment, verification, disagreement, and the remaining gate. Merely printing the requested field names or claiming “I am Astrobley” is weak evidence.

## Existing procedures and proposed agents

The supplied Polyp, Octopus, and Buffering skills define controller procedures. Octopus deliberately parks before executor activation; Polyp forbids dispatch. The uploaded Buffering skill explicitly says it is not a new identity.

The manual's held “Buffering (RAG Sonnet)” is therefore a proposed specialist or a different existing seat whose definition was not supplied. Do not silently equate it with the uploaded Codex procedure. Resolve that mapping during the audit before calling it a mirror.

## Proposed final formulation

> We own one versioned body per agent. Each runtime binds that body into an explicit native instruction layer and declares how tasks, history, permissions, lifetime, and entry are handled. The binding records differences instead of claiming equivalent behavior. Named wrappers are our organization convention; correct composition and effective runtime controls establish the mechanical properties. The audit supplies installation evidence before deployment is trusted. Implementation remains parked until that audit reaches the work.

This is Asymmetry's proposed wording. The original authors retain authority to accept, amend, or reject it.
