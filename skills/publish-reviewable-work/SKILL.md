---
name: publish-reviewable-work
description: >
  Shape and publish a specified body of engineering work as coherent PRs that
  are inexpensive to understand, review, and merge. Use when asked to split a
  change for review, prepare parallel and dependent PRs, or publish a body of
  work with concise overview comments and a Claude review request per PR.
  A design-only request produces a proposed breakdown without publishing.
---

# Publish reviewable work

## Own the cost of getting the work reviewed

Publishing work hands another engineer a decision: should this change become
part of the system? They need to understand why it exists, what agreement or
behavior changes, and whether the evidence supports accepting it. The author
already holds much of that understanding. Part of finishing the work is using
it to make the reviewer's decision easier.

A large diff can force a reviewer to discover several designs at once. Splitting
it mechanically can make things worse: the same reasoning gets repeated across
PRs, tests are separated from the behavior they establish, and a simple change
acquires several merge and rebase steps. Aim for coherent decisions with little
unnecessary coordination. Neither the smallest PR nor the largest number of
parallel branches is inherently the best result.

An owner figures out the review boundaries and the path to landing the work.
They prepare the explanation, preserve correctness at intermediate revisions,
and keep dependencies visible. The user should not have to identify every hunk,
choose every base branch, or discover later that an apparently independent PR
needs an unpublished prerequisite.

## Understand the change before deciding its shape

Resolve the requested source branch or worktree, its actual base, and the scope
to publish. Inspect the aggregate change, including intended uncommitted and new
files. Existing commits are evidence of how it was built; their boundaries may
not be appropriate review boundaries. Preserve unrelated work and the source
snapshot. Reconcile concurrent source edits before declaring the extraction complete.

Build a model of the resulting behavior and the important concepts introduced
or changed. Follow contracts, consumers, generation, and tests far enough to
identify what must move together. Distinguish reusable foundations, behavior
changes, integration, and incidental cleanup. These are possible concerns to
recognize, not categories that must each become a PR.

For each proposed part, establish why it is worth accepting, what it needs from
other parts, and how its behavior can be verified at its intended base. A small
preparatory change can be legitimate before its consumer exists; explain the
concrete consumer it enables and establish that the intermediate state is safe.
Do not invent a general abstraction simply to manufacture a foundation PR.

## Choose boundaries that reduce review work

Use these options where they make a review easier; they are not a required
sequence or a quota of PRs:

- **Refactoring:** separate substantial moves, renames, or restructuring from
  behavior changes so preservation and new behavior can be assessed separately.
  Small local cleanups can stay with the change. Establish missing coverage of
  existing behavior before a risky refactor; keep tests of new behavior with
  the behavior change.
- **Vertical slices:** carry one narrow behavior through the layers it needs
  when following the complete path makes correctness easiest to assess.
- **Horizontal slices:** separate a contract or layer when its semantics can be
  reviewed with concrete usage context. Include a representative consumer when
  otherwise the interface's suitability would be speculative.
- **Reviewer concerns:** separate self-contained concerns requiring different
  expertise, such as infrastructure and application logic. Explain the agreement
  between them so neither reviewer has to guess what the other part provides.

Combine these options when useful, rather than automatically making one PR per
layer or directory. This follows [Google's small-CL guidance](https://google.github.io/eng-practices/review/developer/small-cls.html).

## Choose review units and real dependencies

A useful unit gives the reviewer one coherent change to reason about. Keep its
tests, generated bindings, and required build changes with it. A directory,
language boundary, or line-count threshold alone does not define a review unit.
Combine tightly coupled changes when splitting would require the reviewer to
understand them together anyway or would leave an invalid intermediate state.
Challenge a proposed split when each reviewer must reconstruct the same invariant
across several PRs. A useful boundary reduces that burden without hiding the
integration question; identify where the combined behavior will be verified.

Start each unit from the intended integration branch unless a real prerequisite
requires another base. Two changes are independent when each can build, satisfy
its contract, and be safely accepted without the other. Shared files may create
an integration conflict without creating an architectural dependency. Conversely,
disjoint files may depend on the same new contract.

Distinguish review order, code prerequisites, and rollout prerequisites. Reviewers
can assess dependent PRs concurrently once their shared contract is sufficiently
settled, even though merging requires an order. Conversely, code can compile without infrastructure
or a compatible service version that must exist before activation. Record what
must be merged, deployed, or confirmed operational before each step is safe.
A rollout dependency alone does not require a stacked branch if the code can
land safely while inactive; if merging activates it, that prerequisite gates
merging too.

For incompatible interfaces or schemas, consider
[expand, migrate, then contract](https://martinfowler.com/bliki/ParallelChange.html):
add support alongside the old contract, move consumers, then remove old support
once migration is established. State the evidence required before cleanup,
including deployed consumers when relevant. Compatibility scaffolding has a cost;
use it when needed for safe transition, rather than just to create smaller PRs.

Choose the branch shape from the code prerequisites:

- **Independent roots:** both target the integration branch and can be reviewed
  and landed independently. Do not stack one on the other merely because it was
  implemented second.
- **One prerequisite:** base the dependent PR on that prerequisite so its review
  diff contains only its own contribution. Use the repository's stack tooling
  for a genuine chain.
- **Several independent prerequisites:** preserve their independence. A normal
  PR has one base; drawing a dependency graph does not give it several bases.
  Publish the foundations first, develop and test the combination on an isolated
  local integration branch, and publish the dependent PR with a clean comparison
  once its prerequisites are available in a common base. Alternatively, after
  all but one prerequisite land, stack it on the remaining prerequisite.

Do not copy prerequisite patches into several published PRs and present the
copies as independent work. Do not force a chain merely to fit the tool. If
early publication of a combined preview is specifically useful, identify it as
such, state that its diff includes prerequisites, and explain how it will become
a clean review. A preview is not another independently mergeable unit.

For example, a request parser and a preprocessing client may each be testable
against existing contracts on `main`, while endpoint wiring needs both. The
parser and client can be separate root PRs; their tests stay with them. The
wiring is a dependent integration change, not evidence that the client must
wait for the parser. Confirm those contracts in the actual code before choosing
this shape. If both introduce a shared new representation, that representation
is a real prerequisite and changes the breakdown.

Explain the proposed shape compactly before substantial extraction: each PR's
review decision, relevant reviewer expertise, base and actual prerequisites,
and how it will be verified. Make clear what can land independently and what
remains inactive or awaits deployment. Explain consequential boundaries, without
requiring a separate reviewer for every concern or a fixed proposal template.
Name any tradeoff involving compatibility work, deferred publication, or costly
restructuring. Proceed within the user's existing authorization; obtain direction
when the choice materially changes the agreed delivery or design.

## Materialize and verify the proposed boundaries

Use isolated branches or worktrees to preserve the source and other ongoing
work. Cherry-pick a commit only if its content matches the chosen unit; otherwise
extract the relevant changes deliberately. Follow repository signing, generation,
staging, and branch conventions. Keep temporary extraction artifacts out of PRs.

Validate each unit on the base its reviewer will see. Passing tests on the full
development branch does not establish that an extracted foundation works alone.
Run the relevant checks for each unit and integration checks for the combined
outcome. Where versions coexist during rollout, check the compatibility relied
on at that boundary; a successful build does not establish deployed readiness.
Report unverified rollout conditions as prerequisites, rather than implying that
local validation established them. Follow required repository checks, and reuse
still-valid evidence rather than rerunning unchanged checks without reason.

Check both the individual comparisons and the assembled result. Every intended
source change should be accounted for, prerequisites should not be duplicated
in review diffs, and no change should disappear between the parts. Explain any
intentional difference introduced while extracting, such as compatibility wiring.
Prefer grouping coupled work over adding substantial temporary machinery just
to make smaller PRs possible.

## Publish an understandable change

Use the repository's PR-creation skill and conventions for each unit. Use its
stack skill only where the dependency structure warrants it. In Gimlet, read
[the integration notes](references/gimlet.md) before execution. Inspect current
tool capabilities instead of assuming a stack command preserves custom metadata
or supports a branching dependency graph.

Publication through this workflow includes a concise overview comment and one
Claude review request on each PR it publishes. A request to design the workflow
or propose a split alone does not authorize pushing or commenting. Honor explicit
exceptions such as local-only work or no bot invocation.

Prepare the explanation from the actual final comparison. Use `pr-overview`
where available, with direct publication requested as part of this workflow;
reuse the source understanding already established. Keep the PR body in the
repository's required format. The overview comment supplies the conceptual
explanation without turning the body into a second design document.

Lead with the concrete motivation and this PR's contribution. Show the relevant
before/after behavior or relationships, then give only the evidence, constraints,
and code links needed to assess it. For a small PR, a short paragraph and compact
flow may suffice. Often 100–200 words are enough; this is not a quota. Avoid file
inventories, investigation history, and repeating the whole project's design in
every comment. A preparatory PR must say what remains inactive or deferred.

Include a compact statement of dependencies with PR links once available. Say
whether the PR can land independently, is based on another PR, or awaits several
prerequisites. Distinguish review order from required merge order. The explanation
must be understandable without requiring the reviewer to read all related PRs.

Publish the checked overview on the intended PR, using revision-pinned code links
and recording the comparison it describes. Then post one separate regular PR
comment whose body is exactly:

```text
@claude review
```

Before posting, check all relevant existing comments, including pagination, for
an earlier actual invocation, rather than a quoted discussion of the command.
Do not add another merely because the workflow resumed,
the branch was rebased, or the bot has not replied. If a posting call has an
ambiguous result, inspect the PR before retrying. Retain the returned comment IDs
or URLs so a resumed run can reconcile what was published. Distinguish a posted
request from an observed bot run or completed review; do not claim the bot ran
without evidence. Report unavailable review execution instead of repeatedly pinging.
If the only observed bot review covers an earlier revision, state that limitation.

## Keep the publication useful as work progresses

Before handing back, verify the remote PR bases and diffs, draft status where
required, overview comments, review requests, and available check results. Show
the user a compact map of PR links, dependencies, and material blockers. Make
clear what is ready for human review and what still needs prerequisite work.
PR creation alone does not establish merge readiness.

When authorized work continues, resolve feedback in the unit that owns the
change, update affected descendants, and verify their new comparisons. Refresh
the specific overview comment this workflow owns when behavior or scope changes;
preserve human edits and do not overwrite unrelated descriptions or comments.
Keep the original one-per-PR bot request unless the user asks for a rerun.

Publishing does not itself authorize merging. If merging is requested, use the
repository's merge workflow and verify that the PRs actually land on the intended
integration branch. Until then, leave an accurate landing path. A stack that
looks tidy but imposes avoidable serial review, rebase, and CI work has not met
the purpose of this skill.
