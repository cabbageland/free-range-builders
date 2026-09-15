# Edge0-35B-A3B Preview

- Source: Hugging Face
- Artifact: `Edge0/Edge0-35B-A3B-preview`
- URL: https://huggingface.co/Edge0/Edge0-35B-A3B-preview
- Date: 2026-09-15
- Snapshot studied: Hugging Face commit `15dc6959b64fb579550f2b9b3bfd3e6b3a3b1173`; linked runtime source `Edge0-AI/edge0` at commit `c18eb62e8e7c715a4b5a3781145dcaa496352d66`
- Why picked today: Hugging Face trending showed `Edge0/Edge0-35B-A3B-preview` near the top after the higher-ranked DeepSeek model had already been covered. It is useful because the Hub repo is more than a model card: it bundles a 4-bit MoE checkpoint, LoRA adapter, prerouter adapter, tokenizer/chat template, shard index, and a linked runtime that explains the SSD expert-offload mechanism.

## Executive summary

[`Edge0/Edge0-35B-A3B-preview`](https://huggingface.co/Edge0/Edge0-35B-A3B-preview/tree/15dc6959b64fb579550f2b9b3bfd3e6b3a3b1173) is an experimental edge-inference release for a 35B-class sparse MoE model. The core claim in [`README.md`](https://huggingface.co/Edge0/Edge0-35B-A3B-preview/blob/15dc6959b64fb579550f2b9b3bfd3e6b3a3b1173/README.md) is that it runs with roughly phone-class active memory by keeping 4-bit expert weights on storage, loading only routed experts, predicting next-step routing with a prerouter, and recovering quantization loss with an unmerged LoRA path.

The artifact itself has enough structure to audit. [`config.json`](https://huggingface.co/Edge0/Edge0-35B-A3B-preview/blob/15dc6959b64fb579550f2b9b3bfd3e6b3a3b1173/config.json) declares `qwen3_5_moe`, 4-bit affine quantization with 8-bit gates, 40 layers, 256 experts, 2048 hidden size, 262144 max positions, and a mix of linear-attention and full-attention layers. [`model.safetensors.index.json`](https://huggingface.co/Edge0/Edge0-35B-A3B-preview/blob/15dc6959b64fb579550f2b9b3bfd3e6b3a3b1173/model.safetensors.index.json) maps about 20.4 GB of quantized weights across four shards. [`lora_edge0_35b.safetensors`](https://huggingface.co/Edge0/Edge0-35B-A3B-preview/blob/15dc6959b64fb579550f2b9b3bfd3e6b3a3b1173/lora_edge0_35b.safetensors) and [`prerouter_edge0_35b.safetensors`](https://huggingface.co/Edge0/Edge0-35B-A3B-preview/blob/15dc6959b64fb579550f2b9b3bfd3e6b3a3b1173/prerouter_edge0_35b.safetensors) are sidecar adapters, not marketing labels.

The linked runtime [`Edge0-AI/edge0`](https://github.com/Edge0-AI/edge0/tree/c18eb62e8e7c715a4b5a3781145dcaa496352d66) makes the mechanism concrete. [`src/edge0/streaming/mmap.py`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/src/edge0/streaming/mmap.py) does zero-copy byte-range access into safetensors shards. [`src/edge0/streaming/layer.py`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/src/edge0/streaming/layer.py) implements the streaming MoE expert block. [`src/edge0/prerouter/stager.py`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/src/edge0/prerouter/stager.py) batches prerouter heads and stages predicted experts for the next decode step. [`src/edge0/adapters/lora.py`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/src/edge0/adapters/lora.py) keeps LoRA as a parallel delta path instead of merging it into the quantized base.

## What they built / released

The Hugging Face repo is a ready-to-run Edge0 model directory. It includes the base model shards, tokenizer files, a chat template, generation defaults, preprocessor/processor configs, a visual asset and demo video, a LoRA adapter, and a prerouter adapter. The top-level file list from the Hub API includes [`config.json`](https://huggingface.co/Edge0/Edge0-35B-A3B-preview/blob/15dc6959b64fb579550f2b9b3bfd3e6b3a3b1173/config.json), [`tokenizer.json`](https://huggingface.co/Edge0/Edge0-35B-A3B-preview/blob/15dc6959b64fb579550f2b9b3bfd3e6b3a3b1173/tokenizer.json), [`tokenizer_config.json`](https://huggingface.co/Edge0/Edge0-35B-A3B-preview/blob/15dc6959b64fb579550f2b9b3bfd3e6b3a3b1173/tokenizer_config.json), [`chat_template.jinja`](https://huggingface.co/Edge0/Edge0-35B-A3B-preview/blob/15dc6959b64fb579550f2b9b3bfd3e6b3a3b1173/chat_template.jinja), [`generation_config.json`](https://huggingface.co/Edge0/Edge0-35B-A3B-preview/blob/15dc6959b64fb579550f2b9b3bfd3e6b3a3b1173/generation_config.json), four model shards, and the two adapter files.

The runtime repo turns this into a framework. [`README.md`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/README.md) describes `edge0-35b` and `edge0-8b` tiers, MLX as the current backend, OpenAI-compatible serving, and a Python `AutoEngine` API. [`src/edge0/registry.py`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/src/edge0/registry.py) maps model types such as `qwen3_5_moe` to the `edge0-35b` adapter. [`src/edge0/models/edge0_35b/__init__.py`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/src/edge0/models/edge0_35b/__init__.py) pins the production profile: 40 layers, 256 routed experts, 4-bit affine group-64 quantization, K=4 runtime routing, start layer 7 prerouter, LoRA file, generation defaults, port 8085, and target throughput.

## Why it matters

Edge inference for MoE models is usually bottlenecked by resident memory, not just arithmetic. Edge0's design attacks the memory problem directly: keep all experts in quantized safetensors on disk, mmap the shards, read expert slices as needed, and use a prerouter to overlap expert loads with the next decode step. That is a systems idea, not just a checkpoint release.

It also shows how a model artifact can become a runtime contract. The Hub repo gives the data files. The runtime repo gives the rules for interpreting those files. [`src/edge0/models/edge0_35b/__init__.py`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/src/edge0/models/edge0_35b/__init__.py) is especially useful because it reconciles the artifact into a serving profile. One subtle point: the raw [`config.json`](https://huggingface.co/Edge0/Edge0-35B-A3B-preview/blob/15dc6959b64fb579550f2b9b3bfd3e6b3a3b1173/config.json) text config says `num_experts_per_tok: 8`, while the Edge0 runtime profile and model card describe K=4. Builders should treat the runtime profile as part of the artifact, not an optional wrapper.

## Artifact shape at a glance

- [`README.md`](https://huggingface.co/Edge0/Edge0-35B-A3B-preview/blob/15dc6959b64fb579550f2b9b3bfd3e6b3a3b1173/README.md): card, performance claims, quality table, limitations, and quick start.
- [`config.json`](https://huggingface.co/Edge0/Edge0-35B-A3B-preview/blob/15dc6959b64fb579550f2b9b3bfd3e6b3a3b1173/config.json): model architecture and quantization config.
- [`model.safetensors.index.json`](https://huggingface.co/Edge0/Edge0-35B-A3B-preview/blob/15dc6959b64fb579550f2b9b3bfd3e6b3a3b1173/model.safetensors.index.json): 20.4 GB weight map across four safetensor shards.
- [`lora_edge0_35b.safetensors`](https://huggingface.co/Edge0/Edge0-35B-A3B-preview/blob/15dc6959b64fb579550f2b9b3bfd3e6b3a3b1173/lora_edge0_35b.safetensors): Recover-LoRA adapter sidecar.
- [`prerouter_edge0_35b.safetensors`](https://huggingface.co/Edge0/Edge0-35B-A3B-preview/blob/15dc6959b64fb579550f2b9b3bfd3e6b3a3b1173/prerouter_edge0_35b.safetensors): trained prerouter head weights.
- [`chat_template.jinja`](https://huggingface.co/Edge0/Edge0-35B-A3B-preview/blob/15dc6959b64fb579550f2b9b3bfd3e6b3a3b1173/chat_template.jinja): Qwen-style chat/tool/vision/thinking prompt template.
- [`tokenizer_config.json`](https://huggingface.co/Edge0/Edge0-35B-A3B-preview/blob/15dc6959b64fb579550f2b9b3bfd3e6b3a3b1173/tokenizer_config.json): tokenizer backend, special tokens, and 262144 model max length.
- [`generation_config.json`](https://huggingface.co/Edge0/Edge0-35B-A3B-preview/blob/15dc6959b64fb579550f2b9b3bfd3e6b3a3b1173/generation_config.json): default sampling values (`temperature=1.0`, `top_p=0.95`, `top_k=20`).
- [`configuration.json`](https://huggingface.co/Edge0/Edge0-35B-A3B-preview/blob/15dc6959b64fb579550f2b9b3bfd3e6b3a3b1173/configuration.json): lightweight task/framework metadata.
- [`Edge0-AI/edge0`](https://github.com/Edge0-AI/edge0/tree/c18eb62e8e7c715a4b5a3781145dcaa496352d66): linked runtime with streaming, adapters, prerouter, registry, server, examples, and docs.

## Layered architecture dissection

### High-level system shape

The artifact is two things bound together: a Hugging Face model directory and a custom runtime. The model directory carries static assets. The runtime takes that directory, detects the tier, installs streaming expert layers, installs LoRA, installs the prerouter, and exposes demo/chat/server APIs.

[`src/edge0/registry.py`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/src/edge0/registry.py) is the entry point for that binding. It resolves `config.json` `model_type` to a registered model adapter. For this model, [`src/edge0/models/edge0_35b/__init__.py`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/src/edge0/models/edge0_35b/__init__.py) supplies the Edge0-specific serving config.

### Main layers

**1. Hub packaging layer**  
The Hugging Face repo holds the checkpoint contract: [`config.json`](https://huggingface.co/Edge0/Edge0-35B-A3B-preview/blob/15dc6959b64fb579550f2b9b3bfd3e6b3a3b1173/config.json), [`model.safetensors.index.json`](https://huggingface.co/Edge0/Edge0-35B-A3B-preview/blob/15dc6959b64fb579550f2b9b3bfd3e6b3a3b1173/model.safetensors.index.json), four model shards, tokenizer assets, and sidecar adapter weights.

**2. Model registry layer**  
[`src/edge0/registry.py`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/src/edge0/registry.py) provides `AutoConfig`, `AutoModel`, and `AutoEngine`, with type aliases for `qwen3_5_moe` and `qwen3_5_moe_text` pointing to `edge0-35b`.

**3. Engine loop layer**  
[`src/edge0/engine/base.py`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/src/edge0/engine/base.py) owns the generic prefill/decode/generate lifecycle. It chunks prefill, calls model-specific hooks, samples tokens, updates decode position, and closes expert caches.

**4. Streaming expert layer**  
[`src/edge0/streaming/layer.py`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/src/edge0/streaming/layer.py) is the core systems file. It implements `StreamingSwitchGLU`, the offloaded MoE expert block, with paths for whole-layer prefill, hot-stack prefill, staged decode, exact decode, pinned experts, shared LRU cache, prefetch buffer, fixed staged slots, and zero overflow slots.

**5. Mmap layer**  
[`src/edge0/streaming/mmap.py`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/src/edge0/streaming/mmap.py) opens safetensors shards as mmaps, parses tensor offsets from the header, and returns raw zero-copy byte views. That is the low-level trick that makes "SSD expert offload" specific.

**6. Prerouter layer**  
[`src/edge0/prerouter/stager.py`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/src/edge0/prerouter/stager.py) batches prerouter owner heads, selects expert IDs, and stages next-step experts in streaming layers. Its comments are unusually direct about the cost model: one stacked batch, one eval, one `tolist`, then per-consumer staging.

**7. LoRA recovery layer**  
[`src/edge0/adapters/lora.py`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/src/edge0/adapters/lora.py) wraps target linears with `LoraLinear`, calculating `base(x) + scale * ((x @ A.T) @ B.T)`. The base quantized weights stay byte-identical; the LoRA is not merged or requantized.

**8. API/server layer**  
[`src/edge0/server/app.py`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/src/edge0/server/app.py) and [`src/edge0/server/chat.py`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/src/edge0/server/chat.py) expose the engine as chat and OpenAI-compatible serving. [`examples/bench.py`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/examples/bench.py) is the reproducibility path for the card's throughput claims.

### Inference / data / control flow

The quick path in the card downloads the HF repo and runs `edge0 chat` or `edge0 serve`. Runtime resolution starts in [`registry.py`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/src/edge0/registry.py), which reads [`config.json`](https://huggingface.co/Edge0/Edge0-35B-A3B-preview/blob/15dc6959b64fb579550f2b9b3bfd3e6b3a3b1173/config.json), maps `qwen3_5_moe` to the 35B tier, then constructs the engine.

During prefill, [`Edge0Engine.prefill`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/src/edge0/engine/base.py) processes the prompt in chunks. The streaming layer can load whole expert layers or hot expert stacks depending on the path. During decode, the current token goes through `_step_pre`, the model forward pass, and `_step_post`. The prerouter stager predicts the next step's experts after the current forward's logits materialize; those predicted experts are submitted to streaming layers so the storage reads overlap the following decode work.

The expert bytes come from [`SafetensorsMmap.raw`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/src/edge0/streaming/mmap.py), flow through caches in [`streaming/cache.py`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/src/edge0/streaming/cache.py), and are used by [`StreamingSwitchGLU`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/src/edge0/streaming/layer.py) for the routed-expert GLU. LoRA targets are wrapped at model build time by [`install_lora`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/src/edge0/adapters/lora.py).

## Key files, configs, cards, and artifacts

- [`README.md`](https://huggingface.co/Edge0/Edge0-35B-A3B-preview/blob/15dc6959b64fb579550f2b9b3bfd3e6b3a3b1173/README.md): claims, usage, performance, quality, limitations.
- [`config.json`](https://huggingface.co/Edge0/Edge0-35B-A3B-preview/blob/15dc6959b64fb579550f2b9b3bfd3e6b3a3b1173/config.json): architecture and quantization. Note the runtime's K=4 profile differs from the inherited `num_experts_per_tok: 8` in the raw config.
- [`model.safetensors.index.json`](https://huggingface.co/Edge0/Edge0-35B-A3B-preview/blob/15dc6959b64fb579550f2b9b3bfd3e6b3a3b1173/model.safetensors.index.json): shard and tensor mapping.
- [`lora_edge0_35b.safetensors`](https://huggingface.co/Edge0/Edge0-35B-A3B-preview/blob/15dc6959b64fb579550f2b9b3bfd3e6b3a3b1173/lora_edge0_35b.safetensors): low-rank recovery adapter.
- [`prerouter_edge0_35b.safetensors`](https://huggingface.co/Edge0/Edge0-35B-A3B-preview/blob/15dc6959b64fb579550f2b9b3bfd3e6b3a3b1173/prerouter_edge0_35b.safetensors): next-step expert predictor.
- [`chat_template.jinja`](https://huggingface.co/Edge0/Edge0-35B-A3B-preview/blob/15dc6959b64fb579550f2b9b3bfd3e6b3a3b1173/chat_template.jinja): prompt grammar for tools, tool responses, thinking, image/video placeholders, and assistant generation prompt.
- [`tokenizer_config.json`](https://huggingface.co/Edge0/Edge0-35B-A3B-preview/blob/15dc6959b64fb579550f2b9b3bfd3e6b3a3b1173/tokenizer_config.json): special-token and processor metadata.
- [`src/edge0/models/edge0_35b/__init__.py`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/src/edge0/models/edge0_35b/__init__.py): source-side serving profile.
- [`src/edge0/streaming/layer.py`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/src/edge0/streaming/layer.py): streaming expert implementation.
- [`src/edge0/streaming/mmap.py`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/src/edge0/streaming/mmap.py): byte-range safetensors access.
- [`src/edge0/prerouter/stager.py`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/src/edge0/prerouter/stager.py): prerouter staging.
- [`src/edge0/adapters/lora.py`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/src/edge0/adapters/lora.py): unmerged LoRA installation.
- [`src/edge0/engine/base.py`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/src/edge0/engine/base.py): shared generation loop.

## Important components

[`Qwen35Config`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/src/edge0/models/edge0_35b/__init__.py) is the bridge between the generic Qwen MoE checkpoint and the Edge0 inference profile. It declares the MoE spec, quantization, adapter paths, prerouter settings, generation settings, target memory, and target throughput.

[`SafetensorsMmap`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/src/edge0/streaming/mmap.py) is the storage primitive. It parses the safetensors header, records byte offsets, and returns raw `uint8` views over tensor bytes without materializing whole tensors.

[`StreamingSwitchGLU`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/src/edge0/streaming/layer.py) is the runtime's heart. It owns the expert-loading thread pools, cache/prefetch logic, staged decode slots, hot expert stacks, whole-layer prefill path, and quantized gather/GEMM calls.

[`PrerouterStager`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/src/edge0/prerouter/stager.py) is the latency trick. It turns model-side features into predicted expert IDs, then submits expert loads for the next token so slow storage work overlaps with computation.

[`LoraLinear`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/src/edge0/adapters/lora.py) is the quality-recovery trick. It preserves the quantized base path and adds a small fp16 delta path.

## Important knobs / configs / extension points

- [`config.json`](https://huggingface.co/Edge0/Edge0-35B-A3B-preview/blob/15dc6959b64fb579550f2b9b3bfd3e6b3a3b1173/config.json): 4-bit affine quantization, group size 64, 8-bit router/gate exceptions, 40 layers, 256 experts, 262144 context metadata.
- [`src/edge0/models/edge0_35b/__init__.py`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/src/edge0/models/edge0_35b/__init__.py): runtime K, start layer, hot window, prefill chunk, generation config, target performance numbers.
- [`src/edge0/streaming/options.py`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/src/edge0/streaming/options.py): layer behavior knobs for staged mode, hot layers, cache slots, prefetch, and threading.
- [`chat_template.jinja`](https://huggingface.co/Edge0/Edge0-35B-A3B-preview/blob/15dc6959b64fb579550f2b9b3bfd3e6b3a3b1173/chat_template.jinja): tool-call and thinking grammar. It matters because bad prompt rendering can look like model failure.
- [`generation_config.json`](https://huggingface.co/Edge0/Edge0-35B-A3B-preview/blob/15dc6959b64fb579550f2b9b3bfd3e6b3a3b1173/generation_config.json): Hub-level sampling defaults, which differ from the runtime's `GenerationConfig` in [`Qwen35Config`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/src/edge0/models/edge0_35b/__init__.py).
- [`examples/bench.py`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/examples/bench.py): benchmark reproduction surface.

## Practical questions and answers

**Is this a normal Transformers model repo?**  
No. The Hub metadata says `library_name: mlx`, and the card tells users to run it through [`edge0`](https://github.com/Edge0-AI/edge0/tree/c18eb62e8e7c715a4b5a3781145dcaa496352d66). The ordinary files are present, but the intended behavior depends on [`src/edge0/models/edge0_35b/__init__.py`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/src/edge0/models/edge0_35b/__init__.py), streaming expert replacement, LoRA installation, and prerouter staging.

**What is actually offloaded?**  
The routed MoE experts. [`StreamingSwitchGLU`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/src/edge0/streaming/layer.py) says shared experts, routers, and attention stay resident in the base model, while routed expert projections are streamed.

**Why is the prerouter needed?**  
Without prediction, loading experts after routing can stall decode. [`PrerouterStager`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/src/edge0/prerouter/stager.py) predicts next-step experts and stages them before they are consumed.

**Does LoRA get merged into the 4-bit base?**  
No. [`LoraLinear`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/src/edge0/adapters/lora.py) leaves the base byte-identical and adds the low-rank path in parallel.

**What is the biggest mismatch to watch?**  
The raw Hub config, model card, and runtime profile are not all the same layer of truth. For example, [`config.json`](https://huggingface.co/Edge0/Edge0-35B-A3B-preview/blob/15dc6959b64fb579550f2b9b3bfd3e6b3a3b1173/config.json) says `num_experts_per_tok: 8`, while the runtime [`Qwen35Config`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/src/edge0/models/edge0_35b/__init__.py) and card describe a K=4 Edge0 profile. A deployment should pin the runtime and artifact versions together.

## What is smart

- The release co-locates base checkpoint, [`lora_edge0_35b.safetensors`](https://huggingface.co/Edge0/Edge0-35B-A3B-preview/blob/15dc6959b64fb579550f2b9b3bfd3e6b3a3b1173/lora_edge0_35b.safetensors), and [`prerouter_edge0_35b.safetensors`](https://huggingface.co/Edge0/Edge0-35B-A3B-preview/blob/15dc6959b64fb579550f2b9b3bfd3e6b3a3b1173/prerouter_edge0_35b.safetensors), making the model directory a complete runtime package.
- [`SafetensorsMmap`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/src/edge0/streaming/mmap.py) uses safetensors offsets directly instead of inventing a new expert storage format.
- [`StreamingSwitchGLU`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/src/edge0/streaming/layer.py) is explicit about staged decode, hot sets, LRU cache, and prefetch behavior.
- [`PrerouterStager`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/src/edge0/prerouter/stager.py) batches owner heads to avoid many small sync points.
- [`adapters/lora.py`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/src/edge0/adapters/lora.py) keeps adapter swapping cheap because the base stays read-only and unmerged.

## What is flawed or weak

- The card's headline numbers depend on one backend and one hardware class. [`README.md`](https://huggingface.co/Edge0/Edge0-35B-A3B-preview/blob/15dc6959b64fb579550f2b9b3bfd3e6b3a3b1173/README.md) says the MLX backend currently targets Apple Silicon and other backends are roadmap.
- Long context still grows KV cache. The active expert memory story does not remove the ordinary context-memory story.
- Agent capability is explicitly called weak in the card's limitations. This is not a plug-and-play coding-agent model yet.
- The raw config/runtime mismatch around expert K is a footgun unless users treat the Edge0 runtime as part of the artifact.
- The quality table in [`README.md`](https://huggingface.co/Edge0/Edge0-35B-A3B-preview/blob/15dc6959b64fb579550f2b9b3bfd3e6b3a3b1173/README.md) is self-reported. The repo provides a benchmark script, but not a full independent evaluation pipeline inside the Hub object.

## What we can learn / steal

- Treat model release directories as runtime bundles, not just weight dumps. A base checkpoint plus small adapter files plus a source-side profile is a useful release pattern.
- If large weights are sparse at runtime, store them in a format that supports byte-range reads. [`mmap.py`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/src/edge0/streaming/mmap.py) is a clean example.
- Use prediction to hide IO latency. The prerouter does not make storage faster; it moves storage reads earlier.
- Keep LoRA unmerged when the base is quantized and shared. [`LoraLinear`](https://github.com/Edge0-AI/edge0/blob/c18eb62e8e7c715a4b5a3781145dcaa496352d66/src/edge0/adapters/lora.py) shows how to make recovery adapters compatible with a read-only base.
- Separate backend facade from core runtime. The `edge0` README and file layout put MLX under [`src/edge0/backends/mlx`](https://github.com/Edge0-AI/edge0/tree/c18eb62e8e7c715a4b5a3781145dcaa496352d66/src/edge0/backends/mlx), leaving a plausible path for CUDA later.

## How we could apply it

For any product that serves sparse models, I would borrow the separation of concerns: one artifact directory with weights and sidecars, one runtime profile that knows the serving constraints, one byte-range storage primitive, one cache/prefetch layer, and one normal chat/server surface above it.

For local AI tools, I would copy the idea of overlapping IO with compute. Even outside MoE, many local inference bottlenecks are "wrong thing resident at the wrong time." Edge0's prerouter is specialized, but the broader lesson is to predict and stage the next expensive resource.

For model publishing, I would also copy the candor around limitations. The card names Apple Silicon backend limits, long-context KV growth, and weak agent behavior. That makes the release more useful than a benchmark-only announcement.

## Bottom line

`Edge0/Edge0-35B-A3B-preview` is a strong Hugging Face scout because the artifact has real mechanism: sharded 4-bit MoE weights, LoRA recovery, prerouter prediction, tokenizer/chat templates, and linked runtime source that implements storage-backed expert streaming.

The reusable idea is not "every model should run from SSD." It is that artifact packaging and runtime design can cooperate: when only part of a giant model is active per token, the serving system should make that sparsity visible all the way down to file offsets, caches, and staged loads.
