# Shared workspace and saved results

Resolve the main checkout from the first record of `git worktree list --porcelain
-z`. All linked worktrees use its `.pr-review-queue/`; do not switch its branch.
If needed, locally exclude only `/.pr-review-queue/`, leaving tracked ignores alone.
Namespace entries by full forge/repository/PR identity.

```text
.pr-review-queue/
  index.md
  .jobs/<run-id>/
    manifest.json
    progress.json
    runner.log
  github.com/owner/repo/123/
    overview.md
    review.md
    reviewers/informed.md
    reviewers/blind.md
    reviewers/ownership.md
    notes.md
    state.json
```

Overview explains need, before/after behavior and scope. Review contains findings,
source links and limits; individual reports retain factual evidence/lifecycle
traces, not private reasoning transcripts. Notes preserve discussion decisions.
Existing combined `review.md`/`checks/code-review.md` remains usable without migration.

## Results, completion and freshness

Record the captured comparison and jobs actually requested:

```json
{
  "base": "reviewed merge-base SHA",
  "head": "reviewed head SHA",
  "expected_jobs": ["overview", "informed", "blind", "ownership"],
  "jobs": {
    "overview": {"status": "complete", "report": "overview.md"},
    "informed": {"status": "complete", "report": "reviewers/informed.md"},
    "blind": {"status": "failed", "error": "worker exited without a report"},
    "ownership": {"status": "complete", "report": "reviewers/ownership.md"}
  },
  "review_rules": {"REVIEW.md": "sha256 of reviewed instructions"},
  "files": {"overview.md": "sha256", "review.md": "sha256"}
}
```

States: `pending`, `running`, `complete`, `failed`, `cancelled`. Each complete job
names its report; hash every generated report in `files`, not just those shown.
Coverage limitations are report/job annotations, not job failures. An explicit
overview-only request can select only that role; do not call it a code review.

A run finishes once every task is terminal (`complete`, `failed`, `cancelled`),
even when some roles failed. Record that separately from whether every requested
role produced a report. Failed roles do not keep a run waiting or hide available
results. No design/scope/verification/coverage gate is required, and completion
never implies code execution.

## Job records and concurrency

Manifest: run ID, runner handle, frozen selection/comparisons and roles. Progress:
task status and worker handles. A running update is separate from the prior saved
snapshot, which remains readable. A manifest without a confirmed live runner is
pending/interrupted, not proof of running work.

Use short per-entry/task claims with runner ownership to prevent duplicate dispatch
and publication; do not hold locks during analysis. Runner completion/failure
releases claims. Recover stale claims using runner liveness, not elapsed time alone,
so discussion cannot wait indefinitely on a dead worker.

Write private task output, publish files and atomically replace completion metadata
under the entry's short write claim. Verify membership/attempt before publishing.
Cleanup invalidates attempts before deletion. Workers never recreate a missing
entry. Active readers/explicit keep markers defer pruning. Delete only confirmed
merged/closed entries, never unrelated repository files.

Compare recorded checksums before replacing generated text; reconcile human edits
instead of overwriting them. Notes are maintained separately. Manual deletion
removes membership. Derive the index from entries/live job records, distinguishing
results available, jobs running/failed and known drift. Unknown forge status leaves
membership intact.

## Read before starting work

Read the saved overview/review, relevant notes and state directly. Existing reports
are usable even with partial/missing metadata; say which revision and roles they
cover. Check live job records before scheduling missing work. Do not make a cached
discussion wait for migration, completeness checks or a comparison helper.

At the start of a PR discussion, cheaply compare that PR's current head/actual
merge base with the saved source using metadata and read-only Git views. Reuse
local objects and tree IDs; fetch only missing comparison data. Include modes and
exclude unstaged edits from an index target. Different commits with identical
source/context trees remain covered. Note changed relevant rules separately.

If changed, show the saved review and a brief unreviewed delta: changed commits,
files/behavior and touched prior-finding locations. Distinguish PR changes from
base-context changes, without reevaluating correctness or claiming fixes. Ask once
whether to rerun/update this PR, then wait for authorization; no bots run merely
because freshness changed. Missing objects/metadata mean unverified freshness,
not a fresh review or an automatic rerun. If an update already exists, join it.

Keep recorded base/head, reports and notes intact while summarizing the delta.
Only an authorized rerun publishes a new reviewed comparison. A cheap status/delta
note must not overwrite the old review's findings or mark the newer code reviewed.

The existing `scripts/check_review.py` is a legacy comparison tool with older
completion gates. It is not part of this workflow and must not gate report reuse.

Older `checks` records and explanation-only entries stay readable. Missing new
schema fields do not justify redoing saved analysis or inventing prior bot reports.
Preserve old files/limits; migrate only when useful work requires an entry update.
