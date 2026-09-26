---
name: project-landing-page
description: >
  Create or revise a project landing page that makes the path to shipping easy
  to see. Use for project kickoff docs, workstream trackers, delivery dashboards,
  or plans that need ship gates, parallel work, integration points, deadlines,
  and validation evidence. Works in Notion, Markdown, or another document tool.
---

# Project landing page

Create a page someone can scan to answer: What must be true to ship? What can
happen in parallel? Where does the work join? What evidence supports the date
and the final decision?

## Build the model first

- Read the conversation and any supplied project page, design, issues, or code.
  Preserve existing decisions and distinguish completed work from proposed work.
- Name the first shippable outcome. Separate required behavior from later
  extensions. If the scope is uncertain, show the decision rather than silently
  choosing it.
- Map work as independent paths and the points where they join. Put parallel
  paths at the same level. Within a path, order dependent steps in execution
  order. A larger effort gets a parent item with short child tasks.
- Identify the proof for each major outcome: a test, demo, integration run,
  dashboard, experiment, or review. Include validation work from the start.
- Keep the deadline and the current forecast distinct. Derive the forecast from
  remaining dependencies and evidence; do not infer it from checkbox counts.

## Shape the page

Adapt this structure to the project's size and the user's preferred format:

```text
Goal and first ship scope
Target date and current forecast

Ship gates
  Short, observable outcomes with checkboxes

Checkpoints
  A few dated or timeboxed proofs, including integration and validation

Integration path
  Build in parallel
    Workstream A
      Steps in order
    Workstream B
      Steps in order
    Validation
      Steps in order
  Then join
    Integration steps in order
    Final comparison and ship decision

Open decisions
Later work
Completed foundations and source docs, if useful
```

The ship gates are the front door. Keep them few enough to scan. Each gate
states a result visible outside its implementation, such as "A configured
policy routes a live request." The integration path holds the engineering
steps needed to reach those results. Avoid duplicating a full issue list.

## Write checkboxes that can be used

- Use short, concrete labels. A reader should understand each item without
  opening another page. Put necessary detail in a child item, not a long parent.
- Make each item independently checkable. Prefer "Rebuild per-target state after
  reconnect" to "Handle state and all edge cases."
- Show a dependency by nesting or ordering tasks; do not place a dependent step
  beside work that can proceed in parallel.
- Check off an outcome only when its proof exists. Add the proof link or result
  next to the item when available. A merged change alone may leave a live or
  performance gate open.
- Keep completed foundations accessible but visually quiet. Separate deferred
  work from the path to the first ship.

## Make validation part of the deliverable

For projects that claim performance or quality improvements, plan for three
forms of evidence:

- **Operational view:** Show input/data health, decisions, outcomes, fallbacks,
  and the cost of making each decision.
- **Controlled comparison:** Fix the workload, environment, success limits, and
  measurement rules before comparing a baseline with the new behavior. Include
  failures, unfinished work, request classes, and repeated runs as appropriate.
- **Final explanation:** Show where the new behavior wins, loses, and falls
  back, with the limits of the evidence stated plainly.

Choose the visualization tool that fits the environment. AI can help draft
charts and surface anomalies, but retain the queries, data or run IDs,
filtering rules, and denominators so readers can reproduce the result.

## Publish and maintain

- Use the destination the user chose. If asked for an outline, provide an
  outline; publish only when asked. If asked for a new version, leave the old
  page intact. Inspect an existing destination before editing it.
- Link to task trackers and designs when useful, but make the landing page
  understandable on its own. Do not create issues or duplicate task statuses
  unless requested.
- At each update, mark proven outcomes, identify the next integration proof,
  revise the forecast, and surface decisions or blockers that changed it.
- Return a link or path to the page and briefly state what changed and what
  remains uncertain.
