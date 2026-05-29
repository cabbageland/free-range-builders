# LiteParse

- Repo: `run-llama/liteparse`
- URL: https://github.com/run-llama/liteparse
- Date: 2026-05-29
- Repo snapshot studied: `main` @ `291148f3f3e4e9673066a22f068108e738fcb685`
- Why picked today: It was on GitHub’s trending/explore page on May 29, 2026, it is AI-adjacent without being fake-AI, and the implementation looks like a serious attempt to make local document parsing good enough for agents without hiding behind a cloud VLM.

## Executive summary

LiteParse is a Rust-first document parser whose real trick is not OCR, it is **layout reconstruction**. The pipeline extracts native PDF text with PDFium, selectively OCRs only the weak pages, then projects all those boxes back onto a text grid so the output preserves enough structure for downstream LLM or retrieval use. The repo is small enough to understand in one sitting, but opinionated enough to teach something.

The smartest design choice is that the product surface is multi-language, but the system is not multi-implementation. There is one Rust core, then thin wrappers for Node, Python, CLI, and WASM.

## What they built

They built a local document parsing stack with:

- native PDF text extraction via [`crates/liteparse/src/extract.rs`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/crates/liteparse/src/extract.rs)
- selective OCR and merge logic via [`crates/liteparse/src/ocr_merge.rs`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/crates/liteparse/src/ocr_merge.rs)
- layout reconstruction via [`crates/liteparse/src/projection.rs`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/crates/liteparse/src/projection.rs)
- document conversion for Office files and images via [`crates/liteparse/src/conversion.rs`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/crates/liteparse/src/conversion.rs)
- language bindings in [`crates/liteparse-napi`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/crates/liteparse-napi), [`crates/liteparse-python`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/crates/liteparse-python), and [`crates/liteparse-wasm`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/crates/liteparse-wasm)

It is basically an “agent-ready parser” that stays local by default.

## Why it matters

A lot of document tooling has split into two bad camps:

- cheap text extraction that loses layout and table shape
- expensive cloud parsing that hides the mechanism behind API magic

LiteParse sits in the middle. It says: get as far as possible with native text, OCR only where needed, and reconstruct readable text from spatial boxes. That is a practical builder stance.

## Repo shape at a glance

Top-level structure:

- [`crates/`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/crates) , the real system
  - [`liteparse/`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/crates/liteparse) , core parser and CLI
  - [`pdfium/`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/crates/pdfium) and [`pdfium-sys/`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/crates/pdfium-sys) , PDF bindings layer
  - [`liteparse-napi/`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/crates/liteparse-napi) , Node bridge
  - [`liteparse-python/`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/crates/liteparse-python) , PyO3 bridge
  - [`liteparse-wasm/`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/crates/liteparse-wasm) , browser bridge
- [`packages/`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/packages) , language packaging and JS/Python-facing wrappers
- [`ocr/`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/ocr) , example OCR server adapters
- [`docs/`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/docs) and [`demo/`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/demo) , product/docs layer
- [`integration_tests_data/`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/integration_tests_data) , fixture corpus
- [`.github/workflows/ci.yml`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/.github/workflows/ci.yml) , cross-platform build and smoke tests

This is a healthy shape. Core logic is concentrated, wrappers are thin, and infra is not sprawling.

## Layered architecture dissection

### High-level system shape

The central object is [`LiteParse`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/crates/liteparse/src/parser.rs). It orchestrates:

1. input normalization and format conversion
2. native PDF text extraction
3. optional page rendering for OCR
4. OCR execution and merge
5. projection of spatial boxes into readable page text
6. output formatting or screenshots

That means the product is really a pipeline engine, not just a parser function.

### Main layers

**1. Input and conversion layer**

- [`crates/liteparse/src/conversion.rs`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/crates/liteparse/src/conversion.rs)

This layer decides whether input is already PDF, can be converted through LibreOffice, or should go through ImageMagick. It also keeps temp dirs alive with `PdfInputGuard`, which is a tiny but important piece of hygiene.

**2. Raw extraction layer**

- [`crates/liteparse/src/extract.rs`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/crates/liteparse/src/extract.rs)

This is where the real PDF work starts. Instead of trusting PDFium’s higher-level text rect API, LiteParse walks characters and builds its own text segments. That is the right kind of stubbornness. It lets them handle ligatures, invisible OCR layers, buggy embedded fonts, duplicate text objects, and line breaks with much more control.

**3. OCR layer**

- [`crates/liteparse/src/ocr/mod.rs`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/crates/liteparse/src/ocr/mod.rs)
- [`crates/liteparse/src/ocr/tesseract.rs`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/crates/liteparse/src/ocr/tesseract.rs)
- [`crates/liteparse/src/ocr/http_simple.rs`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/crates/liteparse/src/ocr/http_simple.rs)
- [`OCR_API_SPEC.md`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/OCR_API_SPEC.md)

OCR is deliberately abstracted behind a small engine interface. Built-in Tesseract is the local default, but they also support an HTTP OCR contract. That makes the product extensible without infecting the core with vendor-specific logic.

**4. OCR merge layer**

- [`crates/liteparse/src/ocr_merge.rs`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/crates/liteparse/src/ocr_merge.rs)

This layer is better than it first looks. OCR is not run on every page. They render only pages that appear text-sparse, low-coverage, or image-heavy, then merge OCR boxes only when they do not overlap existing text. That is the key anti-slop move in the whole repo.

**5. Projection layer**

- [`crates/liteparse/src/projection.rs`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/crates/liteparse/src/projection.rs)

This is the heart of the repo. It groups boxes into lines and blocks, detects anchors, reasons about left/right/center snapping, special-cases rotated text, compresses pathological spacing, and decides when a block should be rendered as flowing paragraph text versus structured columns. This file is huge because the product’s actual value lives here.

**6. Binding and distribution layer**

- [`crates/liteparse-napi/src/lib.rs`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/crates/liteparse-napi/src/lib.rs)
- [`crates/liteparse-python/src/lib.rs`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/crates/liteparse-python/src/lib.rs)
- [`crates/liteparse-wasm/src/lib.rs`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/crates/liteparse-wasm/src/lib.rs)
- [`packages/node/src/cli.ts`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/packages/node/src/cli.ts)

The wrappers mostly translate config and types. That is exactly what you want. The repo avoids the classic failure mode where each SDK slowly becomes its own parser.

### Request / data / control flow

Typical parse flow:

1. caller creates config in Rust, Node, Python, or WASM
2. [`parser.rs`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/crates/liteparse/src/parser.rs) resolves the input into a PDF if needed
3. [`extract.rs`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/crates/liteparse/src/extract.rs) extracts native text items page by page
4. if OCR is enabled, [`ocr_merge.rs`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/crates/liteparse/src/ocr_merge.rs) renders only suspect pages and runs OCR concurrently
5. OCR results are merged back into page text items if they do not collide with existing text
6. [`projection.rs`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/crates/liteparse/src/projection.rs) reconstructs a readable text grid
7. output modules or wrappers serialize results

That flow is legible, and the logging hooks in `parser.rs` make performance visible.

## Key directories and files

- [`Cargo.toml`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/Cargo.toml), clean workspace definition
- [`crates/liteparse/src/parser.rs`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/crates/liteparse/src/parser.rs), orchestration brain
- [`crates/liteparse/src/extract.rs`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/crates/liteparse/src/extract.rs), character-level text extraction
- [`crates/liteparse/src/projection.rs`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/crates/liteparse/src/projection.rs), layout heuristics engine
- [`crates/liteparse/src/ocr_merge.rs`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/crates/liteparse/src/ocr_merge.rs), selective OCR merge
- [`crates/liteparse/src/conversion.rs`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/crates/liteparse/src/conversion.rs), format conversion boundary
- [`crates/liteparse/src/main.rs`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/crates/liteparse/src/main.rs), CLI surface
- [`OCR_API_SPEC.md`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/OCR_API_SPEC.md), external OCR contract
- [`.github/workflows/ci.yml`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/.github/workflows/ci.yml), portability discipline

## Important components

- `LiteParse::parse_input` in [`parser.rs`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/crates/liteparse/src/parser.rs), the entire end-to-end pipeline
- `extract_page_text_items` in [`extract.rs`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/crates/liteparse/src/extract.rs), the low-level quality lever
- `render_pages_for_ocr` and `ocr_and_merge_rendered` in [`ocr_merge.rs`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/crates/liteparse/src/ocr_merge.rs), where cost control and merge sanity live
- `project_to_grid` in [`projection.rs`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/crates/liteparse/src/projection.rs), the mechanism that turns coordinates into usable text
- the WASM OCR bridge in [`crates/liteparse-wasm/src/lib.rs`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/crates/liteparse-wasm/src/lib.rs), a nice example of keeping browser OCR pluggable instead of pretending the browser is the same runtime

## Important knobs / configs / extension points

- OCR on/off, OCR language, OCR server URL in [`config.rs`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/crates/liteparse/src/config.rs)
- `target_pages`, `max_pages`, and `dpi`, which matter for both latency and fidelity
- `num_workers`, which controls OCR concurrency rather than blindly maxing out the box
- the HTTP OCR contract in [`OCR_API_SPEC.md`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/OCR_API_SPEC.md)
- wrapper-specific config translation in [`crates/liteparse-napi/src/lib.rs`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/crates/liteparse-napi/src/lib.rs), [`crates/liteparse-python/src/lib.rs`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/crates/liteparse-python/src/lib.rs), and [`crates/liteparse-wasm/src/lib.rs`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/crates/liteparse-wasm/src/lib.rs)

## Practical questions and answers

**How much of the value is “OCR”?**  
Not that much. The value is the decision logic around when to OCR and how to merge it back.

**What is the most reusable idea here?**  
Treat document parsing as a reconciliation problem between native text, OCR text, and page geometry.

**Where would this fail in production?**  
Very weird tables, diagram-heavy PDFs, and edge-case layouts will keep forcing more projection heuristics. That file will only grow.

**Does the repo seem honest about scope?**  
Mostly yes. The README explicitly says complex docs will do better with LlamaParse. That honesty makes the OSS version more credible, not less.

**Is the multi-language support real or superficial?**  
Real enough. The bindings look thin and disciplined, which usually means the core can stay coherent.

## What is smart

- The selective OCR heuristic. Only OCRing low-text or image-heavy pages is the right cost/latency trade.
- The character-level extraction approach. They clearly learned that higher-level PDF text APIs lie.
- One Rust core, many thin wrappers.
- The OCR HTTP spec is intentionally tiny, which makes extension likely instead of theoretical.
- CI runs across Linux, macOS, and Windows in [`.github/workflows/ci.yml`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/.github/workflows/ci.yml), which matters for a parsing tool that touches native deps.

## What is flawed or weak

- [`projection.rs`](https://github.com/run-llama/liteparse/blob/291148f3f3e4e9673066a22f068108e738fcb685/crates/liteparse/src/projection.rs) is doing heroic work, but it is also the maintenance risk. The value is there, but so is future brittleness.
- The non-PDF conversion path depends on external system tools. That is pragmatic, but it means “works locally” can still mean “works if your machine is shaped correctly.”
- The project’s differentiation may be hard to defend if major parser stacks copy the same selective-OCR-plus-projection playbook.
- It is excellent for extraction mechanics, but it is not a full semantic document understanding system. That is fine, just important.

## What we can learn / steal

- Keep the core algorithm in one place and let bindings stay dumb.
- Prefer explicit extension contracts over deep plugin frameworks.
- When dealing with messy source formats, own the reconciliation layer instead of pretending upstream libraries solved it.
- Put the hard-earned heuristics where builders can inspect them. One gnarly file is sometimes better than ten fake-abstraction files.

## How we could apply it

If we were building ingestion for an agent system, I would steal this architecture almost directly:

- native extraction first
- OCR only where evidence says it is needed
- merge with collision checks
- preserve geometry in the structured output
- keep a human-readable text projection alongside machine-friendly JSON

I would also copy the “single core, thin bindings” pattern for any multi-runtime tooling.

## Bottom line

LiteParse is a good repo because it is trying to win on mechanism, not vibes. The core insight is that better local parsing comes from **careful reconciliation of boxes, text, and OCR**, not from slapping an LLM over every page. It is the kind of repo that teaches builders how much product value can hide inside unglamorous heuristics.