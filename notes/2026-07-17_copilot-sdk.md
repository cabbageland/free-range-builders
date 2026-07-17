# GitHub Copilot CLI SDKs

- Repo: `github/copilot-sdk`
- URL: https://github.com/github/copilot-sdk
- Date: 2026-07-17
- Repo snapshot studied: `main` @ `c4dc3e959cc5c3bb945a4c920376dabc969f5942`
- Why picked today: This is a hot official GitHub repo, but the better reason to study it is architectural. It is not six unrelated SDKs. It is one agent runtime and protocol contract, exposed through language-native shells with different installation and transport strategies.

## Executive summary
`copilot-sdk` is best understood as a compatibility monorepo around a single agent engine. The headline in [`README.md`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/README.md) is "agents for every app," but the important design choice is lower level: every language binding talks to the same Copilot runtime over JSON-RPC, and the repo freezes that shared contract in [`sdk-protocol-version.json`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/sdk-protocol-version.json).

The strongest builder move is that the repo separates "language ergonomics" from "agent behavior." [`nodejs/src/client.ts`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/nodejs/src/client.ts) and [`python/copilot/client.py`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/python/copilot/client.py) expose idiomatic clients, but neither reimplements planning, tool orchestration, or session semantics. They are transport, lifecycle, and callback adapters around the same runtime contract documented in [`docs/getting-started.md`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/docs/getting-started.md).

The second smart move is that transport is swappable without changing the wire model. [`nodejs/src/ffiRuntimeHost.ts`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/nodejs/src/ffiRuntimeHost.ts) explicitly says the in-process host still pumps LSP-style `Content-Length` JSON-RPC frames; the transport changes, not the protocol. That is the right kind of flexibility.

The cost is obvious too. A repo with [`nodejs/`](https://github.com/github/copilot-sdk/tree/c4dc3e959cc5c3bb945a4c920376dabc969f5942/nodejs), [`python/`](https://github.com/github/copilot-sdk/tree/c4dc3e959cc5c3bb945a4c920376dabc969f5942/python), [`go/`](https://github.com/github/copilot-sdk/tree/c4dc3e959cc5c3bb945a4c920376dabc969f5942/go), [`dotnet/`](https://github.com/github/copilot-sdk/tree/c4dc3e959cc5c3bb945a4c920376dabc969f5942/dotnet), [`java/`](https://github.com/github/copilot-sdk/tree/c4dc3e959cc5c3bb945a4c920376dabc969f5942/java), and [`rust/`](https://github.com/github/copilot-sdk/tree/c4dc3e959cc5c3bb945a4c920376dabc969f5942/rust) now owns six public SDK surfaces plus the runtime packaging matrix behind them.

## What they built
They built a multi-language shell around the Copilot CLI runtime:

- [`README.md`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/README.md) presents the repo as a programmatic entrypoint to the same engine behind Copilot CLI.
- [`docs/getting-started.md`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/docs/getting-started.md) shows the common interaction model across languages: create client, create session, send prompt, handle tools and permissions.
- [`nodejs/src/client.ts`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/nodejs/src/client.ts) and [`python/copilot/client.py`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/python/copilot/client.py) are representative control-plane clients.
- [`nodejs/src/ffiRuntimeHost.ts`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/nodejs/src/ffiRuntimeHost.ts) adds an in-process hosting path for Node.
- [`rust/src/embeddedcli.rs`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/rust/src/embeddedcli.rs) handles lazy installation and integrity verification of bundled runtime bits.

## Why it matters
This repo matters because it treats agent embedding as a protocol and packaging problem, not as six separate framework rewrites.

1. It keeps one durable runtime and lets each language own only local ergonomics.
2. It makes compatibility explicit with a shared protocol version instead of letting each SDK drift.
3. It exposes a reusable product lesson: when agent behavior is centralized, transport, installation, and auth can vary per platform without fragmenting the core.

## Repo shape at a glance
The top-level tree is unusually honest about what the product is:

- [`sdk-protocol-version.json`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/sdk-protocol-version.json) is the hard compatibility pin.
- [`docs/`](https://github.com/github/copilot-sdk/tree/c4dc3e959cc5c3bb945a4c920376dabc969f5942/docs) explains setup modes, auth, and session flow.
- [`nodejs/`](https://github.com/github/copilot-sdk/tree/c4dc3e959cc5c3bb945a4c920376dabc969f5942/nodejs), [`python/`](https://github.com/github/copilot-sdk/tree/c4dc3e959cc5c3bb945a4c920376dabc969f5942/python), [`go/`](https://github.com/github/copilot-sdk/tree/c4dc3e959cc5c3bb945a4c920376dabc969f5942/go), [`dotnet/`](https://github.com/github/copilot-sdk/tree/c4dc3e959cc5c3bb945a4c920376dabc969f5942/dotnet), [`java/`](https://github.com/github/copilot-sdk/tree/c4dc3e959cc5c3bb945a4c920376dabc969f5942/java), and [`rust/`](https://github.com/github/copilot-sdk/tree/c4dc3e959cc5c3bb945a4c920376dabc969f5942/rust) are peer SDK packages, not plugins around one dominant language.
- [`test/harness`](https://github.com/github/copilot-sdk/tree/c4dc3e959cc5c3bb945a4c920376dabc969f5942/test/harness) contains replay proxies, protocol adapters, mock handlers, and test MCP servers, which tells you the team is testing wire behavior, not just happy-path docs.

## Layered architecture dissection
### High-level system shape
The core shape is simple. Application code calls a language SDK, the SDK starts or connects to the Copilot runtime, then everything goes over JSON-RPC. [`README.md`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/README.md) spells this out directly, and the Node client in [`nodejs/src/client.ts`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/nodejs/src/client.ts) implements that lifecycle concretely with `vscode-jsonrpc`.

### Main layers
**1. Product and setup layer**  
[`README.md`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/README.md), [`docs/getting-started.md`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/docs/getting-started.md), and [`docs/setup/bundled-cli.md`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/docs/setup/bundled-cli.md) define the supported operating modes: bundled runtime, external CLI, auth patterns, and BYOK.

**2. Language-shell layer**  
[`nodejs/src/client.ts`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/nodejs/src/client.ts) and [`python/copilot/client.py`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/python/copilot/client.py) expose language-native session APIs, permission handlers, tool adapters, bearer-token callbacks, and telemetry hooks.

**3. Shared protocol layer**  
[`sdk-protocol-version.json`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/sdk-protocol-version.json) declares protocol version `3`, and [`nodejs/src/client.ts`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/nodejs/src/client.ts) enforces `MIN_PROTOCOL_VERSION = 3`. That is the real cross-language contract.

**4. Runtime transport layer**  
The default model is child-process hosting over stdio, described in [`docs/setup/bundled-cli.md`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/docs/setup/bundled-cli.md). The alternative path is in-process hosting via [`nodejs/src/ffiRuntimeHost.ts`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/nodejs/src/ffiRuntimeHost.ts), which loads a native runtime library and still feeds framed JSON-RPC to the same higher-level client machinery.

**5. Packaging and integrity layer**  
[`rust/src/embeddedcli.rs`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/rust/src/embeddedcli.rs) is where the repo gets serious about shipping the runtime safely. It lazily installs the bundled CLI, verifies bytes, publishes atomically, and rechecks on later runs so consumers do not quietly execute a truncated or quarantined binary.

### Request / data / control flow
The basic control flow is straightforward and good:

1. App code instantiates a client using one of the SDK entrypoints shown in [`docs/getting-started.md`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/docs/getting-started.md).
2. The client starts or resolves a compatible runtime, either as a child process per [`docs/setup/bundled-cli.md`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/docs/setup/bundled-cli.md) or through the in-process host in [`nodejs/src/ffiRuntimeHost.ts`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/nodejs/src/ffiRuntimeHost.ts).
3. [`nodejs/src/client.ts`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/nodejs/src/client.ts) or [`python/copilot/client.py`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/python/copilot/client.py) creates a session and registers permission, tool, and provider-token callbacks.
4. The app sends prompts and receives events over the shared JSON-RPC surface.
5. When the runtime needs a tool result, token, or filesystem/service adapter, the language shell hands control back to application code instead of baking those concerns into the runtime itself.

## Key directories and files
- [`README.md`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/README.md): product framing and six-SDK map.
- [`docs/getting-started.md`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/docs/getting-started.md): the shared session model.
- [`docs/setup/bundled-cli.md`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/docs/setup/bundled-cli.md): bundling matrix and default hosting path.
- [`sdk-protocol-version.json`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/sdk-protocol-version.json): compatibility pin.
- [`nodejs/src/client.ts`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/nodejs/src/client.ts): Node control plane and protocol gatekeeping.
- [`nodejs/src/ffiRuntimeHost.ts`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/nodejs/src/ffiRuntimeHost.ts): in-process runtime transport.
- [`python/copilot/client.py`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/python/copilot/client.py): Python surface with cloud, tool, and session options.
- [`rust/src/embeddedcli.rs`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/rust/src/embeddedcli.rs): runtime installation and integrity logic.
- [`test/harness`](https://github.com/github/copilot-sdk/tree/c4dc3e959cc5c3bb945a4c920376dabc969f5942/test/harness): protocol harness, replay proxies, and mock MCP servers.

## Important components
**The protocol version file is not decoration**  
[`sdk-protocol-version.json`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/sdk-protocol-version.json) plus `MIN_PROTOCOL_VERSION` in [`nodejs/src/client.ts`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/nodejs/src/client.ts) are the real center of gravity. That is how six SDKs avoid silent drift.

**`client.ts` is the Node control plane**  
It is not a thin example wrapper. [`nodejs/src/client.ts`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/nodejs/src/client.ts) owns connection lifecycle, timeout handling, callback serialization, JSON schema conversion for tools, and provider-token plumbing.

**`ffiRuntimeHost.ts` is a good transport abstraction test**  
[`nodejs/src/ffiRuntimeHost.ts`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/nodejs/src/ffiRuntimeHost.ts) proves the repo is serious about transport flexibility without inventing a second protocol.

**`embeddedcli.rs` is quiet but important product work**  
Most SDK repos hand-wave runtime installation. [`rust/src/embeddedcli.rs`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/rust/src/embeddedcli.rs) does not. It treats runtime extraction as a failure-prone systems problem.

## Important knobs / configs / extension points
- Auth strategy choices in [`docs/setup/bundled-cli.md`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/docs/setup/bundled-cli.md): signed-in CLI user, env-provided token, or BYOK.
- Provider and bearer-token callback plumbing in [`nodejs/src/client.ts`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/nodejs/src/client.ts) and [`python/copilot/client.py`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/python/copilot/client.py).
- Session modes, filesystem adapters, and tool wiring in [`python/copilot/client.py`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/python/copilot/client.py) and the Node client surface in [`nodejs/src/client.ts`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/nodejs/src/client.ts).
- Bundled versus external runtime decisions in [`docs/setup/bundled-cli.md`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/docs/setup/bundled-cli.md).

## Practical questions and answers
**Is this six separate SDK implementations?**  
No. The language surfaces differ, but the architecture keeps one runtime and one protocol contract. The repo structure and [`sdk-protocol-version.json`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/sdk-protocol-version.json) make that explicit.

**What is the most reusable idea here?**  
Treat agent embedding as a runtime boundary with callbacks for tools, auth, and permissions, instead of rewriting orchestration per language.

**What is the most production-minded file in the repo?**  
Probably [`rust/src/embeddedcli.rs`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/rust/src/embeddedcli.rs). The atomic publish and integrity recheck logic is the kind of boring robustness most SDKs skip.

**Where should a builder start reading?**  
Start with [`README.md`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/README.md), then [`docs/getting-started.md`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/docs/getting-started.md), [`docs/setup/bundled-cli.md`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/docs/setup/bundled-cli.md), [`nodejs/src/client.ts`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/nodejs/src/client.ts), and [`rust/src/embeddedcli.rs`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/rust/src/embeddedcli.rs).

## What is smart
- One runtime, many language shells, with the protocol contract made explicit.
- In-process FFI hosting in [`nodejs/src/ffiRuntimeHost.ts`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/nodejs/src/ffiRuntimeHost.ts) without inventing a second wire format.
- Real packaging discipline in [`rust/src/embeddedcli.rs`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/rust/src/embeddedcli.rs).
- Test infrastructure in [`test/harness`](https://github.com/github/copilot-sdk/tree/c4dc3e959cc5c3bb945a4c920376dabc969f5942/test/harness) that focuses on adapters and protocol behavior.

## What is flawed or weak
- The public surface area is large enough that language parity will become a permanent maintenance tax.
- Bundling rules are uneven by language, as shown in [`docs/setup/bundled-cli.md`](https://github.com/github/copilot-sdk/blob/c4dc3e959cc5c3bb945a4c920376dabc969f5942/docs/setup/bundled-cli.md), which means the developer experience is not truly uniform.
- The runtime is still an external product boundary, so SDK consumers inherit Copilot CLI behavior changes even when their own wrapper code stays stable.
- The in-process transport is elegant, but it also raises the debugging bar when native library loading goes wrong.

## What we can learn / steal
- Freeze cross-language agent behavior behind a versioned protocol instead of tribal knowledge.
- Keep tools, auth, and permissions as callbacks at the application boundary.
- Treat binary installation and integrity checks as first-class SDK concerns.
- Make alternate transports reuse the same wire model whenever possible.

## How we could apply it
If we wanted to ship our own agent into multiple app stacks, I would copy this structure:

1. one runtime with one protocol contract,
2. per-language SDK shells that stay thin,
3. explicit transport choices rather than transport-specific semantics,
4. serious runtime-installation logic instead of "download and hope."

That keeps the hard agent behavior centralized while still giving every host platform an idiomatic API.

## Bottom line
`copilot-sdk` is worth studying because it turns "embed an agent" from a prompt-wrapper exercise into a disciplined runtime product.

The builder lesson is that multi-language agent support gets easier when you standardize the runtime and protocol first, then let packaging and host-language ergonomics vary around that stable core.
