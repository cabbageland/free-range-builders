# REA

- Repo: morluto/rea
- URL: https://github.com/morluto/rea
- Date: 2026-10-09
- Repo snapshot studied: main at commit 4b8e744d90579e353371649047215c4e4be7a5f6
- Why picked today: It was the top daily GitHub trending repo, with about 15k stars today on the trending page, and it has unusually rich source structure for an agentic reverse-engineering system: MCP server code, CLI paths, provider adapters, evidence ledgers, browser/runtime tools, native bridges, packaging, docs, tests, and an installable skill.

## Executive summary

[morluto/rea](https://github.com/morluto/rea/tree/4b8e744d90579e353371649047215c4e4be7a5f6) is a local reverse-engineering workbench for agents. It exposes one MCP server and one CLI that can inspect native binaries, JavaScript/Electron apps, websites, .NET assemblies, Android APKs, firmware, EVM bytecode, process behavior, browser runtime evidence, and package artifacts.

The interesting part is not just the ambition. The repo is engineered around a strict boundary between contracts, domain models, application services, provider adapters, and server/CLI translation. [src/main.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/main.ts) starts the long-lived MCP adapter. [src/server/createServer.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/server/createServer.ts) registers the actual tool surface. [src/composition/binary.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/composition/binary.ts) wires Hopper, Ghidra, IDA, managed static inspection, and auxiliary providers into one session runtime. [src/application/binary/BinarySession.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/application/binary/BinarySession.ts) owns the active target, provider client lifecycle, evidence records, snapshots, and cleanup.

The builder lesson is strong: this is an evidence system, not a wrapper around disassemblers. Tool calls are supposed to return structured facts with provenance, limitations, availability, cleanup status, and retained evidence. That posture shows up in [docs/mcp-contracts.md](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/docs/mcp-contracts.md), [docs/tool-design.md](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/docs/tool-design.md), the [src/domain](https://github.com/morluto/rea/tree/4b8e744d90579e353371649047215c4e4be7a5f6/src/domain) models, and the generated skill source in [skill-src/reverse-engineer-anything/SKILL.md](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/skill-src/reverse-engineer-anything/SKILL.md).

## What they built

REA packages reverse-engineering capabilities for coding agents and terminal users. The public package is [package.json](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/package.json) as `rea-agents`, with `rea` and `rea-agents` binaries pointing to [scripts/rea.mjs](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/scripts/rea.mjs). The README's target table in [README.md](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/README.md) is broad: native binaries through Hopper, Ghidra, or IDA; JavaScript and Electron static analysis; browser capture; saved network captures; managed .NET metadata; Android APKs; firmware; package resources; recorded crashes; process captures; and EVM bytecode.

The repo has two caller-facing runtimes. MCP mode starts from [src/main.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/main.ts), parses config through [src/config/parseConfig.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/config/parseConfig.ts), creates a binary session through [src/composition/binary.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/composition/binary.ts), then registers tools through [src/server/createServer.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/server/createServer.ts). CLI mode is mostly in [src/cli.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/cli.ts) and [src/cli](https://github.com/morluto/rea/tree/4b8e744d90579e353371649047215c4e4be7a5f6/src/cli), with direct one-shot analysis centralized in [src/application/DirectAnalysis.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/application/DirectAnalysis.ts).

## Why it matters

Agent reverse engineering is usually fragile because the agent either gets a giant dump or has to hand-drive a GUI-ish tool through brittle steps. REA tries to turn that into typed operations: inspect a function, trace a feature, inspect artifact inventory, capture browser behavior, compare versions, export retained evidence, and keep the unknowns visible.

That is a useful pattern beyond reverse engineering. A serious agent tool should not just expose "run the tool and paste output." It should expose small analyst tasks, normalize provider differences, return evidence and limitations, keep large records available without overrunning the MCP transport, and make provider availability explicit. [docs/tool-design.md](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/docs/tool-design.md) states that philosophy directly: tool contracts should be analyst-task-shaped, provider-neutral, complete by default, and honest about read-only, process, filesystem, network, and UI effects.

## Repo shape at a glance

- [src](https://github.com/morluto/rea/tree/4b8e744d90579e353371649047215c4e4be7a5f6/src): TypeScript implementation, split into server adapters, CLI adapters, application services, domain models, provider integrations, contracts, composition, and low-level artifact readers.
- [src/domain](https://github.com/morluto/rea/tree/4b8e744d90579e353371649047215c4e4be7a5f6/src/domain): provider-neutral facts, schemas, evidence, browser models, JavaScript analysis models, native facts, managed facts, artifact graphs, reconstruction coverage, and result/error types.
- [src/application](https://github.com/morluto/rea/tree/4b8e744d90579e353371649047215c4e4be7a5f6/src/application): orchestration layer: sessions, direct analysis, setup, evidence, binary provider routing, JavaScript workflows, browser workflows, managed workflows, Android, firmware, EVM, updates, and doctor diagnostics.
- [src/server](https://github.com/morluto/rea/tree/4b8e744d90579e353371649047215c4e4be7a5f6/src/server): MCP server construction, tool registration, result delivery, retained evidence, session tools, prompts, and transport-aware output handling.
- [src/contracts](https://github.com/morluto/rea/tree/4b8e744d90579e353371649047215c4e4be7a5f6/src/contracts): canonical tool names, input/output schemas, examples, effects, and provider-selection contracts.
- [src/hopper](https://github.com/morluto/rea/tree/4b8e744d90579e353371649047215c4e4be7a5f6/src/hopper), [src/ghidra](https://github.com/morluto/rea/tree/4b8e744d90579e353371649047215c4e4be7a5f6/src/ghidra), and [src/ida](https://github.com/morluto/rea/tree/4b8e744d90579e353371649047215c4e4be7a5f6/src/ida): deep native-analysis providers and bridge protocols.
- [src/browser](https://github.com/morluto/rea/tree/4b8e744d90579e353371649047215c4e4be7a5f6/src/browser), [src/javascript](https://github.com/morluto/rea/tree/4b8e744d90579e353371649047215c4e4be7a5f6/src/javascript), and [src/artifacts](https://github.com/morluto/rea/tree/4b8e744d90579e353371649047215c4e4be7a5f6/src/artifacts): web, runtime, source-map, bundle, package, ASAR, ZIP, DMG, Mach-O, and stable artifact readers.
- [bridge](https://github.com/morluto/rea/tree/4b8e744d90579e353371649047215c4e4be7a5f6/bridge): Python, Java, Swift, and mitmproxy bridge code for external engines and host capabilities.
- [skill-src](https://github.com/morluto/rea/tree/4b8e744d90579e353371649047215c4e4be7a5f6/skill-src): agent-facing instructions that route targets to the right REA tool and preserve evidence discipline.
- [docs](https://github.com/morluto/rea/tree/4b8e744d90579e353371649047215c4e4be7a5f6/docs): runtime contracts, guides, design rules, testing notes, provider setup, and release documentation.
- [tests](https://github.com/morluto/rea/tree/4b8e744d90579e353371649047215c4e4be7a5f6/tests) and the many `*.test.ts` files under [src](https://github.com/morluto/rea/tree/4b8e744d90579e353371649047215c4e4be7a5f6/src): boundary tests, provider fixtures, conformance tests, acceptance tests, and domain-service checks.

## Layered architecture dissection

### High-level system shape

REA is structured as a layered adapter system:

1. The caller enters through MCP or CLI.
2. The server/CLI layer validates inputs against [src/contracts](https://github.com/morluto/rea/tree/4b8e744d90579e353371649047215c4e4be7a5f6/src/contracts).
3. Application services in [src/application](https://github.com/morluto/rea/tree/4b8e744d90579e353371649047215c4e4be7a5f6/src/application) resolve targets, select providers, execute workflows, and record evidence.
4. Provider adapters under [src/hopper](https://github.com/morluto/rea/tree/4b8e744d90579e353371649047215c4e4be7a5f6/src/hopper), [src/ghidra](https://github.com/morluto/rea/tree/4b8e744d90579e353371649047215c4e4be7a5f6/src/ghidra), [src/ida](https://github.com/morluto/rea/tree/4b8e744d90579e353371649047215c4e4be7a5f6/src/ida), [src/browser](https://github.com/morluto/rea/tree/4b8e744d90579e353371649047215c4e4be7a5f6/src/browser), [src/android](https://github.com/morluto/rea/tree/4b8e744d90579e353371649047215c4e4be7a5f6/src/android), [src/dotnet](https://github.com/morluto/rea/tree/4b8e744d90579e353371649047215c4e4be7a5f6/src/dotnet), [src/firmware](https://github.com/morluto/rea/tree/4b8e744d90579e353371649047215c4e4be7a5f6/src/firmware), and [src/evm](https://github.com/morluto/rea/tree/4b8e744d90579e353371649047215c4e4be7a5f6/src/evm) talk to specific engines or parsers.
5. Domain models under [src/domain](https://github.com/morluto/rea/tree/4b8e744d90579e353371649047215c4e4be7a5f6/src/domain) keep the results provider-neutral.

That separation is visible in [src/server/createServer.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/server/createServer.ts): the server does not do analysis itself. It registers binary tools, configured analysis tools, observation tools, prompts, and session tools around application services and provider ports.

### Main layers

The session layer is [src/application/binary/BinarySession.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/application/binary/BinarySession.ts). It owns one active target, serializes target transitions, drains in-flight calls before switching, starts provider clients, retries cleanup, records run IDs, retains evidence, and exports snapshots. That is the central object that prevents the MCP server from becoming a bag of stateless calls with unclear ownership.

The provider-selection layer is [src/application/binary/AnalysisProviderRegistry.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/application/binary/AnalysisProviderRegistry.ts). It discovers candidate providers, validates provider IDs, evaluates availability and target support, handles `auto`, rejects ambiguous choices, and returns structured selection errors. The useful detail is that provider ordering is made deterministic and registration order is not allowed to leak into user-visible behavior.

The direct CLI layer is [src/application/DirectAnalysis.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/application/DirectAnalysis.ts). It opens a target, executes one operation, records evidence, optionally uses or writes an analysis snapshot, and always releases provider resources. It mirrors the MCP semantics enough that CLI and MCP are not two separate products.

The evidence/result layer is spread across [src/domain/evidence.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/domain/evidence.ts), [src/server/toolResult.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/server/toolResult.ts), [src/server/EvidenceMcpServer.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/server/EvidenceMcpServer.ts), and [src/application/investigation](https://github.com/morluto/rea/tree/4b8e744d90579e353371649047215c4e4be7a5f6/src/application/investigation). The design goal is that evidence can be complete, retained, paged through views, exported, compared, and tied back to provider/version/target identity.

### Request / data / control flow

For MCP, [src/main.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/main.ts) snapshots the environment, parses config, creates a logger, builds a session through [src/composition/binary.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/composition/binary.ts), optionally opens an initial target through [src/main/startup.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/main/startup.ts), and starts transport through [src/main/transport.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/main/transport.ts). Shutdown handling in [src/main/shutdown.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/main/shutdown.ts) closes provider resources on EOF or signals.

When a user opens a binary, [src/application/binary/BinarySessionOpen.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/application/binary/BinarySessionOpen.ts) resolves the target, [src/application/binary/SessionProviderRouter.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/application/binary/SessionProviderRouter.ts) routes it, and [src/application/binary/BinarySessionExecution.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/application/binary/BinarySessionExecution.ts) binds an execution target and profile. Subsequent tool calls run through `session.execute`, provider adapters return an `AnalysisExecution`, and the application/server layers wrap that into evidence.

For non-native or target-free work, [src/server/createServer.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/server/createServer.ts) registers services directly: web modules through [src/composition/webModules.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/composition/webModules.ts), web runtime through [src/composition/webRuntime.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/composition/webRuntime.ts), JavaScript recovery through [src/composition/javascriptRecovery.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/composition/javascriptRecovery.ts), firmware through [src/composition/firmware.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/composition/firmware.ts), EVM through [src/composition/evm.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/composition/evm.ts), and Android through [src/composition/android.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/composition/android.ts).

## Key directories and files

- [src/server/createServer.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/server/createServer.ts): the clearest map of the MCP tool surface and which services back each family.
- [src/application/binary/BinarySession.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/application/binary/BinarySession.ts): active target lifecycle, concurrent call draining, cleanup, status, evidence, and snapshot integration.
- [src/application/binary/AnalysisProviderRegistry.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/application/binary/AnalysisProviderRegistry.ts): deterministic deep-provider discovery and selection.
- [src/composition/binary.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/composition/binary.ts): production wiring for Hopper, Ghidra, IDA, managed static inspection, and lazy auxiliary providers.
- [src/application/DirectAnalysis.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/application/DirectAnalysis.ts): one-shot CLI execution, evidence creation, snapshot replay, and cleanup.
- [src/contracts](https://github.com/morluto/rea/tree/4b8e744d90579e353371649047215c4e4be7a5f6/src/contracts): the public API grammar for tools, examples, effects, and output schemas.
- [src/domain/javascript](https://github.com/morluto/rea/tree/4b8e744d90579e353371649047215c4e4be7a5f6/src/domain/javascript): static JavaScript, Electron, semantic graph, source-to-bundle, runtime reconciliation, and feature-trace models.
- [src/application/javascript](https://github.com/morluto/rea/tree/4b8e744d90579e353371649047215c4e4be7a5f6/src/application/javascript): workflow services around JavaScript application analysis, Electron observation, recovery, runtime observation, and semantic traces.
- [docs/mcp-contracts.md](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/docs/mcp-contracts.md): live-server identity, tool availability, result budgets, retained evidence, progress, cancellation, and transport-size behavior.
- [skill-src/reverse-engineer-anything/SKILL.md](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/skill-src/reverse-engineer-anything/SKILL.md): the agent operating manual that routes target types and insists on evidence/unknown discipline.

## Important components

- `createServer` in [src/server/createServer.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/server/createServer.ts): constructs an `EvidenceMcpServer`, installs availability policy, registers native, artifact, managed, web, browser, Electron, JavaScript runtime, Android, firmware, EVM, and session tools.
- `BinarySession` in [src/application/binary/BinarySession.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/application/binary/BinarySession.ts): the session state machine, not just a bag of providers.
- `AnalysisProviderRegistry` in [src/application/binary/AnalysisProviderRegistry.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/application/binary/AnalysisProviderRegistry.ts): separates candidate discovery from client startup and makes ambiguity explicit.
- `runDirectAnalysis` in [src/application/DirectAnalysis.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/application/DirectAnalysis.ts): shows how the CLI preserves the same evidence profile and cleanup model as MCP.
- `EnhancedTools` in [src/application/EnhancedTools.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/application/EnhancedTools.ts): workflow-style tools such as `binary_overview`, `trace_feature`, and native UI/value tracing.
- `EvidenceMcpServer` in [src/server/EvidenceMcpServer.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/server/EvidenceMcpServer.ts): the custom MCP wrapper that ties tool responses to retained evidence.

## Important knobs / configs / extension points

- Provider selection is controlled by config parsed in [src/config/parseConfig.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/config/parseConfig.ts) and honored by [src/application/binary/AnalysisProviderRegistry.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/application/binary/AnalysisProviderRegistry.ts).
- MCP response budget is handled through [src/config/mcpResponseBudget.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/config/mcpResponseBudget.ts) and documented in [docs/mcp-contracts.md](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/docs/mcp-contracts.md). Large evidence should be retained and viewed/exported instead of shoved through one response.
- Ghidra startup timing is configurable through [src/config/ghidraStartupTimeout.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/config/ghidraStartupTimeout.ts) and documented in [docs/mcp-contracts.md](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/docs/mcp-contracts.md).
- Optional provider availability comes from [src/composition/optionalObservationProviders.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/composition/optionalObservationProviders.ts) and is projected into session tool availability by [src/server/sessionAvailabilityPolicy.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/server/sessionAvailabilityPolicy.ts).
- The shipped skill is generated from [skill-src/reverse-engineer-anything](https://github.com/morluto/rea/tree/4b8e744d90579e353371649047215c4e4be7a5f6/skill-src/reverse-engineer-anything), which is a product surface, not just docs.

## Practical questions and answers

Q: Is this mainly a disassembler wrapper?  
A: No. Hopper, Ghidra, and IDA are one provider family. The larger product is a normalized evidence layer across binaries, bundles, browser runtime, JavaScript graphs, managed metadata, firmware, Android, EVM, process capture, and retained comparisons.

Q: Where is the key architecture decision?  
A: The key decision is in [src/application/binary/BinarySession.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/application/binary/BinarySession.ts): keep one active target with controlled transitions, provider profile, run ID, evidence, and cleanup. That gives long-lived MCP sessions enough state to be useful without hiding target ownership.

Q: How does it avoid model-facing tool chaos?  
A: The tool catalog is centralized through [src/contracts](https://github.com/morluto/rea/tree/4b8e744d90579e353371649047215c4e4be7a5f6/src/contracts), registered through [src/server/createServer.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/server/createServer.ts), and documented in [docs/mcp-contracts.md](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/docs/mcp-contracts.md). Availability changes per target, but the catalog does not churn.

Q: What would break first in production?  
A: Provider dependencies and host capabilities. Hopper, Ghidra, IDA, Chrome, JADX, Binwalk, Unblob, pwntools, and platform-specific helpers are inherently uneven. REA handles this better than most by making availability and remediation explicit, but the operational burden is real.

Q: What should a builder copy?  
A: Copy the discipline: typed contracts, evidence records, retained large results, explicit unknowns, provider-neutral domain objects, and one ownership model for target lifecycle.

## What is smart

The smartest move is treating reverse engineering as evidence management. [docs/mcp-contracts.md](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/docs/mcp-contracts.md) says evidence-producing tools return complete canonical evidence, retain it in the session bundle, and provide alternate views/export paths when transport is too small. That is exactly the right posture for agent tools that produce large, high-stakes observations.

The second smart move is keeping provider selection deterministic and explicit. [src/application/binary/AnalysisProviderRegistry.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/application/binary/AnalysisProviderRegistry.ts) sorts providers, separates availability from target support, and errors on ambiguity. That avoids mysterious "it chose a different engine today" behavior.

The third smart move is shipping the agent instructions as source. [skill-src/reverse-engineer-anything/SKILL.md](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/skill-src/reverse-engineer-anything/SKILL.md) is not fluff. It tells agents when to use REA, how to route target types, when not to run diagnostics, how to preserve evidence, and how to avoid pretending static analysis observed runtime behavior.

## What is flawed or weak

The surface area is huge. A repo with [src/browser](https://github.com/morluto/rea/tree/4b8e744d90579e353371649047215c4e4be7a5f6/src/browser), [src/native](https://github.com/morluto/rea/tree/4b8e744d90579e353371649047215c4e4be7a5f6/src/native), [src/ghidra](https://github.com/morluto/rea/tree/4b8e744d90579e353371649047215c4e4be7a5f6/src/ghidra), [src/hopper](https://github.com/morluto/rea/tree/4b8e744d90579e353371649047215c4e4be7a5f6/src/hopper), [src/android](https://github.com/morluto/rea/tree/4b8e744d90579e353371649047215c4e4be7a5f6/src/android), [src/dotnet](https://github.com/morluto/rea/tree/4b8e744d90579e353371649047215c4e4be7a5f6/src/dotnet), [src/firmware](https://github.com/morluto/rea/tree/4b8e744d90579e353371649047215c4e4be7a5f6/src/firmware), and [src/evm](https://github.com/morluto/rea/tree/4b8e744d90579e353371649047215c4e4be7a5f6/src/evm) is powerful, but the cognitive load for contributors is high.

The dependency story is necessarily messy. The project tries to be honest about prerequisites in [README.md](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/README.md) and [skill-src/reverse-engineer-anything/SKILL.md](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/skill-src/reverse-engineer-anything/SKILL.md), but users will still hit platform, version, GUI, Java, browser, and external-tool friction.

The broad tool catalog could also overwhelm weaker agents. The built-in skill helps, and session availability helps, but this product still depends on the calling agent being able to choose a sensible operation from a large set.

## What we can learn / steal

Steal the "complete result plus retained evidence" pattern. For any serious local tool, especially one that can produce large analyses, make the first-class record durable and viewable rather than trimming facts to fit a chat response.

Steal the provider-neutral domain split. [src/domain](https://github.com/morluto/rea/tree/4b8e744d90579e353371649047215c4e4be7a5f6/src/domain) lets provider adapters be weird while application services and user-facing contracts stay stable.

Steal the target lifecycle model. [src/application/binary/BinarySession.ts](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/src/application/binary/BinarySession.ts) serializes target transitions, drains calls, closes providers, and records status. That is applicable to any MCP server that controls external processes.

Steal the skill-as-product idea. [skill-src/reverse-engineer-anything/SKILL.md](https://github.com/morluto/rea/blob/4b8e744d90579e353371649047215c4e4be7a5f6/skill-src/reverse-engineer-anything/SKILL.md) makes operational behavior part of the release, which matters when the tool is meant for agents rather than only humans.

## How we could apply it

For our own builder tools, REA suggests a concrete pattern: define contracts first, keep adapters thin, retain evidence records, expose availability separately from existence, and write the agent operating manual in the repo. If we built a local analysis server for design systems, data pipelines, infrastructure, or product analytics, this architecture would translate well.

The biggest direct application is to any workflow where the agent must explain claims later. REA's evidence bundle pattern would help make "why did the agent say that?" answerable without replaying the whole investigation.

## Bottom line

REA is a serious agent tooling repo because it treats reverse engineering as structured, source-grounded evidence work. The repo is large and operationally complex, but the architecture is worth studying: contracts, provider routing, session ownership, retained evidence, and agent-facing instructions all reinforce the same idea.
