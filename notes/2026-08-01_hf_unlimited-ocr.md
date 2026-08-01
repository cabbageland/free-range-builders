# Unlimited-OCR

- Source: Hugging Face
- Artifact: model `baidu/Unlimited-OCR`
- URL: https://huggingface.co/baidu/Unlimited-OCR
- Date: 2026-08-01
- Snapshot studied: `main` @ `07dea832e22aefee32ad281d4b80551282e1c168`
- Why picked today: It appeared on the current Hugging Face trending models page when checked, and the model API already showed 2,457,387 downloads and 3,697 likes. Unlike a lot of fresh OCR drops, this artifact ships custom model code, preprocessing logic, PDF/multi-page paths, and even a pinned SGLang wheel.

## Executive summary
`Unlimited-OCR` is not just a model card claiming "long-horizon parsing." The useful thing is that the Hugging Face artifact exposes the whole serving contract: [`modeling_unlimitedocr.py`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/modeling_unlimitedocr.py) tiles large pages into local crops, keeps a global page view, injects image-token spans into the language prompt, disables the decoder sliding window during prefill, and can save model output back out as markdown plus boxed regions.

The strongest design move is the hybrid visual encoder path inside [`UnlimitedOCRModel`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/modeling_unlimitedocr.py). It builds both [`build_sam_vit_b`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/deepencoder.py) and [`build_clip_l`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/deepencoder.py), concatenates their features, projects them with [`MlpProjector`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/deepencoder.py), and then scatters the result directly into the decoder input embedding stream. That is a real multimodal mechanism, not a vague OCR badge.

The second strong move is operational honesty. [`README.md`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/README.md) includes transformer and vLLM usage, a custom SGLang recipe via [`wheel/sglang-0.0.0.dev11416+g92e8bb79e-py3-none-any.whl`](https://huggingface.co/baidu/Unlimited-OCR/tree/main/wheel), and separate single-page and multi-page entrypoints. The artifact reads more like a deployable OCR package than a naked checkpoint dump.

## What they built / released
They released a long-document OCR package with inspectable code and deployment surfaces:

- [`README.md`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/README.md): usage recipes for transformers, vLLM, and SGLang, plus PDF and multi-page examples.
- [`modeling_unlimitedocr.py`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/modeling_unlimitedocr.py): the core multimodal model, prompt packing, inference, and output postprocessing.
- [`deepencoder.py`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/deepencoder.py): CLIP/SAM-style visual backbones plus projector code.
- [`conversation.py`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/conversation.py): prompt-template layer adapted from FastChat-style conversations.
- [`config.json`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/config.json) and [`processor_config.json`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/processor_config.json): model and processor knobs.
- [`model.safetensors.index.json`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/model.safetensors.index.json): the weight map proving the checkpoint spans text, SAM, and vision-transformer parameters in one file.
- [`Unlimited-OCR.pdf`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/Unlimited-OCR.pdf): the paper packaged with the artifact instead of only linked externally.

## Why it matters
This artifact matters because most OCR releases still hide the real logic in private serving code. `Unlimited-OCR` exposes the pieces a builder actually needs to judge:

1. How large pages are tiled and tokenized.
2. How visual features are injected into the language model.
3. How multi-page parsing is serialized and decoded.
4. Which repetition guards and deployment shims are needed to keep the system sane.

## Artifact shape at a glance
The artifact is compact in file count but rich in builder-facing surfaces:

- [`README.md`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/README.md): top-level instructions and deployment variants.
- [`config.json`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/config.json): text MoE, projector, and vision settings.
- [`processor_config.json`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/processor_config.json): normalization, patch size, candidate resolutions, and processor class.
- [`modeling_unlimitedocr.py`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/modeling_unlimitedocr.py): inference pipeline and multimodal model implementation.
- [`deepencoder.py`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/deepencoder.py): CLIP/SAM encoders and projector implementation.
- [`conversation.py`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/conversation.py): prompt serialization rules.
- [`wheel`](https://huggingface.co/baidu/Unlimited-OCR/tree/main/wheel): pinned SGLang build for the recommended serving path.

## Layered architecture dissection
### High-level system shape
The system shape is: a prompt containing `<image>` is converted into a plain conversation template, the input page is optionally tiled into multiple local crops plus one global view, SAM and CLIP-style encoders produce visual features, a linear projector maps them into the decoder embedding width, those embeddings are scattered into the language-model token stream, and generation returns markdown-like OCR output that can optionally be postprocessed into bounding-box overlays and extracted image crops.

This is much closer to "document parser with a language-model decoder" than to classic OCR.

### Main layers
**1. Product and deployment layer**  
[`README.md`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/README.md) is operationally useful, not just narrative. It includes transformer inference, multi-page PDF conversion, vLLM recipes, and a custom SGLang path using the bundled wheel.

**2. Prompt and conversation layer**  
[`conversation.py`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/conversation.py) and `format_messages(...)` in [`modeling_unlimitedocr.py`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/modeling_unlimitedocr.py) define how user/assistant turns are serialized. The artifact is not using generic chat formatting by accident; it has a specific prompt contract around `<image>` and DeepSeek-style delimiters.

**3. Image preprocessing and packing layer**  
[`dynamic_preprocess`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/modeling_unlimitedocr.py) slices pages into a grid of local crops chosen by aspect ratio, while [`processor_config.json`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/processor_config.json) pins patch size `16`, downsample ratio `4`, normalization, and the `<image>` token interface.

**4. Multimodal backbone layer**  
[`UnlimitedOCRModel`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/modeling_unlimitedocr.py) combines a DeepSeek-derived language backbone with visual feature extraction from [`build_sam_vit_b`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/deepencoder.py) and [`build_clip_l`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/deepencoder.py). The concat-then-project step via [`MlpProjector`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/deepencoder.py) is the architectural heart of the artifact.

**5. Generation and postprocess layer**  
[`infer`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/modeling_unlimitedocr.py) and [`infer_multi`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/modeling_unlimitedocr.py) handle single-page and multi-page inference, while [`SlidingWindowNoRepeatNgramProcessor`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/modeling_unlimitedocr.py) adds a repetition guard tuned for long outputs. The same file also contains postprocessing that converts tagged output into boxed overlays and embedded image snippets.

### Inference / data / control flow
1. [`README.md`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/README.md) shows the public entrypoints: `infer(...)` for single images and `infer_multi(...)` for multi-page documents.
2. [`modeling_unlimitedocr.py`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/modeling_unlimitedocr.py) formats the conversation, tokenizes text splits around `<image>`, and inserts explicit image-token spans into the sequence.
3. If crop mode is enabled, `dynamic_preprocess(...)` creates a local-crop grid while also preserving a global padded page view.
4. [`UnlimitedOCRModel`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/modeling_unlimitedocr.py) runs SAM and CLIP-style visual encoders, concatenates local/global features, and scatters them into `inputs_embeds` under `images_seq_mask`.
5. Generation temporarily disables the model's sliding window, optionally adds [`SlidingWindowNoRepeatNgramProcessor`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/modeling_unlimitedocr.py), and emits a long markdown-like parse.
6. If saving is enabled, the same file parses `<|ref|>` and `<|det|>` tags, draws boxes, writes `result.md`, and extracts inline images.

## Key files, configs, cards, and artifacts
- [`modeling_unlimitedocr.py`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/modeling_unlimitedocr.py): the single most important file.
- [`deepencoder.py`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/deepencoder.py): visual encoder and projector details.
- [`config.json`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/config.json): 12-layer decoder, 64 routed experts, 6 experts per token, 32k context, and projector settings.
- [`processor_config.json`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/processor_config.json): processor contract and image token behavior.
- [`conversation.py`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/conversation.py): prompt-template logic.
- [`model.safetensors.index.json`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/model.safetensors.index.json): weight map showing one 6.67 GB checkpoint spanning language and vision components.
- [`wheel/sglang-0.0.0.dev11416+g92e8bb79e-py3-none-any.whl`](https://huggingface.co/baidu/Unlimited-OCR/tree/main/wheel): a revealing artifact because it shows the authors expect a custom serving stack, not only stock `transformers`.

## Important components
The most important component is [`UnlimitedOCRForCausalLM.infer`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/modeling_unlimitedocr.py). That method is where the artifact stops being "a model file" and becomes a document-parsing system with crop logic, image-token packing, generation controls, and result export.

The second is [`UnlimitedOCRModel`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/modeling_unlimitedocr.py). Its direct feature injection into the decoder embedding stream is the real multimodal trick.

The third is [`dynamic_preprocess`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/modeling_unlimitedocr.py). Long-horizon OCR usually dies on page geometry, and this is the artifact's explicit answer to that problem.

The fourth is [`SlidingWindowNoRepeatNgramProcessor`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/modeling_unlimitedocr.py). That detail matters because repetitive degeneration is a predictable failure mode for long OCR outputs.

## Important knobs / configs / extension points
- `base_size`, `image_size`, `crop_mode`, `max_length`, `temperature`, `no_repeat_ngram_size`, and `ngram_window` live in [`infer`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/modeling_unlimitedocr.py).
- Multi-page behavior lives in [`infer_multi`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/modeling_unlimitedocr.py), including `<PAGE>` serialization and per-page image token packing.
- Core model capacity knobs like `num_hidden_layers`, `n_routed_experts`, `num_experts_per_tok`, `max_position_embeddings`, and `sliding_window_size` live in [`config.json`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/config.json).
- Processor knobs like `candidate_resolutions`, `patch_size`, `downsample_ratio`, `normalize`, and `image_token` live in [`processor_config.json`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/processor_config.json).
- Deployment extension points live in [`README.md`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/README.md) and the bundled [`wheel`](https://huggingface.co/baidu/Unlimited-OCR/tree/main/wheel).

## Practical questions and answers
**Is the long-horizon claim backed by real code or mostly by the paper?**  
Backed by real code. [`dynamic_preprocess`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/modeling_unlimitedocr.py) explicitly creates crop grids, and [`infer_multi`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/modeling_unlimitedocr.py) concatenates multiple page image-token spans behind one prompt slot.

**What should a builder read first?**  
Start with [`README.md`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/README.md), then read [`modeling_unlimitedocr.py`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/modeling_unlimitedocr.py), then [`config.json`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/config.json), [`processor_config.json`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/processor_config.json), and [`deepencoder.py`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/deepencoder.py).

**What is the most reusable move here?**  
Use one global page view plus aspect-ratio-aware local crops, then make the visual-token layout explicit inside the text decoder stream instead of leaving it buried in server glue.

**Where is the design still brittle?**  
The postprocessing path in [`modeling_unlimitedocr.py`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/modeling_unlimitedocr.py) uses `eval(...)` on model-produced coordinate strings. That is fast for research code, but it is not a production-safe parsing strategy.

## What is smart
- Combining SAM and CLIP-like visual features, then projecting them straight into the language-model embedding stream.
- Treating multi-page and PDF parsing as first-class paths instead of leaving them to downstream users.
- Exposing a custom repetition guard for long outputs in [`SlidingWindowNoRepeatNgramProcessor`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/modeling_unlimitedocr.py).
- Shipping a custom SGLang wheel because the authors are honest about the serving requirements.

## What is flawed or weak
- The code and dependency surface is heavy: custom code, custom wheel, pinned CUDA-era packages, and large BF16 weights.
- [`model.safetensors.index.json`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/model.safetensors.index.json) points everything at one giant shard, which is simple but not especially elegant for distribution.
- The postprocessing logic uses `eval(...)` on generated text, which is an obvious safety smell.
- The README is useful, but the artifact still mixes production-ish deployment advice with research-style script assumptions.

## What we can learn / steal
- Publish the real multimodal inference path, not only a model card and benchmark table.
- Make long-document handling explicit in code: crop policy, image-token layout, repetition guard, and multi-page serialization.
- Bundle deployment artifacts when stock serving stacks need custom support.
- Treat postprocessing as part of the product surface, not as an afterthought hidden in a demo notebook.

## How we could apply it
If we build document agents or visual parsers, I would copy the "global page plus local crops" strategy and the explicit image-token masking approach. Those are the two most reusable ideas here because they attack the actual geometry and context problems.

I would not copy the unsafe parsing shortcuts. The model-side mechanics are worth stealing; the research-script postprocessing needs a harder production pass.

## Bottom line
`baidu/Unlimited-OCR` is worth studying because it exposes the real mechanism behind a modern long-document OCR stack: page tiling, multimodal feature fusion, explicit image-token packing, multi-page flow, and deployment-aware generation controls.

The builder lesson is that good OCR systems are not only better decoders. They are careful about how pages get chopped up, injected into context, and turned back into structured output without collapsing into repetition or geometry blindness.
