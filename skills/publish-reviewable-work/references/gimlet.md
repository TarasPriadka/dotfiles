# Gimlet integration

These notes connect the workflow to Gimlet's existing skills. Read current
`AGENTS.md` and the named skills before executing; they remain the authorities
for repository mechanics. Do not edit the vendored `gh-stack` skill to add
personal policy.

- **`create-pr`:** use its extraction, validation, signing, and PR-body rules.
  Namespaced branches, draft PRs, exact-file staging, and signed commits apply.
  Validate the body with the repository's description rules. Run required lint
  and relevant generation on each extracted branch, not over unrelated work in
  the source checkout. Its extraction starting point assumes the user identifies
  a piece; this workflow supplies that piece from the agreed decomposition.
  Its standalone `main`-based instructions apply to roots; for a dependent unit,
  use the actual parent and the stack-specific procedure. Preserve exact-file
  staging required by `AGENTS.md` even where a helper skill permits `git add -u`.
- **`gh-stack`:** use it for dependent branch chains and keep commands
  noninteractive. Its introductory examples are not decomposition policy: tests
  belong with the behavior they establish, and independent changes need not be
  stacked. A shared prerequisite can also create topology beyond a single chain;
  do not duplicate membership across stacks without checking tool support.
- **PR metadata:** the inspected `gh stack submit --auto` creates draft PRs
  with generated metadata and does not expose custom title/body flags. Recheck
  installed help. Prefer preparing compliant titles and bodies before creation
  and creating drafts with explicit bases through `gh pr create`, then using
  `gh stack link` with the existing PR URLs in dependency order for real chains.
  Verify the remote bases afterward. If generated
  metadata must be corrected, announce the replacement before doing it and obtain
  any agreement required by `AGENTS.md`; never silently overwrite an author's
  existing title or body.
- **`pr-overview`:** retain its source-backed model, compact structural visual,
  and revision-specific comment handling. This publication workflow explicitly
  includes posting the overview, so its direct-publication path applies without
  a separate preview approval for each PR. Design-only invocation still publishes
  nothing. Its explanation is not a correctness approval.
- **`create-pr` next-step reminder:** when the user requests publication through
  this workflow, the overview is already part of the work. Do not finish by merely
  offering to run it later. The separate `@claude review` comment requests the
  user's chosen external bot; it does not invoke `gml-review` or grant approval.
- **`merge-gh-stack`:** consult it when planning the landing cost and when merging
  is authorized. Gimlet's checked-in base check requires `main`; upper stacked
  PRs can be reviewable while blocked from merging. Its squash/queue workflow
  requires revalidating the newly exposed child comparison after a parent lands.
  Recheck current rules when executing. Avoid enabling blanket auto-merge on
  topic-branch bases.

The local workflow files inspected during design do not establish how the Claude
bot is installed. Post the requested trigger when publication is authorized,
then check for an acknowledgment or run. A successful comment write establishes
that review was requested, not that the bot accepted or completed it.
