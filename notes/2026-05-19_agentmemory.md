# agentmemory

- Repo: rohitg00/agentmemory
- URL: https://github.com/rohitg00/agentmemory
- Date: 2026-05-19
- Repo snapshot studied: main @ `c2f231fe8bcf9b1fa296ad5ee81267eec94de768`
- Why picked today: It is one of GitHub's hottest repos right now, it is directly relevant to coding agents, and unlike a lot of "memory" projects it ships a real integration stack instead of just a retrieval demo.

## Executive summary
agentmemory is not just a vector store for prompts. It is a local memory service for coding agents with four real product surfaces layered together: a long-running worker built on iii-engine, a hook/plugin layer that captures agent activity, an MCP/REST interface that exposes memory operations back to agents, and a browser viewer so humans can inspect what the system is storing.

The strongest design choice is that they treat memory as infrastructure, not as an app-specific feature. One backend is shared across Claude Code, Codex CLI, OpenClaw, Cursor, Gemini CLI, Hermes, pi, and others through [`plugin/`](https://github.com/rohitg00/agentmemory/tree/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/plugin), [`integrations/`](https://github.com/rohitg00/agentmemory/tree/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/integrations), and the MCP surface in [`src/mcp/`](https://github.com/rohitg00/agentmemory/tree/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/src/mcp).

The weakness is that the repo is starting to sprawl. It wants to be a memory engine, a CLI installer, an eval harness, a viewer, a plugin pack, an integration zoo, and a landing site at the same time. The core idea is good, but the surface area is getting dangerously broad.

## What they built
They built a self-hosted memory platform for coding agents.

At a practical level it does five things:

1. captures session events and tool activity through hooks and plugins, for example [`src/hooks/session-start.ts`](https://github.com/rohitg00/agentmemory/blob/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/src/hooks/session-start.ts)
2. stores observations, summaries, lessons, profiles, graphs, and search indexes in the iii-backed state layer wired up in [`src/index.ts`](https://github.com/rohitg00/agentmemory/blob/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/src/index.ts)
3. retrieves memory with hybrid keyword, vector, and graph search in [`src/state/hybrid-search.ts`](https://github.com/rohitg00/agentmemory/blob/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/src/state/hybrid-search.ts)
4. exposes that memory back to agents through MCP tools cataloged in [`src/mcp/tools-registry.ts`](https://github.com/rohitg00/agentmemory/blob/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/src/mcp/tools-registry.ts)
5. lets humans inspect the resulting memory state through the local viewer in [`src/viewer/`](https://github.com/rohitg00/agentmemory/tree/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/src/viewer)

## Why it matters
Most agent-memory projects are either thin wrappers around embeddings or static memory-file tricks. This repo is more interesting because it is trying to solve the operational problem: how do you make memory actually survive across sessions, across tools, across agents, and across interfaces without asking the user to manually maintain it?

That makes it much closer to an agent middleware layer than a feature demo.

## Repo shape at a glance
Top-level structure:

- [`src/`](https://github.com/rohitg00/agentmemory/tree/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/src): main product code, including worker boot, storage, search, hooks, providers, viewer, and MCP
- [`plugin/`](https://github.com/rohitg00/agentmemory/tree/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/plugin): packaged hooks, skills, and plugin metadata for agent environments
- [`integrations/`](https://github.com/rohitg00/agentmemory/tree/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/integrations): agent-specific adapters, including [`integrations/openclaw/`](https://github.com/rohitg00/agentmemory/tree/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/integrations/openclaw)
- [`test/`](https://github.com/rohitg00/agentmemory/tree/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/test): very broad test coverage across search, hooks, plugins, viewer security, retention, graph retrieval, and MCP
- [`benchmark/`](https://github.com/rohitg00/agentmemory/tree/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/benchmark): evaluation and load-testing scaffolding
- [`website/`](https://github.com/rohitg00/agentmemory/tree/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/website): marketing/docs site, separate from the runtime itself
- [`packages/mcp/`](https://github.com/rohitg00/agentmemory/tree/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/packages/mcp): standalone MCP shim package
- [`deploy/`](https://github.com/rohitg00/agentmemory/tree/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/deploy): deployment templates for Coolify, Fly, Railway, and Render

This is a monorepo-ish product bundle, not a minimal library.

## Layered architecture dissection
### High-level system shape
The system breaks into six layers:

1. boot/runtime orchestration
2. event capture and hook ingestion
3. memory storage and derived artifacts
4. retrieval and ranking
5. agent-facing APIs and tools
6. human inspection and operational tooling

### Main layers
**1. Boot and runtime layer**

[`src/cli.ts`](https://github.com/rohitg00/agentmemory/blob/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/src/cli.ts) is the operator surface. It starts the worker, wires agents, runs diagnostics, installs integrations, and manages the local iii-engine dependency. [`src/index.ts`](https://github.com/rohitg00/agentmemory/blob/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/src/index.ts) is the real service boot path. It loads config, picks providers, creates KV/search/index primitives, registers a huge list of memory functions, starts API triggers, and turns on the viewer.

This is where the repo reveals its real shape: the "memory app" is actually a worker process with a large function registry.

**2. Capture layer**

The hooks in [`src/hooks/`](https://github.com/rohitg00/agentmemory/tree/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/src/hooks) are the intake valves. [`src/hooks/session-start.ts`](https://github.com/rohitg00/agentmemory/blob/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/src/hooks/session-start.ts) registers sessions and can inject recall context into the agent startup path. Other hooks capture tool use, failures, session end, task completion, and subagent boundaries. The same pattern is packaged into [`plugin/scripts/`](https://github.com/rohitg00/agentmemory/tree/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/plugin/scripts) and agent-specific integration folders.

This is the most important product insight in the repo: memory quality depends on disciplined capture points, not just better retrieval.

**3. Storage and knowledge-construction layer**

The storage primitives live under [`src/state/`](https://github.com/rohitg00/agentmemory/tree/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/src/state), while higher-level memory behaviors live under [`src/functions/`](https://github.com/rohitg00/agentmemory/tree/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/src/functions). This is where observations become summaries, lessons, retention policies, checkpoints, profiles, relations, and graphs.

Notable files:

- [`src/functions/remember.ts`](https://github.com/rohitg00/agentmemory/blob/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/src/functions/remember.ts)
- [`src/functions/consolidation-pipeline.ts`](https://github.com/rohitg00/agentmemory/blob/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/src/functions/consolidation-pipeline.ts)
- [`src/functions/reflect.ts`](https://github.com/rohitg00/agentmemory/blob/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/src/functions/reflect.ts)
- [`src/functions/retention.ts`](https://github.com/rohitg00/agentmemory/blob/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/src/functions/retention.ts)
- [`src/functions/graph.ts`](https://github.com/rohitg00/agentmemory/blob/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/src/functions/graph.ts)

This layer is what turns the project from "searchable log" into "memory system."

**4. Retrieval layer**

[`src/state/hybrid-search.ts`](https://github.com/rohitg00/agentmemory/blob/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/src/state/hybrid-search.ts) is the retrieval spine. It merges BM25, vector search, and graph retrieval, then uses reciprocal-rank style fusion, optional reranking, and session diversification. [`src/functions/graph-retrieval.ts`](https://github.com/rohitg00/agentmemory/blob/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/src/functions/graph-retrieval.ts) adds path-aware entity expansion over a stored graph.

This is the smartest technical section of the repo. They are not betting on one retrieval mode.

**5. Agent interface layer**

The outward-facing tool contract lives in [`src/mcp/tools-registry.ts`](https://github.com/rohitg00/agentmemory/blob/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/src/mcp/tools-registry.ts), with transport/server code in [`src/mcp/server.ts`](https://github.com/rohitg00/agentmemory/blob/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/src/mcp/server.ts), [`src/mcp/standalone.ts`](https://github.com/rohitg00/agentmemory/blob/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/src/mcp/standalone.ts), and [`packages/mcp/`](https://github.com/rohitg00/agentmemory/tree/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/packages/mcp). This is how memory becomes usable from external agents without requiring them to understand iii internals.

**6. Viewer and ops layer**

[`src/viewer/server.ts`](https://github.com/rohitg00/agentmemory/blob/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/src/viewer/server.ts) serves a local UI and proxies back to the REST API. The notable detail here is that they are thinking about local attack surface, with explicit host allowlists and CORS handling to reduce DNS rebinding risk. That is a good sign. A lot of fast-moving agent repos would skip this entirely.

### Request / data / control flow
Typical flow:

1. an agent hook fires, for example session start or post-tool-use
2. the hook posts data to the local memory service
3. the service stores observations and may derive summaries, profiles, lessons, graph nodes, or indexes
4. later, the same or another agent calls an MCP or REST memory tool
5. retrieval combines keyword, vector, and graph signals
6. selected context is returned and can be injected back into the next session

The key architectural bet is that memory is built incrementally from workflow exhaust, then re-served through multiple agent interfaces.

## Key directories and files
- [`src/index.ts`](https://github.com/rohitg00/agentmemory/blob/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/src/index.ts): central boot sequence and function registration map
- [`src/cli.ts`](https://github.com/rohitg00/agentmemory/blob/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/src/cli.ts): installation, doctoring, connect/remove flows, runtime start/stop
- [`src/state/hybrid-search.ts`](https://github.com/rohitg00/agentmemory/blob/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/src/state/hybrid-search.ts): retrieval fusion and diversification
- [`src/functions/context.ts`](https://github.com/rohitg00/agentmemory/blob/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/src/functions/context.ts): decides what recalled memory is actually injected
- [`src/functions/graph-retrieval.ts`](https://github.com/rohitg00/agentmemory/blob/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/src/functions/graph-retrieval.ts): graph traversal and expansion logic
- [`src/mcp/tools-registry.ts`](https://github.com/rohitg00/agentmemory/blob/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/src/mcp/tools-registry.ts): catalog of agent-facing memory operations
- [`src/hooks/`](https://github.com/rohitg00/agentmemory/tree/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/src/hooks): event ingestion layer
- [`integrations/openclaw/README.md`](https://github.com/rohitg00/agentmemory/blob/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/integrations/openclaw/README.md): good example of how the repo adapts to a concrete host agent
- [`test/`](https://github.com/rohitg00/agentmemory/tree/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/test): unusually broad regression net for a fast-moving agent tool project

## Important components
- the **worker bootstrap** in [`src/index.ts`](https://github.com/rohitg00/agentmemory/blob/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/src/index.ts)
- the **hybrid retrieval engine** in [`src/state/hybrid-search.ts`](https://github.com/rohitg00/agentmemory/blob/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/src/state/hybrid-search.ts)
- the **graph retrieval helper** in [`src/functions/graph-retrieval.ts`](https://github.com/rohitg00/agentmemory/blob/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/src/functions/graph-retrieval.ts)
- the **context assembly policy** in [`src/functions/context.ts`](https://github.com/rohitg00/agentmemory/blob/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/src/functions/context.ts)
- the **agent hook pack** in [`plugin/scripts/`](https://github.com/rohitg00/agentmemory/tree/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/plugin/scripts)
- the **MCP tool surface** in [`src/mcp/`](https://github.com/rohitg00/agentmemory/tree/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/src/mcp)
- the **viewer proxy** in [`src/viewer/server.ts`](https://github.com/rohitg00/agentmemory/blob/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/src/viewer/server.ts)

## Important knobs / configs / extension points
- [`package.json`](https://github.com/rohitg00/agentmemory/blob/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/package.json): shows the product split, CLI entrypoint, and optional embedding dependencies
- [`src/cli.ts`](https://github.com/rohitg00/agentmemory/blob/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/src/cli.ts): flags like `--tools`, `--no-engine`, and agent `connect` subcommands
- [`plugin/hooks/hooks.json`](https://github.com/rohitg00/agentmemory/blob/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/plugin/hooks/hooks.json): declarative hook wiring
- [`integrations/`](https://github.com/rohitg00/agentmemory/tree/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/integrations): per-agent extension points
- environment flags referenced in code such as `AGENTMEMORY_INJECT_CONTEXT`, `AGENTMEMORY_AUTO_COMPRESS`, `RERANK_ENABLED`, and `AGENTMEMORY_III_VERSION`

## Practical questions and answers
**Is this basically a wrapper around one memory file?**

No. It can sync with memory-file style workflows, but the core design is service-oriented and event-driven.

**What part is doing the real work?**

The central worker plus the `src/functions/` and `src/state/` layers. The integrations are mostly packaging and ingestion around that core.

**Why is the repo interesting to builders?**

Because it focuses on capture policy, retrieval fusion, and cross-agent compatibility, which are the hard practical parts.

**Where would it fail in production?**

The likely pain points are operational complexity, background-process reliability, privacy expectations, and keeping many integrations in sync as host agents change.

## What is smart
- Treating memory as a shared backend that many agents can use
- Combining BM25, vector, and graph retrieval instead of declaring one winner
- Spending real effort on hook placement and context-assembly policy
- Keeping a broad automated test suite, including viewer security and plugin behavior
- Thinking about local security details like host allowlists in the viewer

## What is flawed or weak
- The product surface is getting too wide for one repo
- The function registry in [`src/index.ts`](https://github.com/rohitg00/agentmemory/blob/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/src/index.ts) is powerful but also a maintainability warning sign
- The repo makes a lot of claims in the README, and the implementation is real, but the conceptual overhead is high for new contributors
- Integration count is a strength today and a breakage factory tomorrow
- Building on a pinned iii-engine version in [`src/cli.ts`](https://github.com/rohitg00/agentmemory/blob/c2f231fe8bcf9b1fa296ad5ee81267eec94de768/src/cli.ts) is pragmatic, but it also signals upstream coupling risk

## What we can learn / steal
- Memory systems need first-class capture hooks, not just better retrieval math
- A shared backend plus thin per-agent adapters is a better scaling pattern than bespoke memory for every tool
- Retrieval diversity and context budgeting should be explicit infrastructure concerns
- Human-visible inspection tooling matters if the system is going to store long-lived behavioral traces

## How we could apply it
If we were building our own agent memory layer, I would copy three ideas first:

1. hook-based capture at stable workflow boundaries
2. hybrid retrieval with explicit fallback paths
3. a narrow, agent-agnostic API surface so multiple frontends share one memory core

I would be more cautious about copying the repo's sheer feature breadth. Better to build the spine first and add graph, viewer, eval, and per-agent packaging only after the base loop is obviously solid.

## Bottom line
agentmemory is one of the more substantial agent repos in today's hot set because it is trying to solve a real systems problem, not just a prompting problem. The best insight in the codebase is simple: useful agent memory is mostly about disciplined capture and serving infrastructure, with retrieval as only one layer of the stack. That makes this repo worth studying even if you never use the product itself.
