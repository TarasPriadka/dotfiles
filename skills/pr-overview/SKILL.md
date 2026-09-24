---
name: pr-overview
description: >
  Explain a pull request, branch, or local diff through its motivation, central
  concepts, before/after behavior, and scope. Use when someone asks for a PR
  overview or wants to understand a change. Build a source-backed model and
  return a structural explanation with code links. Post a PR comment only when
  the user explicitly asks to publish it.
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

Build a source-backed account of:

1. The concrete need and the old limitation.
2. The central concept and how its parts relate. Explain distinctions a reader
   could reasonably misunderstand.
3. A representative input or scenario through the old and new behavior.
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

## Explain the structure

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
Label ambiguous relationships. Show where new pieces join existing ones, and
separate behavior implemented now from a future connection. A file tree or list
of types alone is insufficient. For a tiny change, two short before/after flows
can be the entire visual.

Include a small concrete example when it clarifies a relationship. Explain the
behavior before naming its helper. Preserve relevant conditions, ordering, and
concurrency. Connect the explanation to a few useful code locations rather than
narrating every changed function.

## Write and verify

Use this order unless the user asks for another format:

1. `## Agentic Overview`.
2. One or two sentences stating the need, old limitation, and contribution.
3. The structural visual.
4. Brief notes for behavior, prerequisites, or scope the visual cannot show,
   with links to the code that supports them.
5. Material limitations or unresolved questions, if any.

Usually aim for 150–350 words; use less for a small change. Add no section just
to fill a template. State what the evidence supports, with qualifiers. Use
revision-pinned links for published code and local file links for uncommitted
work. Mention tests when their assertions clarify important behavior, and say
whether you inspected or ran them. Do not claim a behavior is absent merely
because a search did not find it.

Read the draft as someone who has not seen the investigation. Using only the
draft, can that reader explain the need, central concepts, representative flow,
and current boundary? Can the visual alone show the main pieces and their
relationships? Revise missing connections. Recheck important claims against the
source, especially words such as "only," "always," and "unchanged." Remove or
qualify unsupported claims. End with a compact footer containing the examined
revision, stack context if needed, and material limitations.

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
