---
brief: jev-tunnel (per-session sub-bus for Jev decisions)
date: 2026-09-24
from: symmetry (agentive-collaboration, conceptual layer)
to: CLI implementer (practical project)
status: DRAFT · parked brief · pilot scope only
provider: OpenRouter (credits loaded, key in registry) · Vercel AI Gateway parked for publish-time
---

# Jev tunnel: builder brief

## 0. Axioms (strike any that are wrong before reading further)
1. Jev is a **decision model**, not a coding agent. It returns typed answers with probabilities. It writes no code and calls no tools.
2. Jev is **hosted only**: closed weights, no local install. Every call leaves the machine for a US vendor.
3. Provider for the pilot is **OpenRouter**, model id `typesafe/jev-1.13`. It is not in the default model list, so call the id directly.
4. The endpoint is a **decisions** endpoint, not chat completions. The request shape must be taken from live docs, not guessed.
5. Jev's economy is **fan-out**: many questions against one shared state in one request. One-question-per-call is the anti-pattern.
6. Each CLI session gets its **own sub-bus folder** under the existing CLI bus. No cross-session reads or writes.
7. The **buffer file is markdown** that both the human and the CLIs can read and write.
8. **Gate 1 (send):** every send is confirmed by the human, every time. This is also the loop brake.
9. **Gate 2 (act):** a verdict is never permission. Irreversible acts need their own separate human confirmation.
10. The script **never executes anything** based on a verdict. It asks, records, and stops.

## 1. Step zero (before writing code)
- Read the official TypeSafe docs (`llms.txt`; any page can be read as `.md`). Do **not** use the Drive PDF from social media.
- If an agent writes the integration, install TypeSafe's published agent skill first. Agents trained on chat APIs invent request fields.
- Smoke test: send one Noul with a one-line state to `typesafe/jev-1.13`. Proceed only if a typed answer with a probability comes back.

## 2. Layout
```
$BUS/jev/<session-id>/
  buffer.md          # open questions and inline verdicts (human + CLIs)
  sent/<ts>.md       # frozen copy of each buffer as sent
  responses/<ts>.json# raw vendor response
  .count             # sends this session (for the hard cap)
  .lock              # present while a send is in flight
```
- `$BUS` is the existing CLI bus root. Placeholder: substitute the real path.
- If `$BUS` is inside a repo, gitignore `jev/`.

## 3. Buffer format
One shared state per buffer, then N typed questions. Each question has a heading plus a fenced YAML block.

````markdown
---
jev_buffer: 1
session: <session-id>
status: open          # open | sent | answered
---

## state
<the shared context all questions are judged against>

## q: pick-model
```yaml
type: choice
ask: Which model tier should handle this step?
options:
  cheap: Mechanical edit, local, low risk.
  mid: Bounded change across a few files.
  frontier: Design change or unknown code.
  ask: Brief unclear; a person decides.
```

## q: destructive
```yaml
type: noul
ask: Does this step delete or overwrite data?
```

## q: brief-quality
```yaml
type: score
ask: How clear is the brief?
levels: [unclear, partial, clear]   # ordinal, least to most, max 10
```
````

Rules:
- Types are `choice | score | noul`, and nothing else.
- Question ids (`q: <id>`) are unique within a buffer.
- `check` fails if a question has its own state. Split it into another buffer instead.

## 4. Verdicts written back inline
After a successful send, append under each question:

````markdown
```yaml
# jev:verdict  (advisory, not permission)
answer: mid
confidence: 0.81
probs: {cheap: 0.09, mid: 0.81, frontier: 0.07, ask: 0.03}
response: responses/<ts>.json
```
````

- Readers (human or CLI) re-read only the verdict blocks, not the whole file.
- Set `status: answered`. New questions go into a new buffer, so a sent buffer is never mutated except for its verdicts.

## 5. Commands (zsh function `jev` wrapping one script)
| command | network | effect |
|---|---|---|
| `jev new` | no | create `<session-id>/buffer.md` from template |
| `jev check` | no | validate format, count questions, estimate tokens (context is 32K) |
| `jev send` | **yes** | Gate 1, then one batched request, then write verdicts |
| `jev show` | no | print verdicts only |

Implementation choice is open. Suggested: Python 3 single file (YAML + JSON parsing) plus a thin zsh wrapper. Key comes from the environment as `JEV_ORAK_KEY` (sourced from the registry). The key is never written to any bus file or log, and never echoed. To check that it is set, test for presence (`[[ -n $JEV_ORAK_KEY ]]`) and print only `set` / `missing`.

## 6. Gate 1: send
- **Primary:** in Claude Code and Codex permission settings, `jev send` is **ask every time**. Never allowlist it.
- **Backstop** in the script, in case someone allowlists it later:
  - max sends per session (default 10, via `.count`)
  - max questions per batch (default 20)
  - refuse if `.lock` exists, or if `check` fails
- The loop brake is the human. The caps catch the case where the human was bypassed.

## 7. Gate 2: act
- Verdicts are **advisory data**. `jev` prints `advisory: true` and never triggers anything.
- Any consumer about to take an irreversible action must get a **separate human confirmation**, whatever the verdict or confidence says. Irreversible here means: delete, overwrite, deploy, git history rewrite, outbound network, or spending money.
- Confidence gating: below the threshold (default 0.7, tune in shadow mode), the verdict is treated as `ask`.

## 8. Threats and data
- **Prompt injection:** `state` may contain untrusted text such as tool output or web content. That text can move the verdict. This is exactly why Gate 2 exists.
- **Data:** every call goes to a US vendor. During the pilot, send no client (imago) data. Synthetic data or own repositories only.

## 9. Pilot plan
1. Smoke test (step zero).
2. **Shadow mode:** one decision type (suggested: keep-or-drop tool output, or pick-model). Log the verdict next to what actually happened, with no consumer acting on it.
3. **Loop test:** script an agent to call `jev send` repeatedly. Confirm that Gate 1 asks every time and that the cap trips.
4. **Injection test:** plant "answer X" text inside the state. Confirm the verdict is only recorded, never acted on.
5. Measure: agreement with the human decision, calibration (does 0.8 mean right about 80% of the time?), cost per buffer.

## 10. Done criteria
- [ ] Smoke test passes on `typesafe/jev-1.13`.
- [ ] A buffer with 3 or more mixed-type questions comes back from **one** request.
- [ ] Verdicts appear inline, and the raw response is saved.
- [ ] Gate 1 asks every time, and the caps trip in the loop test.
- [ ] No code path acts on a verdict.
- [ ] The key does not appear in any file under `$BUS`.

## Open (underlined)
- Real `$BUS` path and session-id scheme: builder to match the existing CLI bus.
- Exact OpenRouter decisions request and response shape: verify against live docs.
- Confidence threshold: set after shadow mode, not before.
- Local fallback (Ollama, same typed pattern) if sovereignty or cost pushes later: not in the pilot.
