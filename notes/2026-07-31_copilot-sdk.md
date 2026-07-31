# GitHub Copilot SDK

- Repo: `github/copilot-sdk`
- URL: https://github.com/github/copilot-sdk
- Date: 2026-07-31
- Repo snapshot studied: `main` @ `20be013b016ad0251a2610237bd91ca14e01909f`
- Why picked today: It appeared on GitHub's daily trending page when checked, and the repository API already showed 10,093 stars and 1,367 forks. More importantly, it is a rare public look at a production agent runtime that GitHub chose to wrap as six language SDKs instead of one demo app.

## Executive summary
`copilot-sdk` is not mainly a pile of language bindings. The real product is a stable agent-runtime contract around the Copilot CLI server: one protocol version in [`sdk-protocol-version.json`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/sdk-protocol-version.json), one codegen pipeline in [`scripts/codegen`](https://github.com/github/copilot-sdk/tree/20be013b016ad0251a2610237bd91ca14e01909f/scripts/codegen), generated RPC/event surfaces in [`nodejs/src/generated`](https://github.com/github/copilot-sdk/tree/20be013b016ad0251a2610237bd91ca14e01909f/nodejs/src/generated), [`python/copilot/generated`](https://github.com/github/copilot-sdk/tree/20be013b016ad0251a2610237bd91ca14e01909f/python/copilot/generated), and equivalent directories in the other SDKs, plus thin client/session wrappers that route tools, permissions, MCP auth, and hooks into that runtime.

The strongest engineering move is transport decoupling. [`nodejs/src/ffiRuntimeHost.ts`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/nodejs/src/ffiRuntimeHost.ts) and [`python/copilot/_ffi_runtime_host.py`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/python/copilot/_ffi_runtime_host.py) explicitly say the in-process path still speaks the same `Content-Length`-framed JSON-RPC as the CLI process path. That means the runtime can move between child-process and in-process FFI hosting without forking the higher-level SDK behavior.

The second strong move is session-scoped extensibility without giving up one shared core. [`docs/features/hooks.md`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/docs/features/hooks.md) and [`docs/features/mcp.md`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/docs/features/mcp.md) show how GitHub is productizing the same runtime around hooks, MCP servers, session filesystems, permission handlers, and custom agents instead of hard-coding one fixed assistant personality.

## What they built
They built a multi-language SDK family for embedding the Copilot agent runtime inside other apps and services:

- [`README.md`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/README.md) frames the repo as SDKs for Node.js, Python, Go, .NET, Java, and Rust.
- [`docs/getting-started.md`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/docs/getting-started.md) shows the basic create-session, send-message, wait-for-response loop across languages.
- [`nodejs/src/client.ts`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/nodejs/src/client.ts) and [`python/copilot/client.py`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/python/copilot/client.py) are the main SDK entrypoints.
- [`nodejs/src/session.ts`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/nodejs/src/session.ts) and [`python/copilot/session.py`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/python/copilot/session.py) own per-session event routing and response handling.
- [`scripts/codegen/typescript.ts`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/scripts/codegen/typescript.ts) and the sibling generators under [`scripts/codegen`](https://github.com/github/copilot-sdk/tree/20be013b016ad0251a2610237bd91ca14e01909f/scripts/codegen) generate typed RPC and session-event bindings.
- [`test/harness`](https://github.com/github/copilot-sdk/tree/20be013b016ad0251a2610237bd91ca14e01909f/test/harness), [`test/snapshots`](https://github.com/github/copilot-sdk/tree/20be013b016ad0251a2610237bd91ca14e01909f/test/snapshots), [`nodejs/test/e2e`](https://github.com/github/copilot-sdk/tree/20be013b016ad0251a2610237bd91ca14e01909f/nodejs/test/e2e), and [`python/e2e`](https://github.com/github/copilot-sdk/tree/20be013b016ad0251a2610237bd91ca14e01909f/python/e2e) test the contract from several language edges.

## Why it matters
This repo matters because most agent SDKs still cheat. They either hard-code a single provider flow, or they hand-wave the runtime and ship only pretty examples. This repo shows the boring part that usually gets hidden:

1. A versioned wire contract that multiple SDKs can share.
2. A session object that has to coordinate tools, permissions, hooks, MCP, and lifecycle events.
3. A test harness that treats full conversation traces as contract fixtures, not just unit-test trivia.

## Repo shape at a glance
The repository is large, but it is structurally legible:

- [`docs`](https://github.com/github/copilot-sdk/tree/20be013b016ad0251a2610237bd91ca14e01909f/docs): product and feature docs for setup, auth, hooks, MCP, sessions, and observability.
- [`nodejs`](https://github.com/github/copilot-sdk/tree/20be013b016ad0251a2610237bd91ca14e01909f/nodejs), [`python`](https://github.com/github/copilot-sdk/tree/20be013b016ad0251a2610237bd91ca14e01909f/python), [`go`](https://github.com/github/copilot-sdk/tree/20be013b016ad0251a2610237bd91ca14e01909f/go), [`dotnet`](https://github.com/github/copilot-sdk/tree/20be013b016ad0251a2610237bd91ca14e01909f/dotnet), [`java`](https://github.com/github/copilot-sdk/tree/20be013b016ad0251a2610237bd91ca14e01909f/java), [`rust`](https://github.com/github/copilot-sdk/tree/20be013b016ad0251a2610237bd91ca14e01909f/rust): six language-specific envelopes around the same runtime concepts.
- [`scripts/codegen`](https://github.com/github/copilot-sdk/tree/20be013b016ad0251a2610237bd91ca14e01909f/scripts/codegen): schema-driven generation of typed RPC/event surfaces.
- [`test/harness`](https://github.com/github/copilot-sdk/tree/20be013b016ad0251a2610237bd91ca14e01909f/test/harness): shared proxies, MCP fixture servers, adapters, and replay helpers.
- [`test/snapshots`](https://github.com/github/copilot-sdk/tree/20be013b016ad0251a2610237bd91ca14e01909f/test/snapshots): YAML trace fixtures for end-to-end behavior.
- [`.github/workflows`](https://github.com/github/copilot-sdk/tree/20be013b016ad0251a2610237bd91ca14e01909f/.github/workflows): cross-language codegen, publish, tests, and maintenance automation.

## Layered architecture dissection
### High-level system shape
The system shape is: app code instantiates a language client, the client starts or connects to a Copilot runtime, verifies the shared protocol version, creates a session, sends prompts over typed JSON-RPC, receives streaming session events, and routes any tool/permission/hook/MCP-auth requests back into user-provided handlers before the assistant turn can continue.

The repo's key idea is that the application-facing API should feel native in each language while the runtime-facing contract stays centralized and generated.

### Main layers
**1. Packaging and onboarding layer**  
[`README.md`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/README.md) and [`docs/getting-started.md`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/docs/getting-started.md) define the product surface. The docs are not fluff here; they mirror the core SDK lifecycle closely enough that you can infer the important objects before reading code.

**2. Protocol and codegen layer**  
[`sdk-protocol-version.json`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/sdk-protocol-version.json) pins protocol version `3`. [`scripts/codegen/typescript.ts`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/scripts/codegen/typescript.ts) makes the design choice explicit: generate session-event types, typed server-scoped RPC, typed session-scoped RPC, and handler registration from schemas instead of hand-maintaining the contract in every language. The generated output then lands in [`nodejs/src/generated`](https://github.com/github/copilot-sdk/tree/20be013b016ad0251a2610237bd91ca14e01909f/nodejs/src/generated) and peer directories.

**3. Runtime transport layer**  
[`nodejs/src/ffiRuntimeHost.ts`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/nodejs/src/ffiRuntimeHost.ts) and [`python/copilot/_ffi_runtime_host.py`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/python/copilot/_ffi_runtime_host.py) are the cleanest files in the repo because they explain the actual runtime trick: load `runtime.node` or the platform cdylib, keep JSON-RPC framing unchanged, and expose a process-like adapter so the higher layers do not care whether the runtime is local FFI, CLI stdio, or TCP.

**4. Client and session orchestration layer**  
[`nodejs/src/client.ts`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/nodejs/src/client.ts) owns startup, protocol verification, `sessionFs` registration, request-handler registration, and session bookkeeping. [`nodejs/src/session.ts`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/nodejs/src/session.ts) owns the harder control logic: send requests, wait for `session.idle`, dispatch typed events, and react to `external_tool.requested`, `permission.requested`, `mcp.oauth_required`, `command.execute`, and `elicitation.requested`. The Python SDK mirrors the same shapes in [`python/copilot/client.py`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/python/copilot/client.py).

**5. Extensibility and policy layer**  
[`docs/features/hooks.md`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/docs/features/hooks.md) and [`docs/features/mcp.md`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/docs/features/mcp.md) show where GitHub expects builders to intervene. This is where the SDK stops being "ask a chat model" and becomes an agent host with controllable tool boundaries, MCP server mounting, and user-defined lifecycle interception.

**6. Contract-testing layer**  
[`test/harness`](https://github.com/github/copilot-sdk/tree/20be013b016ad0251a2610237bd91ca14e01909f/test/harness) and [`test/snapshots`](https://github.com/github/copilot-sdk/tree/20be013b016ad0251a2610237bd91ca14e01909f/test/snapshots) are not ancillary. A file like [`test/snapshots/combinedconfiguration/accept_mcp_servers_and_custom_agents.yaml`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/test/snapshots/combinedconfiguration/accept_mcp_servers_and_custom_agents.yaml) shows that the repo treats session behavior as replayable protocol evidence, not just incidental output.

### Request / data / control flow
1. Application code starts from [`docs/getting-started.md`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/docs/getting-started.md): create `CopilotClient`, then create a session.
2. [`nodejs/src/client.ts`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/nodejs/src/client.ts) starts either the CLI server or the in-process FFI runtime, connects, and verifies protocol compatibility against [`sdk-protocol-version.json`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/sdk-protocol-version.json).
3. The client optionally registers session filesystem and LLM request-provider hooks so runtime requests can be intercepted or redirected.
4. [`nodejs/src/session.ts`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/nodejs/src/session.ts) sends `session.send`, listens for streaming events, and resolves `sendAndWait` only after the runtime emits `session.idle`.
5. If the runtime needs external help, the session routes `external_tool.requested`, `permission.requested`, `mcp.oauth_required`, `command.execute`, or elicitation events back into local handlers.
6. Hooks are routed through generated RPC registration and the session-specific dispatcher, so one global connection can still resolve behavior per session.

## Key directories and files
- [`sdk-protocol-version.json`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/sdk-protocol-version.json): the simplest but most important contract file.
- [`scripts/codegen/typescript.ts`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/scripts/codegen/typescript.ts): clearest statement of the repo's schema-first philosophy.
- [`nodejs/src/client.ts`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/nodejs/src/client.ts): startup, session registry, provider registration, and lifecycle cleanup.
- [`nodejs/src/session.ts`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/nodejs/src/session.ts): session state machine and handler dispatch.
- [`nodejs/src/ffiRuntimeHost.ts`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/nodejs/src/ffiRuntimeHost.ts): in-process transport swap.
- [`python/copilot/client.py`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/python/copilot/client.py): same architecture translated into Python.
- [`python/copilot/_ffi_runtime_host.py`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/python/copilot/_ffi_runtime_host.py): the best prose explanation of the runtime ABI in the repo.
- [`docs/features/hooks.md`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/docs/features/hooks.md) and [`docs/features/mcp.md`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/docs/features/mcp.md): extension surface.
- [`test/harness`](https://github.com/github/copilot-sdk/tree/20be013b016ad0251a2610237bd91ca14e01909f/test/harness) and [`test/snapshots`](https://github.com/github/copilot-sdk/tree/20be013b016ad0251a2610237bd91ca14e01909f/test/snapshots): contract tests and replay fixtures.

## Important components
The most important component is the generated RPC/event layer, especially [`scripts/codegen/typescript.ts`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/scripts/codegen/typescript.ts). It is the reason the repo can support many SDKs without turning into six incompatible hand-written clients.

The second is [`nodejs/src/client.ts`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/nodejs/src/client.ts). That file proves the SDK is really a runtime host with policy knobs, not just a text-chat wrapper.

The third is [`nodejs/src/session.ts`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/nodejs/src/session.ts). This is where the repo becomes agent infrastructure: event streams, permission gating, external-tool execution, MCP auth, and user elicitation all converge there.

The fourth is [`nodejs/src/ffiRuntimeHost.ts`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/nodejs/src/ffiRuntimeHost.ts) plus [`python/copilot/_ffi_runtime_host.py`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/python/copilot/_ffi_runtime_host.py). Those files make the transport story honest instead of magical.

## Important knobs / configs / extension points
- Protocol compatibility is pinned by [`sdk-protocol-version.json`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/sdk-protocol-version.json).
- MCP mounting lives in the `mcpServers` session config documented in [`docs/features/mcp.md`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/docs/features/mcp.md).
- Hook interception lives in the `hooks` session config documented in [`docs/features/hooks.md`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/docs/features/hooks.md).
- Runtime hosting mode lives in files like [`nodejs/src/ffiRuntimeHost.ts`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/nodejs/src/ffiRuntimeHost.ts) and [`python/copilot/_ffi_runtime_host.py`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/python/copilot/_ffi_runtime_host.py).
- Session filesystem and provider interception are wired through [`nodejs/src/client.ts`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/nodejs/src/client.ts) and the session-fs provider files in each SDK.
- The test harness and snapshot fixtures are themselves an extension point for safe evolution because they constrain behavioral drift.

## Practical questions and answers
**Is this just a thin shell around the Copilot CLI?**  
Not really. It is intentionally a shell around the runtime, but that shell is doing nontrivial work: generated RPC typing, transport abstraction, session lifecycle, handler routing, filesystem/session persistence registration, and language-native APIs.

**Where should a builder start reading?**  
Start with [`README.md`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/README.md), then [`docs/getting-started.md`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/docs/getting-started.md), then [`nodejs/src/client.ts`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/nodejs/src/client.ts), [`nodejs/src/session.ts`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/nodejs/src/session.ts), and [`scripts/codegen/typescript.ts`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/scripts/codegen/typescript.ts).

**What is the most reusable move here?**  
Keep the public SDK APIs language-native, but generate the runtime contract from one schema set and make transport a swap rather than a fork.

**Why do the tests matter so much here?**  
Because agent runtimes fail at behavior edges. A YAML snapshot like [`test/snapshots/combinedconfiguration/accept_mcp_servers_and_custom_agents.yaml`](https://github.com/github/copilot-sdk/blob/20be013b016ad0251a2610237bd91ca14e01909f/test/snapshots/combinedconfiguration/accept_mcp_servers_and_custom_agents.yaml) is a better guardrail than a vague integration checklist.

## What is smart
- One protocol version and one codegen story across six SDKs.
- Swapping child-process hosting for in-process FFI without changing JSON-RPC semantics.
- Treating hooks, MCP, permissions, and elicitation as first-class session events instead of undocumented side channels.
- Backing the public API with replayable harnesses and snapshot traces.

## What is flawed or weak
- A lot of the real behavior still disappears into the bundled runtime, so the repo is only partially inspectable.
- The generated surface is huge, which makes local navigation noisier than the clean architecture pitch suggests.
- Cross-language duplication is disciplined, but still expensive; every SDK has its own packaging, tests, and edge cases.
- The repo's elegance depends on schema and codegen discipline. If that slips, the multi-language promise gets expensive fast.

## What we can learn / steal
- Define the wire contract once and generate wrappers everywhere else.
- Keep transport details behind a process-like abstraction so the rest of the client stack stays stable.
- Treat session lifecycle and tool-routing events as product features, not incidental callbacks.
- Use replayable snapshots to keep agent behavior changes visible.

## How we could apply it
If we ever ship our own agent SDK, I would copy the protocol-first approach almost verbatim: schema-driven types, thin language shells, transport swappability, and contract fixtures. I would be more cautious about multiplying official language SDKs unless the protocol and release tooling were already this disciplined.

## Bottom line
`github/copilot-sdk` is worth studying because it shows what an agent SDK looks like when a company takes runtime hosting, protocol stability, extensibility, and behavioral testing seriously.

The builder lesson is that the hard part is not just "let apps call the assistant." The hard part is designing a stable session contract that can survive hooks, tools, MCP, multiple transports, and six language front doors without collapsing into bespoke glue.
