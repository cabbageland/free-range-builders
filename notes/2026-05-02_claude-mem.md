# Claude-Mem

- Repo: `thedotmack/claude-mem`
- URL: https://github.com/thedotmack/claude-mem
- Date: 2026-05-02
- Repo snapshot studied: `main` @ `28b40c05f2e1316948453b10e4feecce01817b6c`
- Why picked today: It is extremely hot right now, clearly AI-native, and unlike a lot of "memory" wrappers it has real system shape: hooks, a worker daemon, SQLite, vector search, MCP tooling, a viewer UI, and an OpenClaw integration layer.

## Executive summary
Claude-Mem is not just "remember stuff between chats." It is a full memory-capture pipeline for coding agents. It intercepts lifecycle events from Claude Code, ships structured observations into a local worker service, stores them in SQLite plus Chroma, and exposes search/retrieval through MCP tools and context injection.

The smart part is the architectural split. The user-facing plugin stays mostly hook-shaped and non-blocking, while the real work happens in a long-lived worker with storage, queueing, search, summarization, and a live viewer. The repo is messy around the edges because it is carrying multiple distribution surfaces at once, but the core mechanism is real and thoughtfully engineered.

## What they built
They built a persistent memory system for agentic coding sessions, centered on:

- lifecycle hooks for Claude Code in [`plugin/hooks/hooks.json`](https://github.com/thedotmack/claude-mem/blob/main/plugin/hooks/hooks.json)
- a hook orchestrator in [`src/cli/hook-command.ts`](https://github.com/thedotmack/claude-mem/blob/main/src/cli/hook-command.ts)
- a long-lived worker service in [`src/services/worker-service.ts`](https://github.com/thedotmack/claude-mem/blob/main/src/services/worker-service.ts)
- structured storage via [`src/services/worker/DatabaseManager.ts`](https://github.com/thedotmack/claude-mem/blob/main/src/services/worker/DatabaseManager.ts), [`src/services/sqlite/`](https://github.com/thedotmack/claude-mem/tree/main/src/services/sqlite), and [`src/services/sync/`](https://github.com/thedotmack/claude-mem/tree/main/src/services/sync)
- MCP search exposure in [`src/servers/mcp-server.ts`](https://github.com/thedotmack/claude-mem/blob/main/src/servers/mcp-server.ts)
- context injection in [`src/services/context/ContextBuilder.ts`](https://github.com/thedotmack/claude-mem/blob/main/src/services/context/ContextBuilder.ts)
- agent-side summarization via [`src/services/worker/SDKAgent.ts`](https://github.com/thedotmack/claude-mem/blob/main/src/services/worker/SDKAgent.ts)
- OpenClaw deployment support in [`openclaw/`](https://github.com/thedotmack/claude-mem/tree/main/openclaw)

## Why it matters
This repo matters because it treats agent memory as systems plumbing, not prompt magic. The useful insight is that durable memory for coding agents is mostly an ingestion, storage, search, and failure-isolation problem.

A lot of AI memory projects stop at "save transcript, later stuff it back into context." Claude-Mem goes further by introducing:

- structured observation capture instead of raw transcript dumping
- staged retrieval to save tokens
- graceful degradation so the memory system does not block the coding session
- multiple integration surfaces, including OpenClaw and MCP

## Repo shape at a glance
Top-level, the repo breaks into a few clear bands:

- Product and packaging
  - [`package.json`](https://github.com/thedotmack/claude-mem/blob/main/package.json), [`README.md`](https://github.com/thedotmack/claude-mem/blob/main/README.md)
  - [`plugin/`](https://github.com/thedotmack/claude-mem/tree/main/plugin) for the Claude Code plugin payload shipped to users
  - [`openclaw/`](https://github.com/thedotmack/claude-mem/tree/main/openclaw) for OpenClaw-specific packaging and setup
- Core implementation
  - [`src/cli/`](https://github.com/thedotmack/claude-mem/tree/main/src/cli) for hook entrypoints and event handlers
  - [`src/services/`](https://github.com/thedotmack/claude-mem/tree/main/src/services) for worker, storage, context, install, sync, transcript, and infrastructure logic
  - [`src/servers/`](https://github.com/thedotmack/claude-mem/tree/main/src/servers) for the MCP server
  - [`src/sdk/`](https://github.com/thedotmack/claude-mem/tree/main/src/sdk) for prompts and SDK-facing glue
- Distribution and integrations
  - [`cursor-hooks/`](https://github.com/thedotmack/claude-mem/tree/main/cursor-hooks)
  - [`plugin/skills/`](https://github.com/thedotmack/claude-mem/tree/main/plugin/skills)
  - [`src/integrations/`](https://github.com/thedotmack/claude-mem/tree/main/src/integrations)
- Docs, experiments, and tests
  - [`docs/`](https://github.com/thedotmack/claude-mem/tree/main/docs)
  - [`tests/`](https://github.com/thedotmack/claude-mem/tree/main/tests)
  - [`evals/`](https://github.com/thedotmack/claude-mem/tree/main/evals)
  - a lot of planning/artifact directories like [`PATHFINDER-2026-04-21/`](https://github.com/thedotmack/claude-mem/tree/main/PATHFINDER-2026-04-21) and [`plans/`](https://github.com/thedotmack/claude-mem/tree/main/plans)

The core repo is structurally understandable, but the top-level is crowded because source, shipping artifacts, research notes, and plugin payloads all live together.

## Layered architecture dissection
### High-level system shape
The cleanest mental model is:

1. hooks observe session events
2. hook handlers normalize and forward data
3. a worker daemon owns persistence and agent-side summarization
4. an MCP server exposes memory search
5. context generation injects summarized history back into future sessions

This is accurately reflected in [`docs/architecture-overview.md`](https://github.com/thedotmack/claude-mem/blob/main/docs/architecture-overview.md).

### Main layers
**1. Hook and event-capture layer**

- [`plugin/hooks/hooks.json`](https://github.com/thedotmack/claude-mem/blob/main/plugin/hooks/hooks.json) wires Setup, SessionStart, UserPromptSubmit, PostToolUse, PreToolUse, and Stop events.
- [`src/cli/hook-command.ts`](https://github.com/thedotmack/claude-mem/blob/main/src/cli/hook-command.ts) is the main safety valve. It classifies failures into "worker unavailable, keep going" versus "client bug, surface it."
- [`src/cli/handlers/`](https://github.com/thedotmack/claude-mem/tree/main/src/cli/handlers) contains event-specific logic.

**2. Worker orchestration layer**

- [`src/services/worker-service.ts`](https://github.com/thedotmack/claude-mem/blob/main/src/services/worker-service.ts) is the orchestrator that assembles the HTTP server, DB manager, session manager, search manager, SSE broadcaster, transcript watcher, and knowledge-agent components.
- The file header is revealing: it explicitly frames the worker as a slim orchestrator delegating to infrastructure, server, integration, and worker submodules.

**3. HTTP route layer**

- [`src/services/worker/http/routes/SessionRoutes.ts`](https://github.com/thedotmack/claude-mem/blob/main/src/services/worker/http/routes/SessionRoutes.ts)
- [`src/services/worker/http/routes/DataRoutes.ts`](https://github.com/thedotmack/claude-mem/blob/main/src/services/worker/http/routes/DataRoutes.ts)
- [`src/services/worker/http/routes/SearchRoutes.ts`](https://github.com/thedotmack/claude-mem/blob/main/src/services/worker/http/routes/SearchRoutes.ts)
- [`src/services/worker/http/routes/ViewerRoutes.ts`](https://github.com/thedotmack/claude-mem/blob/main/src/services/worker/http/routes/ViewerRoutes.ts)

This is where the system stops being a plugin and starts looking like a local memory microservice.

**4. Persistence and indexing layer**

- [`src/services/worker/DatabaseManager.ts`](https://github.com/thedotmack/claude-mem/blob/main/src/services/worker/DatabaseManager.ts) opens a single long-lived Bun SQLite connection.
- [`src/services/sqlite/SessionStore.ts`](https://github.com/thedotmack/claude-mem/blob/main/src/services/sqlite/SessionStore.ts) and [`src/services/sqlite/SessionSearch.ts`](https://github.com/thedotmack/claude-mem/blob/main/src/services/sqlite/SessionSearch.ts) carry the actual store/search load.
- [`src/services/sync/ChromaSync.ts`](https://github.com/thedotmack/claude-mem/blob/main/src/services/sync/ChromaSync.ts) bridges into vector search.

**5. Retrieval and context layer**

- [`src/servers/mcp-server.ts`](https://github.com/thedotmack/claude-mem/blob/main/src/servers/mcp-server.ts) exposes tools like search and timeline.
- [`src/services/worker/SearchManager.ts`](https://github.com/thedotmack/claude-mem/blob/main/src/services/worker/SearchManager.ts) coordinates direct filtering, semantic search, and result formatting.
- [`src/services/context/ContextBuilder.ts`](https://github.com/thedotmack/claude-mem/blob/main/src/services/context/ContextBuilder.ts) constructs the final injected memory context.

**6. Agent summarization layer**

- [`src/services/worker/SDKAgent.ts`](https://github.com/thedotmack/claude-mem/blob/main/src/services/worker/SDKAgent.ts) runs a separate Claude Agent SDK loop as an observer/summarizer with tools intentionally disabled.
- That is an important design choice: the memory agent is not allowed to recursively act on the codebase.

### Request / data / control flow
The practical flow is:

- a coding session triggers hook events from [`plugin/hooks/hooks.json`](https://github.com/thedotmack/claude-mem/blob/main/plugin/hooks/hooks.json)
- [`src/cli/hook-command.ts`](https://github.com/thedotmack/claude-mem/blob/main/src/cli/hook-command.ts) normalizes payloads and routes them to handlers
- handlers talk to the worker on port 37777 via the worker CLI/service bridge under [`plugin/scripts/`](https://github.com/thedotmack/claude-mem/tree/main/plugin/scripts)
- the worker persists sessions, prompts, and observations through SQLite, optionally syncs embeddings to Chroma, and broadcasts updates over SSE
- MCP tools in [`src/servers/mcp-server.ts`](https://github.com/thedotmack/claude-mem/blob/main/src/servers/mcp-server.ts) query that memory later
- [`src/services/context/ContextBuilder.ts`](https://github.com/thedotmack/claude-mem/blob/main/src/services/context/ContextBuilder.ts) turns results into compact prompt context for future runs

The key pattern is decoupling capture from retrieval. Capture happens continuously and locally. Retrieval is selective and token-aware.

## Key directories and files
- [`src/cli/hook-command.ts`](https://github.com/thedotmack/claude-mem/blob/main/src/cli/hook-command.ts): the best single file for understanding the failure posture
- [`plugin/hooks/hooks.json`](https://github.com/thedotmack/claude-mem/blob/main/plugin/hooks/hooks.json): the actual lifecycle surface
- [`src/services/worker-service.ts`](https://github.com/thedotmack/claude-mem/blob/main/src/services/worker-service.ts): system assembly point
- [`src/services/worker/SDKAgent.ts`](https://github.com/thedotmack/claude-mem/blob/main/src/services/worker/SDKAgent.ts): how summaries and observations are generated
- [`src/services/worker/SearchManager.ts`](https://github.com/thedotmack/claude-mem/blob/main/src/services/worker/SearchManager.ts): retrieval strategy selection
- [`src/services/context/ContextBuilder.ts`](https://github.com/thedotmack/claude-mem/blob/main/src/services/context/ContextBuilder.ts): prompt injection assembly
- [`src/servers/mcp-server.ts`](https://github.com/thedotmack/claude-mem/blob/main/src/servers/mcp-server.ts): MCP boundary
- [`docs/architecture-overview.md`](https://github.com/thedotmack/claude-mem/blob/main/docs/architecture-overview.md): the repo’s own best high-level map
- [`openclaw/SKILL.md`](https://github.com/thedotmack/claude-mem/blob/main/openclaw/SKILL.md): evidence that the project is deliberately expanding beyond Claude Code into agent gateway deployments

## Important components
- **Hook error classifier** in [`src/cli/hook-command.ts`](https://github.com/thedotmack/claude-mem/blob/main/src/cli/hook-command.ts). This is the most important reliability decision in the repo. If the worker is down, the coding session keeps going.
- **WorkerService** in [`src/services/worker-service.ts`](https://github.com/thedotmack/claude-mem/blob/main/src/services/worker-service.ts). This is the composition root.
- **DatabaseManager** in [`src/services/worker/DatabaseManager.ts`](https://github.com/thedotmack/claude-mem/blob/main/src/services/worker/DatabaseManager.ts). It enforces the one-shared-connection model and optional Chroma enablement.
- **SDKAgent** in [`src/services/worker/SDKAgent.ts`](https://github.com/thedotmack/claude-mem/blob/main/src/services/worker/SDKAgent.ts). It runs a separate observer agent with strict tool denial, isolated environment loading, and session-ID hygiene.
- **SearchManager / search submodules** in [`src/services/worker/search/`](https://github.com/thedotmack/claude-mem/tree/main/src/services/worker/search). This is where the "progressive disclosure" story becomes implementation rather than marketing.
- **MCP server** in [`src/servers/mcp-server.ts`](https://github.com/thedotmack/claude-mem/blob/main/src/servers/mcp-server.ts). Thin wrapper, good boundary.
- **ContextBuilder** in [`src/services/context/ContextBuilder.ts`](https://github.com/thedotmack/claude-mem/blob/main/src/services/context/ContextBuilder.ts). It converts stored memory into prompt-time context instead of indiscriminately replaying transcripts.

## Important knobs / configs / extension points
- hook timeouts and lifecycle wiring in [`plugin/hooks/hooks.json`](https://github.com/thedotmack/claude-mem/blob/main/plugin/hooks/hooks.json)
- worker host/port logic in [`src/shared/worker-utils.ts`](https://github.com/thedotmack/claude-mem/blob/main/src/shared/worker-utils.ts)
- settings defaults and environment shaping in [`src/shared/SettingsDefaultsManager.ts`](https://github.com/thedotmack/claude-mem/blob/main/src/shared/SettingsDefaultsManager.ts) and [`src/shared/EnvManager.ts`](https://github.com/thedotmack/claude-mem/blob/main/src/shared/EnvManager.ts)
- transcript-based integrations via [`src/services/transcripts/`](https://github.com/thedotmack/claude-mem/tree/main/src/services/transcripts)
- OpenClaw plugin configuration guidance in [`openclaw/SKILL.md`](https://github.com/thedotmack/claude-mem/blob/main/openclaw/SKILL.md)
- mode and skill surfaces under [`plugin/modes/`](https://github.com/thedotmack/claude-mem/tree/main/plugin/modes) and [`plugin/skills/`](https://github.com/thedotmack/claude-mem/tree/main/plugin/skills)

## Practical questions and answers
**How does it avoid becoming a single point of failure?**
By design. [`src/cli/hook-command.ts`](https://github.com/thedotmack/claude-mem/blob/main/src/cli/hook-command.ts) treats transport errors, timeouts, and 5xx failures as non-blocking and exits successfully.

**What is the real product here, the plugin or the worker?**
The worker. The plugin is just the event tap and transport shell.

**Why not just store raw transcripts?**
Because the repo is optimizing for future retrieval cost and usefulness. The staged search flow in [`src/servers/mcp-server.ts`](https://github.com/thedotmack/claude-mem/blob/main/src/servers/mcp-server.ts) and the context assembly in [`src/services/context/ContextBuilder.ts`](https://github.com/thedotmack/claude-mem/blob/main/src/services/context/ContextBuilder.ts) are explicitly about filtering before spending tokens.

**What is the cleverest design decision?**
Running the summarizer as a separate constrained observer agent in [`src/services/worker/SDKAgent.ts`](https://github.com/thedotmack/claude-mem/blob/main/src/services/worker/SDKAgent.ts) instead of letting the memory layer recursively use tools.

**Where would this get brittle in production?**
At the integration seams: hook payload formats, local worker lifecycle, Bun/Node packaging, and the burden of supporting Claude Code, OpenClaw, Cursor-ish flows, transcript watchers, and multiple AI backends in one repo.

## What is smart
- The graceful-degradation stance is correct. Memory is valuable, but it must not break the main coding flow.
- The split between hook capture and daemonized processing is mature.
- The retrieval model is token-economics aware rather than "dump more context and pray."
- The observer agent runs with tools disallowed, isolated env handling, and explicit session-ID discipline. That is the kind of boring paranoia you want in this class of system.
- The project is ambitiously multi-surface without pretending all surfaces are the same. OpenClaw support lives in its own subtree instead of being hand-waved.

## What is flawed or weak
- The top-level repo is crowded. Product code, generated/plugin payload, planning documents, experiments, and integration artifacts are interleaved.
- There is visible architecture drift. Some docs still describe older shapes, and the worker README even mentions PM2 while current code is clearly on a broader supervisor model.
- The system has a lot of moving pieces for what many users will think of as "a memory plugin." That is not necessarily bad, but it raises maintenance cost fast.
- Multiple distribution targets can turn every refactor into a packaging problem.

## What we can learn / steal
- Treat memory as a service boundary, not a prompt trick.
- Make secondary systems fail open when the primary user workflow must continue.
- Use progressive disclosure for retrieval. Index first, inspect later, fetch full detail only on demand.
- If an auxiliary agent is doing summarization, strip its tools and isolate its credentials.
- Keep retrieval context synthesized and structured, not transcript-shaped by default.

## How we could apply it
For our own agent systems, the best reusable pattern is:

1. capture structured events from tools and prompts
2. persist them in a local store with good metadata
3. add a search layer that can do cheap filter-first retrieval
4. expose that via narrow tools or APIs
5. inject compact context into future sessions only when it pays for itself

If we copied only one thing, it would be the fail-open hook posture plus the staged retrieval model.

## Bottom line
Claude-Mem is one of the more serious AI-memory repos because it understands that the hard part is not "remembering," it is building a dependable local memory pipeline that does not poison or block the main workflow.

The repo is a little sprawling, but the core architecture is better than the hype category it lives in. The best insight here is that useful agent memory looks less like chatbot magic and more like a small observability stack for cognition.
