# Cua

- Repo: trycua/cua
- URL: https://github.com/trycua/cua
- Date: 2026-10-07
- Repo snapshot studied: main at c90e94662e9980b1b575512a9da9ae8710e28f69
- Why picked today: It was on GitHub daily trending, it had fresh same-day activity and roughly 28K stars, and it is not a thin agent wrapper. It is a large computer-use substrate: desktop driver, SDK, in-guest daemon, VM/container images, benchmarks, skills, and small specialist decision models.

## Executive summary

[trycua/cua](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69) is a monorepo for giving AI agents real computers to operate. The surface pitch is simple: Cua Spaces gives agents desktops, Cua Driver lets agents inspect and control apps, Lume runs local VMs, Cua SDK manages sandboxes, Cua Bench evaluates computer-use agents, and CUA-S1 explores small specialist decision models.

The source is interesting because it treats "computer use" as an infrastructure problem, not just as a prompt or a model. The repo has a host control plane in [libs/cua](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua), a cross-platform desktop automation layer in [libs/cua-driver](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-driver), an in-sandbox daemon in [libs/cua-spacesd](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-spacesd), machine images in [libs/images](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/images), evaluation code in [libs/cua-bench](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-bench), and research models in [libs/cua-s1](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-s1).

The key lesson is that agent desktops need contracts everywhere: capability probes, OS permission boundaries, runtime placement, media streams, auth tokens, session lifecycle, test fixtures, and benchmark outputs. The repo is broad and hard to onboard into, but the layering is unusually explicit.

## What they built

Cua is a source-available platform for agent-owned desktops and sandboxes. The root [README.md](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/README.md) lists the main product slices: Cua Spaces, Cua Driver, Lume, the Cua SDK and CLI, CUA-S1, and Cua Bench. Those are not just marketing cards. Most of them have source trees, package docs, installers, tests, and release machinery.

At the bottom, the repo can run machines and images through [libs/cua](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua), [libs/lume](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/lume), [libs/qemu-docker](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/qemu-docker), [libs/fleet](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/fleet), and [libs/images](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/images). Inside those machines, [libs/cua-spacesd](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-spacesd) exposes processes, files, desktop streams, input, teleport, tunnels, and system capabilities. Beside that, [libs/cua-driver](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-driver) is the desktop automation driver that speaks MCP/CLI/SDK and owns the platform-specific accessibility and input work.

The repo also includes evaluation and learning infrastructure. [libs/cua-bench](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-bench) runs computer-use benchmark tasks on local or cloud sandboxes and exports result and trajectory artifacts. [libs/cua-s1/MODEL_CARD.md](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-s1/MODEL_CARD.md) documents narrow specialist models for closed-option GUI decisions and form tasks.

## Why it matters

Computer-use agents fail on substrate details before they fail on reasoning. They need a desktop that is reachable, observable, streamable, and safe enough to share with a human. They need OS-specific permission grants. They need screenshots, accessibility trees, input delivery, clipboard semantics, windows, files, processes, service URLs, and task scoring. Cua is interesting because it pulls those concerns into named layers instead of hiding them behind one "agent browser" abstraction.

The repo also matters as a product architecture example. [libs/cua/crates/cua-sdk/src/lib.rs](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua/crates/cua-sdk/src/lib.rs) explicitly defines one SDK with embedded and daemon topologies. [libs/cua-driver/rust/crates/cua-driver/src/cli.rs](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-driver/rust/crates/cua-driver/src/cli.rs) exposes MCP, daemon, call, permissions, skills, updates, and extension management as real CLI surfaces. [libs/cua-spacesd/README.md](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-spacesd/README.md) spends serious space on auth, capabilities, media, relays, cursor shape, and packaging, which are usually the places agent demos quietly break.

## Repo shape at a glance

- [README.md](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/README.md): the product map and top-level package table.
- [libs/cua](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua): Rust-first SDK workspace, CLI, daemon, sandbox model, image handling, Spaces client, auth, media, teleport, host setup, and UniFFI bindings.
- [libs/cua-driver](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-driver): background desktop automation driver, MCP server, CLI, generated SDK bindings, platform crates, permission modes, perception extension, and E2E harnesses.
- [libs/cua-spacesd](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-spacesd): in-guest daemon and relay stack for processes, files, desktop, streams, input, teleport receive, tunnels, tokens, and capabilities.
- [libs/images](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/images): canonical Linux, Windows, macOS, Android, Omarchy, runtime, and benchmark image definitions.
- [libs/lume](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/lume) and [libs/qemu-docker](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/qemu-docker): local virtualization/runtime foundations.
- [libs/fleet](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/fleet): cloud fleet SDK, backend, Terraform provider, bindings, docs, and E2E material.
- [libs/cua-bench](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-bench): benchmark runner, task adapters, registry, exports, result files, and hermetic tests.
- [libs/cua-s1](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-s1): specialist computer-use model code, training and eval folders, security notes, and model card.
- [skills](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/skills), [samples](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/samples), [examples](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/examples), [docs](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/docs), and [rfcs](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/rfcs): user-facing integration material, architecture decisions, and design history.

## Layered architecture dissection

### High-level system shape

The system has five big planes.

The first is the SDK and CLI control plane in [libs/cua](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua). Its [README.md](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua/README.md) describes one API over embedded and daemon modes, with sandboxes, Fleet, local runtimes, Spaces, auth, media, teleport, and agent setup. [libs/cua/crates/cua-sdk/src/lib.rs](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua/crates/cua-sdk/src/lib.rs) is the binding boundary and the flat error surface foreign languages see.

The second is the machine/runtime plane. [libs/cua/crates/cua-vmm](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua/crates/cua-vmm), [libs/cua/crates/cua-image](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua/crates/cua-image), [libs/cua/crates/cua-fleet](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua/crates/cua-fleet), and [libs/cua/crates/cua-sandbox-core](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua/crates/cua-sandbox-core) split local runtimes, image resolution, cloud pools, and sandbox handles.

The third is the guest environment plane. [libs/cua-spacesd](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-spacesd) runs inside a Space or image and exposes the actual environment: processes, filesystem, desktop streams, input, tokens, relay, teleport receive, and features. Its crate split in [libs/cua-spacesd/crates](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-spacesd/crates) makes the server, desktop services, session model, relay, socks, teleport, and provider traits visible.

The fourth is the desktop-action plane. [libs/cua-driver](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-driver) owns native app inspection and control. Its Rust workspace has platform crates under [libs/cua-driver/rust/crates](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-driver/rust/crates), including [platform-macos](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-driver/rust/crates/platform-macos), [platform-linux](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-driver/rust/crates/platform-linux), [platform-windows](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-driver/rust/crates/platform-windows), [cua-driver-sdk](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-driver/rust/crates/cua-driver-sdk), and [cua-driver-core](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-driver/rust/crates/cua-driver-core).

The fifth is the measurement and research plane. [libs/cua-bench](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-bench) turns tasks into scored runs with traces, summaries, targets, and dataset registry entries. [libs/cua-s1/MODEL_CARD.md](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-s1/MODEL_CARD.md) is unusually candid about narrow task contracts and out-of-distribution failure modes.

### Main layers

The SDK layer is built around one exported crate. [libs/cua/crates/cua-sdk/src/lib.rs](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua/crates/cua-sdk/src/lib.rs) says `cua-sdk` is the only `#[uniffi::export]` crate and presents one object model across sandboxes, spacesd clients, media sessions, Fleet, local runtimes, Spaces, teleport, auth, and agent setup. That keeps Python, Node, Swift, Kotlin, and wasm from each inventing their own contract.

The daemon layer exists twice, on purpose. [libs/cua/crates/cua-daemon](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua/crates/cua-daemon) is the shared SDK runtime host for sandboxes, sockets, webview media, and MCP. [libs/cua-driver/rust/crates/cua-driver/src/serve.rs](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-driver/rust/crates/cua-driver/src/serve.rs) is the local desktop driver daemon, using line-delimited JSON over a Unix socket or Windows named pipe for tool calls, list, describe, and shutdown.

The driver adapter layer is a guardrail layer, not just glue. [libs/cua-driver/rust/crates/cua-driver/src/sdk_adapter.rs](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-driver/rust/crates/cua-driver/src/sdk_adapter.rs) tracks public session state, refuses undead sessions through tombstones, mirrors tool inventory, and bridges transport calls into the SDK-owned runtime.

The in-guest server layer is capability-first. [libs/cua-spacesd/crates/cua-spacesd-server/src/services](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-spacesd/crates/cua-spacesd-server/src/services) separates system, driver, filesystem, tunnel, teleport, diagnose, and volume services. [libs/cua-spacesd/crates/cua-spacesd-server/src/auth.rs](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-spacesd/crates/cua-spacesd-server/src/auth.rs), [libs/cua-spacesd/crates/cua-spacesd-server/src/server.rs](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-spacesd/crates/cua-spacesd-server/src/server.rs), and [libs/cua-spacesd/crates/cua-spacesd-server/src/http](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-spacesd/crates/cua-spacesd-server/src/http) make the transport and ticket model inspectable.

The benchmark layer treats "run an agent" as a reproducible experiment. [libs/cua-bench/README.md](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-bench/README.md) defines `cb run`, local/cloud placement, task images, attempts, retries, detached runs, `result.json`, `trajectory.json`, `summary.json`, and dataset registry resolution. The runner code under [libs/cua-bench/cua_bench/runner](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-bench/cua_bench/runner) is the part to read after the README.

### Request / data / control flow

For a sandbox workflow, a user or agent starts in [libs/cua/crates/cua-cli](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua/crates/cua-cli), a language binding, or the daemon. The SDK creates a sandbox through `local`, `cloud`, or `direct` placement, using image resolution from [libs/cua/crates/cua-image](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua/crates/cua-image) and runtime/fleet machinery from [libs/cua/crates/cua-vmm](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua/crates/cua-vmm) or [libs/cua/crates/cua-fleet](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua/crates/cua-fleet). If the image runs spacesd, [libs/cua/crates/cua-spacesd-client](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua/crates/cua-spacesd-client) connects to the guest daemon and uses capabilities to decide what is possible.

For a desktop-control workflow, an MCP-capable agent launches `cua-driver mcp`, or a user calls `cua-driver call`. [libs/cua-driver/rust/crates/cua-driver/src/cli.rs](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-driver/rust/crates/cua-driver/src/cli.rs) parses whether this process owns the runtime, proxies through a daemon, uses Claude Code compatibility, grants specific launch capabilities, or exposes skills. [libs/cua-driver/rust/crates/cua-driver/src/serve.rs](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-driver/rust/crates/cua-driver/src/serve.rs) receives transport calls and [libs/cua-driver/rust/crates/cua-driver/src/sdk_adapter.rs](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-driver/rust/crates/cua-driver/src/sdk_adapter.rs) invokes the SDK-facing driver runtime.

For a benchmark workflow, `cb run` in [libs/cua-bench/README.md](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-bench/README.md) resolves a task or dataset, chooses local or cloud placement, starts each sandbox, runs setup, runs either an oracle or agent, evaluates the result, and writes a structured run directory. That is the part that turns computer-use from a demo into something you can compare across agents.

## Key directories and files

- [libs/cua/README.md](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua/README.md): the clearest architecture overview for SDK, daemon, sandboxes, Spaces, Fleet, media, teleport, auth, and agent setup.
- [libs/cua/crates/cua-sdk/src/lib.rs](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua/crates/cua-sdk/src/lib.rs): binding boundary, object list, runtime topology, and flat error model.
- [libs/cua-driver/README.md](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-driver/README.md): driver purpose, integration surfaces, perception extension, permission modes, test harnesses, and platform concerns.
- [libs/cua-driver/rust/crates/cua-driver/src/cli.rs](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-driver/rust/crates/cua-driver/src/cli.rs): command map and the practical surface exposed to agents and users.
- [libs/cua-driver/rust/crates/cua-driver/src/serve.rs](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-driver/rust/crates/cua-driver/src/serve.rs): daemon transport, session resume, history control, proxy sessions, and tool call routing.
- [libs/cua-driver/rust/crates/cua-driver/src/sdk_adapter.rs](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-driver/rust/crates/cua-driver/src/sdk_adapter.rs): public session mirror, tombstone guard, tool inventory, and raw invocation bridge.
- [libs/cua-spacesd/README.md](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-spacesd/README.md): in-guest daemon contract, auth model, capabilities, platform table, presence cursor strategy, relay, install, and crate map.
- [libs/cua-spacesd/crates/cua-spacesd-server/src/services](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-spacesd/crates/cua-spacesd-server/src/services): service-level shape for system, driver, filesystem, tunnel, teleport, diagnose, and volumes.
- [libs/cua-bench/README.md](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-bench/README.md): benchmark contract, run flags, dataset registry, output artifacts, task declaration, and harness support.
- [libs/cua-s1/MODEL_CARD.md](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-s1/MODEL_CARD.md): small-model scope, limitations, eval notes, and closed-option decision design.

## Important components

`Cua` in [libs/cua/crates/cua-sdk/src/lib.rs](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua/crates/cua-sdk/src/lib.rs) is the unifying object. The important move is supporting `embedded` and `connect` with the same object model, so a local process and a shared daemon do not fork the product contract.

`cua-driver` in [libs/cua-driver/rust/crates/cua-driver](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-driver/rust/crates/cua-driver) is the agent-facing automation binary. [cli.rs](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-driver/rust/crates/cua-driver/src/cli.rs) shows how many modes a serious desktop driver needs: MCP, socket daemon, direct runtime, describe/call, permissions, skills, autostart, updates, config, history, perception, and extension commands.

`SdkAdapter` in [libs/cua-driver/rust/crates/cua-driver/src/sdk_adapter.rs](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-driver/rust/crates/cua-driver/src/sdk_adapter.rs) is a good defensive adapter. It does not blindly pass JSON along. It keeps session state, tracks ended sessions, exposes a compatible tool inventory, and maps public transport sessions into runtime-scoped sessions.

`cua-spacesd` in [libs/cua-spacesd](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-spacesd) is the guest-side foundation. [libs/cua-spacesd/crates/cua-spacesd-server/src/services/system.rs](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-spacesd/crates/cua-spacesd-server/src/services/system.rs) and its sibling service files are where "can this environment actually do X?" becomes a capability answer rather than an assumption.

`cua-bench` in [libs/cua-bench](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-bench) is the reality check. The repo is clearly aware that a computer-use platform needs traces and scored tasks, not just screenshots. [libs/cua-bench/cua_bench/registry.json](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-bench/cua_bench/registry.json) and [libs/cua-bench/cua_bench/runner](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-bench/cua_bench/runner) make the benchmark system more than a README claim.

## Important knobs / configs / extension points

The Cua SDK placement knobs are `on`, `kind`, `runtime`, `image`, services, sidecars, readiness probes, cloud warm pools, and resource settings. They are documented in [libs/cua/README.md](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua/README.md) and implemented across [libs/cua/crates/cua-sandbox-core](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua/crates/cua-sandbox-core), [libs/cua/crates/cua-vmm](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua/crates/cua-vmm), [libs/cua/crates/cua-image](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua/crates/cua-image), and [libs/cua/crates/cua-fleet](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua/crates/cua-fleet).

The Cua Driver trust knobs are permission mode, grants, capability manifests, existing-profile attachment, bounded mode, unrestricted mode, OS permissions, and optional perception extension. The practical documentation is in [libs/cua-driver/README.md](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-driver/README.md), while [libs/cua-driver/rust/crates/cua-driver/src/cli.rs](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-driver/rust/crates/cua-driver/src/cli.rs) shows how those switches reach the runtime.

The spacesd knobs are tokens, token files, insecure bootstrap, relay join, media routes, cursor probing, capability reporting, feature attributes, and platform service installation. [libs/cua-spacesd/README.md](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-spacesd/README.md) is unusually concrete here: it says unsupported features carry limitation strings and that clients should check capabilities instead of guessing by platform.

The benchmark knobs are in [libs/cua-bench/README.md](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-bench/README.md): `--on`, `--kind`, `--runtime`, `--image`, `--cpu`, `--memory`, `--max-parallel`, `--attempts`, `--retries`, `--dry-run`, and harness environment variables. Those knobs make it possible to separate agent quality from runtime placement failures.

## Practical questions and answers

Q: Is this one product or several projects in one repo?  
A: It is several projects with a shared thesis. The root [README.md](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/README.md) presents them as product surfaces, but the useful source boundary is: SDK/CLI in [libs/cua](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua), desktop automation in [libs/cua-driver](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-driver), in-guest services in [libs/cua-spacesd](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-spacesd), evaluation in [libs/cua-bench](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-bench), and research models in [libs/cua-s1](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-s1).

Q: Where should a builder start reading?  
A: Start with [libs/cua/README.md](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua/README.md), then [libs/cua-driver/README.md](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-driver/README.md), then [libs/cua-spacesd/README.md](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-spacesd/README.md). After that, read [libs/cua/crates/cua-sdk/src/lib.rs](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua/crates/cua-sdk/src/lib.rs) and [libs/cua-driver/rust/crates/cua-driver/src/cli.rs](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-driver/rust/crates/cua-driver/src/cli.rs).

Q: Does every sandbox need spacesd?  
A: No. [libs/cua/README.md](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua/README.md) says lifecycle and readiness do not assume spacesd. A sandbox can run services without it. Spaces primitives such as shell, files, streams, presence, teleport, hotspot, and agents need spacesd.

Q: What is the production-hard part?  
A: OS and session boundaries. [libs/cua-driver/README.md](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-driver/README.md) talks about macOS TCC identity, Windows and Linux GUI sessions, bounded manifests, and optional perception licensing. [libs/cua-spacesd/README.md](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-spacesd/README.md) talks about tokens, tickets, relays, capability checks, and per-platform capture.

Q: What would I copy first?  
A: Copy the capability-first posture. [libs/cua-spacesd/README.md](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-spacesd/README.md) explicitly tells clients to check capabilities rather than platform names. That pattern is useful for every agent tool that spans local machines, browsers, remote VMs, and OS versions.

## What is smart

The smartest architectural choice is splitting host control, guest service, and desktop automation. [libs/cua](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua) does not try to become the whole desktop driver. [libs/cua-driver](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-driver) does not try to own every sandbox concern. [libs/cua-spacesd](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-spacesd) is deliberately server-only, with wire formats and clients in [libs/cua](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua).

The SDK boundary is also clean. [libs/cua/crates/cua-sdk/src/lib.rs](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua/crates/cua-sdk/src/lib.rs) names one UniFFI export crate, one runtime convention, one flat error enum, and typed IDs crossing as strings. That is the kind of boring contract that keeps language bindings from drifting.

The driver permission story is more serious than the average agent demo. [libs/cua-driver/README.md](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-driver/README.md) has standard, bounded, and unrestricted modes, and the optional perception extension is documented with a clear license boundary instead of silently bundling AGPL risk into the MIT driver.

The evaluation stack is a good sign. [libs/cua-bench/README.md](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-bench/README.md) is not just "run benchmark." It defines images, placement, retries, attempts, outputs, task schemas, registry pinning, and coding-agent harnesses.

## What is flawed or weak

The scope is enormous. A builder entering this repo has to understand Rust workspaces, UniFFI, desktop automation, macOS permissions, Windows sessions, Linux display servers, gRPC, gRPC-Web, QUIC media, VM images, cloud pools, installers, benchmark formats, and model evals. The explicit boundaries help, but there is no way to make this a small codebase.

Some parts are necessarily platform-fragile. [libs/cua-spacesd/README.md](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-spacesd/README.md) shows the cross-platform desktop table, and the caveats are the real story: Wayland cursor limits, macOS grants, Windows secure desktop, elevated apps, and capture backends all shape behavior.

The repo mixes product, infra, research, and packaging. That can be practical in a fast-moving platform, but it creates release coupling. [libs/cua-spacesd/README.md](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-spacesd/README.md) even documents release-order dependencies between spacesd, Cua Spaces, and the SDK.

The licensing picture requires attention. The root [README.md](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/README.md) says some app surfaces are source-available under FSL-1.1-MIT, while [libs/cua-driver/README.md](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-driver/README.md) calls out an optional perception extension with AGPL-only OmniParser components. A company adopting this needs to read those boundaries before bundling.

## What we can learn / steal

Steal the three-plane split: host SDK, guest daemon, desktop driver. It keeps agent infrastructure from turning into one undebuggable binary. The split between [libs/cua](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua), [libs/cua-spacesd](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-spacesd), and [libs/cua-driver](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-driver) is the repo's strongest reusable pattern.

Steal capability reporting. A client should ask the environment what it supports, not infer from macOS/Linux/Windows labels. [libs/cua-spacesd/README.md](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-spacesd/README.md) makes that a product rule.

Steal benchmark output discipline. [libs/cua-bench/README.md](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-bench/README.md) defines run logs, result JSON, trajectory JSON, summaries, pass@k, target breakdowns, and schema versioning. Agent tooling without artifacts is hard to improve.

Steal the adapter guardrails from [libs/cua-driver/rust/crates/cua-driver/src/sdk_adapter.rs](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-driver/rust/crates/cua-driver/src/sdk_adapter.rs): keep session lifecycle visible at the transport boundary, and refuse impossible resurrection states early.

## How we could apply it

For our own agent desktop or remote execution work, this suggests a concrete shape: one SDK object for callers, one guest daemon for the environment, one driver for native desktop authority, and one benchmark runner for evaluation. Those should be separately testable and separately releasable, but they should share typed contracts and capability checks.

For any multi-platform automation feature, copy the Cua habit of surfacing limitations as data. Instead of making an agent discover that "scroll did nothing" or "background typing stole focus," expose platform support and limitation strings the way [libs/cua-spacesd/README.md](https://github.com/trycua/cua/blob/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-spacesd/README.md) describes.

For evaluation, copy [libs/cua-bench](https://github.com/trycua/cua/tree/c90e94662e9980b1b575512a9da9ae8710e28f69/libs/cua-bench)'s run artifact model. A result should always say what ran, where it ran, which image digest or runtime was used, what the agent saw, what it did, and how it was scored.

## Bottom line

Cua is not just another "AI can click a desktop" repo. It is a large, messy, serious attempt to make computer-use agents operational: machines, images, drivers, in-guest services, permissions, streams, benchmarks, skills, and specialist models. The reusable lesson is the layering. If an agent needs a computer, the hard work is the substrate contract around that computer.
