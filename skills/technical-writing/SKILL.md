---
name: technical-writing
description: >
  Write and revise technical explanations, design documents, team updates,
  experiment reports, and engineering feedback for human readers. Use when
  drafting technical communication or making it clearer, easier to follow,
  more natural, or less LLM-like. Teaches writing judgment and a deliberate
  self-editing pass while adapting structure to the audience and purpose.
---

# Technical writing

Reader comprehension is costly. Spend effort resolving meaning and relationships
so the reader does not have to reconstruct them. Effective writing lets its
intended reader understand the point, follow the explanation, and use it to
reason or act. A short passage that is hard to follow has missed the goal.

Infer the audience, purpose, and medium from the request and available context.
Honor the user's chosen format and voice. Ask only when a missing detail would
materially change the writing. This skill supplies quality standards, not a
document outline: choose structure, length, tone, and supporting material for
the task. It can complement a task-specific skill without replacing that skill's
format or workflow. A narrow edit should remain narrow.

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

## Give the draft a second read

After drafting, deliberately reread from the intended reader's perspective.
Assess what the words actually communicate using the background that reader can
reasonably have. Do not mentally fill gaps with knowledge from the investigation.
For a short edit, keep this pass proportionate to the changed passage and its
context. Perform this check yourself; do not invoke a shadow reader or a separate
agent as part of this skill.

- **Purpose:** Can the reader tell what this writing explains, proposes, or asks?
- **Context:** Is necessary background present? Does a passage assume knowledge
  available only in the conversation or investigation?
- **Connections:** Can the reader follow the reasoning? Is a causal step,
  dependency, or consequence missing?
- **Concrete meaning:** Is it clear what happens, who does it, and why it matters?
  Would a specific action or example resolve an abstraction?
- **Terminology:** Are unfamiliar terms introduced when needed, names consistent,
  and references such as "this" or "it" unambiguous?
- **Interpretation:** Are quantities, units, comparisons, and relevant conditions
  clear where they appear?
- **Accuracy:** Does the wording preserve evidence, uncertainty, scope, and the
  author's position? Did simplification strengthen a claim?
- **Effort:** Where must the reader reread, jump backward, or keep too much context
  in memory? Would reordering or supplying a connection help?
- **Relevance:** Does each detail help understanding or action? Is anything
  repeated, distracting, or included only to describe the writer's process?
- **Naturalness:** Does the language explain something specific? Which phrases
  add ceremony or emphasis without meaning?

Revise the passages that fail this check. Missing context may need a sentence;
a tangled explanation may need reordering or a concrete example; an unsupported
claim needs verification or qualification. Replace low-value detail with missing
connections instead of automatically appending more explanation. After a
substantial revision, reread the affected passage in context to check that the
fix preserves meaning and flow.

Keep the checklist and editing process internal. Deliver the improved writing
in the requested form, with any material uncertainty the reader needs. Do not
append a self-assessment, claim a reader test was passed, or add sections merely
to demonstrate compliance with this skill.
