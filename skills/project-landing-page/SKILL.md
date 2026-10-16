---
name: project-landing-page
description: >
  Set up a project using self-contained templates for a Notion landing page,
  an architecture overview, and a Linear project with milestones and tasks.
  Use for project launches, staged workstream plans, or creating or revising
  any of these artifacts independently. Also supports Markdown drafts.
---

# Project setup

Make the project's outcome, stages, and parallel work easy to understand.
Use the bundled templates as the default format; fill them with the user's
project context. Keep descriptions short and leave detailed design to the
people doing the work.

## Choose the requested output

| Request | Template |
| --- | --- |
| Landing page or workstream tracker | [Notion landing page](templates/notion-landing-page.md) |
| Architecture or design overview | [Architecture](templates/architecture.md) |
| Linear project, milestones, or issues | [Linear project](templates/linear-project.md) |
| Full project setup | All three, unless the user narrows the scope |

Read only the templates needed for the request. Each works independently;
do not create companion documents or issues merely to fill a template.
For a full setup, establish the stages and workstreams first, then use the
same names and scope across artifacts. Publish only the outputs authorized
by the user. A request for advice or a draft does not authorize publication.

## Use supplied context

- Start with the conversation. Preserve agreed decisions, exclusions, and
  completed work. Distinguish proposals from settled behavior.
- This skill supplies the format. Do not search for external examples,
  templates, documents, or code unless the user supplies or requests them.
  User-provided formats take precedence over the bundled defaults.
- Inspect an existing destination before editing to preserve human changes
  and avoid duplicate pages, milestones, or issues. Reading the destination
  and tool usage instructions is not a request for broader research.
- Omit reference sections and document links unless the user wants them.
  No artifact requires a proposal, repository, or companion page to exist.
- Ask for missing information only when it materially affects the next step.
  Leave unresolved designs open; do not invent owners, dates, approvals,
  performance numbers, or project status to fill placeholders.

## Establish stages and workstreams

- Stages describe priority and increasing capability. Workstreams describe
  responsibilities that people can develop in parallel.
- Stage 0 is a narrow but real end-to-end integration. Reduce supported
  inputs or cases before bypassing essential components. Include the output
  or response path. An integration milestone need not be release-ready.
- Stage 1 fills out the core support. Stage 2 identifies postponed extensions.
  Adjust the number or names of stages when the project calls for it.
- Give each stage an observable completion condition, such as a live demo or
  integration test. Put the work to reach it in workstream TODOs.
- Make dependencies and integration points explicit. Independent workstreams
  belong at the same level; dependent tasks are ordered within them.
- Keep the tracker within the landing page by default. A separate tracker
  should solve a concrete size or workflow problem, not duplicate the page.
- Identify parallel work without assigning people unless assignments are
  agreed. Keep target dates and forecasts distinct when either is included.

## Fill the templates plainly

- Use short sentences and concrete verbs. Explain what changes and why.
  Avoid management vocabulary when a direct task description will do.
- Give each workstream a short summary and independently checkable TODOs.
  Prefer "Return text through the public API" to "Complete integration."
- Keep architecture at the level of responsibilities, lifecycle, interfaces,
  and guarantees. Protocol details can remain open for workstream design.
- Use a simple diagram when it clarifies relationships or ordering. A small
  timeline can explain overlapping work; label illustrative numbers clearly.
- Match validation to the claim. A few end-to-end checks may suffice; a
  performance claim also needs a baseline and representative measurements.
  Distinguish expected behavior from measured results.
- Check an item only when its outcome is supported by evidence. A merged
  change alone does not prove live integration or performance.
- Remove template instructions and unused optional sections from the output.
  Keep unresolved architectural questions explicit rather than filling space.

## Publish and maintain

- Use the chosen destination and preserve unrelated content, native child
  pages, and human edits. Prefer targeted updates over full-page replacement.
- For authorized Linear setup, derive issues from the agreed stages and
  workstreams. Reuse existing issues; do not create a second tracking scheme.
- When both Notion and Linear are used, keep Notion at workstream/outcome
  level and Linear at execution-task level. Do not mirror every issue status.
- Verify the saved structure after a substantial edit, including checkboxes,
  nesting, diagrams, and any milestone or issue relationships.
- Return the artifact links or paths and briefly state what changed and what
  remains unresolved. Do not expand the project to fill the template.
