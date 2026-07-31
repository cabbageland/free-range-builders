# Inkling-Small

- Source: Hugging Face
- Artifact: model `thinkingmachines/Inkling-Small`
- URL: https://huggingface.co/thinkingmachines/Inkling-Small
- Date: 2026-07-31
- Snapshot studied: `main` @ `8cc5877b44d343f88b92086aa1fb72897950f06a`
- Why picked today: It appeared on the current Hugging Face trending models page when checked, and the model API showed 2,971 downloads and 185 likes. Unlike a lot of fresh frontier-model drops, this artifact exposes concrete builder-facing surfaces: the prompt contract, tokenizer markers, processor geometry, weight map, and per-benchmark eval files.

## Executive summary
`Inkling-Small` is not just "an open 12B-active multimodal MoE." The more interesting thing is the packaging contract around it: [`chat_template.jinja`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/chat_template.jinja) serializes reasoning effort, tool declarations, tool invocations, and multimodal placeholders; [`config.json`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/config.json) exposes a 42-layer decoder with 256 routed experts and 6 active experts per token; [`processor_config.json`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/processor_config.json) shows how images and audio are turned into the decoder's expected tokens; and [`model.safetensors.index.json`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/model.safetensors.index.json) reveals how the checkpoint is physically sharded.

The strongest idea is that the model's "agentic" behavior is not left implicit. [`chat_template.jinja`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/chat_template.jinja) literally injects a `Thinking effort level:` system message, emits `tool_declare` metadata as JSON, and expects tool calls to be serialized with `<|content_invoke_tool_json|>`. That is a real interface contract, not a vibes-only claim that the model can use tools.

The second useful signal is how much of the artifact is inspectable without custom repo code. [`README.md`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/README.md), [`config.json`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/config.json), [`tokenizer_config.json`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/tokenizer_config.json), [`processor_config.json`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/processor_config.json), and files under [`.eval_results`](https://huggingface.co/thinkingmachines/Inkling-Small/tree/main/.eval_results) together make the artifact far more dissectible than the average model-card-and-weight-dump release.

## What they built / released
They released a multimodal, tool-capable model package with a surprisingly legible public surface:

- [`README.md`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/README.md): task framing, architecture summary, deployment recipes, and benchmark layer.
- [`chat_template.jinja`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/chat_template.jinja): the real conversation serialization contract.
- [`config.json`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/config.json): text, vision, audio, and MTP architecture settings.
- [`processor_config.json`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/processor_config.json): image/audio preprocessing and placeholder-token mapping.
- [`tokenizer_config.json`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/tokenizer_config.json): special token inventory for roles, multimodal content, thinking, tool invocation, and delimiters.
- [`model.safetensors.index.json`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/model.safetensors.index.json) plus the [32 BF16 weight shards](https://huggingface.co/thinkingmachines/Inkling-Small/tree/main): physical checkpoint layout.
- [`.eval_results`](https://huggingface.co/thinkingmachines/Inkling-Small/tree/main/.eval_results), including [`swe-bench_verified.yaml`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/.eval_results/swe-bench_verified.yaml): benchmark manifest layer.

## Why it matters
This artifact matters because it exposes the pieces a builder actually needs:

1. The prompt and tool-call grammar.
2. The multimodal processor geometry and token mapping.
3. The model's architectural knobs and routing choices.
4. A visible eval-manifest layer instead of only a screenshot of benchmark bars.

## Artifact shape at a glance
The artifact is large in bytes but compact in concepts:

- [`README.md`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/README.md): top-level explanation and benchmark narrative.
- [`chat_template.jinja`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/chat_template.jinja): message packing logic.
- [`config.json`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/config.json): decoder/MoE/vision/audio shape.
- [`processor_config.json`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/processor_config.json): feature extractor and image processor settings.
- [`tokenizer_config.json`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/tokenizer_config.json): special-token surface.
- [`model.safetensors.index.json`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/model.safetensors.index.json): mapping from named tensors to shards.
- [`.eval_results`](https://huggingface.co/thinkingmachines/Inkling-Small/tree/main/.eval_results): per-benchmark YAML files like [`swe-bench_verified.yaml`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/.eval_results/swe-bench_verified.yaml).

## Layered architecture dissection
### High-level system shape
The system shape is: chat-style messages plus optional tools plus image/audio inputs are serialized into a custom token grammar, the processor turns non-text modalities into the expected feature/placeholder representation, the multimodal decoder consumes everything in one shared hidden space, and assistant output can come back as ordinary text, explicit reasoning content, or structured tool-call JSON.

This is less "general AI model with some docs" and more "multimodal agent protocol with weights attached."

### Main layers
**1. Product and benchmark layer**  
[`README.md`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/README.md) gives the high-level pitch: a general-purpose multimodal model, 276B total parameters, 12B active, open weights, multiple deployment recipes, and benchmark claims. It is partly marketing, but still useful because it lists the intended workloads and deployment surfaces.

**2. Conversation-contract layer**  
[`chat_template.jinja`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/chat_template.jinja) is the most important file. It maps `reasoning_effort` strings like `minimal`, `medium`, `high`, and `max` into numeric effort levels, injects them as a system message, serializes tool specs under `tool_declare`, emits assistant reasoning with `<|content_thinking|>`, and formats tool calls as strict JSON objects under `<|content_invoke_tool_json|>`. That is the public contract for tool use and reasoning, not a hidden server behavior.

**3. Backbone-config layer**  
[`config.json`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/config.json) reveals a specific architectural taste: 42 decoder layers, hidden size `4096`, context length `1048576`, local-layer bias for most layers, sliding window size `512`, 256 routed experts with 6 experts active per token, 2 shared experts, and an `mtp_config` block for next-token-prediction helper layers. This is a model trying to win with routing and sequence engineering, not with dense brute force.

**4. Multimodal preprocessing layer**  
[`processor_config.json`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/processor_config.json) shows how modalities hit the model. Audio uses 16 kHz features, 80 mel bins, and 0.05-second token duration. Images use an `InklingImageProcessor` with `40x40` size metadata, normalization stats, and explicit `<|content_image|>` / `<|unused_200054|>` placeholder mapping. The key point is not the exact numbers. The key point is that the artifact exposes them at all.

**5. Token-surface layer**  
[`tokenizer_config.json`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/tokenizer_config.json) exposes the role and content markers: `<|message_user|>`, `<|message_model|>`, `<|message_system|>`, `<|message_tool|>`, `<|content_text|>`, `<|content_image|>`, `<|content_audio_input|>`, `<|content_thinking|>`, and `<|content_model_end_sampling|>`. This is a model with an explicit protocol vocabulary.

**6. Packaging and eval layer**  
[`model.safetensors.index.json`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/model.safetensors.index.json) maps named tensors across 32 BF16 shard files and reports total checkpoint size. [`.eval_results`](https://huggingface.co/thinkingmachines/Inkling-Small/tree/main/.eval_results) gives benchmark entries like [`swe-bench_verified.yaml`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/.eval_results/swe-bench_verified.yaml), which is a much better builder-facing habit than burying all eval evidence inside one giant README table.

### Inference / data / control flow
1. The caller builds a standard chat-style message list as described by [`README.md`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/README.md).
2. [`chat_template.jinja`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/chat_template.jinja) injects reasoning effort, optional tool declarations, and per-role content markers.
3. Image and audio parts are serialized as modality placeholders and then processed according to [`processor_config.json`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/processor_config.json).
4. The decoder described in [`config.json`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/config.json) consumes the mixed stream using hybrid attention plus sparse MoE routing.
5. If the assistant decides to use tools, the template expects a JSON object under `<|content_invoke_tool_json|>` rather than free-form prose.
6. The generated output ends with `<|content_model_end_sampling|>`, and the tokenizer/config surface tells downstream code how to interpret the result.

## Key files, configs, cards, and artifacts
- [`README.md`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/README.md): the top-level product story and benchmark layer.
- [`chat_template.jinja`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/chat_template.jinja): the single best file for understanding behavior.
- [`config.json`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/config.json): the actual architecture statement.
- [`processor_config.json`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/processor_config.json): image/audio preprocessing contract.
- [`tokenizer_config.json`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/tokenizer_config.json): protocol token vocabulary.
- [`model.safetensors.index.json`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/model.safetensors.index.json): checkpoint layout and tensor-to-shard mapping.
- [`swe-bench_verified.yaml`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/.eval_results/swe-bench_verified.yaml): concrete example of the eval-manifest layer.

## Important components
The most important component is [`chat_template.jinja`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/chat_template.jinja). It turns "this model can reason and use tools" from a slogan into an inspectable token grammar.

The second is [`config.json`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/config.json). That file tells you this is a sparse multimodal decoder with deliberate attention and expert-routing choices, not just a random checkpoint blob.

The third is [`processor_config.json`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/processor_config.json). That is where the artifact becomes a real multimodal package instead of a text-only chat model wearing a multimodal badge.

The fourth is [`model.safetensors.index.json`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/model.safetensors.index.json). Most model notes ignore the physical layout, but builders should care because deployment, sharding, and storage costs start there.

## Important knobs / configs / extension points
- `reasoning_effort` in [`chat_template.jinja`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/chat_template.jinja) is a first-class behavior knob.
- Tool declaration and tool-call JSON format also live in [`chat_template.jinja`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/chat_template.jinja).
- `num_hidden_layers`, `local_layer_ids`, `sliding_window_size`, `n_routed_experts`, `num_experts_per_tok`, and `n_shared_experts` live in [`config.json`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/config.json).
- Audio feature parameters and image placeholder wiring live in [`processor_config.json`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/processor_config.json).
- Special message/content tokens live in [`tokenizer_config.json`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/tokenizer_config.json).
- The packaging boundary lives in [`model.safetensors.index.json`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/model.safetensors.index.json).

## Practical questions and answers
**Is the "agentic" part real or just benchmark theater?**  
It looks real at the artifact level. [`chat_template.jinja`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/chat_template.jinja) explicitly supports tool declaration and tool-call emission instead of implying those behaviors through hidden serving code.

**Is the multimodality real or just one image token in the README?**  
It looks real at the packaging layer. [`config.json`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/config.json) includes separate vision and audio config blocks, and [`processor_config.json`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/processor_config.json) exposes both image and audio preprocessing.

**What should a builder read first?**  
Read [`chat_template.jinja`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/chat_template.jinja), then [`config.json`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/config.json), then [`processor_config.json`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/processor_config.json), [`tokenizer_config.json`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/tokenizer_config.json), and one eval manifest like [`swe-bench_verified.yaml`](https://huggingface.co/thinkingmachines/Inkling-Small/blob/main/.eval_results/swe-bench_verified.yaml).

**What is the most reusable move here?**  
Expose the model's real prompt grammar, preprocessing contract, and eval manifests as public files rather than burying them in private serving code.

## What is smart
- Treating reasoning effort as a concrete serialized input rather than a fuzzy inference hint.
- Making tool declaration and tool invocation part of the model's visible chat grammar.
- Exposing multimodal processor settings and token markers directly in the artifact.
- Publishing eval manifests and weight-map metadata instead of only a leaderboard-style README.

## What is flawed or weak
- The README is still benchmark-heavy and somewhat marketing-forward.
- There is no custom modeling Python in the artifact, so some implementation details remain opaque.
- The BF16 package is enormous in storage terms even though only 12B parameters are active per token.
- The custom token grammar is powerful, but it also means integrations must respect a fairly specific template contract.

## What we can learn / steal
- Publish the real prompt and tool-call contract, not just weights and a brag sheet.
- Expose preprocessing details so downstream builders can reason about failure modes.
- Make eval artifacts inspectable file-by-file.
- Treat model packaging as part of product design, not an afterthought.

## How we could apply it
If we release our own model artifacts, I would copy the contract transparency here: ship the template, the processor config, the tokenizer surface, the shard index, and at least some structured eval manifests. I would also copy the habit of making tool-use grammar explicit instead of expecting downstream users to reverse-engineer it from a hosted API.

## Bottom line
`thinkingmachines/Inkling-Small` is worth studying because it is a model release that exposes the interface layer a serious builder actually needs: prompt grammar, multimodal processor surface, routing architecture, and eval evidence.

The builder lesson is that a useful open model is not only a checkpoint. It is the clarity of the contract around reasoning, tools, modalities, and packaging.
