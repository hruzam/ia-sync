# Decision Record — Model × Effort Assignment for CLI Subagents

`status: LOCKED 2026-06-25 (gaveled by majkee)`
`date: 2026-06-25 · thread: capabilities.claude research study`
`shape: ADR — context · locked · consequences · what-an-agent-does-differently`
`research: raw.research/capabilities.claude/ (hypothesis + source-map + 4 lenses + 5 dives + stratification)`

---

## Context

The temple's CLI subagent roster was assembled without a systematic evidence base for model tier and effort level assignments. The pre-study baseline had Houston/Trajectory/Atlas at Sonnet, Agol at Fable (now pulled), and effort levels mostly unset or implicit. A structured research study (40+ sources, live-fetched 2026-06-25) produced the stratification matrix in `raw.research/capabilities.claude/capabilities.claude.stratification.2026-06-25.md`.

---

## Structural Finding

**The "tier = quality" model is wrong. The correct model has three axes:**

```
Quality = f(tier ceiling, effort within tier, task-class fit)
```

1. **Tier** sets the ceiling (what the model can reach at best)
2. **Effort** is a behavioral axis, orthogonal to tier: high effort → more tool calls, explicit planning, self-interrogation before response; low effort → terse, fewer tool calls
3. **Task-class fit** determines where the tier gap is real vs artifact

**Load-bearing finding: effort misconfiguration risk > tier selection risk.**
AMD/Laurenzo (instrumented, 6,852 sessions, 234,760 tool calls): a single default effort change within the same model tier caused 70% reduction in pre-edit research depth, 6× increase in user interrupts, and 122× API cost increase. No tier downgrade comes close.

---

## Locked

**L1 — Agent taxonomy (three classes)**

| Class | Scope | Examples | Holds project context? |
|-------|-------|----------|----------------------|
| Capability agents | Global | Delta, Vector, Trajectory | No — orchestrator teaches them |
| Context agents | Session/project | Houston, Vara | Yes — own the plan + state |
| Reference agents | Global | Color, Janus, Epoch, Agol | No — advisory on demand |

*claude.ai personas (Symmetry, Nabla — in `raw.claude-ai.agents/`) are a separate category: not CLI subagents, not in this matrix.*

**L2 — CLI subagent assignment matrix (15 seats)**

| Agent | Model | Effort | Role |
|-------|-------|--------|------|
| @Houston | opus | high | Architect, planner, gate design, challenge-before-lock |
| @Janus | opus | xhigh | Adversarial challenger — must exceed Houston's reasoning envelope |
| @Color | opus | xhigh | Math/formal reasoning co-brain |
| @Agol | opus | high | Synthesis / continuous advisor (was Fable; Fable 5 pulled 2026-06-25) |
| @Oraculum | fable | high | Scientist-tier strategist — deeper modeling, user-invoked Houston alternative |
| @Vara | sonnet | high | Task runner: holds current session task list, coordinates Trajectory/Delta |
| @Atlas-ui | sonnet | high | Interactive primitive creator |
| @Trajectory | sonnet | high | Senior implementation lead |
| @Atlas-auto | sonnet | medium | Automated primitive emitter (orchestrator-spawned) |
| @Epoch | sonnet | medium | Online researcher, date-calibrated |
| @Vector | sonnet | medium | Middle-tier implementer — context ceiling above Haiku, no judgment needed |
| @CapCom | haiku | low | Human gate — reads houston.goal, assesses risk, awaits confirmation, then spawns Houston |
| @Delta | haiku | low | Surgical execution (read→edit→bash loops) |
| @Recorder | haiku | low | Session memory librarian |
| @Zenith | haiku | low | Harness doc reader (targeted extraction) |

**L3 — Two new seats activated**

`@Vara` — task runner layer between Houston (architect) and Trajectory/Delta (implementers). Receives a gated plan from Houston, holds the task list session-to-session, routes to Trajectory/Vector/Delta, verifies against gate criteria, reports state back. Does NOT re-plan — planning authority lives with Houston. Named for Dorothy Vaughan. Full spec in `~/.claude/agents/vara.md`.

`@Vector` — reliable surgical implementer for tasks that exceed Haiku's context ceiling or require Sonnet-tier code generation but no senior opinion or subagent spawning. Does not flag better approaches. Does not spawn @Delta. Reports exactly what changed. Dispatch when: file > ~40K tokens, medium-complexity new code from spec, or Haiku correction rate >20% on a task class. Named for Oliver Heaviside. Full spec in `~/.claude/agents/vector.md`.

**L4 — Escalation ladder (agentic loops)**

```
Primary:  @Delta      (Haiku, low)     ← simple surgical, known file, known change
Mid:      @Vector     (Sonnet, medium) ← context ceiling exceeded / medium-complexity new code
Senior:   @Trajectory (Sonnet, high)  ← needs opinions, 3+ hop debug, may spawn Delta
Hard:     Opus seat — Houston / Color / Janus (task determines which)

Context escalation trigger: 100–128K tokens consumed (not at 200K cap)
Hard task escalation: Haiku → Opus directly (Sonnet adds only 4pt on SWE-bench Pro vs Opus's 25.6pt)
Cost rule: if task anticipated >150K tokens → Sonnet-from-start (saves uncached reload)
```

*Until GitHub #43083 ships (per-subagent effort from orchestrator): route by agent (Delta / Vector / Trajectory) as the effort proxy. When #43083 ships: Vector and Delta collapse into a single @Delta whose effort the orchestrator specifies per-spawn.*

**L5 — Effort ceiling by task class**

| Task class | Effort ceiling |
|-----------|---------------|
| Classification, extraction, routing, formatting | low |
| Scaffolding, file ops, bash loops | low–medium |
| Code generation from spec (new functions/classes) | medium |
| Hard coding / debugging (multi-file, root cause) | high |
| Planning / orchestration | high |
| Math / formal reasoning (proofs, derivations) | high (Sonnet) / xhigh (Opus) |
| Synthesis / multi-source report | high |
| Adversarial challenge | xhigh |
| ARC-AGI class (novel pattern induction) | high (max effort WORSE than high) |

---

## Consequences

**Key changes from pre-study baseline:**

| Agent | Before | After | Evidence |
|-------|--------|-------|---------|
| @Houston | sonnet | opus · effort:high | LAB all-pass coherence (10.4%); risk-weighting at gate layer; Opus default=high gives self-interrogation |
| @Agol | fable | opus · effort:high | Fable 5 pulled within 48h of launch; silent self-degradation confirmed in Anthropic system card |
| @Janus | opus · effort:high | opus · effort:xhigh | Must exceed architect's reasoning depth; challenge is meaningless if weaker than what Houston already considered |
| @Vara | deferred | sonnet · effort:high | Activated; CrewAI Manager pattern; effort=high gives explicit planning + coordination behavior |
| @Vector | — | sonnet · effort:medium | New seat; Haiku context cap (100–128K real threshold); routing proxy for effort until #43083 |

**Known limitations / open questions:**

1. No published head-to-head benchmark of Opus orchestrator vs Sonnet orchestrator. The 90.2% multi-agent improvement (Anthropic BrowseComp study) proves architectural decomposition wins; it does NOT prove Opus outperforms Sonnet as orchestrator specifically. Houston=Opus is justified by risk-weighting and LAB all-pass coherence — not by a direct tier ablation.
2. GPQA Diamond gap collapses from 17.2pt → ~3.7pt when Sonnet runs with adaptive thinking (the config @Color and @Janus would actually use). Risk-weighting is the primary justification for Opus at Color and Janus seats; the raw GPQA delta is a secondary signal near benchmark saturation.
3. `thinking:` is not a live frontmatter field in the Claude Code agent spec (verified in `raw.settings/raw.claude-agents.harness.2026-06-16.md`). The research matrix's Thinking column is documentation intent; not implementable as a field until it ships.
4. Fable/Mythos return timeline unknown. When Fable returns with stable availability, re-evaluate @Agol and @Houston ceiling.

**Monitoring protocol (Delta / Haiku seat) — operational guidance, not doctrine invariant:**

> These thresholds are starting points; adjust as live data accumulates. Log `(agent, model, effort, task-type, interrupt-count)` per session.

| Signal | Threshold | Action |
|--------|-----------|--------|
| Correction rate | >20% on a task class | Flag that class for Trajectory escalation |
| Context consumption | >100K tokens | Escalate to Trajectory |
| User interrupts per session | >3 on a task type | Review effort level + task-class fit |
| Root-cause failures | Any 3+ hop debug | Route to Trajectory from task start |

---

## What an agent does differently

- **@Houston (now Opus · effort:high):** self-interrogation behavior at effort:high activates by default (Opus 4.8 default). For execution phases: dispatches @Vara, not @Trajectory directly. For planning/gate/challenge: spawns @Janus.
- **@Vara (now active):** receives gated plan, holds task list, routes Trajectory/Vector/Delta session-to-session, verifies output against gate criteria. Does NOT run Bash. Does NOT re-plan.
- **@Janus (now effort:xhigh):** challenge-before-lock function requires deeper reasoning than what Houston already modeled. xhigh is the minimum effort at which the challenge is meaningful. Spawned from Houston; reads context; returns one verdict, one risk, one alternative.
- **@Delta (effort:low confirmed):** fewer tool calls, terse output. Thinking behavior is already baked into Haiku 4.5's 73.3% SWE-bench Verified baseline. Orchestrator must route to @Vector or @Trajectory for tasks exceeding ~100K context or requiring any judgment.
- **@Agol (now Opus · effort:high):** Fable is pulled. Synthesis and cross-phase reasoning at Opus ceiling.
- **@Vector (new):** silent implementer — receives a spec, executes, reports what changed. No opinions. No subagent spawning. The middle rung on the escalation ladder.

---

*Research files: `raw.research/capabilities.claude/` — hypothesis, source-map, lenses L1–L6, dives A–D+X1, stratification.*
*All 15 CLI agent files present in `~/.claude/agents/` on 2026-06-25.*
*Next: monitor Delta seat per the protocol above. Re-evaluate Agol/Houston ceiling when Fable stabilizes.*
