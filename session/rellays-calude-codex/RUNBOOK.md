You are the Codex CLI, running interactively for the operator. I am consulting you as the vendor-side authority on the codex exec --json lifecycle to AUDIT and then TUNE a wrapper script that Claude-side relay agents (astrobley / vega / mirror) use to invoke you headlessly.

Read first — ground truth (your self-knowledge is an inference; verify against these):
- ~/.config/zsh/ai/codex-run.zsh — the wrapper under audit (~103 lines).
- ~/.config/zsh/guides/codex-relay.contract.md — the relay contract, esp. "Prompt-passing discipline (quote safety)".

For EVERY claim below, label your finding [VERIFIED against actual CLI behavior / official docs / the real --json schema**]** or [INFERRED]. Do not present inference as fact.

Invariants the wrapper must keep (do NOT break): take a prompt + optional model; call codex exec --json --ephemeral --sandbox workspace-write [-m model] "$prompt" < /dev/null; survive stdin-hang (#20919, via mandatory < /dev/null) and silent-exit (#19945, via a script -qfc single retry); classify failure into exit codes 3/4/5; return the final agent_message text + usage numbers. Keep set -euo pipefail. Never use path/fpath as var names (zsh reserved).

Hypotheses — confirm or refute:

Input edge (quote safety):
- H1 Inlining the prompt in a double-quoted shell arg lets backticks / $( ) execute in the relay's own shell before you receive it — a break AND a host-injection vector.
- H2 Passing it via a single-quoted-delimiter heredoc captured as "$(cat <<'CDX_PROMPT' … CDX_PROMPT newline )" delivers arbitrary bytes literally to $1 with the CURRENT wrapper — no change needed.
- H3 A native stdin mode — codex-run - [model] doing prompt="$(cat)" (slurp first), keeping < /dev/null on the exec call and keeping the positional form for back-compat — is safe and does not reintroduce #20919.

Output edge:
- H4 The agent_message extraction (lines ~88–92) uses a greedy sed regex + partial unescape (\n, \" only) — mis-parses on escaped quotes, trailing JSON fields, or escapes beyond \n/\". Confirm against your actual --json event schema: name the exact event type carrying final assistant text and the field path, and give the correct jq extraction (+ fallback if jq absent).
- H5 Usage prints only to stderr (line ~103); a relay capturing only stdout returns "silent voice" (observed live in astrobley). Confirm and propose how the wrapper should emit usage so a relay reliably captures it.
- H6 Wave's note: "both fixes needed — JSON-aware extract AND synchronous exec." Clarify what "synchronous exec" means for codex exec — is there a completion-signal race between turn.completed and stream close? Answer from JSONL stream semantics.

Deliverables: (1) a confirmation table H1–H6 → VERIFIED/REFUTED/PARTIAL with evidence; (2) a single tuned codex-run.zsh as a unified diff adding H3 stdin mode, replacing H4 sed with jq (+fallback), fixing H5 usage — preserving every invariant above; (3) a minimal self-test proving the four quote hazards round-trip byte-literal, extraction survives escaped quotes, usage surfaces, positional form still works. Do not remove the two bug mitigations. Do not assume jq without a fallback. Flag every inferred claim.