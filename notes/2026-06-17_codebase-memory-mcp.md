# codebase-memory-mcp

- Repo: `DeusData/codebase-memory-mcp`
- URL: https://github.com/DeusData/codebase-memory-mcp
- Date: 2026-06-17
- Repo snapshot studied: `main` @ `e599df1d563c1e9b0b2fc8c6b12ee85934ade1c5`
- Why picked today: It was near the top of GitHub daily trending when checked, with 718 stars that day on the trending page. More importantly, this is not another "AI agent wrapper" repo. It is a large single-binary C codebase that tries to turn code intelligence into an indexed local graph product with real packaging, persistence, cross-repo linking, a localhost UI, and a surprisingly opinionated MCP tool contract.

## Executive summary
codebase-memory-mcp is a structural code intelligence backend packaged as a local MCP server. The interesting thing is not the marketing line about fewer tokens. It is the way the repo actually splits responsibilities: MCP and JSON-RPC in [`src/mcp/mcp.c`](https://github.com/DeusData/codebase-memory-mcp/blob/main/src/mcp/mcp.c), pipeline orchestration in [`src/pipeline/pipeline.c`](https://github.com/DeusData/codebase-memory-mcp/blob/main/src/pipeline/pipeline.c), SQLite-backed graph storage in [`src/store/store.c`](https://github.com/DeusData/codebase-memory-mcp/blob/main/src/store/store.c), incremental team-share artifacts in [`src/pipeline/artifact.c`](https://github.com/DeusData/codebase-memory-mcp/blob/main/src/pipeline/artifact.c), and a separate frontend bundle in [`graph-ui/`](https://github.com/DeusData/codebase-memory-mcp/tree/main/graph-ui).

The core builder lesson is that the team is treating code search as an indexing-and-querying systems problem, not as a prompt engineering trick. The tool surface in [`src/mcp/mcp.c`](https://github.com/DeusData/codebase-memory-mcp/blob/main/src/mcp/mcp.c) exposes graph search, Cypher queries, architecture views, diff impact, ADR management, and trace ingestion because the product assumption is: build a durable graph once, then let agents query that graph cheaply.

The caution is that the repo is already wide. It bundles vendored parsers, a large multi-pass pipeline, a UI server, multiple package registries, cross-repo linking, semantic search, and local persistence into one binary. That is impressive, but it also means there are many places for hidden complexity, stale claims, and correctness drift to creep in.

## What they built
They built a local code knowledge-graph engine that runs as a stdio MCP server or one-shot CLI:

- entrypoint and runtime threading live in [`src/main.c`](https://github.com/DeusData/codebase-memory-mcp/blob/main/src/main.c)
- the MCP contract and 14-tool surface live in [`src/mcp/mcp.c`](https://github.com/DeusData/codebase-memory-mcp/blob/main/src/mcp/mcp.c)
- indexing passes live under [`src/pipeline/`](https://github.com/DeusData/codebase-memory-mcp/tree/main/src/pipeline)
- storage and query primitives live in [`src/store/store.c`](https://github.com/DeusData/codebase-memory-mcp/blob/main/src/store/store.c)
- graph discovery and language handling live under [`src/discover/`](https://github.com/DeusData/codebase-memory-mcp/tree/main/src/discover)
- the optional UI server lives under [`src/ui/`](https://github.com/DeusData/codebase-memory-mcp/tree/main/src/ui) with the browser bundle in [`graph-ui/`](https://github.com/DeusData/codebase-memory-mcp/tree/main/graph-ui)
- packaging spans [`server.json`](https://github.com/DeusData/codebase-memory-mcp/blob/main/server.json), [`install.sh`](https://github.com/DeusData/codebase-memory-mcp/blob/main/install.sh), [`install.ps1`](https://github.com/DeusData/codebase-memory-mcp/blob/main/install.ps1), and registry-specific definitions under [`pkg/`](https://github.com/DeusData/codebase-memory-mcp/tree/main/pkg)

The product thesis is "index once, query structurally forever." The system stores a persistent graph in SQLite, updates it with a watcher, optionally exports a compressed `.codebase-memory/graph.db.zst` artifact for teammates, and then gives agents tools that operate on graph semantics instead of file-by-file scans.

## Why it matters
Most code agents still behave like talented interns armed with `grep` and too much optimism. This repo tries to harden the backend so the agent stops rediscovering the same codebase from scratch on every question.

That matters for three reasons:

1. It shifts the economics from repeated context stuffing to indexed structural retrieval.
2. It makes cross-file and cross-repo reasoning an explicit product goal rather than an accidental side effect of embeddings.
3. It treats local deployment, packaging, trust, and persistence as first-class features, which is exactly where many "agent infra" repos stay hand-wavy.

## Repo shape at a glance
This repo is large, but the top-level shape is coherent:

- [`src/`](https://github.com/DeusData/codebase-memory-mcp/tree/main/src), the C core: CLI, MCP, pipeline, store, semantic passes, graph buffer, UI, watcher
- [`graph-ui/`](https://github.com/DeusData/codebase-memory-mcp/tree/main/graph-ui), separate TypeScript/Vite frontend for graph browsing and control
- [`vendored/`](https://github.com/DeusData/codebase-memory-mcp/tree/main/vendored), bundled third-party pieces such as SQLite, mimalloc, xxhash, yyjson, and embeddings assets
- [`pkg/`](https://github.com/DeusData/codebase-memory-mcp/tree/main/pkg), package-manager definitions for npm, PyPI, Homebrew, Scoop, Winget, AUR, and more
- [`docs/`](https://github.com/DeusData/codebase-memory-mcp/tree/main/docs), screenshots and supporting assets
- [`tests/`](https://github.com/DeusData/codebase-memory-mcp/tree/main/tests) and [`test-infrastructure/`](https://github.com/DeusData/codebase-memory-mcp/tree/main/test-infrastructure), validation and infra for a repo that clearly expects to be trusted in real workflows
- [`server.json`](https://github.com/DeusData/codebase-memory-mcp/blob/main/server.json), MCP registry metadata and transport packaging

The shape says this is no longer a parser experiment. It is a full distribution product built around a C core with multiple client-facing surfaces.

## Layered architecture dissection
### High-level system shape
The cleanest mental model is:

1. the user or agent starts the binary through stdio or CLI;
2. [`src/main.c`](https://github.com/DeusData/codebase-memory-mcp/blob/main/src/main.c) brings up the MCP server, optional watcher, and optional localhost UI;
3. indexing requests build a multi-pass graph through [`src/pipeline/pipeline.c`](https://github.com/DeusData/codebase-memory-mcp/blob/main/src/pipeline/pipeline.c);
4. results are flushed into SQLite by [`src/store/store.c`](https://github.com/DeusData/codebase-memory-mcp/blob/main/src/store/store.c);
5. query tools in [`src/mcp/mcp.c`](https://github.com/DeusData/codebase-memory-mcp/blob/main/src/mcp/mcp.c) answer graph, code, architecture, and diff questions;
6. the UI server in [`src/ui/http_server.c`](https://github.com/DeusData/codebase-memory-mcp/blob/main/src/ui/http_server.c) exposes the same data locally for browser exploration.

### Main layers
**1. Runtime shell and process management**
[`src/main.c`](https://github.com/DeusData/codebase-memory-mcp/blob/main/src/main.c) is more serious than a typical CLI entrypoint. It handles graceful shutdown, parent-process death detection, background watcher threads, and optional HTTP UI startup. That is product code, not demo glue.

**2. MCP protocol layer**
[`src/mcp/mcp.c`](https://github.com/DeusData/codebase-memory-mcp/blob/main/src/mcp/mcp.c) defines the actual product contract. The tool list includes `index_repository`, `search_graph`, `query_graph`, `trace_path`, `get_architecture`, `search_code`, `detect_changes`, `manage_adr`, and `ingest_traces`. The system is clearly optimized around graph-native agent workflows rather than plain file browsing.

**3. Indexing pipeline**
[`src/pipeline/pipeline.c`](https://github.com/DeusData/codebase-memory-mcp/blob/main/src/pipeline/pipeline.c) coordinates discovery, structure building, source loading, definitions extraction, import/call/usage resolution, semantic post-passes, and final graph dump. The cross-file LSP layer in [`src/pipeline/pass_lsp_cross.c`](https://github.com/DeusData/codebase-memory-mcp/blob/main/src/pipeline/pass_lsp_cross.c) is especially revealing: it merges per-file extraction into language-specific cross-file resolution rather than pretending tree-sitter alone is enough.

**4. Graph storage and query layer**
[`src/store/store.c`](https://github.com/DeusData/codebase-memory-mcp/blob/main/src/store/store.c) owns the SQLite schema, prepared statements, CRUD operations, traversal helpers, and search surfaces. This is the real engine room. The system is not "LLM-first"; it is "graph store first."

**5. Artifact and distribution layer**
[`src/pipeline/artifact.c`](https://github.com/DeusData/codebase-memory-mcp/blob/main/src/pipeline/artifact.c) exports compressed graph snapshots for team sharing. [`server.json`](https://github.com/DeusData/codebase-memory-mcp/blob/main/server.json) and [`pkg/`](https://github.com/DeusData/codebase-memory-mcp/tree/main/pkg) then package the runtime across ecosystems. This is a nice example of operational ergonomics being encoded directly in source, not punted to docs.

**6. Local UI layer**
The browser frontend starts in [`graph-ui/src/App.tsx`](https://github.com/DeusData/codebase-memory-mcp/blob/main/graph-ui/src/App.tsx), while [`src/ui/http_server.c`](https://github.com/DeusData/codebase-memory-mcp/blob/main/src/ui/http_server.c) serves embedded assets and JSON endpoints from `127.0.0.1` only, with explicit localhost-only CORS handling.

### Request / data / control flow
An indexing flow begins through `index_repository` in [`src/mcp/mcp.c`](https://github.com/DeusData/codebase-memory-mcp/blob/main/src/mcp/mcp.c). That eventually creates a pipeline via [`src/pipeline/pipeline.c`](https://github.com/DeusData/codebase-memory-mcp/blob/main/src/pipeline/pipeline.c), which discovers files, extracts definitions, resolves imports and calls, adds semantic edges, and emits nodes and edges into the SQLite-backed store in [`src/store/store.c`](https://github.com/DeusData/codebase-memory-mcp/blob/main/src/store/store.c).

Once indexed, read-oriented tools such as `search_graph`, `query_graph`, `trace_path`, and `get_architecture` query that store instead of rescanning source. If artifact persistence is enabled, [`src/pipeline/artifact.c`](https://github.com/DeusData/codebase-memory-mcp/blob/main/src/pipeline/artifact.c) writes a compressed graph snapshot into `.codebase-memory/` so another teammate can bootstrap from it later.

The optional UI follows the same pattern. [`src/ui/http_server.c`](https://github.com/DeusData/codebase-memory-mcp/blob/main/src/ui/http_server.c) serves local endpoints and talks to its own MCP/store instance, while the frontend in [`graph-ui/`](https://github.com/DeusData/codebase-memory-mcp/tree/main/graph-ui) becomes a thin visualization client over the indexed graph.

## Key directories and files
- [`src/main.c`](https://github.com/DeusData/codebase-memory-mcp/blob/main/src/main.c), process lifecycle, watcher thread, and UI thread bootstrap
- [`src/mcp/mcp.c`](https://github.com/DeusData/codebase-memory-mcp/blob/main/src/mcp/mcp.c), tool definitions and JSON-RPC handling
- [`src/pipeline/pipeline.c`](https://github.com/DeusData/codebase-memory-mcp/blob/main/src/pipeline/pipeline.c), indexing orchestration
- [`src/pipeline/pass_lsp_cross.c`](https://github.com/DeusData/codebase-memory-mcp/blob/main/src/pipeline/pass_lsp_cross.c), cross-file LSP-assisted resolution
- [`src/pipeline/artifact.c`](https://github.com/DeusData/codebase-memory-mcp/blob/main/src/pipeline/artifact.c), compressed shared-graph export/import
- [`src/store/store.c`](https://github.com/DeusData/codebase-memory-mcp/blob/main/src/store/store.c), SQLite graph store and query implementation
- [`src/ui/http_server.c`](https://github.com/DeusData/codebase-memory-mcp/blob/main/src/ui/http_server.c), localhost UI routing and API
- [`graph-ui/src/App.tsx`](https://github.com/DeusData/codebase-memory-mcp/blob/main/graph-ui/src/App.tsx), top-level browser app shell
- [`server.json`](https://github.com/DeusData/codebase-memory-mcp/blob/main/server.json), MCP registry/distribution metadata
- [`pkg/`](https://github.com/DeusData/codebase-memory-mcp/tree/main/pkg), multi-registry packaging definitions

## Important components
**The MCP tool table is the actual product thesis**
The `TOOLS` array in [`src/mcp/mcp.c`](https://github.com/DeusData/codebase-memory-mcp/blob/main/src/mcp/mcp.c) is worth reading in full. It shows which questions the authors think a persistent code graph should answer: impact analysis, architecture recovery, cross-service tracing, ADR authoring, and cross-repo intelligence.

**The pipeline lock is a quiet but important design choice**
[`src/pipeline/pipeline.c`](https://github.com/DeusData/codebase-memory-mcp/blob/main/src/pipeline/pipeline.c) uses a global atomic lock to prevent concurrent runs against the same DB. That is mundane infrastructure discipline, and it is exactly the kind of thing many "AI tools" skip until they corrupt user state.

**Cross-file resolution is treated as a real pass**
[`src/pipeline/pass_lsp_cross.c`](https://github.com/DeusData/codebase-memory-mcp/blob/main/src/pipeline/pass_lsp_cross.c) turns per-file extraction artifacts into cross-file type-aware resolution inputs. That is a more serious approach than treating AST parsing as the whole story.

**The local UI is security-conscious by default**
[`src/ui/http_server.c`](https://github.com/DeusData/codebase-memory-mcp/blob/main/src/ui/http_server.c) binds to localhost and only reflects localhost origins for CORS. That is the right stance for a tool that exposes codebase intelligence over HTTP.

## Important knobs / configs / extension points
- `mode` in `index_repository` in [`src/mcp/mcp.c`](https://github.com/DeusData/codebase-memory-mcp/blob/main/src/mcp/mcp.c): `full`, `moderate`, `fast`, and `cross-repo-intelligence`
- `persistence` in `index_repository`, which writes `.codebase-memory/graph.db.zst`
- pagination and truncation controls in `search_graph` and `search_code`
- localhost UI controls in [`src/main.c`](https://github.com/DeusData/codebase-memory-mcp/blob/main/src/main.c) via `--ui=` and `--port=`
- registry/runtime packaging in [`server.json`](https://github.com/DeusData/codebase-memory-mcp/blob/main/server.json) for `npx` and `uvx`

## Practical questions and answers
**Is this mostly an MCP wrapper around grep?**
No. The source layout shows a genuine indexing engine with graph storage, multi-pass extraction, cross-file resolution, and specialized query surfaces.

**Where is the real system boundary?**
Between indexing and querying. The expensive work happens once in [`src/pipeline/`](https://github.com/DeusData/codebase-memory-mcp/tree/main/src/pipeline); the MCP layer then sells cheap graph-native questions on top of that stored structure.

**What would I inspect first if I had to trust or distrust it quickly?**
[`src/store/store.c`](https://github.com/DeusData/codebase-memory-mcp/blob/main/src/store/store.c), [`src/pipeline/pipeline.c`](https://github.com/DeusData/codebase-memory-mcp/blob/main/src/pipeline/pipeline.c), and [`src/mcp/mcp.c`](https://github.com/DeusData/codebase-memory-mcp/blob/main/src/mcp/mcp.c). Those three files tell you whether this is a real engine or a polished story.

**What is the most reusable idea here?**
Treat code-intelligence answers as materialized graph queries over a local store, then expose a narrow agent protocol on top. That is more durable than repeated ad hoc search.

## What is smart
- Using a persistent graph store instead of repeating source scans per question.
- Treating cross-repo intelligence and artifact export as first-class features, not future TODOs.
- Encoding query ergonomics directly into the tool descriptions with pagination/truncation advice.
- Keeping the UI local-only and CORS-restricted.
- Shipping many registry targets from one codebase instead of forcing one preferred ecosystem.

## What is flawed or weak
- The repo is already carrying product sprawl: core engine, UI, watcher, packaging, artifacts, semantic search, cross-repo linking, and ADR tooling all at once.
- The claims are not perfectly internally aligned. [`README.md`](https://github.com/DeusData/codebase-memory-mcp/blob/main/README.md) repeatedly says 158 languages, while [`server.json`](https://github.com/DeusData/codebase-memory-mcp/blob/main/server.json) says 159. That is not catastrophic, but it is exactly the kind of drift that makes benchmark-heavy tooling harder to trust.
- A single giant C codebase buys deployment simplicity, but it also concentrates maintenance risk. Every new pass and every vendored subsystem raises the blast radius.
- The tool descriptions are strong, but some of the hardest promises here are correctness promises, not speed promises: cross-language resolution, semantic ranking, and impact analysis are where subtle bugs will hide.

## What we can learn / steal
- Build a stable indexed backend before piling on agent prompting.
- Expose explicit tool contracts with pagination and failure guidance baked into the interface.
- Make artifact export/import a product feature if re-index cost is nontrivial.
- Treat local HTTP surfaces as security boundaries, not just convenience servers.
- Package across ecosystems only after the core runtime contract is solid enough to deserve it.

## How we could apply it
If we wanted a serious code-intelligence substrate for our own tools, I would borrow the shape, not the whole implementation:

1. one durable local store,
2. one explicit query protocol,
3. one artifact-sharing path for teams,
4. one thin browser surface for graph inspection,
5. aggressive skepticism about every claim that depends on semantic correctness.

The repo is a good reminder that agent infrastructure gets better when more work moves from prompt-time improvisation into indexed, queryable structure.

## Bottom line
codebase-memory-mcp is one of the more worthwhile trending repos of the day because it is trying to be an actual code-intelligence engine, not merely an AI shell around shell commands.

The reusable lesson is simple: if you want agents to reason structurally about code, stop making them rediscover the structure every time. Build the graph, store it, and make the query layer honest.
