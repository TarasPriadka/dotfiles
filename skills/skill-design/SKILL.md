---
name: skill-design
description: >
  Design or refine the behavior taught by an agent skill. Use when creating a
  skill, changing its workflow or decision criteria, diagnosing unhelpful skill
  behavior, or improving its results while preserving what already works.
  Ordinary use of a skill or a mechanical metadata correction does not need
  this method.
---

# Skill design

A skill helps an agent recognize a situation, develop the understanding it
needs, and exercise useful judgment. Its value appears in the work the agent
does and the effort left for the recipient. Following instructions or producing
the expected headings does not establish that the skill helped.

Own the behavioral design within the user's scope. A brainstorming request
produces a proposal; an authorized change carries through writing and appropriate
validation. When available, use `skill-creator` for packaging, metadata, resources,
and structural validation. This skill supplies the reasoning about what to teach.
It does not require a design document, additional agents, or every activity below
on every edit.

## Choose the depth of the change

When the problem and affected behavior are understood, inspect that part and
its direct dependencies, make the coherent edit, and check its consequences.
Shortening comments need not reopen review criteria or redesign orchestration.

Broaden the investigation when the cause is uncertain, the requested change
crosses responsibilities, or evidence contradicts the current explanation.
For a new skill or substantial workflow change, follow a representative request
through the proposed flow. Use the activities below to resolve the relevant
questions; do not expand a narrow edit merely to complete the method.

## Establish the behavior worth teaching

Start with a representative request and what a useful result enables the user
to understand, decide, or accomplish. Identify the recurring judgment the agent
needs help making. Distinguish the desired outcome from the user's suggested
mechanism and from the artifact the skill happens to produce.

Use available conversations, artifacts, and observed behavior before asking for
examples. Separate what the agent actually did, what the user disliked or valued,
and your hypothesis about the cause. An instruction can be present without being
loaded, loaded without being applied, or followed without producing useful work.
Check which problem you are addressing before adding more wording.

For each consequential addition, be able to explain the decision it should
improve, why the guidance could help, and what behavior would show that it did.
Keep that reasoning in the discussion or existing work record when useful;
do not impose a separate report. Sometimes the right change is a clearer tool,
better task context, or no skill change.

## Preserve useful behavior when refining

Read the existing skill and the references, helpers, or callers affected by the
proposed change. Identify the few behaviors that matter to retain. For a review
queue, those might be parallel preparation, saved-result reuse, and code-only
analysis. Include important constraints and authorization boundaries. Preserve
these behaviors without freezing their wording or implementation.

Distinguish observed successful behavior from intended behavior expressed by the
existing instructions. User feedback can establish what they value; source
inspection establishes what the skill says. If successful use is unavailable,
label the baseline as intended behavior rather than inventing evidence that it
works. Use that baseline to assess the change.

Prefer the smallest coherent change that addresses the cause. This may require
changing several connected instructions: adding a filtering step is incomplete
if the delivery step still says to report every discovered candidate. Follow
the consequences through the flow rather than appending another rule at the end.

Do not reorganize a working skill merely to match this skill's vocabulary or
section structure. New evidence can justify a larger rewrite; explain which
existing relationships prevent a local correction and what useful behavior the
rewrite retains. Remove superseded instructions so old and new rules do not
compete. Reuse existing capabilities rather than duplicating their instructions.

## Design the flow from understanding to result

Discovery, evaluation, and delivery are useful responsibilities to distinguish.
They need not be separate headings, agents, or user checkpoints. Small tasks can
combine them in one pass; contradictory evidence can send work back to discovery.

For consequential activities, trace what each consumes, decides, and produces.
Check that required inputs are available and that later activities use the
result. Distinguish real dependencies from work that can proceed independently.
For example, requiring an overview to wait for every reviewer can serialize a
previously parallel queue without improving either job. Specify when missing or
contradictory evidence requires more discovery, a qualified result, or a stop.
Explain what warrants reopening a conclusion and when the activity has done
enough. The presence of all three responsibilities does not establish a usable flow.

**Discover enough to act from.** Teach which sources and relationships matter,
how to establish relevant behavior, and how to distinguish evidence from claims.
Use a concrete scenario to expose missing transitions or assumptions. Broaden
investigation when it could change a consequential decision; collecting everything
is not a completion condition.

**Evaluate and select.** Treat findings, explanations, and approaches as candidates.
Teach the domain's actual criteria for accepting, rejecting, revising, or retaining
them as uncertain. Discovery asks what might matter; evaluation determines what
is supported and worth doing or presenting. Consider correctness and usefulness
separately. A true observation may have no meaningful consequence; an unresolved
assumption may be important enough to surface. Do not discard a supported minority
finding simply because other reviewers missed it.

For a review skill, useful criteria include whether the issue is introduced by
the change, addressed elsewhere in the stack, consequential for a plausible case,
and improved by the suggested remedy. "Filter out noise" alone leaves the central
judgment untaught. For design, compare the total obligations an approach creates,
including responsibilities moved to other components, against the required behavior.

**Deliver for the intended use.** Investigation notes are source material. Select
and organize what the recipient needs to reason, decide, or act. Explain the
important relationships and preserve conditions that change the conclusion.
For an action skill, carry the selected approach through authorized execution and
verify the intended effect. A recommendation, an attempted action, and an observed
result are different deliverables.

Allow a justified conclusion that no change or finding is needed. Do not create
pressure to manufacture recommendations, edits, abstractions, or PR splits.

## Make judgment concrete without fixing every step

Explain why a behavior matters, then connect it to decisions the agent will face.
Replace vague quality instructions with assessable properties. "Make it clear"
can mean that a reader can follow an input through the relevant boundaries and
predict the result. "Simplify" can mean reducing what people must understand,
coordinate, keep consistent, or revisit while preserving required guarantees.

Reserve fixed sequences for real dependencies and detailed rules for fragile
operations. Use examples to expose the condition that changes the right decision.
Effort should resolve a concrete uncertainty or improve the result enough to
justify time, tokens, and attention.

Keep mechanical invariants in reliable tools when appropriate; prose alone does
not enforce timeouts, locking, or safe file operations. Add helpers only when
their concrete benefit warrants the implementation and maintenance burden.

## Example: improve review comments without reducing coverage

The user says: "The findings are useful, but the comments are overwhelming."

Inspect a representative comment and the instructions that produced it. Weak
candidates surviving selection and good findings presented poorly need different
changes. Suppose the evidence supports a presentation problem:

- **Retain:** investigation depth, evidence standards, severity, and independent
  reviewer roles. Confirm which are observed successes and which are requirements.
- **Change:** replace a vague instruction such as "report findings with supporting
  detail" with composition guidance tied to the reader's task:

  > For each retained finding, explain the issue, a concrete consequence, and the
  > recommended action briefly. Keep source links and conditions that affect the
  > conclusion. Remove repeated proof and investigation history.

- **Connect:** check the final delivery instructions for conflicting demands to
  include all investigation notes. Keep discovery, selection, and reviewer
  scheduling intact unless the diagnosis gives a reason to change them.
- **Compare:** use the same supported finding before and after the edit. Does the
  revised comment preserve its meaning, severity, evidence, and qualifications
  while making the issue easier to understand? Include an already concise comment
  to check that the change does not force unnecessary rewriting.

If the candidates themselves lack support or consequence, improve selection
criteria instead. A request for readability alone does not justify fewer checks
or discarded findings. This example teaches how to choose an edit; its particular
comment structure is not a required format for other skills.

## Assess the change in context

Read the revised flow as a whole. Can the agent reach the intended result from
a realistic request with the context and tools it actually receives? Check the
handoffs between activities, conflicting criteria, permission boundaries, and
whether newly required work defeats the skill's purpose or cost expectations.
A local wording improvement can still damage the overall workflow.

Choose verification for the uncertainty and impact of the change. For a small
instruction refinement, a source review and concrete walkthrough may suffice.
When behavioral evaluation is warranted and feasible, use a fresh session with
the skill and necessary raw artifacts, without the authoring conversation's
intended answer or prior conclusions. Follow applicable delegation permissions.
Confirm which instruction version the session received.

For a consequential revision, compare the existing and proposed skill on the
same representative request and artifacts. Assess the intended improvement and
the behaviors chosen for preservation, including material changes in effort.
Use an ordinary successful case or a nearby case where the new behavior would
be inappropriate to check for regressions. A plausible revised result alone
does not establish an improvement. For a narrow edit, a focused before/after
walkthrough can suffice; do not require fresh-session trials for every change.
Judge observable decisions, work, and recipient effort rather than matching
wording, headings, instruction recitation, or longer autonomous execution.

Distinguish structural validation, reasoned walkthroughs, executed trials, and
real-use feedback. None substitutes for the others. A successful trial supports
that case; limited comparisons do not prove a general improvement. If a trial
is unavailable, describe the proposed behavioral effect as a hypothesis.

## Refine from evidence and finish

Interpret corrections before encoding them. Identify the assumption, criterion,
or transition that needed to change, and preserve unrelated settled direction.
Capture the transferable reasoning and its limits rather than turning one local
implementation choice into a universal rule. Check whether existing guidance
already covers the lesson and whether it failed to be selected or applied.

Stop when the requested change is coherent, useful existing behavior is accounted
for, and appropriate checks are complete with their limits understood. Further
polishing needs a concrete reason. Leave speculative improvements as hypotheses
rather than continually destabilizing a skill that works.

Deliver the skill or authorized refinement with a short explanation of the
intended behavior, why the change should help, what was preserved, and what was
actually checked. Keep internal exploration out of the handoff. Installation and
publication follow the user's established scope and the environment's conventions.
