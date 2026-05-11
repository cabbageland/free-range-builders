# Hermes Agent

- Repo: `NousResearch/hermes-agent`
- URL: https://github.com/NousResearch/hermes-agent
- Date: 2026-05-11
- Repo snapshot studied: `main` @ `e155f2aca9dc9135141d37d3aade060a9a02e470`
- Why picked today: It is extremely hot right now, clearly popular, AI-native, and more interesting than the usual wrapper repo because it is trying to unify agent runtime, messaging gateway, memory, cron, ACP, and RL/eval infrastructure in one codebase.

## Executive summary
Hermes Agent is not just “an AI assistant.” It is a packaging strategy for a persistent agent system: one codebase that can act as a terminal UI, a messaging bot gateway, a protocol server for editor integrations, a cron runner, and a research environment for tool-using agents.

The impressive part is not the chat loop itself. The impressive part is that the repo keeps turning “agent features” into first-class runtime surfaces: memory management, platform delivery, approval flow, tool routing, model/provider abstraction, session continuity, and even Atropos-style training environments.

The main risk is ambition creep. This repo spans product UX, ops, protocol compatibility, platform integrations, and research tooling. That gives it leverage, but also a lot of blast radius.

## What they built
They built a multi-surface agent platform that can be used through:
- a local terminal UI via [`cli.py`](https://github.com/NousResearch/hermes-agent/blob/main/cli.py)
- a messaging gateway via [`gateway/`](https://github.com/NousResearch/hermes-agent/tree/main/gateway)
- an Agent Client Protocol server via [`acp_adapter/`](https://github.com/NousResearch/hermes-agent/tree/main/acp_adapter)
- scheduled automations via [`cron/`](https://github.com/NousResearch/hermes-agent/tree/main/cron)
- RL/eval environments via [`environments/`](https://github.com/NousResearch/hermes-agent/tree/main/environments)

Underneath that, the same agent runtime shares memory, tool execution, model transport layers, and session machinery.

## Why it matters
Most agent repos are thin shells around “prompt + tools + loop.” Hermes is more serious about the surrounding operating system for the agent.

The key idea is that persistence and reach matter as much as raw model quality. Hermes tries to make the same agent available in terminal, chat platforms, editor/protocol contexts, and unattended scheduled workflows, without rebuilding the stack each time.

## Repo shape at a glance
Top-level structure, roughly by role:

- [`agent/`](https://github.com/NousResearch/hermes-agent/tree/main/agent): core runtime concerns, memory, adapters, prompt building, rate limiting, safety, model metadata, transports
- [`gateway/`](https://github.com/NousResearch/hermes-agent/tree/main/gateway): long-running messaging gateway, session handling, platform registry, delivery, pairing, status
- [`gateway/platforms/`](https://github.com/NousResearch/hermes-agent/tree/main/gateway/platforms): concrete chat integrations for Slack, Discord, Telegram, Signal, WhatsApp, Matrix, and others
- [`hermes_cli/`](https://github.com/NousResearch/hermes-agent/tree/main/hermes_cli): CLI commands, config UX, TUI support, setup, diagnostics, gateway control
- [`acp_adapter/`](https://github.com/NousResearch/hermes-agent/tree/main/acp_adapter): ACP server surface for editor/client integrations
- [`cron/`](https://github.com/NousResearch/hermes-agent/tree/main/cron): scheduler, jobs, delivery plumbing for unattended runs
- [`environments/`](https://github.com/NousResearch/hermes-agent/tree/main/environments): Atropos integration, eval/training environments, tool-call parsers
- [`docs/`](https://github.com/NousResearch/hermes-agent/tree/main/docs): docs and design material
- [`docker/`](https://github.com/NousResearch/hermes-agent/tree/main/docker) and [`Dockerfile`](https://github.com/NousResearch/hermes-agent/blob/main/Dockerfile): container packaging
- [`pyproject.toml`](https://github.com/NousResearch/hermes-agent/blob/main/pyproject.toml): dependency and extras map, which is unusually revealing because it shows the product strategy directly

This is a broad monorepo, but it is broad in a coherent way: every major directory corresponds to a runtime surface or a system layer.

## Layered architecture dissection
### High-level system shape
Hermes looks like a layered system built around one central idea: the agent runtime should stay stable while input/output surfaces multiply.

At the center is the agent runtime in [`agent/`](https://github.com/NousResearch/hermes-agent/tree/main/agent). Around it are interface shells:
- terminal shell: [`cli.py`](https://github.com/NousResearch/hermes-agent/blob/main/cli.py) and [`hermes_cli/`](https://github.com/NousResearch/hermes-agent/tree/main/hermes_cli)
- messaging shell: [`gateway/run.py`](https://github.com/NousResearch/hermes-agent/blob/main/gateway/run.py) plus [`gateway/platforms/`](https://github.com/NousResearch/hermes-agent/tree/main/gateway/platforms)
- protocol shell: [`acp_adapter/server.py`](https://github.com/NousResearch/hermes-agent/blob/main/acp_adapter/server.py)
- scheduler shell: [`cron/scheduler.py`](https://github.com/NousResearch/hermes-agent/blob/main/cron/scheduler.py)
- research shell: [`environments/README.md`](https://github.com/NousResearch/hermes-agent/blob/main/environments/README.md) and the environment implementations

### Main layers
**1. Product entrypoint layer**
- [`cli.py`](https://github.com/NousResearch/hermes-agent/blob/main/cli.py) is the huge interactive terminal entrypoint.
- [`hermes_cli/main.py`](https://github.com/NousResearch/hermes-agent/blob/main/hermes_cli/main.py) and neighboring modules package setup, commands, config, auth, diagnostics, and gateway operations.

This layer is about human usability, not model logic.

**2. Core runtime layer**
- [`agent/`](https://github.com/NousResearch/hermes-agent/tree/main/agent) contains the reusable internals: memory, prompt assembly, provider adapters, context compression, safety checks, pricing, retry logic, and transport abstractions.
- [`agent/transports/`](https://github.com/NousResearch/hermes-agent/tree/main/agent/transports) is important because it suggests they want one internal interface across multiple provider APIs.

**3. Persistence and learning layer**
- [`agent/memory_manager.py`](https://github.com/NousResearch/hermes-agent/blob/main/agent/memory_manager.py) orchestrates memory providers and explicitly fences recalled memory so it is treated as reference context rather than new user input.
- The memory layer is one of the repo’s real differentiators because it is treated as infrastructure, not a gimmick bolted onto prompts.

**4. Interface and delivery layer**
- [`gateway/run.py`](https://github.com/NousResearch/hermes-agent/blob/main/gateway/run.py) is the long-lived messaging process.
- [`gateway/platforms/slack.py`](https://github.com/NousResearch/hermes-agent/blob/main/gateway/platforms/slack.py), [`gateway/platforms/discord.py`](https://github.com/NousResearch/hermes-agent/blob/main/gateway/platforms/discord.py), and peers implement per-platform glue.
- This layer handles durability problems that many agent demos avoid: reconnects, session replay, delivery, home channels, and platform-specific behavior.

**5. Automation layer**
- [`cron/scheduler.py`](https://github.com/NousResearch/hermes-agent/blob/main/cron/scheduler.py) turns the agent into a scheduled worker.
- This matters because it changes the product from reactive chat assistant into proactive background system.

**6. Protocol and ecosystem layer**
- [`acp_adapter/server.py`](https://github.com/NousResearch/hermes-agent/blob/main/acp_adapter/server.py) exposes the agent through ACP.
- This is strategically smart because it lets Hermes live inside external tools instead of demanding that every user adopt Hermes-native UX.

**7. Research/training layer**
- [`environments/hermes_base_env.py`](https://github.com/NousResearch/hermes-agent/blob/main/environments/hermes_base_env.py), [`environments/agent_loop.py`](https://github.com/NousResearch/hermes-agent/blob/main/environments/agent_loop.py), and [`environments/tool_context.py`](https://github.com/NousResearch/hermes-agent/blob/main/environments/tool_context.py) connect the same tool-using runtime to eval and RL flows.
- This is unusual and interesting: product runtime and training/eval runtime are being kept close together.

### Request / data / control flow
At a high level the control flow looks like this:
1. A user or external client enters through CLI, gateway, cron, or ACP.
2. The interface layer normalizes that request into agent session state.
3. The runtime layer builds prompt/context, loads tools, and routes model traffic through transport adapters.
4. Tool calls execute against the enabled tool surface.
5. Memory and session state are updated.
6. Output is delivered back through the originating surface, or persisted for later continuation.

The most important architectural point is that Hermes is not organized around one UI. It is organized around shared sessionful agent execution.

## Key directories and files
- [`README.md`](https://github.com/NousResearch/hermes-agent/blob/main/README.md): product thesis and surface area summary
- [`pyproject.toml`](https://github.com/NousResearch/hermes-agent/blob/main/pyproject.toml): best quick scan for supported capabilities, optional extras, and platform ambitions
- [`cli.py`](https://github.com/NousResearch/hermes-agent/blob/main/cli.py): giant terminal entrypoint, shows how much UX and runtime policy is packed into the CLI
- [`agent/memory_manager.py`](https://github.com/NousResearch/hermes-agent/blob/main/agent/memory_manager.py): clean example of memory being formalized as a subsystem
- [`agent/transports/base.py`](https://github.com/NousResearch/hermes-agent/blob/main/agent/transports/base.py) and [`agent/transports/`](https://github.com/NousResearch/hermes-agent/tree/main/agent/transports): model API abstraction layer
- [`gateway/run.py`](https://github.com/NousResearch/hermes-agent/blob/main/gateway/run.py): central gateway lifecycle and replay logic
- [`gateway/platforms/`](https://github.com/NousResearch/hermes-agent/tree/main/gateway/platforms): the integration sprawl, but also a major source of product leverage
- [`cron/scheduler.py`](https://github.com/NousResearch/hermes-agent/blob/main/cron/scheduler.py): unattended execution and delivery logic
- [`acp_adapter/server.py`](https://github.com/NousResearch/hermes-agent/blob/main/acp_adapter/server.py): editor/protocol compatibility layer
- [`environments/README.md`](https://github.com/NousResearch/hermes-agent/blob/main/environments/README.md): the clearest explanation of the research/eval architecture

## Important components
- **CLI shell**: [`cli.py`](https://github.com/NousResearch/hermes-agent/blob/main/cli.py)
- **Gateway runtime**: [`gateway/run.py`](https://github.com/NousResearch/hermes-agent/blob/main/gateway/run.py)
- **Platform adapters**: [`gateway/platforms/`](https://github.com/NousResearch/hermes-agent/tree/main/gateway/platforms)
- **Memory orchestration**: [`agent/memory_manager.py`](https://github.com/NousResearch/hermes-agent/blob/main/agent/memory_manager.py)
- **Transport abstraction**: [`agent/transports/`](https://github.com/NousResearch/hermes-agent/tree/main/agent/transports)
- **ACP server**: [`acp_adapter/server.py`](https://github.com/NousResearch/hermes-agent/blob/main/acp_adapter/server.py)
- **Cron engine**: [`cron/scheduler.py`](https://github.com/NousResearch/hermes-agent/blob/main/cron/scheduler.py)
- **RL/eval harness**: [`environments/agent_loop.py`](https://github.com/NousResearch/hermes-agent/blob/main/environments/agent_loop.py) and [`environments/tool_context.py`](https://github.com/NousResearch/hermes-agent/blob/main/environments/tool_context.py)

## Important knobs / configs / extension points
- Dependency extras in [`pyproject.toml`](https://github.com/NousResearch/hermes-agent/blob/main/pyproject.toml) are effectively feature flags for surfaces like messaging, slack, pty, ACP, voice, web, bedrock, and RL.
- Platform integrations are extensible through [`gateway/platforms/`](https://github.com/NousResearch/hermes-agent/tree/main/gateway/platforms) and registry logic in the gateway layer.
- Memory is pluggable, but deliberately constrained in [`agent/memory_manager.py`](https://github.com/NousResearch/hermes-agent/blob/main/agent/memory_manager.py) to avoid provider conflicts.
- Cron tool availability is configurable in [`cron/scheduler.py`](https://github.com/NousResearch/hermes-agent/blob/main/cron/scheduler.py), which is a subtle but important cost/safety control.
- ACP support in [`acp_adapter/`](https://github.com/NousResearch/hermes-agent/tree/main/acp_adapter) is a strong extension point for editor and client integrations.

## Practical questions and answers
**What is Hermes actually optimizing for?**
A persistent agent that can move across interfaces and keep working, not just a nice one-shot terminal assistant.

**Where is the real engineering weight?**
Not in a novel prompting trick. It is in orchestration: session continuity, provider abstraction, platform delivery, tool execution, and memory containment.

**What would fail first in production?**
The integration perimeter. Multi-platform messaging, protocol compatibility, auth flows, and long-lived gateway correctness are where complexity compounds fast.

**Is the learning story real or marketing?**
More real than usual, because memory and skill infrastructure appear to be represented in code structure, not only README claims. But “self-improving agent” is still a broad promise, and the hard part is quality control, not feature existence.

**Why is the RL/eval layer notable?**
Because it suggests the team wants one continuous stack from product runtime to training loop, which can tighten feedback but also couples research concerns to shipping software.

## What is smart
- The repo is organized around durable runtime surfaces, not just demo UX.
- [`pyproject.toml`](https://github.com/NousResearch/hermes-agent/blob/main/pyproject.toml) shows disciplined modularization through extras instead of pretending every install needs every capability.
- [`agent/memory_manager.py`](https://github.com/NousResearch/hermes-agent/blob/main/agent/memory_manager.py) is careful about fencing recalled memory, which is exactly the kind of subtle failure mode many memory-enabled agents ignore.
- [`cron/scheduler.py`](https://github.com/NousResearch/hermes-agent/blob/main/cron/scheduler.py) shows they understand that unattended agents need operational controls, not just prompts.
- The ACP layer is strategically excellent. It gives Hermes a route into other products and editors without rebuilding the core agent.

## What is flawed or weak
- The codebase is sprawling. Breadth is a feature here, but it also raises maintenance burden substantially.
- [`cli.py`](https://github.com/NousResearch/hermes-agent/blob/main/cli.py) is enormous, which usually means real-world product pressure has outgrown the original abstraction boundaries.
- A repo that promises terminal UX, messaging gateway, memory, skills, cron, protocol serving, and RL environments risks becoming a pile of partially-coupled subsystems unless constant refactoring discipline is maintained.
- The product thesis depends on many external providers and platform APIs. That means the long-term pain is likely in breakage management, not core model calls.

## What we can learn / steal
- Treat memory as a subsystem with explicit containment rules, not as a bag of retrieved text.
- Build one strong sessionful runtime, then attach multiple delivery surfaces to it.
- Make unattended automation a first-class product layer instead of an afterthought.
- Use dependency extras and directory boundaries to mirror product capability boundaries.
- If you want agents to live in editors and other tools, protocol support is more strategic than another chat UI.

## How we could apply it
If we were building our own agent stack, the big reusable idea is this: optimize for runtime portability, not just model portability.

Concretely:
- one shared session/runtime core
- separate shell layers for CLI, messaging, protocol, and scheduled work
- explicit memory fencing
- strong tool gating per surface
- a narrow transport abstraction for provider churn

That is a much better pattern than building four separate “assistant” products that all duplicate the same brittle loop.

## Bottom line
Hermes Agent is interesting because it is trying to be an agent operating system, not just a chatbot wrapper.

The key insight is that its real product is the shared runtime sitting underneath terminal, gateway, ACP, cron, and research flows. If that runtime stays coherent, this repo has real leverage. If it does not, the same breadth becomes the liability.