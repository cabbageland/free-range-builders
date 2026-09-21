# ai-memory

- Repo: akitaonrails/ai-memory
- URL: https://github.com/akitaonrails/ai-memory
- Date: 2026-09-21
- Repo snapshot studied: main at `1fe32bc2be32490ebf614c86eb9ab45718dcceb1`
- Why picked today: It was on the daily GitHub trending page and has a real systems surface behind the pitch: a Rust workspace, lifecycle hooks, MCP tools, a SQLite writer actor, a markdown wiki source of truth, hook capture, cross-agent handoffs, and optional LLM consolidation.

## Executive summary

[akitaonrails/ai-memory](https://github.com/akitaonrails/ai-memory) is a long-term memory server for coding agents. The short version from [README.md](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/README.md) is "quit one agent, open another in the same repo, continue without re-explaining the work." The source makes that concrete: a single Rust workspace captures agent lifecycle events, sanitizes them, writes observations into SQLite, compiles session summaries into a git-backed markdown wiki, exposes search and handoff tools over MCP, and can optionally call LLM providers to consolidate raw observations into better pages.

The best idea is not "vector memory." It is the storage boundary. [crates/ai-memory-wiki/src/lib.rs](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-wiki/src/lib.rs) says the markdown wiki is the source of truth, while [crates/ai-memory-store/src/lib.rs](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-store/src/lib.rs) opens and migrates a SQLite derived index. That is a useful inversion for agent memory: the human-readable artifact survives if the index gets rebuilt, moved, grepped, committed, or audited.

## What they built

ai-memory is an agent-memory infrastructure binary with several faces:

- a CLI defined in [crates/ai-memory-cli/src/cli.rs](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-cli/src/cli.rs), with commands for init, status, search, page reads/writes, serving MCP, hook installation, backup/restore, reindex, handoffs, managed workstreams, and provider checks.
- a hook ingestion service in [crates/ai-memory-hooks/src/router.rs](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-hooks/src/router.rs) that receives agent lifecycle events such as session start, prompt submit, tool use, compaction, and session end.
- a domain vocabulary in [crates/ai-memory-core/src/lib.rs](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-core/src/lib.rs): observations, sessions, handoffs, pages, users, actors, scopes, sanitization, managed runs, and portable page keys.
- a storage layer in [crates/ai-memory-store/](https://github.com/akitaonrails/ai-memory/tree/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-store) with migrations, readers, maintenance, session consolidation jobs, user/auth data, and a single writer actor.
- a wiki layer in [crates/ai-memory-wiki/](https://github.com/akitaonrails/ai-memory/tree/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-wiki) for atomic markdown writes, frontmatter parsing, git commits, admission hooks, backups, and filesystem reconciliation.
- an MCP server in [crates/ai-memory-mcp/src/server.rs](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-mcp/src/server.rs) with tools for memory query, page fetch/write/delete, handoffs, messages, consolidation, retention sweeps, lint, and status.

## Why it matters

Coding-agent work is fragmented. Claude Code, Codex, Cursor, Gemini CLI, OpenCode, and similar tools each have partial context, local histories, and their own memory conventions. ai-memory treats those agents as producers and consumers of one project memory instead of isolated chat sessions.

The architectural bet in [docs/ARCHITECTURE.md](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/docs/ARCHITECTURE.md) is that memory should be compiled over time into pages, not only retrieved from raw turns. That is a stronger builder model. Raw observations are useful evidence, but the durable product is an evolving project wiki with frontmatter, links, entities, decay, evidence, and human-readable commits.

It also matters because the repo is honest about operational pressure. [crates/ai-memory-store/src/writer.rs](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-store/src/writer.rs) has a single-writer actor to avoid SQLite lock chaos. [crates/ai-memory-hooks/src/router.rs](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-hooks/src/router.rs) has bounded in-flight hook ingestion and returns saturation instead of queueing forever. This is the difference between a memory demo and a tool people might leave running all day.

## Repo shape at a glance

- [Cargo.toml](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/Cargo.toml) defines a Rust 2024 workspace with shipped crates for core, store, wiki, MCP, hooks, LLM providers, consolidation, web, CLI, workstreams, and test support.
- [crates/ai-memory-core/](https://github.com/akitaonrails/ai-memory/tree/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-core) is the dependency-light domain model: ids, observations, handoffs, users, pages, sanitization, active-project routing, and workstream vocabulary.
- [crates/ai-memory-store/](https://github.com/akitaonrails/ai-memory/tree/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-store) owns SQLite migrations, readers, writer commands, FTS query prep, auth tokens, maintenance, session consolidation jobs, and project/workspace scope.
- [crates/ai-memory-wiki/](https://github.com/akitaonrails/ai-memory/tree/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-wiki) owns markdown persistence, git checkpoints, atomic writes, admission webhooks, backups, migrations, and watcher reconciliation.
- [crates/ai-memory-hooks/](https://github.com/akitaonrails/ai-memory/tree/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-hooks) owns lifecycle hook parsing, capture policy, router ingestion, payload normalization, and session-page synthesis.
- [crates/ai-memory-mcp/](https://github.com/akitaonrails/ai-memory/tree/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-mcp) exposes the server-facing tool surface.
- [crates/ai-memory-consolidate/](https://github.com/akitaonrails/ai-memory/tree/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-consolidate) owns consolidation, auto-improvement, lint, projection, sweep logic, and prompts.
- [crates/ai-memory-llm/](https://github.com/akitaonrails/ai-memory/tree/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-llm) contains provider adapters for Anthropic, OpenAI-compatible providers, Gemini, local embeddings, reranking, auth, and fallback.
- [hooks/](https://github.com/akitaonrails/ai-memory/tree/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/hooks) contains integration scripts for supported harnesses.
- [docs/](https://github.com/akitaonrails/ai-memory/tree/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/docs) is unusually rich: architecture, install, deploy, security, support matrix, temporal design, local embeddings, managed workstreams, provider fallback, auto-improvement, and prior-art research.

## Layered architecture dissection

### High-level system shape

The system is a capture-to-wiki pipeline. Agent CLIs emit lifecycle events. ai-memory sanitizes and stores those observations. Session end produces a summary page and handoff. Search reads compiled wiki pages, entity/link indexes, raw fallback observations, and optional vectors. MCP and CLI commands give the next agent or human a bounded brief, specific pages, or an explicit handoff.

The source is arranged around that pipeline. [crates/ai-memory-core/src/lib.rs](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-core/src/lib.rs) defines the nouns. [crates/ai-memory-hooks/src/router.rs](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-hooks/src/router.rs) receives events. [crates/ai-memory-store/src/writer.rs](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-store/src/writer.rs) serializes mutations. [crates/ai-memory-wiki/src/lib.rs](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-wiki/src/lib.rs) writes the durable wiki. [crates/ai-memory-mcp/src/server.rs](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-mcp/src/server.rs) exposes it to agents.

### Main layers

The core layer is intentionally pure. [crates/ai-memory-core/src/lib.rs](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-core/src/lib.rs) exports ids, page types, actors, sanitization, handoffs, observations, messages, users, and workstream structures. Keeping that vocabulary IO-free is smart: other crates can share precise types without dragging in the server, database, or HTTP stack.

The ingestion layer is built for hooks, not chat APIs. [crates/ai-memory-hooks/src/router.rs](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-hooks/src/router.rs) documents bounded hook processing, batch limits, project cache limits, ingest gates, and subagent capture filtering. [crates/ai-memory-hooks/src/capture_policy.rs](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-hooks/src/capture_policy.rs) carries the policy edge where event payloads are admitted, dropped, or reduced.

The store layer uses SQLite as an index and operational ledger. [crates/ai-memory-store/src/lib.rs](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-store/src/lib.rs) opens the database, runs migrations, enables WAL, turns foreign keys back on after migrations, backfills indexes, then spawns the writer and read pool. The migrations under [crates/ai-memory-store/migrations/](https://github.com/akitaonrails/ai-memory/tree/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-store/migrations) show real product history: observations, handoffs, decay, embeddings, users, human auth, page windows, entities, agent messages, client activity, and session consolidation jobs.

The wiki layer is the durable materialization boundary. [crates/ai-memory-wiki/src/lib.rs](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-wiki/src/lib.rs) says it owns markdown-on-disk truth, atomic writes, frontmatter parsing/emission, and write-through to the store. That last phrase matters: the design tries to keep file writes and derived indexes aligned instead of letting a background indexer silently fall behind.

The agent-facing layer is MCP plus CLI. [crates/ai-memory-mcp/src/server.rs](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-mcp/src/server.rs) advertises tools for querying, listing, feedback, sweep, lint, consolidation, page writing, raw observations, handoffs, cross-project messages, and activity summaries. [crates/ai-memory-cli/src/cli.rs](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-cli/src/cli.rs) mirrors a lot of those operations for humans and setup scripts.

### Request / data / control flow

A supported agent emits a lifecycle hook. The router in [crates/ai-memory-hooks/src/router.rs](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-hooks/src/router.rs) parses the payload, resolves a workspace/project scope, applies capture policy, sanitizes the body, and turns it into a `NewObservation`. For keyed native events, the ingest key is committed with the observation so retries can converge instead of duplicating evidence.

The mutation goes through the writer actor in [crates/ai-memory-store/src/writer.rs](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-store/src/writer.rs). That actor handles page upserts, observation inserts, session start/end, handoffs, messages, auto-improvement proposals, user records, embeddings, purges, and workstream events. A single writer is not fancy, but it is exactly the right SQLite shape for a local server receiving bursty hook traffic.

On a true session end, [docs/ARCHITECTURE.md](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/docs/ARCHITECTURE.md) describes a rule-based session page plus an automatic handoff for the next agent. If a provider is configured, [crates/ai-memory-consolidate/src/consolidator.rs](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-consolidate/src/consolidator.rs) can ask an LLM for a consolidated page and then write it through the wiki, preserving the supersession and git path.

When the next agent starts or calls MCP, [crates/ai-memory-mcp/src/server.rs](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-mcp/src/server.rs) can return memory search results, raw observations, a briefing snapshot, an accepted handoff, or cross-project messages. Retrieval in [docs/ARCHITECTURE.md](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/docs/ARCHITECTURE.md) is not only vector search: it fuses FTS, entities, link-neighbor signals, optional vectors, optional reranking, access reinforcement, and raw fallback observations.

## Key directories and files

- [Cargo.toml](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/Cargo.toml) is the workspace map and dependency story.
- [docs/ARCHITECTURE.md](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/docs/ARCHITECTURE.md) is the best single read for the data flow and invariants.
- [crates/ai-memory-core/src/lib.rs](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-core/src/lib.rs) is the public domain vocabulary.
- [crates/ai-memory-store/src/lib.rs](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-store/src/lib.rs) opens the store and wires migrations, WAL, writer, reader pool, and backfills.
- [crates/ai-memory-store/src/writer.rs](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-store/src/writer.rs) is the mutation funnel.
- [crates/ai-memory-store/migrations/](https://github.com/akitaonrails/ai-memory/tree/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-store/migrations) is the product's persistence history.
- [crates/ai-memory-hooks/src/router.rs](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-hooks/src/router.rs) is the lifecycle ingest router.
- [crates/ai-memory-wiki/src/lib.rs](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-wiki/src/lib.rs) is the wiki layer index.
- [crates/ai-memory-mcp/src/server.rs](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-mcp/src/server.rs) is the tool server and operator surface.
- [crates/ai-memory-consolidate/src/consolidator.rs](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-consolidate/src/consolidator.rs) is the LLM page-rewrite path.
- [crates/ai-memory-cli/src/cli.rs](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-cli/src/cli.rs) reveals the actual operator contract.

## Important components

The `ObservationKind` vocabulary exported from [crates/ai-memory-core/src/lib.rs](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-core/src/lib.rs) is a key component because it normalizes all the messy vendor hook names into project memory events. Without that layer, every retrieval and consolidation rule would have to special-case each agent.

The single-writer actor in [crates/ai-memory-store/src/writer.rs](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-store/src/writer.rs) is the operational heart. It is not just an abstraction preference; it is a deliberate answer to SQLite write contention.

The wiki write path in [crates/ai-memory-wiki/src/lib.rs](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-wiki/src/lib.rs) is the product heart. Markdown pages are the user's memory, while the database is a derived serving layer.

The MCP `MEMORY_INSTRUCTIONS` and tool router in [crates/ai-memory-mcp/src/server.rs](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-mcp/src/server.rs) are also important. The server not only exposes tools; it tells clients to treat retrieved memory as untrusted historical data. That is the right stance for a system whose entire job is to replay old agent output.

## Important knobs / configs / extension points

- The agent and client matrix is visible in [README.md](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/README.md) and expanded in [docs/support-matrix.md](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/docs/support-matrix.md).
- Hook admission, capture filtering, and subagent-drop behavior live around [crates/ai-memory-hooks/src/capture_policy.rs](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-hooks/src/capture_policy.rs) and [crates/ai-memory-hooks/src/router.rs](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-hooks/src/router.rs).
- LLM providers and embedding providers are separate from the default path in [crates/ai-memory-llm/](https://github.com/akitaonrails/ai-memory/tree/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-llm), which supports the project's zero-LLM default.
- Consolidation, lint, sweep, and auto-improvement are grouped in [crates/ai-memory-consolidate/](https://github.com/akitaonrails/ai-memory/tree/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-consolidate), so memory capture can run without forcing all maintenance work into the hot path.
- The operator surface in [crates/ai-memory-cli/src/cli.rs](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-cli/src/cli.rs) exposes escape hatches: `reindex`, `backup`, `restore`, `doctor`, `forget-sweep`, `lint`, `pending-writes`, `install-hooks`, and `install-mcp`.

## Practical questions and answers

Q: Is this mainly a vector database for agents?

A: No. [README.md](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/README.md) and [docs/ARCHITECTURE.md](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/docs/ARCHITECTURE.md) make the markdown wiki the source of truth. FTS, entities, links, optional embeddings, and raw fallback are serving indexes around that wiki.

Q: What part would fail first under real daily use?

A: Hook capture and project scoping are the risky parts. [crates/ai-memory-hooks/src/router.rs](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-hooks/src/router.rs) has a lot of machinery for keyed ingest, project cache, admission timeout, batch limits, and subagent sessions because that edge is messy. The repo treats it as messy instead of pretending hooks are clean events.

Q: Can it work without an LLM key?

A: Yes. The README's default story is capture, search, and handoffs with no required LLM calls. The LLM path in [crates/ai-memory-consolidate/src/consolidator.rs](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-consolidate/src/consolidator.rs) is optional consolidation, not the base persistence model.

Q: What makes it team-capable rather than just personal notes?

A: The core model includes users, actors, owners, auth levels, messages, workspaces, projects, and scopes in [crates/ai-memory-core/src/lib.rs](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-core/src/lib.rs), while store migrations include users, page authorship, audit log author ids, human auth, API credentials, and cross-project messages in [crates/ai-memory-store/migrations/](https://github.com/akitaonrails/ai-memory/tree/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-store/migrations).

## What is smart

The source-of-truth choice is smart. Many memory products trap value in an opaque database. ai-memory puts the durable value into git-backed markdown pages and treats SQLite as derived infrastructure.

The single-writer store is smart. Agent hook traffic is bursty and boring failure modes matter. [crates/ai-memory-store/src/writer.rs](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-store/src/writer.rs) is the sort of infrastructure decision users will never compliment when it works, but will hate instantly if it is wrong.

The trust boundary is smart. The MCP instructions in [crates/ai-memory-mcp/src/server.rs](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-mcp/src/server.rs) explicitly say retrieved memory is untrusted historical data, not instructions. Agent memory systems need that disclaimer in code, not just in a security blog post.

## What is flawed or weak

The project is broad enough to be hard to adopt casually. A builder who only wants "project notes shared across agents" has to understand hooks, MCP registration, workspace/project scopes, SQLite data directories, wiki git commits, auth, and provider knobs. [crates/ai-memory-cli/src/cli.rs](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-cli/src/cli.rs) is impressively complete, but the command surface is large.

The quality of the memory will depend heavily on hook fidelity. If a harness changes event schemas, runs without proper session ends, or drops tool lifecycle context, the wiki can still exist but be less useful. The number of integration folders under [hooks/](https://github.com/akitaonrails/ai-memory/tree/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/hooks) is a strength and also a maintenance burden.

The auto-improvement and LLM consolidation paths are powerful but delicate. [crates/ai-memory-consolidate/src/consolidator.rs](https://github.com/akitaonrails/ai-memory/blob/1fe32bc2be32490ebf614c86eb9ab45718dcceb1/crates/ai-memory-consolidate/src/consolidator.rs) has bounded retry logic and writes through the wiki, but a bad provider output can still make a convincing bad page unless admission, review, or tests catch it.

## What we can learn / steal

Steal the file-first boundary. If a tool claims to help builders remember project context, make the durable memory readable, versioned, and portable. Use the database to index and serve it.

Steal normalized lifecycle vocabulary. Tool events from different agents should become a small set of domain events before storage and retrieval logic sees them.

Steal claim-once handoffs. Cross-agent continuity should be explicit state with ownership and lifecycle, not an honor-system paragraph at the end of a chat.

Steal the single-writer actor for local SQLite products with multiple async callers. It is simpler than fighting sporadic lock failures across a server, hook drainers, and CLI commands.

## How we could apply it

For our own agent tools, start with a smaller version: capture session starts, user prompts, tool summaries, compactions, and session ends into a local store; generate one `sessions/<id>.md` page; and expose search plus one explicit handoff. Do not begin with embeddings. Begin with a readable page and a rebuildable index.

For team memory, use ai-memory's scoping idea: workspace, project, actor, owner, and global preference scopes. Without that, shared memory becomes a pile of stale personal notes.

For safety, copy the MCP trust stance. Every recalled page or handoff should be treated as quoted historical evidence. Current instructions and current repo state stay authoritative.

## Bottom line

ai-memory is worth studying because it treats agent memory as infrastructure, not a prompt trick. The durable idea is simple: capture the work automatically, compile it into markdown you own, index it for retrieval, and make handoffs explicit enough that one agent can safely pick up where another stopped.
