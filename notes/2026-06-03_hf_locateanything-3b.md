# LocateAnything-3B

- Source: Hugging Face
- Artifact: model `nvidia/LocateAnything-3B`
- URL: https://huggingface.co/nvidia/LocateAnything-3B
- Date: 2026-06-03
- Snapshot studied: revision `7a81d810571dc5f244b2f0b6868128f24b1cbd85`, last modified 2026-05-27
- Why picked today: It was the top model by Hugging Face `trendingScore` when checked, with `trendingScore: 1042`, 1,170 likes, and 78,925 downloads. More importantly, it has inspectable custom Transformers code, model configs, processor code, generation utilities, assets, a demo Space, and a linked NVIDIA technical report.

## Executive summary
LocateAnything-3B is NVIDIA's 3B-parameter vision-language grounding model. It takes image plus text instructions and emits structured localization text: boxes, points, labels, and coordinate tokens. The release is interesting because the implementation does not just ship weights and a model card. It includes custom `trust_remote_code` modules for the model, image processor, multimodal processor, and generation path.

The core idea is Parallel Box Decoding. Instead of generating every coordinate token one by one, the model tries to predict a fixed block of box tokens in parallel. The Hugging Face code exposes three modes: `fast`, `slow`, and `hybrid`. The default hybrid path uses multi-token prediction first, then falls back to autoregressive decoding when a box pattern looks illegal or ambiguous.

The caveat: this is research/development software under a non-commercial NVIDIA license. It is not a casual drop-in for a commercial GUI agent or robotics product. It is also a custom-code model, so the first real operational instruction is: inspect the code before trusting it.

## What they built / released
They released a Hugging Face model repo containing:
- the model card in [`README.md`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/README.md)
- license terms in [`LICENSE`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/LICENSE)
- model config in [`config.json`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/config.json)
- processor config in [`processor_config.json`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/processor_config.json)
- custom config code in [`configuration_locateanything.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/configuration_locateanything.py) and [`configuration_qwen2.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/configuration_qwen2.py)
- custom model code in [`modeling_locateanything.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/modeling_locateanything.py), [`modeling_qwen2.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/modeling_qwen2.py), and [`modeling_vit.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/modeling_vit.py)
- custom processor/image code in [`processing_locateanything.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/processing_locateanything.py) and [`image_processing_locateanything.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/image_processing_locateanything.py)
- generation helpers in [`generate_utils.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/generate_utils.py), [`mask_magi_utils.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/mask_magi_utils.py), and [`mask_sdpa_utils.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/mask_sdpa_utils.py)
- two sharded BF16 safetensor files plus [`model.safetensors.index.json`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/model.safetensors.index.json)
- tokenizer files like [`tokenizer_config.json`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/tokenizer_config.json), [`vocab.json`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/vocab.json), [`merges.txt`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/merges.txt), and [`special_tokens_map.json`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/special_tokens_map.json)
- assets under [`assets/`](https://huggingface.co/nvidia/LocateAnything-3B/tree/main/assets)

The model card links the demo at [`nvidia/LocateAnything`](https://huggingface.co/spaces/nvidia/LocateAnything), the upstream code area at [`NVlabs/Eagle/tree/main/Embodied`](https://github.com/NVlabs/Eagle/tree/main/Embodied), the paper [`arXiv:2605.27365`](https://arxiv.org/abs/2605.27365), and the NVIDIA research page.

## Why it matters
Grounding is becoming one of the key missing pieces for practical multimodal agents. A model that can answer "click the blue export button," "find all damaged parts," "locate every table header," or "point to the object matching this phrase" is more operationally useful than a model that only captions an image.

LocateAnything is interesting because it attacks both quality and decoding speed. Traditional vision-language grounding often serializes coordinates into text and pays the autoregressive cost for every coordinate token. This release tries to make bounding boxes more like structured units: predict the whole block in parallel when confidence is high, then repair by falling back to autoregressive mode when needed.

That matters for GUI agents, robotics, industrial inspection, document AI, and dataset annotation. It also matters as a pattern: when an LLM emits structured outputs, maybe the decoding algorithm should know the output structure instead of treating everything as generic text.

## Artifact shape at a glance
The Hugging Face repo is not just a weight drop:
- [`README.md`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/README.md) is a long model card with use cases, license, architecture, input/output format, evaluation tables, inference code, and deployment notes
- [`config.json`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/config.json) declares `LocateAnythingForConditionalGeneration`, a MoonViT vision config, a Qwen2.5-3B text config, special coordinate/box token IDs, a `block_size` of 6, and `_attn_implementation: "magi"`
- [`processor_config.json`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/processor_config.json) declares the processor class, image/video placeholders, the `<IMG_CONTEXT>` token, patch size 14, and merge kernel size `[2, 2]`
- [`modeling_locateanything.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/modeling_locateanything.py) wires MoonViT visual features into a Qwen language model via an MLP projector and overrides generation
- [`generate_utils.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/generate_utils.py) handles top-p/top-k sampling, repetition penalty, box validation, weighted coordinate decoding, point/box pattern handling, and hybrid fallback signaling
- [`image_processing_locateanything.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/image_processing_locateanything.py) resizes, pads, normalizes, and patchifies images into patch tokens
- [`processing_locateanything.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/processing_locateanything.py) handles images, videos, LMDB-backed data, URLs, base64 images, frame sampling, and chat-template assembly
- [`model.safetensors.index.json`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/model.safetensors.index.json) maps parameters into two safetensor shards with about 7.66 GB total storage

The repo is structurally rich enough to inspect like source code, not merely consume like an endpoint.

## Layered architecture dissection
### High-level system shape
The model stack is:
1. image/video inputs enter through [`processing_locateanything.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/processing_locateanything.py)
2. images are resized, padded, normalized, and patchified by [`image_processing_locateanything.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/image_processing_locateanything.py)
3. MoonViT visual embeddings are produced by the vision backbone in [`modeling_vit.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/modeling_vit.py)
4. [`modeling_locateanything.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/modeling_locateanything.py) projects visual features through an MLP into the Qwen hidden size and inserts them at image token positions
5. the Qwen language model in [`modeling_qwen2.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/modeling_qwen2.py) generates structured text containing references, boxes, points, and coordinate tokens
6. [`generate_utils.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/generate_utils.py) interprets fixed-length generation frames and decides whether to keep parallel decoding, switch to autoregressive decoding, or terminate

### Main layers
**1. Config and auto-map layer**
[`config.json`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/config.json) registers:
- `AutoConfig` to [`configuration_locateanything.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/configuration_locateanything.py)
- `AutoModel` to [`modeling_locateanything.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/modeling_locateanything.py)
- a MoonViT vision config
- a Qwen2 text config
- special tokens for boxes, references, coordinates, masks, image context, and null/switch behavior

This is why loading the model requires `trust_remote_code=True`. The model is not using a vanilla Transformers class.

**2. Vision preprocessing layer**
[`image_processing_locateanything.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/image_processing_locateanything.py) turns images into patch tensors. It rescales images if the patch-token count would exceed an input token limit, pads/resizes to a multiple of merge kernel times patch size, rejects grids too large for positional embeddings, and returns both `pixel_values` and `image_grid_hws`.

The code is simple, but it is central. Grounding quality depends heavily on preserving enough spatial resolution while keeping token counts under control.

**3. Multimodal processor layer**
[`processing_locateanything.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/processing_locateanything.py) is broader than a normal image wrapper. It supports local paths, URLs, base64 images, PIL images, LMDB-backed image data, and video frame sampling through decord or torchvision. It also applies chat templates and processes vision info from multimodal message objects.

That breadth suggests the model was trained and served in a data-heavy environment, not just a notebook demo.

**4. Model fusion layer**
[`modeling_locateanything.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/modeling_locateanything.py) defines `LocateAnythingForConditionalGeneration`. The core fusion step is easy to read: visual features are extracted once, passed through `mlp1`, and written into the language model embeddings where `input_ids == image_token_index`.

The MLP is small but important: LayerNorm over `vit_hidden_size * 4`, a linear projection into the LLM hidden size, GELU, and another linear layer.

**5. Structured generation layer**
[`modeling_locateanything.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/modeling_locateanything.py) overrides `generate()`. It asserts batch size 1 and `use_cache=True`, then supports:
- `fast`: multi-token prediction only
- `slow`: pure autoregressive decoding
- `hybrid`: multi-token prediction first, fallback to autoregressive decoding on illegal/ambiguous boxes, then switch back after a box end

The default hybrid path is the key implementation idea. It is not just "generate text faster." It is "generate structured box frames faster, but recover when structure confidence breaks."

**6. Attention mask layer**
[`mask_magi_utils.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/mask_magi_utils.py) and [`mask_sdpa_utils.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/mask_sdpa_utils.py) implement the attention-range machinery for block-style decoding. The config prefers MagiAttention via `_attn_implementation: "magi"`, but the model card says it falls back to PyTorch SDPA when MagiAttention is unavailable.

### Inference / data / control flow
A typical inference flow:
1. Load tokenizer, processor, and model with `trust_remote_code=True` as shown in [`README.md`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/README.md).
2. Wrap an image and text prompt into chat messages.
3. [`processing_locateanything.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/processing_locateanything.py) applies the chat template and gathers image/video inputs.
4. [`image_processing_locateanything.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/image_processing_locateanything.py) emits patch tensors and image grid sizes.
5. [`modeling_locateanything.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/modeling_locateanything.py) extracts visual features, injects them into token embeddings, and enters generation.
6. In `hybrid` mode, generation creates six-token future frames with mask tokens, samples/decodes candidate box structures via [`generate_utils.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/generate_utils.py), and falls back to autoregressive mode when `handle_pattern()` returns `error_box`.
7. The output is a text sequence with box or point tokens, for example `<box> x1, y1, x2, y2 </box>` style structures described in [`README.md`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/README.md).

## Key files, configs, cards, and artifacts
- [`README.md`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/README.md), model card, usage, evaluation, and worker sample
- [`LICENSE`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/LICENSE), non-commercial NVIDIA license terms
- [`config.json`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/config.json), architecture map, token IDs, MoonViT and Qwen configs
- [`processor_config.json`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/processor_config.json), processor class and image/video placeholder tokens
- [`modeling_locateanything.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/modeling_locateanything.py), model fusion and custom generation
- [`generate_utils.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/generate_utils.py), coordinate decoding, validation, sampling, and fallback classification
- [`mask_magi_utils.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/mask_magi_utils.py), MagiAttention range construction
- [`mask_sdpa_utils.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/mask_sdpa_utils.py), SDPA fallback mask utilities
- [`processing_locateanything.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/processing_locateanything.py), multimodal processor
- [`image_processing_locateanything.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/image_processing_locateanything.py), resize/pad/patchify logic
- [`modeling_vit.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/modeling_vit.py), MoonViT implementation
- [`modeling_qwen2.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/modeling_qwen2.py), Qwen language model code
- [`model.safetensors.index.json`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/model.safetensors.index.json), sharded parameter map
- [`trainer_state.json`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/trainer_state.json), training-state metadata
- [`assets/`](https://huggingface.co/nvidia/LocateAnything-3B/tree/main/assets), demo media and evaluation visuals

## Important components
**The six-token box block is the product idea**
[`config.json`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/config.json) sets `block_size` to 6 inside the Qwen text config, and [`generate_utils.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/generate_utils.py) treats a box frame as a fixed structure: start token, coordinates, end token, or padded variants for empty/point outputs.

**`generate()` is not stock Transformers generation**
[`modeling_locateanything.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/modeling_locateanything.py) overrides generation so it can append mask tokens, predict future structured tokens, maintain KV cache, and switch modes based on pattern validity.

**`handle_pattern()` is the format referee**
[`generate_utils.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/generate_utils.py) classifies generated frames as `coord_box`, `point_box`, `empty_box`, `ref_object`, `error_box`, or `im_end`. This is the practical guardrail that keeps a speed trick from becoming pure malformed text.

**The processor is a training/serving bridge**
[`processing_locateanything.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/processing_locateanything.py) includes LMDB and video support, not just PIL image support. That is a clue about the training and evaluation pipeline.

**The license is a real deployment constraint**
[`LICENSE`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/LICENSE) and [`README.md`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/README.md) frame this as research/development and non-commercial. Any builder using it in a product should stop there and read the terms.

## Important knobs / configs / extension points
- [`config.json`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/config.json) exposes token IDs for `box_start`, `box_end`, coordinate ranges, reference tokens, null tokens, image token, and switch/mask behavior.
- [`config.json`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/config.json) sets `max_position_embeddings` to 32768 and the model card says production prompt/image paths can use long contexts.
- [`processor_config.json`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/processor_config.json) defines image/video placeholder semantics and the `<IMG_CONTEXT>` token.
- [`image_processing_locateanything.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/image_processing_locateanything.py) uses `in_token_limit`, `patch_size`, and `merge_kernel_size` to control visual token count.
- [`modeling_locateanything.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/modeling_locateanything.py) exposes `generation_mode` as `fast`, `slow`, or `hybrid`.
- [`generate_utils.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/generate_utils.py) controls top-k/top-p, repetition penalty, `keep_k`, box validity thresholds, and abnormal-coordinate handling.
- [`mask_magi_utils.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/mask_magi_utils.py) and [`mask_sdpa_utils.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/mask_sdpa_utils.py) are the attention implementation extension points.

## Practical questions and answers
**Is this a detector or a VLM?**
It is a VLM specialized for grounding. It still emits text, but the text contains structured spatial outputs.

**What is the most reusable idea?**
Treat structured visual outputs as blocks during decoding. The model still lives in a language-model interface, but the generation code understands box/point structure.

**Why not just autoregressively generate boxes?**
You can. The `slow` mode does that. The reason to prefer `hybrid` is throughput: use parallel decoding for ordinary boxes, then fall back only when the pattern is uncertain.

**Is it a drop-in commercial GUI agent component?**
No. The license is non-commercial, and the code uses custom remote code. It is better treated as a research artifact and architecture reference unless NVIDIA grants the needed rights.

**What would I inspect before running it?**
At minimum: [`modeling_locateanything.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/modeling_locateanything.py), [`generate_utils.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/generate_utils.py), [`processing_locateanything.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/processing_locateanything.py), [`image_processing_locateanything.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/image_processing_locateanything.py), and [`LICENSE`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/LICENSE).

**What is likely brittle?**
The boundary between parallel and autoregressive decoding. If `handle_pattern()` and the confidence/validity thresholds are wrong for a domain, outputs can be malformed or slower than expected.

## What is smart
- Shipping the custom generation code instead of hiding the Parallel Box Decoding mechanism behind a black-box demo.
- Making `hybrid` the practical default: optimistic parallel decoding, guarded by autoregressive fallback.
- Keeping the model close to standard Transformers loading while using `auto_map` for the custom pieces.
- Including processor code that handles real training/serving surfaces: URLs, base64, local files, LMDB, videos, and frame sampling.
- Exposing enough config to understand the coordinate vocabulary and box-token contract.
- Being explicit that TensorRT/Triton support is not there yet, instead of pretending the release is production-inference polished.

## What is flawed or weak
- `trust_remote_code=True` is required. That is fine for research, but a serious deployment needs code review and pinning.
- Batch size is asserted to 1 in [`modeling_locateanything.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/modeling_locateanything.py), which limits high-throughput serving without additional work.
- The license blocks ordinary commercial product use.
- The model card's benchmark images are helpful but still model-card evidence. Builders need domain tests, especially for GUI, robotics, and documents.
- MagiAttention is recommended for speed but adds a specialized dependency path. SDPA fallback works, but the whole speed story depends on the runtime stack.
- The model weights are around 7.66 GB BF16, so this is not a tiny edge drop-in without quantization/distillation work.

## What we can learn / steal
- For structured generation, put structure into decoding, not only prompting.
- Use hybrid decoding when the output has a fast common case and a correctness-sensitive weird case.
- Keep coordinate tokens and box markers explicit in config so downstream tools can parse and validate outputs.
- Ship processor code that reflects real data modalities, not just a pretty notebook path.
- Make license/deployment constraints impossible to miss.

## How we could apply it
If we were building visual agents or document/GUI tooling, I would copy the pattern, not necessarily the model:
1. define a strict output grammar for boxes, points, and references,
2. add a validator that can reject malformed frames,
3. use fast structured decoding for obvious frames,
4. fall back to slower token-by-token decoding when confidence drops,
5. expose the output as parseable objects to the rest of the agent stack,
6. test per domain rather than trusting general grounding benchmarks.

For an internal agent UI, this could become the perception layer that turns screenshots into actionable targets. For a document pipeline, it could become a layout-grounding layer. For robotics, it is a useful pattern but needs far more safety validation than a model-card demo can provide.

## Bottom line
LocateAnything-3B is a strong Hugging Face pick because it reveals a concrete mechanism: structured parallel box decoding with hybrid fallback. That is more useful than another "vision model does grounding" headline.

The builder lesson is clean: when a model's output has shape, your decoder should know the shape. The sharp edge is also clean: custom-code, non-commercial, batch-1, GPU-oriented research releases belong in a lab notebook before they belong in production.
