# Cua

- Repo: `trycua/cua`
- URL: https://github.com/trycua/cua
- Date: 2026-05-13
- Repo snapshot studied: `main` @ `041916daffebf04ef7ab873f3ebbecfddb913837`
- Why picked today: It is hot right now, AI-native, and more ambitious than a thin agent wrapper. The interesting part is not just “computer use”, it is that they are trying to own the whole stack: runtime, transport, agent loop, benchmark, local virtualization, and MCP-facing tooling.

## Executive summary
Cua is a serious computer-use monorepo, not a single SDK. It bundles cloud and local sandboxes, agent loops, computer-control interfaces, a benchmark harness, a macOS background driver, local Apple-virtualization tooling, a desktop-oriented multi-agent wrapper, and parallel TypeScript/Python SDK surfaces. The repo is trying to be the infrastructure layer for agents that operate full desktops instead of text-only tools.

The strongest idea here is vertical integration. Instead of saying “bring your own VM, benchmark, agent loop, and control substrate”, Cua packages all of them into one system. That makes the repo broader than many “agent” projects, but it also gives them leverage: benchmarks can assume their environment model, agents can assume their computer abstraction, and local/cloud runtimes can present nearly the same API.

## What they built
They built a multi-product monorepo for computer-use agents:

- a unified sandbox SDK for cloud and local environments in [`libs/python/cua-sandbox`](https://github.com/trycua/cua/tree/main/libs/python/cua-sandbox)
- agent orchestration and model-specific loops in [`libs/python/agent`](https://github.com/trycua/cua/tree/main/libs/python/agent)
- low-level computer abstractions in [`libs/python/computer`](https://github.com/trycua/cua/tree/main/libs/python/computer)
- benchmark and training-oriented environments in [`libs/cua-bench`](https://github.com/trycua/cua/tree/main/libs/cua-bench)
- a background macOS computer-use driver in [`libs/cua-driver`](https://github.com/trycua/cua/tree/main/libs/cua-driver)
- Apple Silicon VM management in [`libs/lume`](https://github.com/trycua/cua/tree/main/libs/lume)
- a user-facing multi-agent sandbox launcher in [`libs/cuabot`](https://github.com/trycua/cua/tree/main/libs/cuabot)
- mirrored TypeScript SDKs in [`libs/typescript`](https://github.com/trycua/cua/tree/main/libs/typescript)
- documentation, examples, notebooks, and release plumbing across the repo root and [`docs`](https://github.com/trycua/cua/tree/main/docs)

## Why it matters
Most computer-use repos focus on one slice: model prompting, a browser agent, a benchmark, or a desktop automation shim. Cua is notable because it treats computer-use as a systems problem. The repo assumes serious users need:

- heterogeneous runtimes, cloud and local
- multiple OS targets
- transport layers for screens, shell, input, and files
- model adapters and agent-loop variants
- benchmark environments with verifiable tasks
- local dev ergonomics and MCP integration

That is much more defensible than a prompt wrapper, but also much harder to keep coherent.

## Repo shape at a glance
At the top level, the repo splits into product libraries, docs/content, runnable examples, tests, and release machinery:

- [`README.md`](https://github.com/trycua/cua/blob/main/README.md) presents the repo as a product family, not a single package.
- [`pyproject.toml`](https://github.com/trycua/cua/blob/main/pyproject.toml) defines the Python workspace and shared dev/test dependencies.
- [`libs`](https://github.com/trycua/cua/tree/main/libs) is the real center of gravity.
- [`libs/python`](https://github.com/trycua/cua/tree/main/libs/python) contains the Python agent, sandbox, computer, MCP server, and related packages.
- [`libs/typescript`](https://github.com/trycua/cua/tree/main/libs/typescript) mirrors part of the surface area for JS/TS users.
- [`libs/cua-driver`](https://github.com/trycua/cua/tree/main/libs/cua-driver) and [`libs/lume`](https://github.com/trycua/cua/tree/main/libs/lume) are the more ambitious systems pieces, both Swift-heavy.
- [`libs/cua-bench`](https://github.com/trycua/cua/tree/main/libs/cua-bench) is its own substantial subsystem, not a side demo.
- [`docs`](https://github.com/trycua/cua/tree/main/docs) is a full docs app.
- [`examples`](https://github.com/trycua/cua/tree/main/examples) and [`notebooks`](https://github.com/trycua/cua/tree/main/notebooks) support onboarding and experiments.
- [`.github/workflows`](https://github.com/trycua/cua/tree/main/.github/workflows) shows package-by-package CI/CD, which reinforces that this is a constellation of products.

## Layered architecture dissection
### High-level system shape
The repo is organized like a vertical stack:

1. runtimes and virtualization create controllable machines or containers
2. transports expose those machines over HTTP, websocket, VNC, ADB, SSH, and related channels
3. computer abstractions normalize screen, mouse, keyboard, shell, clipboard, and window operations
4. agent loops call models and tools against those abstractions
5. benchmark and orchestration layers evaluate or deploy those flows at scale
6. MCP, CLI, and cuabot layers make the stack consumable by real agent clients

### Main layers
**Environment and runtime layer**

The core entry point is [`libs/python/cua-sandbox/cua_sandbox/sandbox.py`](https://github.com/trycua/cua/blob/main/libs/python/cua-sandbox/cua_sandbox/sandbox.py). It exposes one `Sandbox` abstraction while hiding runtime selection and lifecycle details. The `_auto_runtime` logic routes across Docker, QEMU, Lume, Android emulator, and Hyper-V depending on image type and host constraints.

That layer fans into runtime implementations under [`libs/python/cua-sandbox/cua_sandbox/runtime`](https://github.com/trycua/cua/tree/main/libs/python/cua-sandbox/cua_sandbox/runtime), where the repo encodes its opinionated answer to “where should this machine actually run?”

**Transport layer**

Below the friendly sandbox API, transports in [`libs/python/cua-sandbox/cua_sandbox/transport`](https://github.com/trycua/cua/tree/main/libs/python/cua-sandbox/cua_sandbox/transport) handle the ugly connectivity details. The existence of cloud, HTTP, websocket, VNC, SSH, QMP, ADB, and emulator-specific transports tells you the real product is not the `Sandbox` class, it is the normalization of many control planes into one interface.

**Computer-control layer**

[`libs/python/computer`](https://github.com/trycua/cua/tree/main/libs/python/computer) turns those transports into higher-level computer semantics. The OS-specific interface split in [`libs/python/computer/computer/interface`](https://github.com/trycua/cua/tree/main/libs/python/computer/computer/interface) is a good sign. They are not pretending Linux, macOS, Windows, and Android have the same primitives.

**Agent layer**

[`libs/python/agent/cua_agent/agent.py`](https://github.com/trycua/cua/blob/main/libs/python/agent/cua_agent/agent.py) is the top-level orchestration point for model-backed agents. The repo then breaks model behavior into loop implementations under [`libs/python/agent/cua_agent/loops`](https://github.com/trycua/cua/tree/main/libs/python/agent/cua_agent/loops). This is one of the most revealing choices in the repo: instead of one “universal” agent loop, they maintain many model-specific or strategy-specific loops.

That is practical and slightly worrying at the same time. Practical because vision-computer models do differ. Worrying because loop sprawl can become the maintenance tax that eventually bends the whole architecture.

**Benchmark layer**

[`libs/cua-bench/cua_bench`](https://github.com/trycua/cua/tree/main/libs/cua-bench/cua_bench) is not just a score runner. It includes agents, apps, sessions, workers, a CLI, processors, training pieces, and a static web dashboard. That means Cua sees benchmark infra as a first-class product and likely uses it as both evaluation harness and data/trajectory pipeline.

**Local desktop and virtualization layer**

Two subsystems stand out:

- [`libs/cua-driver`](https://github.com/trycua/cua/tree/main/libs/cua-driver), a macOS background driver with CLI and MCP server entry points
- [`libs/lume`](https://github.com/trycua/cua/tree/main/libs/lume), which manages macOS/Linux VMs on Apple Silicon and includes server, VNC, SSH, unattended install, and virtualization modules

These are the parts that make the repo feel more like infra than demoware.

### Request / data / control flow
A typical control flow looks like this:

1. a caller creates or connects to a sandbox via [`Sandbox` in `sandbox.py`](https://github.com/trycua/cua/blob/main/libs/python/cua-sandbox/cua_sandbox/sandbox.py)
2. the sandbox picks a runtime from [`cua_sandbox/runtime`](https://github.com/trycua/cua/tree/main/libs/python/cua-sandbox/cua_sandbox/runtime)
3. the runtime exposes a control surface through a transport in [`cua_sandbox/transport`](https://github.com/trycua/cua/tree/main/libs/python/cua-sandbox/cua_sandbox/transport)
4. higher-level computer interfaces in [`computer/interface`](https://github.com/trycua/cua/tree/main/libs/python/computer/computer/interface) translate that into OS-aware actions
5. [`ComputerAgent`](https://github.com/trycua/cua/blob/main/libs/python/agent/cua_agent/agent.py) selects a model loop from [`cua_agent/loops`](https://github.com/trycua/cua/tree/main/libs/python/agent/cua_agent/loops), executes tool calls, and records telemetry/callbacks/trajectory state
6. benchmark or client-facing surfaces like [`cua_bench/cli/main.py`](https://github.com/trycua/cua/blob/main/libs/cua-bench/cua_bench/cli/main.py), [`mcp_server/server.py`](https://github.com/trycua/cua/blob/main/libs/python/mcp-server/mcp_server/server.py), or [`cuabot/src/cuabot.tsx`](https://github.com/trycua/cua/blob/main/libs/cuabot/src/cuabot.tsx) wrap the stack for end users or automation workflows

## Key directories and files
- [`libs/python/cua-sandbox/cua_sandbox/sandbox.py`](https://github.com/trycua/cua/blob/main/libs/python/cua-sandbox/cua_sandbox/sandbox.py): the cleanest single file for understanding their abstraction strategy.
- [`libs/python/cua-sandbox/cua_sandbox/runtime`](https://github.com/trycua/cua/tree/main/libs/python/cua-sandbox/cua_sandbox/runtime): runtime selection and local/cloud execution backends.
- [`libs/python/cua-sandbox/cua_sandbox/transport`](https://github.com/trycua/cua/tree/main/libs/python/cua-sandbox/cua_sandbox/transport): the interoperability plumbing.
- [`libs/python/computer/computer/interface`](https://github.com/trycua/cua/tree/main/libs/python/computer/computer/interface): OS-specific computer surfaces.
- [`libs/python/agent/cua_agent/agent.py`](https://github.com/trycua/cua/blob/main/libs/python/agent/cua_agent/agent.py): main agent orchestration.
- [`libs/python/agent/cua_agent/loops`](https://github.com/trycua/cua/tree/main/libs/python/agent/cua_agent/loops): where model strategy differences accumulate.
- [`libs/python/mcp-server/mcp_server/server.py`](https://github.com/trycua/cua/blob/main/libs/python/mcp-server/mcp_server/server.py) and [`libs/python/mcp-server/mcp_server/session_manager.py`](https://github.com/trycua/cua/blob/main/libs/python/mcp-server/mcp_server/session_manager.py): MCP-facing server and session lifecycle.
- [`libs/cua-bench/cua_bench`](https://github.com/trycua/cua/tree/main/libs/cua-bench/cua_bench): benchmark engine, workers, apps, sessions, and dashboard pieces.
- [`libs/cua-driver/Sources`](https://github.com/trycua/cua/tree/main/libs/cua-driver/Sources): Swift code for CLI, server, recording, permissions, focus, capture, and window/input control.
- [`libs/lume/src`](https://github.com/trycua/cua/tree/main/libs/lume/src): the Apple virtualization and VM-management heart of the project.
- [`libs/cuabot/src`](https://github.com/trycua/cua/tree/main/libs/cuabot/src): the “make this usable by working agent people” wrapper.
- [`.github/workflows`](https://github.com/trycua/cua/tree/main/.github/workflows): evidence of separate release trains for Python, TypeScript, Swift, and container artifacts.

## Important components
**`Sandbox` as the contract boundary**

The repo’s most important design move is the contract in [`sandbox.py`](https://github.com/trycua/cua/blob/main/libs/python/cua-sandbox/cua_sandbox/sandbox.py). Users code against `screen`, `mouse`, `keyboard`, `shell`, `window`, `terminal`, and similar interfaces, while the implementation swaps runtimes and transports under the hood.

**Per-model agent loops**

The loop catalog in [`cua_agent/loops`](https://github.com/trycua/cua/tree/main/libs/python/agent/cua_agent/loops) suggests they do not believe one generic planner is enough. That is a solid engineering instinct for this domain, because model quirks matter a lot in tool-calling and screenshot-grounded behavior.

**Benchmark worker/session infrastructure**

The density of modules in [`cua_bench/workers`](https://github.com/trycua/cua/tree/main/libs/cua-bench/cua_bench/workers), [`cua_bench/sessions`](https://github.com/trycua/cua/tree/main/libs/cua-bench/cua_bench/sessions), and [`cua_bench/runner`](https://github.com/trycua/cua/tree/main/libs/cua-bench/cua_bench/runner) shows they care about parallel evaluation infrastructure, not just single-task demos.

**macOS-native control path**

[`libs/cua-driver/Sources/CuaDriverCore`](https://github.com/trycua/cua/tree/main/libs/cua-driver/Sources/CuaDriverCore) is one of the most strategically interesting directories in the repo. It breaks into capture, input, windows, cursor, focus, permissions, recording, and browser-related functionality. That decomposition looks like real product pressure, especially for background control without stealing focus.

**Lume as the local substrate**

[`libs/lume/src`](https://github.com/trycua/cua/tree/main/libs/lume/src) includes commands, VM abstractions, virtualization services, VNC, SSH, server handlers, unattended setup, and registry/image management. This is not a toy helper. It is the local infra engine that makes the rest of the stack feel vertically integrated on Apple hardware.

## Important knobs / configs / extension points
- [`pyproject.toml`](https://github.com/trycua/cua/blob/main/pyproject.toml) shows the shared Python workspace and package boundaries.
- Runtime choice is a major knob inside [`cua_sandbox/runtime`](https://github.com/trycua/cua/tree/main/libs/python/cua-sandbox/cua_sandbox/runtime), especially Docker vs QEMU vs Lume vs Android emulator vs Hyper-V.
- Image choice is another structural knob through [`libs/python/cua-sandbox/cua_sandbox/image.py`](https://github.com/trycua/cua/blob/main/libs/python/cua-sandbox/cua_sandbox/image.py).
- Model behavior is extensible through the loop families in [`cua_agent/loops`](https://github.com/trycua/cua/tree/main/libs/python/agent/cua_agent/loops).
- MCP integration and session shape live in [`libs/python/mcp-server`](https://github.com/trycua/cua/tree/main/libs/python/mcp-server).
- Release and packaging boundaries are encoded heavily in [`.github/workflows`](https://github.com/trycua/cua/tree/main/.github/workflows), which is effectively an operational architecture diagram.

## Practical questions and answers
**Q: Is this mostly an agent framework?**  
No. It is really an infrastructure stack with an agent framework inside it.

**Q: What is the repo’s actual moat?**  
The moat is not prompting. It is the shared abstraction across cloud sandboxes, local VMs, native desktop control, benchmarks, and MCP/client entry points.

**Q: What feels hardest to replicate?**  
The combination of [`cua-driver`](https://github.com/trycua/cua/tree/main/libs/cua-driver), [`lume`](https://github.com/trycua/cua/tree/main/libs/lume), and the transport/runtime normalization in [`cua-sandbox`](https://github.com/trycua/cua/tree/main/libs/python/cua-sandbox).

**Q: Where is this likely to fail in production?**  
At the seams: OS drift, model-specific breakage, virtualization edge cases, focus/capture weirdness, transport retries, and keeping benchmark tasks representative rather than overfit to their own stack.

**Q: Is the monorepo breadth a strength or a liability?**  
Both. It creates product coherence and leverage, but it also risks spreading the team thin across Python, TypeScript, Swift, docs, infra, and benchmarks.

**Q: What would I inspect next if I were integrating it?**  
I would go straight to [`sandbox.py`](https://github.com/trycua/cua/blob/main/libs/python/cua-sandbox/cua_sandbox/sandbox.py), [`cua_agent/agent.py`](https://github.com/trycua/cua/blob/main/libs/python/agent/cua_agent/agent.py), [`mcp_server/server.py`](https://github.com/trycua/cua/blob/main/libs/python/mcp-server/mcp_server/server.py), and the runtime/transport subtrees.

## What is smart
- The repo uses one clean user-facing sandbox abstraction while accepting ugly backend diversity.
- The product split inside [`README.md`](https://github.com/trycua/cua/blob/main/README.md) is honest about the system being a family of tools, not one overloaded SDK.
- The benchmark subsystem is treated as product infrastructure instead of marketing garnish.
- The separate Swift systems work in [`cua-driver`](https://github.com/trycua/cua/tree/main/libs/cua-driver) and [`lume`](https://github.com/trycua/cua/tree/main/libs/lume) makes the repo feel technically grounded.
- The release workflow fanout in [`.github/workflows`](https://github.com/trycua/cua/tree/main/.github/workflows) matches the repo’s real package boundaries.

## What is flawed or weak
- The scope is huge, and huge scope is itself a bug source.
- The repo surface is broad enough that discoverability will be hard for newcomers, even with good docs.
- Model-specific loop proliferation in [`cua_agent/loops`](https://github.com/trycua/cua/tree/main/libs/python/agent/cua_agent/loops) could become a long-term entropy machine.
- Vertical integration can make benchmarks suspiciously aligned with the house stack unless they fight that bias hard.
- The strongest pieces, especially the Apple-native ones, may also be the hardest to keep portable and robust.

## What we can learn / steal
- Treat computer-use as a stack problem, not just a model prompt problem.
- Put a stable contract at the top, then hide runtime and transport mess underneath.
- Make evaluation infrastructure a first-class subsystem if you want the product to improve credibly.
- Keep OS-specific control code structurally explicit instead of flattening everything into fake uniformity.
- Use monorepo boundaries to reflect product boundaries, then mirror them in CI/CD.

## How we could apply it
If we were building our own agent execution stack, the most reusable pattern here is:

1. define one durable “computer” contract for screen/input/shell/files
2. let runtime backends compete underneath it
3. isolate model quirks in loop adapters instead of smearing conditionals everywhere
4. make benchmarks and trajectory capture part of the core system, not an afterthought

The more opinionated extension is their local substrate strategy. Owning a native driver plus a VM manager is expensive, but it gives much tighter control than bolting onto generic browser automation forever.

## Bottom line
Cua is one of the more substantial computer-use repos on GitHub right now because it is building infrastructure, not just demos. The repo’s key insight is that agents that use computers need a full stack: runtimes, transports, abstractions, loops, benchmarks, and deployment surfaces. That breadth is exactly what makes the project impressive, and exactly what could make it brittle if the team cannot keep the layers coherent.
