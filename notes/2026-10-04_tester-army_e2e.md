# e2e

- Repo: tester-army/e2e
- URL: https://github.com/tester-army/e2e
- Date: 2026-10-04
- Repo snapshot studied: main at f99e80ebc04f8194f967244198783db871390e06
- Why picked today: It was the top GitHub daily trending repository in the scout run, with 344 stars today and 2,658 total stars. It is also a good builder specimen: a natural-language E2E test runner that is not just a wrapper around an LLM, but a monorepo with a runner, engine SPI, web and mobile engines, trace replay, decision-model executor, reports, docs, and benchmark apps.

## Executive summary

`tester-army/e2e` is an agentic end-to-end testing framework for web and mobile apps. The promise in the [README](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/README.md) is simple: write a test with deterministic setup and assertions, give the agent a natural-language step such as "upgrade the workspace to the Pro plan," and let the framework drive the UI. The interesting part is the source shape. The repo treats "AI testing" as a real harness problem: execution budgets, semantic observations, action grammar, secret handling, replayable traces, platform engines, reporters, and CI-friendly artifacts.

The key lesson is that the LLM is intentionally boxed in. The shared loop in [packages/e2e/src/agent/tool-loop.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/e2e/src/agent/tool-loop.ts) owns budgets, verdict tools, loop guards, transcript clipping, provider retries, and forced conclusions. The engine contract in [packages/e2e/src/engine/contract.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/e2e/src/engine/contract.ts) makes browsers and devices report a platform-neutral semantic tree. The trace machinery in [packages/e2e/src/cache/recorder.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/e2e/src/cache/recorder.ts) and [packages/e2e/src/agent/replay.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/e2e/src/agent/replay.ts) tries to make one expensive agent step reusable without pretending UI automation is perfectly stable.

## What they built

They built a TypeScript monorepo around a public `e2e` package plus engine and integration packages. The root [package.json](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/package.json) wires build, lint, typecheck, docs checks, dead-code checks, package validation, and multi-package tests. The published SDK and CLI live under [packages/e2e](https://github.com/tester-army/e2e/tree/f99e80ebc04f8194f967244198783db871390e06/packages/e2e). Browser automation is in [packages/web](https://github.com/tester-army/e2e/tree/f99e80ebc04f8194f967244198783db871390e06/packages/web), mobile automation is in [packages/mobile](https://github.com/tester-army/e2e/tree/f99e80ebc04f8194f967244198783db871390e06/packages/mobile), hosted providers are split into [packages/kernel](https://github.com/tester-army/e2e/tree/f99e80ebc04f8194f967244198783db871390e06/packages/kernel) and [packages/eas](https://github.com/tester-army/e2e/tree/f99e80ebc04f8194f967244198783db871390e06/packages/eas), GitHub PR reporting sits in [packages/github](https://github.com/tester-army/e2e/tree/f99e80ebc04f8194f967244198783db871390e06/packages/github), and a bounded non-generative executor lives in [packages/decision](https://github.com/tester-army/e2e/tree/f99e80ebc04f8194f967244198783db871390e06/packages/decision).

The framework's public usage is familiar test-runner code. The test opens an app, calls `agent.act()` or `agent.assert()`, then verifies with locators and `expect`. Under that surface, the agent does not get arbitrary browser control. It receives observations, can call a defined action vocabulary, and must finish through a verdict. Actions are recorded in a trace, and later runs try a zero-model replay before handing back to the executor.

## Why it matters

Most agentic testing demos fail at the boring parts: repeatability, redaction, run reports, parallel workers, app lifecycle, device lifecycle, CI output, and "what happens after the first successful model run?" This repo is useful because it leans into those boring parts. The agent can be creative only inside a harness that knows what a screen is, what an action is, how long a step may run, what is secret, what can be replayed, and when a run should fail.

The source also shows a good boundary: [packages/e2e/src/engine/contract.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/e2e/src/engine/contract.ts) is platform vocabulary, not Playwright vocabulary. [packages/web/src/engine.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/web/src/engine.ts) adapts Playwright into that contract. [packages/mobile/src/engine.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/mobile/src/engine.ts) adapts `agent-device` into the same contract. That makes the runner and agent layers less tied to one automation backend.

## Repo shape at a glance

- [packages/e2e](https://github.com/tester-army/e2e/tree/f99e80ebc04f8194f967244198783db871390e06/packages/e2e) is the core SDK, runner, CLI, config loader, agent loop, cache, locator layer, report layer, MCP server, OAuth helpers, telemetry, and schemas.
- [packages/web](https://github.com/tester-army/e2e/tree/f99e80ebc04f8194f967244198783db871390e06/packages/web) is the Playwright-backed web engine: browser connection, observation capture, locators, action dispatch, videos, traces, downloads, protected-app handling, and install tooling.
- [packages/mobile](https://github.com/tester-army/e2e/tree/f99e80ebc04f8194f967244198783db871390e06/packages/mobile) is the `agent-device` mobile engine: device sessions, app launch/reset, node location, selectors, screenshots, videos, gestures, links, and hosted-device support.
- [packages/decision](https://github.com/tester-army/e2e/tree/f99e80ebc04f8194f967244198783db871390e06/packages/decision) is a choice-model executor that maps observations into explicit questions instead of free-form action generation.
- [packages/github](https://github.com/tester-army/e2e/tree/f99e80ebc04f8194f967244198783db871390e06/packages/github), [packages/kernel](https://github.com/tester-army/e2e/tree/f99e80ebc04f8194f967244198783db871390e06/packages/kernel), and [packages/eas](https://github.com/tester-army/e2e/tree/f99e80ebc04f8194f967244198783db871390e06/packages/eas) are integration packages rather than core logic.
- [docs](https://github.com/tester-army/e2e/tree/f99e80ebc04f8194f967244198783db871390e06/docs) is a full documentation site and is shipped with the `e2e` package so coding agents can read it offline.
- [apps](https://github.com/tester-army/e2e/tree/f99e80ebc04f8194f967244198783db871390e06/apps) holds testbed and benchmark applications, which is a healthy sign for a testing framework.
- [scripts](https://github.com/tester-army/e2e/tree/f99e80ebc04f8194f967244198783db871390e06/scripts) contains release, package, docs, install, and consistency checks.

## Layered architecture dissection

### High-level system shape

At the top is a test-runner surface: users import from `e2e`, define tests, targets, agents, and expectations, then run the CLI. The package metadata in [packages/e2e/package.json](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/e2e/package.json) exports the public SDK, agent API, engine API, OAuth helpers, CLI binary, JSON schemas, docs, and skills.

The second layer is run orchestration. [packages/e2e/src/run/runner.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/e2e/src/run/runner.ts) is the best entry point: it discovers and resolves config, collects tests, selects targets, allocates app ports, prepares engines, runs workers, emits events, builds reports, handles last-failed selection, writes artifacts, and accounts for infrastructure versus test failures.

The third layer is the engine contract. [packages/e2e/src/engine/contract.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/e2e/src/engine/contract.ts) defines semantic nodes, locators, viewport points, observation pixels, action kinds, app/session hooks, artifacts, and timing. Engines implement this vocabulary. The core runner consumes it without importing browser or device-specific modules.

The fourth layer is agent execution. [packages/e2e/src/agent/tool-loop.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/e2e/src/agent/tool-loop.ts) is the chassis. It owns the model call loop, verdict tool, guard rails, overflow handling, transcript compaction, low-clock wind-down, forced tool-call fallback, and model-call accounting. Concrete executors bring tool vocabularies and prompts.

The fifth layer is trace cache and replay. [packages/e2e/src/cache/recorder.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/e2e/src/cache/recorder.ts) records committed actions as durable descriptors and secret-redacted summaries. [packages/e2e/src/agent/replay.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/e2e/src/agent/replay.ts) tries those actions again against fresh observations, handing off to the agent when a target moved, a gap appears, or an action becomes uncertain.

### Main layers

The SDK/config layer is carried by files such as [packages/e2e/src/config/load.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/e2e/src/config/load.ts), [packages/e2e/src/config/resolve.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/e2e/src/config/resolve.ts), and [packages/e2e/src/index.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/e2e/src/index.ts). This layer turns user declarations into resolved targets, agents, budgets, reporters, outputs, and app processes.

The runtime layer is under [packages/e2e/src/run](https://github.com/tester-army/e2e/tree/f99e80ebc04f8194f967244198783db871390e06/packages/e2e/src/run). It schedules work, starts managed processes, provisions engines, runs worker sessions, writes artifacts, emits events, and builds the final run document.

The observation/action layer spans [packages/e2e/src/agent/actions.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/e2e/src/agent/actions.ts), [packages/e2e/src/agent/observation.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/e2e/src/agent/observation.ts), [packages/e2e/src/locator/screen.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/e2e/src/locator/screen.ts), and the engine contract. This is where vague natural language becomes "tap this semantic node," "type into this field," or "assert this locator."

The platform layer is explicit. [packages/web/src/engine.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/web/src/engine.ts) validates web options, creates a Playwright surface, exposes browser fixtures, captures state, traces, videos, and screenshots, and supports both created and connected browser contexts. [packages/mobile/src/engine.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/mobile/src/engine.ts) validates mobile app declarations, drives installed apps, and exposes device fixtures.

### Request / data / control flow

A run starts in the CLI, resolves config, collects tests, selects targets, and plans target work through [packages/e2e/src/run/runner.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/e2e/src/run/runner.ts) and [packages/e2e/src/run/units.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/e2e/src/run/units.ts). Each target gets a prepared engine through [packages/e2e/src/run/provision.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/e2e/src/run/provision.ts). The engine opens or restarts the app, then deterministic test code and agent steps share the same surface.

When a test reaches an agent step, the executor observes the screen through the engine's semantic and pixel capture APIs. The tool loop in [packages/e2e/src/agent/tool-loop.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/e2e/src/agent/tool-loop.ts) sends bounded context to the model, exposes only the configured tools plus a verdict tool, dispatches actions through the engine, and collects a step transcript. The committed actions are described by [packages/e2e/src/agent/actions.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/e2e/src/agent/actions.ts) so reports, traces, and relocation logic use the same summaries.

On a later run, [packages/e2e/src/agent/replay.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/e2e/src/agent/replay.ts) replays the recorded grammar actions without calling the model. If the trace no longer lines up, replay stops adaptively and hands the partial state back to the executor. That is the right kind of humility for AI-driven UI automation: save the stable parts, but do not fake determinism where the app changed.

## Key directories and files

- [README.md](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/README.md): public pitch, example test, package map, telemetry note, and project status.
- [package.json](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/package.json): root quality gates and package-level orchestration.
- [packages/e2e/package.json](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/e2e/package.json): public exports, CLI binary, schemas, docs, skills, optional AI SDK peers, and Node engine floor.
- [packages/e2e/src/run/runner.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/e2e/src/run/runner.ts): orchestration center for collection, selection, engine preparation, worker execution, events, reports, artifacts, and exit codes.
- [packages/e2e/src/engine/contract.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/e2e/src/engine/contract.ts): platform-neutral engine SPI and semantic observation vocabulary.
- [packages/e2e/src/agent/tool-loop.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/e2e/src/agent/tool-loop.ts): shared model loop, conclusion policy, tool guarding, transcript policy, overflow handling, and loop guards.
- [packages/e2e/src/cache/recorder.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/e2e/src/cache/recorder.ts): trace recorder for committed actions, target descriptors, secret redaction, and replay poisoning rules.
- [packages/e2e/src/agent/replay.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/e2e/src/agent/replay.ts): zero-model replay engine and handoff logic.
- [packages/web/src/engine.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/web/src/engine.ts): Playwright engine adapter.
- [packages/mobile/src/engine.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/mobile/src/engine.ts): mobile engine adapter backed by `agent-device`.
- [packages/decision/src/executor.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/decision/src/executor.ts): choice-model executor with probability and confidence gates.

## Important components

The most important component is the tool-loop chassis in [packages/e2e/src/agent/tool-loop.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/e2e/src/agent/tool-loop.ts). It is packed with production-shaped details: provider hints, context-overflow handling, text-reply notices, forced verdicts near budget exhaustion, loop guard thresholds, transcript caps, tool-result clipping, and hard-stop handling.

The second important component is the semantic engine contract in [packages/e2e/src/engine/contract.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/e2e/src/engine/contract.ts). The central trick is not the model prompt. It is that a browser, a simulator, and later maybe another UI surface can all describe controls as semantic nodes with roles, names, text, states, rectangles, selectors, frame paths, and input purposes.

The trace pair, [packages/e2e/src/cache/recorder.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/e2e/src/cache/recorder.ts) plus [packages/e2e/src/agent/replay.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/e2e/src/agent/replay.ts), is the practical differentiator. Recording a successful action is not enough. The system records target descriptors, container context, redacted summaries, derived-value gaps, scroll spans, viewport positions, and reasons replay must stop.

The platform engines are deliberately thin adapters around the contract. [packages/web/src/engine.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/web/src/engine.ts) validates browser options and delegates most mechanics to the Playwright surface. [packages/mobile/src/engine.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/mobile/src/engine.ts) validates mobile app shape and maps mobile sessions to the same observe, locate, perform, keyboard, session, artifact, and fixture vocabulary.

The choice-model executor in [packages/decision/src/executor.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/decision/src/executor.ts) is a clever alternate path. It asks a model bounded multiple-choice questions about operations and targets, gates decisions by probability and confidence, and only falls back to a text model when it needs field text. That is an antidote to the common "let the model invent JSON actions" design.

## Important knobs / configs / extension points

The main extension point is the engine SPI exposed through [packages/e2e/src/engine/index.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/e2e/src/engine/index.ts) and specified in [packages/e2e/src/engine/contract.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/e2e/src/engine/contract.ts). A new platform needs to implement observation, location, action, keyboard, session, artifact, and fixture hooks. The framework can then reuse the same runner and agent layers.

Agent behavior is controlled through config resolution in [packages/e2e/src/config/resolve.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/e2e/src/config/resolve.ts) and execution budgets consumed by [packages/e2e/src/agent/tool-loop.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/e2e/src/agent/tool-loop.ts). Useful knobs include model choice, max model calls, agent selection, cache mode, strict cache, output directory, retries, workers, trace mode, video mode, last-failed selection, sharding, and reporters.

Replay and cache behavior hangs off the trace files and cache logic under [packages/e2e/src/cache](https://github.com/tester-army/e2e/tree/f99e80ebc04f8194f967244198783db871390e06/packages/e2e/src/cache). This is where builders would tune how aggressively a successful step can be reused and what makes a trace non-replayable.

The CLI initializer under [packages/e2e/src/cli/init](https://github.com/tester-army/e2e/tree/f99e80ebc04f8194f967244198783db871390e06/packages/e2e/src/cli/init) is another important extension surface. It writes starter config, package setup, engine choices, MCP config, gateway choices, and skill material, which matters because testing frameworks live or die by first-run ergonomics.

## Practical questions and answers

Q: Is this just Playwright with an LLM call added?  
A: No. [packages/web/src/engine.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/web/src/engine.ts) uses Playwright, but the core value is the platform-neutral engine contract, agent loop, replay trace, runner, reporting, config, and mobile support. Playwright is one backend, not the architecture.

Q: Does every run need to call a model?  
A: Not necessarily. The [README](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/README.md) says later runs replay recorded actions with no model calls until the app changes. The replay implementation in [packages/e2e/src/agent/replay.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/e2e/src/agent/replay.ts) backs that claim with adaptive handoff instead of blind replay.

Q: Where is the system most likely to fail?  
A: Dynamic UIs with unstable semantic nodes, heavily visual tasks with poor accessibility trees, mobile screens whose node labels drift, and flows where prior recorded actions depended on live data. The trace code in [packages/e2e/src/cache/recorder.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/e2e/src/cache/recorder.ts) explicitly poisons traces rather than storing clipped or redacted values that would replay differently.

Q: What would I test first before adopting it?  
A: I would build a small suite with one stable web flow, one flaky dynamic flow, and one mobile flow. Then I would inspect the report files from [packages/e2e/src/report](https://github.com/tester-army/e2e/tree/f99e80ebc04f8194f967244198783db871390e06/packages/e2e/src/report), the trace cache, replay behavior, and CI output before trusting it for broad regression coverage.

Q: What is the most reusable design pattern?  
A: The "semantic engine contract plus bounded agent grammar" pattern. It is useful beyond testing: any UI agent product should separate platform observation, model loop policy, action grammar, trace recording, and reporting the way this repo does.

## What is smart

The smartest move is the engine contract. By making [packages/e2e/src/engine/contract.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/e2e/src/engine/contract.ts) platform-neutral, the project avoids hard-coding every AI behavior against a browser. The same `screen`, `expect`, and agent concepts can plausibly work across browser and device engines.

The second smart move is replay humility. [packages/e2e/src/agent/replay.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/e2e/src/agent/replay.ts) is not a naive macro player. It tries to relocate semantic descriptors, waits for settling, handles gaps, respects action budgets, and hands off when the world has changed.

The third smart move is one owner for action descriptions. [packages/e2e/src/agent/actions.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/e2e/src/agent/actions.ts) says the same description feeds trace recording, live events, and relocation candidates. That reduces one of the classic framework risks: reports, caches, and runtime behavior slowly developing different interpretations of the same action.

The fourth smart move is giving the decision executor its own package in [packages/decision](https://github.com/tester-army/e2e/tree/f99e80ebc04f8194f967244198783db871390e06/packages/decision). It acknowledges that not every step needs a full free-form agent. Sometimes the better control shape is a set of choices over an observed action space.

## What is flawed or weak

The system has a lot of surface area for a pre-1.0 framework. The top-level package map, the [packages/e2e](https://github.com/tester-army/e2e/tree/f99e80ebc04f8194f967244198783db871390e06/packages/e2e) internals, the web and mobile engines, hosted providers, docs, benchmark apps, skills, MCP server, OAuth flows, telemetry, and scripts are all moving together. That is ambitious and useful, but it creates many version and compatibility edges.

The engine contract depends heavily on semantic observations. That is the correct bet, but the weakest apps are often the ones most in need of agentic tests: canvas-heavy tools, inaccessible controls, unnamed mobile elements, animation-heavy screens, and custom widgets. The fallback to pixels and point actions helps, but every pixel fallback reduces replayability and diagnosability.

The mobile path is still narrower than the web path. [packages/mobile/src/engine.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/mobile/src/engine.ts) explicitly rejects `app.url` for mobile targets and tells users to test installed apps by bundle ID or app path. That is reasonable for a first shape, but it means mobile web and deep-link-heavy workflows still need careful handling.

There is also a business/product risk: the project is open source, but several surrounding concepts point toward hosted infrastructure. [packages/kernel](https://github.com/tester-army/e2e/tree/f99e80ebc04f8194f967244198783db871390e06/packages/kernel) and [packages/eas](https://github.com/tester-army/e2e/tree/f99e80ebc04f8194f967244198783db871390e06/packages/eas) are useful integrations, but teams should separate the open harness value from hosted execution assumptions.

## What we can learn / steal

Steal the contract-first platform design from [packages/e2e/src/engine/contract.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/e2e/src/engine/contract.ts). If an agent product supports multiple environments, define the environment vocabulary before writing provider-specific logic.

Steal the bounded agent loop from [packages/e2e/src/agent/tool-loop.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/e2e/src/agent/tool-loop.ts): hard budgets, a verdict tool, transcript caps, low-clock wind-down, loop guards, and model-failure policy belong in shared infrastructure, not scattered prompts.

Steal the trace philosophy from [packages/e2e/src/cache/recorder.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/e2e/src/cache/recorder.ts). A cached AI action should carry enough target context to be revalidated, and it should become non-replayable rather than silently lossy when secrets, clipped values, or dynamic runtime data are involved.

Steal the alternate executor idea from [packages/decision/src/executor.ts](https://github.com/tester-army/e2e/blob/f99e80ebc04f8194f967244198783db871390e06/packages/decision/src/executor.ts). For many agent tasks, "choose an operation and target from the observed action space" is safer and cheaper than "emit arbitrary tool JSON."

## How we could apply it

For our own builder tools, the reusable idea is to separate agent freedom from harness responsibility. If we built a browsing or app-testing scout, the agent should not hold raw browser automation directly. It should receive a semantic observation, choose from a grammar, and produce a trace that can be replayed or audited.

For Free Range Builders, this repo suggests a better note QA loop: an engine contract for note structure, an agent loop that can edit only through structured actions, a trace of changes, and a replay/check mode that confirms the next run would not have to rediscover the same corrections.

For product teams, the immediate application is regression testing around flows that are currently too expensive to write by hand. Start with flows where natural-language navigation is useful but final assertions are deterministic. Let the model find the path, but let the harness own the verdict.

## Bottom line

`tester-army/e2e` is worth studying because it treats agentic testing as systems engineering, not a prompt demo. The repo's best ideas are the platform-neutral engine contract, bounded agent tool loop, replayable action traces, and honest handoff when the UI changes. The risks are real, especially around semantic coverage and framework surface area, but the architecture is serious.
