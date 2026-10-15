---
name: technical-writing
description: >
  Write and revise technical explanations, design documents, team updates,
  experiment reports, engineering feedback, and agent handoffs. Use when
  drafting technical communication or making it clearer, easier to follow,
  more natural, or less LLM-like. Develop the material broadly, then compose
  and critique an explanation for the recipient's purpose and background.
---

# Technical writing

The writer's understanding and the reader's explanation are different products.
Develop enough understanding to reason correctly, then select and sequence what
the recipient needs to understand, decide, or act. Optimize for useful
understanding per unit of reader effort. Dense shorthand may save tokens while
making the explanation harder to follow.

Infer the audience, purpose, and medium from the request and available context.
Honor the user's chosen format and voice. Ask only when a missing detail would
materially change the writing. This skill supplies writing judgment, not a
document outline. It complements task-specific skills without replacing their
format or workflow. A narrow edit should remain narrow.

## Develop the material, then compose for the reader

For substantial writing, separate two kinds of work:

1. **Develop the material.** Use an expansive working draft to establish the
   relevant facts, mechanisms, dependencies, examples, alternatives, and
   uncertainties. Writing exposes missing connections; resolve consequential
   gaps from evidence or leave them explicit. Stay within the task's scope.
   Breadth is useful when it develops understanding, not when it inventories
   everything related to the topic.
2. **Compose for the recipient.** Treat the working draft as source material.
   Choose the central explanation and rebuild it in the order the reader needs.
   Assume the reader has the appropriate background but does not share your
   investigation history or implicit definitions. Retain what supports their
   understanding or action. Be strict about removing repetition, detours, and
   details that helped you learn but do not help them. Change the structure or
   representation when needed, rather than merely shortening sentences.

Preserve the reasoning, evidence, conditions, and uncertainty needed to assess
the conclusion. A concrete example or an extra sentence explaining a dependency
can be more useful than a shorter, denser claim. Do not replace omitted context
with a conclusion the reader must accept on trust.

Scale the process to the task; a sentence edit needs no elaborate first draft.
Keep working drafts internal unless the user requests them. This process does
not require separate files, extra agents, or an intermediate approval step.

Apply the same judgment to agent handoffs. Give the recipient its objective,
relevant findings and evidence, constraints, unresolved questions, and locations
for further inspection. Preserve reasons behind consequential decisions; omit
the exploration log unless it affects the next action. Do not assume another
agent shares your context or make the handoff cryptic to save tokens.

## What effective writing does

### Explains relationships

Facts form an explanation when the reader understands how they connect. Make
important causes, dependencies, ownership, and consequences explicit. Explain
what happens and why before relying on names for components or abstractions.
Use consistent names once introduced. Choose an order that lets each passage
build on what the reader already understands; discovery order rarely serves
that purpose.

If you cannot explain a transition, resolve the gap in your understanding or
state the uncertainty. Smooth prose must not hide missing evidence. Consult
sources when needed to support a consequential claim, within the task's scope.
Collecting more material is useful only when it resolves a relevant question.

### Supplies context where it is needed

Assume the reader has the background appropriate to the audience, but has not
followed the investigation or conversation. Supply the missing context without
reteaching what they already know. Introduce unfamiliar concepts when they
become necessary. Avoid forcing readers to remember a distant definition to
interpret the current sentence.

Make quantities and comparisons interpretable: what was measured, against what,
under which relevant conditions, and in what units. Tables should carry the
labels and units needed to read them. Links should help readers inspect evidence
or learn more; the main explanation should remain understandable without opening
every link.

### Chooses detail for the reader

Include details that help the reader understand behavior, assess a claim, or
take the intended action. Preserve an explanation that makes a difficult idea
clear even when it adds words. Remove inventories, repeated conclusions, and
investigation history when they do not serve the reader's purpose.

Use examples, tables, diagrams, or code when they make a relationship easier to
understand. Choose the form that suits the information and the medium; none is
mandatory. Keep interpretation close to the evidence it explains. Separate
supporting detail when that improves the main message without hiding a material
qualification.

### Preserves meaning and judgment

Keep the author's position, degree of confidence, and intended request intact.
Do not quietly turn a suggestion into a commitment, a preference into a
requirement, or an observation about someone's work into a judgment about their
character. Improving persuasiveness means clarifying the reasoning and evidence.

Distinguish observed results, implemented behavior, proposals, and hypotheses
when the distinction matters. Keep conditions that change the conclusion. Check
whether words such as "always," "only," "prevents," or "unchanged" overstate the
evidence. If a draft has a substantive factual or logical problem, resolve it
from available sources or flag it rather than merely making it sound convincing.

### Sounds like someone explaining something specific

Use familiar words, concrete verbs, and identifiable actors. Technical terms are
useful when they convey a precise idea the reader understands. Avoid stacking
abstract nouns or introducing labels that require more explanation than the
behavior itself.

Keep the author's natural voice while improving clarity. Remove ceremonial
openings, inflated adjectives, canned transitions, repeated summaries, excessive
emphasis, and contrasts with alternatives nobody raised. Do not manufacture
informality, typos, or personal anecdotes to sound human. Naturalness follows
from having something specific to say and saying it directly.

## Examples of the judgment

These examples illustrate editing choices, not facts to reuse in another task.

**Make the dependency visible.**

> Tokenization moves before routing to support stateful routing.

> The router needs token IDs to compare a request with the model's cached pages.
> We therefore need to tokenize the request before choosing a worker.

The revision explains why the order matters. It replaces a circular justification
with a concrete dependency.

**Rebuild the explanation around the reader's task.**

Suppose a working draft has established these facts:

> There is a tokenizer service. The API receives text. A worker processes the
> request after the router selects it. We considered two tokenizer placements.
> Cached pages are compared using token IDs. Tokenization therefore has to
> finish before routing. Remote tokenization adds a call before selection.

For a reader trying to understand the proposed request flow:

```text
Text request
  → tokenizer returns token IDs
  → router compares those IDs with cached pages and selects a worker
  → selected worker processes the request
```

The tokenizer call must finish before worker selection, so its latency is part
of the time spent before routing.

The revision organizes the facts around execution and retains the consequential
latency dependency. The placement discussion can be omitted for this reader;
for a reader choosing a placement, the alternatives and tradeoff would matter.
This changes the explanation's structure rather than polishing the inventory.

**Translate a metric into its practical meaning.**

> The throughput benefit was primarily latency-target goodput.

> The policy completed roughly the same number of requests per second, but more
> requests received their first token within the latency target.

The revision is longer but requires less background. A report for readers already
familiar with the metric may use its technical name, with the target stated.

**Make an abstract benefit precise.**

> The service provides independent scalability and fault isolation.

> We can add tokenizer workers without adding router replicas. A tokenizer crash
> would fail requests using that worker, but leave the router process running.

The revision describes the benefit and its boundary. It does not imply that
isolating a process prevents request failures.

## Critique the reader-facing draft

Read the composed explanation using only the background its recipient can
reasonably have. Do not mentally fill gaps from the investigation. Perform this
check yourself; do not invoke a shadow reader or a separate agent.

- **Purpose and path:** Can the reader identify the point and follow the steps
  or reasoning to the result? Are concepts introduced when they become useful?
- **Concrete meaning:** Is it clear what happens, who does it, and why? Are
  unfamiliar terms explained and quantities given context, units, and a basis
  for comparison?
- **Fidelity:** Did selection or compression change the author's intent,
  confidence, scope, or a condition that affects the conclusion? Are evidence
  and uncertainty still distinguishable?
- **Reader effort:** Where must the reader reconstruct a relationship, jump
  backward, or hold too much context? Would an example, reordering, or a different
  representation help more than another paragraph?
- **Value:** Does each detail support understanding or action? Remove repetition,
  ceremony, and investigation history that does not serve that purpose.

Rewrite passages that fail. A draft with the wrong organizing idea may need
recomposition, not sentence polishing. After a substantial revision, check the
affected explanation again for clarity and fidelity. Keep the critique internal;
deliver the requested writing and material uncertainties, without a
self-assessment or a claim that a reader test was passed.
