# Code-Graph-RAG

- Repo: `vitali87/code-graph-rag`
- URL: https://github.com/vitali87/code-graph-rag
- Date: 2026-08-09
- Repo snapshot studied: `main` @ `afc2011bc34917b0e566e58e4b679cbdb4438524`
- Why picked today: It showed 2,815 stars, 491 forks, and 59 stars added today on GitHub daily trending when checked. More importantly, this is a source-heavy attempt to turn "code RAG" into a graph-first developer runtime with real parser, graph, MCP, and structural-editing layers instead of another embeddings-only wrapper.

## Executive summary
`code-graph-rag` is best understood as a three-part system: a parser-and-ingest pipeline, a graph-backed query and retrieval layer, and an MCP/tool surface that lets outside agents operate against the indexed repo. The most important source cluster is [`docs/architecture/overview.md`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/docs/architecture/overview.md), [`docs/architecture/graph-schema.md`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/docs/architecture/graph-schema.md), [`codebase_rag/graph_updater.py`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/codebase_rag/graph_updater.py), and [`codebase_rag/mcp/tools.py`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/codebase_rag/mcp/tools.py). Those files reveal the real bet: index source into a typed Memgraph schema, keep enough structure to answer codebase questions and target edits, then expose the graph as a working tool belt rather than as a dashboard.

The strongest move is that the parser story is layered instead of doctrinaire. [`codebase_rag/parser_loader.py`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/codebase_rag/parser_loader.py) lazy-loads only the grammars actually needed, [`codebase_rag/graph_updater.py`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/codebase_rag/graph_updater.py) mixes tree-sitter with optional libclang and Roslyn hybrid passes, and [`codebase_rag/parsers/ast_grep_tier.py`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/codebase_rag/parsers/ast_grep_tier.py) adds a config-driven structural tier for languages that are not yet worth a full handwritten traversal. That is a much more practical scaling story than "we support everything" marketing.

The second strong move is the safety-conscious product surface. [`codebase_rag/docker-compose.yaml`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/codebase_rag/docker-compose.yaml) binds Memgraph and Qdrant to loopback by default, [`codebase_rag/tools/structural_editor.py`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/codebase_rag/tools/structural_editor.py) defaults structural rewrites to dry-run previews and requires approval, and [`codebase_rag/mcp/server.py`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/codebase_rag/mcp/server.py) scopes Cypher generation to the current indexed project so multi-project databases do not quietly bleed together.

## What they built
They built a polyglot codebase indexing stack that stores source structure as a graph and then exposes that graph to both humans and agents:

- [`codebase_rag`](https://github.com/vitali87/code-graph-rag/tree/afc2011bc34917b0e566e58e4b679cbdb4438524/codebase_rag): the main package, covering parsing, graph ingest, querying, MCP, and tools.
- [`docs/architecture`](https://github.com/vitali87/code-graph-rag/tree/afc2011bc34917b0e566e58e4b679cbdb4438524/docs/architecture): schema and system-shape docs that actually map to the code.
- [`codebase_rag/mcp`](https://github.com/vitali87/code-graph-rag/tree/afc2011bc34917b0e566e58e4b679cbdb4438524/codebase_rag/mcp): MCP server, client, and tool registry.
- [`codebase_rag/tools`](https://github.com/vitali87/code-graph-rag/tree/afc2011bc34917b0e566e58e4b679cbdb4438524/codebase_rag/tools): code retrieval, file editing, shell, directory listing, structural search, and structural replace.
- [`evals`](https://github.com/vitali87/code-graph-rag/tree/afc2011bc34917b0e566e58e4b679cbdb4438524/evals): retrieval and graph-quality probes across multiple languages and tasks.

## Why it matters
Most "code RAG" systems flatten source into chunks, compute embeddings, then pretend that is enough structure. This repo matters because it keeps real software relationships alive:

1. A typed graph schema for modules, classes, functions, methods, interfaces, external modules, resources, and findings.
2. Hybrid frontend paths for languages where pure tree-sitter leaves too much semantic value on the floor.
3. A real MCP layer that packages the graph, file tools, and structural editors into an agent-usable surface.
4. Incremental sync logic with hash caches and parser fingerprints so re-indexing is not always a full rebuild.

## Repo shape at a glance
The repository is broad, but the shape is coherent:

- [`pyproject.toml`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/pyproject.toml) defines the package, extras, and a Python 3.12+ CLI-first product.
- [`codebase_rag/graph_updater.py`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/codebase_rag/graph_updater.py) is the ingest engine and real system center of gravity.
- [`codebase_rag/parser_loader.py`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/codebase_rag/parser_loader.py) handles grammar loading and query preparation.
- [`codebase_rag/parsers`](https://github.com/vitali87/code-graph-rag/tree/afc2011bc34917b0e566e58e4b679cbdb4438524/codebase_rag/parsers) contains language-specific frontends and analyzers.
- [`codebase_rag/mcp`](https://github.com/vitali87/code-graph-rag/tree/afc2011bc34917b0e566e58e4b679cbdb4438524/codebase_rag/mcp) packages the indexed graph as an MCP server.
- [`docs/advanced/adding-languages.md`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/docs/advanced/adding-languages.md) and [`codebase_rag/parsers/ast_grep_tier.py`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/codebase_rag/parsers/ast_grep_tier.py) show how the team is trying to make language support scalable instead of bespoke forever.

## Layered architecture dissection
### High-level system shape
The system shape is: load only the parser grammars needed for the repo, walk the source tree into a Memgraph-backed schema, optionally enrich some languages with hybrid semantic passes, then expose the resulting graph through CLI and MCP tools that can query, read, patch, and structurally rewrite code.

### Main layers
**1. Parser bootstrap layer**  
[`codebase_rag/parser_loader.py`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/codebase_rag/parser_loader.py) delays grammar imports until first use and can fall back to local tree-sitter submodules, even building bindings in place when necessary. That is a practical startup-time optimization and a useful "support odd language stacks without exploding startup" move.

**2. Graph ingest layer**  
[`codebase_rag/graph_updater.py`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/codebase_rag/graph_updater.py) owns the full repo sync: file hashing, parser-fingerprint invalidation, AST caching, hybrid C/C++ and C# frontend augmentation, endpoint emission, resource cleanup, and optional semantic search population.

**3. Schema and relationship layer**  
[`docs/architecture/graph-schema.md`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/docs/architecture/graph-schema.md) is more than documentation. It tells you what the product thinks code is: not just symbols, but external resources, `FLOWS_TO` edges, and findings nodes for pattern, smell, and security analysis.

**4. Fallback structural layer**  
[`codebase_rag/parsers/ast_grep_tier.py`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/codebase_rag/parsers/ast_grep_tier.py) gives the repo a second expansion path. Instead of waiting for fully mature tree-sitter handling, it can emit modules, functions, classes, and imports from YAML ast-grep patterns for languages like Ruby.

**5. Agent and MCP layer**  
[`codebase_rag/mcp/server.py`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/codebase_rag/mcp/server.py) plus [`codebase_rag/mcp/tools.py`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/codebase_rag/mcp/tools.py) are the product surface: list/delete/index/update repositories, query the graph, retrieve code, edit files, run structural searches, and optionally run shell commands.

### Request / data / control flow
1. The CLI or MCP server loads parsers through [`parser_loader.py`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/codebase_rag/parser_loader.py), importing only the language grammars that matter.
2. [`GraphUpdater`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/codebase_rag/graph_updater.py) computes hash caches and parser fingerprints to decide whether a full or incremental rebuild is needed.
3. Tree-sitter parsing builds the bulk graph, while hybrid helpers can add C/C++ macro and include facts or C# Roslyn-derived semantics.
4. The ingest sink writes typed nodes and edges into Memgraph under the schema described in [`graph-schema.md`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/docs/architecture/graph-schema.md).
5. The MCP registry in [`mcp/tools.py`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/codebase_rag/mcp/tools.py) exposes query, retrieval, file, shell, and structural-edit tools to outside agents.
6. Natural-language graph questions go through [`tools/codebase_query.py`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/codebase_rag/tools/codebase_query.py), which translates English to Cypher, executes it, and truncates results to sane token limits.

## Key directories and files
- [`pyproject.toml`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/pyproject.toml): package contract, extras, and dependency story.
- [`docs/architecture/overview.md`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/docs/architecture/overview.md): short but accurate system map.
- [`docs/architecture/graph-schema.md`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/docs/architecture/graph-schema.md): the conceptual core of the product.
- [`codebase_rag/graph_updater.py`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/codebase_rag/graph_updater.py): ingest orchestration, incremental sync, hybrid augmentations, and cleanup.
- [`codebase_rag/parser_loader.py`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/codebase_rag/parser_loader.py): lazy grammar loading and query assembly.
- [`codebase_rag/parsers/ast_grep_tier.py`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/codebase_rag/parsers/ast_grep_tier.py): config-first structural language support.
- [`codebase_rag/mcp/server.py`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/codebase_rag/mcp/server.py): MCP bootstrap, project scoping, and server transport.
- [`codebase_rag/mcp/tools.py`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/codebase_rag/mcp/tools.py): the real user-facing tool inventory.
- [`codebase_rag/tools/structural_search.py`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/codebase_rag/tools/structural_search.py) and [`codebase_rag/tools/structural_editor.py`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/codebase_rag/tools/structural_editor.py): the most distinctive editing surface beyond plain file patching.
- [`codebase_rag/docker-compose.yaml`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/codebase_rag/docker-compose.yaml): loopback-first local stack wiring for Memgraph, Lab, and Qdrant.

## Important components
The most important component is [`GraphUpdater`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/codebase_rag/graph_updater.py). That file is where the product stops being a graph schema and becomes a working system with caching, hybrid frontends, endpoint extraction, and post-pass cleanup.

The second is [`parser_loader.py`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/codebase_rag/parser_loader.py). Lazy-loading parser grammars is not glamorous, but it is exactly the sort of disciplined startup optimization and compatibility glue that determines whether a polyglot developer tool feels serious.

The third is the MCP surface in [`mcp/tools.py`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/codebase_rag/mcp/tools.py). This is where the repo stops being "a graph database with docs" and becomes an agent product with query, retrieval, editing, and indexing verbs.

The fourth is [`ast_grep_tier.py`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/codebase_rag/parsers/ast_grep_tier.py). It is strategically important because it lowers the marginal cost of adding a new language or partial support mode.

## Important knobs / configs / extension points
- [`pyproject.toml`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/pyproject.toml) exposes extras such as `treesitter-full`, `semantic`, `milvus`, and `ast-grep`, which materially change the system surface.
- [`docs/advanced/adding-languages.md`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/docs/advanced/adding-languages.md) documents the grammar-extension path.
- [`graph_updater.py`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/codebase_rag/graph_updater.py) carries the important runtime toggles: skip embeddings, hybrid frontend enablement, incremental hash cache usage, and parser-fingerprint invalidation.
- [`tools/structural_editor.py`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/codebase_rag/tools/structural_editor.py) makes rewrites dry-run by default and requires approval for writes.
- [`docker-compose.yaml`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/codebase_rag/docker-compose.yaml) makes network exposure an explicit decision instead of a default footgun.

## Practical questions and answers
**Is this mainly an embeddings product with a graph-shaped veneer?**  
No. The graph is the primary representation. [`graph-schema.md`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/docs/architecture/graph-schema.md) and [`graph_updater.py`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/codebase_rag/graph_updater.py) make that very clear.

**What is the most reusable design move here?**  
Use one authoritative ingest orchestrator that can combine several parsing tiers instead of forcing one parser technology to do every job. The mix of tree-sitter, hybrid semantic enrichers, and ast-grep fallback is worth stealing.

**Where should a builder start reading?**  
Start with [`docs/architecture/overview.md`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/docs/architecture/overview.md), then [`graph-schema.md`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/docs/architecture/graph-schema.md), then [`graph_updater.py`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/codebase_rag/graph_updater.py), and finally the MCP surface in [`mcp/tools.py`](https://github.com/vitali87/code-graph-rag/blob/afc2011bc34917b0e566e58e4b679cbdb4438524/codebase_rag/mcp/tools.py).

**Where does the design still feel brittle?**  
The system still depends on an LLM translating natural language to Cypher, on Memgraph as a central service, and on language-specific heuristics that can only ever be partly semantic without full compiler integration everywhere.

## What is smart
- Mixing parser strategies instead of pretending one parser stack can do everything well.
- Keeping graph schema, ingest passes, and MCP tool surface aligned.
- Treating structural search and replace as first-class agent tools instead of a side script.
- Using loopback-only defaults for Memgraph and Qdrant.
- Making language expansion progressively cheaper with the ast-grep tier.

## What is flawed or weak
- The stack is operationally heavy for an individual developer tool: Memgraph, optional Qdrant, grammars, and model-backed query generation all have to cooperate.
- Query quality still depends on the LLM's Cypher generation discipline.
- The fallback ast-grep tier is intentionally structural and flat, so it cannot substitute for deeper semantic support.
- The README still carries odd suspended-account and badge-recovery commentary, which is not a product problem but does make the presentation feel less polished than the internals.

## What we can learn / steal
- Use a typed graph when the domain really is relationships, not documents.
- Make parser support tiered so the system can grow without all-or-nothing language support.
- Put dry-run and approval rails directly into editing tools.
- Scope shared graph queries to an active project to avoid multi-tenant confusion.

## How we could apply it
If we wanted code intelligence for our own repos, I would copy the ingest philosophy more than the exact stack: one orchestrator, one explicit schema, one agent-facing tool layer, and several parser tiers chosen by cost and fidelity. I would be more cautious about making natural-language-to-query generation the only user path, but the structural backbone is worth studying closely.

## Bottom line
`vitali87/code-graph-rag` is worth reading because it treats code intelligence as a graph systems problem, not as prompt engineering over chunks.

The builder lesson is that serious code RAG needs explicit structure, incremental ingest, and a tool surface that can do more than semantic search.
