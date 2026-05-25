# CodeGraph

- Repo: `colbymchenry/codegraph`
- URL: https://github.com/colbymchenry/codegraph
- Date: 2026-05-25
- Repo snapshot studied: `main` @ `1be8e7830f7ca37e42a378186b0274e684b1d4d8`
- Why picked today: It was one of the hottest GitHub repos on 2026-05-25, it sits directly in the AI coding-tools blast radius, and unlike a lot of "agent productivity" projects it has a very inspectable implementation thesis: precompute structure locally, then let assistants query it instead of thrashing around with grep.

## Executive summary
CodeGraph is a local code-intelligence engine packaged as an MCP server and CLI. The pitch is simple: build a repository-shaped knowledge graph ahead of time, store it in SQLite, then expose a small set of context, traversal, and search tools to agents like Claude Code, Codex CLI, Cursor, OpenCode, and Hermes Agent.

The smart part is not just "graph for code". The smart part is the productization discipline around that graph. This repo is really four products glued together cleanly: a parser/extraction pipeline, a queryable graph store, an MCP tool surface with output-budget controls, and an installer/distribution layer that makes the whole thing actually land inside existing agent workflows.

## What they built
They built a codebase indexing system that:

- scans a project and collects source files into a local index
- parses many languages with tree-sitter and custom extractors
- resolves imports, references, routes, and framework-specific edges
- stores nodes, edges, files, and unresolved references in SQLite
- serves graph-aware MCP tools so coding agents can ask higher-level questions
- keeps the index fresh with file watching and git-hook-based sync paths
- wraps the whole thing in a CLI installer that configures multiple agent surfaces

The most important source surfaces are:

- CLI entrypoint in [`src/bin/codegraph.ts`](https://github.com/colbymchenry/codegraph/blob/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/bin/codegraph.ts)
- extraction pipeline in [`src/extraction/`](https://github.com/colbymchenry/codegraph/tree/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/extraction)
- resolution layer in [`src/resolution/`](https://github.com/colbymchenry/codegraph/tree/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/resolution)
- graph and traversal logic in [`src/graph/`](https://github.com/colbymchenry/codegraph/tree/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/graph)
- context builder in [`src/context/`](https://github.com/colbymchenry/codegraph/tree/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/context)
- MCP server/tool layer in [`src/mcp/`](https://github.com/colbymchenry/codegraph/tree/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/mcp)
- persistence layer in [`src/db/`](https://github.com/colbymchenry/codegraph/tree/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/db)
- installer and agent-target plumbing in [`src/installer/`](https://github.com/colbymchenry/codegraph/tree/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/installer)

## Why it matters
A lot of repo-intelligence projects still feel like wrappers around LLM wandering. CodeGraph is more opinionated. It says the expensive part of coding-assistant work is usually discovery, not final synthesis, so precompute structural facts once and make the agent ask better questions.

That matters because it pushes the system toward deterministic leverage instead of prompt theater. Parsing, indexing, reference resolution, and route extraction happen locally in code. The LLM mostly benefits downstream by reading a better substrate.

## Repo shape at a glance
Top-level structure:

- [`README.md`](https://github.com/colbymchenry/codegraph/blob/1be8e7830f7ca37e42a378186b0274e684b1d4d8/README.md): positioning, install flow, benchmarks, supported agents/frameworks
- [`src/`](https://github.com/colbymchenry/codegraph/tree/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src): the actual product code
  - [`src/bin/`](https://github.com/colbymchenry/codegraph/tree/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/bin): CLI commands and runtime guardrails
  - [`src/extraction/`](https://github.com/colbymchenry/codegraph/tree/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/extraction): scan, parse, and symbol extraction pipeline
  - [`src/resolution/`](https://github.com/colbymchenry/codegraph/tree/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/resolution): import resolution, name matching, framework-specific resolvers
  - [`src/db/`](https://github.com/colbymchenry/codegraph/tree/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/db): schema, adapters, queries, migrations
  - [`src/graph/`](https://github.com/colbymchenry/codegraph/tree/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/graph): traversals and higher-level graph queries
  - [`src/context/`](https://github.com/colbymchenry/codegraph/tree/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/context): task-context assembly for agent consumption
  - [`src/mcp/`](https://github.com/colbymchenry/codegraph/tree/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/mcp): MCP server transport, instructions, tool definitions
  - [`src/sync/`](https://github.com/colbymchenry/codegraph/tree/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/sync): watcher and git-hook freshness mechanisms
  - [`src/installer/`](https://github.com/colbymchenry/codegraph/tree/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/installer): target detection and config writing for supported agents
  - [`src/search/`](https://github.com/colbymchenry/codegraph/tree/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/search): query parsing and scoring helpers
  - [`src/ui/`](https://github.com/colbymchenry/codegraph/tree/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/ui): terminal progress and glyph utilities
- [`site/`](https://github.com/colbymchenry/codegraph/tree/1be8e7830f7ca37e42a378186b0274e684b1d4d8/site): Astro marketing/docs site
- [`docs/`](https://github.com/colbymchenry/codegraph/tree/1be8e7830f7ca37e42a378186b0274e684b1d4d8/docs): design notes, benchmarks, search-quality docs
- [`__tests__/`](https://github.com/colbymchenry/codegraph/tree/1be8e7830f7ca37e42a378186b0274e684b1d4d8/__tests__): broad regression coverage across parsing, resolution, MCP, syncing, and installer behavior
- [`scripts/`](https://github.com/colbymchenry/codegraph/tree/1be8e7830f7ca37e42a378186b0274e684b1d4d8/scripts): packaging and release helper scripts

This is a strong shape. The repo is not tiny, but the subsystem boundaries are legible.

## Layered architecture dissection
### High-level system shape
At a high level, CodeGraph does this:

1. discover the relevant files in a project
2. parse them into symbols and raw relationships
3. resolve cross-file references and framework-specific edges
4. persist the resulting graph into SQLite plus FTS indexes
5. answer higher-level queries through CLI and MCP tools
6. keep the graph fresh with sync/watch infrastructure
7. distribute/configure the system into existing coding agents

## Main layers
**1. CLI and runtime-guard layer**

[`src/bin/codegraph.ts`](https://github.com/colbymchenry/codegraph/blob/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/bin/codegraph.ts) is more than a thin command parser. It hard-blocks unsupported Node versions, re-launches with safer WASM flags for tree-sitter stability, lazy-loads heavy modules for startup speed, and routes commands like `init`, `index`, `sync`, `context`, `callers`, and `impact`. That is grown-up CLI behavior, not hobby glue.

**2. Extraction layer**

[`src/extraction/index.ts`](https://github.com/colbymchenry/codegraph/blob/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/extraction/index.ts) is the pipeline orchestrator. It scans files, respects git visibility, batches file I/O, skips oversized source blobs, and pushes parsing through a worker-thread lifecycle with timeouts and recycling. [`src/extraction/tree-sitter.ts`](https://github.com/colbymchenry/codegraph/blob/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/extraction/tree-sitter.ts) then turns syntax trees into normalized nodes, edges, and unresolved references.

This is the core quality line in the repo. They are not asking an LLM to infer structure from vibes. They are extracting it mechanically.

**3. Resolution and framework layer**

After extraction, CodeGraph spends real effort resolving what raw parsing could not settle. [`src/resolution/import-resolver.ts`](https://github.com/colbymchenry/codegraph/blob/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/resolution/import-resolver.ts) handles language-aware extension resolution, relative paths, alias paths, and external-package detection. The framework resolvers in [`src/resolution/frameworks/`](https://github.com/colbymchenry/codegraph/tree/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/resolution/frameworks) are where the project gets more interesting: it tries to lift route and framework semantics into the graph instead of stopping at generic AST facts.

That is an important product move. Plain symbol graphs are useful. Symbol graphs plus route/controller binding and framework awareness are much more useful for real codebase questions.

**4. Storage and query layer**

[`src/db/schema.sql`](https://github.com/colbymchenry/codegraph/blob/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/db/schema.sql) defines the durable model: `nodes`, `edges`, `files`, `unresolved_refs`, plus FTS5 indexes and triggers. [`src/db/queries.ts`](https://github.com/colbymchenry/codegraph/blob/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/db/queries.ts) is the workhorse query builder that converts DB rows back into typed graph objects and layers ranking logic onto search.

Using SQLite here is the right call. The graph is local, portable, inspectable, and cheap to query. A lot of projects would have over-engineered this into a service.

**5. Graph traversal and context-construction layer**

[`src/graph/queries.ts`](https://github.com/colbymchenry/codegraph/blob/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/graph/queries.ts) and its sibling traversal code turn stored relationships into practical questions: ancestors, children, callers, callees, dependencies, dependents, and impact. [`src/context/index.ts`](https://github.com/colbymchenry/codegraph/blob/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/context/index.ts) is where the repo becomes assistant-native. It mixes search, path relevance, graph expansion, and markdown formatting into a context artifact that models can actually consume.

This is one of the smartest layers in the repo because it recognizes a crucial fact: raw graph data is not yet good assistant context. It has to be compressed, ranked, and shaped.

**6. MCP serving layer**

[`src/mcp/index.ts`](https://github.com/colbymchenry/codegraph/blob/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/mcp/index.ts) implements the server, transport, roots negotiation, and watchdog behavior. [`src/mcp/tools.ts`](https://github.com/colbymchenry/codegraph/blob/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/mcp/tools.ts) defines the exposed tools and, importantly, the guardrails around them: input bounds, output-size budgeting, and heuristics that keep context from exploding.

That output-budgeting logic is a key insight in the repo. Once you hand a graph system to an LLM, the problem shifts from “can I find the code?” to “can I return just enough code without bloating the prompt?” CodeGraph is clearly optimized around that second problem.

**7. Freshness and installation layer**

[`src/sync/watcher.ts`](https://github.com/colbymchenry/codegraph/blob/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/sync/watcher.ts) keeps local indexes updated with debounced native file events, while [`src/installer/index.ts`](https://github.com/colbymchenry/codegraph/blob/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/installer/index.ts) handles multi-agent target detection, config placement, and install UX.

This is less glamorous than graph traversal, but it is why the project feels real. Great internals do not matter much if installation and freshness are painful.

### Request / data / control flow
A typical flow looks like this:

- user installs/configures agent integrations through [`src/installer/index.ts`](https://github.com/colbymchenry/codegraph/blob/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/installer/index.ts)
- project indexing begins through CLI entrypoints in [`src/bin/codegraph.ts`](https://github.com/colbymchenry/codegraph/blob/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/bin/codegraph.ts)
- file discovery and worker-managed parsing run through [`src/extraction/index.ts`](https://github.com/colbymchenry/codegraph/blob/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/extraction/index.ts)
- AST-derived symbols and relationships are emitted by [`src/extraction/tree-sitter.ts`](https://github.com/colbymchenry/codegraph/blob/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/extraction/tree-sitter.ts)
- unresolved references and import paths are reconciled by [`src/resolution/`](https://github.com/colbymchenry/codegraph/tree/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/resolution)
- the graph lands in SQLite per [`src/db/schema.sql`](https://github.com/colbymchenry/codegraph/blob/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/db/schema.sql)
- graph and context queries are served through [`src/graph/`](https://github.com/colbymchenry/codegraph/tree/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/graph), [`src/context/`](https://github.com/colbymchenry/codegraph/tree/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/context), and [`src/mcp/tools.ts`](https://github.com/colbymchenry/codegraph/blob/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/mcp/tools.ts)
- later file changes are folded back in through [`src/sync/watcher.ts`](https://github.com/colbymchenry/codegraph/blob/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/sync/watcher.ts) and sync hooks

## Key directories and files
- [`README.md`](https://github.com/colbymchenry/codegraph/blob/1be8e7830f7ca37e42a378186b0274e684b1d4d8/README.md): product thesis and benchmark claims
- [`src/bin/codegraph.ts`](https://github.com/colbymchenry/codegraph/blob/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/bin/codegraph.ts): command surface and runtime safety logic
- [`src/extraction/index.ts`](https://github.com/colbymchenry/codegraph/blob/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/extraction/index.ts): indexing orchestrator
- [`src/extraction/tree-sitter.ts`](https://github.com/colbymchenry/codegraph/blob/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/extraction/tree-sitter.ts): syntax-tree extraction engine
- [`src/resolution/import-resolver.ts`](https://github.com/colbymchenry/codegraph/blob/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/resolution/import-resolver.ts): cross-file import/path resolution
- [`src/resolution/frameworks/`](https://github.com/colbymchenry/codegraph/tree/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/resolution/frameworks): route/framework semantic lifting
- [`src/db/schema.sql`](https://github.com/colbymchenry/codegraph/blob/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/db/schema.sql): persistent graph schema
- [`src/db/queries.ts`](https://github.com/colbymchenry/codegraph/blob/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/db/queries.ts): search and CRUD query layer
- [`src/graph/queries.ts`](https://github.com/colbymchenry/codegraph/blob/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/graph/queries.ts): higher-level graph questions
- [`src/context/index.ts`](https://github.com/colbymchenry/codegraph/blob/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/context/index.ts): model-facing context assembly
- [`src/mcp/index.ts`](https://github.com/colbymchenry/codegraph/blob/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/mcp/index.ts): MCP server lifecycle
- [`src/mcp/tools.ts`](https://github.com/colbymchenry/codegraph/blob/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/mcp/tools.ts): tool contracts and output controls
- [`src/sync/watcher.ts`](https://github.com/colbymchenry/codegraph/blob/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/sync/watcher.ts): change-watching freshness path
- [`src/installer/index.ts`](https://github.com/colbymchenry/codegraph/blob/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/installer/index.ts): installation and target-integration logic

## Important components
**The extraction orchestrator**

[`src/extraction/index.ts`](https://github.com/colbymchenry/codegraph/blob/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/extraction/index.ts) is carrying a lot of the real engineering weight. It solves unpleasant operational details like git-aware file collection, large-file skipping, worker timeouts, and WASM memory churn.

**The tree-sitter normalization engine**

[`src/extraction/tree-sitter.ts`](https://github.com/colbymchenry/codegraph/blob/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/extraction/tree-sitter.ts) is where language-specific syntax gets flattened into one shared graph model. If this layer is sloppy, the whole product becomes decorative. It does not look decorative.

**The framework resolver family**

[`src/resolution/frameworks/`](https://github.com/colbymchenry/codegraph/tree/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/resolution/frameworks) is arguably the differentiator. This is the layer that lets the tool answer more human questions like “what URL path reaches this handler?” rather than only low-level symbol questions.

**The SQLite + FTS graph store**

[`src/db/schema.sql`](https://github.com/colbymchenry/codegraph/blob/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/db/schema.sql) plus [`src/db/queries.ts`](https://github.com/colbymchenry/codegraph/blob/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/db/queries.ts) give the project a pragmatic storage spine. It is local-first and boring in a good way.

**The context shaper**

[`src/context/index.ts`](https://github.com/colbymchenry/codegraph/blob/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/context/index.ts) is the layer I would study most closely if I were building on this idea. It encodes the practical truth that retrieval is only half the problem. Prompt budget management is the other half.

**The MCP tool guardrails**

[`src/mcp/tools.ts`](https://github.com/colbymchenry/codegraph/blob/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/mcp/tools.ts) has defensive limits around input size, path size, and output size. That is exactly what a serious MCP server needs once exposed to real agent behavior.

## Important knobs / configs / extension points
- supported-agent install targets and config placement live under [`src/installer/targets/`](https://github.com/colbymchenry/codegraph/tree/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/installer/targets)
- supported-language grammars and loader logic live in [`src/extraction/grammars.ts`](https://github.com/colbymchenry/codegraph/blob/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/extraction/grammars.ts)
- framework-specific semantic lifts are concentrated in [`src/resolution/frameworks/`](https://github.com/colbymchenry/codegraph/tree/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/resolution/frameworks)
- sync behavior is governed by [`src/sync/watcher.ts`](https://github.com/colbymchenry/codegraph/blob/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/sync/watcher.ts) and [`src/sync/watch-policy.ts`](https://github.com/colbymchenry/codegraph/blob/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/sync/watch-policy.ts)
- query scoring and symbol matching are tuned in [`src/search/query-parser.ts`](https://github.com/colbymchenry/codegraph/blob/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/search/query-parser.ts) and [`src/search/query-utils.ts`](https://github.com/colbymchenry/codegraph/blob/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/search/query-utils.ts)
- MCP behavior and server instructions are shaped in [`src/mcp/server-instructions.ts`](https://github.com/colbymchenry/codegraph/blob/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/mcp/server-instructions.ts) and [`src/mcp/tools.ts`](https://github.com/colbymchenry/codegraph/blob/1be8e7830f7ca37e42a378186b0274e684b1d4d8/src/mcp/tools.ts)

## Practical questions and answers
**What is the real product here: the graph, the MCP server, or the installer?**

All three matter, but the defensible core is the graph plus the context-shaping layer. The installer is how the product gets adopted. The MCP server is how the product gets consumed.

**What is the strongest engineering insight in the repo?**

Budget the assistant interaction, not just the indexing pipeline. The repo clearly understands that “too much retrieved context” is a failure mode, not a success mode.

**Why not just let the agent grep the codebase?**

Because repetitive discovery is expensive. CodeGraph is trying to turn N exploratory tool calls into one structured query against precomputed local state.

**Where would this fail in practice?**

Large polyglot repos with weird build-time code generation, dynamic dispatch, or framework magic will still produce blind spots. Static structure gets you far, but not all the way.

**What looks unusually thoughtful?**

The operational guardrails around WASM parsing, Node version blocking, watcher fallbacks, and MCP output budgeting. A lot of trending repos have product ideas. Fewer have this much scar tissue encoded into source.

## What is smart
- Using SQLite + FTS5 instead of inventing a service where none is needed
- Treating route/framework semantics as first-class graph data
- Recycling parser workers and forcing safer WASM runtime behavior
- Building model-facing context as a distinct layer, not an afterthought
- Putting hard limits around tool inputs and outputs before agents can abuse them
- Supporting multiple agent surfaces without making the core indexing logic depend on any one vendor

## What is flawed or weak
- The repo is carrying a lot of surface area now: many languages, many frameworks, many agent targets, and a docs site. Support tax is real.
- The benchmark section in [`README.md`](https://github.com/colbymchenry/codegraph/blob/1be8e7830f7ca37e42a378186b0274e684b1d4d8/README.md) is interesting, but still repo-author-reported. I would want independent reproduction before over-trusting the exact savings numbers.
- Static graphs inevitably struggle with reflective or highly dynamic codebases, so some of the neatest demos probably rest on code that is friendlier than the worst production reality.
- The installer ambition is good for adoption, but multi-target integration logic can quietly become a maintenance swamp.

## What we can learn / steal
- Precompute structure once, then spend model budget on reasoning instead of discovery
- Treat retrieval formatting as a product surface with its own tuning and heuristics
- Encode operational pain directly into the codebase: hard blocks, fallbacks, worker recycling, input caps
- Use framework-specific semantic lifts to make code intelligence answer human questions, not just AST questions
- Keep the storage boring and local when the product does not truly need a remote service

## How we could apply it
If we were building repo-intelligence tooling ourselves, I would steal these parts first:

1. a local SQLite graph with FTS-backed symbol search
2. a deterministic parse and reference-resolution pipeline
3. a context-builder layer that aggressively shapes and budgets output
4. framework-specific semantic adapters for the ecosystems we care about most
5. installer plumbing only after the core retrieval quality is proven

I would probably narrow the initial framework/agent matrix more than this repo does. The architecture is strongest where it is disciplined, and surface-area sprawl is the main threat to that discipline.

## Bottom line
CodeGraph is one of the better trending AI tooling repos because it is not mainly selling “agent magic.” It is selling a better substrate for agent work.

The key idea worth stealing is this: do the expensive structural labor once, store it locally, and then spend your model budget on interpretation, not file-system wandering. That is a real product thesis, and the source mostly supports it.
