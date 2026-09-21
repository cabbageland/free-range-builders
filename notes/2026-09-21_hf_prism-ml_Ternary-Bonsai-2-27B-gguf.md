# Ternary-Bonsai-2-27B GGUF

- Source: Hugging Face
- Artifact: model
- URL: https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf
- Date: 2026-09-21
- Snapshot studied: Hugging Face revision `6ed5e12bf84b7a63069882c91dd9e9218647d17b`; linked demo repo `PrismML-Eng/Bonsai-demo` at `23da1365df0364ef9e98d1cd18db6b0c06295751`
- Why picked today: It was at the top of Hugging Face trending, with an unusually inspectable artifact: model card, GGUF metadata, quantized files, multimodal projector files, custom runtime requirements, benchmark claims, and a linked demo repo with setup scripts and format guidance.

## Executive summary

[prism-ml/Ternary-Bonsai-2-27B-gguf](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf) is a GGUF release of a Qwen3.8-27B-derived reasoning model whose language weights are stored in a ternary representation. The card in [README.md](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf/blob/6ed5e12bf84b7a63069882c91dd9e9218647d17b/README.md) claims a 27B-class model can run locally with a roughly 5.95 GB `PTQ1_0` packing or a 7.21 GB `PQ2_0` packing, plus optional vision projector files.

The interesting part is not just low-bit quantization. The artifact is opinionated all the way down: custom GGUF tensor types, a rotated weight basis, Hadamard activation transforms, a special llama.cpp fork, backend-specific pack choices, model metadata carrying the chat template and sampling defaults, and a linked source repo, [PrismML-Eng/Bonsai-demo](https://github.com/PrismML-Eng/Bonsai-demo/tree/23da1365df0364ef9e98d1cd18db6b0c06295751), that is effectively the runtime manual. This is a good example of a model release that is really a coupled model-plus-runtime product.

## What they built / released

The Hugging Face repo ships these visible files:

- [README.md](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf/blob/6ed5e12bf84b7a63069882c91dd9e9218647d17b/README.md), the model card and operating manual.
- [Ternary-Bonsai-2-27B-F16.gguf](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf/blob/6ed5e12bf84b7a63069882c91dd9e9218647d17b/Ternary-Bonsai-2-27B-F16.gguf), the high-precision reference artifact.
- [Ternary-Bonsai-2-27B-PTQ1_0.gguf](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf/blob/6ed5e12bf84b7a63069882c91dd9e9218647d17b/Ternary-Bonsai-2-27B-PTQ1_0.gguf), the dense-trit ternary packing.
- [Ternary-Bonsai-2-27B-PQ2_0.gguf](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf/blob/6ed5e12bf84b7a63069882c91dd9e9218647d17b/Ternary-Bonsai-2-27B-PQ2_0.gguf), the 2-bit-slot packing that the demo repo downloads by default.
- [Ternary-Bonsai-2-27B-mmproj-Q8_0.gguf](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf/blob/6ed5e12bf84b7a63069882c91dd9e9218647d17b/Ternary-Bonsai-2-27B-mmproj-Q8_0.gguf), the optional vision projector for image input.
- [Ternary-Bonsai-2-27B-mmproj-BF16.gguf](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf/blob/6ed5e12bf84b7a63069882c91dd9e9218647d17b/Ternary-Bonsai-2-27B-mmproj-BF16.gguf), the BF16 projector reference.
- [assets/bonsai-logo.svg](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf/blob/6ed5e12bf84b7a63069882c91dd9e9218647d17b/assets/bonsai-logo.svg), plus [LICENSE](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf/blob/6ed5e12bf84b7a63069882c91dd9e9218647d17b/LICENSE) and [NOTICE.txt](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf/blob/6ed5e12bf84b7a63069882c91dd9e9218647d17b/NOTICE.txt).

The API metadata reports `library_name: llama.cpp`, `pipeline_tag: text-generation`, base model `Qwen/Qwen3.8-27B`, GGUF architecture `qwen35`, context length `262144`, and a total file size around 53.8 GB for the repo's GGUF files. It also exposes a long chat template with support for system/user/assistant/tool messages, optional vision content markers, and `enable_thinking` / `reasoning_effort` behavior.

## Why it matters

Local 27B-class inference is mostly a memory-bandwidth and footprint problem. The model card's useful claim is that a reasoning-capable 27B model can be squeezed into a laptop-sized footprint without the characteristic collapse of ordinary extreme low-bit quantization. Whether every benchmark claim holds is a separate question; the important builder lesson is the shape of the release.

This artifact does not pretend the model file is self-sufficient. [README.md](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf/blob/6ed5e12bf84b7a63069882c91dd9e9218647d17b/README.md) repeatedly says stock llama.cpp cannot run these files correctly. [MODEL-FORMATS.md](https://github.com/PrismML-Eng/Bonsai-demo/blob/23da1365df0364ef9e98d1cd18db6b0c06295751/MODEL-FORMATS.md) explains why: Bonsai 2 stores weights in a rotated basis and needs an activation transform that the demo's llama.cpp binaries carry. A model release that requires custom kernels is a distribution system, not just a checkpoint upload.

## Artifact shape at a glance

- The Hugging Face [model card](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf/blob/6ed5e12bf84b7a63069882c91dd9e9218647d17b/README.md) is both marketing and operational documentation: it lists packings, benchmark tables, backend caveats, sampling defaults, and quickstart commands.
- The two runtime packings, [PTQ1_0](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf/blob/6ed5e12bf84b7a63069882c91dd9e9218647d17b/Ternary-Bonsai-2-27B-PTQ1_0.gguf) and [PQ2_0](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf/blob/6ed5e12bf84b7a63069882c91dd9e9218647d17b/Ternary-Bonsai-2-27B-PQ2_0.gguf), are the real product files.
- The optional multimodal layer is split into [mmproj Q8_0](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf/blob/6ed5e12bf84b7a63069882c91dd9e9218647d17b/Ternary-Bonsai-2-27B-mmproj-Q8_0.gguf) and [mmproj BF16](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf/blob/6ed5e12bf84b7a63069882c91dd9e9218647d17b/Ternary-Bonsai-2-27B-mmproj-BF16.gguf) files instead of being always resident.
- The linked runtime repo [PrismML-Eng/Bonsai-demo](https://github.com/PrismML-Eng/Bonsai-demo/tree/23da1365df0364ef9e98d1cd18db6b0c06295751) supplies setup, downloads, backend selection, server launchers, Open WebUI integration, tool demos, vision docs, and community benchmark templates.
- The demo repo's [scripts/download_models.sh](https://github.com/PrismML-Eng/Bonsai-demo/blob/23da1365df0364ef9e98d1cd18db6b0c06295751/scripts/download_models.sh) filters Hugging Face downloads so users do not accidentally pull every quant.
- The demo repo's [scripts/run_llama.sh](https://github.com/PrismML-Eng/Bonsai-demo/blob/23da1365df0364ef9e98d1cd18db6b0c06295751/scripts/run_llama.sh) selects a fork binary, selects the appropriate GGUF file, sets GPU layer offload, context, flash attention, and model-specific sampling flags.

## Layered architecture dissection

### High-level system shape

This release has four layers. The base model layer is Qwen3.8-27B's hybrid-attention causal architecture. The representation layer transforms language weights into ternary groups with per-group scales and a rotated basis. The file layer packages those weights into custom GGUF bands plus optional projector files. The runtime layer uses a PrismML llama.cpp fork or MLX companion support to apply the needed activation transforms and custom kernels.

That stack is visible across both sources. The Hugging Face [README.md](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf/blob/6ed5e12bf84b7a63069882c91dd9e9218647d17b/README.md) documents the model, packings, benchmark claims, and user-facing commands. The demo repo [README.md](https://github.com/PrismML-Eng/Bonsai-demo/blob/23da1365df0364ef9e98d1cd18db6b0c06295751/README.md) makes Bonsai 2 the default local model. [MODEL-FORMATS.md](https://github.com/PrismML-Eng/Bonsai-demo/blob/23da1365df0364ef9e98d1cd18db6b0c06295751/MODEL-FORMATS.md) explains format compatibility and failure modes.

### Main layers

The model layer is a 27.36B-parameter system derived from Qwen3.8-27B according to [README.md](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf/blob/6ed5e12bf84b7a63069882c91dd9e9218647d17b/README.md). It keeps the hybrid-attention backbone and a 262K token context. The card separates language backbone, embedding/LM head, and vision tower, which matters because only the language model must stay resident for text inference.

The representation layer is "ternary g128": values in `{-1, 0, +1}` with one FP16 scale per group of 128 weights. The card says the weights are stored in a blockwise Hadamard-rotated basis and that the runtime applies the matching transform to activations. This is the core reason the model cannot be treated like an ordinary GGUF quant.

The artifact layer ships multiple bands. [PTQ1_0](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf/blob/6ed5e12bf84b7a63069882c91dd9e9218647d17b/Ternary-Bonsai-2-27B-PTQ1_0.gguf) packs trits densely for the smallest footprint. [PQ2_0](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf/blob/6ed5e12bf84b7a63069882c91dd9e9218647d17b/Ternary-Bonsai-2-27B-PQ2_0.gguf) stores each trit in a 2-bit slot, trading memory for easier unpacking and faster prompt processing on many backends. [MODEL-FORMATS.md](https://github.com/PrismML-Eng/Bonsai-demo/blob/23da1365df0364ef9e98d1cd18db6b0c06295751/MODEL-FORMATS.md) says there is no mainline-compatible Bonsai 2 band yet.

The runtime layer lives in the linked demo repo. [scripts/download_models.sh](https://github.com/PrismML-Eng/Bonsai-demo/blob/23da1365df0364ef9e98d1cd18db6b0c06295751/scripts/download_models.sh) chooses `PQ2_0` plus the Q8 projector by default for Bonsai 2. [scripts/run_llama.sh](https://github.com/PrismML-Eng/Bonsai-demo/blob/23da1365df0364ef9e98d1cd18db6b0c06295751/scripts/run_llama.sh) finds the forked `llama-cli`, selects a model based on backend, sets `-fa on`, and applies the model's recommended sampling flags.

### Inference / data / control flow

A user running the official path starts in [Bonsai-demo README.md](https://github.com/PrismML-Eng/Bonsai-demo/blob/23da1365df0364ef9e98d1cd18db6b0c06295751/README.md): clone the demo, run setup, then start the llama server or run one prompt. The setup path calls scripts that download runtime binaries and the Hugging Face model files.

[scripts/download_models.sh](https://github.com/PrismML-Eng/Bonsai-demo/blob/23da1365df0364ef9e98d1cd18db6b0c06295751/scripts/download_models.sh) resolves `BONSAI_FAMILY=bonsai2` by default, maps that to `prism-ml/Ternary-Bonsai-2-27B-gguf`, and uses `huggingface_hub.snapshot_download` with allow patterns. For Bonsai 2 it downloads `*-PQ2_0.gguf` and `*mmproj-Q8_0.gguf` by default.

At run time, [scripts/run_llama.sh](https://github.com/PrismML-Eng/Bonsai-demo/blob/23da1365df0364ef9e98d1cd18db6b0c06295751/scripts/run_llama.sh) locates a forked `llama-cli`, selects the model file using helper logic from [scripts/common.sh](https://github.com/PrismML-Eng/Bonsai-demo/blob/23da1365df0364ef9e98d1cd18db6b0c06295751/scripts/common.sh), exports library paths, computes GPU layer offload, and executes the binary with context and sampling flags. The GGUF metadata then supplies the architecture, chat template, BOS/EOS tokens, sampling defaults, and context assumptions.

For image input, the Q8 projector file is loaded only when needed. That split is a good deployment choice: text-only serving is not forced to keep the vision tower resident.

## Key files, configs, cards, and artifacts

- Hugging Face [README.md](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf/blob/6ed5e12bf84b7a63069882c91dd9e9218647d17b/README.md) is the main card and the benchmark/format story.
- [Ternary-Bonsai-2-27B-PTQ1_0.gguf](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf/blob/6ed5e12bf84b7a63069882c91dd9e9218647d17b/Ternary-Bonsai-2-27B-PTQ1_0.gguf) is the memory-tight dense-trit band.
- [Ternary-Bonsai-2-27B-PQ2_0.gguf](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf/blob/6ed5e12bf84b7a63069882c91dd9e9218647d17b/Ternary-Bonsai-2-27B-PQ2_0.gguf) is the default demo band and the safer general choice in their scripts.
- [Ternary-Bonsai-2-27B-mmproj-Q8_0.gguf](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf/blob/6ed5e12bf84b7a63069882c91dd9e9218647d17b/Ternary-Bonsai-2-27B-mmproj-Q8_0.gguf) is the optional multimodal projector.
- Demo [README.md](https://github.com/PrismML-Eng/Bonsai-demo/blob/23da1365df0364ef9e98d1cd18db6b0c06295751/README.md) is the product-level start point.
- Demo [MODEL-FORMATS.md](https://github.com/PrismML-Eng/Bonsai-demo/blob/23da1365df0364ef9e98d1cd18db6b0c06295751/MODEL-FORMATS.md) is the clearest compatibility and migration doc.
- Demo [scripts/download_models.sh](https://github.com/PrismML-Eng/Bonsai-demo/blob/23da1365df0364ef9e98d1cd18db6b0c06295751/scripts/download_models.sh) is the Hugging Face artifact selector.
- Demo [scripts/run_llama.sh](https://github.com/PrismML-Eng/Bonsai-demo/blob/23da1365df0364ef9e98d1cd18db6b0c06295751/scripts/run_llama.sh) is the simplest inference path.
- Demo [scripts/start_llama_server.sh](https://github.com/PrismML-Eng/Bonsai-demo/blob/23da1365df0364ef9e98d1cd18db6b0c06295751/scripts/start_llama_server.sh) is the local server path.
- Demo [VISION.md](https://github.com/PrismML-Eng/Bonsai-demo/blob/23da1365df0364ef9e98d1cd18db6b0c06295751/VISION.md), [TOOLS.md](https://github.com/PrismML-Eng/Bonsai-demo/blob/23da1365df0364ef9e98d1cd18db6b0c06295751/TOOLS.md), [KV-CACHE.md](https://github.com/PrismML-Eng/Bonsai-demo/blob/23da1365df0364ef9e98d1cd18db6b0c06295751/KV-CACHE.md), and [SPECULATIVE.md](https://github.com/PrismML-Eng/Bonsai-demo/blob/23da1365df0364ef9e98d1cd18db6b0c06295751/SPECULATIVE.md) are the advanced operating docs.

## Important components

The `PTQ1_0` and `PQ2_0` files are the central components. The card presents them as two legitimate packings, not a winner and loser. `PTQ1_0` moves less weight data, while `PQ2_0` can be cheaper to unpack and faster for prompt processing.

The chat template inside GGUF metadata is also important. The API metadata included tool-call formatting, multimodal content markers, and reasoning-effort handling. That means the artifact is not just weights; it is also a protocol expectation for messages, tools, and thinking mode.

The optional `mmproj` files matter because they keep multimodal capability separate from the text-only resident model. That is the right split for local deployment where every gigabyte matters.

The demo repo is part of the artifact whether Hugging Face labels it that way or not. [scripts/download_models.sh](https://github.com/PrismML-Eng/Bonsai-demo/blob/23da1365df0364ef9e98d1cd18db6b0c06295751/scripts/download_models.sh), [scripts/run_llama.sh](https://github.com/PrismML-Eng/Bonsai-demo/blob/23da1365df0364ef9e98d1cd18db6b0c06295751/scripts/run_llama.sh), and [MODEL-FORMATS.md](https://github.com/PrismML-Eng/Bonsai-demo/blob/23da1365df0364ef9e98d1cd18db6b0c06295751/MODEL-FORMATS.md) are the files that turn "download a model" into "run the right model with the right binary."

## Important knobs / configs / extension points

- `BONSAI_FAMILY` and `BONSAI_MODEL` in [Bonsai-demo README.md](https://github.com/PrismML-Eng/Bonsai-demo/blob/23da1365df0364ef9e98d1cd18db6b0c06295751/README.md) select Bonsai 2, earlier ternary, or earlier 1-bit families.
- `BONSAI_CTX`, `BONSAI_NGL`, `BONSAI_SPECULATIVE`, and `BONSAI_KV4` are the important runtime controls documented in [Bonsai-demo README.md](https://github.com/PrismML-Eng/Bonsai-demo/blob/23da1365df0364ef9e98d1cd18db6b0c06295751/README.md) and implemented through launcher scripts.
- The download allow-pattern logic in [scripts/download_models.sh](https://github.com/PrismML-Eng/Bonsai-demo/blob/23da1365df0364ef9e98d1cd18db6b0c06295751/scripts/download_models.sh) prevents accidental giant downloads and expresses which file is recommended.
- [MODEL-FORMATS.md](https://github.com/PrismML-Eng/Bonsai-demo/blob/23da1365df0364ef9e98d1cd18db6b0c06295751/MODEL-FORMATS.md) is the compatibility switchboard for GGUF formats and backend support.
- Sampling defaults in [README.md](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf/blob/6ed5e12bf84b7a63069882c91dd9e9218647d17b/README.md) distinguish thinking mode and instruct mode. The script path for Bonsai 2 in [scripts/run_llama.sh](https://github.com/PrismML-Eng/Bonsai-demo/blob/23da1365df0364ef9e98d1cd18db6b0c06295751/scripts/run_llama.sh) applies `--temp 1.0 --top-p 0.95 --top-k 20`.

## Practical questions and answers

Q: Can I run this with stock llama.cpp?

A: The card says no, and [MODEL-FORMATS.md](https://github.com/PrismML-Eng/Bonsai-demo/blob/23da1365df0364ef9e98d1cd18db6b0c06295751/MODEL-FORMATS.md) explains why. `PQ2_0` and `PTQ1_0` fail safely on stock llama.cpp, while the related `Q2_0` testing band can load incorrectly because upstream knows the type id but not the rotated-basis activation transform.

Q: Which file would I use first?

A: The demo chooses [Ternary-Bonsai-2-27B-PQ2_0.gguf](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf/blob/6ed5e12bf84b7a63069882c91dd9e9218647d17b/Ternary-Bonsai-2-27B-PQ2_0.gguf) and the [Q8 projector](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf/blob/6ed5e12bf84b7a63069882c91dd9e9218647d17b/Ternary-Bonsai-2-27B-mmproj-Q8_0.gguf) by default in [scripts/download_models.sh](https://github.com/PrismML-Eng/Bonsai-demo/blob/23da1365df0364ef9e98d1cd18db6b0c06295751/scripts/download_models.sh). Use [PTQ1_0](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf/blob/6ed5e12bf84b7a63069882c91dd9e9218647d17b/Ternary-Bonsai-2-27B-PTQ1_0.gguf) when memory is tighter and your backend favors it.

Q: What is the real mechanism behind the footprint?

A: The card describes ternary `{-1, 0, +1}` weights with FP16 scale factors per group of 128, plus a blockwise Hadamard rotation folded into stored weights. That reduces resident language-model size, but only if the runtime knows how to apply the corresponding activation transform.

Q: What would I distrust until independently measured?

A: The absolute benchmark numbers and "98.2 percent retained" claim. The source links show a coherent methodology and benchmark table in [README.md](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf/blob/6ed5e12bf84b7a63069882c91dd9e9218647d17b/README.md), but this kind of claim needs third-party runs across prompts, hardware, and tool-calling tasks.

## What is smart

The smartest move is releasing the runtime story with the model. The Hugging Face card points straight to [PrismML-Eng/Bonsai-demo](https://github.com/PrismML-Eng/Bonsai-demo/tree/23da1365df0364ef9e98d1cd18db6b0c06295751), and that repo has real scripts instead of a vague "use llama.cpp" sentence.

The second smart move is explicit failure guidance. [MODEL-FORMATS.md](https://github.com/PrismML-Eng/Bonsai-demo/blob/23da1365df0364ef9e98d1cd18db6b0c06295751/MODEL-FORMATS.md) explains not only what to run, but how old and stock runtimes fail. That is exactly the kind of doc low-level model releases need.

The third smart move is splitting the optional vision projector. Local users who want text do not pay the projector residency cost.

## What is flawed or weak

The artifact is tightly coupled to custom runtime work. That is unavoidable for the technique, but it reduces portability. If the forked llama.cpp binaries lag behind upstream bug fixes, packaging conventions, or platform support, the model's usability falls with them.

The model card mixes strong claims with complex evaluation details. A builder should admire the detail in [README.md](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf/blob/6ed5e12bf84b7a63069882c91dd9e9218647d17b/README.md), but still treat the benchmark aggregate as a claim to reproduce, not a law of nature.

The naming surface is also fragile. [MODEL-FORMATS.md](https://github.com/PrismML-Eng/Bonsai-demo/blob/23da1365df0364ef9e98d1cd18db6b0c06295751/MODEL-FORMATS.md) spends a lot of space on `Q2_0`, `PQ2_0`, group sizes, legacy layouts, and fork-only bands. That documentation is necessary, but the need for it is a sign that distribution will confuse some users.

## What we can learn / steal

Steal the model-plus-runtime packaging mindset. If a model needs custom kernels or prompt semantics, release the scripts, docs, and compatibility matrix as first-class artifacts.

Steal allow-pattern downloads from [scripts/download_models.sh](https://github.com/PrismML-Eng/Bonsai-demo/blob/23da1365df0364ef9e98d1cd18db6b0c06295751/scripts/download_models.sh). Users should not need to know which of five multi-gigabyte files to avoid.

Steal the file split between language model and optional projector. Local inference products should keep optional capabilities out of the hot resident path.

Steal the honest "stock runtime will not work" warning. Quietly producing gibberish is worse than refusing to load.

## How we could apply it

For any model artifact we ship, include a tiny runtime repo or directory with pinned scripts, file-selection logic, hardware defaults, and a compatibility note. Treat "how to run the right file safely" as part of the release.

For low-bit experiments, measure and document the whole stack: true bits per weight, packed file size, prompt-processing speed, decode speed, energy or power where available, benchmark degradation by category, and backend-specific behavior.

For agentic models, publish the actual chat template and tool-call assumptions. This artifact's GGUF metadata does that, and it is essential for downstream clients that want tools, multimodal input, and thinking mode to behave consistently.

## Bottom line

Ternary-Bonsai-2-27B GGUF is interesting because it is not just another quant upload. It is a tightly coupled low-bit model release with custom formats, custom kernels, explicit runtime scripts, optional vision artifacts, and enough documentation to study the trade: impressive footprint, but only inside the runtime stack designed for it.
