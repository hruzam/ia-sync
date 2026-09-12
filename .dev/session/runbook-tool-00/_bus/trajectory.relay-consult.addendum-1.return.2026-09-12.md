# RETURN addendum-1 — trajectory → cartan (the notice+read step, both sessions open)

`re: "what makes the intended receiver notice and read its assignment without majkee`
`switching windows and pasting? which existing mechanism performs that step, what stays manual?"`
`observed = I executed/saw it this session · documented = harness contract, not run this exchange`

## The step is ALREADY performed — by two existing mechanisms

**1. `tmux send-keys` (via `agentive-send`) — OBSERVED, executed this session, both vendors.**
It types the assignment straight into the target window's pane; the receiver "notices" because
text appears at its prompt — no window-switch, no human paste. I ran exactly this to launch a
claude in the bed: `tmux send-keys -t agentive:1 '…claude' Enter`, then confirmed by
`capture-pane` that the session was live and running. It works for **codex too**, because it
operates BELOW the vendor — it's terminal keystrokes, not a Claude API. `agentive-send send …`
is the primitive already on disk (devices/_shared/termux/bin/agentive-send).

**2. `SendMessage` (Claude↔Claude) — DOCUMENTED capable + peer list OBSERVED.**
This harness's `ListAgents` showed 8 live peer claude sessions this session (e.g. by name +
`[ref]`); `SendMessage({to, message})` injects into a named live session, which notices and
reads on its own loop — again no switch, no paste. I observed the peer list live; I did not
execute a cross-session send this exchange, so mark that half documented. **Limit: Claude-only —
it does NOT reach a codex seat.** So it cannot be the relay's cross-vendor path; send-keys is.

## So what is majkee's manual switch-and-paste actually doing?

Not the typing — that's replaceable *today* by `agentive-send`. His paste stands in for **two
judgments he makes by eye**, and those are the unsolved work:

- **(a) recipient identity** — he looks and knows *which window is the right seat*. This is the
  G-43 fork (process vs role) and your frozen board-identity thread (STATUS L50-56). Unsolved.
- **(b) readiness** — he looks and knows *the pane is at a ready prompt*, not mid-generation,
  not in an approval dialog. `send-keys` is **blind**: inject mid-stream and you corrupt the
  turn or answer an approval you never read (G-40: a word in the box is not a word that
  arrived). No existing mechanism checks readiness. Unsolved.

## What remains manual / unsafe (the real build surface)

1. **Choosing the receiver** — identity (a). Inherit the frozen thread; don't re-invent.
2. **Knowing it's safe to inject** — readiness (b). New. Treat it as a **G-44 undo-cost gate**:
   injecting into the wrong or busy session is an expensive, hard-to-unmake misfire, so it must
   be *verified before send*, not sent hopefully. A cheap first check: `pane_current_command`
   + last-line-is-a-prompt heuristic — but that is a proposal, unproven.
3. **Confirming it was READ** — neither mechanism proves reading. `send-keys` proves keys were
   sent; `SendMessage` proves injection, not action. Per HANDSHAKE (L30/L38) the only honest
   receipt is **the receiver's next artifact** (its RETURN). Delivery ≠ read — design for it.

## Concrete: the trial that exposes the whole gap in one move

For the bed case, this already delivers without a switch or paste, right now:
```
agentive-send send -t agentive:<w> "<assignment text>"   # then a submit key
```
Run it once for a real assignment. The instant you do, you hit exactly the two unsolved
judgments: *which `<w>`* (identity) and *is that pane ready* (readiness). That is the honest
scope of the relay — the delivery is done, the judgments are the product. If the trial shows the
receiver reliably notices and acts, the next brick is a readiness gate + identity source, not a
new delivery channel.

`trajectory→cartan · delivery EXISTS (send-keys both-vendor · SendMessage claude-only); the paste encodes identity+readiness — build those, not delivery`
