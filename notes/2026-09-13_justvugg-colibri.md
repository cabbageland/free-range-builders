# Colibri

- Repo: `JustVugg/colibri`
- URL: https://github.com/JustVugg/colibri
- Date: 2026-09-13
- Repo snapshot studied: `main` @ `3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48`
- Why picked today: GitHub's daily trending page had `JustVugg/colibri` at the top of the page, with roughly 29k stars and 652 stars today in the fetched page. I picked it because the pitch is technically sharp: run giant sparse MoE models on ordinary heterogeneous machines by treating disk, RAM, and VRAM as one inference hierarchy.

## Executive summary
[`JustVugg/colibri`](https://github.com/JustVugg/colibri/tree/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48) is not a wrapper around an existing inference server. It is a systems-heavy C runtime for Mixture-of-Experts inference where dense weights stay resident and routed experts move through disk, RAM, and GPU tiers as demand changes. The landing claim in [`README.md`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/README.md) is "tiny engine, immense model"; the source backs that up better than most viral AI repos because the real work is in concrete files like [`c/colibri.c`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/colibri.c), [`c/tier.h`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/tier.h), [`c/expert_store.h`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/expert_store.h), and the accelerator backends under [`c`](https://github.com/JustVugg/colibri/tree/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c).

The core idea is simple and hard: sparse MoE layers do not need every expert resident for every token. [`c/colibri.c`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/colibri.c) computes routing, builds a batch union of selected experts, checks resident tiers, streams misses, overlaps I/O with CPU/GPU work where possible, and records enough telemetry to decide whether an optimization is real. The project is strongest where it treats placement as a performance policy, not a semantic change.

The weak point is also obvious: much of the brain lives in one enormous C file with many compile-time and environment-controlled behaviors. That makes local performance hacking possible, but it raises the cost of understanding the whole correctness surface. Still, this is exactly the kind of repo worth studying: ambitious, source-rich, measurable, and full of reusable systems lessons.

## What they built
Colibri is a local inference engine plus developer platform for sparse frontier-scale models. The README says it supports GLM-5.2/5.3, Inkling, Kimi K3, DeepSeek V4, Qwen3.8, Qwen3.6, and OLMoE families through the same `coli chat`, `coli serve`, and `coli web` front end. The C directory contains the model-family files, including [`c/glm53.c`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/glm53.c), [`c/kimi_k3.c`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/kimi_k3.c), [`c/deepseek_v4.c`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/deepseek_v4.c), [`c/qwen38.c`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/qwen38.c), [`c/qwen36.c`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/qwen36.c), and [`c/olmoe.c`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/olmoe.c).

The project also ships a Python launcher in [`c/coli`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/coli), a pip entry wrapper in [`colibri/cli.py`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/colibri/cli.py), OpenAI-compatible serving through [`c/openai_server.py`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/openai_server.py), and a React dashboard under [`web/src`](https://github.com/JustVugg/colibri/tree/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/web/src). The dashboard is not cosmetic; [`web/src/App.tsx`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/web/src/App.tsx) polls runtime health, streams chat, manages KV cache slots, surfaces profiling, and links into the live expert map rendered by [`web/src/Brain.tsx`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/web/src/Brain.tsx).

## Why it matters
Most open-weight inference talk assumes the model either fits or it does not. Colibri attacks the in-between: a model can be too large for VRAM but sparse enough that only a small changing subset of experts matters per token. [`docs/benchmarks.md`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/docs/benchmarks.md) is refreshingly explicit about the physics: cold GLM-5.2 decode can cost around 11 GB of expert reads per token, so disk, page cache, RAM budget, CPU kernels, and GPU residency all determine the real speed.

The useful lesson is not "this makes huge models free." It is the opposite: make the bottleneck visible, then design around it. [`docs/quickstart.md`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/docs/quickstart.md) tells users a fast NVMe drive is a first-order performance component. [`docs/benchmarks.md`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/docs/benchmarks.md) records negative and machine-specific results rather than flattening everything into one leaderboard number. [`docs/serve_protocol.md`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/docs/serve_protocol.md) exposes the engine/server protocol instead of burying it in ad hoc stdout parsing.

## Repo shape at a glance
- [`README.md`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/README.md): public thesis, supported model roster, memory hierarchy explanation, cluster mode, and measured research claims.
- [`c`](https://github.com/JustVugg/colibri/tree/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c): core runtime, model-family implementations, quantization code, storage readers, accelerator backends, tests, tools, and build files.
- [`c/colibri.c`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/colibri.c): main general engine path, including routing, expert loading, cache/tier state, serving, profiling, speculation, and CLI entry.
- [`c/tier.h`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/tier.h): small promotion/decay/LFRU policy for adaptive resident tiers.
- [`c/expert_store.h`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/expert_store.h) and [`c/expert_store_registry.c`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/expert_store_registry.c): lease-based expert-store API and backend registry.
- [`c/backend_cuda.cu`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/backend_cuda.cu), [`c/backend_metal.mm`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/backend_metal.mm), and [`c/backend_vulkan.c`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/backend_vulkan.c): accelerator paths for heterogeneous expert execution.
- [`c/tests`](https://github.com/JustVugg/colibri/tree/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/tests): many narrow C tests for tokenizers, quantization, stores, tier invariants, serving framing, routing, KV, GPU paths, and adapters.
- [`c/tools`](https://github.com/JustVugg/colibri/tree/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/tools): conversion, oracle, tokenizer, route-analysis, packing, benchmark, and fixture generators.
- [`docs`](https://github.com/JustVugg/colibri/tree/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/docs): architecture notes, benchmark logs, backend docs, model-family docs, and the serving/segment protocol references.
- [`web/src`](https://github.com/JustVugg/colibri/tree/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/web/src): React chat/profiling/brain dashboard for the running engine.
- [`desktop/src-tauri`](https://github.com/JustVugg/colibri/tree/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/desktop/src-tauri): Tauri wrapper for the desktop app path.
- [`docker`](https://github.com/JustVugg/colibri/tree/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/docker): container packaging and docker-compose support.

## Layered architecture dissection
### High-level system shape
Colibri is best understood as an inference kernel wrapped by a practical local product. At the bottom are file formats, safetensor access, quantized matmuls, attention, KV state, and expert FFNs. The middle layer decides where experts live and how misses are served. Above that are the CLI, OpenAI-compatible server, multiplexed serving protocol, telemetry, web UI, and optional desktop/container packaging.

The strong boundary is not "C versus Python"; it is "hot token path versus orchestration." [`c/colibri.c`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/colibri.c) owns the hot path. [`c/coli`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/coli) owns user-facing command selection, resource planning, model resolution, and launcher ergonomics. [`docs/serve_protocol.md`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/docs/serve_protocol.md) owns the protocol contract between engine and server.

### Main layers
**1. Launcher and build layer**  
[`c/coli`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/coli) is a Python command launcher for `chat`, `serve`, `run`, `info`, `plan`, `mirror`, `doctor`, `bench`, `convert`, and `build`. [`pyproject.toml`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/pyproject.toml) packages that as `colibri-engine`, while [`c/Makefile`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/Makefile) spends real effort on platform detection, OpenMP, architecture flags, Windows, macOS, Linux, aarch64, and LTO caution.

**2. Model-family layer**  
The runtime has a general engine path in [`c/colibri.c`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/colibri.c), but it is surrounded by family-specific source files and fixture generators. [`c/family_registry.py`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/family_registry.py) gives the launcher a family vocabulary, while files like [`c/kimi_k3.c`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/kimi_k3.c) and [`c/deepseek_v4.c`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/deepseek_v4.c) carry model-specific math and formats.

**3. Expert residency and storage layer**  
The key structures in [`c/colibri.c`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/colibri.c) distinguish pinned hot experts, LRU cache rows, disk-class counters, mmap/pread loading, direct I/O, mirrors, and GPU-resident tiers. [`c/tier.h`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/tier.h) keeps the adaptive policy intentionally small: heat decays, hot experts only displace cold ones with hysteresis, and LFRU gives frequency priority with recency as a tie breaker.

**4. Per-token MoE execution layer**  
The `moe()` implementation in [`c/colibri.c`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/colibri.c) does the structural work. It computes router logits, selects experts, optionally applies `TOPK`, `TOPP`, `CACHE_ROUTE`, route tracing, or ablation hooks, builds a unique expert union across the batch, resolves each unique expert from VRAM/RAM/LRU/disk, loads misses, and accumulates expert FFN outputs. This is the center of the project.

**5. Accelerator and overlap layer**  
The runtime tries to overlap what can be overlapped. [`c/backend_cuda.cu`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/backend_cuda.cu), [`c/backend_metal.mm`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/backend_metal.mm), and [`c/backend_vulkan.c`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/backend_vulkan.c) make GPU tiers real rather than aspirational. [`c/uring.h`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/uring.h) and the direct/mirror logic in [`c/colibri.c`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/colibri.c) show that storage is treated as an active subsystem, not a file-load prelude.

**6. Serving and telemetry layer**  
[`docs/serve_protocol.md`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/docs/serve_protocol.md) documents the engine/server wire format: `SUBMIT`, `IMAGE`, `STOP`, `CANCEL`, token `DATA`, `DONE` stats, `PERF`, `TIERS`, `EMAP`, `HITS`, `REPIN`, and `TOPK`. [`web/src/Brain.tsx`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/web/src/Brain.tsx) consumes the expert map and hit bitmap to render the live storage tier and routing heat for every expert.

**7. Segment runtime layer**  
[`docs/segment-runtime.md`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/docs/segment-runtime.md) describes a local C ABI for contiguous layer ranges, with adapter registration, capabilities, session isolation, snapshots, and conformance tests. The corresponding files [`c/segment_runtime.h`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/segment_runtime.h), [`c/segment_runtime.c`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/segment_runtime.c), and [`c/segment_adapters.h`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/segment_adapters.h) point toward distributed execution without pretending transport is solved by the ABI.

### Request / data / control flow
A normal local run starts through [`c/coli`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/coli), which resolves the model, RAM budget, mirror path, and subcommand before launching the C engine. `coli serve` or `coli web` then keeps an engine process alive and communicates over the documented protocol in [`docs/serve_protocol.md`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/docs/serve_protocol.md).

Inside the engine, each sparse layer enters `moe()` in [`c/colibri.c`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/colibri.c). Phase A routes every row in the batch and updates heat/recency/trace state. Phase B builds the unique expert set, optionally trims it under decode-safe budgets, and avoids loading duplicate experts for the same batch. Phase C/D resolves the unique experts from the resident tiers or calls `expert_load()` for misses. `expert_load_impl()` then finds tensor names, chooses mmap or pread, uses replicas/mirrors when configured, reads weight and scale tensors, resolves the quantized format, and exposes gate/up/down tensors to the FFN compute path.

Serving emits telemetry as part of the same loop. The web UI reads health and expert maps, [`web/src/App.tsx`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/web/src/App.tsx) turns that into chat and profiling state, and [`web/src/Brain.tsx`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/web/src/Brain.tsx) makes tier placement visible as a grid of experts.

## Key directories and files
- [`c/colibri.c`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/colibri.c): main engine, routing, MoE execution, disk loading, resident tiers, protocol serving, and many runtime knobs.
- [`c/tier.h`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/tier.h): promotion, decay, and LFRU scoring for adaptive tier placement.
- [`c/expert_store.h`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/expert_store.h): lease contract for expert store lookup/release/prefetch/stats.
- [`c/expert_store_registry.c`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/expert_store_registry.c): pluggable expert-store backend registry, including the built-in auto backend.
- [`c/quant.h`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/quant.h): quantization formats and dispatch rules that decide how tensors are interpreted.
- [`c/st.h`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/st.h): safetensor/container access layer used by the expert loader.
- [`c/serve_codec.h`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/serve_codec.h) and [`c/serve_poll.h`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/serve_poll.h): serving support around the engine protocol.
- [`docs/serve_protocol.md`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/docs/serve_protocol.md): reference for mux and legacy engine/server protocols.
- [`docs/benchmarks.md`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/docs/benchmarks.md): measurement log and performance caveats.
- [`docs/segment-runtime.md`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/docs/segment-runtime.md): layer-range ABI and distributed-adapter contract.
- [`web/src/App.tsx`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/web/src/App.tsx) and [`web/src/Brain.tsx`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/web/src/Brain.tsx): browser control surface and live expert map.

## Important components
`moe()` in [`c/colibri.c`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/colibri.c) is the component to read first. It is where routing becomes system behavior: top-k selection, optional cache-aware routing, expert heat, batch union, demand misses, GPU grouping, CPU fallback, budget trimming, and output accumulation all meet in one place.

`expert_load_impl()` in [`c/colibri.c`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/colibri.c) is the second important component. It maps logical expert names to safetensor entries, chooses replicas, handles mmap or pread, reads weights and scales, applies format resolution, and keeps disk-service accounting paired with the actual read work.

[`c/tier.h`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/tier.h) is small but conceptually important. `tier_pick_lfru()` gives one clean example of policy restraint: do not churn resident slots just because something was recent; require a frequency margin before replacing a colder expert.

[`c/expert_store.h`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/expert_store.h) is the maintainability counterweight to the big C file. Its lease contract is explicit: lookup returns a view, release must happen once, prefetch is advisory, and thread-safety is backend-specific.

[`web/src/Brain.tsx`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/web/src/Brain.tsx) is the most delightful UI component. It turns `EMAP` and `HITS` telemetry into a live cortex: tier color, routing heat brightness, recent-hit pulses, and optional atlas labels. That is useful instrumentation, not just decoration.

## Important knobs / configs / extension points
- [`c/coli`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/coli): `COLI_MODEL`, `COLI_MODEL_MIRROR`, `--ram`, `--cap`, `--repin`, `--topp`, `--topk`, `--ngen`, `plan`, `doctor`, `mirror`, and `convert`.
- [`c/colibri.c`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/colibri.c): `DIRECT`, `PREFETCH`, `SPEC`, `DRAFT`, `GRAMMAR`, `TOPK`, `TOPP`, `EXPERT_BUDGET`, `CACHE_ROUTE`, `ROUTE_TRACE`, `COUPLE`, `PILOT`, `PILOT_REAL`, `COLI_NUMA`, `COLI_VULKAN`, and CUDA/Metal tier controls.
- [`docs/benchmarks.md`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/docs/benchmarks.md): the practical tuning order: disk benchmark, chat stats, datapoint script, usage history, hot expert pinning, and quality benchmarks.
- [`docs/serve_protocol.md`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/docs/serve_protocol.md): `SERVE_BATCH`, `KV_SLOTS`, mux framing, image frames, stop/cancel semantics, telemetry lines, and OpenAI-compatible `/v1/chat/completions`.
- [`c/expert_store_registry.c`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/expert_store_registry.c): `COLI_EXPERT_STORE` as the backend selector for linked expert-store implementations.
- [`c/segment_adapters.h`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/segment_adapters.h): explicit adapter registration for engines that want contiguous layer-range execution.

## Practical questions and answers
**Is this mostly hype around "run a giant model locally"?**  
No. The README is loud, but [`c/colibri.c`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/colibri.c), [`docs/benchmarks.md`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/docs/benchmarks.md), and [`c/tests`](https://github.com/JustVugg/colibri/tree/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/tests) show a real engineering project. It may be rough, but it is not a landing page pretending to be a system.

**Where should a builder start reading?**  
Start with [`README.md`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/README.md) for the thesis, then [`docs/benchmarks.md`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/docs/benchmarks.md) for the real bottlenecks, then search inside [`c/colibri.c`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/colibri.c) for `static void moe` and `expert_load_impl`.

**What is the central architectural bet?**  
The central bet is that expert placement can be adaptive and measured while preserving model semantics. A cache hit from VRAM, a RAM-pinned expert, and a disk-loaded expert should compute the same expert, just with different latency. The comments around default policies in [`c/colibri.c`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/colibri.c) repeatedly distinguish measurement-only features from math-changing knobs.

**Where would production pain show up?**  
Operational complexity. A serious deployment would need disciplined profiles for each machine, model family, quant format, storage layout, GPU backend, and request mix. The many knobs in [`c/coli`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/coli) and [`c/colibri.c`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/colibri.c) are powerful, but they also make accidental benchmark theater easy.

**Is the UI worth studying?**  
Yes, because it visualizes runtime truth. [`web/src/Brain.tsx`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/web/src/Brain.tsx) is a model operations view: it renders storage tier, heat, recent routing, and atlas hints from live endpoints. Builders should steal that habit for any adaptive runtime.

## What is smart
- The repo makes storage visible as part of inference. [`docs/benchmarks.md`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/docs/benchmarks.md) treats NVMe behavior, page cache, direct I/O, RAM caps, and CPU kernels as measured variables.
- The adaptive tier policy in [`c/tier.h`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/tier.h) has hysteresis. That is a small but important defense against cache churn.
- [`c/colibri.c`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/colibri.c) builds a batch union of experts before loading/compute, which is the right shape for sparse MoE inference under batch or multi-slot serving.
- [`docs/serve_protocol.md`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/docs/serve_protocol.md) documents forward-compatible telemetry lines instead of leaving downstream clients to reverse-engineer stdout.
- [`web/src/Brain.tsx`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/web/src/Brain.tsx) closes the loop between routing behavior and human intuition.
- [`docs/segment-runtime.md`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/docs/segment-runtime.md) is honest about what an ABI does not own: transport, peer identity, leases, placement, and retry policy.

## What is flawed or weak
- [`c/colibri.c`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/colibri.c) is enormous. That may be useful for single-file hacking and whole-system performance work, but it makes independent review hard.
- The runtime surface has many flags. Powerful knobs like `TOPK`, `TOPP`, `EXPERT_BUDGET`, `CACHE_ROUTE`, `PILOT_REAL`, direct I/O, mirror routing, and GPU tiers need disciplined A/Bs, or users will tune themselves into misleading results.
- The main claims depend heavily on model format availability, fast storage, and machine-specific behavior. [`docs/quickstart.md`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/docs/quickstart.md) is clear that the large model path needs hundreds of GB of disk.
- Some source comments are highly context-dense and mixed-language. They are valuable, but they also encode a lot of project memory in places where a new contributor has to parse performance history before understanding the current invariant.
- The project is closer to a research runtime than a boring product dependency. That is part of its charm, but it matters if you need supportable infrastructure.

## What we can learn / steal
- Treat model inference as a memory hierarchy problem. The split between dense resident weights and routed expert movement in [`README.md`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/README.md) is a reusable lens even if you never run this engine.
- Make placement policies observable. [`docs/serve_protocol.md`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/docs/serve_protocol.md) and [`web/src/Brain.tsx`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/web/src/Brain.tsx) show the right instinct: expose tiers, hits, heat, and profiling to users.
- Keep cache promotion conservative. [`c/tier.h`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/tier.h) is a tiny example of frequency-first LFRU with margin.
- Document the wire protocol. [`docs/serve_protocol.md`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/docs/serve_protocol.md) is a good pattern for any local engine with a UI or HTTP server above it.
- Separate measurement-only instrumentation from math-changing shortcuts. The comments around route tracing, disk classing, speculation, and expert budgets in [`c/colibri.c`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/c/colibri.c) are worth copying as a habit.

## How we could apply it
If we were building a local AI runtime, I would copy the "measure the memory hierarchy first" approach from [`docs/benchmarks.md`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/docs/benchmarks.md). Before adding another scheduler, benchmark the actual read pattern, expose bytes-per-token, separate cold/warm runs, and make the resident set visible.

I would also copy the explicit telemetry contract from [`docs/serve_protocol.md`](https://github.com/JustVugg/colibri/blob/3a70acbf6e7054f6edcf4b7d3b1e679793eb8e48/docs/serve_protocol.md). A local engine should not just return tokens; it should report where the time went, how much memory it used, which tiers served the work, and which assumptions changed during the run.

For our own code, I would be more cautious about file size than Colibri is. The runtime's single-file density helps performance experiments land quickly, but a product team would want smaller modules around loader policy, routing policy, serving protocol, and telemetry before many contributors start touching it.

## Bottom line
`JustVugg/colibri` is an excellent builder study because it turns a hard resource mismatch into a concrete runtime: route sparse experts, keep dense state resident, stream misses, adapt the hot set, use GPUs when they actually help, and show the operator what happened.

The best insight is not that a 744B-class MoE suddenly becomes cheap. The best insight is that "fit" is too blunt a deployment concept for sparse models. Colibri treats inference as placement, movement, measurement, and correctness under pressure. That is worth stealing.
