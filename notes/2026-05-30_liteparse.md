# LiteParse

- Repo: `run-llama/liteparse`
- URL: https://github.com/run-llama/liteparse
- Date: 2026-05-30
- Repo snapshot studied: `main` @ `cf9f08fe89a2b63478dece44f0a0c0030261ae85`
- Why picked today: Hot on GitHub right now, AI-adjacent, and unusually concrete. It is not "AI magic" so much as a carefully engineered local document-ingestion pipeline with just enough OCR and layout reconstruction to be useful.

## Executive summary
LiteParse is a Rust-first document parser that turns PDFs, office docs, and images into structured text plus bounding boxes, then ships that core into Node, Python, and WASM. The interesting part is not the wrappers. The interesting part is the pipeline in [`crates/liteparse/src/parser.rs`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/liteparse/src/parser.rs), [`crates/liteparse/src/extract.rs`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/liteparse/src/extract.rs), [`crates/liteparse/src/ocr_merge.rs`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/liteparse/src/ocr_merge.rs), and especially [`crates/liteparse/src/projection.rs`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/liteparse/src/projection.rs): extract native text with PDFium, OCR only when needed, merge without duplicating, then reconstruct readable layout through a surprisingly opinionated anchor-and-grid projection engine.

The core bet is smart: local parsing quality is mostly a layout problem, not a chatbot problem. LiteParse spends its complexity budget there.

## What they built
They built a local parser with four jobs:
1. normalize non-PDF inputs into PDF when needed via [`crates/liteparse/src/conversion.rs`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/liteparse/src/conversion.rs)
2. extract character- and segment-level text geometry from PDFium via [`crates/liteparse/src/extract.rs`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/liteparse/src/extract.rs) and the wrapper crate [`crates/pdfium`](https://github.com/run-llama/liteparse/tree/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/pdfium)
3. selectively OCR only pages that look weak or image-heavy via [`crates/liteparse/src/ocr_merge.rs`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/liteparse/src/ocr_merge.rs) and the OCR API contract in [`OCR_API_SPEC.md`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/OCR_API_SPEC.md)
4. turn messy positioned text into readable page text through the projector in [`crates/liteparse/src/projection.rs`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/liteparse/src/projection.rs)

## Why it matters
Most "document AI" stacks either punt to a cloud service or overclaim on unstructured OCR. LiteParse is a good reminder that a lot of value comes from disciplined systems work:
- a strong extractor
- selective OCR instead of OCR-everything
- aggressive deduping and cleanup
- layout reconstruction that understands columns, anchors, rotated text, and margin junk

If you are building agents that read files locally, this is the kind of substrate that actually matters.

## Repo shape at a glance
Top-level layout:
- [`crates/liteparse`](https://github.com/run-llama/liteparse/tree/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/liteparse): core Rust library and `lit` CLI
- [`crates/pdfium`](https://github.com/run-llama/liteparse/tree/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/pdfium) and [`crates/pdfium-sys`](https://github.com/run-llama/liteparse/tree/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/pdfium-sys): PDFium wrapper and FFI layer
- [`crates/liteparse-napi`](https://github.com/run-llama/liteparse/tree/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/liteparse-napi), [`crates/liteparse-python`](https://github.com/run-llama/liteparse/tree/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/liteparse-python), [`crates/liteparse-wasm`](https://github.com/run-llama/liteparse/tree/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/liteparse-wasm): thin language bindings around the Rust core
- [`packages/node`](https://github.com/run-llama/liteparse/tree/cf9f08fe89a2b63478dece44f0a0c0030261ae85/packages/node), [`packages/python`](https://github.com/run-llama/liteparse/tree/cf9f08fe89a2b63478dece44f0a0c0030261ae85/packages/python), [`packages/wasm`](https://github.com/run-llama/liteparse/tree/cf9f08fe89a2b63478dece44f0a0c0030261ae85/packages/wasm): packaging, install, and developer-facing wrappers
- [`ocr/easyocr`](https://github.com/run-llama/liteparse/tree/cf9f08fe89a2b63478dece44f0a0c0030261ae85/ocr/easyocr) and [`ocr/paddleocr`](https://github.com/run-llama/liteparse/tree/cf9f08fe89a2b63478dece44f0a0c0030261ae85/ocr/paddleocr): reference HTTP OCR adapters
- [`docs`](https://github.com/run-llama/liteparse/tree/cf9f08fe89a2b63478dece44f0a0c0030261ae85/docs), [`demo`](https://github.com/run-llama/liteparse/tree/cf9f08fe89a2b63478dece44f0a0c0030261ae85/demo), [`wasm-demo-site`](https://github.com/run-llama/liteparse/tree/cf9f08fe89a2b63478dece44f0a0c0030261ae85/wasm-demo-site): docs and demos

The important thing structurally is that the packaging layer is secondary. The real product is the workspace core.

## Layered architecture dissection
### High-level system shape
The central flow in [`crates/liteparse/src/parser.rs`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/liteparse/src/parser.rs) is:
input -> optional conversion -> native text extraction -> conditional page rendering for OCR -> OCR merge -> grid projection -> text/JSON output.

### Main layers
1. **Input normalization layer**
   - [`crates/liteparse/src/conversion.rs`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/liteparse/src/conversion.rs)
   - Handles office docs and images, finds LibreOffice/ImageMagick, stages temp dirs, and keeps temp guards alive until parsing ends.

2. **PDF access layer**
   - [`crates/pdfium/src/library.rs`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/pdfium/src/library.rs)
   - [`crates/pdfium/src/document.rs`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/pdfium/src/document.rs)
   - [`crates/pdfium/src/page.rs`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/pdfium/src/page.rs)
   - Thin Rust façade over PDFium for document/page/text/render operations.

3. **Text extraction layer**
   - [`crates/liteparse/src/extract.rs`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/liteparse/src/extract.rs)
   - Works at character level, not README level. It groups chars into segments, handles invisible OCR layers, ligatures, generated glyphs, overlapping duplicates, and rotation metadata.

4. **OCR augmentation layer**
   - [`crates/liteparse/src/ocr/mod.rs`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/liteparse/src/ocr/mod.rs)
   - [`crates/liteparse/src/ocr/http_simple.rs`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/liteparse/src/ocr/http_simple.rs)
   - [`crates/liteparse/src/ocr/tesseract.rs`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/liteparse/src/ocr/tesseract.rs)
   - OCR is pluggable. The core only demands `{text, bbox, confidence}` results.

5. **Layout reconstruction layer**
   - [`crates/liteparse/src/projection.rs`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/liteparse/src/projection.rs)
   - This is the real differentiator. It detects lines, anchors, columns, flowing text blocks, rotated labels, sparse regions, and margin-number junk, then projects items onto a text grid.

6. **Bindings and packaging layer**
   - [`crates/liteparse-napi/src/lib.rs`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/liteparse-napi/src/lib.rs)
   - [`crates/liteparse-python/src/lib.rs`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/liteparse-python/src/lib.rs)
   - [`crates/liteparse-wasm/src/lib.rs`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/liteparse-wasm/src/lib.rs)
   - Fairly thin, which is the right choice.

### Request / data / control flow
- `LiteParse::parse_input` in [`parser.rs`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/liteparse/src/parser.rs) orchestrates the run.
- It resolves input via [`conversion.rs`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/liteparse/src/conversion.rs).
- It extracts pages and raw text items with [`extract.rs`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/liteparse/src/extract.rs).
- If OCR is enabled, it renders only suspect pages in [`ocr_merge.rs`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/liteparse/src/ocr_merge.rs), runs OCR concurrently, and merges only non-overlapping OCR boxes.
- Then it calls [`projection::project_pages_to_grid`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/liteparse/src/projection.rs) to reconstruct readable page text.
- Bindings simply convert inputs/outputs into JS/Python/WASM-friendly shapes.

## Key directories and files
- [`Cargo.toml`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/Cargo.toml): workspace definition, showing the actual product boundary
- [`crates/liteparse/src/parser.rs`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/liteparse/src/parser.rs): top-level orchestrator
- [`crates/liteparse/src/extract.rs`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/liteparse/src/extract.rs): hardest low-level text extraction logic
- [`crates/liteparse/src/projection.rs`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/liteparse/src/projection.rs): layout engine and the most valuable file in the repo
- [`crates/liteparse/src/ocr_merge.rs`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/liteparse/src/ocr_merge.rs): OCR gating, concurrency, merge, cleanup
- [`crates/liteparse/src/conversion.rs`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/liteparse/src/conversion.rs): external tool integration and temp-lifetime management
- [`OCR_API_SPEC.md`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/OCR_API_SPEC.md): crucial extension seam
- [`packages/node/src/lib.ts`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/packages/node/src/lib.ts) and [`packages/python/liteparse/parser.py`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/packages/python/liteparse/parser.py): packaging-facing API surfaces

## Important components
- **`SegmentBuilder`** in [`extract.rs`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/liteparse/src/extract.rs): groups characters into text items while tracking geometry, font data, ligatures, and line changes
- **`should_skip_invisible`** in [`extract.rs`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/liteparse/src/extract.rs): a subtle but important heuristic for mixed visible/invisible text layers
- **`render_pages_for_ocr`** in [`ocr_merge.rs`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/liteparse/src/ocr_merge.rs): decides which pages are worth OCRing at all
- **`ocr_and_merge_rendered`** in [`ocr_merge.rs`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/liteparse/src/ocr_merge.rs): concurrent OCR execution plus overlap-aware merge
- **anchor extraction / snap resolution / flowing-block detection** in [`projection.rs`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/liteparse/src/projection.rs): the core layout intelligence
- **binding classes** in [`crates/liteparse-napi/src/lib.rs`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/liteparse-napi/src/lib.rs) and [`crates/liteparse-python/src/lib.rs`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/liteparse-python/src/lib.rs): mostly honest transport wrappers, not a second implementation

## Important knobs / configs / extension points
- config surface in [`crates/liteparse/src/config.rs`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/liteparse/src/config.rs): OCR on/off, OCR language, target pages, DPI, page limits, quiet mode, worker count
- pluggable OCR via [`ocr/mod.rs`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/liteparse/src/ocr/mod.rs) and [`OCR_API_SPEC.md`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/OCR_API_SPEC.md)
- multi-language distribution via [`crates/liteparse-napi`](https://github.com/run-llama/liteparse/tree/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/liteparse-napi), [`crates/liteparse-python`](https://github.com/run-llama/liteparse/tree/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/liteparse-python), and [`crates/liteparse-wasm`](https://github.com/run-llama/liteparse/tree/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/liteparse-wasm)
- conversion tool discovery and fallback behavior in [`conversion.rs`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/liteparse/src/conversion.rs)

## Practical questions and answers
**How much of the value is OCR?**
Less than the marketing ecosystem would suggest. The stronger move here is using native PDF text first, then OCR only for pages with low text coverage, low text length, or images. That is both faster and cleaner.

**What is the key engineering insight?**
The killer file is [`projection.rs`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/liteparse/src/projection.rs). They treat document parsing as spatial reconstruction: anchors, columns, floating items, rotated labels, and flowing blocks. That is the part many parser repos hand-wave.

**What assumptions does the system make?**
It assumes a lot of document structure can be recovered from PDF geometry plus a moderate amount of heuristics. That is usually true for reports, forms, and papers, less true for bizarre design-heavy layouts.

**Where would it fail in production?**
Complex tables, charts, handwritten notes, very stylized brochures, and gnarly multi-column edge cases will still break. The repo is explicit that cloud LlamaParse does better on harder documents, which is probably true.

**Is the multi-language story real or shallow?**
Real enough. The bindings look thin, which is good. The architecture is not pretending JS or Python are peers to the Rust core.

## What is smart
- Selective OCR instead of blind OCR-everything in [`ocr_merge.rs`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/liteparse/src/ocr_merge.rs)
- Character-level extraction and deduping in [`extract.rs`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/liteparse/src/extract.rs)
- A genuinely serious layout projector in [`projection.rs`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/liteparse/src/projection.rs)
- OCR as a stable interface contract, not a hardcoded vendor dependency, via [`OCR_API_SPEC.md`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/OCR_API_SPEC.md)
- Thin wrappers around one core implementation instead of multiplying logic across languages

## What is flawed or weak
- The repo surface is clean, but the core depends on a large pile of heuristics. That is unavoidable, but it means correctness is empirical, not principled.
- The README sells broad multi-format support, but those formats are really "convert to PDF first, then parse," which is practical but not the same as native understanding.
- The local-vs-cloud positioning is honest, but also doubles as a funnel into LlamaParse. You can see the product ladder.
- [`projection.rs`](https://github.com/run-llama/liteparse/blob/cf9f08fe89a2b63478dece44f0a0c0030261ae85/crates/liteparse/src/projection.rs) is where the magic lives, and also where long-term maintainability risk lives. It is powerful, but dense.

## What we can learn / steal
- Treat document parsing as a geometry and reconstruction problem first.
- Put extension seams at the OCR boundary, not inside the whole parser.
- Keep wrappers thin and force quality to live in one core.
- Add selective expensive passes based on page-level heuristics, not blanket processing.
- Write tests for nasty real-world regressions, like filename sanitization and overlap deduping, not just happy paths.

## How we could apply it
If we were building a local ingestion stack for agent workflows, I would copy this shape:
- Rust or another strong systems core
- first-pass native extraction
- OCR only on suspect pages
- preserve bounding boxes all the way through
- expose a dead-simple OCR plugin contract
- keep the repo honest about what is deterministic heuristics versus what needs a bigger remote parser

I would also consider carving the projection engine into smaller submodules before it gets even bigger.

## Bottom line
LiteParse is worth studying because it is not pretending parsing is solved by vibes. The repo’s strongest idea is that readable text output comes from ruthless spatial cleanup and reconstruction, not from sprinkling AI on top. If I were stealing one thing, it would be the architecture of the extractor-plus-projector pipeline, especially the selective OCR gate and the anchor-based layout engine.