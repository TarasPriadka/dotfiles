# PR overview examples

These examples show how to explain structure and scope. They are hypothetical.
Use links to inspected code in real overviews; never invent destinations.
Each delivered overview starts with `## Agentic Overview`.

## Configuration preparing later work

The worker currently assembles retry behavior in code. This PR adds a schema
for describing it; the worker does not consume the new schema yet.

```text
RetryPolicy                         [new configuration]
├── Rules for upload                [example]
│   ├── Transient failure → retry
│   └── Delay: exponential backoff
└── Attempt limit: 3

Worker retry loop                   [existing execution]
  Still uses its built-in policy; reading RetryPolicy is later work.
```

Link the schema and the current consumer. The tree shows containment and the
unconnected runtime boundary. Generated bindings make a message available to
callers but do not alone change behavior.

## Small ordering change

Cancellation can now find requests after dispatch and before their response.
Previously, dispatch removed them from `pending_requests`.

- Before: register request → dispatch and remove → receive response.
- After: register request → dispatch → receive response and remove.

Link the changed removal point and the response path. This is enough for a small
change when no important boundary needs more explanation.

## Handoff across components

Suppose a request moves through a gateway, a queue, and a worker. The change
moves removal of its tracking record from queue admission to worker completion.

```text
G Gateway ──request r7──→ Q Queue ──accepted r7──→ W Worker
G Gateway ←─completion reply─ Q Queue ←─done event───── W Worker
G Gateway ←─admission error── Q Queue
```

The labels identify the same components in the trace: start with `r7` tracked
by G. Q accepts it and W receives it; G keeps the record until the completion
event returns. When G replies, the record is removed. If Q rejects admission,
the outcome depends on the inspected error path; do not infer cleanup from the
successful completion path. In a real overview, link the admission, completion,
and rejection code that establishes these transitions. Use this much detail
only when the boundary and return path matter to the change.

## Contract change with an unknown

The receiver now distinguishes an absent timeout from an explicit zero timeout.
Previously, both selected the default.

```text
ResolveTimeout(request)
├── Timeout omitted  → use default          [unchanged]
├── Timeout is zero  → return immediately   [changed]
└── Timeout positive → use supplied timeout [unchanged]
```

Link the interpretation and the caller that now omits the field when it wants
the default. If older senders might explicitly transmit zero, state the
conditional consequence and whether that sender behavior was verified. A test
of the receiver establishes its new interpretation, not compatibility with
senders that were not inspected.
