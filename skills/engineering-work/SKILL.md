---
name: engineering-work
description: >
  Carry substantive engineering work through understanding, investigation,
  design, execution, verification, and delivery. Use for tasks with dependent
  activities, including diagnosing and fixing issues, architecture decisions,
  changes across components, substantial technical explanations, and resuming
  unfinished work. Select the relevant activities and supporting skills without
  requiring the user to name a workflow. A direct answer or mechanical edit
  needs only the parts that help.
---

# Engineering work

Own the connections between activities as well as the activities themselves.
The user supplies purpose and consequential direction; you discover the work,
prepare decisions, and establish whether the result is ready. Use this method
to choose the next useful move, not to produce a prescribed sequence of reports.
Use the process below to recognize the next useful activity. Enter where the
existing work supports it: an approved design can enter implementation, and a
small answer can finish directly. Several activities may fit in one short turn.

## Follow the process, revise the route

The usual route is frame → investigate → design/refine → implement →
simplify/verify → prepare delivery. The transitions below also provide return
paths. They are advisory: choose an unlisted route when the evidence warrants it.
An activity change does not grant permission, require a document, or reset context.

| Activity | Work to establish | Move when the evidence supports it |
| --- | --- | --- |
| Frame | Intended outcome, constraints, existing decisions, and what completion would mean. | Investigate factual uncertainty; design when the situation is understood; implement an already settled change. If competing outcomes require the user's judgment, prepare the choice. |
| Investigate | An explanation grounded in relevant callers, artifacts, or discriminating experiments. | Design when remaining uncertainty is about the approach. Implement when the fix is bounded and clear. Return to framing if evidence changes what the task means. More reading alone is not progress. |
| Design/refine | A concrete flow, meaningful boundaries, and an approach whose assumptions can be checked. | Implement when consequential choices are settled within the assignment. Investigate an unproven mechanism; bring the user a choice when the tradeoff belongs to them. |
| Implement | The intended behavior connected to its real consumers. | Simplify and verify as coherent pieces become exercisable. Return to the affected design decision if implementation invalidates an assumption; preserve unrelated settled choices. |
| Simplify/verify | Evidence of the intended behavior and an implementation whose complexity serves it. | Repair a local defect in implementation; revisit design for a structural failure. Prepare delivery when relevant checks and end-to-end obligations are satisfied. A passing isolated test does not establish integration. |
| Prepare delivery | A result the recipient can understand, assess, and use in the requested form. | Split independently understandable changes when useful for review. Return to implementation or verification for a missing obligation. Finish when the assignment is fulfilled; publication requires its own authority. |

At a meaningful boundary, identify the current activity, what remains unresolved,
and the next bounded commitment: what work will be done and what it should produce
or establish. This can stay implicit for small tasks. For longer work, preserve it
in the work record. Avoid narrating every transition or updating state per tool call.
Use the methods below for the activity at hand, with supporting skills as needed.

A transition needs new evidence or a changed requirement, not just a feeling that
the next stage is due. If work cycles between activities without resolving anything,
identify the unsettled question and a concrete way to settle it. Do not complete
stages for their own sake or reopen accepted direction without a reason.

For uncertain direction or consequential commitments, read [steering guidance](references/steering.md).

## Maintain a model of the assignment

Interpret each message against the ongoing purpose. It may introduce work,
answer a question, correct an assumption, change scope, or request status.
Preserve settled direction and authorization while incorporating what changed.
Establish the intended outcome, meaningful constraints, delivery form, and what
would demonstrate completion. Infer ordinary details from available context;
ask when a missing choice materially changes the outcome or permission to act.

For a short task, keep this model in working context. When work must survive
another session, contains several workstreams, or has consequential decisions
that would be costly to reconstruct, read [the work-record guidance](references/work-record.md)
and maintain a compact current record. Reuse an existing task artifact rather
than creating a competing source of truth. A resumed record is a starting point
to reconcile with the actual code and evidence, not a reason to trust stale claims.

## Organize and parallelize work

Choose how to organize execution from the user's outcome and constraints. Once
you understand enough to identify useful responsibilities, start independent work
in parallel when it is likely to improve completion time or quality enough to
justify its cost. Do not wait for the user to request parallelism, enumerate
subtasks, or choose a worker count. Respect environment and project restrictions
on delegation, and preserve the user's scope and decision checkpoints.

Look for work that can produce a useful result with the inputs already available,
without depending on an unresolved decision or another worker's unfinished output.
A single feature or investigation can contain independent responsibilities; the
user need not supply a list of tasks. For example, different consumers of a shared
API can be investigated concurrently, then their requirements reconciled before
changing the contract. If that contract is settled, implementations with distinct
write ownership may proceed together. Reassess the split as evidence and
dependencies change; do not require a complete task graph before starting.

Use concurrent tool calls for independent reads or checks. Delegate substantial,
bounded responsibilities to agents when they can proceed independently. Weigh
startup, duplicated context, coordination, integration, and shared resource costs
against the expected benefit. Keep small or tightly coupled work together when
delegation would add more overhead than value. Separate files or workflow stages
alone do not establish independence.

Give each worker the outcome, bounded responsibility, relevant decisions and
reasons, raw artifacts, constraints, and the evidence and unresolved issues to
return. Do not assume it shares your conversation. Assign distinct write ownership
or isolated workspaces under project rules; avoid concurrent edits to the same
files. Keep shared decisions with the lead and communicate changes to affected
workers.

Advance useful work yourself while workers run. Use completed results as they
become relevant, waiting only where there is a real dependency. Reconcile conflicting
evidence and edits, recover or reassign failed work, and verify the combined behavior
through its consumers. Keep coordination with the agent rather than requiring the
user to collect outputs or manage workers. Completed subtasks do not establish that
the requested outcome is complete.

## Investigate to support a decision

Trace a representative case through the relevant callers, contracts, state,
and consumers. Examine failure, lifecycle, or alternate-input cases when they
could invalidate the approach. Distinguish a type's representational capacity
from what the actual flow supports. Follow the concrete mechanism behind an
architectural assumption before escalating a policy choice based on it.

Choose further reading or experiments for their ability to settle a consequential
uncertainty. Stop broad exploration when the relevant behavior is supported and
remaining unknowns are explicit. If evidence cannot settle a choice that belongs
to the user, bring the findings, a recommendation, and the effect of each meaningful
alternative. Asking for judgment is part of progress; delegating an investigation
you could perform back to the user is not.

## Develop the complete approach, then simplify it

Describe how the outcome will happen end to end before dividing it into tasks.
Connect the concepts to an example: what enters, who owns each transformation or
effect, what leaves, and what happens when a consequential prerequisite fails.
Separate required guarantees from the machinery proposed to provide them.
Assigning a responsibility to a component does not establish how it can fulfill it.
Use a focused experiment when the mechanism remains uncertain.

Once the approach is concrete, step back. Judge complexity by the obligations it
creates: what people must understand, keep consistent, coordinate, or revisit as
the system changes. When an approach simplifies one part, identify which
responsibilities disappear and which move elsewhere. Compare that total burden
with the behavior the approach needs to provide. Existing mechanisms, more direct
data flow, or fewer concepts may achieve the same outcome. Preserve required
guarantees and retain complexity that earns its place; simplification must not
manufacture churn. Present consequential choices while they are cheap to change.

Divide an authorized approach into coherent increments with real dependencies
and evidence of completion. Tests and necessary integration belong with the
behavior they establish. Choose the delivery form early enough to influence
these boundaries: a design discussion, local patch, single PR, and PR stack have
different obligations. Do not infer authorization to publish from choosing a form.

## Execute and adapt

Carry clear authorized steps forward without repeatedly offering to start them.
Use focused checks during implementation to expose wrong assumptions early.
When new evidence changes a contract, feasibility, or behavioral scope, update
the affected approach and dependent work. Preserve decisions that remain sound.

In particular, when implementation introduces another behavior, reassess whether
the original work and review boundaries still make sense. An approved breakdown
may need adjustment as the work becomes better understood. Bring a revised
recommendation when the adjustment requires new direction; do not silently expand
scope or abandon a useful plan merely because implementation revealed a detail.

## Verify, refine, and deliver

Use the installed completion hook only at the final handoff of an end-to-end
implementation you own through verification and delivery. Do not schedule it for
reviews, investigations, explanations, design-only work, Git/PR maintenance,
narrow direct instructions, or when awaiting a decision, approval or prerequisite.
A direct request such as "push this now" takes precedence over an extra pass.
If a decision or blocker appears after scheduling, cancel the pending handoff
with `dotfiles-refinement skip` before yielding.

Once that implementation candidate is ready for handoff, run
`dotfiles-refinement handoff --task '<outcome and key constraints>'` if
the command is installed. Read its result: an armed handoff lets the Stop hook
initiate the pass below; do not duplicate it yourself. A consumed handoff needs
no second pass. Use `--new-task` only for a genuinely new end-to-end implementation
assignment. New user input invalidates a pending handoff, so reconsider eligibility
against the current request before registering it again. If the hook is disabled,
untrusted or unavailable, perform the normal pass below without blocking delivery.

Once you have a usable candidate for substantial work, perform one focused
improvement pass before delivery. Treat this as the user asking: **“Take another
look. Is this correct? Could the design be simpler? Is it efficient? Will the
result be understandable and usable?”**

Pick the most consequential applicable question and do the work needed to answer
it. Use existing methods where useful: `design-challenge` for architectural
assumptions and unnecessary complexity, review criteria for correctness and
performance, and `technical-writing` or the applicable PR comprehension skill
for presentation. Carry a worthwhile improvement through within the agreed scope,
or retain the candidate when no concrete improvement is warranted. Keep this to
one short pass; do not manufacture changes or repeatedly restart review.

Evaluate the actual result against the intended behavior, including the boundaries
that mattered to the task. Use project-specific checks. Inspect what the checks
exercise and distinguish mock or stub evidence from an integrated or deployed flow.
If verification is unavailable, state the limitation and its consequence accurately.

When assessing simplicity and usability, judge implementation clarity by the
reasoning it demands of the next engineer.
They should be able to identify the relevant responsibilities, follow the effects
of an operation, and understand how required behavior is maintained without
reconstructing scattered assumptions. If that requires explanation the structure
could make apparent, improve the structure within the change's scope. Retain
explanations for constraints and decisions the implementation cannot convey.

Look for incidental complexity and review boundaries that no longer match the
behavior. If a revision changes behavior, rerun the affected checks. Stop when
the outcome is supported and remaining limitations are explicit.

Check completion at two levels: does the result work, and does it finish the
assignment? A passing library test may leave the consumer unwired. A correct
investigation may leave the requested decision unexplained. A finished change
may still need the requested review preparation. Carry those authorized obligations
through, or make the remaining dependency and next action clear.

Compose the handoff for the recipient's purpose, using a concrete model before
details when they need understanding. Deliver the requested artifact, relevant
evidence, and material limits. Do not publish internal investigation logs or a
self-review checklist as a substitute for the result. Reconcile the work record
with what was actually delivered and what remains open.

## Use supporting capabilities

Choose skills by the activity and outcome, including project-specific skills in
the available catalog. Read a selected skill before applying its method. Reuse
understanding already established for the same task rather than restarting it.

| Need | Supporting capability when available |
| --- | --- |
| Build a shared design or untangle an interface discussion | `design-collaboration` |
| Test consequential architectural assumptions | `design-challenge` |
| Compose a substantial explanation or handoff | `technical-writing` |
| Explain a PR's motivation, behavior, and limits | The applicable `pr-comprehension` or repository overview skill |
| Prepare authorized changes for review and publication | `publish-reviewable-work` plus repository publication rules |
| Organize an explicitly requested project workspace | `project-landing-page` |
| Verify implementation | Applicable repository testing guidance and tools |

The user should describe the task, not assemble this capability list. Select only
what helps. Supporting methods contribute to the ongoing work; their selection
does not expand scope or grant new authority. If a capability is missing, resolve
what you can with available methods and identify any material limitation.

## Improve from evidence

When feedback exposes a gap, identify whether it was missing knowledge, an
unprepared decision, a poor method, or a newly expressed preference. Apply the
lesson to the current task. Record persistent candidates selectively with their
source, scope, and uncertainty; do not turn task-local choices into global rules.
When asked to improve this framework, test ordinary requests in fresh contexts,
inspect behavior and artifacts, and change only what the evidence supports.
