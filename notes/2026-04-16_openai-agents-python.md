# OpenAI Agents SDK

- Repo: [openai/openai-agents-python](https://github.com/openai/openai-agents-python)
- URL: https://github.com/openai/openai-agents-python
- Date: 2026-04-16
- Repo snapshot studied: [`main@4f3c8a5379c1b44527c9a0a159d20b46755f4eaf`](https://github.com/openai/openai-agents-python/tree/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf)
- Why picked today: It is hot enough to be socially relevant, but unlike a lot of agent-framework noise, there is actual systems work here: orchestration, tool/runtime plumbing, session persistence, tracing, realtime, sandbox execution, and a serious attempt to keep the public API pleasant.

## Executive summary

This is not “just an agents wrapper.” It is a fairly opinionated orchestration runtime packaged as a Python SDK. The marketing surface is simple — define agents, tools, handoffs, guardrails, sessions, tracing — but the repo reveals the real bet: treat agent execution as a stateful run loop with typed items, resumability, approval interrupts, model-provider abstraction, and optional execution environments like sandbox + voice/realtime.

The strongest design move is the split between the clean public surface in [`src/agents/__init__.py`](https://github.com/openai/openai-agents-python/blob/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/__init__.py) and the gnarly orchestration core in [`src/agents/run.py`](https://github.com/openai/openai-agents-python/blob/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/run.py) plus [`src/agents/run_internal/`](https://github.com/openai/openai-agents-python/tree/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/run_internal). They are trying to make the outer API feel lightweight while hiding a pretty large amount of state-management machinery.

The weakness is also obvious: the simplicity promise depends on a lot of internal complexity. This is now a real framework, not a tiny library. That means more power, but also more surface area for subtle behavior, cross-feature interactions, and maintenance drag.

## What they built

They built a Python SDK for multi-agent workflows with several layers:

- declarative agent definitions via [`src/agents/agent.py`](https://github.com/openai/openai-agents-python/blob/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/agent.py)
- a central runner/orchestrator via [`src/agents/run.py`](https://github.com/openai/openai-agents-python/blob/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/run.py)
- a tool system covering function tools, MCP, web/file/computer tools, shell/apply_patch/custom tools via [`src/agents/tool.py`](https://github.com/openai/openai-agents-python/blob/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/tool.py)
- model/provider abstraction via [`src/agents/models/`](https://github.com/openai/openai-agents-python/tree/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/models)
- session/memory persistence via [`src/agents/memory/`](https://github.com/openai/openai-agents-python/tree/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/memory)
- tracing/observability via [`src/agents/tracing/`](https://github.com/openai/openai-agents-python/tree/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/tracing)
- realtime/voice execution via [`src/agents/realtime/`](https://github.com/openai/openai-agents-python/tree/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/realtime) and [`src/agents/voice/`](https://github.com/openai/openai-agents-python/tree/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/voice)
- sandboxed long-running work via [`src/agents/sandbox/`](https://github.com/openai/openai-agents-python/tree/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/sandbox)

So the product is really “agent workflow runtime with batteries,” not merely agent objects.

## Why it matters

Most agent frameworks collapse into one of two failure modes:

- too toy-like: dead simple demos, no serious execution/runtime model
- too enterprise-gelatinous: giant abstraction stack, hard to trace the real control flow

This repo is trying to sit in the middle. The public API stays teachable, but the implementation admits that real agent execution needs interruption, persistence, tool routing, model backend variability, and observability.

That matters because the actual hard problem in agent systems is not “how do I call an LLM?” It is “how do I manage an evolving run with tools, retries, approvals, conversation state, and different execution environments without everything turning into bespoke app spaghetti?”

## Repo shape at a glance

Top-level repo shape:

- [`src/agents/`](https://github.com/openai/openai-agents-python/tree/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents): the actual SDK implementation
  - [`agent.py`](https://github.com/openai/openai-agents-python/blob/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/agent.py): agent definitions and tool/handoff semantics
  - [`run.py`](https://github.com/openai/openai-agents-python/blob/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/run.py): the main runner and orchestration entrypoints
  - [`run_internal/`](https://github.com/openai/openai-agents-python/tree/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/run_internal): private engine room for turns, tools, state, approvals, persistence, streaming
  - [`tool.py`](https://github.com/openai/openai-agents-python/blob/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/tool.py): massive tool abstraction layer
  - [`models/`](https://github.com/openai/openai-agents-python/tree/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/models): provider/model adapters and routing
  - [`memory/`](https://github.com/openai/openai-agents-python/tree/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/memory): sessions and persistence backends
  - [`sandbox/`](https://github.com/openai/openai-agents-python/tree/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/sandbox): container/workspace/runtime layer for longer tasks
  - [`realtime/`](https://github.com/openai/openai-agents-python/tree/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/realtime): realtime model and session flows
  - [`voice/`](https://github.com/openai/openai-agents-python/tree/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/voice): voice pipeline pieces
  - [`tracing/`](https://github.com/openai/openai-agents-python/tree/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/tracing): spans, traces, processors, setup
- [`examples/`](https://github.com/openai/openai-agents-python/tree/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/examples): lots of runnable patterns rather than one token example
- [`tests/`](https://github.com/openai/openai-agents-python/tree/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/tests): broad subsystem coverage mirroring repo structure
- [`docs/`](https://github.com/openai/openai-agents-python/tree/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/docs): docs site source, including subsystem-specific docs
- [`pyproject.toml`](https://github.com/openai/openai-agents-python/blob/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/pyproject.toml): dependency and optional-feature map; useful for understanding what is first-class vs optional

This is a healthy repo shape. The examples/docs/tests all mirror the implementation domains instead of being tossed in a junk drawer.

## Layered architecture dissection

### High-level system shape

The core execution model appears to be:

1. define an [`Agent`](https://github.com/openai/openai-agents-python/blob/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/agent.py)
2. run it through [`Runner`](https://github.com/openai/openai-agents-python/blob/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/run.py)
3. the runner iterates turns, handling guardrails, tool calls, handoffs, interruptions, persistence, and final output
4. optional subsystems — memory, tracing, sandbox, realtime, voice — plug into the same run machinery rather than being completely separate products

That last point is the important one. The repo is architected around the run loop, not around prompt templates or a DSL.

### Main layers

**1. Public API / export layer**

- [`src/agents/__init__.py`](https://github.com/openai/openai-agents-python/blob/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/__init__.py)

This file is huge, but strategically huge: it centralizes the public surface so the package feels coherent. It re-exports the concepts users are supposed to think in: Agent, Runner, tools, sessions, tracing, sandbox, output schemas, etc.

**2. Agent definition layer**

- [`src/agents/agent.py`](https://github.com/openai/openai-agents-python/blob/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/agent.py)

This layer defines what an agent is: instructions/prompt, tools, MCP servers, handoffs, model selection, guardrails, output types, and hooks. It also includes the “agent as tool” transformation, which is one of the cleaner design choices in the repo.

**3. Orchestration / run loop layer**

- [`src/agents/run.py`](https://github.com/openai/openai-agents-python/blob/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/run.py)
- [`src/agents/run_internal/run_loop.py`](https://github.com/openai/openai-agents-python/tree/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/run_internal)
- [`src/agents/run_internal/run_steps.py`](https://github.com/openai/openai-agents-python/tree/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/run_internal)
- [`src/agents/run_internal/tool_execution.py`](https://github.com/openai/openai-agents-python/tree/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/run_internal)
- [`src/agents/run_internal/session_persistence.py`](https://github.com/openai/openai-agents-python/tree/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/run_internal)

`run.py` is the real heart. The classmethods on `Runner` are a thin facade over `AgentRunner`, and the actual implementation is a serious state machine: handling resumed runs, session persistence, server-managed conversation mode, tracing spans, sandbox preparation, tool-use tracking, interruptions, handoffs, output guardrails, and more.

This is where the project stops being a cute SDK and becomes infrastructure.

**4. Tooling / actuation layer**

- [`src/agents/tool.py`](https://github.com/openai/openai-agents-python/blob/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/tool.py)
- [`src/agents/mcp/`](https://github.com/openai/openai-agents-python/tree/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/mcp)

`tool.py` is enormous because it is effectively a platform boundary. It normalizes many tool kinds into one runtime vocabulary: plain function tools, hosted tools, web search, file search, computer use, shell, apply_patch, custom tools, hosted MCP, local shell, etc.

This is the repo’s most valuable practical layer, because agents become useful only when tool execution semantics are predictable.

**5. Model/provider routing layer**

- [`src/agents/models/`](https://github.com/openai/openai-agents-python/tree/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/models)
- especially [`multi_provider.py`](https://github.com/openai/openai-agents-python/blob/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/models/multi_provider.py)

The provider layer is more thought-through than many OSS agent frameworks. `MultiProvider` routes by model-name prefix and includes practical handling for ambiguous `openai/...` names and unknown prefixes. That is boring in a good way: it shows they have run into real interop headaches and built escape hatches.

**6. Memory/session layer**

- [`src/agents/memory/session.py`](https://github.com/openai/openai-agents-python/tree/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/memory)
- [`src/agents/memory/sqlite_session.py`](https://github.com/openai/openai-agents-python/blob/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/memory/sqlite_session.py)

This is not “vector memory” hype; it is operational memory first: conversation/session persistence, limits, compaction-aware variants, SQLite-backed storage. Good. Most actual apps need durable run/session state before they need memory theater.

**7. Execution-environment layer**

- [`src/agents/sandbox/runtime.py`](https://github.com/openai/openai-agents-python/blob/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/sandbox/runtime.py)
- [`src/agents/sandbox/`](https://github.com/openai/openai-agents-python/tree/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/sandbox)

Sandbox support is not bolted on as an afterthought. `SandboxRuntime` is woven directly into the run lifecycle: prepare agent, manage session, bind capabilities, enqueue memory, clean up, store resume state. That is much more serious than “here is a docker example.”

**8. Observability / tracing layer**

- [`src/agents/tracing/`](https://github.com/openai/openai-agents-python/tree/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/tracing)

The runner creates task spans, turn spans, agent spans, usage attachment, and trace-state propagation. This suggests the repo is designed for debugging real deployments, not just tutorials.

### Request / data / control flow

The main control flow in [`src/agents/run.py`](https://github.com/openai/openai-agents-python/blob/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/run.py) roughly looks like this:

1. normalize input and resumed state
2. resolve conversation/session mode
3. create or rehydrate run state, tracing state, tool-use tracker
4. optionally prepare sandbox runtime
5. loop turns until one of:
   - final output
   - handoff to another agent
   - interruption/approval pause
   - run again after tool execution
   - max-turn failure
6. persist items to session/history as needed
7. run output guardrails
8. finalize traces / cleanup sandbox / dispose computers

That is the right shape. There is one main river of control, with subsystems joining it in specific places.

## Key directories and files

The most important source paths for understanding the system:

- [`src/agents/__init__.py`](https://github.com/openai/openai-agents-python/blob/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/__init__.py)
  - tells you what the product thinks its public vocabulary is
- [`src/agents/agent.py`](https://github.com/openai/openai-agents-python/blob/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/agent.py)
  - the primary abstraction and a good read for framework taste
- [`src/agents/run.py`](https://github.com/openai/openai-agents-python/blob/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/run.py)
  - the orchestration kernel
- [`src/agents/run_internal/`](https://github.com/openai/openai-agents-python/tree/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/run_internal)
  - the actual private implementation modules that keep `run.py` from becoming totally uninhabitable
- [`src/agents/tool.py`](https://github.com/openai/openai-agents-python/blob/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/tool.py)
  - where tool abstraction, approval, timeout, hosted/local tool support, and search surfaces converge
- [`src/agents/models/multi_provider.py`](https://github.com/openai/openai-agents-python/blob/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/models/multi_provider.py)
  - good file for seeing whether “provider-agnostic” is real or fake
- [`src/agents/memory/sqlite_session.py`](https://github.com/openai/openai-agents-python/blob/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/memory/sqlite_session.py)
  - practical persistence implementation, not just interfaces
- [`src/agents/sandbox/runtime.py`](https://github.com/openai/openai-agents-python/blob/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/sandbox/runtime.py)
  - shows how sandbox support plugs into the main lifecycle
- [`examples/`](https://github.com/openai/openai-agents-python/tree/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/examples)
  - reveals intended user journeys and feature priorities
- [`tests/`](https://github.com/openai/openai-agents-python/tree/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/tests)
  - useful for discovering what the maintainers consider contractually important

## Important components

### `Agent`

- [`src/agents/agent.py`](https://github.com/openai/openai-agents-python/blob/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/agent.py)

This object carries almost all user-facing orchestration intent: instructions, tools, handoffs, model, guardrails, output type, hooks, tool-use behavior. It is both the ergonomic center of the SDK and the boundary object feeding the runner.

### `Runner` / `AgentRunner`

- [`src/agents/run.py`](https://github.com/openai/openai-agents-python/blob/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/run.py)

This is the actual operating system of the framework. If you want to know whether the SDK is serious, this is the file to read. It manages resume semantics, turn loops, sessions, trace lifecycles, interruptions, handoffs, tool trackers, and cleanup.

### `FunctionTool` + tool wrappers

- [`src/agents/tool.py`](https://github.com/openai/openai-agents-python/blob/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/tool.py)

The design here is strong because it does not stop at decorator sugar. It deals with JSON schema, error handling, approval hooks, timeout behavior, search-surface exposure, hosted-vs-local execution, and context shaping.

### `MultiProvider`

- [`src/agents/models/multi_provider.py`](https://github.com/openai/openai-agents-python/blob/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/models/multi_provider.py)

This component matters because cross-provider support is where many frameworks become a pile of stringly-typed lies. Here, they at least encode prefix routing explicitly and deal with alias-vs-literal model IDs.

### `SQLiteSession`

- [`src/agents/memory/sqlite_session.py`](https://github.com/openai/openai-agents-python/blob/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/memory/sqlite_session.py)

Not glamorous, but important. This is the kind of implementation detail that tells you whether the team is thinking about actual app durability and concurrency instead of conference-stage vibes.

### `SandboxRuntime`

- [`src/agents/sandbox/runtime.py`](https://github.com/openai/openai-agents-python/blob/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/sandbox/runtime.py)

This is one of the clearest signs of ambition. The framework wants to support agents that do real, longer-horizon work in controlled environments, not just single-turn assistant toys.

## Important knobs / configs / extension points

A few knobs that seem especially important:

- model/provider routing in [`src/agents/models/multi_provider.py`](https://github.com/openai/openai-agents-python/blob/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/models/multi_provider.py)
  - `openai_prefix_mode`
  - `unknown_prefix_mode`
  - custom `provider_map`
- tool behavior in [`src/agents/agent.py`](https://github.com/openai/openai-agents-python/blob/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/agent.py)
  - `tool_use_behavior`
  - `reset_tool_choice`
  - `mcp_servers`
  - `output_type`
- tool execution policies in [`src/agents/tool.py`](https://github.com/openai/openai-agents-python/blob/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/tool.py)
  - `needs_approval`
  - timeout controls
  - `defer_loading`
  - tool namespaces / tool search surfaces
- session settings in [`src/agents/memory/`](https://github.com/openai/openai-agents-python/tree/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/memory)
  - history limits and persistence behavior
- optional dependency groups in [`pyproject.toml`](https://github.com/openai/openai-agents-python/blob/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/pyproject.toml)
  - `voice`, `realtime`, `sqlalchemy`, `redis`, `docker`, `temporal`, etc.

One useful read from `pyproject.toml`: the optional dependency groups basically tell you the product map. This repo is not pretending to be one simple package; it is a hub with multiple operational modes.

## Practical questions and answers

### Is this actually lightweight?

At the API level: reasonably yes.

At the implementation level: absolutely not, and that is fine. The “lightweight” claim mostly means the entrypoint ergonomics are lighter than the internal machinery.

### Is the provider-agnostic claim real?

Partly. The abstraction is real enough to matter, especially around `MultiProvider`, but the project is still clearly optimized around OpenAI-native concepts and Responses API semantics. Provider-agnostic here means “better than hard-coded OpenAI-only,” not “all providers are equal citizens.”

### Does it understand long-running work, or only chat turns?

It does have a real story for longer work: sandbox agents, sessions, interruptions, resume state, and tool execution environments. That is more than most trendy agent repos can say.

### Where would I start reading if I wanted to fork or borrow ideas?

Read in this order:

1. [`README.md`](https://github.com/openai/openai-agents-python/blob/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/README.md)
2. [`src/agents/agent.py`](https://github.com/openai/openai-agents-python/blob/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/agent.py)
3. [`src/agents/run.py`](https://github.com/openai/openai-agents-python/blob/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/run.py)
4. [`src/agents/tool.py`](https://github.com/openai/openai-agents-python/blob/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/tool.py)
5. [`src/agents/models/multi_provider.py`](https://github.com/openai/openai-agents-python/blob/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/models/multi_provider.py)
6. [`src/agents/sandbox/runtime.py`](https://github.com/openai/openai-agents-python/blob/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/sandbox/runtime.py)

### What would likely hurt in production?

A few things:

- feature interaction complexity: sessions + approvals + sandbox + provider routing + tracing is a lot of state coupling
- framework gravity: once you buy into their abstractions, you probably keep buying more of them
- public simplicity may mask internal surprise costs when debugging edge cases
- giant all-in-one modules like [`tool.py`](https://github.com/openai/openai-agents-python/blob/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/tool.py) can become maintenance magnets

## What is smart

A few genuinely smart choices stand out:

- **Thin public facade, thick private engine.** The public API stays approachable while the messy orchestration logic is pushed into `run.py` + `run_internal`.
- **Treating runs as resumable state machines.** Interruptions, approvals, resumed runs, and session persistence are first-class instead of tacked on.
- **Tooling as a real subsystem.** They took tool semantics seriously enough to encode timeout policy, approval policy, hosted/local modes, namespaces, and schema rigor.
- **Operational memory before mystical memory.** The presence of practical session backends like [`SQLiteSession`](https://github.com/openai/openai-agents-python/blob/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/memory/sqlite_session.py) is a good sign.
- **Sandbox integration is lifecycle-aware.** [`SandboxRuntime`](https://github.com/openai/openai-agents-python/blob/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/sandbox/runtime.py) is wired into preparation, memory, cleanup, and resume metadata rather than being an isolated demo folder.

## What is flawed or weak

There are also clear risks:

- **Complexity creep is already here.** This is no longer a small SDK; it is a platform with a small-SDK costume.
- **Some files are too broad.** [`tool.py`](https://github.com/openai/openai-agents-python/blob/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/src/agents/tool.py) especially is carrying a lot of conceptual load.
- **OpenAI gravity remains strong.** Even with provider abstraction, the product center of mass is visibly OpenAI Responses / OpenAI runtime semantics.
- **More optionality means more edge cases.** The many extras in [`pyproject.toml`](https://github.com/openai/openai-agents-python/blob/4f3c8a5379c1b44527c9a0a159d20b46755f4eaf/pyproject.toml) are powerful, but each axis multiplies testing and support burden.

## What we can learn / steal

Things worth stealing:

- design the core around a **run loop/state machine**, not around prompt templates
- keep a **clean public import surface** even if internals are messy
- make **approval/interruption/resume** explicit in the architecture early
- treat tool execution as infrastructure: schema, timeouts, policies, context, provenance
- use repo structure to mirror product structure: `examples/`, `tests/`, and `docs/` should reflect the real subsystems
- offer practical persistence first; don’t jump straight to faux-magic memory branding

## How we could apply it

If we were building agent infrastructure ourselves, the transferable ideas are:

- build a minimal public surface like `Agent` + `Runner`, but keep a disciplined internal orchestration core
- separate **agent declaration** from **run execution** from **tool execution** from **execution environments**
- make approvals and resumability first-class if tools can do anything non-trivial
- expose provider routing deliberately instead of hiding string hacks in config
- treat tracing as part of the product, not as observability garnish added later

The thing I would *not* copy blindly is the breadth. If we only need one narrow workflow, reproducing this whole architecture would be overkill.

## Bottom line

`openai/openai-agents-python` is interesting because it is one of the clearer examples of an agent framework growing up from demo-ware into runtime software.

The repo’s key insight is that the real product is not the `Agent` object — it is the orchestration machinery around turns, tools, interruptions, sessions, and execution environments. The public API is the tip. The real value is the state machine under it.

That makes it worth studying. It also makes it more dangerous to underestimate. If you adopt it, you are not adopting a helper library. You are adopting a workflow runtime.
