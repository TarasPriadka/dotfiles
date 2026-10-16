# Architecture overview template

Fill the skeleton below from the supplied context. Keep sections short;
this is a shared architectural model, not a complete implementation spec.
Use TBD or open questions for unresolved details. Do not invent alternatives
or claim a review took place. Remove bracketed writing instructions.

The overview must explain the entire input-to-output path, including the
response for a request-serving system. Show which component owns each step.
Use one simple architecture diagram and a sequence or timeline only when
it adds clarity. Use the destination's native diagram support where possible.

```markdown
# [Architecture title]

Author(s): [Known authors or TBD]
Date Created: [Actual document creation date]
Status: Draft

## Problem Statement

[The current limitation and why it matters, in a few sentences.]

## Goals

- [Observable outcome]

## Non-Goals

- [Explicit exclusion or deferred capability]

## Background

[Only the existing system context needed to understand this change.]

## Proposed Design

### Overview

[The central change and responsibilities of the main components.]

### Architecture

[Simple diagram of components and their interactions.]

#### Lifecycle

[Who creates, configures, discovers, updates, and removes the components,
as applicable. State readiness expectations without inventing protocols.]

#### End-to-end flow

1. [Input enters the system.]
2. [Components perform the work and hand off results.]
3. [Output or response reaches its consumer.]

### Interfaces & APIs

- [Producer → consumer: information passed and responsibility boundary]

### Invariants & Assumptions

- [Ordering, compatibility, ownership, or consistency guarantee]

### Performance Impact

[Relevant latency or throughput expectations, their reasoning, and what
must be measured. Omit this subsection when it adds no useful information.]

## Security & Privacy Considerations

[Changes to data handling, access, or trust boundaries; unresolved review
questions remain explicit.]

## Alternatives Considered

[Actual alternatives discussed and the relevant tradeoffs, or TBD.]

## Failure Modes

- [Failure → expected behavior or recovery; identify unresolved behavior]

## Validation and Testing Plan

- [Observable check proving the initial integrated outcome]
- [Important failure or correctness check]

## Implementation Strategy

- Stage 0: [First integrated outcome]
- Stage 1: [Core completion]
- Stage 2: [Deferred extensions]

## Open Questions

- [Unresolved decision, with an owner only when agreed]

## Components Affected

| Component | Change | Approvers | Approved |
| --- | --- | --- | --- |
| [Component] | [Responsibility or behavior change] | TBD | No |

## Author Checklist

- [ ] I discussed the design with another engineer.
- [ ] I considered alternatives and major failure modes.
- [ ] I identified the appropriate approvers.
- [ ] I read the complete document before requesting review.
- [ ] The design is ready for the proposed implementation stage.

## Approver Checklist

Approver: [TBD; repeat for each approver]

- [ ] I understand the motivation, scope, and proposed design.
- [ ] The component boundaries and tradeoffs are reasonable.
- [ ] Major failures and security implications have been considered.
- [ ] The validation plan supports the intended outcome.
- [ ] I am comfortable proceeding with the proposed implementation stage.
```

Keep checklists unchecked unless the user provides evidence of completion.
An architectural direction can be agreed while detailed interfaces remain
open. Distinguish those states rather than presenting the whole design as
approved or requiring every implementation question to be settled.
