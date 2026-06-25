# LocateAnything

- Source: Hugging Face
- Artifact: space `nvidia/LocateAnything`
- URL: https://huggingface.co/spaces/nvidia/LocateAnything
- Date: 2026-06-25
- Snapshot studied: space `main` @ `3a017382062aa753a527bd3567573d1821ac7d31`, linked model `nvidia/LocateAnything-3B` @ `c32291ca5e996f5a7a485845b4f57a233936bba0`, last modified 2026-05-30T12:58:14Z
- Why picked today: It was one of the current trending Hugging Face Spaces when checked, and unlike many vision demos it exposes both sides of the product: the Space app logic for logging, parsing, GPU budgeting, and overlay rendering, plus a linked model repo with readable config and hybrid decoding runtime.

## Executive summary
`LocateAnything` is a good Hugging Face scout because it is not just "upload image, get boxes." The Space in [`app.py`](https://huggingface.co/spaces/nvidia/LocateAnything/blob/main/app.py) is a real serving surface with prompt templates, structured-output parsing, ZeroGPU time budgeting, per-inference logging via [`CommitScheduler`](https://huggingface.co/spaces/nvidia/LocateAnything/blob/main/app.py), and separate image/video code paths. The linked model repo in [`nvidia/LocateAnything-3B`](https://huggingface.co/nvidia/LocateAnything-3B) then exposes the interesting mechanism: a Qwen2.5 + MoonViT grounding model with special coordinate/ref tokens in [`config.json`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/config.json) and a batched hybrid runtime whose decode state machine is documented directly in [`batch_utils/engine_hybrid.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/batch_utils/engine_hybrid.py).

The strongest builder insight is that the project treats grounding throughput as a decoding problem, not only a model-capacity problem. The model card in [`README.md`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/README.md) describes Parallel Box Decoding, and the runtime makes that concrete: hybrid mode flips between multi-token prediction and autoregressive repair instead of forcing every coordinate through the same slow path. The Space keeps that sophistication legible enough to study by exposing `model_mode`, prompt overrides, structured `<ref>` / `<box>` outputs, and time-budget guardrails.

The caution is that this is still research-flavored infrastructure. The model uses `trust_remote_code=True` in [`app.py`](https://huggingface.co/spaces/nvidia/LocateAnything/blob/main/app.py), the recommended deployment story is clearly NVIDIA-GPU-heavy, and the model license in [`LICENSE`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/LICENSE) is non-commercial. The code is interesting, but the portability envelope is narrower than the demo impression suggests.

## What they built / released
They released two tightly connected artifacts:

- A Gradio/Spaces app in [`nvidia/LocateAnything`](https://huggingface.co/spaces/nvidia/LocateAnything/tree/main) with [`README.md`](https://huggingface.co/spaces/nvidia/LocateAnything/blob/main/README.md), [`app.py`](https://huggingface.co/spaces/nvidia/LocateAnything/blob/main/app.py), [`requirements.txt`](https://huggingface.co/spaces/nvidia/LocateAnything/blob/main/requirements.txt), and bundled assets.
- A full model repo in [`nvidia/LocateAnything-3B`](https://huggingface.co/nvidia/LocateAnything-3B/tree/main) with a long model card, configs, batch inference utilities, decode runtime code, and demo assets.

The Space supports multiple task shapes in one shell: generic detection, grounding, OCR, GUI grounding, and point-based pointing. The model repo positions the same checkpoint as a generalist grounding engine for natural scenes, documents, GUI elements, and dense detection workloads.

## Why it matters
This artifact matters for three reasons:

1. It shows the serving logic that most grounding demos hide: prompt construction, result parsing, overlay rendering, logging, and GPU time budgeting.
2. It shows the model/runtime split that many Spaces obscure. The demo is thin enough to follow, but the actual inference machinery lives in an inspectable linked repo.
3. It turns structured grounding output into a reusable interface. The app expects tags like `<ref>` and `<box>`, and the model config explicitly reserves token ranges for those structures.

## Artifact shape at a glance
The artifact is best understood as a two-repo stack:

- Space layer:
  [`README.md`](https://huggingface.co/spaces/nvidia/LocateAnything/blob/main/README.md),
  [`app.py`](https://huggingface.co/spaces/nvidia/LocateAnything/blob/main/app.py),
  [`requirements.txt`](https://huggingface.co/spaces/nvidia/LocateAnything/blob/main/requirements.txt),
  and [`assets/`](https://huggingface.co/spaces/nvidia/LocateAnything/tree/main/assets).
- Model layer:
  [`README.md`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/README.md),
  [`config.json`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/config.json),
  [`generation_config.json`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/generation_config.json),
  [`batch_utils/README.md`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/batch_utils/README.md),
  [`batch_utils/engine_hybrid.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/batch_utils/engine_hybrid.py),
  and [`batch_utils/`](https://huggingface.co/nvidia/LocateAnything-3B/tree/main/batch_utils) more broadly.

That split is healthy. The Space is not pretending to be the whole system. It is a product shell over a model/runtime repo that still rewards close reading.

## Layered architecture dissection
### High-level system shape
The Space flow is straightforward but well instrumented:

1. [`run_inference_api`](https://huggingface.co/spaces/nvidia/LocateAnything/blob/main/app.py) receives image or video input plus task parameters.
2. `run_image_gpu_api` or `run_video_gpu_api` preprocesses the media, enforces GPU budgets, and calls `get_worker()`.
3. [`EagleWorker`](https://huggingface.co/spaces/nvidia/LocateAnything/blob/main/app.py) loads `AutoTokenizer`, `AutoProcessor`, and `AutoModel` from `nvidia/LocateAnything-3B` with `trust_remote_code=True`.
4. Model output comes back as text containing structured localization tags.
5. [`parse_mixed_results`](https://huggingface.co/spaces/nvidia/LocateAnything/blob/main/app.py) converts those tags into boxes or points, and [`draw_on_frame`](https://huggingface.co/spaces/nvidia/LocateAnything/blob/main/app.py) renders them back onto images or sampled video frames.
6. The app optionally logs the run into a dataset repo via [`CommitScheduler`](https://huggingface.co/spaces/nvidia/LocateAnything/blob/main/app.py).

### Main layers
**1. Space serving layer**  
[`app.py`](https://huggingface.co/spaces/nvidia/LocateAnything/blob/main/app.py) owns nearly everything on the product side: auth-env discovery, prompt generation, image/video branching, HTML debugging output, logging, and API exposure.

**2. Worker/model loader layer**  
`EagleWorker` in [`app.py`](https://huggingface.co/spaces/nvidia/LocateAnything/blob/main/app.py) is the runtime hinge. It constructs the multimodal chat prompt, runs the processor, and calls model generation in selectable modes.

**3. Structured-output layer**  
[`parse_mixed_results`](https://huggingface.co/spaces/nvidia/LocateAnything/blob/main/app.py) is important because it shows the contract the model is expected to satisfy. The app is not relying on vague natural-language explanations; it expects `<ref>` and `<box>` blocks and has fallback parsing when formatting gets messy.

**4. Video budget / systems layer**  
[`run_video_gpu_api`](https://huggingface.co/spaces/nvidia/LocateAnything/blob/main/app.py) is a practical piece of engineering. It samples frames, estimates remaining budget, trims work if needed, empties CUDA cache, and re-encodes the output video with `ffmpeg` only if enough time remains.

**5. Model/runtime layer**  
The model config in [`config.json`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/config.json) reveals the actual architecture choices: `Qwen2.5-3B-Instruct` as the text backbone, `MoonViT-SO-400M` as the vision backbone, custom coordinate/ref token ids, and a block-oriented grounding output format. The runtime in [`batch_utils/engine_hybrid.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/batch_utils/engine_hybrid.py) then implements the hybrid decode scheduler.

### Inference / data / control flow
The most interesting flow is the hybrid decode path:

1. The Space converts a task like detection or GUI grounding into a concrete prompt string via `generate_raw_prompt` in [`app.py`](https://huggingface.co/spaces/nvidia/LocateAnything/blob/main/app.py).
2. [`EagleWorker.generate`](https://huggingface.co/spaces/nvidia/LocateAnything/blob/main/app.py) packages image + text into processor inputs and calls model generation with `generation_mode`.
3. The model repo's [`config.json`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/config.json) reserves token ids for `box_start`, `box_end`, `coord_start`, `coord_end`, and `ref` markers, so structured localization is part of the formal output vocabulary.
4. [`batch_utils/engine_hybrid.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/batch_utils/engine_hybrid.py) documents the stock state machine as `MTP -> error_box -> AR` and `AR -> box_end_ar -> MTP`, which is the clearest source-level explanation of Parallel Box Decoding in the artifact.
5. The Space parses the result, overlays it, and, for video, applies the same cycle frame by frame within a hard time budget.

## Key files, configs, cards, and artifacts
- [`spaces/nvidia/LocateAnything/blob/main/app.py`](https://huggingface.co/spaces/nvidia/LocateAnything/blob/main/app.py): the actual demo service logic.
- [`spaces/nvidia/LocateAnything/blob/main/requirements.txt`](https://huggingface.co/spaces/nvidia/LocateAnything/blob/main/requirements.txt): runtime dependencies, including `transformers`, `torch`, `decord`, and `spaces`.
- [`nvidia/LocateAnything-3B/blob/main/README.md`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/README.md): model card, use cases, throughput claims, license, and deployment envelope.
- [`nvidia/LocateAnything-3B/blob/main/config.json`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/config.json): special token ids, backbone references, and core architecture metadata.
- [`nvidia/LocateAnything-3B/blob/main/batch_utils/README.md`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/batch_utils/README.md): runtime environment knobs for attention backend and hybrid scheduler behavior.
- [`nvidia/LocateAnything-3B/blob/main/batch_utils/engine_hybrid.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/batch_utils/engine_hybrid.py): the most concrete explanation of hybrid batched decode behavior.
- [`nvidia/LocateAnything-3B/tree/main/assets`](https://huggingface.co/nvidia/LocateAnything-3B/tree/main/assets): task demos for GUI, OCR, pointing, and dense detection.

## Important components
**`EagleWorker` is the operative runtime boundary**  
It is the object that turns the model repo into a serviceable Space: load once, build multimodal chat messages, choose generation mode, and return structured detection text.

**`parse_mixed_results` is a quiet but important product asset**  
Many demos fail at the last mile because the model output is too brittle. [`parse_mixed_results`](https://huggingface.co/spaces/nvidia/LocateAnything/blob/main/app.py) acknowledges that structured outputs can degrade and carries a fallback parser.

**The video path is where the authors show real operational taste**  
[`run_video_gpu_api`](https://huggingface.co/spaces/nvidia/LocateAnything/blob/main/app.py) is not glamorous, but it is the difference between a research demo and a service that can survive Hugging Face GPU constraints.

**`engine_hybrid.py` is the technical core worth stealing**  
The runtime in [`batch_utils/engine_hybrid.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/batch_utils/engine_hybrid.py) makes the throughput story legible by explicitly grouping rows, tracking KV-cache packing, and moving between parallel and autoregressive repair paths.

## Important knobs / configs / extension points
- `MODEL_PATH`, HF token env variables, and dataset-log repo configuration in [`app.py`](https://huggingface.co/spaces/nvidia/LocateAnything/blob/main/app.py).
- `model_mode`, `temp`, `top_p`, `top_k`, `short_size`, and `max_video_frames` in the same Space file.
- `GPU_HARD_LIMIT_IMAGE`, `GPU_HARD_LIMIT_VIDEO`, `PHASE2_RESERVE`, and `EST_SECONDS_PER_FRAME` in [`app.py`](https://huggingface.co/spaces/nvidia/LocateAnything/blob/main/app.py).
- `box_start_token_id`, `box_end_token_id`, `coord_start_token_id`, `coord_end_token_id`, and `ref_*` token ids in [`config.json`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/config.json).
- Attention backend and hybrid scheduler env knobs such as `LA_FLASH_ATTN`, `LA_FLASH_VISION_ATTN`, and `LA_FLASH_HYBRID_SCHEDULER` in [`batch_utils/README.md`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/batch_utils/README.md).

## Practical questions and answers
**Is this only a flashy front end over a hidden model?**  
No. The Space is readable, and the linked model repo is also readable. That combination is why it is worth studying.

**What is the most reusable engineering here?**  
Three things: the structured `<ref>` / `<box>` output contract, the hybrid multi-token-plus-AR repair decode strategy, and the explicit GPU time-budgeting in the Space service.

**Where is the main weakness?**  
This is still very much research and GPU-first infrastructure. `trust_remote_code`, non-commercial licensing, and hardware-heavy expectations narrow the practical deployment surface.

**What should a builder read first?**  
Start with the Space [`app.py`](https://huggingface.co/spaces/nvidia/LocateAnything/blob/main/app.py), then the model [`README.md`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/README.md), then [`config.json`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/config.json), and then [`batch_utils/engine_hybrid.py`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/batch_utils/engine_hybrid.py).

## What is smart
- Making localization a structured token problem instead of a fuzzy prose problem.
- Exposing fast / hybrid / slow generation modes instead of pretending one inference path fits everything.
- Logging each inference as one file with [`CommitScheduler`](https://huggingface.co/spaces/nvidia/LocateAnything/blob/main/app.py), which is a practical trick for concurrent Space sessions.
- Budgeting video inference against hard GPU time limits instead of crashing at the tail end.
- Publishing runtime knobs in [`batch_utils/README.md`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/batch_utils/README.md) so builders can actually tune the backend.

## What is flawed or weak
- The Space logic is concentrated in one large [`app.py`](https://huggingface.co/spaces/nvidia/LocateAnything/blob/main/app.py), which makes the serving layer harder to extend cleanly.
- The model path depends on `trust_remote_code=True`, which raises audit and portability costs.
- The model card in [`README.md`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/README.md) is rich, but the deployment envelope is still clearly optimized around strong NVIDIA GPUs.
- The NVIDIA non-commercial license in [`LICENSE`](https://huggingface.co/nvidia/LocateAnything-3B/blob/main/LICENSE) limits how directly many teams can adopt it.
- The Space is honest about GPU constraints, which is good engineering, but it also means the demo experience is partly shaped by infrastructure scarcity rather than purely by model quality.

## What we can learn / steal
- Use explicit structured output tags for detection and grounding tasks.
- Separate the product-serving shell from the deeper model/runtime repo, but make both inspectable.
- Treat video inference as a budgeted systems workflow, not as "same as image, but in a loop."
- Publish backend knobs and decode modes so advanced users can tune performance.
- Keep the output parser resilient enough to survive imperfect formatting.

## How we could apply it
If we were building our own grounding or GUI-localization system, I would copy the design pattern:

1. a simple app layer that owns prompting, parsing, rendering, and time budgets,
2. a model layer with explicit coordinate tokens and documented decode modes,
3. a hybrid decoding path that can go fast first and repair only when needed,
4. structured logging for each run,
5. separate image and video pipelines with realistic resource controls.

That pattern would translate well to document layout tools, GUI agents, robotics perception demos, and annotation pipelines where throughput matters as much as raw accuracy.

## Bottom line
`LocateAnything` is a strong Hugging Face pick because it exposes the full ladder from product shell to decode runtime.

The builder lesson is that grounding systems become much more useful when they formalize output structure, make the decode strategy explicit, and treat serving constraints as part of the design. This artifact does all three well enough to be worth keeping in the notebook.
