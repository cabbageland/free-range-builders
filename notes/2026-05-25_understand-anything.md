# Understand Anything

- Repo: `Lum1104/Understand-Anything`
- URL: https://github.com/Lum1104/Understand-Anything
- Date: 2026-05-25
- Repo snapshot studied: `main` @ `470cc01dc5f9236a93eb704afdd479cd5db79710`
- Why picked today: It was still sitting at the top of GitHub Trending on 2026-05-25, it is directly relevant to the AI-coding-tools wave, and the implementation is more serious than the usual "repo chat" wrapper. The interesting part is not just the graph, it is the pipeline discipline around building and repairing it.

## Executive summary
Understand Anything turns a repo into a graph artifact that multiple surfaces can reuse: dashboard exploration, codebase chat, diff impact analysis, onboarding, domain mapping, and wiki-style knowledge browsing. The repo is ambitious, but the strongest part is not the ambition. It is the architecture split between deterministic extraction and LLM enrichment.

The key insight is that the project has quietly moved away from a naive "let agents do everything" posture. The most important pipeline steps are now deterministic scripts that enumerate files, detect languages, compute batches with Louvain clustering, and extract structural facts with tree-sitter-backed parsers. The LLM layer is still there, but it is increasingly being used for semantic labeling and review instead of raw mechanical scanning. That is exactly the right direction.

## What they built
They built a cross-platform plugin/tooling stack that:

- scans source trees and knowledge bases into a shared graph JSON artifact
- extracts code structure, imports, calls, definitions, and non-code entities
- enriches that structure with summaries, layers, tours, business-domain views, and knowledge-base relations
- renders an interactive dashboard for structural, domain, and knowledge views
- exposes follow-on workflows like chat, explain, diff, onboarding, and dashboard launch
- installs into Claude Code, Codex, Cursor, Copilot, Gemini CLI, OpenClaw, and similar environments

The important source areas are:

- root packaging and install surface in [`package.json`](https://github.com/Lum1104/Understand-Anything/blob/470cc01dc5f9236a93eb704afdd479cd5db79710/package.json)
- plugin entrypoints in [`understand-anything-plugin/src/`](https://github.com/Lum1104/Understand-Anything/tree/470cc01dc5f9236a93eb704afdd479cd5db79710/understand-anything-plugin/src)
- graph core in [`understand-anything-plugin/packages/core/src/`](https://github.com/Lum1104/Understand-Anything/tree/470cc01dc5f9236a93eb704afdd479cd5db79710/understand-anything-plugin/packages/core/src)
- dashboard UI in [`understand-anything-plugin/packages/dashboard/src/`](https://github.com/Lum1104/Understand-Anything/tree/470cc01dc5f9236a93eb704afdd479cd5db79710/understand-anything-plugin/packages/dashboard/src)
- deterministic analysis scripts in [`understand-anything-plugin/skills/understand/`](https://github.com/Lum1104/Understand-Anything/tree/470cc01dc5f9236a93eb704afdd479cd5db79710/understand-anything-plugin/skills/understand)
- agent contracts in [`understand-anything-plugin/agents/`](https://github.com/Lum1104/Understand-Anything/tree/470cc01dc5f9236a93eb704afdd479cd5db79710/understand-anything-plugin/agents)

## Why it matters
This matters because a lot of code-intelligence repos are still confused about what should be deterministic and what should be probabilistic. Understand Anything is more useful than average because it is starting to draw that boundary correctly.

Static structure extraction, ignore filtering, parser dispatch, batching, and graph assembly should be boring and reproducible. Summaries, semantic labels, onboarding tours, and domain narratives can tolerate LLM fuzziness. This repo increasingly reflects that division.

## Repo shape at a glance
Top-level shape:

- [`assets/`](https://github.com/Lum1104/Understand-Anything/tree/470cc01dc5f9236a93eb704afdd479cd5db79710/assets): screenshots and marketing art
- [`docs/`](https://github.com/Lum1104/Understand-Anything/tree/470cc01dc5f9236a93eb704afdd479cd5db79710/docs): docs and feature writeups
- [`homepage/`](https://github.com/Lum1104/Understand-Anything/tree/470cc01dc5f9236a93eb704afdd479cd5db79710/homepage): Astro site and demo surface
- [`scripts/`](https://github.com/Lum1104/Understand-Anything/tree/470cc01dc5f9236a93eb704afdd479cd5db79710/scripts): helper scripts
- [`tests/`](https://github.com/Lum1104/Understand-Anything/tree/470cc01dc5f9236a93eb704afdd479cd5db79710/tests): skill-level tests
- [`understand-anything-plugin/`](https://github.com/Lum1104/Understand-Anything/tree/470cc01dc5f9236a93eb704afdd479cd5db79710/understand-anything-plugin): real product core
  - [`agents/`](https://github.com/Lum1104/Understand-Anything/tree/470cc01dc5f9236a93eb704afdd479cd5db79710/understand-anything-plugin/agents): role specs for scanner/analyzer/reviewer/tour/domain agents
  - [`hooks/`](https://github.com/Lum1104/Understand-Anything/tree/470cc01dc5f9236a93eb704afdd479cd5db79710/understand-anything-plugin/hooks): auto-update hook config
  - [`packages/core/`](https://github.com/Lum1104/Understand-Anything/tree/470cc01dc5f9236a93eb704afdd479cd5db79710/understand-anything-plugin/packages/core): schema, analyzers, parsers, persistence, search
  - [`packages/dashboard/`](https://github.com/Lum1104/Understand-Anything/tree/470cc01dc5f9236a93eb704afdd479cd5db79710/understand-anything-plugin/packages/dashboard): React dashboard and graph UI
  - [`skills/`](https://github.com/Lum1104/Understand-Anything/tree/470cc01dc5f9236a93eb704afdd479cd5db79710/understand-anything-plugin/skills): end-user commands and pipeline scripts
  - [`src/`](https://github.com/Lum1104/Understand-Anything/tree/470cc01dc5f9236a93eb704afdd479cd5db79710/understand-anything-plugin/src): context builders for chat, diff, explain, onboarding

The structure is a little crowded, but the important separation is clear: core graph logic, UI, skills/pipeline, and agent contracts are distinct.

## Layered architecture dissection
### High-level system shape
The system roughly does this:

1. scan the repo deterministically
2. extract structural facts with parsers
3. batch the work using dependency-aware clustering
4. let agent steps add summaries, layers, tours, and semantic views
5. normalize the graph into a shared JSON IR
6. reuse that IR across dashboard, chat, diff, explain, and onboarding flows

### Main layers
**1. Install and runtime adaptation**

[`install.sh`](https://github.com/Lum1104/Understand-Anything/blob/470cc01dc5f9236a93eb704afdd479cd5db79710/install.sh) and root packaging make the project land inside many agent environments. This is distribution plumbing, but it is part of the product thesis.

**2. Deterministic scan and extraction layer**

The most interesting recent work lives in [`understand-anything-plugin/skills/understand/scan-project.mjs`](https://github.com/Lum1104/Understand-Anything/blob/470cc01dc5f9236a93eb704afdd479cd5db79710/understand-anything-plugin/skills/understand/scan-project.mjs), [`understand-anything-plugin/skills/understand/extract-structure.mjs`](https://github.com/Lum1104/Understand-Anything/blob/470cc01dc5f9236a93eb704afdd479cd5db79710/understand-anything-plugin/skills/understand/extract-structure.mjs), and [`understand-anything-plugin/skills/understand/compute-batches.mjs`](https://github.com/Lum1104/Understand-Anything/blob/470cc01dc5f9236a93eb704afdd479cd5db79710/understand-anything-plugin/skills/understand/compute-batches.mjs).

This is the best architectural move in the repo. File enumeration, ignore handling, language detection, category assignment, tree-sitter analysis, and batching are no longer treated like LLM jobs. They are scripts.

**3. Core graph assembly and normalization**

[`understand-anything-plugin/packages/core/src/analyzer/graph-builder.ts`](https://github.com/Lum1104/Understand-Anything/blob/470cc01dc5f9236a93eb704afdd479cd5db79710/understand-anything-plugin/packages/core/src/analyzer/graph-builder.ts) turns file, function, class, import, call, and non-code analysis into actual graph nodes and edges. [`understand-anything-plugin/packages/core/src/schema.ts`](https://github.com/Lum1104/Understand-Anything/blob/470cc01dc5f9236a93eb704afdd479cd5db79710/understand-anything-plugin/packages/core/src/schema.ts) is the quality gate that keeps the IR from drifting into nonsense.

**4. LLM semantic enrichment layer**

[`understand-anything-plugin/packages/core/src/analyzer/llm-analyzer.ts`](https://github.com/Lum1104/Understand-Anything/blob/470cc01dc5f9236a93eb704afdd479cd5db79710/understand-anything-plugin/packages/core/src/analyzer/llm-analyzer.ts) shows the intended role of the model layer clearly: summarize files, describe the project, tag complexity, and add human-friendly meaning. That is a much saner job for an LLM than filesystem walking.

**5. Task-specific retrieval layer**

[`understand-anything-plugin/src/context-builder.ts`](https://github.com/Lum1104/Understand-Anything/blob/470cc01dc5f9236a93eb704afdd479cd5db79710/understand-anything-plugin/src/context-builder.ts), [`understand-anything-plugin/src/diff-analyzer.ts`](https://github.com/Lum1104/Understand-Anything/blob/470cc01dc5f9236a93eb704afdd479cd5db79710/understand-anything-plugin/src/diff-analyzer.ts), [`understand-anything-plugin/src/explain-builder.ts`](https://github.com/Lum1104/Understand-Anything/blob/470cc01dc5f9236a93eb704afdd479cd5db79710/understand-anything-plugin/src/explain-builder.ts), and [`understand-anything-plugin/src/onboard-builder.ts`](https://github.com/Lum1104/Understand-Anything/blob/470cc01dc5f9236a93eb704afdd479cd5db79710/understand-anything-plugin/src/onboard-builder.ts) reshape the graph for concrete user tasks.

**6. UI exploration layer**

[`understand-anything-plugin/packages/dashboard/src/components/GraphView.tsx`](https://github.com/Lum1104/Understand-Anything/blob/470cc01dc5f9236a93eb704afdd479cd5db79710/understand-anything-plugin/packages/dashboard/src/components/GraphView.tsx) is the heaviest UI file, and it earns that weight. It handles overview-level clustering, drill-down, staged layout, focus behavior, and expanded-container relayout. Community grouping for knowledge graphs is handled in [`understand-anything-plugin/packages/dashboard/src/utils/louvain.ts`](https://github.com/Lum1104/Understand-Anything/blob/470cc01dc5f9236a93eb704afdd479cd5db79710/understand-anything-plugin/packages/dashboard/src/utils/louvain.ts).

### Request / data / control flow
A simplified flow:

- user runs `/understand` per [`understand-anything-plugin/skills/understand/SKILL.md`](https://github.com/Lum1104/Understand-Anything/blob/470cc01dc5f9236a93eb704afdd479cd5db79710/understand-anything-plugin/skills/understand/SKILL.md)
- deterministic scan script enumerates files and classifies them in [`scan-project.mjs`](https://github.com/Lum1104/Understand-Anything/blob/470cc01dc5f9236a93eb704afdd479cd5db79710/understand-anything-plugin/skills/understand/scan-project.mjs)
- batching script computes dependency-aware work groups in [`compute-batches.mjs`](https://github.com/Lum1104/Understand-Anything/blob/470cc01dc5f9236a93eb704afdd479cd5db79710/understand-anything-plugin/skills/understand/compute-batches.mjs)
- structure extractor uses parsers via [`extract-structure.mjs`](https://github.com/Lum1104/Understand-Anything/blob/470cc01dc5f9236a93eb704afdd479cd5db79710/understand-anything-plugin/skills/understand/extract-structure.mjs)
- graph builder turns the results into nodes and edges in [`graph-builder.ts`](https://github.com/Lum1104/Understand-Anything/blob/470cc01dc5f9236a93eb704afdd479cd5db79710/understand-anything-plugin/packages/core/src/analyzer/graph-builder.ts)
- semantic analyzers and specialized agents add summaries, tours, and domain knowledge
- the final graph JSON gets consumed by dashboard and task-specific context builders

The shared-IR pattern is still the deepest idea in the repo.

## Key directories and files
- [`README.md`](https://github.com/Lum1104/Understand-Anything/blob/470cc01dc5f9236a93eb704afdd479cd5db79710/README.md): product claim and workflow surface
- [`understand-anything-plugin/skills/understand/SKILL.md`](https://github.com/Lum1104/Understand-Anything/blob/470cc01dc5f9236a93eb704afdd479cd5db79710/understand-anything-plugin/skills/understand/SKILL.md): the full `/understand` pipeline contract
- [`understand-anything-plugin/skills/understand/scan-project.mjs`](https://github.com/Lum1104/Understand-Anything/blob/470cc01dc5f9236a93eb704afdd479cd5db79710/understand-anything-plugin/skills/understand/scan-project.mjs): deterministic project scan
- [`understand-anything-plugin/skills/understand/extract-structure.mjs`](https://github.com/Lum1104/Understand-Anything/blob/470cc01dc5f9236a93eb704afdd479cd5db79710/understand-anything-plugin/skills/understand/extract-structure.mjs): parser-driven structure extraction
- [`understand-anything-plugin/skills/understand/compute-batches.mjs`](https://github.com/Lum1104/Understand-Anything/blob/470cc01dc5f9236a93eb704afdd479cd5db79710/understand-anything-plugin/skills/understand/compute-batches.mjs): Louvain-based batch planner
- [`understand-anything-plugin/packages/core/src/analyzer/graph-builder.ts`](https://github.com/Lum1104/Understand-Anything/blob/470cc01dc5f9236a93eb704afdd479cd5db79710/understand-anything-plugin/packages/core/src/analyzer/graph-builder.ts): graph assembly logic
- [`understand-anything-plugin/packages/core/src/analyzer/llm-analyzer.ts`](https://github.com/Lum1104/Understand-Anything/blob/470cc01dc5f9236a93eb704afdd479cd5db79710/understand-anything-plugin/packages/core/src/analyzer/llm-analyzer.ts): semantic prompt builders and parsers
- [`understand-anything-plugin/packages/dashboard/src/components/GraphView.tsx`](https://github.com/Lum1104/Understand-Anything/blob/470cc01dc5f9236a93eb704afdd479cd5db79710/understand-anything-plugin/packages/dashboard/src/components/GraphView.tsx): main graph UI engine
- [`understand-anything-plugin/packages/dashboard/src/utils/louvain.ts`](https://github.com/Lum1104/Understand-Anything/blob/470cc01dc5f9236a93eb704afdd479cd5db79710/understand-anything-plugin/packages/dashboard/src/utils/louvain.ts): community detection for knowledge graph clustering

## Important components
**Deterministic scanner**

[`scan-project.mjs`](https://github.com/Lum1104/Understand-Anything/blob/470cc01dc5f9236a93eb704afdd479cd5db79710/understand-anything-plugin/skills/understand/scan-project.mjs) is an important maturity marker. It explicitly replaces LLM-written throwaway scan scripts with reproducible logic.

**Parser-backed structure extraction**

[`extract-structure.mjs`](https://github.com/Lum1104/Understand-Anything/blob/470cc01dc5f9236a93eb704afdd479cd5db79710/understand-anything-plugin/skills/understand/extract-structure.mjs) routes files through plugin registries and tree-sitter-backed parsers instead of relying on regex improv.

**Dependency-aware batching**

[`compute-batches.mjs`](https://github.com/Lum1104/Understand-Anything/blob/470cc01dc5f9236a93eb704afdd479cd5db79710/understand-anything-plugin/skills/understand/compute-batches.mjs) uses Louvain clustering on the import graph to keep related files together. That is a clever practical move for multi-agent analysis because it reduces cross-batch context fragmentation.

**Graph assembler**

[`graph-builder.ts`](https://github.com/Lum1104/Understand-Anything/blob/470cc01dc5f9236a93eb704afdd479cd5db79710/understand-anything-plugin/packages/core/src/analyzer/graph-builder.ts) is where extracted facts become file/function/class nodes and import/call/contains edges. This is the actual spine of the product.

**Graph explorer**

[`GraphView.tsx`](https://github.com/Lum1104/Understand-Anything/blob/470cc01dc5f9236a93eb704afdd479cd5db79710/understand-anything-plugin/packages/dashboard/src/components/GraphView.tsx) is the reason the graph becomes usable rather than decorative.

## Important knobs / configs / extension points
- output-language support in [`README.md`](https://github.com/Lum1104/Understand-Anything/blob/470cc01dc5f9236a93eb704afdd479cd5db79710/README.md)
- auto-update hook config in [`understand-anything-plugin/hooks/hooks.json`](https://github.com/Lum1104/Understand-Anything/blob/470cc01dc5f9236a93eb704afdd479cd5db79710/understand-anything-plugin/hooks/hooks.json)
- parser/plugin extension points in [`understand-anything-plugin/packages/core/src/plugins/`](https://github.com/Lum1104/Understand-Anything/tree/470cc01dc5f9236a93eb704afdd479cd5db79710/understand-anything-plugin/packages/core/src/plugins)
- language registration in [`understand-anything-plugin/packages/core/src/languages/`](https://github.com/Lum1104/Understand-Anything/tree/470cc01dc5f9236a93eb704afdd479cd5db79710/understand-anything-plugin/packages/core/src/languages)
- dashboard state and UX behavior in [`understand-anything-plugin/packages/dashboard/src/store.ts`](https://github.com/Lum1104/Understand-Anything/blob/470cc01dc5f9236a93eb704afdd479cd5db79710/understand-anything-plugin/packages/dashboard/src/store.ts)
- agent-role contracts in [`understand-anything-plugin/agents/`](https://github.com/Lum1104/Understand-Anything/tree/470cc01dc5f9236a93eb704afdd479cd5db79710/understand-anything-plugin/agents)

## Practical questions and answers
**Is this really a multi-agent repo, or mostly a parser-plus-UI repo?**

It is both, but the durable value is increasingly in parser-plus-IR-plus-UI. The agent layer adds semantics and teaching value on top.

**What is the sharpest engineering decision?**

Moving low-level scan and extraction work out of prompts and into deterministic scripts.

**What problem is the Louvain batching solving?**

It tries to keep dependency-neighbor files in the same batch so per-batch analyzers see coherent chunks instead of arbitrary slices of the repo.

**Where is the product still fragile?**

Business-domain inference, plain-English summaries, and guided tours can still become polished wrongness if the semantic layer overreaches.

**What part looks more impressive than the README?**

The front-end graph orchestration and the deterministic pipeline scripts.

## What is smart
- Using deterministic scripts for scan, batch planning, and structural extraction
- Treating the graph JSON as a reusable intermediate representation
- Using community detection both in analysis batching and knowledge-graph display
- Separating structural truth from semantic storytelling
- Building a graph UI that aggregates complexity instead of dumping every node at once

## What is flawed or weak
- The repo still has platform-sprawl risk, because every extra runtime adds support tax.
- Prompt-defined behavior is still effectively code, but harder to test and harder to reason about.
- The root repo remains a little cluttered because product, site, runtime adapters, and fixtures all live together.
- Semantic layers are still the least trustworthy part of the stack, especially for business-domain claims.

## What we can learn / steal
- Put deterministic boundaries around anything that looks like infrastructure, parsing, or batching.
- Use a shared graph artifact across analysis, retrieval, and UI instead of rebuilding context separately for each feature.
- Batch analysis work by actual dependency structure, not arbitrary file counts.
- Make codebase understanding visible and navigable, not just searchable.

## How we could apply it
If we were building repo-intelligence tooling ourselves, I would copy four things first:

1. deterministic file scan and parser extraction
2. a small shared graph IR with repair/validation
3. dependency-aware batching for large analyses
4. a UI that starts with aggregated structure and expands lazily

I would be more conservative than this repo about runtime proliferation. The architecture is strongest where it is boring, typed, and reproducible.

## Bottom line
Understand Anything is still one of the more interesting repos in this wave because it is learning the right lesson: do not ask LLMs to be your filesystem, parser, or scheduler.

The best idea in the repo is not the graph itself. It is the boundary line. Use deterministic machinery to extract and shape structure, then use models to explain it. That is the part worth stealing.