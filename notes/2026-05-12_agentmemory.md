# agentmemory

- Repo: `rohitg00/agentmemory`
- URL: https://github.com/rohitg00/agentmemory
- Date: 2026-05-12
- Repo snapshot studied: `main` @ `292e9f6af1df6eb691c7f8d746c7058e2e740709`
- Why picked today: It is hot right now, squarely in the AI-agent tooling wave, and unlike a lot of “memory for agents” repos it has real implementation weight: a large function surface, MCP transport, hooks/plugins, replay UI, benchmarks, and a serious test suite.

## Executive summary

agentmemory is not just a vector store with agent branding on top. It is a memory runtime for coding agents that tries to solve the full operational problem: capture events from live agent sessions, compress and organize them, retrieve the right fragments later, expose them through MCP and REST, and make the whole thing inspectable with a viewer and replay system.

The important architectural move is this: they are packaging memory as an always-on local service with many access surfaces, not as a library you manually sprinkle into agent code. That is the part worth studying.

## What they built

They built a local memory server for coding agents, powered by [`iii-sdk`](https://github.com/iii-hq/iii) and wrapped with:

- a CLI entrypoint in [`src/cli.ts`](https://github.com/rohitg00/agentmemory/blob/main/src/cli.ts)
- a worker/bootstrap runtime in [`src/index.ts`](https://github.com/rohitg00/agentmemory/blob/main/src/index.ts)
- dozens of memory functions under [`src/functions`](https://github.com/rohitg00/agentmemory/tree/main/src/functions)
- MCP transport and tool registry under [`src/mcp`](https://github.com/rohitg00/agentmemory/tree/main/src/mcp)
- an event/replay viewer under [`src/viewer`](https://github.com/rohitg00/agentmemory/tree/main/src/viewer)
- agent-specific integration packages under [`integrations`](https://github.com/rohitg00/agentmemory/tree/main/integrations) and [`plugin`](https://github.com/rohitg00/agentmemory/tree/main/plugin)

The product claim is “your agent remembers everything.” The codebase shows they mean session observations, summaries, profiles, graph relations, leases, signals, replayable timelines, and governance delete paths, all as first-class memory objects.

## Why it matters

The repo matters because it treats agent memory as infrastructure, not prompt garnish.

A lot of agent-memory projects are really one of three things:
- a vector DB wrapper,
- a note file that grows forever,
- or a framework that only works inside its own runtime.

agentmemory is aiming at a different category: one local service, many agent clients, shared memory across them, with MCP as the common interoperability layer.

That is strategically smart because agent switching is normal now. If memory only works inside one agent shell, it is weaker than it sounds.

## Repo shape at a glance

Top-level repo shape:

- [`src`](https://github.com/rohitg00/agentmemory/tree/main/src): the real product core, including runtime bootstrapping, providers, memory functions, MCP server code, viewer server, triggers, and state/index implementations.
- [`src/functions`](https://github.com/rohitg00/agentmemory/tree/main/src/functions): the largest and most important subsystem, with memory operations like observe, remember, smart-search, graph retrieval, replay, retention, governance, working-memory, and more.
- [`src/mcp`](https://github.com/rohitg00/agentmemory/tree/main/src/mcp): MCP server, transport, REST proxy, tool registry.
- [`src/viewer`](https://github.com/rohitg00/agentmemory/tree/main/src/viewer): browser viewer and replay UI server.
- [`plugin`](https://github.com/rohitg00/agentmemory/tree/main/plugin): packaged hooks, scripts, skills, and `.mcp.json` glue for Claude-style plugin installation.
- [`integrations`](https://github.com/rohitg00/agentmemory/tree/main/integrations): deeper host-specific integrations for OpenClaw, Hermes, filesystem watching, and pi.
- [`benchmark`](https://github.com/rohitg00/agentmemory/tree/main/benchmark): benchmark harnesses and result writeups, including LongMemEval and scale/quality comparisons.
- [`test`](https://github.com/rohitg00/agentmemory/tree/main/test): extremely broad test surface, which is one of the strongest quality signals in the repo.
- [`website`](https://github.com/rohitg00/agentmemory/tree/main/website): landing site and related web assets.

This is structurally a product repo, not a toy package repo.

## Layered architecture dissection

### High-level system shape

The system has five layers:

1. **capture**: hooks, triggers, imports, and integrations collect observations from agent sessions
2. **memory processing**: functions compress, summarize, enrich, relate, deduplicate, and govern that data
3. **storage and indexes**: KV state, vector index, hybrid search, persistence
4. **access surfaces**: REST, MCP tools, viewer, replay, export/import
5. **host integrations**: OpenClaw, Hermes, Claude plugin packaging, standalone MCP, filesystem watcher

### Main layers

**1. Runtime bootstrap layer**

[`src/index.ts`](https://github.com/rohitg00/agentmemory/blob/main/src/index.ts) is the orchestration heart. It loads config, chooses model providers, sets up vector/image embedding providers, registers the worker with iii, then wires in a huge list of function modules and endpoints.

This file is useful because it reveals the product boundary. agentmemory is not “a search function.” It is a registry of many memory behaviors composed into one worker.

**2. CLI and operational shell**

[`src/cli.ts`](https://github.com/rohitg00/agentmemory/blob/main/src/cli.ts) is much more than a thin argument parser. It handles startup, engine checks, install/upgrade paths, demo flows, MCP mode, status/doctor commands, transcript import, and platform-specific runtime setup.

That means the repo is trying to win on operability, not just algorithmics.

**3. Memory-function layer**

[`src/functions`](https://github.com/rohitg00/agentmemory/tree/main/src/functions) is the real payload. The file list alone tells the story: [`observe.ts`](https://github.com/rohitg00/agentmemory/blob/main/src/functions/observe.ts), [`remember.ts`](https://github.com/rohitg00/agentmemory/blob/main/src/functions/remember.ts), [`smart-search.ts`](https://github.com/rohitg00/agentmemory/blob/main/src/functions/smart-search.ts), [`graph.ts`](https://github.com/rohitg00/agentmemory/blob/main/src/functions/graph.ts), [`graph-retrieval.ts`](https://github.com/rohitg00/agentmemory/blob/main/src/functions/graph-retrieval.ts), [`replay.ts`](https://github.com/rohitg00/agentmemory/blob/main/src/functions/replay.ts), [`governance.ts`](https://github.com/rohitg00/agentmemory/blob/main/src/functions/governance.ts), [`retention.ts`](https://github.com/rohitg00/agentmemory/blob/main/src/functions/retention.ts), [`working-memory.ts`](https://github.com/rohitg00/agentmemory/blob/main/src/functions/working-memory.ts), and many more.

This is the main reason the repo feels real. They are encoding memory lifecycle policy, not just search.

**4. Retrieval and indexing layer**

The bootstrap in [`src/index.ts`](https://github.com/rohitg00/agentmemory/blob/main/src/index.ts) wires [`src/state/vector-index.ts`](https://github.com/rohitg00/agentmemory/blob/main/src/state/vector-index.ts), [`src/state/hybrid-search.ts`](https://github.com/rohitg00/agentmemory/blob/main/src/state/hybrid-search.ts), and [`src/state/index-persistence.ts`](https://github.com/rohitg00/agentmemory/blob/main/src/state/index-persistence.ts). The README claims BM25 + vector + graph with RRF fusion, and the source layout supports that claim structurally.

The key point is that retrieval is hybrid by design. They are not betting everything on embeddings.

**5. Interface and distribution layer**

MCP support lives under [`src/mcp`](https://github.com/rohitg00/agentmemory/tree/main/src/mcp), especially [`server.ts`](https://github.com/rohitg00/agentmemory/blob/main/src/mcp/server.ts), [`standalone.ts`](https://github.com/rohitg00/agentmemory/blob/main/src/mcp/standalone.ts), and [`tools-registry.ts`](https://github.com/rohitg00/agentmemory/blob/main/src/mcp/tools-registry.ts). The viewer lives in [`src/viewer/server.ts`](https://github.com/rohitg00/agentmemory/blob/main/src/viewer/server.ts). Distribution glue lives in [`plugin`](https://github.com/rohitg00/agentmemory/tree/main/plugin) and [`integrations/openclaw`](https://github.com/rohitg00/agentmemory/tree/main/integrations/openclaw).

This is probably the repo’s smartest layer. Memory only matters if it plugs into where agents already live.

### Request / data / control flow

The likely end-to-end flow is:

1. a host agent integration or hook emits observations
2. [`src/functions/observe.ts`](https://github.com/rohitg00/agentmemory/blob/main/src/functions/observe.ts) and related functions persist session events
3. compression / enrichment / relation extraction functions turn raw events into more retrievable memory units
4. indexes update through the state/index layer
5. later, an MCP tool or REST call hits search/context functions such as [`src/functions/search.ts`](https://github.com/rohitg00/agentmemory/blob/main/src/functions/search.ts), [`src/functions/context.ts`](https://github.com/rohitg00/agentmemory/blob/main/src/functions/context.ts), or [`src/functions/smart-search.ts`](https://github.com/rohitg00/agentmemory/blob/main/src/functions/smart-search.ts)
6. retrieved memory is returned to the agent or shown in the viewer/replay UI

The repo also supports import/replay paths, which means capture is not only live. That is a practical advantage.

## Key directories and files

- [`src/index.ts`](https://github.com/rohitg00/agentmemory/blob/main/src/index.ts): the best single file for understanding system assembly.
- [`src/cli.ts`](https://github.com/rohitg00/agentmemory/blob/main/src/cli.ts): operational wrapper, bootstrap logic, doctor/status/demo/import tooling.
- [`src/functions`](https://github.com/rohitg00/agentmemory/tree/main/src/functions): the core product surface.
- [`src/functions/observe.ts`](https://github.com/rohitg00/agentmemory/blob/main/src/functions/observe.ts): memory capture entrypoint.
- [`src/functions/smart-search.ts`](https://github.com/rohitg00/agentmemory/blob/main/src/functions/smart-search.ts): likely one of the most important retrieval interfaces.
- [`src/functions/replay.ts`](https://github.com/rohitg00/agentmemory/blob/main/src/functions/replay.ts): replay is a big differentiator because it turns memory into something inspectable.
- [`src/functions/governance.ts`](https://github.com/rohitg00/agentmemory/blob/main/src/functions/governance.ts): tells you they know deletion/audit policy matters.
- [`src/mcp/tools-registry.ts`](https://github.com/rohitg00/agentmemory/blob/main/src/mcp/tools-registry.ts): the MCP product map.
- [`plugin/.mcp.json`](https://github.com/rohitg00/agentmemory/blob/main/plugin/.mcp.json): concrete integration glue.
- [`integrations/openclaw`](https://github.com/rohitg00/agentmemory/tree/main/integrations/openclaw): especially relevant because it shows they are aiming beyond Claude/Cursor monoculture.
- [`benchmark/LONGMEMEVAL.md`](https://github.com/rohitg00/agentmemory/blob/main/benchmark/LONGMEMEVAL.md): benchmark grounding.
- [`test`](https://github.com/rohitg00/agentmemory/tree/main/test): huge validation surface. The quantity is not everything, but it is a strong seriousness signal.

## Important components

The most important component is the registration hub in [`src/index.ts`](https://github.com/rohitg00/agentmemory/blob/main/src/index.ts). It exposes the repo’s true architecture: many narrowly named memory capabilities, all wired into one worker.

The second most important component is the CLI in [`src/cli.ts`](https://github.com/rohitg00/agentmemory/blob/main/src/cli.ts). A lot of the product moat is here because it removes setup friction and gives the system operational commands like `doctor`, `status`, `demo`, `import-jsonl`, and `upgrade`.

The third most important component is the function namespace under [`src/functions`](https://github.com/rohitg00/agentmemory/tree/main/src/functions). This is where product ambition expands from “retrieve snippets” into lifecycle, governance, retention, replay, team memory, signals, and branch awareness.

The fourth important component is the MCP layer under [`src/mcp`](https://github.com/rohitg00/agentmemory/tree/main/src/mcp). Without this, the project would be one more memory backend. With it, they can claim compatibility with many agent shells.

The fifth important component is the integration packaging under [`plugin`](https://github.com/rohitg00/agentmemory/tree/main/plugin) and [`integrations`](https://github.com/rohitg00/agentmemory/tree/main/integrations). This is where “works with every agent” becomes concrete instead of just README theater.

## Important knobs / configs / extension points

The central runtime configuration is loaded through [`src/config.ts`](https://github.com/rohitg00/agentmemory/blob/main/src/config.ts), then consumed in [`src/index.ts`](https://github.com/rohitg00/agentmemory/blob/main/src/index.ts) and [`src/cli.ts`](https://github.com/rohitg00/agentmemory/blob/main/src/cli.ts).

Important knobs visible from the code and README include:

- provider/model selection
- engine URL / REST ports
- token budget for context injection
- whether graph extraction is enabled
- whether auto-compress is enabled
- whether context injection is enabled
- fallback provider configuration
- embedding and image embedding provider availability
- tool visibility for MCP surfaces

The most interesting extension points are:

- new function modules under [`src/functions`](https://github.com/rohitg00/agentmemory/tree/main/src/functions)
- host integrations under [`integrations`](https://github.com/rohitg00/agentmemory/tree/main/integrations)
- plugin hooks and skills under [`plugin/hooks`](https://github.com/rohitg00/agentmemory/tree/main/plugin/hooks) and [`plugin/skills`](https://github.com/rohitg00/agentmemory/tree/main/plugin/skills)
- MCP exposure via [`src/mcp/tools-registry.ts`](https://github.com/rohitg00/agentmemory/blob/main/src/mcp/tools-registry.ts)

## Practical questions and answers

**Is this actually cross-agent, or just cross-agent marketing?**

More real than usual. The repo has separate integration paths for OpenClaw, Hermes, Claude plugin packaging, and standalone MCP, plus REST access. That does not guarantee equal quality everywhere, but it is not fake.

**What is the core implementation bet?**

That memory quality comes from lifecycle plus retrieval, not just embeddings. The repo keeps adding modules around compression, reflection, governance, replay, retention, profiles, and graph relations.

**What is carrying the real code weight?**

[`src/cli.ts`](https://github.com/rohitg00/agentmemory/blob/main/src/cli.ts), [`src/index.ts`](https://github.com/rohitg00/agentmemory/blob/main/src/index.ts), the entire [`src/functions`](https://github.com/rohitg00/agentmemory/tree/main/src/functions) tree, and the giant [`test`](https://github.com/rohitg00/agentmemory/tree/main/test) surface.

**Why is replay important?**

Because it makes the system debuggable. Memory systems are usually opaque. A replay path means you can inspect what got captured and why retrieval succeeded or failed.

**Would I trust the benchmark claims blindly?**

No. The benchmark writeups are better than nothing, but memory benchmarks are notoriously easy to overfit. The more durable signal here is not the headline R@5 number. It is the breadth of retrieval modes and the amount of test coverage.

## What is smart

The smartest move is product architecture: one local memory runtime, many agent surfaces.

The second smart move is keeping multiple retrieval strategies in play. Hybrid search plus graph plus compression is a better posture than embedding monoculture.

The third smart move is treating memory governance and delete flows as first-class features. That is visible in files like [`src/functions/governance.ts`](https://github.com/rohitg00/agentmemory/blob/main/src/functions/governance.ts) and the audit/governance tests under [`test`](https://github.com/rohitg00/agentmemory/tree/main/test).

The fourth smart move is operational UX. `doctor`, `status`, `demo`, replay, viewer, transcript import, and plugin wiring are the kind of details that make a tool actually usable.

The fifth smart move is the huge test surface. For a repo in a noisy category, that is one of the few strong anti-handwave signals.

## What is flawed or weak

The biggest weakness is scope sprawl. The function list is impressive, but it is also a warning. When a memory system grows into governance, graphs, replay, leases, signals, branch awareness, teams, filesystem watching, and multimodal features, cohesion gets harder.

The second weakness is that the runtime depends on a fairly specific iii-engine model. [`src/cli.ts`](https://github.com/rohitg00/agentmemory/blob/main/src/cli.ts) even pins an iii version and explains why. That is honest, but it also reveals integration fragility.

The third weakness is benchmark-heavy positioning. The benchmarks help, but benchmark-led messaging can hide the messiest question: does this remain low-noise after months of real coding sessions?

The fourth weakness is that some repo surfaces feel uneven. [`DESIGN.md`](https://github.com/rohitg00/agentmemory/blob/main/DESIGN.md), for example, appears unrelated to the memory product and looks like accidental or leftover collateral. That kind of clutter matters in a repo that wants to signal rigor.

## What we can learn / steal

Steal the interoperability-first shape. If you are building an agent tool, do not bind it to one shell unless you absolutely must.

Steal the replay idea. Memory, automation, and agent tooling become much more trustworthy when users can inspect timelines instead of accepting magic.

Steal the function-per-capability decomposition. The large [`src/functions`](https://github.com/rohitg00/agentmemory/tree/main/src/functions) tree may sprawl, but it also makes capability boundaries legible.

Steal the operational shell. `doctor`, `status`, `demo`, and import tools are often the difference between a cool repo and a real product.

## How we could apply it

If we were building our own agent memory system, I would copy the outer architecture before copying the retrieval internals:

- one durable local service
- one canonical memory schema
- multiple capture paths
- hybrid retrieval
- replay/debug surfaces
- MCP as the compatibility layer
- strong delete/audit/governance paths from day one

If we were building something adjacent, like workflow memory for support agents or analyst copilots, this repo is a good reminder that “memory” is really a bundle of subsystems: capture, compression, indexing, retrieval, policy, observability, and host integration.

## Bottom line

agentmemory is one of the more substantial repos in the current agent-memory wave. The key thing to notice is not the headline retrieval metric. It is the packaging strategy: memory as a shared local runtime with hooks, MCP, replay, governance, and integrations everywhere. That is the real insight worth stealing.