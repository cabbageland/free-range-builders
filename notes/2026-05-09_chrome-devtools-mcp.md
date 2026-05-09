# Chrome DevTools MCP

- Repo: `ChromeDevTools/chrome-devtools-mcp`
- URL: https://github.com/ChromeDevTools/chrome-devtools-mcp
- Date: 2026-05-09
- Repo snapshot studied: `main@88e543f53e2aeb3fbf74d56963718daa55fe6b00`
- Why picked today: It is both hot and unusually substantive. A lot of "agent browser" repos are thin wrappers over Puppeteer. This one is a real systems repo that fuses Puppeteer, DevTools frontend internals, Lighthouse, trace analysis, and MCP packaging into something builders can actually learn from.

## Executive summary

This repo turns Chrome DevTools into an MCP server so coding agents can drive a live browser, inspect what happened, and get compressed, agent-friendly answers instead of raw browser noise. The big idea is not browser automation by itself. The big idea is exposing browser state through small, deterministic tools while reusing real Chrome/DevTools machinery for traces, issues, heap snapshots, and diagnostics.

The most important architectural choice is that it is not just "Puppeteer with an MCP veneer". It uses Puppeteer for control, but leans on bundled DevTools frontend code and Lighthouse internals to produce higher-level debugging and performance outputs. That makes the repo more durable and more interesting than most agent tooling repos.

## What they built

They built two closely related surfaces:

1. an MCP server entrypoint in [`src/index.ts`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/index.ts)
2. a CLI and daemon wrapper around the same capabilities in [`src/bin/`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/bin) and [`src/daemon/`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/daemon)

The server exposes tool groups for navigation, input, screenshots, snapshots, console inspection, network inspection, performance tracing, Lighthouse audits, memory snapshots, extensions, third-party tools, and WebMCP integrations. The generated reference in [`docs/tool-reference.md`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/docs/tool-reference.md) shows how broad that surface already is.

## Why it matters

Most agent browser stacks fail in one of two ways:

- they are too low-level, so the agent drowns in DOM and protocol noise
- they are too magical, so the behavior is opaque and brittle

This repo threads the middle pretty well. Its design principles in [`docs/design-principles.md`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/docs/design-principles.md) are visible in the code: small tools, semantic summaries, references to heavy artifacts instead of dumping blobs, and actionable errors.

## Repo shape at a glance

At the top level, the repo breaks down into a few clear zones:

- runtime code in [`src/`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src)
- generated and hand-written docs in [`docs/`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/docs)
- developer scripts in [`scripts/`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/scripts)
- agent-facing skills in [`skills/`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/skills)
- a large, serious test suite in [`tests/`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/tests)

Inside [`src/`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src), the structure is also clean:

- browser lifecycle and connection logic in [`src/browser.ts`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/browser.ts)
- MCP server bootstrap in [`src/index.ts`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/index.ts)
- long-lived browser state and collectors in [`src/McpContext.ts`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/McpContext.ts), [`src/McpPage.ts`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/McpPage.ts), and [`src/PageCollector.ts`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/PageCollector.ts)
- tool definitions in [`src/tools/`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/tools)
- output shaping in [`src/formatters/`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/formatters)
- trace parsing in [`src/trace-processing/`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/trace-processing)
- telemetry in [`src/telemetry/`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/telemetry)
- daemon support in [`src/daemon/`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/daemon)
- vendored or bundled dependencies in [`src/third_party/`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/third_party)

## Layered architecture dissection

### High-level system shape

The system has a simple outer shape:

1. start or attach to Chrome
2. create an MCP server
3. register a catalog of narrowly-scoped tools
4. maintain page/browser context between calls
5. translate raw browser and DevTools state into compact responses

That flow is assembled in [`src/index.ts`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/index.ts).

### Main layers

**1. Browser transport and process layer**

[`src/browser.ts`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/browser.ts) handles the ugly but essential part: launch Chrome, attach to an existing instance, support channels and profiles, filter targets, and normalize Puppeteer startup options.

**2. Stateful runtime context**

[`src/McpContext.ts`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/McpContext.ts) is the real core. It tracks selected pages, isolated browser contexts, trace state, screen recording state, heap snapshots, extension workers, workspace-root validation, and collectors for network and console data.

This is the key repo insight: the product is not just a tool list. The product is a persistent browser context with memory and guardrails.

**3. Tool definition layer**

[`src/tools/ToolDefinition.ts`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/tools/ToolDefinition.ts) defines the shared contract, while [`src/tools/tools.ts`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/tools/tools.ts) assembles either the full tool set or the slim profile.

Then each capability family lives in a dedicated module such as [`src/tools/pages.ts`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/tools/pages.ts), [`src/tools/network.ts`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/tools/network.ts), and [`src/tools/performance.ts`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/tools/performance.ts).

**4. Analysis and formatting layer**

This is where the repo gets better than average. Instead of returning raw trace or console payloads, it routes outputs through formatters in [`src/formatters/`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/formatters) and trace processing in [`src/trace-processing/parse.ts`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/trace-processing/parse.ts).

**5. Packaging and session-control layer**

The CLI front doors in [`src/bin/chrome-devtools-mcp.ts`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/bin/chrome-devtools-mcp.ts) and [`src/bin/chrome-devtools.ts`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/bin/chrome-devtools.ts), plus the daemon in [`src/daemon/daemon.ts`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/daemon/daemon.ts), make the system usable outside a single transient MCP session.

### Request / data / control flow

A typical request path looks like this:

- MCP request hits the server registered in [`src/index.ts`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/index.ts)
- the server resolves whether the tool is enabled and what schema applies
- the handler pulls current page/context state from [`src/McpContext.ts`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/McpContext.ts)
- Puppeteer and DevTools do the actual browser work via modules like [`src/browser.ts`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/browser.ts)
- collectors and formatters condense the result
- the response object returns a summary, and points to files when the payload would be too heavy

The performance path is especially revealing. [`src/tools/performance.ts`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/tools/performance.ts) starts Chrome tracing, optionally reloads, saves raw trace data, parses it, optionally enriches it with CrUX data, and then stores structured trace results back in context for follow-up analysis calls.

## Key directories and files

- [`package.json`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/package.json): tells the whole story quickly, including dual binaries, heavy reliance on `puppeteer`, `lighthouse`, and `chrome-devtools-frontend`, plus a build-and-generate workflow.
- [`src/index.ts`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/index.ts): MCP bootstrap, tool registration, category gating, and server lifecycle.
- [`src/browser.ts`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/browser.ts): browser launch/connect behavior and target filtering.
- [`src/McpContext.ts`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/McpContext.ts): long-lived runtime brain.
- [`src/PageCollector.ts`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/PageCollector.ts): console and network event collection.
- [`src/tools/tools.ts`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/tools/tools.ts): capability assembly point.
- [`src/tools/pages.ts`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/tools/pages.ts): navigation lifecycle and allowlist-aware movement.
- [`src/tools/network.ts`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/tools/network.ts): request listing and body retrieval.
- [`src/tools/performance.ts`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/tools/performance.ts): trace orchestration and insight extraction.
- [`src/tools/slim/tools.ts`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/tools/slim/tools.ts): stripped-down mode showing how the team thinks about minimum viable browser control.
- [`src/daemon/daemon.ts`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/daemon/daemon.ts): a local socket wrapper that keeps a reusable MCP-backed browser process alive.
- [`src/third_party/`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/third_party): the vendored/bundled dependency zone that makes the rich analysis possible.
- [`tests/`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/tests): strong sign this is a serious product repo, not just a demo.

## Important components

- [`createMcpServer` in `src/index.ts`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/index.ts): assembles the whole server.
- [`McpContext.from` in `src/McpContext.ts`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/McpContext.ts): initializes the stateful browser context and collectors.
- [`ensureBrowserConnected` and `launch` in `src/browser.ts`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/browser.ts): normalize the browser boundary.
- [`createTools` in `src/tools/tools.ts`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/tools/tools.ts): tool catalog assembly.
- [`listPages`, `newPage`, and `navigatePage` in `src/tools/pages.ts`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/tools/pages.ts): page selection and movement primitives.
- [`startTrace` and `analyzeInsight` in `src/tools/performance.ts`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/tools/performance.ts): trace capture and follow-up insight exploration.
- [`listNetworkRequests` and `getNetworkRequest` in `src/tools/network.ts`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/tools/network.ts): readable network inspection.
- [`ClearcutLogger` in `src/telemetry/ClearcutLogger.ts`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/telemetry/ClearcutLogger.ts): built-in telemetry pipeline, which is operationally important and politically notable.

## Important knobs / configs / extension points

- full vs slim mode via [`src/tools/slim/tools.ts`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/tools/slim/tools.ts)
- category gating and feature flags in [`src/index.ts`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/index.ts) and [`src/tools/categories.ts`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/tools/categories.ts)
- browser attachment vs launch behavior in [`src/browser.ts`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/browser.ts)
- path/root safety for file output in [`src/McpContext.ts`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/McpContext.ts)
- update checks and usage statistics documented in [`README.md`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/README.md)
- third-party developer tool bridging in [`src/tools/thirdPartyDeveloper.ts`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/tools/thirdPartyDeveloper.ts)
- WebMCP bridging in [`src/tools/webmcp.ts`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/tools/webmcp.ts)

## Practical questions and answers

**Is this mostly a Puppeteer wrapper?**

No. Puppeteer is the transport and control plane, but the repo becomes interesting because it layers DevTools frontend, trace parsing, Lighthouse, collectors, and MCP-oriented response shaping on top.

**Where is the real leverage?**

In the stateful context plus semantic output shaping. [`src/McpContext.ts`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/McpContext.ts) and [`src/formatters/`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/formatters) do more product work than the click/type tools.

**What assumption does the system make?**

That agents need compact, structured, follow-up-friendly diagnostics more than raw protocol completeness.

**Where could it fail in production?**

At the browser boundary. Chrome launch quirks, remote-debugging attach failures, profile weirdness, extension edge cases, and GUI/headless environment differences are still the hard part. [`src/browser.ts`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/browser.ts) is where that pain lives.

**What is the most reusable pattern here?**

Treat heavyweight artifacts as files and return summaries plus references. That is a strong design for any agent-facing system, not just browsers.

## What is smart

- Reusing actual Chrome/DevTools internals instead of inventing a parallel fake diagnostics stack.
- Separating tool definitions by capability family, which keeps the surface area large but still navigable.
- Making stateful follow-up possible, especially for traces and page context.
- Having a real slim mode instead of forcing the full product on every client.
- Heavy test coverage across unit, snapshot, daemon, and e2e layers in [`tests/`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/tests).

## What is flawed or weak

- The repo is broad enough that it risks becoming a kitchen sink.
- There is a lot of hidden complexity tied to vendored third-party code in [`src/third_party/`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/88e543f53e2aeb3fbf74d56963718daa55fe6b00/src/third_party), which usually means upgrade pain.
- Built-in telemetry and update checking are operationally sensible, but they add trust and governance questions for people who want local-first tooling.
- The product is only as reliable as Chrome + Puppeteer + platform quirks allow, so "deterministic" still has a browser-sized asterisk on it.

## What we can learn / steal

- Keep tool contracts small and composable.
- Return semantic summaries, not raw exhaust.
- Persist state between calls so agents can ask better second questions.
- Use workspace-root validation when tools can write files.
- Split the capability surface by subsystem, then generate docs from code so the public API stays aligned.

## How we could apply it

For our own agent tools, the best pattern to copy is the combination of:

- a stateful runtime context
- a catalog of narrow tools
- summary-first responses with file references for large payloads
- explicit feature flags and slim/full operating modes

If we ever build an agent-facing debugger or observability surface, this repo is a much better template than most "agent browser" projects on GitHub.

## Bottom line

This is one of the more legitimate agent-infra repos on GitHub right now. It is not exciting because it clicks buttons in Chrome. It is exciting because it packages real browser debugging and performance machinery into an agent-friendly interface without hiding the underlying system too much.

The standout insight is simple: the valuable part is not automation, it is compression. They turned Chrome's huge debugging surface into a set of small, stateful, inspectable tools that agents can actually reason over.