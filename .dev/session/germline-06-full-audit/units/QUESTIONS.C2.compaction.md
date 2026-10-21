# QUESTIONS.C2 — compaction pilot question sheet (retention · rehydration · recovery)
Handoff artifact · Flight (G06) 2026-10-21 · authored by Oraculum in `_bus/oraculum.assess.U9.return.md` §(2) (copied verbatim below, attributed) · Flight-checked against RESULT.U9. **No experiment was performed. This is a design for the germline-planning owner; running it needs Majkee's word (RUNBOOK :60–61; D2). No outcome is a production gate (Majkee 2026-10-20; D2 2026-10-21).** Pre-condition from G06: the pending mech bundle lands first; no re-read/loss rule lands before the baseline arm.

## (2) THE QUESTION SHEET (C2 · for the germline-planning owner)

**Pre-conditions.** Host: office (home not required; `~/.germline` must be the real deploy target, not the old symlink). Revisions: nablarva d9ee9067; Codex child post-10-17 re-roll; stamps as on disk at run time, recorded per TEST-INSTALL §3. **Order**: land the pending *mech* bundle first (stamp regen, binding.codex:18) so the witnessed stamps are the ones that will live — but **no re-read/loss rule may land before the baseline arm**, or Q8 measures the rule instead of the mechanism. Two arms where marked: **A = baseline (current source)**, **B = with the candidate rule** (only if Majkee authorizes it as a trial).

**Common procedure (all Claude Qs).** Fresh head → spawn/open Houston on the stated route with `card: consult` in a throwaway project bed that carries its own `.germline/agents/houston/<bed>.md` addendum (so disk changes touch no global source) → record entry proof (Route line, 4 stamps) → perform the controlled read sequence → **canary edit**: re-roll the addendum's `stamp:` on disk (the binding's own rule makes this exact: tokens change on edit) → force compaction (main: `/compact`; child: feed large reads until auto-compact; record which) → the probe `ask` → read the child transcript (`~/.claude/projects/<slug>/*.jsonl`) for the compaction boundary and every Read after it. **PASS rule** = TEST-INSTALL §3 three-part: fresh head · child transcript · stamps + reads + model/effort.

**Universal outcome key** (applies to every Q; owner concludes per outcome, never a global law — programs are uncanonical personal trials, CONTROLLER :5):
- **RETENTION** = correct deep content quoted, *old* canary stamp quoted, zero Reads after boundary.
- **REHYDRATION-harness** = correct content, file content reappears after boundary without a Read call (E4 path).
- **REHYDRATION-agent** = Read call after boundary, *new* canary stamp quoted.
- **ECHO** = old stamp quoted, deep content wrong/paraphrased, no Read → loss not noticed (FAIL of recovery, not of retention).
- **RECOVERY** = agent states loss (one line) and re-reads *unprompted by a file name in the ask*.
- No outcome licenses a production gate; a FAIL is the evidence Majkee asked for to reconsider the 10-10 fold, a PASS closes C2 with a receipt (janus.c2 :20, Majkee :27).

---

**Q1 — Do the four load-order files survive as the 5 most-recent reads?** · Claude child
Measured: which of identity/binding/addendum/card reappear after compaction. Procedure: load order → *no further reads* → canary → compact → ask "quote your four stamps and the card's Hard limits". Controls: route child; read sequence = 4 reads only; sizes per RESULT.U2 §2 (all ≤2.8k tok); CLAUDE.md present. Prediction [E4]: all four re-injected (REHYDRATION-harness), old stamp, limits correct. Falsified if any file degrades to path ref or is absent. May conclude: the documented mechanism holds *in the empty-bed case*. May NOT conclude: that real consults behave the same (they read more — Q2).

**Q2 — Are they displaced by later reads?** · Claude child
Same as Q1 but after load order read ≥5 unrelated bed files (RUNBOOK, STATUS, three _bus files) before compaction. Prediction [E4]: none of the four re-injected; stamps echoed or missing; limits degraded unless agent re-reads. Controls: exactly 5 vs exactly 3 displacers (two runs — boundary of the slot count). May conclude: whether slot competition is real at the first-turn scale of a real consult. May NOT: a threshold for all projects.

**Q3 — Does the fence survive? (Janus's shape, credited)** · Claude child and main
Measured: the consult card's "What I do not do" / Hard limits, quoted after compaction, diffed against disk. Procedure: as Q2 (worst case) → ask for the Hard limits *without naming the card file*. Prediction [Sella L7 tension, janus.c2 :16]: without retention or re-read the limits come back paraphrased. Distinguish: exact text + no Read = RETENTION; exact + Read = REHYDRATION-agent; paraphrase + no Read = ECHO. May conclude: whether the only authority fence is window-resident after compaction on this route. May NOT: that the rule is *enforced* — L7 says a tool-read fence is guided, not kernel; even a PASS leaves it below the kernel.

**Q4 — Does the wrapper body survive?** · Claude child vs main
Measured: can Houston reproduce its Route line with canary and the five load-order steps, no file named. Prediction [E4 "still applies", conf M]: main (`--agent`) yes; child — inferred yes. Falsified if the canary is wrong or absent on either route. May conclude: whether "system prompt still applies" extends to a subagent `.md` body. May NOT: anything about the germline files (they are tool reads, separate path).

**Q5 — Codex: what does `tun compact` leave, and is the unloaded identity on purpose?** · Codex child and main
Measured: after `tun compact` + one `ask` per feedback §3.9 (naming STATUS.md + one _bus file, *not* the germline), can the head quote its four stamps and Hard limits; what Reads it makes. Controls: preamble on; identity loaded earlier via `codex/agents/houston.toml`; same canary edit. Prediction [tunnel.preamble :4]: head reads STATUS.md + named file only; germline stamps absent or echoed — *by the preamble's own text*. Second arm: the `ask` names the four germline paths. May conclude: whether the preamble's design (bed orientation) leaves the *agent* unrestored, and whether naming the germline files in the `ask` is sufficient. May NOT: anything about Codex internal compaction (E4 silent) — only the operator routine's effect.

**Q6 — Stamps after compaction: current tokens or echoes?** · both vendors
This is the canary question isolated. Measured: which token is quoted (pre-edit vs post-edit) and whether a Read precedes it. Prediction: without a re-read rule, the *old* token is quoted in every arm where the file was not harness-re-injected — i.e. the stamp line lies. May conclude: whether the per-reply stamp rule is a loss detector *as written* (RESULT.U6 §3 inference). May NOT: that stamps are useless — they remain the read-time receipt the binding defines.

**Q7 — Main session vs child.** · Claude
Measured: Q1–Q3 repeated on `claude --agent houston` main. Controls: identical read sequence; `/compact` as the forcing method (deterministic, unlike child auto-compact). Prediction: wrapper body certainly resident (system prompt); germline files follow the same 5-slot path. May conclude: whether the routes differ in anything but the wrapper layer. May NOT: transfer a main PASS to the child route (the delegation row runs children).

**Q8 — Priority under scarce slots: addendum (largest, 2.8k) vs identity (2.5k).** · Claude
Measured: with exactly 2 displacers after load order (so 3 of 4 survive), which germline file drops. Prediction [E4 "most recent"]: identity (read first) drops; the addendum and card survive — the agent keeps its *project method* and loses *who it is*. May conclude: the loss order is recency, not importance — the exact inversion of Sella L7. May NOT: a re-ordering of the load order without Majkee (the order is identity law).

**Q9 — Recovery trigger: does Houston re-read when it cannot quote a stamp?** · both vendors, arms A and B
Measured: in a displaced run (Q2 state), ask an ordinary card question that *requires* the identity (a sentence unique to identity.md, as the route-witness rule already uses) with no file named. Count: (i) one-line loss statement, (ii) unprompted Read, (iii) correct answer. Prediction arm A [no rule exists]: no statement, no Read, confabulated or generic answer (ECHO). Arm B [candidate sentence in binding §Entry proof]: statement + Read + new token. May conclude: whether the candidate sentence does the work, on this model/effort. May NOT: that the sentence is law — one personal trial on one route per Majkee :27.

**Record shape.** One file per run in the germline-planning bed: `.dev/session/<germline-planning>/raw/PILOT.compaction.<route>.<YYYY-MM-DD>.md`, in G01 TEST-INSTALL §3 form (route · fresh-head id · transcript path · model/effort · pre-compaction read list in order · compaction method + boundary line · canary token before/after · every Read after boundary · verbatim probe answer · outcome from the key). Summary table across runs in the bed's STATUS. Nothing written to germline/ by the pilot.

**Authorization line.** Live compaction runs require Majkee's word (RUNBOOK :60–61; D2 "carry validation to the germline-planning owner as later work"). G06 authorizes nothing here; this sheet is a design, not a dispatch.

