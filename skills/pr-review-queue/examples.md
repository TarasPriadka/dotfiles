# Workflow scenarios

## Background preparation and later discussion

"Update my review queue in the background."

Discover all review requests, check saved entries for merged/closed PRs, capture
revisions once and reuse unchanged results. Confirm a real runner; persist its
handle/manifest. Fill slots with independent overview/review jobs, save results as
they arrive and return the runner/index link. No PR builds/tests. Without a capable
runner, leave a pending manifest and explain the missing capability; do not keep
the foreground conversation waiting as a substitute for background execution.

Later: "Help me review #123."

Find the entry before starting bots. Say it is the prepared review from the queue;
explain its saved change/findings/limits. Focused reads answer follow-ups and useful
decisions go into notes. No discovery, new review or whole-queue refresh.

## Missing entry or work already running

"Review #456" has neither an entry nor live work: prepare only #456, save its
overview/reviews and discuss them. Explicit overview-only requests keep that scope.
If #456 is already running, join/prioritize it without a duplicate. Use finished
outputs with limits, or discuss an older saved snapshot while its update continues.

## Parallelism and stopping

Nine PRs produce 36 jobs with three available slots. Keep slots full; each
completion dispatches another eligible PR/role immediately. No overview dependency,
whole-role serial loop, nested-coordinator wait or slowest-PR publication barrier.
Runtime is bounded by actual capacity/bot duration plus small coordination overhead.

One bot returns limited analysis; another crashes. Save the former as complete,
the latter as failed, and publish other results. No coverage-audit loop, extra
reviewer, automatic retry or build. An explicit update retries missing/failed roles
once while reusing completed roles.

#123 moves H1 to H2 mid-run: finish/save H1 once with its revision; do not chase H2.
Later discussion uses H1 with a known freshness note. The next explicit update
prepares H2. Equal base/head trees reuse results even with different commit IDs.
After soft reset, matching staged content reuses the saved review; unstaged edits
are excluded. Rule/source drift is reported, not an automatic restart instruction.

## Cleanup and races

An update confirms #123 merged/#124 closed: invalidate their pending attempts and
prune entries/index rows when not active/marked to keep. Unknown forge status does
not authorize deletion; open entries remain. Never delete repository branches/files.
Late workers cannot resurrect removed entries or overwrite newer attempts. Fresh
explicit discovery can add a reopened/requested PR again. Single-PR discussion
does not trigger whole-queue cleanup.

## General workflow check

Dry-run these scenarios with a small simulated queue: new PR, saved PR, already
running PR, merged PR and a head that changes mid-run. Check that free slots fill,
outputs publish per PR, cached discussion starts no bots, live work is joined,
merged entries are pruned without late resurrection, and changed heads do not
restart the run. Also check that an unavailable runner is reported honestly.
Use simulated outputs, not real PR reviews or builds, to validate the instructions.
