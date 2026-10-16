# Notion landing page template

Use this structure for the landing page. Repeat the workstream section as
needed. In Notion, put each workstream's TODOs inside a native toggle; in
Markdown, use a TODO heading. Do not copy these instructions into the page.

Keep stage summaries about outcomes and workstream TODOs about the work.
Omit empty stage groups and the open-decisions section when unnecessary.
Include owners or dates only when known and useful. Add links to other
artifacts only when requested; the page must stand on its own.

```markdown
# [Project name]

[One or two sentences explaining what we are building and why.]

## Stages

### Stage 0 — [First integrated outcome]

[Smallest real end-to-end capability, its bounded scope, and the demo or
test that establishes it works.]

### Stage 1 — [Complete the core support]

[Capabilities to flesh out after initial integration and the completion
condition for this stage.]

### Stage 2 — [Extensions]

[Explicitly postponed capabilities.]

## [Workstream name]

[One or two sentences describing this part's responsibility and handoff.]

### TODOs

Stage 0
- [ ] [Concrete task]
- [ ] [Integration or validation task]

Stage 1
- [ ] [Concrete task]

Stage 2
- [ ] [Deferred task]

## Open decisions

- [Question that affects scope, ownership, or coordination]
```

Repeat workstreams at the same heading level. Order dependent TODOs and
name cross-workstream dependencies in plain language. Avoid a separate
integration checklist that repeats the same tasks. Keep completed items
accessible but visually quiet.
