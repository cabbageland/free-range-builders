# Understand Anything

- Repo: `Lum1104/Understand-Anything`
- URL: https://github.com/Lum1104/Understand-Anything
- Date: 2026-05-26
- Repo snapshot studied: `main` @ `26edf61856fa476e466bda1814819a266a293c47`
- Why picked today: It was still a hot GitHub repo on 2026-05-26, it is directly aimed at the AI coding-tool moment, and the implementation has more real architecture in it than the usual repo-chat hype wrappers.

## Executive summary
Understand Anything turns a codebase or wiki into a reusable graph artifact, then layers multiple experiences on top of that artifact: graph exploration, chat context, diff analysis, onboarding, domain mapping, and knowledge-base browsing. The repo is interesting not because it has an interactive graph, but because it is increasingly strict about what should be deterministic versus what should be LLM-generated.

The key insight is that the project is quietly becoming less agent-mystical and more engineering-serious. File scanning, language detection, ignore handling, parser dispatch, and work batching are handled by code. The model layer is mostly used for semantic labeling, summaries, and review. That boundary is the smartest thing in the repo.

## What they built
They built a cross-platform repo-understanding system that:

- scans repositories and wiki-like knowledge bases into a graph JSON artifact
- extracts files, functions, classes, imports, calls, definitions, and some non-code entities
- enriches the graph with summaries, layers, tours, domain views, and knowledge links
- exposes task-specific flows for chat, explain, onboarding, and diff analysis
- renders an interactive dashboard for structural and knowledge exploration
- packages the whole thing for Claude Code, Codex, Cursor, Copilot, Gemini CLI, OpenClaw, and others

The most important source areas are:

- root product surface in [`README.md`](https://github.com/Lum1104/Understand-Anything/blob/26edf61856fa476e466bda1814819a266a293c47/README.md)
- plugin-facing workflows in [`understand-anything-plugin/skills/`](https://github.com/Lum1104/Understand-Anything/tree/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/skills)
- graph core in [`understand-anything-plugin/packages/core/src/`](https://github.com/Lum1104/Understand-Anything/tree/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/packages/core/src)
- dashboard UI in [`understand-anything-plugin/packages/dashboard/src/`](https://github.com/Lum1104/Understand-Anything/tree/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/packages/dashboard/src)
- task-specific prompt/context builders in [`understand-anything-plugin/src/`](https://github.com/Lum1104/Understand-Anything/tree/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/src)
- agent contracts in [`understand-anything-plugin/agents/`](https://github.com/Lum1104/Understand-Anything/tree/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/agents)

## Why it matters
A lot of code-intelligence projects still blur together because they ask models to do everything, including jobs that should be boring infrastructure. Understand Anything matters because it is moving toward a more durable split: parsers and scripts establish structural truth, then models explain and organize that truth.

That makes the project more reusable. Once the graph exists, the same intermediate representation can power multiple product surfaces instead of rebuilding context separately for every feature.

## Repo shape at a glance
Top-level structure:

- [`assets/`](https://github.com/Lum1104/Understand-Anything/tree/26edf61856fa476e466bda1814819a266a293c47/assets): screenshots and promo images
- [`docs/`](https://github.com/Lum1104/Understand-Anything/tree/26edf61856fa476e466bda1814819a266a293c47/docs): docs and feature writeups
- [`homepage/`](https://github.com/Lum1104/Understand-Anything/tree/26edf61856fa476e466bda1814819a266a293c47/homepage): Astro marketing/demo site
- [`scripts/`](https://github.com/Lum1104/Understand-Anything/tree/26edf61856fa476e466bda1814819a266a293c47/scripts): helper scripts
- [`tests/`](https://github.com/Lum1104/Understand-Anything/tree/26edf61856fa476e466bda1814819a266a293c47/tests): higher-level skill tests
- [`understand-anything-plugin/`](https://github.com/Lum1104/Understand-Anything/tree/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin): the real product core
  - [`agents/`](https://github.com/Lum1104/Understand-Anything/tree/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/agents): role specs for scanner, analyzer, reviewer, domain, and tour workers
  - [`hooks/`](https://github.com/Lum1104/Understand-Anything/tree/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/hooks): post-commit auto-update wiring
  - [`packages/core/`](https://github.com/Lum1104/Understand-Anything/tree/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/packages/core): graph schema, parsers, language registry, persistence, search
  - [`packages/dashboard/`](https://github.com/Lum1104/Understand-Anything/tree/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/packages/dashboard): React dashboard and graph UI
  - [`skills/`](https://github.com/Lum1104/Understand-Anything/tree/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/skills): end-user commands plus deterministic analysis scripts
  - [`src/`](https://github.com/Lum1104/Understand-Anything/tree/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/src): prompt/context builders for chat, diff, explain, onboarding

The repo is broad, but the internal split is understandable: distribution, analysis core, dashboard, skill contracts, and feature-specific prompt builders.

## Layered architecture dissection
### High-level system shape
At a high level the system does this:

1. install the plugin into many coding environments
2. scan the target repo deterministically
3. extract structural facts with parser-backed analyzers
4. batch work by dependency structure
5. enrich the graph with human-readable summaries and domain semantics
6. persist a shared graph artifact
7. reuse that artifact across dashboard and task-specific experiences

## Main layers
**1. Distribution and platform adaptation**

[`install.sh`](https://github.com/Lum1104/Understand-Anything/blob/26edf61856fa476e466bda1814819a266a293c47/install.sh), [`install.ps1`](https://github.com/Lum1104/Understand-Anything/blob/26edf61856fa476e466bda1814819a266a293c47/install.ps1), and the plugin descriptor files under [`.claude-plugin/`](https://github.com/Lum1104/Understand-Anything/tree/26edf61856fa476e466bda1814819a266a293c47/.claude-plugin), [`.cursor-plugin/`](https://github.com/Lum1104/Understand-Anything/tree/26edf61856fa476e466bda1814819a266a293c47/.cursor-plugin), and [`.copilot-plugin/`](https://github.com/Lum1104/Understand-Anything/tree/26edf61856fa476e466bda1814819a266a293c47/.copilot-plugin) are distribution plumbing. It is unglamorous, but it is core to the thesis that repo understanding should live wherever developers already are.

**2. Deterministic scan and preprocessing**

[`understand-anything-plugin/skills/understand/scan-project.mjs`](https://github.com/Lum1104/Understand-Anything/blob/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/skills/understand/scan-project.mjs) is one of the most important files in the repo. It explicitly documents the decision to replace LLM-authored one-off scan scripts with deterministic file enumeration, ignore filtering, language detection, file categorization, and complexity estimation.

[`understand-anything-plugin/skills/understand/extract-import-map.mjs`](https://github.com/Lum1104/Understand-Anything/blob/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/skills/understand/extract-import-map.mjs), [`extract-structure.mjs`](https://github.com/Lum1104/Understand-Anything/blob/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/skills/understand/extract-structure.mjs), and [`build-fingerprints.mjs`](https://github.com/Lum1104/Understand-Anything/blob/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/skills/understand/build-fingerprints.mjs) continue that pattern.

**3. Core graph extraction and normalization**

[`understand-anything-plugin/packages/core/src/plugins/tree-sitter-plugin.ts`](https://github.com/Lum1104/Understand-Anything/blob/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/packages/core/src/plugins/tree-sitter-plugin.ts) is the structural extractor backbone. It loads grammars, routes files to language-specific extractors, and resolves imports/calls where possible.

[`understand-anything-plugin/packages/core/src/analyzer/graph-builder.ts`](https://github.com/Lum1104/Understand-Anything/blob/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/packages/core/src/analyzer/graph-builder.ts) turns extracted facts into nodes and edges. [`understand-anything-plugin/packages/core/src/schema.ts`](https://github.com/Lum1104/Understand-Anything/blob/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/packages/core/src/schema.ts) provides the IR contract that keeps all downstream features pointed at the same data model.

**4. LLM enrichment layer**

[`understand-anything-plugin/packages/core/src/analyzer/llm-analyzer.ts`](https://github.com/Lum1104/Understand-Anything/blob/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/packages/core/src/analyzer/llm-analyzer.ts) is a clean statement of what the model is for: file summaries, project summaries, tags, and language notes. This is the right place for fuzzier semantic work.

**5. Batch orchestration and graph teaching**

[`understand-anything-plugin/skills/understand/compute-batches.mjs`](https://github.com/Lum1104/Understand-Anything/blob/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/skills/understand/compute-batches.mjs) groups related files using graph/community logic so analysis batches track dependency neighborhoods instead of arbitrary file counts.

The agent contracts in [`understand-anything-plugin/agents/`](https://github.com/Lum1104/Understand-Anything/tree/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/agents) then add architecture reviews, tours, and domain-oriented interpretation.

**6. Task-specific retrieval layer**

[`understand-anything-plugin/src/context-builder.ts`](https://github.com/Lum1104/Understand-Anything/blob/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/src/context-builder.ts), [`diff-analyzer.ts`](https://github.com/Lum1104/Understand-Anything/blob/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/src/diff-analyzer.ts), [`explain-builder.ts`](https://github.com/Lum1104/Understand-Anything/blob/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/src/explain-builder.ts), and [`onboard-builder.ts`](https://github.com/Lum1104/Understand-Anything/blob/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/src/onboard-builder.ts) show the product strategy clearly. The graph is not the end product. It is the shared substrate for multiple understanding tasks.

**7. Interactive dashboard layer**

[`understand-anything-plugin/packages/dashboard/src/components/GraphView.tsx`](https://github.com/Lum1104/Understand-Anything/blob/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/packages/dashboard/src/components/GraphView.tsx), [`KnowledgeGraphView.tsx`](https://github.com/Lum1104/Understand-Anything/blob/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/packages/dashboard/src/components/KnowledgeGraphView.tsx), and [`DomainGraphView.tsx`](https://github.com/Lum1104/Understand-Anything/blob/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/packages/dashboard/src/components/DomainGraphView.tsx) turn the graph into something explorable instead of merely serializable. Utility files like [`utils/louvain.ts`](https://github.com/Lum1104/Understand-Anything/blob/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/packages/dashboard/src/utils/louvain.ts) and [`utils/elk-layout.ts`](https://github.com/Lum1104/Understand-Anything/blob/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/packages/dashboard/src/utils/elk-layout.ts) matter because graph UX dies without sensible clustering and layout.

### Request / data / control flow
A simplified flow looks like this:

- user invokes `/understand` as defined in [`understand-anything-plugin/skills/understand/SKILL.md`](https://github.com/Lum1104/Understand-Anything/blob/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/skills/understand/SKILL.md)
- deterministic scripts scan the project and generate import/structure fingerprints in [`skills/understand/`](https://github.com/Lum1104/Understand-Anything/tree/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/skills/understand)
- parser-backed core code extracts functions, classes, imports, exports, and call relationships via [`packages/core/src/plugins/`](https://github.com/Lum1104/Understand-Anything/tree/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/packages/core/src/plugins)
- [`graph-builder.ts`](https://github.com/Lum1104/Understand-Anything/blob/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/packages/core/src/analyzer/graph-builder.ts) assembles the knowledge graph
- LLM analyzers and agent contracts enrich that graph with summaries, tours, and domain semantics
- the final JSON artifact feeds dashboard views plus task-specific prompt builders for chat, explain, diff, and onboarding

## Key directories and files
- [`README.md`](https://github.com/Lum1104/Understand-Anything/blob/26edf61856fa476e466bda1814819a266a293c47/README.md): product scope, install surface, and workflow overview
- [`understand-anything-plugin/skills/understand/SKILL.md`](https://github.com/Lum1104/Understand-Anything/blob/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/skills/understand/SKILL.md): pipeline contract for `/understand`
- [`understand-anything-plugin/skills/understand/scan-project.mjs`](https://github.com/Lum1104/Understand-Anything/blob/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/skills/understand/scan-project.mjs): deterministic scanner and file classifier
- [`understand-anything-plugin/skills/understand/compute-batches.mjs`](https://github.com/Lum1104/Understand-Anything/blob/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/skills/understand/compute-batches.mjs): dependency-aware batching
- [`understand-anything-plugin/packages/core/src/plugins/tree-sitter-plugin.ts`](https://github.com/Lum1104/Understand-Anything/blob/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/packages/core/src/plugins/tree-sitter-plugin.ts): grammar loading and structural extraction
- [`understand-anything-plugin/packages/core/src/analyzer/graph-builder.ts`](https://github.com/Lum1104/Understand-Anything/blob/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/packages/core/src/analyzer/graph-builder.ts): node/edge assembly
- [`understand-anything-plugin/packages/core/src/analyzer/llm-analyzer.ts`](https://github.com/Lum1104/Understand-Anything/blob/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/packages/core/src/analyzer/llm-analyzer.ts): LLM prompt and response contract
- [`understand-anything-plugin/packages/dashboard/src/components/GraphView.tsx`](https://github.com/Lum1104/Understand-Anything/blob/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/packages/dashboard/src/components/GraphView.tsx): main structural graph UI
- [`understand-anything-plugin/src/context-builder.ts`](https://github.com/Lum1104/Understand-Anything/blob/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/src/context-builder.ts): graph-to-chat context shaping

## Important components
**Deterministic project scanner**

[`scan-project.mjs`](https://github.com/Lum1104/Understand-Anything/blob/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/skills/understand/scan-project.mjs) is the maturity marker. It explicitly frames LLM filesystem walking as a bad trade and replaces it with code.

**Tree-sitter-backed extractor layer**

[`tree-sitter-plugin.ts`](https://github.com/Lum1104/Understand-Anything/blob/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/packages/core/src/plugins/tree-sitter-plugin.ts) is the core structural engine. It loads grammars, picks extractors by language, and degrades gracefully when a grammar is unavailable.

**Graph assembly spine**

[`graph-builder.ts`](https://github.com/Lum1104/Understand-Anything/blob/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/packages/core/src/analyzer/graph-builder.ts) creates file, function, class, and non-code nodes plus contains/imports/calls edges. This is the product spine.

**Semantic prompt contract**

[`llm-analyzer.ts`](https://github.com/Lum1104/Understand-Anything/blob/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/packages/core/src/analyzer/llm-analyzer.ts) is deliberately narrow. That narrowness is a strength.

**Graph UX engine**

[`GraphView.tsx`](https://github.com/Lum1104/Understand-Anything/blob/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/packages/dashboard/src/components/GraphView.tsx) is what stops the graph from becoming an unreadable node dump. It is where usability earns or loses the whole thesis.

**State model that preserves multiple views of the same graph**

[`packages/dashboard/src/store.ts`](https://github.com/Lum1104/Understand-Anything/blob/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/packages/dashboard/src/store.ts) does more than hold UI toggles. It keeps separate indexes for first-match layer navigation versus all-layer membership filtering. That is a small but serious sign that the team has already hit real graph-navigation edge cases and encoded them explicitly instead of pretending every node belongs to one clean place.

## Important knobs / configs / extension points
- multi-platform install paths in [`install.sh`](https://github.com/Lum1104/Understand-Anything/blob/26edf61856fa476e466bda1814819a266a293c47/install.sh)
- command behavior and analysis options in [`understand-anything-plugin/skills/understand/SKILL.md`](https://github.com/Lum1104/Understand-Anything/blob/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/skills/understand/SKILL.md)
- parser and extractor extension points in [`understand-anything-plugin/packages/core/src/plugins/`](https://github.com/Lum1104/Understand-Anything/tree/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/packages/core/src/plugins)
- language registration in [`understand-anything-plugin/packages/core/src/languages/`](https://github.com/Lum1104/Understand-Anything/tree/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/packages/core/src/languages)
- dashboard interaction state and indexing tradeoffs in [`understand-anything-plugin/packages/dashboard/src/store.ts`](https://github.com/Lum1104/Understand-Anything/blob/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/packages/dashboard/src/store.ts)
- token-gated dashboard loading and data fetch flow in [`understand-anything-plugin/packages/dashboard/src/App.tsx`](https://github.com/Lum1104/Understand-Anything/blob/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/packages/dashboard/src/App.tsx)
- auto-update hook wiring in [`understand-anything-plugin/hooks/hooks.json`](https://github.com/Lum1104/Understand-Anything/blob/26edf61856fa476e466bda1814819a266a293c47/understand-anything-plugin/hooks/hooks.json)

## Practical questions and answers
**What is the deepest idea in the repo?**

The shared graph artifact. Once they have the graph, they can reuse it for browsing, teaching, prompting, diff analysis, and onboarding.

**What is the sharpest recent engineering move?**

Replacing prompt-written scan logic with deterministic scripts. That cuts cost, latency, and failure modes all at once.

**What is the clever practical move?**

Dependency-aware batching, plus explicit dashboard state indexes for navigation versus filtering. Grouping related files before semantic analysis improves context quality, and splitting first-match layer lookup from all-layer membership keeps the UI honest when one node participates in more than one architectural slice.

**What is still fragile?**

Anything that claims semantic truth beyond structural truth. Domain views, summaries, and guided tours can still become polished wrongness.

**What is the product really selling?**

Not just a graph, but a reusable understanding substrate that many AI coding surfaces can consume.

## What is smart
- drawing a cleaner deterministic-versus-LLM boundary
- using tree-sitter and explicit registries instead of prompt improv for structural work
- treating the graph JSON as a durable intermediate representation
- batching analysis around dependency neighborhoods instead of arbitrary file counts
- investing in UI aggregation and layout so the graph teaches instead of merely impressing

## What is flawed or weak
- platform sprawl creates support tax, because every new coding surface adds packaging and behavior drift risk
- prompt-defined behavior still acts like code but is harder to test and version than normal code
- the repo is broad enough that marketing site, runtime adapters, product logic, and experiments can feel crowded together
- semantic layers remain the least trustworthy part of the system, especially when crossing from code structure into business meaning

## What we can learn / steal
- make parser, scan, and batching layers deterministic as early as possible
- centralize extracted structure in one shared IR that multiple product surfaces can reuse
- use dependency structure to shape analysis work instead of slicing by file count
- design graph UX around aggregation and progressive reveal, not maximal node display
- use LLMs for explanation and interpretation after extraction, not as a substitute for extraction

## How we could apply it
If we built repo-intelligence tooling ourselves, the first things worth copying would be:

1. deterministic scan plus ignore handling
2. grammar-backed structural extraction
3. a typed graph IR shared across features
4. dependency-aware batching before semantic enrichment
5. a graph UI that defaults to grouped structure and only drills down when asked

I would be more conservative than this repo about platform spread, but I would absolutely steal the architectural boundary line.

## Bottom line
Understand Anything is interesting because it is learning the right lesson. The graph is not the breakthrough. The boundary is.

Use deterministic machinery for filesystem walking, parsing, batching, and graph assembly. Then let models explain, label, and teach from that structure. That is the part of this repo that feels durable rather than trendy.
