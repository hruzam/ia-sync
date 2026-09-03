# How practitioners actually run agentic coding sessions

Independent field-research response to *BRIEF — how practitioners actually run agentic coding sessions*  
Research cutoff: 2026-09-02

## Bottom line

The practice that has actually converged is smaller and less mystical than the surrounding discourse:

1. Give an agent an outcome-sized job, not an indefinitely growing relationship.
2. Give it a cheap executable way to prove the result: tests, a build, a linter, a browser check, or a purpose-built oracle.
3. Put recoverable state in Git and a few deliberately scoped files; do not rely on the transcript as the only memory.
4. Parallelize independent discovery freely, but parallelize writes only where ownership and integration are explicit.
5. Treat prompts, skills, hooks, MCP servers, and workflow kits as code: measure whether they help, and delete them when they do not.

Several premises in the brief have aged. By September 2026, Claude Code and Codex both support persistent and resumable chats, compaction, branching/forking, background work, worktrees, subagents, and movement between surfaces. The old contrast—“Claude users reset; Codex users keep one thread”—is no longer a reliable mechanical distinction. Current vendor guidance and the sampled practitioner workflows best support a hybrid: retain a coherent thread while the problem remains coherent; start a fresh context at a semantic boundary or after accumulated failed approaches; carry the result through Git, executable checks, and a small written handoff.

Two findings deserve special emphasis. First, the current `AGENTS.md` study found no statistically significant general task-success gain over no context file; generated files raised cost by more than 20% and added steps, and the study did **not** establish an optimal file length. Second, “overnight” work is not one eight-hour inference. A harness repeatedly calls a model, executes tools, evaluates progress, and either continues the same logical chat or starts a fresh process with state recovered from the repository.

## Evidence policy

“Documented fact” below means a current product mechanism, primary engineering report, paper, or directly inspectable implementation. Product documentation was checked on 2026-09-02. “Community practice” means practitioner reports, repositories, issue discussions, and public workflows. Those sources are useful for mechanisms and failure reports, but they are not representative surveys. “Inference” is my synthesis.

Confidence means confidence in the answer, not confidence that the practice is universal:

- **High:** directly documented mechanics or a conclusion supported by several independent primary sources.
- **Medium:** a repeated but still anecdotal field pattern, or a synthesis with important sampling limits.
- **Low:** sparse reports or a prevalence claim for which no trustworthy population evidence exists.

I found no defensible market-share survey of surfaces, no telemetry ranking slash-command use, and no survey telling us whether most overnight runs use one logical session or repeated fresh sessions. I say so where those gaps matter.

## Part 1 — surfaces

### 1. Claude Code: CLI versus desktop application

**Confidence: High on current mechanics; medium on the division of labour; low on prevalence.**

**Documented fact.** As of 2026-09-02, this is not a choice between two different agents. Anthropic says the CLI and desktop application use the same Claude Code engine. Local sessions share project instructions and much local configuration, while session histories remain separate and cloud/SSH environments can have different configuration sources. The CLI exposes terminal-native work, pipes and scripting, `--print`, remote shells, and explicit worktree control. Desktop foregrounds several visible sessions, panes, visual diff review, previews, browser/computer use, cloud and SSH sessions, side chats, and cross-session supervision; its automatic per-session worktree isolation applies to Git repositories. `/desktop` can transfer a CLI session on supported macOS and x64 Windows installations using a Claude subscription; it is unavailable with API-key authentication and the listed third-party providers. [Claude Code Desktop](https://code.claude.com/docs/en/desktop)

**Community practice.** I found three real camps, not a winner. Terminal-first developers value shell composition, `tmux`, SSH, exact control of the local environment, and a close read-run-edit loop. Desktop-first developers value readable history, discoverable sessions, visual review, automatic isolation, and the ability to supervise parallel or background work. The hybrid camp uses the CLI for intimate repository or infrastructure work and Desktop as a control plane for several agents, previews, or UI-heavy verification. Current discussion samples contain all three positions; they are self-selected reports, not adoption data. [ClaudeAI discussion](https://www.reddit.com/r/ClaudeAI/comments/1v0mnwx/should_i_be_using_claude_code_desktop_app_instead/), [ClaudeCode discussion](https://www.reddit.com/r/ClaudeCode/comments/1ryq4t7/terminal_vs_desktop_app_whats_the_difference/)

**Inference.** The best-supported answer is division of labour. Experienced users do have preferences, but the surface increasingly follows the job: CLI for composable, closely steered, remote, or automation-heavy work; Desktop for portfolio supervision, isolation, visual review, and browser/preview work. Early claims that Desktop lacked worktrees, remote access, or serious multi-session support are already stale.

### 2. Codex: CLI, IDE extension, desktop, and cloud

**Confidence: High on mechanics; medium on the division of labour; low on prevalence.**

**Documented fact.** The surfaces make different loops salient:

| Surface | Default shape of work |
|---|---|
| CLI | One focused local terminal loop, installed repository tools, shell composition, `codex exec`, and CI automation. [CLI documentation](https://learn.chatgpt.com/docs/codex/cli) |
| IDE extension | File- and selection-aware iteration, inline diffs, tight manual review, and delegation of longer work to cloud. [IDE documentation](https://learn.chatgpt.com/docs/codex/ide) |
| Desktop Codex view | Parallel projects and worktrees, long-running tasks, visual review, computer use, schedules, and cloud supervision. [Desktop documentation](https://learn.chatgpt.com/docs/app) |
| Cloud | Reproducible isolated environments, asynchronous or parallel jobs, and PR-oriented handback. [Cloud documentation](https://learn.chatgpt.com/docs/cloud) |

Movement is deliberate product behavior, not a workaround. On supported macOS and Windows installations, `/app` opens the exact saved CLI chat in Desktop. `codex cloud` submits and lists cloud work, while `codex apply` applies a cloud diff locally. IDE work can be delegated to cloud; host-to-host handoff carries chat and Git state while creating or reusing a worktree. [Codex developer commands](https://learn.chatgpt.com/docs/developer-commands?surface=cli), [remote connections](https://learn.chatgpt.com/docs/remote-connections)

**Community practice.** Current discussion samples show stable CLI, IDE, Desktop, and mixed camps. The recurring split is CLI for remote, devcontainer, or composable local work; IDE for a tight edit-review loop; Desktop for a wide loop supervising threads and worktrees; cloud for work that should outlive the local process or run in a reproducible environment. [April 2026 discussion](https://www.reddit.com/r/codex/comments/1sc45kf/codex_app_vs_cli_whats_your_real_workflow/), [July 2026 discussion](https://www.reddit.com/r/codex/comments/1uvkndu/are_you_using_codex_cli_or_desktop_and_why/)

**Inference.** Many experienced users move between surfaces because the joints are first-class, but plenty remain single-surface. No published telemetry supports ranking those populations.

### 3. Does the surface change the shape of the work?

**Confidence: High on the changed affordances; medium-high on their behavioral effect.**

**Documented fact plus inference.** Yes, especially beyond a small patch. The surface changes four structural properties:

- **Context aperture:** an IDE selection and open files, a terminal checkout, or project-level sources and memory.
- **Execution topology:** one checkout, automatic worktrees, or isolated cloud environments.
- **Time structure:** synchronous steering versus background delegation and later review.
- **Human role:** pair programmer inspecting each change versus manager of a queue of agents and artifacts.

This is a gradient, not a capability wall. CLI users can create worktrees and submit cloud tasks; Desktop includes a terminal; the same underlying agent can edit and test in several surfaces. But defaults affect decomposition. An IDE encourages a bounded edit with immediate inspection. A terminal encourages a command-and-evidence loop. Desktop encourages concurrent workstreams. Cloud encourages a queued branch or pull request whose main human interaction is acceptance. Calling the difference “only ergonomics” misses the changed concurrency, feedback latency, authority, and integration boundary.

## Part 2 — the session routine

### 4. One agent for the whole job, or document handoffs?

**Confidence: High on vendor guidance; medium that the hybrid is field convergence.**

**Documented fact.** Current guidance converges on **one coherent outcome or workstream per main session**, not one agent for an indefinitely large project. Anthropic’s basic loop keeps explore → plan → implement → verify in one session. For a large feature it recommends producing a self-contained specification, then starting a fresh implementation session; research subagents keep noisy exploration outside the main context. [Claude Code best practices](https://code.claude.com/docs/en/best-practices) OpenAI’s Project guidance recommends a separate chat for each distinct outcome while project files and instructions carry common context; the CLI provides `/new` and `/resume`. [Codex Projects](https://learn.chatgpt.com/docs/projects)

**Community practice.** A small, well-specified change is commonly explored, edited, tested, and reviewed in one thread. Large, ambiguous, or parallelizable work is split into discovery, specification, implementation, and independent review—sometimes as top-level sessions, sometimes as subagents. Code, Git, tests, a plan, and short status notes form the joint. Boris Cherny has described several local and web Claude sessions in separate checkouts and abandoning weak attempts; Karel D’Oosterlinck describes a lead agent coordinating workers while occasionally addressing a crucial worker directly. Those are prominent individual workflows, not representative samples. [Cherny workflow report](https://www.infoq.com/news/2026/01/claude-code-creator-workflow/), [D’Oosterlinck workflow](https://www.linkedin.com/pulse/i-spent-10000-automate-my-research-openai-codex-karel-d-oosterlinck-ltykc)

**Inference.** The practical unit is an independently verifiable outcome. Keep a thread while its accumulated history helps that outcome. Split when a subproblem has independent inputs and acceptance criteria, when exploration would pollute the main context, or when fresh eyes are itself the point. Writing a formal handoff for every trivial step is overhead; relying on one transcript for a multi-day project is fragility.

### 5. Strong planning, cheap execution, strong review

**Confidence: High that the pattern and mechanisms exist; medium on when it helps; low on comparative prevalence or savings.**

**Documented fact.** Both harnesses can implement the pattern. Claude’s `opusplan` explicitly uses Opus in plan mode and Sonnet for execution. Claude and Codex support named subagents pinned to different models; Codex can configure a separate review model. [Claude model configuration](https://code.claude.com/docs/en/model-config), [Claude subagents](https://code.claude.com/docs/en/sub-agents), [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)

**Community practice.** Some developers manually switch models; some encode the routing in agents or an orchestrator. [`Jogan/soluna-workflow`](https://github.com/Jogan/soluna-workflow) is a concrete, explicitly opinionated example of stronger planning/root/review with cheaper implementation and file-based handoffs. The counter-camp is real: Cherny reported preferring the strongest model for coding because reliability and reduced steering outweighed the price. Armin Ronacher has likewise favored a cheaper capable model throughout some workflows rather than treating the largest model as mandatory. [Ronacher’s agentic coding workflow](https://lucumr.pocoo.org/2025/6/12/agentic-coding/)

**Inference.** Tiering works best when execution is genuinely bounded: named files and interfaces, explicit exclusions, and cheap acceptance tests. Handoffs can be automatic within a parent/subagent harness or manual across top-level sessions and vendors. They fail when the planner’s summary loses rationale, the task remains ambiguous, workers overlap, or the final reviewer merely reads prose instead of rerunning evidence. I found no controlled field study showing that this three-tier pattern is cheaper or more reliable end to end.

### 6. What ends a session?

**Confidence: High on mechanisms; medium on which cause dominates in practice.**

**Documented fact and community practice.** The main boundary is semantic, not clock time:

1. the verified outcome is complete;
2. the next work is a distinct outcome or scope;
3. repeated corrections or failed approaches have polluted the thread;
4. context pressure or lossy compaction makes continuation unattractive;
5. a parallel attempt is deliberately abandoned;
6. a permission, usage, runtime, budget, or human stop intervenes.

Anthropic says to clear between unrelated tasks and suggests a clean session after more than two failed correction cycles on the same issue. For Pro/Max sessions that are both inactive for roughly an hour and over 100,000 tokens, resumption may offer a compacted summary instead of full history. [Claude Code best practices](https://code.claude.com/docs/en/best-practices), [Claude sessions](https://code.claude.com/docs/en/sessions) Codex goals and saved chats can span sittings, so “end of the workday” need not end the logical session.

**Inference.** Mature practice scopes the intended stop before context exhaustion. Exhaustion is a cleanup trigger or a sign the unit was too large, not the ideal definition of completion. There is no public usage dataset showing which stop cause is most common.

### 7. What carries over when work continues?

**Confidence: High.**

**Documented fact.** Carryover has a reliability hierarchy:

1. **Repository ground truth:** code, the Git tree and commits, tests, diffs, and pull requests.
2. **Durable task artifacts:** issue or specification, plan/checklist, decision record, status/handoff note, exact verification output.
3. **Standing context:** `CLAUDE.md` or `AGENTS.md`, scoped rules, skills, hooks, configuration, and selected memory.
4. **Conversation state:** a full resumed, forked, or branched transcript—or a necessarily lossy compacted summary.

Claude resume restores full history and tool results plus much session configuration, active goal, and eligible scheduled tasks; `/branch` clones the transcript and `/compact` replaces earlier context with a summary. [Claude sessions](https://code.claude.com/docs/en/sessions) Codex `/resume`, `/fork`, `/compact`, Projects, memories, and `AGENTS.md` cover parallel layers. [Codex Projects](https://learn.chatgpt.com/docs/projects), [Codex memories](https://learn.chatgpt.com/docs/customization/memories), [Codex `AGENTS.md`](https://learn.chatgpt.com/docs/agent-configuration/agents-md)

**Inference.** Tacit rationale, rejected alternatives, exact intermediate evidence, and unstated taste do not magically cross a fresh boundary. The best handoff is not a transcript dump; it is reproducible repository state plus a short account of intent, decisions, open risks, and the exact commands that establish the current truth.

## Part 3 — long threads and the two doctrines

### 8. Reset often versus stay and compact

**Confidence: High on current mechanics and the hybrid; low on community prevalence.**

**False-premise correction.** I cannot support “Claude users reset; Codex users stay” as a current population claim. There is no representative cross-community survey.

**Documented fact.** Claude’s guidance does teach aggressive context hygiene: clear unrelated work, restart after repeated miscorrection, and use a specification followed by a clean implementation session for a large feature. But Claude also has saved/named sessions, full resume, `/compact`, `/branch`, persistent goals, and cross-surface transfer. Codex explicitly recommends a new chat for each distinct outcome inside a Project, while `/resume`, `/compact`, `/fork`, `/side`, and `/goal` support continuity for one unfinished outcome. [Claude best practices](https://code.claude.com/docs/en/best-practices), [Claude sessions](https://code.claude.com/docs/en/sessions), [Codex Projects](https://learn.chatgpt.com/docs/projects)

**Community practice.** Claude’s published guidance and the visible Ralph tradition are more reset-oriented. Codex has a visible long-thread camp that values preserving “the same eyes” and files issues when compaction or deep resumption loses dependencies. Issue traffic proves the concern exists, not how common either camp is. [Codex compaction issue](https://github.com/openai/codex/issues/10823), [Codex resume issue](https://github.com/openai/codex/issues/24366)

**Inference.** The best-supported convergence is: resume or compact within one unfinished workstream; reset at an outcome boundary or after polluted reasoning; externalize anything a successor must know. Neither doctrine alone fits the current mechanics or sampled practice.

### 9. Is the historical split mechanical or cultural?

**Confidence: High on the mechanical comparison; medium-high on the cultural argument.**

**Argument.** It was both, but by September 2026 it is more cultural and default-driven than mechanically necessary. Both harnesses now provide fresh starts, saved resume, compaction, transcript branching, worktrees, standing instructions, memory, subagents, background execution, and multi-surface operation. That rules out a hard capability split.

There is still workflow gravity. Claude’s surfaces keep separate histories and `/desktop` transfers a CLI session; Codex `/app` opens the exact saved chat in Desktop. Codex Projects make common sources across separate chats explicit, and host-to-host handoff carries chat with Git state; current remote-connection documentation explicitly does not support handoff into Codex cloud. Claude’s best-practices page more forcefully teaches clearing and clean restart. Codex Desktop foregrounds persistent goals, parallel boards, worktrees, and cross-surface movement. Those affordances and teaching materials shape habits even when the underlying capability sets converge.

**Inference.** The older cultures arose from real differences in UX, context behavior, and product timing. Treating them now as immutable philosophies confuses historical path dependence with current necessity.

### 10. What does fresh lose, and what does continuation lose?

**Confidence: High on the trade-offs; medium on how consistently the hybrid is implemented.**

| Choice | Keeps or gains | Loses or pays |
|---|---|---|
| Fresh session | Clean attention; lower carried-token cost; less anchoring on failed paths; genuinely independent review; repeatable inputs | Chronology; tacit rationale; rejected alternatives; tool output; attachments; active goals and workers unless externalized |
| In-thread continuation | Chronology; prior corrections; unstated nuance; exact evidence; warm environment and task state | Context dilution; recurring token cost; anchoring; stale assumptions; accumulated tool noise; information flattened or omitted by compaction |

**Documented fact and community practice.** Both vendors now offer the building blocks for keeping the benefits of each: branch/fork the original, open a side chat or research subagent, put shared rules outside the transcript, and use Git, tests, a specification, and a concise handoff as durable truth. Anthropic explicitly recommends a fresh-context writer/reviewer split; Codex supports side chats and forks without destroying the parent.

**Inference.** The best current architecture is a persistent human-facing or lead workstream with clean, bounded worker/reviewer contexts. It preserves intent at the top while giving implementation and review fresh attention. Compaction should be treated as a useful lossy cache, never as the sole record.

### 11. How is a long Codex thread actually managed?

**Confidence: High on current commands; low on usage ranking.**

**Documented fact.** These are the concrete CLI affordances as of 2026-09-02. [Codex developer commands](https://learn.chatgpt.com/docs/developer-commands?surface=cli), [Codex CLI](https://learn.chatgpt.com/docs/codex/cli)

| Command or affordance | What it does |
|---|---|
| `/status` | Shows chat ID, context use, and rate limits; the basic continue-or-compact diagnostic. |
| `/compact` | Replaces earlier turns with a concise summary and frees context; it is lossy. |
| `/resume`; `codex resume [ID\|name]`, `--last`, `--all` | Reloads a saved chat rather than starting over. |
| `/rename` | Gives a saved chat a durable name. |
| `/new [name]` | Starts a fresh chat in the same CLI while leaving terminal output visible. |
| `/clear [name]` | Clears the display and starts a genuinely fresh chat; this differs from `Ctrl+L`. |
| `/fork`; `codex fork [ID]` | Copies a saved chat under a new ID and leaves the original unchanged. |
| `/side` | Opens an ephemeral fork for a tangent, then returns to the parent. |
| `/goal` | Sets, edits, pauses, resumes, or clears a persistent completion goal. |
| `/review` | Runs a review, optionally with a configured review model. |
| `/diff` | Shows the working diff; `/status` and `/diff` ground continuation in repository state. |
| `/app` | Opens the exact saved CLI chat in the desktop Codex view on supported macOS/Windows installations. |
| `/cloud`, `/local`, `/worktree` | Delegate or move work across cloud, host checkout, and isolated worktree topologies. |
| `/agent` or `/subagents` | Inspect or switch among agent threads. |

**Community practice.** There is no command telemetry, so I cannot honestly say which experienced users use most. `/status`, `/compact`, `/resume`, `/new` or `/clear`, `/fork`, and `/side` form the documented continuity set; issue traffic shows that compact/resume matter, not their rank.

**Inference.** There is no base CLI command literally named “handoff.” In-harness movement is explicit through `/app`, cloud/local/worktree, and remote-host handoff. Cross-vendor handoff is now also first-class in OpenAI’s official Claude Code plugin: `/codex:transfer` creates a persistent Codex thread from the Claude conversation and returns a `codex resume` command. A `HANDOFF.md` or status file remains a practitioner convention, not a built-in semantic operation. [Official Codex plugin for Claude Code](https://github.com/openai/codex-plugin-cc)

## Part 4 — the durable files

### 12. How long should an always-loaded instruction file be?

**Confidence: High that no evidence-backed optimum exists; high on the cited measurements.**

**Documented fact.** There are real numbers in circulation, but they are not equivalent:

- Anthropic currently advises keeping each `CLAUDE.md` concise and targets **under about 200 lines**. That is a product heuristic about adherence and maintenance, not a published optimum from a controlled length experiment. [Claude Code memory](https://code.claude.com/docs/en/memory)
- Codex’s default **32 KiB** combined limit for the project-directory `AGENTS.md` chain is an ingestion cap. It does not apply to the separate user/global file and is not a recommendation to fill 32 KiB. [Codex `AGENTS.md`](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- A descriptive study of 2,303 repository instruction files reported median lengths around 336 words for `AGENTS.md`, 485 for `CLAUDE.md`, and 535 for GitHub Copilot instruction files. Those are observed medians, not success thresholds. [*Agent READMEs: An Empirical Study of Context Files for Agentic Coding*](https://arxiv.org/abs/2511.12884)

The strongest measurement I found is the June 2026 revision of *Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?* It evaluated **438 unique tasks**—300 from SWE-bench and 138 from CTXBench—across four harness/model pairs. Developer-written files averaged roughly 641 words, with a wide 24–2,003-word range. The study found no significant general task-success improvement over no context file. Generated files raised cost by about 20% on SWE-bench and 23% on CTXBench and added an average 2.45 and 3.92 agent steps, respectively. Developer-written files were better than generated ones, but their roughly 2.4-point gain over no file was not statistically significant. On CTXBench, an observational binned analysis found no clear relationship between word count and success or cost. That is not the same as a randomized length intervention, so it cannot tell us an optimum. [Gloaguen et al., current preprint](https://arxiv.org/abs/2602.11988)

**Community practice.** “Keep it under 100 lines,” “under 200 lines,” and similar budgets are widely repeated. They are useful forcing functions, but I found no benchmark validating a universal count.

**Inference.** The right budget is the smallest always-loaded spine that changes behavior on most tasks. Move rare, path-specific, procedural, or reference-heavy material behind a trigger. Measure acceptance and repeated mistakes, not compliance with a folklore line count.

### 13. What actually fails when the instruction file is long?

**Confidence: High on the observed behavioral and cost effects; low-to-medium on the proposed causal mechanisms.**

**Documented fact.** The measured failure is not simply “the model cannot read it.” In the AGENTS.md study, agents often followed extra instructions: they took more steps, invoked more tools, and spent more, without a corresponding general success gain. In a narrower ablation—GPT-5.2 using generated files—removing test-oriented instructions significantly reduced cost on both benchmarks without a significant accuracy change. Repository overviews also did not reliably make agents find the relevant files sooner. The authors argue that observed cost growth is better explained by instruction-induced reasoning and tool use than by raw word count. [Gloaguen et al.](https://arxiv.org/abs/2602.11988)

**Inference, informed by that study and adjacent long-context work.** Several mechanisms can stack:

1. **Recurring context load.** Always-loaded text consumes context and may add input or cache cost on every eligible turn, although host caching changes the direct billing effect.
2. **Instruction competition.** Numerous, overlapping, stale, or conflicting rules make selection harder; lower-value rules can steal attention from the task and critical constraints.
3. **Behavioral overcompliance.** The agent performs requested rituals—extra searches, tests, summaries, or formatting—whose cost exceeds their contribution on the current task.
4. **Poor locality.** A global rule about one directory or workflow reaches unrelated work; the agent must decide whether it applies.
5. **Truncation or dilution.** Hosts cap discovered instruction bytes, and long context has well-established position and retrieval sensitivity. A loaded token is not the same as a salient token.
6. **Maintenance drift.** Large files accumulate obsolete commands and exceptions, producing internally inconsistent ground truth.

Adjacent long-context research demonstrates middle-position and ordering sensitivity, although it is not a coding-instruction-file experiment. [*Lost in the Middle*](https://arxiv.org/abs/2307.03172)

The study directly supports extra compliant activity without a general success gain. It does **not** establish that file length itself causes instruction competition, poor locality, truncation, or drift; those are plausible mechanisms and engineering risks, not measured causal conclusions.

**Inference.** The characteristic symptom—more obedient activity with no better result—can come from spending reasoning and tool budget on globally present but locally low-value policy. The remedy is not merely tighter prose; it is narrower scope, stronger triggers, deterministic enforcement for hard rules, and deletion of redundant instructions.

### 14. Always-loaded spine plus on-demand parts

**Confidence: High.**

**Documented fact.** This is an established pattern, usually called **progressive disclosure** or **scoped instructions**:

- Keep a short repository spine in `AGENTS.md` or `CLAUDE.md`: purpose, non-obvious commands, invariants, and pointers.
- Put directory-specific rules in nested instruction files or path/glob-scoped rules. Claude discovers nested `CLAUDE.md` files when it reads files in that subtree, and path-scoped rules activate on matching files. Codex is different: at startup it loads the `AGENTS.md` chain from the repository root to the launch working directory; merely editing a deeper file does not dynamically load that directory’s file. Launching Codex with that subdirectory as its working directory brings the deeper rule into the chain.
- Put procedural workflows in an Agent Skill. The skill’s small metadata entry is discoverable; the full `SKILL.md` is loaded when the agent selects it semantically or the user invokes it explicitly; bundled references, templates, or scripts are opened only when needed. [Agent Skills specification](https://agentskills.io/specification), [Claude Code skills](https://code.claude.com/docs/en/skills), [Codex skills](https://learn.chatgpt.com/docs/build-skills)
- Put large factual references in ordinary repository documents and link to them. The task or skill instructs the agent when to read them.

Claude’s `@file` imports are useful composition, but they load imported content with the instruction file; they are not on-demand retrieval. Codex loads a separate user/global file and then the project-directory chain to its current working directory; the default 32 KiB budget applies to that project chain. Claude has user, project, local, nested, and path-scoped layers. [Claude memory](https://code.claude.com/docs/en/memory), [Codex instruction discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md)

**Community practice.** The common migration is from one giant file to: a terse root map, local directory rules, a small set of explicitly useful skills, and ordinary docs. Trigger quality matters. A skill whose description is vague may never load; one whose description is too broad loads constantly and recreates the original tax.

**Inference.** Progressive disclosure works when the routing metadata is precise and the hidden material has a clear consumer. Merely splitting one bloated file into ten files that are all imported at startup changes maintenance, not context economics.

### 15. Writing style, order, and critical-rule placement

**Confidence: High that style advice is mostly heuristic; medium on the best synthesis.**

**Documented fact.** Vendor guidance converges on concise, concrete, verifiable instructions; short sections and bullets; explicit commands; links instead of copied reference material; and removal of contradictions or guidance the model already follows. The 2,303-file descriptive study found shallow Markdown structures, typically one top heading, several second-level headings, and a mix of prose and lists. It did not measure which style caused better task performance. [Agent README study](https://arxiv.org/abs/2511.12884)

**Community practice.** Practitioners tend to use:

- bullets or declarative lines for operational rules and commands;
- prose for rationale, architecture, and trade-offs that require judgment;
- critical constraints near the smallest scope where they always apply;
- a short root summary with links to detail;
- examples or executable checks when wording alone is ambiguous.

Some put “must” rules first or repeat them at the end, but I found no coding-agent experiment demonstrating a reliable primacy/recency layout rule. General long-context research should not be laundered into a precise repository-file recipe.

**Inference.** Write for decision value, not incantation. “Use `pnpm test --filter api` before claiming completion” is better than “ensure high quality.” If a rule is truly critical, placement is a weak control: encode it in CI, a hook, permissions, types, or the repository structure.

### 16. Can a plan section be marked closed in a way the agent respects?

**Confidence: High that Markdown alone is advisory; medium-high on the working controls.**

**Documented fact.** A heading such as “DONE,” a checked box, or a prose instruction can guide the model, but it does not create immutable state. Current examples add structured state and recorded evidence; the strongest also add a completion gate:

- OpenAI’s workflow recipe uses explicit phase states such as Not started, In progress, Blocked, and Complete, together with recorded verification evidence. [Iterating development workflows with Codex](https://developers.openai.com/cookbook/examples/codex/iterating-development-workflows-with-codex)
- Anthropic’s long-running harness instructed agents to change only a structured feature list’s `passes` field from false to true after end-to-end verification, alongside a progress file and Git history. That transition was model-enacted discipline, not a cryptographically enforced verifier. [Anthropic long-running-agent harness](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- Claude Code Agent Teams can use a `TaskCompleted` hook whose exit code 2 blocks completion until required checks pass. [Claude hooks](https://code.claude.com/docs/en/hooks)

**Community practice.** Checkboxes work for a cooperative single writer. For unattended or multi-agent work, teams prefer machine-readable status, evidence links, commits, and a coordinator that owns transitions. JSON is sometimes chosen because it makes accidental prose rewrites less likely, not because JSON is intrinsically trustworthy.

**Inference.** Section-closing is solved only conditionally: **state + evidence + a gate**. No Markdown marker has a special closed-world semantic. If reopening is dangerous, protect the artifact with ownership or a hook and make the acceptance condition executable.

### 17. Immutable plan and volatile working state in separate files

**Confidence: High that the pattern exists; medium on whether strict immutability holds.**

**Documented fact.** Yes, several first-party and named workflows separate stable intent from changing state:

- OpenAI’s 25-hour Codex experiment used a stable `Prompt.md` contract, a milestone-oriented `Plan.md`, and a more volatile `Documentation.md`, with Git, worktrees, and generated outputs as additional state. [OpenAI long-horizon report](https://developers.openai.com/blog/run-long-horizon-tasks-with-codex)
- Anthropic’s long-running harness separated a narrative progress file from a structured feature list and Git history. The list itself co-located stable descriptions and steps with the mutable `passes` field, so this is logical intent/state separation, not an immutable-plan implementation. [Anthropic harness](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- Ralph variants commonly distinguish a PRD or structured backlog from `progress.txt` state, but some explicitly let the agent update both. They support separate roles, not necessarily a frozen plan. [Matt Pocock’s Ralph guide](https://www.aihero.dev/getting-started-with-ralph)

There is an important counter-pattern. OpenAI’s ExecPlan is explicitly a **living document**: progress, discoveries, decisions, and outcomes are updated as reality changes. [Codex ExecPlans](https://developers.openai.com/cookbook/articles/codex_exec_plans)

**Community practice.** The separation holds best for the objective, constraints, acceptance criteria, and non-negotiable interfaces. Detailed implementation sequencing often changes after repository exploration, so teams either amend the plan through a deliberate decision record or use a living plan rather than pretending it is immutable.

**Inference.** The robust distinction is not frozen file versus writable file. It is **stable contract versus observed state**. Freeze what would require human authorization to change; let discoveries, blockers, completed steps, evidence, and next action evolve. A plan that cannot record a disproven assumption becomes a source of error.

### 18. Several agents and a human appending to one shared log

**Confidence: High that uncoordinated shared writing is unreliable; low on how often teams nevertheless use it.**

**Documented fact.** Append-only logs work for one serialized writer or a system with real locking and event semantics. Raw concurrent agent editing of one Markdown file does not provide that. Anthropic’s agent-team guidance warns about same-file overwrites and uses a task store plus per-agent mailboxes rather than treating one prose file as a safe bus. Its parallel C-compiler experiment used separate clones, lock files, and Git and still found conflicts to be a major coordination cost. [Claude agent teams](https://code.claude.com/docs/en/agent-teams), [Anthropic C compiler report](https://www.anthropic.com/engineering/building-c-compiler)

Thoughtworks’ “accidental blackboard” describes a repository-mediated multi-agent workflow coordinated through plans, commits, rebases, and CI. Frequent commits and pushes overloaded CI; backing off then weakened the continuous update flow. It is not evidence that several models safely append arbitrary prose to one file. [An Accidental Blackboard](https://martinfowler.com/articles/exploring-gen-ai/an-accidental-blackboard.html)

**Community practice.** Sequential append appears in Ralph-style single-agent loops. In the multi-agent reports I found, workers instead wrote separate results or commits for a coordinator to merge, or the system used a locked task store, database, queue, per-writer journal, or mailbox. I found no usage telemetry for either design.

**Inference.** Even if an OS gives atomic append for individual byte writes, agent tools often patch or rewrite a whole file; network filesystems complicate atomicity further. And byte safety would not solve semantic races: duplicate tasks, out-of-order facts, contradictory conclusions, stale summaries, and no agreed owner of “current truth.” A shared log can be an audit trail. It is a poor coordination database unless writes are serialized and state transitions are explicit.

## Part 5 — unattended running

### 19. What is mechanically running for hours or overnight?

**Confidence: High on the mechanisms; medium on their prevalence.**

**Documented fact.** “An agent ran overnight” can describe at least four different systems:

1. A persistent harness process runs many model/tool turns. Current Claude Code `/goal`, for example, keeps a goal attached to a session and uses an evaluator after turns to decide whether to continue. It can stop when that evaluator judges success, impossibility, or an unrecoverable error; on cancellation; or on an evaluator-interpreted time/turn clause in the goal. Those natural-language clauses are not hard counters, and a no-tool progress stall can stop iteration while leaving the goal active; an outer wrapper is still needed for a hard timeout or iteration cap. [Claude Code goals](https://code.claude.com/docs/en/goal) Codex likewise supports long-running local, remote, cloud, and scheduled chats.
2. An outer shell or workflow repeatedly starts a fresh non-interactive agent process. Geoffrey Huntley’s original Ralph loop was literally an infinite Bash loop piping `PROMPT.md` into `claude-code`; each invocation returned before the shell launched the next one. [Huntley’s original description](https://ghuntley.com/ralph/)
3. A cloud or background supervisor owns the process. The terminal can close while the hosted task, VM, `tmux` session, desktop background host, CI job, or workflow runner remains alive.
4. A lead session coordinates shorter workers or subagents. The lead keeps task state; workers get fresh contexts and return summaries, patches, or commits.

The state is layered. A live session may retain a transcript, tool results, goals, and a compacted summary. Durable state lives in the working tree, Git commits, tests, specifications, task/status files, and harness records. OpenAI’s published 25-hour Codex experiment explicitly relied on repository files, docs, worktrees, and generated outputs as external state; Anthropic’s long-running-agent harness used a progress file, a JSON feature list, an initialization script, and Git history. [OpenAI long-horizon report](https://developers.openai.com/blog/run-long-horizon-tasks-with-codex), [Anthropic long-running-agent harness](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

**Community practice.** Ralph-style loops, `tmux`/VM runs, hosted cloud tasks, and persistent interactive sessions all exist in real reports. RepoMirror, for example, ran a `claude -p` loop in `tmux` on cloud VMs and left it overnight. [RepoMirror report](https://github.com/repomirrorhq/repomirror/blob/main/repomirror.md)

**Inference.** The outer harness, not the model, supplies persistence and the stop policy. Possible stops include a completion evaluator or sentinel, max iterations/time/cost, a command failure, a pending permission or question, loss of service/credits, manual cancellation, or machine shutdown. An infinite loop without a wrapper has no intrinsic notion of “done.”

### 20. Is an overnight run one long session or many short ones?

**Confidence: High that both forms are real; low on which is more common.**

**Documented fact.** Both are directly evidenced. OpenAI’s 25-hour experiment was one long **logical** Codex job, although it repeatedly planned, edited, tested, observed, repaired, and externalized state; that does not imply one unchanged model context. Huntley’s Ralph and RepoMirror’s implementation launched many fresh processes joined by files, tests, and Git. Anthropic’s long-running harness also treats large work as discrete sessions that rehydrate from durable state. Cursor has described planner/worker cycles that end with a judge and begin the next iteration fresh. [Cursor’s scaling experiment](https://cursor.com/blog/scaling-agents)

**Community practice.** The hybrid is increasingly visible: a persistent human-facing or lead thread, fresh research/implementation workers, automatic compaction inside long chats, and repository state across all of them.

**Inference.** “One long session versus many short sessions” is the wrong binary. The useful questions are: where is authoritative state, how often is attention reset, and what independently checks completion? I found no trustworthy prevalence survey.

### 21. What class of task is safe unattended?

**Confidence: High on the controls; medium-high on the task classification.**

**Documented fact.** Verification is central but insufficient. A relatively safe unattended job combines a narrow outcome; fast automated feedback; an isolated branch, worktree, container, or disposable runner; least privilege; bounded time/cost/iterations; observable logs; and a reviewable output such as a diff or pull request. OpenAI’s non-interactive guidance defaults toward restricted execution and shows designs that separate a read-capable model job producing a patch from a later credentialed job that opens a PR. Anthropic’s long-running work found that agents prematurely declared features done unless required to exercise them end to end. [Codex non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode), [Anthropic harness report](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

**Community practice.** Common low-blast-radius candidates include read-only audits, issue triage, release notes, test generation, lint/type fixes, documentation updates, bounded migrations, and isolated greenfield prototypes. Practitioners are much more cautious about production deploys, destructive data migrations, secrets or access-control changes, payments, external messages, ambiguous architecture decisions, and any task without a behavioral oracle.

**Inference.** The safety condition is:

> verifiable outcome + bounded blast radius + recoverability + least privilege + an explicit stop

A green test suite can test the wrong thing, omit important behavior, or be weakened by the agent. Other limits are prompt injection in untrusted repository content, secret exposure, shared services, environment flakiness, runaway cost, and decisions that require product judgment.

### 22. Place the Ralph-style shell loop precisely.

**Confidence: High.**

**Documented fact.** The lineage needs separating:

- Geoffrey Huntley named and described the original Ralph technique on 2025-07-14. Its pure form was `while :; do cat PROMPT.md | claude-code ; done`. It used a plan/specifications, tests, Git, and a brief agent file as backpressure and memory. **The original loop had no completion sentinel or iteration cap.** It stopped only through an external interruption or failure. [Original Ralph](https://ghuntley.com/ralph/)
- The exact form remembered in the brief—fresh non-interactive invocations, `PRD.md` plus `progress.txt`, an iteration bound, and a `<promise>COMPLETE</promise>` early exit—is well placed as Matt Pocock’s `afk-ralph.sh`. [Getting Started With Ralph](https://www.aihero.dev/getting-started-with-ralph)
- Anthropic later published a related state-transfer architecture using an initializer session, subsequent coding sessions, `claude-progress.txt`, a JSON feature list, `init.sh`, and Git. [Anthropic’s harness](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- Packaged variants such as [`snarktank/ralph`](https://github.com/snarktank/ralph) use `prd.json`, `progress.txt`, Git, a default iteration limit, and the completion sentinel. `ClaytonFarr/ralph-playbook` has bounded and unlimited plan/build modes. The similarly named `ghuntley/how-to-ralph-wiggum` repository is a fork of that playbook; it is not the source of Huntley’s original one-line loop.

**Inference.** The important mechanism is not the cute loop. It is forced re-orientation from a stable goal, a small next task, external state, executable backpressure, and a bound. Without the last three, Ralph is merely an infinite stochastic process.

### 23. Worktrees and parallel agents: where does scaling stop paying?

**Confidence: High on mechanics; medium on the 3–5 heuristic; low on any universal number.**

**Documented fact.** Git worktrees isolate working directories, indexes, HEADs, and usually branches while sharing the object database. They prevent agents from editing the same checkout; they do not prevent semantic conflicts at merge time, and they do not isolate ports, databases, caches, containers, queues, or external APIs. [Git worktree manual](https://git-scm.com/docs/git-worktree)

Claude and Codex both have harness support for worktree-isolated sessions. Anthropic’s current operational guidance suggests starting around 3–5 teammates and says three focused workers often beat five scattered ones; it also limits that advice to independent research, hypotheses, modules, or cleanly owned layers. [Claude agent-team guidance](https://code.claude.com/docs/en/agent-teams)

**Community practice.** Boris Cherny publicly described 3–5 worktrees as a major productivity pattern. Reports from individual developers commonly cluster around two to five concurrent streams, but the binding constraint is often the human reviewer rather than CPU or model capacity. These are anecdotes, not a distribution.

Cursor’s first-party scaling experiment is the useful counterexample. In a flat design, 20 agents sharing a file and lock degraded to the effective throughput of roughly 2–3 because of waiting, leaked locks, duplicate work, and task avoidance. A purpose-built planner/worker/judge hierarchy later ran hundreds of workers, but required enormous independent task pools, custom orchestration, automated integration, and trillions of tokens. [Cursor scaling agents](https://cursor.com/blog/scaling-agents)

**Inference.** Parallelism stops paying when the pool of independently executable, simultaneously ready tasks is exhausted. After that, dependencies, shared concepts/files, CI and merge queues, shared runtime resources, coordination, and review become the critical path. Worktrees solve checkout interference, not architectural coupling. Three to five is a useful human-supervised starting heuristic; two implementation streams may already saturate one reviewer; hundreds are an infrastructure project, not a worktree trick.

## Part 6 — over-preparation

### 24. Where is the line between useful preparation and process theatre?

**Confidence: High that proportional preparation is the convergence; medium-high on how widespread it is.**

**Documented fact.** Current Claude Code guidance offers the sharpest heuristic: if you could describe the diff in one sentence, skip the plan; plan when the approach is uncertain, the change spans files, or the code is unfamiliar. [Claude Code best practices](https://code.claude.com/docs/en/best-practices) Codex guidance similarly reserves planning for difficult or ambiguous work and recommends adding durable guidance only after a mistake repeats.

**Community practice.** Spec-driven kits have generated a visible backlash for small brownfield work. GitHub Spec Kit users have reported six-phase flows, dozens of touched files, and large generated artifacts for tiny code changes; defenders tend to say the same structure is useful for substantial, uncertain, or handed-off work. [Spec Kit issue 1174](https://github.com/github/spec-kit/issues/1174), [Spec Kit issue 2673](https://github.com/github/spec-kit/issues/2673), [Spec Kit discussion 1784](https://github.com/github/spec-kit/discussions/1784)

Armin Ronacher’s simpler rule is based on repetition: automate only work already performed several times, then compare repeated results and ask whether he would accept them. He reports that clear ad-hoc instruction often beats elaborate prewritten prompts. [Agentic Coding Things That Didn’t Work](https://lucumr.pocoo.org/2025/7/30/things-that-didnt-work/)

**Inference.** Task topology, not line count, sets the threshold. Preparation earns its keep when it resolves a decision the implementation cannot safely improvise, becomes durable input for another person/session, or creates a falsifiable acceptance gate. It becomes theatre when the artifact has no downstream consumer and its production is mistaken for progress. There is no established “N files,” “N sessions,” or “N hours” threshold.

### 25. Do people abandon structures they built?

**Confidence: Medium-high that abandonment is repeatedly documented; low on prevalence; medium on the mix of causes.**

**Community practice.** Yes. The unusually useful reports are specific:

- Ronacher retired or stopped using `/fix-bug`, `/commit`, `/add-tests`, `/fix-nits`, and `/next-todo` commands because they did not outperform a direct request, did not match his style, were inconsistent, or never became habitual. He also narrowed hooks, print-mode scripts, and write-heavy subagents. [Ronacher’s failure report](https://lucumr.pocoo.org/2025/7/30/things-that-didnt-work/)
- Practitioners report shrinking full spec lifecycles into one small spec or native plan mode for well-understood changes.
- Large always-loaded files are moved into path-scoped rules, on-demand skills, or specialist agents when standing context cost becomes visible.
- Some practitioners dropped MCP integrations for ordinary CLI tools because of 2025 context costs. A 2026 Checkly comparison found that deferred loading and resource links had largely erased its earlier token gap, restored some MCP use, and recommended choosing by feature fit and host preference—retirement decisions can themselves expire. [Checkly MCP versus CLI](https://www.checklyhq.com/blog/mcp-vs-cli-token-efficiency/)
- Broad writing swarms are often narrowed to read-only investigation or cleanly owned modules because merge and review costs erase the apparent speedup.

**Inference.** What gets abandoned is usually not “structure” in the abstract. It is structure whose invocation cost, context tax, false activation, review burden, or maintenance exceeds the corrections it saves.

### 26. How is process retired?

**Confidence: Medium-high.**

**Documented fact.** Claude’s current guidance says to prune instructions that merely restate behavior the model already gets right and use deterministic enforcement for rules that truly must hold. Recent Claude Code versions also expanded `/doctor` to diagnose setup and redundant or disused configuration. Codex’s closest creation gate is to add durable guidance after the same mistake recurs and turn a workflow into a skill only when it is genuinely repeatable. [Codex best practices](https://developers.openai.com/codex/learn/best-practices)

**Community practice.** The best explicit retirement rule I found is Ronacher’s: if he automated recurring work and then stopped using the automation, it failed and he deletes it. His lightweight evaluation is three repetitions and a manual acceptance/variance check. Other practitioners audit standing tokens, actual invocation counts, duplicate rules, and configuration locality; delete anything reproducible with a one-line request; and compare a custom workflow against the now-current native feature.

**Inference.** There is no established cross-vendor lifecycle—no common owner, expiry date, last-used TTL, deprecation field, or scheduled retirement review. Process accumulates by default. A workable local policy is:

1. record the problem and a baseline;
2. test the custom mechanism on representative repeats;
3. keep it only if it improves acceptance rate, latency, cost, or risk;
4. record the native feature or model improvement that would obsolete it;
5. review unused or high-context mechanisms periodically.

## Part 7 — harness mechanics

### 27. Can a skill restrict or grant tools? Is its allowlist enforced?

**Confidence: High.**

The premise needs a host-specific answer; “Agent Skills” is a portable packaging convention, not one universal permission system.

**Documented fact — Claude Code, current 2026-09-02.** A skill’s `allowed-tools` is enforced as a **temporary pre-approval grant** for the invoking turn. It does not restrict the remaining tools: unlisted tools stay callable under the session’s ordinary permission policy, and the grant clears with the next user message. Claude Code also supports `disallowed-tools`, which removes named tools from the available pool for that turn. Skill instructions stay in context after the turn; those permission effects do not. A security-significant exception is that workspace trust does not gate a project skill’s `allowed-tools`, including `claude -p` or SDK runs in a never-trusted repository; Anthropic explicitly warns that a project skill can grant itself broad access. [Claude Code skills](https://code.claude.com/docs/en/skills), [Claude permissions](https://code.claude.com/docs/en/permissions)

**Documented fact — portable Agent Skills.** The open specification labels `allowed-tools` experimental and says implementation support varies. It means “pre-approved,” not a portable hard allowlist. [Agent Skills specification](https://agentskills.io/specification)

**Documented fact — Codex.** Current Codex skill documentation does not define a skill-body tool allowlist as a hard security boundary. Skills are instructions and resources. Tool availability and enforcement come from the hosting session, subagent configuration, permission profile/sandbox, command rules, administrator policy, and controls for MCP/browser/connectors.

**Inference.** Never use prose or portable `allowed-tools` as the sole security boundary. In Claude Code, use `disallowed-tools` or a restricted subagent for turn-local capability shaping and permission/sandbox policy for durable enforcement. In Codex, constrain the agent or runtime that loads the skill.

### 28. What reliably constrains tools, and how do the mechanisms compose?

**Confidence: High on each vendor; high that there is no cross-vendor universal order.**

**Documented fact — Claude Code.** Reliable controls are host-enforced permission rules, permission modes, subagent tool pools, hooks, sandboxing, managed settings, and scoped MCP configuration. Within Claude permission rules, precedence is **deny → ask → allow**; specificity does not overturn that order. A matching deny at any settings scope wins. PreToolUse hooks can block or force a prompt, but they cannot bypass matching deny/ask rules; OS-level sandbox boundaries cover subprocesses that tool-name rules cannot see. Managed policy is the highest configuration tier. Prompts and `CLAUDE.md` shape attempts but do not grant authority. [Claude permissions](https://code.claude.com/docs/en/permissions)

A Claude subagent’s `disallowedTools` is applied before its `tools` allowlist is resolved, so a tool in both is absent. [Claude subagents](https://code.claude.com/docs/en/sub-agents)

**Documented fact — Codex.** Current permission profiles, marked **Beta** and subject to change, create local filesystem and command-network boundaries. Within a profile, narrower deny rules survive broader read/write grants, and network deny wins over allow **when the Codex network proxy or an administrator-managed proxy is active**. If network access is enabled while that proxy is off, commands receive direct unrestricted network access and the profile’s domain rules are not enforced. Command rules governing execution outside the sandbox apply the most restrictive matching decision: `forbidden > prompt > allow`. Administrator requirements can further restrict what users select. Permission profiles do **not** compose with the older `sandbox_mode` settings; Codex uses one system or the other for a session. MCP servers, hosted web search, connectors, browser/computer use, and cloud tasks have separate controls and must be configured directly. [Codex permissions](https://learn.chatgpt.com/docs/permissions), [Codex command rules](https://learn.chatgpt.com/docs/agent-configuration/rules)

**Inference.** Think in layers, not one allowlist:

1. platform/administrator and OS sandbox boundaries;
2. session or agent tool pool;
3. permission decisions and hooks for attempted calls;
4. tool-specific service permissions;
5. behavioral instructions.

The last layer is useful steering, not enforcement.

### 29. Can an agent body branch on the model it is running as?

**Confidence: High that there is no documented reliable body-level conditional; medium on all private harnesses.**

**Documented fact.** Neither current Claude nor Codex agent Markdown defines a reliable `if model == …` language inside the instruction body. Claude subagent definitions and skills can select a model in frontmatter; a skill can also select an effort level for the current turn. Codex custom agent files and orchestrator spawn configuration can select `model` and `model_reasoning_effort`, with documented inheritance and precedence. [Claude subagent model selection](https://code.claude.com/docs/en/sub-agents), [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)

**Inference.** Asking the model to self-identify and then follow a prose branch is not a dependable policy mechanism: identifiers can be hidden, aliased, changed, or misreported, and enforcement still rests with the host. The working alternative is external dispatch—select a different agent/skill/profile or render different instructions before the turn based on the configured model. If behavior differs by capability, define `fast-scan` and `deep-review` roles and let the orchestrator bind each role to a model; do not put model introspection in the role’s prose.

### 30. Is competence escalation to a stronger model established?

**Confidence: High on current mechanics; medium-low on field prevalence.**

**Documented fact.** Claude now has an experimental first-party **advisor** mechanism, the closest native implementation I found. A faster main model may consult an advisor that is at least as capable; the advisor receives the full conversation, tool calls, and results. The main model decides when to consult it—for approach selection, recurring errors, or completion review—and `/advisor`, `--advisor`, and `advisorModel` configure it. This is model-driven escalation, not a deterministic “after N failures” rule. Availability is currently narrower than Claude Code overall: it requires the Anthropic API, compatible models, and feature-flag fetching and is unavailable through Bedrock, Google Cloud’s Agent Platform, Microsoft Foundry, and Claude Platform on AWS. [Claude Code advisor](https://code.claude.com/docs/en/advisor)

The other building blocks are established: both harnesses can assign different models or effort to workers and reviewers, use orchestrator/worker patterns, and run a separate evaluator. Claude’s `opusplan`, a pinned senior subagent, and a fresh strong-model review are explicit variants. Codex supports named strong reviewers and parent re-dispatch but documents no equivalent native advisor or competence-threshold router.

**Community practice.** The repeated pattern is a strong planner or lead, cheaper readers/workers for bounded tasks, and a strong independent reviewer for ambiguity or risk. Some teams instead use the strongest model throughout because reduced steering and rework can be cheaper overall. Aside from the new advisor, escalation is usually manual or orchestrator-policy driven: a worker returns `blocked`, `needs-decision`, failed verification, or unresolved alternatives; the lead assigns a higher-effort agent or asks the human. Field evidence for advisor adoption is still sparse because the feature is new.

**Inference.** Senior escalation is established; trustworthy automatic competence detection is not. A reliable policy escalates on observable evidence—repeated failed checks, conflicting evidence, security or data-loss risk, an architectural decision, or inability to produce a bounded plan—and passes the stronger reviewer the attempted approaches and verifier output. API/model fallback on transport failure is not competence escalation.

## Part 8 — prior art as a discipline

### 31. Is “does the harness already ship this?” an established pre-build practice?

**Confidence: Medium.**

**Documented fact.** The duplicate-building hazard is real because the products change extremely quickly. Current Claude Code ships capabilities such as `/doctor`, review, batch, debug, loop, run, verify, goals, workflows, hooks, and teams. Current Codex has plan/review/init, goals, forks/side chats, skills, subagents, worktrees, scheduled work, import, and an app server. Those lists were materially different only months earlier. [Claude Code skills and built-ins](https://code.claude.com/docs/en/skills), [Codex developer commands](https://learn.chatgpt.com/docs/developer-commands?surface=cli)

**Community practice.** Careful practitioners do check the installed command list, official docs/changelog, team skill library, plugins, and existing scripts before adding a new workflow. Concrete reports also show the opposite: people build context audits, custom commands, hooks, agent relays, and wrappers, then discover a native command or a new release covers most of it. The cross-agent `coding-agent-toolkit`, for example, explicitly records that its predecessor external subprocess relay was abandoned while the file/Git handoff conventions survived. [Toolkit background](https://github.com/stefan-jansen/coding-agent-toolkit)

**Inference.** This is a recognizable discipline, not an established mandatory gate. I found no evidence that most teams enforce it and cannot estimate adoption.

### 32. What does the check look like, and does it survive a deadline?

**Confidence: Medium on the useful shape; low-to-medium on deadline survival.**

**Community practice and inference.** The strongest lightweight preflight is:

1. Name the desired capability in one sentence.
2. Check the installed version’s `/help`, command menu, and feature status.
3. Search current official docs and changelog—not remembered 2025 advice.
4. Search the repository, user/team skills, installed plugins, hooks, MCP inventory, and issue tracker.
5. Run one representative native baseline.
6. Build only the missing delta and record what future native change should retire it.

I found no study of deadline behavior. Field reports of discovering overlap after building imply that a broad discretionary search often loses. A two-minute native-feature check survives when embedded in the creation template or review gate; “remember to research the ecosystem” does not. Under deadline, skip the landscape survey, not the installed-feature check.

## Part 9 — cross-vendor

### 33. Do real workflows cross vendors? What is the joint?

**Confidence: High that the pattern exists; medium on prevalence.**

**Documented fact.** Yes, and it is no longer only DIY. OpenAI maintains an official Codex plugin for Claude Code. Claude can ask Codex for a read-only or adversarial review, delegate a rescue task, run it in the background, inspect/cancel the job, and create a persistent Codex thread from the current Claude transcript with `/codex:transfer`; the plugin prints `codex resume <session-id>`. It uses the Codex app server and local Codex configuration. [Official Codex plugin for Claude Code](https://github.com/openai/codex-plugin-cc)

Codex itself can import supported Claude Code or Cursor instructions, settings, skills, plugins, projects, and recent chats; the desktop app can also import Claude Cowork. [Import from another agent](https://learn.chatgpt.com/docs/import)

**Community practice.** The simplest cross-vendor joint remains the repository: Git commits/branches/worktrees, a diff or PR, tests and logs, an issue/spec, and a short Markdown or JSON handoff. Other live joints are CLI subprocesses, MCP/app-server calls, plugins, and orchestration frameworks. A small pre-1.0 example, `coding-agent-toolkit`, uses canonical `AGENTS.md`, a one-line Claude import, `.workspace` state, and handoff files containing read-only commands plus expected outputs to detect drift. Its earlier outside-in subprocess orchestrator was retired because it lost useful host context. [coding-agent-toolkit](https://github.com/stefan-jansen/coding-agent-toolkit)

**Inference.** Cross-vendor review—one model writes, another with a fresh context challenges—is more mature than full bidirectional co-implementation. The most robust joint is evidence the second harness can independently verify, not prose claiming what the first one did.

### 34. Is there a portable instruction or handoff convention?

**Confidence: High on syntax support; medium-low on semantic portability.**

**Documented fact.** There are two partial standards:

- `AGENTS.md` is natively discovered by Codex and several other agents. Claude Code still natively reads `CLAUDE.md`, but its current docs recommend a one-line `@AGENTS.md` import or symlink when a repository uses the portable file. [Codex `AGENTS.md`](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [Claude memory and `AGENTS.md` import](https://code.claude.com/docs/en/memory)
- The Agent Skills specification standardizes a `SKILL.md` package and progressive loading. Frontmatter beyond the core is host-dependent; `allowed-tools` is explicitly experimental. [Agent Skills specification](https://agentskills.io/specification)

**Community practice.** Plain Markdown handoffs, Git/PR state, checklists, and small JSON task/progress files travel well because every harness can read them. There is no widely adopted cross-vendor handoff schema for decisions, rejected alternatives, confidence, verification evidence, dependencies, and authority.

**Inference.** Portability is stable at the file and Markdown syntax layer, less stable at discovery, precedence, activation, tool names, permissions, compaction, and lifecycle semantics. A portable handoff should therefore avoid harness commands and include: objective, immutable constraints, current commit/worktree, changes made, open decisions, failed approaches, exact verification commands/results, and the next safe action.

### 35. What survives switching among several projects?

**Confidence: High on the layers; medium on the best contents.**

**Documented fact.** Both ecosystems have a layer above the repository. Codex loads user-level `~/.codex/AGENTS.md`, configuration, skills, agents, rules, and connections before project-scoped equivalents. Claude has user-level `~/.claude/CLAUDE.md`, rules, skills, agents, settings, and optional memory, then project and nested instructions. Both systems give more local project guidance later/higher relevance. [Codex instruction discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [Claude memory scopes](https://code.claude.com/docs/en/memory)

**Community practice.** Experienced users keep operator preferences, preferred tools, general review discipline, safety posture, and genuinely cross-project skills in the user layer. Project architecture, commands, dependencies, decisions, current work, and exceptions stay in the repository. Global skill sprawl is a recurring cleanup target.

**Inference.** The global layer should describe the operator, not pretend to be a multi-project database. Volatile project state above the projects creates stale or conflicting truth. A project switch should rehydrate from that repository plus its issue/PR state; the global layer supplies stable working agreements and credentials/connections under separate permission controls.

## Part 10 — the honest close

### 36. What do experienced practitioners say they got wrong in the first six months?

**Confidence: Medium-high; this is a synthesis of repeated first-person reports, not a survey.**

The recurring admissions are strikingly consistent:

1. **Treating the agent as autocomplete or chat.** They under-delegated outcomes, then overcorrected into vague “build everything” prompts.
2. **Optimizing prompts before the environment.** They wrote large instruction files instead of making tests, builds, logs, and error messages fast and legible.
3. **Letting a thread outlive its scope.** Repeated corrections and stale approaches accumulated until a clean prompt would have been cheaper.
4. **Trusting self-reported completion.** They reviewed claims instead of requiring executable evidence and a diff.
5. **Parallelizing coupled writes.** More agents created merge conflicts, contradictory assumptions, shared-service collisions, and review debt.
6. **Automating before repetition.** They built commands, hooks, MCP plumbing, and process frameworks for tasks they had not yet learned to perform consistently.
7. **Confusing permission bypass with autonomy.** Broad credentials and production reach made a recoverable coding error into an operational risk.
8. **Letting process only accumulate.** Stale rules, skills, plugins, and generated specs taxed every later session.

Ronacher’s retrospective is the clearest primary account: most of his custom automations did not stick; write-heavy subagents created chaos; long sessions forgot early context; and automation encouraged mental disengagement. [Things That Didn’t Work](https://lucumr.pocoo.org/2025/7/30/things-that-didnt-work/)

### 37. What is the single highest-leverage, non-obvious practice?

**Confidence: High.**

Give the agent a **fast, local, executable verification loop** and make completion depend on its evidence.

This outranks prompt cleverness. A test, type check, build, deterministic script, browser scenario, screenshot comparison, or high-signal log turns the model from a one-shot code generator into an iterative search process. It also determines whether you can step away. Anthropic’s current guidance says the difference between a watched session and a walk-away session is a check the agent can run. Simon Willison emphasizes tests, interactive testing, linters, type checkers, formatters, and detailed errors. Ronacher emphasizes fast, observable, hard-to-misuse tools. [Claude Code best practices](https://code.claude.com/docs/en/best-practices), [Willison on agent-ready codebases](https://simonwillison.net/2025/Oct/25/coding-agent-tips/), [Ronacher’s recommendations](https://lucumr.pocoo.org/2025/6/12/agentic-coding/)

The newcomer’s surprise is that this is mostly ordinary software engineering. Improving the repository’s feedback surfaces benefits humans and every model, survives vendor changes, and reduces the amount of prompt process needed.

### 38. Where is practice thinnest?

**Confidence: Medium-high.**

The thinnest area is **trustworthy durable state and integration across concurrent sessions, people, and vendors**.

We have good local loops and increasingly capable orchestrators. We do not have a stable, widely adopted answer for what should be remembered; who may mutate it; how decisions, provenance, confidence, and rejected alternatives are represented; how staleness is detected; how contradictory writers reconcile; or how a new session distinguishes fact from an old agent’s confident summary. Transcripts are rich but host-specific and noisy. Markdown is portable but weakly typed and easily stale. Shared logs invite concurrency and ordering failures. Harness task stores are stronger but nonportable. Git reliably stores code changes, not all of the reasoning needed to resume safely.

The second half of the same problem is integration capacity: worktrees and subagents make generation cheap faster than they make review, semantic merge, and responsibility cheap. The field is working around this with single-writer coordination, PRs, per-agent artifacts, verification gates, and short handoff files. That is a collection of good local techniques, not yet a settled state model.

## Implications for a “cold-start card” or handoff layer

**Inference, confidence: Medium-high.** The research supports a narrow version of this idea and argues against a grand one.

A useful card is not universal memory. It is a compact re-entry contract containing:

- the outcome and immutable constraints;
- repository/worktree and exact commit;
- current state and the next independently verifiable step;
- decisions plus unresolved choices, with provenance;
- failed approaches worth not repeating;
- exact verification commands and the last observed results;
- ownership/authority and an expiry or freshness marker.

Keep canonical intent separate from volatile execution state if the harness can enforce ownership or read-only access. Prefer one coordinator or per-agent records over several writers appending prose to a single file. Let every receiving agent re-run cheap read-only probes rather than trusting the card blindly. The strongest form is therefore a small state pointer plus verification receipt—not a larger prompt that tries to preserve the whole conversation.
