# CLI-Anything

- Repo: HKUDS/CLI-Anything
- URL: https://github.com/HKUDS/CLI-Anything
- Date: 2026-05-19
- Repo snapshot studied: main @ `a32f11fc67052ff233dfaa5106de5bb1ccdf24ec`
- Why picked today: It is one of GitHub's hottest repos today, it is AI-agent infrastructure rather than another model wrapper, and it has enough concrete machinery to reward source study.

## Executive summary
CLI-Anything is trying to standardize a very specific pattern: turn GUI apps, web services, and oddball tools into stateful CLIs that AI coding agents can actually drive. The repo is not one product. It is a factory plus a registry plus a growing pile of per-app harnesses.

The smart part is the decomposition. Instead of building one giant universal agent layer, they define a repeatable harness recipe in [`cli-anything-plugin/HARNESS.md`](https://github.com/HKUDS/CLI-Anything/blob/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/cli-anything-plugin/HARNESS.md), generate agent-facing docs via [`cli-anything-plugin/skill_generator.py`](https://github.com/HKUDS/CLI-Anything/blob/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/cli-anything-plugin/skill_generator.py), publish install metadata in [`registry.json`](https://github.com/HKUDS/CLI-Anything/blob/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/registry.json) and [`public_registry.json`](https://github.com/HKUDS/CLI-Anything/blob/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/public_registry.json), and expose discovery and install through [`cli-hub/`](https://github.com/HKUDS/CLI-Anything/tree/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/cli-hub).

The weakness is also obvious: the repo scales by multiplying harness directories. That makes the project impressive as a pattern library, but harder to keep coherent, secure, and deeply tested as the count grows.

## What they built
They built four things at once:

1. a **harness-generation playbook** for converting software into agent-usable CLIs, centered on [`cli-anything-plugin/HARNESS.md`](https://github.com/HKUDS/CLI-Anything/blob/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/cli-anything-plugin/HARNESS.md)
2. a **distribution/catalog layer** for those harnesses, centered on [`cli-hub/`](https://github.com/HKUDS/CLI-Anything/tree/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/cli-hub), [`registry.json`](https://github.com/HKUDS/CLI-Anything/blob/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/registry.json), and [`public_registry.json`](https://github.com/HKUDS/CLI-Anything/blob/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/public_registry.json)
3. a **plugin/skill layer** so agents like Claude Code, Codex, Pi, OpenClaw, and others can discover and use the CLIs, via [`cli-anything-plugin/`](https://github.com/HKUDS/CLI-Anything/tree/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/cli-anything-plugin), [`codex-skill/`](https://github.com/HKUDS/CLI-Anything/tree/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/codex-skill), [`opencode-commands/`](https://github.com/HKUDS/CLI-Anything/tree/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/opencode-commands), and the canonical [`skills/`](https://github.com/HKUDS/CLI-Anything/tree/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/skills) tree
4. a **large library of concrete harnesses** such as [`gimp/agent-harness/`](https://github.com/HKUDS/CLI-Anything/tree/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/gimp/agent-harness), [`blender/agent-harness/`](https://github.com/HKUDS/CLI-Anything/tree/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/blender/agent-harness), [`browser/agent-harness/`](https://github.com/HKUDS/CLI-Anything/tree/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/browser/agent-harness), and dozens more top-level app folders

## Why it matters
If you buy the premise that future agents need to operate existing software, then this is a useful middle path between brittle GUI automation and full bespoke API integrations.

Instead of saying "teach the model to click better," they say "wrap the software in a stable textual control surface with JSON output, state, undo/redo, and a skill file." That is a much more practical systems instinct.

## Repo shape at a glance
Top-level shape:

- [`README.md`](https://github.com/HKUDS/CLI-Anything/blob/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/README.md), [`CONTRIBUTING.md`](https://github.com/HKUDS/CLI-Anything/blob/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/CONTRIBUTING.md), [`SECURITY.md`](https://github.com/HKUDS/CLI-Anything/blob/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/SECURITY.md): project contract and contribution rules
- [`cli-anything-plugin/`](https://github.com/HKUDS/CLI-Anything/tree/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/cli-anything-plugin): the generation workflow, templates, scripts, and harness SOP
- [`cli-hub/`](https://github.com/HKUDS/CLI-Anything/tree/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/cli-hub): package-manager style installer/discovery tool for harnesses
- [`skills/`](https://github.com/HKUDS/CLI-Anything/tree/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/skills): canonical agent-facing skill files for installed harnesses
- [`registry.json`](https://github.com/HKUDS/CLI-Anything/blob/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/registry.json) and [`public_registry.json`](https://github.com/HKUDS/CLI-Anything/blob/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/public_registry.json): machine-readable inventory of official harnesses plus external public CLIs
- many app directories such as [`gimp/`](https://github.com/HKUDS/CLI-Anything/tree/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/gimp), [`freecad/`](https://github.com/HKUDS/CLI-Anything/tree/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/freecad), [`n8n/`](https://github.com/HKUDS/CLI-Anything/tree/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/n8n), [`obsidian/`](https://github.com/HKUDS/CLI-Anything/tree/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/obsidian): each typically contains an `agent-harness` package
- [`docs/`](https://github.com/HKUDS/CLI-Anything/tree/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/docs) and [`assets/`](https://github.com/HKUDS/CLI-Anything/tree/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/assets): protocol notes, previews, demos, and diagrams
- [`.github/workflows/`](https://github.com/HKUDS/CLI-Anything/tree/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/.github/workflows): CI for tests, docs, labels, and publishing

This is basically a monorepo of small productized wrappers rather than a single runtime.

## Layered architecture dissection
### High-level system shape
The stack looks like this:

1. **Methodology layer**: how to turn software into an agent-native CLI
2. **Harness implementation layer**: one package per target app or service
3. **Skill/agent integration layer**: make the resulting CLI discoverable by agent frameworks
4. **Registry/distribution layer**: let agents search, install, update, and launch harnesses

### Main layers
**1. Harness methodology layer**

[`cli-anything-plugin/HARNESS.md`](https://github.com/HKUDS/CLI-Anything/blob/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/cli-anything-plugin/HARNESS.md) is the core design doc. It prescribes phases: analyze the codebase, design CLI groups, implement state and backend adapters, write tests, document test results, and generate `SKILL.md` for agents. That document is the real product spine.

**2. Harness package layer**

A harness usually follows a common shape. In [`gimp/agent-harness/cli_anything/gimp/`](https://github.com/HKUDS/CLI-Anything/tree/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/gimp/agent-harness/cli_anything/gimp), you can see the template clearly:

- [`gimp_cli.py`](https://github.com/HKUDS/CLI-Anything/blob/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/gimp/agent-harness/cli_anything/gimp/gimp_cli.py): Click-based entrypoint, REPL, command groups, JSON output switch, autosave behavior
- [`core/`](https://github.com/HKUDS/CLI-Anything/tree/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/gimp/agent-harness/cli_anything/gimp/core): project, layer, canvas, export, media, filter, and session logic
- [`utils/gimp_backend.py`](https://github.com/HKUDS/CLI-Anything/blob/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/gimp/agent-harness/cli_anything/gimp/utils/gimp_backend.py): boundary to the real underlying software path
- [`tests/`](https://github.com/HKUDS/CLI-Anything/tree/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/gimp/agent-harness/cli_anything/gimp/tests): planned and executed test suites, including `TEST.md`
- [`skills/SKILL.md`](https://github.com/HKUDS/CLI-Anything/blob/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/gimp/agent-harness/cli_anything/gimp/skills/SKILL.md): packaged agent-facing instructions

This pattern repeats across the repo. The important idea is that each harness is both a human CLI and an agent contract.

**3. Skill-generation layer**

[`cli-anything-plugin/skill_generator.py`](https://github.com/HKUDS/CLI-Anything/blob/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/cli-anything-plugin/skill_generator.py) parses harness structure, CLI commands, README hints, and setup metadata, then emits a standardized skill definition. That is a clever bridge. The model does not have to infer usage from arbitrary source. The repo manufactures an agent-readable affordance.

**4. Registry and package-manager layer**

[`cli-hub/cli_hub/cli.py`](https://github.com/HKUDS/CLI-Anything/blob/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/cli-hub/cli_hub/cli.py) exposes `list`, `search`, `info`, `install`, `update`, `uninstall`, and `launch`. It merges two inventories: official harnesses from [`registry.json`](https://github.com/HKUDS/CLI-Anything/blob/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/registry.json) and broader public CLIs from [`public_registry.json`](https://github.com/HKUDS/CLI-Anything/blob/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/public_registry.json). That means the project is evolving from "generate wrappers" into "agent tool distribution hub."

### Request / data / control flow
Typical flow:

1. Agent discovers a tool through [`cli-hub`](https://github.com/HKUDS/CLI-Anything/tree/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/cli-hub) or a [`skills/`](https://github.com/HKUDS/CLI-Anything/tree/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/skills) file.
2. Agent installs the harness from metadata in [`registry.json`](https://github.com/HKUDS/CLI-Anything/blob/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/registry.json).
3. The harness entrypoint, for example [`gimp_cli.py`](https://github.com/HKUDS/CLI-Anything/blob/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/gimp/agent-harness/cli_anything/gimp/gimp_cli.py), maps commands into project/session operations.
4. The harness core modules mutate structured project state under [`core/`](https://github.com/HKUDS/CLI-Anything/tree/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/gimp/agent-harness/cli_anything/gimp/core).
5. Backend adapters call the real application or service as needed, for example [`utils/gimp_backend.py`](https://github.com/HKUDS/CLI-Anything/blob/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/gimp/agent-harness/cli_anything/gimp/utils/gimp_backend.py).
6. Results come back as human text or `--json` output for the agent.

That is the right control-flow shape for agent tooling: discovery, install, stable command interface, stateful execution, structured output.

## Key directories and files
- [`cli-anything-plugin/HARNESS.md`](https://github.com/HKUDS/CLI-Anything/blob/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/cli-anything-plugin/HARNESS.md): the repo's real doctrine
- [`cli-anything-plugin/skill_generator.py`](https://github.com/HKUDS/CLI-Anything/blob/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/cli-anything-plugin/skill_generator.py): extracts CLI structure into agent-readable skills
- [`cli-hub/cli_hub/cli.py`](https://github.com/HKUDS/CLI-Anything/blob/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/cli-hub/cli_hub/cli.py): discovery and install interface
- [`cli-hub/setup.py`](https://github.com/HKUDS/CLI-Anything/blob/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/cli-hub/setup.py): packaging for the hub itself
- [`registry.json`](https://github.com/HKUDS/CLI-Anything/blob/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/registry.json): official harness registry
- [`public_registry.json`](https://github.com/HKUDS/CLI-Anything/blob/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/public_registry.json): third-party/public CLI registry
- [`skills/`](https://github.com/HKUDS/CLI-Anything/tree/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/skills): canonical installable skill definitions
- [`gimp/agent-harness/cli_anything/gimp/gimp_cli.py`](https://github.com/HKUDS/CLI-Anything/blob/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/gimp/agent-harness/cli_anything/gimp/gimp_cli.py): concrete reference harness
- [`gimp/agent-harness/cli_anything/gimp/core/`](https://github.com/HKUDS/CLI-Anything/tree/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/gimp/agent-harness/cli_anything/gimp/core): where domain behavior actually lives
- [`gimp/agent-harness/cli_anything/gimp/tests/TEST.md`](https://github.com/HKUDS/CLI-Anything/blob/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/gimp/agent-harness/cli_anything/gimp/tests/TEST.md): revealing because it captures planned workflow coverage, not just code
- [`.github/workflows/`](https://github.com/HKUDS/CLI-Anything/tree/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/.github/workflows): the scale-control layer for a repo with many harnesses

## Important components
- **HARNESS SOP** in [`cli-anything-plugin/HARNESS.md`](https://github.com/HKUDS/CLI-Anything/blob/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/cli-anything-plugin/HARNESS.md), which standardizes how contributors build wrappers
- **Skill generation** in [`cli-anything-plugin/skill_generator.py`](https://github.com/HKUDS/CLI-Anything/blob/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/cli-anything-plugin/skill_generator.py), which makes the wrappers legible to agents
- **Hub CLI** in [`cli-hub/cli_hub/cli.py`](https://github.com/HKUDS/CLI-Anything/blob/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/cli-hub/cli_hub/cli.py), which makes the catalog operational
- **Canonical skills tree** in [`skills/`](https://github.com/HKUDS/CLI-Anything/tree/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/skills), which separates generated agent docs from individual harness packages
- **Per-harness core/session split** illustrated by [`gimp/agent-harness/cli_anything/gimp/core/session.py`](https://github.com/HKUDS/CLI-Anything/blob/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/gimp/agent-harness/cli_anything/gimp/core/session.py) and [`gimp/agent-harness/cli_anything/gimp/core/project.py`](https://github.com/HKUDS/CLI-Anything/blob/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/gimp/agent-harness/cli_anything/gimp/core/project.py)

## Important knobs / configs / extension points
- adding a new harness by contributing another top-level app directory plus `agent-harness`
- adding or updating install metadata in [`registry.json`](https://github.com/HKUDS/CLI-Anything/blob/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/registry.json)
- expanding public-tool coverage via [`public_registry.json`](https://github.com/HKUDS/CLI-Anything/blob/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/public_registry.json)
- customizing agent guidance with canonical skill files under [`skills/`](https://github.com/HKUDS/CLI-Anything/tree/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/skills)
- choosing per-harness backend strategy, for example native app invocation vs API wrapping, as described in [`cli-anything-plugin/HARNESS.md`](https://github.com/HKUDS/CLI-Anything/blob/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/cli-anything-plugin/HARNESS.md)

## Practical questions and answers
**Is this a universal agent runtime?**
No. It is closer to a toolkit and registry for manufacturing lots of narrow agent-native interfaces.

**Where is the actual leverage?**
In the repeated shape: stable subcommands, REPL, JSON output, state, undo/redo, backend adapters, and agent-readable `SKILL.md`.

**What is the best abstraction here?**
Treating each external app as a bounded domain with its own CLI contract, instead of pretending one generic agent prompt can safely operate everything.

**What is the scaling risk?**
Harness sprawl. Every added app raises the maintenance burden on docs, packaging, compatibility, and security review.

**Is the hub important or just packaging gloss?**
Important. Without [`cli-hub`](https://github.com/HKUDS/CLI-Anything/tree/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/cli-hub), the repo would feel like a bag of examples. The hub makes it an ecosystem.

## What is smart
- They picked the right interface primitive: text commands plus JSON, not screen scraping by default.
- They turned contributor behavior into a process artifact with [`HARNESS.md`](https://github.com/HKUDS/CLI-Anything/blob/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/cli-anything-plugin/HARNESS.md).
- They understand that agents need discoverability, so they generate `SKILL.md` instead of hoping the model reverse-engineers usage.
- The split between official harness registry and public CLI registry is strategically smart. It lets them become a broader agent tool catalog, not just a wrapper factory.
- The per-harness reference shape, visible in [`gimp/agent-harness/cli_anything/gimp/`](https://github.com/HKUDS/CLI-Anything/tree/a32f11fc67052ff233dfaa5106de5bb1ccdf24ec/gimp/agent-harness/cli_anything/gimp), is concrete enough that contributors can copy it.

## What is flawed or weak
- The repo is huge and increasingly directory-heavy. Cognitive load is real.
- Quality may become uneven across harnesses. A pattern can scale faster than maintainers can validate each instance.
- Security risk expands with every wrapper that shells out to a complex desktop app or external service.
- The grand claim, "making all software agent-native," is stronger than the current evidence. What they really have is a promising monorepo of wrappers plus a decent packaging story.
- The architecture favors breadth over deep shared runtime abstraction. That is practical now, but could become duplication debt later.

## What we can learn / steal
- Write an explicit harness SOP before inviting contributors.
- Make agent-facing docs a build artifact, not an afterthought.
- Standardize on JSON output, REPL mode, state files, and undo/redo for agent tools.
- Separate the **tool contract** from the **backend adapter**.
- Build a registry and installer early if you expect many narrow integrations.

## How we could apply it
For our own agent tooling, the best thing to copy is not the whole repo. It is the recipe:

1. define a strict CLI contract for one external system
2. give it machine-readable output and a state model
3. add a generated skill/instruction layer for the agent
4. keep a registry of those wrappers so agents can discover and install them predictably

If we ever need agent access to awkward desktop or internal software, this repo is a good template for building wrappers that are inspectable and composable.

## Bottom line
CLI-Anything is most interesting as infrastructure taste. It recognizes that agents do better with explicit command surfaces than with vague "figure out the GUI" heroics.

My key takeaway: the real moat is not one amazing wrapper, it is the disciplined pipeline that keeps producing wrappers, tests, skills, and install metadata in the same shape.