---
canon: shared-body (vendor-neutral identity, vendor-shaped plumbing)
scope: seller-upgrade   # ← word from voice input; rename if "seller" misfired
date: 2026-09-21
thread: agentive-collaboration
authors: symmetry (claude.ai) · asymmetry (codex, verification 2026-09-21) · majkee (germline editor)
status: CANDIDATE CANON · design confirmed both sides · build parked inside the audit
sovereignty: HIGH — body lives in files; only plumbing is vendor-owned
companion: manual_builder-knobs_seller-upgrade_2026-09-21.md (operational; expected to churn)
---

# CANON — one body, many harnesses

## Axioms (strike cheaply before reading on)
1. An agent identity is text interpreted by a model. No vendor makes it immutable at runtime. (verified: both)
2. Every agent — parent or child — runs in ONE context window. There is no separate identity window beside the process window. (verified: both)
3. A child gets its own window, separate from the parent's. (verified: both)
4. What protects identity is the file on disk, not the running state. Durable across runs; not shielded within a run.
5. Therefore keeping the body inside a vendor's native format buys no protection the shared file wouldn't have.
6. What differs between vendors is plumbing, not identity: when the body loads, what history crosses, whose permissions win, how long the child lives, where you may enter.
7. The invariant is the body. The knobs are weather.
8. A generic shell that swaps bodies at spawn makes identity the most volatile thing in the window; one named wrapper per agent keeps it the most fixed.
9. Cost of a design = build + translation + ongoing verification. Verification is paid on every vendor regardless — it is not a portability penalty.
10. This is built inside the audit, not ahead of need. If the audit doesn't happen, this doesn't either.

## The shape
- **Body** — one markdown per agent: name, story, doctrine, return contract. Vendor-blind. Shared by Claude Code, Codex, and whatever ships next.
- **Wrapper** — one per agent per vendor, thin: model, tools, permissions, pointer to the body. `.claude/agents/*.md` on one side, `.codex/agents/*.toml` on the other. The wrapper COMPOSES the body into the instruction layer at startup; it never says "read this later."
- **Dispatch skill** — selects the agent by name, hands it a bounded task, stops if the agent doesn't exist. Same skill text both sides; the spawn verb underneath differs.
- **Families, not one line** — roster grouped by purpose, wrappers kept per agent. Reduction comes from the shared body and shared conventions, not from collapsing wrappers.

## The seller exchange (what mirrors what)
The scope exists because the two CLIs are asymmetric in mechanism and symmetric in guarantee. When something is done on one side, the manual names its mirror on the other. Where a mirror is missing, the wrapper DECLARES the gap — it never pretends parity.

Known asymmetries as of this date:
- **Entry point** — Claude lets the operator enter at the child directly; Codex requires a parent. (majkee, observed)
- **Wrapper richness** — Claude wrapper carries a markdown body natively; Codex wrapper is TOML `developer_instructions` and currently embeds Astrobley's body inline — not yet factored out. (asymmetry, verified)
- **Lifetime verb** — Claude: `SendMessage` resumes a child; Codex: follow-up steering on the agent thread. (symmetry, doc search; asymmetry, doc)

## Brakes
- No build before the audit. This is one chapter of the reduction/smoothing pass, not its own project.
- Permissions are the proof obligation: read-only child profiles on Codex can be overridden by live parent permissions. Test on the actual install before trusting a TOML. (asymmetry)
- Asymmetry verified published docs, not the home/office CLIs. Loading behavior on the real machines is UNVERIFIED.

## Telemetry (closer)
- Re-grounding an agent repeatedly = the task exceeds one context. Decompose, don't re-prime.
- A wrapper whose declared knobs don't match the mirror side = a gap to record, not a bug to hide.
