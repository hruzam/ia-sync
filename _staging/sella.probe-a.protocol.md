---
what: Probe A protocol — cold orientation, two lanes (ecological + normalized)
state: STAGED — protocol only; results file follows execution
verified: 2026-08-05 (Wave review + amendments folded)
by: atlas-ui (office) · reviewed by wave (GPT-5-family, advisory)
ref:
  - radio.wave-to-atlas.sella-codex-line.2026-08-03.md (probe definitions)
  - radio.wave-to-atlas.sella-consultation.2026-08-05.md (two-lane split, amendments)
  - sella.cross-vendor.architecture.errata-r1.2026-08-04.md (G4 probe ordering)
  - raw.guides/codex-line.user.md + codex-line.builder.md (Codex harness surface)
next:
  - majkee executes A-eco, then A-norm (Probe B already CLOSED)
  - results → sella.probe-a.results.<date>.md (same _staging/)
  - Probe D follows A (G4 order: B(done) → A → D)
---

# Probe A — cold orientation

## Purpose

Measure how each vendor's native harness discovery shapes cold orientation quality
on the same repo with the same goal. Two lanes test different questions:

- **A-eco (ecological):** the real deployed ecosystems as they stand today. Claude
  has 15+ project-local files; Codex has zero. Measures **operator outcome** — what
  the user actually gets.
- **A-norm (normalized):** isolated substrate comparison. Both vendors get equivalent
  minimal context. Measures **cold-start quality** when ecosystem richness is
  controlled for.

Both feed B1-vs-B2 indirectly: if richer harness produces measurably better
orientation, shared core laws must account for it. If both orient similarly
despite asymmetric config, the portable core is thinner than expected.

**Scope mark:** exploratory, n=1 per lane. First measurement, not a vendor-level
verdict. Signal, not proof.

## Venue

**applications-in-common** (the factory). Rationale: real project with real
structure, Claude-side harness is rich (3 agents, 5 skills, 3 rules files,
2 hooks, settings.local.json, CLAUDE.md, AGENTS.md). Codex-side has zero
project-local config — only AGENTS.md, which both vendors discover natively.
The asymmetry IS the measurement in A-eco; A-norm controls for it.

## Probe ordering (G4 gavel, errata-r1)

Gaveled order: **B → A → D.** Probe B CLOSED (2026-08-05, Jacquard trial,
fix promoted). This probe is next. Probe D follows after A results are recorded.

## Lane A-eco — ecological (real harness asymmetry)

### Clean conditions

| | Claude | Codex |
|---|---|---|
| Session | Fresh `claude` from project root. No `--resume`, no `--agent` | Fresh `codex` from project root |
| Project config | Full `.claude/` (agents, skills, rules, hooks, settings) + CLAUDE.md + AGENTS.md | No `.codex/`, no project config. AGENTS.md only |
| Global config | Normal `~/.claude/` (CLAUDE.md, agents, skills, settings.json) | Normal `~/.codex/` (config.toml, hooks.json, agents/ if present) |
| Steering | Zero — the prompt only. Operator does NOT name any file | Same |

### Repository snapshot

Each run gets its **own identical snapshot**. Do not run Claude and Codex
sequentially against one mutable copy.

1. Record current state: `git rev-parse --short HEAD`, `git status`, timestamp
2. Create two identical working copies (e.g., `git worktree add` or `cp -a`):
   - `probe-a-eco-claude/` — Claude runs here
   - `probe-a-eco-codex/` — Codex runs here
3. Record snapshot identity: commit hash + dirty status + `find . -type f | sort | sha256sum` or equivalent

### Execution

1. **Claude run:** open fresh session in its snapshot copy. Paste the prompt
   verbatim. Do NOT steer — observe silently. Log every tool call (Read/Grep/
   Glob/Bash), every statement, timestamps. When it declares "done" or stalls, stop
2. **Codex run:** open fresh session in its snapshot copy. Same protocol.
   Log identically
3. Record client versions: `claude --version`, `codex --version`
4. Record run order (Claude-first or Codex-first — flip a coin, note it)

## Lane A-norm — normalized (clean substrate comparison)

### Clean conditions

| | Claude | Codex |
|---|---|---|
| Session | Fresh, from a clean snapshot (see below) | Same clean snapshot |
| Project config | `.claude/` directory **REMOVED**. CLAUDE.md stripped to ONLY `@AGENTS.md` (the bridge line — no other content). AGENTS.md unchanged | No `.codex/`. AGENTS.md unchanged |
| Global config | **Exact spec below** | **Exact spec below** |
| Steering | Zero | Same |

### Global config — exact specification (not "equivalent")

**Claude:**
- `~/.claude/CLAUDE.md` — present (global instructions are part of the product)
- `~/.claude/agents/` — empty or absent (no agent routing influence)
- `~/.claude/skills/` — empty or absent (no skill preloads)
- `~/.claude/settings.json` — minimal: only `permissions` if needed for the
  project directory; no hooks, no custom `allowedTools`
- Environment: record `CLAUDE_*` env vars, `ANTHROPIC_*` vars, PATH

**Codex:**
- `~/.codex/config.toml` — default/minimal (no custom profiles, no model pins)
- `~/.codex/agents/` — empty or absent (no global custom agents)
- `~/.codex/hooks.json` — default install state (inspect and record contents)
- Environment: record `CODEX_*` env vars, `OPENAI_*` vars, PATH

**Shared:**
- Record: network state (online/offline), available tools (`lsof`, `jq`, etc.),
  shell (`$SHELL`, version), OS, terminal
- Both sessions must have equivalent tool permissions (both can read files,
  run commands, etc.)

### Repository snapshot

Same procedure as A-eco, but AFTER stripping Claude config:

1. Start from the same commit as A-eco
2. Remove `.claude/` directory
3. Replace CLAUDE.md contents with exactly: `@AGENTS.md`
4. Create two identical copies from this stripped state
5. Record snapshot identity (commit + modifications + hash)

### Execution

Same as A-eco. Fresh session, paste prompt, silent observation, full logging.

## The identical prompt (verbatim to both vendors, both lanes)

```
You are starting cold in this project. Your task:

1. Orient yourself using whatever native mechanisms you have.
2. One-paragraph summary: what is this project and how is work organized?
3. Find the most recently active experiment — describe its hypothesis, state,
   and which files carry it.
4. This project has a zsh-based developer toolkit. Find it, describe its boot
   sequence, and name one thing that would fail if the tmux server is not running.
5. Name the three most important files a new contributor should read first,
   in order.

Work from evidence, not assumptions. Show your orientation path.
```

## Metrics

### Primary (Wave's five, operationalized)

| # | Metric | How to measure |
|---|---|---|
| M1 | Tokens to correct project identification | Count tool calls + tokens until first accurate "what this is" statement |
| M2 | Wrong / unnecessary file reads | Every file-open logged. Mark: necessary (on path to answer) vs dead-end (wrong guess) |
| M3 | Unsupported assumptions | Statements made before evidence is in context |
| M4 | First evidence-producing action | Which file/command was the first move contributing to a correct answer? |
| M5 | Operator correction count | Target: zero. Pure observation, no steering |

### Evidence categories (Wave amendment 3 — three-layer separation)

For each vendor run, separate evidence into:

1. **Model-claimed loaded sources** — what the model SAYS it was given or read
   at startup. This is self-report, not loader proof
2. **Externally-observed file reads** — tool-use log showing every actual Read/
   file-open action the model took, with timestamps
3. **Canary adoption** (optional, recommended for A-norm) — if instruction
   canaries are placed in candidate source files, record which canaries appear
   in the model's behavior/output. Evidence of actual loading, not just claim

## What this really tests

**A-eco:** does Claude's richer project-local ecosystem produce measurably
better orientation than Codex's AGENTS.md-only discovery? This is the
operator-outcome question — what do you get today?

**A-norm:** when ecosystem richness is controlled for, does the underlying
model/harness cold-start mechanism differ in quality? This is the substrate
question — is the difference in the config or in the mind?

**Combined:** if A-eco shows a gap that A-norm closes, the gap lives in the
ecosystem (fixable by adding Codex config). If A-norm also shows a gap, the
gap lives in the substrate (model capability or harness mechanics).

Neither lane tests the exchange contract directly. Probe D does that.

## Recording

- Protocol: this file (`sella.probe-a.protocol.md`)
- Results: `sella.probe-a.results.<date>.md` (one file, both lanes, comparison table)
- Raw logs: operator's discretion (full session logs if practical; at minimum
  the tool-use trace per run)

## Scope boundaries

- This is n=1 exploratory. Do not generalize to "Claude is better/worse at X"
- One venue (the factory). Different projects may produce different results
- Sequential runs (not parallel). Order effects possible — record and note
- The prompt tests orientation, not coding. A separate probe could test
  task-completion quality on an identical well-defined change
