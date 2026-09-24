# Resolve PRs and revisions

Use the available forge integration or an authenticated CLI. For GitHub, use
`gh pr view` to obtain the PR number, URL, title, body, base and head revisions,
repository identity, state, and comments. Confirm that a supplied URL refers to
the intended repository.
Read relevant inline comments separately when they explain the author's intent
or a changed decision.

Obtain code at the resolved revisions through Git objects, a separate worktree,
or the API. If objects are missing, fetch the head and base without switching
the user's branch. Account for forks. Record the merge base used by the PR diff;
read old code there and new code at the head SHA. Do not substitute possibly
dirty working files for either revision.

A stacked PR's base may be another PR. Inspect its metadata and relevant later
consumers only when they clarify this PR's purpose. Do not expand the comparison
to the whole stack.

For local work, identify the base revision and staged, unstaged, and untracked
scope. Do not include unrelated untracked files or label a dirty diff with HEAD
alone. Use local file links for uncommitted code. Recheck that the relevant diff
has not changed before delivery.
