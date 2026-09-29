# TeleOCR

- Source: Hugging Face
- Artifact: model
- URL: https://huggingface.co/XingChen-AGI/TeleOCR
- Date: 2026-09-29
- Snapshot studied: revision `e92585356c0d0b7b7a65938f3da035c6593cc9a6`, last modified `2026-09-29T00:30:57Z`
- Why picked today: It was high on the Hugging Face trending page, had about 30k downloads and 859 likes, and shipped more than a model card: config, tokenizer assets, preprocessing config, generated Qwen2.5-VL modeling code, examples, and document-parsing assets are inspectable.

## Executive summary

[XingChen-AGI/TeleOCR](https://huggingface.co/XingChen-AGI/TeleOCR/tree/e92585356c0d0b7b7a65938f3da035c6593cc9a6) is a document-parsing VLM specialized for OCR, table extraction, formulas, code snippets, layout analysis, distorted/camera-captured documents, and scientific figures. Hugging Face reports a BF16 safetensors weight set with about 1.42B parameters, while the [README](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/README.md) describes the release as a lightweight roughly 1.2B parameter model.

The useful builder lesson is the task framing. TeleOCR is not just "image to text." The examples in the [README](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/README.md) use different prompts and post-processing contracts for plain text, table OTSL, LaTeX formulas, code, layout, distorted layout, and scientific figures. The artifact pairs a normal Qwen2.5-VL style model with domain-specific output formats and conversion code.

## What they built / released

The HF repo ships:

- [README.md](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/README.md): model card, benchmark tables, task examples, OTSL-to-HTML conversion helpers, and usage snippets.
- [config.json](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/config.json): Qwen2.5-VL architecture config with 28 text layers, 32 vision layers, 1024 text hidden size, 1280 vision hidden size, 128k max positions, and `auto_map` entries pointing to custom remote code.
- [modeling_naviocr.py](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/modeling_naviocr.py): generated Transformers implementation of the Qwen2.5-VL model classes used by the artifact.
- [preprocessor_config.json](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/preprocessor_config.json): image processor contract with 14-pixel patches, merge size 2, Qwen2.5-VL processor class, and a large max-pixel ceiling.
- [generation_config.json](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/generation_config.json): low-temperature, top-k-1 generation defaults.
- [chat_template.jinja](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/chat_template.jinja), [tokenizer_config.json](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/tokenizer_config.json), [tokenizer.json](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/tokenizer.json), [vocab.json](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/vocab.json), and [merges.txt](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/merges.txt) for chat and tokenization.
- [model.safetensors](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/model.safetensors): the weight artifact.
- Example images under [assets](https://huggingface.co/XingChen-AGI/TeleOCR/tree/e92585356c0d0b7b7a65938f3da035c6593cc9a6/assets), including text, table, formula, code, layout, distorted layout, scientific figure, score, and icon examples.

## Why it matters

Document parsing is messy because "OCR" is not one task. A product document can contain paragraphs, multi-row tables, formulas, code blocks, figure captions, rotated regions, distorted camera geometry, and reading-order constraints. TeleOCR matters because the card and examples make that multi-output nature explicit.

The artifact is also practical. It is not a 70B general VLM pressed into OCR duty. [config.json](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/config.json) defines a smaller Qwen2.5-VL style stack, and [generation_config.json](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/generation_config.json) leans toward deterministic extraction rather than creative sampling. That is the right bias for OCR.

## Artifact shape at a glance

- Card and cookbook: [README.md](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/README.md) contains benchmark claims, task prompts, helper dataclasses, OTSL token parsing, HTML conversion, equation post-processing, and inference code.
- Model contract: [config.json](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/config.json) declares Qwen2.5-VL text/vision subconfigs and remote-code auto mappings.
- Runtime implementation: [modeling_naviocr.py](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/modeling_naviocr.py) provides the classes loaded by `trust_remote_code=True`.
- Preprocessing: [preprocessor_config.json](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/preprocessor_config.json) defines Qwen2.5-VL image processing: patch size 14, temporal patch size 2, merge size 2, CLIP-like image mean/std, and max pixels.
- Decoding: [generation_config.json](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/generation_config.json) sets `temperature: 0.1`, `top_k: 1`, `top_p: 0.001`, and `repetition_penalty: 1.05`.
- Token/chat surface: [chat_template.jinja](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/chat_template.jinja), [special_tokens_map.json](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/special_tokens_map.json), [added_tokens.json](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/added_tokens.json), and tokenizer files define how image tokens and text instructions are packed.
- Demonstration assets: [assets/table.png](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/assets/table.png), [assets/formula.png](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/assets/formula.png), [assets/layout_distorted.jpg](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/assets/layout_distorted.jpg), and [assets/scientific_figure.png](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/assets/scientific_figure.png) show the intended input classes.

## Layered architecture dissection

### High-level system shape

TeleOCR is a Qwen2.5-VL derived image-text-to-text model specialized for document parsing. Images are converted into visual patch tokens by the vision tower. Text prompts and special image tokens are packed through the chat template. The multimodal decoder then generates task-specific markup or text, and the examples post-process certain formats into more usable artifacts.

The pipeline is therefore:

1. Image preprocessing by [preprocessor_config.json](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/preprocessor_config.json).
2. Chat/template packing by [chat_template.jinja](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/chat_template.jinja).
3. Vision patch encoding and multimodal position handling in [modeling_naviocr.py](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/modeling_naviocr.py).
4. Text generation with deterministic extraction-oriented defaults from [generation_config.json](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/generation_config.json).
5. Optional downstream conversion, especially OTSL table tokens into HTML, implemented in the [README](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/README.md) examples.

### Main layers

The vision layer is configured in [config.json](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/config.json): 32 vision layers, hidden size 1280, 16 heads, patch size 14, spatial merge size 2, temporal patch size 2, and full-attention blocks at indexes 7, 15, 23, and 31. [modeling_naviocr.py](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/modeling_naviocr.py) implements `Qwen2_5_VisionPatchEmbed`, `Qwen2_5_VLVisionAttention`, and the vision transformer class.

The text layer in [config.json](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/config.json) is smaller than Qwen's large general models: 28 layers, hidden size 1024, intermediate size 3072, 16 attention heads, 8 KV heads, tied embeddings, and a 151,936-token vocabulary. That shape explains the practical deployment pitch: it is built for document parsing, not broad chat.

The multimodal position layer is visible in [modeling_naviocr.py](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/modeling_naviocr.py), especially `get_rope_index`. It computes 3D rotary positions for visual temporal/height/width grids and normal text positions after vision tokens. That matters for documents because layout tasks depend on preserving spatial relationships, not only reading token content.

The extraction/post-processing layer is in the [README](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/README.md). The example code defines `ContentBlock`, `TableCell`, OTSL tokens such as `<nl>`, `<fcel>`, `<ecel>`, `<lcel>`, `<ucel>`, and `<xcel>`, then converts table output into HTML. Equations are wrapped into display-math delimiters. That is domain glue, and it is part of the usable system.

### Inference / data / control flow

The README's `infer` function builds a chat message with one image and one text prompt, calls `processor.apply_chat_template`, then sends the image and prompt through `AutoProcessor` and `AutoModel` with `trust_remote_code=True`. The model generates up to 4096 new tokens with cache enabled and no sampling in the example path.

Different task prompts steer different output contracts:

- Plain OCR uses "Please output the text content from the image."
- Table extraction asks for OTSL format, then [README.md](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/README.md) converts OTSL into HTML.
- Formula extraction asks for LaTeX and normalizes the output into display math.
- Code extraction requests the parsing result directly.
- Layout extraction asks the model to analyze page layout, including distorted documents.
- Scientific figures ask for a table implied by the figure, then reuse table conversion.

That is the core design: one model, multiple structured output modes, and small per-mode adapters.

## Key files, configs, cards, and artifacts

- [README.md](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/README.md): card, benchmarks, cookbook, OTSL parser, post-processing, and inference examples.
- [config.json](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/config.json): architecture and remote-code contract.
- [modeling_naviocr.py](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/modeling_naviocr.py): generated Qwen2.5-VL implementation loaded by the auto map.
- [preprocessor_config.json](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/preprocessor_config.json): image resolution and patching contract.
- [generation_config.json](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/generation_config.json): decoding defaults tuned for extraction.
- [chat_template.jinja](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/chat_template.jinja): multimodal chat packing for image and text content.
- [model.safetensors](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/model.safetensors): single weight file reported by HF as about 2.84 GB of storage.
- [assets](https://huggingface.co/XingChen-AGI/TeleOCR/tree/e92585356c0d0b7b7a65938f3da035c6593cc9a6/assets): test images for the task modes the card advertises.

## Important components

- `Qwen2_5_VisionPatchEmbed` in [modeling_naviocr.py](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/modeling_naviocr.py): converts image/video patches into visual embeddings.
- `Qwen2_5_VLPatchMerger` in [modeling_naviocr.py](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/modeling_naviocr.py): merges spatial patch groups before the language side consumes them.
- `get_rope_index` in [modeling_naviocr.py](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/modeling_naviocr.py): computes multimodal 3D position IDs for vision tokens and text positions.
- `Qwen2_5_VLForConditionalGeneration` in [modeling_naviocr.py](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/modeling_naviocr.py): the model class used by `AutoModel`.
- `convert_otsl_to_html` in [README.md](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/README.md): practical post-processing that turns model table output into a normal HTML table.
- `post_process` in [README.md](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/README.md): small but important normalization for equations and block filtering.

## Important knobs / configs / extension points

- Image size and patching knobs live in [preprocessor_config.json](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/preprocessor_config.json): `min_pixels`, `max_pixels`, `patch_size`, `temporal_patch_size`, and `merge_size`.
- Model capacity knobs live in [config.json](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/config.json): text layers, vision layers, hidden sizes, heads, max positions, and rope configuration.
- Output behavior lives partly in [generation_config.json](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/generation_config.json), but the README examples override sampling by calling `model.generate(..., do_sample=False)`.
- Task control is prompt-level. The [README](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/README.md) prompts are the thin API for selecting text, table, formula, code, layout, or figure extraction.
- Structured downstream output is adapter-level. The OTSL parser and equation post-processing in [README.md](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/README.md) are easy to replace with stricter parsers in a production app.

## Practical questions and answers

Q: Is this an OCR engine or a general VLM?

A: It is a VLM architecture specialized for document parsing. The file surface is Qwen2.5-VL shaped, but the card, examples, and benchmarks are all OCR/document tasks.

Q: Does the HF repo expose the claimed training innovations?

A: Only partially. The [README](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/README.md) names Multi-node Consensus Voting, geometry-aware modeling, CGDP, self-verification, four-stage training, and content-structure decoupling. The HF artifact exposes model/config/inference assets, not the full data-generation and training pipeline.

Q: What is the most reusable engineering idea?

A: Treat document outputs as separate contracts. Text, tables, formulas, code, and layout should not all become one untyped blob. The [README](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/README.md) examples show prompt plus parser pairs.

Q: What should a production user verify?

A: Verify output validity per mode. Tables need OTSL/HTML validation, formulas need LaTeX validation, layout blocks need schema checks, and long documents need page-level consistency. The model can emit text, but the application has to own correctness checks.

Q: Any deployment cautions?

A: Yes. Loading uses `trust_remote_code=True` in the [README](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/README.md), which means consumers should pin the revision and audit [modeling_naviocr.py](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/modeling_naviocr.py). The model also wants BF16 GPU inference in the example.

## What is smart

The prompt/output split is smart. TeleOCR asks for OTSL when it wants tables, LaTeX when it wants formulas, and normal text when it wants text. That lets application code parse the output instead of guessing one universal representation.

The model sizing is also smart. [config.json](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/config.json) shows a compact text decoder and a vision tower large enough for layout-sensitive documents. This is a better product shape than shipping a giant general model and hoping OCR falls out.

The example assets are useful. [assets/layout_distorted.jpg](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/assets/layout_distorted.jpg), [assets/table.png](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/assets/table.png), and [assets/scientific_figure.png](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/assets/scientific_figure.png) make it obvious what the authors think the model should handle.

## What is flawed or weak

The strongest training claims are not fully inspectable in the HF artifact. The model card talks about pseudo-label generation, geometry-aware modeling, CGDP, self-verification, progressive training, and content-structure decoupling, but the released repo mostly gives inference-time assets. That is normal for model releases, but it means we can inspect the serving surface more deeply than the research pipeline.

[modeling_naviocr.py](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/modeling_naviocr.py) starts with a generated-code warning from Transformers' Qwen2.5-VL implementation. That is not bad, but it means the custom value is likely in weights, data, prompts, and post-processing rather than a novel checked-in model implementation.

The [README](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/README.md) example post-processors are helpful but permissive. In production, an OTSL parser should fail loudly on malformed row/column structure and an equation parser should validate syntax rather than only wrapping delimiters.

## What we can learn / steal

Steal the idea of task-specific output contracts. For any document AI product, make the model emit an intermediate representation that downstream code can validate. Tables should be tables, formulas should be formulas, layout blocks should have bounding boxes and types.

Steal the small adapter layer. The OTSL-to-HTML conversion in [README.md](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/README.md) is a reminder that model quality alone is not enough. The useful system is model plus parser plus validation plus rendering.

Steal the deterministic decoding bias for extraction. [generation_config.json](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/generation_config.json) is conservative, and the README examples set `do_sample=False`. That is what you want for document parsing.

## How we could apply it

For our own document-ingestion work, use TeleOCR's structure as a product template:

1. Define one prompt and one schema per document task: text, table, formula, code, layout, figure.
2. Keep parsers beside prompts, like the OTSL and equation helpers in [README.md](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/README.md).
3. Pin model revisions and audit remote code when using artifacts such as [modeling_naviocr.py](https://huggingface.co/XingChen-AGI/TeleOCR/blob/e92585356c0d0b7b7a65938f3da035c6593cc9a6/modeling_naviocr.py).
4. Build validation around generated structures before trusting the output in downstream workflows.

TeleOCR is also a good candidate for a local OCR fallback when cloud VLMs are too expensive or privacy-sensitive, as long as the application owns schema validation.

## Bottom line

TeleOCR is interesting because it makes document parsing feel like a set of structured extraction contracts rather than a single OCR string. The artifact is not fully transparent about training, but the released config, remote code, examples, and post-processing surface are enough to learn a practical pattern: specialize prompts and output formats, then make code responsible for turning model text into checked document structures.
