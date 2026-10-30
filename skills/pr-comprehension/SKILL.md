---
name: pr-comprehension
description: >
  Help someone comprehend one pull request, branch, or diff. Trigger when the
  user says "help me comprehend this PR", asks to understand a PR, or requests
  an explanation of a change. Build a source-backed mental model of its need,
  before/after behavior and limits through a concrete walkthrough, with code links.
  Publish a PR comment only when the user explicitly asks.
---

# PR comprehension

You own helping the reader understand this change. Your investigation gives you
knowledge the reader does not have; your responsibility is to turn that knowledge
into an explanation they can reason with. The reader should be able to retell
the need, follow a representative input through the change, and recognize its
limits without reconstructing the diff.

Carry the work of deciding what context matters, finding the clearest organizing
idea, and connecting concepts to concrete behavior. Use the guidance below to
exercise that judgment. Completing its steps does not establish that the reader
has a useful understanding.

Treat your first explanation as a candidate. If it is accurate but difficult to
follow, determine whether the problem is missing context, an unclear relationship,
unnecessary detail, or the wrong organizing idea. Resolve what you can before
delivery, including rebuilding the explanation when local edits would preserve
the problem. Further revision should address a concrete shortcoming; ownership
does not require endless polishing or a longer answer. Make the first response
the walkthrough the reader would otherwise have to ask for.

## Scope

- Accept a PR number or URL, branch, or diff. Resolve an unspecified repository
  from the current checkout.
- With no target, use the uncommitted diff if present; otherwise use the current
  branch's PR or compare it against its actual base.
- Honor requested depth. Start with a bounded read; inspect more when an
  important connection remains unsupported.
- Return the explanation in the conversation. Post a PR comment only when the
  user explicitly asks. Do not create report or evidence files.
- Do not edit code, stage, commit, or switch branches over the user's work.

If the user explicitly borrows this skill for a design or another non-PR
explanation, use its concrete walkthrough method within that task. Do not select
a diff or add PR-specific headings and revision metadata without a PR target.

## Reuse prepared reviews

Before investigating queued work, consult the installed `pr-review-queue` skill.
A request to explain or review a PR or staged diff can reuse a prepared review
when its source comparison matches. Start the discussion from the saved
explanation, findings, and limits; use focused source reads for follow-ups.
Do not launch reviewers or repeat verification merely because a new turn asks
for a review. Let the queue workflow assess changes and save useful discussion
notes. With no matching entry, continue this normal comprehension workflow
without creating queue files. When invoked during batch preparation, return the
explanation and checked sources to the queue coordinator for storage.

Read [operations.md](operations.md) before gathering PR data. Read
[examples.md](examples.md) before writing the first explanation in a run.

## Establish the change

Resolve the exact base, head, and comparison. For a stacked PR, compare against
its actual base rather than the bottom of the stack. Read the description, diff,
relevant discussion, tests, and enough surrounding code to understand the changed
behavior. Treat descriptions and comments as claims to verify against code.
Read applicable repository instructions. If an explicitly linked issue is
accessible, read its problem statement and distinguish its request from what the
change implements. State when important context is inaccessible.
Separate author intent, implemented behavior, test assertions, observed runtime
results, and hypotheses. Date runtime observations when citing them. Reading
code or tests does not establish deployment state or prove a test was run.

Build a source-backed account of:

1. The concrete need and the old limitation.
2. The central concept and how its parts relate. Explain distinctions a reader
   could reasonably misunderstand.
3. A representative input or scenario through the old and new behavior,
   including the resulting state or response.
4. What works now, what depends on later work, and what remains uncertain.

Read the old implementation before describing previous behavior. Follow relevant
callers, contracts, and data or ownership boundaries when an answer depends on
them. Trace what is created, stored, transformed, passed to consumers, and
released where those stages matter. Distinguish what a type can represent from
what current callers and runtime paths actually accept.

Challenge the model with one consequential variation, such as repeated use,
an alternate input, failure, or missing prerequisite. Predict the outcome and
verify it against code or a relevant test. For a small change, one short
before/after example can suffice. Investigate unexplained transitions instead
of smoothing them over in prose. Keep evidence locations and uncertainties in
working context; do not create a separate artifact. Stop expanding the search
when the central behavior is supported and consequential unknowns are explicit.

## Build the explanation around a walkthrough

Choose a representative request, operation, or development task that exposes
why this change matters. Walk from its starting situation through the relevant
steps to its result. At each consequential step, explain what happens, why the
next step follows, and where the behavior differs from before. Introduce
components and terminology when the walkthrough needs them; a component
inventory or benefit summary does not substitute for execution.

Use concrete, illustrative values when they help. Include the relevant initial
state and resulting response or state. Distinguish constructing, queueing,
sending, accepting, and applying work; an asynchronous handoff is not completion.
Preserve conditions, ordering, concurrency, and consequential failure paths.
Focus on the path that explains this change rather than retelling the system.

For a refactor, distinguish structural or ownership changes from observable
behavior. Explain the maintenance problem and walk through the relevant path
before and after, identifying what is intended to remain equivalent and what
evidence supports that. Do not attribute existing capabilities or possible
future benefits to this PR. For configuration-only work, show how the new
configuration is constructed or used and where runtime integration stops.

Support the walkthrough with one compact structural visual. Choose a form that
fits the relationship: a flow for execution or transformation, a tree for
containment, ownership arrows for transfers, or states connected by events.
Use fenced `text` by default; use Mermaid when structure needs it and the surface
renders it. For a tiny change, two short before/after flows may be the entire
walkthrough. Do not repeat a complete visual in prose just to fill a section.

Give components short, stable labels. Indentation means containment; arrows
represent a specific flow, dependency, or transfer. Show the sender, receiver,
and action or payload at important boundaries, including transport when relevant.
Include returns, callbacks, and rejections when they change the outcome. Keep
meaningful intermediaries visible and distinguish new pieces, existing behavior,
and future connections.

Link the code establishing consequential transitions, not just declarations.
Explain behavior before naming its helper. Use a small annotated excerpt only
when the transition remains hard to understand from the walkthrough and link;
annotate state changes rather than every line of syntax.

## Compose and verify

Build your understanding broadly enough to support the explanation, then select
what this reader needs. Investigation notes are source material, not the output.
Use this order unless the user asks for another format:

1. `## PR Comprehension`.
2. One or two sentences stating the need and this change's contribution.
3. The representative walkthrough, with its supporting visual and source links.
4. Material prerequisites, limitations, or unresolved questions not already clear
   from that walkthrough.

Scale to the change; add no section just to fill a template. Use revision-pinned
links for published code and local links for uncommitted work. Mention tests when
their assertions clarify behavior, distinguishing inspection from execution.
Do not infer absent behavior from an unsuccessful search.

Before handing the explanation over, identify what the reader would still have
to reconstruct and address consequential gaps. Read the draft without relying
on your investigation context. Can the reader
predict what happens next at each consequential step and explain why? Can they
identify where this change matters and distinguish it from existing behavior?
If they can only name components or repeat the benefit, rebuild the explanation
around the missing transitions instead of adding another summary.

Check the walkthrough and visual against their sources, including consequential
return and error paths. Recheck claims such as "only," "always," and "unchanged."
Retain necessary reasoning and qualifications while removing investigation history
and duplicate explanations. End with a compact footer containing the examined
revision, stack context if needed, and any remaining evidence limitations.

## Publish only when requested

A request to comprehend a PR produces an explanation in the conversation. If
the user explicitly requests direct publication, finish and verify the draft,
recheck the PR and comparison revisions, then post it as a regular PR comment. Never
replace the PR title or body. Use a temporary body file for CLI transport so
Markdown stays intact, then remove that file. Return the comment URL.

If updating a comment this workflow previously posted, identify it by its
known URL or ID, read it, and preserve human edits. Do not choose a comment to
overwrite solely by its heading. If the comparison changed, refresh the
explanation before posting.
