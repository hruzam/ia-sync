# Guide: Invoking Gemini Agents

> **⚕ Cut on the surgical table.** This file is deployed from `~/ia-sync` (the surgical
> table — the like-composer syncing both machines). Do not edit it in place: cut in
> ia-sync, deploy outward. Before trusting any machine fact here, reality-check the sync
> part: `git -C ~/ia-sync log --oneline -5 -- zsh/guides/guide-for-user.md` (intent) **and** repo↔live
> `rsync -n` (reality). Commits say what *should* be deployed; only the diff says what *is*.

`~/.config/zsh/guides/guide-for-user.md`

---

## Quick reference

| Alias | Seat | Model | Use case |
|---|---|---|---|
| `g-vega [task]` | Vega — Architect/Advisor | gemini-2.5-pro | Structural decisions, cross-phase synthesis, drift detection |
| `g-orby [task]` | Orby — Researcher | gemini-2.5-flash | Web research, citations, volatile facts |
| `g-astro [task]` | Astrobley — Implementer | gemini-3.5-flash | Load-bearing code, large refactors, tool-call-heavy tasks |
| `g-astro-yolo [task]` | Astrobley — YOLO | gemini-3.5-flash | Auto-approval mode — use deliberately |
| `g-bluebottle [blob]` | Bluebottle — Synthesizer | gemini-2.5-flash | Second-model synthesis of research blobs (headless REST) |

---

**Note:** The Gemini REST seats (orby, vega, bluebottle, astrobley) answer from model weights only — no live web access. For date-sensitive or current-version facts, use the Claude-line @Epoch instead. Orby is for synthesis and general research passes.

---

## UI session (interactive)

Launch with no argument → opens the agent's interactive REPL:

```bash
g-vega           # Vega: architect/advisor session
g-orby           # Orby: researcher session
g-astro          # Astrobley: implementer (approval required by default)
g-astro-yolo     # Astrobley: auto-approval ⚠ deliberate opt-in — TTY only, never from scripts/capture (Class B hang)
```

Inside the CLI:
- `/agents` — switch seat mid-session
- `/model` — verify the active model hasn't silently switched (Gemini 2.5 Pro is known to auto-downgrade to Flash under load)
- `/compress` — compress context (use every ~20-30 turns to prevent token bloat)

Bluebottle has no interactive mode — it is headless-only.

---

## Headless one-shot

Pass a task argument → runs headless, prints response, exits:

```bash
g-vega "review this phase plan for drift"
g-orby "what is the current gemini-cli stable version"
g-astro "add pagination to UsersController"
```

Each headless call is a fresh session — no context accumulation between calls.

---

## Bluebottle synthesis (second-model pass)

Bluebottle is headless-only — synthesizes a research blob via REST:

```bash
# Inline argument:
g-bluebottle "your research blob here"

# Stdin pipe:
cat report.md | g-bluebottle

# File argument:
g-bluebottle path/to/blob.md
```

Output format: `## @BlueBottle cross-check\n\n<synthesis>`

For a **raw pass without any agent persona** (no `@name` injection, no GEMINI.md context):
```bash
GEMINI_SYSTEM_MD=false gemini -p "your raw prompt here"
# Or via stdin pipe:
echo "prompt" | GEMINI_SYSTEM_MD=false gemini -p ""
```

---

## Hygiene

- **Fresh session** (token-clean context): `gemini-fresh` / `agy-fresh` — spins a new clean-context subshell.
- **Compress mid-session**: type `/compress` inside the CLI every ~20-30 turns. Note: if context is very large, compression may fail (bug #8609 — use session restart as fallback).
- **Stateless headless** (best mitigation for #8609): prefer `g-vega "task"` over long interactive sessions. Each headless call starts fresh — no `thoughtSignature` accumulation.
- **Model verification**: use `/model` to confirm the active model. Gemini 2.5 Pro has a known silent auto-downgrade to Flash under backend load — verify before relying on pro-depth reasoning.
- **Do NOT use** `gemini-3.1-pro-preview` in any script — documented hang/loop failures, tracked as priority/p1.

---

## Patch protocol (coding with Gemini)

`astrobley.sh --patch` drives a stateless multi-turn coding session via REST.
Model: gemini-3.5-flash (pinned). Output contract: unified diff only, or `QUESTION: ...`.

**5-step driver loop (run by you or your orchestrating agent):**

1. Build a context pack: target file(s) in full + dependency signature stubs + the task statement.
2. `astrobley.sh --patch session/gemini-coder/<task-id>.ledger.json "<context pack + task>"` → capture stdout.
3. `git apply --check` on work branch — reject non-diff output outright.
4. Apply + run tests. Green → done. Red → pass the failing output as the next message.
5. **Ceiling: 4 iterations** (gaveled). After 4, stop and hand to human.

**Ledger convention:**
- Location: project-local `session/gemini-coder/<task-id>.ledger.json` (script takes any path).
- One task = one ledger. Never reuse across tasks.
- Re-fire on 503: call with no message (`astrobley.sh --patch <ledger>`) — ledger sent as-is.
- Size guard: if ledger > 200KB, a warning is printed to stderr. Trim or split the task.

**Example:**
```bash
ledger="session/gemini-coder/task-001.ledger.json"
astrobley.sh --patch "$ledger" "Context: ... Task: ..."
git apply --check < output.diff && git apply < output.diff
# on failure:
astrobley.sh --patch "$ledger" "Test failed: $(cat test-output.txt)"
```

## ai-install :: gemini

Underlying CLI binary (`gemini`, npm package `@google/gemini-cli`) — separate from the
agent-seat wrappers above (`g-vega` / `g-orby` / `g-astro` / …). Installed globally via npm,
no sudo, custom user prefix.

**What changed (2026-07-27):** npm was silently falling back to the system `/etc/npmrc`
(`prefix=/usr`) because `~/.npmrc` had no prefix of its own — any `npm install -g` (including
a routine gemini-cli version bump) hit `EACCES` trying to write under `/usr/lib/node_modules`.
Separately, two optional native deps gemini-cli pulls in transitively (`@github/keytar`,
`node-pty`) warned on every install because their install/postinstall scripts aren't covered
by npm's `allow-scripts` policy — a one-time inline `--allow-scripts=...` fixes a single run
but does **not** persist.

Both are now fixed for good in `~/.npmrc`:
```
prefix=/home/hruzam/.npm-global
allow-scripts=@github/keytar,node-pty
```

**Last loop (the fix, in order):**
```bash
# 1. persist prefix — stops npm install -g from falling back to /usr
npm config set prefix ~/.npm-global

# 2. persist allow-scripts — stops the keytar/node-pty warning on every install
npm config set allow-scripts=@github/keytar,node-pty --location=user

# 3. install/update gemini-cli itself
npm install -g @google/gemini-cli@0.52.0

# 4. verify
gemini --version
```

Note: `allow-scripts` here is a **global user-level npm setting** — applies to any future
global npm install, not scoped to gemini-cli specifically. Re-audit if either package's
install script ever changes.

---

## Pointer

Builder guide (adding a new seat): `~/.config/zsh/guides/guide-for-builder.md`

---

## Project devenv transport

Per-project git repos carry W3 agentive + process files across machines.
Pull before you push — always.

| Key | Action | Notes |
|---|---|---|
| `fr-sync` | freya: pull --rebase + sync.sh (app → repo) | CLAUDE.md backup-diff lane fires |
| `fr-deploy` | freya: pull --rebase + deploy.sh (repo → app) | deploy-guard fires on branch/HEAD mismatch |
| `fr-status` | freya: git status + log -5 | quick orientation |
| `bo-sync` | fantasyobchod: pull --rebase + sync.sh | |
| `bo-deploy` | fantasyobchod: pull --rebase + deploy.sh | |
| `bo-status` | fantasyobchod: git status + log -5 | |

Full reference: `devenv-help` (keyboard.zsh PARTITION 11).
Discipline: `~/www/imago_cz/freya.devenv/SYNC_DISCIPLINE.md`.
