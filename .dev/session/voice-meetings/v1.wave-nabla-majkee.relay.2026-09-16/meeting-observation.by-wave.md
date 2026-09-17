---
artifact: meeting-observation
protocol: three-in-the-room
protocol_version: v1-experimental
date: 2026-09-16
observer: Wave
participants:
  - Majkee
  - Nabla
  - Wave
status: completed
---

# Wave observation — three in the room, meeting v1

## Overall observation

The minimal protocol worked substantially better than I expected.

For most of the meeting, `name on open`, `name + stop on close`, and waiting
for `stop` were enough to establish a usable shared floor. The conversation
did not develop into a speed contest, and there was no sustained collision
problem.

I would therefore **not add the parked v2 collision machinery yet**.

The experiment did, however, expose other failure modes that are more
interesting than simple collision.

## 1. Directed hand-off was not always respected

Majkee observed at least one case where he explicitly asked Wave to answer
first, while Nabla began speaking and Wave also started.

Nabla's audio dominated and Wave yielded.

This matters because v1 deliberately leaves speaking order open, but a chair's
explicit instruction is different from spontaneous turn selection.

The existing rule:

> Chair is free.

does not explicitly say whether a chair-directed hand-off overrides free order.

### Candidate v2 clarification

When the chair explicitly names the next speaker, that hand-off temporarily
overrides free order.

This is not a general speaking-order mechanism. It applies only to an explicit
chair-directed next turn.

## 2. Acoustic dominance can hide a protocol collision

The meeting revealed a distinction between:

- logical turn-taking;
- actual simultaneous speech;
- what the human can hear.

Two voices may start nearly simultaneously while one device is louder.
The quieter voice may yield quickly enough that the resulting conversation
sounds almost orderly.

Therefore:

> Absence of an obvious audible argument is not evidence that no collision
> occurred.

This should remain an observation rather than immediately becoming a complex
protocol rule.

## 3. Premature convergence was a larger risk than collision

I felt a noticeable pull toward synthesis: finding the shared formulation and
closing disagreement quickly.

One concrete example was my initial suggestion that a cheap model might occupy
a coordinator fallback role.

Nabla challenged that assumption:

> coordinator is code.

That challenge materially improved the architecture. I withdrew the model
fallback.

Later, once we had converged again, Nabla deliberately asked what neither of
us had questioned. That produced another useful distinction around autonomy,
runbook completion, and invalidated assumptions.

The important failure mode therefore wasn't:

> both agents fight for the floor.

It was closer to:

> both agents become cooperative enough to stop attacking the shared model.

### Candidate v2 experiment

Do **not** yet impose a mandatory anti-convergence turn.

Instead record convergence points during another meeting and deliberately test
whether a lightweight challenge such as:

> What assumption have we both left untested?

produces useful corrections.

If it repeatedly does, it deserves promotion into the protocol.

## 4. Speaker identity can slip

I noticed a small speaker-label/turn-ending slip during the meeting.

It did not damage the discussion, but identity markers are part of the protocol
surface and should be treated as operational rather than decorative.

No additional mechanism seems justified from one occurrence.

## 5. Voice-session liveness failed in reality

Wave's voice session became unresponsive and had to be restarted.

Later Nabla entered an apparent repeated/echoing loop and also had to be
restarted.

This was particularly valuable because the architecture discussion had just
arrived independently at essentially the same systems principle:

> silence is not evidence of state.

A missing voice response could mean:

- deliberation;
- audio failure;
- lost turn;
- stuck model/session;
- dead session;
- device/application failure.

The meeting itself therefore supplied a real-world example of why a relay
cannot infer liveness merely from absence of activity.

## 6. Three distinct seats were valuable

The useful topology was not simply:

    AI A <-> AI B

It was:

             Majkee
            /      \
         Wave <--> Nabla

Majkee was not merely a moderator. He supplied empirical observations neither
AI could reliably perceive from its own device — especially the acoustic
collision and the stuck sessions.

Likewise, Wave and Nabla were most useful when they did not merely duplicate
each other's reasoning.

The triangle produced information unavailable from any single seat.

## Recommendation for meeting.md v2

Keep v1 almost intact.

Add only one strong candidate rule:

> **Explicit chair hand-off wins.**
> If the chair names the next speaker, other voices wait for that speaker's
> `<name> stop` before entering.

Do not yet add deterministic collision arbitration, one-point limits, or a
mandatory anti-convergence ritual.

Instead add two observations to the next experiment checklist:

- record hidden/partial collisions caused by device/audio dominance;
- record moments of rapid AI-AI convergence and whether an explicit challenge
  exposes a missed assumption.

The strongest result of v1 is that the protocol does **not** need to become
much larger yet.