# Open Code Review

- Repo: `alibaba/open-code-review`
- URL: https://github.com/alibaba/open-code-review
- Date: 2026-07-25
- Repo snapshot studied: `main` @ `c9b145635c6b6343b108941c2a627ac636836c6b`
- Why picked today: It was one of GitHub's daily trending repos when checked, showing 1,066 stars today. More importantly, it is a serious attempt to turn code review into a constrained systems problem instead of a vague "ask Claude to look at the diff" wrapper.

## Executive summary
`open-code-review` is not just a CLI prompt shell. The center of gravity is a Go review runtime that tries to pin down the parts generic coding agents are bad at: file coverage, tool discipline, line positioning, rule targeting, session persistence, and post-filtering. The public pitch in [`README.md`](https://github.com/alibaba/open-code-review/blob/c9b145635c6b6343b108941c2a627ac636836c6b/README.md) says "deterministic pipelines + LLM Agent," and the source mostly earns that phrase.

The strongest design move is that review is decomposed into a predictable pipeline. [`cmd/opencodereview/review_cmd.go`](https://github.com/alibaba/open-code-review/blob/c9b145635c6b6343b108941c2a627ac636836c6b/cmd/opencodereview/review_cmd.go) validates refs, loads rules and tools, injects MCP tools, and hands a fully wired dependency bundle to [`internal/agent/agent.go`](https://github.com/alibaba/open-code-review/blob/c9b145635c6b6343b108941c2a627ac636836c6b/internal/agent/agent.go). That agent then parses diffs, filters files deterministically, optionally runs a plan phase, executes the main tool-use loop per file, and finally runs a review filter pass over collected comments.

The other quiet but important move is precision recovery after the model speaks. [`internal/diff/resolver.go`](https://github.com/alibaba/open-code-review/blob/c9b145635c6b6343b108941c2a627ac636836c6b/internal/diff/resolver.go) resolves comment line numbers against diff hunks first and full file content second. That is exactly the kind of boring infrastructure most "AI review" tools skip, and it is why this repo is worth studying.

## What they built
They built a multi-surface code-review product around one Go engine:

- [`cmd/opencodereview`](https://github.com/alibaba/open-code-review/tree/c9b145635c6b6343b108941c2a627ac636836c6b/cmd/opencodereview) is the CLI surface for `review`, `scan`, `delegate`, `rules`, `config`, `viewer`, and session commands.
- [`internal/agent`](https://github.com/alibaba/open-code-review/tree/c9b145635c6b6343b108941c2a627ac636836c6b/internal/agent) owns diff-based review orchestration.
- [`internal/scan`](https://github.com/alibaba/open-code-review/tree/c9b145635c6b6343b108941c2a627ac636836c6b/internal/scan) is a separate full-file scan path with batching and token-budget controls.
- [`internal/llmloop`](https://github.com/alibaba/open-code-review/tree/c9b145635c6b6343b108941c2a627ac636836c6b/internal/llmloop) runs the actual tool-calling loop and token accounting.
- [`internal/tool`](https://github.com/alibaba/open-code-review/tree/c9b145635c6b6343b108941c2a627ac636836c6b/internal/tool) defines the deliberately small built-in toolset.
- [`internal/config/rules`](https://github.com/alibaba/open-code-review/tree/c9b145635c6b6343b108941c2a627ac636836c6b/internal/config/rules) loads embedded system rules plus project and user overrides.
- [`package.json`](https://github.com/alibaba/open-code-review/blob/c9b145635c6b6343b108941c2a627ac636836c6b/package.json), [`scripts/install.js`](https://github.com/alibaba/open-code-review/blob/c9b145635c6b6343b108941c2a627ac636836c6b/scripts/install.js), [`plugins/open-code-review`](https://github.com/alibaba/open-code-review/tree/c9b145635c6b6343b108941c2a627ac636836c6b/plugins/open-code-review), and [`skills/open-code-review`](https://github.com/alibaba/open-code-review/tree/c9b145635c6b6343b108941c2a627ac636836c6b/skills/open-code-review) package the engine for npm, agent plugins, and reusable skills.

## Why it matters
This repo matters because it treats code review quality as a control-plane problem, not only a model-choice problem.

1. It narrows the model's job to analysis while deterministic code handles filtering, rule routing, and comment placement.
2. It splits diff review and full-file scan into separate pipelines instead of forcing one prompt to serve both.
3. It productizes the engine across CLI, npm binaries, MCP-aware review, session viewer, and agent integrations.

## Repo shape at a glance
The top-level tree is more mature than the homepage pitch suggests:

- [`cmd/opencodereview`](https://github.com/alibaba/open-code-review/tree/c9b145635c6b6343b108941c2a627ac636836c6b/cmd/opencodereview): command entrypoints and CLI UX.
- [`internal/agent`](https://github.com/alibaba/open-code-review/tree/c9b145635c6b6343b108941c2a627ac636836c6b/internal/agent), [`internal/scan`](https://github.com/alibaba/open-code-review/tree/c9b145635c6b6343b108941c2a627ac636836c6b/internal/scan), [`internal/llmloop`](https://github.com/alibaba/open-code-review/tree/c9b145635c6b6343b108941c2a627ac636836c6b/internal/llmloop), [`internal/diff`](https://github.com/alibaba/open-code-review/tree/c9b145635c6b6343b108941c2a627ac636836c6b/internal/diff), and [`internal/tool`](https://github.com/alibaba/open-code-review/tree/c9b145635c6b6343b108941c2a627ac636836c6b/internal/tool): the real engine layers.
- [`internal/mcp`](https://github.com/alibaba/open-code-review/tree/c9b145635c6b6343b108941c2a627ac636836c6b/internal/mcp): optional external tool bridge.
- [`pages`](https://github.com/alibaba/open-code-review/tree/c9b145635c6b6343b108941c2a627ac636836c6b/pages): web session viewer frontend.
- [`npm`](https://github.com/alibaba/open-code-review/tree/c9b145635c6b6343b108941c2a627ac636836c6b/npm): per-platform binary packaging.

## Layered architecture dissection
### High-level system shape
The architecture is: CLI command -> context/rule/tool loading -> per-file review subtasks -> constrained tool loop -> collected comments -> precision cleanup. [`cmd/opencodereview/main.go`](https://github.com/alibaba/open-code-review/blob/c9b145635c6b6343b108941c2a627ac636836c6b/cmd/opencodereview/main.go) is just the dispatcher; the heavy lifting starts once `review` or `scan` hands off to the internal packages.

### Main layers
**1. Command and packaging layer**  
[`cmd/opencodereview/review_cmd.go`](https://github.com/alibaba/open-code-review/blob/c9b145635c6b6343b108941c2a627ac636836c6b/cmd/opencodereview/review_cmd.go) wires flags, background files, resume state, tool registries, and MCP clients. [`package.json`](https://github.com/alibaba/open-code-review/blob/c9b145635c6b6343b108941c2a627ac636836c6b/package.json) wraps the Go binary with npm install/update flows.

**2. Rule and file-selection layer**  
[`internal/config/rules/system_rules.go`](https://github.com/alibaba/open-code-review/blob/c9b145635c6b6343b108941c2a627ac636836c6b/internal/config/rules/system_rules.go) merges embedded rules with custom, project, and global rule files. First-match ordering and include/exclude filters are explicit, not prompt folklore.

**3. Review orchestration layer**  
[`internal/agent/agent.go`](https://github.com/alibaba/open-code-review/blob/c9b145635c6b6343b108941c2a627ac636836c6b/internal/agent/agent.go) parses diffs, freezes the tool registry, skips oversized prompts, runs a plan phase when useful, and executes the main loop per file.

**4. LLM execution layer**  
[`internal/llmloop/loop.go`](https://github.com/alibaba/open-code-review/blob/c9b145635c6b6343b108941c2a627ac636836c6b/internal/llmloop/loop.go) is the conversation runtime: it sends messages with tool definitions, executes tool calls, aggregates token usage, retries empty rounds, and gates termination on `task_done`.

**5. Precision and evidence layer**  
[`internal/tool/code_comment.go`](https://github.com/alibaba/open-code-review/blob/c9b145635c6b6343b108941c2a627ac636836c6b/internal/tool/code_comment.go) collects structured findings, while [`internal/diff/resolver.go`](https://github.com/alibaba/open-code-review/blob/c9b145635c6b6343b108941c2a627ac636836c6b/internal/diff/resolver.go) relocates them onto real lines.

**6. Extended review modes**  
[`internal/scan/agent.go`](https://github.com/alibaba/open-code-review/blob/c9b145635c6b6343b108941c2a627ac636836c6b/internal/scan/agent.go) gives full-file review its own path, and [`internal/scan/batch.go`](https://github.com/alibaba/open-code-review/blob/c9b145635c6b6343b108941c2a627ac636836c6b/internal/scan/batch.go) adds grouping by language or directory.

### Request / data / control flow
1. `ocr review` lands in [`review_cmd.go`](https://github.com/alibaba/open-code-review/blob/c9b145635c6b6343b108941c2a627ac636836c6b/cmd/opencodereview/review_cmd.go), which validates refs and builds runtime state.
2. [`agent.go`](https://github.com/alibaba/open-code-review/blob/c9b145635c6b6343b108941c2a627ac636836c6b/internal/agent/agent.go) loads diffs, filters files, resolves per-path rules, and renders the plan/main prompts.
3. [`llmloop/loop.go`](https://github.com/alibaba/open-code-review/blob/c9b145635c6b6343b108941c2a627ac636836c6b/internal/llmloop/loop.go) runs the tool loop with the built-in tools and any safe MCP additions from [`internal/mcp/provider.go`](https://github.com/alibaba/open-code-review/blob/c9b145635c6b6343b108941c2a627ac636836c6b/internal/mcp/provider.go).
4. The model emits structured comments through [`code_comment.go`](https://github.com/alibaba/open-code-review/blob/c9b145635c6b6343b108941c2a627ac636836c6b/internal/tool/code_comment.go).
5. [`diff/resolver.go`](https://github.com/alibaba/open-code-review/blob/c9b145635c6b6343b108941c2a627ac636836c6b/internal/diff/resolver.go) recovers line positions, and the optional review-filter pass removes provably bad comments.

## Key directories and files
- [`README.md`](https://github.com/alibaba/open-code-review/blob/c9b145635c6b6343b108941c2a627ac636836c6b/README.md): product framing and benchmark claims.
- [`cmd/opencodereview/main.go`](https://github.com/alibaba/open-code-review/blob/c9b145635c6b6343b108941c2a627ac636836c6b/cmd/opencodereview/main.go): command dispatcher.
- [`cmd/opencodereview/review_cmd.go`](https://github.com/alibaba/open-code-review/blob/c9b145635c6b6343b108941c2a627ac636836c6b/cmd/opencodereview/review_cmd.go): review runtime setup.
- [`internal/agent/agent.go`](https://github.com/alibaba/open-code-review/blob/c9b145635c6b6343b108941c2a627ac636836c6b/internal/agent/agent.go): review orchestration.
- [`internal/llmloop/loop.go`](https://github.com/alibaba/open-code-review/blob/c9b145635c6b6343b108941c2a627ac636836c6b/internal/llmloop/loop.go): tool-use loop and token accounting.
- [`internal/diff/resolver.go`](https://github.com/alibaba/open-code-review/blob/c9b145635c6b6343b108941c2a627ac636836c6b/internal/diff/resolver.go): comment line recovery.
- [`internal/config/rules/system_rules.go`](https://github.com/alibaba/open-code-review/blob/c9b145635c6b6343b108941c2a627ac636836c6b/internal/config/rules/system_rules.go): layered rule resolver.
- [`internal/scan/agent.go`](https://github.com/alibaba/open-code-review/blob/c9b145635c6b6343b108941c2a627ac636836c6b/internal/scan/agent.go): full-file scan mode.

## Important components
The most reusable component is the narrow tool contract in [`internal/tool`](https://github.com/alibaba/open-code-review/tree/c9b145635c6b6343b108941c2a627ac636836c6b/internal/tool). They did not hand the reviewer a general shell. They handed it file reads, diff reads, search, and comment submission.

The second important component is the layered rule system in [`system_rules.go`](https://github.com/alibaba/open-code-review/blob/c9b145635c6b6343b108941c2a627ac636836c6b/internal/config/rules/system_rules.go). A lot of "AI reviewer customization" is just more prompt sludge; this repo keeps path routing explicit and ordered.

The third is [`internal/scan/batch.go`](https://github.com/alibaba/open-code-review/blob/c9b145635c6b6343b108941c2a627ac636836c6b/internal/scan/batch.go). Separate batching logic for scan mode is the right call because whole-repo auditing has different failure modes than diff review.

## Important knobs / configs / extension points
- Rule layering and path matching in [`internal/config/rules/system_rules.go`](https://github.com/alibaba/open-code-review/blob/c9b145635c6b6343b108941c2a627ac636836c6b/internal/config/rules/system_rules.go).
- Plan threshold, concurrency, and timeout settings in [`internal/agent/agent.go`](https://github.com/alibaba/open-code-review/blob/c9b145635c6b6343b108941c2a627ac636836c6b/internal/agent/agent.go).
- Built-in versus MCP tools in [`internal/mcp/provider.go`](https://github.com/alibaba/open-code-review/blob/c9b145635c6b6343b108941c2a627ac636836c6b/internal/mcp/provider.go).
- Packaging and binary resolution in [`package.json`](https://github.com/alibaba/open-code-review/blob/c9b145635c6b6343b108941c2a627ac636836c6b/package.json).

## Practical questions and answers
**Is the main trick a better prompt?**  
No. The better prompt matters, but the source says the real trick is tighter runtime structure: deterministic file/rule selection, a constrained tool loop, and line-number repair.

**What should a builder read first?**  
Read [`review_cmd.go`](https://github.com/alibaba/open-code-review/blob/c9b145635c6b6343b108941c2a627ac636836c6b/cmd/opencodereview/review_cmd.go), [`agent.go`](https://github.com/alibaba/open-code-review/blob/c9b145635c6b6343b108941c2a627ac636836c6b/internal/agent/agent.go), [`loop.go`](https://github.com/alibaba/open-code-review/blob/c9b145635c6b6343b108941c2a627ac636836c6b/internal/llmloop/loop.go), and [`resolver.go`](https://github.com/alibaba/open-code-review/blob/c9b145635c6b6343b108941c2a627ac636836c6b/internal/diff/resolver.go).

**Where is the strongest product thinking?**  
In the non-glamorous layers: session resume, scan mode, npm binary packaging, agent skills/plugins, and MCP integration.

## What is smart
- Separating deterministic review plumbing from model judgment.
- Keeping the tool surface intentionally small.
- Repairing comment line positions after inference instead of trusting the model.
- Giving full-file scan its own batching and token-budget logic.

## What is flawed or weak
- The repo now owns a wide surface: CLI, npm installers, viewer, agent plugins, rules, scan, MCP, and review prompts.
- The per-file subtask model improves stability, but it can still miss system-level bugs that only appear across file boundaries.
- The product explicitly biases toward precision, which means some teams will experience it as under-reporting rather than as "better."

## What we can learn / steal
- Treat reviewer quality as a systems design problem.
- Use ordered, path-based rules instead of one giant universal review prompt.
- Preserve a tiny tool contract unless you have hard evidence a broader one helps.
- Add post-processing layers where the model is predictably sloppy.

## How we could apply it
If we wanted our own code-review agent, I would copy the runtime pattern, not the marketing language: deterministic candidate selection, a minimal evidence toolset, structured comment collection, and a relocation pass before anything is shown to humans.

## Bottom line
`open-code-review` is worth studying because it is one of the clearer examples of an AI coding tool getting better by becoming less magical.

The key builder lesson is that review quality goes up when you make the LLM do less unchecked work and give the runtime more responsibility for coverage, constraints, and precision.
