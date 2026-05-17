# CodeGraph

- Repo: `colbymchenry/codegraph`
- URL: https://github.com/colbymchenry/codegraph
- Date: 2026-05-17
- Repo snapshot studied: `main` @ `7e617d819b74686f70eca5dddf5620868f4754bd`
- Why picked today: Hot on GitHub trending, directly relevant to AI coding workflows, and more interesting than the usual "agent wrapper" because it is trying to change the discovery economics of code exploration rather than just add another chat shell.

## Executive summary
CodeGraph is a local semantic indexer plus MCP server for codebases. The pitch is simple: precompute a code knowledge graph into SQLite, then let Claude Code query that graph instead of paying repeated grep/glab/read taxes every time it needs orientation. The repo is small enough to understand in one sitting, but substantial enough to show real systems thinking around parsing, indexing, traversal, caching, and agent-facing tool design.

The key idea is not just "build a code graph." The sharper move is packaging that graph as an AI-facing product with an installer, MCP tools, and context-shaping heuristics. It is trying to be infrastructure for agent exploration, not a generic static-analysis framework.

## What they built
They built a TypeScript CLI and library that:
- initializes a project-local `.codegraph/` directory
- parses source files across many languages via tree-sitter
- stores symbols, edges, file metadata, and unresolved references in SQLite
- resolves references into a traversable graph
- exposes search, context-building, caller/callee, impact, and file-tree queries to Claude Code via MCP
- optionally watches the filesystem and incrementally syncs changes

Core entry points live in [`src/index.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/index.ts), the CLI in [`src/bin/codegraph.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/bin/codegraph.ts), and MCP tool definitions in [`src/mcp/tools.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/mcp/tools.ts).

## Why it matters
Most AI coding sessions waste time on discovery. CodeGraph attacks that specific bottleneck. Instead of hoping the model finds the right files by repeated filesystem poking, it precomputes a graph and shapes queries into bounded, high-signal outputs.

That matters because the real cost in agentic coding is often not raw model IQ, it is context acquisition latency and tool-call churn.

## Repo shape at a glance
Top-level shape:
- [`src/`](https://github.com/colbymchenry/codegraph/tree/7e617d819b74686f70eca5dddf5620868f4754bd/src): product code
- [`src/bin/`](https://github.com/colbymchenry/codegraph/tree/7e617d819b74686f70eca5dddf5620868f4754bd/src/bin): CLI entrypoints
- [`src/extraction/`](https://github.com/colbymchenry/codegraph/tree/7e617d819b74686f70eca5dddf5620868f4754bd/src/extraction): parsing/indexing pipeline, grammar loading, worker-based extraction
- [`src/db/`](https://github.com/colbymchenry/codegraph/tree/7e617d819b74686f70eca5dddf5620868f4754bd/src/db): SQLite adapter, schema, migrations, queries
- [`src/resolution/`](https://github.com/colbymchenry/codegraph/tree/7e617d819b74686f70eca5dddf5620868f4754bd/src/resolution): import/path/reference resolution and framework detection
- [`src/graph/`](https://github.com/colbymchenry/codegraph/tree/7e617d819b74686f70eca5dddf5620868f4754bd/src/graph): traversal and graph query logic
- [`src/context/`](https://github.com/colbymchenry/codegraph/tree/7e617d819b74686f70eca5dddf5620868f4754bd/src/context): context assembly and ranking heuristics
- [`src/mcp/`](https://github.com/colbymchenry/codegraph/tree/7e617d819b74686f70eca5dddf5620868f4754bd/src/mcp): MCP server surface area
- [`src/sync/`](https://github.com/colbymchenry/codegraph/tree/7e617d819b74686f70eca5dddf5620868f4754bd/src/sync): file watching and auto-sync
- [`src/installer/`](https://github.com/colbymchenry/codegraph/tree/7e617d819b74686f70eca5dddf5620868f4754bd/src/installer): guided Claude Code installation/configuration
- [`__tests__/`](https://github.com/colbymchenry/codegraph/tree/7e617d819b74686f70eca5dddf5620868f4754bd/__tests__): test suite, including evaluation cases

The repo is basically six stacked layers: ingest, store, resolve, traverse, present-to-agents, and operational glue.

## Layered architecture dissection
### High-level system shape
The system shape is:
1. scan project files
2. parse source into nodes/edges/unresolved refs
3. persist graph state in SQLite
4. resolve names/imports/re-exports/framework routes into richer edges
5. answer graph queries through CLI and MCP
6. keep the graph fresh via sync and watch modes

The main façade is the [`CodeGraph` class](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/index.ts), which wires together database access, extraction, resolution, graph traversal, context building, and file watching.

### Main layers
**1. Interface layer**
- CLI: [`src/bin/codegraph.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/bin/codegraph.ts)
- MCP surface: [`src/mcp/tools.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/mcp/tools.ts)
- Installer: [`src/installer/index.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/installer/index.ts)

This is the productization layer. It turns a graph engine into something an agent can actually consume.

**2. Orchestration layer**
- Main API: [`src/index.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/index.ts)

This layer owns lifecycle, locking, indexing, sync, stats, watch control, and high-level query methods.

**3. Extraction layer**
- Index pipeline: [`src/extraction/index.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/extraction/index.ts)
- Tree-sitter parsing: [`src/extraction/tree-sitter.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/extraction/tree-sitter.ts)
- Parse worker: [`src/extraction/parse-worker.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/extraction/parse-worker.ts)
- Language-specific extractors like [`src/extraction/vue-extractor.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/extraction/vue-extractor.ts) and [`src/extraction/svelte-extractor.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/extraction/svelte-extractor.ts)

This is the hardest engineering layer. It manages file discovery, size limits, grammar loading, worker recycling, parse timeouts, retries, and storage handoff.

**4. Storage layer**
- Schema: [`src/db/schema.sql`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/db/schema.sql)
- Queries: [`src/db/queries.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/db/queries.ts)
- Adapter: [`src/db/sqlite-adapter.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/db/sqlite-adapter.ts)

SQLite is the product choice that makes the whole thing feel local, cheap, and shippable.

**5. Resolution and graph semantics layer**
- Import resolver: [`src/resolution/import-resolver.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/resolution/import-resolver.ts)
- Name matching: [`src/resolution/name-matcher.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/resolution/name-matcher.ts)
- Traversal: [`src/graph/traversal.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/graph/traversal.ts)
- Graph queries: [`src/graph/queries.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/graph/queries.ts)

This is where raw parse output becomes useful intelligence.

**6. Agent-context shaping layer**
- Context ranking/assembly: [`src/context/index.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/context/index.ts)
- Markdown formatting: [`src/context/formatter.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/context/formatter.ts)

This layer is unusually important. They are not just returning raw graph matches. They are curating what an agent sees.

### Request / data / control flow
Typical flow for `codegraph context` or an MCP call:
- user/agent asks a code question through [`src/bin/codegraph.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/bin/codegraph.ts) or [`src/mcp/tools.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/mcp/tools.ts)
- API methods on [`src/index.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/index.ts) call query/traversal/context builders
- context logic in [`src/context/index.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/context/index.ts) combines exact symbol extraction, FTS search, term boosting, traversal, import-resolution cleanup, and node caps
- traversal logic in [`src/graph/traversal.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/graph/traversal.ts) expands neighbors
- storage/query logic in [`src/db/queries.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/db/queries.ts) fetches nodes, edges, and FTS results
- response gets trimmed and formatted for agent consumption in [`src/mcp/tools.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/mcp/tools.ts)

Indexing flow is similarly layered:
- file scan and git-aware discovery in [`src/extraction/index.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/extraction/index.ts)
- parse in a worker thread via [`src/extraction/parse-worker.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/extraction/parse-worker.ts)
- write nodes/edges/unresolved refs into SQLite using [`src/db/queries.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/db/queries.ts)
- resolve deferred references using the resolver stack in [`src/resolution/`](https://github.com/colbymchenry/codegraph/tree/7e617d819b74686f70eca5dddf5620868f4754bd/src/resolution)

## Key directories and files
- [`package.json`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/package.json): shows the product stack clearly, especially the `better-sqlite3` optional native fast path and `node-sqlite3-wasm` fallback.
- [`src/index.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/index.ts): central façade and lifecycle API.
- [`src/extraction/index.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/extraction/index.ts): the real heart of the system, including git fast paths, batching, worker lifecycle, timeout handling, retries, and file storage rules.
- [`src/db/schema.sql`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/db/schema.sql): defines the graph model, FTS index, unresolved ref staging area, and file metadata tables.
- [`src/context/index.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/context/index.ts): ranking heuristics and context-budget management.
- [`src/mcp/tools.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/mcp/tools.ts): where the graph becomes an agent toolset, including aggressive output shaping.
- [`src/resolution/import-resolver.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/resolution/import-resolver.ts): handles aliased paths, import mapping, and re-export chasing.
- [`src/graph/traversal.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/graph/traversal.ts): BFS/DFS/caller/callee/impact/path logic.
- [`src/sync/watcher.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/sync/watcher.ts): debounced watch-mode freshness.
- [`README.md`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/README.md): strong product framing and benchmark narrative.

## Important components
**`CodeGraph` façade**
- [`src/index.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/index.ts)
- cleanly composes DB, extraction orchestrator, resolver, traverser, context builder, and watcher
- exposes both lifecycle and query APIs, so the public surface stays coherent

**`ExtractionOrchestrator`**
- [`src/extraction/index.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/extraction/index.ts)
- arguably the most valuable implementation in the repo
- does git-aware file discovery, bounded parallel I/O, worker recycling, parse timeout protection, retry passes, framework detection, and incremental sync

**SQLite schema with FTS + unresolved refs**
- [`src/db/schema.sql`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/db/schema.sql)
- smart split: parse first, resolve later
- unresolved references table is the pressure-release valve that keeps parsing simple and resolution composable

**ContextBuilder**
- [`src/context/index.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/context/index.ts)
- where the product gets noticeably opinionated
- combines symbol extraction, FTS, text search, multi-term boosting, CamelCase recovery, test-file suppression, diversity caps, and edge recovery

**MCP tool handler**
- [`src/mcp/tools.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/mcp/tools.ts)
- not a thin wrapper, it aggressively shapes outputs around context budgets
- `codegraph_explore` is basically a source-packing algorithm for agents

**Import/re-export resolver**
- [`src/resolution/import-resolver.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/resolution/import-resolver.ts)
- supports alias maps, package heuristics, and barrel chasing, which are table stakes if you want this to work on modern TS repos

## Important knobs / configs / extension points
- `.codegraph/config.json`, managed by [`src/config.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/config.ts)
- include/exclude globs
- `languages`
- `frameworks`
- `maxFileSize`
- `extractDocstrings`
- `trackCallSites`
- custom regex-based extraction patterns

Operational knobs worth noticing:
- worker parse timeout and recycle interval in [`src/extraction/index.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/extraction/index.ts)
- MCP output budgets in [`src/mcp/tools.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/mcp/tools.ts)
- debounce timing in [`src/sync/watcher.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/sync/watcher.ts)

## Practical questions and answers
**Q: Is this mostly a static analysis engine?**
A: Half yes, half no. The underlying mechanics are static analysis and graph storage, but the repo is really optimized around agent ergonomics. The context-builder and MCP surfaces are as important as the parser.

**Q: What assumption does the system make?**
A: That pre-indexed structure is a better primitive for code exploration than repeated live filesystem search. That assumption is strong for medium and large repos.

**Q: Where would it fail in production?**
A: On weird language corners, framework-specific magic, giant repos with pathological parse cases, or environments stuck on the WASM SQLite fallback where performance and locking behavior degrade.

**Q: Why SQLite instead of a graph database?**
A: Product pragmatism. Local install, zero services, good-enough graph queries, and FTS5 in one artifact beats shipping a "real graph DB" dependency.

**Q: Is the watch/sync story credible?**
A: Mostly yes. The design in [`src/sync/watcher.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/sync/watcher.ts) is sane, and the git-aware sync path in [`src/extraction/index.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/extraction/index.ts) is a strong practical shortcut.

**Q: What is the single most reusable idea here?**
A: Treat "what context should the agent see?" as a first-class ranking problem, not an afterthought.

## What is smart
- Using SQLite plus FTS5 instead of overbuilding infrastructure.
- Splitting extraction from resolution via `unresolved_refs`, which keeps the ingest pipeline robust.
- Git-aware scanning and sync, which is exactly the kind of practical optimization a tool like this needs.
- Worker recycling and timeout logic around tree-sitter/WASM, which shows they learned from ugly real-world failures.
- Aggressive context shaping in [`src/context/index.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/context/index.ts) and [`src/mcp/tools.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/mcp/tools.ts). This is where the repo stops being a toy.
- Surfacing the native-vs-WASM backend status directly to users, which is honest and operationally useful.

## What is flawed or weak
- The README benchmark story is compelling, but still largely vendor-style proof from the project itself. It is useful, but I would want more adversarial evaluation.
- The repo supports many languages, which is great for distribution, but broad language support almost always hides shallow corners. Some ecosystems will be first-class and some will be "good enough on happy paths."
- A lot of value depends on ranking heuristics in [`src/context/index.ts`](https://github.com/colbymchenry/codegraph/blob/7e617d819b74686f70eca5dddf5620868f4754bd/src/context/index.ts). That is fine, but it means behavior can feel magical when it works and mysterious when it does not.
- SQLite is the right call, but impact/path/traversal richness will eventually run into query-model limits if they keep pushing toward heavier graph semantics.
- The MCP output trimming logic is sensible, but any summarizing gateway risks hiding the one file that mattered.

## What we can learn / steal
- Build an intermediate representation once, then optimize the human or agent experience on top of it.
- Keep the storage layer embarrassingly simple if the product value is actually in query shaping.
- Design around real failure modes early: parse hangs, path alias weirdness, git submodules, stale locks, giant files, test-file noise.
- If a tool is meant for agents, output-budget design is not polish, it is core architecture.
- Use heuristics unapologetically, but isolate them in well-named components so they can evolve.

## How we could apply it
For our own tools, the directly transferable pattern is:
1. precompute a durable local model of the workspace
2. store enough structure to avoid repeated raw scanning
3. expose a small set of high-signal query surfaces
4. spend real effort on ranking, trimming, and packing context

If we built something adjacent, I would copy the local-first storage choice, the unresolved-reference staging model, and the idea that agent context assembly deserves its own subsystem.

## Bottom line
CodeGraph is one of the better recent "AI coding infrastructure" repos because it is not pretending the model alone solves code understanding. It treats discovery as a systems problem.

The best insight is this: the moat is not just parsing code into a graph, it is turning that graph into bounded, trustworthy, agent-usable context. That is the real product here.
