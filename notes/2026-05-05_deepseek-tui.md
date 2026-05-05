# DeepSeek TUI

- Repo: `Hmbown/DeepSeek-TUI`
- URL: https://github.com/Hmbown/DeepSeek-TUI
- Date: 2026-05-05
- Repo snapshot studied: `main@16142b5f5eda95450d0362c53857004b5c043262`
- Why picked today: It is hot right now, clearly AI-related, and more substantial than the usual terminal-agent wrapper. The interesting part is not the TUI paint, it is the amount of runtime infrastructure packed behind a single Rust binary.

## Executive summary
DeepSeek TUI is a terminal-native coding agent that wants to be a local operating shell for long-running AI work, not just a chat client. It wraps model access, tool execution, approval policy, session persistence, background tasks, runtime HTTP/SSE APIs, MCP integration, skills, and post-edit LSP diagnostics into one Rust workspace.

The key insight is that the repo is selling a TUI, but building a runtime. The TUI is only the front door. The real product is a stateful agent host with durable threads, side-git rollback, background automation, and a broad tool plane. The main weakness is architectural sprawl: the workspace is being split into crates, but the live runtime still concentrates a lot of real behavior inside `crates/tui`.

## What they built
They built a Rust-first coding agent with three visible surfaces:

- a dispatcher CLI in [`crates/cli/src/main.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/cli/src/main.rs)
- the main terminal runtime in [`crates/tui/src/main.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/tui/src/main.rs)
- a headless runtime server in [`crates/tui/src/runtime_api.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/tui/src/runtime_api.rs)

Under that, they built a fairly serious agent host:

- the async agent engine in [`crates/tui/src/core/engine.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/tui/src/core/engine.rs)
- the streaming turn loop in [`crates/tui/src/core/engine/turn_loop.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/tui/src/core/engine/turn_loop.rs)
- tool execution and parallel fanout in [`crates/tui/src/core/engine/tool_execution.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/tui/src/core/engine/tool_execution.rs)
- persistent thread and message storage in [`crates/state/src/lib.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/state/src/lib.rs)
- a durable task queue in [`crates/tui/src/task_manager.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/tui/src/task_manager.rs)
- a typed tool capability layer in [`crates/tools/src/lib.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/tools/src/lib.rs)
- model/provider resolution in [`crates/agent/src/lib.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/agent/src/lib.rs)

## Why it matters
A lot of open-source coding agents are still thin shells around an API client plus a handful of tools. DeepSeek TUI is more ambitious. It tries to make the agent resumable, automatable, auditable, and scriptable.

That makes it useful to study for a simple reason: the hard part of agent products is usually not “stream tokens into a terminal”. It is state management, interruption handling, approval boundaries, persistence, recovery, and giving the same runtime multiple surfaces.

## Repo shape at a glance
Top-level structure:

- [`crates/`](https://github.com/Hmbown/DeepSeek-TUI/tree/16142b5f5eda95450d0362c53857004b5c043262/crates) is the main workspace and contains the actual product.
- [`crates/tui/`](https://github.com/Hmbown/DeepSeek-TUI/tree/16142b5f5eda95450d0362c53857004b5c043262/crates/tui) is still the center of gravity: TUI, engine, runtime API, task manager, skills, MCP glue, sandboxing, memory, LSP hooks.
- [`crates/cli/`](https://github.com/Hmbown/DeepSeek-TUI/tree/16142b5f5eda95450d0362c53857004b5c043262/crates/cli) is the tiny entrypoint binary.
- [`crates/state/`](https://github.com/Hmbown/DeepSeek-TUI/tree/16142b5f5eda95450d0362c53857004b5c043262/crates/state) is SQLite-backed persistence for threads, messages, checkpoints, and jobs.
- [`crates/tools/`](https://github.com/Hmbown/DeepSeek-TUI/tree/16142b5f5eda95450d0362c53857004b5c043262/crates/tools) is the shared tool contract layer.
- [`crates/agent/`](https://github.com/Hmbown/DeepSeek-TUI/tree/16142b5f5eda95450d0362c53857004b5c043262/crates/agent) currently carries model/provider registry logic, not a whole independent agent runtime.
- [`crates/app-server/`](https://github.com/Hmbown/DeepSeek-TUI/tree/16142b5f5eda95450d0362c53857004b5c043262/crates/app-server), [`crates/mcp/`](https://github.com/Hmbown/DeepSeek-TUI/tree/16142b5f5eda95450d0362c53857004b5c043262/crates/mcp), [`crates/config/`](https://github.com/Hmbown/DeepSeek-TUI/tree/16142b5f5eda95450d0362c53857004b5c043262/crates/config), [`crates/execpolicy/`](https://github.com/Hmbown/DeepSeek-TUI/tree/16142b5f5eda95450d0362c53857004b5c043262/crates/execpolicy), and [`crates/protocol/`](https://github.com/Hmbown/DeepSeek-TUI/tree/16142b5f5eda95450d0362c53857004b5c043262/crates/protocol) show a gradual split into reusable subsystems.
- [`docs/`](https://github.com/Hmbown/DeepSeek-TUI/tree/16142b5f5eda95450d0362c53857004b5c043262/docs) is unusually important here because it documents the intended boundaries better than the codebase currently enforces.
- [`npm/deepseek-tui/`](https://github.com/Hmbown/DeepSeek-TUI/tree/16142b5f5eda95450d0362c53857004b5c043262/npm/deepseek-tui) is just distribution plumbing for the binary installer path.

This is not a small library repo. It is a product workspace, mid-refactor.

## Layered architecture dissection
### High-level system shape
The cleanest mental model is:

1. command entry and configuration
2. sessionful agent runtime
3. tool and extension plane
4. persistence and background execution
5. optional API/server surfaces around the same runtime

The repo’s own architecture note says the same thing explicitly in [`docs/ARCHITECTURE.md`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/docs/ARCHITECTURE.md), and that file is worth reading because it admits an important truth: the crate split exists, but `crates/tui` still owns much of the live behavior.

### Main layers
**1. Entry and command layer**

- [`crates/cli/src/main.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/cli/src/main.rs) is a tiny launcher.
- [`crates/tui/src/main.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/tui/src/main.rs) is the real command router. It owns subcommands for sessions, auth, models, reviews, MCP, sandbox, server mode, evals, and interactive runs.
- That is a strong clue that the TUI crate is really the application crate.

**2. Agent runtime layer**

- [`crates/tui/src/core/engine.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/tui/src/core/engine.rs) is the main orchestrator.
- It carries model/session config, workspace boundaries, compaction, cycle management, capacity guardrails, sub-agent settings, network policy, memory injection, strict tool mode, and runtime services.
- [`crates/tui/src/core/engine/turn_loop.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/tui/src/core/engine/turn_loop.rs) is where the actual turn mechanics live: streaming retries, steer-input ingestion, compaction, context overflow recovery, LSP diagnostic injection, tool selection, and request assembly.

**3. Tool and extension layer**

- [`crates/tools/src/lib.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/tools/src/lib.rs) defines capability flags like read-only, file writes, shell execution, network, sandboxability, and approval requirements.
- [`crates/tui/src/core/engine/tool_execution.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/tui/src/core/engine/tool_execution.rs) turns those contracts into actual execution behavior, including parallel read-only fanout and terminal pause/resume handling for interactive tools.
- MCP and skills are plugged in from [`crates/tui/src/mcp.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/tui/src/mcp.rs) and [`crates/tui/src/skills.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/tui/src/skills.rs).

**4. Persistence and job layer**

- [`crates/state/src/lib.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/state/src/lib.rs) provides the durable SQLite schema for threads, messages, checkpoints, and jobs.
- [`crates/tui/src/task_manager.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/tui/src/task_manager.rs) adds a richer durable task abstraction on top: timelines, artifacts, checklist state, verification gates, PR-attempt tracking, and bounded workers.
- This is the part that most “CLI agents” do not have.

**5. API and multi-surface layer**

- [`crates/tui/src/runtime_api.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/tui/src/runtime_api.rs) exposes local HTTP/SSE endpoints for sessions, tasks, threads, runtime turns, MCP inventory, skills, and workspace status.
- That means the TUI is not just an app, it is also a local agent server.

### Request / data / control flow
A typical interactive run looks like this:

1. [`crates/cli/src/main.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/cli/src/main.rs) delegates into the TUI binary.
2. [`crates/tui/src/main.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/tui/src/main.rs) parses mode, workspace, profile, model, and subcommand state.
3. The engine boots from [`crates/tui/src/core/engine.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/tui/src/core/engine.rs) with session state, tool registry, MCP pool, and config-derived runtime services.
4. [`crates/tui/src/core/engine/turn_loop.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/tui/src/core/engine/turn_loop.rs) assembles a streaming request, handles retries, and decides whether compaction or context recovery is needed before a call.
5. Tool calls route through [`crates/tui/src/core/engine/tool_execution.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/tui/src/core/engine/tool_execution.rs), which enforces execution locks, approval constraints, and MCP dispatch.
6. Results and events are written into session/thread state, then the loop continues until completion, failure, or interruption.
7. If edits occurred, the LSP hook path described in [`docs/ARCHITECTURE.md`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/docs/ARCHITECTURE.md) injects diagnostics back into the next turn.

A headless/API flow adds one more shell around the same machinery:

1. [`crates/tui/src/runtime_api.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/tui/src/runtime_api.rs) receives HTTP requests.
2. It creates or resumes runtime threads and tasks.
3. Those feed into the same underlying engine and persistence stack.

## Key directories and files
- [`Cargo.toml`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/Cargo.toml): the fastest way to understand intended boundaries across the workspace.
- [`README.md`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/README.md): product positioning, feature surface, and user-facing promises.
- [`docs/ARCHITECTURE.md`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/docs/ARCHITECTURE.md): the most honest map of the runtime shape.
- [`crates/tui/src/main.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/tui/src/main.rs): the actual app binary and command surface.
- [`crates/tui/src/core/engine.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/tui/src/core/engine.rs): core runtime state and orchestration.
- [`crates/tui/src/core/engine/turn_loop.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/tui/src/core/engine/turn_loop.rs): the real agent loop.
- [`crates/tui/src/core/engine/tool_execution.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/tui/src/core/engine/tool_execution.rs): approval-aware and parallel-aware tool execution.
- [`crates/state/src/lib.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/state/src/lib.rs): durable schema for sessions and jobs.
- [`crates/tui/src/task_manager.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/tui/src/task_manager.rs): background automation, task durability, and evidence capture.
- [`crates/tui/src/runtime_api.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/tui/src/runtime_api.rs): local server surface over the runtime.
- [`crates/agent/src/lib.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/agent/src/lib.rs): provider/model normalization and fallback logic.
- [`crates/tools/src/lib.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/tools/src/lib.rs): the typed tool contract that helps keep the runtime sane.

## Important components
**The engine config as product spec**

The `EngineConfig` struct in [`crates/tui/src/core/engine.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/tui/src/core/engine.rs) is almost a compressed product map. It includes workspace root, shell permissioning, compaction, cycle checkpoints, capacity guardrails, sub-agent overrides, network policy, snapshots, LSP, runtime services, memory injection, and strict tool mode. That is not a toy chat client config. That is an agent host config.

**The turn loop**

[`crates/tui/src/core/engine/turn_loop.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/tui/src/core/engine/turn_loop.rs) is where the product earns its keep. It does stream retries, max-step handling, context compaction, preflight token-budget checks, overflow recovery, steering, LSP diagnostic injection, layered context checkpoints, and tool-choice assembly. That is all the annoying runtime reality most demos hide.

**Tool capability typing**

[`crates/tools/src/lib.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/tools/src/lib.rs) is simple but important. Tool capability and approval requirements are explicit enum values, not fuzzy comments. That lets the engine reason concretely about what can run in parallel, what can auto-approve, and what must be blocked.

**Interactive-tool terminal guard**

The `InteractiveTerminalGuard` in [`crates/tui/src/core/engine/tool_execution.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/tui/src/core/engine/tool_execution.rs) is a small but very real piece of engineering. It fixes a class of terminal corruption bugs around cancellation by using RAII to guarantee resume events even when a tool future gets dropped. That is the kind of scar-tissue code you only write after living with the product.

**Durable task manager**

[`crates/tui/src/task_manager.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/tui/src/task_manager.rs) is one of the most interesting parts of the repo. It treats long-running agent work as first-class durable state, with timelines, verification gates, task-local artifacts, and bounded workers. This is much closer to a lightweight agent job system than to a normal CLI background process.

**SQLite state store**

[`crates/state/src/lib.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/state/src/lib.rs) anchors the whole system. Threads, messages, checkpoints, and jobs live in a local schema, which is what makes resume, fork, recovery, and task durability believable.

## Important knobs / configs / extension points
- [`~/.deepseek/config.toml` as described in `README.md`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/README.md) is the main user/runtime control surface.
- [`docs/MCP.md`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/docs/MCP.md) matters if you want external tool servers.
- [`crates/tui/src/main.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/tui/src/main.rs) exposes runtime flags like workspace, resume, profile, model, yolo mode, and server mode.
- [`crates/agent/src/lib.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/agent/src/lib.rs) is the extension seam for provider/model mapping and fallback logic.
- [`crates/tools/src/lib.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/tools/src/lib.rs) and the tool modules under [`crates/tui/src/tools/`](https://github.com/Hmbown/DeepSeek-TUI/tree/16142b5f5eda95450d0362c53857004b5c043262/crates/tui/src/tools) are the capability extension seam.
- [`crates/tui/src/runtime_api.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/tui/src/runtime_api.rs) is the seam if you want to drive the runtime from another client.
- [`crates/state/src/lib.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/state/src/lib.rs) is where durability and schema evolution pressure shows up first.

## Practical questions and answers
**Is this mostly a nice TUI around a model?**

No. The TUI is the visible shell, but the repo’s real weight is the runtime beneath it.

**What is the strongest engineering idea here?**

Treating an agent session as durable operating state, not transient chat state.

**What is actually differentiated?**

The combination of local binary distribution, durable tasks, runtime API, side-git rollback, and explicit tool-policy machinery.

**Where is the architecture still awkward?**

The workspace split is only partially complete. The project talks like a multi-crate system, but `crates/tui` still owns too much of the real runtime.

**Would I trust it as infrastructure?**

For personal or team-agent workflows, maybe yes. As a deeply stable platform, not yet. It is still moving fast and the boundaries are still settling.

## What is smart
- The repo is honest about runtime concerns like cancellations, context overflow, resume, approval policy, and recovery.
- The tool capability model in [`crates/tools/src/lib.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/tools/src/lib.rs) is clean and practical.
- The engine’s turn loop shows real experience with long-running model sessions.
- The local runtime API in [`crates/tui/src/runtime_api.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/tui/src/runtime_api.rs) is a smart move because it lets the same system serve both humans and automation.
- The durable task layer in [`crates/tui/src/task_manager.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/tui/src/task_manager.rs) is more serious than the average repo in this category.
- The repo has several nice “operator pain” fixes, especially around terminal pause/resume and post-edit diagnostics.

## What is flawed or weak
- The architectural split is aspirational in places. The clean crate story is ahead of the code reality.
- `crates/tui/src/main.rs` is huge, which usually means too many concerns are still coupled.
- The product surface is broad: TUI, CLI, tasks, runtime API, MCP, skills, LSP, snapshots, sandbox, background jobs. That is powerful, but also maintenance-heavy.
- The differentiation leans hard on DeepSeek-specific product assumptions like huge context and prefix-cache economics. That is fine today, but could become a portability constraint.
- Like every tool-rich coding agent, it still inherits the normal reliability problem: the runtime can be robust while the model still makes bad decisions.

## What we can learn / steal
- Treat cancellations and terminal cleanup as first-class engineering work, not edge cases.
- Model tool capabilities explicitly so approval and concurrency behavior can be derived instead of hand-waved.
- Persist threads, messages, checkpoints, and jobs if you want serious resume/fork/background workflows.
- Give the same core agent runtime both an interactive shell and a local API surface.
- Use side-git snapshots for rollback instead of touching the user’s repo history.

## How we could apply it
If we were building our own local agent shell, I would steal these ideas first:

1. a typed tool capability/approval model like [`crates/tools/src/lib.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/tools/src/lib.rs)
2. a durable state store like [`crates/state/src/lib.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/state/src/lib.rs)
3. a background task system with evidence capture like [`crates/tui/src/task_manager.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/tui/src/task_manager.rs)
4. the interactive-tool RAII safety pattern from [`crates/tui/src/core/engine/tool_execution.rs`](https://github.com/Hmbown/DeepSeek-TUI/blob/16142b5f5eda95450d0362c53857004b5c043262/crates/tui/src/core/engine/tool_execution.rs)

I would be more cautious about copying the whole repo shape. The better lesson is not “one giant agent app”. It is “build one runtime that can support multiple surfaces cleanly”.

## Bottom line
DeepSeek TUI looks like a terminal app, but the real asset is the runtime under it.

The key insight is that the repo treats coding-agent work as durable operations, not ephemeral chat. That is the part worth studying and stealing.