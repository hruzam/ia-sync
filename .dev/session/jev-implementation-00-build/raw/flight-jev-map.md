---
title: Flight — Jev role map, schemas and brainstorm
date: 2026-10-04
author: flight (Claude Code, Opus; MANNED, operator-driven)
host: office · hruzam-120922
status: >-
  Filed with majkee's blessing (2026-10-04) as a raw keeper beside raw/flight-review.md.
  It is a brainstorm and role map, NOT design and NOT gaveled. Cartan owns synthesis. The
  pilot gate, RUNBOOK and STATUS are unchanged by this file.
answers: >-
  majkee's hand-drawn notes of 2026-10-03 (pages 0–5, "JEV IMPLEMENTATION"), the tunnel
  protocols [1]–[3] (informative only), and the study screens (advisor post, CMU paper,
  Jev-engineering note).
inputs:
  - raw/epoch.janus-belnap-skills-vs-agent.2026-10-02.md
  - ~/reposoma/.majkee/journal/2026-10-01.md §1.2c (Jev is a callee, not a session to observe)
  - ~/reposoma/.majkee/journal/2026-10-03.md §2 (shuttle package, parked questions)
  - ~/unikuklatrix/nablarva/.dev/session/nablarva-X0-restarted/_bus/02.oraculum.point.md
provenance_images: >-
  raw/majkee-photos.2026-10-03/ holds the 13 photos and screens: byte-identical copies
  with readable names, and an INDEX.md mapping each file to the §1 ids. Copied 2026-10-05
  at majkee's request; the originals stay host-local in
  ~/.claude/uploads/5325e884-a1cd-434a-bfb8-13885be3bf1b/.
---

# 0. Read this first

**The program owns the loop. Jev is a typed branch inside it.**

- Code detects.
- Jev judges what can be read off the text.
- An LLM derives.
- The human gavels.

Everything below is that sentence applied to majkee's questions, plus shapes he asked
Flight to look for.

Nothing here authorizes a send, a watcher, a deploy or a new agent.

Phase labels used throughout:
- **P1**: this pilot, with per-send confirmation.
- **P2**: wallet mode, where the session budget is the spending authority.
- **P3+**: later.

# 1. The questions, transcribed (Flight's reading of the photos)

| id | majkee's question (condensed) | answered in |
|---|---|---|
| p0 | Goal: find or assign Jev's role in the system (roles map, implementation draft, Jev as a build). Philosophy: think as a senior developer, not a prompt engineer; the process is session events, not AI events; deterministic process first, LLM thinking is a bonus. `zsh/ai/` is growing too much. | §2, §11 |
| Q1.1 | Can the bus agent (shuttle) use Jev after each loop to check whether a file arrived? Or can Jev be an "epistemic session key", an attractor that keeps `shuttle{sonnet::max}` attention alive? | §5 |
| Q1.2 | Where inside Protocol [1] can Jev have a role? | §5, §10 |
| Q1.3 | Could Jev play the bus itself instead of shuttle (Claude; Codex if reasonable)? | §5 |
| Q2.1 | Place Jev as: (A) an operational device, cheap, for "living linux"; (B) a relay bridge or router (zsh wrapper + cSharp RUNBOOK → JSON, a sensitive layer reacting on files); (C) a PTY attractor filling an event messenger, running in parallel with the RUNBOOK tree, in a living session with watchdogs on bus files and STATUS. | §5, §8.9 |
| Q3.1 | How rich can our harness be when a vendor can ship its own TUI wrapper and leave us stranded? Skills, agents, memory or workflow protocols? | §2 |
| Q3.2 | Or think of Jev as a different shape. Favour what is programmatically based: [CLIs] × Jev. | §2, §8 |
| X.1 | Jev as a challenger organ: Janus() or Mirror → Codex, Jev. A mirror as a thinking level that creates a ticket or uses a specific logic "school". | §8.2 |
| Q3.3 | The maths part: proof by disagreement or conflict. Analytic judgment; synthetic judgment (is it the same as deduction?); conflict judgment. A [JUD] node fed by same-agent method judges and by other-vendor parts (Jev, Codex) via ticket/spawn/bash/py; Claude produces the output; the same works for blind triangulation; `claude -p` stays locked as "not use". | §3, §4 |
| p5 | No composite now: Codex(Claude, Jev) is impossible, only Codex(Jev). | §4 |
| Q3.4 | Can Jev have a child, or iterate in a chain, where each result defines the next observation and the stop condition, so the path need not be straight (hypothesis level)? | §6 |
| p5 | Wanted now: schema, map and use cases; then an implementation plan or research. Draw trees. Own solutions welcome; synthesize from context rather than "best practices confirmed". | whole file |
| T[1]–[3] | Tunnel protocols, informative only. | §10 |
| — | The Jev "agent" name: majkee names it later. The budget is volatile: majkee fills or drains it at any time. | §5 |

# 2. Thesis: Jev is an `if`, not a seat

This answers Q3.1 and Q3.2.

- An agent identity is vendor territory, and a vendor TUI can swallow it. A shell command
  plus a ledger is ours.
- So Jev lives in the shell layer: one CLI (`jev`), one host-local ledger (`~/.jev/`) and
  portable rubric files (§8.1).
- Claude, Codex, a tmux pane or the phone all call it the same way. Skills and agent cards
  only point at it.

That is [CLIs] × Jev: the product of two layers, neither owning the other.

What Jev is not: a writer, a mover, a memory, or an agent with tools. It returns a typed
answer with probabilities and nothing else, no prose. That last property matters again in
§8.3.

# 3. Schema 1: the judgment ladder

```
judgment
├─ analytic ─────────────── CODE      free, certain
│   file arrived? hash changed? count ≥ 3? exit ≠ 0?
├─ synthetic, read off text ─ JEV     ~$0.0001, typed
│   relevant? which tier? needs the head? brief clear?
├─ synthetic, derived ─────── LLM     main model
│   │  is this code correct? does the argument hold?
│   └─ hard decision point ── ADVISOR stronger model,
│                              model-timed (Claude Code)
└─ conflict / value ───────── HUMAN   gavel
```

Each rung escalates to the next, and none skips down.

**Synthesis vs deduction (Q3.3): not the same.**
- Deduction unpacks what the premises already contain. It preserves truth, so code or a
  proof checker can verify it (the analytic rung).
- Synthesis adds what the premises lack (it is ampliative). It can be corroborated, never
  proven.

**Proof by conflict is real but narrow.**
- Two independent judges disagreeing proves that at least one is wrong. That is a valid
  proof that an error exists, not of where it is.
- Agreement between correlated judges proves nothing. Agreement between decorrelated
  judges is corroboration.

**Evidence for where the Jev rung ends**: CMU, "JEV-as-a-Judge" (arXiv 2609.26550).
- **v1** (22 Sep, from the operator's screenshot):
  - Jev comes within three points of a state-of-the-art LLM judge on ordinary preference
    and evidence-grounded factuality, at 0.36% of its fee.
  - The gaps are larger "when judgments require checking a derivation or resisting an
    elaborately written wrong answer".
  - The gap is concentrated in low-confidence decisions.
- **v3** (29 Sep, fetched 2026-10-04; quotes came via a summarizer, so re-read the PDF
  before citing them elsewhere):
  - It names "math, code, and logic" as the cases where "the verdict must be derived".
  - It reports unreliable confidence routing on "style-adversarial pairs and
    reference-free prose".
  - Its cascade was "0.9 points more accurate than GPT-6 on 1,610 held-out pairs at 41% of
    its fee".
- **Consequence:** Jev never judges "is this code correct?" or "done?" on its own.

**The advisor rung is real.**
- It is Claude Code's experimental advisor tool: `--advisor`, `/advisor`, the
  `advisorModel` setting (code.claude.com/docs/en/advisor, fetched 2026-10-04).
- Its timing is model-driven: "There is no setting to cap or force advisor calls". Each
  call re-reads the full transcript, uncached.
- Jev sits at the opposite end: code-timed, bounded input, ledgered. The two compose
  rather than compete.

# 4. Schema 2: the [JUD] node as Belnap logic (Q3.3, X.1)

```
[JUD]  inputs: verdict A (Claude, own method)
               distribution B (Jev, typed)
               (+ C: Codex via tunnel/mirror, optional)
├─ A yes · B sharp yes ────── TRUE     proceed, normal gates
├─ A no  · B sharp no  ────── FALSE    don't
├─ A, B disagree sharply ──── BOTH     tertium: escalate with
│                                      both sides shown
└─ B split (or A unsure) ──── NEITHER  gather evidence
                                       (tertium, later) or ask
```

- **Belnap's four values** (Epoch F3) are exactly the possible outcomes of two judges.
  This gives Epoch F4 what it asked for: real BOTH and NEITHER cases from which to define
  tertium, instead of inventing it.
- **Thresholds:** `sharp` and `split` need a threshold per rubric version (§8.1), set from
  scored history, not a universal 0.7.
- **Decorrelation is genuine**: a different vendor and a different architecture. Its value
  holds only on read-off questions (§3).
- **Composites (p5):**
  - From the Claude side, Claude(Codex via tunnel, Jev via bash) works, with Claude
    adjudicating.
  - From the Codex side, only Codex(Jev) is possible, because `claude -p` stays locked.
  - The asymmetry is fine: one adjudicator is enough.
- **Closes an Epoch open item** ("did not inspect jev's own spawn mechanism"). Jev spawns
  nothing; it is an HTTP callee. Epoch F2 (per-spawn model override) does not apply to it.

# 5. Schema 3: the living session (Q1.1–Q1.3, Q2.1 B+C) — P2

```
event sources (code, deterministic)
├─ _bus/ file N appears ──┐
├─ STATUS.md changed      ├─→ watchdog (stat/inotify,
└─ PTY idle (EVENTS map) ─┘    no AI) emits event
            │
            ▼
   JEV triage — rubric "needs the head now?"
   ├─ sharp no  → ledger note; no early wake
   ├─ sharp yes → wake shuttle / head now
   ├─ split     → wake head + show uncertainty
   └─ alarm     → majkee (gavel conflict, scope)
```

- **Q1.1.** Never spend Jev on *whether* a file arrived; that is analytic and free in code.
  Spend it on whether the arrival *matters now*. "Keeping attention alive" means the
  expensive minds sleep and Jev decides when to wake them early.
- **"Sharp no" means no *early* wake, never "never".** The head's normal cadence, which is
  code, still reads every arrival. Jev can only add attention (L1, §7).
- **Q1.3.** Jev cannot *be* the bus: it has no hands, no memory and no file I/O. It can be
  the bus's switch. Shuttle stays the hands (Claude sonnet·high, per the tunnel-02
  package), and Jev filters what wakes it. That means fewer wakes and lower cost, with the
  same guarantees.
- **Q1.2.** Within Protocol [1], Jev's role is the switch above, plus §10.
- **Precondition: wallet mode (P2).** An automatic watchdog → Jev call breaks per-send
  confirmation, so this exists only in P2.
  - The session budget majkee unlocks is the spending authority, and the borrowed key's
    provider limit is the wall (review §D′ and §D″).
  - P1 confirms every send; P2 makes the budget the gate.
  - The budget being volatile is a feature: majkee drains it to stop the whole layer
    instantly.
- **Event sources** reuse nablarva's EVENTS map (journal 2026-10-01.md §1.2c). Jev is a
  callee: it appears as the caller's `tool_started`/`tool_ended`, and its ledger is a
  record source.

# 6. Cascade: Jev child and iteration (Q3.4) — P3, hypothesis level

```
R1  Choice "why did the test fail?"
├─ "stale test" → R2 (parent = R1)
│                 Noul "fixture older than the change?"
│                 └─ sharp → stop, report
├─ "real bug"   → stop → LLM (derivation rung)
└─ split        → stop → head
stop when: sharp · depth ≥ 3 · budget · BOTH/NEITHER
```

- **Jev has no memory, so the chain lives in code.** Each child request records
  `parent_request_id`.
- **The path is not straight, but it is bounded.** It is a tree compiled per rubric
  (§8.1), not an open loop.
- **Errors compound.** If each step is right with probability pᵢ, the leaf is right with
  probability at most ∏pᵢ. So depth stays small and any split stops the chain.
- TypeSafe's own guidance agrees in substance: dependent judgments need code to compose
  the results, or another call (`provider-recheck.2026-10-01.md`).

# 7. Five laws (the GUIDE seed, refined)

1. **L1 — escalate only.** Jev may add attention (wake, ask, flag). It never removes
   attention that the deterministic process already schedules.
2. **L2 — autonomy only where reversible.** Jev may decide alone only reversible, logged
   choices: what to read first, or what to keep in context when the full output stays on
   disk. Irreversible acts keep their human gate whatever Jev says.
3. **L3 — no hands.** Jev never writes, moves or executes anything. Code acts on typed
   answers under the consumer's own permissions.
4. **L4 — read-off only.** Questions must be answerable from the supplied text.
   Derivation goes to tests, the LLM or the advisor.
5. **L5 — bounded spend.** Every call is a ledger event inside a session wallet. P1 also
   needs per-send confirmation. Automatic calls happen only in P2.

The 2×2 behind L1 and L2:

| | reversible | irreversible |
|---|---|---|
| Jev sharp | may act alone, logged | human gate unchanged |
| Jev split | escalate | human gate + flag |

# 8. Brainstorm: shapes beyond the drawings

## 8.1 The distillation: rubric programs on a cheap CPU

Every shape in this file reduces to three primitives, plus a revision step:

```
rubric   versioned file: questions, criteria, branch
         table, stop rules, law class (L2: reversible?)
         ← LLM drafts · majkee gavels
run      one ledger event: code fills state, Jev answers
score    code, later: observed outcome vs prediction
         → Brier (Noul, Choice) · ranked probability
           score (Score, ordinal)
revise   LLM proposes rubric v2 from scored misses
         → majkee gavels
```

- **Read it as programming:** the rubric is source, Jev is the CPU, the ledger is the
  trace, the score is the test suite, the gavel is code review, and a cascade is control
  flow inside a rubric.
- **Learning without auto-learning.** The design forbids auto-tuned thresholds and
  auto-promotion.
  - Here, learning happens only as new, gaveled rubric versions.
  - The experience ledger becomes computable, because a Brier score is deterministic code.
  - The sharp/split thresholds come from each version's scored history.
- **One rubric, three CPUs.** The typed form doesn't care who answers it. The same rubric
  can be answered by Jev, by an LLM, or by majkee with one tap on the phone.
  - majkee's answers become labels for scoring.
  - Agreement between Jev and majkee (Cohen's κ) measures whether a rubric is ready to run
    unattended.
  - Calibration then becomes something he can do while waiting, with no study bed.
- **Cost math.**
  - Asking the frontier model every time costs N·c_f. A rubric costs c_r once, plus N·c_j.
  - Break-even is N* = c_r / (c_f − c_j). If writing the rubric costs about one frontier
    call, N* ≈ 1.
  - Caveat from the older handoff: savings exist only if frontier work is *removed*. Most
    frontier decisions happen implicitly inside a turn, so measure end to end. Adding Jev
    calls alone only adds cost.
- **Where rubrics live:** as portable source in `ia-sync/zsh/jev/rubrics/` (§16).
  The ledger stays host-local. Each of the 16 design situations is a candidate rubric,
  built only when a use earns it.

## 8.2 Generate, then select (X.1 — Janus(Jev))

Generation is expensive and creative; selection is cheap and typed.

- Janus (or Mirror) writes k candidate weakest assumptions.
- Jev ranks them blind with a Choice.
- [JUD] compares Janus's pick with Jev's top choice.

Cost: the Janus call, already paid, plus about $0.0001.

Caveat: the candidate texts are persuasive by construction, which is Jev's documented weak
spot. So this is a pilot question, not a law.

## 8.3 The thermometer: uncertainty as a signal (phone-native)

Jev returns distributions, so its *uncertainty* is data.

- **Signal.** Take the entropy of each call, H = −Σ p·log p (binary entropy for a Noul),
  and average it per bed per rubric version. That gives an "uncertainty temperature".
- **Meaning.** A rising temperature means the work is getting ambiguous, which is worth
  majkee's attention.
- **Baseline.** Compare only within one rubric version, because the question mix moves the
  baseline.
- **Fit for the phone.** Typed outputs are tiny by nature (a word, a percent), so this
  shape fits the Redmi/Galaxy screen: one light per bed in `ov-ls`.
- **Safety.** It is read-only and carries no decision authority, so it is the safest shape
  of all.

## 8.4 The linter: judge artifacts at authoring time

Before an expensive spawn:
- Code checks that a brief's four dispatch fields exist (file scope, one-sentence task,
  expected output, report path). That is analytic.
- Jev scores whether the task sentence is specific enough. That is read-off.

The same rubric fits RUNBOOK prompts ("is the gate testable?"). It is cheap, and it sits
before the cost rather than after it.

## 8.5 The human-attention router

majkee's attention is the scarcest resource, and P1 spends it on every send.

- Jev can rank *his* queue (POINTs to carry, gavels, reviews) by "which item unblocks the
  most work?".
- Under L1 it can move an item up, never hide one.
- `/gavel-loop`'s qualify phase ("binary, escalating to an 8-question pass on doubt") is
  already Jev-shaped. Jev may pre-qualify, and may only *promote* formal → strategic,
  never demote.

## 8.6 Harness drift: Atlas's standing check

AGENTS.md asks Atlas to sweep per-project seats that duplicate global ones.

- Code narrows the candidate pairs (name and description overlap).
- One Jev request, with all the descriptions in its state, asks up to 20 pairwise Nouls:
  "same purpose?".

That is read-off, uses own material, and suits Jev's many-questions-per-request economy.
It is a good P2 workload with honest ground truth: Atlas's own fold decisions.

## 8.7 The determinism probe, before building any cache

As research: send one canonical request twice under two separate approvals (about
$0.00004 in total) and compare the answers.

- **If they are identical,** the request SHA-256 is an exact cache key, and the same
  question is never paid for twice.
- **If they differ,** the variance is a free uncertainty signal and caching must stay off.

This is unknown today and cheap to find out.

## 8.8 Negative space: where Jev must not go

- secrets in its state
- imago or other client data
- derivation (code correctness, proofs, maths)
- irreversible decisions on its own
- judging gavels (gavels are provenance, never input to vote on)
- promoting its own rubrics
- high-stakes questions whose text is persuasive by design

## 8.9 The machine-layer sensor: Q2.1 (A), "living linux"

ia-sync's own job is host maintenance. The shape: code tails warning-level logs and
redacts them, then Jev answers "does this need the operator today?".

This is the lowest priority, because logs leave the host for a US vendor. They can carry
paths, hostnames and client project names (`~/www/imago_cz/…` exists on office). If it is
done at all, it needs redaction in code and majkee's approval per log source.

# 9. Use-case map by rung and phase

| use case | rung | phase | note |
|---|---|---|---|
| file arrived · repeats · stale input · bad reply | code | P1 | never Jev |
| brief clear enough? (Score) | Jev | P1 | the look-back shadow batch |
| which model tier (Choice) | Jev → majkee confirms | P1 | advisory |
| which files or chunks to read (Score) | Jev | P2 | L2, reversible |
| keep or drop tool output (Score) | Jev | P2 | L2 only if the full output stays on disk |
| arrival needs the head now? (Noul) | Jev | P2 | the favourite: ground truth is "did the head act?" |
| does the RETURN answer the POINT? (Noul) | Jev | P2 | handshake boundary |
| seat-drift pairs (Noul ×20) | Jev | P2 | §8.6 |
| uncertainty thermometer | Jev, aggregated | P2 | §8.3, read-only |
| safe to run? (Noul) | Jev, escalate only | P2 | L1: a low p never skips a gate |
| done? / code correct? | tests + LLM/advisor | — | Jev is weak at derivation |
| conflicting sources | Jev flags, LLM inspects | P2 | [JUD] |
| conflict with a gavel | human | always | — |
| cascade chains | Jev + code | P3 | §6 |
| pattern across streams → rubric v2 | LLM drafts, majkee gavels | P3 | §8.1 |

# 10. Tunnel protocols (informative)

- **[1] Two hemispheres** (Codex head, Claude shuttle on the bus): Jev is shuttle's
  arrival switch (§5), plus a Noul for "is the PAD ready for the human?" before pinging
  majkee.
- **[2] Claude head spawning Codex workers:**
  - a Choice for which worker or tier gets the ticket;
  - a Noul for "does the return answer the brief?" before the head reads it in full.
  - Q1 (can A and B be the same main?) stays parked, per journal 2026-10-03 §2.
- **[3] Tester, hands on the computer:** a Noul for "does the PAD step's observed result
  match the expected line?". That is a clean read-off; on a split, the human looks.
- **Vega/Mirror redundancy** (p4: "two Claude agents, I don't think we need so many"):
  Flight agrees. That is a separate fold, outside this bed.

# 11. Placement: keep `zsh/ai/` from growing

`zsh/ai/` holds 44 entries today, and Jev does not go there. **Final placement (§16):**
its own folder in the zsh layer, `ia-sync/zsh/jev/`, riding the existing `zsh/` deploy
leg; `~/.jev/` holds runtime only.

- The runtime part of `~/.jev/` (`projects/`) stays host-local and is never synced.
- Promotion follows compose-first, dry-run and fresh-session proof, after the pilot.
- The pilot's `impl/` stays in this bed, as the RUNBOOK says.

# 12. Plan

1. **P1 pilot unchanged** (Cartan → Astrobley), plus two decisions *before* `impl/`:
   - (a) Oraculum's envelope POINT (§13);
   - (b) which of Flight's review revisions are accepted.
2. **Research**, in Epoch-sized pieces:
   - the §8.7 determinism probe (two approved sends);
   - re-verify OpenRouter management keys (review §D);
   - whether Codex has `!` shell input;
   - whether `permissions.ask` holds under auto mode;
   - a read-off vs derivation split on our own question types.
3. **P2 bed:** wallet mode, plus the watchdog → Jev "needs the head now?" switch, the [JUD]
   Belnap node and the thermometer. The first rubric is arrival triage.
4. **P3:** cascade, the rubric revision loop, and composites.

# 13. Open, with owners

- **majkee:** carry Oraculum's envelope POINT to Cartan:
  `~/unikuklatrix/nablarva/.dev/session/nablarva-X0-restarted/_bus/02.oraculum.point.md`.
  The reply goes to the sibling `02.cartan.return.md`.
  - **Flight's view:** accept it, with one naming caution. `data.certainty: confirmed` on
    a validated reply must mean that *the receipt is confirmed*, not that *the judgment is
    right*. The judgment's epistemic state lives in its probabilities and in the [JUD]
    Belnap value.
  - **Decide in the same pass:** `parent_request_id`, `reconsider_of` and the budget
    events (review §D″).
- **majkee:** ~~Jev's name (later)~~. The agent (seat) is named **belnap** (2026-10-04);
  `jev` stays the runtime and folder. See §14.
- **Cartan:**
  - whether `budget_granted` and `budget_locked` become new kinds or `data` variants;
  - whether the rubric (§8.1) becomes the unit behind `question_version`.
- **Flight:** remains the witness. Post-implementation verification goes to
  `raw/flight-verification.md`.

# 14. Name: belnap (majkee, 2026-10-04)

majkee named the Jev agent **belnap**.

**Collision sweep (2026-10-04): clear.** The following were checked:
- `~/.claude/{agents,skills}`;
- ia-sync `claude/`, `codex/`, `zsh/` and `_staging/`;
- `~/reposoma/.germline`, `~/.codex/{agents,skills}` and `~/.config/zsh`;
- file names under reposoma, ia-sync and unikuklatrix;
- `compgen -c`.

The only hit is the Epoch file's own *proposal* of a `belnap` agent, which this name
absorbs (see below).

## majkee's clarification (2026-10-04): runtime vs seat

Flight first read belnap as a rename of the whole layer. majkee corrected this the same
day: **belnap is the agent's name; `jev` stays the process and the folder**, treated like
the other vendors. That is the temple's existing pattern, where runtime identity and seat
coexist (AGENTS.md).

| runtime (process + dot-folder) | identities on it |
|---|---|
| `claude` · `~/.claude/` | Flight, Houston, Janus, … |
| `codex` · `~/.codex/` | Cartan, Astrobley, … |
| `gemini` · `~/.gemini/` | Gemini-side seats |
| `jev` · `~/.jev/` | **belnap** (a protocol, §15) |

- **jev is the process.** It is our CLI, the ledger under `~/.jev/`, and the provider
  adapter (OpenRouter → `typesafe/jev-1.13`). Names stay as designed: the `jev` command,
  `~/.jev/` and `jev.event/v1`. `~/.jev/` does not exist yet (checked 2026-10-04); the
  pilot creates it.
- **belnap is the first Jev identity.** Following majkee's later direction (§15), a Jev
  identity is defined by its protocol, not by a seat card. It cannot initiate, write,
  remember or act. It only answers typed questions, and it answers in told-values (below).
- **The belnap protocol** is how the seat is asked and how its answers count:
  rubric → `jev` run → told-values → [JUD] union with other seats' verdicts → tertium for
  BOTH/NEITHER. It is **a document plus rubric files, not a second wrapper**: one program
  (`jev`), one seat (belnap), one protocol chapter.
- **tertium** is the later resolution rule for BOTH and NEITHER (Epoch F4). It is where an
  LLM, a read-only probe or majkee comes in.
- **Epoch F3 folds in.** The Claude-side Bash agent that Epoch planned under this name is
  not needed. Detection is the protocol (code); evidence-gathering belongs to tertium's
  NEITHER branch, as read-only probes in a later phase.

## Why the name fits

Nuel Belnap's four-valued logic ("How a computer should think" and "A useful four-valued
logic", both 1977) was built for exactly this case: a computer that is *told* things by
several fallible sources and must not collapse when they contradict each other.

- Its values are epistemic: told true, told false, told both, told neither. They describe
  what was said, not what is true.
- That puts the review's caution into the name itself: a belnap verdict records what the
  sources said. It never certifies that a judgment is correct.

## The belnap protocol's verdict: code, no LLM needed

1. **Each source tells a subset of {T, F}.** Every typed answer reduces to a proposition
   with a probability p:
   - Noul: p itself.
   - Choice: p of the option under test, i.e. the other judge's pick.
   - Score: P(level ≥ k) = Σ_{j≥k} p_j.
2. **Thresholds per rubric version** (§8.1) turn p into what was told:
   - p ≥ θ_hi → {T}
   - p ≤ θ_lo → {F}
   - otherwise → ∅ (abstain)
3. **Failure modes get principled places:**
   - A failed request tells nothing → ∅ (NEITHER).
   - A self-contradictory reply (the choice is not the argmax, or the score is off its
     weighted level) tells both → {T, F} (BOTH). It is preserved, and never displayed as
     advice.
4. **Combining sources is set union**, which is the join in Belnap's information order:
   {T} ∪ {F} = BOTH and X ∪ ∅ = X. Union is associative, commutative and idempotent, so:
   - the order of judges does not matter;
   - a third judge (Codex) is one more union;
   - the [JUD] node of §4 is a deterministic function.
5. **Reading the information order:**
   - NEITHER is under-informed → gather (tertium: probe or ask).
   - BOTH is over-informed → resolve (tertium: escalate with both sides).

## No rename (withdrawn 2026-10-04)

Flight's earlier rename proposal (`belnap` command, `~/.belnap/`, `belnap.event/v1`,
`zsh/belnap/`) is withdrawn. Names stay as designed, and Cartan has nothing to rename. A
skill launcher, if one is ever wanted, would follow the naming law Epoch cites:
`belnap-<verb>`.

## Small mismatches to watch (none blocking)

1. **Our runtime is homemade.** `claude` and `codex` are vendor binaries; `jev` is ours.
   If TypeSafe ever ships its own `jev` command, the two collide on PATH. Check before
   promotion. Today nothing named `jev` is on PATH or in zsh (checked 2026-10-04).
2. **A seat without a prompt.** A decision model takes state and questions; it has no
   system prompt. So belnap's "card" cannot be a prompt. Its identity is the five laws
   (§7), its rubric library (§8.1) and the told-values protocol. That is what is new about
   this seat, not a defect.
3. **Callee only.** Other seats start work; belnap is always called (journal
   2026-10-01.md §1.2c calls Jev "a callee"). Its ledger is a record source, never a
   session to observe.

## Not in the germline (majkee, 2026-10-04)

Flight briefly suggested a germline identity for belnap. That is withdrawn; see §15 for
the reasons. Jev identities are protocols, and they live in `ia-sync/jev/protocols/`.

# 15. Operator direction (majkee, 2026-10-04): protocols, not seats

majkee said, by voice, after §14:
- Jev and belnap do not belong in the germline. Jev's behaviour, and the way it is called,
  differs too much from the shared Claude/Codex identities the germline exists for.
- Jev identities should have their own names, recognizable as different from the LLM
  seats. Jev needs no personality; working protocols matter more than agents.
- ia-sync can hold a `jev/` folder, deployed later the same way as the Claude and Codex
  harnesses.
- Sessions should be scoped to projects, like the other CLIs. Every exchange goes into
  JSONL with hash IDs.
- A thinking model (for example an Opus spawn beside the main agent) formulates the Jev
  questions and interprets the answers back. majkee will paste his process description.

## Flight's position: agreed, with reasons

- **Germline: agreed; the suggestion is withdrawn.** The germline holds vendor-blind
  identities that render into a Claude or Codex prompt. Jev takes state and typed
  questions: there is no prompt to render into, and nothing is spawned. A different kind
  of artifact needs a different home.
- **Identity = protocol.** A Jev identity is its protocol file: name, purpose, rubric(s),
  law class (§7), verdict rule, who formulates and who interprets, and phase. belnap is
  the first. The RUNBOOK already points this way: prompt-2 forbids a new agent identity.
- **Recognizable names (suggestion only).** Use logicians as the naming family, since
  each protocol is a small logic (typed decisions plus a verdict rule); belnap is the
  first. The folder `jev/protocols/` is the namespace. Sweep each new name for collisions
  when it is created.

## The harness, mirroring the existing pattern

> **Superseded by §16** (majkee, later the same day): the code and portable content move
> into the zsh layer, and `~/.jev/` becomes runtime only.

ia-sync already has `claude/`, `codex/` and `gemini/` at top level. `deploy.sh` has legs
for `~/.claude` and `~/.codex`, and each leg rsyncs only named subfolders (skills, agents,
commands; AGENTS.md, agents, skills). `jev/` follows suit:

```
ia-sync/jev/                    portable source (git)
├─ bin/jev.py                   the CLI (stdlib only)
├─ protocols/belnap.md          identities = protocols
├─ rubrics/                     versioned rubric files (§8.1)
├─ config.json                  defaults: budget, thresholds; no secrets
└─ README.md                    the five laws (§7), layout

~/.jev/                         live (a later deploy leg)
├─ bin/ protocols/ rubrics/ config.json   ← deployed
└─ projects/<project-slug>/              ← runtime: host-local,
   ├─ <YYYY-MM-DDThh-mm>-<session-id>.jsonl   never synced,
   ├─ <session-id>.buffer.md                 never deployed over
   └─ <session-id>.lock
```

- **Project scoping combines the two existing patterns.**
  - Like Claude Code (`~/.claude/projects/<slug>/`), the folder is the project.
  - Like Codex (`~/.codex/sessions/YYYY/MM/DD/rollout-<ts>-<uuid>.jsonl`), the file name
    sorts by time.
  - The slug comes from the bound project root, or from the working directory when nothing
    is bound, as Claude does. No registry is needed.
- **One JSONL per session, written every time.**
  - Line 1 is a `session_opened` record carrying the binding (project root, bed, protocol,
    wallet).
  - That replaces the mutable `session.json` and closes review finding 4: changing a
    binding is a new event, never an edit.
  - Every exchange appends events with `event_id` and `request_sha256`.
- **"Shortened" is a view, not storage.** The full provider reply is small and stays in the
  JSONL; `jev show` prints the short form.
- **Deploy is safe by construction.** As with `~/.claude`, the leg rsyncs only `bin/`,
  `protocols/`, `rubrics/` and `config.json`, and never touches `projects/`.
- **The zsh layer keeps one thin `jev` function.** Nothing more goes into `zsh/ai/`.

## The formulator and interpreter pattern: four guards

A thinking model is the right formulator, because writing a good rubric is the hard part
(§8.1). Four guards keep the pattern honest:
1. **Freeze first.** The formulation is frozen and hashed before the send, and the human
   approves that exact request (P1).
2. **Label the interpretation.** It is recorded as its own, labelled event, and the main
   agent always sees Jev's raw answer beside it.
3. **No reformulating until the answer agrees.** A new formulation is a new request, with
   `reconsider_of` and a fresh approval.
4. **Reuse before writing.** A gaveled protocol is reused whenever one fits. The thinking
   model is needed only when none fits, which is where its cost amortizes.

## For Cartan, before `impl/`

- The storage layout above replaces the design's `~/.jev/sessions/<id>/` +
  `session.json` (§"Smallest proposed implementation"). Decide it in the same pass as the
  envelope POINT.
- `session_opened` joins the budget events as a candidate new kind (or a `data` variant).
- The pilot still builds in `impl/` with temporary roots: no deploy leg and no live
  `~/.jev`, as the RUNBOOK says.

This file does not edit RUNBOOK, STATUS or the design. Those are Cartan's.

# 16. Placement revised (majkee, 2026-10-04): code in the zsh layer, runtime in `~/.jev/`

majkee, by voice, after §15:
- `claude/` and `codex/` exist because those are third-party binaries whose config we
  copy.
- Jev's harness is *our own application*, so its code belongs in the zsh layer.
- `~/.jev/` holds the living part: memory and config.
- He asked for Flight's and Cartan's view.

## Flight's view: agreed, and smaller than §15

- **Precedent.** Our own applications already live in the zsh layer as a Python engine, a
  zsh face and JSON config. `zsh/session/` holds `runbook.py` + `runbook.zsh`, and
  `ovitmugen.py` + `ovitmugen.zsh` + `ovitmugen.presets.json`.
- **No new deploy machinery.** `deploy.sh` already rsyncs `zsh/` → `~/.config/zsh/`
  (around line 252). A `zsh/jev/` folder rides that leg; `deploy.sh` gets no jev leg.
  `zsh/ai/` stays untouched.
- **`~/.jev/` becomes runtime only.** Nothing is deployed into it at all, so it is safe by
  construction. That is stronger than §15's "rsync only named subfolders".
- **Engine in Python, face in zsh.** "Within zsh" should mean within the zsh *layer*, not
  written in zsh script. Canonical JSON, SHA-256, `flock`, `fsync` and HTTPS are fragile in
  shell. This is the same split as runbook and ovitmugen, and the RUNBOOK already asks for
  a Python CLI callable from zsh or bash.

```
ia-sync/zsh/jev/              → ~/.config/zsh/jev/ (existing leg)
├─ jev.py                     engine (stdlib only)
├─ jev.zsh                    face: the `jev` function
├─ protocols/belnap.md        identities = protocols
├─ rubrics/                   versioned rubric files
├─ jev.defaults.json          budget $0.05, thresholds; no secrets
└─ help/HELP.md               short, phone-width, like ovitmugen's

~/.jev/                       runtime only: host-local,
├─ projects/<slug>/            never synced, never deployed into
│  ├─ <time>-<id>.jsonl        line 1 = binding (session_opened)
│  ├─ <id>.buffer.md
│  └─ <id>.lock
└─ config.json                optional host-local overrides

~/.secrets/jev/               the gpg-locked management key
```

**The key follows the existing secrets convention.**
- It does not go in `~/.jev/`, and it does not go in the plaintext `~/.config/zsh/.env/`.
- `env-vault`'s header keeps its own key at `~/.secrets/zsh/id.age` and states its threat
  model: it "DEFENDS a leaked repo" and "IGNORES a compromised live machine".
- The gpg lock (review §C) is the extra on-box layer that env-vault deliberately does not
  provide.
- The key is decrypted only in the send process's memory, never to disk.

## One engine, two faces: cooperation and routing

```
jev.py (one engine, one ledger, one wallet, the protocols)
├─ callee face — P1
│   any CLI calls `jev` through its ordinary shell:
│   Claude's Bash, Codex's shell, `!` in the UI, a tmux pane.
│   No hooks, no MCP, no plugin. Agents prepare / show /
│   ref / dispose; sends follow P1 rules.
└─ router face — P2
    `jev watch <bed>`: a foreground process in the bed's
    ovitmugen `jev` tab; started by majkee, visible,
    killable, wallet-gated. Never a systemd daemon.
    event → belnap protocol "needs the head now?" → signal
```

How the router signals, within existing rules:
- always as a ledger event;
- as a visual signal in the bed's tmux frame (message or bell), never by typing into a
  pane, which is ovitmugen's own rule;
- for a Codex head bound through the tunnel, via the tunnel's bound-thread send, if that
  protocol allows it;
- for alarms, on majkee's phone.

Claude heads cannot be woken programmatically while `claude -p` stays locked. They pick
the signal up at their own cadence (for example `/loop` over the bus or ledger), or majkee
relays it. This is the same asymmetry as the composites in §4.

Cooperation is therefore not integration code. It is the shared ledger plus bus records,
and that is what keeps Jev vendor-neutral.

## Who decides

- Cartan owns the design and the integration, so the layout is his to adopt or modify.
- Flight records a view and verifies.
- majkee gavels.

Everything since §13 should reach Cartan as one bundle before `impl/`:
- the envelope POINT;
- protocols, not agents (§15);
- this placement;
- `session_opened` replacing `session.json`.

The pilot itself is unchanged: `impl/` in the bed, temporary roots, no deploy and no live
`~/.jev`.
