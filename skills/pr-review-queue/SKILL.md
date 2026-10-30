---
name: pr-review-queue
description: >
  Prepare and cache code reviews and PR overviews for later discussion. Use for
  explicit discovery/background queue updates, and before discussing or reviewing
  a PR: use saved analysis first, join existing work, or prepare and save a missing
  PR. Check freshness and summarize later changes without rerunning bots; ask before
  updating stale reviews. Prune merged/closed entries during queue maintenance.
---

# PR review queue

The queue is a persistent workspace shared by preparation jobs and discussion
agents. Run analysis bots once for a captured revision; later conversations use
their saved results. Preparation should take bot execution time plus small
fetching, scheduling, consolidation and storage overhead.

## Choose the operation

- **Prepare/update:** only on an explicit discovery, preparation or queue-update
  request. Discover the selection, prune obsolete entries, reuse saved work and
  schedule missing analysis. Read [preparation.md](preparation.md).
- **Discuss/review a PR:** look in the shared workspace first. Read its saved
  overview, findings and relevant notes before investigating or launching bots.
  Say once: "I'm using the prepared review from the queue," naming its revision.
  Make the lightweight freshness check below; it does not start a new review.
- **Cache miss:** prepare only that PR, save its results and discuss them. Do not
  discover unrelated PRs. Honor explicit overview-only or findings-only scope.
- **Show/status:** read the local index and job records; no GitHub fetch or new work.
- **Explicit refresh/rerun:** update the selected PRs. Reuse finished jobs for an
  unchanged comparison; a requested full rerun starts a new attempt.

Read [storage.md](storage.md) when locating, matching or writing entries. See
[examples.md](examples.md) for scheduling, reuse and cleanup scenarios.

## Discussion uses saved work

Keep result availability, job completion, coverage limits and freshness separate:

| Available work | Discussion behavior |
| --- | --- |
| Saved analysis | Explain it directly, check freshness, and preserve its reviewed revision and limits. |
| Stale saved analysis | Show the old review plus a short unreviewed-change summary; ask before rerunning. |
| Saved analysis with an update running | Use the saved snapshot and mention the update. |
| Running job, no saved analysis | Join/prioritize it; use finished outputs as they arrive. |
| No entry or job | Run and save the single-PR analysis jobs. |
| Some bots failed | Use completed reports and name missing roles. Retry only in an explicit update. |

Do not block useful discussion on other PRs, optional checks, complete coverage or
CI success. Name the specific dependency if the requested result is still running.
Never duplicate a running job. Focused source reads can answer questions without
restarting bots. Save consequential discoveries/decisions in notes.

On opening a PR discussion, check only that PR's current head and actual merge
base against the saved comparison. Reuse local objects/tree IDs where available;
fetch only missing comparison data. Do not scan the queue, poll heads, inspect all
CI runs or launch bots for this check. Identical source/context trees remain
covered after a commit-ID-only change. Source/context or relevant rule changes
make the saved review stale; missing evidence makes freshness unverified.

When stale, keep the saved review visible and give a short, factual summary of
changes since it: new commits/changed areas and whether old finding locations were
touched. Separate changes to the PR from base-context changes. This is a delta
summary, not a correctness review: do not silently mark old findings fixed or
claim the new code is reviewed. Then ask once for that revision: "Rerun the bots
and update the saved review?" Until the user agrees, use the old snapshot with its
limits. If that update is already running, join it instead of asking to duplicate
it. An explicit rerun request is already authorization; do not ask again.

Say which roles finished and disclose missing reports/coverage limits. A review
is ready for its recorded source when the requested bots returned and their
reports are saved; partial or stale results remain useful but must be labeled.

For staged work, compare local HEAD to the index, excluding unstaged edits. Match
saved source contents rather than branch association after a soft reset. Do not
invent a forge identity for unrelated local-only work.

## Code analysis only

Default jobs are a PR overview and the repository's review bots. In Gimlet, use
`pr-overview` and the informed, blind and ownership roles from `gml-review`, passing
review criteria unchanged. This queue controls orchestration: overview and review
jobs run independently, outputs are saved locally, and publication is not prompted.

Do not run builds, tests, benchmarks, lint, deployments or PR source edits during
preparation/discussion. Existing CI can be recorded if already available; fetching
it is optional and never gates a result. Bots may suggest checks. Execute checks
only when the user separately requests them.

The coordinator schedules, saves and consolidates. It does not conduct a fourth
review, launch extra design/split/reader bots, audit full-file reading, or reopen
finished workers for completeness passes. Preserve supported findings, disagreements
and coverage limits. A returned limited analysis is a finished job; a crashed or
missing bot is failed. Do not turn missing evidence into a claim of full coverage.

## Deliver

Publish each PR's results as they arrive; a slow PR must not hold back others.
Background launch responses include the actual runner handle and workspace/index
path. Ending a chat is not background execution. Without a real capable runner,
state the limitation and leave a pending manifest instead of silently waiting in
the foreground or claiming jobs are running.

Batch completion returns the index and finished/running/failed job counts. During
PR discussion, return the explanation and findings directly with the saved-entry
link. Finished preparation is not approval or test execution. Post to GitHub only
on an explicit request.
