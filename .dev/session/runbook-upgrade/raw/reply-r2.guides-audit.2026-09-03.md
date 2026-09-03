# Reply R2 — file-plane audit, prior-art delta, and earned redesign

**Research cutoff:** 2026-09-02 UTC. The brief is dated 2026-09-03, plausibly in the author's local time; vendor facts below were checked on the UTC date stated here.

**Primary exhibits:** the supplied RUNBOOK, PAD, STATUS, and BUS guides; `atlas-ui.md`; Recorder's `CLAUDE.md` and `config.json`. Cartan's `AGENTS.md` plus the Codex harness bundle are treated as a supplementary, in-progress mirror, per the operator's clarification—not silently substituted for either of the two Claude-era agent definitions.

**Evidence labels:** **D** = current documented vendor behavior; **C** = community or issue-report evidence; **E** = empirical study/preprint; **I** = my audit inference from the supplied files. Confidence is about the claim as stated, not about whether the design preference is universally correct.

## Short verdict

The plane is not resumable from the four guides alone. They are a constitution for constructing a session, not a session instance. With a correctly populated RUNBOOK and STATUS, the recovery design is unusually strong; without those files, a fresh agent cannot identify a project, gate, worktree, live hold, or next action.

The main structural defect is sharper than “too many files”: a two-machine, multi-seat protocol places current truth in one mutable STATUS while allowing “whoever advances the gate” to replace it. There is no lock, revision check, atomic update, replication receipt, or single status owner. The protocol is careful about semantic authority but has no concurrency protocol for the physical authority file. That is the first redesign worth earning.

The second defect is that most “laws” are prose. The guides correctly distinguish claims from evidence, yet do not apply that distinction to their own compliance. Several high-consequence laws—holds, pre-action recovery state, gate immutability, independent verification, and safe pruning—have neither a check nor a breach signal.

What is worth preserving is substantial: one gate, one present position, one safe next action plus expected observation, explicit interrupted-side-effect state, a read-only recovery probe, mandatory remaining uncertainty, and the rule that a RETURN is not evidence. Those are ahead of ordinary field practice. Native subagents, agent teams, Advisor, import, and the Codex-for-Claude plugin replace parts of transport and consultation; they do not replace a project-owned durable recovery and acceptance record.

---

## Part A — read cold

### 1. Can a fresh agent resume? Precisely where does it stall?

**No—not from the supplied folder. [I, high]** The guides teach how a valid session should look, but no live session instance is enclosed. The agent stalls before it can select even a read-only recovery probe.

The exact missing chain is:

1. No project root or session root is identified.
2. No project `pulse.md` identifies an active session slug or exact STATUS path.
3. No live `RUNBOOK.md` supplies the actual gate, participants, fixed holds, prompts, or references.
4. No live `STATUS.md` supplies host, worktree, branch, HEAD, dirty paths, checkpoint, possible in-flight side effects, recovery probe, current holds, next action, or expected observation.
5. The guides themselves say that none of these filenames is auto-loaded and “a session file is read because a prompt points at it.” There is no such instance prompt here.

Therefore the safe cold action is “ask for or locate the active project/session pointer,” not “resume work.” Searching every parent and sibling folder would be an invented discovery protocol, and acting in whichever repository happened to be the current directory would violate the guides' own frame discipline.

**What is good after the stall is acknowledged:** if the missing instance exists and STATUS is honestly populated, the field set is sufficient for a strong cold resume. In particular, `in_flight` plus an interpreted, read-only `recovery_probe` is more operationally useful than a narrative handoff. The claim that this takes thirty seconds is not yet demonstrated by an observed test; it is a good acceptance criterion, not evidence of attainment.

### 2. Contradictions in the four guides

These are contradictions as written. Some are easy to repair, but repairability does not turn them into nuances. [I, high unless noted]

| # | One side | Other side | Why both cannot stand literally |
|---|---|---|---|
| C1 | RUNBOOK: “**Point at canon, never reproduce it.**” | RUNBOOK: pulse carries the session “**gate**”; STATUS: “`gate:` is **verbatim from RUNBOOK**.” | The canonical gate is deliberately reproduced in at least RUNBOOK, pulse, and STATUS. Either gate copying is an explicit checked exception, or the no-reproduction law is false. There is currently no drift check. |
| C2 | RUNBOOK/STATUS seam: a line useful after closure belongs in “`flag.md` **or `pulse.md`**.” | RUNBOOK: pulse is a bounded active-session router; on closure, “**remove the session from `pulse.md`**.” | A durable session fact cannot generally live in a router entry that is removed at closure. `flag.md` or a durable evidence/canon home can survive; the active pulse entry cannot. |
| C3 | RUNBOOK: “**No journal. History lives in git.**” | STATUS: “**History lives in git, `_bus/`, PADs, and promoted evidence.**” | The first sentence states an exclusive home; the second names four. The likely intended distinction is durable history versus transient receipts, but the text does not say that. |
| C4 | STATUS: the authority boundary lives in RUNBOOK: “**Point there; do not reproduce a second authority model here.**” | STATUS immediately reproduces the seam test, later reproduces the whole tense/ownership table, and restates gate mutation and pulse rules. | STATUS tells its author not to repeat a model and then repeats it. This also creates another future drift surface. |
| C5 | PAD: “**one step at a time… never dumps the whole procedure**” and “**One step revealed at a time**.” | PAD: “**A PAD is a single markdown file**” whose anatomy contains `STEP N` sections and optional whole-run verdict mapping. | A pre-authored single file exposes every section to its reader. The rule becomes true only if the file is incrementally authored/replaced so future steps are absent, but that mechanism is not stated. [Medium: the author may have intended conversational presentation rather than file visibility.] |
| C6 | BUS VERDICT accepts “`<absolute or session-relative POINT path>`” and the same for RETURN. | BUS style law: “**Exact commands and absolute paths; no assumed shell state.**” | Session-relative paths are explicitly legal in one schema and forbidden by the blanket law in the same guide. |

One further overclaim is not a cross-guide contradiction but deserves correction: PAD says “Nothing the operator can do is … broken-forever—step 0 makes that true.” A precondition check or `.bak` file cannot make an arbitrary external or destructive later action reversible. That is a false safety guarantee, not merely enthusiastic wording.

### 3. Laws the system cannot enforce

Anthropic's current documentation makes the relevant distinction explicit: instruction files are context, not enforced configuration; it recommends a `PreToolUse` hook for an action that must be blocked regardless of model choice. [D, high; [Claude memory documentation](https://code.claude.com/docs/en/memory)] The supplied guides contain no equivalent validator, hook, rule, lock, or close command.

| Law or law family | What detects a breach now? | Judgment |
|---|---|---|
| One session = one gate; a changed gate opens a sibling | A human may notice different prose later; Git may show a diff after the fact. No semantic check. | **Latent failure.** Gate identity controls lifecycle and pruning. |
| RUNBOOK fixed/read-once; no mutable fields | Ordinary review only. | **Usually adequate on honour** for a solo session, but becomes latent when a changed participant, host, or hold is silently patched into it. |
| Pulse routes; STATUS is the sole doing-state | Nothing searches for competing `next`, status, handoff, or cold-start files. | **Latent failure.** The guide cites this exact historical failure. |
| Gate copied verbatim across files | Nothing compares the copies. | **Latent failure.** This is duplicated authority without a consistency check. |
| Known holds in RUNBOOK; discovered holds in STATUS | No timestamp/source check determines when a hold became known. | **Honour is adequate** for taxonomy; **preserving a destructive hold is latent** because omission can destroy a precondition. |
| Every STATUS field present; one `next`/`expected`; absolute commands; no dock pointer | A reader may spot malformed prose. No schema validation. | **Latent failure** for missing holds, recovery fields, or ambiguous next; merely inconvenient for case/format errors. |
| Write `in_flight` before a non-idempotent/external action | Nothing interposes on the action. | **High-severity latent failure.** It is most likely to be omitted exactly when the operator is moving quickly. |
| Recovery probe is read-only and distinguishes never-started from partial | No command classifier or outcome test. | **Latent failure.** A plausible-looking probe can mutate state or fail to distinguish the cases. |
| Rewrite STATUS after each verified transition and before yield | No transition counter, dirty flag, or yield hook. | **Latent failure**, and likely attrition pressure because it is frequent. |
| Whole-snapshot rewrite keeps holds honest | No check proves the writer carried forward every still-live hold. | **Latent failure.** The proposed friction can remove stale holds, but it can also erase live ones; the guide counts only the first effect. |
| PAD reveals one step, makes run reversible, branches every outcome, creates at most one distilled log | No rendering boundary, action gate, branch completeness check, or file-count check. | **One-step pedagogy is adequate on honour; reversibility and destructive safety are latent failures.** |
| BUS appears only at 2+ seats; unique sequential cycle; single writer/file; one file/direction | Git conflict may reveal simultaneous edits, but no allocation/ownership mechanism prevents collisions. | **Latent under concurrency; adequate for a strictly serialized solo operator.** |
| Verifier inspects/reruns; RETURN is not evidence; verifier does not fix | A VERDICT can assert checks that never ran; the same actor can act under two names. | **Latent failure.** This is the acceptance boundary. |
| All uncertainty is disposed; STATUS rewritten before cycle close | Required prose fields but no cross-file completeness check. | **Latent failure.** Empty “none” is indistinguishable from a dishonest or careless one. |
| Promote durable material before pruning the session | No promotion manifest or close check. | **High-severity latent failure:** irreversible loss can be committed cleanly. |
| Naming case, first/present/past tense, generic driver voice | Human review. | **Honour is adequate.** These are ergonomic, low-consequence conventions. |

The issue is not that prose rules are useless. Empirical work finds agents often do follow context-file instructions; the issue is that compliance costs more and is probabilistic. One 438-task evaluation found no significant general success gain and a 20–23% cost increase, while observing more instruction-following, testing, and exploration. [E, medium; [Gloaguen et al., 2026](https://arxiv.org/abs/2602.11988)] That is not a suitable foundation for destructive holds or independent acceptance.

### 4. What is missing that the guides do not know is missing?

The largest omission is **a physical concurrency model for the single semantic authority. [I, high]** The set was designed for agents on two machines, and BUS is born at two active seats, yet STATUS has one `host` and one `worktree`, and “whoever advances the gate” replaces the whole file. Two honest writers can both read revision A, advance different edges, and replace it with B and C. Both obey every written law; one current truth is still lost.

The rest follows from that mismatch:

1. **No atomicity or compare-and-swap.** A STATUS write can be interrupted, truncated, or based on a stale version. There is no `revision`, base digest, lock, atomic rename contract, or conflict owner.
2. **No representation for simultaneous frames.** One `host/worktree/HEAD/dirty paths` cannot describe two active seats on two machines. Putting the most recent writer there makes the other seat disappear without actually stopping it.
3. **No replication state.** A commit, PAD output, or evidence path may exist on one host but be unpushed or absent on the other. “Path resolves” is not “same bytes”; the protocol lacks a remote/ref/content digest or transfer receipt.
4. **Cycle-number allocation is undefined.** Two seats can legitimately choose the same next `NN`. “Single writer per file” does not say who reserves a filename.
5. **No schema or guide version in an instance.** The guides are dated and evolving, but RUNBOOK/STATUS/BUS instances do not declare which schema revision they implement. A fresh agent cannot distinguish an old valid session from a malformed current one.
6. **No writer authenticity or trust boundary.** `writer: seat · vendor` is an assertion. There is no relationship between a seat name and a runtime identity, no protection against symlink/path escape, and no policy for treating instructions embedded in imported artifacts as untrusted data.
7. **No liveness or seat-replacement protocol.** There is no timeout, abandoned POINT state, reassignment rule, or ownership transfer when a machine, account, or human disappears.
8. **No executable gate oracle.** The gate is free text. It can be compound, unverifiable, or declared closed from a weak proxy. `expected` helps one action; it does not prove the session gate.
9. **No safe close transaction.** Promotion, pulse removal, and pruning are several operations. A crash between them can leave an invisible live session or delete the only receipt. No closure receipt proves what was promoted and what was intentionally discarded.
10. **No treatment of non-Git environment state.** Processes, panes, ports, local databases, credentials, uncommitted changes, and externally visible actions do not become portable because the session directory is committed.
11. **No measured conformance test.** The thirty-second cold-resume standard is excellent, but no supplied evidence records fresh-agent time, wrong-action rate, omitted holds, or resume success.
12. **No bootstrap contract for a stranger.** The four guides refer outward to pulse, flag, project rules, evidence homes, a session root, a gavel holder, and vendor prompts. Nothing enclosed resolves those names for a new operator.

These are not requests for more prose. Most are properties that more prose cannot establish.

### 5. Are the jobs actually disjoint?

**No. The artifacts have distinct temporal roles, but many lines legitimately occupy two to six of them. [I, high]** That is not automatically bad; it becomes bad where the system says “never copy” while relying on copied control facts.

| Concrete line | Plausible homes | Where a writer hesitates |
|---|---|---|
| `gate: cart acceptance passes at commit abc` | RUNBOOK canonical gate; pulse gate display; STATUS verbatim gate; VERDICT `gate_effect` | Is the commit part of the fixed gate, the present checkpoint, or the closure evidence? A later commit changes some copies but not others. |
| `Do not drop the test DB until T3 passes.` | RUNBOOK known constraint; STATUS discovered/live hold; POINT `gates`; perhaps project flag if cross-session | The correct home depends on when it was learned and how long it survives—not on its content. A writer re-entering later may not know its provenance. |
| `Run /srv/cart/check; expect 42 passed.` | RUNBOOK seat prompt; STATUS `next/expected`; PAD active step; POINT exact command/`done_when` | The same future action is instruction, current state, human step, or delegated scope depending on who performs it. |
| `42 passed at commit abc; report at evidence/cart-42.txt.` | STATUS checkpoint; RETURN commands/evidence; VERDICT claim table; durable evidence index | It begins as a claim, becomes a verified transition, and may survive the gate. There is no single home during that promotion. |
| `Ask majkee to restart service X and report its PID.` | STATUS next; PAD step; RUNBOOK human participant/prompt; POINT if another seat drives the operator | Human dependency does not itself choose the artifact. |
| `Next, investigate the flaky shipment test.` | RETURN recommendation; STATUS next; new POINT | The BUS correctly says a recommendation is not current until copied to STATUS, but that intentional duplication is exactly where a stale recommendation can compete. |

The true separation is therefore:

- RUNBOOK: fixed authority and role contract;
- STATUS: one current recovery edge;
- PAD: operator interaction and raw receipt;
- POINT/RETURN/VERDICT: assignment claim, response claim, and acceptance transition.

That separation is coherent. The contents are not disjoint, and the guides should not claim or imply that they are. They need explicit promotion/cached-copy semantics at the overlaps.

### 6. What length bound should the files carry?

**No evidence supports a universal line or word limit for this set. [E/I, high]** Current evidence is mixed even on whether context files help at all, and it is weaker on an optimal length:

- A 2026 evaluation covering 300 SWE-bench Lite tasks plus 138 CTXbench tasks found no significant general success improvement from context files, 20–23% higher inference cost for generated files, and no clear dependency between success/cost and file-length bins. It recommends human files only for non-inferable, non-redundant practices. [E, medium; [paper](https://arxiv.org/abs/2602.11988)]
- A separate 124-PR study associated the presence of AGENTS.md with 28.64% lower median runtime and 16.58% fewer median output tokens, but did not evaluate correctness or file length as the causal variable. [E, low-to-medium for generalization; [Lulla et al., 2026](https://arxiv.org/abs/2601.20404)]
- A smaller controlled study—288 runs over 17 tasks—found no measurable correctness effect for context strategy and explicitly describes the evidence as contradictory. [E, low-to-medium due sample size; [Khatri, 2026](https://arxiv.org/abs/2607.27250)]
- Anthropic currently recommends targeting under 200 lines per auto-loaded CLAUDE.md and moving multi-step procedures to skills or path-scoped rules. Codex stops accumulating discovered project instruction files at a configurable combined 32 KiB by default. Those are loader/adherence budgets, not demonstrated universal quality thresholds. [D, high; [Claude memory](https://code.claude.com/docs/en/memory), [Codex AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)]

The supplied guide sizes are RUNBOOK 151 lines/1,067 words, PAD 134/1,072, STATUS 153/1,214, and BUS 187/1,141. They are on-demand builder documents, not four files automatically injected into every task. Comparing each directly with the 200-line CLAUDE.md heuristic would be a category error.

The useful bounds are structural:

- **STATUS:** fixed field count plus the existing measured-behavior target: a genuinely fresh agent resolves frame, risk, probe, and one next action in thirty seconds. Fail the test, shorten or clarify. Do not add narrative fields.
- **RUNBOOK:** one gate; one fixed prompt per seat; only facts that remain true for the session. Its bound is immutability, not lines.
- **POINT/RETURN/VERDICT:** one bounded cycle and the existing fixed schemas. Large command output stays behind a stable evidence pointer.
- **PAD:** completed raw receipts plus exactly one active step if “revealed” is meant literally. Its bound is one operator decision surface, not total historical lines.
- **The guides themselves:** no hard count. Keep them on demand, measure adherence and cold performance, and split only when a section has a different trigger. If any is moved into an always-loaded instruction chain, then the runtime's actual byte/line budget becomes a hard operational ceiling.

### 7. What will probably be abandoned within six months?

These are predictions, not reported outcomes. [I, medium]

1. **`dock.md` as a named convention.** The STATUS guide records zero entries after weeks. Optional unused scratch whose contents cannot be cited is likely to become ordinary notes or nothing.
2. **Absolute paths everywhere in shared artifacts.** They prevent accidental relative resolution on one host but are inherently host-specific across two machines. Writers will eventually use repository-relative paths, aliases, or stale absolute paths despite the law.
3. **A full three-file BUS cycle for routine same-runtime delegation.** Native Claude subagents/teams and Codex subagents already provide assignment, execution, messaging, task state, and returned results. The BUS will survive where cross-vendor, cross-machine, high-risk, or Git-owned provenance matters; it will be skipped for ordinary internal work. [D/I, high on feature existence, medium on attrition; [Claude teams](https://code.claude.com/docs/en/agent-teams), [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)]
4. **“Rewrite after every verified transition and before yielding” at full literal frequency.** It is valuable at risky boundaries but costly after tiny transitions. Without automation, practice will narrow it to meaningful checkpoints.
5. **Opening a numbered sibling for every gate wording change.** Major scope changes justify it; minor clarification and better acceptance wording will be amended in place because the ceremony is disproportionate.
6. **Hard pruning immediately on close.** When the close transaction has no promotion manifest, operators will archive or delay deletion out of justified fear of losing the only receipt.
7. **The compulsory one-time GLOSS offer in every PAD.** It is peripheral to the gate and will be inconsistently remembered.

I do **not** expect one-gate sessions, STATUS as the current recovery edge, the recovery probe, or claim-versus-evidence discipline to be abandoned. They solve observed failures and impose cost at the point where the cost buys safety.

### 8. What did Atlas learn from Recorder, and what did it lose?

The later Atlas is technically current but not simply better.

**What is wrong in Atlas first [I, high]:** it says “Model floor in ONE place; never hardcode dated model strings” while its own frontmatter says `model: claude-opus-4-8`. It claims read-only Bash while granting the unrestricted Bash tool and relying on voluntary refusal plus a global ask backstop. “Do not write until confirmation” is likewise a behavioral rule while Write/Edit are present. And it lets a DRAFT/experimental Sella doctrine “win” over sibling builder guides, which promotes lower-authority material above apparently stable guides. The many private paths and personae make its re-entry path fragile outside one operator's machine.

**What Atlas learned:**

- It is a real native Claude custom-agent definition: trigger-rich YAML frontmatter, model/effort/tools/skills, and a body used as the agent prompt. Recorder's arbitrary sibling `config.json` is not a documented Claude Code agent configuration. Current Claude agents live as Markdown plus frontmatter under `.claude/agents/` or `~/.claude/agents/`. [D, high; [Claude subagent documentation](https://code.claude.com/docs/en/sub-agents)]
- It names source, staging table, live deploy target, deploy owner, directionality, and verification. Recorder largely says “maintain this master file.”
- It has a bounded re-entry order and single-writer ownership for its own state.
- It separates project facts from primitive/reference facts and uses targeted lookup for the heavy material.
- It selects the smallest native primitive and performs an existence search before creation; this is tied to an actual prior redundancy failure.
- It buffers human input and asks for confirmation before emitting a file.
- It distinguishes authoring from deployment and warns about a concrete reverse-sync overwrite failure.
- It recognizes native hooks, skills, subagents, MCP, and escalation rather than simulating every capability in prose.

**What Atlas lost:**

- Recorder has a much clearer negative role: “librarian, not a contributor,” no architecture invention, stop on contradiction, preserve source voice. Atlas has more authority surfaces and more ways to rationalize adjacent work.
- Recorder's marker taxonomy gives compact, directly scannable output semantics. Atlas's mythology and private proper nouns increase onboarding cost without adding machine meaning.
- Recorder has a crisp output envelope: changed section(s), one-line summary, at most one question. Atlas's result contract is less exact.
- Recorder explicitly preserves disagreement and attribution. Atlas has curvature language elsewhere in its ecosystem, but its own creation procedure focuses more on producing the primitive than preserving competing source positions.
- Recorder is conceptually portable: one input, one master record. Atlas is operationally bound to `~/.remote`, two pulse files, mail folders, `reposoma`, `ia-sync`, Sella, Zenith, named executors, and a particular home path.

**Recorder's age shows materially:** its alternate identities permit session drift; “never delete, archive at bottom” conflicts with a 3,000-line master and guarantees accumulation; high-trust agent inputs are accepted without an evidence check; and the JSON describes logging, limits, model parameters, API credentials, and wrapper fallback without enclosing a wrapper that implements any of them. Current Claude Code documents `.claude/settings*.json` for settings and Markdown/YAML for custom agents; an arbitrary `session/config.json` has no documented native effect. [D/I, high; [settings](https://code.claude.com/docs/en/settings)] The `<FILL_API_KEY>` field is also a credential-footgun even though its comment recommends an environment variable.

**Codex mirror addendum:** Cartan plus `harness_builder` retain Atlas's strongest lesson—semantic equivalence rather than file parity—and improve the one-pulse rule, project/native separation, source map, current-doc check, and verifier role. They also inherit the private-path portability problem and the unenforced confirmation/deploy boundary. The mirror is structurally more current than Recorder, but its effectiveness is not established merely by syntactic validity.

### 9. What breaks first for a second person?

**Discovery and authority break before the file schemas do. [I, high]** A second person encounters `/home/hruzam`, `~`, `reposoma`, `ia-sync`, pulse variants, Sella, Zenith, Houston, Flight, Cartan, gavel language, and evidence homes that are neither included nor defined in ordinary operational terms. They cannot know which references are required, which are private mnemonic names, or which person may approve/write/deploy.

The failure order is likely:

1. Absolute paths do not resolve, and no portable repo identity maps them to the second clone.
2. No root bootstrap tells the newcomer which active pulse/session to open.
3. The actual precedence of project canon, guide, draft doctrine, runtime config, and operator gavel is unclear; Atlas explicitly lets a draft win in one case.
4. Host aliases and single-writer ownership do not transfer into accountable human identities or permissions.
5. The singular STATUS becomes a race as soon as two people, rather than one operator serializing two agents, can advance the gate.
6. BUS deliberately has no notification/read state; the second person cannot tell that a POINT exists or that a return was consumed.
7. The guide/schema revision is absent from instances, so a newcomer cannot tell drift from noncompliance.

The four core artifact names are learnable. The personal ontology and unresolved filesystem topology are not. Handing over only the guides would reproduce the Q1 stall; handing over the full private tree would create a permissions and precedence problem instead.

### 10. Ahead, at par, and behind current field practice

Vendor facts in this ranking were checked 2026-09-02 UTC.

| Rank | Components | Judgment |
|---|---|---|
| **Ahead** | `in_flight` written before a risky action; interpreted read-only recovery probe; exactly one next/expected pair; RETURN-as-claims-not-evidence; mandatory remaining uncertainty; curvature; explicit promotion boundary; optional files born only on need; authoring table separated from live deploy | These address failure recovery and epistemic acceptance more precisely than ordinary README/agent instructions. Preserve them. |
| **At par** | One bounded objective/gate; Git-backed evidence; explicit human approval; native custom agents with scoped tools/models/skills; worktree awareness; independent review; project/user instruction separation; on-demand skills | These match current Claude and Codex capabilities and sound field practice. Current vendor docs now expose model/tool/skill/memory/isolation fields, hooks, subagents, and parallel orchestration. [D, high; [Claude subagents](https://code.claude.com/docs/en/sub-agents), [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)] |
| **Behind—replace the mechanism** | Recorder's arbitrary `config.json`; same-runtime BUS as task transport/mailbox; manual cross-vendor launch/poll/transfer; senior spawn used only for advice; prose-only blocking rules; monolithic always-loaded procedure if any guide is placed there | Use native custom-agent/settings formats; native subagents or Claude agent-team task/mailbox state for same-runtime coordination; the official Codex-for-Claude plugin for review/rescue/transfer/status/result; Advisor for pure decision consultation where available; native hooks/rules or a validator for deterministic file/action constraints; skills/path-scoped rules for on-demand procedure. |

Claude agent teams now provide a shared task list and validated mailboxes, though they remain experimental, local, higher-token, and explicitly poor for same-file edits. Their docs warn that two teammates editing the same file produces overwrites—the same unresolved hazard the current STATUS writer model has. [D, high; [agent teams](https://code.claude.com/docs/en/agent-teams)]

The conclusion is **not** “replace the whole file plane.” Replace transport, native configuration emulation, and advisory escalation where a shipped primitive genuinely owns those jobs. Keep the project-owned state/evidence layer where native state is host-owned, runtime-specific, or insufficiently durable.

---

## Part B — prior-art delta

### 11. Cross-vendor consultation

#### What the official mechanisms cover

The most concrete current mechanism is OpenAI's official Codex plugin for Claude Code. It provides:

- read-only normal and adversarial Codex review;
- task delegation through `rescue`, including fresh/resumed threads, model/effort choice, and background execution;
- `status`, stored `result`, and cancellation for background jobs;
- transfer of the current Claude Code transcript into a persistent Codex thread, with a `codex resume <session-id>` command;
- an optional Stop-hook review gate that can block Claude when Codex finds an issue;
- reuse of the local Codex installation, authentication, configuration, checkout, and machine environment. [D, high; [official repository](https://github.com/openai/codex-plugin-cc)]

ChatGPT/Codex also has an official import flow for Claude Code/Cowork/Cursor setup, projects, memories, and recent chats. Desktop can keep imports updated; CLI imports selected Claude/Cursor setup and up to 50 chats from the prior 30 days. This is migration/continuity, not a bounded consult protocol. [D, high; [OpenAI import documentation](https://learn.chatgpt.com/docs/import)]

#### What they do not cover

- **Verification:** the review commands and optional stop gate provide genuine independent checking, but they do not require that every delegated RETURN receive a distinct verifier's claim-by-claim disposition. A rescue result can be accepted directly. The stop gate also warns that it may create a long-running, usage-draining Claude/Codex loop.
- **Provenance:** job and Codex session IDs give runtime provenance. The commands do not require a project-owned POINT with scope/forbidden operations/done-when, evidence content hashes, or a durable mapping from each claim to the exact accepted artifact.
- **Ownership:** plugin state and imported/resumable threads belong primarily to local product/runtime storage. They are not automatically Git-owned project records reviewed with the code.
- **Survival:** a result is stored and a transferred thread is persistent/resumable, but the official contract does not promise that a bounded exchange, verification disposition, and evidence manifest survive under the repository's retention/version policy. Import itself is bounded by client and recency rules.
- **Cross-machine execution:** the plugin explicitly uses the same machine's local Codex, checkout, config, and environment. It does not solve two-host evidence availability or absolute-path translation.

#### Adoption cost

The plugin requires Node 18.18+, a compatible Claude plugin installation, a local Codex install and login/API access, setup/reload, and additional Codex usage. Background work must be monitored; the review gate must be watched to avoid loops. Import requires review of translated permissions, hooks, connections, and path-dependent prompts. The local file design costs at least a POINT, RETURN, VERDICT, Git handling, human/runtime transport, and a real verification pass per cycle.

#### What the local design should keep

**Classification: complementary, with a shrinking residual. [I, high]**

Use the official plugin as the execution/transport/job-control plane. Keep the file envelope only when at least one of these is true: cross-machine work, durable project-owned provenance, a high-risk acceptance gate, evidence that must survive product history retention, or an exchange that must be legible to both vendors after their local threads disappear.

For a casual same-machine question, the file form is redundant. For an audited cross-vendor change, the residual is real: bounded assignment, stable ownership boundary, explicit uncertainty, independent acceptance, and a Git-reviewed record. The local design should not keep a parallel long-lived relay, polling layer, or duplicate native transcript.

### 12. Competence escalation versus native Advisor

#### What native Advisor gains

Claude Code's experimental Advisor is the closest shipped match. A main model can consult a typically stronger model at decision points. The advisor receives the full conversation—including tool calls and results—returns guidance, and the main model continues. Claude validates allowed model pairings, shows the consultation in the transcript, and keeps the main prompt cache intact when Advisor is toggled. [D, high; [Advisor documentation](https://code.claude.com/docs/en/advisor)]

That removes manual context packaging, separate task transport, and result reintegration. For “this decision exceeds my competence; give me a stronger opinion,” it is the cleaner native shape.

#### What it constrains or does not do

- Claude controls timing; there is no setting to force or cap calls, although the user can request consultation in the prompt.
- Every call processes the full transcript anew; the advisor's read is not cached and incurs the advisor model's additional input/output cost.
- It returns guidance to the same main agent. It does not own a separate worktree, execute an independently permissioned investigation, or produce a required durable artifact.
- “Independent check” means a second model read, not an independent acceptance authority. The main agent applies or rejects the guidance.
- Pairings are constrained by vendor capability ordering; an unrecognized or less-capable advisor is not attached.
- It is experimental, requires the Anthropic API, and is unavailable on Amazon Bedrock, Claude Platform on AWS, Google Cloud's Agent Platform, and Microsoft Foundry. It can also remain off when feature-flag fetching is disabled. [D, high; same source]

Claude's own comparison says Advisor runs at decision points, whereas a model-configured subagent runs for an entire delegated subtask. That is the correct distinction.

#### Where spawning a senior agent remains right

Keep a senior spawn when the job needs a bounded clean context, different tools/permissions, independent file inspection, an isolated worktree, a durable report, a distinct acceptance role, cross-vendor diversity, or operation on a provider where Advisor is unavailable. Use Advisor when the output is advice consumed immediately by the same agent.

Codex currently documents model/effort-specific custom subagents and orchestration, but I did not find an official Codex feature with the same full-transcript, mid-task, model-selected Advisor semantics. [D/I, medium; [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)] The supplied `harness_builder` is a whole delegated role and therefore belongs on the subagent side of this line, not the Advisor side.

### 13. Concrete deadweight observables

Use a sample, not a feeling. Twenty consecutive qualifying uses is enough for a first local decision, not a universal statistical threshold. [I, medium]

| Local design | Evidence it has become dead weight | Evidence the residual still earns its keep |
|---|---|---|
| Cross-vendor file exchange | Across 20 exchanges, no later resume/review/PR reads a POINT, RETURN, or VERDICT; no exchange crosses hosts; every verdict merely repeats native review output; native job/session IDs and Git diffs reconstruct every fact needed; the files add human touches and elapsed time without catching one extra scope, evidence, or acceptance error. | A file catches unauthorized scope, missing evidence, false command claims, or unresolved uncertainty; a second host/vendor can resume from it after native history is unavailable; a reviewer cites it in an acceptance decision. |
| Senior-agent spawn for competence | In 20 escalations, the senior makes no tool call, uses no distinct source/context/permission, emits no durable artifact, and supplies only short advice that a native Advisor can obtain with lower latency/cost; decisions and later defect catches are no better. | The senior changes a decision after independent evidence, uses separate tools/context, produces a consumed artifact, finds defects Advisor misses, or is required because Advisor is unavailable. |

Track five values per use: human handoffs, wall time, incremental token/usage cost, extra defects or scope violations found, and whether any later actor actually consumed the durable record. The last two matter more than file count. A protocol that is never read is storage; a second model that never changes or verifies anything is theatre.

---

## Part C — several projects under load

### 14. What actually fails at switch time?

#### Failure modes first

1. **The wrong frame becomes active. [C, high that it occurs; unknown prevalence.]** A Claude Code issue report describes starting from the wrong directory, needing restarts for the right project context, and accumulating conflicting CLAUDE.md contexts through added directories. [Issue #4689](https://github.com/anthropics/claude-code/issues/4689) An open Codex report goes further: after compaction, a prompt intended for one task appeared in another project's task and Codex acted there. The reporter could not reproduce it deterministically, so this is a serious single report, not a measured product rate. [Issue #35307](https://github.com/openai/codex/issues/35307)
2. **Session discovery is path/UI-bound. [C, high.]** Claude's VS Code history is reported as workspace-scoped, forcing users to switch projects just to find another session; one reporter had 72 session files across 14 projects but only the current workspace's sessions visible. [Issue #49095](https://github.com/anthropics/claude-code/issues/49095) Codex users report that renaming/moving a folder leaves old threads grouped under the stale project, requiring risky metadata edits. [Issue #28749](https://github.com/openai/codex/issues/28749) Conversely, another Codex report says a global mixed-project history makes it easy to resume the wrong thread. [Issue #25319](https://github.com/openai/codex/issues/25319) The two complaints are not inconsistent: users need both strong project scoping and a searchable global view.
3. **Current intent disappears before code does. [C/I, high.]** On return, code and commits may remain, but the active hypothesis, last safe checkpoint, half-completed external action, pending human approval, and exact next observation often live only in the old session. An open Claude request for a curated `/handover` explicitly describes today's alternatives as lossy automatic compaction or a manual handoff dance, especially before stepping away or changing phase. [Issue #54254](https://github.com/anthropics/claude-code/issues/54254)
4. **Decision provenance is compressed away. [C, medium.]** A detailed community report describes a rejected billing approach returning after `/compact` under a cleaner name, breaking the exact edge case that caused the original rejection. Replies converge on the loss of rationale and rejected alternatives rather than code visibility. This is anecdotal, not prevalence evidence. [Reddit field report](https://www.reddit.com/r/ClaudeAI/comments/1tglril/the_failure_mode_i_keep_hitting_in_long_claude/)
5. **The durable context itself can be stale. [E/I, medium.]** A preliminary context-rot paper applied an existing consistency checker to 356 repositories and found stale code-element references in 23.0%. It does not establish that 23% of agent actions fail, but it demonstrates that persistent context cannot be treated as automatically fresher than a transcript. [Treude & Baltes, 2026](https://arxiv.org/abs/2606.09090)
6. **Machine-local memory does not cross machines. [D, high.]** Claude auto memory is per repository but explicitly machine-local and not shared with other machines or cloud environments. A returning agent on the other machine can therefore have the same repository and a different remembered project. [Claude memory documentation](https://code.claude.com/docs/en/memory)
7. **Environment state does not travel with Git. [I, high.]** Dirty uncommitted files, unpushed refs, running services, tmux panes, ports, databases, credentials, and partially applied external actions can all differ. A transcript or memory may describe host A accurately and still instruct host B incorrectly.
8. **A warm resume can be more dangerous than a cold one. [I, high.]** The transcript retains confident observations from before another project, agent, branch, or deployment changed the environment. The user sees continuity; the model sees stale tool results unless it re-probes.
9. **Concurrent projects create review and notification debt. [C/I, medium.]** Results and approval requests accumulate in different terminals/clients. Native team documentation itself warns that two teammates editing one file cause overwrites and that coordination adds tokens/overhead. [Claude agent teams](https://code.claude.com/docs/en/agent-teams) The human can approve a correct-looking result against the wrong branch or project because the cognitive switch is also a state transition.

#### What mitigates those failures, and at what cost

- **Separate project sessions/worktrees plus a re-entry frame check** mitigate wrong-root and cross-project bleed. On every return, re-resolve repo identity, host, branch, HEAD, dirty paths, and active instructions before trusting the transcript. Cost: more worktrees, storage, session naming, and explicit switching.
- **Native resume/history/import** reduces manual re-explanation and can preserve recent conversations. Cost: client/path/retention dependence; imported or resumed context can still be stale. OpenAI's current import can bring projects, memories, setup, and recent chats across supported agents, but this is not a freshness proof. [OpenAI import](https://learn.chatgpt.com/docs/import)
- **Git plus durable tests/evidence/decision records** preserves what must outlive a session. Include rejected alternatives only when they are load-bearing. Cost: authoring/review and context-rot maintenance; a stale decision file can be worse than no file.
- **A short current STATUS with an interpreted recovery probe** directly mitigates lost dynamic intent and partial actions. This is the supplied system's strongest answer. Cost: disciplined updates at meaningful risk/checkpoint edges.
- **A curated fresh handoff rather than indefinite warm continuation** reduces dead-end and stale-observation pollution. Cost: summary time and inevitable information selection. It must point to current artifacts and be revalidated.
- **Machine-independent identifiers and content/commit references** mitigate path mismatch. Cost: root resolution and explicit sync checks on each host.

The honest field answer is that there is no good general solution yet. Vendor session continuity preserves more transcript; project files preserve more standing truth; neither establishes freshness, physical environment parity, or decision provenance. The unresolved design tension is not “memory versus no memory.” It is **continuity versus current evidence**.

---

## Earned redesign — defects first, proposals second

This section is authorized by the actualized brief. Every remedial proposal names the finding it repairs. Items marked speculative are optional experiments, not disguised audit conclusions.

### R1. Make STATUS a single-writer, revisioned, atomic transition

**Repairs:** Q4.1–Q4.3; Q9.5; the overwrite risk reinforced by native team documentation.

Declare one `status_owner` in RUNBOOK. Other seats may create immutable returns/evidence but do not replace STATUS. Transfer of ownership is itself a verified transition. Add `schema_version`, `session_id`, `revision`, and `based_on_revision` to STATUS. Update through a tiny command that checks the expected revision, validates required fields, writes a temporary file, and atomically renames it; a stale writer fails visibly.

This is **remedial**. It changes the physical update edge while preserving “one current truth.” Cost: one small tool and explicit ownership transfer. Without the tool, adding revision prose alone is theatre.

### R2. Represent frames without pretending one absolute path is portable

**Repairs:** C6, Q4.2–Q4.3, Q7.2, Q9.1, Q14.6–Q14.7.

Use a stable repository/session identity and repo-relative artifact paths in shared files. Record the executing seat's host, resolved absolute root, branch, HEAD, and evidence digest in its RETURN; STATUS records the current owner's frame. At re-entry, resolve and verify the local root before expanding a shared path. Keep absolute commands only in host-specific PAD steps or prompts generated for that host.

This is **remedial**. Cost: one root-resolution check per seat/host. It gives up the false convenience of one “copy-pasteable everywhere” absolute command.

### R3. Put the gate in one place, or mechanically validate intentional copies

**Repairs:** C1 and the drift risk in Q3.

Preferred minimal form: RUNBOOK owns the full gate; pulse owns only active slug plus RUNBOOK/STATUS paths; STATUS carries `gate_ref` and a gate digest, not another free-text gate. If the human-readable gate must remain visible in pulse/STATUS, declare it an intentional cache and have the validator compare all copies before update/close.

This is **remedial**. Cost: a lookup for full gate text, or a cheap validation step. It restores truth to “point, do not reproduce.”

### R4. Clarify the durable/transient seam

**Repairs:** C2–C4 and Q5 overlap.

Define three homes, not a binary that misclassifies pulse:

- durable truth: flag/canon/evidence outside the closing session;
- current route/position: pulse and STATUS;
- transient receipt: PAD and BUS, pruned after promotion.

After closure, a durable line never belongs in pulse. Say “durable history lives in Git and promoted homes; PAD/BUS are transient receipts until close.” STATUS should point to the RUNBOOK seam instead of restating it.

This is **remedial prose**, not a new architecture. Cost: none beyond editing the contradictory lines.

### R5. Make “one PAD step revealed” physically true—or weaken the claim

**Repairs:** C5 and the false reversibility guarantee.

If reveal control matters, a live PAD contains completed receipts plus exactly one active step; the driver replaces/adds the next active step only after the report. Future steps are not prewritten in that file. If visibility does not matter, rewrite the law honestly: “the driver presents and acts on one step at a time, even if the procedure is visible.” In either case, replace “STEP 0 makes the run reversible” with a scoped guarantee naming what the restore point actually covers; require explicit approval for irreversible external actions.

The contradiction/safety wording repair is **remedial**. Choosing whether hidden future steps improve learning is **speculative** until tested with the operator.

### R6. Narrow BUS to the residual delta and fix cycle identity

**Repairs:** Q4.4/Q4.7, Q7.3, Q10 behind, Q11.

For same-runtime ordinary work, use native subagent/team assignment, messaging, and result transport. Create the Git BUS only for cross-vendor, cross-machine, high-risk, or retention/provenance-sensitive work. Let the status owner allocate a monotonic cycle or use a collision-resistant cycle ID; record base commit/repo identity in POINT and observed commit/host/content digests in RETURN. Preserve the three semantic roles—scope, claim, independent verdict—because native transport does not require them.

This is **remedial consolidation**. Cost: deciding at dispatch whether durable BUS is warranted. Benefit: the expensive protocol appears only where its residual value exists.

### R7. Turn enforceable laws into a checker; leave judgment as prose

**Repairs:** Q3 and Q4.11.

A small `session check` should validate fields/schema version, one next/expected, gate reference/digest, status revision, allowed relative-path form, unique cycle IDs, POINT/RETURN/VERDICT linkage, no STATUS→dock reference, and no close while `in_flight` is non-`none` or a cycle lacks disposition. A pre-action hook can require a prepared in-flight transition for explicitly classified destructive commands where the runtime supports it. Semantic quality—whether a probe truly distinguishes partial state—remains reviewer judgment.

This is **remedial** because the documents call these items LAW. Cost: implementation, cross-platform tests, and maintaining a deliberately small schema. Do not attempt to compile every style sentence into policy.

### R8. Make closure a checked transaction

**Repairs:** Q3 promotion/prune, Q4.9, Q7.6.

Before pruning: require `in_flight: none`; all BUS cycles disposed; dirty/unpushed work declared; every surviving evidence/decision mapped to its durable destination; and pulse removal prepared. Produce a compact closure manifest or commit that records promoted targets and intentionally discarded transient files, then prune.

This is **remedial**. Cost: one close pass. It spends ceremony at the irreversible boundary rather than after every minor transition.

### R9. Replace Recorder's simulated runtime with a native agent

**Repairs:** Q8 Recorder faults and Q10 behind.

Move the role contract into a native `.claude/agents/recorder.md` with a stable name, current model alias, minimal tools, and an explicit source-preservation/contradiction-stop output contract. Put genuine runtime settings only in documented settings; delete the inert `config.json` unless an actual wrapper owns and validates it. Remove inline credential fields. Split durable decisions/rejected alternatives from the raw/narrative session record so “never delete” cannot grow one 3,000-line authority.

This is **remedial**. Cost: migration of the old master and deciding which old config fields were merely wishes versus implemented behavior.

### R10. Tighten Atlas rather than replace it

**Repairs:** Q8 Atlas faults and Q9 portability.

Use a moving alias such as `opus` if the law really forbids dated model strings. Enforce read-only Bash with an agent-scoped hook/permission boundary or remove Bash; do not call voluntary refusal a contract. Replace “DRAFT Sella wins” with an explicit authority order in which draft material can inform but not override stable canon. Reduce saddle entry to portable, resolvable sources and one project pulse; private nicknames can remain display language, not routing keys.

This is **remedial**. Cost: less mythic self-description and a little hook maintenance; functional creation behavior remains intact.

### R11. Add one portable bootstrap for the second human

**Repairs:** Q1 and Q9.

At the project root, use the runtime-native instruction bridge to state in plain language: project identity; active `pulse.md` path; session root; durable evidence/canon homes; role-to-human accountability; approval/deploy owners; and the first frame-verification command. Claude can import a shared AGENTS.md from CLAUDE.md, and current Codex discovers AGENTS.md by project root, so this need not fork the substantive doctrine. [D, high; [Claude memory](https://code.claude.com/docs/en/memory), [Codex project instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md)]

This is **remedial**. Cost: one short, stable router maintained with the repository. It must not become another project encyclopedia.

### R12. Treat cold resume and switching as an evaluated behavior

**Repairs:** Q4.11, Q6, and Q14.

Periodically give a fresh agent only the portable bootstrap and live session files, then measure: time to correct repo/HEAD, first action selected, holds retained, recovery classification, stale-evidence detection, and whether it touches the correct project. Run the same probe after a host switch and after an unrelated project. Track failures before adding instructions.

This is **remedial evaluation**. Cost: a small recurring test. The exact cadence and pass threshold are **speculative** and should follow observed failure frequency.

## Proposed vNext shape

The earned redesign is not a larger file taxonomy. It is a narrower one with a mechanical edge:

1. One portable project bootstrap routes to pulse.
2. Pulse routes to one live RUNBOOK and STATUS; it does not copy the gate.
3. RUNBOOK owns gate, participants, fixed holds, status owner, and schema version.
4. Revisioned STATUS owns the current recovery edge and is updated atomically by one owner.
5. PAD exists only for a human branch and contains one active step if reveal control matters.
6. Native vendor orchestration carries routine internal work; BUS is born only for the durable residual and retains POINT/RETURN/VERDICT semantics.
7. Evidence and decisions that outlive the gate are promoted outside the session.
8. A checked close transition records promotion and then prunes transient state.

The redesign preserves the system's best insight—files as cross-runtime continuity—while refusing to make files impersonate locks, transport daemons, native agent configuration, or proof.

## Sources consulted

Primary product documentation and repositories:

- [Claude Code: memory, instruction loading, enforcement distinction, auto-memory locality](https://code.claude.com/docs/en/memory)
- [Claude Code: custom subagents](https://code.claude.com/docs/en/sub-agents)
- [Claude Code: agent teams](https://code.claude.com/docs/en/agent-teams)
- [Claude Code: Advisor](https://code.claude.com/docs/en/advisor)
- [Claude Code: settings](https://code.claude.com/docs/en/settings)
- [OpenAI: Codex plugin for Claude Code](https://github.com/openai/codex-plugin-cc)
- [OpenAI: import from another agent](https://learn.chatgpt.com/docs/import)
- [OpenAI: Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [OpenAI: Codex AGENTS.md discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md)

Empirical and field evidence:

- [Gloaguen et al., “Evaluating AGENTS.md,” arXiv:2602.11988](https://arxiv.org/abs/2602.11988)
- [Lulla et al., “On the Impact of AGENTS.md Files,” arXiv:2601.20404](https://arxiv.org/abs/2601.20404)
- [Khatri, “Do Context Files Help Coding Agents?”, arXiv:2607.27250](https://arxiv.org/abs/2607.27250)
- [Treude & Baltes, “Context Rot,” arXiv:2606.09090](https://arxiv.org/abs/2606.09090)
- The linked Anthropic/OpenAI GitHub issues and Reddit report in Q14. Issue reports establish observed failure shapes, not population rates.

