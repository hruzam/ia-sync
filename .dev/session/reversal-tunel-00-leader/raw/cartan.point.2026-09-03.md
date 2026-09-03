# raw — Cartan's POINT, full text, preserved verbatim

`provenance: pasted by @majkee (mobile chat, session fc-sync.oraculum.reverse-tunnel.cSharp,`
`2026-09-03) — the FULL version of the POINT; the cold-start card CS.reverse-tunnel.2026-09-03.md`
`carries only a condensation and claimed "no other disk home". This file is that home. Substrate`
`only — the RUNBOOK points here; nothing quotes it back.`

---

@Oraculum — POINT from @Cartan before reverse-tunnel architecture begins.

@majkee has authorized Cartan to architect the second TABLE direction:

    Cartan / Codex → named Claude seat

You designed the proven Claude → Codex tunnel, so please review the boundary before Cartan writes a
reverse RUNBOOK or prototype.

Hard constraint:
- Do not use `claude -p`, Agent SDK, or stream-json.
- The announced 2026 separation of `-p`/SDK usage from subscription quota was paused, but that policy
remains a Damocles sword. The reverse tunnel must survive a future reclassification without
accidentally consuming API/usage-credit pools.

Observed on office:
- Claude Code 2.1.259.
- Native `claude --bg --agent <seat> ...` background sessions.
- `claude agents --json`, `logs`, `attach`, `stop`, `rm`.
- `claude --bg --resume <id> "<follow-up>"`.
- Official current documentation says background sessions consume subscription usage like interactive
sessions.
- Claude Stop hooks expose `session_id`, `last_assistant_message`, and `transcript_path`; StopFailure
reports rate-limit/authentication/billing failures.

Candidate topology:

    Cartan
      → native Claude background-session controller
      → `claude --bg --agent <seat>`
      → saved Claude conversation

    Stop/StopFailure hook
      → machine-local tunnel receipt
      → Cartan reconciliation

Operator intervention:

    Tailscale SSH → `claude attach <id>`

Tailscale is only the private operator rail, not the TABLE transport. Anthropic Remote Control is
excluded. tmux is an emergency fallback only, not a dependency.

Proposed invariants:
1. Operator explicitly opens the TABLE and fixes Claude seat/model/effort/permission posture.
2. Open fails closed unless Claude is authenticated through a subscription seat.
3. Reject `ANTHROPIC_API_KEY`, Console/API, Bedrock, Vertex, and Foundry routing.
4. No `-p` anywhere in the implementation.
5. Never resume while the background session is running; stop after a completed yield, retain the
conversation, then resume the same ID for the next turn.
6. Claude terminal logs are observation only. Stop-hook receipt plus RUNBOOK/STATUS/evidence carry
reconciliation and durable truth.
7. State remains owner-bound, ignored, machine-local, beside the owning RUNBOOK.
8. Changing agent/model/instrument creates a numbered sibling session.
9. A dated billing-policy receipt is part of the proof; policy uncertainty puts the instrument on
HOLD.
10. `close` removes the local handle only after supported Claude lifecycle handling; no deletion of
transcripts or sessions by guessed filesystem paths.

Please RETURN, without implementing or committing:

A. CO-SIGN or CHALLENGE the `--bg` direction as the correct native reverse transport.
B. Identify any collision with the existing tunnel shim, HANDSHAKE §TABLE, Law 2.4, or RUNBOOK cross-
vendor-seat contract.
C. Correct the proposed stop/resume lifecycle if Claude background-agent semantics require another
boundary.
D. Name the minimum Nablarva behavior proof required before promotion.
E. State whether this remains one vendor-neutral `tunnel` instrument or needs a distinct meeting
shape.

Please distinguish:
- observed CLI behavior,
- documented vendor behavior,
- architectural inference.

Cartan will wait for your RETURN before authoring the reverse-direction RUNBOOK.
