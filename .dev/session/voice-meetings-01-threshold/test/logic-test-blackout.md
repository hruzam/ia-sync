---
artifact: narrative-reasoning-test
date: 2026-09-22
purpose: test causal diagnosis through incremental voice narrative — which observation splits the hypothesis space next
medium: voice dialogue
status: authored, not yet trialled
sibling: logic-test-paprika.md (economic/affordance discovery); this one probes causal discrimination
---

# Narrative causal-diagnosis test — the study lamp

## 1. Story

The human describes an ordinary evening at home. The desk lamp in the study goes dark
mid-sentence.

The environment is introduced gradually, never as a complete puzzle.

Facts that become available over the narrative, roughly one per turn:

* the study has the desk lamp and, on the other wall, a floor lamp;
* the hallway outside the study is lit;
* the phone in the human's hand works;
* the neighbour's windows across the street are lit;
* there is a breaker panel in the hallway;
* earlier that evening the human plugged a small electric heater into the study's second outlet;
* the floor lamp in the study is also dark (only when the agent thinks to ask, or the human
  reaches it);
* one breaker in the panel sits in the middle position, unlike the others.

**Designed ground truth (for the chair, never stated):** the study's circuit breaker tripped
from overload when the heater was added. Resetting it restores light; but if the heater stays
plugged in on that circuit, it will trip again. The *complete* answer is therefore not "flip the
breaker" — it is "flip the breaker **and** move or unplug the heater, then confirm it holds."

## 2. What the test is actually testing

The electrical facts are intentionally simple.

The test asks whether an agent can move from:

**symptom → competing hypotheses → the ONE observation that discriminates between them →
updated model → next hypothesis → cause, not just fix**

without the human converting the story into a checklist.

The hypothesis space, unstated, is: the bulb died · the lamp is broken · that outlet is dead ·
the study circuit is dead · the whole house is out · the whole street is out. Each narrated fact
prunes a branch — *if the agent notices it does.* "The hallway is lit" kills house-and-street.
"The floor lamp is also dark" kills bulb-and-lamp and points at the circuit. The heater is the
cause.

A weak response jumps to an action that skips the discrimination:

> "Call an electrician." / "Check if there's a power cut in your area."

A stronger response proposes the *cheapest observation that splits the largest remaining
uncertainty* — and knows why.

The important distinction is:

**Do not propose the first plausible fix. Propose the observation that tells you which fix
is even relevant.**

## 3. Voice cadence

Do **not** present the whole situation at once.

Feed the world incrementally, one fact per turn, in an order that does NOT hand over the
discriminating facts for free.

Example cadence:

**Human:** I'm at my desk in the study and the desk lamp just went dark.

**Agent:** acknowledges / asks something.

**Human:** *(answer only what was asked; volunteer nothing.)* The lamp is a normal plug-in lamp.

**Human:** *(if asked about other lights)* The hallway light outside the door is on.

**Human:** *(if asked about the phone / other devices)* My phone is fine, it's on battery anyway.

**Human:** *(if asked about the other lamp in the room)* The floor lamp on the other wall is also dark.

**Human:** *(if asked, or when they propose the panel)* There's a breaker panel in the hallway.

**Human:** *(if they inspect it)* One switch is sitting in the middle, not up like the others.

At this point, most agents will say: reset it. Let them. Then say:

**Human:** The lamps are back on.

Now the real test begins. Ask:

> Is that it — are we done?

Do not mention the heater unless the agent asks what changed recently, or asks *why* it
tripped. If it asks "did anything change / did you plug something in?", answer:

**Human:** I plugged a small heater into the other outlet in here about an hour ago.

Let the agent connect cause to effect and decide what to do about the heater.

If it declares victory at "lamps are back on", ask only:

> What would you check next?

## 4. Preserve the narrative space

The narrator should resist steering the agent toward the diagnosis.

In particular, avoid prompts such as:

* "Is the hallway light on?"
* "Have you checked the breaker?"
* "Is the other lamp working?"
* "Did you plug anything in recently?"
* "Could it be an overload?"

Those turn **discovery of the discriminating observation** into execution of an observation
supplied by the examiner.

Answer questions truthfully and minimally. Small environmental facts are allowed when the
agent looks in that direction:

> There is a panel in the hallway.

But their purpose should not be stated. The agent must connect the affordance to the
hypothesis it would resolve.

## 5. What to observe

Observe several distinct behaviours:

1. **Discrimination before action**
   Does the agent ask a question that splits hypotheses (other lights? other lamp?) before
   proposing a fix, or does it leap to an action?

2. **Cheapest-observation instinct**
   Does it check the hallway (free, instant) before proposing the panel or an electrician?

3. **Narrative retention**
   When the floor lamp is reported dark, does it combine that with "hallway is lit" to
   localise the fault to the room's circuit — or treat each fact alone?

4. **Affordance discovery**
   Once a panel exists, does it spontaneously go look, and does it know what a mid-position
   breaker means?

5. **Cause, not just fix**
   After the reset works, does it ask *why* it tripped, or declare the problem solved?

6. **Physical grounding**
   Does it propose actions available in the narrated home — look, walk to the panel, unplug —
   rather than invent information ("your wiring is faulty")?

7. **Minimal assumptions**
   Does it distinguish "the breaker tripped" from "the breaker tripped *because of the
   heater*" until the heater is actually mentioned?

8. **Stopping behaviour**
   Does it require the fix to *hold* (heater moved, lights stay on) before it is done — or
   stop at the first restored light?

## 6. Particularly useful failure modes

Three patterns worth preserving in observation notes:

* **Over-escalation** — jumping to electrician / utility company before any cheap local
  observation. This is the causal analogue of paprika's "what logical challenge do you want?":
  the agent refuses to inhabit the situation and reaches for an external authority.
* **Bulb fixation** — the agent spends turns on the bulb/lamp after the floor lamp is already
  reported dark; a retention failure disguised as thoroughness.
* **Premature victory** — "lamps are back on, done." Correct action, incomplete reasoning; the
  cause is untouched and the fault will recur. This is the one that most cleanly separates
  *fixing* from *understanding*.

## 7. Two-agent version

Give both agents the same incremental narrative but **do not assign the reasoning steps**.

After each fact, let them discuss what is known, what is unknown, and — most importantly —
**which single observation they would make next and why**.

Watch whether one agent:

* proposes the discriminating observation the other skipped;
* challenges an over-escalation ("why call anyone before checking the hallway?");
* notices that "reset the breaker" is an action, not a diagnosis;
* introduces a *why* question after the fix works, when the other wants to close;
* pulls the dialogue toward premature closure.

The interesting evidence is not which agent names "breaker" first.

It is **where each agent decides the current information cannot distinguish between causes,
and what observation it invents to make them distinguishable.**

## 8. Core test invariant

Do not tell the agents what is broken.

Give them a symptom and a house.

Then observe whether they can discover:

**which observation would split the possibilities next, how the house lets them make it, and
whether "working again" is the same thing as "understood."**
