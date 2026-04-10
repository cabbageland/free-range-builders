# MarkItDown

- Repo: `microsoft/markitdown`
- URL: https://github.com/microsoft/markitdown
- Date: 2026-04-10
- Repo snapshot studied: `main` @ `63cbbd9de6afa01ee3b97127e4945c5706a29472`
- Why picked today: It is the hottest repo on GitHub today by a wide margin, it is genuinely AI-adjacent rather than fake-agent fluff, and the implementation is interesting because it treats “convert anything to LLM-friendly markdown” as a registry-and-routing problem instead of a single parser trick.

## Executive summary

MarkItDown is a document-ingestion router disguised as a tiny CLI. The core idea is simple: normalize every input into a binary stream plus a small metadata object, guess what the stream probably is, and then run a stack of converters in priority order until one can produce Markdown.

That design choice matters. It means the project is not really “a PDF tool” or “a DOCX tool”; it is a conversion bus for LLM ingestion. PDFs, Office docs, images, audio, ZIPs, HTML, YouTube pages, and even MCP requests all plug into the same dispatch path. The repo stays small because the center is thin and the format-specific intelligence lives in isolated converter modules and optional plugin packages.

The smart part is the architecture, not the markdown output alone. The weak part is also the architecture: once you promise one abstraction over many messy file types, your quality ceiling is bounded by the worst extractor in the chain, and some of the heuristics are inevitably brittle.

## What they built

They built a Python package and CLI that converts heterogeneous documents into Markdown optimized for LLM consumption.

At a high level it can ingest:
- local files
- stdin streams
- HTTP/HTTPS URLs
- `file:` URIs
- `data:` URIs

And then route those inputs through format-specific converters for:
- PDF
- DOCX
- PPTX
- XLS/XLSX/CSV
- HTML / RSS / Wikipedia / YouTube / notebook pages
- images
- audio
- EPUB
- Outlook `.msg`
- ZIP archives, recursively

Around that core, the repo also ships:
- an MCP server package for agent/tool use: [`packages/markitdown-mcp`](https://github.com/microsoft/markitdown/tree/main/packages/markitdown-mcp)
- an OCR plugin that overrides built-in converters with LLM-vision-enhanced ones: [`packages/markitdown-ocr`](https://github.com/microsoft/markitdown/tree/main/packages/markitdown-ocr)
- a sample plugin package that demonstrates the extension contract via RTF support: [`packages/markitdown-sample-plugin`](https://github.com/microsoft/markitdown/tree/main/packages/markitdown-sample-plugin)

## Why it matters

A lot of “AI file ingestion” products are wrappers around one parser plus marketing. MarkItDown is more honest and more reusable. It says: most AI systems need a rough-but-structured textual representation of messy inputs; Markdown is good enough; the problem is mainly detection, routing, and graceful degradation.

That makes it useful as:
- a pre-processor for RAG pipelines
- a normalizer for agent toolchains
- a lightweight replacement for people who do not want a massive unstructured ETL stack
- a composable library inside larger ingestion systems

The most important practical move is that the project optimizes for *LLM-readable structure*, not pixel-perfect reproduction.

## Repo shape at a glance

Top-level repo structure:

- [`packages/`](https://github.com/microsoft/markitdown/tree/main/packages) — monorepo home for the core package plus extension packages
  - [`packages/markitdown/`](https://github.com/microsoft/markitdown/tree/main/packages/markitdown) — main Python library, CLI, converters, tests
    - [`src/markitdown/_markitdown.py`](https://github.com/microsoft/markitdown/blob/main/packages/markitdown/src/markitdown/_markitdown.py) — orchestration core: input normalization, guessing, converter registry, dispatch
    - [`src/markitdown/_base_converter.py`](https://github.com/microsoft/markitdown/blob/main/packages/markitdown/src/markitdown/_base_converter.py) — converter interface and result object
    - [`src/markitdown/_stream_info.py`](https://github.com/microsoft/markitdown/blob/main/packages/markitdown/src/markitdown/_stream_info.py) — metadata carrier for mime / extension / charset / filename / URL
    - [`src/markitdown/converters/`](https://github.com/microsoft/markitdown/tree/main/packages/markitdown/src/markitdown/converters) — actual format handlers
    - [`tests/`](https://github.com/microsoft/markitdown/tree/main/packages/markitdown/tests) — CLI, module, and format-behavior tests
  - [`packages/markitdown-mcp/`](https://github.com/microsoft/markitdown/tree/main/packages/markitdown-mcp) — exposes MarkItDown as an MCP tool/server
  - [`packages/markitdown-ocr/`](https://github.com/microsoft/markitdown/tree/main/packages/markitdown-ocr) — plugin package that swaps in OCR-enhanced document converters
  - [`packages/markitdown-sample-plugin/`](https://github.com/microsoft/markitdown/tree/main/packages/markitdown-sample-plugin) — reference implementation for third-party plugins
- [`Dockerfile`](https://github.com/microsoft/markitdown/blob/main/Dockerfile) — thin container wrapper around the CLI
- [`.github/workflows/`](https://github.com/microsoft/markitdown/tree/main/.github/workflows) — CI/release plumbing
- [`README.md`](https://github.com/microsoft/markitdown/blob/main/README.md) — user-facing install/usage overview

This is a tidy monorepo, but it is not a microservices thing. It is more like “one narrow core, several packaging surfaces.”

## Layered architecture dissection

### High-level system shape

The architecture is basically:

1. **Input adapters** turn files, stdin, responses, and URIs into a binary stream plus hints.
2. **Type-guessing** enriches those hints using filename/mimetype logic plus Magika and charset detection.
3. **Converter dispatch** walks a priority-ordered registry of converters.
4. **Format-specific converters** emit Markdown.
5. **Packaging surfaces** expose that core through CLI, MCP, and plugin entry points.

That centerline lives in [`_markitdown.py`](https://github.com/microsoft/markitdown/blob/main/packages/markitdown/src/markitdown/_markitdown.py).

### Main layers

#### 1. Contract layer

The abstraction boundary is tiny:
- [`DocumentConverter`](https://github.com/microsoft/markitdown/blob/main/packages/markitdown/src/markitdown/_base_converter.py)
- [`DocumentConverterResult`](https://github.com/microsoft/markitdown/blob/main/packages/markitdown/src/markitdown/_base_converter.py)
- [`StreamInfo`](https://github.com/microsoft/markitdown/blob/main/packages/markitdown/src/markitdown/_stream_info.py)

That is the whole trick. A converter gets a seekable binary stream plus `StreamInfo`, decides whether it accepts it, and if so returns markdown. Because the contract is so narrow, the system can host wildly different converters without the core caring much.

#### 2. Ingestion + normalization layer

[`MarkItDown.convert()`](https://github.com/microsoft/markitdown/blob/main/packages/markitdown/src/markitdown/_markitdown.py), `convert_stream()`, `convert_uri()`, and `convert_response()` all collapse different input sources into the same internal representation.

Important details:
- non-seekable streams are copied into `BytesIO`
- URLs are fetched with a requests session that explicitly prefers markdown in `Accept` headers
- `file:`, `data:`, `http:`, and `https:` URIs are handled in one place
- content-disposition / URL / extension / mimetype / charset hints are all merged into `StreamInfo`

That means converter authors do not need to think about stdin vs URL vs local file. Nice separation.

#### 3. Guessing + routing layer

The real brain is `_get_stream_info_guesses()` plus `_convert()` in [`_markitdown.py`](https://github.com/microsoft/markitdown/blob/main/packages/markitdown/src/markitdown/_markitdown.py).

What it does:
- expands incomplete hints from extension ↔ mimetype
- runs [Magika](https://github.com/google/magika) on the stream to infer file type from content
- uses `charset-normalizer` for text encodings
- produces one or more plausible `StreamInfo` guesses
- sorts the converter registry by priority
- tries `accepts()` and then `convert()` for each guess/converter pair
- rewinds the stream between attempts
- records failed attempts and only throws rich conversion errors if something really tried and failed

This is the key design decision in the repo. They turned a huge format matrix into a bounded search problem.

#### 4. Converter layer

The actual format work is isolated in [`converters/`](https://github.com/microsoft/markitdown/tree/main/packages/markitdown/src/markitdown/converters).

Patterns worth noticing:
- some converters are straightforward wrappers around libraries, like [`_docx_converter.py`](https://github.com/microsoft/markitdown/blob/main/packages/markitdown/src/markitdown/converters/_docx_converter.py) using Mammoth
- some use HTML as an intermediate representation, then route through [`_html_converter.py`](https://github.com/microsoft/markitdown/blob/main/packages/markitdown/src/markitdown/converters/_html_converter.py)
- some are more heuristic-heavy, especially [`_pdf_converter.py`](https://github.com/microsoft/markitdown/blob/main/packages/markitdown/src/markitdown/converters/_pdf_converter.py)
- nested/container formats like ZIP recurse back into the core router via [`_zip_converter.py`](https://github.com/microsoft/markitdown/blob/main/packages/markitdown/src/markitdown/converters/_zip_converter.py)

So the system is not a flat set of unrelated parsers; converters can compose through the central dispatcher.

#### 5. Extension + distribution layer

There are three extension surfaces:

- **CLI** via [`packages/markitdown/src/markitdown/__main__.py`](https://github.com/microsoft/markitdown/blob/main/packages/markitdown/src/markitdown/__main__.py)
- **Plugins** discovered through Python entry points in [`_markitdown.py`](https://github.com/microsoft/markitdown/blob/main/packages/markitdown/src/markitdown/_markitdown.py)
- **MCP server** via [`packages/markitdown-mcp/src/markitdown_mcp/__main__.py`](https://github.com/microsoft/markitdown/blob/main/packages/markitdown-mcp/src/markitdown_mcp/__main__.py)

That makes the core useful both as a library and as agent infrastructure.

### Request / data / control flow

Typical path for `markitdown some.pdf`:

1. CLI in [`__main__.py`](https://github.com/microsoft/markitdown/blob/main/packages/markitdown/src/markitdown/__main__.py) parses flags.
2. It constructs `MarkItDown(...)` with built-ins enabled and maybe plugins/docintel enabled.
3. `convert()` opens the file and produces a seekable binary stream.
4. `_get_stream_info_guesses()` merges extension/mimetype hints with Magika guesses.
5. `_convert()` iterates over the priority-sorted converters.
6. [`PdfConverter`](https://github.com/microsoft/markitdown/blob/main/packages/markitdown/src/markitdown/converters/_pdf_converter.py) accepts the stream.
7. The converter returns `DocumentConverterResult(markdown=...)`.
8. The CLI writes markdown to stdout or a file.

Typical plugin path:

1. User enables plugins.
2. `_load_plugins()` loads Python entry points from the `markitdown.plugin` group.
3. Each plugin calls `register_converters(...)`.
4. Those converters enter the same routing pipeline, possibly with higher priority than built-ins.

Typical MCP path:

1. MCP tool `convert_to_markdown(uri)` receives a URI.
2. The MCP server calls `MarkItDown(...).convert_uri(uri)`.
3. Same conversion machinery runs.
4. Markdown is returned over MCP.

That reuse is elegant. The MCP server is basically a very thin shell, which is exactly what you want.

## Key directories and files

Core understanding lives in these paths:

- [`packages/markitdown/src/markitdown/_markitdown.py`](https://github.com/microsoft/markitdown/blob/main/packages/markitdown/src/markitdown/_markitdown.py)
  - orchestrator, plugin loading, guess generation, conversion dispatch, registry priorities
- [`packages/markitdown/src/markitdown/_base_converter.py`](https://github.com/microsoft/markitdown/blob/main/packages/markitdown/src/markitdown/_base_converter.py)
  - converter API contract
- [`packages/markitdown/src/markitdown/_stream_info.py`](https://github.com/microsoft/markitdown/blob/main/packages/markitdown/src/markitdown/_stream_info.py)
  - metadata merge object passed around everywhere
- [`packages/markitdown/src/markitdown/converters/_pdf_converter.py`](https://github.com/microsoft/markitdown/blob/main/packages/markitdown/src/markitdown/converters/_pdf_converter.py)
  - the gnarliest built-in converter; table/form heuristics live here
- [`packages/markitdown/src/markitdown/converters/_docx_converter.py`](https://github.com/microsoft/markitdown/blob/main/packages/markitdown/src/markitdown/converters/_docx_converter.py)
  - Office-doc path using Mammoth + HTML intermediary
- [`packages/markitdown/src/markitdown/converters/_pptx_converter.py`](https://github.com/microsoft/markitdown/blob/main/packages/markitdown/src/markitdown/converters/_pptx_converter.py)
  - slide traversal, image handling, chart/table extraction, note capture
- [`packages/markitdown/src/markitdown/converters/_html_converter.py`](https://github.com/microsoft/markitdown/blob/main/packages/markitdown/src/markitdown/converters/_html_converter.py)
  - central markdownification bridge for HTML-like intermediate outputs
- [`packages/markitdown/src/markitdown/converters/_image_converter.py`](https://github.com/microsoft/markitdown/blob/main/packages/markitdown/src/markitdown/converters/_image_converter.py)
  - exif metadata + optional LLM image caption path
- [`packages/markitdown/src/markitdown/converters/_audio_converter.py`](https://github.com/microsoft/markitdown/blob/main/packages/markitdown/src/markitdown/converters/_audio_converter.py)
  - metadata + optional transcription path
- [`packages/markitdown/src/markitdown/converters/_zip_converter.py`](https://github.com/microsoft/markitdown/blob/main/packages/markitdown/src/markitdown/converters/_zip_converter.py)
  - recursive container strategy, reusing the main router
- [`packages/markitdown/src/markitdown/converters/_doc_intel_converter.py`](https://github.com/microsoft/markitdown/blob/main/packages/markitdown/src/markitdown/converters/_doc_intel_converter.py)
  - cloud-assisted extraction route using Azure Document Intelligence
- [`packages/markitdown-mcp/src/markitdown_mcp/__main__.py`](https://github.com/microsoft/markitdown/blob/main/packages/markitdown-mcp/src/markitdown_mcp/__main__.py)
  - MCP wrapper and transport server
- [`packages/markitdown-ocr/src/markitdown_ocr/_plugin.py`](https://github.com/microsoft/markitdown/blob/main/packages/markitdown-ocr/src/markitdown_ocr/_plugin.py)
  - shows how plugins replace built-ins by priority
- [`packages/markitdown-sample-plugin/src/markitdown_sample_plugin/_plugin.py`](https://github.com/microsoft/markitdown/blob/main/packages/markitdown-sample-plugin/src/markitdown_sample_plugin/_plugin.py)
  - minimal reference for third-party extension authors

## Important components

### `MarkItDown` orchestrator

[`MarkItDown`](https://github.com/microsoft/markitdown/blob/main/packages/markitdown/src/markitdown/_markitdown.py) is the actual product. It owns:
- requests session setup
- built-in converter registration
- plugin loading
- global conversion options like LLM client/model, exiftool path, style map
- stream guess generation
- converter dispatch and fallback behavior

This is not a “fat parser”; it is more like a mini runtime.

### `StreamInfo`

[`StreamInfo`](https://github.com/microsoft/markitdown/blob/main/packages/markitdown/src/markitdown/_stream_info.py) looks humble, but it is one of the best design choices in the repo. It gives every layer one place to carry:
- mimetype
- extension
- charset
- filename
- local path
- URL

That keeps the rest of the system from devolving into giant argument soup.

### Priority-based converter registration

Converter registration is done through `register_converter(...)` in [`_markitdown.py`](https://github.com/microsoft/markitdown/blob/main/packages/markitdown/src/markitdown/_markitdown.py). Lower priority numbers run first. Built-ins mostly sit around priority `0.0`, generic catch-alls like HTML/plain text/ZIP are lower-precedence with higher numeric priority, and plugins can jump ahead by registering with negative priorities.

That is a simple mechanism with real leverage.

### HTML intermediary path

Several converters effectively do:
- parse source into HTML-ish structure
- reuse [`HtmlConverter`](https://github.com/microsoft/markitdown/blob/main/packages/markitdown/src/markitdown/converters/_html_converter.py)
- let one markdownification path handle tables/lists/basic structure

That keeps the codebase smaller and reduces formatting divergence between converters.

### `PdfConverter`

[`_pdf_converter.py`](https://github.com/microsoft/markitdown/blob/main/packages/markitdown/src/markitdown/converters/_pdf_converter.py) is where the repo gets interesting and messy. It contains logic for:
- post-processing broken line numbering
- extracting table-like structures
- detecting form-style layouts from word positions
- choosing when a page is paragraph-like vs grid-like

This is where “convert everything” stops being clean theory and turns into empirical PDF trench warfare.

### MCP wrapper

[`markitdown-mcp`](https://github.com/microsoft/markitdown/tree/main/packages/markitdown-mcp) is strategically important. It turns the package into a tool that agents can call directly. That is a natural fit: many agents need to ingest files and webpages but do not want to understand every file format themselves.

### OCR plugin override strategy

[`markitdown-ocr/_plugin.py`](https://github.com/microsoft/markitdown/blob/main/packages/markitdown-ocr/src/markitdown_ocr/_plugin.py) is a nice example of architectural leverage. It does not fork the core. It just registers OCR-enhanced converters with priority `-1.0`, so they run before the built-ins and effectively replace them when enabled.

That is clean.

## Important knobs / configs / extension points

Key knobs a builder would care about:

- optional dependency groups in [`packages/markitdown/pyproject.toml`](https://github.com/microsoft/markitdown/blob/main/packages/markitdown/pyproject.toml)
  - `pdf`, `docx`, `pptx`, `xlsx`, `xls`, `audio-transcription`, `youtube-transcription`, `az-doc-intel`, `all`
- `enable_plugins=True` on `MarkItDown(...)`
- `docintel_endpoint` and related Document Intelligence settings
- `llm_client`, `llm_model`, `llm_prompt` for image descriptions and OCR plugin flows
- `keep_data_uris` for retaining inline image payloads in markdown output
- `style_map` for DOCX conversion customization via Mammoth
- plugin discovery through Python entry points under `markitdown.plugin`
- `MARKITDOWN_ENABLE_PLUGINS` env var for the MCP package

The nicest part is that the knobs mostly stay at package construction boundaries rather than leaking everywhere.

## Practical questions and answers

### Why does this repo feel smaller than its capability list suggests?

Because the capability list is produced by a stable central runtime plus lots of narrow adapters. That is better than stuffing all logic into one monster parser.

### What is the actual core innovation?

Not Markdown. Not any one converter. It is the combination of:
- unified stream abstraction
- metadata guessing + compatibility checks
- stable priority-based converter routing
- plugin override support

That combination makes the surface area extensible without turning the codebase into soup.

### Where would this fail in production?

Mostly where all ingestion systems fail:
- ugly PDFs with weird layout semantics
- scanned documents without the right OCR path enabled
- inconsistent Office exports
- huge archives or mixed nested content
- multimodal description quality varying with model choice
- network-bound URL conversions that pull unexpected content or rate-limit

Also: the project can *convert* many things, but “good enough markdown” is a moving target depending on your downstream task.

### Is the plugin system real or decorative?

Real enough. The OCR plugin and sample plugin both use the same entry-point mechanism the core loads in [`_load_plugins()`](https://github.com/microsoft/markitdown/blob/main/packages/markitdown/src/markitdown/_markitdown.py). The OCR package is especially convincing because it uses priority override instead of awkward monkey-patching.

### Why is ZIP support more important than it first looks?

Because ZIP is a container format. By recursively feeding member files back into the main conversion router, MarkItDown shows it understands ingestion as a graph problem, not just a flat file-extension problem.

### Is the MCP package substantial?

Operationally yes, structurally no. That is good. The best wrapper is a thin wrapper around a good core, and that is what [`markitdown-mcp`](https://github.com/microsoft/markitdown/tree/main/packages/markitdown-mcp) is.

## What is smart

- **The abstraction boundary is tiny.** Stream + metadata + converter contract is enough.
- **Priority-based dispatch is simple and powerful.** No over-engineered plugin framework required.
- **The repo is honest about optional capabilities.** Feature groups in `pyproject.toml` make dependency cost explicit.
- **The HTML intermediary is pragmatic.** Reusing one markdownification path beats duplicating formatting logic everywhere.
- **MCP packaging is strategically correct.** This repo naturally belongs in agent stacks.
- **Plugin override via priority is elegant.** The OCR plugin demonstrates a clean extension story.
- **They normalized around seekable binary streams.** That avoids a whole class of adapter weirdness.

## What is flawed or weak

- **PDF quality is heuristic-bound.** The more “supports PDF” becomes central to the pitch, the more users will blame the whole system for one cursed layout.
- **Output fidelity is intentionally lossy.** That is fine for LLM ingestion, but some users will still expect “document conversion” to mean prettier reproduction.
- **Converter quality is uneven by nature.** A DOCX via Mammoth and a weird scanned PDF are not equally reliable, yet the top-level interface flattens that difference.
- **Plugin safety is trust-based.** Entry-point plugins run Python code in-process; that is normal for Python, but not exactly a hardened extension model.
- **The MCP server has a sharp edge.** The code explicitly warns that non-localhost binding exposes file/network access with no authentication in [`markitdown_mcp/__main__.py`](https://github.com/microsoft/markitdown/blob/main/packages/markitdown-mcp/src/markitdown_mcp/__main__.py). Good warning, but still a footgun for careless users.
- **The repo’s marketing headline undersells the hard parts.** “Convert files to Markdown” sounds trivial until you meet PDFs, OCR, charts, encodings, and nested archives.

## What we can learn / steal

- Build the narrowest possible core contract first.
- Normalize messy inputs before you specialize them.
- Use stable priority ordering instead of giant conditional jungles.
- Let plugins *replace* built-ins cleanly instead of bolting on afterthought hooks.
- Keep dependency-heavy capabilities optional.
- Reuse intermediary representations when several formats converge structurally.
- Be explicit about where the system is heuristic and lossy.

## How we could apply it

A few reusable ideas worth stealing:

1. **Agent ingestion tool design**
   - For any “read arbitrary artifacts” tool, copy the pattern of `convert_uri` / `convert_stream` / `convert_response` collapsing into one dispatch path.

2. **Extension architecture**
   - If we build multi-format readers, indexers, or importers, use negative-priority plugin overrides the way `markitdown-ocr` does instead of special-case branching.

3. **LLM pipeline hygiene**
   - Convert upstream into a coarse but regular text representation before retrieval/analysis. Downstream systems become simpler when input normalization is someone else’s job.

4. **Monorepo packaging discipline**
   - Keep the core package small and ship adjacent distribution surfaces as sibling packages, not tangled subcommands.

5. **Heuristic honesty**
   - When quality varies by input class, expose that variance clearly rather than pretending one API call means equal reliability across formats.

## Bottom line

MarkItDown is not magic document understanding. It is a well-shaped ingestion runtime for turning messy artifacts into LLM-friendly Markdown.

That sounds modest, but the repo is worth studying because it gets the architecture mostly right:
- one narrow core
- converter registry instead of spaghetti branching
- optional heavy features
- plugins that genuinely extend behavior
- agent-facing packaging via MCP

The main lesson is not “Markdown good.” The main lesson is: if you have a messy many-format problem, build a small dispatch kernel with clean extension boundaries, then let format-specific ugliness live at the edges where it belongs.
