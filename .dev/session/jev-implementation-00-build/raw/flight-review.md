---
title: Flight review — Jev pilot design, before implementation
date: 2026-10-01T08:31+02:00
author: flight (Claude Code 2.1.286, Opus; operator-woken, MANNED, review scope only)
host: office · hruzam-120922 (php74 + hostname + $MACHINE_NAME agree)
reviews: RUNBOOK.md, STATUS.md, raw/design.2026-10-01.md, raw/provider-recheck.2026-10-01.md,
  raw/jev-events.example.jsonl; provenance: raw/session-draft-memory.md,
  raw/JEV_RESEARCH_AND_CLI_HANDOFF.md, raw/jev_smoke.py
writes: this file only. No paid call, installation, deploy, settings change, or ~/.jev creation.
---

# Verdict: REVISE

The design is mostly sound. Cartan has already written the most important sentence: "a TTY
prompt, cap, file flag or cooperative shell convention is not a security boundary." But the
pilot is still framed so that **each CLI consumer** is expected to show per-send human
confirmation. On this host, neither enabled runtime can do that in a way that binds the
confirmation to the request. Both runtimes also inherit the credential. Revise before
delegating to Astrobley: make the operator-run send the **only** send path in the pilot, and
make consumers local-only. The gate text does not need to change. Its acceptance line already
says that "unsupported approval paths do not send".

Ranked findings, most material first:

| # | finding | severity |
|---|---|---|
| 1 | No enabled consumer path can enforce per-send confirmation, and both inherit the key | blocks as framed |
| 2 | The approval must bind to the bytes actually sent, not to a display | must fix in impl |
| 3 | Recovery of a partial tail or an indeterminate send has no defined reconcile step | must fix in impl |
| 4 | `session.json` is a mutable second authority for binding and limits | should fix |
| 5 | Model-tier advice has no consumer that acts on it, so the pilot measures little | smaller pilot exists |
| 6 | The bus record needs embedded evidence when read on another host | spec detail |

## Weakest assumption

**"Every send can be shown to require human confirmation in the intended Claude/Codex
workflow."** This comes from the memory draft's Gate 1: "`jev send` is ask every time; never
allowlist it". Evidence from this host says it does not hold for either runtime:

- **The credential is everywhere.** In this Flight Bash tool: `JEV_ORAK_KEY=set`,
  `OPENROUTER_API_KEY=set` (presence test only, no value read). They are exported from
  `~/.config/zsh/.env/secrets.zsh:9-10`, which `~/.config/zsh/config.zsh` sources into every
  shell, agent shells included. Any agent subprocess can call OpenRouter without `jev` at all.
- **Claude Code.** This Flight session runs with **auto mode active** (harness-reported), so
  there is no per-command prompt by default. `~/.claude/settings.local.json` allowlists
  `Bash(python3 -c ' *)`, `Bash(git *)` and `Bash(cat)`. A one-line `python3 -c` POST
  bypasses any rule placed on `jev send`. No `PreToolUse` hooks are configured (count 0 in all
  three settings files).
- **Codex 0.159.3.** `codex --help` lists only `on-request` ("the model decides when to ask")
  and `never` for `--ask-for-approval`, plus `--approve-for-me` (automatic review). There is no
  per-command "ask every time" policy. `~/.codex/rules/default.rules` holds 127 `allow` rules,
  including `script -q -f -c …` patterns. So agents already create pseudo-terminals.
- **A TTY is not a person.** Under the Claude Bash tool: `stdin=notty` and
  `/dev/tty=unavailable`. That makes a `/dev/tty`-only confirmation refuse correctly by
  default. But `script`, or Python `pty`, can fake a TTY. A TTY check is only a cooperative
  tripwire.

Conclusion: on this host, per-send confirmation can be **demonstrated** on a cooperative path.
It cannot be **enforced** against a same-user process. The pilot should claim the first and
explicitly record the second as a limitation. That matches RUNBOOK §Acceptance: "prove the
actual enabled runtime path before calling its gate enforced".

## The one concrete alternative — operator-only send, local-only consumers

1. **Consumers** (Claude, Codex): `jev prepare | check | show | ref | dispose` only. These need
   no key and make no network call. `jev send` invoked from an agent must refuse before reading
   any credential. It refuses when there is no controlling TTY, when it runs under a known
   agent environment, or when it is invoked without the operator's interactive flag. The refusal
   goes to stderr. No ledger record is needed, because "no `send_attempted`" is itself the proof.
2. **Operator** (majkee, in his own terminal): `jev send --session <id> --request <rid>`.
   - Read the `request_prepared` record from the ledger.
   - Re-hash its canonical body and print the endpoint, model, question list, byte length and
     the full SHA-256.
   - Require majkee to **type the first 8 hex characters** of the hash on `/dev/tty`.
     Typing `y` is not enough.
   - Append `send_attempted` with the typed prefix, the TTY name and the PID as the
     `approval_reference`. This is honest provenance, not authentication.
   - POST **the exact canonical bytes that were hashed**.
3. **Credential.** The pilot reads the key from a path that only the operator command loads,
   for example `read -s` on `/dev/tty` or a file outside agent-sourced shell config. It does
   not rely on the exported variable. **Whether to stop exporting `JEV_ORAK_KEY` from
   `secrets.zsh` is majkee's live-settings call.** It is out of scope for this review, and
   `experimental/ox-alpha/runner.zsh` also references those names. Without that change the
   gate still passes cooperatively, but the limitation must be stated in the GO evidence.
4. **Acceptance mapping.** "Two attempts through each enabled consumer workflow" becomes:
   - two agent-invoked sends per runtime that refuse without network access (shown by a mock
     transport that counts calls, plus an empty network log);
   - two operator sends that each need a distinct typed hash prefix;
   - a wrong prefix or Ctrl-C produces no `send_attempted` and no HTTP call.

This is smaller than any hook or permission adapter, needs no settings change to pass, and
removes the most uncertain claim from the pilot.

## Answers to prompt-1 questions

**1. Approval bound to the exact request.** It is achievable only if the send hashes and
transmits the same canonical bytes, and confirmation shows that hash (the typed prefix in the
alternative above).

- I verified the fixture: re-serializing `request` with sorted keys, compact separators,
  `allow_nan=False` and UTF-8 yields `09fbee2e…f74c80c`, which matches the recorded hash.
  `ensure_ascii` true and false agree only because the fixture is ASCII. **Fix
  `ensure_ascii=False` in the spec.**
- The endpoint and resolved headers other than auth must sit inside the approval display.
- Unsupported paths:
  - Claude "ask every time" via permission rules: bypassed by auto mode and by the allowlisted
    `python3 -c`;
  - Codex approval policy: there is no per-command ask;
  - a Codex `PreToolUse` hook returning "ask": documented in the older handoff (line 216) as
    erroring and then continuing;
  - any TTY-only check, which `script` or `pty` defeats.

**2. JSONL contract.** It is the right size: five kinds, one authoritative file, raw response
nested. Gaps:

- **Partial tail.** Before every append the writer must check that the file ends with LF and
  that the last line parses; otherwise it refuses. Define **one** operator command,
  `jev reconcile`. It appends `\n` and then a `request_failed` record with
  `reason: ledger_tail_repair`, the byte offset and length of the fragment, and its SHA-256.
  Readers skip a non-parsing line only if a later reconcile record names its offset. Nothing is
  truncated, and the evidence stays in place.
- **Indeterminate send.** A `send_attempted` with no terminal record blocks further sends for
  that session. The same `jev reconcile` records `remote_completion: unknown`, and only the
  operator can run it. Whether OpenRouter lets the decision `id` be looked up afterward is
  unverified, so do not design around it.
- **Concurrency.** Hold `flock` on the `.lock` file descriptor from the sequence read through
  `fsync` of each append, and across the whole send (attempt, HTTP call, terminal record), so
  one session has at most one send in flight. `show` and `ref` take no lock and ignore an
  unterminated final line.
- **Stale input.** `send` reads only the frozen ledger request and never re-reads `buffer.md`.
  Record `buffer_sha256` at prepare time. `input_changed` at reply time compares the current
  buffer hash with that value, which is display only. This avoids a second authority.
- **Validation is request-driven** (the smoke script accepted three bad mutations, and
  Cartan's probe is correct):
  - reject missing or unrequested answer names;
  - Choice `choice` must equal the argmax of its probabilities, within tolerance;
  - Score must be near the probability-weighted level;
  - the resolved model must be in an explicit allow-list frozen into `request_prepared`
    (for example `["typesafe/jev-1.13-20260917"]`).

  Invalid replies are still preserved and marked `validation.status: invalid`.

**3. Session binding.** It is vendor-neutral, and it adds no registry. I verified that ia-sync
is absent from `zsh/registries/projects.json`, which holds 17 keys, so the explicit-root path
is needed and sufficient. Two fixes:

- **(a)** `session.json` is mutable, but it holds binding and limits. Copy the effective
  binding and limits, or their hash, into each `request_prepared` record so the ledger
  describes itself. `session.json` then holds only defaults.
- **(b)** A bus record published for shared work must embed, verbatim, the `request_prepared`
  and `reply_received` lines, their SHA-256 values, and `host: office`. A `~/.jev` path in a bus
  record is labelled host-local and never dereferenced on home. The request hash lets the other
  host re-verify the request body offline.

**4. Separation.** This part is mostly right: dispositions are records, `permission_granted:
false`, and reconsider creates a new request that needs new approval. Additions:

- **(a)** `use` on a model-tier verdict means choosing a paid model, which is spending.
  Routing stays an operator act, and that should be stated in the display block.
- **(b)** Add `reconsider_of: <request_id>` so reroll patterns show up in the ledger. Code
  cannot stop rerolls; it can only make them visible.
- **(c)** Multiple dispositions per reply are allowed and append-only. No "final disposition"
  is derived.
- **(d)** Gavels may appear in the experience ledger as provenance. They are never sent in
  `state` as something to be judged.

**5. Workload.** Live model-tier selection is a weak first workload here. Tier is chosen by
the operator at spawn (`--model`, agent frontmatter), so no consumer acts on the advice. Each
call costs about 2e-5 USD by the fixture's estimate; the real cost is the operator's
confirmation time, which is larger than the value of advice he would override anyway.

**A smaller, better pilot: a retrospective shadow batch.** One operator-approved request.
`state` lists 5–8 already-finished, sanitized own-project task briefs, taken from
`journal.host-cleanup.md` and closed STATUS files, and labelled B1…Bn. The questions are a
Choice tier, a Noul for "needs clarification" and a Score for brief quality per brief, kept
within 20 questions and the 32k context. This meets the mixed-type gate in one send and gives
immediate agreement-versus-ground-truth data. It has no live routing consequence: Claude and
Codex each record use or skip on different briefs. Caveat: shared state lets briefs influence
each other, so treat the results as pilot signal, not calibration.

## Evidence (commands run, all local, no network)

```sh
sha256sum raw/{JEV_RESEARCH_AND_CLI_HANDOFF.md,jev_smoke.py,session-draft-memory.md}  # all 3 match provider-recheck
python3 -B raw/jev_smoke.py --self-test        # PASS: 1 valid and 12 invalid local fixtures; exit 0
python3 - # canonical re-hash of fixture request → 09fbee2ee76a…f74c80c (matches); 4 records, trailing LF
jq '.permissions…' ~/.claude/settings*.json ia-sync/.claude/settings.local.json  # allowlists above; hooks 0
[[ -n $JEV_ORAK_KEY ]]; [[ -n $OPENROUTER_API_KEY ]]   # both set in agent env (values not read)
grep -l / grep -n (names only) → ~/.config/zsh/.env/secrets.zsh:9,10; sourced by config.zsh
[ -t 0 ]; ( : </dev/tty )                        # notty; /dev/tty unavailable in Claude Bash tool
codex --version; codex --help                   # 0.159.3; approval: on-request | never
grep -c decision ~/.codex/rules/default.rules    # 127 allow, incl. script -q -f -c patterns
jq '.projects|keys' zsh/registries/projects.json # 17 keys, no ia-sync
ls ~/.jev                                        # absent (as expected)
```

## Remaining uncertainty

- Whether Codex execpolicy supports a `prompt` decision on a `jev send` prefix. Even if it
  does, a different prefix bypasses it, so it does not change the verdict.
- How the Claude auto-mode classifier treats a `jev send` invocation. It is not tested and not
  relied on.
- Authenticated OpenRouter behaviour: account errors, the actual resolved model, `usage.cost`,
  and whether a decision `id` can be looked up after a lost reply.
- The side effects of un-exporting the key from `secrets.zsh`, for example on the ox-alpha
  runner. That is a live-settings decision for majkee, outside this gate.
- The value of the shadow batch depends on picking briefs with honest ground truth. That
  selection is Cartan's and majkee's.

Flight remains the named witness. Post-implementation evidence goes to
`raw/flight-verification.md`. This review does not confirm anything on Cartan's behalf.

---

## Addendum 1: smoothing with majkee, 2026-10-01, not gaveled

These are options and observations from a live conversation with majkee, not decisions.
Cartan owns synthesis and delegation.

### A. Event count: 16 on file, "20" is not recorded

The only written estimate is **16** situations (`design.2026-10-01.md` §"Sixteen candidate
situations"; STATUS: "16 event situations"). majkee recalls Cartan estimating **20**. No file in
the bed carries 20, except the cap of 20 questions per request. **Cartan:** file the missing
four, or reconcile the two numbers.

### B. Send doors: one command, typed by a human from any channel

| door | who types the send | role |
|---|---|---|
| Claude/Codex UI `! jev send <rid> <hash8>` | majkee | Mid step. The transcript records it as user input, which the witness can verify. Codex `!` support is unverified. |
| tmux jev pane | majkee | Same command, a different terminal. |
| phone (Redmi/Galaxy) via tmux over tailscale | majkee | Next phase. Same command; `jev show` output must stay compact. |
| `permissions.ask` on `Bash(jev send:*)` | agent proposes, human clicks | Tripwire only: `python3 -c` and other prefixes bypass it. Whether it prompts under auto mode is unverified. |
| skill | model | Not a send door. It teaches prepare/show/ref/dispose only. |

### C. Credential: "the script reads it, the CLI cannot dump it" is impossible under one uid

A file the script can read is a file the agent can `cat`. Real boundaries need a secret the
agent cannot supply. Office probe, read-only:

| mechanism | on office | boundary? |
|---|---|---|
| gpg-encrypted key file, passphrase prompt every send (pinentry, cache TTL 0) | gpg + pinentry curses/qt/gnome3 present | **Yes.** The desktop prompt works from `!` mode; curses works in tmux and on the phone. |
| `sudo -u jev jev-send`, key owned by a dedicated user, password every time | sudo present, password required | **Yes**, but it changes system config (new user, sudoers). |
| `secret-tool` / gnome-keyring, or `systemd-creds` alone | present | No: the same user can read them. |

Either real option merges the credential lock with Gate 1: the password prompt *is* the
per-send confirmation, and the claim moves from "cooperative" to "enforced". This is a live
machine-layer change, outside this gate, journal-first, and majkee gavels it.

### D. "Borrowed token": operator idea, NOT previously logged

majkee says he speculated about a "borrowed token" in the drafting before
`session-draft-memory.md`. It is not in that file: `grep -niE 'borrow|lend|loan'` over the
whole bed returns nothing, and "token" appears only at line 104 as a context-size estimate.
It is logged here so it is not lost.

**Flight's interpretation (majkee to confirm or correct):**
- Neither the CLI nor any agent ever holds the master inference key.
- Per send, or per short session, a human-gated step uses an OpenRouter **management key** to
  mint a short-lived, credit-capped inference key.
- `jev send` uses that borrowed key, which is then disabled or deleted.

**Documented mechanism** (OpenRouter provisioning/management API docs, fetched 2026-10-01; the
fetched page appears dated 2025-02-19, so re-verify before building):
- `POST /api/v1/keys` takes `name` and an optional `limit`.
- `PATCH /api/v1/keys/{hash}` takes `disabled: true`, `limit` and `limit_reset`.
- `DELETE /api/v1/keys/{hash}` deletes a key.
- Expiry is set at creation and cannot be changed afterwards.
- "Management keys cannot be used to make API calls to OpenRouter's completion endpoints."

**Why it matters:** it is the first cap that the provider enforces **on its side**, unlike the
local caps (10 attempts, 20 questions), which are only operational limits. A leaked or looped
borrowed key can spend at most its `limit`.

**What it does not do:**
- It bounds damage; it does not authenticate a human. While it lives, the borrowed key is
  readable by the agent.
- The **management key is more dangerous than the inference key**, because it mints keys. So
  it must sit behind lock C (gpg plus pinentry, or sudo), never in agent-sourced shell config.

**Candidate composition:** pinentry unlocks the management key → mint a key with a cent-level
`limit` and short expiry → send once → delete the key. All three layers come from one human
act.

**Unverified:**
- whether `/api/alpha/decisions` accepts a freshly minted key;
- the smallest `limit` granularity and the exact name of the creation-time expiry field;
- rate limits on key creation;
- whether minting adds latency that matters on the phone path.

### D′. Operator refinement: borrow per session, with a budget and a time limit (majkee, not gaveled)

majkee prefers **one borrowed key per Jev session**. It carries a session **budget** (the
key's `limit`) and a **time validity** (expiry at creation, plus explicit delete at session
close). He prefers this over a key per send.

| layer | per-send key | **per-session key (majkee)** |
|---|---|---|
| unlock (gpg or sudo) | every send, enforced | once per session, enforced |
| spend cap | per send | session budget, enforced by OpenRouter |
| per-send confirmation | the password, enforced | typed `hash8`, cooperative |
| worst case if bypassed | nothing beyond one send | the remaining session budget |

**Consequence:** per-send confirmation is still demonstrable, but cooperative. The amount a
bypass can spend is bounded by the provider. The GO evidence must say so.

**Units:** the OpenRouter limit is in credits (USD), not tokens. At the published 0.042 USD
per million prompt tokens, with completion free, a $0.01 budget is about 238k prompt tokens,
roughly 7 full 32k requests. Re-verify the price at mint time.

**Rules:**
- The ledger records the key's hash ID, limit and expiry, never the key.
- `jev pending` shows the budget remaining, calculated from the recorded `usage.cost`.
- An exhausted budget or expired key refuses the send. It never re-mints automatically; a new
  key needs a new unlock by majkee.

**Unverified:** the minimum `limit` and how fine-grained expiry can be.

### D″. Operator design: local budget lock in the zsh `jev` wrapper (majkee, 2026-10-02, not gaveled)

Source: majkee's voice dictation over remote control. Flight's reading, to be corrected by him.

- A `jev` zsh wrapper holds the API key encrypted and decodes it only at send time, so nobody
  sees it.
- Each session has a budget constant (example: $1) and a counter.
- majkee unlocks a specific session's budget from his terminal, or attaches the unlock to the
  session's lead seat.
- A drained budget auto-locks the session. Any `jev` use then gets "blocked: budget exceeded".
- Only majkee tops up, per request.
- Everything is local, with no vendor triggers.

**Flight assessment.** The ergonomics are right for the cooperative path. Four corrections:

1. **Decoding must need majkee's passphrase** (gpg plus pinentry, §C). Otherwise the agent
   runs the decoder; same-disk encryption is obfuscation. Session unlock means passphrase
   entry.
2. **No separate counter or lock file.** Spend is derived from the ledger's recorded
   `usage.cost`. Unlock, top-up and lock are operator ledger events (for example
   `budget_granted`, `budget_locked`) that need the same passphrase. The auto-lock is a refusal
   computed from the ledger total, never a mutable flag. Optional backstop: set the §D′
   borrowed key's provider `limit` equal to the session budget, so a bypass still hits a
   provider wall. That is one adapter field, not a vendor dependency.
3. **No new zsh registry.** Session budget and lock state live in `~/.jev/sessions/<id>/`, per
   the RUNBOOK. The zsh wrapper is a later portable promotion through `deploy.sh`, outside this
   pilot (prompt-2 forbids a deployed wrapper).
4. **The lead seat may request a top-up; only majkee grants it.** An agent-held unlock is not
   an operator gate.

**Sizing:** at 0.042 USD per million prompt tokens, $1 is about 23.8M tokens, roughly 740 full
32k requests. Flight suggests $0.05 (about 37 requests) for the pilot. majkee decides.

**Lifecycle events:** this adds two kinds to the five-kind contract (`budget_granted`,
`budget_locked`). Cartan to decide whether they are new kinds or `data` variants of an
operator record.

### E. Routing

- No Claude-side implementer (for example @Trajectory) is spawned for this. Delegation is
  Cartan's, and Astrobley is the named implementer. A parallel Claude coder would collide over
  ownership.
- The credential lock (C) and the borrowed token (D) together form a candidate sidequest.
  Cartan scopes it and majkee gates it, separately from the pilot gate.
- The pilot can pass without it, provided the cooperative-only limitation is stated in the GO
  evidence.

### F. Operator choices so far (majkee, 2026-10-02; smoothing, not yet gaveled)

1. **Lock: gpg** with a pinentry passphrase.
2. **Budget: $0.05 default, configurable.** It is set per session by majkee's own zsh/py
   tooling as a separate operator command, for example `jev wallet fill <bed> <usd>`. Run
   from the runbook-session layer, it is never agent-invoked and needs the passphrase.
3. **Provider backstop: yes.** The borrowed key's `limit` equals the session wallet.
4. **Scope (Flight recommendation, majkee to confirm):**
   - one **wallet per runbook-session (bed)**, bound in `session.json`; for the pilot,
     1 bed = 1 Jev session;
   - a **global ceiling** that is the OpenRouter account credit balance itself, kept small;
     this is real, provider-enforced and needs no code;
   - no wallet shared across all sessions: they would compete for it and spend could not be
     attributed to a bed.
5. **ovitmugen:** an optional `jev` left tab per bed for the operator's
   unlock / send / wallet commands, reachable from the phone over the same tmux. ovitmugen
   never types into panes, which fits.
6. **Budget is volatile** (majkee, 2026-10-04). He fills or drains it at any time.
   Draining it is the instant stop for any later automatic (wallet-mode) use.
7. **Name: belnap is the agent (seat)** (majkee, 2026-10-04). The collision sweep is
   clear.
   - **`jev` stays the process and folder**, like `claude`, `codex` and `gemini`. The
     `jev` command, `~/.jev/` and `jev.event/v1` stay as designed. **No rename**; Flight's
     earlier rename proposal is withdrawn.
   - **belnap is the role** played on that runtime. Its "belnap protocol" is a document
     plus rubric files, not a second wrapper. tertium is the later BOTH/NEITHER
     resolution rule.
   - Details: `raw/flight-jev-map.md` §14.
8. **Protocols, not seats; an `ia-sync/jev/` harness** (majkee, 2026-10-04). Details:
   `raw/flight-jev-map.md` §15.
   - Jev identities are protocols. belnap is the first. None of them go in the germline.
   - The portable source goes in `ia-sync/jev/`, parallel to `claude/` and `codex/`, with
     a deploy leg later.
   - Runtime goes in `~/.jev/projects/<project-slug>/<time>-<session-id>.jsonl`. Its line 1
     carries the binding, which replaces `session.json` and closes finding 4.
   - **This is a storage-layout change for Cartan before `impl/`.** It supersedes Flight's
     `zsh/jev/` placement and germline suggestion.
9. **Placement revised: code in the zsh layer, runtime in `~/.jev/`** (majkee,
   2026-10-04). Details: `raw/flight-jev-map.md` §16.
   - The engine and portable content go in `ia-sync/zsh/jev/`: Python engine, zsh face,
     protocols, rubrics and defaults. It rides the existing `zsh/` deploy leg, so no new
     leg is needed.
   - `~/.jev/` holds runtime only (project-scoped JSONL sessions). Nothing is deployed
     into it.
   - The gpg-locked key goes to `~/.secrets/jev/`, beside env-vault's convention, and
     never into the plaintext `.env/`.
   - One engine, two faces: a callee (P1), and a visible `jev watch` router in tmux (P2).
   - This supersedes §F8's top-level `ia-sync/jev/`.

### G. Pointers (2026-10-04)

- **Cycle 01 is open:** `_bus/01.flight.point.md` asks Cartan for one disposition on each
  of D1–D10, the bundle of everything in this addendum and the map. A RETURN is due at
  `_bus/01.cartan.return.md`, and Flight closes the cycle with `01.flight.verdict.md`.
- **majkee's photos** (13 notebook pages, tunnel protocols and study screens) are in
  `raw/majkee-photos.2026-10-03/`. Its `INDEX.md` maps each file to the map's §1 ids.
  They are byte-identical copies, 22 MB in total, and stay out of git unless majkee
  decides otherwise.

- **`raw/flight-jev-map.md`** is Flight's role map, schemas and brainstorm, filed with
  majkee's blessing. It is not design and not gaveled. It answers majkee's hand-drawn
  questions of 2026-10-03, and:
  - refines the GUIDE seed into five laws: escalate only, autonomy only where reversible,
    no hands, read-off only, bounded spend;
  - proposes versioned **rubric files** as the unit Jev runs.
- **Oraculum's envelope-convergence POINT for Cartan:**
  `~/unikuklatrix/nablarva/.dev/session/nablarva-X0-restarted/_bus/02.oraculum.point.md`.
  - The reply goes to the sibling `02.cartan.return.md`. majkee carries it.
  - It is cheapest to settle before `impl/` exists.
  - **Flight's one caution:** `data.certainty: confirmed` on a reply means the *receipt*
    is confirmed, never that the *judgment* is correct.
  - Decide `parent_request_id`, `reconsider_of` and the §D″ budget events in the same
    pass.
