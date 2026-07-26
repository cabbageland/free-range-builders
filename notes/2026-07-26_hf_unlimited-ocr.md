# Unlimited OCR Works

- Source: Hugging Face
- Artifact: model `baidu/Unlimited-OCR`
- URL: https://huggingface.co/baidu/Unlimited-OCR
- Date: 2026-07-26
- Snapshot studied: `main` @ `27a5997fa0524f9adcf9e2f3d5e7d3f784434fa5`
- Why picked today: It was near the top of the Hugging Face trending models list when checked, and the Hub repo exposes real custom code rather than only a model card. With 2,593,460 downloads and 3,178 likes at inspection time, it is hot enough to matter and inspectable enough to teach something.

## Executive summary
`Unlimited-OCR` is not just a weight dump for OCR bragging rights. The Hub repo includes custom model code, processor settings, deployment instructions, a local SGLang wheel, and post-processing logic for turning model output into boxed images and markdown. The result is a much better artifact to study than the average open-weights OCR release.

The key mechanism lives in [`modeling_unlimitedocr.py`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/modeling_unlimitedocr.py). [`UnlimitedOCRModel`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/modeling_unlimitedocr.py) runs a SAM-style vision encoder and a CLIP-L path from [`deepencoder.py`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/deepencoder.py), concatenates those features, projects them into the language-model hidden size, then inserts them into the token stream with `masked_scatter_` at positions marked by `images_seq_mask`. That is the real trick, not the marketing phrase "one-shot long-horizon parsing."

The other useful design choice is that the repo shows its operating assumptions. [`config.json`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/config.json) exposes a 32k context, 64 routed experts with 6 experts per token, and the multimodal auto-map. [`processor_config.json`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/processor_config.json) exposes the image token, patch size, downsample ratio, and processor class. [`README.md`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/README.md) then shows how the authors expect you to run it under Transformers, vLLM, and SGLang.

## What they built / released
They released a Hugging Face model repo that is really a deployment bundle:

- [`README.md`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/README.md): model card plus concrete inference recipes.
- [`config.json`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/config.json): multimodal model config and language/vision/projector settings.
- [`processor_config.json`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/processor_config.json): image token and patching rules.
- [`modeling_unlimitedocr.py`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/modeling_unlimitedocr.py): multimodal model wrapper, image preprocessing, single-image inference, multi-page inference, and output post-processing.
- [`deepencoder.py`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/deepencoder.py): projector plus vision encoder pieces.
- [`conversation.py`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/conversation.py): prompt-template handling.
- [`wheel/sglang-0.0.0.dev11416+g92e8bb79e-py3-none-any.whl`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/wheel/sglang-0.0.0.dev11416%2Bg92e8bb79e-py3-none-any.whl): bundled runtime dependency for the recommended SGLang path.

## Why it matters
This artifact matters because it turns OCR quality into a systems packaging problem instead of only a benchmark screenshot.

1. It treats long-document OCR as a sequence construction problem: global view, local crops, image tokens, and 32k context.
2. It exposes the actual inference recipes and runtime tweaks needed to make the release usable.
3. It includes output reconstruction logic, which is where a lot of OCR demos quietly hand-wave away the last mile.

## Artifact shape at a glance
The Hub repo has a useful shape:

- [`README.md`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/README.md): release notes, examples, and serving recipes.
- [`Unlimited-OCR.pdf`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/Unlimited-OCR.pdf): paper artifact in the same repo.
- [`config.json`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/config.json) and [`processor_config.json`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/processor_config.json): the model's real knobs.
- [`modeling_unlimitedocr.py`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/modeling_unlimitedocr.py), [`deepencoder.py`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/deepencoder.py), and [`conversation.py`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/conversation.py): custom code paths that explain how the model is supposed to behave.
- [`model-00001-of-000001.safetensors`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/model-00001-of-000001.safetensors) and [`model.safetensors.index.json`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/model.safetensors.index.json): the actual weights surface.
- [`assets`](https://huggingface.co/baidu/Unlimited-OCR/tree/main/assets): overview and demo images.

## Layered architecture dissection
### High-level system shape
The core flow is: build a prompt with `<image>` placeholders -> preprocess one or more pages into global and optional local views -> allocate image-token positions in the text stream -> run the vision encoders and projector -> replace masked token positions with visual embeddings -> generate structured text -> optionally rewrite that text into markdown plus boxed-image artifacts.

### Main layers
**1. Release and serving layer**  
[`README.md`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/README.md) is unusually useful. It shows three deployment paths: Transformers, vLLM, and SGLang, and it includes concrete knobs like `max_length=32768`, `base_size=1024`, `image_size=640`, and the recommended SGLang launch arguments.

**2. Config layer**  
[`config.json`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/config.json) says the model is an `UnlimitedOCRForCausalLM` with DeepSeek-style language internals, 64 routed experts, 6 experts per token, 12 hidden layers, 10 attention heads, and 32k maximum positions. [`processor_config.json`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/processor_config.json) defines the image token as `<image>`, patch size 16, and downsample ratio 4.

**3. Vision fusion layer**  
[`deepencoder.py`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/deepencoder.py) defines the projector logic, while [`UnlimitedOCRModel` in `modeling_unlimitedocr.py`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/modeling_unlimitedocr.py) creates a SAM ViT-B path and a CLIP-L path, concatenates their features, and projects them into the LM hidden size.

**4. Multimodal language-model layer**  
[`UnlimitedOCRModel.forward`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/modeling_unlimitedocr.py) is the heart of the repo. It creates `image_newline` and `view_seperator` embeddings, builds global and local feature sequences, and injects them into `inputs_embeds` with `masked_scatter_` according to `images_seq_mask`.

**5. Prompt and conversation layer**  
[`conversation.py`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/conversation.py) and the `format_messages` path in [`modeling_unlimitedocr.py`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/modeling_unlimitedocr.py) show that the release still treats OCR as an instruction-following chat problem, not a separate decoder with a private output format.

**6. Inference and output layer**  
[`infer`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/modeling_unlimitedocr.py) handles single-image or single-document OCR with optional crop mode. [`infer_multi`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/modeling_unlimitedocr.py) concatenates multiple page image-token blocks at one `<image>` slot and uses `<PAGE>` delimiters in output. The same file then rewrites structured refs into cropped images, bounding boxes, and markdown.

### Inference / data / control flow
1. The user prompt is formatted through `format_messages` and the conversation templates in [`conversation.py`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/conversation.py).
2. [`infer`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/modeling_unlimitedocr.py) loads the image, optionally calls [`dynamic_preprocess`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/modeling_unlimitedocr.py) to split it into local crops, and creates a padded global view.
3. The same function emits explicit image token blocks into `tokenized_str` and marks those positions in `images_seq_mask`.
4. [`UnlimitedOCRModel.forward`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/modeling_unlimitedocr.py) runs the vision stacks, appends newline and view-separator embeddings, and writes the visual sequence into the language-model embedding stream.
5. Generation runs with the model's sliding window disabled temporarily, optional no-repeat-gram control, and up to 32k length.
6. If `save_results` is enabled, the repo parses `<|ref|>` and `<|det|>` structures, draws bounding boxes, crops embedded images, and writes `result.md` plus `result_with_boxes*.jpg`.

## Key files, configs, cards, and artifacts
- [`README.md`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/README.md): best high-level entrypoint.
- [`config.json`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/config.json): architecture and context settings.
- [`processor_config.json`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/processor_config.json): image tokenization rules.
- [`modeling_unlimitedocr.py`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/modeling_unlimitedocr.py): fusion, inference, and post-processing.
- [`deepencoder.py`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/deepencoder.py): projector and encoder plumbing.
- [`conversation.py`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/conversation.py): prompt templates.
- [`wheel/sglang-0.0.0.dev11416+g92e8bb79e-py3-none-any.whl`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/wheel/sglang-0.0.0.dev11416%2Bg92e8bb79e-py3-none-any.whl): practical serving artifact, not just documentation.

## Important components
The most important component is [`UnlimitedOCRModel.forward`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/modeling_unlimitedocr.py). That is the line where the release stops being a vague multimodal claim and becomes a concrete visual-token insertion strategy.

The second is [`infer`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/modeling_unlimitedocr.py) plus [`dynamic_preprocess`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/modeling_unlimitedocr.py). The crop/global-view split is the practical answer to "how do we cover long pages without destroying detail."

The third is the output-rewrite path in [`modeling_unlimitedocr.py`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/modeling_unlimitedocr.py). Saving markdown, region crops, and boxed previews is not glamorous, but it makes the artifact much more useful to downstream builders.

## Important knobs / configs / extension points
- `base_size`, `image_size`, and `crop_mode` in [`README.md`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/README.md) and [`infer`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/modeling_unlimitedocr.py).
- `max_length=32768`, `no_repeat_ngram_size`, and `ngram_window` in [`README.md`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/README.md) and [`modeling_unlimitedocr.py`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/modeling_unlimitedocr.py).
- `image_token`, `patch_size`, and `downsample_ratio` in [`processor_config.json`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/processor_config.json).
- Expert-routing and context limits in [`config.json`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/config.json).
- The SGLang deployment path and bundled wheel in [`README.md`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/README.md) and [`wheel/sglang-0.0.0.dev11416+g92e8bb79e-py3-none-any.whl`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/wheel/sglang-0.0.0.dev11416%2Bg92e8bb79e-py3-none-any.whl).

## Practical questions and answers
**Is the main trick just a larger OCR model?**  
No. Scale matters, but the more reusable lesson is packaging: split pages into local crops plus a global view, represent those views as explicit token spans, and keep the whole thing inside a standard generation path.

**What makes it "long-horizon" in practice?**  
[`config.json`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/config.json) exposes a 32k context, while [`infer`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/modeling_unlimitedocr.py) and [`infer_multi`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/modeling_unlimitedocr.py) build long image-token sequences from crops or multiple pages. The repo is explicitly engineering for wide coverage, not only single screenshots.

**Where should a builder start reading?**  
Read [`README.md`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/README.md), [`config.json`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/config.json), [`processor_config.json`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/processor_config.json), [`modeling_unlimitedocr.py`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/modeling_unlimitedocr.py), and [`deepencoder.py`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/deepencoder.py).

## What is smart
- The Hub repo exposes real custom code instead of pretending the model card is enough.
- Global-view plus local-crop fusion is implemented explicitly in source, not hidden in a private serving stack.
- The release includes workable serving instructions for multiple runtimes.
- The artifact thinks through post-processing and output packaging, not only token generation.

## What is flawed or weak
- [`modeling_unlimitedocr.py`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/modeling_unlimitedocr.py) is doing too much at once: preprocessing, generation, and output rendering all live in one large script-like file.
- The repo mutates generation config state at runtime by disabling the sliding window during inference, which is practical but brittle.
- Output parsing uses regex plus `eval` in places inside [`modeling_unlimitedocr.py`](https://huggingface.co/baidu/Unlimited-OCR/blob/main/modeling_unlimitedocr.py), which is a code smell for anything expected to be robust or secure.
- Shipping a custom wheel inside the model repo is convenient, but it widens the trust and maintenance surface for downstream users.

## What we can learn / steal
- Release the real configs, processor rules, and inference scripts with the model.
- Treat long-document OCR as multimodal sequence engineering, not just better visual features.
- Add last-mile artifact generation so model output becomes immediately inspectable by humans.
- Make deployment recipes part of the artifact, not a separate scavenger hunt.

## How we could apply it
If we shipped our own document parser, I would borrow this pattern: one token-level multimodal path, a global-plus-local view strategy, explicit long-context settings, and output post-processing that writes something a human can audit immediately.

## Bottom line
`baidu/Unlimited-OCR` is worth studying because it exposes the mechanics of a modern OCR release instead of stopping at weight files and screenshots.

The builder lesson is that strong multimodal releases are not only about model quality. They are about sequence construction, inference packaging, and the boring output plumbing that turns model text into a useful document artifact.
