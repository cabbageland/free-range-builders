# gpt-oss-120b

- Source: Hugging Face
- Artifact: `openai/gpt-oss-120b`
- URL: https://huggingface.co/openai/gpt-oss-120b
- Date: 2026-09-13
- Snapshot studied: Hugging Face commit `b5c939de8f754692c1647ca79fbf85e8c1e70f8a`; linked source repo `openai/gpt-oss` @ `7b583341fe16729127f6d5b94a7b09ccae97e1a1`
- Why picked today: The Hugging Face API returned `openai/gpt-oss-120b` among high-signal text-generation models, with roughly 5.4M downloads and 5.2k likes in the fetched metadata. I picked it because the Hub artifact is not just weights: it exposes model config, MXFP4 quantization metadata, chat-template protocol, tokenizer metadata, sharded indexes, original weights, and a linked reference implementation repository.

## Executive summary
[`openai/gpt-oss-120b`](https://huggingface.co/openai/gpt-oss-120b/tree/b5c939de8f754692c1647ca79fbf85e8c1e70f8a) is the larger OpenAI open-weight gpt-oss artifact: 117B total parameters, about 5.1B active parameters per token, Apache-2.0 license, and a Hugging Face package intended for Transformers, vLLM, Ollama, LM Studio, and reference implementations. The most useful artifact-level files are [`config.json`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/config.json), [`chat_template.jinja`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/chat_template.jinja), [`tokenizer_config.json`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/tokenizer_config.json), [`generation_config.json`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/generation_config.json), and [`model.safetensors.index.json`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/model.safetensors.index.json).

The central model shape is clear from [`config.json`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/config.json): `GptOssForCausalLM`, 36 layers, 128 local experts, 4 experts per token, 2880 hidden size, 64 attention heads, 8 KV heads, alternating sliding and full attention layers, 131,072 maximum positions, YaRN-style RoPE scaling, and MXFP4 quantization for MoE weights while attention/router/embeddings/lm head stay unconverted. The safetensors index reports about 65.25 GB for the transformed model shards, plus original-format files under [`original`](https://huggingface.co/openai/gpt-oss-120b/tree/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/original) and a large [`metal/model.bin`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/metal/model.bin).

The most important builder insight is that the runtime contract is as important as the weights. [`chat_template.jinja`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/chat_template.jinja) encodes the harmony response format, reasoning effort, channels, built-in tools, tool schemas, and tool-call rendering. A gateway that loads the shards but ignores this template can still serve the model incorrectly.

## What they built / released
OpenAI released a Hugging Face model artifact for `gpt-oss-120b`, plus a linked source repository at [`openai/gpt-oss`](https://github.com/openai/gpt-oss/tree/7b583341fe16729127f6d5b94a7b09ccae97e1a1). The Hub card in [`README.md`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/README.md) frames it as the production/high-reasoning member of the gpt-oss family, intended to fit on a single 80 GB GPU in optimized stacks.

The artifact includes ordinary Hub packaging files, a model card, license and usage policy, tokenizer metadata, a 16 KB chat template, model config, generation config, 15 transformed safetensor shards named [`model-00000-of-00014.safetensors`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/model-00000-of-00014.safetensors) through [`model-00014-of-00014.safetensors`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/model-00014-of-00014.safetensors), a transformed [`model.safetensors.index.json`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/model.safetensors.index.json), original-format shards in [`original`](https://huggingface.co/openai/gpt-oss-120b/tree/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/original), and [`tokenizer.json`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/tokenizer.json).

The source repo is the missing half of the artifact story. [`gpt_oss/torch/model.py`](https://github.com/openai/gpt-oss/blob/7b583341fe16729127f6d5b94a7b09ccae97e1a1/gpt_oss/torch/model.py) is a readable PyTorch model, [`gpt_oss/triton/moe.py`](https://github.com/openai/gpt-oss/blob/7b583341fe16729127f6d5b94a7b09ccae97e1a1/gpt_oss/triton/moe.py) shows the optimized MoE kernel shape, [`gpt_oss/torch/weights.py`](https://github.com/openai/gpt-oss/blob/7b583341fe16729127f6d5b94a7b09ccae97e1a1/gpt_oss/torch/weights.py) decodes MXFP4 blocks, and [`gpt_oss/tokenizer.py`](https://github.com/openai/gpt-oss/blob/7b583341fe16729127f6d5b94a7b09ccae97e1a1/gpt_oss/tokenizer.py) defines the `o200k_harmony` special-token layer.

## Why it matters
This release matters because it makes a modern reasoning/tool-use model inspectable at multiple layers: weights, model config, chat protocol, tokenizer, reference math, optimized kernel shape, examples, and Responses-compatible serving. The card in [`README.md`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/README.md) says the model was trained for the harmony response format and should be used with it. The actual contract lives in [`chat_template.jinja`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/chat_template.jinja) and [`gpt_oss/tokenizer.py`](https://github.com/openai/gpt-oss/blob/7b583341fe16729127f6d5b94a7b09ccae97e1a1/gpt_oss/tokenizer.py).

It also matters because the quantization story is explicit. [`config.json`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/config.json) declares `quant_method` `mxfp4` and lists modules that are not converted: self-attention, MLP router, embeddings, and `lm_head`. [`gpt_oss/torch/weights.py`](https://github.com/openai/gpt-oss/blob/7b583341fe16729127f6d5b94a7b09ccae97e1a1/gpt_oss/torch/weights.py) shows what that means mechanically: 32 FP4 values packed into 16-byte blocks, scale tensors biased by 127, and chunked expansion back into bfloat16 for the simple reference path.

The release is still not reproducible in the research sense. There is no training data, training pipeline, or full evaluation harness in the Hub artifact. But for builders trying to serve, fine-tune, test, or wrap the model, the exposed source surface is unusually useful.

## Artifact shape at a glance
- [`README.md`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/README.md): model card, deployment examples, reasoning levels, tool-use claims, downloads, and links to guides/source.
- [`config.json`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/config.json): architecture truth for layers, experts, attention, RoPE, context, quantization, token IDs, and Transformers version.
- [`chat_template.jinja`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/chat_template.jinja): harmony prompt compiler for messages, channels, reasoning effort, built-in tools, user tools, tool calls, and generation prompts.
- [`tokenizer_config.json`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/tokenizer_config.json) and [`tokenizer.json`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/tokenizer.json): tokenizer class, special tokens, `o200k`-style vocabulary, and model input names.
- [`generation_config.json`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/generation_config.json): default sampling and stop-token IDs.
- [`model.safetensors.index.json`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/model.safetensors.index.json): 65,248,815,744-byte transformed tensor map across 15 shards.
- [`original/config.json`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/original/config.json), [`original/dtypes.json`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/original/dtypes.json), and [`original/model.safetensors.index.json`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/original/model.safetensors.index.json): original checkpoint metadata and seven original shards.
- [`metal/model.bin`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/metal/model.bin): large Metal-targeted artifact for Apple runtime paths.
- [`USAGE_POLICY`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/USAGE_POLICY) and [`LICENSE`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/LICENSE): policy and Apache-2.0 license files.
- [`openai/gpt-oss`](https://github.com/openai/gpt-oss/tree/7b583341fe16729127f6d5b94a7b09ccae97e1a1): reference source repository with torch, triton, vLLM, Metal, tools, examples, compatibility tests, and Responses API code.

## Layered architecture dissection
### High-level system shape
There are two connected objects here. The Hugging Face repo is the deployable artifact: files, config, tokenizer, templates, indexes, and weights. The GitHub repo is the reference implementation and integration lab: educational PyTorch, optimized Triton, Metal, vLLM wrapper, tool servers, chat app, examples, evals, and compatibility tests.

That split is practical. A production stack may never run [`gpt_oss/torch/model.py`](https://github.com/openai/gpt-oss/blob/7b583341fe16729127f6d5b94a7b09ccae97e1a1/gpt_oss/torch/model.py), but it should understand the same math and prompt protocol. A serving wrapper may download from [`openai/gpt-oss-120b`](https://huggingface.co/openai/gpt-oss-120b/tree/b5c939de8f754692c1647ca79fbf85e8c1e70f8a), compile its own kernels, and still use [`chat_template.jinja`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/chat_template.jinja) as the real interface contract.

### Main layers
**1. Hub packaging layer**  
The root HF files identify the artifact as `transformers` text generation. [`README.md`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/README.md) gives runnable examples for Transformers, vLLM, Ollama, and LM Studio. [`generation_config.json`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/generation_config.json) lists `do_sample: true` and stop IDs `200002`, `199999`, and `200012`.

**2. Architecture and quantization layer**  
[`config.json`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/config.json) declares the deployable architecture: 36 layers, `layer_types` alternating `sliding_attention` and `full_attention`, `sliding_window` 128, `max_position_embeddings` 131072, `rope_scaling` factor 32, 128 local experts, and top-4 expert routing. The `quantization_config` says MoE weights are MXFP4 while attention, router, embeddings, and `lm_head` remain outside conversion.

**3. Weight layout layer**  
[`model.safetensors.index.json`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/model.safetensors.index.json) maps transformed tensor names such as `model.layers.*.mlp.experts.gate_up_proj_blocks`, `gate_up_proj_scales`, `down_proj_blocks`, router weights, attention weights, embeddings, norm, and `lm_head` into 15 safetensor shards. The original variant under [`original`](https://huggingface.co/openai/gpt-oss-120b/tree/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/original) keeps a separate seven-shard index.

**4. Reference model layer**  
[`gpt_oss/torch/model.py`](https://github.com/openai/gpt-oss/blob/7b583341fe16729127f6d5b94a7b09ccae97e1a1/gpt_oss/torch/model.py) defines `ModelConfig`, RMSNorm, RoPE with YaRN-style scaling, sliding attention on alternating layers, `MLPBlock`, and the full `Transformer`. The PyTorch `MLPBlock` gates tokens over experts, takes top-k experts, softmaxes expert weights, runs two expert MLP projections with SwiGLU, all-reduces sharded intermediate outputs, and combines expert outputs by gate weight.

**5. Optimized MoE layer**  
[`gpt_oss/triton/moe.py`](https://github.com/openai/gpt-oss/blob/7b583341fe16729127f6d5b94a7b09ccae97e1a1/gpt_oss/triton/moe.py) shows the faster shape: route with `triton_kernels.routing`, use `matmul_ogs`, pass MXFP4 scales through `PrecisionConfig`, optionally fuse `swiglu`, and scatter weighted expert outputs back. The file is short because most speed lives in imported Triton kernels, which is exactly the production lesson.

**6. Harmony/tokenization layer**  
[`chat_template.jinja`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/chat_template.jinja) compiles conversation state into the model's expected token format. [`gpt_oss/tokenizer.py`](https://github.com/openai/gpt-oss/blob/7b583341fe16729127f6d5b94a7b09ccae97e1a1/gpt_oss/tokenizer.py) defines `o200k_harmony` by extending `o200k_base` with special tokens for start/end, channel, message, return, constrain, and call. [`tokenizer_config.json`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/tokenizer_config.json) mirrors those special tokens for standard HF tooling.

**7. Serving, tools, and examples layer**  
The source repo includes [`gpt_oss/generate.py`](https://github.com/openai/gpt-oss/blob/7b583341fe16729127f6d5b94a7b09ccae97e1a1/gpt_oss/generate.py) for model-parallel demo generation, [`gpt_oss/vllm/token_generator.py`](https://github.com/openai/gpt-oss/blob/7b583341fe16729127f6d5b94a7b09ccae97e1a1/gpt_oss/vllm/token_generator.py) for vLLM integration, [`gpt_oss/responses_api`](https://github.com/openai/gpt-oss/tree/7b583341fe16729127f6d5b94a7b09ccae97e1a1/gpt_oss/responses_api) for Responses-style events, and [`gpt-oss-mcp-server`](https://github.com/openai/gpt-oss/tree/7b583341fe16729127f6d5b94a7b09ccae97e1a1/gpt-oss-mcp-server) for reference browser/python tools.

### Inference / data / control flow
A caller starts with messages, optional tools, optional built-in `browser` or `python`, model identity, and `reasoning_effort`. [`chat_template.jinja`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/chat_template.jinja) renders a system message, available tools, valid channels, developer/user/assistant turns, tool calls, and final generation prompt. [`tokenizer_config.json`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/tokenizer_config.json) and [`gpt_oss/tokenizer.py`](https://github.com/openai/gpt-oss/blob/7b583341fe16729127f6d5b94a7b09ccae97e1a1/gpt_oss/tokenizer.py) define the special token IDs used by that rendered prompt.

The model then runs alternating attention and MoE blocks. In the reference PyTorch implementation, [`AttentionBlock`](https://github.com/openai/gpt-oss/blob/7b583341fe16729127f6d5b94a7b09ccae97e1a1/gpt_oss/torch/model.py) builds Q/K/V, applies RoPE, includes attention sinks, and uses sliding attention for even layers. [`MLPBlock`](https://github.com/openai/gpt-oss/blob/7b583341fe16729127f6d5b94a7b09ccae97e1a1/gpt_oss/torch/model.py) normalizes, routes over 128 experts, selects 4, computes expert SwiGLU projections, and weighted-sums them. In the Triton path, [`gpt_oss/triton/moe.py`](https://github.com/openai/gpt-oss/blob/7b583341fe16729127f6d5b94a7b09ccae97e1a1/gpt_oss/triton/moe.py) performs the same conceptual flow with specialized routing and grouped matmul kernels.

If using the reference Responses surface, events are represented by models in [`gpt_oss/responses_api/events.py`](https://github.com/openai/gpt-oss/blob/7b583341fe16729127f6d5b94a7b09ccae97e1a1/gpt_oss/responses_api/events.py): output text deltas, reasoning deltas, output item events, web-search events, code-interpreter events, and completion. This matters because gpt-oss is not just next-token text; the intended product surface includes reasoning traces and tool actions.

## Key files, configs, cards, and artifacts
- [`README.md`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/README.md): card, examples, model-family description, reasoning levels, tool-use claims, and source links.
- [`config.json`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/config.json): architecture and quantization source of truth.
- [`chat_template.jinja`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/chat_template.jinja): the artifact file I would test first in any gateway integration.
- [`tokenizer_config.json`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/tokenizer_config.json): special token metadata and tokenizer class for HF clients.
- [`generation_config.json`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/generation_config.json): stop tokens and default sampling behavior.
- [`model.safetensors.index.json`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/model.safetensors.index.json): tensor-to-shard map and transformed model size.
- [`original/config.json`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/original/config.json): compact original config with `num_experts`, `experts_per_token`, RoPE, sliding window, and hidden sizes.
- [`gpt_oss/torch/model.py`](https://github.com/openai/gpt-oss/blob/7b583341fe16729127f6d5b94a7b09ccae97e1a1/gpt_oss/torch/model.py): readable reference architecture and generation loop.
- [`gpt_oss/torch/weights.py`](https://github.com/openai/gpt-oss/blob/7b583341fe16729127f6d5b94a7b09ccae97e1a1/gpt_oss/torch/weights.py): MXFP4 checkpoint reader and dequantization logic.
- [`gpt_oss/triton/moe.py`](https://github.com/openai/gpt-oss/blob/7b583341fe16729127f6d5b94a7b09ccae97e1a1/gpt_oss/triton/moe.py): optimized routing/fused-MoE shape.
- [`gpt_oss/tokenizer.py`](https://github.com/openai/gpt-oss/blob/7b583341fe16729127f6d5b94a7b09ccae97e1a1/gpt_oss/tokenizer.py): `o200k_harmony` tokenizer construction.
- [`gpt_oss/responses_api/events.py`](https://github.com/openai/gpt-oss/blob/7b583341fe16729127f6d5b94a7b09ccae97e1a1/gpt_oss/responses_api/events.py): concrete event classes for text, reasoning, web search, code interpreter, and completion events.

## Important components
[`config.json`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/config.json) is the first component because it tells you what a server is actually hosting: sparse MoE, top-4 routing, MXFP4 MoE weights, full/sliding attention alternation, GQA-style 64 attention heads with 8 KV heads, long context, and explicit stop/pad token IDs.

[`chat_template.jinja`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/chat_template.jinja) is the second. It renders TypeScript-style tool schemas, built-in browser/python tools, model identity, reasoning effort, channels, assistant analysis/final turns, tool calls, and generation prompts. This is where "agentic capabilities" become a concrete serialization contract.

[`gpt_oss/torch/model.py`](https://github.com/openai/gpt-oss/blob/7b583341fe16729127f6d5b94a7b09ccae97e1a1/gpt_oss/torch/model.py) is the readable math. Its `MLPBlock` makes the sparse routing easy to inspect: route, top-k, softmax weights, expert MLP1, SwiGLU, expert MLP2, optional all-reduce, weighted sum, residual.

[`gpt_oss/torch/weights.py`](https://github.com/openai/gpt-oss/blob/7b583341fe16729127f6d5b94a7b09ccae97e1a1/gpt_oss/torch/weights.py) is the quantization explainer. It maps parameter names, opens safetensors lazily, reads blocks and scales, expands low/high nibbles through an FP4 lookup table, and uses `torch.ldexp` with scale exponents.

[`gpt_oss/triton/moe.py`](https://github.com/openai/gpt-oss/blob/7b583341fe16729127f6d5b94a7b09ccae97e1a1/gpt_oss/triton/moe.py) is the performance sketch. It shows the production-facing shape more honestly than a long prose claim: routing, grouped matmul, MX scale layouts, fused activation, scatter, and gate scaling.

## Important knobs / configs / extension points
- [`chat_template.jinja`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/chat_template.jinja): `reasoning_effort`, `builtin_tools`, `model_identity`, tool schemas, channels, and generation prompt behavior.
- [`config.json`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/config.json): `num_local_experts`, `num_experts_per_tok`, `layer_types`, `sliding_window`, `rope_scaling`, `max_position_embeddings`, and `quantization_config`.
- [`generation_config.json`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/generation_config.json): `do_sample`, `bos_token_id`, and the three EOS/stop token IDs.
- [`model.safetensors.index.json`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/model.safetensors.index.json): transformed shard layout, including expert `blocks` and `scales`.
- [`original`](https://huggingface.co/openai/gpt-oss-120b/tree/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/original): alternative checkpoint format for code paths that expect the original naming and index.
- [`gpt_oss/generate.py`](https://github.com/openai/gpt-oss/blob/7b583341fe16729127f6d5b94a7b09ccae97e1a1/gpt_oss/generate.py): backend selector for `torch`, `triton`, and `vllm`.
- [`pyproject.toml`](https://github.com/openai/gpt-oss/blob/7b583341fe16729127f6d5b94a7b09ccae97e1a1/pyproject.toml): optional dependency split for `torch`, `triton`, `metal`, `test`, and `eval`.
- [`compatibility-test`](https://github.com/openai/gpt-oss/tree/7b583341fe16729127f6d5b94a7b09ccae97e1a1/compatibility-test): provider compatibility cases for chat/tool behavior.

## Practical questions and answers
**Is this enough to reproduce training?**  
No. [`openai/gpt-oss-120b`](https://huggingface.co/openai/gpt-oss-120b/tree/b5c939de8f754692c1647ca79fbf85e8c1e70f8a) gives weights and runtime metadata, and [`openai/gpt-oss`](https://github.com/openai/gpt-oss/tree/7b583341fe16729127f6d5b94a7b09ccae97e1a1) gives inference/source examples. It does not give the training corpus, training pipeline, or full evaluation reproduction.

**Is the model card enough for integration?**  
No. Read [`chat_template.jinja`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/chat_template.jinja), [`tokenizer_config.json`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/tokenizer_config.json), and [`generation_config.json`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/generation_config.json). Tool calls, reasoning channels, return/call tokens, and stop behavior are integration-critical.

**What is the actual sparse mechanism?**  
[`config.json`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/config.json) declares 128 local experts and 4 selected experts per token. [`gpt_oss/torch/model.py`](https://github.com/openai/gpt-oss/blob/7b583341fe16729127f6d5b94a7b09ccae97e1a1/gpt_oss/torch/model.py) shows the reference route/top-k/softmax/weighted-sum path. [`gpt_oss/triton/moe.py`](https://github.com/openai/gpt-oss/blob/7b583341fe16729127f6d5b94a7b09ccae97e1a1/gpt_oss/triton/moe.py) shows how the optimized path groups that work.

**Can ordinary hardware run the 120B artifact comfortably?**  
Not in the simple reference path. The card says the 120B model targets a single 80 GB GPU in optimized stacks, and [`gpt_oss/torch/model.py`](https://github.com/openai/gpt-oss/blob/7b583341fe16729127f6d5b94a7b09ccae97e1a1/gpt_oss/torch/model.py) explicitly describes the PyTorch implementation as educational. Consumer-local use is more realistic through smaller `gpt-oss-20b` or heavily optimized runtimes.

**What is easiest to get wrong?**  
The harmony protocol. If a serving framework treats the model as a generic causal LM and ignores [`chat_template.jinja`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/chat_template.jinja), it can produce subtly broken reasoning/tool behavior even when token generation works.

## What is smart
- The artifact exposes the protocol as code in [`chat_template.jinja`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/chat_template.jinja), not only prose.
- [`config.json`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/config.json) clearly marks which modules are kept out of MXFP4 conversion, which helps builders reason about quality and kernel requirements.
- [`gpt_oss/torch/model.py`](https://github.com/openai/gpt-oss/blob/7b583341fe16729127f6d5b94a7b09ccae97e1a1/gpt_oss/torch/model.py) is readable enough to serve as a reference oracle even if it is not production-fast.
- [`gpt_oss/triton/moe.py`](https://github.com/openai/gpt-oss/blob/7b583341fe16729127f6d5b94a7b09ccae97e1a1/gpt_oss/triton/moe.py) keeps the optimized MoE path short and inspectable by relying on specialized kernels instead of hiding the routing shape.
- [`gpt_oss/tokenizer.py`](https://github.com/openai/gpt-oss/blob/7b583341fe16729127f6d5b94a7b09ccae97e1a1/gpt_oss/tokenizer.py) makes the harmony special-token layer concrete and testable.
- The source repo includes [`compatibility-test`](https://github.com/openai/gpt-oss/tree/7b583341fe16729127f6d5b94a7b09ccae97e1a1/compatibility-test), which is the right instinct for a model meant to run across many providers and serving stacks.

## What is flawed or weak
- The HF artifact is not a full reproducibility package. [`README.md`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/README.md) links a model card and gives usage examples, but builders cannot reproduce training or independently audit data mixture from these files.
- The "fits on one 80 GB GPU" story depends on optimized runtimes. The educational path in [`gpt_oss/torch/model.py`](https://github.com/openai/gpt-oss/blob/7b583341fe16729127f6d5b94a7b09ccae97e1a1/gpt_oss/torch/model.py) is intentionally not the deployment path.
- [`chat_template.jinja`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/chat_template.jinja) is large and semantically loaded. That is good for explicitness, but gateways need snapshot tests because a tiny template mismatch can change tool or channel behavior.
- [`model.safetensors.index.json`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/model.safetensors.index.json) maps a large transformed format, while [`original`](https://huggingface.co/openai/gpt-oss-120b/tree/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/original) carries another naming/layout scheme. That is flexible, but it creates integration branches.
- Reasoning-trace access is powerful but operationally sensitive. Any product exposing or storing reasoning outputs from this model needs a deliberate policy, not just a pass-through.

## What we can learn / steal
- Treat a model release as a runtime contract, not just a blob of weights. The minimum study set here is [`config.json`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/config.json), [`chat_template.jinja`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/chat_template.jinja), [`tokenizer_config.json`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/tokenizer_config.json), and [`generation_config.json`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/generation_config.json).
- Keep reference math readable. [`gpt_oss/torch/model.py`](https://github.com/openai/gpt-oss/blob/7b583341fe16729127f6d5b94a7b09ccae97e1a1/gpt_oss/torch/model.py) is valuable even if nobody should benchmark it as the product.
- Put quantization mechanics where builders can inspect them. [`gpt_oss/torch/weights.py`](https://github.com/openai/gpt-oss/blob/7b583341fe16729127f6d5b94a7b09ccae97e1a1/gpt_oss/torch/weights.py) makes MXFP4 blocks and scales understandable.
- Separate protocol compatibility tests from pure model tests. [`compatibility-test`](https://github.com/openai/gpt-oss/tree/7b583341fe16729127f6d5b94a7b09ccae97e1a1/compatibility-test) is a pattern worth copying for tool-use models.
- Document when a path is educational. [`gpt_oss/generate.py`](https://github.com/openai/gpt-oss/blob/7b583341fe16729127f6d5b94a7b09ccae97e1a1/gpt_oss/generate.py) and the README distinguish demo/reference code from production serving expectations.

## How we could apply it
If we were integrating `gpt-oss-120b`, I would start with conformance tests around [`chat_template.jinja`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/chat_template.jinja). Feed it plain chat, developer messages, browser/python built-ins, custom function tools, tool responses, and prior assistant reasoning. Assert rendered markers and stop IDs before testing quality.

I would also keep separate deployment profiles for reference, optimized GPU, and provider-hosted use. [`gpt_oss/torch/model.py`](https://github.com/openai/gpt-oss/blob/7b583341fe16729127f6d5b94a7b09ccae97e1a1/gpt_oss/torch/model.py) is good for understanding, [`gpt_oss/triton/moe.py`](https://github.com/openai/gpt-oss/blob/7b583341fe16729127f6d5b94a7b09ccae97e1a1/gpt_oss/triton/moe.py) is closer to performance reality, and the HF card's vLLM/Ollama paths in [`README.md`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/README.md) are the practical starting points.

Finally, I would use [`model.safetensors.index.json`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/model.safetensors.index.json) and [`original/model.safetensors.index.json`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/original/model.safetensors.index.json) as explicit artifact-contract fixtures. A serving stack should fail loudly if expected expert block/scale names, shard counts, or special tokens drift.

## Bottom line
`openai/gpt-oss-120b` is worth studying because it is a modern open-weight model release with inspectable runtime contracts. The model is sparse, quantized, long-context, and tool/reasoning oriented, but the practical product is the alignment between [`config.json`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/config.json), [`chat_template.jinja`](https://huggingface.co/openai/gpt-oss-120b/blob/b5c939de8f754692c1647ca79fbf85e8c1e70f8a/chat_template.jinja), tokenizer metadata, safetensor indexes, and the reference source in [`openai/gpt-oss`](https://github.com/openai/gpt-oss/tree/7b583341fe16729127f6d5b94a7b09ccae97e1a1).

The reusable lesson is clear: for agentic models, weights are only one layer. The prompt template, special tokens, stop tokens, tool schema rendering, event surface, quantization layout, and serving backend together decide whether the release actually works.
