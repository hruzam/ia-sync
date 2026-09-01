# Codex relay — canonical plumbing contract

**Authoritative source for the shared plumbing of the Codex relay family:
@Astrobley (coder) · @Vega (blind crosscheck) · @Mirror (adversarial challenger).**
Point here, never copy (Janus verdict 2026-07-31: "the plumbing wants to be one;
the contract must stay two" — seats keep their opposite refusal contracts, this file
holds the shared delivery layer). Each agent carries a minimal self-contained snippet
(wrapper path + exit codes) so it functions if this file is unreachable; on any
divergence, THIS file wins and the agent snippet is stale.

## Wrapper

- **One path:** `~/.config/zsh/ai/codex-run.zsh` (mounted via ia-sync deploy).
  The old `.larva/agents-staging/` fallback is DEAD (dir deleted 2026-07-30) — no
  agent may reference it.
- Never call `codex exec` bare. One call per brief/task; no follow-up exchanges
  beyond the wrapper's built-in single retry.

## Prompt-passing discipline (quote safety) — the brief is untrusted text

The brief / master prompt is **arbitrary text**: it may contain backticks, `$`, `$( )`,
`"`, `'`, and newlines. All are shell-active. How the relay hands this text to the wrapper
decides whether the primary prompt survives the trip — and whether the relay's own host
shell stays safe. (The wrapper itself is not the risk: it reads the prompt as `$1`, an inert
string, and the retry path uses `printf '%q'`. The break happens one layer up, when the
agent composes the Bash command that calls the wrapper.)

**Never inline the prompt in double quotes.** Inside `"..."` the shell STILL runs
`` `...` `` and `$( )` and expands `$VAR` — a brief containing `` `rm -rf ~` `` or
`$(...)` EXECUTES in the relay's own host shell before Codex ever sees it. This is both a
break (truncated / garbled prompt) and an injection vector (brief text → host command).

**PREFERRED — wrapper stdin mode.** A heredoc whose delimiter is single-quoted disables
ALL expansion; pass it directly to the wrapper so no command substitution is needed:

```bash
~/.config/zsh/ai/codex-run.zsh - "$model" <<'CDX_PROMPT'
…brief, verbatim, any characters…
CDX_PROMPT
```

- The quote on `'CDX_PROMPT'` is **load-bearing** — it turns off expansion. Unquoted, the
  body would expand again.
- The closing `CDX_PROMPT` MUST sit at **column 0** with no leading indentation and no trailing
  space, or the heredoc never terminates. A relay composing this must not indent the delimiter
  line; a human pasting an indented example will get a hang (verified in P1, 2026-09-01).
- Other failure mode: a body line exactly equal to the delimiter. Use a rare sentinel
  (`CDX_PROMPT`), never `EOF`.

**BACK-COMPAT — quoted heredoc captured as one argument.** The original form remains safe
for shell-active characters and existing callers:

```bash
~/.config/zsh/ai/codex-run.zsh "$(cat <<'CDX_PROMPT'
…brief, verbatim, any characters…
CDX_PROMPT
)" "$model"
```

`"$( … )"` keeps the captured text in one argument. It is not an arbitrary-byte transport:
shell variables cannot contain NUL, and command substitution removes trailing newlines.

**FALLBACK — arg form (only if a heredoc is impossible).** Single-quote the whole prompt;
escape every embedded `'` as `'\''`. Never double-quote. (The unescaped `'` closing the
string early is the "accidentally doubled apostrophe" break.)

**This is the VERBATIM contract at the input edge for shell text.** A quoting break silently
mutates the brief before the mirror/blind geometry sees it — corrupting exactly the
decorrelation these seats exist to provide. NUL bytes are outside the wrapper contract.

## Exit codes (graceful-fail, shared by all three seats)

| exit | meaning | relay behavior |
|---|---|---|
| 3 | no `turn.completed` | return `[<SEAT> UNAVAILABLE: no turn.completed — raw diagnostic on stderr]` |
| 4 | empty stream after retry | return `[<SEAT> UNAVAILABLE: silent-exit regression — stream empty after retry]` |
| 5 | auth / 429 / unknown model | return `[<SEAT> UNAVAILABLE: upstream error — <verbatim error text>]` — LOUD, needs operator |

**Never block the caller.** On UNAVAILABLE the orchestrator continues. Cross-vendor
seats (Vega/Mirror) may be backed up by a same-vendor Claude seat, but any such verdict
MUST be labeled `SAME-VENDOR FALLBACK — decorrelation not achieved`. Silent fallback is
the one outcome worse than no answer.

## Return discipline

- Codex output comes back **VERBATIM** — no summary, no editorializing, no reconciling,
  no self-assessment. Re-interpretation by the relay re-correlates the answer toward
  Claude priors and destroys the decorrelation the seat exists to provide.
- The wrapper appends usage numbers to stdout as a final `[usage: ...]` line; preserve that
  line in every report.

## Economics (E1)

Each call costs 16–45K input tokens against the shared ChatGPT Plus quota (5h rolling
window). Batch; bounce micro-tasks (<~10 expected lines) back with a batching suggestion.

## The contract split (why three seats, one plumbing)

| seat | brief precondition | function |
|---|---|---|
| @Astrobley | refuses VAGUE scope | relay coder — well-scoped implementation |
| @Vega | refuses a POSITION (blind) | position-free second opinion / triangulation |
| @Mirror | REQUIRES a position | adversarial audit — attack the weakest assumption |

Intent lives in **which seat you spawn** — visible in the trace, never inferred by the relay.

---
*Established 2026-07-31 (transition session, majkee gaveled). Companion:
`codex-relay.metadata-scripting.2026-07-31.md` (Epoch practitioner guide, same folder).*
