---
name: pr-overview
description: >
  Explain a pull request, branch, or local diff through its motivation, central
  concepts, before/after behavior, and scope. Use when someone asks for a PR
  overview or wants to understand a change. Build a source-backed component
  map and representative trace so the reader can focus their code inspection.
  Post a PR comment only when the user explicitly asks to publish it.
---

# PR overview

Help an engineer unfamiliar with a change understand why it exists, how it works,
and where to inspect it. Explain relationships and behavior, not just a list of
edited files.

## Scope

- Accept a PR number or URL, branch, or diff. Resolve an unspecified repository
  from the current checkout.
- With no target, use the uncommitted diff if present; otherwise use the current
  branch's PR or compare it against its actual base.
- Honor requested depth. Start with a bounded read; inspect more when an
  important connection remains unsupported.
- Return the overview in the conversation. Post a PR comment only when the user
  explicitly asks. Do not create report or evidence files.
- Do not edit code, stage, commit, or switch branches over the user's work.

Read [operations.md](operations.md) before gathering PR data. Read
[examples.md](examples.md) before writing the first overview in a run.

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

## Map and trace the structure

Put one compact structural visual at the center of the overview. Choose a form
that matches the relationship:

| Relationship | Useful form |
| --- | --- |
| Containment or configuration | Annotated tree |
| Ordering or control flow | Connected flow with branches |
| Transformation | Inputs → processing → output |
| Ownership or lifetime | Owners and labeled transfer/release arrows |
| State transitions | States connected by events |

Use a fenced `text` tree or flow by default; use Mermaid when branching or
structure needs it and the output surface renders it. Indentation means
containment; arrows must represent a specific flow, dependency, or transfer.
For a change spanning several components, give the relevant components short,
stable labels and reuse those labels in the trace and source notes. Show the
boundary crossed by each important arrow: sender, receiver, action or payload,
and transport when it matters. Include a return, callback, or rejection path
when it changes the outcome. Do not skip a meaningful intermediary just to make
the map look simpler. Show where new pieces join existing ones, and separate
behavior implemented now from a future connection. A file tree or list of
types alone is insufficient. For a tiny change, two short before/after flows
can be the entire visual.

Trace one concrete example through that same map when the behavior needs more
than the visual alone. State the starting input and relevant state, what each
changed boundary does, and the final state or response. Mark example values as
illustrative. Distinguish constructing, queueing, sending, accepting, and
applying work when those stages differ. Preserve relevant conditions, ordering,
and concurrency; do not imply that an asynchronous handoff has completed.
Explain behavior before naming its helper. Link the code that establishes the
important transition, not just the file containing its data type. Use a tiny
annotated excerpt only when the transition remains hard to see from the map and
source link; annotate state changes rather than every line of syntax.

## Write and verify

Use this order unless the user asks for another format:

1. `## Agentic Overview`.
2. One or two sentences stating the need, old limitation, and contribution.
3. The structural visual.
4. A short trace or notes for behavior, prerequisites, or scope the visual
   cannot show. Connect consequential transitions to the code that supports
   them, and say why each linked location is useful.
5. Material limitations or unresolved questions, if any.

Use as much space as the change needs to explain its mechanism and important
boundary; keep small changes short. Add no section just to fill a template.
State what the evidence supports, with qualifiers. Use revision-pinned links
for published code and local file links for uncommitted work. Mention tests
when their assertions clarify important behavior, and say
whether you inspected or ran them. Do not claim a behavior is absent merely
because a search did not find it.

Read the draft as someone who has not seen the investigation. Using only the
draft, can that reader explain the need, central concepts, representative flow,
resulting state, and current boundary? Can the visual alone show the main
pieces and their relationships? Can they tell which source locations explain
the consequential transitions? Revise missing connections. Check each arrow
and trace step against its source, including return and error paths. Recheck
important claims, especially words such as "only," "always," and "unchanged."
Cut lines that do not add a relationship, evidence, necessary context, or useful
navigation; qualify unsupported claims. End with a compact footer containing
the examined revision, stack context if needed, and material limitations.

## Publish only when requested

A request for an overview produces a draft in the conversation. If the user
explicitly requests direct publication, finish and verify the draft, recheck
the PR and comparison revisions, then post it as a regular PR comment. Never
replace the PR title or body. Use a temporary body file for CLI transport so
Markdown stays intact, then remove that file. Return the comment URL.

If updating a comment this workflow previously posted, identify it by its
known URL or ID, read it, and preserve human edits. Do not choose a comment to
overwrite solely by its heading. If the comparison changed, refresh the
explanation before posting.
