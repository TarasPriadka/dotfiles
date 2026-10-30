# Background preparation

## Discover and capture once

On an explicit discovery/update, resolve the authenticated user and repository.
An explicit repository, organization, author or PR selection overrides the default;
otherwise find all open PRs requesting the user's review, following every page.
Do not ask for PR numbers the service can discover. Report search/access limits
rather than calling an incomplete result an empty queue.

Capture the selection and exact head/actual merge base, including stacked bases,
in the manifest. Fetch Git objects, descriptions and useful discussion in parallel;
use exact source views without switching the user's branch. Avoid full source
copies/worktrees unless needed. Launch each PR's jobs as soon as its inputs arrive,
without a whole-batch fetching barrier.

This is the run's snapshot. Do not rediscover the selection, repeatedly check heads
or chase rebases while bots run. Finish the captured revision; note known drift.
New heads belong to the next explicit update.

## Use a real runner

Choose an available background agent/task runner that keeps scheduling after the
conversation ends. Persist its confirmed handle, manifest and progress before
reporting it started. The runner owns dispatch/completion; ordinary chat subagents
or yielded shell calls alone do not establish durable background execution.
Do not install a daemon or create a recurring schedule unless requested. Without
a capable runner, save a pending manifest and report the missing capability.

## Keep slots occupied

Use a flat queue of `(PR, comparison, bot role)` tasks, each with its own context.
In Gimlet: overview, informed, blind and ownership. Informed gets intent/description;
blind and ownership receive only comparison, source and repository rules. Withhold
overviews/prior findings from blind roles. Overview runs alongside reviews.

- Fill available slots immediately; each completion dispatches the next eligible
  task without waiting for siblings, another PR or an entire batch stage.
- Avoid nested coordinators consuming slots while waiting for child bots, and
  long-lived role agents walking all PRs serially. Schedule at bot-job granularity;
  the runner's real capacity is the only concurrency barrier.
- Count observed live worker handles, including pre-existing/cancelling work,
  against capacity until their runner confirms release; do not assume a slot is free.
- Join existing live work for the same comparison/role and reuse finished outputs.
  Prioritize a PR requested for discussion without duplicating/cancelling work.
- Run every scheduled task once per attempt. Save failures and continue; no
  automatic retry, coverage-audit loop or reopening a returned bot.
- An explicit update can resume missing/failed roles while retaining finished
  ones. An explicit full rerun creates a new attempt.

Save every output immediately. Publish overviews/partial findings as available;
consolidate a PR when its own review jobs finish, without waiting for other PRs.
Failed/cancelled tasks are terminal: a partial run can finish without retrying them.
Consolidation deduplicates and records disagreements/limits; it does not trigger
another investigation or regenerate completed bot outputs.

## Prune during maintenance

During explicit updates, check saved PRs' authoritative merged/closed status,
preferably batched with discovery. Prune confirmed obsolete entries and index rows;
open PRs keep their analysis. This is queue cleanup, never Git branch/source
deletion. Do not scan/clean the whole queue when discussing a single PR.

An unavailable status lookup is not permission to delete. Defer entries explicitly
marked to keep or actively used. Cancel/invalidate pending tasks before pruning,
and wait for short reader/writer claims to clear. Workers publish only while their
entry exists and attempt is current: late results cannot resurrect deleted entries
or overwrite newer work. Fresh explicit discovery may add a reopened/requested PR
under a new attempt; old manifests and workers cannot add it back themselves.
