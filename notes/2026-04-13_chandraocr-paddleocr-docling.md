# ChandraOCR vs PaddleOCR vs Docling / TableFormer

- Repo: comparative teardown of `ChandraOCR`, `PaddlePaddle/PaddleOCR`, and `docling-project/docling`
- URL:
  - ChandraOCR: unavailable for fresh API re-fetch from this environment during this pass; analysis below reflects earlier source inspection plus cross-checking against the architecture we already established
  - PaddleOCR: https://github.com/PaddlePaddle/PaddleOCR
  - Docling: https://github.com/docling-project/docling
- Date: 2026-04-13
- Repo snapshot studied:
  - PaddleOCR: `main`
  - Docling: `main`
  - ChandraOCR: earlier inspected code paths referenced in this comparison
- Why picked today: This is a useful builder comparison because these three systems all live in the broad “OCR / document understanding” space but represent three very different architectural bets: generative VLM OCR, modular OCR toolkit design, and staged document-conversion with specialist table reconstruction.

## Executive summary

These three projects are solving related problems, but they are not really the same kind of system.

- **ChandraOCR** is best understood as a **layout-aware VLM OCR system**. It gives a page image to a multimodal model and asks the model to generate structured output directly.
- **PaddleOCR** is a **modular OCR platform**. It exposes explicit submodels and explicit pipelines for detection, recognition, orientation, layout, tables, formulas, and document structure.
- **Docling + TableFormer** is a **document conversion pipeline**. OCR is one stage inside a larger document reconstruction flow, and TableFormer is a specialist stage for table structure.

The most important difference is not benchmark flavor. It is architectural shape:

- ChandraOCR: **the model writes the document**
- PaddleOCR: **the pipeline assembles the document**
- Docling/TableFormer: **the document system reconstructs the document**

That distinction matters a lot when you care about debuggability, extensibility, production failure modes, and table extraction quality.

## What they built

### ChandraOCR

ChandraOCR appears to be an end-to-end VLM OCR stack organized around a few critical files:

- `chandra/model/hf.py`
- `chandra/model/vllm.py`
- `chandra/prompts.py`
- `chandra/output.py`

The core idea is simple and powerful:

1. render or load a page image
2. prompt a multimodal model to output structured HTML / markdown / JSON-like content
3. parse the model output back into text/layout artifacts
4. optionally recover block structure, bboxes, and cropped figure regions from generated tags/attributes

The repo’s center of gravity is not a forest of classical OCR modules. It is the combo of:

- multimodal model wrapper
- prompt design
- output postprocessing / layout reconstruction

### PaddleOCR

PaddleOCR is much broader and more explicit.

The key repo surfaces I inspected in this pass:

- top-level pipeline package: [`paddleocr/_pipelines/`](https://github.com/PaddlePaddle/PaddleOCR/tree/main/paddleocr/_pipelines)
- model wrappers: [`paddleocr/_models/`](https://github.com/PaddlePaddle/PaddleOCR/tree/main/paddleocr/_models)
- older low-level internals: [`ppocr/`](https://github.com/PaddlePaddle/PaddleOCR/tree/main/ppocr)

Important pipeline files:

- OCR pipeline: [`paddleocr/_pipelines/ocr.py`](https://github.com/PaddlePaddle/PaddleOCR/blob/main/paddleocr/_pipelines/ocr.py)
- table pipeline: [`paddleocr/_pipelines/table_recognition_v2.py`](https://github.com/PaddlePaddle/PaddleOCR/blob/main/paddleocr/_pipelines/table_recognition_v2.py)
- structured-doc pipeline: [`paddleocr/_pipelines/pp_structurev3.py`](https://github.com/PaddlePaddle/PaddleOCR/blob/main/paddleocr/_pipelines/pp_structurev3.py)

Important model wrappers:

- layout detection: [`paddleocr/_models/layout_detection.py`](https://github.com/PaddlePaddle/PaddleOCR/blob/main/paddleocr/_models/layout_detection.py)
- text detection: [`paddleocr/_models/text_detection.py`](https://github.com/PaddlePaddle/PaddleOCR/blob/main/paddleocr/_models/text_detection.py)
- text recognition: [`paddleocr/_models/text_recognition.py`](https://github.com/PaddlePaddle/PaddleOCR/blob/main/paddleocr/_models/text_recognition.py)
- table structure recognition: [`paddleocr/_models/table_structure_recognition.py`](https://github.com/PaddlePaddle/PaddleOCR/blob/main/paddleocr/_models/table_structure_recognition.py)
- table cell detection: [`paddleocr/_models/table_cells_detection.py`](https://github.com/PaddlePaddle/PaddleOCR/blob/main/paddleocr/_models/table_cells_detection.py)

This repo is not pretending OCR is one magic model. It is a toolkit of specialists with configurable composition.

### Docling / TableFormer

Docling is a document conversion system with strong staged-pipeline structure.

The files that matter most here:

- pipeline orchestration: [`docling/pipeline/standard_pdf_pipeline.py`](https://github.com/docling-project/docling/blob/main/docling/pipeline/standard_pdf_pipeline.py)
- layout stage: [`docling/models/stages/layout/layout_object_detection_model.py`](https://github.com/docling-project/docling/blob/main/docling/models/stages/layout/layout_object_detection_model.py)
- table structure stage: [`docling/models/stages/table_structure/table_structure_model.py`](https://github.com/docling-project/docling/blob/main/docling/models/stages/table_structure/table_structure_model.py)
- config surface: [`docling/datamodel/pipeline_options.py`](https://github.com/docling-project/docling/blob/main/docling/datamodel/pipeline_options.py)
- stage tree: [`docling/models/stages/`](https://github.com/docling-project/docling/tree/main/docling/models/stages)

Docling’s core pitch is not “OCR only.” It is:

- preprocess pages
- run layout detection
- run OCR as needed through pluggable backends
- reconstruct tables, reading order, figures, etc.
- assemble a coherent document model

TableFormer is therefore a **specialist inside a broader document engine**, not the whole product.

## Why it matters

People often talk about OCR systems as if they are interchangeable. They are not.

These repos embody three different bets:

1. **Generative OCR is enough if the VLM is strong enough.**
2. **OCR should be decomposed into specialist modules.**
3. **OCR is only one stage inside document reconstruction.**

Those bets create very different tradeoffs.

If you want fast iteration and holistic page understanding, the VLM approach is attractive.
If you want fine-grained control and swappable components, the modular toolkit approach wins.
If you want serious document conversion and grounded table extraction, the staged document pipeline is stronger.

This matters because teams keep arguing over “best OCR” when they are actually choosing between totally different system architectures.

## Repo shape at a glance

### ChandraOCR

The useful shape, from earlier inspection, is compact and model-centered:

- `chandra/model/` — model runtime wrappers
- `chandra/prompts.py` — prompt templates and output contract framing
- `chandra/output.py` — parse / convert / recover structured result

That shape already tells the story: prompt + model + parser is the architecture.

### PaddleOCR

Top-level repo shape relevant to this comparison:

- [`paddleocr/`](https://github.com/PaddlePaddle/PaddleOCR/tree/main/paddleocr) — newer public-facing wrappers and pipelines
  - [`paddleocr/_pipelines/`](https://github.com/PaddlePaddle/PaddleOCR/tree/main/paddleocr/_pipelines) — high-level composed tasks
  - [`paddleocr/_models/`](https://github.com/PaddlePaddle/PaddleOCR/tree/main/paddleocr/_models) — individual model wrappers
- [`ppocr/`](https://github.com/PaddlePaddle/PaddleOCR/tree/main/ppocr) — deeper internals, data, modeling, postprocess, utils

This is a broad toolkit repo. It exposes both the high-level convenience surface and the lower-level engine internals.

### Docling

The repo has a much more obviously layered systems shape:

- [`docling/pipeline/`](https://github.com/docling-project/docling/tree/main/docling/pipeline) — pipeline orchestration
- [`docling/models/`](https://github.com/docling-project/docling/tree/main/docling/models) — model abstractions, factories, stages, inference engines
- [`docling/models/stages/`](https://github.com/docling-project/docling/tree/main/docling/models/stages) — stage-specialized components
  - `layout/`
  - `ocr/`
  - `table_structure/`
  - `reading_order/`
  - `page_assemble/`
  - `vlm_convert/`
- [`docling/datamodel/`](https://github.com/docling-project/docling/tree/main/docling/datamodel) — pipeline options, specs, document data types

This shape is a big tell: Docling is organized as a serious conversion framework, not just a bag of recognizers.

## Layered architecture dissection

### High-level system shape

The deepest contrast between the three is this:

- **ChandraOCR** collapses OCR, layout understanding, and structured output into one generative pass.
- **PaddleOCR** decomposes the problem into explicit perception subproblems.
- **Docling** treats OCR and table extraction as stages in a larger document assembly process.

All three can output something like structured text or tables. But they arrive there through very different internal contracts.

### Main layers

### ChandraOCR layers

#### 1. Input and model runtime layer

The runtime wrappers in `chandra/model/hf.py` and `chandra/model/vllm.py` are the inference shell. They decide how the page image is handed to the model and how generation is run.

#### 2. Prompt contract layer

`chandra/prompts.py` is not cosmetic. In a generative OCR system, prompt design is part of the architecture. It defines:

- the output schema style
- what structure the model should preserve
- whether labels/bboxes appear
- how much layout reasoning the model is asked to perform explicitly

#### 3. Output reconstruction layer

`chandra/output.py` is where generated text becomes a usable artifact.

That includes:

- parsing generated HTML or similar structure
- converting to markdown
- recovering block labels and bounding boxes
- cropping figures/images from predicted regions

The model generates the structure; the parser tries to make that structure operational.

### PaddleOCR layers

#### 1. Preprocessing layer

In [`paddleocr/_pipelines/ocr.py`](https://github.com/PaddlePaddle/PaddleOCR/blob/main/paddleocr/_pipelines/ocr.py), the pipeline explicitly includes:

- document orientation classification
- document unwarping

That means image normalization is a first-class stage, not a hidden side effect.

#### 2. Text perception layer

Still in the OCR pipeline, you see explicit submodules for:

- text detection
- textline orientation
- text recognition

This is classic staged OCR design, but cleaned up into a configurable wrapper surface.

#### 3. Structured-document layer

[`paddleocr/_pipelines/pp_structurev3.py`](https://github.com/PaddlePaddle/PaddleOCR/blob/main/paddleocr/_pipelines/pp_structurev3.py) broadens the system to include:

- layout detection
- table recognition
- formula recognition
- chart recognition
- seal recognition
- region detection

This is where PaddleOCR stops being “just OCR” and becomes a practical document-understanding platform.

#### 4. Table-specialist layer

[`paddleocr/_pipelines/table_recognition_v2.py`](https://github.com/PaddlePaddle/PaddleOCR/blob/main/paddleocr/_pipelines/table_recognition_v2.py) is especially revealing.

The pipeline explicitly wires:

- layout detection
- table classification
- wired table structure recognition
- wireless table structure recognition
- wired table cells detection
- wireless table cells detection
- OCR model
- doc preprocessor

That is a very engineered table stack.

### Docling layers

#### 1. Pipeline orchestration layer

[`docling/pipeline/standard_pdf_pipeline.py`](https://github.com/docling-project/docling/blob/main/docling/pipeline/standard_pdf_pipeline.py) is the orchestration heart.

What stands out:

- per-run isolation
- bounded queues
- worker threads
- explicit backpressure
- deterministic shutdown behavior
- model initialization separated from per-run mutation

This is much more production-pipeline shaped than most ML repo glue.

#### 2. Layout stage

[`docling/models/stages/layout/layout_object_detection_model.py`](https://github.com/docling-project/docling/blob/main/docling/models/stages/layout/layout_object_detection_model.py) runs object detection, maps labels to document semantics, and then postprocesses detections into layout clusters.

So the layout stage is not just “boxes.” It is document-aware clustering.

#### 3. OCR stage

Docling treats OCR as pluggable stage machinery rather than product identity.

The options surface in [`docling/datamodel/pipeline_options.py`](https://github.com/docling-project/docling/blob/main/docling/datamodel/pipeline_options.py) supports multiple OCR backends and their configuration. That means OCR can be swapped while the document assembly pipeline remains the same.

#### 4. Table structure stage

[`docling/models/stages/table_structure/table_structure_model.py`](https://github.com/docling-project/docling/blob/main/docling/models/stages/table_structure/table_structure_model.py) is the table specialist.

Its logic is notably grounded:

- find table clusters from the layout prediction
- gather page tokens/cells from PDF segmentation or OCR-derived cells
- scale into model space
- call the TableFormer predictor
- optionally do cell matching
- emit structured table objects with row/column counts, cells, and sequence representation

This is much more grounded than purely generative table output.

#### 5. Assembly / reading-order layer

Docling also has stage families for:

- reading order
- page assembly
- picture description / classification
- VLM conversion

This makes the system feel like a document factory, not a recognizer pile.

### Request / data / control flow

### ChandraOCR flow

A simplified flow:

1. page image enters multimodal model wrapper
2. prompt tells model to emit structured transcription
3. model generates HTML/markdown/JSON-ish output
4. output parser reconstructs layout blocks / markdown / crops

This is elegant because the flow is short.
It is risky because so much depends on one generation step doing the right thing.

### PaddleOCR flow

From the code path in the OCR and table pipelines, the characteristic flow is:

1. optional orientation classify / unwarp
2. layout detection or text detection depending on task
3. textline orientation if needed
4. text recognition
5. table type / structure / cell detection if table path is enabled
6. fuse OCR results into table or structured-document output

The strength here is explicit decomposition. If one stage is bad, you can often see which one.

### Docling flow

The shape is more document-native:

1. preprocess/load page
2. run layout stage
3. run OCR stage as needed / available
4. run table structure stage on detected table regions
5. run reading-order logic
6. assemble page/document outputs

This lets table extraction depend on upstream document semantics while still staying separate enough to debug.

## Key directories and files

### ChandraOCR

The important files from earlier inspection:

- `chandra/model/hf.py`
- `chandra/model/vllm.py`
- `chandra/prompts.py`
- `chandra/output.py`

These four files appear to carry most of the architecture.

### PaddleOCR

If I wanted to understand the system quickly, I would read these first:

- [`paddleocr/_pipelines/ocr.py`](https://github.com/PaddlePaddle/PaddleOCR/blob/main/paddleocr/_pipelines/ocr.py)
- [`paddleocr/_pipelines/table_recognition_v2.py`](https://github.com/PaddlePaddle/PaddleOCR/blob/main/paddleocr/_pipelines/table_recognition_v2.py)
- [`paddleocr/_pipelines/pp_structurev3.py`](https://github.com/PaddlePaddle/PaddleOCR/blob/main/paddleocr/_pipelines/pp_structurev3.py)
- [`paddleocr/_models/layout_detection.py`](https://github.com/PaddlePaddle/PaddleOCR/blob/main/paddleocr/_models/layout_detection.py)
- [`paddleocr/_models/table_structure_recognition.py`](https://github.com/PaddlePaddle/PaddleOCR/blob/main/paddleocr/_models/table_structure_recognition.py)
- [`paddleocr/_models/table_cells_detection.py`](https://github.com/PaddlePaddle/PaddleOCR/blob/main/paddleocr/_models/table_cells_detection.py)
- [`ppocr/`](https://github.com/PaddlePaddle/PaddleOCR/tree/main/ppocr)

### Docling

The fastest path into the architecture is:

- [`docling/pipeline/standard_pdf_pipeline.py`](https://github.com/docling-project/docling/blob/main/docling/pipeline/standard_pdf_pipeline.py)
- [`docling/models/stages/layout/layout_object_detection_model.py`](https://github.com/docling-project/docling/blob/main/docling/models/stages/layout/layout_object_detection_model.py)
- [`docling/models/stages/table_structure/table_structure_model.py`](https://github.com/docling-project/docling/blob/main/docling/models/stages/table_structure/table_structure_model.py)
- [`docling/datamodel/pipeline_options.py`](https://github.com/docling-project/docling/blob/main/docling/datamodel/pipeline_options.py)
- [`docling/models/stages/`](https://github.com/docling-project/docling/tree/main/docling/models/stages)

## Important components

### ChandraOCR: prompt + parser as core infrastructure

The most important ChandraOCR architectural idea is that prompt design and output parsing are not accessories. They are the system.

That means:

- prompt quality partly substitutes for detector design
- parser quality partly substitutes for structured postprocessors
- model obedience becomes an architectural dependency

That is both the beauty and fragility of the approach.

### PaddleOCR: explicit model wrappers and explicit pipelines

The strongest design move in PaddleOCR is that it separates:

- individual predictors (`_models`)
- composed task flows (`_pipelines`)

That allows:

- swapping modules
- task-specific wrappers
- easier debugging
- better operational tuning

The table path is especially serious because it distinguishes wired and wireless tables instead of pretending all tables have the same visual structure.

### Docling: stage-specialized document conversion

The strongest design move in Docling is not TableFormer by itself. It is the existence of a coherent stage graph around it.

That means TableFormer gets:

- table regions from layout
- tokens from PDF segmentation or OCR
- a document-native assembly environment downstream

So TableFormer is used as a grounded structural specialist, not a floating guesser.

## Important knobs / configs / extension points

### ChandraOCR

The important knobs are likely concentrated in:

- prompt templates
- model backend choice (`hf.py` vs `vllm.py`)
- output contract / parser behavior

This is a smaller knob surface, but a high-leverage one.

### PaddleOCR

The knob surface is huge.

In the public wrappers you can configure:

- orientation classify on/off
- unwarping on/off
- text detection thresholds and limits
- recognition batch sizes
- OCR language/model choice
- layout detection model choice
- table classification choice
- wired/wireless table models
- whether OCR results are fused with table cells
- whether end-to-end wired/wireless table recognition is used

These are not marketing knobs. They map to real stage boundaries in the code.

### Docling

The configuration surface in [`docling/datamodel/pipeline_options.py`](https://github.com/docling-project/docling/blob/main/docling/datamodel/pipeline_options.py) is a major part of the design.

Useful knobs include:

- OCR backend selection
- layout model selection
- table structure options
- `TableFormerMode` (`fast` vs `accurate`)
- whether cell matching is enabled
- accelerator / engine choices
- VLM options for conversion-related paths

This is a proper systems configuration surface, not a couple of demo flags.

## Practical questions and answers

### Which one is most “end-to-end VLM OCR”?

**ChandraOCR.**

That is the one where the core move is: page in, structured generation out.

### Which one is the broadest OCR toolkit?

**PaddleOCR.**

It exposes the most explicit module family and task-specific pipeline family.

### Which one is strongest for serious document conversion?

**Docling.**

Because it is architected as a full document pipeline rather than just an OCR engine.

### Which one has the most serious table-specific pipeline?

For table-centric document reconstruction, I would rank them:

1. **Docling / TableFormer**
2. **PaddleOCR**
3. **ChandraOCR**

The reason is not that Chandra is bad. It is that TableFormer and Paddle both make table structure a first-class explicit problem.

### Which one is easiest to debug when results are wrong?

**PaddleOCR**, then **Docling**, then **ChandraOCR**.

- Paddle gives you clean stage boundaries.
- Docling gives you stages too, but in a larger pipeline context.
- Chandra collapses many errors into one generation surface.

### Which one is likely best on bizarre messy pages?

Potentially **ChandraOCR**, especially when holistic page reasoning matters more than exact geometric grounding.

That is where a strong VLM can feel magical.

### Which one is likely best when table geometry fidelity matters a lot?

**Docling / TableFormer**, because the table structure path is grounded in explicit table regions and token alignment.

## What is smart

### ChandraOCR

What is smart is the refusal to overbuild classical stages when a VLM can often infer the whole page at once.

The short path is attractive:

- fewer handoff boundaries
- fewer brittle heuristics
- richer holistic reasoning

That is a genuine architectural simplification, not just hype.

### PaddleOCR

The smart part is the explicit decomposition without giving up usability.

The repo manages to be:

- broad
- configurable
- task-oriented
- still fairly legible from the wrapper layer

The wired/wireless table split is especially pragmatic.

### Docling

The smart part is that it treats document parsing like a pipeline engineering problem, not just a modeling problem.

I especially like:

- production-minded pipeline orchestration
- stage specialization
- token-grounded table reconstruction
- clear config/datamodel surfaces

This repo feels like it has spent time around real documents instead of only benchmark leaderboards.

## What is flawed or weak

### ChandraOCR

The weakness of the VLM approach is control.

If output quality is wrong, the failure could come from:

- prompt ambiguity
- model hallucination
- layout misunderstanding
- parser mismatch

Those failures are harder to isolate cleanly.

Also, generative bboxes and structure can feel plausible without being truly well-grounded.

### PaddleOCR

The weakness is stage sprawl and error propagation.

If upstream layout or table classification is wrong, downstream structure quality can collapse.

A modular stack is powerful, but every extra stage is another failure interface.

### Docling

The weakness is system complexity.

It has:

- more moving parts
- more pipeline orchestration burden
- dependence on upstream stage quality
- the usual pain of matching table structure back to messy source tokens

It is probably the strongest document system here, but also the heaviest one mentally and operationally.

## What we can learn / steal

A few very reusable lessons come out of this comparison.

### From ChandraOCR

- Generative structured OCR is real enough to be a serious architecture, not just a toy demo.
- Prompt design can function as an architectural layer when the model is strong enough.
- Sometimes collapsing stages is worth the loss of modular purity.

### From PaddleOCR

- Separate predictor wrappers from higher-level task pipelines.
- Keep module boundaries explicit so systems remain debuggable.
- Treat tables, formulas, and layout as first-class subproblems, not bolt-ons.

### From Docling

- For documents, OCR should often live inside a larger conversion pipeline.
- Table extraction benefits a lot from token grounding and layout-region grounding.
- Good pipeline architecture can matter as much as good model choice.

## How we could apply it

If we were building around these ideas ourselves, I would borrow different things from each.

### If we want a lightweight modern OCR product

Borrow the **ChandraOCR** posture:

- image in
- structured text out
- minimal bespoke CV staging
- parser/postprocessor doing cleanup

That is especially good for rapid iteration.

### If we want a configurable OCR platform

Borrow the **PaddleOCR** posture:

- explicit modules
- explicit pipelines
- task-oriented composition
- exposed operational knobs

That is better for long-lived product teams.

### If we want serious document intelligence

Borrow the **Docling** posture:

- pipeline orchestration first
- OCR as stage, not identity
- table structure as grounded structured prediction
- document assembly as the true end product

That is the strongest conceptual frame for PDFs, reports, and document-native UX.

## Bottom line

These three systems sit in the same neighborhood, but they are making different philosophical bets.

- **ChandraOCR** is the cleanest expression of end-to-end generative OCR.
- **PaddleOCR** is the most toolkit-like and operationally modular.
- **Docling / TableFormer** is the most convincing document-engineering system, especially when tables matter.

If I had to compress the whole comparison into one builder rule, it would be this:

**Before choosing an OCR stack, decide whether your real problem is page transcription, OCR pipeline control, or full document reconstruction. Those are not the same problem, and these repos prove it.**

## Caveat

For this writeup, PaddleOCR and Docling sections were cross-checked against fresh repo/API reads in this environment. The ChandraOCR section reflects earlier source inspection and the architecture established in prior analysis, because I could not cleanly re-fetch that repo through the GitHub API during this pass.