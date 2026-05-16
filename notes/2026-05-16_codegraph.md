# CodeGraph

- Repo: `colbymchenry/codegraph`
- URL: https://github.com/colbymchenry/codegraph
- Date: 2026-05-16
- Repo snapshot studied: `main` @ `7e617d819b74686f70eca5dddf5620868f4754bd`
- Why picked today: It is hot right now, clearly AI-adjacent, and unlike a lot of agent tooling repos it has a real systems problem to solve: compressing codebase exploration into a reusable local substrate instead of burning tokens on repeated file discovery.

## Executive summary
CodeGraph is a local semantic indexing engine for codebases, wrapped as both a CLI and an MCP server for Claude Code. The key move is not “search code better.” The key move is to precompute a graph of symbols, references, routes, and file metadata into SQLite, then expose that graph through token-cheap tools so an agent can answer architectural questions without repeatedly walking the filesystem.

The repo is stronger than the average MCP utility because it has actual internal layers: parsing, persistence, reference resolution, graph traversal, context synthesis, CLI flows, and always-on sync. It is also ambitious enough to be slightly fragile. Supporting 19+ languages, cross-framework route extraction, native-or-WASM SQLite, and file watching in one package creates lots of surface area.

## What they built
They built a TypeScript system that:
- scans a project and indexes supported source files through [`src/extraction/`](https://github.com/colbymchenry/codegraph/tree/7e617d819b74686f70eca5dddf5620868f4754bd/src/extraction)
- stores symbols, edges, files, unresolved references, and FTS indexes in SQLite via [`src/db/schema.sql`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/db/schema.sql)
- resolves imports and framework-specific references through [`src/resolution/`](https://github.com/colbymchenry/codegraph/tree/7e617d819b74686f70eca5dddf5620868f4754bd/src/resolution)
- traverses the resulting graph with query and BFS/DFS helpers in [`src/graph/`](https://github.com/colbymchenry/codegraph/tree/7e617d819b74686f70eca5dddf5620868f4754bd/src/graph)
- converts natural-language tasks into focused graph-backed context in [`src/context/index.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/context/index.ts)
- exposes everything as a CLI in [`src/bin/codegraph.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/bin/codegraph.ts) and an MCP tool surface in [`src/mcp/tools.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/mcp/tools.ts)

## Why it matters
This repo matters because it treats agent coding assistance as an indexing problem, not just a prompting problem. That is the right instinct.

A lot of agent tooling still burns most of its budget on finding the relevant files. CodeGraph tries to front-load that cost, keep everything local, and let later exploration run against a graph-plus-FTS substrate. If that pattern sticks, it is reusable well beyond Claude Code.

## Repo shape at a glance
Top-level structure:
- [`src/`](https://github.com/colbymchenry/codegraph/tree/7e617d819b74686f70eca5dddf5620868f4754bd/src): all product code
- [`__tests__/`](https://github.com/colbymchenry/codegraph/tree/7e617d819b74686f70eca5dddf5620868f4754bd/__tests__): unit, integration, security, sync, and evaluation coverage
- [`docs/`](https://github.com/colbymchenry/codegraph/tree/7e617d819b74686f70eca5dddf5620868f4754bd/docs): plans and search-quality documentation
- [`scripts/`](https://github.com/colbymchenry/codegraph/tree/7e617d819b74686f70eca5dddf5620868f4754bd/scripts): support scripts, including grammar patching
- [`package.json`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/package.json): exposes the real operating model, especially build, CLI, tests, and eval flows

Inside `src/`, the weight is concentrated in a few areas:
- [`src/extraction/`](https://github.com/colbymchenry/codegraph/tree/7e617d819b74686f70eca5dddf5620868f4754bd/src/extraction), about 7.3k lines: parsing, file scanning, grammar loading, language-specific extractors
- [`src/resolution/`](https://github.com/colbymchenry/codegraph/tree/7e617d819b74686f70eca5dddf5620868f4754bd/src/resolution), about 6.5k lines: import/reference resolution and framework-specific route handling
- [`src/db/`](https://github.com/colbymchenry/codegraph/tree/7e617d819b74686f70eca5dddf5620868f4754bd/src/db): persistence and query plumbing
- [`src/mcp/`](https://github.com/colbymchenry/codegraph/tree/7e617d819b74686f70eca5dddf5620868f4754bd/src/mcp): tool contracts and transport
- [`src/context/`](https://github.com/colbymchenry/codegraph/tree/7e617d819b74686f70eca5dddf5620868f4754bd/src/context): natural-language-to-context bridge

The repo shape says “indexer core with two product shells,” namely CLI and MCP.

## Layered architecture dissection
### High-level system shape
The system has six layers:
1. project discovery and CLI entry
2. file scanning and parsing
3. relational-plus-graph storage
4. reference and framework resolution
5. graph traversal plus context synthesis
6. external interfaces: CLI commands, MCP tools, and background watcher sync

### Main layers
### 1) CLI and lifecycle orchestration
[`src/bin/codegraph.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/bin/codegraph.ts) is not a thin wrapper. It handles installer mode, init/index/sync/status/query commands, colorful progress UX, Node 25 hard-blocking because of tree-sitter WASM crashes, and lazy loading to keep startup fast.

[`src/index.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/index.ts) is the composition root. It assembles the database connection, extraction orchestrator, resolver, graph manager, traverser, context builder, file lock, and watcher into one `CodeGraph` object.

### 2) File scanning and extraction
[`src/extraction/index.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/extraction/index.ts) is the heavy center of gravity. It:
- prefers `git ls-files` over naive directory walking so `.gitignore` behavior is inherited correctly
- hashes content for change detection
- batches file I/O separately from parse work
- parses via worker threads with timeouts and worker recycling to contain WASM memory issues
- falls back to full scan when git-based diffing is unavailable

[`src/extraction/grammars.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/extraction/grammars.ts) shows a practical design choice: load only the grammars actually needed for the languages present, and load them sequentially to dodge known `web-tree-sitter` race problems.

### 3) SQLite as semantic substrate
The schema in [`src/db/schema.sql`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/db/schema.sql) is simple but correct:
- `nodes` for symbols
- `edges` for relationships
- `files` for file-level tracking and hashes
- `unresolved_refs` for deferred resolution
- `nodes_fts` for FTS5-backed search
- `project_metadata` and schema versioning for lifecycle state

This is a good design choice. They are not forcing everything into “graph database” theater. They use SQLite tables plus targeted graph traversal, which is cheaper and more portable.

[`src/db/sqlite-adapter.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/db/sqlite-adapter.ts) is also revealing: they strongly prefer native `better-sqlite3`, but keep a WASM adapter as a portability fallback. That broadens installability at the cost of complexity and slower degraded-mode behavior.

### 4) Reference resolution and framework awareness
The most interesting structural move is that extraction does not try to perfectly understand every reference in one pass. Instead it records unresolved references, then [`src/resolution/`](https://github.com/colbymchenry/codegraph/tree/7e617d819b74686f70eca5dddf5620868f4754bd/src/resolution) cleans them up with language and framework logic.

[`src/resolution/frameworks/index.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/resolution/frameworks/index.ts) registers framework resolvers across Express, Django, Flask, FastAPI, Rails, Spring, Go routers, Rust web frameworks, ASP.NET, SwiftUI/UIKit/Vapor, and others.

A concrete example is [`src/resolution/frameworks/express.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/resolution/frameworks/express.ts), which pattern-matches route declarations, emits `route` nodes, and links them to handler functions. That is exactly the kind of cross-file semantic shortcut a coding agent actually benefits from.

### 5) Graph traversal and context building
[`src/graph/traversal.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/graph/traversal.ts) provides BFS/DFS traversal, caller/callee lookup, and impact-style expansion. One nice touch: BFS prioritizes `contains` and `calls` edges ahead of weaker reference edges, which helps the traversal discover internal structure before fanning out into noisy usage links.

[`src/context/index.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/context/index.ts) then bridges natural-language requests to graph queries. It extracts likely symbol names from prose, merges exact symbol lookup with semantic/FTS search, traverses outward, and formats a bounded context package. That is the real product interface, even more than the raw graph.

### 6) MCP and always-fresh sync
[`src/mcp/tools.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/mcp/tools.ts) defines the tool contract. The surface is intentionally split between cheap lookup tools (`search`, `callers`, `callees`, `impact`, `files`, `node`) and heavier context/explore tools. That separation is smart because it encodes context-budget discipline into the API itself.

[`src/sync/watcher.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/sync/watcher.ts) keeps the graph warm using native recursive `fs.watch`, debouncing changes and ignoring `.codegraph/` writes to avoid self-trigger loops.

### Request / data / control flow
Typical flow:
1. CLI or MCP entry opens a project through [`src/index.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/index.ts)
2. extraction in [`src/extraction/index.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/extraction/index.ts) scans visible files, parses them, and records nodes plus unresolved references
3. resolution in [`src/resolution/`](https://github.com/colbymchenry/codegraph/tree/7e617d819b74686f70eca5dddf5620868f4754bd/src/resolution) turns imports, symbol references, and framework route bindings into edges
4. graph queries in [`src/graph/`](https://github.com/colbymchenry/codegraph/tree/7e617d819b74686f70eca5dddf5620868f4754bd/src/graph) and context assembly in [`src/context/`](https://github.com/colbymchenry/codegraph/tree/7e617d819b74686f70eca5dddf5620868f4754bd/src/context) answer user questions
5. MCP tools in [`src/mcp/tools.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/mcp/tools.ts) package those answers for agent consumption
6. watcher sync in [`src/sync/watcher.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/sync/watcher.ts) incrementally refreshes the local graph as files change

## Key directories and files
- [`src/index.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/index.ts): composition root and main API surface
- [`src/bin/codegraph.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/bin/codegraph.ts): CLI, installer dispatch, status, UX, and lifecycle controls
- [`src/extraction/index.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/extraction/index.ts): scanning, hashing, batching, parsing orchestration, and incremental sync
- [`src/extraction/grammars.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/extraction/grammars.ts): lazy grammar loading and language detection
- [`src/db/schema.sql`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/db/schema.sql): semantic store design
- [`src/db/sqlite-adapter.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/db/sqlite-adapter.ts): native/WASM backend abstraction
- [`src/resolution/frameworks/`](https://github.com/colbymchenry/codegraph/tree/7e617d819b74686f70eca5dddf5620868f4754bd/src/resolution/frameworks): framework-aware symbol and route resolution
- [`src/graph/traversal.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/graph/traversal.ts): traversal logic and impact mechanics
- [`src/context/index.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/context/index.ts): the natural-language retrieval layer
- [`src/mcp/tools.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/mcp/tools.ts): tool contracts and token-budget strategy
- [`__tests__/evaluation/runner.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/__tests__/evaluation/runner.ts): a real evaluation harness, which is more serious than the average agent repo benchmark screenshot

## Important components
- `CodeGraph` in [`src/index.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/index.ts), the assembled domain object
- `ExtractionOrchestrator` in [`src/extraction/index.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/extraction/index.ts), the indexing engine
- `QueryBuilder` in [`src/db/queries.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/db/queries.ts), the SQL access layer
- `GraphTraverser` in [`src/graph/traversal.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/graph/traversal.ts), the graph-walking engine
- `ContextBuilder` in [`src/context/index.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/context/index.ts), the NL query reducer
- `ToolHandler` and tool definitions in [`src/mcp/tools.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/mcp/tools.ts), the external protocol surface
- `FileWatcher` in [`src/sync/watcher.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/sync/watcher.ts), the freshness loop

## Important knobs / configs / extension points
- include/exclude patterns and project config in [`src/config.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/config.ts)
- language support and grammar loading strategy in [`src/extraction/grammars.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/extraction/grammars.ts)
- framework resolver registration in [`src/resolution/frameworks/index.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/resolution/frameworks/index.ts)
- MCP output shaping and explore-call budgeting in [`src/mcp/tools.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/mcp/tools.ts)
- backend behavior when native SQLite is unavailable in [`src/db/sqlite-adapter.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/db/sqlite-adapter.ts)
- installer behavior and Claude-specific integration templates in [`src/installer/`](https://github.com/colbymchenry/codegraph/tree/7e617d819b74686f70eca5dddf5620868f4754bd/src/installer)

## Practical questions and answers
### What is the real product here?
A reusable local semantic cache for coding agents, not just another MCP server.

### What assumption does the system make?
That most exploration latency comes from repeated discovery, and that pre-indexing plus bounded graph expansion beats live filesystem wandering.

### Where is the deepest leverage?
In the combination of FTS-backed symbol search, deferred reference resolution, and graph-aware context assembly. Any one of those alone is useful. Together they create a much better agent substrate.

### Where would it fail in production?
Language breadth is the obvious risk. Every extra grammar, framework resolver, and fallback mode multiplies maintenance burden. The second risk is trust calibration. If the graph is stale or a resolver guesses wrong, an agent may act on a confidently incomplete map.

### Is the benchmark story convincing?
Partly. The benchmark framing in the README is directionally plausible, and the presence of an evaluation harness in [`__tests__/evaluation/runner.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/__tests__/evaluation/runner.ts) is better than pure marketing. But the strongest claims still depend on the quality of the task set, the explore prompts, and whether retrieval errors are being counted honestly.

### What would I copy?
The local-first retrieval substrate, the route-aware framework resolution, and the tool-surface split between cheap targeted lookups and heavier context builders.

### What would I avoid?
Packing every language and every framework into one repo forever without more modular boundaries. This architecture wants pluginization over time.

## What is smart
- Using SQLite plus graph traversal instead of chasing a heavier graph database story
- Preferring `git ls-files` to inherit real ignore semantics during scan
- Treating unresolved references as a first-class intermediate representation instead of pretending extraction can perfectly resolve everything immediately
- Prioritizing structural edges during BFS so context expansion stays informative longer
- Designing MCP tools around context-budget discipline, not just feature count
- Providing a native SQLite fast path while still having a portability fallback

## What is flawed or weak
- The repo is trying to do a lot: installer, CLI UX, parsing infra, resolution heuristics, watcher sync, MCP server, benchmarks. That is a lot of long-term maintenance burden for a relatively small project.
- Framework resolution is necessarily heuristic-heavy. That works great until it doesn’t, and the failure modes can be subtle.
- “19+ languages” is a nice headline, but it also signals a potentially endless compatibility treadmill.
- The project is tightly optimized around Claude Code usage today. That is fine tactically, but some product decisions may be overfit to one agent workflow.

## What we can learn / steal
- Build reusable semantic substrates instead of forcing agents to rediscover structure every run.
- Decompose understanding into extraction, deferred resolution, traversal, and presentation layers.
- Encode cost discipline into tool design. Tool shape affects agent quality.
- Local-first storage is still a strong product move when latency, privacy, and repeatability matter.

## How we could apply it
If we were building our own agent-facing repo intelligence layer, I would copy the broad pattern, not the exact implementation:
1. start with one or two languages only
2. keep SQLite as the default store
3. treat routes, handlers, jobs, and config edges as first-class nodes
4. add an evaluation harness early, not after shipping
5. make staleness and confidence visible so the agent knows when to distrust the graph

## Bottom line
CodeGraph is one of the better agent-tooling repos because it is trying to solve the right problem at the right layer. The big idea is not MCP, and it is not “AI coding.” The big idea is that codebase understanding gets much cheaper once you precompute structure and expose it through disciplined retrieval tools.

That is a real architectural lesson worth stealing.