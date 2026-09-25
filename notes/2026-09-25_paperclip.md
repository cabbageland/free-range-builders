# Paperclip

- Repo: paperclipai/paperclip
- URL: https://github.com/paperclipai/paperclip
- Date: 2026-09-25
- Repo snapshot studied: master at bd203093235b28631760a76b602b35028322e06f
- Why picked today: It was the top GitHub daily trending repo when scouted, showing 1,853 stars today on the trending page, 83k+ total stars through the GitHub API, and a fresh push on 2026-09-25. It is also very on-theme: a serious-looking control plane for coordinating teams of AI agents at work.

## Executive summary

[paperclipai/paperclip](https://github.com/paperclipai/paperclip/tree/bd203093235b28631760a76b602b35028322e06f) is a monorepo for running "AI-agent companies": companies, goals, org charts, issues, budgets, approvals, heartbeats, adapters, connectors, and a board UI. The [README.md](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/README.md) markets it as a task-manager-shaped app, but the source tree shows something deeper: a governance and runtime-control surface around autonomous agents.

The most important design split is in [doc/GOAL.md](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/doc/GOAL.md) and [doc/PRODUCT.md](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/doc/PRODUCT.md): Paperclip is the control plane, not the execution plane. Agents run through adapters and runners. The app keeps the durable company model, task hierarchy, budget controls, approvals, audit trail, and human board intervention path.

The useful builder lesson is that agent orchestration quickly becomes enterprise software. The interesting files are not just the UI or a prompt. They are [server/src/services/heartbeat.ts](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/server/src/services/heartbeat.ts), [packages/paperclip-runner/src/backends/native-backend-factory.ts](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/packages/paperclip-runner/src/backends/native-backend-factory.ts), [packages/paperclip-runner/src/control-plane/durable-prp-control-plane.ts](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/packages/paperclip-runner/src/control-plane/durable-prp-control-plane.ts), and [server/src/services/connector-runtime.ts](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/server/src/services/connector-runtime.ts), because those are where "agent task manager" turns into execution contracts, provider boundaries, recovery, and tool governance.

## What they built

They built a self-hosted control plane for autonomous AI work. The V1 contract in [doc/SPEC-implementation.md](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/doc/SPEC-implementation.md) says a human board creates a company, defines goals, creates agents in an org tree, invokes agent heartbeats, tracks work through tasks/comments, watches cost usage, and can pause or override work.

The repo packages that as a TypeScript monorepo. [server](https://github.com/paperclipai/paperclip/tree/bd203093235b28631760a76b602b35028322e06f/server) is the REST API and orchestration service. [ui](https://github.com/paperclipai/paperclip/tree/bd203093235b28631760a76b602b35028322e06f/ui) is the React board interface. [cli](https://github.com/paperclipai/paperclip/tree/bd203093235b28631760a76b602b35028322e06f/cli) is the `paperclipai` install/run/configuration tool. [packages/db](https://github.com/paperclipai/paperclip/tree/bd203093235b28631760a76b602b35028322e06f/packages/db), [packages/shared](https://github.com/paperclipai/paperclip/tree/bd203093235b28631760a76b602b35028322e06f/packages/shared), [packages/adapters](https://github.com/paperclipai/paperclip/tree/bd203093235b28631760a76b602b35028322e06f/packages/adapters), [packages/paperclip-runner](https://github.com/paperclipai/paperclip/tree/bd203093235b28631760a76b602b35028322e06f/packages/paperclip-runner), and [packages/plugins](https://github.com/paperclipai/paperclip/tree/bd203093235b28631760a76b602b35028322e06f/packages/plugins) carry the reusable substrate.

## Why it matters

Most agent demos pretend the hard part is calling a model. Paperclip is more interesting because it treats agents as workers inside a governable organization. The primitives in [doc/PRODUCT.md](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/doc/PRODUCT.md) are companies, employees, org structure, task hierarchy, adapter configuration, budgets, and board-level oversight.

That matters because the failure modes of multi-agent systems are mostly coordination failures: unbounded spend, lost context, unclear ownership, duplicated work, stale sessions, unsafe tools, and nobody knowing when a run is stuck. The source tree is full of answers to those problems: company-scoped routes in [server/src/routes](https://github.com/paperclipai/paperclip/tree/bd203093235b28631760a76b602b35028322e06f/server/src/routes), runtime services in [server/src/services](https://github.com/paperclipai/paperclip/tree/bd203093235b28631760a76b602b35028322e06f/server/src/services), native runners in [packages/paperclip-runner/src](https://github.com/paperclipai/paperclip/tree/bd203093235b28631760a76b602b35028322e06f/packages/paperclip-runner/src), and adapter packages under [packages/adapters](https://github.com/paperclipai/paperclip/tree/bd203093235b28631760a76b602b35028322e06f/packages/adapters).

## Repo shape at a glance

- [server](https://github.com/paperclipai/paperclip/tree/bd203093235b28631760a76b602b35028322e06f/server) is the core control plane: Express app, routes, auth, services, storage, realtime, native runtime integration, background scheduling, and static UI serving.
- [ui](https://github.com/paperclipai/paperclip/tree/bd203093235b28631760a76b602b35028322e06f/ui) is the board UI, with pages for companies, agents, projects, issues, goals, approvals, costs, apps, skills, secrets, plugins, and settings.
- [cli](https://github.com/paperclipai/paperclip/tree/bd203093235b28631760a76b602b35028322e06f/cli) is the install, onboard, run, doctor, service, worktree, adapter, and API client command surface.
- [packages/db](https://github.com/paperclipai/paperclip/tree/bd203093235b28631760a76b602b35028322e06f/packages/db) wraps Drizzle/Postgres, embedded Postgres, migrations, backup/restore, and schema exports.
- [packages/shared](https://github.com/paperclipai/paperclip/tree/bd203093235b28631760a76b602b35028322e06f/packages/shared) is the contract layer: validators, types, constants, path names, native finalization schemas, decision schemas, connection schemas, and telemetry helpers.
- [packages/adapters](https://github.com/paperclipai/paperclip/tree/bd203093235b28631760a76b602b35028322e06f/packages/adapters) contains local and gateway adapter packages for Claude, Codex, Cursor, Gemini, Grok, Kimi, OpenClaw, OpenCode, Pi, and Hermes-like runtimes.
- [packages/paperclip-runner](https://github.com/paperclipai/paperclip/tree/bd203093235b28631760a76b602b35028322e06f/packages/paperclip-runner) is the native runner/protocol layer for sessions, turns, semantic tools, app-server transports, recovery, and provider conformance.
- [packages/plugins](https://github.com/paperclipai/paperclip/tree/bd203093235b28631760a76b602b35028322e06f/packages/plugins) contains the plugin SDK, examples, sandbox providers, and bundled plugins.
- [.agents/skills](https://github.com/paperclipai/paperclip/tree/bd203093235b28631760a76b602b35028322e06f/.agents/skills) and [skills](https://github.com/paperclipai/paperclip/tree/bd203093235b28631760a76b602b35028322e06f/skills) are operational skill packs for repo maintenance and runtime connector guidance.
- [doc](https://github.com/paperclipai/paperclip/tree/bd203093235b28631760a76b602b35028322e06f/doc) is unusually important; the V1 system boundaries are specified there, not inferred from marketing copy.

## Layered architecture dissection

### High-level system shape

The outer product is a board-facing web app. [ui/src/App.tsx](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/ui/src/App.tsx) wires a large route surface: dashboard, timeline, companies, agents, projects, workspaces, issues, goals, approvals, inbox, decisions, apps, skills, secrets, plugins, profile settings, and advanced tools.

The API layer is [server/src/app.ts](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/server/src/app.ts), which imports and mounts route modules for companies, agents, projects, issues, routines, pipelines, goals, board chat, approvals, secrets, tool access, chat channels, costs, activity, dashboards, decisions, plugins, auth, cloud, and more. The route index in [server/src/routes/index.ts](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/server/src/routes/index.ts) shows the system's nouns.

The domain layer lives in services. [server/src/services/agents.ts](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/server/src/services/agents.ts) manages agent identity, adapter config, permissions, runtime config, budget fields, config revisions, secret bindings, wakeup requests, and run state. [server/src/services/heartbeat.ts](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/server/src/services/heartbeat.ts) is the busy orchestration center for waking agents, admitting continuations, resolving connectors, handling stop/recovery paths, and projecting run status.

The execution layer is outside the app's direct business model. [packages/paperclip-runner/src/backends/native-backend-factory.ts](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/packages/paperclip-runner/src/backends/native-backend-factory.ts) chooses a native backend for Codex, ACPX, or OpenCode and deliberately rejects provider kinds not included in the release slice. [packages/paperclip-runner/src/control-plane/durable-prp-control-plane.ts](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/packages/paperclip-runner/src/control-plane/durable-prp-control-plane.ts) is the durable protocol/control-plane implementation with command types like `run.prepare`, `turn.start`, `turn.steer`, `turn.stop`, `semantic_tool.result`, `session.snapshot`, `runner.suspend`, and `runner.shutdown`.

### Main layers

The monorepo layer is governed by [pnpm-workspace.yaml](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/pnpm-workspace.yaml), which includes [packages](https://github.com/paperclipai/paperclip/tree/bd203093235b28631760a76b602b35028322e06f/packages), [server](https://github.com/paperclipai/paperclip/tree/bd203093235b28631760a76b602b35028322e06f/server), [ui](https://github.com/paperclipai/paperclip/tree/bd203093235b28631760a76b602b35028322e06f/ui), and [cli](https://github.com/paperclipai/paperclip/tree/bd203093235b28631760a76b602b35028322e06f/cli). The root [package.json](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/package.json) has scripts for dev, build, typecheck, tests, migrations, releases, storybook, runner acceptance tests, smoke tests, and visual tests.

The persistence layer is [packages/db/src/index.ts](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/packages/db/src/index.ts), which exports database creation, migration inspection/application, embedded Postgres helpers, backup/restore helpers, and schema modules.

The contract layer is [packages/shared/src/index.ts](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/packages/shared/src/index.ts). It exposes validators and types for adapters, runner goals, native finalization, decisions, connection intents, and many route-level inputs.

The provider layer is [packages/adapters](https://github.com/paperclipai/paperclip/tree/bd203093235b28631760a76b602b35028322e06f/packages/adapters). The Codex adapter in [packages/adapters/codex-local/src/index.ts](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/packages/adapters/codex-local/src/index.ts) shows the pattern: identify an adapter type, define install defaults, normalize model IDs, advertise supported reasoning efforts, and keep provider quirks inside adapter code.

The plugin layer is [packages/plugins/sdk/src/index.ts](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/packages/plugins/sdk/src/index.ts), which exports `definePlugin`, `runWorker`, worker RPC host utilities, JSON-RPC helpers, test harnesses, bundler presets, and capability errors.

### Request / data / control flow

A human or CLI starts an instance through [cli/src/commands/run.ts](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/cli/src/commands/run.ts). That command resolves instance paths, loads config, runs onboarding if needed, seeds worktrees, runs doctor checks, imports the server, writes runtime info, and exposes the dashboard URL.

The browser UI calls the REST API through [ui/src/api/client.ts](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/ui/src/api/client.ts). That client sends credentials, applies non-authoritative observability headers such as tab visibility and route, handles JSON errors, and coalesces safe GETs in-tab.

When the board creates or wakes agents, routes like [server/src/routes/agents.ts](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/server/src/routes/agents.ts) validate inputs, enforce authz, resolve adapter/runtime config, apply connector skills, and call services. The heartbeat service then prepares execution context, resolves queued conversations or continuations, checks blockers, connects assigned tools, and dispatches through either legacy adapters or native runner paths.

If native execution is used, [packages/paperclip-runner/src/backends/native-backend-factory.ts](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/packages/paperclip-runner/src/backends/native-backend-factory.ts) selects the supported backend. The durable control-plane in [packages/paperclip-runner/src/control-plane/durable-prp-control-plane.ts](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/packages/paperclip-runner/src/control-plane/durable-prp-control-plane.ts) constrains commands, frame sizes, state size, leases, tickets, runner digests, and committed event windows. That is the serious part: Paperclip treats run recovery and provider attachment as protocol state, not a pile of ad hoc subprocess calls.

## Key directories and files

- [README.md](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/README.md): public product pitch and quickstart.
- [AGENTS.md](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/AGENTS.md): contributor map, setup instructions, and core engineering rules.
- [doc/GOAL.md](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/doc/GOAL.md): the cleanest statement of the control-plane versus execution-service split.
- [doc/PRODUCT.md](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/doc/PRODUCT.md): product model for companies, agents, tasks, goals, skills, and adapter configuration.
- [doc/SPEC-implementation.md](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/doc/SPEC-implementation.md): V1 implementation contract and explicit product decisions.
- [pnpm-workspace.yaml](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/pnpm-workspace.yaml): monorepo package map and pinned overrides/patches.
- [server/src/app.ts](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/server/src/app.ts): Express app assembly and route/service wiring.
- [server/src/routes/agents.ts](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/server/src/routes/agents.ts): agent lifecycle route surface.
- [server/src/services/heartbeat.ts](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/server/src/services/heartbeat.ts): core wake/run/continuation/recovery orchestration.
- [server/src/services/connector-runtime.ts](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/server/src/services/connector-runtime.ts): connector assignment and runtime-only skill overlay.
- [packages/paperclip-runner/src/backends/native-backend-factory.ts](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/packages/paperclip-runner/src/backends/native-backend-factory.ts): provider backend selection.
- [packages/paperclip-runner/src/control-plane/durable-prp-control-plane.ts](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/packages/paperclip-runner/src/control-plane/durable-prp-control-plane.ts): durable runner protocol and recovery state.
- [packages/plugins/sdk/src/index.ts](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/packages/plugins/sdk/src/index.ts): plugin worker SDK entrypoint.
- [cli/src/commands/run.ts](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/cli/src/commands/run.ts): local instance startup flow.
- [ui/src/App.tsx](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/ui/src/App.tsx): board UI route map.

## Important components

The company-scoped product model is the center. [doc/SPEC-implementation.md](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/doc/SPEC-implementation.md) explicitly chooses single-tenant deployment with a multi-company data model, strict org tree reporting, tasks/comments as the communication model, atomic task checkout, monthly UTC budgets, and board intervention.

The adapter boundary is the second key component. [packages/adapters/codex-local/src/index.ts](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/packages/adapters/codex-local/src/index.ts) is small but revealing: provider defaults, model normalization, reasoning-effort menus, and install commands live in adapter packages rather than being scattered across UI and services.

The native runner protocol is the third key component. [packages/paperclip-runner/src/control-plane/durable-prp-control-plane.ts](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/packages/paperclip-runner/src/control-plane/durable-prp-control-plane.ts) includes protocol versions, secure-frame schema, max command sizes, lease records, bootstrap tickets, committed events, runner digest validation, and command allowlists. That is a real attempt at durable execution semantics.

The connector runtime in [server/src/services/connector-runtime.ts](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/server/src/services/connector-runtime.ts) is also worth copying. Connectors declare trusted tool contributions, resolve assigned resources, execute governed calls, and inject connector skills as a runtime-only overlay instead of persisting automatic assignments into agent preferences.

## Important knobs / configs / extension points

The main operational knobs are in [package.json](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/package.json): dev runners, DB migration commands, typechecking, runner acceptance tests, smoke tests, e2e tests, release scripts, and token/security checks.

The workspace extension map is [pnpm-workspace.yaml](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/pnpm-workspace.yaml). New packages fit into the existing app, adapters, plugins, and examples layout.

The agent runtime extension point is [packages/adapters](https://github.com/paperclipai/paperclip/tree/bd203093235b28631760a76b602b35028322e06f/packages/adapters), plus the backend selection in [packages/paperclip-runner/src/backends/native-backend-factory.ts](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/packages/paperclip-runner/src/backends/native-backend-factory.ts).

The plugin extension point is [packages/plugins/sdk/src/index.ts](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/packages/plugins/sdk/src/index.ts), backed by plugin examples and sandbox providers under [packages/plugins](https://github.com/paperclipai/paperclip/tree/bd203093235b28631760a76b602b35028322e06f/packages/plugins).

The connector extension point is the definition table in [server/src/services/connector-runtime.ts](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/server/src/services/connector-runtime.ts), where each connector supplies a key, label, skill name, tools, resolver, and executor.

## Practical questions and answers

Q: Is Paperclip an agent runtime?
A: Not primarily. [doc/GOAL.md](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/doc/GOAL.md) says Paperclip orchestrates while agents run wherever they run and phone home.

Q: Where is the product's center of gravity?
A: In the company/task/agent model described by [doc/PRODUCT.md](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/doc/PRODUCT.md) and implemented through [server/src/routes](https://github.com/paperclipai/paperclip/tree/bd203093235b28631760a76b602b35028322e06f/server/src/routes) plus [server/src/services](https://github.com/paperclipai/paperclip/tree/bd203093235b28631760a76b602b35028322e06f/server/src/services).

Q: What is the cleverest mechanism?
A: The durable native runner layer. [packages/paperclip-runner/src/control-plane/durable-prp-control-plane.ts](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/packages/paperclip-runner/src/control-plane/durable-prp-control-plane.ts) treats sessions, turns, receipts, snapshots, budget changes, and shutdown as protocol commands with recovery state.

Q: Where would this be hardest to maintain?
A: The cross-cutting route/service surface. [server/src/app.ts](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/server/src/app.ts) and [server/src/services](https://github.com/paperclipai/paperclip/tree/bd203093235b28631760a76b602b35028322e06f/server/src/services) show a very large feature matrix, so boundaries and tests have to stay disciplined.

Q: What would I copy first?
A: The explicit "control plane, not execution plane" split from [doc/GOAL.md](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/doc/GOAL.md), then the adapter/provider boundary from [packages/adapters](https://github.com/paperclipai/paperclip/tree/bd203093235b28631760a76b602b35028322e06f/packages/adapters) and [packages/paperclip-runner](https://github.com/paperclipai/paperclip/tree/bd203093235b28631760a76b602b35028322e06f/packages/paperclip-runner).

## What is smart

The repo starts from governance, not chat. Companies, goals, org charts, budgets, approvals, and issues are first-class. That is a better mental model for durable autonomous work than "a room full of agents talking."

The adapter strategy is healthy. [packages/adapters](https://github.com/paperclipai/paperclip/tree/bd203093235b28631760a76b602b35028322e06f/packages/adapters) keeps provider assumptions out of the core product, while [packages/paperclip-runner/src/backends/native-backend-factory.ts](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/packages/paperclip-runner/src/backends/native-backend-factory.ts) refuses to execute future provider kinds before their reviewed runtime ships.

The connector runtime is careful. [server/src/services/connector-runtime.ts](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/server/src/services/connector-runtime.ts) treats resource assignments as data that are checked on every call, not as permanent agent-authored authority.

The UI/API client has practical polish. [ui/src/api/client.ts](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/ui/src/api/client.ts) includes tab visibility hints, route hints, tenant-session recovery, and in-tab GET coalescing. That is not glamorous, but it matters in a live operations surface.

## What is flawed or weak

The surface area is enormous. The route list in [server/src/routes](https://github.com/paperclipai/paperclip/tree/bd203093235b28631760a76b602b35028322e06f/server/src/routes) and service list in [server/src/services](https://github.com/paperclipai/paperclip/tree/bd203093235b28631760a76b602b35028322e06f/server/src/services) are a strength if they are well tested, but also a maintenance hazard.

The product pitch in [README.md](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/README.md) is much simpler than the implementation reality. A new builder might expect a small app and instead find a complex control plane with runners, plugins, connectors, secrets, auth modes, and recovery protocols.

The plugin framework is promising but appears intentionally early/local in [doc/SPEC-implementation.md](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/doc/SPEC-implementation.md), which says cloud marketplace and packaged public distribution are out of V1 scope. Builders should evaluate it as a local/self-hosted extension layer first.

## What we can learn / steal

Steal the noun model: company, goal, agent, issue, comment, approval, budget, run, adapter, connector. It is much easier to govern agents when the control plane has concrete business objects.

Steal the provider boundary from [packages/adapters](https://github.com/paperclipai/paperclip/tree/bd203093235b28631760a76b602b35028322e06f/packages/adapters). Do not let provider-specific defaults and capabilities leak everywhere.

Steal the runtime-only connector overlay pattern from [server/src/services/connector-runtime.ts](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/server/src/services/connector-runtime.ts). Tool access should be derived from current assignments and rechecked on execution.

Steal the durable command vocabulary from [packages/paperclip-runner/src/control-plane/durable-prp-control-plane.ts](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/packages/paperclip-runner/src/control-plane/durable-prp-control-plane.ts): prepare, attach, open, start, steer, interrupt, stop, resolve request, receive semantic result, snapshot, set goal, increase budget, cancel, drain, suspend, shutdown.

## How we could apply it

For any serious agent product, start with the control plane data model before choosing model prompts. Define the equivalent of [doc/PRODUCT.md](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/doc/PRODUCT.md): who owns work, what goals it serves, how runs are invoked, where cost is tracked, and how humans intervene.

If building a multi-provider agent platform, put all provider quirks behind an adapter package like [packages/adapters/codex-local/src/index.ts](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/packages/adapters/codex-local/src/index.ts), then put durable execution semantics in a runner protocol layer like [packages/paperclip-runner](https://github.com/paperclipai/paperclip/tree/bd203093235b28631760a76b602b35028322e06f/packages/paperclip-runner).

If adding tool connectors, copy the reauthorization-on-call idea from [server/src/services/connector-runtime.ts](https://github.com/paperclipai/paperclip/blob/bd203093235b28631760a76b602b35028322e06f/server/src/services/connector-runtime.ts) instead of handing agents permanent tool bundles.

## Bottom line

Paperclip is worth studying because it treats agent orchestration as an operations and governance problem. The repo is big and still carries early-platform complexity, but its core shape is right: durable business objects, provider adapters, protocolized runner control, scoped connectors, and a board UI that can watch and intervene.
