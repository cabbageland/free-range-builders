# TencentDB Agent Memory

- Repo: `TencentCloud/TencentDB-Agent-Memory`
- URL: https://github.com/TencentCloud/TencentDB-Agent-Memory
- Date: 2026-08-02
- Repo snapshot studied: `feat/server_team` @ `f3df79326dfd763f45199c441e2129d780467949`
- Why picked today: It appeared on GitHub's daily trending page when checked, and the repo API already showed 10,700 stars and 1,017 forks. More importantly, this is a real multi-service memory system with capture, extraction, recall, governance, and agent-injection code in public, not another "AI memory" landing page wrapped around a vector store.

## Executive summary
`TencentDB-Agent-Memory` is not mainly a memory database. The interesting thing is the control-plane split across [`MemoryCore`](https://github.com/TencentCloud/TencentDB-Agent-Memory/tree/f3df79326dfd763f45199c441e2129d780467949/MemoryCore), [`MemoryKnowledge`](https://github.com/TencentCloud/TencentDB-Agent-Memory/tree/f3df79326dfd763f45199c441e2129d780467949/MemoryKnowledge), [`MemoryProxy`](https://github.com/TencentCloud/TencentDB-Agent-Memory/tree/f3df79326dfd763f45199c441e2129d780467949/MemoryProxy), and [`MemoryPanel`](https://github.com/TencentCloud/TencentDB-Agent-Memory/tree/f3df79326dfd763f45199c441e2129d780467949/MemoryPanel). That split lets the project treat "memory" as four separate jobs: capture raw conversation, extract structured memory, expose document/code assets as tools, and govern who gets which assets.

The smartest move is the repo's refusal to inject everything by default. The product framing in [`README.md`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/README.md) describes L0 through L3 memory layers, but the runtime code goes further: [`MemoryProxy/src/injection/injectors/tdai-profile-memory-injector.ts`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/MemoryProxy/src/injection/injectors/tdai-profile-memory-injector.ts) injects L3 persona plus an L2 scene index, then tells the agent to fetch L1/L0 details with tools on demand. That is a better memory policy than dumping a giant recall blob into every request.

The second smart move is capture discipline. [`MemoryCore/src/core/hooks/auto-capture.ts`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/MemoryCore/src/core/hooks/auto-capture.ts) combines L0 recording and checkpoint advancement under an atomic lock so concurrent agent-end events do not duplicate records. That is exactly the kind of boring correctness work most "memory for agents" repos skip.

## What they built
They built a team-level memory stack for agents where conversation memory, docs, and code all become governed assets:

- [`README.md`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/README.md) defines the product shape as layered memory plus asset binding rather than as one retrieval API.
- [`MemoryCore`](https://github.com/TencentCloud/TencentDB-Agent-Memory/tree/f3df79326dfd763f45199c441e2129d780467949/MemoryCore) handles raw conversation capture, L1 extraction/dedup, and recall.
- [`MemoryKnowledge`](https://github.com/TencentCloud/TencentDB-Agent-Memory/tree/f3df79326dfd763f45199c441e2129d780467949/MemoryKnowledge) turns wikis and code graphs into queryable resources with a read-only tool surface.
- [`MemoryProxy`](https://github.com/TencentCloud/TencentDB-Agent-Memory/tree/f3df79326dfd763f45199c441e2129d780467949/MemoryProxy) sits in front of agent traffic and injects context blocks at protocol-specific anchors.
- [`MemoryPanel`](https://github.com/TencentCloud/TencentDB-Agent-Memory/tree/f3df79326dfd763f45199c441e2129d780467949/MemoryPanel) acts as the governance/control surface for listing, creating, binding, and reading those assets.

## Why it matters
This repo matters because most public agent-memory projects are really one of two things: a vector index with a nice README, or a prompt-prepend trick pretending to be long-term memory. `TencentDB-Agent-Memory` is more serious than that:

1. It separates capture, extraction, retrieval, and injection into different subsystems.
2. It treats docs and code as callable tools, not just more chunks to stuff into embeddings.
3. It adds ACL and fixed-binding logic so shared memory can exist without becoming a universal prompt leak.
4. It exposes the ugly operational truth: asynchronous builds, multiple services, caches, and protocol adapters are part of the real product.

## Repo shape at a glance
The repository is opinionated and modular rather than monolithic:

- [`MemoryCore`](https://github.com/TencentCloud/TencentDB-Agent-Memory/tree/f3df79326dfd763f45199c441e2129d780467949/MemoryCore): memory runtime, extraction pipeline, storage adapters, and OpenClaw-facing plugin surfaces.
- [`MemoryKnowledge`](https://github.com/TencentCloud/TencentDB-Agent-Memory/tree/f3df79326dfd763f45199c441e2129d780467949/MemoryKnowledge): wiki/code-graph ingestion, graph search, and tool execution routes.
- [`MemoryProxy`](https://github.com/TencentCloud/TencentDB-Agent-Memory/tree/f3df79326dfd763f45199c441e2129d780467949/MemoryProxy): protocol adapters, injectors, identity routing, and session caches.
- [`MemoryPanel`](https://github.com/TencentCloud/TencentDB-Agent-Memory/tree/f3df79326dfd763f45199c441e2129d780467949/MemoryPanel): HTTP routes and domain logic for knowledge and chat-memory governance.
- [`INSTALL.md`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/INSTALL.md), [`README.deployment.md`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/README.deployment.md), and [`README.docker.md`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/README.docker.md): operational surfaces proving this is meant to be deployed, not only read.

## Layered architecture dissection
### High-level system shape
The system shape is: agent conversations are captured into L0, filtered and lifted into L1 structured memories, summarized into L2/L3 user-and-agent context, and then selectively reintroduced through proxy hooks and read-only knowledge tools. Documents and repositories do not automatically become prompt text. They become separate assets that an agent can discover through a tool registry and read only when needed.

That is a healthier mental model than "memory = vector search." It makes memory cost-aware and policy-aware.

### Main layers
**1. Product framing and memory model**  
[`README.md`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/README.md) explains the L0/L1/L2/L3 hierarchy and the asset model. It is not mere marketing; the layer names map onto actual files and control paths in the codebase.

**2. Capture, extraction, and recall layer**  
[`MemoryCore/src/core/hooks/auto-capture.ts`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/MemoryCore/src/core/hooks/auto-capture.ts), [`MemoryCore/src/core/record/l1-extractor.ts`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/MemoryCore/src/core/record/l1-extractor.ts), and [`MemoryCore/src/core/hooks/auto-recall.ts`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/MemoryCore/src/core/hooks/auto-recall.ts) are the core runtime trio. They record raw turns, run scene-aware L1 extraction plus dedup, and perform hybrid recall with persona and scene loading.

**3. Knowledge-asset layer**  
[`MemoryKnowledge/src/routes/tools.ts`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/MemoryKnowledge/src/routes/tools.ts) exposes `/tools/list` and `/tools/call` for wiki and code-graph resources, while [`MemoryKnowledge/src/engines/wiki/graph-search.ts`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/MemoryKnowledge/src/engines/wiki/graph-search.ts) implements multi-hop graph expansion with decay and node caps.

**4. Injection and protocol-adaptation layer**  
[`MemoryProxy/src/injection/pipeline.ts`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/MemoryProxy/src/injection/pipeline.ts) parses provider-specific request bodies into a neutral context, runs hooks, and writes the modified request back out. This is the layer that turns memory policy into actual model input.

**5. Governance and panel layer**  
[`MemoryPanel/src/panel/http/routes/knowledge/wiki-routes.ts`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/MemoryPanel/src/panel/http/routes/knowledge/wiki-routes.ts) shows the control-plane pattern: validate headers, check ACL, and then proxy the allowed operation to the knowledge service.

### Request / data / control flow
1. An agent session ends and [`performAutoCapture`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/MemoryCore/src/core/hooks/auto-capture.ts) records the new L0 slice while atomically advancing the per-session cursor.
2. [`extractL1Memories`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/MemoryCore/src/core/record/l1-extractor.ts) filters low-quality turns, scene-segments the remaining messages in one LLM pass, then batch-deduplicates before storing records.
3. When recall is needed, [`performAutoRecall`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/MemoryCore/src/core/hooks/auto-recall.ts) runs keyword, embedding, or hybrid search, applies budgets, and also loads scoped L3 persona plus L2 scene navigation.
4. [`InjectionPipeline.process(...)`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/MemoryProxy/src/injection/pipeline.ts) selects the proper protocol adapter, builds an `AgentContext`, identifies the agent profile, and runs registered hooks.
5. [`TdaiProfileMemoryInjector`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/MemoryProxy/src/injection/injectors/tdai-profile-memory-injector.ts) injects persona, an L2 scene index, and a tools guide instead of blindly pasting every recalled record.
6. If the model wants deeper knowledge, [`MemoryKnowledge/src/routes/tools.ts`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/MemoryKnowledge/src/routes/tools.ts) whitelists the read-only wiki/code-graph calls, and [`wiki-routes.ts`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/MemoryPanel/src/panel/http/routes/knowledge/wiki-routes.ts) enforces the panel-side permissions around those assets.

## Key directories and files
- [`MemoryCore/src/core/hooks/auto-capture.ts`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/MemoryCore/src/core/hooks/auto-capture.ts): atomic L0 recording and checkpoint advancement.
- [`MemoryCore/src/core/record/l1-extractor.ts`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/MemoryCore/src/core/record/l1-extractor.ts): the LLM-based scene segmentation, extraction, and dedup pipeline.
- [`MemoryCore/src/core/hooks/auto-recall.ts`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/MemoryCore/src/core/hooks/auto-recall.ts): hybrid search, persona load, scene load, and budget handling.
- [`MemoryKnowledge/src/routes/tools.ts`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/MemoryKnowledge/src/routes/tools.ts): read-only tool registry and dispatcher for wiki/code-graph assets.
- [`MemoryKnowledge/src/engines/wiki/graph-search.ts`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/MemoryKnowledge/src/engines/wiki/graph-search.ts): graph-expansion logic instead of plain full-text lookup.
- [`MemoryProxy/src/injection/pipeline.ts`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/MemoryProxy/src/injection/pipeline.ts): protocol-neutral injection orchestration.
- [`MemoryProxy/src/injection/injectors/tdai-profile-memory-injector.ts`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/MemoryProxy/src/injection/injectors/tdai-profile-memory-injector.ts): the clearest statement of the repo's actual memory policy.
- [`MemoryPanel/src/panel/http/routes/knowledge/wiki-routes.ts`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/MemoryPanel/src/panel/http/routes/knowledge/wiki-routes.ts): governance wrapper around wiki operations.

## Important components
The most important component is [`performAutoCapture`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/MemoryCore/src/core/hooks/auto-capture.ts). It solves a real systems problem by holding the lock across cursor read, record write, and cursor advance. That turns "conversation memory" from a nice demo into something less likely to duplicate or corrupt under concurrency.

The second is [`extractL1Memories`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/MemoryCore/src/core/record/l1-extractor.ts). It does not simply embed chat logs. It filters, scene-segments, extracts structured memories, and batch-deduplicates them before storage.

The third is [`createToolsRoutes`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/MemoryKnowledge/src/routes/tools.ts). That file turns documents and code into a controlled tool surface with explicit whitelists, which is much cleaner than covertly pasting repo text into the prompt.

The fourth is [`InjectionPipeline`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/MemoryProxy/src/injection/pipeline.ts). It is the bridge between storage semantics and real inference traffic.

The fifth is [`TdaiProfileMemoryInjector`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/MemoryProxy/src/injection/injectors/tdai-profile-memory-injector.ts). It makes the repo's core bet explicit: inject small, stable memory directly; keep heavier memory behind tools.

## Important knobs / configs / extension points
- Recall behavior lives in [`auto-recall.ts`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/MemoryCore/src/core/hooks/auto-recall.ts): strategy selection, timeout handling, hybrid search, and recall budgeting.
- Extraction shape lives in [`l1-extractor.ts`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/MemoryCore/src/core/record/l1-extractor.ts): max messages per extraction, background-window size, dedup toggle, and memory cap per session.
- Asset query capabilities live in [`tools.ts`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/MemoryKnowledge/src/routes/tools.ts): the allowed wiki/code-graph tool names are explicit extension points.
- Injection policy lives in [`tdai-profile-memory-injector.ts`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/MemoryProxy/src/injection/injectors/tdai-profile-memory-injector.ts): cache strategy, anchor slot, and tool-guide behavior are all first-class knobs.
- Governance policy lives in [`wiki-routes.ts`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/MemoryPanel/src/panel/http/routes/knowledge/wiki-routes.ts): read versus write gating and team-bound operations are visible instead of magical.

## Practical questions and answers
**Is this basically just RAG with branding?**  
No. The repo has retrieval pieces, but the more important move is asset governance plus injection policy. [`tools.ts`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/MemoryKnowledge/src/routes/tools.ts) and [`tdai-profile-memory-injector.ts`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/MemoryProxy/src/injection/injectors/tdai-profile-memory-injector.ts) show that the repo is deciding what should be in prompt, what should stay in tools, and who can read which asset.

**What is the most reusable design move here?**  
Inject L3 persona and an L2 index directly, but make L1/L0 and knowledge assets on-demand. That keeps prompts lighter and gives the model a map before it gets the raw payload.

**Where should a builder start reading?**  
Start with [`README.md`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/README.md), then go to [`auto-capture.ts`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/MemoryCore/src/core/hooks/auto-capture.ts), [`auto-recall.ts`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/MemoryCore/src/core/hooks/auto-recall.ts), [`tools.ts`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/MemoryKnowledge/src/routes/tools.ts), and [`pipeline.ts`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/MemoryProxy/src/injection/pipeline.ts).

**Where would this likely hurt in production?**  
The service split is powerful but expensive. Four packages, asynchronous knowledge builds, ACL checks, protocol adapters, and injection caches mean there are many places for latency and policy drift to creep in. The README itself admits some parts are still under iteration, especially automated routing and private-repo support.

## What is smart
- Using atomic capture in [`auto-capture.ts`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/MemoryCore/src/core/hooks/auto-capture.ts) instead of pretending memory ingestion is single-threaded.
- Running scene segmentation, extraction, and dedup as a deliberate L1 pipeline in [`l1-extractor.ts`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/MemoryCore/src/core/record/l1-extractor.ts).
- Treating wiki/code assets as discoverable read-only tools in [`tools.ts`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/MemoryKnowledge/src/routes/tools.ts).
- Injecting L2/L3 as orientation while keeping heavier recall behind tools in [`tdai-profile-memory-injector.ts`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/MemoryProxy/src/injection/injectors/tdai-profile-memory-injector.ts).

## What is flawed or weak
- The repo's default branch being [`feat/server_team`](https://github.com/TencentCloud/TencentDB-Agent-Memory/tree/feat/server_team) is a small but telling signal that the public release still feels a bit mid-flight.
- The architecture is powerful, but the operational surface is heavy: multiple services, caches, ACL layers, and protocol-specific adapters mean this is not a casual plug-in.
- The injected memory blocks in [`tdai-profile-memory-injector.ts`](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/f3df79326dfd763f45199c441e2129d780467949/MemoryProxy/src/injection/injectors/tdai-profile-memory-injector.ts) are still large XML-like slabs. That is more disciplined than naive RAG, but it can still become prompt ballast.
- The README notes that wiki/code-graph builds are asynchronous and fully automated routing is still evolving, which means the system's policy story is stronger than its end-to-end smoothness.

## What we can learn / steal
- Separate memory by stability and retrieval cost instead of treating everything as one index.
- Make knowledge and code callable tools with explicit whitelists rather than invisible prompt stuffing.
- Do the concurrency-hardening work early for capture paths, because duplicate memory records destroy trust fast.
- Use governance routes as first-class product code, not as afterthought glue around a demo.

## How we could apply it
If we build long-lived agent systems, I would steal the asset policy more than the branding. Inject durable persona and scene indices directly, keep volatile details and repo/doc contents behind on-demand tools, and make permission checks explicit at the control plane. That is a much saner default than spraying retrieved text into every prompt.

I would not copy the full service sprawl unless we really need cross-team governance. The architectural principle is worth stealing; the entire deployment footprint should be earned.

## Bottom line
`TencentCloud/TencentDB-Agent-Memory` is worth studying because it exposes the real shape of an agent-memory product: atomic capture, L1 extraction, scoped recall, read-only knowledge tools, prompt injection policy, and governance routes.

The builder lesson is that the best memory systems are not the ones that remember the most. They are the ones that decide what to store, what to inject, what to leave behind a tool call, and who is allowed to touch any of it.
