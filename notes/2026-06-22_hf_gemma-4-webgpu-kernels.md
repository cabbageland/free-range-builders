# Gemma 4 WebGPU Kernels

- Source: Hugging Face
- Artifact: space `webml-community/gemma-4-webgpu-kernels`
- URL: https://huggingface.co/spaces/webml-community/gemma-4-webgpu-kernels
- Date: 2026-06-22
- Snapshot studied: `main` @ `158f16ae0f672943ca304d59c47c8e3a264e399e`, last modified 2026-06-17T22:28:48Z
- Why picked today: It was one of the top Hugging Face trending Spaces when checked, and unlike most "run a model in the browser" demos it exposes the interesting parts: progress accounting, warmup, cache reuse, GPU feature gating, and the actual WebGPU kernel bundle.

## Executive summary
This Space is a static, fully client-side Gemma 4 chat app, but the valuable part is not the demo itself. The valuable part is how much of the on-device serving stack is left visible in source. [`index.html`](https://huggingface.co/spaces/webml-community/gemma-4-webgpu-kernels/blob/main/index.html) owns the entire app shell, load lifecycle, progress UX, streaming metrics, and chat loop. [`landing.js`](https://huggingface.co/spaces/webml-community/gemma-4-webgpu-kernels/blob/main/landing.js) runs a GPU-hungry WebGL hero background but deliberately pauses it when the chat dominates the viewport so it stops competing with the model. [`gemma-4-e2b.js`](https://huggingface.co/spaces/webml-community/gemma-4-webgpu-kernels/blob/main/gemma-4-e2b.js) bundles the actual `Gemma4Mobile` runtime, tokenizer, cache-aware generation state, device feature inspection, and a large embedded library of WGSL kernel manifests and templates.

The strongest builder lesson is that this demo treats browser inference as a systems problem. `Gemma4Mobile.load` in [`gemma-4-e2b.js`](https://huggingface.co/spaces/webml-community/gemma-4-webgpu-kernels/blob/main/gemma-4-e2b.js) emits explicit load phases, enables shader capture, and streams byte-level weight progress separately from tensor-materialization progress. The chat loop in [`index.html`](https://huggingface.co/spaces/webml-community/gemma-4-webgpu-kernels/blob/main/index.html) tracks TTFT and decode throughput live. The generation runtime reuses prefix cache across turns rather than recomputing the whole conversation blindly.

The caution is that the artifact is simultaneously admirably transparent and annoyingly opaque. The important logic is present, but much of it is packed into a giant generated bundle. That makes the engineering visible enough to study, but harder to modify than a small modular codebase.

## What they built / released
They released a browser-first WebGPU chat product around [`google/gemma-4-E2B-it-qat-mobile-transformers`](https://huggingface.co/google/gemma-4-E2B-it-qat-mobile-transformers) with only a handful of repo files:

- [`README.md`](https://huggingface.co/spaces/webml-community/gemma-4-webgpu-kernels/blob/main/README.md), minimal Space metadata plus the linked model
- [`index.html`](https://huggingface.co/spaces/webml-community/gemma-4-webgpu-kernels/blob/main/index.html), the entire product shell, chat UX, progress bar, metrics, kernel drawer, and generation loop
- [`landing.js`](https://huggingface.co/spaces/webml-community/gemma-4-webgpu-kernels/blob/main/landing.js), the WebGL/Three.js landing background and GPU-budget management logic
- [`gemma-4-e2b.js`](https://huggingface.co/spaces/webml-community/gemma-4-webgpu-kernels/blob/main/gemma-4-e2b.js), the bundled WebGPU runtime and kernels

This is not a hosted inference wrapper. The whole pitch is local execution: the browser requests a WebGPU device, downloads model assets, caches them, warms kernels, and generates tokens on the client.

## Why it matters
Many Hugging Face Spaces claim "runs in browser" while hiding the interesting mechanics behind a library import. This one is more revealing.

That matters for three reasons:

1. It shows the real UX work required to make browser inference feel credible: progress phases, cache messaging, warmup, TTFT stats, and graceful feature failure.
2. It makes kernel selection and device capability gating visible instead of pretending all GPUs behave the same.
3. It demonstrates that a good demo should manage GPU contention across the whole page, not just inside the model call.

## Artifact shape at a glance
The artifact is small in file count but layered in responsibility:

- [`README.md`](https://huggingface.co/spaces/webml-community/gemma-4-webgpu-kernels/blob/main/README.md), bare Space config and model attachment
- [`index.html`](https://huggingface.co/spaces/webml-community/gemma-4-webgpu-kernels/blob/main/index.html), app shell, styles, status system, load pipeline, and streaming chat UI
- [`landing.js`](https://huggingface.co/spaces/webml-community/gemma-4-webgpu-kernels/blob/main/landing.js), the ornamental-but-careful GPU front page
- [`gemma-4-e2b.js`](https://huggingface.co/spaces/webml-community/gemma-4-webgpu-kernels/blob/main/gemma-4-e2b.js), model runtime, tokenizer path, cache logic, op manifests, and WGSL templates

The repo shape says the team optimized for one thing: make the "all local, all browser" story legible enough that people can see both the performance and the kernel craft.

## Layered architecture dissection
### High-level system shape
The stack is straightforward:

1. [`index.html`](https://huggingface.co/spaces/webml-community/gemma-4-webgpu-kernels/blob/main/index.html) loads the app and checks `navigator.gpu`;
2. clicking load calls `Gemma4Mobile.load` from [`gemma-4-e2b.js`](https://huggingface.co/spaces/webml-community/gemma-4-webgpu-kernels/blob/main/gemma-4-e2b.js);
3. the runtime loads tokenizer/config/weights, requests a WebGPU device, and warms kernels;
4. chat messages stream through `model.generate(...)`;
5. the UI coalesces renders, shows TTFT/tokens-per-second, and exposes kernel details in a drawer.

### Main layers
**1. Product shell layer**
[`index.html`](https://huggingface.co/spaces/webml-community/gemma-4-webgpu-kernels/blob/main/index.html) is doing far more than markup. It owns status transitions, progress smoothing, load buttons, abort handling, seed prompts, markdown rendering, live metric updates, and kernel drawer interactions. This is effectively the whole frontend app in one file.

**2. Model lifecycle layer**
The `loadModel()` path in [`index.html`](https://huggingface.co/spaces/webml-community/gemma-4-webgpu-kernels/blob/main/index.html) is careful about user trust. It distinguishes `init`, `tokenizer`, `weights`, and `ready` phases, scrolls the viewer into the chat during load, warms kernels after weights arrive, and only enables interaction after warmup completes.

**3. Runtime and caching layer**
`Gemma4Mobile` in [`gemma-4-e2b.js`](https://huggingface.co/spaces/webml-community/gemma-4-webgpu-kernels/blob/main/gemma-4-e2b.js) is the most instructive component. `load()` creates or reuses the WebGPU runtime, loads tokenizer config and model snapshot, captures shaders, and surfaces progress events. `generate()` then computes the longest shared prompt prefix, reuses cached generation state when possible, and only resets the cache when the conversation diverges. That is exactly the kind of detail that separates toy demos from serious local inference products.

**4. Kernel-selection layer**
The same bundle embeds op manifests with `when` guards keyed to things like `device.features.has("subgroups")`, `device.features.has("chromium-experimental-subgroup-matrix")`, and reported subgroup sizes in `adapterInfo`. The bundle contains multiple shader families, including templates such as `norm-row-stats.wgsl.jinja`, `decode-gate-up-norm-presrq.wgsl.jinja`, and `decode-gate-up-norm-sgmat.wgsl.jinja`, with staged, subgroup, and subgroup-matrix variants. That is the heart of the artifact's claim: it is not merely running a model in WebGPU, it is selecting kernel strategies based on actual device capability.

**5. Page-wide GPU arbitration layer**
[`landing.js`](https://huggingface.co/spaces/webml-community/gemma-4-webgpu-kernels/blob/main/landing.js) is surprisingly builder-relevant. The animated Three.js hero pauses itself when the chat view dominates the page, explicitly "freeing the GPU for the WebGPU model so decode throughput isn't dragged down by the WebGL background." That is a small but very real systems decision.

### Inference / data / control flow
The load and generation loop is the artifact in miniature:

1. `loadModel()` in [`index.html`](https://huggingface.co/spaces/webml-community/gemma-4-webgpu-kernels/blob/main/index.html) starts the progress UI and calls `Gemma4Mobile.load`.
2. `Gemma4Mobile.load` in [`gemma-4-e2b.js`](https://huggingface.co/spaces/webml-community/gemma-4-webgpu-kernels/blob/main/gemma-4-e2b.js) requests a runtime, loads tokenizer/config, downloads or reuses cached weights, and reports phase progress through `onProgress`.
3. `warmup()` runs short generations to prime kernels and then resets generation state.
4. `send()` in [`index.html`](https://huggingface.co/spaces/webml-community/gemma-4-webgpu-kernels/blob/main/index.html) calls `model.generate(messages, { maxNewTokens: 4096, signal })`.
5. The UI streams the full accumulated text, tracks first-token time and decode speed, and uses `requestAnimationFrame` to cap markdown re-renders so the UI does not steal too much time from generation.

## Key files, configs, cards, and artifacts
- [`README.md`](https://huggingface.co/spaces/webml-community/gemma-4-webgpu-kernels/blob/main/README.md), minimal config plus underlying model link
- [`index.html`](https://huggingface.co/spaces/webml-community/gemma-4-webgpu-kernels/blob/main/index.html), application UI and local-generation loop
- [`landing.js`](https://huggingface.co/spaces/webml-community/gemma-4-webgpu-kernels/blob/main/landing.js), landing background plus GPU-throttling policy
- [`gemma-4-e2b.js`](https://huggingface.co/spaces/webml-community/gemma-4-webgpu-kernels/blob/main/gemma-4-e2b.js), runtime, cache logic, and embedded kernel inventory
- [`google/gemma-4-E2B-it-qat-mobile-transformers`](https://huggingface.co/google/gemma-4-E2B-it-qat-mobile-transformers), the model repo the Space points at

## Important components
**`Gemma4Mobile` is the real product abstraction**
It wraps device setup, tokenizer/template loading, generation-state caching, warmup, streaming generation, reset behavior, and device capability reporting. That is the actual "run a serious local model in the browser" interface.

**The progress path is unusually honest**
[`index.html`](https://huggingface.co/spaces/webml-community/gemma-4-webgpu-kernels/blob/main/index.html) explicitly refuses to drive the progress bar from tensor-materialization counts because those can race ahead of true download progress. That is not glamorous, but it is exactly the kind of UX honesty most demos skip.

**The kernel manifests are the core technical asset**
The bundled WGSL templates and manifest guards in [`gemma-4-e2b.js`](https://huggingface.co/spaces/webml-community/gemma-4-webgpu-kernels/blob/main/gemma-4-e2b.js) are where the artifact becomes interesting. The code is clearly trying to match decode strategy to hardware features instead of pretending one shader fits all browsers and GPUs.

**The page-level GPU budget work is smart**
Pausing the WebGL hero while chat is active in [`landing.js`](https://huggingface.co/spaces/webml-community/gemma-4-webgpu-kernels/blob/main/landing.js) is the kind of detail that tells you the authors actually measured contention instead of just shipping a pretty background.

## Important knobs / configs / extension points
- `maxNewTokens: 4096` and abort-signal handling in [`index.html`](https://huggingface.co/spaces/webml-community/gemma-4-webgpu-kernels/blob/main/index.html)
- byte-vs-tensor progress distinction and phase mapping in the same file
- `Gemma4Mobile.load(..., { onProgress, cache, force, cacheName, fetch, signal, runtimeOptions })` in [`gemma-4-e2b.js`](https://huggingface.co/spaces/webml-community/gemma-4-webgpu-kernels/blob/main/gemma-4-e2b.js)
- `warmup()` in the same bundle, which primes generations at short token counts before interaction
- device capability checks such as `shader-f16`, `subgroups`, `chromium-experimental-subgroup-matrix`, and subgroup min/max size in [`gemma-4-e2b.js`](https://huggingface.co/spaces/webml-community/gemma-4-webgpu-kernels/blob/main/gemma-4-e2b.js)
- `qualityPresets` and hero pause behavior in [`landing.js`](https://huggingface.co/spaces/webml-community/gemma-4-webgpu-kernels/blob/main/landing.js)

## Practical questions and answers
**Is this just a flashy frontend over remote inference?**
No. The source is very explicit that the work happens locally through WebGPU, with local cache reuse, warmup, and device capability reporting.

**What is the most reusable engineering here?**
Three things: the prefix-cache reuse in `generate()`, the honest progress accounting that separates bytes from tensor events, and the capability-gated kernel selection based on subgroup and subgroup-matrix support.

**What should a builder read first?**
Read [`index.html`](https://huggingface.co/spaces/webml-community/gemma-4-webgpu-kernels/blob/main/index.html) first for the UX contract, then jump to `Gemma4Mobile.load`, `generate`, `warmup`, and `deviceInfo` in [`gemma-4-e2b.js`](https://huggingface.co/spaces/webml-community/gemma-4-webgpu-kernels/blob/main/gemma-4-e2b.js), then read [`landing.js`](https://huggingface.co/spaces/webml-community/gemma-4-webgpu-kernels/blob/main/landing.js) for the GPU-budget choices.

**Where is the weak point?**
The runtime is transparent enough to admire but packaged too monolithically to extend comfortably. The huge generated bundle is practical for distribution, but awkward for maintainers or outside contributors.

## What is smart
- Treating browser inference as a full product lifecycle, not just a `generate()` call.
- Reusing prompt prefix cache across turns instead of recomputing everything.
- Surfacing TTFT and decode speed live in the interface.
- Choosing kernels based on actual device features and subgroup capabilities.
- Pausing the decorative WebGL hero when the model needs the GPU.

## What is flawed or weak
- [`README.md`](https://huggingface.co/spaces/webml-community/gemma-4-webgpu-kernels/blob/main/README.md) is nearly empty, so the artifact is much less self-explanatory than it should be.
- The main runtime is packed into one giant generated bundle, which raises the learning and debugging cost.
- The implementation clearly leans into modern browser/WebGPU features, so portability across weaker browsers and devices will always be constrained.
- A lot of the "kernel craftsmanship" is present but not pleasantly explorable because the source is bundled rather than kept as small readable modules.

## What we can learn / steal
- Make load phases explicit when local model startup is heavy.
- Separate UI render cadence from token cadence so the UI does not sabotage decode speed.
- Reuse generation cache aggressively for multi-turn local chat.
- Gate shader strategies on real device capabilities rather than static assumptions.
- Think about total page GPU budget, not only the model kernel itself.

## How we could apply it
If we were building our own browser-side model demo, I would copy this shape:

1. a thin app shell with explicit load phases,
2. a runtime object that owns cache, warmup, and capability reporting,
3. live latency/throughput instrumentation in the UI,
4. feature-gated shader or execution variants,
5. aggressive control of non-model GPU work on the page.

Even if we never touch Gemma, those ideas transfer directly to any serious on-device inference product.

## Bottom line
`gemma-4-webgpu-kernels` is a strong Hugging Face scout because it exposes the hidden work behind "LLM in the browser." The interesting story is not the chat box. It is the combination of cache reuse, capability-aware kernels, honest progress UX, and GPU-budget discipline.

The builder lesson is simple: local inference demos get compelling when they reveal the runtime truths instead of hiding them. This Space does that well enough to be worth studying.
