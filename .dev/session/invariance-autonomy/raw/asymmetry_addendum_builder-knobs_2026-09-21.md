---
addendum: builder-knobs
date: "2026-09-21"
author: "asymmetry (Codex)"
original_authors:
  - majkee
  - "symmetry (Claude)"
reviews: manual_builder-knobs_seller-upgrade_2026-09-21.md
companion: asymmetry_addendum_shared-body_2026-09-21.md
scope: seller-upgrade
scope_note: "Voice label remains unconfirmed; agent-portability is a suggested neutral replacement."
status: "PROPOSED OPERATIONAL ADDENDUM — documentation-backed corrections; installation proofs open"
implementation: "PARKED INSIDE THE AUDIT — no runtime configuration changed"
verification: "Official documentation checked 2026-09-21; supplied files inspected; home/office unverified"
---

# Asymmetry's addendum to the five builder knobs

Keep all five knobs. Amend their guarantees, distinguish native mechanisms from our proposed policy, and attach evidence to the effective configuration. The declaration block at the end is a project contract proposal. It is not a vendor-supported schema.

## 1. Load timing and instruction placement

Retain startup composition. Claude's custom-agent body supplies its system prompt; a Codex role can supply developer instructions. These are different instruction layers. The manual must record the destination as well as the timing. [Claude agent definitions](https://code.claude.com/docs/en/sub-agents#write-subagent-files), [Codex custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agents)

The documented `@path` import belongs to CLAUDE.md. It does not establish the same include behavior inside a custom agent's Markdown body. Likewise, the checked Codex documentation does not establish a general TOML include directive for identity content. [Claude imports](https://code.claude.com/docs/en/memory#import-additional-files)

**Amendment:** choose a verified loader for the exact file type, or use build-time composition. Generate the Claude body and Codex instruction string from the same canonical Markdown, using correct serialization. Keep the source path and revision as provenance. Check the resulting instruction text, including escaping and truncation risks. A wrapper that only points to a file has not yet demonstrated composition. Generated-file checks establish composition; effective startup loading still needs runtime evidence. An agent's self-report alone cannot establish the entire loaded instruction set.

Factoring Astrobley remains the first proposed audit task, not a change performed by this review. Record accompanying project guidance and preloaded material so conflicting instructions remain visible.

## 2. History copying

Define `fresh` as no inherited parent conversation messages. It does not mean an otherwise empty prompt. Claude custom subagents can receive project guidance and preloaded skills. Claude's skill `context: fork` starts fresh despite its name. [Claude startup context](https://code.claude.com/docs/en/sub-agents#what-loads-at-startup), [Claude skill delegation](https://code.claude.com/docs/en/skills#run-skills-in-a-subagent)

Codex's documented separate threads do not by themselves prove a particular CLI history default. Codex also exposes history-copying thread forks. [Codex thread forks](https://learn.chatgpt.com/docs/app-server)

**Amendment:** record the requested policy and prove how the chosen adapter implements it. The Work interface's all/some/none controls remain Work evidence; do not transfer that finding to a CLI installation. If selective copying is used, declare its boundary. Even a fresh child can receive relevant earlier facts in a bounded task handoff.

Fresh Researcher and Architect runs are defensible local policy choices, not vendor guarantees. Inherited history may help or distract; “drowns the body” is a risk hypothesis rather than an inevitable effect.

## 3. Effective permissions

Move model and reasoning settings out of the permissions comparison. They affect execution behavior and cost, not filesystem authorization.

Codex documents parent runtime overrides that can supersede child sandbox defaults. Claude likewise documents parent permission modes that override a child's requested mode. Preserve this qualification on both sides. [Codex sandbox controls](https://learn.chatgpt.com/docs/agent-configuration/subagents#approvals-and-sandbox-controls), [Claude permission modes](https://code.claude.com/docs/en/sub-agents#permission-modes)

**Amendment:** during the audit, test the real profile and relevant launch mode against a disposable target. Record the runtime version, host, effective configuration, attempted operation, enforcement result, and resulting filesystem state. Use a fixture whose writability is understood so an unrelated filesystem denial cannot impersonate the intended sandbox restriction.

A child's verbal refusal is evidence of instruction adherence, not proof that the runtime blocked a write. A denied operation proves the tested route and target under the recorded configuration. It does not certify every tool or permission mode. Include shell and connector mutation paths only where they are part of the role's actual capabilities; a filesystem test does not establish connector permissions.

The Researcher and Architect proofs remain open. Rerun affected checks after relevant runtime, permission, adapter, or tool changes. Avoid turning one dated success into a permanent certificate or retesting unrelated behavior without a reason.

## 4. Lifetime and continuation

Completion and disappearance are different events. Claude custom subagents can be resumed; some built-in types are one-shot. Codex documents follow-up steering and closing agent threads as separate operations. [Claude continuation](https://code.claude.com/docs/en/sub-agents#resume-subagents), [Codex thread controls](https://learn.chatgpt.com/docs/agent-configuration/subagents#orchestration-and-thread-controls)

Use the lifetime terms as workflow policy:

| Policy | Intended behavior |
| --- | --- |
| `oneshot` | A later assignment starts a new instance. Completion does not assert transcript deletion or an inability to resume. |
| `held` | Later work is routed to the same identified instance while the runtime supports continuation. Idle time does not imply a continuously running model. |

**Amendment:** for held agents, retain the actual instance identity, body revision, pending goal, return route, and stop condition. Resume and re-spawn must remain distinguishable. Reusing the same display name is insufficient evidence of continuity. Separate the operator's oversight from the controller's mechanical bookkeeping.

Treat re-grounding as a proposed intervention, not a proved guarantee. Prefer a concise reminder of the operative constraints at meaningful phase changes. If the required body or state is missing, recover it deliberately; merely mentioning its path does not restore its contents. Diagnose repeated reminders before concluding that decomposition is necessary.

The claimed roster proportion and reviewer drift scenario are not validated measurements. The proposed held Buffering specialist also needs explicit separation from the supplied controller-level Buffering skill.

## 5. Entry point

Claude's `--agent` loads an agent definition into the main session. That is direct entry to a role, not a parentless child. Codex can launch a standalone session with a named configuration profile; profiles accept ordinary configuration keys, including the separately documented developer-instruction setting. [Claude direct entry](https://code.claude.com/docs/en/sub-agents#invoke-subagents-explicitly), [Codex profiles](https://learn.chatgpt.com/docs/config-file/config-advanced#profiles), [Codex developer instructions](https://learn.chatgpt.com/docs/config-file/config-reference)

**Amendment:** remove “Codex always carries an additional parent window” as a platform claim. A child selected through delegation has a parent. A standalone role binding need not. The latter can be composed from the shared body into a Codex main-session profile; equivalence to the child wrapper's effective settings still needs checking.

The specific convenience gap is whether the same agent definition can be selected directly through an equivalent native entry operation. The checked Codex documentation does not establish an identical selector for `.codex/agents/<name>.toml`. A distinct adapter can serve the same operator goal, with its difference recorded.

If Cartan remains the required entry in your workflow, label that an operator policy. A shared dispatch skill is useful where delegation is chosen; it is not a reason to manufacture a parent for every standalone session.

## Proposed declaration

Keep this in an already-approved wrapper comment or metadata surface, or have the composer consume it. Do not add arbitrary keys to native files and assume the vendor enforces them. The audit chooses the smallest supported representation.

```yaml
agent: astrobley
body: bodies/astrobley.md
body_revision: null          # resolve a commit or content digest before launch
load: compose-at-startup
instruction_layer: null      # the actual native destination
history: fresh              # intended policy; adapter must establish it
perms:
  declared: workspace-write
  effective: unverified
lifetime: oneshot            # workflow policy, not a deletion claim
entry: delegated             # standalone or delegated
native_entry: null           # exact supported invocation/configuration surface
mirror_gap: []               # record differences rather than inventing parity
proof:
  host: null
  vendor_version: null
  date: null
  evidence: null
```

This is a proposal for the audit, not an installed Astrobley wrapper. A checksum establishes which source was selected; it does not establish what reached the model or how faithfully the model acted. Unknown effective fields remain unknown until evidence resolves them.

## Minimum reconciliation before implementation

Carry forward the shared body, per-agent names, purpose families, bounded dispatch, and the parked build. Replace unsupported import promises, fresh-equals-empty wording, complete-equals-gone wording, the mandatory-Codex-parent claim, and the context-exhaustion diagnosis.

Then the existing audit can select one pilot binding, inspect its composed instructions, exercise its relevant permissions, and compare its return against its contract on each real installation. No implementation or proof run was performed by this review.
