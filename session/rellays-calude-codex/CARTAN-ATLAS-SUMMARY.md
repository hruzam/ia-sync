# Codex relay repair — Cartan → Atlas + @majkee

`status: CONCENTRATED HANDOFF — current state + recommendations; not canon`
`by: @Cartan · office · 2026-09-01`
`audience: @majkee (gavel) · @Atlas (Claude harness builder)`
`coarchitecture: Cartan supplies Codex-native evidence/design review; Atlas owns Claude projection`

## Read this first — one-screen state

The original Atlas consult was correct about the main output defect: `codex-run.zsh` parsed
JSON with greedy `sed`, and usage lived only on stderr. The tabled repair now:

- accepts `codex-run - [model]` from a single-quoted heredoc;
- retains the positional form for backward compatibility;
- selects final assistant text from
  `item.completed.item.text` when `item.type == "agent_message"`;
- parses with jq, falling back to Python's JSON parser;
- appends `[usage: {...}]` on stdout;
- retains `set -euo pipefail`, `--ephemeral`, `--sandbox workspace-write`,
  `< /dev/null`, exit codes 3/4/5, and the `script -qfc` single retry;
- passes 2/2 deterministic wrapper tests without network, quota, or a Codex session record.

**Do not deploy yet.** Cartan found one retry-only injection boundary still open: the prompt is
escaped before `script -qfc`, but `CODEX_TIMEOUT` and the optional model are interpolated into
shell source without quoting. Harden and adversarially test that retry first.

The wrapper is already foreground/synchronous. Wave's “sync exec” warning concerned a relay
backgrounding the wrapper and returning before terminal state/usage came back; it was not
evidence of a `turn.completed` versus stream-close race inside the current wrapper.

## Exact map — what, where, why, owner, gate

| Part | State | Exact source | Why | Recommended owner / done when |
|---|---|---|---|---|
| Atlas brief | consumed | `session/rellays-calude-codex/RUNBOOK.md` | H1–H6 audit request | Keep as source brief; do not rewrite history |
| Wrapper repair | tabled, not deployed | `zsh/ai/codex-run.zsh` | safe stdin edge, JSON-aware final text, stdout usage | Cartan/implementer; done only after retry P0 + live probe |
| Deterministic test | new, 2/2 green | `zsh/ai/codex-run.selftest.zsh` | tests four quote hazards, last message, trailing JSON field, jq, Python fallback, positional form, usage | Extend with forced-retry adversarial lane |
| Canonical relay contract | tabled, not deployed | `zsh/guides/codex-relay.contract.md` | one plumbing truth for Astrobley/Vega/Mirror | Keep authoritative; deploy with wrapper after proof |
| Codex observation | complete, deploy-inert | `_staging/codex/cartan.observation.codex-relay-wrapper-boundary.2026-09-01.md` | evidence, curvature, promotion gates | Sella/Atlas point here; do not copy into canon |
| Claude seat projection | deferred | `claude/agents/{astrobley,vega,mirror}.md` | snippets still say stderr usage and show older heredoc | Atlas-owned pass after live wrapper proof |
| Historical builder/user guidance | stale-weather review needed | `~/reposoma/raw.guides/codex-builder-user/{codex-line.builder.md,codex-line.user.md}` | version 0.145 snapshot; cwd/economics claims drifted | Draft refresh; @majkee gavels shared-guide promotion |
| Durable receipt supervisor | no demonstrated requirement | Nablarva experimental bed, not `codex-run.zsh` | cross-run history/async recovery is a different primitive | Design only if a real consumer needs records |

Current working tree contains only the wrapper/contract/test/observation work plus this handoff.
Nothing has been deployed, committed, pushed, journaled into Sella, or written into reposoma or
Nablarva.

## H1–H6 — concentrated verdict

| H | Verdict | Evidence and consequence |
|---|---|---|
| H1 — double-quoted inline prompt | **VERIFIED, with scope** | Shell syntax placed literally inside a generated command is evaluated before the wrapper sees it. Passing an already-populated variable as `"$prompt"` is not recursive evaluation; the danger is command-string construction/eval/tool command composition. Prefer quoted heredoc stdin. |
| H2 — captured quoted heredoc is arbitrary-byte literal | **PARTIAL** | It protects backticks, `$()`, quotes, `$`, and embedded newlines. It is not arbitrary bytes: shell variables cannot hold NUL, and command substitution removes trailing newlines. Existing callers remain safe for shell text. |
| H3 — wrapper stdin mode | **VERIFIED** | The wrapper slurps stdin first, then invokes Codex with the prompt as an argument and keeps Codex stdin on `/dev/null`; the stdin-hang mitigation remains. |
| H4 — greedy `sed` parser is wrong | **VERIFIED** | Current OpenAI JSONL shape carries final text at `.item.text` on `type == "item.completed"` with `.item.type == "agent_message"`; usage is `.usage` on `turn.completed`. jq/Python now parse JSON rather than escapes by regex. |
| H5 — stderr-only usage is lost | **VERIFIED** | Old line 103 wrote usage to fd 2. A relay returning raw stdout could omit it. New stdout tail makes final text + usage one return contract. |
| H6 — JSON parser plus synchronous exec | **PARTIAL / terminology corrected** | Both concerns matter, but at different boundaries. The wrapper was already synchronous. The observed race was caused by relay-level background dispatch. Keep wrapper calls foreground; do not invent another internal sync mechanism. |

Current OpenAI authority, retrieved 2026-09-01:
<https://developers.openai.com/codex/noninteractive/>. Historical reports do not override it.

## What changed on the surgical table

### `zsh/ai/codex-run.zsh`

Input:

```zsh
codex-run - "$model" <<'CDX_PROMPT'
…untrusted prompt text…
CDX_PROMPT
```

The old `codex-run "<prompt>" [model]` form still works.

Output:

```text
<final agent message, decoded by JSON parser>
[usage: {"input_tokens":...,"cached_input_tokens":...,"output_tokens":...,"reasoning_output_tokens":...}]
```

The parser takes the last matching completed agent message and last `turn.completed` usage.
If jq is absent, Python's standard `json` module performs the same extraction. If neither is
present, the wrapper exits 3 with a diagnostic rather than silently returning corrupted text.

### `zsh/ai/codex-run.selftest.zsh`

The test substitutes a local fake `codex`; it does not contact OpenAI. It proves:

- stdin quote hazards remain literal: `` `date` ``, `$(hostname)`, `"`, and `'`;
- the last of multiple `agent_message` items wins;
- a field after `text` does not contaminate extraction;
- escaped quote/backslash/tab/Unicode content survives JSON decoding;
- usage appears on stdout;
- positional compatibility remains;
- both jq and Python fallback lanes work.

It does **not** prove current live Codex initialization, authentication, event ordering under
real execution, or absence of a version-specific CLI regression. That is the P1 fresh probe.

### `zsh/guides/codex-relay.contract.md`

The contract now makes stdin heredoc preferred, captured heredoc backward-compatible, NUL
explicitly out of contract, and stdout usage authoritative.

## P0 — retry hardening before deploy

Normal invocation is argument-safe:

```zsh
timeout "$timeout_val" codex exec … "${model_flag[@]}" "$prompt" < /dev/null
```

The silent-exit retry currently re-enters shell parsing through:

```zsh
script -qfc \
  "timeout ${timeout_val} … ${model_flag[*]-} $(printf '%q' "$prompt") < /dev/null" \
  /dev/null
```

Static source inspection verifies:

- prompt receives zsh `%q` escaping;
- model and timeout do not;
- the shell chosen by `script(1)` is assumed to understand zsh's `%q` output.

Recommended repair invariant:

1. Keep `script -qfc` and exactly one retry.
2. Make the `-c` program fixed—no prompt/model/timeout interpolation into program text.
3. Select zsh explicitly for the retry.
4. Carry prompt, model, and timeout through positional parameters or environment values.
5. Rebuild `model_flag` as an array inside that zsh.
6. Keep `< /dev/null` on the actual Codex invocation.
7. Add a forced-silent-first-call fixture proving that `;`, `$()`, backticks, whitespace,
   quotes, and newlines in prompt/model remain data and execute nothing.

Cartan recommendation: this is a pre-deploy gate, not a future cleanup, because the entire task
is about keeping untrusted relay text out of host-shell syntax.

## P1 — live proof after P0

Run in this order under the normal ia-sync discipline:

1. `zsh -n zsh/ai/codex-run.zsh zsh/ai/codex-run.selftest.zsh`
2. `zsh/ai/codex-run.selftest.zsh`
3. `bash deploy.sh --dry-run` — inspect intended files only.
4. `bash deploy.sh` — only after @majkee's deploy gate.
5. Confirm table and live wrapper/contract are byte-identical.
6. Count `~/.codex/sessions` files before the probe.
7. Run one fresh `codex-run -` probe using the four literal hazards and a response containing
   escaped quotes/backslash/tab/Unicode.
8. Verify: correct final text; one stdout usage line; foreground completion; exit 0; no raw JSON
   leakage; no extra persisted session file (`--ephemeral`).
9. Exercise one classified failure fixture for exits 3/4/5 without spending a second live turn.

The earlier managed probe failed before a turn because `~/.codex` was mounted read-only. That is
environment evidence, not a CLI lifecycle verdict. Run P1 from a normal fresh Codex/terminal
frame where ephemeral initialization can write whatever non-session runtime state it requires.

## Relay recommendations — architecture, not just syntax

### One pipe, three refusal contracts

Keep one shared transport (`codex-run.zsh` + `codex-relay.contract.md`) and three Claude relay
seats with distinct preconditions:

- Astrobley refuses vague implementation scope.
- Vega refuses a prior position so it can return a blind second signal.
- Mirror requires a position and attacks its weakest assumption.

Do not duplicate wrapper logic into the cards. Do not collapse the refusal contracts merely
because the plumbing is shared; that would destroy the intended decorrelation.

### Foreground is the default contract

Every relay should wait for the wrapper's terminal result and return its stdout verbatim. If a
relay backgrounds the wrapper, it must no longer claim the synchronous relay contract. Async
requires a separate job identity, terminal state, receipt location, recovery procedure, and
record policy.

### One return channel

Successful stdout is:

```text
final agent text
[usage: {...}]
```

Failure diagnostics remain stderr plus wrapper exit 3/4/5. Relay cards should not reconstruct
JSON, decode escapes, or hunt detached stderr for successful usage.

### Records are opt-in architecture

`--ephemeral` means the normal relay does not persist session rollouts. Wave's proposed
`runs/<id>/…` receipt ledger is valuable only when a consumer needs cross-run supervision,
historical budgeting, CI recovery, or async completion. It must not silently appear inside the
one-shot wrapper.

If that requirement arrives, route the prototype to Nablarva's experimental bed. Define:

- who authorizes record creation;
- request/event/final/receipt schemas;
- atomic `running → completed|failed` transition;
- retention and redaction;
- supervisor sandbox and credential boundary;
- native-event versus derived-event precedence;
- resume/retry semantics.

This follows Asymmetry's strongest point: Codex's outside edge—JSONL/app-server/external
evaluation—is powerful, but wrapping it in more state without better evidence, isolation, or
recoverability is architectural theatre.

## Atlas task routing

Atlas can consume this handoff by part:

### A. If Atlas is reviewing the Codex wrapper

Read:

1. this file §§ H1–H6, P0, P1;
2. `zsh/ai/codex-run.zsh`;
3. `zsh/ai/codex-run.selftest.zsh`;
4. `_staging/codex/cartan.observation.codex-relay-wrapper-boundary.2026-09-01.md`.

Return: challenge the retry-hardening design and the acceptance gates. Do not rewrite Codex
mechanics into Claude-native approximations.

### B. If Atlas is updating Claude relay cards

Wait until P1 passes, then edit only:

- `claude/agents/astrobley.md`
- `claude/agents/vega.md`
- `claude/agents/mirror.md`

Change only the stale transport projection:

- preferred invocation becomes `codex-run - "$model" <<'CDX_PROMPT'`;
- captured heredoc remains documented as backward-compatible if useful;
- usage is already the final stdout line and must be preserved, not appended from stderr;
- foreground dispatch is explicit;
- exit 3/4/5 behavior remains unchanged.

Do not alter each seat's refusal contract, persona, model, or task geometry in this pass.

### C. If Atlas is refreshing shared knowledge

Treat these as historical sources:

- `~/reposoma/raw.guides/codex-builder-user/codex-line.builder.md`
- `~/reposoma/raw.guides/codex-builder-user/codex-line.user.md`
- `~/unikuklatrix/nablarva/meshup/natural-ladders-grounded-phase.a-sym/`
  `asymmetry.codex-bonding-layer.research.2026-08-05.md`

Known drift to carry into a proposal, not silently edit:

- guide baseline `codex-cli 0.145.0`; installed observation is 0.150.1;
- “no cwd flag” is stale—current local help has `-C, --cd <DIR>`;
- 16–45K input-token economics conflicts with a prior 258,594-token cold probe;
- current JSONL/event claims should cite dated OpenAI documentation;
- stable wrapper doctrine and volatile CLI/quota weather should be separated.

Reposoma canon/shared guidance remains @majkee-gaveled. Do not modify Nablarva's settled locks
to absorb a wrapper observation.

## Co-architecture contract

- **@majkee:** gavel, deploy authority, canon/shared-guide promotion.
- **@Atlas:** interactive Claude harness builder; owns the minimal Claude-side projection after
  confirmation and proof.
- **@Cartan:** Codex resident/controller and Codex-native coarchitect; owns evidence synthesis,
  retry-boundary recommendation, test/verification review, and curvature reporting. Cartan does
  not become another relay seat.
- **Wave / Asymmetry:** family evidence and architectural lenses, not current runtime authority.
  Their contribution is strongest at the external-supervisor boundary; current OpenAI docs and
  observed local behavior decide volatile CLI facts.

The invariant shared across Atlas and Cartan is `harness_builder`: smallest native primitive,
one authority boundary, explicit activation/write scope, and behavior proof before promotion.
The runtime renderings differ naturally; parity is not the goal.

No new agent, hook, receipt ledger, or exchange mechanism is recommended for this repair.
`HANDSHAKE.md` is referenced by the ia-sync instructions but absent from this checkout; this
handoff therefore uses the already-authorized session file rather than inventing a substitute.

## Decision card for @majkee

Recommended call:

1. **Accept** the stdin/JSON parser/stdout-usage direction.
2. **Hold deploy** until retry P0 is fixed and its adversarial fixture passes.
3. After P1 live proof, **authorize Atlas** to align only the three relay transport snippets.
4. Keep persistent receipts **out of this wrapper**; open a Nablarva design task only when an
   async/cross-run consumer is named.
5. Treat the reposoma guide refresh as a separate, dated promotion task.

That sequence closes the observed “capable hands, silent voice” defect without turning a small
relay pipe into a second orchestration platform.
