# OpenShell

- Repo: NVIDIA/OpenShell
- URL: https://github.com/NVIDIA/OpenShell
- Date: 2026-09-29
- Repo snapshot studied: main at `12ef86c2857f8885a54c3c1e488e2d6c0847ab1e`
- Why picked today: It was near the top of GitHub daily trending, had about 10.2k stars, and was pushed today. More importantly, it is not another agent wrapper: it is an ambitious Rust control plane and sandbox runtime for letting autonomous agents touch files, networks, and credentials without becoming a blank check.

## Executive summary

[NVIDIA/OpenShell](https://github.com/NVIDIA/OpenShell/tree/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e) is a policy-enforced runtime for autonomous AI agents. The repo combines a CLI, gateway, supervisor, sandbox boundary, provider profiles, formal policy prover, protobuf API, compute drivers, Kubernetes/Docker/Podman/VM integrations, and end-to-end tests.

The useful builder lesson is the boundary split. OpenShell does not trust a single "agent runner" process to do everything. The [gateway](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/architecture/gateway.md) owns durable platform state and authorization, the [supervisor](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/crates/openshell-supervisor/src/main.rs) owns sandbox-local policy application and relays, the [sandbox boundary](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/crates/openshell-sandbox/src/main.rs) owns process and kernel isolation, and the [prover](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/crates/openshell-prover/src/lib.rs) checks dangerous policy changes before they become runtime authority.

## What they built

OpenShell is a safe runtime for fleets of coding or operations agents. The [README](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/README.md) frames the core problem clearly: agents need to read files, install packages, call APIs, and use credentials, but users need to declare exactly what they can touch.

The checked-in implementation supports that claim structurally:

- A Rust workspace in [Cargo.toml](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/Cargo.toml) with crates for CLI, gateway, supervisor, sandbox, policies, providers, compute drivers, SDKs, OpenTelemetry, and the Z3-backed prover.
- A public gRPC resource model in [proto/openshell.proto](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/proto/openshell.proto) for sandbox lifecycle, provider attachment, service exposure, logs, and related gateway operations.
- Architecture docs for [gateway](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/architecture/gateway.md), [sandbox](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/architecture/sandbox.md), [compute runtimes](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/architecture/compute-runtimes.md), and [security policy](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/architecture/security-policy.md).
- Runtime examples and profiles under [examples](https://github.com/NVIDIA/OpenShell/tree/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/examples) and [providers](https://github.com/NVIDIA/OpenShell/tree/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/providers), including the endpoint-bound [providers/openai.yaml](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/providers/openai.yaml).
- Test and deployment surfaces under [e2e](https://github.com/NVIDIA/OpenShell/tree/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/e2e), [deploy](https://github.com/NVIDIA/OpenShell/tree/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/deploy), and [.github/workflows](https://github.com/NVIDIA/OpenShell/tree/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/.github/workflows).

## Why it matters

Most agent security systems are either policy documents with no enforcement muscle or sandboxes with no product-level credential story. OpenShell is interesting because it tries to bind all of the uncomfortable parts together: process identity, filesystem policy, outbound network mediation, provider credentials, workload identity, formal review of policy changes, and deployable gateway operations.

The design also treats provider credentials as scoped runtime material instead of environment variables sprinkled into an agent process. The [OpenAI provider profile](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/providers/openai.yaml) declares host, port, protocol, enforcement mode, credential mapping, and allowed binaries. That is the right shape: a credential is only meaningful together with where it can be sent and which process may send it.

## Repo shape at a glance

- [crates](https://github.com/NVIDIA/OpenShell/tree/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/crates) is the real product: CLI, gateway, sandbox, supervisor, policy/prover, providers, SDK, compute drivers, extension core, OpenTelemetry, and test-support crates.
- [proto](https://github.com/NVIDIA/OpenShell/tree/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/proto) defines the public API and internal protocol contracts.
- [architecture](https://github.com/NVIDIA/OpenShell/tree/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/architecture) is unusually important documentation. It explains the gateway/supervisor/sandbox trust split and what belongs behind driver boundaries.
- [providers](https://github.com/NVIDIA/OpenShell/tree/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/providers) holds provider profile templates for OpenAI, Anthropic, AWS, GitHub, Google, OpenRouter, PyPI, Cursor, Copilot, and others.
- [examples](https://github.com/NVIDIA/OpenShell/tree/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/examples) demonstrates concrete policy and integration scenarios, including local inference, policy advisor, private IP routing, and governance interceptors.
- [deploy](https://github.com/NVIDIA/OpenShell/tree/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/deploy) contains packaging and Kubernetes/Docker deployment material.
- [docs](https://github.com/NVIDIA/OpenShell/tree/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/docs) and [fern](https://github.com/NVIDIA/OpenShell/tree/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/fern) feed the public docs surface.
- [e2e](https://github.com/NVIDIA/OpenShell/tree/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/e2e) is broad enough to matter: Docker, Kubernetes, gateway, MCP conformance, GPU, parity, and policy-advisor scenarios are represented.

## Layered architecture dissection

### High-level system shape

OpenShell is a control-plane plus data-plane system:

1. User surfaces: [openshell-cli](https://github.com/NVIDIA/OpenShell/tree/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/crates/openshell-cli), SDK crates, and TUI code talk to the gateway.
2. Control plane: [openshell-gateway](https://github.com/NVIDIA/OpenShell/tree/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/crates/openshell-gateway) and [openshell-server](https://github.com/NVIDIA/OpenShell/tree/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/crates/openshell-server) own API state, auth, provider records, policy revisions, sandbox lifecycle, relay coordination, and persistence.
3. Runtime boundary: [openshell-supervisor](https://github.com/NVIDIA/OpenShell/tree/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/crates/openshell-supervisor) and [openshell-sandbox](https://github.com/NVIDIA/OpenShell/tree/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/crates/openshell-sandbox) are the sandbox-local security machinery.
4. Policy and verification: [openshell-policy](https://github.com/NVIDIA/OpenShell/tree/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/crates/openshell-policy), [openshell-policy-schema](https://github.com/NVIDIA/OpenShell/tree/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/crates/openshell-policy-schema), and [openshell-prover](https://github.com/NVIDIA/OpenShell/tree/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/crates/openshell-prover) define, compose, validate, and reason about policy.
5. Infrastructure drivers: driver crates like [openshell-driver-docker](https://github.com/NVIDIA/OpenShell/tree/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/crates/openshell-driver-docker), [openshell-driver-kubernetes](https://github.com/NVIDIA/OpenShell/tree/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/crates/openshell-driver-kubernetes), [openshell-driver-podman](https://github.com/NVIDIA/OpenShell/tree/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/crates/openshell-driver-podman), and [openshell-driver-vm](https://github.com/NVIDIA/OpenShell/tree/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/crates/openshell-driver-vm) translate abstract lifecycle semantics into platform-specific operations.

### Main layers

The CLI layer starts in [crates/openshell-cli/src/main.rs](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/crates/openshell-cli/src/main.rs). It resolves gateway identity, TLS/auth options, GPU request arguments, sandbox commands, provider commands, gateway commands, and completions. The important pattern is that the CLI is mostly a client and context resolver. It should not know how Docker, Kubernetes, or Landlock work.

The gateway entry point is tiny in [crates/openshell-gateway/src/main.rs](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/crates/openshell-gateway/src/main.rs): it delegates to server code with default compute drivers installed. That is a good sign. The control plane is a crate boundary, not a 3,000-line main.

The supervisor entry point in [crates/openshell-supervisor/src/main.rs](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/crates/openshell-supervisor/src/main.rs) is where runtime posture becomes explicit. It accepts roles for `IsolationBackend` and `NetworkProxy`, takes policy files, auth bundles, backend descriptors, gateway endpoint, SSH socket, upstream proxy controls, and readiness sockets. This is the middle process that knows enough to apply policy and relay traffic but is still separated from the untrusted agent child.

The in-workload boundary in [crates/openshell-sandbox/src/main.rs](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/crates/openshell-sandbox/src/main.rs) is the most security-heavy part. It has commands for bootstrap, workspace validation, capability probes, capability-free launching, and Linux runtime qualification. The probe code explicitly checks non-root UID/GID, zero capabilities, `no_new_privs`, Landlock ABI, seccomp notification, socket virtualization, DNS relay behavior, and TCP allow/deny round trips.

The policy layer in [crates/openshell-policy/src/lib.rs](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/crates/openshell-policy/src/lib.rs) is the adapter between authored YAML policy and runtime protobuf structures. It owns L7 validation, JSON-RPC/MCP config flattening, provider-rule composition, merge warnings, network ambiguity checks, and the runtime representation consumed by the supervisor.

The prover layer in [crates/openshell-prover/src/lib.rs](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/crates/openshell-prover/src/lib.rs) parses policy and credentials, loads binary/API capability registries, builds a Z3 model, runs queries, applies accepted risks, and returns a pass/fail exit code. The real design intent is described in [crates/openshell-prover/src/queries.rs](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/crates/openshell-prover/src/queries.rs): link-local reach, L7-bypass with credential, credential reach expansion, and capability expansion.

### Request / data / control flow

A typical create/run path looks like this:

1. A user invokes the CLI. [crates/openshell-cli/src/main.rs](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/crates/openshell-cli/src/main.rs) resolves the gateway endpoint, local auth material, TLS mode, GPU request, and sandbox/provider command shape.
2. The request crosses the public API defined in [proto/openshell.proto](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/proto/openshell.proto), where operations such as `CreateSandbox`, `AttachSandboxProvider`, `CreateSshSession`, and `ExposeService` have explicit authorization options.
3. The gateway persists and reconciles desired state. Per [architecture/gateway.md](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/architecture/gateway.md), it owns policy revisions, provider records, settings, sandbox state, relay sessions, and supervisor authentication.
4. A compute driver provisions the runtime and starts sandbox components. Per [architecture/sandbox.md](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/architecture/sandbox.md), the driver validates outer network-fence evidence before untrusted code runs.
5. The supervisor attaches, fetches config, applies policy, and coordinates with the in-workload sandbox over protected channels.
6. The agent child runs with zero capabilities, restricted filesystem access, mediated network egress, and endpoint-bound credentials. Ordinary outbound traffic flows through a policy proxy rather than raw sockets.
7. Proposed policy changes can be routed through the prover path in [crates/openshell-prover/src/queries.rs](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/crates/openshell-prover/src/queries.rs), where new credentialed reach, new methods, metadata reach, or L7 bypasses become reviewable findings.

## Key directories and files

- [README.md](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/README.md): product promise, quickstart, and the concise kernel-enforcement/formal-verification claim.
- [architecture/README.md](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/architecture/README.md): best single map of gateway, supervisor, sandbox, drivers, credentials, and identity.
- [architecture/sandbox.md](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/architecture/sandbox.md): trust levels, startup flow, isolation layers, and the most precise statement of runtime guarantees.
- [Cargo.toml](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/Cargo.toml): workspace dependencies tell the story: tokio, tonic/prost, axum, rustls, sqlx, kube, z3, OpenTelemetry, metrics, SPIFFE, Landlock/seccomp-adjacent crates, and CLI tooling.
- [proto/openshell.proto](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/proto/openshell.proto): public resource model and authorization annotations.
- [crates/openshell-sandbox/src/main.rs](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/crates/openshell-sandbox/src/main.rs): capability-free boundary and Linux primitive probes.
- [crates/openshell-supervisor/src/main.rs](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/crates/openshell-supervisor/src/main.rs): supervisor role, auth-bundle loading, proxy mode, gateway connection, readiness, and policy inputs.
- [crates/openshell-policy/src/lib.rs](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/crates/openshell-policy/src/lib.rs): authored policy parsing and runtime conversion.
- [crates/openshell-prover/src/queries.rs](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/crates/openshell-prover/src/queries.rs): the most reusable security idea in the repo.
- [providers/openai.yaml](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/providers/openai.yaml): concrete example of endpoint-bound credential scope and binary allowlisting.

## Important components

- [OpenShell service](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/proto/openshell.proto): the API contract is rich enough to expose workspaces, sandboxes, templates, providers, SSH sessions, service endpoints, and gateway info without leaking internal compute-driver types.
- [Gateway control plane](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/architecture/gateway.md): persistence, auth, provider resolution, policy delivery, and relay coordination stay out of the sandbox boundary.
- [Supervisor role switch](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/crates/openshell-supervisor/src/main.rs): `IsolationBackend` and `NetworkProxy` make the same enforcement machinery usable in different placements.
- [Runtime qualification](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/crates/openshell-sandbox/src/main.rs): active probes check the kernel properties the sandbox depends on instead of assuming the host can enforce them.
- [Policy parser/adapter](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/crates/openshell-policy/src/lib.rs): YAML friendliness and protobuf runtime contracts are separate concerns.
- [Prover query categories](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/crates/openshell-prover/src/queries.rs): the findings are specific enough to be useful in review, not a vague "policy risk" label.
- [Provider profiles](https://github.com/NVIDIA/OpenShell/tree/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/providers): providers are treated as data with credentials, endpoints, binaries, and enforcement mode.

## Important knobs / configs / extension points

- [Provider profiles](https://github.com/NVIDIA/OpenShell/tree/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/providers): change endpoints, credentials, auth style, allowed binaries, and enforcement mode.
- [Sandbox policy schema](https://github.com/NVIDIA/OpenShell/tree/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/crates/openshell-policy-schema): controls what an authored policy can express.
- [Compute drivers](https://github.com/NVIDIA/OpenShell/tree/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/crates/openshell-driver-docker): driver crates are the extension seam for Docker, Kubernetes, Podman, VM, MXC, and future runtimes.
- [Gateway interceptors](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/architecture/gateway.md): middleware can bind to selected unary OpenShell methods under explicit allowlists.
- [Prover registry inputs](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/crates/openshell-prover/src/lib.rs): custom registries can override embedded binary/API capability registries.
- [Supervisor proxy flags](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/crates/openshell-supervisor/src/main.rs): upstream proxy, no-proxy, auth file, CA bundle, and hostname dialing are runtime integration knobs.

## Practical questions and answers

Q: Is this just Docker for agents?

A: No. Docker is one possible compute runtime. The interesting layer is the policy and credential contract above the runtime, plus the supervisor/sandbox split inside it. The driver crates translate into runtime operations; they are not the security model by themselves.

Q: Where are credentials protected?

A: Provider profiles such as [providers/openai.yaml](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/providers/openai.yaml) declare credential material and allowed endpoints. The [sandbox architecture](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/architecture/sandbox.md) says the agent child does not receive raw provider credentials; outbound traffic is mediated and credentials are injected only for approved destinations.

Q: What should a builder copy first?

A: Copy the idea of reviewing policy changes as deltas. [crates/openshell-prover/src/queries.rs](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/crates/openshell-prover/src/queries.rs) looks for new credentialed reach and new methods, not just whether a policy is globally "valid."

Q: What is the highest operational risk?

A: The runtime guarantee depends on many layers agreeing: driver evidence, kernel primitives, network fences, supervisor sessions, policy conversion, and provider profiles. That is unavoidable for this problem, but the blast radius is real. A small app should not casually copy the whole architecture.

Q: Is the codebase inspectable enough for trust?

A: It is large, but the boundaries are legible. [architecture/README.md](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/architecture/README.md) and the crate layout make it possible to audit one layer at a time.

## What is smart

The strongest idea is the separation between durable authority and local enforcement. The gateway can reason about resources and policy, but it is not the thing observing the agent's local process identity and sockets. The supervisor and sandbox boundary handle that closer to where the kernel facts exist.

The second smart idea is treating policy approval as a formal reachability problem. The [prover queries](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/crates/openshell-prover/src/queries.rs) encode categories that map to real failures: metadata service reach, credentialed bypass, newly credentialed destinations, and new HTTP capabilities.

The third smart idea is provider profiles as first-class artifacts. [providers/openai.yaml](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/providers/openai.yaml) is deliberately not just `OPENAI_API_KEY`. It names host, port, protocol, access level, enforcement mode, and binary paths.

## What is flawed or weak

The docs are strong, but this is still a young, high-complexity stack. The repo has hundreds of open issues, and the architecture depends on platform-specific enforcement details that are easy to misunderstand. The [sandbox qualification](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/crates/openshell-sandbox/src/main.rs) is valuable partly because the underlying assumptions are so fragile.

The provider profile example also exposes a usability burden: [providers/openai.yaml](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/providers/openai.yaml) tells users to copy and edit binary paths for their image. That is correct security posture, but it is a sharp setup edge.

The formal prover is scoped to declared risks. It is useful, but it cannot prove the implementation has no bug in proxying, driver evidence, or kernel setup. Treat it as a policy-change reviewer, not a magic correctness seal.

## What we can learn / steal

Steal the three-boundary mental model:

- Control plane decides desired state and stores audit history.
- Supervisor applies policy and mediates live access.
- Sandbox boundary proves and enforces local kernel/runtime properties.

Also steal the provider-profile shape. Any agent product that handles secrets should bind each secret to destination hosts, protocols, methods, and process identities. Raw environment-variable injection is too blunt.

Finally, steal the "new reach" review pattern. Most permission UIs ask whether a policy contains a risky thing. OpenShell's prover direction asks whether this change newly grants credentialed reach or new methods. That is a more human review question.

## How we could apply it

For our own agent tooling, a smaller version would be:

1. Describe every external provider as a data profile like [providers/openai.yaml](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/providers/openai.yaml).
2. Keep user-authored policy separate from runtime policy, like [crates/openshell-policy/src/lib.rs](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/crates/openshell-policy/src/lib.rs).
3. Compare policy deltas before approval, with categories inspired by [crates/openshell-prover/src/queries.rs](https://github.com/NVIDIA/OpenShell/blob/12ef86c2857f8885a54c3c1e488e2d6c0847ab1e/crates/openshell-prover/src/queries.rs).
4. Make runtime capability checks explicit and testable instead of assuming the host has the primitives we need.

We probably would not copy the full multi-driver architecture until the product needs Kubernetes and VM placements. But the credential and policy surfaces are useful immediately.

## Bottom line

OpenShell is worth studying because it treats "agent safety" as a systems problem, not a prompt or UI problem. The best lesson is not any single Rust crate. It is the way the repo ties endpoint-bound credentials, kernel-level runtime facts, policy deltas, and deployable control-plane state into one inspectable architecture.
