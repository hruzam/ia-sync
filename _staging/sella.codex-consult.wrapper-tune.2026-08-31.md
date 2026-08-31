---
what: master prompt for a hand-released interactive Codex session — audit + tune codex-run.zsh
state: CONSULT BRIEF — Claude-authored (atlas-ui), for majkee to paste into `codex` directly
by: atlas-ui · office · 2026-08-31
unifies: input-edge quote-safety (relay ①/② this session) + output-edge Sella findings
         (dev-journal.sella.md: "silent voice" wrapper stdout gap · Wave "jq + sync exec")
apply-path: Codex emits a unified diff → apply to ~/ia-sync/zsh/ai/codex-run.zsh (table) →
            deploy → fresh-Codex verify (ia-sync/AGENTS.md rule). NOT auto-applied.
---

# The master prompt (paste everything below the line into interactive `codex`)

---

You are the Codex CLI, running interactively for the operator. I am consulting you as the
vendor-side authority on the `codex exec --json` lifecycle to AUDIT and then TUNE a wrapper
script that Claude-side relay agents (astrobley / vega / mirror) use to invoke you headlessly.

## Read first — ground truth (your self-knowledge is an inference; verify against these)

- `~/.config/zsh/ai/codex-run.zsh` — the wrapper under audit (~103 lines).
- `~/.config/zsh/guides/codex-relay.contract.md` — the relay contract, esp. the section
  "Prompt-passing discipline (quote safety)".

For EVERY claim below, label your finding **[VERIFIED** against actual CLI behavior / official
docs / the real `--json` event schema**]** or **[INFERRED]**. Do not present inference as fact —
this consult exists precisely because an agent's self-report of its own harness is not evidence.

## What the wrapper must do (unchanged invariants — do NOT break these)

Take a prompt (arbitrary text) + optional model; call
`codex exec --json --ephemeral --sandbox workspace-write [-m model] "$prompt" < /dev/null`;
survive two known bugs — stdin-hang (GitHub #20919, mitigated by the mandatory `< /dev/null`)
and silent-exit regression (GitHub #19945, mitigated by a `script -qfc` single retry); classify
failure into exit codes 3 (no turn.completed) / 4 (empty after retry) / 5 (auth·429·unknown
model); then return the FINAL agent_message text plus usage numbers. Keep `set -euo pipefail`.
Do NOT use `path` or `fpath` as variable names (reserved in zsh).

## Hypotheses to confirm or refute

### Input edge — quote safety
- **H1** A relay that inlines the prompt into a *double-quoted* shell argument lets backticks
  and `$( )` execute in the relay's OWN shell before you receive anything — a correctness break
  AND a host-command-injection vector.
- **H2** Passing the prompt via a single-quoted-delimiter heredoc, captured as
  `"$(cat <<'CDX_PROMPT'` … `CDX_PROMPT` … newline `)"`, delivers arbitrary bytes literally into
  `$1` with the CURRENT wrapper — no wrapper change required to be safe.
- **H3** Adding a native stdin mode — `codex-run - [model]` (or `--stdin`) doing
  `prompt="$(cat)"` (slurp stdin FIRST), while KEEPING `< /dev/null` on the `codex exec` call and
  KEEPING the positional `codex-run "<prompt>" [model]` form for back-compat — is safe and does
  not reintroduce #20919 (stdin is fully consumed before exec).

### Output edge — the "silent voice" and extraction findings
- **H4** The agent_message extraction (wrapper lines ~88–92) uses a greedy `sed` regex to pull
  `"text":"..."` then a partial unescape handling only `\n` and `\"`. This mis-parses when the
  JSONL `text` field contains escaped quotes, trailing JSON fields after `text`, or escape
  sequences beyond `\n`/`\"` (`\t`, `\\`, `\uXXXX`). Confirm against your ACTUAL `--json` event
  schema: name the exact event `type` that carries the final assistant text and the exact field
  path, and give the correct `jq` extraction. State the jq dependency and a graceful fallback if
  jq is absent.
- **H5** Usage numbers are printed only to stderr (line ~103). A relay that captures only stdout
  gets "silent voice" — no usage surfaced (observed in a live astrobley run). Confirm, and
  propose how the wrapper should emit usage so a relay reliably captures it (structured stdout
  tail vs. a documented stderr contract the relay is told to read).
- **H6** Wave's note: "both fixes needed — JSON-aware extract AND synchronous exec." Clarify what
  "synchronous exec" means for `codex exec`: is the current invocation fully synchronous, or is
  there a completion-signal race between `turn.completed` and stream close? Answer from the JSONL
  stream semantics.

## Deliverables

1. **Confirmation table** — each H → VERIFIED / REFUTED / PARTIAL, with the evidence (quote the
   relevant `--json` event shape or cite the CLI behavior). Mark INFERRED rows explicitly.
2. **A single tuned `codex-run.zsh` as a unified diff** against the current file that: adds the
   H3 stdin mode; replaces the H4 sed extraction with correct jq (+ fallback); fixes the H5 usage
   surfacing — while PRESERVING every invariant above (`< /dev/null`, positional back-compat,
   exit codes 3/4/5, the #19945 retry, `set -euo pipefail`, no `path`/`fpath`).
3. **A minimal self-test** you would run to prove the tune: the four quote hazards
   (`` `date` ``, `$(hostname)`, a double quote, an apostrophe) round-trip byte-literal to you;
   extraction survives a `text` value containing escaped quotes; usage surfaces to the relay;
   the positional form still works.

Do not remove the two bug mitigations. Do not assume jq without a fallback. Flag every claim you
can only infer rather than verify.

---

## After Codex answers (majkee / Flight)
- Apply the diff to `~/ia-sync/zsh/ai/codex-run.zsh` (surgical table), deploy, verify from a
  FRESH Codex session (ia-sync/AGENTS.md — unchanged file ≠ unchanged behavior).
- If H4/H5 land: they close the Sella "capable hands, silent voice" defect (dev-journal.sella.md
  2026-08-05) — log the resolution there.
- If H2 confirmed: the relay quote-safety rule ① is proven correct; H3 makes ② concrete.
