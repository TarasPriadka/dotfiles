---
name: design-challenge
description: >
  Challenge an architecture, system design, or project approach by examining
  whether its assumptions and mechanisms support the intended outcome. Use
  when the user asks to pressure-test a design, find missing considerations,
  assess architectural readiness, or uncover consequential blind spots.
  Focus on reasoning and relevant counterexamples, not a review checklist,
  document template, or code-level review.
---

# Design challenge

Treat a design as a simplified explanation of how an outcome will happen.
Find omissions or assumptions that could change the outcome or the choice of
architecture. Preserve simplifications that are appropriate for the task.

These are reasoning moves to use where useful, not stages to complete or
sections to reproduce. A narrow question may need only one of them.

## Establish the outcome

Describe what a person or another system must be able to accomplish, under
what conditions, without using the proposal's component names. This separates
the need from the chosen solution.

Separate stated requirements, inherited behavior, and your assumptions. When
replacing something, establish what it actually does today. Read relevant
evidence or ask a focused question when a consequential fact is missing.

Judge the intended stage: a prototype and a production rollout can promise
different things. A deferral is sound when the stage still delivers its stated
outcome without that behavior.

## Find the gaps in the explanation

Mentally execute a concrete case. Explain why each action is possible and why
it produces the required result. Notice when you must invent information,
authority, coordination, or capacity to make the story continue.

Assigning a responsibility does not establish feasibility. Look for a plausible
implementation within the proposed boundaries. Details can remain open; "the
component handles it" cannot substitute for reasoning about whether it can.

Follow effects beyond the returned result when obligations remain, such as
resources to release or decisions another actor depends on.

## Vary the conditions

Choose a small, valid case that stresses an assumption. Change a relevant
condition and follow the consequences through the same design. Find where it
stops delivering the outcome, then assess whether that boundary is acceptable.
Do not turn every imaginable adverse condition into a requirement.

A booking system may work until payment completes as a reservation expires.
The useful question is which action can commit the booking and what the other
actor observes. "Add retries" does not answer it. If an existing atomic
transition resolves the race, verify that and close the concern.

For efficiency claims, identify what work grows with what input. A rough bound
can expose an unsuitable representation. For correctness claims, examine
whether valid individual steps still produce a valid result together. Two
accurate cached summaries may describe different points in time; whether that
matters depends on what the combined report promises.

## Follow complexity across boundaries

When a proposal makes something simpler, identify which responsibility vanished
and which moved elsewhere. An abstraction or shared component can hide work
from one participant while creating coordination for another.

For example, a shared approval group may simplify individual teams' processes
while creating a queue with limited decision capacity. Compare that tradeoff
with the promised turnaround time. The reasoning applies to people and software.

Compare alternatives against the same outcome and conditions, including the
effort to adopt and operate them. Existing capabilities can matter more than
architectural uniformity, but reuse alone does not justify a poor fit. Explain
the needed guarantee before proposing machinery to enforce it.

## Spend attention where being wrong matters

Prioritize uncertain assumptions that could invalidate other work or be costly
to reverse. Leave local, reversible choices to implementation.

Distinguish missing explanation, unresolved decisions, and evidence of a design
flaw. Silence in a document does not prove missing behavior in the system.

Suggest the smallest useful way to resolve an important uncertainty: inspect
existing behavior, work through an example, establish an agreement, or propose
an experiment. A critique request does not itself authorize edits or experiments.

## Make the critique useful

Present the few observations that most affect the decision. Connect each to a
concrete scenario, the assumption it tests, and why the consequence matters.
Explain what would resolve the concern or make it an acceptable tradeoff.
Match the conversation; impose no report format or questionnaire.

Be willing to conclude that the design is sufficient for its stage. Do not
manufacture objections or reopen decisions without a reason. Stop when the
important uncertainties and the next useful action are clear.
