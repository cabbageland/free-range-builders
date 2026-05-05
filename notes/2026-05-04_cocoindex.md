# CocoIndex

- Repo: `cocoindex-io/cocoindex`
- URL: https://github.com/cocoindex-io/cocoindex
- Date: 2026-05-04
- Repo snapshot studied: `main@31ef7059195903dd8b7501b4cbb9946f9ba42e45`
- Why picked today: It is genuinely hot, clearly AI-relevant, and not just another “agent wrapper.” Under the glossy README there is a real systems move: a Python declarative API backed by a Rust incremental engine that tries to make live agent context cheap, explainable, and continuously fresh.

## Executive summary
`cocoindex` is an incremental indexing framework for AI workloads. The pitch is RAG and agent memory, but the actual product is a stateful dataflow engine: you declare transformations in Python, and a Rust runtime tracks lineage, memoization, progress, target state, and live updates so only the delta re-runs.

The key insight is that this repo is not really “about embeddings.” It is about **incremental recomputation as infrastructure**. The Python layer is the ergonomic DSL. The Rust layer is the real moat.

## What they built
They built a hybrid system with four major parts:

- a Python-facing declarative app and function API in [`python/cocoindex/_internal/api.py`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/python/cocoindex/_internal/api.py), [`python/cocoindex/_internal/app.py`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/python/cocoindex/_internal/app.py), and [`python/cocoindex/_internal/function.py`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/python/cocoindex/_internal/function.py)
- a Rust execution engine that owns components, runtime state, progress tracking, cancellation, and target reconciliation under [`rust/core/src/engine/`](https://github.com/cocoindex-io/cocoindex/tree/31ef7059195903dd8b7501b4cbb9946f9ba42e45/rust/core/src/engine)
- connector and target libraries for sources like the local filesystem and stores like Postgres in [`python/cocoindex/connectors/`](https://github.com/cocoindex-io/cocoindex/tree/31ef7059195903dd8b7501b4cbb9946f9ba42e45/python/cocoindex/connectors)
- a large examples-and-docs layer that acts like the real product surface for users in [`examples/`](https://github.com/cocoindex-io/cocoindex/tree/31ef7059195903dd8b7501b4cbb9946f9ba42e45/examples) and [`docs/src/`](https://github.com/cocoindex-io/cocoindex/tree/31ef7059195903dd8b7501b4cbb9946f9ba42e45/docs/src)

So the repo is closer to “React for persistent dataflows” than to “LangChain for indexing.”

## Why it matters
A lot of AI infra repos stop at one-shot pipelines. That is fine for demos, but bad for real agent context, where the expensive part is not the first build, it is keeping derived state fresh after small source and code changes.

CocoIndex matters because it treats freshness, lineage, and partial recomputation as first-class. The repo is trying to make this workflow normal:

source changes or code changes -> detect affected components -> reuse what is still valid -> re-run only the impacted work -> keep targets in sync.

That is a much more serious problem than “split text and embed it.”

## Repo shape at a glance
Top-level structure:

- [`python/cocoindex/`](https://github.com/cocoindex-io/cocoindex/tree/31ef7059195903dd8b7501b4cbb9946f9ba42e45/python/cocoindex), the public Python package and most user-facing APIs
  - [`python/cocoindex/_internal/`](https://github.com/cocoindex-io/cocoindex/tree/31ef7059195903dd8b7501b4cbb9946f9ba42e45/python/cocoindex/_internal), the real runtime-facing Python bridge layer
  - [`python/cocoindex/connectors/`](https://github.com/cocoindex-io/cocoindex/tree/31ef7059195903dd8b7501b4cbb9946f9ba42e45/python/cocoindex/connectors), sources and targets for filesystems, Postgres, vector stores, queues, graph DBs, and cloud storage
  - [`python/cocoindex/ops/`](https://github.com/cocoindex-io/cocoindex/tree/31ef7059195903dd8b7501b4cbb9946f9ba42e45/python/cocoindex/ops), reusable transforms like chunking and language detection
- [`rust/core/`](https://github.com/cocoindex-io/cocoindex/tree/31ef7059195903dd8b7501b4cbb9946f9ba42e45/rust/core), the incremental engine core
- [`rust/py/`](https://github.com/cocoindex-io/cocoindex/tree/31ef7059195903dd8b7501b4cbb9946f9ba42e45/rust/py), the PyO3 bridge that exposes the Rust engine into Python
- [`rust/ops_text/`](https://github.com/cocoindex-io/cocoindex/tree/31ef7059195903dd8b7501b4cbb9946f9ba42e45/rust/ops_text), native text operations behind the Python text helpers
- [`examples/`](https://github.com/cocoindex-io/cocoindex/tree/31ef7059195903dd8b7501b4cbb9946f9ba42e45/examples), the best place to understand intended use cases
- [`docs/src/`](https://github.com/cocoindex-io/cocoindex/tree/31ef7059195903dd8b7501b4cbb9946f9ba42e45/docs/src), Astro docs site
- [`skills/cocoindex/`](https://github.com/cocoindex-io/cocoindex/tree/31ef7059195903dd8b7501b4cbb9946f9ba42e45/skills/cocoindex), an AI-coding-agent assist layer, which tells you the team is explicitly targeting agent-assisted development

The shape is healthy. The examples are abundant, but the engine is still clearly centralized instead of being scattered into vague framework mush.

## Layered architecture dissection
### High-level system shape
At a high level, the system is:

Python app declaration -> Python decorator/runtime bridge -> Rust component engine -> source scanning / function execution / memo reuse -> target reconciliation -> optional live watching.

The important thing is that CocoIndex does not just call user code directly. It wraps user functions as engine components with stable paths, context, memo fingerprints, and target-state semantics.

### Main layers
**1. App and orchestration layer**
- [`python/cocoindex/_internal/app.py`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/python/cocoindex/_internal/app.py)
- [`rust/core/src/engine/app.rs`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/rust/core/src/engine/app.rs)

This is where updates and drops are started, tracked, cancelled, and watched. On the Python side, `UpdateHandle` exposes progress snapshots and results. On the Rust side, `AppUpdateOptions`, `AppOpHandle`, and `App::update` own the real lifecycle.

This layer matters because it shows the repo is not a plain library call. It is an operation-oriented engine with long-running stateful work.

**2. Function wrapping, memoization, and execution-context layer**
- [`python/cocoindex/_internal/function.py`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/python/cocoindex/_internal/function.py)
- [`python/cocoindex/_internal/runner.py`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/python/cocoindex/_internal/runner.py)
- [`rust/core/src/engine/function.rs`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/rust/core/src/engine/function.rs)
- [`rust/core/src/engine/execution.rs`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/rust/core/src/engine/execution.rs)

This layer is the heart of the product idea. Decorated functions are fingerprinted, contextualized, memo-aware, and optionally serialized through runners. The GPU runner is especially telling: instead of pretending GPU work is “just another async call,” they give it an execution model with queueing and optional subprocess isolation.

**3. Component graph and incremental-state layer**
- [`rust/core/src/engine/component.rs`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/rust/core/src/engine/component.rs)
- [`rust/core/src/engine/context.rs`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/rust/core/src/engine/context.rs)
- [`rust/core/src/state/stable_path.rs`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/rust/core/src/state/stable_path.rs)
- [`rust/core/src/engine/logic_registry.rs`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/rust/core/src/engine/logic_registry.rs)

This is where the framework becomes a real incremental engine instead of a convenience wrapper. Stable paths and logic tracking let the runtime reason about identity and code changes. That is the machinery you need if you want “only the delta” to mean something real.

**4. Source, live-feed, and connector layer**
- [`python/cocoindex/connectors/localfs/_source.py`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/python/cocoindex/connectors/localfs/_source.py)
- [`rust/core/src/engine/live_component.rs`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/rust/core/src/engine/live_component.rs)
- [`python/cocoindex/_internal/api.py`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/python/cocoindex/_internal/api.py)

The local filesystem walker is a good example of the repo’s style. It supports both catch-up iteration and live watch mode, and exposes keyed item streams that fit naturally into `mount_each()` processing. This is a concrete sign that the team designed for continuously updated sources, not just static backfills.

**5. Target-state and sink layer**
- [`python/cocoindex/connectors/postgres/_target.py`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/python/cocoindex/connectors/postgres/_target.py)
- [`rust/core/src/engine/target_state.rs`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/rust/core/src/engine/target_state.rs)
- [`rust/core/src/state/target_state_path.rs`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/rust/core/src/state/target_state_path.rs)

The repo does not think in terms of “return a dataset.” It thinks in terms of durable target state that must be reconciled, diffed, created, updated, and deleted. The Postgres target’s two-level model, table first and rows second, is a nice concrete example.

**6. Developer-facing ops and examples layer**
- [`python/cocoindex/cli.py`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/python/cocoindex/cli.py)
- [`examples/code_embedding/main.py`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/examples/code_embedding/main.py)
- [`examples/conversation_to_knowledge/`](https://github.com/cocoindex-io/cocoindex/tree/31ef7059195903dd8b7501b4cbb9946f9ba42e45/examples/conversation_to_knowledge)
- [`docs/src/content/docs/`](https://github.com/cocoindex-io/cocoindex/tree/31ef7059195903dd8b7501b4cbb9946f9ba42e45/docs/src/content/docs)

This is partly productization and partly go-to-market, but it also reveals design intent. The examples are not throwaway toy scripts. They are the quickest way to see which abstractions the team thinks are strong enough to reuse.

### Request / data / control flow
A typical flow looks like this:

1. a user defines an app and decorated functions in Python via [`python/cocoindex/_internal/api.py`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/python/cocoindex/_internal/api.py)
2. the app is wrapped in [`python/cocoindex/_internal/app.py`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/python/cocoindex/_internal/app.py), which exposes update handles and progress watchers
3. user functions are transformed into engine processors in [`python/cocoindex/_internal/function.py`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/python/cocoindex/_internal/function.py)
4. the Rust app engine launches an update task in [`rust/core/src/engine/app.rs`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/rust/core/src/engine/app.rs)
5. components execute through the engine graph, reusing memoized results when logic and inputs still match
6. sources such as the local filesystem emit keyed items through connectors like [`python/cocoindex/connectors/localfs/_source.py`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/python/cocoindex/connectors/localfs/_source.py)
7. targets such as Postgres reconcile durable state via [`python/cocoindex/connectors/postgres/_target.py`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/python/cocoindex/connectors/postgres/_target.py)
8. if live mode is enabled, watchers continue feeding incremental changes instead of treating the run as a one-shot batch

That is a coherent control loop. The repo’s real thesis is that indexing should behave like a maintained application, not a nightly job.

## Key directories and files
If you want the fastest path to understanding the repo, study these first:

- [`pyproject.toml`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/pyproject.toml), because it shows the Python package boundaries, optional connector extras, and the maturin bridge into Rust
- [`Cargo.toml`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/Cargo.toml), because it reveals the Rust workspace split and that `rust/core` is the center of gravity
- [`python/cocoindex/_internal/app.py`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/python/cocoindex/_internal/app.py), for update handles and progress semantics
- [`python/cocoindex/_internal/function.py`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/python/cocoindex/_internal/function.py), for memo, fingerprint, and wrapper behavior
- [`python/cocoindex/_internal/runner.py`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/python/cocoindex/_internal/runner.py), for serialized runner execution and subprocess isolation
- [`rust/core/src/engine/app.rs`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/rust/core/src/engine/app.rs), for update/drop lifecycle
- [`rust/core/src/engine/component.rs`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/rust/core/src/engine/component.rs), for the component orchestration model
- [`rust/core/src/engine/target_state.rs`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/rust/core/src/engine/target_state.rs), for reconciliation semantics
- [`python/cocoindex/connectors/localfs/_source.py`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/python/cocoindex/connectors/localfs/_source.py), for live source behavior
- [`python/cocoindex/connectors/postgres/_target.py`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/python/cocoindex/connectors/postgres/_target.py), for one of the most concrete target implementations
- [`python/cocoindex/ops/text.py`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/python/cocoindex/ops/text.py), for the clean Python wrapper over native chunking and code-language detection
- [`examples/`](https://github.com/cocoindex-io/cocoindex/tree/31ef7059195903dd8b7501b4cbb9946f9ba42e45/examples), because the examples encode the supported mental model better than the marketing copy does

## Important components
- `UpdateHandle` in [`python/cocoindex/_internal/app.py`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/python/cocoindex/_internal/app.py), which exposes a sane progress API instead of making users poll raw engine state
- `_ENV_MAX_INFLIGHT_COMPONENTS` and `_DEFAULT_MAX_INFLIGHT_COMPONENTS` in [`python/cocoindex/_internal/app.py`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/python/cocoindex/_internal/app.py), which show the framework already expects scale and backpressure tuning
- `GPURunner` in [`python/cocoindex/_internal/runner.py`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/python/cocoindex/_internal/runner.py), which serializes GPU work and can isolate it in a subprocess
- `AppUpdateOptions` and `AppOpHandle` in [`rust/core/src/engine/app.rs`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/rust/core/src/engine/app.rs), which make live mode and full reprocess explicit runtime concepts
- `DirWalker.items()` and `_LiveDirItems.watch()` in [`python/cocoindex/connectors/localfs/_source.py`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/python/cocoindex/connectors/localfs/_source.py), which make keyed live source updates feel native
- the Postgres type-mapping and target-state machinery in [`python/cocoindex/connectors/postgres/_target.py`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/python/cocoindex/connectors/postgres/_target.py), which turns Python data types into actual durable sinks
- `detect_code_language`, `SeparatorSplitter`, and `RecursiveSplitter` in [`python/cocoindex/ops/text.py`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/python/cocoindex/ops/text.py), which are small but important because they show a nice Python-over-Rust boundary

## Important knobs / configs / extension points
- [`pyproject.toml`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/pyproject.toml) exposes a wide extras matrix, which is how the repo avoids forcing every connector dependency into the base install
- `COCOINDEX_MAX_INFLIGHT_COMPONENTS` in [`python/cocoindex/_internal/app.py`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/python/cocoindex/_internal/app.py), a concurrency/backpressure knob for component execution
- `COCOINDEX_RUN_GPU_IN_SUBPROCESS` in [`python/cocoindex/_internal/runner.py`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/python/cocoindex/_internal/runner.py), a pragmatic isolation switch for unstable GPU workloads
- `AppUpdateOptions.full_reprocess` and `.live` in [`rust/core/src/engine/app.rs`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/rust/core/src/engine/app.rs), the two big mode toggles that define whether this behaves like a rebuild or a continuously updating app
- `PgType` in [`python/cocoindex/connectors/postgres/_target.py`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/python/cocoindex/connectors/postgres/_target.py), a clean extension point for schema control
- `CustomLanguageConfig` in [`python/cocoindex/ops/text.py`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/python/cocoindex/ops/text.py), a nice escape hatch for domain-specific chunking

## Practical questions and answers
**What is this project actually optimizing for?**

Freshness and incremental maintenance, not raw ingestion throughput alone. The recurring pattern everywhere is “what can we avoid recomputing?”

**What assumption does the system make?**

That your transformations can be expressed as structured components with stable identity and replayable semantics. If your pipeline is chaotic, side-effect-heavy, or impossible to fingerprint, the model weakens.

**Where would it break first in production?**

In the gray zone between pure dataflow and messy user code. Connectors, LLM calls, GPU work, and external services all create nondeterminism. The framework can track a lot, but it cannot magically make impure code incremental-safe.

**Is the Python-over-Rust split justified?**

Yes. Python is the right surface for authoring flows, but the engine work, concurrency, state tracking, and target reconciliation benefit from Rust. This is one of the better reasons to go hybrid.

**What is hardest to copy?**

The stable-path, memo, and target-state machinery in the engine. Fancy examples are easy to clone. A trustworthy incremental core is not.

**What is probably more marketing than reality?**

The broad “any source, any target, any scale” vibe in the README. The architecture is real, but practical reliability will still depend heavily on connector maturity and the specific workloads people try to push through it.

## What is smart
- The Python API is thin enough that the repo does not hide where the real power lives.
- The engine clearly models long-running operations, progress, and cancellation instead of treating them as afterthoughts.
- The live filesystem source is practical and well aligned with the incremental thesis.
- The GPU runner design is sober. Serializing GPU execution and allowing subprocess isolation is the kind of unglamorous decision that saves pain later.
- The connector extras strategy in [`pyproject.toml`](https://github.com/cocoindex-io/cocoindex/blob/31ef7059195903dd8b7501b4cbb9946f9ba42e45/pyproject.toml) is sensible for a wide-surface infra library.
- The repo ships a lot of examples, which is not just marketing. It is how a framework like this proves its abstractions are reusable.

## What is flawed or weak
- The README is heavily merchandised. It sells hard before it explains. That is fine for growth, but it obscures the genuinely interesting engine underneath.
- The repo surface is broad: many connectors, many examples, docs, skills, CLI, and a hybrid runtime. Breadth is useful, but it increases the chance that some connectors are much more mature than others.
- The system’s promise depends on users writing relatively well-behaved transformation code. That is an unavoidable weakness of this category.
- The framework still needs trust in its invalidation logic. If incremental correctness is even slightly wrong, users will get stale or inconsistent state with false confidence.
- Some of the repo’s conceptual vocabulary is dense. New users may understand the examples before they understand the model.

## What we can learn / steal
- Treat incremental recomputation as a product feature, not an optimization pass.
- Model target state explicitly instead of pretending outputs are just blobs.
- Give long-running pipeline operations first-class progress and cancellation APIs.
- Keep the user-facing DSL high-level, but push the fragile concurrency/state machinery into a stricter runtime.
- Build examples that correspond to real deployment patterns, not just “hello world” demos.

## How we could apply it
If we were building our own agent-data system, I would steal three ideas immediately:

1. the split between a friendly Python declaration layer and a stricter engine core
2. stable identity plus memo-aware invalidation as the backbone of incremental updates
3. target reconciliation as a first-class abstraction, especially for DB-backed outputs

I would be more cautious about copying the whole ambition envelope at once. Better to start with one source family, one target family, and one rock-solid invalidation story than to imitate the whole connector matrix too early.

## Bottom line
CocoIndex is one of the more serious AI-data repos in the current wave because it is solving the right boring problem.

The key insight is simple: the valuable thing is not “RAG pipelines.” The valuable thing is a runtime that can keep derived agent context continuously correct and cheap as sources and code change. This repo actually seems to understand that.