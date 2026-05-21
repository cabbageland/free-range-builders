# CodeGraph

- Repo: colbymchenry/codegraph
- URL: https://github.com/colbymchenry/codegraph
- Date: 2026-05-21
- Repo snapshot studied: main @ `4329a52becbef247a5641f6342d525dffd17192c`
- Why picked today: It was one of the hottest GitHub repos on May 21, 2026, it is directly relevant to agent coding workflows, and unlike generic "AI coding" wrappers it makes a concrete systems claim that is inspectable in source.

## Executive summary
CodeGraph is a local semantic indexing system for codebases, packaged as a CLI plus MCP server for coding agents. Its pitch is simple: stop paying for repeated grep-and-read exploration by precomputing a graph of symbols, references, routes, and file structure, then let agents query that graph directly.

The repo is more serious than the hype layer suggests. Under the README benchmark marketing, the actual implementation is a fairly disciplined TypeScript system built around tree-sitter extraction, SQLite storage, graph traversal, context shaping, and a practical installer layer for Claude Code, Cursor, Codex CLI, and opencode. The most important insight is that CodeGraph is not really a “knowledge graph product” first. It is a **cost-control and discovery-boundary product** for agents.

## What they built
They built a local code-intelligence stack with five main pieces:

1. a **CLI and installer surface** in [`src/bin/codegraph.ts`](https://github.com/colbymchenry/codegraph/blob/4329a52becbef247a5641f6342d525dffd17192c/src/bin/codegraph.ts) and [`src/installer/`](https://github.com/colbymchenry/codegraph/tree/4329a52becbef247a5641f6342d525dffd17192c/src/installer) that bootstraps agents and project setup
2. an **indexing pipeline** in [`src/extraction/`](https://github.com/colbymchenry/codegraph/tree/4329a52becbef247a5641f6342d525dffd17192c/src/extraction) that scans git-visible files, parses source with tree-sitter, and emits nodes plus unresolved references
3. a **storage and query layer** in [`src/db/`](https://github.com/colbymchenry/codegraph/tree/4329a52becbef247a5641f6342d525dffd17192c/src/db) that persists symbols, edges, files, unresolved references, and FTS indexes in SQLite
4. a **resolution and graph layer** in [`src/resolution/`](https://github.com/colbymchenry/codegraph/tree/4329a52becbef247a5641f6342d525dffd17192c/src/resolution) and [`src/graph/`](https://github.com/colbymchenry/codegraph/tree/4329a52becbef247a5641f6342d525dffd17192c/src/graph) that turns parsed facts into a queryable code graph
5. an **agent-facing MCP/context layer** in [`src/mcp/`](https://github.com/colbymchenry/codegraph/tree/4329a52becbef247a5641f6342d525dffd17192c/src/mcp) and [`src/context/`](https://github.com/colbymchenry/codegraph/tree/4329a52becbef247a5641f6342d525dffd17192c/src/context) that tries to give agents just enough architecture context without dumping huge files into the prompt

## Why it matters
Most coding agents are still inefficient archaeologists. They pay repeatedly to rediscover structure that could have been indexed once.

CodeGraph matters because it attacks the expensive part of agent coding, which is not generation but discovery. Its bet is that a fast, local, structured index can replace a lot of file-system thrash. Even if the benchmark numbers in [`README.md`](https://github.com/colbymchenry/codegraph/blob/4329a52becbef247a5641f6342d525dffd17192c/README.md) are self-authored and should be treated skeptically, the core product thesis is strong.

## Repo shape at a glance
Top-level shape:

- [`README.md`](https://github.com/colbymchenry/codegraph/blob/4329a52becbef247a5641f6342d525dffd17192c/README.md): positioning, setup, supported languages, and benchmark claims
- [`src/`](https://github.com/colbymchenry/codegraph/tree/4329a52becbef247a5641f6342d525dffd17192c/src): the real product code, roughly 100 source files
- [`__tests__/`](https://github.com/colbymchenry/codegraph/tree/4329a52becbef247a5641f6342d525dffd17192c/__tests__): a substantial test suite, including evaluation and integration coverage
- [`scripts/`](https://github.com/colbymchenry/codegraph/tree/4329a52becbef247a5641f6342d525dffd17192c/scripts): language-addition helpers, release scripts, and agent-eval harnesses
- [`docs/`](https://github.com/colbymchenry/codegraph/tree/4329a52becbef247a5641f6342d525dffd17192c/docs): light design notes rather than a giant docs platform
- [`package.json`](https://github.com/colbymchenry/codegraph/blob/4329a52becbef247a5641f6342d525dffd17192c/package.json): packaging, CLI entrypoints, and build/test scripts
- [`tsconfig.json`](https://github.com/colbymchenry/codegraph/blob/4329a52becbef247a5641f6342d525dffd17192c/tsconfig.json) and [`vitest.config.ts`](https://github.com/colbymchenry/codegraph/blob/4329a52becbef247a5641f6342d525dffd17192c/vitest.config.ts): TypeScript and test configuration

Inside [`src/`](https://github.com/colbymchenry/codegraph/tree/4329a52becbef247a5641f6342d525dffd17192c/src), the project divides into fairly clean subsystems:

- [`src/bin/`](https://github.com/colbymchenry/codegraph/tree/4329a52becbef247a5641f6342d525dffd17192c/src/bin): CLI commands and runtime guards
- [`src/installer/`](https://github.com/colbymchenry/codegraph/tree/4329a52becbef247a5641f6342d525dffd17192c/src/installer): agent config writing and install UX
- [`src/extraction/`](https://github.com/colbymchenry/codegraph/tree/4329a52becbef247a5641f6342d525dffd17192c/src/extraction): parsing, grammars, worker lifecycle, and language extractors
- [`src/db/`](https://github.com/colbymchenry/codegraph/tree/4329a52becbef247a5641f6342d525dffd17192c/src/db): schema, migrations, SQLite adapter, and query builder
- [`src/resolution/`](https://github.com/colbymchenry/codegraph/tree/4329a52becbef247a5641f6342d525dffd17192c/src/resolution): import/path resolution plus framework-specific route detection
- [`src/graph/`](https://github.com/colbymchenry/codegraph/tree/4329a52becbef247a5641f6342d525dffd17192c/src/graph): traversal and graph querying
- [`src/context/`](https://github.com/colbymchenry/codegraph/tree/4329a52becbef247a5641f6342d525dffd17192c/src/context): compact task-context assembly for agents
- [`src/mcp/`](https://github.com/colbymchenry/codegraph/tree/4329a52becbef247a5641f6342d525dffd17192c/src/mcp): MCP server transport and tool definitions
- [`src/sync/`](https://github.com/colbymchenry/codegraph/tree/4329a52becbef247a5641f6342d525dffd17192c/src/sync): file-watcher and git-hook sync logic

## Layered architecture dissection
### High-level system shape
The system shape is:

1. install and initialize a project
2. scan source files, preferably through git-visible file discovery
3. parse files into symbols and references with tree-sitter and language-specific extractors
4. store nodes, edges, files, and unresolved references in SQLite
5. resolve imports and framework routing into graph edges
6. answer agent queries through MCP tools or built context bundles
7. keep the index warm with sync and file watching

That shape is practical. It is not trying to be a cloud service, an embedding pipeline, or a giant IDE replacement.

### Main layers
**1. Bootstrap and UX layer**

[`src/bin/codegraph.ts`](https://github.com/colbymchenry/codegraph/blob/4329a52becbef247a5641f6342d525dffd17192c/src/bin/codegraph.ts) is more important than it first looks. It handles CLI verbs, lazy-loads heavy modules to keep startup fast, and even hard-blocks Node 25 because of known WASM crashes. That is a very pragmatic sign: this repo is optimized for surviving real user environments, not just looking elegant in a diagram.

The installer code in [`src/installer/`](https://github.com/colbymchenry/codegraph/tree/4329a52becbef247a5641f6342d525dffd17192c/src/installer) turns the product into an agent add-on rather than a library. It writes config and instruction files into agent-specific surfaces instead of requiring users to hand-wire MCP setup.

**2. Extraction and indexing layer**

[`src/extraction/index.ts`](https://github.com/colbymchenry/codegraph/blob/4329a52becbef247a5641f6342d525dffd17192c/src/extraction/index.ts) is the real ingestion spine. It prefers git-visible file enumeration over naive directory walking, respects ignore patterns, hashes file content, batches file I/O, and pushes parse work through a worker thread. The design detail I like most is that it explicitly recycles parse workers because WASM memory grows but does not shrink. That is the kind of boring systems realism that keeps tools stable.

The extractor layer is not one parser pretending all languages look alike. [`src/extraction/languages/`](https://github.com/colbymchenry/codegraph/tree/4329a52becbef247a5641f6342d525dffd17192c/src/extraction/languages) contains language-specific logic, while custom extractors like [`src/extraction/svelte-extractor.ts`](https://github.com/colbymchenry/codegraph/blob/4329a52becbef247a5641f6342d525dffd17192c/src/extraction/svelte-extractor.ts), [`src/extraction/vue-extractor.ts`](https://github.com/colbymchenry/codegraph/blob/4329a52becbef247a5641f6342d525dffd17192c/src/extraction/vue-extractor.ts), and [`src/extraction/liquid-extractor.ts`](https://github.com/colbymchenry/codegraph/blob/4329a52becbef247a5641f6342d525dffd17192c/src/extraction/liquid-extractor.ts) show they are willing to special-case awkward formats.

**3. Storage and query layer**

[`src/db/schema.sql`](https://github.com/colbymchenry/codegraph/blob/4329a52becbef247a5641f6342d525dffd17192c/src/db/schema.sql) makes the data model very legible. The core objects are `nodes`, `edges`, `files`, and `unresolved_refs`, with an FTS5 virtual table over symbol fields. This is not a mysterious graph engine. It is a sensible SQLite-backed fact store with graph semantics layered on top.

That is a good trade. SQLite keeps everything local, debuggable, and easy to ship. It also keeps the product honest, because the design has to fit a real storage model instead of hand-waving about “semantic layers.”

**4. Resolution and graph layer**

Parsing alone is not enough, so [`src/resolution/import-resolver.ts`](https://github.com/colbymchenry/codegraph/blob/4329a52becbef247a5641f6342d525dffd17192c/src/resolution/import-resolver.ts) resolves relative imports, tsconfig-style path aliases, and language-specific import patterns. Then framework resolvers in [`src/resolution/frameworks/`](https://github.com/colbymchenry/codegraph/tree/4329a52becbef247a5641f6342d525dffd17192c/src/resolution/frameworks) add higher-level structure like Django, Express, NestJS, Rails, Spring, Go, Rust, ASP.NET, and Vapor routes.

This is a big deal. It means CodeGraph is not just indexing syntax trees. It is trying to lift framework conventions into queryable graph edges, which is much closer to the questions builders actually ask.

**5. Agent context and MCP layer**

[`src/context/index.ts`](https://github.com/colbymchenry/codegraph/blob/4329a52becbef247a5641f6342d525dffd17192c/src/context/index.ts) builds task context by combining search plus graph traversal, then caps output aggressively. [`src/mcp/tools.ts`](https://github.com/colbymchenry/codegraph/blob/4329a52becbef247a5641f6342d525dffd17192c/src/mcp/tools.ts) is especially revealing: it contains adaptive output budgets, container-node summarization, line-number injection, and other prompt-shaping tricks to keep the graph useful without flooding the model.

That is the deepest product insight in the repo. The hard problem is not only extracting structure. It is packaging structure into an agent-sized payload.

**6. Freshness layer**

[`src/sync/watcher.ts`](https://github.com/colbymchenry/codegraph/blob/4329a52becbef247a5641f6342d525dffd17192c/src/sync/watcher.ts) provides debounced, native file-event syncing, while [`src/sync/git-hooks.ts`](https://github.com/colbymchenry/codegraph/blob/4329a52becbef247a5641f6342d525dffd17192c/src/sync/git-hooks.ts) covers repository-driven refresh paths. This is a necessary layer because stale indexes kill trust quickly.

### Request / data / control flow
Typical flow:

1. The user runs [`codegraph install`](https://github.com/colbymchenry/codegraph/blob/4329a52becbef247a5641f6342d525dffd17192c/src/bin/codegraph.ts) or the zero-arg installer path.
2. Project setup creates local config and later [`codegraph init`](https://github.com/colbymchenry/codegraph/blob/4329a52becbef247a5641f6342d525dffd17192c/src/bin/codegraph.ts) builds a `.codegraph/` index.
3. [`src/extraction/index.ts`](https://github.com/colbymchenry/codegraph/blob/4329a52becbef247a5641f6342d525dffd17192c/src/extraction/index.ts) scans files, parses them, stores nodes and unresolved references, and records file metadata.
4. [`src/resolution/`](https://github.com/colbymchenry/codegraph/tree/4329a52becbef247a5641f6342d525dffd17192c/src/resolution) resolves links between symbols, imports, and route handlers into graph edges.
5. The agent calls MCP tools from [`src/mcp/tools.ts`](https://github.com/colbymchenry/codegraph/blob/4329a52becbef247a5641f6342d525dffd17192c/src/mcp/tools.ts), or context assembly from [`src/context/`](https://github.com/colbymchenry/codegraph/tree/4329a52becbef247a5641f6342d525dffd17192c/src/context), to answer architecture questions.
6. [`src/sync/watcher.ts`](https://github.com/colbymchenry/codegraph/blob/4329a52becbef247a5641f6342d525dffd17192c/src/sync/watcher.ts) keeps the local graph current as files change.

The repo is basically an extraction pipeline plus a careful prompt-budgeting layer wrapped in agent ergonomics.

## Key directories and files
- [`src/index.ts`](https://github.com/colbymchenry/codegraph/blob/4329a52becbef247a5641f6342d525dffd17192c/src/index.ts): the central `CodeGraph` class and subsystem wiring
- [`src/bin/codegraph.ts`](https://github.com/colbymchenry/codegraph/blob/4329a52becbef247a5641f6342d525dffd17192c/src/bin/codegraph.ts): CLI entrypoint and operational guardrails
- [`src/extraction/index.ts`](https://github.com/colbymchenry/codegraph/blob/4329a52becbef247a5641f6342d525dffd17192c/src/extraction/index.ts): indexing orchestration, file selection, hashing, and parse lifecycle
- [`src/extraction/parse-worker.ts`](https://github.com/colbymchenry/codegraph/blob/4329a52becbef247a5641f6342d525dffd17192c/src/extraction/parse-worker.ts): worker-thread isolation for parsing
- [`src/db/schema.sql`](https://github.com/colbymchenry/codegraph/blob/4329a52becbef247a5641f6342d525dffd17192c/src/db/schema.sql): the actual persistent model
- [`src/resolution/import-resolver.ts`](https://github.com/colbymchenry/codegraph/blob/4329a52becbef247a5641f6342d525dffd17192c/src/resolution/import-resolver.ts): path/import matching and alias logic
- [`src/resolution/frameworks/index.ts`](https://github.com/colbymchenry/codegraph/blob/4329a52becbef247a5641f6342d525dffd17192c/src/resolution/frameworks/index.ts): registry of framework-aware resolvers
- [`src/context/index.ts`](https://github.com/colbymchenry/codegraph/blob/4329a52becbef247a5641f6342d525dffd17192c/src/context/index.ts): task-context assembly and filtering
- [`src/mcp/tools.ts`](https://github.com/colbymchenry/codegraph/blob/4329a52becbef247a5641f6342d525dffd17192c/src/mcp/tools.ts): tool surface and context-budget policy
- [`src/sync/watcher.ts`](https://github.com/colbymchenry/codegraph/blob/4329a52becbef247a5641f6342d525dffd17192c/src/sync/watcher.ts): debounced file-watcher freshness loop
- [`__tests__/`](https://github.com/colbymchenry/codegraph/tree/4329a52becbef247a5641f6342d525dffd17192c/__tests__): useful signal that the team cares about regression control, not just demos
- [`scripts/agent-eval/`](https://github.com/colbymchenry/codegraph/tree/4329a52becbef247a5641f6342d525dffd17192c/scripts/agent-eval): the self-benchmark harness behind the headline claims

## Important components
- **`CodeGraph`** in [`src/index.ts`](https://github.com/colbymchenry/codegraph/blob/4329a52becbef247a5641f6342d525dffd17192c/src/index.ts), which acts as the top-level composition root
- **`ExtractionOrchestrator`** in [`src/extraction/index.ts`](https://github.com/colbymchenry/codegraph/blob/4329a52becbef247a5641f6342d525dffd17192c/src/extraction/index.ts), the ingestion backbone
- **SQLite schema plus query builder** in [`src/db/schema.sql`](https://github.com/colbymchenry/codegraph/blob/4329a52becbef247a5641f6342d525dffd17192c/src/db/schema.sql) and [`src/db/queries.ts`](https://github.com/colbymchenry/codegraph/blob/4329a52becbef247a5641f6342d525dffd17192c/src/db/queries.ts), where the semantic index becomes operational
- **framework resolvers** in [`src/resolution/frameworks/`](https://github.com/colbymchenry/codegraph/tree/4329a52becbef247a5641f6342d525dffd17192c/src/resolution/frameworks), which push it beyond plain symbol lookup
- **`ContextBuilder`** in [`src/context/index.ts`](https://github.com/colbymchenry/codegraph/blob/4329a52becbef247a5641f6342d525dffd17192c/src/context/index.ts), which decides what information an agent should actually see
- **MCP tool output-budget logic** in [`src/mcp/tools.ts`](https://github.com/colbymchenry/codegraph/blob/4329a52becbef247a5641f6342d525dffd17192c/src/mcp/tools.ts), which is likely where a lot of real-world UX quality comes from

## Important knobs / configs / extension points
- [`package.json`](https://github.com/colbymchenry/codegraph/blob/4329a52becbef247a5641f6342d525dffd17192c/package.json) defines CLI surfaces like `install`, `init`, `index`, `sync`, `context`, and `files`
- [`src/db/schema.sql`](https://github.com/colbymchenry/codegraph/blob/4329a52becbef247a5641f6342d525dffd17192c/src/db/schema.sql) defines what structural facts are even queryable
- [`src/extraction/grammars.ts`](https://github.com/colbymchenry/codegraph/blob/4329a52becbef247a5641f6342d525dffd17192c/src/extraction/grammars.ts) and [`src/extraction/languages/`](https://github.com/colbymchenry/codegraph/tree/4329a52becbef247a5641f6342d525dffd17192c/src/extraction/languages) control language support
- [`src/resolution/path-aliases.ts`](https://github.com/colbymchenry/codegraph/blob/4329a52becbef247a5641f6342d525dffd17192c/src/resolution/path-aliases.ts) is a useful extension point for real-world TS/JS repos
- [`src/resolution/frameworks/index.ts`](https://github.com/colbymchenry/codegraph/blob/4329a52becbef247a5641f6342d525dffd17192c/src/resolution/frameworks/index.ts) makes framework-aware routing expandable
- [`src/mcp/tools.ts`](https://github.com/colbymchenry/codegraph/blob/4329a52becbef247a5641f6342d525dffd17192c/src/mcp/tools.ts) contains the tuning knobs for output size, file count, relationship display, and line-number behavior
- [`src/sync/watcher.ts`](https://github.com/colbymchenry/codegraph/blob/4329a52becbef247a5641f6342d525dffd17192c/src/sync/watcher.ts) exposes debounce timing and freshness behavior

## Practical questions and answers
**Is this just symbol search with prettier branding?**
No. Symbol search is part of it, but the more interesting layer is the combination of symbol extraction, reference resolution, framework route inference, graph traversal, and budgeted task-context generation.

**What is the real product advantage?**
The repo’s strongest idea is not “graph” by itself. It is that agent exploration should happen against a precomputed local structure, then be aggressively compressed before it hits prompt context.

**Where is the implementation most impressive?**
The operational details. Git-aware file enumeration, worker recycling for WASM memory, Node-version guardrails, framework-specific route resolvers, and prompt-budget logic all suggest the author has felt the actual failure modes.

**What is most likely overstated?**
The benchmark halo. The headline savings in [`README.md`](https://github.com/colbymchenry/codegraph/blob/4329a52becbef247a5641f6342d525dffd17192c/README.md) are interesting, but they come from the project’s own evaluation harness in [`scripts/agent-eval/`](https://github.com/colbymchenry/codegraph/tree/4329a52becbef247a5641f6342d525dffd17192c/scripts/agent-eval). That is evidence, not neutral proof.

**Where would this fail first?**
At the edges of semantic ambiguity, dynamic behavior, and stale or partial indexing. Static extraction gets you far, but highly dynamic frameworks, runtime metaprogramming, and generated code will always punch holes in a graph like this.

**What does the repo understand better than many competitors?**
That graph quality alone is not enough. If the MCP/tool payload is too fat, the agent still loses. The repo pays a lot of attention to context shaping, which is where many “smart index” projects quietly fall apart.

## What is smart
- The architecture is local-first and technically honest.
- SQLite is a good substrate here: simple, portable, inspectable.
- The extractor system is language-aware instead of pretending generic parsing is enough.
- Framework route resolvers are a high-leverage addition because they connect code structure to real app behavior.
- The prompt-budgeting logic in [`src/mcp/tools.ts`](https://github.com/colbymchenry/codegraph/blob/4329a52becbef247a5641f6342d525dffd17192c/src/mcp/tools.ts) shows unusually good taste.
- The repo has real test surface, not just a README demo path.

## What is flawed or weak
- The README marketing is stronger than the evidentiary standard. The benchmarks are useful but still house-produced.
- The repo is large enough now that it risks becoming a pile of exceptions for every language and framework edge case.
- Static graph extraction will always underrepresent dynamic runtime behavior.
- Agent integration is a strength, but also a dependency trap. If agent vendors change conventions, installer upkeep grows fast.
- The product claim can sound like “repository understanding,” but the implementation is still primarily a static structural accelerator.

## What we can learn / steal
- Precompute structure once, then spend effort on payload shaping.
- Use ordinary storage tech for ambitious products when it keeps the system inspectable.
- Add framework-specific understanding only where it changes practical questions users ask.
- Treat parser memory and environment instability as first-class product concerns.
- Build tooling that reduces discovery cost before trying to improve model reasoning.

## How we could apply it
If we were building internal agent tooling, I would copy this pattern:

1. git-aware corpus selection
2. language-specific structural extraction
3. small durable local store for symbols and edges
4. targeted higher-level resolvers for the frameworks we actually use
5. a strict context-budget layer that returns structure before raw code

That seems especially valuable for large app repos where the model keeps paying rediscovery tax.

## Bottom line
CodeGraph is one of the more interesting current agent-tooling repos because it focuses on the real bottleneck, which is discovery cost, not model theatrics.

My main takeaway: the best part of the repo is not that it builds a graph. It is that it treats **graph extraction, graph freshness, and graph-to-prompt compression** as one integrated system.