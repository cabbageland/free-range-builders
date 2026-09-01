# pdf-inspector

- Repo: `firecrawl/pdf-inspector`
- URL: https://github.com/firecrawl/pdf-inspector
- Date: 2026-09-01
- Repo snapshot studied: `main` @ `23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd`
- Why picked today: GitHub's live trending page had `firecrawl/pdf-inspector` on it when checked at 17,766 stars and 545 stars today. More importantly, the inspected source is a real parser stack: native PDF classification, text extraction, table/layout recovery, markdown assembly, optional OCR, and bindings for Python, Node, and the browser.

## Executive summary
[`pdf-inspector`](https://github.com/firecrawl/pdf-inspector/tree/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd) is best understood as a fast native-first PDF router, not as "OCR but cheaper." The public pitch in [`README.md`](https://github.com/firecrawl/pdf-inspector/blob/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/README.md) is honest: first detect whether the document is text-based or scan-heavy, then extract structured text locally, then fall back to OCR only for the pages that actually need it.

The repo shape makes the architecture legible. [`src/detector.rs`](https://github.com/firecrawl/pdf-inspector/blob/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/src/detector.rs) samples content streams and classifies the document into `TextBased`, `Scanned`, `ImageBased`, or `Mixed`. [`src/extractor/mod.rs`](https://github.com/firecrawl/pdf-inspector/blob/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/src/extractor/mod.rs) and the nested [`src/extractor`](https://github.com/firecrawl/pdf-inspector/tree/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/src/extractor) directory do the heavy lifting for content streams, fonts, links, reading order, and XObjects. [`src/tables`](https://github.com/firecrawl/pdf-inspector/tree/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/src/tables) and [`src/markdown`](https://github.com/firecrawl/pdf-inspector/tree/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/src/markdown) turn that low-level extraction into something downstream systems can actually use.

The strongest builder move is dependency discipline. [`Cargo.toml`](https://github.com/firecrawl/pdf-inspector/blob/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/Cargo.toml) keeps OCR, model caching, HTTP downloads, PDFium rendering, and Python bindings behind separate features, while [`src/vision/mod.rs`](https://github.com/firecrawl/pdf-inspector/blob/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/src/vision/mod.rs) makes it explicit that the default path is still the pure extractor. The weak side is exactly what you would expect from a heuristic-heavy parser: lots of correctness depends on format-specific judgment calls, and the full OCR path still asks operators to manage external PDFium and ONNX Runtime libraries.

## What they built
They built a PDF processing library and toolchain that tries to answer one practical routing question early: "Do I need OCR at all?" The exported surface in [`src/lib.rs`](https://github.com/firecrawl/pdf-inspector/blob/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/src/lib.rs) exposes both high-level one-call operations like `process_pdf()` and narrower building blocks like `detect_pdf_type()`, positioned text extraction, markdown conversion, and OCR-aware processing.

This is not a single-language crate either. The root ships:

- the Rust core in [`src`](https://github.com/firecrawl/pdf-inspector/tree/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/src)
- Node bindings in [`napi`](https://github.com/firecrawl/pdf-inspector/tree/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/napi)
- browser WASM packaging in [`wasm`](https://github.com/firecrawl/pdf-inspector/tree/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/wasm)
- Python packaging hooks via [`pyproject.toml`](https://github.com/firecrawl/pdf-inspector/blob/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/pyproject.toml) and the optional [`src/python.rs`](https://github.com/firecrawl/pdf-inspector/blob/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/src/python.rs)

## Why it matters
Most document pipelines make one of two bad tradeoffs: they either OCR everything and pay the latency bill, or they trust raw PDF text extraction and accept garbage output on scanned or badly encoded pages. `pdf-inspector` inserts a routing layer between those extremes.

That matters because the source shows three good instincts:

1. Classification is cheap and first-class, not an afterthought in the OCR path.
2. The document is loaded once and shared between stages, which is the opposite of the usual wasteful parse-detect-parse-again loop.
3. OCR is page-selective and provenance-aware instead of being a giant black-box replacement for the native extractor.

## Repo shape at a glance
The repository has a clean "core plus surfaces" shape:

- [`src`](https://github.com/firecrawl/pdf-inspector/tree/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/src): Rust parser core, classifiers, extractors, tables, markdown, and optional vision/OCR pipeline
- [`napi`](https://github.com/firecrawl/pdf-inspector/tree/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/napi): Node.js wrapper and async OCR-facing API
- [`wasm`](https://github.com/firecrawl/pdf-inspector/tree/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/wasm): browser packaging for local extraction without a server round trip
- [`docs`](https://github.com/firecrawl/pdf-inspector/tree/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/docs): API, OCR runtime, debugging, and benchmarking guides
- [`examples`](https://github.com/firecrawl/pdf-inspector/tree/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/examples): small usage examples such as [`basic_usage.py`](https://github.com/firecrawl/pdf-inspector/blob/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/examples/basic_usage.py)
- [`tests`](https://github.com/firecrawl/pdf-inspector/tree/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/tests): fixture-heavy regression coverage
- [`external`](https://github.com/firecrawl/pdf-inspector/tree/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/external): bundled CMaps and similar support assets

That split is a good sign. The real engine stays in one place, and the language surfaces mostly adapt it rather than re-implementing it.

## Layered architecture dissection
### High-level system shape
The high-level flow is: validate PDF bytes, sample a subset of pages to classify the document, extract positioned text and layout evidence from the parsed document, detect tables and chart regions, convert the result into markdown, and only then route weak pages to OCR when the caller opted into the native vision path.

### Main layers
**1. Feature and packaging layer**  
[`Cargo.toml`](https://github.com/firecrawl/pdf-inspector/blob/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/Cargo.toml) is important reading, because it defines the real product boundaries: `python`, `vision`, `model-cache`, `model-download`, `ocr-oar`, `render-pdfium`, and the umbrella `ocr` feature. This is not cosmetic; it keeps the default library slim while still supporting a fuller OCR stack for native consumers.

**2. Detection layer**  
[`src/detector.rs`](https://github.com/firecrawl/pdf-inspector/blob/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/src/detector.rs) implements page sampling, early-exit versus full scan strategies, OCR reason codes, and heuristics for mixed documents. The default `DetectionConfig` uses `ScanStrategy::Sample(8)`, which is a pragmatic latency/accuracy compromise.

**3. Native extraction layer**  
[`src/extractor`](https://github.com/firecrawl/pdf-inspector/tree/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/src/extractor) splits the parser into sensible concerns: [`content_stream.rs`](https://github.com/firecrawl/pdf-inspector/blob/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/src/extractor/content_stream.rs), [`fonts.rs`](https://github.com/firecrawl/pdf-inspector/blob/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/src/extractor/fonts.rs), [`layout.rs`](https://github.com/firecrawl/pdf-inspector/blob/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/src/extractor/layout.rs), [`reading_order.rs`](https://github.com/firecrawl/pdf-inspector/blob/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/src/extractor/reading_order.rs), [`links.rs`](https://github.com/firecrawl/pdf-inspector/blob/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/src/extractor/links.rs), and [`xobjects.rs`](https://github.com/firecrawl/pdf-inspector/blob/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/src/extractor/xobjects.rs). That is the core parser.

**4. Structure recovery layer**  
[`src/tables/mod.rs`](https://github.com/firecrawl/pdf-inspector/blob/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/src/tables/mod.rs) shows that table handling is not a one-trick detector. The crate uses rectangle-guided, line-guided, heuristic, and structure-tree-aware approaches. [`src/markdown/mod.rs`](https://github.com/firecrawl/pdf-inspector/blob/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/src/markdown/mod.rs) then merges headings, tables, charts, captions, code-like text, and continuation tables into the final markdown pass.

**5. OCR routing layer**  
[`src/vision/mod.rs`](https://github.com/firecrawl/pdf-inspector/blob/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/src/vision/mod.rs) makes the optional vision stack explicit. [`src/vision/pipeline.rs`](https://github.com/firecrawl/pdf-inspector/blob/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/src/vision/pipeline.rs) then wires together `route_ocr_pages`, `run_ocr_pages`, and `fuse_ocr_pages_adaptive_with_routes`, so OCR augments the native extractor instead of replacing it wholesale.

### Request / data / control flow
1. A caller enters through [`src/lib.rs`](https://github.com/firecrawl/pdf-inspector/blob/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/src/lib.rs) using `process_pdf`, `detect_pdf_type`, or the OCR-aware path.
2. [`src/detector.rs`](https://github.com/firecrawl/pdf-inspector/blob/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/src/detector.rs) samples pages and classifies document type plus page-level OCR reasons.
3. [`src/extractor/mod.rs`](https://github.com/firecrawl/pdf-inspector/blob/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/src/extractor/mod.rs) extracts positioned text, font metadata, links, and layout groupings from the same parsed document.
4. [`src/tables`](https://github.com/firecrawl/pdf-inspector/tree/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/src/tables) and [`src/markdown`](https://github.com/firecrawl/pdf-inspector/tree/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/src/markdown) recover structure and assemble markdown.
5. If OCR is enabled, [`src/vision/pipeline.rs`](https://github.com/firecrawl/pdf-inspector/blob/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/src/vision/pipeline.rs) renders only routed pages, runs local PP-OCRv6 Small, and fuses the result back into page markdown with provenance.
6. Bindings in [`napi/src/lib.rs`](https://github.com/firecrawl/pdf-inspector/blob/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/napi/src/lib.rs) and the Python surface expose the same pipeline in language-native result shapes.

## Key directories and files
- [`Cargo.toml`](https://github.com/firecrawl/pdf-inspector/blob/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/Cargo.toml): feature gates, binaries, and packaging contract
- [`src/lib.rs`](https://github.com/firecrawl/pdf-inspector/blob/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/src/lib.rs): public API and end-to-end result types
- [`src/detector.rs`](https://github.com/firecrawl/pdf-inspector/blob/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/src/detector.rs): document classification and OCR routing hints
- [`src/extractor/mod.rs`](https://github.com/firecrawl/pdf-inspector/blob/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/src/extractor/mod.rs): positioned-text extraction entrypoint
- [`src/tables/mod.rs`](https://github.com/firecrawl/pdf-inspector/blob/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/src/tables/mod.rs): table-recovery strategy hub
- [`src/markdown/mod.rs`](https://github.com/firecrawl/pdf-inspector/blob/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/src/markdown/mod.rs): markdown assembly and chart masking logic
- [`src/vision/mod.rs`](https://github.com/firecrawl/pdf-inspector/blob/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/src/vision/mod.rs): optional OCR subsystem boundary
- [`src/vision/pipeline.rs`](https://github.com/firecrawl/pdf-inspector/blob/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/src/vision/pipeline.rs): page routing, OCR execution, and adaptive fusion
- [`napi/src/lib.rs`](https://github.com/firecrawl/pdf-inspector/blob/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/napi/src/lib.rs): Node-facing API and OCR provenance surface
- [`docs/ocr-runtime.md`](https://github.com/firecrawl/pdf-inspector/blob/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/docs/ocr-runtime.md): real operator-facing setup constraints

## Important components
The most important component is [`src/detector.rs`](https://github.com/firecrawl/pdf-inspector/blob/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/src/detector.rs), because it decides whether the cheap native path is trustworthy.

The second is [`src/extractor`](https://github.com/firecrawl/pdf-inspector/tree/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/src/extractor), especially the content-stream, font, and reading-order modules. That is where the parser earns its keep.

The third is [`src/tables`](https://github.com/firecrawl/pdf-inspector/tree/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/src/tables), because tables are where most PDF-to-markdown tools fall apart.

The fourth is [`src/vision/pipeline.rs`](https://github.com/firecrawl/pdf-inspector/blob/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/src/vision/pipeline.rs), which is where selective OCR becomes a real control flow instead of a slogan.

The fifth is [`napi/src/lib.rs`](https://github.com/firecrawl/pdf-inspector/blob/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/napi/src/lib.rs), because it proves the team is packaging the same engine across surfaces instead of building parallel implementations.

## Important knobs / configs / extension points
- [`Cargo.toml`](https://github.com/firecrawl/pdf-inspector/blob/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/Cargo.toml): `python`, `vision`, `model-cache`, `model-download`, `ocr-oar`, `render-pdfium`, and `ocr`
- [`src/detector.rs`](https://github.com/firecrawl/pdf-inspector/blob/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/src/detector.rs): `ScanStrategy`, `min_text_ops_per_page`, and `text_page_ratio_threshold`
- [`src/lib.rs`](https://github.com/firecrawl/pdf-inspector/blob/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/src/lib.rs): `PdfOptions`, `ProcessMode`, page filters, and markdown formatting options
- [`src/vision/pipeline.rs`](https://github.com/firecrawl/pdf-inspector/blob/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/src/vision/pipeline.rs): `OcrPdfOptions`, render DPI, `minimum_confidence`, page selection, offline model directory, and hosted recommendation threshold
- [`napi/src/lib.rs`](https://github.com/firecrawl/pdf-inspector/blob/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/napi/src/lib.rs): `OcrMode` and page provenance objects for application integration

## Practical questions and answers
**Is this an OCR-first parser?**  
No. The default path is the native extractor. The OCR stack is opt-in in [`Cargo.toml`](https://github.com/firecrawl/pdf-inspector/blob/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/Cargo.toml) and explicitly secondary in [`src/vision/mod.rs`](https://github.com/firecrawl/pdf-inspector/blob/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/src/vision/mod.rs).

**Where does the speed claim come from?**  
From cheap page sampling in [`src/detector.rs`](https://github.com/firecrawl/pdf-inspector/blob/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/src/detector.rs), one shared document load in [`src/lib.rs`](https://github.com/firecrawl/pdf-inspector/blob/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/src/lib.rs), and not paying OCR costs on clean PDFs.

**What is the sharpest implementation idea here?**  
Selective OCR with fusion. [`src/vision/pipeline.rs`](https://github.com/firecrawl/pdf-inspector/blob/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/src/vision/pipeline.rs) routes only weak pages to OCR, then merges the OCR result back into the native output instead of throwing away everything the parser already knew.

**Where is it most likely to be brittle?**  
In heuristic boundaries: reading order, chart masking, table recovery, and mixed-document detection. The structure is good, but PDFs are adversarial file formats and the repo has to make a lot of judgment calls.

## What is smart
- Keeping the fast native extractor as the default product and making OCR genuinely optional
- Treating classification as a separate subsystem instead of burying it in extraction
- Using multiple table-detection strategies instead of pretending one heuristic is enough
- Shipping one engine across Rust, Node, Python, and WASM surfaces
- Exposing operator realities like PDFium and ONNX Runtime setup in docs instead of hiding them

## What is flawed or weak
- The full OCR path still depends on external runtime libraries, which raises friction for production rollouts
- A large share of the product value sits in heuristics, so correctness drift is a permanent maintenance tax
- The public README benchmark story is good, but the repo still asks you to trust a sizable amount of custom format logic
- The surface area is already broad for a parser library: CLI, bindings, WASM, OCR, model download, and benchmarks all add upkeep pressure

## What we can learn / steal
- Put a fast router in front of expensive document AI
- Keep optional heavyweight dependencies behind hard feature boundaries
- Reuse one native core across bindings instead of building separate parsers per language
- Preserve page-level provenance when mixing deterministic extraction with model inference

## How we could apply it
If we were building any document ingestion system, I would copy the control-flow idea almost directly: first classify, then extract natively, then OCR only where the native output is weak, and always keep the page-level reason codes. I would also copy the packaging discipline from [`Cargo.toml`](https://github.com/firecrawl/pdf-inspector/blob/23cf1ad7b37eec6e3a21df61f8e6d5dce66c46bd/Cargo.toml): make expensive capabilities opt-in instead of accidental defaults.

## Bottom line
`pdf-inspector` is worth studying because it is not selling magic. The source shows a grounded document pipeline with strong subsystem boundaries, good feature hygiene, and a believable answer to the "when do we actually need OCR?" question.

The reusable builder lesson is simple: treat document parsing as a routing problem, not just an extraction problem.
