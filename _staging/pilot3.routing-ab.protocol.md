# Pilot 3 — Routing A/B Protocol
`Authored: 2026-08-05 · atlas-ui · For: @majkee to run · Routes to: Houston for D1′ gavel`

## What this closes

The one open fact from the Arch/Unix doctrine pilot:
> Do `<example>` blocks inside `description` measurably change auto-routing behavior?

D1′ is already structurally confirmed (examples ARE part of the routing carrier — they live in
`description`, which is the only field the parent sees at route time). This pilot closes the
EMPIRICAL question: does richer carrier signal help, hurt, or make no difference in practice?

## The two agents (both in _staging/claude/agents/ — promote before running)

| File | Description style | Body |
|------|------------------|------|
| `routing-ab-terse.md` | One trigger sentence only | identical |
| `routing-ab-rich.md` | Trigger sentence + 3 `<example>` blocks | identical |

**Name them both `routing-ab-*` to avoid name collision with any live agent.**
Promote one at a time — never both simultaneously (names differ so they can coexist,
but having both live muddies the observation).

## Test procedure

**Setup**
1. `cp _staging/claude/agents/routing-ab-terse.md ~/.claude/agents/`
2. Restart or reload Claude Code so the new agent is in the pool.

**Round 1 — terse variant**

In a fresh conversation (no prior routing context), say each prompt EXACTLY:
```
T1: "how many kilometers is 30 miles?"
T2: "convert 100°C to Fahrenheit"
T3: "5 kilograms in pounds"
T4: "how far is 26.2 miles in km" 
```
For each: note whether Claude (a) auto-delegated to `routing-ab-terse` without prompting,
(b) handled inline without mentioning the agent, or (c) mentioned but didn't delegate.

**Teardown + setup for Round 2**
1. `rm ~/.claude/agents/routing-ab-terse.md`
2. `cp _staging/claude/agents/routing-ab-rich.md ~/.claude/agents/`
3. Restart / reload.

**Round 2 — example-rich variant**

Same four prompts (T1–T4) in a fresh conversation.

## What to record

Fill in and drop into `_mail/houston/inbox/pilot3.routing-ab.result.<date>.md`:

```
## Pilot 3 — Routing A/B result

Date: <YYYY-MM-DD>
Tester: @majkee
Model at test time: <model in use>

### Round 1 — terse description
T1: [ auto-delegated | inline | mentioned-only ]
T2: [ auto-delegated | inline | mentioned-only ]
T3: [ auto-delegated | inline | mentioned-only ]
T4: [ auto-delegated | inline | mentioned-only ]

### Round 2 — example-rich description  
T1: [ auto-delegated | inline | mentioned-only ]
T2: [ auto-delegated | inline | mentioned-only ]
T3: [ auto-delegated | inline | mentioned-only ]
T4: [ auto-delegated | inline | mentioned-only ]

### Observation
<one paragraph: did examples change delegation rate? faster / slower / same?>

### Fact to codify
<one sentence suitable for D1′ amendment or confirmation — e.g.:
  "Examples in description did not measurably increase auto-delegation rate (4/4 inline both variants)"
  "Example-rich description auto-delegated 3/4 vs terse 1/4 — rich carrier provides routing lift">
```

## Cleanup

After recording the result: `rm ~/.claude/agents/routing-ab-rich.md`
Both files in `_staging/` can stay until after the gavel — then archive or delete.

## Routes to

Houston for D1′ codification on majkee's gavel.
If examples DO help routing: D1′ amendment — "include examples where they measurably lift routing."
If no difference: D1′ confirmed as-is — "one trigger sentence sufficient."
