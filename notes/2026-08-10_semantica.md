# Semantica

- Repo: `semantica-agi/semantica`
- URL: https://github.com/semantica-agi/semantica
- Date: 2026-08-10
- Repo snapshot studied: `main` @ `6f310d1d7acf11013dc7e68d4e68823eb96cec4d`
- Why picked today: GitHub daily trending showed 3,911 stars, 461 forks, and 967 stars added today when checked. More importantly, this is not another thin "graph RAG" wrapper. The repo has a real package tree, multiple runtime surfaces, and source files that show an actual attempt to turn provenance, reasoning, and agent context into infrastructure.

## Executive summary
`semantica` is trying to be a full accountability substrate for AI systems rather than a single library. The repo breaks into five real layers: a facade and lifecycle layer in [`semantica/core/orchestrator.py`](https://github.com/semantica-agi/semantica/blob/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/semantica/core/orchestrator.py), a large in-memory context and decision layer in [`semantica/context/context_graph.py`](https://github.com/semantica-agi/semantica/blob/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/semantica/context/context_graph.py), ingestion and graph-building modules such as [`semantica/ingest/repo_ingestor.py`](https://github.com/semantica-agi/semantica/blob/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/semantica/ingest/repo_ingestor.py) and [`semantica/kg/graph_builder.py`](https://github.com/semantica-agi/semantica/blob/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/semantica/kg/graph_builder.py), reasoning and ontology modules such as [`semantica/reasoning/reasoner.py`](https://github.com/semantica-agi/semantica/blob/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/semantica/reasoning/reasoner.py), and interface surfaces including the JSON-RPC MCP server in [`mcp/server.py`](https://github.com/semantica-agi/semantica/blob/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/mcp/server.py).

The strongest signal is not the README rhetoric. It is the source layout. The top-level tree includes [`semantica`](https://github.com/semantica-agi/semantica/tree/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/semantica), [`explorer`](https://github.com/semantica-agi/semantica/tree/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/explorer), [`integrations`](https://github.com/semantica-agi/semantica/tree/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/integrations), [`plugins`](https://github.com/semantica-agi/semantica/tree/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/plugins), [`cookbook`](https://github.com/semantica-agi/semantica/tree/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/cookbook), and a large [`tests`](https://github.com/semantica-agi/semantica/tree/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/tests) suite. That means the product surface is broad enough to be studied as a system, not just as a concept.

The biggest weakness is sprawl. [`pyproject.toml`](https://github.com/semantica-agi/semantica/blob/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/pyproject.toml) labels the base dependency set as a "safe default" even though it already pulls in `torch`, `transformers`, `spacy`, `faiss-cpu`, `opencv-python`, `librosa`, `sentence-transformers`, and more. The repo also has a telltale "god object" smell: [`context_graph.py`](https://github.com/semantica-agi/semantica/blob/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/semantica/context/context_graph.py) is not just a graph container. It wants to be graph store, policy layer, decision recorder, analytics hub, and hybrid search surface at the same time.

## What they built
They built a graph-heavy package for turning raw sources into auditable agent context:

- [`semantica/context`](https://github.com/semantica-agi/semantica/tree/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/semantica/context): in-memory context graph, decision recording, policy checks, causal analysis, and precedent search.
- [`semantica/ingest`](https://github.com/semantica-agi/semantica/tree/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/semantica/ingest): file, repo, API, email, Databricks, Snowflake, Google Drive, and MCP ingestion paths.
- [`semantica/kg`](https://github.com/semantica-agi/semantica/tree/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/semantica/kg): graph building, temporal reasoning, and graph algorithms.
- [`semantica/reasoning`](https://github.com/semantica-agi/semantica/tree/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/semantica/reasoning): deductive, abductive, Datalog, SPARQL, graph, and Rete-style reasoning layers.
- [`semantica/ontology`](https://github.com/semantica-agi/semantica/tree/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/semantica/ontology): ontology generation, validation, naming, and documentation.
- [`mcp`](https://github.com/semantica-agi/semantica/tree/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/mcp) and [`semantica/mcp_server`](https://github.com/semantica-agi/semantica/tree/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/semantica/mcp_server): MCP entry points for tool and resource exposure.

## Why it matters
Most agent-memory products collapse into "chunk some text, embed it, and add a dashboard." This repo matters because the code keeps pushing toward a more explicit contract:

1. Context is a graph structure with first-class decisions, not just a retrieval cache.
2. Ingestion is treated as a multi-source systems problem, not a file upload form.
3. Reasoning is surfaced as its own layer instead of being outsourced entirely to an LLM prompt.
4. Interfaces exist for CLI, explorer, plugins, and MCP, which suggests they want one substrate beneath many agent environments.

## Repo shape at a glance
The repo shape is broad but legible:

- [`pyproject.toml`](https://github.com/semantica-agi/semantica/blob/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/pyproject.toml) defines a very large base package plus many optional extras for graph stores, vector stores, clouds, and LLM providers.
- [`ARCHITECTURE.md`](https://github.com/semantica-agi/semantica/blob/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/ARCHITECTURE.md) is the declared system map.
- [`semantica/core`](https://github.com/semantica-agi/semantica/tree/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/semantica/core) is the facade and lifecycle layer.
- [`semantica/context`](https://github.com/semantica-agi/semantica/tree/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/semantica/context) is the package center of gravity.
- [`semantica/ingest`](https://github.com/semantica-agi/semantica/tree/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/semantica/ingest), [`semantica/kg`](https://github.com/semantica-agi/semantica/tree/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/semantica/kg), and [`semantica/reasoning`](https://github.com/semantica-agi/semantica/tree/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/semantica/reasoning) hold the actual pipeline and inference mechanics.
- [`semantica/explorer/routes`](https://github.com/semantica-agi/semantica/tree/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/semantica/explorer/routes) shows the productized web surface with graph, decisions, ontology, provenance, SPARQL, and temporal routes.

## Layered architecture dissection
### High-level system shape
The high-level shape is: ingest heterogeneous sources, normalize them into entities and relationships, construct a graph, attach provenance and decision semantics, run deterministic reasoning passes, then expose the result through code APIs, an explorer UI, and MCP.

### Main layers
**1. Facade and lifecycle layer**  
[`semantica/core/orchestrator.py`](https://github.com/semantica-agi/semantica/blob/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/semantica/core/orchestrator.py) defines a lazy-loading `Semantica` facade. It wires config, lifecycle management, plugin registry, provenance storage, and module getters for embeddings, graph building, reasoning, parsing, and ingestion. That is a sensible "one import for users, lazy internals for everything else" move.

**2. Context and decision layer**  
[`semantica/context/context_graph.py`](https://github.com/semantica-agi/semantica/blob/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/semantica/context/context_graph.py) is where the repo's philosophy becomes concrete. It is an in-memory graph store plus decision recording, precedent search, causal tracing, policy enforcement, centrality analysis, community detection, and hybrid similarity. That file is both the most interesting part of the package and the clearest sign of architectural concentration risk.

**3. Ingestion and graph-construction layer**  
[`semantica/ingest/repo_ingestor.py`](https://github.com/semantica-agi/semantica/blob/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/semantica/ingest/repo_ingestor.py) handles git cloning, file extraction, language detection, commit analysis, and dependency/doc extraction. [`semantica/kg/graph_builder.py`](https://github.com/semantica-agi/semantica/blob/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/semantica/kg/graph_builder.py) turns extracted items into entities and relationships, with options for merge strategies, conflict resolution, and temporal features.

**4. Reasoning and ontology layer**  
[`semantica/reasoning/reasoner.py`](https://github.com/semantica-agi/semantica/blob/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/semantica/reasoning/reasoner.py) is a facade over rule-based reasoning. The broader [`semantica/reasoning`](https://github.com/semantica-agi/semantica/tree/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/semantica/reasoning) tree suggests they want multiple reasoning modes living beside each other: Datalog, deductive, graph, temporal, SPARQL, and Rete.

**5. Interface layer**  
[`mcp/server.py`](https://github.com/semantica-agi/semantica/blob/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/mcp/server.py) is intentionally thin: JSON-RPC over stdio, tool listing, tool dispatch, resource reads, and minimal server info. That is good. The server is a transport shell around existing tool definitions instead of a second business-logic stack.

### Request / data / control flow
1. A caller enters through the [`Semantica`](https://github.com/semantica-agi/semantica/blob/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/semantica/core/orchestrator.py) facade, which lazy-loads only the needed subsystems.
2. An ingestor such as [`repo_ingestor.py`](https://github.com/semantica-agi/semantica/blob/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/semantica/ingest/repo_ingestor.py) pulls raw source material into typed content objects.
3. [`graph_builder.py`](https://github.com/semantica-agi/semantica/blob/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/semantica/kg/graph_builder.py) turns extracted entities and relationships into a graph, optionally merging duplicates and resolving conflicts.
4. [`context_graph.py`](https://github.com/semantica-agi/semantica/blob/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/semantica/context/context_graph.py) stores decisions, relationships, analytics state, and graph metrics.
5. [`reasoner.py`](https://github.com/semantica-agi/semantica/blob/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/semantica/reasoning/reasoner.py) or one of the more specialized reasoning modules derives new conclusions from facts and rules.
6. External tools reach the graph through [`mcp/server.py`](https://github.com/semantica-agi/semantica/blob/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/mcp/server.py) or the explorer routes under [`semantica/explorer/routes`](https://github.com/semantica-agi/semantica/tree/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/semantica/explorer/routes).

## Key directories and files
- [`pyproject.toml`](https://github.com/semantica-agi/semantica/blob/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/pyproject.toml): package contract and optional-backend story.
- [`ARCHITECTURE.md`](https://github.com/semantica-agi/semantica/blob/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/ARCHITECTURE.md): declared system decomposition.
- [`semantica/core/orchestrator.py`](https://github.com/semantica-agi/semantica/blob/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/semantica/core/orchestrator.py): top-level facade and lazy module loader.
- [`semantica/context/context_graph.py`](https://github.com/semantica-agi/semantica/blob/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/semantica/context/context_graph.py): in-memory graph plus analytics and decision substrate.
- [`semantica/ingest/repo_ingestor.py`](https://github.com/semantica-agi/semantica/blob/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/semantica/ingest/repo_ingestor.py): a good example of the repo's ingestion ambition.
- [`semantica/kg/graph_builder.py`](https://github.com/semantica-agi/semantica/blob/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/semantica/kg/graph_builder.py): graph construction and conflict hooks.
- [`semantica/reasoning/reasoner.py`](https://github.com/semantica-agi/semantica/blob/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/semantica/reasoning/reasoner.py): high-level rule engine facade.
- [`mcp/server.py`](https://github.com/semantica-agi/semantica/blob/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/mcp/server.py): MCP transport and dispatch.

## Important components
The most important component is [`ContextGraph`](https://github.com/semantica-agi/semantica/blob/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/semantica/context/context_graph.py). It is where Semantica stops being a thesis statement and becomes a working memory, decision, and analytics runtime.

The second is the [`Semantica` facade](https://github.com/semantica-agi/semantica/blob/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/semantica/core/orchestrator.py). Lazy-loading subsystems through properties is a practical way to survive a package this broad.

The third is [`GraphBuilder`](https://github.com/semantica-agi/semantica/blob/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/semantica/kg/graph_builder.py). That is the bridge between ingestion outputs and the higher-level graph abstractions.

The fourth is [`mcp/server.py`](https://github.com/semantica-agi/semantica/blob/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/mcp/server.py). It is simple on purpose, which is the right instinct for an interface layer.

## Important knobs / configs / extension points
- [`pyproject.toml`](https://github.com/semantica-agi/semantica/blob/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/pyproject.toml) exposes the extension surface through extras for graph stores, vector stores, cloud providers, LLM providers, SHACL, GPU, and more.
- [`graph_builder.py`](https://github.com/semantica-agi/semantica/blob/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/semantica/kg/graph_builder.py) carries the most consequential runtime knobs: `merge_entities`, `entity_resolution_strategy`, `resolve_conflicts`, `enable_temporal`, `track_history`, and `version_snapshots`.
- [`context_graph.py`](https://github.com/semantica-agi/semantica/blob/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/semantica/context/context_graph.py) exposes builder-facing switches such as advanced analytics, centrality analysis, community detection, and node embeddings through the constructor examples and method surface.
- [`orchestrator.py`](https://github.com/semantica-agi/semantica/blob/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/semantica/core/orchestrator.py) reads nested config like `provenance.storage_path`, which is a small but useful sign that infrastructure concerns are being treated as first-class config.

## Practical questions and answers
**Is this just graph-RAG marketing with a larger README than codebase?**  
No. The README is loud, but the source tree is louder. The package structure, ingestors, graph builder, reasoning modules, explorer routes, and MCP server all exist as real code.

**What is the actual center of gravity?**  
[`semantica/context/context_graph.py`](https://github.com/semantica-agi/semantica/blob/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/semantica/context/context_graph.py). That file is where the product worldview gets encoded: decisions become graph objects, analytics are built in, and provenance plus policy are assumed rather than bolted on.

**Where should a builder start reading?**  
Start with [`pyproject.toml`](https://github.com/semantica-agi/semantica/blob/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/pyproject.toml) to understand the ambition, then [`semantica/core/orchestrator.py`](https://github.com/semantica-agi/semantica/blob/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/semantica/core/orchestrator.py), [`semantica/context/context_graph.py`](https://github.com/semantica-agi/semantica/blob/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/semantica/context/context_graph.py), [`semantica/ingest/repo_ingestor.py`](https://github.com/semantica-agi/semantica/blob/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/semantica/ingest/repo_ingestor.py), and [`semantica/kg/graph_builder.py`](https://github.com/semantica-agi/semantica/blob/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/semantica/kg/graph_builder.py).

**What feels brittle in production?**  
The breadth. The repo wants to support too many backends, too many processing modes, and too many interfaces from one package. That can work, but only if module boundaries stay strict. Right now the dependency footprint and the size of the context layer suggest that boundary discipline is under pressure.

## What is smart
- Using one facade to lazy-load a very broad subsystem graph instead of eagerly importing the world.
- Treating provenance, policy, and decision history as structural features rather than reporting add-ons.
- Building a thin MCP transport layer that dispatches into existing definitions instead of duplicating business logic there.
- Shipping many ingestors because real enterprise context is a source-integration problem before it is a prompting problem.

## What is flawed or weak
- The base dependency set is too heavy to honestly call a safe default.
- [`context_graph.py`](https://github.com/semantica-agi/semantica/blob/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/semantica/context/context_graph.py) appears to carry too many responsibilities.
- The repo pitch leans hard into "Open Source Palantir" branding, which invites skepticism the code then has to work extra hard to overcome.
- The MCP surface is split across top-level [`mcp`](https://github.com/semantica-agi/semantica/tree/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/mcp) and package-level [`semantica/mcp_server`](https://github.com/semantica-agi/semantica/tree/6f310d1d7acf11013dc7e68d4e68823eb96cec4d/semantica/mcp_server), which works but hints at some interface duplication.

## What we can learn / steal
- Put the interface layer on a short leash. `mcp/server.py` is lean because it mostly routes.
- If a system has to handle many source types, isolate that complexity in dedicated ingestors instead of burying it in one giant import pipeline.
- Auditable agent infrastructure gets more believable when decisions are explicit graph objects rather than log messages.
- Lazy module loading is not glamorous, but it is one of the few sane ways to make a package this broad usable.

## How we could apply it
If we wanted an auditable memory substrate for our own agent systems, I would copy the overall shape more than the exact implementation: one facade, explicit ingestors, a graph-building layer, first-class decision objects, and thin external surfaces like MCP. I would be stricter than this repo about dependency slimming and module boundaries, but the structural idea is worth studying.

## Bottom line
`semantica` is interesting because it is genuinely trying to turn context, provenance, and reasoning into infrastructure rather than into UI copy.

The builder lesson is that serious agent accountability needs explicit data structures and multiple access surfaces, but the cost of that ambition is architectural sprawl that has to be managed relentlessly.
