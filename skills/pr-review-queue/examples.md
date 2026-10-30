# Queue scenarios

## Batch first, discuss later

"Prepare these eight PRs so I can review them tomorrow."

Complete the code reviews, explanations, design/scope assessments, and relevant
verification. Preserve the review skill's independent reviewer isolation. Save
every check result locally and return the queue index; do not post to GitHub.
Compare each stacked PR against its own base. Reading a prerequisite does not add
it to the queue. If tests cannot run, save the reason and the resulting evidence
limit instead of claiming a pass.

Later: "Help me review #123."

The reviewed comparison still matches. Read the saved note and reports, state that
the prepared review is being reused, and start with the concrete walkthrough.
No new reviewers or repeated test run are needed. Follow-up questions cause
focused source reading and useful notes, not repeated review cycles.

## Staged changes after git uncommit

The saved review covers B → H. The user soft-resets to B, leaving H in the index,
and asks "review the staged changes."

The matching script compares HEAD's tree with B and the index with H. Reuse the
prepared review despite the local HEAD and current branch's associated PR changing.
An unrelated unstaged edit does not enter the staged review. If that edit is later
staged, inspect its delta before claiming the saved review covers it.

## Content and context changes

A new commit has exactly the reviewed tree and the same base tree: reuse even
though its SHA differs. If a dependency changed during a rebase, inspect the base
and head changes and their effect on the saved conclusions. Equal patch text alone
does not establish equal context. Update affected checks, or explain why a full
rerun is warranted. A title edit, approval, or new bot comment does not restart
the batch. A substantive new comment can require a focused follow-up.

"Rerun the full review of #123" explicitly requests fresh reviewers. Preserve
blind/ownership isolation from the prior reports and save the new results.

## A simpler PR needs fewer separate checks

A small configuration change still gets its code review and an explanation of
where the configuration is consumed. Record why a separate architecture critique
or split proposal adds nothing. Reuse the code review's existing performance,
ownership, and convention checks instead of launching duplicate specialist work.

## Partial results and human edits

One PR's required review fails halfway through. Save completed checks, leave code
review incomplete, and continue the other PRs. Resuming fills the missing work.
Verification unavailable in this environment remains a clearly limited check.

The user edits `review.md` or adds decisions to `notes.md`. Preserve that text
when refreshing. A checksum difference protects edits; it does not invalidate
the source comparison. Showing the queue reads local files without GitHub calls.

## Existing explanations and deleted entries

An old entry contains only `overview.md` and `evidence.md`. Reuse its supported
understanding, but do not claim reviewers already ran. If a matching completed
review exists in the current session, import it instead of repeating it.

A user deletes an entry or clears the queue. Do not restore it from the index,
conversation, or a pending worker result. Adding that PR again requires a new
explicit addition. Linked worktrees always share the main checkout's queue.

## Check this workflow

Run the comparison helper's tests in a disposable directory:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s <skill-directory>/tests -v
```

The cases exercise matching staged content after a soft reset, source/context
changes, identical trees under different commits, missing/edited reports, changed
rules, and incomplete legacy entries. Also walk through the prompts above to
check that the written workflow starts discussion without launching reviewers.
