# Magika

- Repo: [google/magika](https://github.com/google/magika)
- URL: https://github.com/google/magika
- Date: 2026-04-17
- Repo snapshot studied: [`main@0a8cb9626bbf76c2194117d9830b23e9052a1548`](https://github.com/google/magika/tree/0a8cb9626bbf76c2194117d9830b23e9052a1548)
- Why picked today: It is hot, genuinely useful, and not another fake-agent wrapper. Also, it solves a boring-but-important problem with real engineering discipline: fast file-type detection that works at production scale and is portable across Python, Rust, JS, and Go.

## Executive summary

Magika is not trying to understand an entire file. Its core trick is much more pragmatic: sample just the beginning and end of a file, strip surrounding whitespace, run a tiny ONNX model, then apply per-type trust thresholds and fall back to generic `txt` / `unknown` when confidence is not good enough. That is the real product idea.

The repo is strong because it separates the **core detection contract** from the **language surfaces**. The canonical model assets live under [`assets/models/`](https://github.com/google/magika/tree/0a8cb9626bbf76c2194117d9830b23e9052a1548/assets/models), while the implementations in [`python/`](https://github.com/google/magika/tree/0a8cb9626bbf76c2194117d9830b23e9052a1548/python), [`rust/`](https://github.com/google/magika/tree/0a8cb9626bbf76c2194117d9830b23e9052a1548/rust), [`js/`](https://github.com/google/magika/tree/0a8cb9626bbf76c2194117d9830b23e9052a1548/js), and [`go/`](https://github.com/google/magika/tree/0a8cb9626bbf76c2194117d9830b23e9052a1548/go) are mostly adapters around that same detection logic.

The key insight is that Magika behaves less like a giant ML product and more like a **carefully engineered inference kernel with trust policy**. The weakness is that once you look closely, some bindings are more first-class than others. Python and Rust feel mature; Go is explicitly WIP; JS is useful but shaped around browser/TFJS constraints rather than bulk throughput.

## What they built

They built a file-type detection system with several deployable faces:

- a Python package and API centered on [`python/src/magika/magika.py`](https://github.com/google/magika/blob/0a8cb9626bbf76c2194117d9830b23e9052a1548/python/src/magika/magika.py)
- a Rust library centered on [`rust/lib/src/lib.rs`](https://github.com/google/magika/blob/0a8cb9626bbf76c2194117d9830b23e9052a1548/rust/lib/src/lib.rs)
- a high-performance Rust CLI in [`rust/cli/src/main.rs`](https://github.com/google/magika/blob/0a8cb9626bbf76c2194117d9830b23e9052a1548/rust/cli/src/main.rs)
- a JS/TS library around TensorFlow.js in [`js/src/model.ts`](https://github.com/google/magika/blob/0a8cb9626bbf76c2194117d9830b23e9052a1548/js/src/model.ts)
- a Go binding around ONNX Runtime in [`go/magika/scanner.go`](https://github.com/google/magika/blob/0a8cb9626bbf76c2194117d9830b23e9052a1548/go/magika/scanner.go)
- shared assets and model metadata in [`assets/`](https://github.com/google/magika/tree/0a8cb9626bbf76c2194117d9830b23e9052a1548/assets)
- a hefty regression/reference corpus in [`tests_data/`](https://github.com/google/magika/tree/0a8cb9626bbf76c2194117d9830b23e9052a1548/tests_data)

So the repo is really a portable detector platform, not just one library.

## Why it matters

File-type detection sounds mundane until you remember what depends on it: malware scanning, upload routing, parser choice, content-policy pipelines, preview generation, and all the places where extensions and MIME headers lie.

The smart thing here is that Magika is optimized for **routing decisions**, not for perfect semantic understanding. It tries to answer: “what should the rest of the system do with this blob?” That is a very operational framing.

It matters because a lot of software still relies on brittle magic bytes, file extensions, or ad hoc heuristics. Magika says: keep some rule-based shortcuts, but use a tiny model to classify ambiguous stuff fast enough that you can actually deploy it in production.

## Repo shape at a glance

Top-level repo shape:

- [`assets/`](https://github.com/google/magika/tree/0a8cb9626bbf76c2194117d9830b23e9052a1548/assets)
  - model assets, knowledge-base JSON, screenshots, and paper artifacts
  - most important subdir: [`assets/models/`](https://github.com/google/magika/tree/0a8cb9626bbf76c2194117d9830b23e9052a1548/assets/models)
- [`python/`](https://github.com/google/magika/tree/0a8cb9626bbf76c2194117d9830b23e9052a1548/python)
  - Python package, CLI fallback/client glue, packaged model/config assets, tests
  - most important code path: [`python/src/magika/`](https://github.com/google/magika/tree/0a8cb9626bbf76c2194117d9830b23e9052a1548/python/src/magika)
- [`rust/`](https://github.com/google/magika/tree/0a8cb9626bbf76c2194117d9830b23e9052a1548/rust)
  - canonical Rust library and Rust CLI
  - split into [`rust/lib/`](https://github.com/google/magika/tree/0a8cb9626bbf76c2194117d9830b23e9052a1548/rust/lib) and [`rust/cli/`](https://github.com/google/magika/tree/0a8cb9626bbf76c2194117d9830b23e9052a1548/rust/cli)
- [`js/`](https://github.com/google/magika/tree/0a8cb9626bbf76c2194117d9830b23e9052a1548/js)
  - browser/Node package with TFJS-based inference
- [`go/`](https://github.com/google/magika/tree/0a8cb9626bbf76c2194117d9830b23e9052a1548/go)
  - Go binding, ONNX wrapper, example, and sample Docker packaging
- [`tests_data/`](https://github.com/google/magika/tree/0a8cb9626bbf76c2194117d9830b23e9052a1548/tests_data)
  - curated fixtures, miss-detections, feature extraction references, inference references
- [`website/`](https://github.com/google/magika/tree/0a8cb9626bbf76c2194117d9830b23e9052a1548/website) and [`website-ng/`](https://github.com/google/magika/tree/0a8cb9626bbf76c2194117d9830b23e9052a1548/website-ng)
  - docs/demo web surfaces rather than core detection logic
- [`.github/workflows/`](https://github.com/google/magika/tree/0a8cb9626bbf76c2194117d9830b23e9052a1548/.github/workflows)
  - CI/release automation for the multi-language distribution story

Structurally, this is a **hub-and-spokes repo**: shared assets + per-language runtimes + test corpus + docs surfaces.

## Layered architecture dissection

### High-level system shape

The actual system shape is roughly:

1. extract a tiny feature vector from a file or byte stream
2. avoid ML entirely for obvious ruled cases like empty files, directories, symlinks, or trivially small content
3. run an ONNX/TFJS model over the feature vector
4. map the top prediction through thresholds and overwrite/fallback rules
5. return a type enriched with label, description, MIME, group, and extensions

That same pattern shows up across Python, Rust, JS, and Go. The surfaces differ; the conceptual pipeline stays the same.

### Main layers

**1. Shared model assets and metadata**

- [`assets/models/`](https://github.com/google/magika/tree/0a8cb9626bbf76c2194117d9830b23e9052a1548/assets/models)
- [`assets/content_types_kb.min.json`](https://github.com/google/magika/blob/0a8cb9626bbf76c2194117d9830b23e9052a1548/assets/content_types_kb.min.json)
- [`rust/lib/src/model.rs`](https://github.com/google/magika/blob/0a8cb9626bbf76c2194117d9830b23e9052a1548/rust/lib/src/model.rs)

This layer defines the model contract: feature sizes, padding token, thresholds, overwrite map, and label space. It is the real backbone of the project.

**2. Feature extraction layer**

- [`python/src/magika/magika.py`](https://github.com/google/magika/blob/0a8cb9626bbf76c2194117d9830b23e9052a1548/python/src/magika/magika.py)
- [`rust/lib/src/input.rs`](https://github.com/google/magika/blob/0a8cb9626bbf76c2194117d9830b23e9052a1548/rust/lib/src/input.rs)
- [`go/magika/features.go`](https://github.com/google/magika/blob/0a8cb9626bbf76c2194117d9830b23e9052a1548/go/magika/features.go)

This is the mechanical heart: read a bounded block from the beginning and end, strip whitespace, pad to fixed size, flatten into model features. Importantly, inference cost is almost independent of total file size because they refuse to scan the whole thing.

**3. Inference runtime layer**

- [`python/src/magika/magika.py`](https://github.com/google/magika/blob/0a8cb9626bbf76c2194117d9830b23e9052a1548/python/src/magika/magika.py)
- [`rust/lib/src/session.rs`](https://github.com/google/magika/blob/0a8cb9626bbf76c2194117d9830b23e9052a1548/rust/lib/src/session.rs)
- [`js/src/model.ts`](https://github.com/google/magika/blob/0a8cb9626bbf76c2194117d9830b23e9052a1548/js/src/model.ts)
- [`go/onnx/`](https://github.com/google/magika/tree/0a8cb9626bbf76c2194117d9830b23e9052a1548/go/onnx)

Each language hosts the same basic model with a runtime appropriate to that ecosystem: ONNX Runtime for Python/Rust/Go, TensorFlow.js for the browser-friendly JS path.

**4. Policy / output normalization layer**

- [`python/src/magika/magika.py`](https://github.com/google/magika/blob/0a8cb9626bbf76c2194117d9830b23e9052a1548/python/src/magika/magika.py)
- [`go/magika/scanner.go`](https://github.com/google/magika/blob/0a8cb9626bbf76c2194117d9830b23e9052a1548/go/magika/scanner.go)
- [`rust/lib/src/file.rs`](https://github.com/google/magika/blob/0a8cb9626bbf76c2194117d9830b23e9052a1548/rust/lib/src/file.rs)

This is where Magika becomes more trustworthy than a dumb top-1 classifier. Predictions are filtered through confidence thresholds and overwrite rules so the tool can say “generic text” or “unknown binary” instead of hallucinating certainty.

**5. Product surfaces layer**

- [`rust/cli/src/main.rs`](https://github.com/google/magika/blob/0a8cb9626bbf76c2194117d9830b23e9052a1548/rust/cli/src/main.rs)
- [`python/src/magika/cli/`](https://github.com/google/magika/tree/0a8cb9626bbf76c2194117d9830b23e9052a1548/python/src/magika/cli)
- [`js/README.md`](https://github.com/google/magika/blob/0a8cb9626bbf76c2194117d9830b23e9052a1548/js/README.md)
- [`go/cli/`](https://github.com/google/magika/tree/0a8cb9626bbf76c2194117d9830b23e9052a1548/go/cli)

The CLI, package bindings, and browser demo are just deployment skins over the same detection core.

### Request / data / control flow

A practical control flow looks like this:

1. caller provides path, bytes, or stream to [`Magika`](https://github.com/google/magika/blob/0a8cb9626bbf76c2194117d9830b23e9052a1548/python/src/magika/magika.py) or to a [`Session`](https://github.com/google/magika/blob/0a8cb9626bbf76c2194117d9830b23e9052a1548/rust/lib/src/session.rs)
2. feature extraction code in [`python/src/magika/magika.py`](https://github.com/google/magika/blob/0a8cb9626bbf76c2194117d9830b23e9052a1548/python/src/magika/magika.py) or [`rust/lib/src/input.rs`](https://github.com/google/magika/blob/0a8cb9626bbf76c2194117d9830b23e9052a1548/rust/lib/src/input.rs) either:
   - returns an immediate ruled result for empty/small/simple cases, or
   - emits a fixed-length feature vector
3. inference runtime executes the model
4. post-processing applies thresholds and overwrite map from [`rust/lib/src/model.rs`](https://github.com/google/magika/blob/0a8cb9626bbf76c2194117d9830b23e9052a1548/rust/lib/src/model.rs) / packaged JSON config
5. caller receives a normalized content-type result with metadata

In the CLI, [`rust/cli/src/main.rs`](https://github.com/google/magika/blob/0a8cb9626bbf76c2194117d9830b23e9052a1548/rust/cli/src/main.rs) adds one more layer: parallel feature extraction, batched inference, result reordering, and formatted output.

## Key directories and files

The concrete source paths that matter most:

- [`README.md`](https://github.com/google/magika/blob/0a8cb9626bbf76c2194117d9830b23e9052a1548/README.md)
  - product promise, deployment surfaces, and operating assumptions
- [`python/src/magika/magika.py`](https://github.com/google/magika/blob/0a8cb9626bbf76c2194117d9830b23e9052a1548/python/src/magika/magika.py)
  - easiest place to understand the end-to-end detection pipeline
- [`rust/lib/src/input.rs`](https://github.com/google/magika/blob/0a8cb9626bbf76c2194117d9830b23e9052a1548/rust/lib/src/input.rs)
  - clearest feature extraction implementation
- [`rust/lib/src/model.rs`](https://github.com/google/magika/blob/0a8cb9626bbf76c2194117d9830b23e9052a1548/rust/lib/src/model.rs)
  - generated model config, thresholds, overwrite map, label space
- [`rust/lib/src/lib.rs`](https://github.com/google/magika/blob/0a8cb9626bbf76c2194117d9830b23e9052a1548/rust/lib/src/lib.rs)
  - public library surface and reference tests against the shared corpus
- [`rust/cli/src/main.rs`](https://github.com/google/magika/blob/0a8cb9626bbf76c2194117d9830b23e9052a1548/rust/cli/src/main.rs)
  - where the scalable CLI behavior lives
- [`go/magika/scanner.go`](https://github.com/google/magika/blob/0a8cb9626bbf76c2194117d9830b23e9052a1548/go/magika/scanner.go)
  - useful for seeing the distilled scanner contract
- [`js/src/model.ts`](https://github.com/google/magika/blob/0a8cb9626bbf76c2194117d9830b23e9052a1548/js/src/model.ts)
  - browser/Node inference path
- [`tests_data/reference/`](https://github.com/google/magika/tree/0a8cb9626bbf76c2194117d9830b23e9052a1548/tests_data/reference)
  - regression truth for features and inference

## Important components

### `Magika` (Python)

- [`python/src/magika/magika.py`](https://github.com/google/magika/blob/0a8cb9626bbf76c2194117d9830b23e9052a1548/python/src/magika/magika.py)

This is the best “spec by implementation” in the repo. It shows initialization, config loading, feature extraction, batch inference, confidence handling, and result shaping in one place.

### `FeaturesOrRuled` and feature extraction

- [`rust/lib/src/input.rs`](https://github.com/google/magika/blob/0a8cb9626bbf76c2194117d9830b23e9052a1548/rust/lib/src/input.rs)

This is the most elegant component in the repo. The library explicitly distinguishes between content that can be decided by rules immediately and content that deserves model inference. That keeps the ML path honest and cheap.

### Generated model config

- [`rust/lib/src/model.rs`](https://github.com/google/magika/blob/0a8cb9626bbf76c2194117d9830b23e9052a1548/rust/lib/src/model.rs)

This file matters because it exposes the non-mystical part of the model product: thresholds, overwrite map, label count, and the actual feature sizes. It demystifies the system.

### Rust CLI batching pipeline

- [`rust/cli/src/main.rs`](https://github.com/google/magika/blob/0a8cb9626bbf76c2194117d9830b23e9052a1548/rust/cli/src/main.rs)

This is where the repo graduates from “cool model demo” to “usable ops tool.” It parallelizes extraction, batches inference, and reorders results so the CLI can chew through lots of files without becoming sloppy.

### Go `Scanner`

- [`go/magika/scanner.go`](https://github.com/google/magika/blob/0a8cb9626bbf76c2194117d9830b23e9052a1548/go/magika/scanner.go)

This file is useful because it compresses the whole idea into a tiny API: extract features, maybe skip ML, run ONNX, apply thresholds, return content type.

## Important knobs / configs / extension points

A few knobs that actually matter:

- prediction mode in [`python/src/magika/types/prediction_mode.py`](https://github.com/google/magika/blob/0a8cb9626bbf76c2194117d9830b23e9052a1548/python/src/magika/types/prediction_mode.py)
  - `high-confidence`, `medium-confidence`, `best-guess`
- model config and thresholds in [`rust/lib/src/model.rs`](https://github.com/google/magika/blob/0a8cb9626bbf76c2194117d9830b23e9052a1548/rust/lib/src/model.rs)
  - `beg_size`, `end_size`, `min_file_size_for_dl`, `padding_token`, threshold table, overwrite map
- content-type knowledge base in [`assets/content_types_kb.min.json`](https://github.com/google/magika/blob/0a8cb9626bbf76c2194117d9830b23e9052a1548/assets/content_types_kb.min.json)
  - label metadata, MIME, extensions, grouping
- CLI throughput knobs in [`rust/cli/src/main.rs`](https://github.com/google/magika/blob/0a8cb9626bbf76c2194117d9830b23e9052a1548/rust/cli/src/main.rs)
  - batch size, number of tasks, ONNX threading, optimization level
- alternate models/assets in [`assets/models/`](https://github.com/google/magika/tree/0a8cb9626bbf76c2194117d9830b23e9052a1548/assets/models)
  - obvious extension point for future model versions

The design lesson: they expose knobs mostly around **trust and runtime behavior**, not endless product fluff.

## Practical questions and answers

### What is the real technical trick here?

Not “AI for files” in the abstract. The trick is the bounded feature extraction: sample a tiny, fixed-size slice from the start and end, normalize it, and classify that. Cheap enough to use everywhere, rich enough to beat dumb signatures on many file types.

### Is this actually ML-heavy?

Less than the README vibe suggests. It uses ML, yes, but the repo’s real sophistication is in the feature extraction and output policy. The model is small; the surrounding engineering is what makes it production-credible.

### Why the fallback to generic `txt` / `unknown` matters?

Because false confidence is worse than useful ambiguity in routing systems. The threshold logic in [`python/src/magika/magika.py`](https://github.com/google/magika/blob/0a8cb9626bbf76c2194117d9830b23e9052a1548/python/src/magika/magika.py) and [`go/magika/scanner.go`](https://github.com/google/magika/blob/0a8cb9626bbf76c2194117d9830b23e9052a1548/go/magika/scanner.go) is one of the healthiest choices in the repo.

### Which implementation feels most canonical?

For understanding: Python.

For operational polish: Rust.

The Python file is easier to read as a conceptual spec. The Rust CLI and library feel more engineered for serious deployment and distribution.

### What are the sharp edges?

- binding parity is uneven
- JS uses TFJS, which is practical for the web demo but not the same operational story as ONNX Runtime
- the small-feature approach will always have edge cases for adversarial or heavily ambiguous formats
- the repo depends on maintaining synchronized semantics across several languages, which is always harder than it looks

## What is smart

A few things are genuinely smart here:

- **Bounded feature extraction instead of whole-file scanning.** This is the main systems win.
- **Rules first, ML second.** Empty files, directories, symlinks, and tiny files avoid unnecessary inference.
- **Per-label thresholds.** Different types deserve different trust bars.
- **Generic fallback outputs.** Better to return useful uncertainty than fake precision.
- **Shared test/reference corpus.** [`tests_data/reference/`](https://github.com/google/magika/tree/0a8cb9626bbf76c2194117d9830b23e9052a1548/tests_data/reference) makes cross-language consistency much more believable.
- **Multi-language architecture without pretending every port is magical.** The repo is fairly explicit about what is mature and what is WIP.

## What is flawed or weak

The weak spots are also visible:

- **Repo sprawl.** Multi-language repos age badly unless maintainers are disciplined.
- **Asymmetric maturity.** Python + Rust carry the weight; some other surfaces feel secondary.
- **Model/config generation path is maintainable but not cozy.** Generated files like [`rust/lib/src/model.rs`](https://github.com/google/magika/blob/0a8cb9626bbf76c2194117d9830b23e9052a1548/rust/lib/src/model.rs) are useful, but editing/extending the system is clearly a maintainer workflow, not a casual contributor workflow.
- **The “AI-powered” framing is a bit louder than the repo’s true beauty.** The elegant part is not generic AI branding; it is disciplined feature engineering plus conservative output policy.

## What we can learn / steal

Things worth stealing:

- build ML products around a **tight systems contract**, not vague intelligence claims
- keep inference cheap by constraining the input representation aggressively
- separate **feature extraction**, **inference**, and **trust policy** into clear layers
- use fallback classes when confidence is low instead of forcing a top-1 label
- back multi-language ports with a shared reference corpus so parity is testable
- treat CLI throughput and batching as first-class engineering, not an afterthought

## How we could apply it

If we were building our own classifier or routing tool, the reusable pattern is:

1. define the smallest input slice that still carries enough signal
2. use rules for obvious cases
3. reserve model inference for the genuinely ambiguous middle
4. add confidence-aware fallback classes
5. make cross-language compatibility a product feature, backed by shared fixtures

This pattern would transfer well beyond file typing: MIME normalization, document routing, lightweight malware triage, upload preprocessing, even some content moderation pre-routing.

## Bottom line

`google/magika` is worth studying because it is a rare AI repo whose best idea is not hype but restraint.

It does not try to read everything. It reads just enough. Then it refuses to overclaim when confidence is weak.

That combination — **small features, fast inference, conservative outputs** — is the real builder lesson here. The repo’s deepest insight is that trust policy is part of the model, not an afterthought glued on after inference.