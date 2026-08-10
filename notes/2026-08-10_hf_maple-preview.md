# Maple-Preview

- Source: Hugging Face
- Artifact: model `deepgrove/maple-preview`
- URL: https://huggingface.co/deepgrove/maple-preview
- Date: 2026-08-10
- Snapshot studied: `main` @ `ac1ddd79d2b5cb4406f5d2bebdf95406ce505a07`
- Why picked today: It appeared in the Hugging Face trending models API when checked, showing 307 likes, 1,344 downloads, and a `trendingScore` of 294. More importantly, the repo is unusually inspectable for a fresh model release: it ships the chat template, config, custom Transformers code, FlashAttention wrapper, and sharded weights instead of hiding behind a card and a benchmark table.

## Executive summary
`maple-preview` is a much better builder artifact than its marketing headline suggests. The real value is in the combination of [`README.md`](https://huggingface.co/deepgrove/maple-preview/blob/main/README.md), [`chat_template.jinja`](https://huggingface.co/deepgrove/maple-preview/blob/main/chat_template.jinja), [`config.json`](https://huggingface.co/deepgrove/maple-preview/blob/main/config.json), [`configuration_maple.py`](https://huggingface.co/deepgrove/maple-preview/blob/main/configuration_maple.py), [`modeling_maple.py`](https://huggingface.co/deepgrove/maple-preview/blob/main/modeling_maple.py), and [`fa3.py`](https://huggingface.co/deepgrove/maple-preview/blob/main/fa3.py). Together they show how DeepGrove packages a custom-code reasoning model with mixture-of-experts routing, a sliding/global attention schedule, and a tool-aware chat grammar.

The most useful insight is that the public artifact exposes both the software contract and the runtime assumptions. [`chat_template.jinja`](https://huggingface.co/deepgrove/maple-preview/blob/main/chat_template.jinja) shows exactly how `system`, `user`, `assistant`, and `tool` messages are serialized, including XML-ish `<tool_call>` wrappers and `<think>` reasoning spans. [`config.json`](https://huggingface.co/deepgrove/maple-preview/blob/main/config.json) reveals the actual architecture: 24 layers, 256 experts, 8 active experts per token, grouped-query attention, a 131,072-token context, and a scheduled mix of sliding and full attention.

The second useful insight is that the repo is honest in code even when the headline is slippery. The README advertises a "5.31 GB checkpoint" and 200+ tok/s on a Mac mini M4, but it also notes that the included Transformers path depends on Triton and FlashAttention and that the Apple Silicon result used a separate runtime. Meanwhile [`model.safetensors.index.json`](https://huggingface.co/deepgrove/maple-preview/blob/main/model.safetensors.index.json) says the published Hugging Face tensor set has a `total_size` of `40428060672`, about 40.4 GB of raw tensor footprint across nine shards. That discrepancy is exactly the kind of builder caveat worth capturing.

## What they built / released
They released a custom-code Hugging Face model repo with more than just weights:

- [`README.md`](https://huggingface.co/deepgrove/maple-preview/blob/main/README.md): release framing, claimed speed/performance, and deployment caveats.
- [`chat_template.jinja`](https://huggingface.co/deepgrove/maple-preview/blob/main/chat_template.jinja): the exact message and tool-call grammar.
- [`config.json`](https://huggingface.co/deepgrove/maple-preview/blob/main/config.json): the architectural truth.
- [`configuration_maple.py`](https://huggingface.co/deepgrove/maple-preview/blob/main/configuration_maple.py): custom `MapleConfig` class for `transformers`.
- [`modeling_maple.py`](https://huggingface.co/deepgrove/maple-preview/blob/main/modeling_maple.py): custom model, attention, gating, and MoE execution logic.
- [`fa3.py`](https://huggingface.co/deepgrove/maple-preview/blob/main/fa3.py): FlashAttention integration glue with version-sensitive feature detection.
- [`model.safetensors.index.json`](https://huggingface.co/deepgrove/maple-preview/blob/main/model.safetensors.index.json): nine-shard weight layout and total size.

## Why it matters
This artifact matters because it exposes the real packaging surface of a modern custom model release:

1. The prompt and tool protocol is published as source, not implied by a hosted API.
2. The architectural knobs are visible in a normal `transformers` config file.
3. The attention runtime is not hand-waved away; it has a concrete FlashAttention adapter.
4. The weight index makes operational cost explicit instead of hiding it behind a single benchmark graphic.

## Artifact shape at a glance
The artifact is structurally richer than a normal model-card-only release:

- [`README.md`](https://huggingface.co/deepgrove/maple-preview/blob/main/README.md): product story, speed claims, and caveats.
- [`assets`](https://huggingface.co/deepgrove/maple-preview/tree/main/assets): benchmark images and launch framing.
- [`chat_template.jinja`](https://huggingface.co/deepgrove/maple-preview/blob/main/chat_template.jinja): conversation wire format.
- [`config.json`](https://huggingface.co/deepgrove/maple-preview/blob/main/config.json) and [`configuration_maple.py`](https://huggingface.co/deepgrove/maple-preview/blob/main/configuration_maple.py): configuration contract and AutoConfig glue.
- [`modeling_maple.py`](https://huggingface.co/deepgrove/maple-preview/blob/main/modeling_maple.py): the real mechanics file.
- [`fa3.py`](https://huggingface.co/deepgrove/maple-preview/blob/main/fa3.py): low-level attention adapter for FlashAttention.
- [`model.safetensors.index.json`](https://huggingface.co/deepgrove/maple-preview/blob/main/model.safetensors.index.json): shard map.
- [`tokenizer.json`](https://huggingface.co/deepgrove/maple-preview/blob/main/tokenizer.json), [`tokenizer_config.json`](https://huggingface.co/deepgrove/maple-preview/blob/main/tokenizer_config.json), and [`vocab.json`](https://huggingface.co/deepgrove/maple-preview/blob/main/vocab.json): tokenizer contract.

## Layered architecture dissection
### High-level system shape
The public system shape is: serialize chat messages with a custom template, load a custom Maple config and model class through `transformers`, run grouped-query attention with alternating sliding and global windows, route tokens through a sparse expert stack, and rely on FlashAttention-backed kernels for the fast path.

### Main layers
**1. Release and positioning layer**  
[`README.md`](https://huggingface.co/deepgrove/maple-preview/blob/main/README.md) frames Maple as a 20B-A1B ternary-weight reasoning model with strong speed/performance claims. The useful part is not the benchmark chest-thumping. It is the note that the shipped Transformers implementation is CUDA-oriented and not the same path as the reported on-device runtime.

**2. Prompt-protocol layer**  
[`chat_template.jinja`](https://huggingface.co/deepgrove/maple-preview/blob/main/chat_template.jinja) is the cleanest file in the repo. It defines role serialization, optional tool exposure under `<tools>`, function call emission under `<tool_call>`, and reasoning output inside `<think>...</think>`. That makes the model's expected conversation structure inspectable instead of folkloric.

**3. Architecture-config layer**  
[`config.json`](https://huggingface.co/deepgrove/maple-preview/blob/main/config.json) is where the mechanism shows up. The model uses `hidden_size=2048`, `num_hidden_layers=24`, `num_attention_heads=16`, `num_key_value_heads=4`, `num_experts=256`, `num_experts_per_tok=8`, `max_position_embeddings=131072`, `sliding_window=512`, and a `layer_types` sequence that alternates three sliding-attention layers with one full-attention layer.

**4. Model-mechanics layer**  
[`configuration_maple.py`](https://huggingface.co/deepgrove/maple-preview/blob/main/configuration_maple.py) provides the `MapleConfig` type. [`modeling_maple.py`](https://huggingface.co/deepgrove/maple-preview/blob/main/modeling_maple.py) implements the actual behavior: `MapleGate` softmaxes routing scores and selects top-k experts, `MapleSparseMoeBlock` dispatches tokens across 256 experts, and `MapleAttention` switches between sliding-window and global attention depending on the layer schedule.

**5. Kernel-integration layer**  
[`fa3.py`](https://huggingface.co/deepgrove/maple-preview/blob/main/fa3.py) is a nice builder detail. It introspects the available FlashAttention function signature to see whether `window_size`, `deterministic`, and `softcap` kwargs are supported, then adapts the forward pass accordingly. That is a practical compatibility move, not just a benchmark trick.

### Inference / data / control flow
1. Messages are rendered with [`chat_template.jinja`](https://huggingface.co/deepgrove/maple-preview/blob/main/chat_template.jinja), including tool schemas and `<tool_call>` output when tools are enabled.
2. [`configuration_maple.py`](https://huggingface.co/deepgrove/maple-preview/blob/main/configuration_maple.py) registers `MapleConfig` so AutoConfig and AutoModel can resolve the custom classes.
3. [`config.json`](https://huggingface.co/deepgrove/maple-preview/blob/main/config.json) sets the alternating attention schedule, long context length, and sparse MoE knobs.
4. [`modeling_maple.py`](https://huggingface.co/deepgrove/maple-preview/blob/main/modeling_maple.py) runs grouped-query attention, applies rotary embeddings, and routes tokens to 8 of 256 experts through `MapleGate` and `MapleSparseMoeBlock`.
5. [`fa3.py`](https://huggingface.co/deepgrove/maple-preview/blob/main/fa3.py) chooses the FlashAttention fast path, including variable-length and sliding-window handling when available.

## Key files, configs, cards, and artifacts
- [`README.md`](https://huggingface.co/deepgrove/maple-preview/blob/main/README.md): release story plus deployment caveat.
- [`chat_template.jinja`](https://huggingface.co/deepgrove/maple-preview/blob/main/chat_template.jinja): the actual prompt/tool contract.
- [`config.json`](https://huggingface.co/deepgrove/maple-preview/blob/main/config.json): architecture and runtime knobs.
- [`configuration_maple.py`](https://huggingface.co/deepgrove/maple-preview/blob/main/configuration_maple.py): AutoConfig glue.
- [`modeling_maple.py`](https://huggingface.co/deepgrove/maple-preview/blob/main/modeling_maple.py): MoE and attention implementation.
- [`fa3.py`](https://huggingface.co/deepgrove/maple-preview/blob/main/fa3.py): FlashAttention adapter.
- [`model.safetensors.index.json`](https://huggingface.co/deepgrove/maple-preview/blob/main/model.safetensors.index.json): nine shards and 40.4 GB declared total size.

## Important components
The most important component is [`modeling_maple.py`](https://huggingface.co/deepgrove/maple-preview/blob/main/modeling_maple.py). That file proves this is a real custom-code release rather than a stock checkpoint with a renamed README.

The second is [`chat_template.jinja`](https://huggingface.co/deepgrove/maple-preview/blob/main/chat_template.jinja). It exposes the conversation grammar, which is often the most annoying missing piece in modern model drops.

The third is [`fa3.py`](https://huggingface.co/deepgrove/maple-preview/blob/main/fa3.py). It makes the runtime dependency story explicit and shows how much of the headline speed depends on specialized attention kernels.

The fourth is [`model.safetensors.index.json`](https://huggingface.co/deepgrove/maple-preview/blob/main/model.safetensors.index.json). That is the operational honesty file.

## Important knobs / configs / extension points
- [`config.json`](https://huggingface.co/deepgrove/maple-preview/blob/main/config.json): `num_experts=256`, `num_experts_per_tok=8`, `layer_types`, `sliding_window=512`, `max_position_embeddings=131072`, and `quantize=true`.
- [`chat_template.jinja`](https://huggingface.co/deepgrove/maple-preview/blob/main/chat_template.jinja): tool-call behavior, `<think>` behavior, and generation prompt framing.
- [`fa3.py`](https://huggingface.co/deepgrove/maple-preview/blob/main/fa3.py): FlashAttention compatibility handling for `window_size`, deterministic mode, and varlen execution.
- [`modeling_maple.py`](https://huggingface.co/deepgrove/maple-preview/blob/main/modeling_maple.py): top-k expert routing behavior and layer-specific sliding/global attention behavior.

## Practical questions and answers
**Does this artifact expose real implementation code or just a card?**  
It exposes real implementation code. [`configuration_maple.py`](https://huggingface.co/deepgrove/maple-preview/blob/main/configuration_maple.py), [`modeling_maple.py`](https://huggingface.co/deepgrove/maple-preview/blob/main/modeling_maple.py), and [`fa3.py`](https://huggingface.co/deepgrove/maple-preview/blob/main/fa3.py) are the main proof.

**What is the most reusable hidden detail?**  
Publish the chat template. [`chat_template.jinja`](https://huggingface.co/deepgrove/maple-preview/blob/main/chat_template.jinja) removes a whole category of downstream guesswork around roles, tool calls, and reasoning formatting.

**Is the public Hugging Face artifact the same thing as the 5.31 GB on-device story?**  
Not really. The README says the Apple Silicon speed result used a separate runtime, while [`model.safetensors.index.json`](https://huggingface.co/deepgrove/maple-preview/blob/main/model.safetensors.index.json) declares a much larger tensor footprint for the published HF shards. Builders should treat the Hugging Face repo as the inspectable reference implementation, not as proof that the same setup is lightweight on commodity hardware.

**What is the most interesting architectural move?**  
The scheduled attention pattern. [`config.json`](https://huggingface.co/deepgrove/maple-preview/blob/main/config.json) alternates three sliding-attention layers with one full-attention layer, which is a concrete attempt to trade global context cost against long-context throughput instead of running every layer the same way.

## What is smart
- Shipping the chat template, config, and custom model code together.
- Making the MoE routing policy explicit in code rather than hiding it in a paper.
- Using a version-tolerant FlashAttention wrapper instead of hard-coding one kernel interface.
- Publishing a model that is structurally inspectable even if the README is benchmark-heavy.

## What is flawed or weak
- The README headline can easily make builders underestimate the actual public artifact size and runtime demands.
- The shipped Transformers path depends on Triton and FlashAttention, so the friendly Apple Silicon headline is not the whole deployment story.
- The tool-call format uses custom XML-ish wrappers that downstream clients still need to learn.
- The README admits weak agentic post-training, so the release is more "reasoning checkpoint with useful source" than turnkey agent model.

## What we can learn / steal
- Always ship the chat template with the model.
- Put custom model code in the repo if the architecture is even slightly nonstandard.
- Expose kernel integration details when those details explain the performance claims.
- Be explicit about the difference between active-parameter efficiency and full artifact footprint.

## How we could apply it
If we release our own model artifacts, I would copy the packaging discipline here: publish the chat grammar, publish the custom config and model class, and publish the low-level runtime adapter if speed claims depend on it. I would also be even more explicit than this repo about the gap between benchmark headline and actual public deployment shape.

## Bottom line
`deepgrove/maple-preview` is worth studying because the useful part is not the benchmark image. The useful part is that the release exposes the prompt contract, architecture, MoE routing code, and kernel assumptions in one place.

The builder lesson is that a modern model artifact should ship its software contract with the weights, and that "fast small active model" claims need to be checked against the actual published shard layout.
