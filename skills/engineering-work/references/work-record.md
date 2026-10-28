# A durable model of the work

Use a record when work spans sessions, dependent workstreams, or decisions whose
reasons would be costly to reconstruct. Reuse an existing ticket, plan, or project
record if it can carry this information. Avoid maintaining two competing accounts.

Otherwise use `.agent-work/<descriptive-task-name>/work.md` in the agreed project
workspace. Before creating one, check for a relevant existing record. Keep local
records uncommitted unless the user requests otherwise. Respect project ignore
conventions; do not change tracked ignore files or stage records automatically.
If a repository has no convention, a narrow entry in its local Git exclude file
can keep the record local. Honor a user-specified destination or no-file request.

Maintain current understanding, not a transcript. Update after meaningful findings,
decisions, verification, and before a handoff or context boundary. Do not rewrite
the record after every tool call. Link evidence rather than copying large outputs.
For a small resumable change, a few paragraphs can preserve the purpose, mechanism,
authorization, evidence, and next action. Crossing a session boundary does not make
it a large project. Omit line-by-line inventories of inspected files and exhaustive
future test plans; retain the behavior and consequential checks the next worker
must establish. Expand only for real decisions, dependencies, or uncertainty.
Use the compact form below by default. Expand into sections or child records when
actual complexity warrants it. Do not include skill-loading narration or environment
history unless the next action depends on it. This is working state, not a report
of the investigation.

```markdown
# <Outcome>

**Assignment:** Purpose, scope, authorization, and completion conditions.
**State:** Current behavior and consequential evidence; relevant workspace/revision.
**Approach:** Current proposal or decision and its reason; open questions if any.
**Verification:** Checks actually run and results; what still needs establishing.
**Next:** Next useful action and its dependencies, or delivered outcome and limits.
```

For substantial ongoing work, use **Next** to preserve the current activity and
bounded commitment: the work to do, what it should establish, and the evidence or
decision needed before moving on. For example: "Investigating: trace one failed
request through decoding and routing to distinguish malformed input from a routing
error. Then choose the affected implementation boundary." This is not a mandatory
schema or a new record alongside the existing one. Omit it when the task is finished.

Keep consequential user wording or a source reference separate from your current
interpretation. Mark whether a correction changes the outcome, scope, approach,
or merely clarifies it. Preserve earlier accepted constraints that still apply.
Record requested checkpoints and delegated authority when they affect continuation;
the activity label itself conveys no permission.

For example, a small design handoff can preserve enough in this form:

> **Assignment:** Reject invalid batch items without submitting a partial batch.
> Design only; implementation and publication are not authorized yet.
> **State:** `submit.py:submit_batch` currently validates and sends each item in
> one loop. Later validation failures can leave earlier items submitted.
> **Approach:** Proposed: validate the entire batch before sending any item.
> Keep the existing validation rules and transport error behavior. Atomicity
> across transport failures is outside this change.
> **Verification:** Existing three tests passed at revision X. No proposed behavior
> is implemented. Establish that an invalid later item causes zero submissions
> and valid batches retain their ordering.
> **Next:** After implementation authorization, reconcile `submit_batch` with this
> record, separate validation from sending, and verify those two behaviors.

Larger work may need explicit decisions with their reasons, independent work items,
and evidence sections. Mark superseded choices and separate user-approved direction
from proposals. Open questions should identify what can settle them and what they
block. Keep observed facts, assumptions, and intended verification distinguishable.

Create child records only when work is independently manageable; connect each to
the parent outcome and dependencies. Where several workers contribute, designate
an owner for the shared record and give others bounded artifacts to return.
Resolve conflicting findings before presenting a single authoritative conclusion.

On resumption, read the current record, inspect the workspace and referenced
evidence needed for the next action, and reconcile drift. A record claiming a
check passed at an earlier revision does not verify newer changes. Continue from
supported conclusions instead of repeating the entire investigation.

Keep reusable project facts in an existing project knowledge location when they
have value beyond this task. Include their evidence and relevant revision or
conditions. Preserve requirements, proposals, observations, decisions, and open
questions as distinct claims. Candidate working lessons need scope and evidence;
propose updates to durable instructions when authorized rather than silently
altering the user's operating defaults.
