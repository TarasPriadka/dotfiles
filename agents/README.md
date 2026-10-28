# Personal agent framework

The default guide establishes ownership and collaboration expectations. The
engineering-work skill organizes substantive work and selects supporting skills.
A compact work record carries the current model across sessions when useful.
Ask for an outcome normally; you do not need to assemble the skills yourself.
The engineering method now provides an advisory graph of activities and evidence
for moving between them, with direct entry for settled work and return paths when
an assumption fails. [Steering guidance](../skills/engineering-work/references/steering.md)
helps choose the next bounded commitment and prepare consequential user decisions.
Small tasks need no stage ceremony. These are experimental working instructions,
not a background scheduler or a demonstrated improvement in agent quality.

## Install the defaults

```sh
curl -fsSL https://raw.githubusercontent.com/TarasPriadka/dotfiles/main/skills/install.sh | bash
```

The normal dotfiles setup runs this command already. Existing installations should
rerun it once to upgrade the old skills-only updater. It installs the update helper
and hourly user timer, then downloads the guide and skills as one release.
No source checkout or Python package installation is needed for this path.

- `~/.codex/AGENTS.md` resolves through the managed release's `AGENTS.md`.
- `~/.agents/skills/<name>` resolves through the same release for managed skills.
- A single cache pointer selects the guide and skill versions on subsequent updates.

The installer migrates the original pilot links under `~/code/dotfiles` together.
Unrelated guide files, overrides, and conflicting core skills stop the update before
the active release advances. Other custom skills remain in place. Download failures
and incomplete releases preserve the previous installation. The updater serializes
manual and timer runs.

Use `DOTFILES_CODEX_HOME=/absolute/path` on installation to select a custom Codex
directory; the location is retained for future timer runs. On first normal install,
`CODEX_HOME` is honored if there is no saved location. `DOTFILES_SKILLS_HOME` is a
test-home override; it does not redirect a normally launched Codex session.

Start a fresh Codex session in your project. To check discovery without confusing
file availability with actual loading, ask:

> Without reading files, identify the personal working guide already supplied in
> your initial instructions and explain how it treats a small question versus a
> multi-step implementation.

For real work, describe the desired result and constraints. The guide is headed
“Working with Taras.” Project-specific instructions continue to apply.

## Architecture and extension

[AGENTS.md](AGENTS.md) contains default expectations: ownership, understandable
decisions, appropriate initiative, and economical effort.
[engineering-work](../skills/engineering-work/SKILL.md) connects the relevant
activities and existing specialist capabilities.
[Work-record guidance](../skills/engineering-work/references/work-record.md)
preserves the task's purpose, facts, decisions, evidence, and continuation.

Improve the default guide for expectations that apply to every task. Improve the
working method for missing transitions between activities. Add a specialist skill
for a distinct reusable capability. Keep project commands and conventions in the
project rather than the personal core.

Each capability should make its triggering situation, required context, owned
responsibility, result, evidence limits, and authorization boundaries understandable.
Use standard skill descriptions for discovery. Link a capability from the working
method when a recurring activity needs the connection. Avoid circular dependencies,
duplicated ownership instructions, or restarting an investigation already completed
for the same task. Evaluate it with a realistic request that does not name the skill.

## Develop and test locally

`python3 agents/install.py --home /tmp/<test-home>` installs guide/workflow links
from this checkout into an isolated filesystem test home. The local development
installer preserves conflicts and removes only its own links with `--uninstall`.
It deliberately does not replace a managed installation. Normal installation and
updates use `skills/install.sh` instead.

Run the filesystem and publication-path tests:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s agents/tests -v
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/tests -v
```

The updater tests use local archives and disposable homes, including a complete
installer bootstrap followed by an update. They do not contact GitHub or modify
the real user's configuration. Use the skill-creator structural validator for
changed skills when available.

[Evaluation scenarios](evals/README.md) exercise automatic selection, design-only
scope, and fresh-session continuation with a disposable fixture. Inspect artifacts
and tool evidence as well as test results. Record instruction versions, model,
observable cost, and user interventions; keep raw session logs local.
Classify gaps as selection, method execution, or coordination. A bounded functional
trial establishes feasibility, not a general improvement in reliability.

The standalone `agent-workflow` repository contains the frozen baseline, process-only
and process-plus-steering variants, and comparison tooling under `evals/`. Dotfiles
distributes the candidate guidance; keep the experiment runner and its baseline in
that repository. Record exact guidance hashes when comparing trials, since the
hourly updater can change the active release.
