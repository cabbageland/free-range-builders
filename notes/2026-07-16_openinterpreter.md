# Open Interpreter

- Repo: `openinterpreter/openinterpreter`
- URL: https://github.com/openinterpreter/openinterpreter
- Date: 2026-07-16
- Repo snapshot studied: `main` @ `be37756b53f91401e13019ffce41c02a0682cd89`
- Why picked today: It was one of the current GitHub trending repos when checked, but the real reason to study it is that this is not the old Python "let the model run shell commands" project anymore. It is a very large Rust fork of Codex that is explicitly trying to squeeze better coding-agent behavior out of cheaper providers by routing each model through a chosen harness and transport shape.

## Executive summary
Open Interpreter is now best understood as a product fork of Codex rather than a clean-sheet agent. The public story in [`README.md`](https://github.com/openinterpreter/openinterpreter/blob/be37756b53f91401e13019ffce41c02a0682cd89/README.md) is blunt about it: this is the new Rust version, focused on harness emulation for low-cost models. The repo shape confirms that claim. [`codex-cli/bin/codex.js`](https://github.com/openinterpreter/openinterpreter/blob/be37756b53f91401e13019ffce41c02a0682cd89/codex-cli/bin/codex.js) is just a platform launcher, [`codex-rs/cli/src/main.rs`](https://github.com/openinterpreter/openinterpreter/blob/be37756b53f91401e13019ffce41c02a0682cd89/codex-rs/cli/src/main.rs) is the native command router, and the real product lives in the giant Rust workspace declared in [`codex-rs/Cargo.toml`](https://github.com/openinterpreter/openinterpreter/blob/be37756b53f91401e13019ffce41c02a0682cd89/codex-rs/Cargo.toml).

The most important systems idea is not "support many models." It is "reshape the same agent core into different tool-harness dialects." [`codex-rs/model-provider-info/src/lib.rs`](https://github.com/openinterpreter/openinterpreter/blob/be37756b53f91401e13019ffce41c02a0682cd89/codex-rs/model-provider-info/src/lib.rs) chooses default harnesses from provider/model identity, and [`codex-rs/core/src/harness/routing.rs`](https://github.com/openinterpreter/openinterpreter/blob/be37756b53f91401e13019ffce41c02a0682cd89/codex-rs/core/src/harness/routing.rs) decides whether a turn should run through native Responses, chat-completions compatibility, Messages-native Claude shaping, or a harness-specific chat adapter. That is the repo's real bet: performance comes as much from prompt/tool/transport shape as from the model itself.

The caution is that this leverage comes with a huge inheritance burden. The package metadata in [`codex-cli/package.json`](https://github.com/openinterpreter/openinterpreter/blob/be37756b53f91401e13019ffce41c02a0682cd89/codex-cli/package.json) still points at `@openai/codex`, the workspace has well over a hundred crates, and the fork now has to track upstream architectural churn while also maintaining its own harness opinions and product identity.

## What they built
They built a multi-surface local coding-agent stack:

- [`codex-cli/`](https://github.com/openinterpreter/openinterpreter/tree/be37756b53f91401e13019ffce41c02a0682cd89/codex-cli) is the npm-distributed launcher layer.
- [`codex-rs/cli`](https://github.com/openinterpreter/openinterpreter/tree/be37756b53f91401e13019ffce41c02a0682cd89/codex-rs/cli) is the native entrypoint for interactive TUI, `exec`, review, MCP, plugin, sandbox, resume, and cloud-task flows.
- [`codex-rs/core`](https://github.com/openinterpreter/openinterpreter/tree/be37756b53f91401e13019ffce41c02a0682cd89/codex-rs/core) is the real engine: threads, sessions, prompts, sandboxing, tools, skills, web search, rollout recording, and unified exec.
- [`codex-rs/model-provider-info`](https://github.com/openinterpreter/openinterpreter/tree/be37756b53f91401e13019ffce41c02a0682cd89/codex-rs/model-provider-info) maps providers onto wire protocols and recommended harnesses.
- [`codex-rs/core/src/harness`](https://github.com/openinterpreter/openinterpreter/tree/be37756b53f91401e13019ffce41c02a0682cd89/codex-rs/core/src/harness) carries the harness-specific request shaping and prompt assets.
- [`codex-rs/collaboration-mode-templates`](https://github.com/openinterpreter/openinterpreter/tree/be37756b53f91401e13019ffce41c02a0682cd89/codex-rs/collaboration-mode-templates) adds plan / execute / pair-programming collaboration overlays.

## Why it matters
This repo matters because it treats agent quality as a routing problem instead of only a model-selection problem.

1. It assumes many providers are good enough if you hand them the right harness.
2. It keeps the expensive product shell from being duplicated per provider by centralizing it in one core workspace.
3. It exposes a practical builder lesson: transport compatibility, tool schema shape, and system-prompt dialect often matter more than benchmark bragging.

## Repo shape at a glance
The top of the repo already reveals the architecture:

- [`README.md`](https://github.com/openinterpreter/openinterpreter/blob/be37756b53f91401e13019ffce41c02a0682cd89/README.md) frames the product around harness switching, QA skill support, ACP mode, and local state.
- [`codex-cli/`](https://github.com/openinterpreter/openinterpreter/tree/be37756b53f91401e13019ffce41c02a0682cd89/codex-cli) is tiny, mostly packaging and launcher glue.
- [`codex-rs/Cargo.toml`](https://github.com/openinterpreter/openinterpreter/blob/be37756b53f91401e13019ffce41c02a0682cd89/codex-rs/Cargo.toml) is the true repo map, listing the CLI, TUI, core agent, app server, exec server, MCP, skills, connectors, sandboxing, plugin, memories, and provider crates.
- [`codex-rs/core/src/lib.rs`](https://github.com/openinterpreter/openinterpreter/blob/be37756b53f91401e13019ffce41c02a0682cd89/codex-rs/core/src/lib.rs) shows the core library's scope: agents, sessions, prompts, tools, sandboxing, state, skills, spawn, shell, rollout, and safety.
- [`codex-rs/core/src/harness/`](https://github.com/openinterpreter/openinterpreter/tree/be37756b53f91401e13019ffce41c02a0682cd89/codex-rs/core/src/harness) is a distinct subsystem rather than an incidental prompt file dump.

## Layered architecture dissection
### High-level system shape
The boot path is straightforward. [`codex-cli/bin/codex.js`](https://github.com/openinterpreter/openinterpreter/blob/be37756b53f91401e13019ffce41c02a0682cd89/codex-cli/bin/codex.js) resolves a platform package and spawns the native binary. [`codex-rs/cli/src/main.rs`](https://github.com/openinterpreter/openinterpreter/blob/be37756b53f91401e13019ffce41c02a0682cd89/codex-rs/cli/src/main.rs) then fans out into interactive TUI, headless exec, review, MCP server, app server, sandbox, login, and session-management flows. From there, almost everything converges on the shared library surface exported by [`codex-rs/core/src/lib.rs`](https://github.com/openinterpreter/openinterpreter/blob/be37756b53f91401e13019ffce41c02a0682cd89/codex-rs/core/src/lib.rs).

### Main layers
**1. Packaging layer**  
[`codex-cli/bin/codex.js`](https://github.com/openinterpreter/openinterpreter/blob/be37756b53f91401e13019ffce41c02a0682cd89/codex-cli/bin/codex.js) is a Node shim that finds the correct bundled native binary and forwards signals. The JavaScript layer is intentionally small.

**2. Command surface layer**  
[`codex-rs/cli/src/main.rs`](https://github.com/openinterpreter/openinterpreter/blob/be37756b53f91401e13019ffce41c02a0682cd89/codex-rs/cli/src/main.rs) defines the product surface: `exec`, review, login, MCP, plugin, ACP, app server, sandbox, apply, resume, archive, fork, and cloud.

**3. Core agent/runtime layer**  
[`codex-rs/core/src/lib.rs`](https://github.com/openinterpreter/openinterpreter/blob/be37756b53f91401e13019ffce41c02a0682cd89/codex-rs/core/src/lib.rs) pulls together the real machinery: sessions, prompt assembly, tool wiring, MCP, sandbox policy, state DB, skills, rollout recording, and spawning.

**4. Provider and harness-selection layer**  
[`codex-rs/model-provider-info/src/lib.rs`](https://github.com/openinterpreter/openinterpreter/blob/be37756b53f91401e13019ffce41c02a0682cd89/codex-rs/model-provider-info/src/lib.rs) chooses wire protocol and default harness from provider/model identity. Anthropic maps to `claude-code`, Qwen maps to `qwen-code`, DeepSeek defaults to `claude-code-bare`, and so on.

**5. Harness-routing layer**  
[`codex-rs/core/src/harness/routing.rs`](https://github.com/openinterpreter/openinterpreter/blob/be37756b53f91401e13019ffce41c02a0682cd89/codex-rs/core/src/harness/routing.rs) decides how a session is actually shaped on the wire: native Responses, Messages-native Claude/ZCode, chat-completions compatibility, or harness-specific chat shims like `minimal`, `qwen-code`, `deepseek-tui`, and `swe-agent`.

### Request / data / control flow
The most interesting flow is the "cheap model, stronger harness" path:

1. The user launches the product through [`bin/codex.js`](https://github.com/openinterpreter/openinterpreter/blob/be37756b53f91401e13019ffce41c02a0682cd89/codex-cli/bin/codex.js).
2. [`main.rs`](https://github.com/openinterpreter/openinterpreter/blob/be37756b53f91401e13019ffce41c02a0682cd89/codex-rs/cli/src/main.rs) chooses TUI or headless exec.
3. The session loads provider metadata from [`model-provider-info/src/lib.rs`](https://github.com/openinterpreter/openinterpreter/blob/be37756b53f91401e13019ffce41c02a0682cd89/codex-rs/model-provider-info/src/lib.rs) and picks a default harness.
4. [`tui/src/chatwidget/model_popups.rs`](https://github.com/openinterpreter/openinterpreter/blob/be37756b53f91401e13019ffce41c02a0682cd89/codex-rs/tui/src/chatwidget/model_popups.rs) exposes those harness choices explicitly in the UI.
5. [`core/src/harness/routing.rs`](https://github.com/openinterpreter/openinterpreter/blob/be37756b53f91401e13019ffce41c02a0682cd89/codex-rs/core/src/harness/routing.rs) resolves the transport route for the chosen provider and harness.
6. [`core/src/client.rs`](https://github.com/openinterpreter/openinterpreter/blob/be37756b53f91401e13019ffce41c02a0682cd89/codex-rs/core/src/client.rs) can then carry Claude-style shaping over `/chat/completions`, which is exactly how `claude-code-bare` can run against chat-only providers like DeepSeek.
7. For the simplest chat-harness path, [`core/src/harness/minimal.rs`](https://github.com/openinterpreter/openinterpreter/blob/be37756b53f91401e13019ffce41c02a0682cd89/codex-rs/core/src/harness/minimal.rs) builds a compact system prompt, chat messages, and tool list for cheaper models.

## Key directories and files
- [`README.md`](https://github.com/openinterpreter/openinterpreter/blob/be37756b53f91401e13019ffce41c02a0682cd89/README.md): the product framing and harness story.
- [`codex-cli/bin/codex.js`](https://github.com/openinterpreter/openinterpreter/blob/be37756b53f91401e13019ffce41c02a0682cd89/codex-cli/bin/codex.js): platform launcher and binary handoff.
- [`codex-rs/Cargo.toml`](https://github.com/openinterpreter/openinterpreter/blob/be37756b53f91401e13019ffce41c02a0682cd89/codex-rs/Cargo.toml): the real topology map.
- [`codex-rs/cli/src/main.rs`](https://github.com/openinterpreter/openinterpreter/blob/be37756b53f91401e13019ffce41c02a0682cd89/codex-rs/cli/src/main.rs): command and entrypoint surface.
- [`codex-rs/core/src/lib.rs`](https://github.com/openinterpreter/openinterpreter/blob/be37756b53f91401e13019ffce41c02a0682cd89/codex-rs/core/src/lib.rs): core runtime export surface.
- [`codex-rs/model-provider-info/src/lib.rs`](https://github.com/openinterpreter/openinterpreter/blob/be37756b53f91401e13019ffce41c02a0682cd89/codex-rs/model-provider-info/src/lib.rs): provider registry and default harness logic.
- [`codex-rs/core/src/harness/routing.rs`](https://github.com/openinterpreter/openinterpreter/blob/be37756b53f91401e13019ffce41c02a0682cd89/codex-rs/core/src/harness/routing.rs): transport-resolution brain.
- [`codex-rs/core/src/harness/minimal.rs`](https://github.com/openinterpreter/openinterpreter/blob/be37756b53f91401e13019ffce41c02a0682cd89/codex-rs/core/src/harness/minimal.rs): cheapest harness baseline.

## Important components
**Harness routing is the product's actual differentiator**  
The repo's value is concentrated in the harness subsystem, not in the launcher. [`routing.rs`](https://github.com/openinterpreter/openinterpreter/blob/be37756b53f91401e13019ffce41c02a0682cd89/codex-rs/core/src/harness/routing.rs) makes the provider/harness combination explicit and testable.

**Provider defaults encode product taste**  
[`default_harness_for_provider_model`](https://github.com/openinterpreter/openinterpreter/blob/be37756b53f91401e13019ffce41c02a0682cd89/codex-rs/model-provider-info/src/lib.rs) is where the repo quietly encodes its opinion that DeepSeek works best with `claude-code-bare`, Anthropic with `claude-code`, and Qwen with `qwen-code`.

**The TUI is part of the model-control plane**  
[`tui/src/chatwidget/model_popups.rs`](https://github.com/openinterpreter/openinterpreter/blob/be37756b53f91401e13019ffce41c02a0682cd89/codex-rs/tui/src/chatwidget/model_popups.rs) is not mere UX chrome. It exposes model, provider, reasoning, and harness selection as first-class control points.

## Important knobs / configs / extension points
- Provider definitions, wire protocol, retry behavior, and auth settings in [`model-provider-info/src/lib.rs`](https://github.com/openinterpreter/openinterpreter/blob/be37756b53f91401e13019ffce41c02a0682cd89/codex-rs/model-provider-info/src/lib.rs).
- Harness selection and recommendation text in [`tui/src/chatwidget/model_popups.rs`](https://github.com/openinterpreter/openinterpreter/blob/be37756b53f91401e13019ffce41c02a0682cd89/codex-rs/tui/src/chatwidget/model_popups.rs).
- Harness implementations and prompt assets in [`core/src/harness/`](https://github.com/openinterpreter/openinterpreter/tree/be37756b53f91401e13019ffce41c02a0682cd89/codex-rs/core/src/harness).
- Collaboration overlays in [`collaboration-mode-templates/templates/`](https://github.com/openinterpreter/openinterpreter/tree/be37756b53f91401e13019ffce41c02a0682cd89/codex-rs/collaboration-mode-templates/templates).

## Practical questions and answers
**Is this still the original Open Interpreter project?**  
Only in brand lineage. The current repo is explicitly the Rust Codex-derived version, as stated in [`README.md`](https://github.com/openinterpreter/openinterpreter/blob/be37756b53f91401e13019ffce41c02a0682cd89/README.md).

**What is the most reusable idea here?**  
Separate "provider wire protocol" from "agent harness shape." That split lets one agent core speak differently to Anthropic, DeepSeek, Qwen, or Kimi without cloning the whole product.

**Where should a builder start reading?**  
Start with [`README.md`](https://github.com/openinterpreter/openinterpreter/blob/be37756b53f91401e13019ffce41c02a0682cd89/README.md), then [`codex-rs/Cargo.toml`](https://github.com/openinterpreter/openinterpreter/blob/be37756b53f91401e13019ffce41c02a0682cd89/codex-rs/Cargo.toml), [`codex-rs/cli/src/main.rs`](https://github.com/openinterpreter/openinterpreter/blob/be37756b53f91401e13019ffce41c02a0682cd89/codex-rs/cli/src/main.rs), [`codex-rs/model-provider-info/src/lib.rs`](https://github.com/openinterpreter/openinterpreter/blob/be37756b53f91401e13019ffce41c02a0682cd89/codex-rs/model-provider-info/src/lib.rs), and [`codex-rs/core/src/harness/routing.rs`](https://github.com/openinterpreter/openinterpreter/blob/be37756b53f91401e13019ffce41c02a0682cd89/codex-rs/core/src/harness/routing.rs).

## What is smart
- Treating harness choice as a first-class systems knob instead of burying it in prompt text.
- Carrying Claude-style shaping across non-Responses transports in [`core/src/client.rs`](https://github.com/openinterpreter/openinterpreter/blob/be37756b53f91401e13019ffce41c02a0682cd89/codex-rs/core/src/client.rs).
- Keeping the JS package thin and putting almost all durable logic in Rust.
- Letting interactive UI explicitly expose provider, model, reasoning, and harness rather than hiding them behind one "auto" switch.

## What is flawed or weak
- The fork inherits a massive upstream monorepo surface, and [`codex-rs/Cargo.toml`](https://github.com/openinterpreter/openinterpreter/blob/be37756b53f91401e13019ffce41c02a0682cd89/codex-rs/Cargo.toml) makes that maintenance bill obvious.
- Branding and packaging are still visibly fork-shaped: [`codex-cli/package.json`](https://github.com/openinterpreter/openinterpreter/blob/be37756b53f91401e13019ffce41c02a0682cd89/codex-cli/package.json) still points at `@openai/codex`.
- Harness proliferation can easily become prompt debt if the team keeps adding dialects faster than it tests them.
- The product promise is "better low-cost coding agents," but that advantage depends on tuning discipline that can quietly regress.

## What we can learn / steal
- Keep one durable agent core and move adaptation logic into explicit harness layers.
- Model/provider selection UI is worth exposing when behavior differences are large and predictable.
- Compatibility shims can be a product feature, not just a migration crutch.
- A monorepo can support many agent surfaces if the routing boundaries are explicit.

## How we could apply it
If we wanted to support many cheaper providers without rewriting our agent stack, I would copy the separation used here:

1. one core tool/runtime layer,
2. one provider metadata layer,
3. one harness-routing layer,
4. thin UI and packaging shells over that core.

That pattern is more durable than building a separate "best prompt" per model family.

## Bottom line
Open Interpreter is worth studying because it turns agent performance tuning into software architecture.

The builder lesson is that cheap-model reliability often comes from disciplined harness shaping, transport compatibility, and explicit runtime boundaries, not just from finding a slightly better model. The repo is heavy, inherited, and somewhat fork-awkward, but the routing idea is real and reusable.
