# Linear project template

Use this mapping when Linear setup is requested. It works from conversation
context alone; a Notion page or architecture document is not required.
Inspect the destination project and its existing issues before creating work.
Reuse matching milestones and issues, preserving existing states and owners.

## Project

```text
Name: [Project name]
Summary: [One sentence describing the outcome]

Description:
[Short description of the scope and first integrated outcome.]

Included:
- [Core capability]

Deferred:
- [Later extension]
```

Omit empty sections. Add reference links only when the user wants them.
Set lead, dates, priority, and status only from supplied context or existing
project settings. Do not overwrite existing metadata merely to fit the format.

## Milestones

Create one milestone per agreed stage. Use the same names as other requested
artifacts. Dates are optional; never derive them from the stage number.

```text
Name: Stage [number] — [Outcome]

Description:
[What capability exists when this stage is complete.]

Complete when:
- [Observable demo, integration result, or validation condition]
```

## Workstream parent issues

Use one parent issue per workstream to group execution tasks. If the existing
project already has a grouping convention, reuse it rather than adding a
competing hierarchy. A parent spanning stages should not be forced into one
milestone; assign milestones to its execution tasks.

```text
Title: [Workstream name]

Description:
[One or two sentences describing responsibility and the expected handoff.]

Complete when:
- [Workstream outcome within the agreed project scope]
```

## Implementation subissues

Create tasks large enough to represent useful work and small enough to check
independently. Include design tasks for unresolved interfaces instead of
inventing implementation decisions. Include integration and validation tasks.

```text
Title: [Concrete action and object]

Description:
[What needs to change and why, in a short paragraph.]

Done when:
- [Observable completion condition]

Dependencies: [Only actual blockers; omit when none]

Parent: [Workstream issue]
Milestone: [Applicable stage]
Assignee: [Only when agreed]
```

Use native relationships for parents, milestones, and known blockers. Use
the project's existing workflow for new tasks and preserve states on updates.
Leave assignments and deadlines unset when unknown. Do not make later-stage
work appear ready to start when it depends on earlier tasks.

If Notion is also requested, keep its checklist at the workstream/outcome
level; Linear holds execution detail. Do not reproduce every issue and
status on the landing page. Verify relationships and check for duplicates
after publishing.
