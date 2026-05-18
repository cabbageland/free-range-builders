# OpenHuman

- Repo: `tinyhumansai/openhuman`
- URL: https://github.com/tinyhumansai/openhuman
- Date: 2026-05-18
- Repo snapshot studied: `main` @ `0b053c55f508d24aaf295a47d20fd57fa74d96af`
- Why picked today: It was the hottest AI-adjacent repo on GitHub trending, but unlike most trending agent repos it actually has a large code surface, a real desktop product, and enough architectural ambition to reward a proper teardown.

## Executive summary
OpenHuman is a local-first desktop agent product that tries to collapse several markets into one app: chat agent, messaging hub, long-term memory system, desktop mascot, channel router, voice interface, and tool-integrated assistant. The repo is not a thin wrapper around an LLM API. It is a fairly serious full-stack desktop system with a Rust core, a React/Tauri shell, a large connector/tool surface, and a memory subsystem that is clearly treated as a first-class product feature.

The sharpest idea in the repo is not the mascot or the "super intelligence" branding. It is the decision to make context acquisition a product primitive: sync external systems, canonicalize them into local markdown-ish artifacts, compress and score them, store them in SQLite-backed structures, and feed that material back into agent runs. In other words, the real product is a context engine wearing an assistant costume.

## What they built
They built a desktop AI harness with:
- a React app in [`app/src/`](https://github.com/tinyhumansai/openhuman/tree/0b053c55f508d24aaf295a47d20fd57fa74d96af/app/src)
- a Tauri desktop shell plus native integrations in [`app/src-tauri/`](https://github.com/tinyhumansai/openhuman/tree/0b053c55f508d24aaf295a47d20fd57fa74d96af/app/src-tauri)
- a large Rust core in [`src/openhuman/`](https://github.com/tinyhumansai/openhuman/tree/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/openhuman)
- an agent runtime and sub-agent system in [`src/openhuman/agent/`](https://github.com/tinyhumansai/openhuman/tree/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/openhuman/agent)
- a memory platform in [`src/openhuman/memory/`](https://github.com/tinyhumansai/openhuman/tree/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/openhuman/memory)
- multi-channel messaging and outbound delivery in [`src/openhuman/channels/`](https://github.com/tinyhumansai/openhuman/tree/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/openhuman/channels)
- a large internal tool surface in [`src/openhuman/tools/`](https://github.com/tinyhumansai/openhuman/tree/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/openhuman/tools)
- scheduling/automation infrastructure in [`src/openhuman/cron/`](https://github.com/tinyhumansai/openhuman/tree/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/openhuman/cron)

The repo is best understood as a bundled personal-agent operating environment, not just a chatbot app.

## Why it matters
Most agent products still treat memory, connectors, background work, and UI as bolted-on features. OpenHuman is trying to make those the center of the product. That matters because real assistant usefulness is rarely about a better answer model alone. It is about whether the system can ingest your world, keep that world fresh, and act through the surfaces you already use.

The repo also matters as a case study in where open-source agent products are heading: not single-purpose coding shells, but sprawling personal automation stacks with opinionated memory, channel, and native OS layers.

## Repo shape at a glance
Top-level shape:
- [`README.md`](https://github.com/tinyhumansai/openhuman/blob/0b053c55f508d24aaf295a47d20fd57fa74d96af/README.md): product pitch and contributor entrypoint
- [`src/`](https://github.com/tinyhumansai/openhuman/tree/0b053c55f508d24aaf295a47d20fd57fa74d96af/src): Rust core entrypoints and domain modules
- [`src/openhuman/`](https://github.com/tinyhumansai/openhuman/tree/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/openhuman): the real product core, split into many subsystems
- [`app/src/`](https://github.com/tinyhumansai/openhuman/tree/0b053c55f508d24aaf295a47d20fd57fa74d96af/app/src): React frontend
- [`app/src-tauri/`](https://github.com/tinyhumansai/openhuman/tree/0b053c55f508d24aaf295a47d20fd57fa74d96af/app/src-tauri): desktop shell, native bridges, recipes, scanners, permissions
- [`remotion/`](https://github.com/tinyhumansai/openhuman/tree/0b053c55f508d24aaf295a47d20fd57fa74d96af/remotion): runtime asset rendering pipeline for mascot/media bits
- [`scripts/`](https://github.com/tinyhumansai/openhuman/tree/0b053c55f508d24aaf295a47d20fd57fa74d96af/scripts): huge operational glue layer for builds, tests, release, debugging, installs, and experiments
- [`tests/`](https://github.com/tinyhumansai/openhuman/tree/0b053c55f508d24aaf295a47d20fd57fa74d96af/tests): Rust integration and end-to-end coverage
- [`docs/`](https://github.com/tinyhumansai/openhuman/tree/0b053c55f508d24aaf295a47d20fd57fa74d96af/docs) and [`gitbooks/`](https://github.com/tinyhumansai/openhuman/tree/0b053c55f508d24aaf295a47d20fd57fa74d96af/gitbooks): architecture notes, feature docs, product surface documentation

The repo has three obvious macro-layers:
1. product shell and UX
2. Rust runtime and domain services
3. operations/docs/distribution scaffolding

## Layered architecture dissection
### High-level system shape
The system shape looks like this:
1. a desktop/web UI gathers user intent and displays state
2. a Rust core exposes RPC/controllers and runs the heavy logic
3. the agent runtime decides which models/tools/subagents to use
4. channels and connectors bring external messages/data in and out
5. memory pipelines canonicalize and store context locally
6. cron/background jobs keep the system warm, synced, and proactive

The core binary entrypoint in [`src/main.rs`](https://github.com/tinyhumansai/openhuman/blob/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/main.rs) is thin by design. It sets up observability and then hands control to [`src/lib.rs`](https://github.com/tinyhumansai/openhuman/blob/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/lib.rs), which dispatches into the real module graph under [`src/openhuman/`](https://github.com/tinyhumansai/openhuman/tree/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/openhuman).

### Main layers
**1. Product/UI layer**
- Routes are defined in [`app/src/AppRoutes.tsx`](https://github.com/tinyhumansai/openhuman/blob/0b053c55f508d24aaf295a47d20fd57fa74d96af/app/src/AppRoutes.tsx)
- major user surfaces include [`app/src/features/human/`](https://github.com/tinyhumansai/openhuman/tree/0b053c55f508d24aaf295a47d20fd57fa74d96af/app/src/features/human), [`app/src/components/intelligence/`](https://github.com/tinyhumansai/openhuman/tree/0b053c55f508d24aaf295a47d20fd57fa74d96af/app/src/components/intelligence), [`app/src/components/channels/`](https://github.com/tinyhumansai/openhuman/tree/0b053c55f508d24aaf295a47d20fd57fa74d96af/app/src/components/channels), and [`app/src/components/skills/`](https://github.com/tinyhumansai/openhuman/tree/0b053c55f508d24aaf295a47d20fd57fa74d96af/app/src/components/skills)

This layer reveals the product truth: they are building a broad consumer-ish desktop assistant, not a devtool-only shell.

**2. Desktop/native bridge layer**
- Tauri packaging and permissions live in [`app/src-tauri/tauri.conf.json`](https://github.com/tinyhumansai/openhuman/blob/0b053c55f508d24aaf295a47d20fd57fa74d96af/app/src-tauri/tauri.conf.json) and [`app/src-tauri/permissions/`](https://github.com/tinyhumansai/openhuman/tree/0b053c55f508d24aaf295a47d20fd57fa74d96af/app/src-tauri/permissions)
- native-facing code lives in [`app/src-tauri/src/`](https://github.com/tinyhumansai/openhuman/tree/0b053c55f508d24aaf295a47d20fd57fa74d96af/app/src-tauri/src)
- browser/app recipes for automation targets live in [`app/src-tauri/recipes/`](https://github.com/tinyhumansai/openhuman/tree/0b053c55f508d24aaf295a47d20fd57fa74d96af/app/src-tauri/recipes)

This is where the repo gets more ambitious than a normal Electron chat app. It is trying to touch meetings, scanners, notifications, camera/video, and app/webview surfaces.

**3. Agent orchestration layer**
- overview and public surface are documented in [`src/openhuman/agent/README.md`](https://github.com/tinyhumansai/openhuman/blob/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/openhuman/agent/README.md)
- the domain lives in [`src/openhuman/agent/`](https://github.com/tinyhumansai/openhuman/tree/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/openhuman/agent)

This layer owns the LLM tool loop, subagent dispatch, prompt assets, trigger triage, and session runtime. It is the brainstem of the product.

**4. Tool and action layer**
- shared tool surface is in [`src/openhuman/tools/`](https://github.com/tinyhumansai/openhuman/tree/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/openhuman/tools)
- implementation categories under [`src/openhuman/tools/impl/`](https://github.com/tinyhumansai/openhuman/tree/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/openhuman/tools/impl) include browser, filesystem, memory, computer, network, system, cron, and agent tools

This is how the agent stops being just a text generator.

**5. Memory/context layer**
- memory overview: [`src/openhuman/memory/README.md`](https://github.com/tinyhumansai/openhuman/blob/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/openhuman/memory/README.md)
- new memory-tree pipeline: [`src/openhuman/memory/tree/README.md`](https://github.com/tinyhumansai/openhuman/blob/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/openhuman/memory/tree/README.md)
- ingestion pipeline: [`src/openhuman/memory/ingestion/`](https://github.com/tinyhumansai/openhuman/tree/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/openhuman/memory/ingestion)
- store/backend layer: [`src/openhuman/memory/store/`](https://github.com/tinyhumansai/openhuman/tree/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/openhuman/memory/store)

This is the most strategically interesting subsystem in the repo. They are building a structured local memory backend, not just stuffing conversation turns into a vector DB.

**6. Channel/connectivity layer**
- channel overview: [`src/openhuman/channels/README.md`](https://github.com/tinyhumansai/openhuman/blob/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/openhuman/channels/README.md)
- provider/runtime code: [`src/openhuman/channels/providers/`](https://github.com/tinyhumansai/openhuman/tree/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/openhuman/channels/providers) and [`src/openhuman/channels/runtime/`](https://github.com/tinyhumansai/openhuman/tree/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/openhuman/channels/runtime)
- composio-based integrations sit nearby in [`src/openhuman/composio/`](https://github.com/tinyhumansai/openhuman/tree/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/openhuman/composio)

This layer turns the assistant into a routing fabric across Slack, Discord, Telegram, web, email, and more.

**7. Scheduling and daemon layer**
- cron overview: [`src/openhuman/cron/README.md`](https://github.com/tinyhumansai/openhuman/blob/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/openhuman/cron/README.md)
- service/daemon modules: [`src/openhuman/service/`](https://github.com/tinyhumansai/openhuman/tree/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/openhuman/service)

This is what lets the product keep working when you are not actively typing.

### Request / data / control flow
A typical user-facing flow appears to be:
- user interacts with a page from [`app/src/AppRoutes.tsx`](https://github.com/tinyhumansai/openhuman/blob/0b053c55f508d24aaf295a47d20fd57fa74d96af/app/src/AppRoutes.tsx)
- the desktop shell in [`app/src-tauri/src/`](https://github.com/tinyhumansai/openhuman/tree/0b053c55f508d24aaf295a47d20fd57fa74d96af/app/src-tauri/src) brokers native calls and core-process communication
- the Rust core dispatches through controller registries rooted in modules like [`src/core/all.rs`](https://github.com/tinyhumansai/openhuman/blob/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/core/all.rs)
- agent work is executed in [`src/openhuman/agent/`](https://github.com/tinyhumansai/openhuman/tree/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/openhuman/agent)
- tool calls fan into [`src/openhuman/tools/impl/`](https://github.com/tinyhumansai/openhuman/tree/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/openhuman/tools/impl)
- connected channels/providers feed data into memory and agent flows through [`src/openhuman/channels/`](https://github.com/tinyhumansai/openhuman/tree/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/openhuman/channels), [`src/openhuman/composio/`](https://github.com/tinyhumansai/openhuman/tree/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/openhuman/composio), and [`src/openhuman/memory/`](https://github.com/tinyhumansai/openhuman/tree/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/openhuman/memory)
- scheduled/background work is maintained by [`src/openhuman/cron/scheduler.rs`](https://github.com/tinyhumansai/openhuman/blob/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/openhuman/cron/scheduler.rs) and the service layer

The memory-specific flow is especially notable:
- source adapters feed canonical material into [`src/openhuman/memory/tree/ingest.rs`](https://github.com/tinyhumansai/openhuman/blob/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/openhuman/memory/tree/ingest.rs)
- chunking happens in [`src/openhuman/memory/tree/chunker.rs`](https://github.com/tinyhumansai/openhuman/blob/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/openhuman/memory/tree/chunker.rs)
- persisted state lands in [`src/openhuman/memory/tree/store.rs`](https://github.com/tinyhumansai/openhuman/blob/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/openhuman/memory/tree/store.rs)
- retrieval and drill-down happen through [`src/openhuman/memory/tree/retrieval/`](https://github.com/tinyhumansai/openhuman/tree/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/openhuman/memory/tree/retrieval)

## Key directories and files
- [`Cargo.toml`](https://github.com/tinyhumansai/openhuman/blob/0b053c55f508d24aaf295a47d20fd57fa74d96af/Cargo.toml): the fastest way to see how broad the product really is, from Axum and rusqlite to audio, automation, crypto, embeddings, and channel dependencies.
- [`src/main.rs`](https://github.com/tinyhumansai/openhuman/blob/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/main.rs): thin launcher, good evidence that the binary is mostly a shell around a big modular core.
- [`src/openhuman/agent/README.md`](https://github.com/tinyhumansai/openhuman/blob/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/openhuman/agent/README.md): unusually useful module-level map for the agent subsystem.
- [`src/openhuman/memory/README.md`](https://github.com/tinyhumansai/openhuman/blob/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/openhuman/memory/README.md): best single clue to what the team thinks the enduring moat is.
- [`src/openhuman/memory/tree/README.md`](https://github.com/tinyhumansai/openhuman/blob/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/openhuman/memory/tree/README.md): concrete pipeline description, including canonicalization, chunking, storage, scoring, trees, and jobs.
- [`src/openhuman/channels/README.md`](https://github.com/tinyhumansai/openhuman/blob/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/openhuman/channels/README.md): shows the repo is built as a multi-channel runtime, not a single-app assistant.
- [`app/src/AppRoutes.tsx`](https://github.com/tinyhumansai/openhuman/blob/0b053c55f508d24aaf295a47d20fd57fa74d96af/app/src/AppRoutes.tsx): tells you what the product surfaces actually are.
- [`app/src-tauri/src/core_process.rs`](https://github.com/tinyhumansai/openhuman/blob/0b053c55f508d24aaf295a47d20fd57fa74d96af/app/src-tauri/src/core_process.rs): important bridge between desktop shell and the core runtime.
- [`scripts/install.sh`](https://github.com/tinyhumansai/openhuman/blob/0b053c55f508d24aaf295a47d20fd57fa74d96af/scripts/install.sh): evidence that they care about frictionless distribution, not just source builds.
- [`tests/`](https://github.com/tinyhumansai/openhuman/tree/0b053c55f508d24aaf295a47d20fd57fa74d96af/tests): large cross-cutting test surface, especially around memory, routing, channels, and agent behavior.

## Important components
**Agent runtime**
- [`src/openhuman/agent/harness/`](https://github.com/tinyhumansai/openhuman/tree/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/openhuman/agent/harness)
- This owns the actual conversational/tool-calling loop and subagent execution. If this layer is weak, the whole product becomes UI theater.

**Memory tree pipeline**
- [`src/openhuman/memory/tree/`](https://github.com/tinyhumansai/openhuman/tree/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/openhuman/memory/tree)
- The pipeline of canonicalize → chunk → persist → score → tree summaries is the repo’s most reusable systems idea.

**Channel supervisor and providers**
- [`src/openhuman/channels/runtime/`](https://github.com/tinyhumansai/openhuman/tree/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/openhuman/channels/runtime)
- [`src/openhuman/channels/providers/`](https://github.com/tinyhumansai/openhuman/tree/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/openhuman/channels/providers)
- This is what makes the assistant feel ambient instead of app-confined.

**Tool implementation lattice**
- [`src/openhuman/tools/impl/`](https://github.com/tinyhumansai/openhuman/tree/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/openhuman/tools/impl)
- The breadth here is notable because it suggests the product is architected as an action runtime, not only a retrieval system.

**Desktop-native integration layer**
- [`app/src-tauri/src/`](https://github.com/tinyhumansai/openhuman/tree/0b053c55f508d24aaf295a47d20fd57fa74d96af/app/src-tauri/src)
- This layer is carrying substantial complexity: scanners, meet integration, notifications, screen capture, hotkeys, and native bridges.

## Important knobs / configs / extension points
- [`Cargo.toml`](https://github.com/tinyhumansai/openhuman/blob/0b053c55f508d24aaf295a47d20fd57fa74d96af/Cargo.toml) exposes feature flags like `channel-matrix`, `whatsapp-web`, `browser-native`, `sandbox-landlock`, and `rag-pdf`.
- [`app/package.json`](https://github.com/tinyhumansai/openhuman/blob/0b053c55f508d24aaf295a47d20fd57fa74d96af/app/package.json) shows multiple run/build modes and where the desktop workflow really lives.
- [`app/src-tauri/recipes/`](https://github.com/tinyhumansai/openhuman/tree/0b053c55f508d24aaf295a47d20fd57fa74d96af/app/src-tauri/recipes) is an important extension seam for app-specific automation targets.
- [`src/openhuman/channels/controllers/schemas.rs`](https://github.com/tinyhumansai/openhuman/blob/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/openhuman/channels/controllers/schemas.rs) makes the outbound/inbound channel control surface explicit.
- [`src/openhuman/memory/tree/types.rs`](https://github.com/tinyhumansai/openhuman/blob/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/openhuman/memory/tree/types.rs) and [`src/openhuman/memory/tree/chunker.rs`](https://github.com/tinyhumansai/openhuman/blob/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/openhuman/memory/tree/chunker.rs) define the practical chunk model and token-bound assumptions.

## Practical questions and answers
**Q: Is this mainly a desktop shell around LLM APIs?**
A: No. It has that layer, but the bigger story is a bundled runtime for memory, tools, channels, and automation.

**Q: What assumption does the system make?**
A: That the winning personal agent will be the one that can keep a local, structured, continuously refreshed model of your world.

**Q: What is the most important architectural bet?**
A: Local memory as durable product infrastructure, not as a sidecar feature.

**Q: Where is the likely production pain?**
A: Connector churn, native-platform edge cases, permission weirdness, and the sheer coordination cost of a repo this wide.

**Q: Is the breadth a strength or a risk?**
A: Both. It creates a stronger end-to-end experience if maintained well, but it also invites thinness and regressions across many subsystems.

**Q: What feels most reusable for other builders?**
A: The memory tree pipeline and the way channels, cron, and agent execution are treated as one system instead of separate products.

## What is smart
- Treating memory as a real architecture layer instead of a vibes feature.
- Using Rust for the heavy core while keeping a consumer-facing React/Tauri shell.
- Keeping module-level READMEs in key subsystems like [`src/openhuman/agent/README.md`](https://github.com/tinyhumansai/openhuman/blob/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/openhuman/agent/README.md), [`src/openhuman/memory/README.md`](https://github.com/tinyhumansai/openhuman/blob/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/openhuman/memory/README.md), and [`src/openhuman/channels/README.md`](https://github.com/tinyhumansai/openhuman/blob/0b053c55f508d24aaf295a47d20fd57fa74d96af/src/openhuman/channels/README.md). That is a real gift in a repo this large.
- Building proactive/background behavior into the architecture through cron, channels, and service modules instead of treating it as a future add-on.
- Keeping the tool surface broad enough that the agent can plausibly act, not just answer.

## What is flawed or weak
- The README is loaded with maximalist claims, and the marketing language outruns the architectural credibility at times. There is real engineering here, but the pitch often sounds more finished than the repo likely is.
- The surface area is borderline dangerous. Channels, native scanners, voice, automation, memory, integrations, and desktop UX all in one codebase creates heavy coordination tax.
- Some of the repo feels like three startups fused together: personal memory engine, assistant UI, and automation runtime. That can be powerful, but it also muddies product focus.
- The more this system touches messaging, meetings, and desktop automation, the more permissions, trust, and safety become make-or-break. That risk is structural, not cosmetic.
- Early-beta plus giant scope usually means a lot of unevenness. The hard part is not demo richness, it is keeping all the edges reliable.

## What we can learn / steal
- If memory is core to the product, give it explicit pipeline stages and its own architecture docs.
- Module-level README files are worth the maintenance cost in large repos.
- Treat channels, scheduling, memory, and agent execution as one unified runtime if the product goal is a truly ambient assistant.
- A desktop assistant becomes much more defensible when it has a serious local core rather than a pure cloud wrapper.
- Wide product ambition is acceptable only if the repo boundaries stay legible. OpenHuman mostly succeeds there because the subsystem splits are clear even when the scope is sprawling.

## How we could apply it
If we were borrowing ideas from this repo, I would not copy the whole product shape. I would steal the narrower pattern:
1. ingest external context continuously
2. normalize it into durable local artifacts
3. score/compress it before it hits the model
4. keep tools and channels close to the agent runtime
5. make background jobs first-class

The key reusable lesson is that an assistant gets better when context logistics are treated as infrastructure.

## Bottom line
OpenHuman is messy, ambitious, and much more substantial than the average trending AI repo. The repo’s strongest idea is not its mascot or its broad integration count. It is the architecture-level claim that personal-agent usefulness comes from continuous local context building, not just model access.

That is the part worth studying, stealing, and pressure-testing.