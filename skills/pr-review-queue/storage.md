# Storage and comparison

## One queue shared across worktrees

Resolve the main checkout from the first record of
`git worktree list --porcelain -z`. Store `.pr-review-queue/` there, regardless of
its checked-out branch. Do not switch it to `main` or create a separate queue in
a linked worktree. If no main checkout is available, resolve a destination with
the user. If necessary, add only `/.pr-review-queue/` to that checkout's local Git
exclude file; do not stage artifacts or modify tracked ignore files.

Namespace by full forge identity:

```text
.pr-review-queue/
  index.md
  github.com/owner/repo/123/
    review.md
    checks/
      code-review.md
      design.md
      scope.md
      verification.md
    notes.md                 # Only when discussion adds useful context.
    state.json
```

`review.md` is the reading surface: PR link/title, concise comprehension
walkthrough, consolidated findings, and material verification limits. Each check
report holds its factual results, source links, and relevant limitations. Keep the
individual code reviewers' reports under labeled sections of `code-review.md`.
Save additional specialist reports under `checks/` when run. A short reason for
not applying a design/scope check is sufficient; no empty report template is needed.

Directories are membership; the index is derived. Explicit additions include the
selection authorized by a fresh review-request discovery request. Such a request
can add a previously deleted PR again when it still matches. A refresh of saved
reviews, worker completion, or old index must not recreate an entry the user deleted.
Before completing a worker result, verify the entry still exists and belongs to
that preparation. Do not delete entries merely because a PR merged.

After discovery, group current review requests separately from other saved entries
in the index. A local show preserves that last known grouping without claiming it
is live GitHub state. Discovery failure must not mark existing entries as no longer
requested. Keep selection information out of the code-review completion record;
it does not change whether a prepared comparison is covered. Keep only current
generated reports, with no automatic history or global store.

## Small completion record

Use this shape; paths are relative to the entry unless they identify review rules:

```json
{
  "base": "actual reviewed merge-base commit SHA",
  "head": "reviewed head commit SHA",
  "checks": {
    "code-review": "complete",
    "design": "complete",
    "scope": "not-applicable",
    "verification": "limited"
  },
  "review_rules": {"REVIEW.md": "sha256 of the reviewed file"},
  "files": {
    "review.md": "sha256 of generated content",
    "checks/code-review.md": "sha256 of generated content",
    "checks/design.md": "sha256 of generated content",
    "checks/scope.md": "sha256 of generated content",
    "checks/verification.md": "sha256 of generated content"
  }
}
```

Allowed check states are `complete`, `limited`, `not-applicable`, and `incomplete`.
Record all four areas above and any extra checks selected. A limited result must
explain the missing evidence; an unavailable required code review is incomplete.
Record the actual instruction sources used for the review; paths are relative to
the repository or absolute for personal/installed rules. Fingerprints identify
changed instructions so their effect can be assessed, not to demand a whole rerun.

Identity comes from the path and PR link; purpose comes from the note. Do not
duplicate titles, authors, branches, timestamps, request IDs, PR state, discussion
fingerprints, or summaries in this record. Git objects provide tree identities
from the base/head commits. Do not invent facts for missing objects or evidence.

Write reports before completion metadata, using atomic replacement where possible.
Missing metadata, missing reports, or an incomplete check means preparation needs
attention. Report checks that could not run without implying they passed.

Checksums protect human edits. Read existing reports before replacement; if their
hashes differ, preserve the edits and reconcile or obtain direction before
overwriting. Edited prose does not by itself require another code review.
`notes.md` is maintained separately and never replaced by a batch refresh.

## Match a staged or committed comparison

For a staged review, including a PR opened with `git uncommit`:

```bash
python3 <skill-directory>/scripts/check_review.py \
  --entry <main-checkout>/.pr-review-queue/github.com/owner/repo/123 \
  --repo <current-checkout> --base HEAD --head index
```

For a published PR or clean branch, resolve the current actual merge base/head
and pass those commit references to `--base` and `--head`. Matching an index to a
saved head examines all tracked source, including mode changes; unstaged files
are outside that target. Read matching staged source from the index when needed.

The script returns JSON with `reusable`, `changed`, `incomplete`, or `unverified`,
plus reasons and any edited reports. It compares both base and target trees and
checks review-rule fingerprints. It performs no writes or network access. A
`changed` result identifies work to inspect, not an instruction to rerun reviewers.
All outcomes exit successfully; malformed invocation is a command error.

## Existing queues

Preserve old `overview.md`, `evidence.md`, and metadata until their useful content
and edits have been carried forward. Old `ready` means explanation prepared,
not code review completed. Import an already completed review only when its
comparison and evidence can be established, including from the current session;
do not rerun it merely to fill the new format. Otherwise retain the explanation
and mark code review incomplete. Remove obsolete generated files only when
authorized and repository deletion rules permit; never require deletion to reuse
an entry. This skill update alone does not migrate or rerun existing queues.
