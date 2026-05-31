# Supermemory

- Repo: `supermemoryai/supermemory`
- URL: https://github.com/supermemoryai/supermemory
- Date: 2026-05-31
- Repo snapshot studied: `main` @ `4eb8399358ce0383214862b705307acc7cb06889`
- Why picked today: It is hot right now on GitHub, clearly AI-related, and more interesting than the average memory-for-agents repo because it is not just a retrieval package. It is a productized memory stack spread across an MCP server, SDK/tooling wrappers, a consumer app, plugin installers, and a graph UI.

## Executive summary
Supermemory is not really a “single memory engine repo” in the way the README pitch first suggests. The public repository is better understood as the packaging and delivery shell around a hosted memory platform. The interesting part is how many surfaces they wrapped around that platform: a Cloudflare-hosted MCP server, prompt-injection middleware for agent frameworks, a Next.js app, plugin install flows, document/memory graph visualization, and multi-client onboarding.

That is both the strength and the caveat.

The strength is product realism. They are not betting on one SDK alone. They are trying to make memory feel native inside Codex, Claude Code, OpenClaw, MCP clients, and their own app.

The caveat is that the core “magic” mostly lives behind `api.supermemory.ai`, so the repo reveals more about distribution architecture than about the actual ranking/extraction/ontology engine they claim as the moat.

My take: this is a very smart integration-and-surface-area repo, but a less transparent systems repo than the branding implies.

## What they built
They built a monorepo for shipping Supermemory across several layers:
- a bun/turbo workspace root in [`package.json`](https://github.com/supermemoryai/supermemory/blob/main/package.json),
- a Cloudflare Worker MCP server in [`apps/mcp/`](https://github.com/supermemoryai/supermemory/tree/main/apps/mcp),
- a user-facing web app in [`apps/web/`](https://github.com/supermemoryai/supermemory/tree/main/apps/web),
- a reusable memory graph UI package in [`packages/memory-graph/`](https://github.com/supermemoryai/supermemory/tree/main/packages/memory-graph),
- agent/framework wrappers in [`packages/tools/`](https://github.com/supermemoryai/supermemory/tree/main/packages/tools),
- smaller shared packages in [`packages/lib/`](https://github.com/supermemoryai/supermemory/tree/main/packages/lib), [`packages/ui/`](https://github.com/supermemoryai/supermemory/tree/main/packages/ui), and [`packages/validation/`](https://github.com/supermemoryai/supermemory/tree/main/packages/validation),
- plus auxiliary client surfaces like the browser extension in [`apps/browser-extension/`](https://github.com/supermemoryai/supermemory/tree/main/apps/browser-extension) and docs in [`apps/docs/`](https://github.com/supermemoryai/supermemory/tree/main/apps/docs).

This is a distribution monorepo, not just an API client.

## Why it matters
A lot of AI memory startups still package themselves as either:
- an embeddings wrapper,
- an MCP toy,
- or a vector-store abstraction with a lot of branding paint.

Supermemory is more serious than that in one particular way: it treats adoption surfaces as part of the product architecture. The repo keeps asking, “how does memory actually get into the agent loop people already use?”

That is why the important layers are not just storage calls. They are:
- protocol exposure through MCP,
- prompt/context injection middleware,
- plugin-specific install flows,
- project-scoped organization,
- graph inspection UI,
- and a consumer-facing app that makes the system legible.

Even if you distrust some of the benchmark-heavy claims in [`README.md`](https://github.com/supermemoryai/supermemory/blob/main/README.md), that go-to-market architecture is genuinely worth studying.

## Repo shape at a glance
Top-level structure:
- [`apps/`](https://github.com/supermemoryai/supermemory/tree/main/apps), product/application surfaces
- [`packages/`](https://github.com/supermemoryai/supermemory/tree/main/packages), reusable libraries and wrappers
- [`skills/`](https://github.com/supermemoryai/supermemory/tree/main/skills), packaged skill assets
- [`.github/workflows/`](https://github.com/supermemoryai/supermemory/tree/main/.github/workflows), CI/release automation

Inside [`apps/`](https://github.com/supermemoryai/supermemory/tree/main/apps), the key split is:
- [`apps/mcp/`](https://github.com/supermemoryai/supermemory/tree/main/apps/mcp), the protocol-facing server and app resource layer
- [`apps/web/`](https://github.com/supermemoryai/supermemory/tree/main/apps/web), the main product UI
- [`apps/browser-extension/`](https://github.com/supermemoryai/supermemory/tree/main/apps/browser-extension), capture/install surface
- [`apps/docs/`](https://github.com/supermemoryai/supermemory/tree/main/apps/docs), developer docs
- [`apps/memory-graph-playground/`](https://github.com/supermemoryai/supermemory/tree/main/apps/memory-graph-playground), isolated graph experimentation

Inside [`packages/`](https://github.com/supermemoryai/supermemory/tree/main/packages), the most important pieces are:
- [`packages/tools/`](https://github.com/supermemoryai/supermemory/tree/main/packages/tools), memory-aware wrappers for agent frameworks and model SDKs
- [`packages/memory-graph/`](https://github.com/supermemoryai/supermemory/tree/main/packages/memory-graph), graph rendering and graph data shaping
- [`packages/lib/`](https://github.com/supermemoryai/supermemory/tree/main/packages/lib), shared app utilities
- [`packages/validation/`](https://github.com/supermemoryai/supermemory/tree/main/packages/validation), API/data contracts
- [`packages/ai-sdk/`](https://github.com/supermemoryai/supermemory/tree/main/packages/ai-sdk), separate SDK packaging surface

This is a monorepo organized around product touchpoints, not around one central backend service.

## Layered architecture dissection
### High-level system shape
At a high level the system looks like this:
1. a hosted API at `api.supermemory.ai` acts as the real memory backend,
2. [`apps/mcp/src/index.ts`](https://github.com/supermemoryai/supermemory/blob/main/apps/mcp/src/index.ts) exposes that backend as an authenticated MCP service on Cloudflare,
3. [`apps/mcp/src/server.ts`](https://github.com/supermemoryai/supermemory/blob/main/apps/mcp/src/server.ts) translates MCP tools/resources/prompts into Supermemory client operations,
4. [`packages/tools/`](https://github.com/supermemoryai/supermemory/tree/main/packages/tools) injects memory/profile retrieval into app and agent frameworks,
5. [`apps/web/`](https://github.com/supermemoryai/supermemory/tree/main/apps/web) gives users a native UI to inspect documents, memories, integrations, and chat,
6. [`packages/memory-graph/`](https://github.com/supermemoryai/supermemory/tree/main/packages/memory-graph) makes the memory structure inspectable rather than invisible.

The notable thing is that the open-source repo mostly wraps and operationalizes a remote backend instead of implementing the full memory engine locally.

### Main layers
**1. Workspace and shipping layer**
- [`package.json`](https://github.com/supermemoryai/supermemory/blob/main/package.json) shows the repo’s real center of gravity: bun workspace management, turbo orchestration, and a mostly TypeScript stack.
- The root dependencies tell a lot about the shape: Hono, Cloudflare, Drizzle, AI SDK packages, Postgres clients, and UI/shared tooling.

This is less “research repo” and more “multi-surface product monorepo.”

**2. MCP protocol layer**
- [`apps/mcp/src/index.ts`](https://github.com/supermemoryai/supermemory/blob/main/apps/mcp/src/index.ts) is the transport shell. It handles CORS, OAuth metadata discovery, API-key vs OAuth auth, and binds MCP requests into a Durable Object-backed server.
- [`apps/mcp/src/server.ts`](https://github.com/supermemoryai/supermemory/blob/main/apps/mcp/src/server.ts) is the most important file in the repo. It registers the `memory`, `recall`, `listProjects`, `whoAmI`, `memory-graph`, and `fetch-graph-data` tools, plus profile/resources and a `context` prompt.
- [`apps/mcp/src/client.ts`](https://github.com/supermemoryai/supermemory/blob/main/apps/mcp/src/client.ts) is the adapter that turns those tool calls into SDK/API operations, including hybrid search, profile fetches, document fetches, and semantic fallback on forget.

This layer is the cleanest proof that Supermemory understands current agent distribution channels.

**3. Memory access and prompt-injection layer**
- [`packages/tools/src/shared/memory-client.ts`](https://github.com/supermemoryai/supermemory/blob/main/packages/tools/src/shared/memory-client.ts) centralizes profile fetching, deduplication, query extraction, and prompt building.
- [`packages/tools/src/shared/prompt-builder.ts`](https://github.com/supermemoryai/supermemory/blob/main/packages/tools/src/shared/prompt-builder.ts) converts profile state into markdown and then into a system-prompt payload.
- [`packages/tools/src/openai/middleware.ts`](https://github.com/supermemoryai/supermemory/blob/main/packages/tools/src/openai/middleware.ts) shows the operational pattern clearly: inspect the last user message, call `/v4/profile`, deduplicate results, and append the resulting memory context into the system prompt.
- [`packages/tools/src/openai/tools.ts`](https://github.com/supermemoryai/supermemory/blob/main/packages/tools/src/openai/tools.ts) exposes explicit function-call schemas for search, add, profile fetch, document list/add/delete, and forget.

This is a very practical design choice. Instead of forcing one agent framework, they keep re-implementing the same memory retrieval contract across frameworks.

**4. Consumer app layer**
- [`apps/web/app/`](https://github.com/supermemoryai/supermemory/tree/main/apps/web/app) is a Next.js App Router surface for login, onboarding, settings, and the main app shell.
- [`apps/web/components/chat/index.tsx`](https://github.com/supermemoryai/supermemory/blob/main/apps/web/components/chat/index.tsx) makes it obvious that the app is not just a document browser. It includes a full “Nova” chat surface with model selection, project scoping, thread management, and grounding against memory/document counts.
- [`apps/web/lib/plugin-catalog.ts`](https://github.com/supermemoryai/supermemory/blob/main/apps/web/lib/plugin-catalog.ts) is surprisingly important. It encodes the real product thesis: memory should be installed into Claude Code, Codex, OpenCode, OpenClaw, and Hermes with client-specific setup flows.
- [`apps/web/lib/chat-search-memory-results.ts`](https://github.com/supermemoryai/supermemory/blob/main/apps/web/lib/chat-search-memory-results.ts) normalizes heterogeneous search payloads so the UI can show memory cards sanely.

The app layer is doing product legibility work: it turns a hidden retrieval service into something users can browse, install, and reason about.

**5. Visualization layer**
- [`packages/memory-graph/src/hooks/use-graph-data.ts`](https://github.com/supermemoryai/supermemory/blob/main/packages/memory-graph/src/hooks/use-graph-data.ts) computes graph edges and lays out document and memory nodes with a deterministic spiral-plus-orbit layout.
- [`packages/memory-graph/src/components/memory-graph.tsx`](https://github.com/supermemoryai/supermemory/blob/main/packages/memory-graph/src/components/memory-graph.tsx) and [`packages/memory-graph/src/components/graph-canvas.tsx`](https://github.com/supermemoryai/supermemory/blob/main/packages/memory-graph/src/components/graph-canvas.tsx) provide the reusable graph UI shell.
- [`apps/mcp/src/ui/mcp-app.ts`](https://github.com/supermemoryai/supermemory/blob/main/apps/mcp/src/ui/mcp-app.ts) consumes backend graph data and renders an MCP app resource for interactive inspection.

This is one of the better design ideas in the repo. If you claim to maintain a memory graph, showing the graph matters.

### Request / data / control flow
A simplified flow looks like this:
1. a user or agent hits the MCP endpoint implemented in [`apps/mcp/src/index.ts`](https://github.com/supermemoryai/supermemory/blob/main/apps/mcp/src/index.ts),
2. auth is validated against the hosted API and the request is bound to a user plus optional `containerTag`,
3. [`apps/mcp/src/server.ts`](https://github.com/supermemoryai/supermemory/blob/main/apps/mcp/src/server.ts) maps MCP tool calls to higher-level operations like save, recall, project listing, graph fetch, or context prompt generation,
4. [`apps/mcp/src/client.ts`](https://github.com/supermemoryai/supermemory/blob/main/apps/mcp/src/client.ts) calls the Supermemory SDK and remote API endpoints,
5. the same backend can also be hit by framework wrappers in [`packages/tools/`](https://github.com/supermemoryai/supermemory/tree/main/packages/tools), which fetch profile/search context and inject it into model prompts,
6. the web UI in [`apps/web/`](https://github.com/supermemoryai/supermemory/tree/main/apps/web) then reads and visualizes the resulting documents, memories, and plugin/install state.

The key architectural fact is that almost every open-source surface in this repo points inward to a hosted service boundary.

## Key directories and files
- [`README.md`](https://github.com/supermemoryai/supermemory/blob/main/README.md), strong on positioning, weaker on exposing the actual core engine internals
- [`package.json`](https://github.com/supermemoryai/supermemory/blob/main/package.json), workspace and dependency map
- [`apps/mcp/src/index.ts`](https://github.com/supermemoryai/supermemory/blob/main/apps/mcp/src/index.ts), Cloudflare Worker transport/auth shell
- [`apps/mcp/src/server.ts`](https://github.com/supermemoryai/supermemory/blob/main/apps/mcp/src/server.ts), the single best file for understanding the repo’s public behavior
- [`apps/mcp/src/client.ts`](https://github.com/supermemoryai/supermemory/blob/main/apps/mcp/src/client.ts), remote memory/document adapter
- [`apps/mcp/src/ui/mcp-app.ts`](https://github.com/supermemoryai/supermemory/blob/main/apps/mcp/src/ui/mcp-app.ts), graph visualization surface for MCP apps
- [`apps/web/components/chat/index.tsx`](https://github.com/supermemoryai/supermemory/blob/main/apps/web/components/chat/index.tsx), evidence that Supermemory is also trying to be a full assistant/app experience
- [`apps/web/lib/plugin-catalog.ts`](https://github.com/supermemoryai/supermemory/blob/main/apps/web/lib/plugin-catalog.ts), explicit install/distribution map across supported clients
- [`apps/web/lib/chat-search-memory-results.ts`](https://github.com/supermemoryai/supermemory/blob/main/apps/web/lib/chat-search-memory-results.ts), payload normalization glue that reveals API heterogeneity
- [`packages/tools/src/shared/memory-client.ts`](https://github.com/supermemoryai/supermemory/blob/main/packages/tools/src/shared/memory-client.ts), shared retrieval/prompt assembly logic
- [`packages/tools/src/openai/middleware.ts`](https://github.com/supermemoryai/supermemory/blob/main/packages/tools/src/openai/middleware.ts), concrete memory injection path for chat completions
- [`packages/tools/src/openai/tools.ts`](https://github.com/supermemoryai/supermemory/blob/main/packages/tools/src/openai/tools.ts), explicit callable tool surface
- [`packages/memory-graph/src/hooks/use-graph-data.ts`](https://github.com/supermemoryai/supermemory/blob/main/packages/memory-graph/src/hooks/use-graph-data.ts), graph edge computation and node layout logic

## Important components
**`SupermemoryMCP` is the public control plane**
[`apps/mcp/src/server.ts`](https://github.com/supermemoryai/supermemory/blob/main/apps/mcp/src/server.ts) is where the product becomes concrete. It does not just proxy raw API calls. It curates the mental model: memory save/forget, recall, projects, graph, and context prompt.

**`SupermemoryClient` hides the backend boundary**
[`apps/mcp/src/client.ts`](https://github.com/supermemoryai/supermemory/blob/main/apps/mcp/src/client.ts) is honest about the architecture. It is a wrapper around a remote service, not a local engine. The semantic-forget fallback is a nice touch, but it also shows how much logic is policy around API use, not core model implementation.

**Prompt-injection middleware is a first-class product surface**
[`packages/tools/src/openai/middleware.ts`](https://github.com/supermemoryai/supermemory/blob/main/packages/tools/src/openai/middleware.ts) makes the business model legible. The product is not only “store memory,” it is “quietly insert the right context into the agent loop you already have.”

**The plugin catalog is part of the architecture**
[`apps/web/lib/plugin-catalog.ts`](https://github.com/supermemoryai/supermemory/blob/main/apps/web/lib/plugin-catalog.ts) looks mundane, but it is actually one of the clearest strategic files in the repo. It encodes a client-by-client memory land grab.

**The memory graph UI is their trust-building layer**
[`packages/memory-graph/src/hooks/use-graph-data.ts`](https://github.com/supermemoryai/supermemory/blob/main/packages/memory-graph/src/hooks/use-graph-data.ts) plus [`apps/mcp/src/ui/mcp-app.ts`](https://github.com/supermemoryai/supermemory/blob/main/apps/mcp/src/ui/mcp-app.ts) give users a way to inspect relations like `updates`, `extends`, and `derives` instead of treating memory as opaque hidden state.

## Important knobs / configs / extension points
- [`package.json`](https://github.com/supermemoryai/supermemory/blob/main/package.json) defines the workspace topology and deployment toolchain.
- [`apps/mcp/wrangler.jsonc`](https://github.com/supermemoryai/supermemory/blob/main/apps/mcp/wrangler.jsonc) is a major deployment seam because the MCP service is built for Cloudflare Workers.
- [`apps/mcp/src/server.ts`](https://github.com/supermemoryai/supermemory/blob/main/apps/mcp/src/server.ts) exposes `containerTag` as the main scoping knob for projects/spaces.
- [`packages/tools/src/openai/middleware.ts`](https://github.com/supermemoryai/supermemory/blob/main/packages/tools/src/openai/middleware.ts) exposes retrieval mode knobs like `profile`, `query`, and `full`, plus `customId` and `containerTag`.
- [`packages/tools/src/shared/prompt-builder.ts`](https://github.com/supermemoryai/supermemory/blob/main/packages/tools/src/shared/prompt-builder.ts) leaves room for prompt-template variation.
- [`apps/web/lib/plugin-catalog.ts`](https://github.com/supermemoryai/supermemory/blob/main/apps/web/lib/plugin-catalog.ts) acts as an extension matrix for supported clients and installation patterns.

## Practical questions and answers
**Is the actual memory engine open here?**
Not really, at least not in the way the marketing language might lead you to expect. The repo exposes many clients and wrappers around the engine, but the heavy lifting appears to sit behind hosted endpoints like the `/v4/profile` calls used in [`packages/tools/src/openai/middleware.ts`](https://github.com/supermemoryai/supermemory/blob/main/packages/tools/src/openai/middleware.ts).

**What is the architectural center of gravity?**
[`apps/mcp/src/server.ts`](https://github.com/supermemoryai/supermemory/blob/main/apps/mcp/src/server.ts). If you want to know what the company thinks the product is, that file answers it more clearly than the README.

**What is the smartest reusable idea?**
Treat memory as an adoption problem, not just a retrieval problem. The combination of MCP, framework middleware, app UI, plugin onboarding, and graph inspection is the real play.

**What would I copy?**
The consistent project/container scoping, the graph inspectability, and the “same backend, many delivery surfaces” strategy.

**What would I be careful about copying?**
The dependence on silent prompt injection as the main integration technique. It is pragmatic, but it can get messy when multiple memory/context systems compete for the system prompt.

**What is most likely brittle?**
Payload normalization and surface sprawl. Files like [`apps/web/lib/chat-search-memory-results.ts`](https://github.com/supermemoryai/supermemory/blob/main/apps/web/lib/chat-search-memory-results.ts) exist for a reason: when one platform serves many clients, response-shape drift becomes real operational debt.

## What is smart
- The MCP surface in [`apps/mcp/src/server.ts`](https://github.com/supermemoryai/supermemory/blob/main/apps/mcp/src/server.ts) is thoughtfully curated rather than dumped raw.
- [`packages/tools/src/shared/memory-client.ts`](https://github.com/supermemoryai/supermemory/blob/main/packages/tools/src/shared/memory-client.ts) and [`packages/tools/src/openai/middleware.ts`](https://github.com/supermemoryai/supermemory/blob/main/packages/tools/src/openai/middleware.ts) show a strong instinct for reuse across frameworks.
- [`apps/web/lib/plugin-catalog.ts`](https://github.com/supermemoryai/supermemory/blob/main/apps/web/lib/plugin-catalog.ts) reveals that they understand distribution friction at the level of specific clients, not just generic APIs.
- [`packages/memory-graph/src/hooks/use-graph-data.ts`](https://github.com/supermemoryai/supermemory/blob/main/packages/memory-graph/src/hooks/use-graph-data.ts) turns the memory graph idea into something users can actually inspect.
- The repo is product-complete in a way many AI repos are not. There is app UX, install UX, protocol UX, and SDK UX.

## What is flawed or weak
- [`README.md`](https://github.com/supermemoryai/supermemory/blob/main/README.md) sells the system like a transparent engine repo, but the code you can inspect is mostly wrapper/integration/UI logic around a hosted backend.
- The actual core extraction/ranking/ontology machinery is largely offstage, which limits how much a builder can truly audit.
- [`apps/web/`](https://github.com/supermemoryai/supermemory/tree/main/apps/web) and [`packages/tools/`](https://github.com/supermemoryai/supermemory/tree/main/packages/tools) together create a wide surface area that will be expensive to keep behaviorally consistent.
- The product leans heavily on prompt injection and context assembly, which is practical but also vulnerable to prompt-budget pressure and competing system prompts.
- Multi-client support is a moat if executed well, but it is also a maintenance trap.

## What we can learn / steal
- Make inspectability a feature. If you claim memory, expose the graph.
- Ship the same capability through multiple user-native surfaces instead of demanding that users adopt one blessed interface.
- Treat scoping as first-class. `containerTag` is a simple but important product boundary.
- Keep the public control plane opinionated. Curated tools beat raw low-level endpoints.
- Build install flows as architecture, not documentation afterthought.

## How we could apply it
If we were building a memory/context product, I would copy this shape:
1. one canonical backend contract,
2. one MCP surface,
3. one agent-middleware surface,
4. one human-facing app for inspection and correction,
5. one graph/debug view for trust,
6. strict scoping primitives from day one.

What I would do differently is expose more of the actual engine mechanics, or at least provide a clearer boundary between “open-source delivery shell” and “hosted proprietary core.” That honesty would make the repo easier to trust.

## Bottom line
Supermemory is a strong repo to study if you care about how AI memory becomes a real product instead of a benchmark slide. The deepest lesson is not in embeddings or knowledge graphs. It is in packaging.

Their best move is turning memory into a protocol, middleware, UI, and plugin problem all at once.

Their weakest point is that the core engine itself remains mostly hidden behind the service boundary, so the public repo teaches you more about memory productization than about memory science.