# Compound Engineering Plugin

- Repo: `EveryInc/compound-engineering-plugin`
- URL: https://github.com/EveryInc/compound-engineering-plugin
- Date: 2026-05-29
- Repo snapshot studied: `main` @ `85987d496fdfdc8a18faf592fd53329e23266537`
- Why picked today: It is one of the hotter AI-agent repos in the current GitHub stream, but unlike a lot of agent-wrapper noise, this one has a real internal architecture. It is a plugin distribution system plus a workflow philosophy, and the code actually shows how they translate one plugin surface into several agent runtimes.

## Executive summary
This repo is not mainly an app. It is an adapter layer for a way of working. The product idea is “compound engineering” as a reusable set of skills, prompts, and reviewer agents, and the implementation challenge is shipping that idea into multiple coding-agent ecosystems without rewriting it from scratch for each one.

The smart core is simple: treat Claude-compatible plugin content as the source format, parse that structure, convert it into target-specific bundles, and install those bundles into Codex, OpenCode, Pi, Gemini, Kiro, and native plugin-compatible tools. In other words, the interesting thing here is not the prompts themselves. It is the repo’s attempt to build a portability layer for agent workflows.

## What they built
They built a multi-target plugin/tooling repo with two major surfaces:
- the actual Compound Engineering plugin content in [`plugins/compound-engineering/`](https://github.com/EveryInc/compound-engineering-plugin/tree/main/plugins/compound-engineering), including agents, manifests, and docs,
- and a Bun/TypeScript conversion and installation CLI in [`src/`](https://github.com/EveryInc/compound-engineering-plugin/tree/main/src) that parses Claude-style plugin structure and rewrites it for other targets.

There is also a smaller example or sibling plugin in [`plugins/coding-tutor/`](https://github.com/EveryInc/compound-engineering-plugin/tree/main/plugins/coding-tutor), which is useful because it suggests the repo is not hard-coded to one plugin forever. It is trying to be a generic converter/distributor, with Compound Engineering as the flagship package.

## Why it matters
A lot of AI tooling repos are trapped by platform silos. They create a useful prompt or workflow once, then reimplement it poorly for every other agent host. This repo is trying to centralize that work:
- author once in a Claude-style source format,
- convert to target-specific formats,
- preserve skills, agents, hooks, MCP config, and install behavior where possible.

That is a practical systems problem, not a branding problem. If you believe the future is many agent hosts with slightly incompatible plugin models, this kind of repo becomes infrastructure.

## Repo shape at a glance
Top-level shape:
- [`plugins/compound-engineering/`](https://github.com/EveryInc/compound-engineering-plugin/tree/main/plugins/compound-engineering), the main shipped plugin with agents, manifests, and plugin docs
- [`plugins/coding-tutor/`](https://github.com/EveryInc/compound-engineering-plugin/tree/main/plugins/coding-tutor), a second plugin that exercises the same packaging system
- [`src/`](https://github.com/EveryInc/compound-engineering-plugin/tree/main/src), the CLI, parser, converters, target writers, and utilities
- [`docs/skills/`](https://github.com/EveryInc/compound-engineering-plugin/tree/main/docs/skills), user-facing docs for many CE skills
- [`tests/`](https://github.com/EveryInc/compound-engineering-plugin/tree/main/tests), fixtures and conversion/install tests
- [`scripts/release/`](https://github.com/EveryInc/compound-engineering-plugin/tree/main/scripts/release), release metadata and validation helpers
- [`package.json`](https://github.com/EveryInc/compound-engineering-plugin/blob/main/package.json), the Bun CLI and release/test entrypoints

This is a nice split. Plugin payload lives under `plugins/`, while the transport machinery that converts and installs those payloads lives under `src/`.

## Layered architecture dissection
### High-level system shape
There are four real layers:
1. plugin source content,
2. parser and normalization,
3. target conversion,
4. target-specific installation and cleanup.

That layered split is what makes the repo interesting. The content and the distribution logic are coupled, but not tangled.

### Main layers
**1. Plugin content layer**
- [`plugins/compound-engineering/.claude-plugin/plugin.json`](https://github.com/EveryInc/compound-engineering-plugin/blob/main/plugins/compound-engineering/.claude-plugin/plugin.json) defines the plugin identity and metadata.
- [`plugins/compound-engineering/agents/`](https://github.com/EveryInc/compound-engineering-plugin/tree/main/plugins/compound-engineering/agents) contains the specialized reviewer, researcher, and workflow agents.
- [`plugins/compound-engineering/README.md`](https://github.com/EveryInc/compound-engineering-plugin/blob/main/plugins/compound-engineering/README.md) is effectively the component catalog.

This layer is the knowledge/product layer: what skills and agents exist, what they are for, and how the system is meant to be used.

**2. Parse and normalize layer**
- [`src/parsers/claude.ts`](https://github.com/EveryInc/compound-engineering-plugin/blob/main/src/parsers/claude.ts) is one of the key files in the repo.
- It resolves a Claude plugin root, reads plugin manifests, walks agent/command/skill directories, parses frontmatter, loads hooks, and optionally merges MCP server definitions.

This is the first important architectural choice: Claude-style plugin layout is treated as the canonical source representation.

**3. Conversion layer**
- [`src/converters/`](https://github.com/EveryInc/compound-engineering-plugin/tree/main/src/converters) holds the format translators for Codex, Copilot, Droid, Gemini, Kiro, OpenCode, and Pi.
- [`src/targets/index.ts`](https://github.com/EveryInc/compound-engineering-plugin/blob/main/src/targets/index.ts) registers which targets exist and how they are written.

This layer turns a single normalized plugin into several target bundles. That is the portability engine.

**4. Install and target-state management layer**
- [`src/commands/install.ts`](https://github.com/EveryInc/compound-engineering-plugin/blob/main/src/commands/install.ts) is the main operational entrypoint.
- [`src/commands/convert.ts`](https://github.com/EveryInc/compound-engineering-plugin/blob/main/src/commands/convert.ts) handles conversion-only flows.
- [`src/targets/codex.ts`](https://github.com/EveryInc/compound-engineering-plugin/blob/main/src/targets/codex.ts) shows the hard part: install manifests, cleanup of stale files, config merging, hook merging, and preservation of managed versus unmanaged state.
- [`src/utils/codex-agents.ts`](https://github.com/EveryInc/compound-engineering-plugin/blob/main/src/utils/codex-agents.ts) patches an `AGENTS.md` compatibility block so Codex can interpret Claude-ish tool assumptions.

This is where the repo graduates from prompt pack to real systems code. Installation is messy, stateful, and target-specific, and they are doing that work.

### Request / data / control flow
A simplified flow looks like this:
1. the CLI entrypoint in [`src/index.ts`](https://github.com/EveryInc/compound-engineering-plugin/blob/main/src/index.ts) dispatches to `install`, `convert`, `cleanup`, `list`, or `plugin-path`,
2. `install` or `convert` loads a Claude-style plugin via [`src/parsers/claude.ts`](https://github.com/EveryInc/compound-engineering-plugin/blob/main/src/parsers/claude.ts),
3. the chosen target in [`src/targets/index.ts`](https://github.com/EveryInc/compound-engineering-plugin/blob/main/src/targets/index.ts) converts that normalized plugin into a target bundle,
4. the target writer, for example [`src/targets/codex.ts`](https://github.com/EveryInc/compound-engineering-plugin/blob/main/src/targets/codex.ts), writes files, merges config, removes stale managed artifacts, and preserves non-managed user state where possible,
5. helper utilities like [`src/utils/detect-tools.ts`](https://github.com/EveryInc/compound-engineering-plugin/blob/main/src/utils/detect-tools.ts) and [`src/utils/resolve-output.ts`](https://github.com/EveryInc/compound-engineering-plugin/blob/main/src/utils/resolve-output.ts) decide where the bundle should land.

The control flow is straightforward. The subtlety is in the file ownership and upgrade path.

## Key directories and files
- [`README.md`](https://github.com/EveryInc/compound-engineering-plugin/blob/main/README.md), the product philosophy and install matrix
- [`package.json`](https://github.com/EveryInc/compound-engineering-plugin/blob/main/package.json), CLI scripts and dependency surface
- [`plugins/compound-engineering/`](https://github.com/EveryInc/compound-engineering-plugin/tree/main/plugins/compound-engineering), the flagship plugin payload
- [`plugins/compound-engineering/agents/`](https://github.com/EveryInc/compound-engineering-plugin/tree/main/plugins/compound-engineering/agents), the subagent inventory that gives the workflow its specialization
- [`docs/skills/`](https://github.com/EveryInc/compound-engineering-plugin/tree/main/docs/skills), skill-level docs that explain the intended loop
- [`src/index.ts`](https://github.com/EveryInc/compound-engineering-plugin/blob/main/src/index.ts), CLI composition root
- [`src/parsers/claude.ts`](https://github.com/EveryInc/compound-engineering-plugin/blob/main/src/parsers/claude.ts), canonical plugin ingestion
- [`src/commands/install.ts`](https://github.com/EveryInc/compound-engineering-plugin/blob/main/src/commands/install.ts), install orchestration
- [`src/commands/convert.ts`](https://github.com/EveryInc/compound-engineering-plugin/blob/main/src/commands/convert.ts), conversion orchestration
- [`src/targets/`](https://github.com/EveryInc/compound-engineering-plugin/tree/main/src/targets), target-specific writers
- [`src/utils/codex-agents.ts`](https://github.com/EveryInc/compound-engineering-plugin/blob/main/src/utils/codex-agents.ts), compatibility glue for Codex expectations
- [`tests/`](https://github.com/EveryInc/compound-engineering-plugin/tree/main/tests), the safety net for format conversion and install behavior

## Important components
**The Claude plugin parser**
[`src/parsers/claude.ts`](https://github.com/EveryInc/compound-engineering-plugin/blob/main/src/parsers/claude.ts) is the center of gravity. Once a repo chooses a canonical intermediate representation, that parser becomes the border crossing for everything else.

**The install command**
[`src/commands/install.ts`](https://github.com/EveryInc/compound-engineering-plugin/blob/main/src/commands/install.ts) does more than copy files. It resolves plugin sources, checks installed tools, computes output roots, supports scope decisions, and invokes target writers with install semantics.

**The target registry**
[`src/targets/index.ts`](https://github.com/EveryInc/compound-engineering-plugin/blob/main/src/targets/index.ts) keeps the repo honest. New platforms are explicit entries with conversion and write behavior, not ad hoc branches all over the codebase.

**The Codex writer**
[`src/targets/codex.ts`](https://github.com/EveryInc/compound-engineering-plugin/blob/main/src/targets/codex.ts) is the best example of real engineering in the repo. It tracks managed artifacts, merges hooks and config, cleans old prompts/skills/agents, and tries not to delete user-owned state.

**The compatibility shim**
[`src/utils/codex-agents.ts`](https://github.com/EveryInc/compound-engineering-plugin/blob/main/src/utils/codex-agents.ts) is revealing because it encodes semantic translation, not just file conversion. It literally maps Claude-oriented tool concepts into Codex equivalents.

## Important knobs / configs / extension points
- [`plugins/compound-engineering/.claude-plugin/plugin.json`](https://github.com/EveryInc/compound-engineering-plugin/blob/main/plugins/compound-engineering/.claude-plugin/plugin.json), plugin metadata and identity
- [`src/commands/install.ts`](https://github.com/EveryInc/compound-engineering-plugin/blob/main/src/commands/install.ts), target choice, scope, permissions, extra outputs, branch source, and inclusion flags
- [`src/targets/index.ts`](https://github.com/EveryInc/compound-engineering-plugin/blob/main/src/targets/index.ts), where supported targets and default behaviors are declared
- [`src/utils/detect-tools.ts`](https://github.com/EveryInc/compound-engineering-plugin/blob/main/src/utils/detect-tools.ts), installed-tool detection logic
- [`scripts/release/`](https://github.com/EveryInc/compound-engineering-plugin/tree/main/scripts/release), release validation and metadata sync

The biggest extension point is obvious: add another converter/target pair and the whole plugin ecosystem widens.

## Practical questions and answers
**What is the real product here?**
Not just the CE prompts. The real product is a portable workflow system for agent-assisted engineering.

**What is the deepest implementation idea?**
Use one canonical plugin representation, then generate target-native bundles from it.

**Where is the highest engineering risk?**
State management during install and upgrade. Target-specific config merging and cleanup are where portability projects usually become brittle.

**What looks most reusable?**
The parser -> normalized model -> target writer pipeline. That pattern is reusable well beyond this repo.

**Does the repo feel generic or bespoke?**
Both. The architecture wants to be generic, but a lot of the value is still bundled tightly around the Compound Engineering worldview and its agent roster.

## What is smart
- The repo cleanly separates plugin payload from distribution machinery.
- Claude-style plugin format is treated as a canonical source, which reduces duplication.
- Target support is centralized in an explicit registry instead of hidden conditionals.
- The Codex path shows serious thought about managed artifact ownership and upgrade safety.
- The system ships both philosophy and mechanism: docs describe the loop, code installs the loop.

## What is flawed or weak
- The repo’s conceptual center is clear, but its market surface is slightly fragmented: plugin system, workflow doctrine, cross-agent portability layer, and content catalog all live together.
- The flagship plugin has a lot of agents and skills, which is powerful but risks discoverability bloat.
- Portability across agent hosts always degrades toward least-common-denominator semantics. The compatibility blocks are clever, but they also reveal the inherent mismatch.
- Long term, install/cleanup logic per target can become the maintenance tax that eats the elegance of the core idea.

## What we can learn / steal
- Pick one canonical authoring format, then compile outward.
- Treat installer cleanup and ownership boundaries as first-class architecture, not janitorial afterthoughts.
- Keep target registration explicit and typed.
- Encode cross-platform semantic shims in a single obvious place.
- If a workflow philosophy matters, document it close to the implementation instead of in a separate marketing site.

## How we could apply it
If we wanted to ship our own internal agent workflows across several hosts, I would copy this pattern almost directly:
1. define a canonical content format,
2. parse it into a normalized in-memory model,
3. emit target-native bundles,
4. maintain a strict notion of managed artifacts so upgrades stay safe.

What I would watch carefully is plugin sprawl. The portability layer is strongest when the content model stays disciplined.

## Bottom line
This repo is worth studying because it solves a real problem beneath the AI-tooling hype: how do you make agent workflows portable without rewriting them by hand for every runtime?

My main takeaway is that the most valuable thing here is not any single prompt. It is the compiler mindset. They are treating agent workflows like source code that should be parsed, transformed, installed, and upgraded with discipline.