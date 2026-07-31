# Codex relay family — metadata/scripting upgrade guide
`Date: 2026-07-31 · @Epoch · practitioner guide, not canon — draft for @majkee gavel if adopted`
`Scope: @vega (blind crosscheck relay = codex-crosscheck.md on disk) · @astrobley (relay coder =`
`codex-coder.md on disk) · @mirror (position-aware adversarial challenger — NOT YET ON DISK,`
`no file found under ~/.claude/agents/ at time of writing; treat mirror sections as design notes)`

## 0 — What's actually on disk right now (verified 2026-07-31)

- `~/.claude/agents/codex-crosscheck.md` — model: haiku, tools: `Bash, Read`. No `maxTurns`,
  no `disallowedTools`, no `hooks`. Matches the "@vega" brief.
- `~/.claude/agents/codex-coder.md` — model: **sonnet** (not haiku — the task brief says all
  three are haiku gates; codex-coder is not). tools: `Read, Grep, Glob, Bash`.
- No `mirror.md`, `astrobley.md`, `vega.md`, `gemini-cross-check.md` exist on disk. The names
  in the task map onto the two files above by role description, not by filename. CONFIDENCE: H
  (direct `find`/`ls` against `~/.claude/agents/`, 2026-07-31).
- Wrapper: `~/.config/zsh/ai/codex-run.zsh` — reads exactly 2 positional args (`prompt`,
  `model`), no `maxTurns`-equivalent, single retry via `script -qfc`, exit codes 3/4/5 documented
  in-file. CONFIDENCE: H (read source directly).

## a) Agent-frontmatter vs SKILL-frontmatter — precise field split

Web-verified 2026-07-31 against `code.claude.com/docs/en/sub-agents` and
`code.claude.com/docs/en/skills` (current as of that fetch). CONFIDENCE: H unless noted.

**Valid in agent `.md` frontmatter** (`.claude/agents/<name>.md`):
`name, description, tools, disallowedTools, model, permissionMode, maxTurns, skills,
mcpServers, hooks, memory, background, effort, isolation, color, initialPrompt`.
Only `name`+`description` required. `maxTurns` IS a real, current agent-only field — confirms
the task brief's `gemini-cross-check` reference is plausible in shape (file itself not found
on disk under that name, so I can't confirm its current value — see §0).

**Valid in SKILL.md frontmatter** (`<skills-dir>/<name>/SKILL.md`):
`name, description, when_to_use, argument-hint, arguments, disable-model-invocation,
user-invocable, allowed-tools, disallowed-tools, model, effort, context, agent, background,
hooks, paths, shell`.

**Keys that look similar but live on ONE side only — do not cross-apply:**
| Concept | Agent-side key | Skill-side key |
|---|---|---|
| tool allowlist | `tools` (also accepts `Agent(name)` scoping) | `allowed-tools` (hyphenated, turn-scoped, clears next message) |
| tool denylist | `disallowedTools` (camelCase) | `disallowed-tools` (hyphenated) |
| turn cap | `maxTurns` — **agent only, no skill equivalent** | — |
| fork to subagent | N/A (an agent file IS the subagent) | `context: fork` + `agent: <type>` |
| block auto-trigger | N/A (agents are always explicitly invoked) | `disable-model-invocation: true` |
| `!` backtick hydration | N/A — agent body is static system prompt, no preprocessing pass | native — runs once, top to bottom, before Claude sees content |
| argument substitution ($ARGUMENTS, $0, $name) | N/A — agents receive a delegation message from the caller, not positional args | native |

**Key correction to the harness report's model** (2026-07-20 report, §5d): that report shows
`allowed-tools`, `context: fork`, `agent:`, `effort:`, `model:` as one undifferentiated
"skill frontmatter" block. That's accurate for skills but the report doesn't flag that agent
`.md` files use a *different, non-overlapping* vocabulary (`tools` not `allowed-tools`,
`disallowedTools` not `disallowed-tools`, no `context`/`agent`/`arguments` keys at all). This
guide's table above is the correction. CONFIDENCE: H (both docs pages fetched live 2026-07-31).

## b) Concrete upgrades — evaluated per candidate

**1. `maxTurns` cap on the three relay agents — REAL, cheap, do it.**
All three are meant to be single-shot relays (one wrapper call, verbatim return). Nothing in
their current `.md` bodies stops a future edit from letting them loop (retry logic creep,
follow-up questions to Codex). `maxTurns: 3` (one Bash call + one Read/verify + one report turn)
on codex-crosscheck and codex-coder costs nothing and closes that door structurally instead of
relying on prose discipline ("One call per brief. No follow-ups" is currently prose-only in
codex-crosscheck.md line 43). WHY it's real: it's a load-bearing frontmatter field, verified
current, and matches the existing prose contract — this converts a promise into an enforced cap.
```yaml
---
name: codex-crosscheck
model: haiku
tools: Bash, Read
maxTurns: 3
---
```

**2. Skill-side `/mirror` or `/crosscheck` entry points with `!` hydration — REAL but only for
the human-invoked path, not the relay agent itself.**
The relay AGENT (`codex-crosscheck.md`) cannot use `!` backtick hydration — that syntax only
fires in SKILL.md bodies. What IS real: a skill at `~/.claude/skills/crosscheck/SKILL.md` that
pre-assembles a brief (e.g. pulls the live plan from `flag.md`, strips position language via a
grep/sed pass) BEFORE handing off to the codex-crosscheck agent via `context: fork` +
`agent: codex-crosscheck`. This is the correct division of labor: skill = brief assembly
(deterministic, scriptable, auditable), agent = the trust boundary (position-leak refusal,
wrapper invocation, graceful-fail). Example:
```yaml
---
name: crosscheck
description: Brief a blind Codex crosscheck against the current plan.
disable-model-invocation: true
context: fork
agent: codex-crosscheck
---
## Plan under review (position stripped)
!`grep -v -iE 'i think|recommend|lean|prefer' flag.md`

## Task
Carry the brief above to Codex verbatim. Refuse if it still leaks a position.
```
CAVEAT: this only helps if the `!` grep-strip is trustworthy — a crude regex is not a real
position-leak filter, it just removes the most obvious phrasing. Keep the agent-side refusal
check (codex-crosscheck.md lines 19-34) as the real gate; treat the skill-side strip as a
best-effort pre-filter, not a substitute.

**3. `context: fork` + `agent:` composition — REAL, already the mechanism above. Nothing to add
beyond #2; don't build a second parallel composition path.**

**4. Argument substitution for wrapper flags — REAL, narrow, low value but zero cost.**
A skill entry point (`/codex-task <files> <task>`) can use `arguments: [files, task]` and
`$files`/`$task` substitution to hand a cleanly-templated brief to codex-coder, instead of
relying on the calling agent to hand-assemble prose every time. Only worth it if this relay is
invoked by humans directly with any frequency — if it's always orchestrator-to-subagent (Houston/
Flight/Vara → codex-coder via Agent tool), skip this: the Agent tool's delegation message
already carries structured task text, and a skill layer adds a hop for no benefit.

**5. `disable-model-invocation` for side-effectful skills — REAL, apply to any skill wrapping
codex-coder (which touches files via `git apply`).** Do not let Claude auto-trigger a Codex
write-task from ambient conversation. This mirrors the doc's own `/deploy` example exactly —
codex-coder calls carry real cost (16-45K tokens, shared ChatGPT Plus quota per codex-line
guides) and real side effects (file writes). Set it on any skill entry point, not on the agent
file itself (agents have no such field — see table in §a).

**6. `disallowedTools` on the relay agents — REAL, small, matches existing prose.**
codex-crosscheck.md already declares `tools: Bash, Read` (a tight allowlist — good). No action
needed there. If a `mirror` agent is built with a wider tool set (position-aware adversarial
challenger implies it may need `Grep`/`Glob` to read the position under challenge),
`disallowedTools: AskUserQuestion` keeps it from stalling on interactive prompts inside an
automated pipeline — this is the harness report's §5e safeguard #4, correctly agent-side since
`disallowedTools` is a real agent frontmatter field (camelCase form).

## c) Codex-CLI mechanics the relay agents should surface as metadata (not prose)

From `raw.guides/codex-line.builder.md` (WS2/WS3, verified 2026-07-24/25, CONFIDENCE H — distilled
from live Epoch passes, itself due for refresh if >1 month stale, i.e. by 2026-08-24):

- **Exit codes 3/4/5 are already correctly handled in prose** in both codex-crosscheck.md and
  codex-coder.md, matching the wrapper's actual behavior (verified by reading codex-run.zsh
  directly, §0 above). No upgrade needed here — this is already right, don't touch it.
- **E1 economics contract (16-45K token overhead per call)** — codex-coder.md already encodes
  this as a bounce-micro-tasks rule. codex-crosscheck.md does NOT mention token cost at all.
  Given crosscheck is explicitly for "stone trials and second-opinion synthesis ONLY," the missing
  cost note is consistent with its narrower use — but if crosscheck calls become routine, add the
  same E1 line. Not urgent.
- **`-m` model flag exists but no `--list-models`** (G6 in the builder guide) — model errors are
  silent failures upstream, not something codex-run.zsh can validate before calling. Both agents
  already say "surface model errors LOUD" / "must be LOUD" — correct, keep as-is.
- **Nothing in the codex cards suggests a `maxTurns`-equivalent wrapper flag exists.** Codex CLI's
  own session model (7h auto-compacting sessions, `/fork` checkpoints) is irrelevant to a single
  `codex exec --ephemeral` call — the wrapper already forces ephemeral, single-shot semantics.
  Do NOT try to plumb Codex's `/fork`/Goal Mode concepts through the relay agents; those are
  interactive-TUI concepts with no `exec` equivalent (codex-line.user.md, item 4).

## d) What is NOT worth doing (the theater)

- **Skill-side `!` hydration inside the relay AGENT body itself.** Impossible (agent .md bodies
  are static system-prompt text, not skill bodies) and even as a skill it would just be
  re-implementing what codex-run.zsh already does at the shell layer. Don't build a second
  templating system on top of a wrapper that already does `cat`/`grep`/build-and-exec.
- **`memory:` field on codex-coder/codex-crosscheck.** These are stateless, verbatim relays by
  design ("I do not: Summarize / Editorialize / Reconcile" — codex-crosscheck.md). Persistent
  agent memory across sessions actively contradicts the "blind" and "verbatim" contracts — a
  memory directory would let the relay accumulate a position over time, which is the exact thing
  decision 0005's blind-triangulation method exists to prevent.
- **`isolation: worktree` on the relay agents.** They don't write code themselves — codex-coder's
  actual file writes happen via `git apply` inside the CALLING session's working tree, driven by
  Codex's diff output. Worktree isolation on the *relay agent* wouldn't isolate the actual
  mutation (that's Codex's `--sandbox workspace-write`, already handled by the wrapper); it would
  just add a git-worktree layer that the `git apply --recount` step would then have to reconcile
  back out. Complexity with no matching real boundary.
- **Multi-agent V2 / Codex `spawn_agent`.** Explicitly OFF per codex-line.builder.md ("Temple
  position: our orchestration stays on the Claude side... do not enable until a real need + these
  bugs close" — referencing open GH #31814/#20077/#26753). Nothing about the relay family changes
  that calculus; a Codex-side spawn would break the "Claude plans, Codex executes" split (0005).
- **`background: true` on the relay agents themselves.** These are meant to return synchronously
  into a triangulation or coding flow where the orchestrator is waiting on the verbatim output to
  proceed (crosscheck feeds a triangulation decision; coder feeds a diff-apply step). Backgrounding
  them just adds a poll/notify hop for a call whose entire value is a bounded synchronous relay.
- **`hooks:` (PreToolUse/PostToolUse) on the relay agents to "validate" the wrapper call.** The
  wrapper already IS the validation layer (stdin-hang guard, retry, exit-code classification —
  codex-line.builder.md G1-G8). A hook re-validating Bash calls before they reach the wrapper
  would duplicate logic that's already centralized in codex-run.zsh, which is the entire point of
  "never call codex exec directly" (both agent files, verbatim). Keep the wrapper as the single
  home of the mitigations, per its own header comment.

## Sources
- `/home/hruzam/reposoma/raw.research/harness/reports/2026-07-20-harness-lifecycle-skill-injection-safe-protocol.md` — CONFIDENCE H (local, dated 2026-07-20)
- `/home/hruzam/reposoma/raw.guides/codex-line.builder.md`, `codex-line.user.md` — CONFIDENCE H (local, DRAFT-for-gavel 2026-07-25, distilled from live Epoch passes)
- `/home/hruzam/reposoma/raw.settings/raw.card.claude-code.md` — CONFIDENCE H (local, verified 2026-07-16, half-life 21 days — due refresh ~2026-08-06)
- `~/.claude/agents/codex-crosscheck.md`, `codex-coder.md`, `~/.config/zsh/ai/codex-run.zsh` — CONFIDENCE H (read directly, 2026-07-31)
- [code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents) — CONFIDENCE H (live-fetched 2026-07-31)
- [code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills) — CONFIDENCE H (live-fetched 2026-07-31)
- `@mirror` agent file: NOT FOUND on disk at time of writing — recommendations in §b/§d for
  "mirror" are design guidance to apply IF/WHEN that file is created, not a description of an
  existing config. Flag this to whoever builds it.

## e) POST-SCRIPTUM — state change + naming law (Atlas, same day, majkee gaveled)

- §0 is already historical: the on-disk names changed hours after this guide was written.
  `codex-crosscheck.md` → **`vega.md`** · `codex-coder.md` → **`astrobley.md`** ·
  **`mirror.md` now EXISTS** — all on the ia-sync table, deploy-pending. `maxTurns` from §b1
  was ADOPTED (vega/mirror: 3 · astrobley: 6). `memory:`/`hooks:`/`background:` anti-recs honored.
- **NAMING LAW (majkee, 2026-07-31): a skill and an agent must NEVER share a name.**
  §b2's `/crosscheck` example is now safe (agent renamed to vega) — but a `/mirror` skill
  would collide with @mirror and is FORBIDDEN under that name. If/when the skill-side entry
  points are built, name them off-agent (e.g. `/stone-trial`, `/mirror-brief`, `/codex-task`) —
  never `/vega`, `/astrobley`, `/mirror`.

`refresh trigger: re-verify if this guide is used after 2026-08-24 (codex-line.builder.md's own`
`monthly refresh window) or after any codex-run.zsh / agent-frontmatter-doc change.`
