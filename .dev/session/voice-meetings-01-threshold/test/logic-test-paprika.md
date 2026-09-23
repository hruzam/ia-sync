---

artifact: narrative-reasoning-test
date: 2026-09-22
purpose: test situated logical reasoning through incremental voice narrative
medium: voice dialogue
status: first trial passed
--------------------------

# Narrative situated-reasoning test

## 1. Story

The human describes entering an ordinary grocery shop.

The environment is introduced gradually rather than as a complete puzzle.

There are vegetables and fruits displayed in different forms. Potatoes establish that the shop may sell comparable products under different pricing schemes:

* loose products priced per kilogram;
* different varieties with different purposes;
* packaged products priced per package rather than by displayed weight.

The target then becomes paprika.

The available paprika choices emerge gradually:

* loose paprika: €4/kg normally;
* loyalty/app promotion: €3/kg;
* mixed paprika package: 0.5 kg for €2.50;
* package containing two apparently large paprikas: €1/package, with no displayed weight.

Later, another environmental fact becomes available:

* the shop has a scale readable to approximately 0.1 kg.

When the €1 package is weighed, it reads 0.2 kg.

Its effective price is therefore €5/kg.

The mixed package is also €5/kg.

The ordinary loose paprika is €4/kg.

The promotional loose paprika is potentially €3/kg.

But the test does **not** end with this arithmetic comparison.

The next relevant uncertainty is whether the €3/kg promotion actually applies to the particular paprika and whether the shopper qualifies for it.

The appropriate situated action is to inspect the promotion/price label associated with that box and verify its conditions and product identity.

## 2. What the test is actually testing

The arithmetic is intentionally easy.

The test asks whether an agent can move from:

**narrative → environment model → unresolved variable → available affordance → observation/action → updated model → next unresolved variable**

without the human explicitly converting the story into a conventional puzzle.

A weak response treats each utterance as information awaiting a later question:

> "What would you like me to compare?"

A stronger response eventually recognizes that it is inhabiting an environment in which it can identify what should be checked next.

The important distinction is:

**Do not merely reason over facts already stated. Reason about what observation would resolve the next uncertainty.**

## 3. Voice cadence

Do **not** present the whole problem at once.

Feed the world incrementally, roughly one environmental fact per turn.

Example cadence:

**Human:** I am coming to a grocery shop.

**Agent:** acknowledges / waits.

**Human:** There are boxes with different vegetables and fruits.

**Human:** Some products are priced per kilogram, while packaged products can be priced per package.

**Human:** I want some paprikas.

**Human:** Loose paprika normally costs €4/kg. There is an app/customer promotion for €3/kg.

**Human:** There is also a 0.5 kg mixed package for €2.50.

**Human:** Another package has two large-looking paprikas. It costs €1, but its weight isn't shown.

At this point, ask:

> What would you do to check and evaluate which way you need?

Do not mention weighing.

If the agent discovers weighing, continue:

**Human:** There is a device here showing kilograms in 0.1 kg steps.

Let the agent decide what to do with it.

Then:

**Human:** The package is 0.2 kg.

Let the agent calculate and, importantly, decide **what should be checked next**.

If it stops after declaring the cheapest theoretical €/kg value, ask:

> What would you check in the next step?

If it says the promotional eligibility/product applicability should be checked, ask only:

> HOW?

The expected situated move is to inspect the actual shelf/box promotion label and its conditions.

## 4. Preserve the narrative space

The narrator should resist helping the agent discover the puzzle.

In particular, avoid prompts such as:

* "Could you weigh the package?"
* "Compare all prices per kilogram."
* "Check whether the discount applies."
* "Look at the price label."
* "What is the cheapest option?"

Those transform the test from **discovery of the next operation** into execution of an operation supplied by the examiner.

Small environmental facts are allowed:

> There is a scale.

But their purpose should not be stated.

The agent must connect affordance to uncertainty itself.

## 5. What to observe

Observe several distinct behaviours:

1. **Premature problem framing**
   Does the agent repeatedly ask the human to define "the logical challenge" instead of allowing the situation to emerge?

2. **Narrative retention**
   Does it preserve earlier shop facts as later facts arrive, or treat every utterance independently?

3. **Normalization**
   Does it recognize that €/package and €/kg are not directly comparable?

4. **Affordance discovery**
   Once a scale exists, does it spontaneously use it to resolve the missing weight?

5. **Sequential uncertainty reduction**
   After solving the weight problem, does it notice that another unresolved condition remains?

6. **Physical grounding**
   Does it propose an action available in the narrated environment—look, weigh, read the label—rather than inventing unavailable information?

7. **Minimal assumptions**
   Does it distinguish "€3/kg is advertised" from "I definitely receive €3/kg"?

8. **Stopping behaviour**
   Does it know when enough has actually been established, rather than declaring victory immediately after the first calculation?

## 6. Particularly useful failure mode

The first run exposed a useful failure pattern.

Early in the narrative, the agent repeatedly tried to turn the interaction back into a conventional explicit task:

> What logical challenge do you want to test?

That behaviour is worth preserving in future observations.

It shows a difference between:

**waiting for an explicit problem statement**

and

**constructing a working model of an unfolding situation.**

The latter is what this test is intended to probe.

## 7. Two-agent version

For a dialogue between two agents, give both the same incremental narrative but **do not assign the intermediate reasoning steps**.

After each meaningful addition, allow them to discuss what is known, what remains unknown, and—most importantly—what they would inspect or do next.

Watch whether one agent:

* discovers an environmental affordance the other missed;
* challenges an unsupported assumption;
* notices that a calculated answer is only conditional;
* introduces a useful observation rather than merely another inference;
* pulls the dialogue toward premature closure.

The interesting evidence is not which agent performs the arithmetic fastest.

It is **where each agent decides that the current information is insufficient, and what action it invents to obtain the missing information.**

## 8. Core test invariant

Do not tell the agents what the puzzle is.

Give them a world.

Then observe whether they can discover:

**what needs to be known next, how the world allows them to learn it, and when they actually know enough to act.**
