---
name: pr-review-queue
description: >
  Batch full PR reviews, explanations, design critiques, and relevant checks for
  later discussion. Discover open PRs requesting the user's review when asked to
  prepare PRs for their review without an explicit selection. Save results in
  the repository's shared local queue.
  Also use before reviewing or explaining queued PRs or staged changes: reuse a
  matching prepared review instead of launching reviewers again. Refresh changed
  conclusions when needed or rerun when explicitly requested.
---

# PR review queue

Prepare the expensive review work ahead of the user's reading. Later sessions
use the saved understanding to explain and discuss each change immediately.
This skill owns preparation, storage, matching, and refresh; specialist skills
own their analysis methods. A completed review is separate from human approval.

## Choose the operation first

- **Prepare a batch:** resolve the supplied PRs or author/assignment selection.
  With no explicit selection, discover the user's review requests as described
  below. Reuse matching preparation and complete missing or affected checks. A queue
  request authorizes local artifacts, not GitHub publication or source edits.
  Keep publication invitations from individual skills out of batch preparation;
  return the saved results unless the user asks to publish.
- **Discuss or review queued work:** check for a matching prepared review before
  starting any workflow that launches reviewers. Ordinary requests such as
  "review the staged changes" or "help me understand this PR" normally reuse it.
- **Show:** derive the index from existing entry directories without rerunning
  checks or fetching GitHub metadata solely to display the queue.
- **Refresh:** reconcile existing entries with current code and update affected
  results. An explicit full rerun bypasses reuse for the requested scope.

With no queue or matching entry, an ordinary single-PR request follows the normal
review/explanation workflow without creating queue files. After a fresh review
of an existing entry, save the results there so the next discussion can reuse
them. Do not backfill unrelated PRs or start a new batch during discussion.

Read [storage.md](storage.md) before writing or matching entries, and
[examples.md](examples.md) for refresh, staged-work, and migration scenarios.

## Discover PRs requesting the user's review

Treat "prepare PRs for my review" and "refresh my review requests" as discovery
and preparation requests. Without an explicit selection, identify the authenticated
GitHub user and the current repository from its remote, then find every open PR
in that repository currently requesting that user's review. An explicit repository,
organization, or PR selection overrides this default. Do not ask the user to supply
PR numbers that the connected service can discover. If identity or scope cannot
be established, resolve that missing information before claiming discovery is complete.

Use the available GitHub tools or CLI and follow every result page. If search or
access limits prevent a complete result, report the uncovered scope; do not present
a partial list or a failed query as all requests or as an empty queue. Review
requests are the selection criterion; authorship, assignment, and mentions alone
do not add PRs unless the user asks for that selection.

A fresh discovery request authorizes adding all matching PRs, including ones
removed from an earlier queue. Add newly found entries, check existing comparisons
before launching reviewers, reuse matching preparation, refresh affected results,
and finish incomplete checks. Repeat discovery on each such request so new review
requests are included. Keep preparation local under the existing publication rules.

After complete discovery, put the current matches first in the index in useful
stack order. Keep saved entries outside that selection separately, preserving their
reports and notes; a PR merging, closing, or losing its review request does not
remove its entry. Report how many PRs matched and their preparation readiness. An
empty successful result means no current review requests in the resolved scope.
"Show my queue" remains a local read, and refreshing saved reviews alone does not
implicitly discover or add PRs.

## Prepare reviews, not just explanations

Establish each PR's exact head and actual merge base, including stacked bases.
Read the description and relevant discussion as claims to check against code.
Use exact source views without switching branches or changing the user's files.
The preparation should establish:

| Area | Method and saved result |
| --- | --- |
| Understanding | Use installed `pr-comprehension`: motivation, building blocks, one concrete end-to-end walkthrough, source links, and the implemented boundary. |
| Code review | Use the repository's review skill and `REVIEW.md`. In Gimlet, run `gml-review`, including its informed, blind, and ownership reviewers. Save each reviewer's factual report and the consolidated findings. |
| Design | Apply installed `design-challenge` where architectural assumptions, ownership, dependencies, or complexity warrant it. Save supported concerns and alternatives, or why no separate critique applies. |
| Reviewability | Assess coherent behavior and stack dependencies. Apply `identify-pr-splits` when splitting could materially simplify review; otherwise record why the boundary is cohesive. |
| Verification | Run relevant authorized tests/builds on the reviewed source and inspect useful CI evidence. Distinguish executed, inspected, unavailable, and deferred checks. |

Select other available specialist checks from the actual languages, contracts,
and risks changed. Do not invoke every installed skill by name matching, repeat
checks already covered by the review, or turn preparation into fixes, publication,
or a deployment. Report a missing required review capability as a limitation;
an explanation alone must not be labeled a completed code review.

Preserve independent reviewer isolation: blind and ownership reviewers receive
the comparison and repository rules, without the overview, rationale, prior
findings, or design critique. Reconcile the results before composing the main
note; include only supported findings and material limits there. Check reports
may retain factual coverage and source evidence, not private reasoning transcripts.

Schedule the batch within available execution capacity. Account for the review
skill's own workers rather than nesting unbounded PR workers. When delegation
is prohibited or unavailable, follow the review skill's permitted fallback and
record the resulting limits. Do not imply work continues after the turn ends.

Save check results as they finish. Finish the explanation after the checks so it
reflects their discoveries. Recheck the source comparison before marking the
entry ready. If the code moved, identify the delta and refresh affected results
or leave the entry clearly incomplete for that comparison. One failed PR must
not erase its previous usable report or prevent preparing the other PRs.

## Reuse before launching reviewers

1. Resolve the requested comparison. For staged changes, the base is local
   `HEAD` and the target is the index; exclude unstaged edits. For a clean branch
   or PR, resolve its actual comparison rather than assuming `main`.
2. Find the entry by repository/PR identity. After `git uncommit`, branch metadata
   may point at the parent PR: match the saved base/head contents against the
   staged comparison instead of trusting that association or changed filenames.
3. Use `scripts/check_review.py` as described in `storage.md`. It reads local
   Git objects and reports whether the code, base context, and review rules match.
   It does not fetch, edit files, or launch checks.
4. On a match, read `review.md`, relevant check reports, and `notes.md`. Say once
   that the prepared review is being reused, then answer the user's question.
   Do not rerun reviewers, tests, or the whole explanation merely to reproduce it.

Focused source reading is encouraged when it answers a follow-up. It does not
restart the review. Use the saved reports as the evidence-backed starting point;
retain important limits and distinguish prior execution from newly run checks.

If content or context differs, compare it with the reviewed revision and update
only the conclusions and checks affected when that is sufficient. Identical diff
text alone does not establish identical surrounding code. Changed commit IDs
alone do not invalidate identical source trees. A base update needs an impact
assessment, not an automatic full rerun. Apply changed review rules to the gaps
they create. New PR comments can warrant focused investigation; titles, bot
comments, CI updates, timestamps, and merge/approval state are not blanket review
invalidation rules.

Rerun a full review when requested, or when material changes or missing evidence
make incremental reuse unreliable. State the concrete reason before launching
it. Update the saved comparison only after the prior results and new work jointly
cover it. If freshness cannot be established, explain what remains unverified;
use clearly scoped existing results while investigating rather than silently
calling them fresh or reflexively launching reviewers.

## Keep the discussion useful

Begin with the change's need and a concrete walkthrough using the saved note.
Adapt the explanation to what the user is struggling with; do not recite every
report. Bring relevant findings into that walkthrough and link their evidence.
Consult detailed reports when asked which reviewer raised an issue or how a
conclusion was established.

Save consequential discoveries, user decisions, deferred follow-ups, and resolved
questions in `notes.md` for that existing entry. Update a finding when new evidence
changes it. Preserve user edits and keep facts, proposals, and decisions distinct;
do not save a conversation transcript or reopen settled choices without cause.

## Deliver

The index contains PR links, one-line purposes, and preparation readiness, in a
useful stack order. Keep it a reading queue rather than a metadata dashboard.
Ready means review preparation is complete, including recorded verification
limits; it never means approval, passing unexecuted tests, or production readiness.

Return the main checkout's absolute index link and counts of ready entries and
entries needing attention. During discussion, return the explanation and findings
directly rather than requiring the user to open files. Explain once that deleting
an entry removes it from the queue, and deleting the queue clears it.
