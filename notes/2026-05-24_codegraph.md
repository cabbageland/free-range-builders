# CodeGraph

- Repo: `colbymchenry/codegraph`
- URL: https://github.com/colbymchenry/codegraph
- Date: 2026-05-24
- Repo snapshot studied: `main` @ `1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e`
- Why picked today: It was on GitHub Trending on 2026-05-24, it is AI-tooling-adjacent rather than pure LLM wrapper fluff, and the implementation is much more serious than the marketing pitch suggests.

## Executive summary
CodeGraph is a local code-intelligence layer for coding agents. The product idea is simple: pre-index a repo into a SQLite-backed symbol graph, then expose that graph through MCP tools so Claude Code, Cursor, Codex CLI, and similar agents stop doing endless grep/read loops. The interesting part is that the repo is not just a parser plus database. It is a full retrieval-and-behavior-shaping system: graph extraction, reference resolution, SQLite query surfaces, MCP tool design, installer/config wiring for multiple agents, and benchmark-driven prompt/tool tuning.

The most important insight is that the repo understands the real bottleneck correctly. The problem is not merely “find symbols faster.” The problem is “make agents answer directly from a bounded structural index instead of spawning expensive exploration behavior.” That idea shows up everywhere, from [`src/mcp/server-instructions.ts`](https://github.com/colbymchenry/codegraph/blob/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/mcp/server-instructions.ts) to the payload-budget logic in [`src/mcp/tools.ts`](https://github.com/colbymchenry/codegraph/blob/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/mcp/tools.ts) to the benchmark writeups in [`docs/benchmarks/`](https://github.com/colbymchenry/codegraph/tree/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/docs/benchmarks).

## What they built
They built a CLI + MCP server that turns a source tree into a local knowledge graph. The public surfaces are:

- a CLI in [`src/bin/codegraph.ts`](https://github.com/colbymchenry/codegraph/blob/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/bin/codegraph.ts)
- the core `CodeGraph` lifecycle/orchestration class in [`src/index.ts`](https://github.com/colbymchenry/codegraph/blob/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/index.ts)
- a SQLite schema and query layer in [`src/db/`](https://github.com/colbymchenry/codegraph/tree/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/db)
- extraction and indexing logic in [`src/extraction/`](https://github.com/colbymchenry/codegraph/tree/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/extraction)
- cross-file resolution and framework heuristics in [`src/resolution/`](https://github.com/colbymchenry/codegraph/tree/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/resolution)
- graph traversal/context construction in [`src/graph/`](https://github.com/colbymchenry/codegraph/tree/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/graph) and [`src/context/`](https://github.com/colbymchenry/codegraph/tree/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/context)
- MCP transport and tools in [`src/mcp/`](https://github.com/colbymchenry/codegraph/tree/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/mcp)
- installer and agent config writers in [`src/installer/`](https://github.com/colbymchenry/codegraph/tree/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/installer)
- file watching and sync plumbing in [`src/sync/`](https://github.com/colbymchenry/codegraph/tree/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/sync)

## Why it matters
This repo matters because it attacks a real weakness in coding agents: they burn money and latency on discovery, not just on reasoning. CodeGraph’s pitch is that a repo should be pre-digested into a graph so the agent can ask structural questions cheaply.

That is not novel in the abstract. The useful part is that this implementation is opinionated about agent ergonomics, not just parsing theory. It ships installer flows, instruction templates, MCP server behavior, trace/context/explore tools, and ongoing benchmark loops specifically to change how the agent behaves in practice.

## Repo shape at a glance
Top-level structure:

- [`src/`](https://github.com/colbymchenry/codegraph/tree/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src): all runtime code
  - [`src/bin/`](https://github.com/colbymchenry/codegraph/tree/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/bin): CLI entrypoints, uninstall, Node runtime guards
  - [`src/db/`](https://github.com/colbymchenry/codegraph/tree/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/db): SQLite schema, migrations, query adapter
  - [`src/extraction/`](https://github.com/colbymchenry/codegraph/tree/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/extraction): scanning, grammar loading, parse workers, language-specific extractors
  - [`src/resolution/`](https://github.com/colbymchenry/codegraph/tree/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/resolution): import/path/framework/reference resolution and heuristic edge synthesis
  - [`src/graph/`](https://github.com/colbymchenry/codegraph/tree/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/graph): traversal and higher-level graph queries
  - [`src/context/`](https://github.com/colbymchenry/codegraph/tree/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/context): task-oriented retrieval and formatting
  - [`src/search/`](https://github.com/colbymchenry/codegraph/tree/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/search): query parsing and search utilities
  - [`src/mcp/`](https://github.com/colbymchenry/codegraph/tree/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/mcp): MCP server, transport, tool definitions, instruction text
  - [`src/installer/`](https://github.com/colbymchenry/codegraph/tree/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/installer): multi-agent installer/config layer
  - [`src/sync/`](https://github.com/colbymchenry/codegraph/tree/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/sync): watcher and sync hooks
- [`__tests__/`](https://github.com/colbymchenry/codegraph/tree/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/__tests__): a large test surface covering extraction, DB behavior, MCP behavior, installers, watchers, security, and benchmarks
- [`docs/benchmarks/`](https://github.com/colbymchenry/codegraph/tree/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/docs/benchmarks): performance experiments that directly influence product direction
- [`docs/design/`](https://github.com/colbymchenry/codegraph/tree/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/docs/design): design notes for tricky graph-coverage problems
- [`scripts/`](https://github.com/colbymchenry/codegraph/tree/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/scripts): packaging, evaluation, and install helpers

This is a solid shape. It is not “one giant parser file.” It is a product repo with meaningful subsystem boundaries.

## Layered architecture dissection
### High-level system shape
The architecture is roughly:

1. scan files
2. parse them into symbol/reference extraction results
3. persist nodes, edges, file metadata, and unresolved references into SQLite
4. resolve cross-file references and framework-specific links
5. expose structural queries over CLI and MCP
6. keep the index warm with sync/watch behavior
7. steer agent usage with instructions plus bounded tool output

### Main layers
**1. CLI and lifecycle shell**

[`src/bin/codegraph.ts`](https://github.com/colbymchenry/codegraph/blob/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/bin/codegraph.ts) handles command routing, environment checks, installer invocation, and UX. [`src/index.ts`](https://github.com/colbymchenry/codegraph/blob/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/index.ts) then acts as the façade tying DB, extraction, resolution, traversal, context building, and file watching together.

**2. Storage layer**

The schema in [`src/db/schema.sql`](https://github.com/colbymchenry/codegraph/blob/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/db/schema.sql) is the system’s backbone. The core objects are `nodes`, `edges`, `files`, `unresolved_refs`, and an FTS5 virtual table `nodes_fts`. This is a pragmatic choice. SQLite plus FTS is enough for local-first developer tooling, and much simpler to ship than an external graph database.

**3. Extraction/indexing layer**

[`src/extraction/index.ts`](https://github.com/colbymchenry/codegraph/blob/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/extraction/index.ts) is doing more than “parse files.” It decides how to scan repos, when to trust `git ls-files`, how to avoid huge blobs, how to batch I/O, how to recycle parse workers to reclaim WASM memory, and how to fall back when git-based discovery is unavailable. This is one of the strongest parts of the repo because it shows operational realism.

**4. Resolution layer**

[`src/resolution/index.ts`](https://github.com/colbymchenry/codegraph/blob/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/resolution/index.ts) handles the ugly middle stage between raw symbol extraction and actually useful graph edges. It combines import resolution, alias handling, framework detection, and bounded caches. The design notes in [`docs/design/callback-edge-synthesis.md`](https://github.com/colbymchenry/codegraph/blob/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/docs/design/callback-edge-synthesis.md) show they are explicitly chasing dynamic-dispatch gaps, not pretending static parsing alone is enough.

**5. Graph/query/context layer**

[`src/graph/queries.ts`](https://github.com/colbymchenry/codegraph/blob/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/graph/queries.ts) and [`src/context/index.ts`](https://github.com/colbymchenry/codegraph/blob/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/context/index.ts) convert the stored graph into task-shaped retrieval. This is where “symbol graph” becomes “usable answer surface.” The context builder is deliberately optimized for small, bounded outputs, shallow traversal, and high-information node kinds.

**6. MCP behavior layer**

[`src/mcp/index.ts`](https://github.com/colbymchenry/codegraph/blob/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/mcp/index.ts), [`src/mcp/tools.ts`](https://github.com/colbymchenry/codegraph/blob/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/mcp/tools.ts), and [`src/mcp/server-instructions.ts`](https://github.com/colbymchenry/codegraph/blob/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/mcp/server-instructions.ts) are effectively the product surface. The repo understands that tool semantics, tool budgets, and prompt steering are part of the architecture, not an afterthought.

**7. Distribution/config layer**

[`src/installer/index.ts`](https://github.com/colbymchenry/codegraph/blob/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/installer/index.ts) exists because this is not just a library. It is trying to land inside real agent environments and stay configured across Claude Code, Cursor, Codex CLI, opencode, and Hermes.

### Request / data / control flow
A typical control flow looks like:

- user runs `codegraph init -i` via [`src/bin/codegraph.ts`](https://github.com/colbymchenry/codegraph/blob/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/bin/codegraph.ts)
- `CodeGraph` in [`src/index.ts`](https://github.com/colbymchenry/codegraph/blob/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/index.ts) initializes the directory + database
- the orchestrator in [`src/extraction/index.ts`](https://github.com/colbymchenry/codegraph/blob/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/extraction/index.ts) scans files, parses sources, and stores raw graph material
- the resolver in [`src/resolution/index.ts`](https://github.com/colbymchenry/codegraph/blob/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/resolution/index.ts) turns unresolved refs into edges and framework-aware links
- the MCP server in [`src/mcp/index.ts`](https://github.com/colbymchenry/codegraph/blob/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/mcp/index.ts) opens the nearest initialized project and exposes tools
- tool handlers in [`src/mcp/tools.ts`](https://github.com/colbymchenry/codegraph/blob/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/mcp/tools.ts) query the DB/graph/context layers and emit bounded responses
- file updates trigger debounced sync in [`src/sync/watcher.ts`](https://github.com/colbymchenry/codegraph/blob/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/sync/watcher.ts)

## Key directories and files
- [`package.json`](https://github.com/colbymchenry/codegraph/blob/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/package.json): shows the repo’s packaging philosophy, minimal runtime deps, and bundled binary entrypoint
- [`src/index.ts`](https://github.com/colbymchenry/codegraph/blob/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/index.ts): central façade
- [`src/db/schema.sql`](https://github.com/colbymchenry/codegraph/blob/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/db/schema.sql): core persistence model
- [`src/extraction/index.ts`](https://github.com/colbymchenry/codegraph/blob/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/extraction/index.ts): file scanning/indexing pipeline
- [`src/resolution/index.ts`](https://github.com/colbymchenry/codegraph/blob/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/resolution/index.ts): cross-file linking brain
- [`src/context/index.ts`](https://github.com/colbymchenry/codegraph/blob/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/context/index.ts): task-context builder
- [`src/mcp/tools.ts`](https://github.com/colbymchenry/codegraph/blob/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/mcp/tools.ts): the actual product behavior surface
- [`src/mcp/server-instructions.ts`](https://github.com/colbymchenry/codegraph/blob/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/mcp/server-instructions.ts): agent-steering logic encoded as system guidance
- [`src/installer/index.ts`](https://github.com/colbymchenry/codegraph/blob/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/installer/index.ts): distribution/config wedge
- [`docs/benchmarks/answer-directly-vs-explore-agent.md`](https://github.com/colbymchenry/codegraph/blob/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/docs/benchmarks/answer-directly-vs-explore-agent.md): benchmark evidence for the product’s main UX claim
- [`docs/benchmarks/call-sequence-analysis.md`](https://github.com/colbymchenry/codegraph/blob/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/docs/benchmarks/call-sequence-analysis.md): unusually honest analysis of how agent/tool behavior really plays out

## Important components
- **`CodeGraph` façade** in [`src/index.ts`](https://github.com/colbymchenry/codegraph/blob/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/index.ts): lifecycle entrypoint for init/open/index/sync/watch
- **ExtractionOrchestrator** in [`src/extraction/index.ts`](https://github.com/colbymchenry/codegraph/blob/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/extraction/index.ts): scan/parse/store coordinator
- **ReferenceResolver** in [`src/resolution/index.ts`](https://github.com/colbymchenry/codegraph/blob/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/resolution/index.ts): ambiguous cross-file meaning-maker
- **GraphQueryManager** in [`src/graph/queries.ts`](https://github.com/colbymchenry/codegraph/blob/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/graph/queries.ts): traversal-backed context/dependency queries
- **ContextBuilder** in [`src/context/index.ts`](https://github.com/colbymchenry/codegraph/blob/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/context/index.ts): converts natural-language task intent into graph-shaped retrieval
- **MCPServer** in [`src/mcp/index.ts`](https://github.com/colbymchenry/codegraph/blob/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/mcp/index.ts): transport and lifecycle bridge into coding agents
- **tool budget logic** in [`src/mcp/tools.ts`](https://github.com/colbymchenry/codegraph/blob/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/mcp/tools.ts): this is where they aggressively control payload size, line numbering, and per-project exploration budgets
- **FileWatcher** in [`src/sync/watcher.ts`](https://github.com/colbymchenry/codegraph/blob/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/sync/watcher.ts): keeps the graph current without requiring full reindexing

## Important knobs / configs / extension points
- SQLite schema and FTS design in [`src/db/schema.sql`](https://github.com/colbymchenry/codegraph/blob/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/db/schema.sql)
- parser/runtime behavior such as worker recycle and parse timeout in [`src/extraction/index.ts`](https://github.com/colbymchenry/codegraph/blob/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/extraction/index.ts)
- search filtering grammar in [`src/search/query-parser.ts`](https://github.com/colbymchenry/codegraph/blob/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/search/query-parser.ts)
- MCP instruction strategy in [`src/mcp/server-instructions.ts`](https://github.com/colbymchenry/codegraph/blob/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/mcp/server-instructions.ts)
- output-budget and tool-shaping heuristics in [`src/mcp/tools.ts`](https://github.com/colbymchenry/codegraph/blob/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/mcp/tools.ts)
- multi-target install behavior in [`src/installer/index.ts`](https://github.com/colbymchenry/codegraph/blob/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/src/installer/index.ts)

## Practical questions and answers
**How much of this repo is parser tech versus product plumbing?**
A lot of the repo’s value is product plumbing. The extraction/resolution core matters, but installer support, instructions, sync, and MCP tool semantics are what make it usable.

**Why SQLite instead of a dedicated graph engine?**
Because the product wants to be local, portable, and dead simple to install. For this use case, graph workloads are bounded enough that relational tables plus FTS5 are a sensible trade.

**Where would this fail in production?**
Dynamic dispatch, metaprogramming, macro-heavy systems, and very weird build layouts will still create blind spots. The design docs openly show they are patching those holes with heuristics, which is good, but it also means the graph is approximate in hard cases.

**What part feels most differentiated?**
Not the graph itself. The strongest differentiation is the feedback loop between benchmark findings and tool/instruction design. The docs show a team actively instrumenting agent behavior and then changing tool semantics accordingly.

**What is likely brittle?**
The “teach the agent the right call sequence” layer. If future coding agents change how they route tool calls, some of these carefully tuned patterns may decay fast.

## What is smart
- Using SQLite + FTS5 instead of inventing infrastructure.
- Treating MCP instruction text as a first-class architecture surface, not docs garnish.
- Putting real effort into scan/sync pragmatics like `git ls-files`, file-size limits, worker recycling, and watcher behavior.
- Writing benchmark docs that are actually diagnostic, especially [`docs/benchmarks/call-sequence-analysis.md`](https://github.com/colbymchenry/codegraph/blob/1f3625a3e94441b5e9e72f2b03f3a4f42d5e860e/docs/benchmarks/call-sequence-analysis.md), which asks why a read reduction did not convert cleanly into wall-clock wins.
- Chasing graph-coverage gaps like callback/observer synthesis instead of pretending static extraction is complete.

## What is flawed or weak
- The README marketing is stronger than the guarantees. This is still best-effort structural intelligence, not truth.
- The benchmark story is compelling, but a lot depends on the agent actually following the intended tool path.
- Cross-language breadth is ambitious. Supporting 19+ languages plus framework-aware routing can easily become a maintenance burden with shallow correctness at the edges.
- Some of the moat is prompt/tool steering rather than core irreducible technology. That is useful, but easier for others to imitate.

## What we can learn / steal
- If you build agent tooling, study agent behavior as seriously as you study parsing or retrieval quality.
- Productize local-first developer infrastructure by default. Simpler deployment wins adoption.
- Put explicit budgets on retrieval surfaces. Unlimited “smart context” tools become sludge immediately.
- Use design docs plus benchmark postmortems as active steering mechanisms, not dead documentation.

## How we could apply it
- For any repo-aware assistant we build, separate the problem into indexing, resolution, retrieval shaping, and agent steering. Do not stop at embeddings or grep wrappers.
- Copy the idea of benchmark-driven tool redesign. If a tool saves reads but not latency, inspect call sequence and payload shape, not just headline metrics.
- Steal the local persistence pattern: SQLite + compact graph + FTS + bounded tool outputs is a very practical baseline.

## Bottom line
CodeGraph is a serious repo, not a thin AI veneer. The best part is not that it builds a symbol graph. The best part is that it understands a coding agent as a system with bad instincts, then designs the graph, tools, installer, and prompts together to redirect those instincts. That is the reusable lesson.
