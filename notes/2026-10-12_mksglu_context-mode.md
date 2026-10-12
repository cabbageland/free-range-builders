# Context Mode

- Repo: mksglu/context-mode
- URL: https://github.com/mksglu/context-mode
- Date: 2026-10-12
- Repo snapshot studied: main at commit 98cd9ab0ed417b769dab873f427c5684f6d46d35
- Why picked today: It was high on GitHub daily trending, had same-day activity, and had a real system to dissect: an MCP server, sandboxed execution tools, FTS5 search, session hooks, security gates, status tooling, and plugin packaging for several coding-agent hosts.

## Executive summary

[mksglu/context-mode](https://github.com/mksglu/context-mode/tree/98cd9ab0ed417b769dab873f427c5684f6d46d35) is a context-window management system for coding agents. The product claim is simple: keep raw tool output out of the model's conversation, run analysis in a sandbox, persist useful material into a local searchable store, and restore session memory after compaction. The source is more interesting than the claim because it tries to make that behavior portable across Claude Code, Codex, OpenClaw, Gemini CLI, Copilot, Cursor, and other hosts.

The repo is a TypeScript package with three big surfaces. The MCP server in [src/server.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/server.ts) registers the `ctx_*` tools, tracks bytes saved, indexes large outputs, and routes search through FTS5. The execution layer in [src/executor.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/executor.ts) runs user code in temporary subprocesses across several languages. The hook layer under [hooks](https://github.com/mksglu/context-mode/tree/98cd9ab0ed417b769dab873f427c5684f6d46d35/hooks) injects routing guidance, captures session events, and nudges tool calls away from raw context floods.

The smart part is not "use SQLite" or "use an MCP server." The smart part is treating context as an I/O budget with accounting, routing, and recovery. [src/store.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/store.ts) chunks and ranks content; [src/session/db.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/session/db.ts) persists event memory; [hooks/routing-block.mjs](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/hooks/routing-block.mjs) gives the agent operational rules; and [hooks/core/routing.mjs](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/hooks/core/routing.mjs) decides when to warn, redirect, or pass through.

## What they built

Context Mode is both an MCP server and a packaging layer for agent hosts. Its public tool contract is visible in [package.json](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/package.json) and [openclaw.plugin.json](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/openclaw.plugin.json): `ctx_execute`, `ctx_execute_file`, `ctx_index`, `ctx_search`, `ctx_fetch_and_index`, `ctx_batch_execute`, `ctx_stats`, `ctx_doctor`, `ctx_upgrade`, `ctx_purge`, and `ctx_insight`.

The core workflow is "think in code." Instead of reading a huge page, file, log, or API response into the conversation, the agent is supposed to run code through [ctx_execute in src/server.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/server.ts#L1648), print only a derived answer, and optionally index large output. For durable material, [ctx_index in src/server.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/server.ts#L2237) writes content into the local FTS5 store. For follow-up questions, [ctx_search in src/server.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/server.ts#L2554) retrieves ranked chunks instead of replaying the original bytes.

The repo also ships host-specific plugin metadata. [.codex-plugin/plugin.json](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/.codex-plugin/plugin.json) and [.codex-plugin/hooks.json](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/.codex-plugin/hooks.json) wire Codex hooks. [.claude-plugin/plugin.json](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/.claude-plugin/plugin.json) handles Claude Code. [.openclaw-plugin/openclaw.plugin.json](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/.openclaw-plugin/openclaw.plugin.json) declares the OpenClaw tool contract and permissive sandbox expectations.

## Why it matters

AI coding tools are increasingly bottlenecked by context operations, not only model intelligence. A long shell output, browser snapshot, issue list, or docs page can consume the working memory the model needs to reason about code. Context Mode attacks that as a systems problem: route risky reads, keep raw bytes in a local store, expose precise retrieval, and preserve decisions across compaction.

The builder lesson is that memory and context saving need product machinery. [hooks/sessionstart.mjs](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/hooks/sessionstart.mjs) does not just print advice; it builds routing context, emits lifecycle events, self-heals plugin cache problems, and restores compacted session knowledge. [hooks/precompact.mjs](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/hooks/precompact.mjs) writes a resume snapshot before compaction. That is much closer to an agent runtime subsystem than a prompt trick.

## Repo shape at a glance

- [README.md](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/README.md): product explanation, install flows, platform matrix, slash commands, and the "think in code" philosophy.
- [package.json](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/package.json): npm package, exports, binaries, build commands, adapters, bundled files, dependencies, and versioned plugin manifests.
- [src/server.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/server.ts): MCP server, registered `ctx_*` tools, tracking wrappers, fetch/index/search logic, stats, and lifecycle safeguards.
- [src/cli.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/cli.ts): CLI entry point for server startup, hook dispatch, doctor, upgrade, setup, and host-specific commands.
- [src/executor.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/executor.ts): temporary-script execution runtime for JavaScript, TypeScript, Python, shell, Ruby, Go, Rust, PHP, Perl, R, Elixir, and C#.
- [src/store.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/store.ts): SQLite FTS5 content store, query sanitation, markdown chunking, source labels, stale source handling, and BM25 fallback search.
- [src/store-directory.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/store-directory.ts): bounded recursive directory indexing with extension filters, .gitignore support, max-file caps, and symlink escape controls.
- [src/security.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/security.ts): deny/allow/ask policy parsing, chained shell command splitting, file path glob checks, and project containment.
- [src/session/db.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/session/db.ts): per-project session DB, storage directory resolution, `CONTEXT_MODE_DIR`, resume snapshots, and event persistence.
- [hooks](https://github.com/mksglu/context-mode/tree/98cd9ab0ed417b769dab873f427c5684f6d46d35/hooks): host hook scripts for routing, session start, user prompt submit, precompact, stop, platform bridge behavior, and self-healing.
- [tests](https://github.com/mksglu/context-mode/tree/98cd9ab0ed417b769dab873f427c5684f6d46d35/tests): regression tests for executor behavior, routing, hooks, status line, storage caps, security, stale detection, and plugin integration.

## Layered architecture dissection

### High-level system shape

At the top, Context Mode is a host adapter. Plugin manifests like [.codex-plugin/hooks.json](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/.codex-plugin/hooks.json) and [.openclaw-plugin/openclaw.plugin.json](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/.openclaw-plugin/openclaw.plugin.json) install hooks and expose tools in each platform's native shape.

Below that is the hook/routing layer. [hooks/routing-block.mjs](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/hooks/routing-block.mjs) is the agent-facing rulebook: gather with batch execution, follow up with search, process raw data in code, write artifacts with native file tools. [hooks/core/routing.mjs](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/hooks/core/routing.mjs) contains the policy logic that throttles guidance, detects risky commands, and decides when to return additional context or redirect.

The middle is the MCP tool layer in [src/server.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/server.ts). This layer translates agent calls into sandbox execution, indexing, fetching, search, stats, doctor, and upgrade operations. It wraps handlers to track requests and protect long-running bridge children from idle reaping.

The bottom is local state: [src/executor.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/executor.ts) for subprocess work, [src/store.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/store.ts) for indexed content, [src/session/db.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/session/db.ts) for session events, and [src/security.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/security.ts) for command and path policies.

### Main layers

The plugin distribution layer is explicit and duplicated by host. [package.json](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/package.json) publishes bundles, plugin directories, hook files, skills, and start scripts. That duplication is not pretty, but it is realistic: each host has different hook names, config paths, plugin caches, and MCP boot behavior.

The routing layer is intentionally conservative. [hooks/core/routing.mjs](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/hooks/core/routing.mjs) strips heredocs and quoted content before matching command tokens, keeps guidance markers in temp files so cross-process hooks do not spam the model, and treats unknown shell commands as potentially unbounded unless they match a safe pattern.

The execution layer in [src/executor.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/executor.ts) writes code to temporary scripts, chooses runtime-specific extensions, hides Windows consoles, restores inherited PATH for shell runs, handles background timeouts, and cleans temp directories. This is the layer that makes "think in code" concrete.

The indexing/search layer is split between [src/store.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/store.ts), [src/store-directory.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/store-directory.ts), and [src/search](https://github.com/mksglu/context-mode/tree/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/search). It chunks markdown by headings, caps oversized chunks, filters stopwords for BM25, walks directories within bounds, and merges indexed content with auto-captured session memory.

The continuity layer spans [hooks/sessionstart.mjs](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/hooks/sessionstart.mjs), [hooks/precompact.mjs](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/hooks/precompact.mjs), and [src/session/db.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/session/db.ts). It stores decisions, prompts, errors, files, compaction events, and snapshots so a fresh or compacted session can recover relevant state without dumping the whole transcript back into context.

### Request / data / control flow

A fresh session starts through a host hook such as [hooks/sessionstart.mjs](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/hooks/sessionstart.mjs). That hook detects the platform, builds a host-specific routing block from [hooks/routing-block.mjs](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/hooks/routing-block.mjs), probes security initialization, emits a session lifecycle event, and may inject resume material.

Before a risky tool call, [hooks/pretooluse.mjs](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/hooks/pretooluse.mjs) reads the host payload, extracts tool name/input, and delegates to [hooks/core/routing.mjs](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/hooks/core/routing.mjs). That layer can pass through, add guidance, deny, ask, or write marker files that later hooks use for byte accounting and rejected-approach events.

When the agent calls `ctx_execute`, [src/server.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/server.ts) applies deny policies, instruments JavaScript/TypeScript reads and network bytes, runs through [src/executor.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/executor.ts), echoes the executed source for auditability, and either returns stdout, indexes large output, or returns a searchable summary.

When the agent calls `ctx_fetch_and_index`, [src/server.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/server.ts#L3413) fetches URLs, converts fetched material into indexable content, writes it serially into the FTS5 store, and returns only small previews plus `ctx_search` instructions. Batch fetches can run concurrently, but SQLite writes drain serially.

On compaction, [hooks/precompact.mjs](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/hooks/precompact.mjs) reads captured events from the session DB, builds a compact resume snapshot, and records compaction telemetry. On the next session start, [hooks/sessionstart.mjs](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/hooks/sessionstart.mjs) can inject the resume directive and auto-injection material.

## Key directories and files

- [src/server.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/server.ts): the main server and tool registry. It is the fastest way to understand the product's actual surface.
- [src/executor.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/executor.ts): the sandbox execution mechanism and cross-platform process handling.
- [src/store.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/store.ts): content chunking, FTS5 writes, BM25 search, stale-source handling, and result formatting.
- [src/store-directory.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/store-directory.ts): bounded directory indexing, which is where the product avoids turning "index this repo" into unbounded local ingestion.
- [src/security.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/security.ts): security policy parsing and shell/path matching.
- [src/session/db.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/session/db.ts): storage root resolution and persistent event DB.
- [hooks/routing-block.mjs](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/hooks/routing-block.mjs): the agent-facing behavioral contract.
- [hooks/core/routing.mjs](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/hooks/core/routing.mjs): the hook policy engine.
- [.codex-plugin/hooks.json](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/.codex-plugin/hooks.json): concrete evidence that the repo is not just a Claude plugin; it wires Codex lifecycle hooks too.
- [tests/security.test.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/tests/security.test.ts), [tests/runtime.test.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/tests/runtime.test.ts), and [tests/store.test.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/tests/store.test.ts): useful test entry points for the risky parts.

## Important components

The `ctx_execute` implementation in [src/server.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/server.ts#L1648) is the product's thesis in code. It instruments JavaScript/TypeScript, tracks file/network bytes, enforces deny policies, auto-indexes large output, and returns source echo plus stdout so the user can audit what ran.

The FTS5 store in [src/store.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/store.ts) is not a memory dump. It chunks, sanitizes queries, handles oversized sections, labels sources, and preserves raw content outside the model context until a targeted search asks for it.

The hook guidance in [hooks/routing-block.mjs](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/hooks/routing-block.mjs) is a product interface. It tells the model when to gather, search, process, write, and avoid reading raw content. Without that layer, the MCP tools would exist but agents would keep falling back to ordinary reads.

The storage override logic in [src/session/db.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/session/db.ts) is more important than it looks. A cross-host tool needs predictable storage, support for `CONTEXT_MODE_DIR`, and helpful errors when a configured storage path is invalid.

## Important knobs / configs / extension points

- Add or change host integration through manifests such as [.codex-plugin/plugin.json](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/.codex-plugin/plugin.json), [.claude-plugin/plugin.json](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/.claude-plugin/plugin.json), and [.openclaw-plugin/openclaw.plugin.json](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/.openclaw-plugin/openclaw.plugin.json).
- Change package and bundle behavior through [package.json](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/package.json), especially the `bundle`, `assert-bundle`, and plugin cache repair scripts.
- Tune storage placement with `CONTEXT_MODE_DIR`, implemented in [src/session/db.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/session/db.ts).
- Tune search flood behavior through environment variables in [src/server.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/server.ts), including the search window, soft cap, and block threshold.
- Tune generic shell nudging with `CONTEXT_MODE_BASH_NUDGE_MIN_COMMAND_BYTES`, implemented in [hooks/core/routing.mjs](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/hooks/core/routing.mjs).
- Bound directory indexing through options exposed by [ctx_index in src/server.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/server.ts#L2237): include/exclude globs, max depth, max files, extensions, gitignore respect, and symlink following.

## Practical questions and answers

Q: Is this just a wrapper around shell commands?
A: No. [src/executor.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/executor.ts) runs code, but [src/server.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/server.ts), [src/store.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/store.ts), and [hooks](https://github.com/mksglu/context-mode/tree/98cd9ab0ed417b769dab873f427c5684f6d46d35/hooks) add routing, indexing, memory, stats, security, and host lifecycle integration.

Q: What should a builder copy?
A: Copy the separation of raw bytes, derived answers, and searchable memory. `ctx_execute` in [src/server.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/server.ts#L1648) processes data; [src/store.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/store.ts) keeps exact chunks; `ctx_search` retrieves only what is needed.

Q: Where is it most brittle?
A: Host integration. The source has many self-heal blocks in [hooks/pretooluse.mjs](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/hooks/pretooluse.mjs), [hooks/sessionstart.mjs](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/hooks/sessionstart.mjs), [src/cli.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/cli.ts), and [start.mjs](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/start.mjs), which is a clue that plugin caches, hook paths, and host version skew are operationally messy.

Q: Does it trust the model too much?
A: It depends on the host. The routing block in [hooks/routing-block.mjs](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/hooks/routing-block.mjs) is guidance, while [src/security.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/security.ts) and the server-side checks in [src/server.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/server.ts) are enforcement. The enforcement exists, but any install that lacks hooks loses a lot of the product's intended behavior.

Q: Why is the repo so comment-heavy?
A: Many comments are issue-linked operational history. That makes the source noisy, but it also tells you which bugs were real: Windows temp cleanup, plugin cache version skew, empty MCP tool lists, search flooding, stale path repair, and storage directory mistakes.

## What is smart

The strongest design choice is making the agent program the analysis instead of reading all evidence into context. [ctx_execute](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/server.ts#L1648) makes that workflow first-class.

The second smart choice is memory as indexed events, not transcript replay. [src/session/db.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/session/db.ts), [hooks/sessionstart.mjs](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/hooks/sessionstart.mjs), and [hooks/precompact.mjs](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/hooks/precompact.mjs) together avoid the common failure mode where "memory" just becomes another giant blob.

The third smart choice is explicit byte accounting. Even when the exact numbers are estimates, [src/server.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/server.ts) treats cached, indexed, returned, and sandboxed bytes as product metrics.

## What is flawed or weak

The product is operationally complicated. Multi-host plugin support forces a lot of adapter code, version repair, hook bootstrapping, platform detection, and cache healing. That complexity is visible in [hooks/sessionstart.mjs](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/hooks/sessionstart.mjs) and [src/cli.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/cli.ts).

The security boundary needs careful interpretation. [src/executor.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/executor.ts) runs real code, and [openclaw.plugin.json](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/openclaw.plugin.json) declares permissive/full access. The code has policy gates, but this is not a narrow, locked-down evaluator.

The README's marketing claims are stronger than the source can universally guarantee. The 98% savings story may be true for chosen examples, but actual savings depend on host behavior, hook availability, model compliance, output sizes, and whether agents consistently choose the `ctx_*` path.

## What we can learn / steal

Steal the layered approach: host hooks for behavior, server tools for capability, indexed storage for raw bytes, and session DB for continuity. Most agent tools mix these concerns and then wonder why memory becomes mushy.

Steal the "source echo before stdout" idea from [ctx_execute in src/server.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/server.ts#L1648). If an agent runs generated code on behalf of a user, the output should remain auditable.

Steal the bounded directory walker in [src/store-directory.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/store-directory.ts). Recursive indexing needs max depth, max files, extension filters, gitignore, and symlink rules from the start.

Steal the hook guidance structure in [hooks/routing-block.mjs](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/hooks/routing-block.mjs): not a vague style prompt, but a tool-selection hierarchy.

## How we could apply it

For our own coding-agent workflows, the immediate pattern is to split "discover" from "read." Large discovery should run as code that prints a small answer; only files being edited need exact bytes in the model context.

For internal tools, we could use the same content-store pattern: fetch docs or API results into a local searchable index, then answer from targeted retrieval. [ctx_fetch_and_index in src/server.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/server.ts#L3413) is a useful shape for that.

For long-running work, we should store decisions, failures, and open tasks as events rather than hoping transcript compaction preserves them. The combination of [hooks/precompact.mjs](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/hooks/precompact.mjs) and [src/session/db.ts](https://github.com/mksglu/context-mode/blob/98cd9ab0ed417b769dab873f427c5684f6d46d35/src/session/db.ts) is a concrete implementation to learn from.

## Bottom line

Context Mode is worth studying because it treats context management as runtime infrastructure, not prompt advice. The repo is messy in the way real cross-platform agent tools are messy, but the central pattern is strong: route raw bytes away from the conversation, run derivations in code, index durable material, and restore only the memory that helps the next step.
