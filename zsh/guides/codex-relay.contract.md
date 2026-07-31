# Codex relay — canonical plumbing contract

**Authoritative source for the shared plumbing of the Codex relay family:
@Astrobley (coder) · @Vega (blind crosscheck) · @Mirror (adversarial challenger).**
Point here, never copy (Janus verdict 2026-07-31: "the plumbing wants to be one;
the contract must stay two" — seats keep their opposite refusal contracts, this file
holds the shared delivery layer). Each agent carries a minimal self-contained snippet
(wrapper path + exit codes) so it functions if this file is unreachable; on any
divergence, THIS file wins and the agent snippet is stale.

## Wrapper

- **One path:** `~/.config/zsh/ai/codex-run.zsh` (mounted via ia-sync deploy).
  The old `.larva/agents-staging/` fallback is DEAD (dir deleted 2026-07-30) — no
  agent may reference it.
- Never call `codex exec` bare. One call per brief/task; no follow-up exchanges
  beyond the wrapper's built-in single retry.

## Exit codes (graceful-fail, shared by all three seats)

| exit | meaning | relay behavior |
|---|---|---|
| 3 | no `turn.completed` | return `[<SEAT> UNAVAILABLE: no turn.completed — raw diagnostic on stderr]` |
| 4 | empty stream after retry | return `[<SEAT> UNAVAILABLE: silent-exit regression — stream empty after retry]` |
| 5 | auth / 429 / unknown model | return `[<SEAT> UNAVAILABLE: upstream error — <verbatim error text>]` — LOUD, needs operator |

**Never block the caller.** On UNAVAILABLE the orchestrator continues. Cross-vendor
seats (Vega/Mirror) may be backed up by a same-vendor Claude seat, but any such verdict
MUST be labeled `SAME-VENDOR FALLBACK — decorrelation not achieved`. Silent fallback is
the one outcome worse than no answer.

## Return discipline

- Codex output comes back **VERBATIM** — no summary, no editorializing, no reconciling,
  no self-assessment. Re-interpretation by the relay re-correlates the answer toward
  Claude priors and destroys the decorrelation the seat exists to provide.
- Append wrapper-stderr usage numbers labeled `[usage: ...]` to every report.

## Economics (E1)

Each call costs 16–45K input tokens against the shared ChatGPT Plus quota (5h rolling
window). Batch; bounce micro-tasks (<~10 expected lines) back with a batching suggestion.

## The contract split (why three seats, one plumbing)

| seat | brief precondition | function |
|---|---|---|
| @Astrobley | refuses VAGUE scope | relay coder — well-scoped implementation |
| @Vega | refuses a POSITION (blind) | position-free second opinion / triangulation |
| @Mirror | REQUIRES a position | adversarial audit — attack the weakest assumption |

Intent lives in **which seat you spawn** — visible in the trace, never inferred by the relay.

---
*Established 2026-07-31 (transition session, majkee gaveled). Companion:
`codex-relay.metadata-scripting.2026-07-31.md` (Epoch practitioner guide, same folder).*
