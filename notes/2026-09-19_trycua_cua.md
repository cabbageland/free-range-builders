# Cua

- Repo: trycua/cua
- URL: https://github.com/trycua/cua
- Date: 2026-09-19
- Repo snapshot studied: main at `83f142c4290a0f7d9ed545ae8532858c6e4f8145`
- Why picked today: It was high on the daily GitHub trending page, had a fresh push on the target date, and has real source depth instead of just a product page. The interesting lesson is how Cua treats computer-use agents as infrastructure: drivers, sandboxes, fleets, local VMs, benchmarks, generated SDKs, and release automation in one monorepo.

## Executive summary

[trycua/cua](https://github.com/trycua/cua) is a large computer-use-agent monorepo. The public pitch in [README.md](https://github.com/trycua/cua/blob/83f142c4290a0f7d9ed545ae8532858c6e4f8145/README.md) is "give AI agents computers they can use," but the source shape is more specific: [libs/cua-driver/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/cua-driver) drives native desktops and exposes MCP/CLI/SDK boundaries; [libs/fleet/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/fleet) manages cloud desktop capacity; [libs/lume/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/lume) handles local Apple Virtualization VMs; and [libs/cua-bench/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/cua-bench) turns tasks into verifiable benchmark environments.

The best builder lesson is boundary discipline. [libs/cua-driver/README.md](https://github.com/trycua/cua/blob/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/cua-driver/README.md) explicitly separates agent MCP access, shell CLI access, in-process Python/TypeScript SDK access, Rust runtime ownership, stable C ABI, UniFFI bindings, daemon sockets, and macOS permission identity. That is the kind of unglamorous layering that makes "computer use" survive outside a demo.

## What they built

Cua is not one library. It is a platform stack for agents that need to inspect, operate, provision, and evaluate computers.

At the interaction boundary, [libs/cua-driver/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/cua-driver) exposes `cua-driver mcp`, `cua-driver call`, generated language SDKs, a Rust daemon/runtime, and platform crates for macOS, Linux, and Windows. The driver is the part that turns a model's intent into tool calls such as listing apps/windows, clicking, typing, verifying state, and capturing screenshots.

At the capacity boundary, [libs/fleet/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/fleet) is the cloud service and UI layer. Its tree includes a Go backend under [libs/fleet/backend/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/fleet/backend), Rego authorization policy in [libs/fleet/backend/auth/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/fleet/backend/auth), database migrations in [libs/fleet/backend/database/migrations/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/fleet/backend/database/migrations), a React/Vite app configured by [libs/fleet/package.json](https://github.com/trycua/cua/blob/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/fleet/package.json), SDK schema packages, and a Terraform provider.

At the local virtualization boundary, [libs/lume/README.md](https://github.com/trycua/cua/blob/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/lume/README.md) describes creating macOS and Linux VMs on Apple Silicon using Apple's Virtualization Framework, including unattended macOS setup presets, SSH enablement, telemetry controls, and SIP-related optional tooling.

At the evaluation boundary, [libs/cua-bench/README.md](https://github.com/trycua/cua/blob/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/cua-bench/README.md) describes a benchmark framework with a gym-like interface, worker servers, benchmark runners, simulated Playwright environments, and throughput measurement.

## Why it matters

Computer-use agents are easy to demo and hard to productize. This repo matters because it exposes many of the pieces that turn GUI automation into an infrastructure product: native permission identity, background delivery, generated contracts, capability manifests, SDK loaders, cloud pool accounting, VM lifecycle, cross-platform containers, release gates, compatibility tests, and benchmark harnesses.

The repo is also useful because it is not pretending the model is the whole system. The root [pyproject.toml](https://github.com/trycua/cua/blob/83f142c4290a0f7d9ed545ae8532858c6e4f8145/pyproject.toml) defines a Python workspace with packages such as [libs/python/agent/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/python/agent), [libs/python/computer/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/python/computer), [libs/python/computer-server/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/python/computer-server), and [libs/python/mcp-server/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/python/mcp-server). The root [package.json](https://github.com/trycua/cua/blob/83f142c4290a0f7d9ed545ae8532858c6e4f8145/package.json) is intentionally thin, while TypeScript package surfaces live under [libs/typescript/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/typescript).

## Repo shape at a glance

- [README.md](https://github.com/trycua/cua/blob/83f142c4290a0f7d9ed545ae8532858c6e4f8145/README.md) frames the product into Cua Fleets, Cua Driver, Lume, and Cua Bench.
- [pyproject.toml](https://github.com/trycua/cua/blob/83f142c4290a0f7d9ed545ae8532858c6e4f8145/pyproject.toml) defines the Python workspace and shared tooling for `uv`, Ruff, mypy, pytest, and local packages.
- [libs/cua-driver/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/cua-driver) is the native driver stack: Rust runtime, Python wrapper, TypeScript wrapper, contract files, fixtures, docs, tests, and platform helpers.
- [libs/cua-driver/rust/crates/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/cua-driver/rust/crates) includes the CLI/daemon crate, core crate, SDK crate, contract crate, bindgen crate, testkit, platform crates, cursor overlay, and preview helpers.
- [libs/fleet/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/fleet) is a service/application stack with Go backend, React UI, Rust/TypeScript SDK machinery, RBAC tests, Playwright tests, Terraform provider, and nginx/container config.
- [libs/lume/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/lume) is the Apple Virtualization VM layer with Swift packages, resources, scripts, tests, and install docs.
- [libs/cua-bench/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/cua-bench) contains benchmark tasks, datasets, workers, scripts, and a Python package.
- [libs/qemu-docker/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/qemu-docker), [libs/xfce/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/xfce), [libs/kasm/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/kasm), and [libs/lumier/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/lumier) provide desktop/container/runtime variants.
- [.github/workflows/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/.github/workflows) is huge because each component has separate CI/CD lanes for Python, TypeScript, Rust, Swift, containers, docs, release metadata, and compatibility.
- [.github/scripts/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/.github/scripts) contains release validation and synchronization scripts that keep multi-language packages aligned.

## Layered architecture dissection

### High-level system shape

Cua is a stack with three hard boundaries. The first is the agent boundary: MCP and CLI calls give external agents a runtime-neutral way to use a desktop. The second is the runtime boundary: Rust/platform code owns OS integration, permissions, accessibility, screenshots, input delivery, and native ABI. The third is the capacity boundary: fleets, sandboxes, VMs, containers, and benchmarks provide places where the agent can act and where its behavior can be measured.

The important architectural move is that those boundaries are explicit in source. [libs/cua-driver/README.md](https://github.com/trycua/cua/blob/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/cua-driver/README.md) says MCP remains implemented by the `cua-driver` executable as the runtime-neutral agent boundary. Application SDKs import Python or TypeScript packages, but those call the same in-process native runtime through generated UniFFI bindings rather than maintaining separate MCP facades.

### Main layers

The driver layer lives in [libs/cua-driver/rust/crates/cua-driver/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/cua-driver/rust/crates/cua-driver). [libs/cua-driver/rust/crates/cua-driver/src/cli.rs](https://github.com/trycua/cua/blob/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/cua-driver/rust/crates/cua-driver/src/cli.rs) shows a large CLI surface: `mcp`, `list-tools`, `describe`, `call`, `serve`, `status`, `sessions`, `history`, `doctor`, `permissions`, `config`, `telemetry`, `manifest`, `skills`, and cursor-theme commands. That is not a toy wrapper; it is an operator interface around a native runtime.

The contract layer is [libs/cua-driver/contract/README.md](https://github.com/trycua/cua/blob/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/cua-driver/contract/README.md). It says the Rust contract crate generates the manifest and typed request/result records consumed by both the live daemon and UniFFI SDK. The typed slice covers sessions, desktop state, cursor, windows, clipboard, clicks, drags, scrolls, menu invocation, verification, and cursor theming, while platform schemas can remain richer.

The platform/runtime layer is split into [libs/cua-driver/rust/crates/platform-macos/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/cua-driver/rust/crates/platform-macos), [libs/cua-driver/rust/crates/platform-linux/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/cua-driver/rust/crates/platform-linux), and [libs/cua-driver/rust/crates/platform-windows/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/cua-driver/rust/crates/platform-windows). That split matters because desktop control is mostly platform-specific behavior wearing a shared tool schema.

The cloud capacity layer is [libs/fleet/backend/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/fleet/backend). The file tree shows service modules for auth, billing, chat, config, database, feature flags, GitHub trust, handlers, image uploads, Kubernetes-style namespaces, usage metering, signed service URLs, and migrations. [libs/fleet/package.json](https://github.com/trycua/cua/blob/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/fleet/package.json) shows the UI side: React, Vite, Cloudscape components, noVNC, Keycloak, Model Context Protocol SDK, Playwright, and SDK model tests.

The local environment layer is [libs/lume/README.md](https://github.com/trycua/cua/blob/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/lume/README.md). Lume handles local macOS and Linux VMs, unattended setup presets, telemetry preferences, and optional VNC-based SIP operations. It gives builders a local, repeatable desktop substrate rather than assuming cloud desktops are the only answer.

The benchmark layer is [libs/cua-bench/README.md](https://github.com/trycua/cua/blob/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/cua-bench/README.md). It defines core gym tests, HTTP worker client/server tests, benchmark runner tests, worker manager tests, action parsing, simulated Playwright environments, and throughput measurement. That layer turns computer-use from "the agent clicked something" into reset/step/evaluate loops.

### Request / data / control flow

For an agent integration, the flow starts outside the repo in an MCP-capable or shell-oriented agent. The agent launches `cua-driver mcp` or calls `cua-driver call`, which is parsed by [libs/cua-driver/rust/crates/cua-driver/src/cli.rs](https://github.com/trycua/cua/blob/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/cua-driver/rust/crates/cua-driver/src/cli.rs). The CLI either owns the runtime directly, talks to a daemon socket, or proxies through an app-owned daemon on macOS when permission identity matters.

Tool schemas and portable SDK shapes are produced by the contract layer in [libs/cua-driver/contract/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/cua-driver/contract). [libs/cua-driver/contract/README.md](https://github.com/trycua/cua/blob/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/cua-driver/contract/README.md) describes typed Rust inputs and outputs feeding live MCP tools, Python SDKs, and TypeScript SDKs. That avoids hand-maintaining separate tool contracts.

Native execution then drops into [libs/cua-driver/rust/crates/cua-driver-core/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/cua-driver/rust/crates/cua-driver-core), platform crates, and SDK/ABI layers. The public C boundary is [libs/cua-driver/rust/include/cua_driver_abi.h](https://github.com/trycua/cua/blob/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/cua-driver/rust/include/cua_driver_abi.h); the README says it is generated from Rust `repr(C)` exports and checked in CI so shipped headers and implementation cannot drift.

For cloud usage, the user or agent claims a desktop from Fleet capacity. Source inspection shows that this is backed by the Go service modules in [libs/fleet/backend/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/fleet/backend), policy rules in [libs/fleet/backend/auth/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/fleet/backend/auth), persistent schema migrations in [libs/fleet/backend/database/migrations/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/fleet/backend/database/migrations), and a browser UI in [libs/fleet/src/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/fleet/src).

For evaluation, [libs/cua-bench/README.md](https://github.com/trycua/cua/blob/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/cua-bench/README.md) describes the reset/step/evaluate path. Tasks can be run through worker servers and benchmark runners, with simulated Playwright environments keeping tests fast enough for CI.

## Key directories and files

- [libs/cua-driver/README.md](https://github.com/trycua/cua/blob/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/cua-driver/README.md): best conceptual map of the driver, MCP, SDK, permission, daemon, and publishing surfaces.
- [libs/cua-driver/rust/crates/cua-driver/src/cli.rs](https://github.com/trycua/cua/blob/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/cua-driver/rust/crates/cua-driver/src/cli.rs): command surface and runtime ownership flags.
- [libs/cua-driver/contract/README.md](https://github.com/trycua/cua/blob/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/cua-driver/contract/README.md): generated SDK/MCP contract design.
- [libs/cua-driver/rust/include/cua_driver_abi.h](https://github.com/trycua/cua/blob/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/cua-driver/rust/include/cua_driver_abi.h): stable native ABI boundary for language packages.
- [libs/cua-driver/rust/crates/platform-macos/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/cua-driver/rust/crates/platform-macos), [libs/cua-driver/rust/crates/platform-linux/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/cua-driver/rust/crates/platform-linux), and [libs/cua-driver/rust/crates/platform-windows/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/cua-driver/rust/crates/platform-windows): OS-specific backends.
- [libs/fleet/backend/auth/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/fleet/backend/auth): Rego policy files and Go authorization glue for Fleet.
- [libs/fleet/backend/database/migrations/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/fleet/backend/database/migrations): persistent schema history for usage, reservations, conversations, billing, account lookup, and signed URLs.
- [libs/fleet/package.json](https://github.com/trycua/cua/blob/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/fleet/package.json): front-end dependencies and SDK/test scripts.
- [libs/lume/README.md](https://github.com/trycua/cua/blob/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/lume/README.md): local VM lifecycle, unattended macOS setup, telemetry controls.
- [libs/cua-bench/README.md](https://github.com/trycua/cua/blob/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/cua-bench/README.md): benchmark test structure and worker throughput tools.
- [.github/scripts/validate_release_versions.py](https://github.com/trycua/cua/blob/83f142c4290a0f7d9ed545ae8532858c6e4f8145/.github/scripts/validate_release_versions.py) and [.github/scripts/sync_driver_release_docs.py](https://github.com/trycua/cua/blob/83f142c4290a0f7d9ed545ae8532858c6e4f8145/.github/scripts/sync_driver_release_docs.py): examples of release synchronization machinery.

## Important components

`cua-driver` is the spine. [libs/cua-driver/rust/crates/cua-driver/src/cli.rs](https://github.com/trycua/cua/blob/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/cua-driver/rust/crates/cua-driver/src/cli.rs) makes the runtime modes visible: direct MCP, daemon serve, socket selection, bounded capability manifests, unrestricted mode, history preview, permissions, autostart, manifests, and skill install/update commands.

The SDK contract is the discipline mechanism. [libs/cua-driver/contract/README.md](https://github.com/trycua/cua/blob/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/cua-driver/contract/README.md) says typed Rust input/output declarations build the live MCP tool and generated SDK contract, while CI checks parity against the live registry. That is how you avoid subtle skew between "what the agent sees" and "what the app SDK sees."

Fleet authorization is a real subsystem, not a placeholder. [libs/fleet/backend/auth/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/fleet/backend/auth) contains policy for billing, chat, config, feature flags, GitHub trust, Kubernetes, namespaces, keys, signed service URLs, usage, images, pools, and custom resource admission. That tells us cloud desktop capacity is treated as a multi-tenant product surface.

Lume is the local escape hatch. [libs/lume/README.md](https://github.com/trycua/cua/blob/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/lume/README.md) supports repeatable macOS VM creation and setup. That matters because local agent development needs controlled desktop machines too, not only remote browser containers.

Cua Bench is the feedback loop. [libs/cua-bench/README.md](https://github.com/trycua/cua/blob/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/cua-bench/README.md) is organized around `make`, `reset`, `step`, `evaluate`, worker HTTP endpoints, and benchmark runners. Without that layer, a computer-use stack cannot tell whether agent changes improved behavior or merely looked impressive.

## Important knobs / configs / extension points

Driver permission mode is one of the most important knobs. [libs/cua-driver/README.md](https://github.com/trycua/cua/blob/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/cua-driver/README.md) distinguishes `standard`, `bounded`, and `unrestricted`, with `bounded` tied to reviewed manifests and unrestricted requiring an explicit bypass flag.

Runtime ownership is another key knob. The same README describes macOS standalone, direct MCP, and embedded launch modes. That is not just packaging detail: macOS Accessibility and Screen Recording grants are attributed to app identity, so the responsible process chain is part of the security model.

The contract versioning knobs in [libs/cua-driver/contract/README.md](https://github.com/trycua/cua/blob/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/cua-driver/contract/README.md) are also important: `contract_version`, `tools_list_schema_version`, `capability_version`, and `mcp_protocol_version`. Those are the handles downstream clients need when generated SDKs and live tools evolve.

Fleet exposes product knobs through [libs/fleet/backend/config/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/fleet/backend/config), [libs/fleet/backend/featureflagadmin/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/fleet/backend/featureflagadmin), [libs/fleet/backend/billing/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/fleet/backend/billing), and [libs/fleet/backend/auth/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/fleet/backend/auth). That is where capacity, usage, entitlement, and tenant safety get enforced.

Benchmark knobs are in [libs/cua-bench/README.md](https://github.com/trycua/cua/blob/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/cua-bench/README.md): provider selection, worker count, step count, task path, browser extras, and simulated providers. These determine whether a benchmark run is cheap enough for dev loops or realistic enough for evaluation.

## Practical questions and answers

Q: Is Cua mainly a driver, a cloud product, or a benchmark suite?

A: It is all three. The repo shape says Cua is trying to own the full computer-use loop: create or claim a machine, let an agent drive it, observe/verifiably interact with it, and evaluate the result. [README.md](https://github.com/trycua/cua/blob/83f142c4290a0f7d9ed545ae8532858c6e4f8145/README.md) is the product map; [libs/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs) is the proof.

Q: What should a builder read first?

A: Read [libs/cua-driver/README.md](https://github.com/trycua/cua/blob/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/cua-driver/README.md), then [libs/cua-driver/contract/README.md](https://github.com/trycua/cua/blob/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/cua-driver/contract/README.md), then [libs/cua-driver/rust/crates/cua-driver/src/cli.rs](https://github.com/trycua/cua/blob/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/cua-driver/rust/crates/cua-driver/src/cli.rs). That path teaches the runtime boundary better than the root README.

Q: What is the most transferable design idea?

A: Keep protocol, native runtime, and language SDKs separate. Cua uses MCP/CLI for agents, Rust/native code for desktop execution, generated UniFFI bindings for Python/TypeScript application SDKs, and checked contracts to keep them aligned.

Q: Where would this be hardest to operate?

A: Release and compatibility pressure. The repo has many languages, platforms, container images, package registries, generated bindings, and CI workflows under [.github/workflows/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/.github/workflows). A change in the driver ABI, platform behavior, or Fleet authorization contract can ripple far.

## What is smart

The smartest move is making the agent boundary runtime-neutral. [libs/cua-driver/README.md](https://github.com/trycua/cua/blob/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/cua-driver/README.md) says MCP is implemented by the executable, while language packages are application SDKs. That avoids asking each agent integration to import a Cua-specific library.

The second smart move is contract-first SDK generation. [libs/cua-driver/contract/README.md](https://github.com/trycua/cua/blob/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/cua-driver/contract/README.md) is explicit about generated manifests, shared Rust types, portable subsets, live registry parity, and CI checks. Computer-use tools are too stateful for loose schema drift.

The third smart move is treating permissions as product architecture. The macOS identity discussion in [libs/cua-driver/README.md](https://github.com/trycua/cua/blob/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/cua-driver/README.md) is exactly the kind of thing many automation demos ignore until deployment breaks.

The fourth smart move is putting benchmark infrastructure in the same repo as the driver and sandbox stack. [libs/cua-bench/README.md](https://github.com/trycua/cua/blob/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/cua-bench/README.md) makes evaluation a first-class companion to automation.

## What is flawed or weak

The biggest weakness is complexity. The monorepo spans Rust, Python, TypeScript, Swift, Go, Rego, Docker, Nix, Terraform, Playwright, and many release workflows. That may be necessary for a serious cross-platform product, but it raises onboarding and change-risk costs.

The second weakness is that the cloud Fleet layer is less self-explanatory than the driver layer. [libs/fleet/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/fleet) has rich source, but no top-level README was present at the inspected path. You can infer a lot from [libs/fleet/package.json](https://github.com/trycua/cua/blob/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/fleet/package.json) and [libs/fleet/backend/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/fleet/backend), but newcomers need a map.

The third weakness is operational trust. A driver that can click, type, read windows, and attach to existing profiles needs excellent permission UX. The repository shows serious effort, but the blast radius remains high by nature.

The fourth weakness is release burden. The driver README mentions exact Rust release versions, generated ABI headers, SDK packages, native artifacts, and `.github` validation scripts. That is good engineering, but also a lot of things that can get out of sync.

## What we can learn / steal

Steal the boundary split: one runtime-neutral agent interface, one native runtime, one generated contract, and thin language bindings. That is cleaner than writing separate Python, Node, and MCP implementations by hand.

Steal the permission-mode vocabulary from [libs/cua-driver/README.md](https://github.com/trycua/cua/blob/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/cua-driver/README.md): standard, bounded, and unrestricted. Agents need explicit operating modes, not only prompts that say "be careful."

Steal the benchmark loop from [libs/cua-bench/README.md](https://github.com/trycua/cua/blob/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/cua-bench/README.md): reset, step, evaluate, worker, runner, throughput. GUI agents need tasks that can be scored repeatedly.

Steal the release parity mindset. Files such as [.github/scripts/validate_release_versions.py](https://github.com/trycua/cua/blob/83f142c4290a0f7d9ed545ae8532858c6e4f8145/.github/scripts/validate_release_versions.py) exist because multi-language native SDKs are fragile unless version drift is treated as a build failure.

## How we could apply it

For our own agent tooling, define the protocol contract first. A compact version of [libs/cua-driver/contract/README.md](https://github.com/trycua/cua/blob/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/cua-driver/contract/README.md) would let CLI, MCP, and SDK consumers share typed request/result shapes.

For any desktop-control feature, make permission ownership a design document before implementation. [libs/cua-driver/README.md](https://github.com/trycua/cua/blob/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/cua-driver/README.md) shows that OS attribution, direct mode, embedded mode, and daemon mode all matter.

For cloud sandboxes, use [libs/fleet/backend/auth/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/fleet/backend/auth) as a reminder that tenant policy is core product logic, not a wrapper added after launch.

For evaluations, make [libs/cua-bench/](https://github.com/trycua/cua/tree/83f142c4290a0f7d9ed545ae8532858c6e4f8145/libs/cua-bench) style environments part of the dev loop. The useful question is not "can an agent click once," but "can it repeatedly solve tasks under measured reset/step/evaluate conditions."

## Bottom line

Cua is worth studying because it treats computer use as a systems problem. The repo shows the layers a serious implementation needs: native driver, agent protocol, generated SDK contracts, platform permissions, cloud fleets, local VMs, containers, benchmarks, and release machinery. The reusable lesson is not one clever algorithm; it is the discipline of turning GUI control into a bounded, testable, multi-surface infrastructure stack.
