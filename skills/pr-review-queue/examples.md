# Queue behavior examples

These scenarios describe the queue workflow. Use the overview skill's examples
for explanation quality; this skill adds no second report format.

## Prepare a batch

Request: "Prepare #123 and #124 so I can review them later."

Resolve both PRs in the current repository, use `pr-overview` for each, and save
their overviews, evidence, and state under the main checkout's
`.pr-review-queue/`. Return the index
link and any preparation limitations. Do not post comments or launch code
reviewers. If #124 depends on #123, explain that relationship and compare #124
against its own base.

## A single immediate explanation

Request: "Explain #123."

Use `pr-overview` and return the explanation in the conversation. Do not create
or refresh a queue merely because one already exists. "Queue #123 for tomorrow"
does request a saved entry, even though it names only one PR.

## Prepare from a linked worktree

The agent runs in `/tmp/project-feature`, linked to the main checkout at
`/home/developer/code/project`. Resolve the main-worktree record and write the
queue under `/home/developer/code/project/.pr-review-queue/`. A later invocation
from another linked worktree reads that same queue. Do not create a queue under
`/tmp/project-feature`, or switch the main checkout's branch. Check ignore rules
in the main checkout, even when the feature worktree already ignores the path.

## Delete as you go

The user deletes #123's directory after reading it. The old index still lists
PRs #123 and #124. On "show my queue" or "refresh my queue," rebuild membership
from the remaining directories: only #124 remains. The old index is not an
instruction to restore #123. If a worker for #123 is still running, discard its
result instead of recreating the directory.

If the user deletes the entire queue, a subsequent refresh reports an empty
queue. "Add #123 again" explicitly creates a new entry.

## Refresh without accumulating history

PR #124's head stays the same, but its base changes. Recompute the comparison and
refresh its overview through `pr-overview`; replace the generated files after
successful preparation. Do not append a revision archive. If its saved overview
contains user edits, preserve them and report that replacement needs direction.

If GitHub is unavailable, keep the last explanation labeled with its original
revision and report that freshness could not be verified. Other ready entries
remain usable.

## Check the workflow

Try the scenarios above in a disposable checkout when changing queue behavior.
Verify that single overviews create no files, all worktrees use the main
checkout's queue, batch output is ignored by Git there,
deleted entries stay absent after refresh and worker completion, and changed
bases invalidate cached understanding. A ready queue entry is preparation, not
a code-review verdict.
