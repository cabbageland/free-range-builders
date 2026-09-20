# Agent-Native

- Repo: BuilderIO/agent-native
- URL: https://github.com/BuilderIO/agent-native
- Date: 2026-09-20
- Repo snapshot studied: main at `d4744015ee6d89155c2f4e49d00dc2f1a95a150d`
- Why picked today: It was high on the daily GitHub trending page, it was not one of yesterday's picks, and it has a real source surface behind the pitch: framework core, action routing, agent protocol, templates, skills, browser/desktop extensions, and product examples.

## Executive summary

[BuilderIO/agent-native](https://github.com/BuilderIO/agent-native) is a TypeScript framework for building applications where the agent and the UI share the same capabilities. The headline in [README.md](https://github.com/BuilderIO/agent-native/blob/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/README.md) is simple: define each capability once as an action, then let both the agent and the UI call it. The source tree backs that up. [packages/core/](https://github.com/BuilderIO/agent-native/tree/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/core) owns actions, auth, SQL-facing state, agent execution, HTTP routes, MCP/A2A exposure, Vite integration, and templates. [packages/agentkit/](https://github.com/BuilderIO/agent-native/tree/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/agentkit) owns the portable agent interaction protocol and React bindings. [packages/toolkit/](https://github.com/BuilderIO/agent-native/tree/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/toolkit) owns the UI primitives and product surfaces.

The useful builder lesson is that Agent-Native refuses to make the agent a browser-clicking visitor inside the app. [packages/core/src/action.ts](https://github.com/BuilderIO/agent-native/blob/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/core/src/action.ts) models each action with schema, caller context, access controls, audit hooks, approvals, and caller attribution. [packages/core/src/server/action-routes.ts](https://github.com/BuilderIO/agent-native/blob/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/core/src/server/action-routes.ts) projects those same actions onto HTTP routes. [packages/core/src/server/action-discovery.ts](https://github.com/BuilderIO/agent-native/blob/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/core/src/server/action-discovery.ts) discovers local and package-contributed actions. [packages/core/src/vite/action-types-plugin.ts](https://github.com/BuilderIO/agent-native/blob/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/core/src/vite/action-types-plugin.ts) generates type-safe client bindings and static server registries so serverless bundles do not lose action files.

## What they built

Agent-Native is an app framework, not only a chat widget. It gives builders a way to ship task-specific agent products where the user can inspect, edit, approve, and share agent work in a normal UI. The root [package.json](https://github.com/BuilderIO/agent-native/blob/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/package.json) shows a large monorepo with workspace scripts for build, typecheck, guard suites, template audits, release automation, e2e tests, and smoke checks.

The heart of the system is the action abstraction. The example in [README.md](https://github.com/BuilderIO/agent-native/blob/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/README.md) defines an action with `defineAction`, a Zod schema, an optional HTTP method, and a `run` implementation. The same named action becomes an agent tool, a React `useActionQuery` or `useActionMutation` target, an HTTP endpoint, an MCP tool, an A2A operation, and a CLI-callable command.

Around that core, the repo ships starter apps under [templates/](https://github.com/BuilderIO/agent-native/tree/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/templates), reusable skills under [skills/](https://github.com/BuilderIO/agent-native/tree/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/skills), packaged product surfaces under [packages/](https://github.com/BuilderIO/agent-native/tree/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages), MCP registry material under [mcp-registry/](https://github.com/BuilderIO/agent-native/tree/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/mcp-registry), and open-source example agents under [community-templates/](https://github.com/BuilderIO/agent-native/tree/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/community-templates).

## Why it matters

Most agent apps split into two awkward halves: a chat backend that can do work, and a UI that can display or edit state. That creates duplicate permissions, duplicate validation, duplicate transport code, and a fuzzy boundary where the agent may be tempted to drive the product by clicking. Agent-Native's action layer is a cleaner contract: the agent and the UI both call named capabilities through the same schema and authorization path.

That matters because knowledge-work agents need product surfaces. The user does not only want a final paragraph; they want review threads, database rows, calendar events, drafts, assets, visual plans, approvals, and history. The package list under [packages/core/src/](https://github.com/BuilderIO/agent-native/tree/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/core/src) shows the product concerns this framework is trying to standardize: sharing, reviews, notifications, jobs, feature flags, MCP actions, user profiles, workspace connections, upload flows, org access, triggers, and usage metering.

The project is also interesting because it treats agent UI as a protocol layer. [packages/agentkit/ARCHITECTURE.md](https://github.com/BuilderIO/agent-native/blob/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/agentkit/ARCHITECTURE.md) explicitly separates Agent-Native Core, AgentKit, and Toolkit. Core owns execution and durable truth. AgentKit owns portable conversation events, validation, transports, client state, and React composition. Toolkit owns semantic UI pieces.

## Repo shape at a glance

- [README.md](https://github.com/BuilderIO/agent-native/blob/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/README.md) explains the shared-action thesis and lists open-source app examples.
- [package.json](https://github.com/BuilderIO/agent-native/blob/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/package.json) shows a pnpm monorepo with extensive guard, QA, release, template, and e2e scripts.
- [packages/core/](https://github.com/BuilderIO/agent-native/tree/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/core) is the main framework runtime: actions, server routes, auth, data, jobs, agent chat, MCP/A2A, templates, Vite plugins, and generated registries.
- [packages/agentkit/](https://github.com/BuilderIO/agent-native/tree/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/agentkit) is the portable agent interaction package with protocol, adapters, client state, conformance tests, and React bindings.
- [packages/toolkit/](https://github.com/BuilderIO/agent-native/tree/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/toolkit) contains UI primitives, composer pieces, data grids, dashboards, design-system adapters, editor components, sharing primitives, and workspace UI.
- [templates/](https://github.com/BuilderIO/agent-native/tree/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/templates) contains many starter apps: chat, calendar, clips, content, CRM, design, dispatch, forms, mail, plan, slides, tasks, videos, and more.
- [skills/](https://github.com/BuilderIO/agent-native/tree/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/skills) contains reusable agent skills such as [skills/turn-into-app/SKILL.md](https://github.com/BuilderIO/agent-native/blob/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/skills/turn-into-app/SKILL.md), [skills/visual-edit/SKILL.md](https://github.com/BuilderIO/agent-native/blob/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/skills/visual-edit/SKILL.md), and [skills/context-xray/SKILL.md](https://github.com/BuilderIO/agent-native/blob/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/skills/context-xray/SKILL.md).
- [registry/](https://github.com/BuilderIO/agent-native/tree/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/registry) and [mcp-registry/](https://github.com/BuilderIO/agent-native/tree/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/mcp-registry) show that external agent/app discovery is a first-class concern.
- [packages/vscode-extension/](https://github.com/BuilderIO/agent-native/tree/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/vscode-extension), [packages/desktop-app/](https://github.com/BuilderIO/agent-native/tree/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/desktop-app), [packages/agent-browser-extension/](https://github.com/BuilderIO/agent-native/tree/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/agent-browser-extension), and [packages/agent-chrome-extension/](https://github.com/BuilderIO/agent-native/tree/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/agent-chrome-extension) show multiple host surfaces beyond a web app.

## Layered architecture dissection

### High-level system shape

Agent-Native has four main layers. The product app layer is a React/Nitro style application created from a template. The action layer is the shared capability boundary between agent, UI, HTTP, MCP, A2A, CLI, and automations. The agent interaction layer is AgentKit, which turns backend runs into a versioned event stream and React/headless state. The toolkit layer provides reusable UI primitives and workspace components.

The key design choice is that the agent does not operate by screen scraping the UI. It calls the same action layer the UI uses. That gives the product one place to validate input, enforce access, attribute caller identity, write audit records, and decide what is safe for autonomous execution.

### Main layers

The action contract is centered in [packages/core/src/action.ts](https://github.com/BuilderIO/agent-native/blob/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/core/src/action.ts). `ActionCaller` distinguishes `tool`, `http`, `frontend`, `cli`, `mcp`, `webmcp`, `a2a`, and `automation`. `ActionRunContext` carries user email, org id, app roles, app permissions, request headers, automation lineage, network lineage, attachments, abort signal, thread/run ids, and approval metadata. That is a serious context object, not a demo callback.

The HTTP/action route layer is [packages/core/src/server/action-routes.ts](https://github.com/BuilderIO/agent-native/blob/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/core/src/server/action-routes.ts). It mounts actions under `/_agent-native/actions`, parses query/body arguments, handles CORS and embed origins, resolves caller identity, tags frontend requests, and applies action validation/authorization before calling the action.

The discovery and bundling layer is split between [packages/core/src/server/action-discovery.ts](https://github.com/BuilderIO/agent-native/blob/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/core/src/server/action-discovery.ts) and [packages/core/src/vite/action-types-plugin.ts](https://github.com/BuilderIO/agent-native/blob/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/core/src/vite/action-types-plugin.ts). Discovery scans app action files, supports legacy CLI-style default exports, preserves action flags, and merges package-contributed actions. The Vite plugin generates `.generated/action-types.d.ts` and `.generated/actions-registry.ts`, a practical fix for serverless bundles where dynamic filesystem discovery would otherwise 404 every action.

The protocol/UI interaction layer is [packages/agentkit/](https://github.com/BuilderIO/agent-native/tree/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/agentkit). [packages/agentkit/ARCHITECTURE.md](https://github.com/BuilderIO/agent-native/blob/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/agentkit/ARCHITECTURE.md) says events are append-only, ordered, replayable, explicitly terminal, and reconnectable by sequence. It also insists that AgentKit does not own app data, authorization policy, persistence, or agent execution. That restraint is good engineering.

The template and product layer is [templates/](https://github.com/BuilderIO/agent-native/tree/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/templates) plus [packages/core/src/templates/](https://github.com/BuilderIO/agent-native/tree/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/core/src/templates). Template files such as [templates/chat/agent-native.json](https://github.com/BuilderIO/agent-native/blob/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/templates/chat/agent-native.json) and [packages/core/src/templates/default/actions/hello.ts](https://github.com/BuilderIO/agent-native/blob/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/core/src/templates/default/actions/hello.ts) show the generated-app shape.

### Request / data / control flow

A builder writes an action file using `defineAction` in an app's `actions/` directory. During development and build, [packages/core/src/vite/action-types-plugin.ts](https://github.com/BuilderIO/agent-native/blob/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/core/src/vite/action-types-plugin.ts) discovers those files, generates TypeScript client types, and creates a static action registry for the server bundle.

At runtime, [packages/core/src/server/action-discovery.ts](https://github.com/BuilderIO/agent-native/blob/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/core/src/server/action-discovery.ts) combines local actions and package-contributed actions. [packages/core/src/server/action-routes.ts](https://github.com/BuilderIO/agent-native/blob/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/core/src/server/action-routes.ts) exposes eligible actions through HTTP, while the agent loop exposes eligible actions as tools. The UI calls the same named action through typed client hooks, and AgentKit widgets call stable action identifiers through `AgentTransport.invokeAction`.

The action implementation receives [ActionRunContext](https://github.com/BuilderIO/agent-native/blob/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/core/src/action.ts). It can branch on `ctx.caller`, check auth/access, use request identity, emit streaming events during a tool call, observe an abort signal, and attach audit metadata. If it mutates shared state, the change can be surfaced back into UI and agent context through the same product state layer.

## Key directories and files

- [packages/core/src/action.ts](https://github.com/BuilderIO/agent-native/blob/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/core/src/action.ts) is the core action contract, caller taxonomy, context, and safe failure machinery.
- [packages/core/src/server/action-routes.ts](https://github.com/BuilderIO/agent-native/blob/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/core/src/server/action-routes.ts) turns actions into HTTP endpoints and handles identity, CORS, route parsing, and invocation.
- [packages/core/src/server/action-discovery.ts](https://github.com/BuilderIO/agent-native/blob/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/core/src/server/action-discovery.ts) discovers app/package actions and supports old CLI-style actions.
- [packages/core/src/vite/action-types-plugin.ts](https://github.com/BuilderIO/agent-native/blob/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/core/src/vite/action-types-plugin.ts) generates client action types and a static server registry.
- [packages/agentkit/ARCHITECTURE.md](https://github.com/BuilderIO/agent-native/blob/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/agentkit/ARCHITECTURE.md) explains ownership boundaries and protocol invariants.
- [packages/agentkit/src/protocol/](https://github.com/BuilderIO/agent-native/tree/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/agentkit/src/protocol) contains protocol validation, compatibility, and event/result types.
- [packages/agentkit/src/client/](https://github.com/BuilderIO/agent-native/tree/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/agentkit/src/client) contains headless client state and transport handling.
- [packages/agentkit/src/react/](https://github.com/BuilderIO/agent-native/tree/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/agentkit/src/react) contains React bindings and chat/composition pieces.
- [packages/toolkit/src/composer/](https://github.com/BuilderIO/agent-native/tree/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/toolkit/src/composer) and [packages/toolkit/src/editor/](https://github.com/BuilderIO/agent-native/tree/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/toolkit/src/editor) show the reusable UI layer.
- [packages/core/src/templates/default/](https://github.com/BuilderIO/agent-native/tree/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/core/src/templates/default) is the default generated app template.
- [templates/design/](https://github.com/BuilderIO/agent-native/tree/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/templates/design), [templates/content/](https://github.com/BuilderIO/agent-native/tree/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/templates/content), and [templates/calendar/](https://github.com/BuilderIO/agent-native/tree/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/templates/calendar) are concrete product templates rather than docs-only examples.

## Important components

`defineAction` is the central component, even though the repository is much larger than that helper. It is where app capability becomes a durable product surface. The surrounding pieces in [packages/core/src/action.ts](https://github.com/BuilderIO/agent-native/blob/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/core/src/action.ts) make actions aware of authorization, caller type, audit, approval, external exposure, read-only status, and tool availability.

`ActionRunContext` is a strong design move. Many frameworks pass only `{ args }`; Agent-Native passes identity, org/app scope, caller source, attachments, abort signal, automation lineage, network lineage, and agent run metadata. That makes it possible to write actions that are safe across UI, tool, HTTP, automation, and external agent callers.

`action-types-plugin` is less glamorous but very practical. The comment in [packages/core/src/vite/action-types-plugin.ts](https://github.com/BuilderIO/agent-native/blob/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/core/src/vite/action-types-plugin.ts) names the serverless bundling problem directly: without static imports, dynamic action discovery sees no files inside a bundled server function. The generated registry is an operational fix.

`AgentKit` is the separable protocol package. The invariants in [packages/agentkit/ARCHITECTURE.md](https://github.com/BuilderIO/agent-native/blob/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/agentkit/ARCHITECTURE.md) cover replay, reconnect, terminal events, binary uploads, approvals, smart objects, and controller ownership. This is the right level of rigor for a UI layer that may be backed by multiple runtimes.

## Important knobs / configs / extension points

- `http` on an action controls whether it is exposed as POST, GET, or not exposed through HTTP. The behavior is documented in [packages/core/src/server/action-routes.ts](https://github.com/BuilderIO/agent-native/blob/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/core/src/server/action-routes.ts).
- `caller` in [ActionRunContext](https://github.com/BuilderIO/agent-native/blob/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/core/src/action.ts) lets an action treat frontend, tool, MCP, A2A, CLI, and automation calls differently when necessary.
- Action flags preserved by [action-discovery.ts](https://github.com/BuilderIO/agent-native/blob/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/core/src/server/action-discovery.ts) include access, `agentTool`, `mcpTool`, `requiresAuth`, `uiOnly`, `readOnly`, `parallelSafe`, `endsTurn`, `dedupe`, and capability scopes.
- [agent-native.json](https://github.com/BuilderIO/agent-native/blob/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/templates/chat/agent-native.json) is the generated app manifest surface.
- [packages/core/src/vite/agent-native-config-loader.ts](https://github.com/BuilderIO/agent-native/blob/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/core/src/vite/agent-native-config-loader.ts) is where app config loading plugs into the Vite side.
- [packages/agentkit/src/adapters/http.ts](https://github.com/BuilderIO/agent-native/blob/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/agentkit/src/adapters/http.ts) is the transport adapter extension point for AgentKit-style runtimes.

## Practical questions and answers

Q: Is this just a chat UI library?

A: No. [packages/agentkit/](https://github.com/BuilderIO/agent-native/tree/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/agentkit) is the chat/protocol layer, but [packages/core/](https://github.com/BuilderIO/agent-native/tree/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/core) owns actions, auth, data, jobs, sharing, review, MCP/A2A, and server routes. The repo is closer to an app framework for agent products.

Q: Where is the real abstraction?

A: The real abstraction is named actions. The same action can be called by the agent, the UI, HTTP, CLI, MCP, A2A, and automations. That is visible in [packages/core/src/action.ts](https://github.com/BuilderIO/agent-native/blob/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/core/src/action.ts) and [packages/core/src/server/action-routes.ts](https://github.com/BuilderIO/agent-native/blob/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/core/src/server/action-routes.ts).

Q: How does it avoid losing action files in serverless deployments?

A: It does not rely only on runtime filesystem scanning. [packages/core/src/vite/action-types-plugin.ts](https://github.com/BuilderIO/agent-native/blob/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/core/src/vite/action-types-plugin.ts) generates a static action registry module with imports that bundlers can see.

Q: What would be hard to adopt?

A: The monorepo is huge and opinionated. A team that only needs a thin action SDK may find [packages/core/](https://github.com/BuilderIO/agent-native/tree/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/core), [packages/toolkit/](https://github.com/BuilderIO/agent-native/tree/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/toolkit), templates, skills, extension packages, and guard scripts to be more platform than library.

## What is smart

The smartest move is collapsing UI and agent capability into one action contract. This prevents a slow drift where the UI validates one shape, the agent tool validates another shape, and the backend quietly accepts a third shape.

The second smart move is caller attribution. A `delete-customer` style action can know whether it came from a human UI click, an agent tool call, MCP, A2A, or automation. That is essential for approvals, audit, and different safety policies.

The third smart move is the AgentKit boundary. [packages/agentkit/ARCHITECTURE.md](https://github.com/BuilderIO/agent-native/blob/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/agentkit/ARCHITECTURE.md) does not pretend a UI package can own persistence, authorization, tenancy, or agent execution. It owns protocol and projection.

## What is flawed or weak

The repo is broad enough to be intimidating. The first `find` pass shows more than templates and core packages: extensions, mobile app, desktop app, dispatch, creative context, docs, migrations, scheduling, registry, and many guard scripts. That breadth is a strength for a platform but a weakness for a builder evaluating the minimal concept.

The action abstraction also creates a trap: if teams put too much business logic in UI-only routes instead of actions, they lose the framework's main benefit. The generated skills under [packages/core/src/templates/workspace-core/.claude/skills/](https://github.com/BuilderIO/agent-native/tree/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/core/src/templates/workspace-core/.claude/skills) repeatedly teach "put normal app data through actions," which suggests the authors know this is a behavior they must enforce culturally and with guards.

Finally, a shared action layer does not make security automatic. [packages/agentkit/ARCHITECTURE.md](https://github.com/BuilderIO/agent-native/blob/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/agentkit/ARCHITECTURE.md) is explicit that thread ids, run ids, action ids, widget payloads, and smart objects are not authorization grants. The host still has to do the hard auth and data scoping work.

## What we can learn / steal

Steal the named-action contract. Any agent product with a UI should define work as first-class backend capabilities that both humans and agents call. Do not let the agent drive hidden browser flows unless the UI is itself the target of the work.

Steal caller attribution. Every capability should know whether it was called by a user, an agent, automation, an external network, or a CLI. That single field makes audit, approval, rate limiting, and safety much easier.

Steal the static registry trick. If a system discovers plugin/action files dynamically in development, it still needs a bundle-visible registry for serverless production.

Steal the AgentKit ownership split. Keep runtime execution, durable state, protocol events, and React presentation separate enough that one layer can change without turning the whole product into a knot.

## How we could apply it

For our own agent apps, start with a small action manifest: reads marked GET/read-only, mutations marked POST, risky mutations requiring approval, and every action receiving a context with caller, user, org, app, and run id. Then generate client hooks and agent tools from that one manifest.

For multi-agent UI, borrow the AgentKit idea of append-only ordered events, durable snapshots, explicit terminal states, and no duplicate controller owners. This would prevent many "chat stream says one thing, UI state says another" bugs.

For app templates, copy the shape of [packages/core/src/templates/default/](https://github.com/BuilderIO/agent-native/tree/d4744015ee6d89155c2f4e49d00dc2f1a95a150d/packages/core/src/templates/default): ship example actions, a manifest, dev docs, app shell, and tests together so builders learn the framework by modifying a working product, not by wiring ten empty packages.

## Bottom line

Agent-Native is worth studying because it treats agents as product participants, not chatbots bolted onto product pages. Its best idea is simple and durable: a capability should be one action with one schema, one authorization path, one audit story, and multiple surfaces.
