# Supertonic

- Repo: `supertone-inc/supertonic`
- URL: https://github.com/supertone-inc/supertonic
- Date: 2026-05-15
- Repo snapshot studied: `main` @ `0a98c9f127ac7c9979228a12c0c25d71204a447e`
- Why picked today: It was high on GitHub trending, AI-related in a real product sense, and unlike a lot of flashy voice repos it is shipping a concrete on-device inference surface across Python, Node, Web, Rust, Swift, Go, Java, C++, C#, Flutter, and iOS.

## Executive summary
Supertonic is a multilingual, on-device text-to-speech stack packaged around ONNX Runtime. The repo’s central move is not inventing a giant application, it is making one TTS model family feel portable everywhere.

The interesting thing here is that this is less a “core model training repo” and more an aggressively cross-platform inference-distribution repo. The actual learned weights live outside the repo in Hugging Face assets, while this repository focuses on inference wrappers, text preprocessing, style loading, denoising loops, WAV output, and platform-specific runtime glue.

My short verdict: the model story may be the headline, but the real engineering lesson is the disciplined replication of one inference contract across a wide surface area.

## What they built
They built a local-first TTS delivery layer with three practical pieces:

1. a shared ONNX model contract in `assets/onnx` and `assets/voice_styles` described in the root [`README.md`](https://github.com/supertone-inc/supertonic/blob/0a98c9f127ac7c9979228a12c0c25d71204a447e/README.md)
2. per-language runtimes that all load the same model family and voice-style JSONs, like [`py/helper.py`](https://github.com/supertone-inc/supertonic/blob/0a98c9f127ac7c9979228a12c0c25d71204a447e/py/helper.py), [`nodejs/helper.js`](https://github.com/supertone-inc/supertonic/blob/0a98c9f127ac7c9979228a12c0c25d71204a447e/nodejs/helper.js), and [`rust/src/helper.rs`](https://github.com/supertone-inc/supertonic/blob/0a98c9f127ac7c9979228a12c0c25d71204a447e/rust/src/helper.rs)
3. UI and app examples that prove the same stack can run in the browser and on Apple platforms, especially [`web/main.js`](https://github.com/supertone-inc/supertonic/blob/0a98c9f127ac7c9979228a12c0c25d71204a447e/web/main.js) and [`ios/ExampleiOSApp/TTSService.swift`](https://github.com/supertone-inc/supertonic/blob/0a98c9f127ac7c9979228a12c0c25d71204a447e/ios/ExampleiOSApp/TTSService.swift)

This is basically a portability product masquerading as a model release.

## Why it matters
A lot of open TTS projects say “local,” but still feel like Python demos. Supertonic is more ambitious. It treats local inference as a deployment problem: same assets, same style concept, same rough synthesis pipeline, many runtimes.

That matters because the hard part for many teams is not just model quality. It is turning a model into a reusable edge component that can survive real product surfaces.

## Repo shape at a glance
Top-level shape:

- [`py/`](https://github.com/supertone-inc/supertonic/tree/0a98c9f127ac7c9979228a12c0c25d71204a447e/py): Python examples and helper implementation, including the most readable reference logic.
- [`nodejs/`](https://github.com/supertone-inc/supertonic/tree/0a98c9f127ac7c9979228a12c0c25d71204a447e/nodejs): Node wrapper around ONNX Runtime Node.
- [`web/`](https://github.com/supertone-inc/supertonic/tree/0a98c9f127ac7c9979228a12c0c25d71204a447e/web): browser demo using `onnxruntime-web`, with WebGPU fallback to WASM.
- [`rust/`](https://github.com/supertone-inc/supertonic/tree/0a98c9f127ac7c9979228a12c0c25d71204a447e/rust): Rust port of the helper pipeline.
- [`swift/`](https://github.com/supertone-inc/supertonic/tree/0a98c9f127ac7c9979228a12c0c25d71204a447e/swift) and [`ios/`](https://github.com/supertone-inc/supertonic/tree/0a98c9f127ac7c9979228a12c0c25d71204a447e/ios): Apple-platform packaging and an example app.
- [`go/`](https://github.com/supertone-inc/supertonic/tree/0a98c9f127ac7c9979228a12c0c25d71204a447e/go), [`java/`](https://github.com/supertone-inc/supertonic/tree/0a98c9f127ac7c9979228a12c0c25d71204a447e/java), [`cpp/`](https://github.com/supertone-inc/supertonic/tree/0a98c9f127ac7c9979228a12c0c25d71204a447e/cpp), [`csharp/`](https://github.com/supertone-inc/supertonic/tree/0a98c9f127ac7c9979228a12c0c25d71204a447e/csharp), and [`flutter/`](https://github.com/supertone-inc/supertonic/tree/0a98c9f127ac7c9979228a12c0c25d71204a447e/flutter): parallel SDK/demo surfaces.
- [`img/`](https://github.com/supertone-inc/supertonic/tree/0a98c9f127ac7c9979228a12c0c25d71204a447e/img): performance charts and marketing assets.
- [`test_all.sh`](https://github.com/supertone-inc/supertonic/blob/0a98c9f127ac7c9979228a12c0c25d71204a447e/test_all.sh): useful map of what the maintainers consider the supported cross-runtime matrix.

That shape tells the truth of the repo quickly: this is a runtime-portability matrix more than a single-language codebase.

## Layered architecture dissection
### High-level system shape
The system shape is simple in concept:

- normalize text
- map text into indexed unicode IDs with language tags
- load voice-style tensors
- predict duration and encode text
- run iterative denoising in latent space
- vocode the latent into waveform
- trim output and write WAV

The repo repeats that same inference skeleton in multiple ecosystems.

### Main layers
**1. Asset contract layer**
- Root setup in [`README.md`](https://github.com/supertone-inc/supertonic/blob/0a98c9f127ac7c9979228a12c0c25d71204a447e/README.md)
- Python package metadata in [`py/pyproject.toml`](https://github.com/supertone-inc/supertonic/blob/0a98c9f127ac7c9979228a12c0c25d71204a447e/py/pyproject.toml)

Everything revolves around a fixed asset layout: ONNX graphs, a `tts.json` config, a unicode indexer, and voice-style JSON blobs. The repo assumes the model is already exported and focuses on making those artifacts consumable everywhere.

**2. Text normalization and tokenization layer**
- Python reference in [`py/helper.py`](https://github.com/supertone-inc/supertonic/blob/0a98c9f127ac7c9979228a12c0c25d71204a447e/py/helper.py)
- Node equivalent in [`nodejs/helper.js`](https://github.com/supertone-inc/supertonic/blob/0a98c9f127ac7c9979228a12c0c25d71204a447e/nodejs/helper.js)
- Rust equivalent in [`rust/src/helper.rs`](https://github.com/supertone-inc/supertonic/blob/0a98c9f127ac7c9979228a12c0c25d71204a447e/rust/src/helper.rs)

This layer does Unicode normalization, emoji stripping, punctuation cleanup, expression replacement, language validation, and wraps text in `<lang>...</lang>` tags before indexing characters.

That is a notable design choice. They are not doing a heavyweight text frontend here. They are standardizing a pragmatic unicode-to-index preprocessing contract across runtimes.

**3. Inference orchestration layer**
- [`py/helper.py`](https://github.com/supertone-inc/supertonic/blob/0a98c9f127ac7c9979228a12c0c25d71204a447e/py/helper.py)
- [`nodejs/helper.js`](https://github.com/supertone-inc/supertonic/blob/0a98c9f127ac7c9979228a12c0c25d71204a447e/nodejs/helper.js)
- [`rust/src/helper.rs`](https://github.com/supertone-inc/supertonic/blob/0a98c9f127ac7c9979228a12c0c25d71204a447e/rust/src/helper.rs)

This is the heart of the repo. The pipeline predicts duration, encodes text, samples noisy latent tensors, iteratively denoises over `total_step`, and finally calls the vocoder. The architecture is closer to “portable inference graph runner” than “SDK with deep abstraction barriers.”

**4. Platform adapter layer**
- Browser app in [`web/main.js`](https://github.com/supertone-inc/supertonic/blob/0a98c9f127ac7c9979228a12c0c25d71204a447e/web/main.js)
- iOS adapter in [`ios/ExampleiOSApp/TTSService.swift`](https://github.com/supertone-inc/supertonic/blob/0a98c9f127ac7c9979228a12c0c25d71204a447e/ios/ExampleiOSApp/TTSService.swift)
- Example entrypoints like [`py/example_onnx.py`](https://github.com/supertone-inc/supertonic/blob/0a98c9f127ac7c9979228a12c0c25d71204a447e/py/example_onnx.py), [`nodejs/example_onnx.js`](https://github.com/supertone-inc/supertonic/blob/0a98c9f127ac7c9979228a12c0c25d71204a447e/nodejs/example_onnx.js), and [`rust/src/example_onnx.rs`](https://github.com/supertone-inc/supertonic/blob/0a98c9f127ac7c9979228a12c0c25d71204a447e/rust/src/example_onnx.rs)

Each runtime has thin glue for session creation, tensor marshalling, file paths, and audio writing, but the conceptual contract stays stable.

**5. Validation and support layer**
- [`test_all.sh`](https://github.com/supertone-inc/supertonic/blob/0a98c9f127ac7c9979228a12c0c25d71204a447e/test_all.sh)

This script matters because it shows the repo is not only publishing sample snippets. It is attempting to keep the language matrix testable, including batch and long-form inference modes.

### Request / data / control flow
A practical flow looks like this:

1. A caller picks text, language, and a voice-style JSON.
2. The runtime loads `tts.json`, the unicode indexer, and ONNX models from `assets/onnx`.
3. The text processor normalizes text and turns characters into indexed IDs with a text mask.
4. The duration predictor estimates timing, then the text encoder produces embeddings.
5. The runtime samples a masked noisy latent and iteratively denoises it for `total_step` iterations.
6. The vocoder converts the final latent to waveform samples.
7. The app trims by predicted duration, writes a WAV, and optionally displays or plays it.

The nice thing is that this same mental model holds in Python, Node, Web, Rust, and Swift.

## Key directories and files
- [`README.md`](https://github.com/supertone-inc/supertonic/blob/0a98c9f127ac7c9979228a12c0c25d71204a447e/README.md): the clearest map of supported platforms and asset expectations.
- [`py/helper.py`](https://github.com/supertone-inc/supertonic/blob/0a98c9f127ac7c9979228a12c0c25d71204a447e/py/helper.py): best single-file reference for the synthesis pipeline.
- [`nodejs/helper.js`](https://github.com/supertone-inc/supertonic/blob/0a98c9f127ac7c9979228a12c0c25d71204a447e/nodejs/helper.js): useful because it exposes the cost of tensor marshalling and JS portability work.
- [`web/helper.js`](https://github.com/supertone-inc/supertonic/blob/0a98c9f127ac7c9979228a12c0c25d71204a447e/web/helper.js): the browser-specific inference core.
- [`web/main.js`](https://github.com/supertone-inc/supertonic/blob/0a98c9f127ac7c9979228a12c0c25d71204a447e/web/main.js): shows product-minded deployment choices like WebGPU-first with WASM fallback.
- [`rust/src/helper.rs`](https://github.com/supertone-inc/supertonic/blob/0a98c9f127ac7c9979228a12c0c25d71204a447e/rust/src/helper.rs): a strongly typed restatement of the same core pipeline.
- [`ios/ExampleiOSApp/TTSService.swift`](https://github.com/supertone-inc/supertonic/blob/0a98c9f127ac7c9979228a12c0c25d71204a447e/ios/ExampleiOSApp/TTSService.swift): shows how the repo packages model assets into a mobile app boundary.
- [`test_all.sh`](https://github.com/supertone-inc/supertonic/blob/0a98c9f127ac7c9979228a12c0c25d71204a447e/test_all.sh): the most honest map of operational ambition.

## Important components
- **`UnicodeProcessor`** in [`py/helper.py`](https://github.com/supertone-inc/supertonic/blob/0a98c9f127ac7c9979228a12c0c25d71204a447e/py/helper.py), [`nodejs/helper.js`](https://github.com/supertone-inc/supertonic/blob/0a98c9f127ac7c9979228a12c0c25d71204a447e/nodejs/helper.js), and [`rust/src/helper.rs`](https://github.com/supertone-inc/supertonic/blob/0a98c9f127ac7c9979228a12c0c25d71204a447e/rust/src/helper.rs), which keeps the input contract aligned across languages.
- **`TextToSpeech`** in those same helper files, which owns duration prediction, denoising iteration, and vocoder calls.
- **Voice-style loading** across helpers, because style JSON is the user-facing control surface for voice identity.
- **Browser runtime selection** in [`web/main.js`](https://github.com/supertone-inc/supertonic/blob/0a98c9f127ac7c9979228a12c0c25d71204a447e/web/main.js), which tries WebGPU first and falls back to WASM.
- **Bundle resource discovery** in [`ios/ExampleiOSApp/TTSService.swift`](https://github.com/supertone-inc/supertonic/blob/0a98c9f127ac7c9979228a12c0c25d71204a447e/ios/ExampleiOSApp/TTSService.swift), which is exactly the sort of boring but necessary code edge deployments live or die on.

## Important knobs / configs / extension points
- `total_step` controls denoising iterations in helpers like [`py/helper.py`](https://github.com/supertone-inc/supertonic/blob/0a98c9f127ac7c9979228a12c0c25d71204a447e/py/helper.py) and the browser UI in [`web/main.js`](https://github.com/supertone-inc/supertonic/blob/0a98c9f127ac7c9979228a12c0c25d71204a447e/web/main.js).
- `speed` is exposed as a practical duration knob in the same inference path.
- `AVAILABLE_LANGS` in the helpers defines the supported multilingual surface.
- Voice-style JSON files under `assets/voice_styles` are the primary extension point for speaker/style selection, as described in the root [`README.md`](https://github.com/supertone-inc/supertonic/blob/0a98c9f127ac7c9979228a12c0c25d71204a447e/README.md).
- Execution providers in [`web/main.js`](https://github.com/supertone-inc/supertonic/blob/0a98c9f127ac7c9979228a12c0c25d71204a447e/web/main.js) are a deployment knob, especially WebGPU versus WASM.

## Practical questions and answers
### Is this a model-training repo?
Not really. It is mainly an inference and distribution repo. The training story is mostly offstage; the repo expects exported ONNX artifacts and voice-style assets.

### Where is the center of gravity?
The center of gravity is the helper implementations, especially [`py/helper.py`](https://github.com/supertone-inc/supertonic/blob/0a98c9f127ac7c9979228a12c0c25d71204a447e/py/helper.py), plus the browser and mobile packaging paths.

### What is the smartest design choice?
Keeping one portable inference contract and re-implementing it consistently across runtimes, instead of making each platform a one-off demo.

### What would fail first in production?
Asset packaging and runtime drift. When the real model lives outside the repo and every platform has its own wrapper, the risk is not just model quality. It is keeping configs, tensor shapes, voice-style formats, and platform-specific runtime expectations in sync.

### Is the browser path a gimmick?
No. The browser path in [`web/main.js`](https://github.com/supertone-inc/supertonic/blob/0a98c9f127ac7c9979228a12c0c25d71204a447e/web/main.js) is one of the repo’s most practical ideas because it treats local inference as something users can actually touch immediately.

## What is smart
- The repo understands that deployment breadth is a product feature.
- The core preprocessing and inference logic is deliberately mirrored across languages.
- WebGPU-first with WASM fallback is exactly the right posture for browser inference right now.
- The iOS bundle lookup code shows real respect for app-shipping constraints.
- [`test_all.sh`](https://github.com/supertone-inc/supertonic/blob/0a98c9f127ac7c9979228a12c0c25d71204a447e/test_all.sh) is a strong sign that the maintainers know cross-platform promises rot unless you keep exercising them.

## What is flawed or weak
- The repo’s most valuable asset, the actual model weights, lives elsewhere. That makes the GitHub repository look more complete than it really is by itself.
- There is obvious code duplication across Python, Node, Web, and Rust helpers. That is understandable, but it creates drift risk.
- The text frontend is intentionally simple. That keeps portability high, but it probably leaves reading-quality edge cases on the table compared with language-specific normalization stacks.
- The repo is much better at inference portability than at explaining the model internals. If you want to understand the architecture of the TTS model itself, this repo is not the full story.

## What we can learn / steal
- Treat model export format plus asset layout as a product contract.
- Pick one inference pipeline and replicate it faithfully instead of hand-waving parity across SDKs.
- Make browser inference a first-class demo path, not an afterthought.
- Invest in the boring adapter layer, because that is what turns “research artifact” into “something a product can embed.”
- Add cross-runtime validation scripts early if you are going to claim many platforms.

## How we could apply it
If we were borrowing from this repo, I would copy the packaging mindset:

- define one canonical model-asset contract
- keep a reference implementation in the clearest language
- port that contract to the few runtimes that matter most
- expose only a handful of high-value knobs like language, style, speed, and denoising steps
- ship a browser demo to collapse evaluation friction

The larger lesson is that edge AI products often win on portability and integration quality, not just raw model novelty.

## Bottom line
Supertonic is not most interesting as a mysterious TTS model. It is most interesting as a disciplined attempt to make a local TTS model usable everywhere.

The key insight is that the repo’s real architecture is a cross-platform inference contract: shared assets, repeated helper logic, thin platform adapters, and enough test scaffolding to keep the portability promise honest.

That is worth studying, and worth stealing.