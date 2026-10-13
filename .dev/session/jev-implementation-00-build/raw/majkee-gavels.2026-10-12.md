---
title: majkee gavels — Jev pilot, cycle 01
date: 2026-10-12
questions_by: >-
  flight. This is a plain-language rendering of Cartan's operator packet
  (raw/design.2026-10-05.md, last section) plus the context behind each item.
answers_by: majkee
recorded_by: cartan, after Flight's VERDICT 01
status: open, waiting for majkee's picks
---

# majkee gavels — Jev pilot, cycle 01

## How this sheet works

- **Eight decisions, one at a time.** Each one says what it is about, what each choice
  leads to, and what Cartan and Flight recommend.
- **Answering:** tick one box per decision (`[ ]` → `[x]`) and add a note if you want.
  If you prefer chat, tell Flight something like "1A 2A 3B $0.10…" and Flight copies your
  words in here, marked as dictated.
- **When your picks count:** after Flight's verification (`_bus/01.flight.verdict.md`).
  If that verification finds a problem with an item, Flight tells you before Cartan
  records it.
- **Who edits what:** Flight wrote the questions. From now on only you change the answers,
  and Cartan records them.
- **Limits:** nothing in this sheet, on its own, approves a paid call, key handling or
  implementation.

**Not for you.** Cartan decides these and Flight verifies them:
- ledger hardening (D4);
- the shared event format with the nablarva project (D5), which is already one line in
  Cartan's STATUS;
- event kinds and lineage fields (D9).

---

## 1. Who may send a request to Jev? (D1)

**Context.** Sending is the only step that costs money and leaves this machine. Everything
else is local: preparing, checking, showing a reply, giving its file path, and recording
use/skip/reconsider.

**Proposal.** Only you send, from your own terminal:
`jev send --session <id> <request-id>`.
- It shows the frozen request and its hash.
- You type the first 8 characters of the hash to confirm.
- It sends exactly those bytes, once.

Claude and Codex can do everything except send. If an agent tries, the send is refused
before any key is touched.

**Consequences.**
- One send path to build and test, and agents can never spend.
- The check is cooperative: a program running as your user could imitate a terminal. The
  pilot states this limit openly instead of claiming enforcement.
- `!` in the Claude UI and the phone are *not* send paths yet. Each needs a witnessed test
  first.

- [ ] A — Yes, as proposed (Cartan and Flight recommend)
- [ ] B — Change it: ______

Note:

---

## 2. Build the wallet before or after the first live test? (D2, order)

**Context.** The "wallet" is the budget safety from our October 2–4 talks:
- a gpg password unlocks an OpenRouter management key;
- that key creates a temporary key for the session, with a small spending limit and an
  expiry.

It depends on OpenRouter behaviour nobody has tested yet: can a new key call Jev, how small
can the limit be, and how fast does revocation work?

- [ ] A — **Offline first, wallet later** (Cartan and Flight recommend).
  - The pilot is built and tested offline first.
  - The wallet becomes its own task, done before any automatic use.
  - The key for the first live test is a separate decision you approve at that point. It
    never quietly falls back to the key that is exported into every shell today.
- [ ] B — **Wallet first.** The first live test waits until the wallet is built and
  tested. Spending is safer from the very first call, but the pilot is slower, and more
  untested provider behaviour sits on the critical path.

Note:

---

## 3. Default budget per session (D2, amount)

**Context.** This is the wallet's spending limit for one session.
- At the published price (about $0.042 per million input tokens, output free; check again
  before use), $0.05 covers about 37 requests of maximum size.
- That is the whole pilot test many times over.
- Whether OpenRouter accepts a limit this small is untested.

- [ ] A — $0.05 (proposed; you chose it on Oct 2)
- [ ] B — Another amount: $______

Note:

---

## 4. What does one wallet cover? (D3)

**Context.** For the pilot, one bed (session folder) = one Jev session = one budget.
- A second Jev session in the same bed gets no new money.
- Sharing one bed's budget across several sessions later needs its own lock.
- Your OpenRouter account balance is only a backstop, not a guaranteed ceiling: top-ups and
  other usage can change it.

- [ ] A — Yes: one bed = one session = one budget for the pilot (Cartan and Flight recommend)
- [ ] B — Change it: ______

Note:

---

## 5. Names (D6)

**Context.**
- `jev` is the program and its folder (`~/.jev/`), like `claude` and `codex`.
- **belnap** is the first *protocol*: a fixed set of typed questions plus the rules for
  reading the answers.
  - It is not an agent with a personality, and it does not go in the germline.
  - Its question set is frozen by content and hash, not just by name.

- [ ] A — Yes (your direction from Oct 4; Cartan agrees)
- [ ] B — Change it: ______

Note:

---

## 6. Where Jev keeps its session memory (D7)

**Context.** Each Jev session is one JSONL file:
`~/.jev/projects/<project-name>-<short-hash>/<time>-<session-id>.jsonl`.
- **First line:** it freezes what the session belongs to (project, bed, protocol, limits).
  Moving the session means opening a new one, never editing the old one.
- **Every request and reply** is one line. Hashes show whether a line was altered, but not
  who altered it.
- **Privacy:** only your user account can read these files.

- [ ] A — Yes (your direction from Oct 4, with Cartan's safety details)
- [ ] B — Change it: ______

Note:

---

## 7. Where the code lives after the pilot (D8)

**Context.** This applies only after the pilot is accepted and a promotion is separately
approved.
- Code, protocols and defaults go to `ia-sync/zsh/jev/`, deployed by the existing zsh step.
- `~/.jev/` never receives code, only memory.
- Until then, the pilot lives in its session folder.

- [ ] A — Yes (your direction from Oct 4; Cartan agrees)
- [ ] B — Change it: ______

Note:

---

## 8. The first live test (D10)

**Context.** One request you approve:
- **Five synthetic briefs:** sanitized re-tellings of finished own work.
- **Three questions each:** which model tier, does it need clarification, and how clear is
  it. That is 15 questions, under the 20-question cap.
- **Expected answers** are written down before the call.
- **Afterwards,** Claude and Codex each show the reply and record use/skip/reconsider.

It proves the plumbing works. Five examples prove nothing about accuracy or savings.

- [ ] A — Yes, as proposed (Cartan and Flight recommend)
- [ ] B — A different test: ______

Note:
