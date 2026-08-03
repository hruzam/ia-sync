---
what: sella.coder-guide — founding document of Sella, the temple's discipline-language
     for Claude Code primitives
state: DRAFT — pending majkee gavel
verified: 2026-08-03 (source reports dated 2026-07-16 .. 2026-08-02)
next:
  - majkee gavel (canon is operator-gaveled; agent-authored-direct canon forbidden)
  - after reposoma merge, home: raw.guides/sella.coder-guide.md
  - receipts re-verify on next platform version jump (last anchor: v2.1.220, 2026-07-25)
---

# SELLA — coder guide

## Receipts (cited as [S1]..[S5] throughout)

- [S1] `raw.research/agent-docs/report/raw.agent-docs.2026-08-01.md` — platform ground
  truth: frontmatter keys, hooks, skills, memory, settings
- [S2] `raw.research/arch/2026-08-01-arch-unix-mind-on-agent-primitives.md` — Unix
  cognates + tensions; D1/D2 doctrine candidates
- [S3] `raw.research/harness/reports/2026-07-20-harness-lifecycle-skill-injection-safe-protocol.md`
  — the authority stack, cold-start order, EXIF frame, §7 layer rule
- [S4] `raw.research/agent-docs/report/2026-07-17-claude-skills-nesting-rube-goldberg.md`
  — inverted precedence, fork contract, nesting verdicts
- [S5] `~/unikuklatrix/nablarva/session/flag.md` — L6/L7/L9: promotion protocol,
  moving-target guardrail, session-surfaces law (the conforming-application precedent)

---

## 0 · NAME · MISSION

**Sella** (Latin: saddle). A discipline-language for Claude Code primitives. Not a file
format — everything stays `.md`. A language you CONFORM to, the way C code conforms to
POSIX: the platform runs anything; Sella says what is well-formed.

Core thesis: **agents = programs, skills = class methods, harness = OS** — with one
premise no language ever had: **the compiler is stochastic and drifts.** Unchanged `.md`
≠ unchanged behavior; the model is a moving target [S5·L7] [S2·tension 4].

Mission — the spine: **AX, agent experience.** An application-for-AI is a place whose
user is an agent. Its quality metric is tokens-to-orientation and verifiability, not UX.
Where UX asks "is it pleasant," AX asks "how many tokens until the agent knows where it
is, and can every claim be checked."

Epistemics clause: `.md` is genotype, behavior is phenotype. You breed and select —
pilots, receipts, gavels — you do not compile deterministically.

Audience: any agent or human building primitives (agents, skills, hooks) or
applications-for-AI (project beds, rooms, harnesses).

---

## 1 · MACHINE MODEL — the authority stack

Three layers. Contracts placed in the wrong layer silently lose authority [S3·§7].

```
KERNEL (enforced · resident · highest authority)     = system prompt
  ├── Anthropic built-in
  ├── agent .md definition (the program's identity)
  ├── --append-system-prompt
  └── skill METADATA (description, ~100 tokens each, resident from startup)

─── boundary ───

USERLAND (guided, not enforced)                      = user-message layer
  ├── CLAUDE.md (all scopes, concatenated; arrives as a user message)
  ├── auto memory (MEMORY.md — first 200 lines / 25 KB)  [S1·memory]
  └── skill BODY (loaded at trigger)

─── PREPROCESSOR (fires before either layer sees a token) ───
  └── !`command` hydration in skill bodies — run-once, no recursion  [S3·§6]
```

Facts that make the stack real, not metaphor [S3·§2]:

- CLAUDE.md is NOT system prompt. It arrives as a user message after the boundary —
  lower authority than the kernel. This is why it is "guided, not enforced."
- Skill descriptions load into the KERNEL at startup — higher authority than anything
  in CLAUDE.md. A description is a behavioral contract, not a label [S3·§5a].
- The preprocessor is the constructive EXIF pattern [S3·§4]: everything fires before
  the model's first reasoning token. The model receives assembled data, not
  instructions to assemble it. Same architecture as the EXIF photo payload — intent is
  the differentiator; audit discipline (L5) is the safeguard.

OS cognates:

| Mechanism | What actually happens | Receipt |
|---|---|---|
| **dlopen** | skill body loads at trigger via literal `cat SKILL.md` — text injection into the current window, not a process | [S3·§3] |
| **exec()** | `context: fork` + `agent:` spawns a specialist with a clean context; it sees nothing of the parent conversation, only the pre-hydrated skill body | [S3·§5d] [S4·§2] |
| **paging** | compaction: skill bodies survive 5,000 tokens each, 25,000 combined, newest first; CLAUDE.md re-injected from disk | [S3·§2,§6] |

---

## 2 · SOURCE MODEL

Every Sella source file has the same anatomy:

- **header = frontmatter** — the declaration the router/linker sees. For agents this is
  the routing surface; for skills it is resident in the kernel from startup.
- **body = implementation** — for agents, the body loads ONLY as the spawned agent's own
  system prompt. It never enters the parent's routing view. Write bodies for the
  spawned process, never for the router.
- **description = the exported symbol** — the one string by which the linker resolves
  you. Everything else in the file is invisible until after resolution.

### Agent frontmatter — full current key surface [S1·sub-agents]

| Key | Notes |
|---|---|
| `name` | required; lowercase+hyphens; no `:` (v2.1.218+) |
| `description` | required; when to delegate — the exported symbol |
| `tools` / `disallowedTools` | allowlist (inherits all if omitted) / denylist; `mcp__<server>` strips a whole server |
| `model` | `sonnet`/`opus`/`haiku`/`fable`/full ID/`inherit` (default) |
| `permissionMode` | `default`/`acceptEdits`/`auto`/`dontAsk`/`bypassPermissions`/`plan`/`manual` |
| `maxTurns` | agentic-turn cap |
| `skills` | preloaded at startup — FULL content injected (the clean bridge [S4·§5]) |
| `mcpServers` / `hooks` | scoped to this agent; ignored for plugin agents |
| `memory` | `user`/`project`/`local` — own cross-session auto memory |
| `background` | `true` = always background (background default since v2.1.198) |
| `effort` | `low`..`max`; overrides session effort |
| `isolation` | `worktree` = isolated git worktree |
| `color` / `initialPrompt` | display; auto-submitted first turn under `--agent` |

The platform absorbed the lifehacks: `memory`, `isolation`, `effort`, per-agent `hooks`
are native keys now — do not rebuild them as conventions.

### Skill frontmatter — full current key surface [S1·skills]

| Key | Notes |
|---|---|
| `name` | display label; the command comes from the directory name |
| `description` | when to use; `description` + `when_to_use` truncate at 1,536 chars combined [S3·§5a] |
| `when_to_use` | extra trigger context; counts toward the 1,536 cap |
| `argument-hint` / `arguments` | autocomplete hint; named args for `$name` substitution |
| `disable-model-invocation` | `true` = user-only; NOT preloadable into subagents [S4·§5] |
| `user-invocable` | `false` = hidden from `/` menu, Claude-only |
| `allowed-tools` / `disallowed-tools` | pre-approved / removed for the skill turn; clears on next message |
| `model` / `effort` | one-turn overrides |
| `context` | `fork` = run in forked subagent — the exec() slot |
| `agent` | subagent type when forked |
| `background` | `false` = wait for forked result (v2.1.218+; default `true`) |
| `hooks` | scoped to skill; `once: true` available here |
| `paths` | glob patterns limiting auto-activation |
| `shell` | `bash` (default) or `powershell` for inline shell |

Substitutions available in bodies: `$ARGUMENTS`, `$N`, `$name`, `${CLAUDE_SESSION_ID}`,
`${CLAUDE_EFFORT}`, `${CLAUDE_SKILL_DIR}`, `${CLAUDE_PROJECT_DIR}` [S1·skills].

---

## 3 · THE NINE LAWS

**L1 — Right contract, right layer.**
Identity and ground-truth declarations → kernel (agent .md, skill description);
workflow conventions → CLAUDE.md; procedural playbooks → skill bodies; live data →
preprocessor. WHY: authority is positional — a rule in the wrong layer is a rule the
model may treat as a suggestion. Receipt: [S3·§7], verbatim harness-builder's rule.

**L2 — Terse header.**
One trigger sentence in the description; examples only if they demonstrably earn
routing lift; the 1,536-char truncation for skills is documented, not folklore. WHY:
the header is a resident kernel cost paid every session by every agent, and `<example>`
blocks are training signal for the router, bloat for the human reader [S2·tension 1].
Receipt: [S1·skills 1,536 cap] [S3·§5a].

**L3 — One job, one name.**
The name teaches the function: a *ferry* carries context across a boundary, a *cairn*
marks a path already walked. If the job statement needs "and", it is two primitives.
WHY: the router resolves by description, but humans and agents both grep by name —
a name that teaches saves the read. Receipt: [S2·Part A] — McIlroy's "do one thing
well" as literal evaluation criterion, not metaphor.

**L4 — EXIT/OUTPUT contract, man-page style.**
Every primitive declares what it returns and how it fails. For hooks: **exit 2 is the
ONLY blocking code; exit 1 does NOT block** — it shows stderr and continues. Exit 0
parses stdout JSON. WHY: the `set -e` instinct ("nonzero fails the pipeline") is a trap
here; a guard hook exiting 1 guards nothing. Receipt: [S1·hooks exit codes + the
blockable/non-blockable event lists].

**L5 — Read before run.**
Audit every `!`-line manually before the skill exists on your disk. NO dry-run/trace
mode exists on the platform (verified 2026-08-02) — there is no `bash -x` analog for
the preprocessor. Treat skills like installing software: the AUR trust model — nobody
vets the artifact for you; verifying it is your step. WHY: descriptions inject
kernel-level authority and `!`-lines run arbitrary shell with your privileges, before
the first token, on a routing decision you did not make. Receipt: [S2·AUR/PKGBUILD]
[S3·§4,§5e — "treat Skills like installing software"] [S2·tension 2 — dry-run named as
missing mitigation].

**L6 — Precedence inversion.**
Skills: higher scope wins (Enterprise > Personal > Project). Subagents: more local wins
(Managed > CLI > Project > User > Plugin). These are opposite; never design assuming
one rule. WHY: a name collision across scopes silently resolves to a different file
depending on primitive kind — the wrong-definition failure is invisible until behavior
drifts. Receipt: [S4·§4].

**L7 — Prelude split.**
Only the kernel layer survives inattention. What you need when you don't think you need
anything — identity, hard limits, the one safety rule — must live in the kernel; the
rest can live below the boundary. WHY: CLAUDE.md is a user message and compaction
prunes userland; the kernel is the only resident memory. Receipt: [S3·§2 cold-start
order + §6 "CLAUDE.md adherence: user-message layer — not enforced, only guided"].

**L8 — Moving compiler.**
D2′, verbatim: *unchanged `.md` ≠ unchanged behavior; the model is a moving target.*
Receipts, pilots, and gavels replace determinism: a primitive is trusted because it was
piloted on a dated model and the result was recorded — never because its diff is clean.
Genotype (`.md`) / phenotype (behavior) honesty: you select what survives, you do not
compile. WHY: git-diff-clean ≠ behavior-identical breaks the "verify once, trust
forever" model every other language assumes. Receipt: [S2·tension 4 → D2] [S5·L7].

**L9 — Anchors, not full reads.**
Agents get anchors — descriptions, provenance stones, `next[]` pointers, grep targets;
humans get full reads. Point, never copy. WHY: AX token economy — every full read an
agent did not need is orientation budget burned; the platform itself works this way
(~100-token skill metadata, 200-line memory cap, progressive disclosure). Receipt:
[S3·§3 progressive-disclosure table] [S1·memory limits].

---

## 4 · HOW TO CODE — three walks

Pad style: numbered stations, each with a verify gate. Do not skip gates.

### Walk A — write a program (an agent)

1. **Name sweep.** Grep the name across every scope: `~/.claude/agents/`,
   `.claude/agents/`, plugin dirs. Remember L6: for agents, project beats user — a
   project file with your name shadows you. Name: lowercase+hyphens, no `:`.
   *Gate: zero collisions, or the collision is intentional shadowing you can state.*
2. **One-job statement.** Write the job in one sentence. If it contains "and", split
   into two agents (L3).
   *Gate: the sentence has one verb-object.*
3. **Declare the header.** `name`, `description` (the exported symbol — one trigger
   sentence, L2), `tools` as an explicit allowlist (inherit-all is a decision, make it
   consciously), `model`, `effort`; `memory`/`isolation` only if the job needs them.
   *Gate: every key exists in the [S1] agent table — no invented keys.*
4. **Write the body.** Identity, operating rules, output contract. The body is the
   spawned agent's system prompt and nothing else — it never reaches the parent's
   routing view. Assume no conversation history exists.
   *Gate: read the body as a cold-started stranger; nothing references "above" or
   "the user said".*
5. **EXIT/OUTPUT contract (L4).** State in the body what the agent returns: shape,
   length, failure form ("if scope is unclear, return the question, do not guess").
   *Gate: a caller can parse success from failure without reading prose.*
6. **Audit attachments (L5).** If the header preloads `skills:` or declares `hooks`,
   read every preloaded body and hook command as if installing it fresh.
   *Gate: you have personally read every line that will execute or enter the kernel.*
7. **Invoke test — order, not channel.** Spawn it once with a real scoped task
   (subagent spawn or interactive seat — a program's contract is the one-line
   ORDER it accepts, never a vendor flag; print-mode flags are volatile against
   vendor shift and must not be baked into builds — operator law 2026-08-03).
   Then probe routing: phrase the job naturally, check the router picks this agent.
   *Gate: correct result + correct routing + tokens-to-orientation you can defend.
   Record the pilot: date, model, verdict (L8) — this receipt IS the trust.*

### Walk B — write a method (a skill)

1. **Skill or agent?** Reference content that should stay in the caller's window →
   plain skill. Self-contained task needing isolation → `context: fork`. Reference
   content + fork = Rube Goldberg — the subagent gets rules but no task [S4·verdict
   table].
   *Gate: you can say which row of the [S4] verdict table you are.*
2. **Directory + name.** The command comes from the directory name; `name` is display
   only. One job (L3).
   *Gate: name sweep across skill scopes — and remember L6: for skills, PERSONAL beats
   project.*
3. **Header.** `description` + `when_to_use` ≤ 1,536 chars combined (L2) — count them.
   `arguments` for named substitution; `allowed-tools` minimal;
   `disable-model-invocation: true` for anything with side effects [S3·§5e] — noting
   it then cannot be preloaded into subagents [S4·§5].
   *Gate: char count under cap; side-effect skills are user-only.*
4. **Body with hydration.** Playbook steps; `!`-lines for live data, each with a
   fallback so a missing file degrades loudly, not silently:
   `` !`cat $file 2>/dev/null || echo "[FILE NOT FOUND]"` `` [S3·§5b]. Hydration is
   run-once, no recursion, fires before the first token.
   *Gate: every !-line has a failure branch that names itself.*
5. **Audit the !-lines (L5).** No dry-run exists — run each command by hand in a
   shell, with the arguments you expect and with garbage arguments.
   *Gate: you executed every line manually; none surprised you.*
6. **Fork wiring (if forking).** `agent:` names the specialist; the body must carry
   the complete task — the fork sees no parent history [S4·§2]. `background: false`
   if the caller must wait.
   *Gate: the body read alone is a complete, answerable brief.*
7. **Trigger test.** Invoke as `/name` with real args; then phrase the trigger
   naturally and confirm auto-invocation (or confirm it does NOT auto-invoke, if
   `disable-model-invocation`).
   *Gate: both invocation paths behave as declared. Record the pilot (L8).*

### Walk C — wire an event (a hook)

1. **Pick the event — and check it can block.** Only some events honor exit 2
   (`PreToolUse`, `Stop`, `UserPromptSubmit`, `PreCompact`, ...); `PostToolUse`,
   `SessionStart`, `SubagentStart` CANNOT block [S1·hooks].
   *Gate: your event is on the right list for your intent.*
2. **Matcher + scope.** Exact string for one tool, regex for families,
   `mcp__<server>__.*` for MCP. Placement is scope: skill/agent frontmatter = lives
   and dies with the component; `.claude/settings.json` = project-wide;
   `~/.claude/settings.json` = everywhere. Prefer the narrowest scope that works.
   *Gate: you can state why this scope and not one narrower.*
3. **Write the command — L4 is the whole station.** Block = exit 2 + reason on
   stderr. Decide = exit 0 + JSON on stdout (`permissionDecision`,
   `additionalContext`, `updatedInput`). Exit 1 = non-blocking noise. Shell form vs
   exec form: `args` present means no shell — no pipes, no `&&`.
   *Gate: the script's exit paths are explicit; no code path falls through to
   exit 1 while meaning "block".*
4. **Timeout + async.** Default 600s; `UserPromptSubmit` capped at 30s;
   `SessionEnd` shares a 1.5s budget. `async: true` for fire-and-forget;
   `asyncRewake: true` to wake Claude on exit 2.
   *Gate: worst-case runtime fits the event's budget.*
5. **Test all three exit paths.** Force a 0, a 2, and a nonzero-non-2 from the real
   hook in a live session.
   *Gate: exit 2 actually blocked; exit 1 actually did not. You have watched both.*

---

## 5 · A CONFORMING APPLICATION

An application-for-AI is a place whose user is an agent. Conformance is four provisions:

**1. A saddle** — a single entry file declaring the read-order by seat: "you are X,
read A → B → C, then you are oriented." Tokens-to-orientation is the metric; the saddle
is its instrument. No conforming application makes an agent discover its own
orientation path.

**2. Surfaces** — exactly three, per the nablarva session-surfaces law [S5·L9], which
is the precedent because it was gaveled on an 8-root survival survey, not on taste:

| Surface | Role | Discipline |
|---|---|---|
| `flag.md` | the locks | append-only; locked items are not re-litigated without new evidence |
| `pulse.md` | canonical doing-state | ONE file — the survey receipt: pulse forks reliably orphan one branch |
| `dock.md` | uncanonical scratch | any seat writes without blessing; prunable without ceremony; never citable as truth |

No standing `plan.md` — zero survivors in 8 surveyed roots; plans rot into orphans and
journals die [S5·L9]. Task-scoped work gets `session/<topic>/` dirs that die with the
task.

**3. Provenance stones** — every durable artifact opens with the four-key YAML header:
`what` / `state` / `verified` / `next[]`. These are gamebook pointers: `next[]` tells
the reader where to walk from here, so an agent landing mid-graph orients from the
stone alone (L9 — the stone is the anchor; the body is the full read). `verified` is a
date, because of L8 — an undated claim is an unclaimed claim.

**4. A promotion protocol** — experimental shapes are bred in the bed; promotion out is
a REVIEWED MERGE, never auto-deploy [S5·L6]. Nothing an agent wrote reaches a live
surface (`~/.claude/`, a deploy target) without passing a human or gate review. This is
L8 operationalized: selection pressure applied at the boundary, with a receipt.

---

## 6 · GLOSSARY

| Sella term | Platform term | Unix cognate |
|---|---|---|
| program | subagent (`.claude/agents/*.md`) | binary in `$PATH` |
| method | skill (`SKILL.md`) | shared-library function |
| exported symbol | `description` frontmatter | symbol table entry / man NAME line |
| kernel | system prompt (agent .md + skill metadata) | kernel space, resident |
| userland | CLAUDE.md + memory + skill bodies | userland config, dotfiles |
| preprocessor | `!`-hydration in skill bodies | `$(...)` substitution / cpp |
| dlopen | skill body load at trigger | `dlopen(3)` |
| exec | `context: fork` + `agent:` | `fork(2)`/`exec(3)` |
| paging | compaction (5k/25k budgets) | swap / page eviction |
| event wire | hook | `trap` / git hook / systemd unit |
| gate | blocking exit 2 | nonzero exit under `set -e` |
| saddle | entry read-order file | login rc / `init` |
| flag | locked-decisions file | append-only log |
| pulse | canonical doing-state | `/var/run` state file |
| dock | uncanonical scratch | `/tmp` |
| provenance stone | what/state/verified/next[] header | man-page header / `.PKGINFO` |
| receipt | dated source citation | PKGBUILD checksum |
| pilot | dated trial run on a named model | canary deploy |
| gavel | operator approval locking canon | signed merge to main |
| AX | agent experience (tokens-to-orientation) | man-page discipline / DX |

---

*Sella coder guide · draft for gavel · forged 2026-08-03 · sources [S1]–[S5] above.*
