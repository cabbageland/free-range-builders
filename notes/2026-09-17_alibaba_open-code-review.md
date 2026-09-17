# OpenCodeReview

- Repo: alibaba/open-code-review
- URL: https://github.com/alibaba/open-code-review
- Date: 2026-09-17
- Repo snapshot studied: main at `189be5b024d3309dd10fdc8cd8ee31b2530c210b`
- Why picked today: It is a hot GitHub trending AI-code-review tool with real source depth, not just a prompt wrapper. The useful idea is its hard split between deterministic diff/session machinery and a narrower agent loop.

## Executive summary

[OpenCodeReview](https://github.com/alibaba/open-code-review) is an AI code-review CLI that tries to make LLM review less sloppy by taking file selection, diff parsing, grouping, line relocation, session persistence, and output accounting out of the model's hands. The model still reasons about code, calls tools, and writes comments, but the repo is mostly a Go control plane around that model.

The big lesson is simple: for code review, an "agent" is strongest when it is fenced in by boring systems work. [internal/agent/selection.go](https://github.com/alibaba/open-code-review/blob/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/agent/selection.go) makes the review set explicit before dispatch, [internal/diff/git.go](https://github.com/alibaba/open-code-review/blob/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/diff/git.go) owns git resolution, [internal/agent/grouping.go](https://github.com/alibaba/open-code-review/blob/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/agent/grouping.go) controls how files are batched, and [internal/llmloop/loop.go](https://github.com/alibaba/open-code-review/blob/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/llmloop/loop.go) centralizes the tool-use conversation.

## What they built

They built a cross-platform CLI, published through npm and native release artifacts, that reviews diffs, commit ranges, single commits, or full files. The top-level command registration lives in [cmd/opencodereview/root.go](https://github.com/alibaba/open-code-review/blob/189be5b024d3309dd10fdc8cd8ee31b2530c210b/cmd/opencodereview/root.go), while the small executable wrapper is [cmd/opencodereview/main.go](https://github.com/alibaba/open-code-review/blob/189be5b024d3309dd10fdc8cd8ee31b2530c210b/cmd/opencodereview/main.go).

The user-facing surface is broader than "run a prompt over a patch": `ocr review` handles workspace/range/commit review, `ocr scan` handles full-file scans, `ocr delegate` lets a coding agent do the model work, `ocr session` persists and resumes runs, `ocr viewer` opens a browser viewer, and `ocr config` resolves provider/model setup. That surface is wired in [cmd/opencodereview/root.go](https://github.com/alibaba/open-code-review/blob/189be5b024d3309dd10fdc8cd8ee31b2530c210b/cmd/opencodereview/root.go).

## Why it matters

Most AI review systems fail in unglamorous places: they miss files, drift line numbers, over-report low-confidence comments, or make review quality depend on prompt luck. This repo is interesting because it spends engineering effort on those failure modes directly.

The design says: let deterministic code decide what must be exact, then let the LLM work inside that shape. [internal/agent/agent.go](https://github.com/alibaba/open-code-review/blob/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/agent/agent.go) parses diffs, freezes run identity, records coverage, dispatches subtasks, waits for background compression, and finalizes session manifests. The agent is not the whole system; it is one worker inside a review pipeline.

## Repo shape at a glance

- [cmd/opencodereview/](https://github.com/alibaba/open-code-review/tree/189be5b024d3309dd10fdc8cd8ee31b2530c210b/cmd/opencodereview) is the Cobra CLI layer and command wiring.
- [internal/agent/](https://github.com/alibaba/open-code-review/tree/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/agent) is the diff-review orchestrator: selection, grouping, dispatch, manifests, coverage, resume, and filters.
- [internal/scan/](https://github.com/alibaba/open-code-review/tree/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/scan) adapts the same review machinery for full-file scanning.
- [internal/diff/](https://github.com/alibaba/open-code-review/tree/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/diff) wraps git diff modes, parsing, hunk handling, relocation, and workspace file reads.
- [internal/llm/](https://github.com/alibaba/open-code-review/tree/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/llm) handles provider protocols, retries, request metadata, token accounting, and embedded provider loading.
- [internal/llmloop/](https://github.com/alibaba/open-code-review/tree/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/llmloop) owns the repeated model/tool conversation used by both review and scan.
- [internal/tool/](https://github.com/alibaba/open-code-review/tree/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/tool) defines the constrained tool surface: file read, diff read, code search, find, response, and code-comment capture.
- [internal/config/](https://github.com/alibaba/open-code-review/tree/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/config) stores built-in rules, allowlists, task templates, scan templates, and tool config.
- [internal/session/](https://github.com/alibaba/open-code-review/tree/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/session) persists run history, manifests, comments, resume state, and comparison data.
- [internal/viewer/](https://github.com/alibaba/open-code-review/tree/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/viewer) and [pages/](https://github.com/alibaba/open-code-review/tree/189be5b024d3309dd10fdc8cd8ee31b2530c210b/pages) provide the session viewer UI.
- [plugins/open-code-review/](https://github.com/alibaba/open-code-review/tree/189be5b024d3309dd10fdc8cd8ee31b2530c210b/plugins/open-code-review) packages integrations for Claude Code, Codex, Cursor, Kimi Code, OpenCode, and QCA.

## Layered architecture dissection

### High-level system shape

At the top, [cmd/opencodereview/root.go](https://github.com/alibaba/open-code-review/blob/189be5b024d3309dd10fdc8cd8ee31b2530c210b/cmd/opencodereview/root.go) selects a mode and validates global concerns such as color output and git version. Below that, command handlers build an `agent.Args` or `scan.Args` object with a git repository, loaded templates, resolved LLM client, tool registry, rule resolver, session, and runtime limits.

The core review path is [internal/agent/agent.go](https://github.com/alibaba/open-code-review/blob/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/agent/agent.go). Its `Run` method follows a staged pipeline: load diffs, inject a diff map into tools, select supported files, register coverage, apply resume state, group files, dispatch concurrent group subtasks, join background work, finalize the manifest, and persist the session. This is the repo's real spine.

### Main layers

The git/input layer is [internal/diff/](https://github.com/alibaba/open-code-review/tree/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/diff). [internal/diff/git.go](https://github.com/alibaba/open-code-review/blob/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/diff/git.go) defines workspace, commit, and range modes, freezes resolved base/head commits, and excludes known noisy directories before the review layer ever sees them.

The selection layer is [internal/agent/selection.go](https://github.com/alibaba/open-code-review/blob/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/agent/selection.go). It applies binary, secret-path, user include/exclude, extension, default path, deletion, and token-size gates in a pure pass. That is a good sign: preview and execution share the same selection answer.

The grouping layer is [internal/agent/grouping.go](https://github.com/alibaba/open-code-review/blob/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/agent/grouping.go). Small changes can be bundled locally; larger changes can ask an LLM to produce semantic groups using integer file indexes instead of long paths. Any grouping failure degrades to per-file review.

The model/tool loop is [internal/llmloop/loop.go](https://github.com/alibaba/open-code-review/blob/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/llmloop/loop.go), with tools from [internal/tool/](https://github.com/alibaba/open-code-review/tree/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/tool). That layer tracks token use, tool failures, background compression, and request identity instead of hiding all execution inside the CLI command.

The persistence layer is [internal/session/](https://github.com/alibaba/open-code-review/tree/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/session). The important detail is not just "there are logs"; the run manifest captures coverage, terminal state, resume lineage, input resolution, provider/model labels, and per-item results.

### Request / data / control flow

A normal diff review flows like this. Cobra dispatch enters the review command. A diff provider from [internal/diff/git.go](https://github.com/alibaba/open-code-review/blob/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/diff/git.go) resolves the chosen workspace/range/commit and parses `model.Diff` objects. [internal/agent/selection.go](https://github.com/alibaba/open-code-review/blob/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/agent/selection.go) narrows that list to reviewable files. [internal/agent/grouping.go](https://github.com/alibaba/open-code-review/blob/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/agent/grouping.go) decides review batches. [internal/agent/agent.go](https://github.com/alibaba/open-code-review/blob/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/agent/agent.go) sends those groups concurrently into the LLM loop. The LLM can use [internal/tool/file_read.go](https://github.com/alibaba/open-code-review/blob/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/tool/file_read.go), [internal/tool/file_read_diff.go](https://github.com/alibaba/open-code-review/blob/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/tool/file_read_diff.go), [internal/tool/code_search.go](https://github.com/alibaba/open-code-review/blob/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/tool/code_search.go), and [internal/tool/code_comment.go](https://github.com/alibaba/open-code-review/blob/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/tool/code_comment.go). Comments are collected, line-resolved, optionally relocated, filtered, serialized, and displayed.

## Key directories and files

- [internal/agent/agent.go](https://github.com/alibaba/open-code-review/blob/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/agent/agent.go): the review orchestrator and dispatch loop.
- [internal/agent/selection.go](https://github.com/alibaba/open-code-review/blob/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/agent/selection.go): deterministic file admission and exclusion reasons.
- [internal/agent/grouping.go](https://github.com/alibaba/open-code-review/blob/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/agent/grouping.go): semantic grouping, local grouping fallback, token-budget enforcement.
- [internal/diff/git.go](https://github.com/alibaba/open-code-review/blob/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/diff/git.go): git input mode, diff set construction, commit endpoint freezing.
- [internal/llmloop/loop.go](https://github.com/alibaba/open-code-review/blob/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/llmloop/loop.go): reusable model/tool runner for review and scan.
- [internal/config/template/task_template.json](https://github.com/alibaba/open-code-review/blob/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/config/template/task_template.json): built-in review prompt/template configuration.
- [internal/config/template/scan_template.json](https://github.com/alibaba/open-code-review/blob/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/config/template/scan_template.json): full-file scan prompt/template configuration.
- [internal/config/rules/system_rules.json](https://github.com/alibaba/open-code-review/blob/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/config/rules/system_rules.json): language/file-specific review guidance.
- [plugins/open-code-review/README.md](https://github.com/alibaba/open-code-review/blob/189be5b024d3309dd10fdc8cd8ee31b2530c210b/plugins/open-code-review/README.md): cross-agent integration surface.

## Important components

`Agent.Args` in [internal/agent/agent.go](https://github.com/alibaba/open-code-review/blob/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/agent/agent.go) is worth copying as a pattern. It makes dependencies explicit: repository, diff range, templates, rules, file filters, LLM client, tool definitions, concurrency, token budgets, background context, provider/model labels, git runner, session, resume state, and sealed input resolution.

The selection pass in [internal/agent/selection.go](https://github.com/alibaba/open-code-review/blob/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/agent/selection.go) is another key component. It returns one `fileDecision` per diff, preserving the difference between "selected", "retained as context", and "excluded". That supports accurate coverage reporting instead of hand-wavy "reviewed the PR" claims.

The shared LLM runner in [internal/llmloop/loop.go](https://github.com/alibaba/open-code-review/blob/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/llmloop/loop.go) is the third important piece. It abstracts conversation execution without abstracting away observability: token counters, tool failures, warning records, request metadata, background compression, and budget gates stay visible.

## Important knobs / configs / extension points

The most important knobs are the review templates in [internal/config/template/task_template.json](https://github.com/alibaba/open-code-review/blob/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/config/template/task_template.json), scan templates in [internal/config/template/scan_template.json](https://github.com/alibaba/open-code-review/blob/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/config/template/scan_template.json), built-in tool configuration in [internal/config/toolsconfig/tools.json](https://github.com/alibaba/open-code-review/blob/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/config/toolsconfig/tools.json), and system rules in [internal/config/rules/system_rules.json](https://github.com/alibaba/open-code-review/blob/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/config/rules/system_rules.json).

Users can influence file inclusion through rule config loaded by [internal/config/rules/](https://github.com/alibaba/open-code-review/tree/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/config/rules). Agents can integrate through plugin packaging in [plugins/open-code-review/](https://github.com/alibaba/open-code-review/tree/189be5b024d3309dd10fdc8cd8ee31b2530c210b/plugins/open-code-review). Model providers are abstracted in [internal/llm/](https://github.com/alibaba/open-code-review/tree/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/llm), with endpoint resolution kept separate from review execution.

## Practical questions and answers

Q: Is this just a prompt pack?

A: No. The prompt templates matter, but most of the repo is deterministic infrastructure. The decisive parts are [internal/diff/](https://github.com/alibaba/open-code-review/tree/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/diff), [internal/agent/](https://github.com/alibaba/open-code-review/tree/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/agent), [internal/session/](https://github.com/alibaba/open-code-review/tree/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/session), and [internal/tool/](https://github.com/alibaba/open-code-review/tree/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/tool).

Q: Where would I look first if line numbers are wrong?

A: Start with [internal/tool/code_comment.go](https://github.com/alibaba/open-code-review/blob/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/tool/code_comment.go), [internal/diff/resolver.go](https://github.com/alibaba/open-code-review/blob/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/diff/resolver.go), and [internal/diff/relocation.go](https://github.com/alibaba/open-code-review/blob/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/diff/relocation.go), then check how comments are finalized in [internal/agent/agent.go](https://github.com/alibaba/open-code-review/blob/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/agent/agent.go).

Q: What production failure is the repo most openly designing around?

A: Partial coverage. The code tracks selected files, excluded files, failed subtasks, budget stops, resume reuse, and manifest terminal states instead of pretending every run is all-or-nothing.

## What is smart

The cleanest move is making file selection pure in [internal/agent/selection.go](https://github.com/alibaba/open-code-review/blob/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/agent/selection.go). That avoids one of the worst classes of AI-tool bugs: preview, execution, and reporting silently disagreeing about what was reviewed.

The second smart move is the fallback-heavy grouping design in [internal/agent/grouping.go](https://github.com/alibaba/open-code-review/blob/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/agent/grouping.go). Semantic grouping can help, but the system does not trust it as a critical dependency. If grouping fails, per-file dispatch still works.

The third smart move is making session and manifest persistence first-class in [internal/session/](https://github.com/alibaba/open-code-review/tree/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/session). Review tools need replayability and auditability because model behavior changes under your feet.

## What is flawed or weak

There is a lot of machinery here. The strength is also the maintenance cost: review, scan, session, viewer, config, plugin packaging, and provider support all have to move together. A smaller team cloning this architecture should copy the boundaries, not the whole surface.

The LLM grouping step is useful but still a soft spot. [internal/agent/grouping.go](https://github.com/alibaba/open-code-review/blob/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/agent/grouping.go) falls back safely, but semantic partitioning by file metadata can still produce uneven batches or miss cross-file coupling.

The benchmark claims in [README.md](https://github.com/alibaba/open-code-review/blob/189be5b024d3309dd10fdc8cd8ee31b2530c210b/README.md) are interesting but should be treated as claims until reproduced locally. The repo links the [AACR-Bench dataset](https://huggingface.co/datasets/Alibaba-Aone/aacr-bench), which is good; serious adopters should run their own project-shaped evaluations.

## What we can learn / steal

Steal the architecture pattern: deterministic shell around probabilistic reasoning. The review agent should receive a curated, audited problem, not discover the whole problem from scratch.

Steal the coverage vocabulary from [internal/agent/agent.go](https://github.com/alibaba/open-code-review/blob/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/agent/agent.go): selected, retained, excluded, reused, failed, skipped, completed. That language forces honest reporting.

Steal the constrained tool surface from [internal/tool/](https://github.com/alibaba/open-code-review/tree/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/tool). A code-review model does not need every possible tool; it needs reliable read/search/diff/comment actions with strong post-processing.

## How we could apply it

For any internal code-review assistant, start by implementing the pieces this repo made boring: diff parsing, file selection, exclusion reasons, per-file coverage, review result schema, and a session manifest. Only then add a model loop.

For larger automation systems, copy the shared-runner idea from [internal/llmloop/loop.go](https://github.com/alibaba/open-code-review/blob/189be5b024d3309dd10fdc8cd8ee31b2530c210b/internal/llmloop/loop.go): one conversation engine, multiple orchestration modes. That makes it easier to support both changed-file review and full-file audit without duplicating all LLM accounting.

For plugin distribution, [plugins/open-code-review/README.md](https://github.com/alibaba/open-code-review/blob/189be5b024d3309dd10fdc8cd8ee31b2530c210b/plugins/open-code-review/README.md) is a reminder that agent tools need packaging, not just code. If users live in Claude Code, Codex, Cursor, Kimi, or OpenCode, the integration path is part of the product.

## Bottom line

OpenCodeReview is worth studying because it treats AI code review as a systems problem. The useful part is not that an LLM reads a diff; it is that the repo builds enough deterministic scaffolding around the LLM for coverage, positioning, persistence, and failure modes to be visible.
