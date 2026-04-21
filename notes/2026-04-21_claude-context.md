# Claude Context

- Repo: `zilliztech/claude-context`
- URL: https://github.com/zilliztech/claude-context
- Date: 2026-04-21
- Repo snapshot studied: `master` @ `66d761633b5bc308c2d55a0c6287bc1d6aac4933`
- Why picked today: It is hot on GitHub right now, directly AI-tooling relevant, and more interesting than the usual MCP-wrapper hype because it actually has a retrieval engine, change-detection layer, and multiple product surfaces.

## Executive summary

Claude Context is a semantic code-search system packaged three ways: as a reusable indexing/search core, as an MCP server for coding agents, and as editor integrations. The core idea is simple: do not stuff an entire repo into an agent context window, index it into a vector store instead, then pull back the smallest useful slices when the user asks a question.

The repo is more substantial than the README pitch suggests. The center of gravity is [`packages/core/src/context.ts`](https://github.com/zilliztech/claude-context/blob/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/core/src/context.ts), which owns file discovery, ignore handling, chunking, embedding, vector-store writes, hybrid retrieval, and incremental reindexing hooks. Around that, the MCP package adds a lot of operational glue: snapshot persistence, cloud-state reconciliation, background indexing, and defensive recovery for corrupted local state.

The strongest idea here is that they treat retrieval as a stateful system, not just a search call. The weakest part is that the implementation is still fairly operationally noisy, with a lot of logic packed into a few giant classes and a hard product bias toward Milvus/Zilliz.

## What they built

They built a codebase indexing and retrieval stack for AI coding agents.

Concretely, the repo provides:

- a reusable indexing/search engine in [`packages/core`](https://github.com/zilliztech/claude-context/tree/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/core)
- an MCP server in [`packages/mcp`](https://github.com/zilliztech/claude-context/tree/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/mcp) exposing tools like `index_codebase`, `search_code`, and `get_indexing_status`
- a VS Code extension in [`packages/vscode-extension`](https://github.com/zilliztech/claude-context/tree/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/vscode-extension)
- a Chrome extension in [`packages/chrome-extension`](https://github.com/zilliztech/claude-context/tree/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/chrome-extension)
- evaluation harnesses in [`evaluation`](https://github.com/zilliztech/claude-context/tree/66d761633b5bc308c2d55a0c6287bc1d6aac4933/evaluation) to benchmark retrieval quality and token savings

This is basically “semantic grep for agents,” but productized as an indexing pipeline plus agent-facing transport layer.

## Why it matters

Lots of agent tooling says “give the model more context.” Claude Context makes the opposite bet: give the model less, but make retrieval smarter. That is the right instinct for large repos, where brute-force context loading becomes both expensive and dumb.

The important engineering angle is that they combine:

- AST-aware chunking when they can
- character-based fallback when they cannot
- dense plus BM25-style sparse retrieval
- file-change detection for incremental reindexing
- MCP packaging so the retrieval system feels native to the agent

That is more useful than another thin MCP wrapper around a single SaaS endpoint.

## Repo shape at a glance

The repo is a clean monorepo with a clear center and several adapters:

- [`packages/core`](https://github.com/zilliztech/claude-context/tree/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/core), the real engine: chunking, embeddings, vector DB access, indexing flow, and sync logic
- [`packages/mcp`](https://github.com/zilliztech/claude-context/tree/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/mcp), MCP server, tool handlers, snapshot recovery, and background sync
- [`packages/vscode-extension`](https://github.com/zilliztech/claude-context/tree/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/vscode-extension), IDE-facing UI and commands
- [`packages/chrome-extension`](https://github.com/zilliztech/claude-context/tree/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/chrome-extension), browser integration surface
- [`evaluation`](https://github.com/zilliztech/claude-context/tree/66d761633b5bc308c2d55a0c6287bc1d6aac4933/evaluation), benchmarking and case-study scaffolding
- [`docs`](https://github.com/zilliztech/claude-context/tree/66d761633b5bc308c2d55a0c6287bc1d6aac4933/docs), setup, deep dives, and troubleshooting
- [`examples`](https://github.com/zilliztech/claude-context/tree/66d761633b5bc308c2d55a0c6287bc1d6aac4933/examples), lightweight example consumers of the core package

The main hierarchy is good: one real engine package, then delivery surfaces layered around it.

## Layered architecture dissection

### High-level system shape

The system has five layers:

1. repository scanning and file selection in [`packages/core/src/context.ts`](https://github.com/zilliztech/claude-context/blob/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/core/src/context.ts)
2. code chunking in [`packages/core/src/splitter`](https://github.com/zilliztech/claude-context/tree/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/core/src/splitter)
3. embedding and vector-store persistence in [`packages/core/src/embedding`](https://github.com/zilliztech/claude-context/tree/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/core/src/embedding) and [`packages/core/src/vectordb`](https://github.com/zilliztech/claude-context/tree/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/core/src/vectordb)
4. incremental sync state in [`packages/core/src/sync`](https://github.com/zilliztech/claude-context/tree/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/core/src/sync)
5. product adapters and agent-facing tools in [`packages/mcp`](https://github.com/zilliztech/claude-context/tree/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/mcp) and [`packages/vscode-extension`](https://github.com/zilliztech/claude-context/tree/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/vscode-extension)

That is the right macro-shape for this kind of project. The engine is mostly separate from the agent protocol.

### Main layers

#### 1) Context orchestration layer

[`packages/core/src/context.ts`](https://github.com/zilliztech/claude-context/blob/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/core/src/context.ts) is the brain. It:

- chooses supported file extensions and ignore patterns
- discovers code files recursively
- prepares collection names based on repo path and retrieval mode
- batches chunk processing and embedding generation
- writes documents into Milvus/Zilliz
- runs either pure dense search or hybrid dense+sparse search
- handles full reindex and change-based reindex

This file is doing a lot, maybe too much, but it makes the architecture legible.

#### 2) Chunking layer

[`packages/core/src/splitter/ast-splitter.ts`](https://github.com/zilliztech/claude-context/blob/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/core/src/splitter/ast-splitter.ts) is one of the more interesting pieces. It uses tree-sitter grammars to split code by meaningful syntactic units like functions, classes, methods, interfaces, and exports. When the language is unsupported or parsing fails, it falls back to [`packages/core/src/splitter/langchain-splitter.ts`](https://github.com/zilliztech/claude-context/blob/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/core/src/splitter/langchain-splitter.ts).

That AST-plus-fallback design is pragmatic. It gets most of the semantic benefit without turning unsupported languages into hard failures.

#### 3) Embedding and retrieval layer

The embedding providers live under [`packages/core/src/embedding`](https://github.com/zilliztech/claude-context/tree/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/core/src/embedding), while Milvus/Zilliz integration lives under [`packages/core/src/vectordb`](https://github.com/zilliztech/claude-context/tree/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/core/src/vectordb).

The key structural point is that retrieval is hybrid by default. [`packages/core/src/context.ts`](https://github.com/zilliztech/claude-context/blob/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/core/src/context.ts) builds dense query embeddings, pairs them with sparse BM25-style search requests, and uses reciprocal-rank fusion. On the storage side, [`packages/core/src/vectordb/milvus-restful-vectordb.ts`](https://github.com/zilliztech/claude-context/blob/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/core/src/vectordb/milvus-restful-vectordb.ts) creates hybrid collections with both `vector` and `sparse_vector` fields.

That is the repo’s best technical choice. Pure vector search is usually not enough for code.

#### 4) Change-detection and synchronization layer

Incremental indexing is handled by [`packages/core/src/sync/synchronizer.ts`](https://github.com/zilliztech/claude-context/blob/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/core/src/sync/synchronizer.ts), which snapshots file hashes under `~/.context/merkle`, builds a Merkle DAG, compares current and previous states, then returns added, removed, and modified files.

This is a solid systems choice. It keeps reindexing bounded and makes the tool more plausible on real repos where full reindexing every time would be annoying.

#### 5) MCP operations layer

The MCP package is where the project stops being “index some files” and becomes “operate a retrieval service for agents.” [`packages/mcp/src/index.ts`](https://github.com/zilliztech/claude-context/blob/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/mcp/src/index.ts) wires up the server and tool contracts. [`packages/mcp/src/handlers.ts`](https://github.com/zilliztech/claude-context/blob/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/mcp/src/handlers.ts) runs the real workflows: cloud sync, absolute-path validation, background indexing, index recovery, and search behavior. [`packages/mcp/src/snapshot.ts`](https://github.com/zilliztech/claude-context/blob/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/mcp/src/snapshot.ts) persists codebase state and defends against a nasty “0/0 indexed” poisoning bug.

This operational layer is probably the biggest underappreciated part of the repo.

### Request / data / control flow

A typical indexing flow looks like this:

1. agent or editor calls `index_codebase` through the MCP server in [`packages/mcp/src/index.ts`](https://github.com/zilliztech/claude-context/blob/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/mcp/src/index.ts)
2. request lands in [`packages/mcp/src/handlers.ts`](https://github.com/zilliztech/claude-context/blob/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/mcp/src/handlers.ts), which validates path, snapshot state, collection state, and background-task setup
3. the core [`Context`](https://github.com/zilliztech/claude-context/blob/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/core/src/context.ts) scans files, applies ignore rules, and chunks files via AST or fallback splitter
4. chunk batches are embedded and inserted into Milvus/Zilliz through [`packages/core/src/vectordb`](https://github.com/zilliztech/claude-context/tree/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/core/src/vectordb)
5. snapshot and Merkle state are updated so future runs can reuse and incrementally sync
6. later, `search_code` generates a query embedding, runs hybrid retrieval, and returns snippets with file paths and line ranges

The important point is that the system is built around persistent indexing state, not ephemeral one-shot retrieval.

## Key directories and files

- [`README.md`](https://github.com/zilliztech/claude-context/blob/66d761633b5bc308c2d55a0c6287bc1d6aac4933/README.md), product overview and supported integration surfaces
- [`packages/core/src/context.ts`](https://github.com/zilliztech/claude-context/blob/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/core/src/context.ts), the main orchestration file and best starting point for understanding the system
- [`packages/core/src/splitter/ast-splitter.ts`](https://github.com/zilliztech/claude-context/blob/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/core/src/splitter/ast-splitter.ts), syntax-aware chunking logic with fallback behavior
- [`packages/core/src/sync/synchronizer.ts`](https://github.com/zilliztech/claude-context/blob/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/core/src/sync/synchronizer.ts), Merkle-based change detection and snapshot persistence
- [`packages/core/src/vectordb/milvus-restful-vectordb.ts`](https://github.com/zilliztech/claude-context/blob/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/core/src/vectordb/milvus-restful-vectordb.ts), vector store adapter and hybrid-collection schema definitions
- [`packages/mcp/src/index.ts`](https://github.com/zilliztech/claude-context/blob/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/mcp/src/index.ts), MCP entrypoint and tool declarations
- [`packages/mcp/src/handlers.ts`](https://github.com/zilliztech/claude-context/blob/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/mcp/src/handlers.ts), operational workflow logic and startup healing
- [`packages/mcp/src/snapshot.ts`](https://github.com/zilliztech/claude-context/blob/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/mcp/src/snapshot.ts), local persistent state model and corruption-avoidance logic
- [`packages/vscode-extension/src/extension.ts`](https://github.com/zilliztech/claude-context/blob/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/vscode-extension/src/extension.ts), editor-side integration entrypoint
- [`evaluation`](https://github.com/zilliztech/claude-context/tree/66d761633b5bc308c2d55a0c6287bc1d6aac4933/evaluation), useful if you want to inspect how seriously they test retrieval claims

## Important components

### `Context`

[`packages/core/src/context.ts`](https://github.com/zilliztech/claude-context/blob/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/core/src/context.ts) is effectively the application kernel. If you understand this class, you understand most of the product.

### `AstCodeSplitter`

[`packages/core/src/splitter/ast-splitter.ts`](https://github.com/zilliztech/claude-context/blob/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/core/src/splitter/ast-splitter.ts) is where repo semantics get preserved instead of being flattened into arbitrary character windows.

### `FileSynchronizer`

[`packages/core/src/sync/synchronizer.ts`](https://github.com/zilliztech/claude-context/blob/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/core/src/sync/synchronizer.ts) is the component that makes incremental indexing believable.

### `MilvusRestfulVectorDatabase`

[`packages/core/src/vectordb/milvus-restful-vectordb.ts`](https://github.com/zilliztech/claude-context/blob/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/core/src/vectordb/milvus-restful-vectordb.ts) is a good example of environment-sensitive adapter design. They explicitly keep a REST path for constrained environments like VS Code extensions.

### `SnapshotManager` and MCP handlers

[`packages/mcp/src/snapshot.ts`](https://github.com/zilliztech/claude-context/blob/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/mcp/src/snapshot.ts) and [`packages/mcp/src/handlers.ts`](https://github.com/zilliztech/claude-context/blob/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/mcp/src/handlers.ts) carry a lot of the production hardening. The code is a little sprawling, but it clearly comes from debugging real state-sync failures.

## Important knobs / configs / extension points

- embedding provider and model selection via [`packages/mcp/src/config.ts`](https://github.com/zilliztech/claude-context/blob/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/mcp/src/config.ts)
- `HYBRID_MODE`, which flips dense-only vs hybrid retrieval behavior inside [`packages/core/src/context.ts`](https://github.com/zilliztech/claude-context/blob/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/core/src/context.ts)
- `CUSTOM_EXTENSIONS` and `CUSTOM_IGNORE_PATTERNS`, which extend file-discovery rules in [`packages/core/src/context.ts`](https://github.com/zilliztech/claude-context/blob/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/core/src/context.ts)
- `EMBEDDING_BATCH_SIZE`, which controls chunk batching in [`packages/core/src/context.ts`](https://github.com/zilliztech/claude-context/blob/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/core/src/context.ts)
- the splitter choice exposed by MCP in [`packages/mcp/src/index.ts`](https://github.com/zilliztech/claude-context/blob/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/mcp/src/index.ts)
- vector DB backend implementations under [`packages/core/src/vectordb`](https://github.com/zilliztech/claude-context/tree/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/core/src/vectordb)

## Practical questions and answers

### Is this just an MCP wrapper around embeddings?

No. The core engine matters here. The MCP layer is only one surface over a more real indexing/retrieval system.

### What is the smartest architectural choice?

Hybrid retrieval plus AST-aware chunking. Those two choices address the two biggest ways code search systems get dumb: bad chunk boundaries and bad lexical recall.

### What is the most reusable idea for our own work?

Treat retrieval state as a product surface. Their snapshot-healing and sync logic is a reminder that agent tools live or die on operational trust, not just demo relevance scores.

### Where does this feel brittle?

Large god classes, lots of mutable local state, and a tight dependency on Milvus/Zilliz assumptions. It is not yet a beautifully narrow kernel.

### Does the repo show signs of real production pain?

Yes. The snapshot poisoning defenses in [`packages/mcp/src/snapshot.ts`](https://github.com/zilliztech/claude-context/blob/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/mcp/src/snapshot.ts) and startup healing in [`packages/mcp/src/handlers.ts`](https://github.com/zilliztech/claude-context/blob/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/mcp/src/handlers.ts) look like fixes for bugs that actually hurt users.

## What is smart

- using AST chunking where available, not pretending all files should be split the same way
- combining sparse and dense retrieval rather than betting on vectors alone
- keeping a RESTful Milvus adapter for constrained environments
- adding Merkle-based file change detection instead of brute-force full reindex loops
- treating snapshot corruption and out-of-sync cloud/local state as first-class problems
- packaging the same engine behind multiple surfaces instead of duplicating logic per client

## What is flawed or weak

- [`packages/core/src/context.ts`](https://github.com/zilliztech/claude-context/blob/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/core/src/context.ts) and [`packages/mcp/src/handlers.ts`](https://github.com/zilliztech/claude-context/blob/66d761633b5bc308c2d55a0c6287bc1d6aac4933/packages/mcp/src/handlers.ts) are doing too much, which will make future refactors harder
- there is a lot of console-driven operational logic, which is useful in practice but not especially elegant
- the product story is still heavily tied to Zilliz/Milvus, even if the interfaces try to look generic
- tree-sitter coverage is good but still partial, so some languages inevitably fall back to rougher chunking
- the README marketing pitch is cleaner than the underlying operational complexity, which means adopters may underestimate setup and failure modes

## What we can learn / steal

- hybrid retrieval should be the default for code, not an optional nice-to-have
- AST chunking with graceful fallback is a strong practical design, better than purity in either direction
- state recovery logic is part of the product, not maintenance trivia
- if a repo has background indexing, it also needs clear snapshot semantics and corruption guards
- one engine with multiple adapters is usually better than separate products that drift apart

## How we could apply it

For our own tooling, the most reusable pattern is:

1. define one indexing/search kernel
2. make retrieval hybrid by default
3. preserve syntax structure when chunking
4. store enough persistent local state to support incremental refresh and crash recovery
5. expose the same kernel through agent tools, CLI, and IDE surfaces

The operational lesson matters most: once an agent depends on retrieval, “what happens when local state and remote state disagree?” becomes a core product question.

## Bottom line

Claude Context is not just hot because “MCP” is hot. It is interesting because it contains a real retrieval engine plus the messy state-management work needed to keep that engine useful in an agent workflow.

My main takeaway is that the best part of the repo is not the vector search itself. It is the way they treat indexing, recovery, and retrieval as one continuous system. That is the difference between a demo and a tool people can keep installed.