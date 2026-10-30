---
name: machine-diagnosis
description: >-
  Diagnose a slow or full development machine, profile personal disk usage, and
  identify forgotten experiments, stale processes, and cleanup candidates.
  Use when the user wants to find space, investigate resource hogs, or clean up
  experiment artifacts and build caches. Supports scoped cleanup after diagnosis.
---

# Machine diagnosis

Turn resource usage into understandable cleanup decisions. Connect large files
and running processes to the experiments, builds, or worktrees they belong to.
Help the user reclaim space without losing expensive results or interrupting
useful work. Start with diagnosis unless cleanup of specific targets is already
explicitly authorized. Invoking this skill alone authorizes inspection.

## Establish the scope and current pressure

Use the conversation to determine the machine, owner, paths, and intended result.
Default to the user's home directory and their experiments or temporary
worktrees; inspect shared filesystem capacity to put personal usage in context.
Do not broaden cleanup to other users or system services without authorization.
Honor instructions such as “don't fix it yet.”

Check filesystem bytes and inodes, available RAM, swap, CPU count, load, and
resource pressure. On Linux, useful starting points are `df -h`, `df -i`,
`free -h`, `nproc`, `uptime`, and `/proc/pressure/*`. Follow up with short samples
from `vmstat`, `iostat`, or `pidstat` when they distinguish likely causes.
Interpret load relative to CPU count, and use available rather than free RAM.
A single latency spike or large process does not establish a system bottleneck.

Check whether process visibility is isolated by the execution sandbox. An empty
process list or missing `/proc/<pid>` inside that namespace does not establish
that a host process has exited. Use the environment's approved host inspection
mechanism when needed; state any remaining visibility limits.

## Profile disk usage without making the machine worse

Start with one shallow traversal of the selected paths. Save timestamped output,
errors, hostname, scope, and exclusions in a private temporary location so later
questions can reuse the same measurements. Capture intermediate results instead
of piping the entire traversal through a sort that hides progress. Summarize and
sort the saved output afterward. Do not print file contents or environment
variables that might contain credentials.

For Linux, `du -x -h --max-depth=N <path>` measures allocated space without
crossing filesystems or following symlinks by default. Choose enough output
levels to expose likely cache owners, such as individual Bazel output bases.
The depth limit reduces output, not traversal work. Avoid overlapping scans;
reuse parent measurements before drilling into the largest unexplained areas.
Keep shared-node scans low priority when supported. Do not install tools merely
to obtain a prettier report.

Bazel test runfiles and sandboxes can contain enormous numbers of entries.
For a quick initial pass, consider `--exclude='*.runfiles'` and report that
exclusion alongside the totals. Do not silently exclude experiment output or
sandbox trees merely because they are large. Bound expensive follow-up scans,
retain partial results, and explain when an exact count is not worth the cost.
Keep permission and disappearing-file errors visible in the saved report.

Distinguish physical allocation, apparent size, symlinks, hard links, and nested
totals when that affects reclaim estimates. Do not add a parent and its children
or promise that deleting one hard link frees all reported bytes. If `df` and
`du` disagree materially, consider excluded paths, other users, snapshots,
reserved blocks, mounts, and deleted files held open by processes. Inspect
open deleted files when useful; avoid an unbounded whole-machine walk.

Compare only scans with matching scope and exclusions. Record free capacity at
start and finish: concurrent builds or cleanup can change it independently.

## Find forgotten experiments and explain ownership

For the largest candidates, identify purpose, owner, size, relevant dates, and
whether work is still using them. Prioritize likely experiment locations,
checkpoint/model directories, generated datasets, logs, build outputs, download
caches, and artifacts associated with temporary worktrees. Search selectively
within measured hotspots rather than crawling all files again.

Use process owner, executable, working directory, parent/child relationships,
elapsed time, resource samples, and open output files to associate jobs with
artifacts. Check GPUs or containers if the workload uses them and tools are
available. Prefer selected metadata over broad command lines that may expose
secrets. Use narrow open-file checks on candidate paths, not recursive `lsof`
across a huge cache.

Separate these situations:

- Active work whose outputs or checkpoints are still changing.
- A completed or failed experiment with large outputs left behind.
- A long-lived process that may be idle, detached, waiting, or still valuable.
- Rebuildable caches and outputs, with a concrete rebuild or download cost.
- Source worktrees or unique experiment results that require preservation.

Age, low CPU use, a missing terminal, or an orphaned parent are clues, not proof
that work is abandoned. Sample activity when needed. Modification time does not
prove last use, and access time may be disabled or misleading. Mark uncertain
cases for the user's judgment instead of calling them safe to remove.

For Bazel, map hashed output bases to workspaces using `DO_NOT_BUILD_HERE`,
workspace metadata, or execroot links. Identify current server/process activity
with host visibility. Separate shared repository downloads, per-workspace
outputs, sandboxes, and any configured disk cache. Follow repository guardrails;
in Gimlet, do not run `bazel clean` or its variants and do not delete untracked
Git files. A source checkout and its generated cache are different candidates.

## Present a concrete cleanup choice

Lead with current pressure, the largest findings, and what changed since the
last comparable scan. Rank candidates by expected benefit and cost. For each
candidate provide the exact path or process identity, measured size or resource
use, what it belongs to, evidence of activity or staleness, proposed action,
reclaim estimate, uncertainty, and consequence. Group related job/artifact pairs
so the user can decide about an experiment as a whole.

Recommend a small useful first batch. For example, distinguish expendable logs
from checkpoints that would require rerunning a costly experiment. Offer
preservation of selected results when appropriate; moving files on the same
filesystem does not reclaim capacity. Do not upload artifacts elsewhere without
authorization. Keep the report concise enough to make a decision directly.

If the request was diagnosis only, deliver the findings and stop. If cleanup is
wanted but targets are not yet authorized, ask for approval of the concrete
batch, not generic permission to “clean the machine.” Honor existing approval
for explicit targets without asking again. A vague request to find space does
not authorize deletion of unique experiment results or termination of jobs.

## Execute authorized cleanup and verify

Immediately before acting, recheck paths, ownership, symlink resolution, process
identity/start time, and activity where relevant. Stay inside the approved
scope; pause a target whose identity or state has materially changed. Avoid
broad name-based process kills or deletion globs. Check for worktree changes
before proposing source removal, and respect the rule against deleting
untracked files.

For an approved job termination, use its supported shutdown or SIGTERM first.
Verify host-visible exit and child processes. Escalate to SIGKILL only within
the authorized scope and after allowing graceful exit. Do not restart stopped
work or kill another user's process based solely on resource consumption.

Delete only the approved artifacts or use an appropriate scoped cache cleanup
mechanism. Recheck filesystem availability and any surviving open deleted
files. Distinguish estimated reclaim from observed capacity change; concurrent
activity may obscure attribution. Report what was removed or stopped, what was
preserved or skipped, and remaining candidates. Do not leave scans running
unmentioned at turn end or claim cleanup from a successful command alone.
