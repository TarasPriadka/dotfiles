---
name: pr-review-queue
description: >
  Prepare and refresh a persistent queue of PR overviews for later reading.
  Use when the user supplies a batch of PRs to explain, asks to queue PRs for
  later, or wants an existing queue refreshed. Uses the installed pr-overview
  skill for each explanation and stores browsable, disposable files
  in the main repository checkout, shared across its worktrees.
---

# PR review queue

Prepare understanding ahead of the human's reading. This skill owns queue
membership, storage, refresh, and the index. Load and use the installed
`pr-overview` skill for every explanation; do not duplicate its
investigation or writing instructions here. If it is unavailable, report the
missing dependency before preparing entries. A prepared queue does not imply
that anyone has approved a PR.

## Inputs and scope

- Accept PR numbers or URLs, a batch to prepare, or a request to show or refresh
  the existing queue. Resolve bare numbers against the current repository.
- A batch of overviews or an explicit queue request authorizes local queue
  files. Honor requests for conversation-only output instead. A single PR can
  be queued when the user explicitly wants to prepare it for later.
- With no new PRs supplied, operate only on entries still present on disk. If
  the queue does not exist, report that it is empty without creating it.
- Resolve the main repository checkout for storage as described below. Do not
  switch branches, modify implementation files, stage queue files, or create a
  personal/global store.
- Queue preparation writes local files only. Posting to GitHub is a separate
  task requiring an explicit request.

Read [examples.md](examples.md) for membership and refresh scenarios.

## Storage and membership

Use `.pr-review-queue/` in the **main repository checkout**, not the worktree
where the agent happens to run. Resolve its absolute path from the first
(main-worktree) record of `git worktree list --porcelain -z`. Do not use the
current worktree's `git rev-parse --show-toplevel` as the storage root. "Main"
means the original checkout, regardless of the branch checked out there; never
switch it to the `main` branch. If the repository is bare or the main checkout
is unavailable, ask for a destination rather than creating a second queue.

All linked worktrees share that one queue. Check ignore rules from the resolved
main checkout before writing. If `/.pr-review-queue/` is not ignored there, add
only that entry to its local Git exclude file; the main checkout may not yet
contain this PR's `.gitignore` change. Do not stage generated queue files or
modify the main checkout's tracked files to enable storage.

Namespace entries by their full GitHub identity so numbers from different
repositories cannot collide:

```text
.pr-review-queue/
  index.md
  github.com/
    owner/
      repo/
        123/
          overview.md
          evidence.md
          state.json
```

Existing entry directories are the source of truth for membership. `index.md`
is a derived view, not a list to replay. Create an entry only for a PR explicitly
supplied in the current add/prepare request. A user can delete an entry directory
after reading it, or delete the entire queue to clear it. Never recreate deleted
entries from an old index, conversation, cached task list, or external store.
Re-adding a deleted PR requires a new explicit request.

Keep only the current explanation and evidence for each entry. Do not create
automatic history directories, backups, or another queue elsewhere. Do not
automatically delete entries when PRs close or merge; show their state so the
user can decide when to remove them. Follow repository rules about deleting
untracked files; user-managed deletion needs no agent cleanup operation.

Each entry contains:

- `overview.md`: the concise explanation returned by `pr-overview`, with
  revision-pinned links and the examined comparison in its footer.
- `evidence.md`: selective claims and checked sources, instruction sources,
  tests inspected or run, and consequential unknowns. No reasoning transcript.
- `state.json`: schema version, host/owner/repository/PR number and URL, head
  SHA, base SHA, merge-base SHA, preparation timestamp and requested focus/depth,
  progress, PR state, relevant discussion fingerprint, and any refresh error.
  Record hashes of the overview and evidence when written so user edits can be
  detected before replacement. Use null for facts that could not be obtained.

Progress is `pending`, `reading`, `ready`, `stale`, `incomplete`, or `blocked`.
Keep it separate from the PR's `open`, `closed`, or `merged` state. `ready` means
the explanation is prepared for that comparison, not that review is complete.

## Add and prepare

1. Resolve and deduplicate the supplied PR identities. Inspect existing entry
    directories before creating anything; an existing entry should be reused.
2. Obtain each PR's current metadata and exact comparison using the overview
    skill's gathering instructions. Record its actual base, including stacked
    bases. Reading prerequisite PRs does not automatically add them to the queue.
3. Create entries for explicit additions with `pending` state. Reuse unchanged,
    complete entries when their comparison, discussion, focus, and depth match.
4. Run `pr-overview` for each entry that needs preparation. Supply the exact
    target, comparison, focus/depth, and available context. Use its returned
    explanation. The queue worker also collects the checked sources, comparison,
    checks performed, and unknowns needed for this skill's evidence and state;
    the overview skill does not define or write those artifacts.
5. Verify that the PR comparison has not moved before marking the entry ready.
    If it moved, retain the explanation's original revision and mark it stale;
    refresh within the task's scope or report that work remains.
6. Write the overview and evidence, then mark the state ready. Use atomic file
    replacement where possible; never mark ready before all output is complete.
    On failure, retain the previous usable explanation, mark its limitation, and
    continue preparing other entries.

For a batch, use one overview worker per PR, bounded by available agent slots.
Workers read the overview skill and return content; they do not write queue
files, publish comments, or spawn additional agents. The coordinator owns all
writes and the index. Process sequentially if delegation is unavailable.

Before writing a worker's result, confirm the entry still exists and represents
the same request you assigned. If the user deleted it or cleared the queue while
preparation was running, discard the result. Only the explicit addition step
may create directories; refresh and completion must not recreate them.

## Show and refresh

To show the queue, rebuild the index from existing entry directories. Do not
fetch or regenerate overviews unless requested. Display missing or malformed
state as incomplete rather than treating the entry as ready.

To refresh, check current PR metadata and relevant discussion for existing
entries only. A changed head, base, merge base, discussion, or requested focus
can make an explanation stale. An unchanged head alone is not sufficient.
Reuse valid entries; run `pr-overview` for stale or incomplete ones. Pass the
previous explanation as claims to recheck, not as authoritative context.

If the overview or evidence differs from its recorded hash, preserve the user's
edits and report that replacement needs direction. Do not overwrite those files
as an incidental refresh. Missing metadata or API access leaves freshness
unverified; retain the previous revision and explain the limitation.

Mark closed or merged PRs with their current state without regenerating them
automatically. Rebuild the index after processing and exclude directories the
user removed. Do not infer approval from a merged PR or a completed explanation.

## Deliver

Write `index.md` with relative links to the entry overviews. Use one compact
table: PR, one-line purpose, preparation status, PR state, and consequential
unknown or blocker. Preserve the user's requested order where possible and show
stack dependencies when they help the reader choose an order. Do not invent
review-time estimates or rank entries by finding count.

Return an absolute link to the index in the main checkout and a short count of
ready entries and those needing attention. Explain once that the user can delete
entry directories as they go and delete `.pr-review-queue/` there to clear the
queue. Do not repeat every overview in the conversation unless requested.
