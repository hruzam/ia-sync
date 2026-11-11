# Native TUI notification plus file bus — observed Jev cooperation

Cartan(jev-01), office, November 10. Transfer material for majkee to relay to Nablarva.
This is an observed local substrate pattern, not a new global primitive, canon promotion
or a claim of cross-host transport. No message was sent to Nablarva by this document.

## What worked

Two existing main Codex sessions cooperated through native TUI messages while keeping
assignments, evidence and verified decisions in the existing Jev session `_bus/`.
The reader peer was **not** a newly spawned child and was not controlled through
`collaboration.send_message`. Both seats called themselves Cartan; file writer label
`cartan-reader` disambiguated ownership without creating a new persona/profile.

- Engineering head observed thread: `01a17a76-073b-7750-8bd9-7a899d3b4646`.
- Reader peer observed thread: `01a1aa8a-b5d4-70d3-9823-4f44f05af2d2`.
- Bus: `~/ia-sync/.dev/session/jev-01-codex-pilot/_bus/`.
- Authority: majkee explicitly blessed peer→head TUI delivery and allowed replies **only
  for receipt confirmation and bus information**. Later: max10 further handoffs, wait for
  completed turns, no overlapping assignments or repeated nudges.
- Post-limit exchange used3 notifications: cycle11 POINT pointer, completed RETURN pointer,
  closure pointer. No assignment is active; do not consume the other7 merely because allowed.

## Mechanism observed, not promised persistence

Discover tool metadata by name/description in the current runtime. The observed callable was
`tools.mcp__codex_tui__send_message_to_thread` inside `functions.exec`, with:

```javascript
await tools.mcp__codex_tui__send_message_to_thread({
  threadId: "01a1aa8a-b5d4-70d3-9823-4f44f05af2d2",
  prompt: "Received RETURN. VERDICT and next POINT are available at the exact bus paths."
});
```

Tool metadata imposed a maximum1000UTF-8-byte prompt; `model` is optional and was omitted.
Calls returned the target thread ID. Incoming events appeared with `source_thread_id` and
an input string carrying the RETURN path. Tool acceptance alone did not prove peer reading
or task completion; the subsequent RETURN and its verified artifacts supplied that evidence.
The tool can trigger a turn, so a courtesy notification is not assumed side-effect-free.
Do not use it as a keepalive or send duplicate prompts while the other seat is working.

A successor must discover current availability and use **its own observed CLI identity**.
These old handles are addresses observed on this host, not an API guarantee that they can
be resumed indefinitely. On a new real assignment, identify the successor's current thread
in the POINT/notification so the peer does not return to the retiring head. If no native
route exists, majkee can relay a path; never invent a watcher or reset thread ownership.

## Durable discipline

Apply `~/reposoma/raw.guides/bus/GUIDE.md`, especially **File ownership and cycle economy**,
**RETURN — six fields, all mandatory**, and **Verifying a RETURN**:

1. Head writes one bounded `NN.cartan.point.md`, with exact read/write ownership and done-when.
2. Send one short native notification pointing there; authority/scope remain in the file.
3. Wait for the peer's completed `NN.cartan-reader.return.md`. Presence of a file while it
   is being authored is not a finished handoff. Do not enqueue more work during its turn.
4. Inspect actual diffs/artifacts and rerun proportional checks. Head writes one VERDICT;
   only head updates STATUS. A RETURN is evidence pointers and claims, not verified truth.
5. Send only receipt/verdict/next-POINT paths. A fix is a fresh cycle, not edits during review.

No per-message Markdown files, inbox/read markers, daemon or second STATUS were introduced.
The bus keeps past exchanges; STATUS alone keeps current position. Thread messages are
notifications, not a second authority or a substitute for durable evidence.

## Evidence and scars

- Cycle09: peer found actual Markdown fidelity failure; head independently reproduced it.
  `~/ia-sync/.dev/session/jev-01-codex-pilot/_bus/09.cartan.verdict.md` is REVISE.
- Cycle10: seven tests and original examples passed, but head's additional tilde-fence
  counterexample failed. `~/ia-sync/.dev/session/jev-01-codex-pilot/_bus/10.cartan.verdict.md`
  is REVISE. Passing the author's tests did not justify installing the change.
- Cycle11: peer corrected only the demonstrated gap; head verified8tests and exact prior
  counterexamples, ACCEPTED, then separately installed2files with backup and fresh checks.
  `~/ia-sync/.dev/session/jev-01-codex-pilot/_bus/11.cartan.verdict.md` and
  `~/ia-sync/.dev/session/jev-01-codex-pilot/raw/reader-installed-check.2026-11-10.json`.
- Budget did not become a mandate to run10turns. Completed turns, bounded ownership,
  short notifications and one STATUS kept this exchange legible.
- Raw Markdown substring presence did not prove safe rendered output. Parser-level tests
  mattered; acceptance remains scoped to Python-Markdown3.10.3 configurations, not all GUIs.

## Reuse boundary for Nablarva

This can inform a bounded native notification adapter over an existing project bus. It does
not justify replacing that project's current ownership/status paths, adding automatic
agent chains, or treating tool delivery as an acknowledged protocol. Local operator consent
and available thread tools are prerequisites. Explore any generalization in the owning
project's task bed; this note makes no harness/config change and no deployment request.
