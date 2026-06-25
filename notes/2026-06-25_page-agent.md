# Page Agent

- Repo: `alibaba/page-agent`
- URL: https://github.com/alibaba/page-agent
- Date: 2026-06-25
- Repo snapshot studied: `main` @ `187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32`
- Why picked today: It was one of the hot GitHub trending repos when checked, but the real reason to study it is that it is not another headless-browser bot farm. It is a client-side GUI agent that tries to live inside the page itself, with a real monorepo split between DOM extraction, agent control flow, UI, extension transport, and model-provider plumbing.

## Executive summary
`page-agent` is best read as an attempt to turn "AI control of a web UI" into an embeddable front-end subsystem instead of a remote automation stack. The core composition is explicit in [`packages/page-agent/src/PageAgent.ts`](https://github.com/alibaba/page-agent/blob/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/page-agent/src/PageAgent.ts): a [`PageController`](https://github.com/alibaba/page-agent/blob/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/page-controller/src/PageController.ts) turns the live DOM into a simplified indexed interaction surface, [`PageAgentCore`](https://github.com/alibaba/page-agent/blob/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/core/src/PageAgentCore.ts) runs a forced tool-calling loop over that surface, and the [`@page-agent/ui`](https://github.com/alibaba/page-agent/tree/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/ui) panel package gives it a product shell instead of leaving it as a library demo.

The strongest builder idea is the repo's refusal to pretend the agent sees a magical browser. [`PageController.getBrowserState()`](https://github.com/alibaba/page-agent/blob/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/page-controller/src/PageController.ts) constructs a bounded textual browser state with page metrics, scroll hints, and simplified interactive HTML. [`packages/core/src/tools/index.ts`](https://github.com/alibaba/page-agent/blob/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/core/src/tools/index.ts) then exposes a deliberately small action vocabulary rather than a giant fantasy tool list. The agent loop in [`PageAgentCore.ts`](https://github.com/alibaba/page-agent/blob/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/core/src/PageAgentCore.ts) forces one macro-tool call per step, keeps structured history, and injects task state, browser state, and system observations into every turn.

The caution is equally clear: the whole product inherits the blind spots of a DOM-first worldview. Canvas-heavy apps, visually encoded state, and complex custom widgets will always be harder than ordinary forms and buttons. The repo knows this well enough to include an experimental JavaScript escape hatch and a Chrome-extension/MCP bridge, but those are also admissions that a purely text-and-DOM strategy does not cover everything.

## What they built
They built a layered browser agent product, not just an npm wrapper:

- [`packages/page-agent/`](https://github.com/alibaba/page-agent/tree/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/page-agent) is the public composition layer that combines agent runtime, controller, and panel.
- [`packages/core/`](https://github.com/alibaba/page-agent/tree/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/core) is the actual agent engine: step loop, prompt assembly, tool registry, history, observations, and stop/dispose lifecycle.
- [`packages/page-controller/`](https://github.com/alibaba/page-agent/tree/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/page-controller) owns DOM flattening, selector maps, indexed actions, scroll behavior, and masking.
- [`packages/llms/`](https://github.com/alibaba/page-agent/tree/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/llms) handles OpenAI-compatible tool-calling transport and request normalization.
- [`packages/mcp/`](https://github.com/alibaba/page-agent/tree/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/mcp) and [`packages/extension/`](https://github.com/alibaba/page-agent/tree/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/extension) stretch the same agent into multi-page, browser-assisted workflows.
- [`packages/website/`](https://github.com/alibaba/page-agent/tree/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/website) and [`docs/`](https://github.com/alibaba/page-agent/tree/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/docs) turn it into a documented product, not only a source drop.

## Why it matters
Most GUI-agent repos still assume a server-side operator with screenshots, headless browsers, and a lot of ambient privilege. `page-agent` matters because it inverts that assumption.

1. It is meant to be embedded directly into an existing web app, with plain JavaScript and no Python runtime in the critical path.
2. It treats browser control as a structured front-end systems problem: DOM extraction, action vocabulary, prompt budgeting, page-state deltas, and framework quirks.
3. It exposes a realistic path from single-page in-app copilot to cross-page browser operator through the extension and MCP bridge, instead of pretending those are the same thing.

## Repo shape at a glance
The repo is a monorepo, but it is a fairly disciplined one:

- [`package.json`](https://github.com/alibaba/page-agent/blob/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/package.json) defines eight workspaces: controller, UI, LLM adapters, core runtime, product wrapper, MCP bridge, extension, and website.
- [`README.md`](https://github.com/alibaba/page-agent/blob/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/README.md) frames the product around in-page DOM control, optional Chrome extension, and BYO LLMs.
- [`packages/core/`](https://github.com/alibaba/page-agent/tree/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/core) is the control plane.
- [`packages/page-controller/`](https://github.com/alibaba/page-agent/tree/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/page-controller) is the browser-state extraction and action plane.
- [`packages/llms/`](https://github.com/alibaba/page-agent/tree/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/llms) is the provider adapter plane.
- [`packages/mcp/`](https://github.com/alibaba/page-agent/tree/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/mcp) is the external control plane for agent clients.
- [`scripts/`](https://github.com/alibaba/page-agent/tree/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/scripts) carries build and CI orchestration for the monorepo.

## Layered architecture dissection
### High-level system shape
The public object is intentionally thin. [`PageAgent`](https://github.com/alibaba/page-agent/blob/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/page-agent/src/PageAgent.ts) creates a [`PageController`](https://github.com/alibaba/page-agent/blob/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/page-controller/src/PageController.ts) with masking enabled by default, passes it into [`PageAgentCore`](https://github.com/alibaba/page-agent/blob/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/core/src/PageAgentCore.ts), and mounts a [`Panel`](https://github.com/alibaba/page-agent/tree/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/ui). That is the right split: control logic stays reusable, while the UI layer remains optional.

### Main layers
**1. Agent loop layer**  
[`PageAgentCore.ts`](https://github.com/alibaba/page-agent/blob/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/core/src/PageAgentCore.ts) is a classic ReAct-style loop, but with stronger shape than most. It tracks status, emits history and activity events, injects observations like URL changes and step-budget warnings, and forces the model through a single macro-tool schema via `#packMacroTool()`.

**2. Browser state layer**  
[`PageController.ts`](https://github.com/alibaba/page-agent/blob/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/page-controller/src/PageController.ts) updates a flat DOM tree, builds selector and text maps, and turns the current page into an LLM-readable state with `header`, `content`, and `footer` sections. That is the most important systems decision in the repo.

**3. Tool layer**  
[`packages/core/src/tools/index.ts`](https://github.com/alibaba/page-agent/blob/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/core/src/tools/index.ts) keeps the agent action surface small: done, wait, ask_user, click, input, select, scroll, horizontal scroll, and experimental JavaScript execution. The repo is explicitly choosing constrained affordances over fake generality.

**4. Provider adapter layer**  
[`packages/llms/src/OpenAIClient.ts`](https://github.com/alibaba/page-agent/blob/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/llms/src/OpenAIClient.ts) turns the internal tool schemas into OpenAI-compatible tool definitions, forces `parallel_tool_calls: false`, supports named tool choice, and normalizes errors into typed invoke failures.

**5. Browser bridge layer**  
[`packages/mcp/src/index.js`](https://github.com/alibaba/page-agent/blob/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/mcp/src/index.js) plus [`packages/mcp/src/hub-bridge.js`](https://github.com/alibaba/page-agent/blob/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/mcp/src/hub-bridge.js) open a local launcher page, wait for the extension hub to connect over WebSocket, and expose `execute_task`, `get_status`, and `stop_task` to MCP clients.

### Request / data / control flow
The control path is cleaner than the README marketing makes it sound:

1. A page creates [`PageAgent`](https://github.com/alibaba/page-agent/blob/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/page-agent/src/PageAgent.ts) and calls `execute(task)`.
2. [`PageAgentCore.execute`](https://github.com/alibaba/page-agent/blob/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/core/src/PageAgentCore.ts) asks the controller for fresh browser state.
3. [`PageController.updateTree`](https://github.com/alibaba/page-agent/blob/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/page-controller/src/PageController.ts) flattens interactive DOM into indexed simplified HTML.
4. [`#assembleUserPrompt()`](https://github.com/alibaba/page-agent/blob/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/core/src/PageAgentCore.ts) packages task, step budget, history, observations, optional page instructions, and optional fetched `llms.txt`.
5. [`OpenAIClient.invoke`](https://github.com/alibaba/page-agent/blob/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/llms/src/OpenAIClient.ts) calls `/chat/completions` with the macro tool.
6. The chosen action is executed through [`packages/core/src/tools/index.ts`](https://github.com/alibaba/page-agent/blob/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/core/src/tools/index.ts), which delegates to controller actions.
7. The loop repeats until the model calls `done`, or an external stop/dispose interrupts it.
8. For multi-page external control, the same task can be routed through [`hub-bridge.js`](https://github.com/alibaba/page-agent/blob/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/mcp/src/hub-bridge.js) to the browser extension hub.

## Key directories and files
- [`packages/page-agent/src/PageAgent.ts`](https://github.com/alibaba/page-agent/blob/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/page-agent/src/PageAgent.ts): the top-level composition object.
- [`packages/core/src/PageAgentCore.ts`](https://github.com/alibaba/page-agent/blob/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/core/src/PageAgentCore.ts): the heart of the runtime.
- [`packages/core/src/tools/index.ts`](https://github.com/alibaba/page-agent/blob/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/core/src/tools/index.ts): the real action contract.
- [`packages/page-controller/src/PageController.ts`](https://github.com/alibaba/page-agent/blob/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/page-controller/src/PageController.ts): DOM flattening, browser state generation, and action execution.
- [`packages/page-controller/src/dom/`](https://github.com/alibaba/page-agent/tree/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/page-controller/src/dom): the lower-level DOM tree machinery.
- [`packages/llms/src/OpenAIClient.ts`](https://github.com/alibaba/page-agent/blob/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/llms/src/OpenAIClient.ts): provider bridge and tool-call normalization.
- [`packages/mcp/src/index.js`](https://github.com/alibaba/page-agent/blob/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/mcp/src/index.js) and [`packages/mcp/src/hub-bridge.js`](https://github.com/alibaba/page-agent/blob/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/mcp/src/hub-bridge.js): the outer browser automation bridge.

## Important components
**`PageAgentCore` is the real product, not the wrapper**  
The wrapper in [`PageAgent.ts`](https://github.com/alibaba/page-agent/blob/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/page-agent/src/PageAgent.ts) is tiny. The actual product behavior lives in the evented runtime, macro-tool packing, prompt assembly, and execution lifecycle in [`PageAgentCore.ts`](https://github.com/alibaba/page-agent/blob/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/core/src/PageAgentCore.ts).

**`PageController` is the differentiator**  
The repo's main idea is not "LLM clicks a button." It is the state abstraction in [`PageController.ts`](https://github.com/alibaba/page-agent/blob/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/page-controller/src/PageController.ts): flatten the interactive DOM, preserve index-addressable elements, and turn scroll position into explicit prompt context.

**The tool contract is intentionally narrow**  
[`tools/index.ts`](https://github.com/alibaba/page-agent/blob/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/core/src/tools/index.ts) is worth reading because it reveals the repo's operating philosophy. A short action vocabulary is easier to reason about, log, and stabilize than a kitchen-sink browser API.

**The MCP bridge is surprisingly pragmatic**  
[`hub-bridge.js`](https://github.com/alibaba/page-agent/blob/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/mcp/src/hub-bridge.js) does not over-architect the transport. It serves a local page, waits for an extension hub to connect, and sends `execute` / `stop` messages over WebSocket. That is a product-minded compromise.

## Important knobs / configs / extension points
- Workspace topology and build targets in [`package.json`](https://github.com/alibaba/page-agent/blob/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/package.json).
- `maxSteps`, `stepDelay`, `customTools`, `experimentalScriptExecutionTool`, and lifecycle hooks in [`PageAgentCore.ts`](https://github.com/alibaba/page-agent/blob/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/core/src/PageAgentCore.ts).
- `experimentalLlmsTxt`, page-specific instruction callbacks, and `transformPageContent` in the same runtime file.
- `enableMask`, viewport expansion, attribute inclusion, and interactivity blacklists in [`PageController.ts`](https://github.com/alibaba/page-agent/blob/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/page-controller/src/PageController.ts).
- LLM request transformation and named-tool-choice behavior in [`OpenAIClient.ts`](https://github.com/alibaba/page-agent/blob/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/llms/src/OpenAIClient.ts).
- Local MCP bridge port and model env vars in [`packages/mcp/src/index.js`](https://github.com/alibaba/page-agent/blob/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/mcp/src/index.js).

## Practical questions and answers
**Is this really a browser agent, or just a fancy prompt wrapper?**  
It is a real browser agent, but a very opinionated one. It sees a textualized DOM interaction surface, not pixels and not a hidden remote browser.

**What is the most reusable idea here?**  
The combination of bounded browser-state serialization plus a forced macro-tool schema. That is a better base for productization than letting the model freestyle arbitrary browser API calls.

**Where will it struggle?**  
Canvas-heavy products, visual-only state, and cross-page workflows without the extension. The repo can work around some of that with `execute_javascript` and the MCP/extension path, but those are escape hatches, not proof that the core abstraction solves everything.

**What should a serious builder read first?**  
Read [`README.md`](https://github.com/alibaba/page-agent/blob/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/README.md), then [`PageAgent.ts`](https://github.com/alibaba/page-agent/blob/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/page-agent/src/PageAgent.ts), [`PageAgentCore.ts`](https://github.com/alibaba/page-agent/blob/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/core/src/PageAgentCore.ts), [`PageController.ts`](https://github.com/alibaba/page-agent/blob/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/page-controller/src/PageController.ts), and [`OpenAIClient.ts`](https://github.com/alibaba/page-agent/blob/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/llms/src/OpenAIClient.ts).

## What is smart
- Making the model act through one macro-tool call per step instead of a loose conversational contract.
- Treating browser state as a bounded artifact with page metrics and scroll hints.
- Supporting page-specific instructions and even `llms.txt` fetches in [`PageAgentCore.ts`](https://github.com/alibaba/page-agent/blob/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/core/src/PageAgentCore.ts).
- Keeping the DOM/action layer LLM-independent in [`PageController.ts`](https://github.com/alibaba/page-agent/blob/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/page-controller/src/PageController.ts).
- Using a dead-simple local WebSocket bridge for the MCP/browser-extension path.

## What is flawed or weak
- The DOM-first approach is intrinsically weaker on visually rich apps than screenshot- or accessibility-tree-heavy systems.
- The agent loop still depends on prompt budget and LLM reliability; large, messy pages can flood the abstraction even when the controller tries to simplify them.
- The extension + loopback WebSocket path in [`hub-bridge.js`](https://github.com/alibaba/page-agent/blob/187d5deccb6bbb9eedb5c4dc15f9b0a85e1f3a32/packages/mcp/src/hub-bridge.js) is pragmatic, but operationally brittle compared with a fully managed remote control plane.
- `execute_javascript` is useful, but it is also an escape hatch that can bypass the discipline of the structured action vocabulary.
- The repo is product-shaped enough that docs, website, extension, MCP, UI, and runtime all need to stay aligned. That coordination burden will grow fast.

## What we can learn / steal
- Serialize browser state explicitly instead of letting the model hallucinate what the page looks like.
- Keep the agent action vocabulary small and observable.
- Separate the front-end controller layer from the model-provider layer.
- Treat multi-page support as a transport problem with its own bridge, not as an afterthought.
- Let pages inject local instructions and policy into the agent prompt instead of shipping one universal behavior.

## How we could apply it
If we wanted our own in-product GUI agent, I would copy the shape more than the branding:

1. a controller that turns the live app into a compact, indexed interaction model,
2. a core loop that always returns structured action decisions,
3. a tiny action surface with good logs,
4. optional page-specific instruction hooks,
5. a separate bridge for out-of-page or multi-tab control.

That pattern would work for internal admin copilots, workflow automation in SaaS dashboards, and accessibility layers. The transferable lesson is to make the page interaction model explicit before you worry about "agent magic."

## Bottom line
`page-agent` is worth studying because it has a real architecture for in-page browser agency instead of just a spicy demo.

The builder lesson is that GUI agents get more credible when the browser state is treated like data, the action space is constrained, and the multi-page story is separated into its own bridge. The repo is not a universal answer to browser automation, but it is a strong blueprint for the part that lives inside the product.
