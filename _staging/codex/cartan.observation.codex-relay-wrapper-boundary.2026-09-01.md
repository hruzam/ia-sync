# Cartan observation — Codex relay wrapper boundary after JSONL repair

`status: OBSERVATION — deploy-inert; recommendations, not canon`
`by: @Cartan · office · 2026-09-01`
`scope: codex-run JSONL repair · retry quoting · receipt boundary · source drift`

## Evidence cross-section

- Current surgical-table sources: `zsh/ai/codex-run.zsh`,
  `zsh/ai/codex-run.selftest.zsh`, and `zsh/guides/codex-relay.contract.md`.
- Sella line: `_staging/dev-journal.sella.md` and
  `_staging/radio.wave-to-atlas.sella-consultation.2026-08-05.md`.
- Historical builder/operator guides:
  `~/reposoma/raw.guides/codex-builder-user/{codex-line.builder.md,codex-line.user.md}`.
- Historical architecture snapshot:
  `~/unikuklatrix/nablarva/meshup/natural-ladders-grounded-phase.a-sym/`
  `asymmetry.codex-bonding-layer.research.2026-08-05.md`.
- Current authority: OpenAI, “Non-interactive mode,” retrieved 2026-09-01:
  <https://developers.openai.com/codex/noninteractive/>.
- Installed runtime observed 2026-09-01: `codex-cli 0.150.1`.

The reposoma guides and Nablarva research are historical evidence, not current product
authority. The OpenAI page currently documents `--ephemeral`, JSONL on stdout,
`item.completed.item.text` for an `agent_message`, and usage on `turn.completed`.

## Observed transition

The tabled wrapper repair closes the failure named by Sella and the earlier Cartan temple-map
probe:

- stdin mode accepts a quoted heredoc without placing untrusted text inside a generated shell
  command;
- jq, with Python JSON fallback, selects the final
  `item.completed` whose `item.type` is `agent_message`;
- usage is emitted on the same stdout return path as the final message;
- the wrapper remains foreground/synchronous and uses `--ephemeral`;
- deterministic fixture tests pass through both parser lanes without a Codex call or session
  record.

This has not been deployed or verified against a fresh live Codex invocation. The managed
session could inspect CLI help, but an ephemeral probe failed before the turn because the
runtime could not initialize against the read-only `~/.codex` mount. The test receipt is
therefore wrapper-level, not end-to-end runtime proof.

## Curvature found

### 1. “Synchronous exec” named two different boundaries

The current wrapper already waits for `codex exec` to finish before parsing its captured
stream. Wave's n=4 failure concerned a relay backgrounding the wrapper, detaching terminal
state and stderr from the relay lifecycle. There is no evidence here of a race between
`turn.completed` and stream close inside the foreground wrapper.

Recommendation: keep the relay call foreground. If asynchronous UX is later required,
background the whole receipt-producing job and give that job a real lifecycle contract.

### 2. A durable run directory is a different primitive

Wave's conceptual `runs/<run-id>/{request.md,events.jsonl,final.md,stderr.log,receipt.json,`
`exit-status}` is useful when supervision depends on multiple sessions, historical state,
budgets, CI, or recovery. It is not a free reliability improvement to the present one-shot
relay: it changes an explicitly ephemeral call into a record-producing subsystem, adds
retention and credential questions, and places an unsandboxed supervisor around a sandboxed
agent.

This matches the Nablarva snapshot's decision gate: use external supervision for cross-run or
historical decisions, and do not duplicate lifecycle semantics without precedence.

Recommendation: keep `codex-run.zsh` as the small synchronous result pipe. If durable receipts
become a real requirement, design a separate supervisor in Nablarva's experimental bed with an
explicit record-consent gate, schema, retention policy, sandbox, and failure-state transition.

### 3. Retry-only command construction still crosses the quote boundary

**[VERIFIED by static source inspection]** The normal path passes model and prompt as array/
quoted arguments. The silent-exit retry instead builds shell source for `script -qfc`:

```text
timeout ${timeout_val} ... ${model_flag[*]-} $(printf '%q' "$prompt")
```

The prompt is escaped, but `CODEX_TIMEOUT` and the optional model are interpolated into the
command string without shell quoting. A model value containing shell syntax would become
active only on the silent-exit retry path. The retry also relies on the shell chosen by
`script(1)` understanding zsh's `%q` rendering.

Recommendation — **pre-deploy hardening gate**: make the retry command text fixed. Pass timeout,
model, and prompt as positional parameters or environment values to an explicitly selected zsh,
rebuild the model array inside that shell, and add an adversarial retry fixture covering `;`,
`$()`, backticks, whitespace, quotes, and newlines. Preserve the `script -qfc` single retry and
`< /dev/null` mitigation.

### 4. Shared prose now trails the canonical contract

The Astrobley and Vega cards still say usage comes from stderr; Astrobley, Vega, and Mirror
still show the older command-substitution heredoc. The older call remains compatible, and each
card declares the shared relay contract authoritative, so this is documentation drift rather
than a current functional break.

Recommendation: after the wrapper passes its live gate, update the three card snippets in one
Claude-owned pass: stdin heredoc as preferred, positional heredoc as back-compat, and stdout
`[usage: ...]` preservation.

### 5. The requested historical guides contain weather

The builder guide is stamped for `codex-cli 0.145.0`; the installed CLI is 0.150.1. At least one
statement is now stale: the guide says there is no cwd flag, while current local help exposes
`-C, --cd <DIR>`. The 16–45K exec-cost estimate also conflicts with the earlier Cartan probe's
258,594 input-token receipt. Neither figure should be silently promoted as current economics.

Recommendation: leave both guides historical until a gaveled refresh. A refresh should separate
stable wrapper doctrine from dated CLI/version/quota observations and attach retrieval dates to
each volatile claim.

## Ranked next gates

1. **P0 — before deploy:** harden and adversarially test the `script -qfc` retry boundary.
2. **P1 — behavior proof:** deploy dry-run, deploy, then run one fresh `--ephemeral` relay probe;
   verify final text, stdout usage, exit status, stream completion, and unchanged session-file
   count.
3. **P1 — Claude projection:** align Astrobley/Vega/Mirror snippets with the canonical contract.
4. **P2 — shared knowledge:** propose a dated refresh of `codex-line.builder.md` and
   `codex-line.user.md`; @majkee gavels any shared-guide promotion.
5. **P2 — only on demonstrated need:** prototype durable receipt supervision in Nablarva, not
   inside the small wrapper.

## Promotion boundary

This file is the recommendation record. It does not alter Sella's journal, reposoma guides,
Nablarva canon, deployed zsh, or live Codex state. Sella may point here as the Codex-side
closure/curvature note; durable conclusions promote by meaning only after their respective
owner and @majkee review them.
