# Agent Governance Toolkit

- Repo: `microsoft/agent-governance-toolkit`
- URL: https://github.com/microsoft/agent-governance-toolkit
- Date: 2026-07-28
- Repo snapshot studied: `main` @ `2a23e34b90ed0d33c3f31e2a67fb74838d56f093`
- Why picked today: It was on GitHub's trending page when checked, showing 5,060 stars and 831 forks there. More importantly, it is one of the clearer attempts to turn "agent safety" from prompt theater into an explicit control plane.

## Executive summary
`agent-governance-toolkit` is not one package. It is a governance monorepo whose real center of gravity is an intermediate representation for agent control: intervention points, manifests, policy bindings, approval routing, and normalized verdicts. The serious files are not the homepage snippets. They are the compatibility bridge in [`agent-governance-python/agt-policies/src/agt/policies/bridge.py`](https://github.com/microsoft/agent-governance-toolkit/blob/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/agent-governance-python/agt-policies/src/agt/policies/bridge.py), the Rust runtime in [`policy-engine/core/src/runtime.rs`](https://github.com/microsoft/agent-governance-toolkit/blob/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/policy-engine/core/src/runtime.rs), and the host wrapper in [`agent-governance-python/agt-policies/src/agt/policies/runtime.py`](https://github.com/microsoft/agent-governance-toolkit/blob/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/agent-governance-python/agt-policies/src/agt/policies/runtime.py).

The strongest design move is that AGT treats governance as an explicit event stream over agent execution. [`runtime.rs`](https://github.com/microsoft/agent-governance-toolkit/blob/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/policy-engine/core/src/runtime.rs) takes an intervention-point request, projects the relevant tool and policy target, builds canonical policy input, runs annotators, dispatches policy evaluation, and emits telemetry. That is much more robust than "wrap the model with a safety prompt."

The second strong move is compatibility instead of purity. [`bridge.py`](https://github.com/microsoft/agent-governance-toolkit/blob/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/agent-governance-python/agt-policies/src/agt/policies/bridge.py) translates an older `GovernancePolicy` shape into an AGT manifest plus stock Rego helper calls. That means the repo is not only inventing a new governance spec. It is building migration rails for existing agent stacks.

## What they built
They built a multi-language governance stack for agents, not a single library:

- [`policy-engine`](https://github.com/microsoft/agent-governance-toolkit/tree/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/policy-engine) is the core spec and Rust engine for manifests, policy dispatch, intervention-point evaluation, and telemetry.
- [`agent-governance-python`](https://github.com/microsoft/agent-governance-toolkit/tree/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/agent-governance-python) carries Python host wrappers, adapters, sandboxing, compliance, discovery, runtime, and integrations.
- [`agent-governance-typescript`](https://github.com/microsoft/agent-governance-toolkit/tree/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/agent-governance-typescript), [`agent-governance-dotnet`](https://github.com/microsoft/agent-governance-toolkit/tree/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/agent-governance-dotnet), [`agent-governance-rust`](https://github.com/microsoft/agent-governance-toolkit/tree/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/agent-governance-rust), and [`agent-governance-golang`](https://github.com/microsoft/agent-governance-toolkit/tree/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/agent-governance-golang) package the same control ideas for other ecosystems.
- [`agent-governance-claude-code`](https://github.com/microsoft/agent-governance-toolkit/tree/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/agent-governance-claude-code), [`agent-governance-copilot-cli`](https://github.com/microsoft/agent-governance-toolkit/tree/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/agent-governance-copilot-cli), and [`agent-governance-opencode`](https://github.com/microsoft/agent-governance-toolkit/tree/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/agent-governance-opencode) show the product intent: meet agents where they already run.
- [`examples`](https://github.com/microsoft/agent-governance-toolkit/tree/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/examples) is unusually broad, covering OpenAI Agents, Smolagents, MCP receipt governance, pipeline governance, multi-agent governance, governed OpenClaw demos, and more.

## Why it matters
This repo matters because it frames agent governance as a runtime systems problem, not a model-alignment slogan.

1. It introduces explicit intervention points instead of relying on one giant guard prompt.
2. It cleanly separates host adapters from the policy engine.
3. It ships policy evaluation, approval routing, sandboxing, and telemetry as one control surface.
4. It acknowledges migration reality by translating legacy policy shapes into the new manifest format.

## Repo shape at a glance
The repo is a wide monorepo, but the shape is disciplined:

- [`policy-engine/core/src`](https://github.com/microsoft/agent-governance-toolkit/tree/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/policy-engine/core/src): Rust runtime, manifest loader, policy dispatch, verdict normalization, telemetry, and annotation plumbing.
- [`policy-engine/sdk`](https://github.com/microsoft/agent-governance-toolkit/tree/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/policy-engine/sdk): bindings, including the Python SDK that the AGT wrapper expects.
- [`agent-governance-python/agt-policies/src/agt/policies`](https://github.com/microsoft/agent-governance-toolkit/tree/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/agent-governance-python/agt-policies/src/agt/policies): AGT-facing Python wrapper, snapshot/result types, manifest bridge, and runtime wrapper.
- [`agent-governance-python/agent-os/src/agent_os`](https://github.com/microsoft/agent-governance-toolkit/tree/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/agent-governance-python/agent-os/src/agent_os): host-side policy evaluation and integration surface, including a lightweight entry point.
- [`agent-governance-python/agent-sandbox/src/agent_sandbox`](https://github.com/microsoft/agent-governance-toolkit/tree/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/agent-governance-python/agent-sandbox/src/agent_sandbox): sandbox providers, OCI runtime selection, Docker hardening, and static pre-execution scanning.
- [`examples`](https://github.com/microsoft/agent-governance-toolkit/tree/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/examples), [`docs`](https://github.com/microsoft/agent-governance-toolkit/tree/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/docs), and [`tests`](https://github.com/microsoft/agent-governance-toolkit/tree/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/tests): the tutorial, scenario, and verification belt around the engine.

## Layered architecture dissection
### High-level system shape
The architecture is: host SDK or adapter emits a normalized snapshot -> AGT/ACS runtime resolves the relevant intervention point -> Rust engine projects tool and policy target -> annotators enrich policy input -> policy dispatcher returns a verdict -> host wrapper maps that verdict into local exceptions, approvals, or audit results.

### Main layers
**1. Governance IR and migration layer**  
[`bridge.py`](https://github.com/microsoft/agent-governance-toolkit/blob/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/agent-governance-python/agt-policies/src/agt/policies/bridge.py) is the best single file to read if you want the repo's philosophy. It maps old knobs like `max_tokens`, `max_tool_calls`, `blocked_patterns`, and `require_human_approval` into stock AGT helpers and an emitted manifest. The repo is effectively compiling older policy intent into a stricter runtime format.

**2. Manifest and policy-definition layer**  
[`policy-engine/core/src/manifest.rs`](https://github.com/microsoft/agent-governance-toolkit/blob/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/policy-engine/core/src/manifest.rs) defines intervention points, tool metadata, annotators, and the optional approval section. [`policy-engine/core/src/policy.rs`](https://github.com/microsoft/agent-governance-toolkit/blob/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/policy-engine/core/src/policy.rs) defines supported policy backends (`rego`, `cedar`, `test`, `custom`) and hardens URL-sourced manifests by rejecting unsafe filesystem references and unpinned remote bundles.

**3. Runtime enforcement layer**  
[`policy-engine/core/src/runtime.rs`](https://github.com/microsoft/agent-governance-toolkit/blob/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/policy-engine/core/src/runtime.rs) is where governance actually happens. It validates manifests, enforces limits, builds policy input, collects annotations, calls the policy dispatcher, normalizes verdicts, and emits decision and timing telemetry.

**4. Host wrapper layer**  
[`agent-governance-python/agt-policies/src/agt/policies/runtime.py`](https://github.com/microsoft/agent-governance-toolkit/blob/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/agent-governance-python/agt-policies/src/agt/policies/runtime.py) is a pragmatic shell over the native ACS SDK. It translates AGT snapshots, maps verdicts into AGT result objects, and wires the approval callback so `escalate` becomes a real host decision path instead of a dead-end label.

**5. Sandbox and execution-isolation layer**  
[`agent-governance-python/agent-sandbox/src/agent_sandbox/docker_provider/provider.py`](https://github.com/microsoft/agent-governance-toolkit/blob/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/agent-governance-python/agent-sandbox/src/agent_sandbox/docker_provider/provider.py) hardens per-session Docker containers with dropped capabilities, `no-new-privileges`, optional read-only filesystems, non-root execution, and PID limits. [`agent-governance-python/agent-sandbox/src/agent_sandbox/code_scanner.py`](https://github.com/microsoft/agent-governance-toolkit/blob/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/agent-governance-python/agent-sandbox/src/agent_sandbox/code_scanner.py) adds a lightweight AST gate that blocks obvious subprocess-spawning patterns before code enters the sandbox.

### Request / data / control flow
1. A host calls [`AgtRuntime`](https://github.com/microsoft/agent-governance-toolkit/blob/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/agent-governance-python/agt-policies/src/agt/policies/runtime.py) with an intervention point and AGT snapshot.
2. The Python wrapper translates that snapshot and hands it to the native ACS runtime.
3. [`Runtime::evaluate_intervention_point`](https://github.com/microsoft/agent-governance-toolkit/blob/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/policy-engine/core/src/runtime.rs) locates the intervention-point config, projects the relevant tool, and builds canonical policy input.
4. The runtime gathers annotations and dispatches policy evaluation using the policy binding chosen in [`manifest.rs`](https://github.com/microsoft/agent-governance-toolkit/blob/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/policy-engine/core/src/manifest.rs) and [`policy.rs`](https://github.com/microsoft/agent-governance-toolkit/blob/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/policy-engine/core/src/policy.rs).
5. The result is normalized into a verdict, optionally routed through approval resolution, then surfaced back to the host with telemetry and identities attached.

## Key directories and files
- [`README.md`](https://github.com/microsoft/agent-governance-toolkit/blob/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/README.md): product framing and quickstart claims.
- [`policy-engine/core/src/runtime.rs`](https://github.com/microsoft/agent-governance-toolkit/blob/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/policy-engine/core/src/runtime.rs): the real enforcement engine.
- [`policy-engine/core/src/manifest.rs`](https://github.com/microsoft/agent-governance-toolkit/blob/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/policy-engine/core/src/manifest.rs): manifest grammar, approval config, and intervention-point schema.
- [`policy-engine/core/src/policy.rs`](https://github.com/microsoft/agent-governance-toolkit/blob/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/policy-engine/core/src/policy.rs): policy backend types and path hardening.
- [`agent-governance-python/agt-policies/src/agt/policies/runtime.py`](https://github.com/microsoft/agent-governance-toolkit/blob/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/agent-governance-python/agt-policies/src/agt/policies/runtime.py): host-facing Python entry point over the native engine.
- [`agent-governance-python/agt-policies/src/agt/policies/bridge.py`](https://github.com/microsoft/agent-governance-toolkit/blob/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/agent-governance-python/agt-policies/src/agt/policies/bridge.py): legacy-policy translation seam.
- [`agent-governance-python/agent-sandbox/src/agent_sandbox/docker_provider/provider.py`](https://github.com/microsoft/agent-governance-toolkit/blob/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/agent-governance-python/agent-sandbox/src/agent_sandbox/docker_provider/provider.py): hardened container runtime.
- [`examples`](https://github.com/microsoft/agent-governance-toolkit/tree/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/examples): where the product ambition becomes visible.

## Important components
The single most important component is the intervention-point runtime in [`runtime.rs`](https://github.com/microsoft/agent-governance-toolkit/blob/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/policy-engine/core/src/runtime.rs). That file shows AGT is trying to govern agent execution as structured data, not as prose policy.

The second is the manifest grammar in [`manifest.rs`](https://github.com/microsoft/agent-governance-toolkit/blob/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/policy-engine/core/src/manifest.rs). Optional approval routing, intervention-point definitions, tool metadata, and annotators all live there. This is the repo's control-plane schema.

The third is the compatibility compiler in [`bridge.py`](https://github.com/microsoft/agent-governance-toolkit/blob/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/agent-governance-python/agt-policies/src/agt/policies/bridge.py). It is easy to underrate, but migration tooling is what turns a neat architecture into something teams may actually adopt.

## Important knobs / configs / extension points
- Policy backend choice in [`policy.rs`](https://github.com/microsoft/agent-governance-toolkit/blob/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/policy-engine/core/src/policy.rs): `rego`, `cedar`, `test`, or `custom`.
- Approval routing, timeout behavior, and fatigue windows in [`manifest.rs`](https://github.com/microsoft/agent-governance-toolkit/blob/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/policy-engine/core/src/manifest.rs).
- Host approval callbacks and result mapping in [`agt/policies/runtime.py`](https://github.com/microsoft/agent-governance-toolkit/blob/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/agent-governance-python/agt-policies/src/agt/policies/runtime.py).
- Docker hardening, network enablement, and runtime choice in [`docker_provider/provider.py`](https://github.com/microsoft/agent-governance-toolkit/blob/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/agent-governance-python/agent-sandbox/src/agent_sandbox/docker_provider/provider.py) and [`isolation_runtime.py`](https://github.com/microsoft/agent-governance-toolkit/blob/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/agent-governance-python/agent-sandbox/src/agent_sandbox/isolation_runtime.py).
- Legacy-policy compilation targets in [`bridge.py`](https://github.com/microsoft/agent-governance-toolkit/blob/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/agent-governance-python/agt-policies/src/agt/policies/bridge.py).

## Practical questions and answers
**Is this mostly prompt-layer safety?**  
No. The interesting work happens before or around execution: manifest validation, tool projection, canonical policy input building, policy dispatch, and approval routing.

**Where should a builder start reading?**  
Start with [`bridge.py`](https://github.com/microsoft/agent-governance-toolkit/blob/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/agent-governance-python/agt-policies/src/agt/policies/bridge.py), then [`runtime.rs`](https://github.com/microsoft/agent-governance-toolkit/blob/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/policy-engine/core/src/runtime.rs), [`manifest.rs`](https://github.com/microsoft/agent-governance-toolkit/blob/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/policy-engine/core/src/manifest.rs), and [`agt/policies/runtime.py`](https://github.com/microsoft/agent-governance-toolkit/blob/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/agent-governance-python/agt-policies/src/agt/policies/runtime.py).

**Is the monorepo breadth justified?**  
Mostly yes. The repo is broad because it is trying to own the full path from policy authoring to runtime enforcement to agent-specific integrations. The danger is surface-area sprawl, not conceptual confusion.

## What is smart
- Using intervention points and canonical policy input instead of vague safety prose.
- Shipping a bridge from older governance objects into the stricter AGT manifest world.
- Hardening URL-sourced manifests to fail closed around local paths and remote bundles.
- Treating approval as a first-class runtime path rather than a comment in the docs.
- Defaulting the Docker sandbox to a more paranoid stance than most agent repos bother with.

## What is flawed or weak
- The repo surface is enormous. Python, Rust, TypeScript, Go, .NET, multiple CLI plugins, sandboxing, docs, and examples all move together, which raises maintenance risk.
- The clean architecture still depends on a native Rust-backed engine; [`agt/policies/runtime.py`](https://github.com/microsoft/agent-governance-toolkit/blob/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/agent-governance-python/agt-policies/src/agt/policies/runtime.py) explicitly requires the `agent_control_specification` SDK and a built native binding. "One pip install" is directionally true, but the internals are not lightweight.
- The lightweight path in [`agent_os/lite.py`](https://github.com/microsoft/agent-governance-toolkit/blob/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/agent-governance-python/agent-os/src/agent_os/lite.py) exposes an `escalate` parameter, stores it as `_escalate`, and never actually consults it in evaluation. That makes the beginner-friendly layer look slightly ahead of its implementation.
- [`code_scanner.py`](https://github.com/microsoft/agent-governance-toolkit/blob/2a23e34b90ed0d33c3f31e2a67fb74838d56f093/agent-governance-python/agent-sandbox/src/agent_sandbox/code_scanner.py) is useful, but it is intentionally lightweight and cannot replace runtime syscall/process enforcement.

## What we can learn / steal
- Use a manifest/intervention-point IR as the stable contract between agent frameworks and governance logic.
- Provide migration compilers when changing safety architecture.
- Fail closed on remote policy loading and path resolution.
- Separate lightweight host adapters from the real enforcement engine.
- Treat sandbox defaults as part of governance, not as an optional ops appendix.

## How we could apply it
If we built our own governed-agent stack, I would copy the shape more than the brand names: a normalized snapshot format, explicit intervention points, a pluggable policy backend layer, a host-side approval callback, and a hardened sandbox that assumes agent code is untrustworthy by default.

## Bottom line
`agent-governance-toolkit` is worth studying because it is one of the more serious open attempts to make agent governance executable instead of rhetorical.

The builder lesson is that "agent safety" gets more real when it stops living in prompts and starts living in manifests, runtimes, verdicts, approval paths, and hardened execution boundaries.
