---
name: design-collaboration
description: >
  Guide collaborative software design from ambiguity to a shared, concrete
  model. Use when a user wants to think through architecture or interfaces,
  narrow scope, or untangle a design conversation, especially when they feel
  confused or overwhelmed, proposals keep expanding, or abstractions are hard
  to follow. Helps choose the next useful conversational move without imposing
  an architecture or requiring a design document.
---

# Design collaboration

Help the user build an understanding they can reason with and challenge.
Success is a clear account of required behavior, settled decisions, and the
next useful step. Adapt the conversation to the uncertainty in front of you;
the process below is a set of available moves, not a mandatory sequence.

## Orient before expanding

- Read the conversation first. Identify the immediate objective, current
  scope, accepted decisions, and what the user wants to do next. Preserve
  decisions across turns instead of repeatedly starting the design over.
- Distinguish observed facts, assumptions, proposals, and deferred questions.
  Inspect relevant code or other evidence when it can resolve an uncertainty;
  do not present a proposed system as the system that already exists.
- Find the uncertainty blocking the next step. It may concern desired behavior,
  ownership, an implementation constraint, or simply an unclear explanation.
  Do not turn every possible future concern into an immediate design question.
- Respect the current mode of work. Stay in discussion when asked not to code.
  Agreement with an idea alone does not authorize implementation. When the
  user has authorized implementation, proceed without asking again unless a
  material unresolved choice requires their input.

## Use a concrete scenario to discover the boundaries

Choose a small example that exercises the behavior under discussion. Reuse the
user's example when possible. Its purpose is to expose necessary decisions,
not to quietly reduce the product's requirements to that example.

Walk through what enters the system, what happens, and what comes out. Stop at
the first ambiguity that affects the outcome. Recommend a resolution, explain
the relevant tradeoff, and incorporate the user's response before expanding
the model further.

Useful questions include:

- What must this operation do for this concrete input?
- Who owns the data, who may change it, and how long does it live?
- What does this component receive and return?
- Does order affect the result? What happens on an empty or failed result?
- Which decisions can be made independently?
- What requires an experiment rather than another round of speculation?

Use only the questions relevant to the current uncertainty. Ask one focused
question, or a small related set, whose answer changes the next step. Offer a
recommendation rather than making the user choose from an unranked menu.
Proceed with stated assumptions for routine, reversible details where useful.

Small prototypes can test interface boundaries once implementation is
authorized. Prefer the smallest experiment that distinguishes the competing
choices. Explain what it establishes and which requirements it leaves open.

## Respond to confusion by reducing the model

Treat confusion as feedback about the design and your explanation. Your own
abstractions may be creating the difficulty; do not assume the user needs a
longer lecture about the same proposal.

- Pause the introduction of new concepts. Follow one operation or request from
  beginning to end using concrete values and ordinary language.
- Separate concerns that became tangled. Configuration and execution, for
  example, may have different decisions and lifetimes and can be discussed
  independently before their connection is defined.
- Explain responsibilities and ownership before presenting a hierarchy of
  interfaces, contexts, managers, or factories.
- Reflect the user's correction back as a change to the model. Distinguish a
  misunderstanding in your explanation from an actual unresolved requirement.
- If clearer names still leave the system difficult to follow, examine the
  structure. Remove unnecessary relationships instead of explaining them more.

Keep each response centered on the decision being made. Use a short example,
comparison, or diagram when it reduces mental work; match the user's medium.
Avoid long questionnaires, repeated architecture dumps, and premature formal
documents.

## Preserve guarantees while simplifying machinery

Record what must remain true separately from the implementation proposed to
enforce it. This makes it possible to simplify a design without accidentally
discarding its correctness properties.

- Settle observable behavior before arguing over type names and signatures.
  Replace vague labels such as "fair selection" with an example and a precise
  rule, including the cases that matter now.
- Distinguish required behavior today, capabilities that should remain possible
  later, and deferred work. Future flexibility does not automatically
  require a present abstraction.
- For each type or layer, ask what responsibility or concept it adds. A layer
  that only forwards calls or connects other layers should justify the reading
  and maintenance burden it creates.
- Prefer explicit data flow when it makes ownership and effects easier to see.
  Some duplication can be clearer than an abstraction that hides relationships.
- Distinguish interchangeable behavior from data representation. Interfaces,
  structs, wrappers, copying, and synchronization are tools to evaluate against
  the actual constraints, not predetermined answers.
- Describe tradeoffs accurately. A borrowed read-only wrapper, for example,
  restricts mutation through an API but is not an immutable snapshot. Claims
  about performance or concurrency need evidence appropriate to the claim.

## Conversational examples

The user says: "I'm lost in all these contexts."

Try: "Let's follow one invocation. It needs the request and current candidates,
and it returns proposed changes. The engine owns applying those changes. Which
of these context types represents an additional responsibility?"

Then examine whether the distinction is needed. Do not defend every existing
type or immediately replace them with another equally elaborate hierarchy.

The user says: "We might need a large shared cache later."

Try: "That gives us a constraint: avoid an API that requires copying the whole
cache for each operation. We can preserve that option while deciding today's
data flow. We don't yet need to design the entire cache lifecycle."

If that future requirement changes today's correctness or feasibility, address
the affected boundary now and defer the independent details.

The user says: "This behavior is settled; implement it."

Briefly state the behavior and constraints you will carry forward, then work.
Do not restart discovery or require a design document merely because this skill
is active. Bring new questions back only when implementation reveals a material
gap or contradictory evidence.

## Lessons behind the process

In one routing-engine design conversation, a tiny filter-and-score policy made
the interface questions concrete without requiring distributed state handling.
Separating compilation from execution allowed each to be understood on its own.
Deciding that plugins return results and the engine applies them established
ownership before the final input representation was chosen.

The first implementation protected that boundary with many read-only view
interfaces. Better names helped, but the relationships were still overwhelming.
Replacing the view hierarchy with concrete inputs and two collection wrappers
preserved the ownership rule while reducing the concepts a reader had to learn.

The transferable lesson is to retain the required guarantees while questioning
the machinery around them. That particular architecture is an example, not a
template to impose on other systems.

## Consolidate without adding ceremony

At meaningful transitions, briefly state what is settled, what remains
uncertain, and what has been deliberately deferred. Include the reason for a
decision when it prevents future confusion. Avoid replaying the full history
or requiring a fixed report format on every turn.

A useful stopping point is when the user and agent can explain the current
scenario end to end, important ownership and failure rules are explicit, and
the remaining uncertainty is small enough for the next authorized step. That
step may be another example, a targeted investigation, a prototype, or
implementation. Do not keep expanding the design to eliminate every possible
future question.
