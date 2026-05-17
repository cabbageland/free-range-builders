# CLI-Anything

- Repo: `HKUDS/CLI-Anything`
- URL: https://github.com/HKUDS/CLI-Anything
- Date: 2026-05-17
- Repo snapshot studied: `main` @ `e8e7f408604e28ddb15e57697bd5c1b021b12d7e`
- Why picked today: It is genuinely hot right now, clearly AI-shaped rather than AI-labeled, and it is trying something ambitious and concrete: convert lots of existing software into agent-usable CLIs instead of waiting for native MCP/server support.

## Executive summary
CLI-Anything is a monorepo for building and distributing agent-facing CLIs for software that was never designed for agents. The clever move is not "LLMs can use CLIs". That part is obvious. The clever move is standardizing the conversion process: analyze GUI app internals, expose the real state model, wrap the backend, force JSON output, add REPL ergonomics, generate a `SKILL.md`, and publish each harness as an installable tool.

The repo is best understood as three products living together: a harness factory, a marketplace/distribution layer, and a large catalog of per-software adapters. It is practical, a little sprawling, and more serious than the marketing copy first suggests.

## What they built
They built a repeatable pipeline for turning GUI apps, web services, and other software into agent-native CLIs.

In practice that means:
- a standard operating procedure in [`cli-anything-plugin/HARNESS.md`](https://github.com/HKUDS/CLI-Anything/blob/e8e7f408604e28ddb15e57697bd5c1b021b12d7e/cli-anything-plugin/HARNESS.md)
- a plugin/generator layer in [`cli-anything-plugin/`](https://github.com/HKUDS/CLI-Anything/tree/e8e7f408604e28ddb15e57697bd5c1b021b12d7e/cli-anything-plugin)
- a packaging and discovery hub in [`cli-hub/`](https://github.com/HKUDS/CLI-Anything/tree/e8e7f408604e28ddb15e57697bd5c1b021b12d7e/cli-hub)
- a canonical skill surface in [`skills/`](https://github.com/HKUDS/CLI-Anything/tree/e8e7f408604e28ddb15e57697bd5c1b021b12d7e/skills)
- roughly 55 adapter subprojects, each with its own [`agent-harness/`](https://github.com/HKUDS/CLI-Anything/tree/e8e7f408604e28ddb15e57697bd5c1b021b12d7e/blender/agent-harness)-style package

## Why it matters
A lot of agent infrastructure assumes the world will slowly recompile itself into APIs, MCP servers, or agent-specific products. CLI-Anything takes the opposite bet: there is already an enormous installed base of software, and the fastest path is to wrap it in a disciplined command surface.

That matters because it shifts agent enablement from "replace the stack" to "instrument the stack".

## Repo shape at a glance
At top level the repo is a monorepo with four big zones:

- the core build method and plugin runtime in [`cli-anything-plugin/`](https://github.com/HKUDS/CLI-Anything/tree/e8e7f408604e28ddb15e57697bd5c1b021b12d7e/cli-anything-plugin)
- the install/discovery product in [`cli-hub/`](https://github.com/HKUDS/CLI-Anything/tree/e8e7f408604e28ddb15e57697bd5c1b021b12d7e/cli-hub)
- the catalog/metadata layer in [`registry.json`](https://github.com/HKUDS/CLI-Anything/blob/e8e7f408604e28ddb15e57697bd5c1b021b12d7e/registry.json), [`public_registry.json`](https://github.com/HKUDS/CLI-Anything/blob/e8e7f408604e28ddb15e57697bd5c1b021b12d7e/public_registry.json), and [`skills/`](https://github.com/HKUDS/CLI-Anything/tree/e8e7f408604e28ddb15e57697bd5c1b021b12d7e/skills)
- many per-target harness directories like [`blender/`](https://github.com/HKUDS/CLI-Anything/tree/e8e7f408604e28ddb15e57697bd5c1b021b12d7e/blender), [`gimp/`](https://github.com/HKUDS/CLI-Anything/tree/e8e7f408604e28ddb15e57697bd5c1b021b12d7e/gimp), [`n8n/`](https://github.com/HKUDS/CLI-Anything/tree/e8e7f408604e28ddb15e57697bd5c1b021b12d7e/n8n), [`browser/`](https://github.com/HKUDS/CLI-Anything/tree/e8e7f408604e28ddb15e57697bd5c1b021b12d7e/browser), and many more

The result feels less like one app and more like a factory plus marketplace for many small app-specific control planes.

## Layered architecture dissection
### High-level system shape
The system has a pretty clean top-down flow:

1. define a method for converting software into a CLI
2. generate or hand-build the harness
3. emit skill metadata so agents can discover and use it
4. publish registry entries so humans and agents can install it
5. run the installed harness against real software backends

### Main layers
**1. Method / SOP layer**

The most important design artifact is [`cli-anything-plugin/HARNESS.md`](https://github.com/HKUDS/CLI-Anything/blob/e8e7f408604e28ddb15e57697bd5c1b021b12d7e/cli-anything-plugin/HARNESS.md). It defines the repo's real product: a 6.5-phase recipe for codebase analysis, CLI architecture, backend wrapping, REPL design, test planning, test execution, and skill generation.

**2. Generator / plugin layer**

[`cli-anything-plugin/skill_generator.py`](https://github.com/HKUDS/CLI-Anything/blob/e8e7f408604e28ddb15e57697bd5c1b021b12d7e/cli-anything-plugin/skill_generator.py) parses a harness, extracts commands and metadata, and generates discoverable `SKILL.md` files. This is where the repo stops being just "some CLIs" and becomes an agent ecosystem.

**3. Distribution / marketplace layer**

[`cli-hub/cli_hub/cli.py`](https://github.com/HKUDS/CLI-Anything/blob/e8e7f408604e28ddb15e57697bd5c1b021b12d7e/cli-hub/cli_hub/cli.py) is the user-facing package manager. It can list, search, install, update, inspect, and launch harnesses. [`cli-hub/cli_hub/registry.py`](https://github.com/HKUDS/CLI-Anything/blob/e8e7f408604e28ddb15e57697bd5c1b021b12d7e/cli-hub/cli_hub/registry.py) fetches and caches registry data, and [`cli-hub/cli_hub/installer.py`](https://github.com/HKUDS/CLI-Anything/blob/e8e7f408604e28ddb15e57697bd5c1b021b12d7e/cli-hub/cli_hub/installer.py) dispatches installation through pip, npm, uv, bundled tools, or arbitrary install commands.

**4. Registry / metadata layer**

[`registry.json`](https://github.com/HKUDS/CLI-Anything/blob/e8e7f408604e28ddb15e57697bd5c1b021b12d7e/registry.json) and [`public_registry.json`](https://github.com/HKUDS/CLI-Anything/blob/e8e7f408604e28ddb15e57697bd5c1b021b12d7e/public_registry.json) are the marketplace index. The repo-root [`skills/README.md`](https://github.com/HKUDS/CLI-Anything/blob/e8e7f408604e28ddb15e57697bd5c1b021b12d7e/skills/README.md) shows the newer canonical pattern: skill files live at the repo root even if packaged copies still exist deeper in each harness.

**5. Per-software harness layer**

Each target app gets its own subproject, usually `<software>/agent-harness`, containing a Python package, tests, and adapter logic. This is the actual workhorse layer, because every supported app has unique state, backend invocation, export mechanics, and failure modes.

### Request / data / control flow
A typical flow looks like this:

- an agent invokes the plugin or installs an existing harness
- the harness exposes subcommands plus a REPL with JSON/human output modes
- commands mutate or inspect project state, often through generated files or wrapped native backends
- the skill file tells higher-level agents how to discover and call the CLI
- the hub/registry layer makes the harness installable and searchable at scale

So the architecture is not "one server talks to one model". It is "many narrow command surfaces standardized enough for agents to chain".

## Key directories and files
- [`README.md`](https://github.com/HKUDS/CLI-Anything/blob/e8e7f408604e28ddb15e57697bd5c1b021b12d7e/README.md): the public story and quick-start paths for Claude Code, OpenClaw, Codex, Pi, and others
- [`cli-anything-plugin/HARNESS.md`](https://github.com/HKUDS/CLI-Anything/blob/e8e7f408604e28ddb15e57697bd5c1b021b12d7e/cli-anything-plugin/HARNESS.md): the real architecture contract
- [`cli-anything-plugin/skill_generator.py`](https://github.com/HKUDS/CLI-Anything/blob/e8e7f408604e28ddb15e57697bd5c1b021b12d7e/cli-anything-plugin/skill_generator.py): extracts CLI structure and emits `SKILL.md`
- [`cli-anything-plugin/repl_skin.py`](https://github.com/HKUDS/CLI-Anything/blob/e8e7f408604e28ddb15e57697bd5c1b021b12d7e/cli-anything-plugin/repl_skin.py): standardized REPL presentation layer
- [`cli-hub/cli_hub/cli.py`](https://github.com/HKUDS/CLI-Anything/blob/e8e7f408604e28ddb15e57697bd5c1b021b12d7e/cli-hub/cli_hub/cli.py): CLI-Hub package manager entrypoint
- [`cli-hub/cli_hub/installer.py`](https://github.com/HKUDS/CLI-Anything/blob/e8e7f408604e28ddb15e57697bd5c1b021b12d7e/cli-hub/cli_hub/installer.py): install/update/remove orchestration across multiple package strategies
- [`cli-hub/cli_hub/registry.py`](https://github.com/HKUDS/CLI-Anything/blob/e8e7f408604e28ddb15e57697bd5c1b021b12d7e/cli-hub/cli_hub/registry.py): remote registry fetch and cache layer
- [`registry.json`](https://github.com/HKUDS/CLI-Anything/blob/e8e7f408604e28ddb15e57697bd5c1b021b12d7e/registry.json): first-party harness registry
- [`public_registry.json`](https://github.com/HKUDS/CLI-Anything/blob/e8e7f408604e28ddb15e57697bd5c1b021b12d7e/public_registry.json): public CLI catalog expansion path
- [`skills/`](https://github.com/HKUDS/CLI-Anything/tree/e8e7f408604e28ddb15e57697bd5c1b021b12d7e/skills): canonical skill surface for agent discovery and `npx skills` installation

## Important components
- **HARNESS SOP**: the real product, because it encodes how to decompose GUI software into an agent-usable control surface
- **skill generator**: turns a working harness into an AI-discoverable capability instead of a hidden binary
- **CLI-Hub**: converts a scattered repo into a searchable/installable ecosystem
- **registry files**: the control plane for publishing and categorization
- **per-app harnesses**: where abstraction meets reality and most brittleness lives

## Important knobs / configs / extension points
- install strategy fields in [`registry.json`](https://github.com/HKUDS/CLI-Anything/blob/e8e7f408604e28ddb15e57697bd5c1b021b12d7e/registry.json) and [`public_registry.json`](https://github.com/HKUDS/CLI-Anything/blob/e8e7f408604e28ddb15e57697bd5c1b021b12d7e/public_registry.json), which decide whether a tool is installed by pip, npm, uv, bundled logic, or a raw command
- the `--json` dual-output pattern documented in [`cli-anything-plugin/HARNESS.md`](https://github.com/HKUDS/CLI-Anything/blob/e8e7f408604e28ddb15e57697bd5c1b021b12d7e/cli-anything-plugin/HARNESS.md), which is essential for agent reliability
- canonical skill placement under [`skills/`](https://github.com/HKUDS/CLI-Anything/tree/e8e7f408604e28ddb15e57697bd5c1b021b12d7e/skills), which decouples agent discovery from package internals
- backend wrappers per harness, which are the extension point that maps abstract commands to real software behavior

## Practical questions and answers
**Does it actually control software directly, or mostly generate wrappers?**
Both. The repo's center of gravity is wrapper generation and standardization, but each shipped harness is expected to call real software backends or APIs.

**What is the most valuable idea here?**
Treating agent enablement as a packaging and interface-discipline problem, not just a model problem.

**Where is the real complexity?**
Not in the top-level hub. It is in the long tail of per-app harnesses, export validation, session/state handling, and keeping dozens of adapters consistent.

**Is the repo pretending all software can be abstracted the same way?**
Not exactly. The SOP is standardized, but the harness layout admits that every target has a different backend and different failure surface.

**What assumption does the system make?**
That many important apps already have enough internal structure, automation hooks, or scriptable backends that a disciplined CLI layer can expose them to agents.

## What is smart
- The repo frames CLI as the lingua franca between agents and legacy software instead of waiting for every vendor to ship native agent protocols.
- The strongest artifact is procedural: `HARNESS.md` is a serious playbook, not fluff.
- The dual move of shipping both CLIs and `SKILL.md` files is sharp. It covers both execution and discoverability.
- CLI-Hub is a pragmatic ecosystem layer. Without it, the project would feel like a pile of unrelated adapters.
- The canonical `skills/` reorganization is the right kind of boring infrastructure cleanup. It makes the repo more legible to agents and contributors.

## What is flawed or weak
- The monorepo is already sprawling. 55 harnesses means review quality and consistency are real risks.
- The top-level README is energetic, but it can make the project seem more turnkey than the adapter reality underneath.
- Success depends on each harness being deeply grounded in real backend behavior. That does not scale cheaply.
- Registry-driven install commands are powerful, but they also widen the trust and maintenance surface.
- Some of the value is operational rather than architectural beauty: a lot of work here is repetitive adapter craftsmanship.

## What we can learn / steal
- Write the method down. A strong SOP can be the product.
- Separate capability generation, capability discovery, and capability distribution into distinct layers.
- Force machine-readable output from day one. Agents need JSON, not vibes.
- Treat skill metadata as first-class packaging, not an afterthought.
- Use a marketplace index to keep a multi-adapter system from collapsing into tribal knowledge.

## How we could apply it
If we needed agent access to a messy internal stack, I would copy the pattern almost directly:

1. define a harness contract per system
2. require JSON output plus human output
3. wrap real backends, not mock abstractions
4. generate agent-readable skill metadata automatically
5. publish everything through one searchable internal registry

The big lesson is that "agent-native" often means disciplined interface engineering, not fancy model orchestration.

## Bottom line
CLI-Anything is more substantial than it first appears. Under the hype layer, it is building a practical bridge from existing software to agent workflows by standardizing how adapters are designed, packaged, discovered, and installed.

The key insight is simple and useful: if you want agents to use the world's software soon, the fastest path is not to rebuild the world, it is to wrap it well.